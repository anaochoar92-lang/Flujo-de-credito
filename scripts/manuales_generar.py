"""Genera los manuales de usuario del MVP (uno por rol) en PDF.


Primero correr scripts/manuales_capturas.py. Uso: python scripts/manuales_generar.py <capturas> trabajos/mi-proceso/14-mvp/manuales
Dependencias extra: reportlab, pillow. Usa las fuentes Segoe UI de Windows.
"""
import sys, os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table,
                                TableStyle, KeepTogether)

CAP, OUT = sys.argv[1], sys.argv[2]
F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("UI", F + "segoeui.ttf"))
pdfmetrics.registerFont(TTFont("UI-B", F + "segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("UI-SB", F + "seguisb.ttf"))
pdfmetrics.registerFont(TTFont("UI-I", F + "segoeuii.ttf"))
pdfmetrics.registerFont(TTFont("SYM", F + "seguisym.ttf"))
pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-B", italic="UI-I", boldItalic="UI-B")

TEAL, DARK, INK, MUTED = colors.HexColor("#0f7c7a"), colors.HexColor("#0e3b43"), colors.HexColor("#142334"), colors.HexColor("#57687c")
SOFT, LINE, WARN, RED = colors.HexColor("#e8f4f3"), colors.HexColor("#dce4ef"), colors.HexColor("#fff4d9"), colors.HexColor("#c8553d")
VERSION = "Versión 1.1 · 30/10/2026"
W = letter[0] - 3.6 * cm

st = {
    "p": ParagraphStyle("p", fontName="UI", fontSize=9.5, leading=13.5, textColor=INK),
    "lbl": ParagraphStyle("l", fontName="UI-B", fontSize=9.5, leading=13.5, textColor=INK, spaceBefore=4, keepWithNext=1),
    "small": ParagraphStyle("s", fontName="UI", fontSize=8.5, leading=11.5, textColor=MUTED),
    "h": ParagraphStyle("h", fontName="UI-B", fontSize=13, leading=16, textColor=DARK, spaceBefore=10, spaceAfter=5, keepWithNext=1),
    "cell": ParagraphStyle("c", fontName="UI", fontSize=8.8, leading=11.8, textColor=INK),
    "cellh": ParagraphStyle("ch", fontName="UI-SB", fontSize=8.8, leading=11.8, textColor=colors.white),
    "num": ParagraphStyle("n", fontName="UI-B", fontSize=10, leading=12, textColor=colors.white, alignment=1),
    "cap": ParagraphStyle("cap", fontName="UI-I", fontSize=8, leading=10, textColor=MUTED, alignment=1, spaceBefore=2, spaceAfter=6),
}
P = lambda t, s="p": Paragraph(t, st[s])
H = lambda t: P(t, "h")

def btn(t):  # nombre de un botón o elemento de pantalla
    return f'<font name="UI-SB" color="#0f7c7a">«{t}»</font>'

def img(nombre, ancho_cm, pie=None):
    ruta = os.path.join(CAP, nombre + ".png")
    w, h = PILImage.open(ruta).size
    ancho = min(ancho_cm * cm, W)
    i = Image(ruta, width=ancho, height=ancho * h / w)
    t = Table([[i]], colWidths=[ancho + 4])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, LINE), ("LEFTPADDING", (0, 0), (-1, -1), 2),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return [t, P(pie, "cap")] if pie else [t, Spacer(1, 6)]

def pasos(items, inicio=1, ancho=None):
    ancho = ancho or W
    filas = []
    for k, txt in enumerate(items, inicio):
        num = Table([[P(str(k), "num")]], colWidths=[0.62 * cm], rowHeights=[0.62 * cm])
        num.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL), ("ROUNDEDCORNERS", [9, 9, 9, 9]),
                                 ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 0),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 1), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
        filas.append([num, P(txt)])
    t = Table(filas, colWidths=[0.9 * cm, ancho - 0.9 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t

def caja(txt, fondo=SOFT, borde=TEAL, ancho=None):
    t = Table([[P(txt)]], colWidths=[ancho or W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fondo), ("LINEBEFORE", (0, 0), (0, -1), 3, borde),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t

def tabla(cab, filas, anchos):
    data = [[P(c, "cellh") for c in cab]] + [[P(c, "cell") for c in f] for f in filas]
    t = Table(data, colWidths=[a * W for a in anchos], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), DARK), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f8fb")]),
                           ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINE), ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t

def lado_a_lado(izq, der, ancho_izq=0.5):
    t = Table([[izq, der]], colWidths=[W * ancho_izq, W * (1 - ancho_izq)])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("RIGHTPADDING", (0, 0), (0, -1), 10), ("RIGHTPADDING", (1, 0), (1, -1), 0)]))
    return t

