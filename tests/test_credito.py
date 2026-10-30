"""Pruebas del MVP Flujo de crédito preaprobado (REQ-MVP-01 a 03, trabajos/mi-proceso/14-mvp). Datos SINTÉTICOS."""
from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.camunda import CamundaError

TIPOS = ["IDENTIDAD", "INGRESOS", "ESTADO_CUENTA", "PAGARE"]

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'credito.sqlite3'}")
    monkeypatch.setenv("ENGINE_MODE", "mock")
    with TestClient(app) as c: yield c

class FakeCamunda:
    """Doble de CamundaClient para probar CAM-4 sin red ni clúster real (incluye lo que usa el
    trabajador automático, aunque estas pruebas no dependen de él: no hay trabajos reales pendientes)."""
    def __init__(self):
        self.iniciadas, self.mensajes, self.completadas = [], [], []
        self._contador, self._tareas = 1000, {}

    def start(self, process_id, variables):
        self._contador += 1
        self.iniciadas.append((process_id, dict(variables)))
        return {"processInstanceKey": self._contador}

    def tasks(self, instance_key): return self._tareas.get(str(instance_key), [])

    def complete(self, key, variables): self.completadas.append((key, dict(variables)))

    def publish_message(self, name, correlation_key, variables=None, ttl_ms=60000):
        self.mensajes.append((name, correlation_key, dict(variables or {})))

    def activate_jobs(self, job_type, max_jobs=10, timeout_ms=10000, worker="credito-mvp"): return []
    def complete_job(self, job_key, variables=None): pass

    def agregar_tarea(self, instance_key, element_id, task_key):
        self._tareas.setdefault(str(instance_key), []).append(
            {"elementId": element_id, "userTaskKey": task_key, "state": "CREATED"})

@pytest.fixture()
def client_camunda(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'credito_camunda.sqlite3'}")
    monkeypatch.setenv("ENGINE_MODE", "camunda")
    fake = FakeCamunda()
    # Sustituye la clase real ANTES de levantar la app: el trabajador automático del lifespan
    # arranca con app.state.camunda, así que nunca debe tocar la red real durante las pruebas.
    monkeypatch.setattr("app.main.CamundaClient", lambda: fake)
    with TestClient(app) as c:
        c.fake = fake
        yield c

def doc(tipo, dias=5, legible=True, cedula="001-0000001-1"):
    d = {"tipo": tipo, "fecha_expedicion": (date.today() - timedelta(days=dias)).isoformat(), "legible": legible,
         "nombre": "Cliente Demo"}
    if tipo in ("IDENTIDAD", "PAGARE"): d["cedula"] = cedula
    if tipo == "INGRESOS": d["salario"] = 45000
    if tipo == "PAGARE": d["monto"] = 350000
    return d

def nuevo(client):
    r = client.post("/api/credito/casos", json={"cliente_alias": "Cliente Demo", "correo_cliente": "demo@ejemplo.test", "monto": 350000})
    assert r.status_code == 201, r.text
    return r.json()

def tareas(client, rol): return client.get(f"/api/credito/tareas?rol={rol}").json()

def completar(client, key, **body): return client.post(f"/api/credito/tareas/{key}/completar", json={"actor": "demo", **body})

def test_id_formato_y_enlace(client):
    c = nuevo(client)
    assert c["id_solicitud"].startswith("SOL-9") and len(c["id_solicitud"]) == 9
    assert c["estado"] == "ENLACE_ENVIADO" and c["fuente_datos"] == "SINTETICO"
    assert [t["elementId"] for t in tareas(client, "cliente")] == ["CL_CARGAR"]
    assert client.get(f"/api/credito/casos/{c['id']}/bitacora").json()[0]["tarea"] == "TB_SND_ENLACE"

def test_req01_documentos_validos_van_a_despacho(client):
    c = nuevo(client)
    r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS])
    assert r.status_code == 200, r.text
    assert r.json()["estado"] == "VERIFICACION_DESPACHO"
    assert all(d["intentos"] == 0 for d in r.json()["documentos"])
    assert tareas(client, "legal") == []

