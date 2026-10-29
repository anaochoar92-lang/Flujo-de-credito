"""Prueba manual de extremo a extremo del MVP de crédito contra un servidor real en ENGINE_MODE=camunda.

Uso:
  1. Levantar el servidor en otra terminal (si no está corriendo ya):
       .venv/Scripts/python.exe -m uvicorn app.main:app --port 8000
     (requiere ENGINE_MODE=camunda en el .env; ya lo está)
  2. Ejecutar este script:
       .venv/Scripts/python.exe scripts/prueba_manual_credito.py

Recorre: crear caso (arranca instancia real en Camunda) -> esperar el job automático
TB_SND_ENLACE -> cargar los 4 documentos válidos y consistentes (sin diferencias, va directo
a Despacho) -> esperar a que la tarea de Despacho aparezca -> completarla con OK -> el caso
queda VERIFICADO. Imprime el instance_key, la bitácora y el estado remoto en Camunda.

También sirve de referencia para pruebas manuales repetidas: cambia DATOS_DOC para forzar un
caso dudoso (declarar cédula o monto distinto en PAGARE) y validar la ruta de Legal.
"""
import sys, time
import httpx

BASE = "http://127.0.0.1:8000"
TIMEOUT_JOB = 60  # segundos esperando a que el worker automático (trabajador_camunda) actúe


def hace(dias):
    from datetime import date, timedelta
    return (date.today() - timedelta(days=dias)).isoformat()


DOCS_VALIDOS = [
    {"tipo": "IDENTIDAD", "fecha_expedicion": hace(5), "legible": True, "nombre": "Cliente Demo", "cedula": "001-0000001-1"},
    {"tipo": "INGRESOS", "fecha_expedicion": hace(5), "legible": True, "nombre": "Cliente Demo", "salario": 45000},
    {"tipo": "ESTADO_CUENTA", "fecha_expedicion": hace(5), "legible": True, "nombre": "Cliente Demo"},
    {"tipo": "PAGARE", "fecha_expedicion": hace(5), "legible": True, "nombre": "Cliente Demo", "cedula": "001-0000001-1", "monto": 350000},
]


def esperar(fn, descripcion, timeout=TIMEOUT_JOB, intervalo=2):
    fin = time.time() + timeout
    while time.time() < fin:
        r = fn()
        if r:
            return r
        time.sleep(intervalo)
    raise TimeoutError(f"Tiempo agotado esperando: {descripcion}")


def main():
    with httpx.Client(base_url=BASE, timeout=15) as c:
        sol = c.post("/api/credito/casos", json={
            "cliente_alias": "Cliente Demo", "correo_cliente": "demo@ejemplo.test", "monto": 350000,
        })
        sol.raise_for_status()
        caso = sol.json()
        caso_id, id_solicitud, instance_key = caso["id"], caso["id_solicitud"], caso["instance_key"]
        print(f"1) Caso creado: {id_solicitud} (id={caso_id}, instance_key={instance_key})")

        def hay_estado(estado_esperado):
            def chk():
                actual = c.get(f"/api/credito/casos/{caso_id}").json()
                return actual if actual["estado"] == estado_esperado else None
            return chk

        print("2) Cargando los 4 documentos válidos...")
        resp = c.post(f"/api/credito/casos/{caso_id}/documentos", json=DOCS_VALIDOS)
        if resp.status_code not in (200, 422):
            resp.raise_for_status()
        print(f"   -> estado tras carga: {resp.json().get('estado')}, camunda_sincronizado={resp.json().get('camunda_sincronizado')}")

        print("3) Esperando a que aparezca la tarea de Despacho (worker automático completando TB_SVC_VALIDAR)...")
        tarea = esperar(lambda: next((t for t in c.get("/api/credito/tareas", params={"rol": "despacho"}).json()
                                      if t["caso_id"] == caso_id), None),
                         "tarea de Despacho")
        print(f"   -> tarea activa: {tarea['key']} ({tarea['name']})")

        print("4) Completando Despacho con resultado OK...")
        r = c.post(f"/api/credito/tareas/{tarea['key']}/completar", json={"actor": "prueba-manual", "resultado": "OK"})
        r.raise_for_status()
        print(f"   -> {r.json()['caso']['estado']}")

        final = esperar(hay_estado("VERIFICADO"), "estado VERIFICADO", timeout=20)
        print(f"5) Caso cerrado: estado={final['estado']}, cerrado_en={final['cerrado_en']}")

        bitacora = c.get(f"/api/credito/casos/{caso_id}/bitacora").json()
        print("\nBitácora:")
        for ev in bitacora:
            print(f"   {ev['momento']}  {ev['accion']:<28} tarea={ev['tarea']}")

        print(f"\nOK: flujo completo verificado end-to-end para {id_solicitud} (instance_key={instance_key})")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"FALLÓ: {ex}", file=sys.stderr)
        sys.exit(1)