def construir(archivo, rol, subtitulo, story):
    def pagina(c, doc):
        c.saveState()
        ancho, alto = letter
        if doc.page == 1:
            c.setFillColor(DARK); c.rect(0, alto - 3.5 * cm, ancho, 3.5 * cm, stroke=0, fill=1)
            c.setFillColor(colors.HexColor("#9db7b3")); c.setFont("UI-SB", 8)
            c.drawString(1.8 * cm, alto - 1.15 * cm, "MANUAL DE USUARIO · MVP FLUJO DE CRÉDITO PREAPROBADO")
            c.setFillColor(colors.white); c.setFont("UI-B", 22); c.drawString(1.8 * cm, alto - 2.15 * cm, rol)
            c.setFont("UI", 10); c.setFillColor(colors.HexColor("#d5e6e4")); c.drawString(1.8 * cm, alto - 2.8 * cm, subtitulo)
            c.setFont("UI-SB", 8); c.drawRightString(ancho - 1.8 * cm, alto - 1.15 * cm, VERSION)
        else:
            c.setFillColor(DARK); c.rect(0, alto - 0.9 * cm, ancho, 0.9 * cm, stroke=0, fill=1)
            c.setFillColor(colors.white); c.setFont("UI-SB", 8.5)
            c.drawString(1.8 * cm, alto - 0.58 * cm, f"Manual de usuario · {rol}")
        c.setStrokeColor(LINE); c.line(1.8 * cm, 1.35 * cm, ancho - 1.8 * cm, 1.35 * cm)
        c.setFillColor(MUTED); c.setFont("UI", 7.5)
        c.drawString(1.8 * cm, 0.95 * cm, "Datos SINTÉTICOS / DEMOSTRACIÓN. No use nombres, cédulas ni correos reales.")
        c.drawRightString(ancho - 1.8 * cm, 0.95 * cm, f"Página {doc.page}")
        c.restoreState()
    doc = BaseDocTemplate(os.path.join(OUT, archivo), pagesize=letter, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                          title=f"Manual de usuario · {rol}", author="Equipo Flujo de crédito (CESA MBA)",
                          subject="MVP Flujo de crédito preaprobado")
    alto = letter[1]
    f1 = Frame(1.8 * cm, 1.6 * cm, W, alto - 3.5 * cm - 2.0 * cm, id="f1")
    f2 = Frame(1.8 * cm, 1.6 * cm, W, alto - 0.9 * cm - 2.0 * cm, id="f2")
    doc.addPageTemplates([PageTemplate("primera", [f1], onPage=pagina, autoNextPageTemplate="resto"),
                          PageTemplate("resto", [f2], onPage=pagina)])
    doc.build(story)

URL_PORTAL, URL_BUZON = "http://localhost:8000/credito", "http://localhost:8000/buzon"
INGRESO_DEMO = ("Esta es una demostración local: <b>no hay usuario ni contraseña</b>. Si la página no abre, pida al "
                "responsable de la demo que levante la aplicación.")
MSG_TAREA = [
    ["«La tarea ya no está activa (¿doble clic?)»", "Alguien (o un segundo clic) ya completó esa tarea.", "Recargue la página (F5). No repita la acción."],
    ["«No se pudo completar la tarea en Camunda…»", "El motor de procesos no confirmó el paso (la app ya reintentó unos segundos). <b>No se guardó nada</b>: el portal y Camunda siguen iguales.", "Espere un momento y pulse de nuevo; si sigue, avise a soporte."],
]