def test_req01_vencido_cuenta_intento_y_solo_se_sube_el_rechazado(client):
    c = nuevo(client)
    docs = [doc(t) for t in TIPOS[:3]] + [doc("PAGARE", dias=25)]
    r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=docs)
    assert r.status_code == 422
    rech = {d["tipo"]: d for d in r.json()["documentos"]}
    assert rech["PAGARE"]["motivo_rechazo"] == "vencido (> 20 días)" and rech["PAGARE"]["intentos"] == 1
    assert rech["IDENTIDAD"]["estado"] == "VALIDO"
    # volver a subir un documento ya válido no se permite (DAT-2b)
    assert client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("IDENTIDAD")]).status_code == 409
    ok = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE")])
    assert ok.status_code == 200 and ok.json()["estado"] == "VERIFICACION_DESPACHO"

def test_req01_falta_documento_e_ilegible(client):
    c = nuevo(client)
    r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("IDENTIDAD"), doc("INGRESOS", legible=False)])
    rech = {d["tipo"]: d for d in r.json()["documentos"]}
    assert r.status_code == 422
    assert rech["INGRESOS"]["motivo_rechazo"] == "ilegible"
    assert rech["PAGARE"]["motivo_rechazo"] == "falta" and rech["PAGARE"]["intentos"] == 1

def test_req01_cinco_intentos_y_sexto_bloqueado(client):
    c = nuevo(client)
    validos = [doc(t) for t in TIPOS[:3]]
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=validos + [doc("PAGARE", dias=30)])
    for _ in range(4):
        r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE", dias=30)])
    assert r.json()["estado"] == "RUTA_PAPEL"
    assert {d["tipo"]: d for d in r.json()["documentos"]}["PAGARE"]["estado"] == "AGOTADO"
    sexto = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE")])
    assert sexto.status_code == 409 and "intentos agotados" in sexto.json()["detail"]

def test_req02_caso_dudoso_va_a_legal(client):
    c = nuevo(client)
    docs = [doc(t) for t in TIPOS[:3]] + [doc("PAGARE", cedula="002-9999999-9")]
    r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=docs)
    assert r.json()["estado"] == "REVISION_LEGAL" and r.json()["caso_dudoso"] is True
    assert tareas(client, "despacho") == []
    t = tareas(client, "legal")
    assert t[0]["elementId"] == "TB_ACT_REVISAR"
    assert completar(client, t[0]["key"], resultado="ACEPTA").status_code == 200
    assert completar(client, t[0]["key"], resultado="ACEPTA").status_code == 409  # doble clic
    assert [x["elementId"] for x in tareas(client, "despacho")] == ["TB_ACT_VERIF"]

def test_req02_legal_rechaza_pasa_a_papel(client):
    c = nuevo(client)
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS[:3]] + [doc("PAGARE", cedula="X")])
    r = completar(client, tareas(client, "legal")[0]["key"], resultado="RECHAZA")
    assert r.json()["caso"]["estado"] == "RUTA_PAPEL"
    assert tareas(client, "despacho") == []

def test_req03_despacho_verifica_y_csv(client):
    c = nuevo(client)
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS])
    key = tareas(client, "despacho")[0]["key"]
    assert completar(client, key).status_code == 422  # sin resultado
    assert completar(client, key, resultado="ACEPTA").status_code == 422  # resultado de otro rol
    r = completar(client, key, resultado="OK")
    assert r.json()["caso"]["estado"] == "VERIFICADO" and r.json()["caso"]["verificado_en"]
    acciones = [e["accion"] for e in client.get(f"/api/credito/casos/{c['id']}/bitacora").json()]
    assert acciones[-1] == "EXPEDIENTE_VERIFICADO"
    csv_casos = client.get("/api/credito/export/casos.csv").text
    assert "correo_cliente" in csv_casos.splitlines()[0] and "SINTETICO" in csv_casos
    assert "EXPEDIENTE_VERIFICADO" in client.get("/api/credito/export/eventos.csv").text
    assert "PAGARE" in client.get("/api/credito/export/documentos.csv").text

