"""Capturas de pantalla para los manuales de usuario (14-mvp/manuales). Datos SINTETICOS.

Requiere el servidor en mock con base vacia en el puerto 8011 y Microsoft Edge:
  DATABASE_URL=sqlite:///manual.sqlite3 ENGINE_MODE=mock python -m uvicorn app.main:app --port 8011
  python scripts/manuales_capturas.py <carpeta_capturas>
Dependencias extra (no estan en requirements.txt): playwright, httpx, pillow.
"""
import sys, httpx
from datetime import date, timedelta
from playwright.sync_api import sync_playwright
B = "http://127.0.0.1:8011"; OUT = sys.argv[1]
TIPOS = ["IDENTIDAD", "INGRESOS", "ESTADO_CUENTA", "PAGARE"]
def doc(t, dias=5, cedula="001-0000001-1", nombre="Cliente Demo"):
    d = {"tipo": t, "fecha_expedicion": (date.today()-timedelta(days=dias)).isoformat(), "legible": True, "nombre": nombre}
    if t in ("IDENTIDAD", "PAGARE"): d["cedula"] = cedula
    if t == "INGRESOS": d["salario"] = 45000
    if t == "PAGARE": d["monto"] = 350000
    return d
h = httpx.Client(base_url=B)
def caso(alias, correo):
    return h.post("/api/credito/casos", json={"cliente_alias": alias, "correo_cliente": correo, "monto": 350000}).json()
p = caso("Pedro Demo", "pedro@ejemplo.test"); h.post(f"/api/credito/casos/{p['id']}/documentos", json=[doc(t, nombre="Pedro Demo") for t in TIPOS])
l = caso("Laura Demo", "laura@ejemplo.test"); h.post(f"/api/credito/casos/{l['id']}/documentos", json=[doc(t, nombre="Laura Demo") for t in TIPOS[:3]] + [doc("PAGARE", cedula="002-9999999-9", nombre="Laura Demo")])
r = caso("Rosa Demo", "rosa@ejemplo.test"); h.post(f"/api/credito/casos/{r['id']}/documentos", json=[doc(t, nombre="Rosa Demo") for t in TIPOS[:3]] + [doc("PAGARE", dias=25, nombre="Rosa Demo")])

with sync_playwright() as pw:
    br = pw.chromium.launch(channel="msedge")
    pg = br.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2, locale="es-DO")
    panel = lambda txt: pg.locator("section.panel", has_text=txt).first
    # Analista: crear solicitud
    pg.goto(B + "/credito"); pg.wait_for_timeout(800)
    panel("1. Solicitud aceptada").screenshot(path=f"{OUT}/a_form.png")
    pg.click("text=Enviar enlace al portal"); pg.wait_for_timeout(1200)
    pg.locator("#message").screenshot(path=f"{OUT}/a_msg.png")
    nuevo = h.get("/api/credito/casos").json()[0]
    # Cliente: buzón con el correo del enlace
    pg.goto(B + "/buzon"); pg.wait_for_timeout(1200)
    pg.select_option("#filtro select", "demo@ejemplo.test"); pg.wait_for_timeout(800)
    pg.locator(".item").first.click(); pg.wait_for_timeout(800)
    pg.locator("section.panel").screenshot(path=f"{OUT}/c_buzon.png")
    # Cliente: formulario de carga
    pg.goto(B + f"/credito?caso={nuevo['id']}"); pg.wait_for_timeout(1200)
    pg.click("text=Llenar ejemplo válido"); pg.wait_for_timeout(300)
    panel("2. Carga de documentos").screenshot(path=f"{OUT}/c_carga.png")
    # Cliente: documento rechazado
    pg.goto(B + f"/credito?caso={r['id']}"); pg.wait_for_timeout(1200)
    panel("2. Carga de documentos").screenshot(path=f"{OUT}/c_rechazo.png")
    # Cliente: consultar solicitud
    pg.fill("#estado input[name=id]", r["id_solicitud"]); pg.click("#estado button"); pg.wait_for_timeout(800)
    pg.locator("#consulta").screenshot(path=f"{OUT}/c_consulta.png")
    # Legal y Despacho: buzón y bandeja
    for rol, txt in (("legal", "3a. Bandeja de Legal"), ("despacho", "3b. Bandeja de Despacho")):
        pg.goto(B + "/buzon"); pg.wait_for_timeout(1000)
        pg.click(f"#tabs button:has-text('{rol.capitalize()}')"); pg.wait_for_timeout(800)
        pg.locator(".item").first.click(); pg.wait_for_timeout(800)
        pg.locator("section.panel").screenshot(path=f"{OUT}/{rol[0]}_buzon.png")
        pg.goto(B + "/credito"); pg.wait_for_timeout(1200)
        panel(txt).screenshot(path=f"{OUT}/{rol[0]}_bandeja.png")
    # Analista: bitácora del caso de Pedro
    pg.goto(B + f"/credito?caso={p['id']}"); pg.wait_for_timeout(1200)
    panel("4. Bitácora").screenshot(path=f"{OUT}/a_bitacora.png")
    br.close()
print("ok")