# ─────────────────────────────── CLIENTE ───────────────────────────────
cliente = [
    H("¿Para qué sirve?"),
    P("Desde el portal usted carga los <b>4 documentos</b> de su crédito preaprobado, corrige los que se rechacen y consulta "
      "en qué va su solicitud, sin ir al concesionario."),
    H("1. Cómo ingresar"),
    pasos([f"Abra su buzón de correo: {URL_BUZON} y quédese en la pestaña {btn('Cliente')}.",
           f"En {btn('Buzón de')} elija su dirección de correo.",
           f"Abra el correo <b>«SOL-NNNNN · Cargue sus documentos en el portal»</b> y pulse {btn('Ir al portal')}. "
           "El portal se abre con su solicitud ya seleccionada. Guarde su número <b>SOL-NNNNN</b>."]),
    caja(INGRESO_DEMO, WARN, colors.HexColor("#e0b84a")),
    Spacer(1, 6),
    *img("c_buzon", 15.5, "Buzón del cliente con el correo del enlace al portal."),
    H("2. Cargar sus documentos"),
    lado_a_lado(
        [pasos([f"Vaya a la sección {btn('2. Carga de documentos')}. Verifique que en {btn('Caso')} aparezca su SOL-NNNNN.",
                "Para cada documento (Cédula, Comprobante de ingresos, Estado de cuenta y Pagaré) llene:<br/>"
                "• <b>Fecha de expedición</b>: máximo 20 días calendario antes de hoy.<br/>"
                "• <b>Nombre declarado</b>: escríbalo <b>igual</b> en los 4 documentos.<br/>"
                "• <b>Cédula</b> (Cédula y Pagaré), <b>Salario</b> (Comprobante) y <b>Monto</b> (Pagaré), tal como aparecen en el papel.",
                f"Pulse {btn('Buscar archivo…')}, elija en su equipo el archivo del documento (PDF, JPG o PNG) y verifique "
                "que su nombre aparezca junto al botón.",
                f"Deje marcada la casilla {btn('Legible')} solo si el documento se lee completo.",
                f"Pulse {btn('Cargar documentos')}. Verá una barra de avance mientras se «sube»."], ancho=W * 0.56 - 10),
         caja("<b>Demostración:</b> el archivo <b>no sale de su equipo</b>; el portal solo muestra su nombre. "
              f"Los botones {btn('Llenar ejemplo válido')} y {btn('Llenar ejemplo dudoso')} llenan datos y un archivo de prueba.",
              ancho=W * 0.56 - 10)],
        img("c_carga_corta", 7.2, "Formulario de carga (se muestra el primer documento).")[:2], 0.56),
    H("Reglas para que sus documentos se acepten"),
    caja("• Los <b>4</b> documentos son obligatorios.  • Fecha de expedición de <b>máximo 20 días calendario</b> (20 días exactos sí vale).<br/>"
         "• Deben ser <b>legibles</b>.  • Nombre, cédula, salario y monto deben <b>coincidir</b> entre documentos; si no, Legal lo revisa.<br/>"
         "• Tiene <b>5 intentos por documento</b>; al quinto rechazo su solicitud pasa a atención presencial."),
    H("3. Qué pasa después de cargar"),
    tabla(["Mensaje en pantalla", "Qué significa", "Qué hacer"], [
        ["Verde: «Documentos válidos»", "Sus 4 documentos fueron aceptados y pasan a revisión del banco.", "Nada. Le llegarán correos con cada avance."],
        ["Rojo: «Rechazados: Pagaré (vencido (&gt; 20 días))…»", "Uno o más documentos no se aceptaron. Cada rechazo suma 1 intento a ese documento.", "Corrija solo esos documentos (paso 4)."],
        ["Rojo: «No se aceptan más cargas: intentos agotados…»", "Un documento llegó a 5 intentos.", "Espere la llamada de un asesor para entregarlo en papel."],
        ["Rojo: «Seleccione el archivo de: …»", "Falta elegir el archivo de esos documentos. No se envió nada.", f"Pulse {btn('Buscar archivo…')} en cada uno y cargue de nuevo."],
        ["Rojo: «Camunda no confirmó la carga; no se registró nada…»", "El sistema del banco no confirmó la recepción. No se guardó ni se descontó ningún intento.", "Espere unos segundos y pulse de nuevo; si sigue, avise a su asesor."],
    ], [0.32, 0.38, 0.30]),
    H("4. Corregir un documento rechazado"),
    lado_a_lado(
        pasos([f"Abra el correo <b>«Documentos con observaciones»</b> o <b>«Despacho pide corregir un documento»</b> y pulse {btn('Ir al portal')}.",
               "Los documentos aceptados aparecen arriba con <font name='SYM'>✓</font> y <b>no</b> se vuelven a subir.",
               "Solo verá los rechazados, con el motivo en rojo y el conteo de <b>intentos x/5</b>.",
               f"Corrija los datos o la fecha, elija de nuevo el archivo con {btn('Buscar archivo…')}, revise {btn('Legible')} "
               f"y pulse {btn('Cargar documentos')}."], ancho=W * 0.5 - 10),
        img("c_rechazo", 7.6, "Pagaré rechazado por vencido; los otros 3 ya están aceptados.")[:2], 0.5),
    H("5. Consultar en qué va su solicitud"),
    pasos([f"En la sección {btn('Consultar mi solicitud')} escriba su número <b>SOL-NNNNN</b> y pulse {btn('Consultar')}.",
           "Verá el hito actual y la fecha del último cambio (no muestra datos personales)."]),
    *img("c_consulta", 14, None),
    tabla(["Hito", "Qué significa"], [
        ["Enlace enviado", "Falta que cargue sus documentos."],
        ["Documentos con observaciones", "Hay documentos por corregir (revise su correo)."],
        ["En revisión", "Legal revisa una diferencia entre sus documentos."],
        ["En verificación", "Despacho verifica su expediente."],
        ["Expediente verificado", "Listo: su expediente digital quedó completo."],
        ["Pasa a atención presencial", "Un asesor lo contactará para entregar documentos en papel."],
    ], [0.35, 0.65]),
]