def test_req03_despacho_pide_correccion(client):
    c = nuevo(client)
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS])
    key = tareas(client, "despacho")[0]["key"]
    assert completar(client, key, resultado="CORREGIR").status_code == 422  # falta documento
    r = completar(client, key, resultado="CORREGIR", documento="INGRESOS", observacion="Comprobante cortado")
    assert r.json()["caso"]["estado"] == "ESPERANDO_CORRECCION" and not r.json()["caso"]["verificado_en"]
    assert [t["elementId"] for t in tareas(client, "cliente")] == ["CL_CARGAR"]
    ok = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("INGRESOS")])
    assert ok.json()["estado"] == "VERIFICACION_DESPACHO"

def test_entradas_invalidas(client):
    assert client.post("/api/credito/casos", json={"cliente_alias": "X", "correo_cliente": "no-es-correo", "monto": 1}).status_code == 422
    assert client.post("/api/credito/casos", json={"cliente_alias": "Cliente", "correo_cliente": "a@b.test", "monto": 0}).status_code == 422
    c = nuevo(client)
    futuro = doc("IDENTIDAD", dias=-3)
    r = client.post(f"/api/credito/casos/{c['id']}/documentos", json=[futuro])
    assert {d["tipo"]: d for d in r.json()["documentos"]}["IDENTIDAD"]["motivo_rechazo"] == "fecha futura"
    assert client.post("/api/credito/casos/9999/documentos", json=[doc("IDENTIDAD")]).status_code == 404
    assert completar(client, "cred-9999-legal-0", resultado="ACEPTA").status_code == 404


def estado(client, id_solicitud): return client.get(f"/api/credito/estado/{id_solicitud}")

def test_inc1_hitos_visibles_para_el_cliente(client):
    c = nuevo(client)
    sol = c["id_solicitud"]
    r = estado(client, sol)
    assert r.status_code == 200 and set(r.json()) == {"id_solicitud", "hito", "actualizado_en"}
    assert r.json()["hito"] == "Enlace enviado"
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS[:3]])
    assert estado(client, sol).json()["hito"] == "Documentos con observaciones"
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE", cedula="002-9999999-9")])
    assert estado(client, sol.lower()).json()["hito"] == "En revisión"
    completar(client, tareas(client, "legal")[0]["key"], resultado="ACEPTA")
    assert estado(client, sol).json()["hito"] == "En verificación"
    completar(client, tareas(client, "despacho")[0]["key"], resultado="OK")
    assert estado(client, sol).json()["hito"] == "Expediente verificado"
    limpio = nuevo(client)
    client.post(f"/api/credito/casos/{limpio['id']}/documentos", json=[doc(t) for t in TIPOS])
    completar(client, tareas(client, "despacho")[0]["key"], resultado="CORREGIR", documento="INGRESOS")
    assert estado(client, limpio["id_solicitud"]).json()["hito"] == "Documentos con observaciones"
    otro = nuevo(client)
    client.post(f"/api/credito/casos/{otro['id']}/documentos", json=[doc(t) for t in TIPOS[:3]] + [doc("PAGARE", cedula="002-9999999-9")])
    completar(client, tareas(client, "legal")[0]["key"], resultado="RECHAZA")
    assert estado(client, otro["id_solicitud"]).json()["hito"] == "Pasa a atención presencial"

def test_inc1_no_revela_ids_ni_datos_personales(client):
    c = nuevo(client)
    inexistente = "SOL-00001" if c["id_solicitud"] != "SOL-00001" else "SOL-00002"
    a, b = estado(client, inexistente), estado(client, "no-es-un-id")
    assert a.status_code == b.status_code == 404 and a.json() == b.json()
    texto = estado(client, c["id_solicitud"]).text
    assert "demo@ejemplo.test" not in texto and "350000" not in texto and "001-0000001-1" not in texto


# --- CAM-4 (ronda 25): conexión real con Camunda, probada con FakeCamunda (sin red) ---

