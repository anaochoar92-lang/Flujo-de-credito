"""Pruebas del MVP Flujo de crédito preaprobado (REQ-MVP-01 a 03, trabajos/mi-proceso/14-mvp). Datos SINTÉTICOS."""
from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from app.main import app

TIPOS = ["IDENTIDAD", "INGRESOS", "ESTADO_CUENTA", "PAGARE"]

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path/'credito.sqlite3'}")
    monkeypatch.setenv("ENGINE_MODE", "mock")
    with TestClient(app) as c: yield c

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