# ─────────────────────────────── LEGAL ───────────────────────────────
legal = [
    H("¿Para qué sirve?"),
    P("Legal decide los <b>casos dudosos</b>: solicitudes con los 4 documentos válidos pero en las que el nombre, la cédula, "
      "el salario o el monto <b>no coinciden</b> entre documentos. Hasta que Legal decida, el caso no pasa a Despacho."),
    H("1. Cómo ingresar"),
    pasos([f"Abra el buzón: {URL_BUZON} y pulse la pestaña {btn('Legal')} (buzón legal@credito-demo.test). El número rojo indica correos sin leer.",
           "Abra el correo <b>«SOL-NNNNN · Nueva tarea: Revisar documento dudoso»</b>. El texto dice <b>qué dato no coincide</b>.",
           f"Pulse {btn('Abrir en mi bandeja')}. También puede entrar directo a {URL_PORTAL} y bajar a {btn('3a. Bandeja de Legal')}."]),
    caja(INGRESO_DEMO, WARN, colors.HexColor("#e0b84a")),
    Spacer(1, 6),
    *img("l_buzon", 15.5, "Buzón de Legal con el aviso de tarea nueva."),
    H("2. Revisar y decidir"),
    lado_a_lado(
        pasos(["Ubique la tarjeta con el número <b>SOL-NNNNN</b> del correo.",
               "Compare los datos declarados en cada documento (nombre y cédula se muestran en la tarjeta).",
               f"Si la diferencia es aceptable (p. ej. error de digitación), pulse {btn('Acepta')}.",
               f"Si no se puede validar en línea, pulse {btn('Rechaza (ruta en papel)')}.",
               "Verá el mensaje verde <b>«Tarea completada»</b> y la tarjeta desaparece de su bandeja."], ancho=W * 0.52 - 10),
        img("l_bandeja", 8.2, "Bandeja de Legal: la cédula del pagaré no coincide.")[:2], 0.52),
    caja("<b>Atención:</b> la decisión se guarda al primer clic y <b>no se puede deshacer</b>; la pantalla no pide confirmación.",
         colors.HexColor("#fbe3dd"), RED),
    H("3. Qué pasa con cada decisión"),
    tabla(["Decisión", "Estado del caso", "Quién recibe correo"], [
        ["Acepta", "Pasa a «En verificación» y aparece en la bandeja de Despacho.", "Despacho: «Nueva tarea: Verificar expediente digital»."],
        ["Rechaza (ruta en papel)", "Se cierra como «Pasa a atención presencial».", "Cliente: «Su solicitud pasa a atención presencial»."],
    ], [0.25, 0.40, 0.35]),
    H("4. Mensajes que puede ver"),
    tabla(["Mensaje", "Qué significa", "Qué hacer"], MSG_TAREA, [0.34, 0.36, 0.30]),
    H("5. Consultar el historial de un caso"),
    P(f"En {btn('2. Carga de documentos')} elija el caso en {btn('Caso')}; la sección {btn('4. Bitácora y datos para Preset')} "
      "muestra cada paso con fecha, hora y quién lo hizo, incluida su decisión."),
]