def test_cam4_crea_instancia_real_y_publica_la_validacion(client_camunda):
    c = client_camunda
    caso = nuevo(c)
    assert caso["instance_key"].isdigit()
    assert caso["bpmn_id"] == "Process_Credito_MVP"
    assert c.fake.iniciadas == [("Process_Credito_MVP", {"solicitudId": caso["id_solicitud"]})]

    r = c.post(f"/api/credito/casos/{caso['id']}/documentos", json=[doc(t) for t in TIPOS])
    assert r.status_code == 200 and r.json()["camunda_sincronizado"] is True
    assert c.fake.mensajes[-1] == ("documentos-cargados", caso["id_solicitud"], {"resultadoValidacion": "valido"})

def test_cam4_completa_las_tareas_reales_de_legal_y_despacho(client_camunda):
    c = client_camunda
    caso = nuevo(c)
    c.post(f"/api/credito/casos/{caso['id']}/documentos",
           json=[doc(t) for t in TIPOS[:3]] + [doc("PAGARE", cedula="002-9999999-9")])
    instance_key = c.get(f"/api/credito/casos/{caso['id']}").json()["instance_key"]
    assert c.fake.mensajes[-1][2] == {"resultadoValidacion": "dudoso"}

    c.fake.agregar_tarea(instance_key, "TB_ACT_REVISAR", "RZT-1")
    r = completar(c, tareas(c, "legal")[0]["key"], resultado="ACEPTA")
    assert r.status_code == 200 and c.fake.completadas[-1] == ("RZT-1", {"legalAcepta": True})
    assert r.json()["caso"]["estado"] == "VERIFICACION_DESPACHO"

    c.fake.agregar_tarea(instance_key, "TB_ACT_VERIF", "DZT-1")
    r = completar(c, tareas(c, "despacho")[0]["key"], resultado="CORREGIR", documento="INGRESOS")
    assert r.status_code == 200 and c.fake.completadas[-1] == ("DZT-1", {"expedienteOk": False})

def test_cam4_si_camunda_no_tiene_la_tarea_no_cambia_nada_local(client_camunda):
    c = client_camunda
    caso = nuevo(c)
    c.post(f"/api/credito/casos/{caso['id']}/documentos", json=[doc(t) for t in TIPOS])
    key = tareas(c, "despacho")[0]["key"]
    # No se registró la tarea gemela en el Fake: Camunda no la tiene -> debe fallar sin tocar el estado local.
    r = completar(c, key, resultado="OK")
    assert r.status_code == 502 and not c.fake.completadas
    assert c.get(f"/api/credito/casos/{caso['id']}").json()["estado"] == "VERIFICACION_DESPACHO"

def test_cam4_si_camunda_falla_al_iniciar_no_crea_el_caso(client_camunda):
    c = client_camunda
    def falla(*a, **k): raise CamundaError("clúster no disponible (simulado)")
    c.fake.start = falla
    r = c.post("/api/credito/casos", json={"cliente_alias": "Cliente Demo", "correo_cliente": "demo@ejemplo.test", "monto": 350000})
    assert r.status_code == 502
    assert c.get("/api/credito/casos").json() == []

# INC-4: buzón de correos simulados (cliente, Legal y Despacho). No se envía nada.
def buzon(client, rol, **filtro): return client.get("/api/credito/correos", params={"rol": rol, **filtro}).json()

def test_inc4_enlace_aviso_a_despacho_y_verificado(client):
    c = nuevo(client)
    m = buzon(client, "cliente")
    assert len(m) == 1 and m[0]["elemento"] == "TB_SND_ENLACE" and m[0]["para"] == "demo@ejemplo.test"
    assert m[0]["asunto"].startswith(c["id_solicitud"]) and m[0]["enlace"] == f"/credito?caso={c['id']}" and not m[0]["leido"]
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS])
    assert [x["elemento"] for x in buzon(client, "despacho")] == ["TB_ACT_VERIF"]
    assert buzon(client, "legal") == []
    completar(client, tareas(client, "despacho")[0]["key"], resultado="OK")
    assert [x["elemento"] for x in buzon(client, "cliente")] == ["END_VERIFICADO", "TB_SND_ENLACE"]  # más reciente primero

def test_inc4_rechazo_dudoso_y_papel_avisan_a_quien_corresponde(client):
    c = nuevo(client)
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS[:3]] + [doc("PAGARE", dias=25)])
    rech = buzon(client, "cliente")[0]
    assert rech["elemento"] == "TB_SND_CORREGIR" and "Pagaré: vencido (> 20 días) (intento 1 de 5)" in rech["cuerpo"]
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE", cedula="002-9999999-9")])
    legal = buzon(client, "legal")
    assert len(legal) == 1 and legal[0]["elemento"] == "TB_ACT_REVISAR" and "cédula" in legal[0]["cuerpo"]
    assert legal[0]["para"] == "legal@credito-demo.test" and buzon(client, "despacho") == []
    completar(client, tareas(client, "legal")[0]["key"], resultado="RECHAZA")
    assert buzon(client, "cliente")[0]["elemento"] == "END_PAPEL_LEGAL" and buzon(client, "despacho") == []

def test_inc4_correccion_de_despacho_y_legal_acepta(client):
    c = nuevo(client)
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc(t) for t in TIPOS[:3]] + [doc("PAGARE", cedula="X")])
    completar(client, tareas(client, "legal")[0]["key"], resultado="ACEPTA")
    assert [x["elemento"] for x in buzon(client, "despacho")] == ["TB_ACT_VERIF"]
    completar(client, tareas(client, "despacho")[0]["key"], resultado="CORREGIR", documento="INGRESOS", observacion="Comprobante cortado")
    m = buzon(client, "cliente")[0]
    assert m["elemento"] == "TB_SND_CORREGIR" and "Comprobante de ingresos" in m["cuerpo"] and "Comprobante cortado" in m["cuerpo"]

def test_inc4_intentos_agotados_avisan_ruta_en_papel(client):
    c = nuevo(client)
    validos = [doc(t) for t in TIPOS[:3]]
    client.post(f"/api/credito/casos/{c['id']}/documentos", json=validos + [doc("PAGARE", dias=30)])
    for _ in range(4):
        client.post(f"/api/credito/casos/{c['id']}/documentos", json=[doc("PAGARE", dias=30)])
    m = buzon(client, "cliente")
    assert m[0]["elemento"] == "END_PAPEL_AGOTADO" and "Pagaré" in m[0]["cuerpo"]
    assert sum(x["elemento"] == "TB_SND_CORREGIR" for x in m) == 4  # el 5.º rechazo ya no pide volver a cargar

def test_inc4_filtro_leido_y_entradas_invalidas(client):
    a = nuevo(client)
    client.post("/api/credito/casos", json={"cliente_alias": "Otra Demo", "correo_cliente": "otra@ejemplo.test", "monto": 1000})
    assert len(buzon(client, "cliente")) == 2
    solo = buzon(client, "cliente", para="demo@ejemplo.test")
    assert len(solo) == 1 and solo[0]["caso_id"] == a["id"]
    r = client.post(f"/api/credito/correos/{solo[0]['id']}/leido")
    assert r.status_code == 200 and r.json()["leido"] is True
    assert buzon(client, "cliente", para="demo@ejemplo.test")[0]["leido"] is True
    assert client.post("/api/credito/correos/9999/leido").status_code == 404
    assert client.get("/api/credito/correos", params={"rol": "gerente"}).status_code == 422
    assert client.get("/buzon").status_code == 200

def test_inc4_si_camunda_falla_no_queda_correo(client_camunda):
    c = client_camunda
    caso = nuevo(c)
    c.post(f"/api/credito/casos/{caso['id']}/documentos", json=[doc(t) for t in TIPOS])
    assert completar(c, tareas(c, "despacho")[0]["key"], resultado="OK").status_code == 502
    assert [x["elemento"] for x in buzon(c, "cliente")] == ["TB_SND_ENLACE"]  # sin «verificado»