# ─────────────────────────────── DESPACHO ───────────────────────────────
despacho = [
    H("¿Para qué sirve?"),
    P("Despacho hace la <b>verificación final del expediente digital</b>: confirma que los 4 documentos están completos y "
      "correctos, o pide al cliente que corrija uno."),
    H("1. Cómo ingresar"),
    pasos([f"Abra el buzón: {URL_BUZON} y pulse la pestaña {btn('Despacho')} (buzón despacho@credito-demo.test).",
           "Abra el correo <b>«SOL-NNNNN · Nueva tarea: Verificar expediente digital»</b>. Le llega cuando los documentos son "
           "válidos o cuando Legal aceptó un caso dudoso.",
           f"Pulse {btn('Abrir en mi bandeja')}. También puede entrar directo a {URL_PORTAL} y bajar a {btn('3b. Bandeja de Despacho')}."]),
    caja(INGRESO_DEMO, WARN, colors.HexColor("#e0b84a")),
    Spacer(1, 6),
    *img("d_buzon", 15.5, "Buzón de Despacho con el aviso de tarea nueva."),
    H("2. Verificar el expediente"),
    *img("d_bandeja", 9.5, "Bandeja de Despacho."),
    P("Si todo está bien:", "lbl"),
    pasos([f"Revise los datos de la tarjeta y pulse {btn('Expediente OK')}.",
           "Verá «Tarea completada». El caso queda <b>«Expediente verificado»</b> con fecha y hora, y el cliente recibe el correo de confirmación."]),
    P("Si un documento necesita corrección:", "lbl"),
    pasos([f"En la lista junto al botón elija el documento (Cédula, Comprobante de ingresos, Estado de cuenta o Pagaré).",
           f"Pulse {btn('Pedir corrección')}.",
           "El caso vuelve a «Documentos con observaciones» y el cliente recibe <b>«Despacho pide corregir un documento»</b>. "
           "Esta corrección <b>no</b> le suma intentos al cliente.",
           "Cuando el cliente vuelva a cargar el documento, le llegará un nuevo aviso de tarea."], 3),
    caja("Pida una sola corrección por clic y elija bien el documento antes de pulsar: la acción se guarda al primer clic y "
         "no pide confirmación. En esta versión el motivo que recibe el cliente es «Corrección pedida por Despacho».",
         colors.HexColor("#fbe3dd"), RED),
    H("3. Mensajes que puede ver"),
    tabla(["Mensaje", "Qué significa", "Qué hacer"], MSG_TAREA, [0.34, 0.36, 0.30]),
    H("4. Consultar el historial de un caso"),
    P(f"En {btn('2. Carga de documentos')} elija el caso en {btn('Caso')}; la sección {btn('4. Bitácora y datos para Preset')} "
      "muestra cada paso con fecha, hora y actor."),
]

# ─────────────────────────────── ANALISTA ───────────────────────────────
analista = [
    H("¿Para qué sirve?"),
    P("El analista de crédito <b>registra la solicitud aceptada</b> (con eso el sistema envía al cliente el enlace al portal), "
      "hace <b>seguimiento</b> de los casos y descarga los datos para el tablero de Preset."),
    H("1. Cómo ingresar"),
    pasos([f"Abra el portal: {URL_PORTAL}.",
           f"Para ver los correos que envía el sistema, abra en otra pestaña el buzón: {URL_BUZON}."]),
    caja(INGRESO_DEMO + "<br/><font size=8>Responsable de la demo, en la carpeta del proyecto: "
         "<font name='Courier'>.venv\\Scripts\\python -m uvicorn app.main:app --port 8000</font></font>",
         WARN, colors.HexColor("#e0b84a")),
    caja("<b>Con Camunda conectado</b>, cada paso del portal se confirma primero en Camunda: si Camunda no responde, el portal "
         "no avanza y muestra el error, así ambos muestran siempre lo mismo. Cree las solicitudes <b>siempre desde el portal</b>: "
         "una instancia iniciada desde la consola de Camunda queda sin número SOL y el portal no puede seguirla."),
    H("2. Registrar una solicitud aceptada"),
    lado_a_lado(
        pasos([f"En {btn('1. Solicitud aceptada')} escriba el <b>alias</b> del cliente, su <b>correo</b> y el <b>monto aprobado</b> (RD$). Use solo datos sintéticos.",
               f"Pulse {btn('Enviar enlace al portal')}.",
               "Arriba aparece el mensaje verde <b>«Enlace enviado (simulado) · SOL-NNNNN»</b>. Ese es el número de la solicitud.",
               "El cliente recibe en su buzón el correo «Cargue sus documentos en el portal»."], ancho=W * 0.55 - 10),
        img("a_form", 7.2, "Formulario de solicitud aceptada.")[:2], 0.55),
    *img("a_msg", 16, "Confirmación con el número de solicitud."),
    H("3. Hacer seguimiento"),
    pasos([f"En {btn('2. Carga de documentos')}, la lista {btn('Caso')} muestra todas las solicitudes con su estado.",
           f"Elija una: la sección {btn('4. Bitácora y datos para Preset')} muestra cada paso con fecha, hora, elemento BPMN y actor.",
           f"Las bandejas {btn('3a. Legal')} y {btn('3b. Despacho')} muestran qué casos esperan a cada área.",
           f"En el buzón, pestaña {btn('Cliente')} con {btn('Todos los clientes')}, ve todos los correos enviados."]),
    *img("a_bitacora", 16, "Bitácora de un caso y botones de descarga."),
    tabla(["Estado", "Qué significa", "Quién actúa"], [
        ["ENLACE_ENVIADO", "Solicitud registrada; el cliente aún no carga documentos.", "Cliente"],
        ["DOCUMENTOS_RECHAZADOS", "Algún documento no pasó la validación (vencido, ilegible o faltante).", "Cliente"],
        ["REVISION_LEGAL", "Datos distintos entre documentos.", "Legal"],
        ["VERIFICACION_DESPACHO", "Documentos válidos, falta la verificación final.", "Despacho"],
        ["ESPERANDO_CORRECCION", "Despacho pidió corregir un documento.", "Cliente"],
        ["VERIFICADO", "Expediente digital verificado (fin).", "—"],
        ["RUTA_PAPEL", "Intentos agotados o Legal rechazó (fin).", "Asesor, fuera del portal"],
    ], [0.30, 0.50, 0.20]),
    H("4. Descargar datos para Preset"),
    P(f"Pulse {btn('CSV casos')}, {btn('CSV documentos')} o {btn('CSV eventos')}. Todos traen la columna "
      "<b>fuente_datos = SINTETICO</b> para no mezclarlos con datos reales."),
    P(f"{btn('CSV todos los casos en Camunda')} lista <b>todas</b> las instancias del proceso en Camunda (activas, completadas y "
      "canceladas), no solo la del caso elegido, con su estado en Camunda junto al estado en el portal. Sirve para comprobar "
      "que ambos coinciden. Solo funciona con Camunda conectado."),
    H("5. Mensajes que puede ver"),
    tabla(["Mensaje", "Qué hacer"], [
        ["El navegador marca el correo o el monto en rojo", "Corrija el formato: correo con @ y dominio; monto mayor que 0."],
        ["«No se pudo iniciar el proceso en Camunda…»", "El motor de procesos no respondió y la solicitud <b>no</b> se creó. Intente de nuevo o avise a soporte."],
        ["«Camunda no confirmó la carga…» / «No se pudo completar la tarea en Camunda…»", "El paso no se guardó en ningún lado. Espere unos segundos y repita; si persiste, revise los permisos del cliente API en Camunda."],
        ["Al abrir el CSV de Camunda: «solo está disponible con ENGINE_MODE=camunda»", "La demo corre sin Camunda (modo simulado). Use los otros CSV."],
    ], [0.42, 0.58]),
]

os.makedirs(OUT, exist_ok=True)
construir("manual-cliente.pdf", "Cliente", "Portal de expediente digital: cargar documentos y consultar su solicitud", cliente)
construir("manual-legal.pdf", "Legal", "Revisión de documentos dudosos", legal)
construir("manual-despacho.pdf", "Despacho", "Verificación del expediente digital", despacho)
construir("manual-analista.pdf", "Analista de crédito", "Registro de solicitudes aceptadas, seguimiento y datos para Preset", analista)
print("ok")
