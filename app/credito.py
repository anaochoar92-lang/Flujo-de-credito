"""MVP Flujo de crédito preaprobado (trabajos/mi-proceso/14-mvp). Datos SINTÉTICOS; solo modo mock.

Porción TO-BE: envío del enlace (TB_SND_ENLACE) → carga del cliente (CL_CARGAR) → validación
(TB_SVC_VALIDAR, simulada) → Legal si hay datos distintos (TB_ACT_REVISAR) → Despacho (TB_ACT_VERIF).
Las tareas no se guardan en tabla: se derivan del estado del caso, igual que el modo mock del kit.
"""
import csv, io, json, random, re
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import String, Float, Integer, Boolean, Date, DateTime, ForeignKey, Text, select, text, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

TIPOS = ["IDENTIDAD", "INGRESOS", "ESTADO_CUENTA", "PAGARE"]
MAX_INTENTOS = 5          # por documento (REQ-MVP-01, DAT-2)
VIGENCIA_DIAS = 20        # días calendario desde la expedición (REQ-MVP-01)
PROCESO_TOBE = "Process_Credito_TOBE"
ZONA = ZoneInfo("America/Santo_Domingo")  # PEND-03 (ronda 21)
ESPERA_DOCUMENTOS = ("ENLACE_ENVIADO", "DOCUMENTOS_RECHAZADOS", "ESPERANDO_CORRECCION")
TAREA_POR_ESTADO = {
    **{e: ("cliente", "CL_CARGAR", "Cargar documentos en el portal") for e in ESPERA_DOCUMENTOS},
    "REVISION_LEGAL": ("legal", "TB_ACT_REVISAR", "Revisar documento dudoso"),
    "VERIFICACION_DESPACHO": ("despacho", "TB_ACT_VERIF", "Verificar expediente digital"),
}
RESULTADOS = {"legal": ("ACEPTA", "RECHAZA"), "despacho": ("OK", "CORREGIR")}


class CredCaso(Base):
    __tablename__ = "cred_casos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_solicitud: Mapped[str] = mapped_column(String(9), unique=True, index=True)
    bpmn_id: Mapped[str] = mapped_column(String(100), default=PROCESO_TOBE)
    instance_key: Mapped[str | None] = mapped_column(String(80), nullable=True)
    cliente_alias: Mapped[str] = mapped_column(String(80))
    correo_cliente: Mapped[str] = mapped_column(String(120))
    monto: Mapped[float] = mapped_column(Float)
    estado: Mapped[str] = mapped_column(String(30), default="ENLACE_ENVIADO")
    etapa: Mapped[int] = mapped_column(Integer, default=0)
    caso_dudoso: Mapped[bool] = mapped_column(Boolean, default=False)
    decision_legal: Mapped[str | None] = mapped_column(String(10), nullable=True)
    resultado_despacho: Mapped[str | None] = mapped_column(String(10), nullable=True)
    fuente_datos: Mapped[str] = mapped_column(String(12), default="SINTETICO")
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    verificado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cerrado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    documentos: Mapped[list["CredDocumento"]] = relationship(back_populates="caso", cascade="all, delete-orphan", order_by="CredDocumento.id")
    eventos: Mapped[list["CredEvento"]] = relationship(back_populates="caso", cascade="all, delete-orphan", order_by="CredEvento.id")


class CredDocumento(Base):
    __tablename__ = "cred_documentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    caso_id: Mapped[int] = mapped_column(ForeignKey("cred_casos.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(20))
    fecha_expedicion: Mapped[date | None] = mapped_column(Date, nullable=True)
    legible: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    intentos: Mapped[int] = mapped_column(Integer, default=0)
    estado: Mapped[str] = mapped_column(String(12), default="PENDIENTE")
    motivo_rechazo: Mapped[str | None] = mapped_column(String(120), nullable=True)
    nombre_declarado: Mapped[str | None] = mapped_column(String(120), nullable=True)
    cedula_declarada: Mapped[str | None] = mapped_column(String(30), nullable=True)
    salario_declarado: Mapped[float | None] = mapped_column(Float, nullable=True)
    monto_declarado: Mapped[float | None] = mapped_column(Float, nullable=True)
    cargado_en: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    caso: Mapped[CredCaso] = relationship(back_populates="documentos")


class CredEvento(Base):
    __tablename__ = "cred_eventos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    caso_id: Mapped[int] = mapped_column(ForeignKey("cred_casos.id"), index=True)
    momento: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    accion: Mapped[str] = mapped_column(String(60))
    tarea: Mapped[str | None] = mapped_column(String(40), nullable=True)
    actor: Mapped[str] = mapped_column(String(80), default="sistema")
    detalles: Mapped[str] = mapped_column(Text, default="{}")
    caso: Mapped[CredCaso] = relationship(back_populates="eventos")


class CasoCredito(BaseModel):
    cliente_alias: str = Field(min_length=2, max_length=80)
    correo_cliente: str = Field(max_length=120, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    monto: float = Field(gt=0, le=100_000_000)


class DocumentoCarga(BaseModel):
    tipo: str = Field(pattern="^(IDENTIDAD|INGRESOS|ESTADO_CUENTA|PAGARE)$")
    fecha_expedicion: date
    legible: bool
    nombre: str | None = Field(default=None, max_length=120)
    cedula: str | None = Field(default=None, max_length=30)
    salario: float | None = Field(default=None, ge=0)
    monto: float | None = Field(default=None, ge=0)


class CompletarCredito(BaseModel):
    actor: str = Field(default="demo", min_length=2, max_length=80)
    resultado: str | None = None
    documento: str | None = None
    observacion: str = Field(default="", max_length=500)


def crear_vista_preset(engine):
    """Vista para Preset (DAT-3 = c). Todo es SINTÉTICO; con datos reales hay que quitar correo, alias y *_declarado."""
    if "vw_preset_mvp_casos" in inspect(engine).get_view_names():
        return
    with engine.begin() as conn:
        conn.execute(text("""CREATE VIEW vw_preset_mvp_casos AS
          SELECT c.id, c.id_solicitud, c.bpmn_id, c.cliente_alias, c.correo_cliente, c.monto, c.estado,
                 c.caso_dudoso, c.decision_legal, c.resultado_despacho, c.fuente_datos,
                 c.creado_en, c.verificado_en, c.cerrado_en,
                 d.tipo, d.fecha_expedicion, d.legible, d.intentos, d.estado AS estado_documento,
                 d.motivo_rechazo, d.nombre_declarado, d.cedula_declarada, d.salario_declarado, d.monto_declarado,
                 (SELECT SUM(x.intentos) FROM cred_documentos x WHERE x.caso_id = c.id) AS intentos_caso
          FROM cred_casos c JOIN cred_documentos d ON d.caso_id = c.id"""))


router = APIRouter(prefix="/api/credito", tags=["credito"])

def now(): return datetime.now(timezone.utc)
def iso(v): return v.isoformat() if v else None
def db_session(req: Request): return req.app.state.session_factory()

def log(db, caso, accion, tarea=None, actor="sistema", detalles=None):
    caso.eventos.append(CredEvento(accion=accion, tarea=tarea, actor=actor, detalles=json.dumps(detalles or {}, ensure_ascii=False)))

def cambiar_estado(caso, estado):
    # Cada cambio sube la etapa: una clave de tarea vieja deja de ser válida (doble clic → 409).
    caso.estado = estado
    caso.etapa += 1
    if estado in ("VERIFICADO", "RUTA_PAPEL"):
        caso.cerrado_en = now()

def tarea_activa(caso):
    t = TAREA_POR_ESTADO.get(caso.estado)
    if not t: return None
    rol, element_id, nombre = t
    return {"key": f"cred-{caso.id}-{rol}-{caso.etapa}", "name": nombre, "role": rol, "elementId": element_id,
            "caso_id": caso.id, "id_solicitud": caso.id_solicitud}

def ser_doc(d):
    return {"tipo": d.tipo, "estado": d.estado, "intentos": d.intentos, "motivo_rechazo": d.motivo_rechazo,
            "fecha_expedicion": iso(d.fecha_expedicion), "legible": d.legible, "nombre_declarado": d.nombre_declarado,
            "cedula_declarada": d.cedula_declarada, "salario_declarado": d.salario_declarado,
            "monto_declarado": d.monto_declarado, "cargado_en": iso(d.cargado_en)}

def ser_caso(c):
    return {"id": c.id, "id_solicitud": c.id_solicitud, "bpmn_id": c.bpmn_id, "instance_key": c.instance_key,
            "cliente_alias": c.cliente_alias, "correo_cliente": c.correo_cliente, "monto": c.monto, "estado": c.estado,
            "caso_dudoso": c.caso_dudoso, "decision_legal": c.decision_legal, "resultado_despacho": c.resultado_despacho,
            "fuente_datos": c.fuente_datos, "creado_en": iso(c.creado_en), "verificado_en": iso(c.verificado_en),
            "cerrado_en": iso(c.cerrado_en), "documentos": [ser_doc(d) for d in c.documentos]}

def ser_evento(e):
    return {"id": e.id, "caso_id": e.caso_id, "momento": iso(e.momento), "accion": e.accion, "tarea": e.tarea,
            "actor": e.actor, "detalles": e.detalles}

def obtener(db, caso_id):
    c = db.get(CredCaso, caso_id)
    if not c: raise HTTPException(404, "Caso no encontrado")
    return c

def nuevo_id(db):
    # SOL-90000 a SOL-99999: nunca choca con los sintéticos de 09-datos (SOL-00001 a SOL-08000), DAT-1.
    while True:
        candidato = f"SOL-{random.randint(90000, 99999)}"
        if not db.scalar(select(CredCaso.id).where(CredCaso.id_solicitud == candidato)):
            return candidato

def motivo(d: DocumentoCarga):
    dias = (datetime.now(ZONA).date() - d.fecha_expedicion).days  # 20 días exactos es válido (PEND-03)
    if dias < 0: return "fecha futura"
    if dias > VIGENCIA_DIAS: return "vencido (> 20 días)"
    if not d.legible: return "ilegible"
    return None

def diferencias(docs):
    """Campos declarados que no coinciden entre documentos (solo se comparan los valores presentes)."""
    campos = {"nombre": "nombre_declarado", "cedula": "cedula_declarada", "salario": "salario_declarado", "monto": "monto_declarado"}
    out = []
    for etiqueta, attr in campos.items():
        valores = {str(getattr(d, attr)).strip().lower() for d in docs if getattr(d, attr) not in (None, "")}
        if len(valores) > 1: out.append(etiqueta)
    return out


@router.post("/casos", status_code=201)
def crear(payload: CasoCredito, req: Request):
    with db_session(req) as db:
        c = CredCaso(id_solicitud=nuevo_id(db), cliente_alias=payload.cliente_alias.strip(),
                     correo_cliente=payload.correo_cliente.strip(), monto=payload.monto)
        c.documentos = [CredDocumento(tipo=t) for t in TIPOS]
        db.add(c); db.flush()
        c.instance_key = f"DEMO-{c.id}"
        # El correo se simula: se registra el evento, no se envía nada (alcance del MVP).
        log(db, c, "ENLACE_ENVIADO", tarea="TB_SND_ENLACE", detalles={"correo": "simulado"})
        db.commit()
        return ser_caso(c)

@router.post("/casos/{caso_id}/documentos")
def cargar(caso_id: int, docs: list[DocumentoCarga], req: Request):
    with db_session(req) as db:
        c = obtener(db, caso_id)
        por_tipo = {d.tipo: d for d in c.documentos}
        if any(d.estado == "AGOTADO" for d in c.documentos):
            raise HTTPException(409, "No se aceptan más cargas: intentos agotados; el caso pasó a la ruta en papel")
        if c.estado not in ESPERA_DOCUMENTOS:
            raise HTTPException(409, f"El caso no espera documentos (estado {c.estado})")
        if len({d.tipo for d in docs}) != len(docs):
            raise HTTPException(422, "Cada tipo de documento se envía una sola vez")
        ya_validos = [d.tipo for d in docs if por_tipo[d.tipo].estado == "VALIDO"]
        if ya_validos:
            raise HTTPException(409, f"Documento ya válido, no se vuelve a subir: {', '.join(ya_validos)}")

        rechazos = {}
        for d in docs:
            fila = por_tipo[d.tipo]
            fila.fecha_expedicion, fila.legible, fila.cargado_en = d.fecha_expedicion, d.legible, now()
            fila.nombre_declarado, fila.cedula_declarada = d.nombre, d.cedula
            fila.salario_declarado, fila.monto_declarado = d.salario, d.monto
            m = motivo(d)
            if m: rechazos[d.tipo] = m
            else: fila.estado, fila.motivo_rechazo = "VALIDO", None
        enviados = {d.tipo for d in docs}
        for fila in c.documentos:
            if fila.tipo not in enviados and fila.estado != "VALIDO":
                rechazos[fila.tipo] = "falta"

        for tipo, m in rechazos.items():
            fila = por_tipo[tipo]
            fila.intentos += 1
            fila.motivo_rechazo = m
            fila.estado = "AGOTADO" if fila.intentos >= MAX_INTENTOS else "RECHAZADO"
        log(db, c, "DOCUMENTOS_VALIDADOS", tarea="TB_SVC_VALIDAR", actor="cliente",
            detalles={"enviados": sorted(enviados), "rechazos": rechazos})

        if rechazos:
            agotados = [t for t in rechazos if por_tipo[t].estado == "AGOTADO"]
            if agotados:
                c.estado = "RUTA_PAPEL"; c.etapa += 1; c.cerrado_en = now()
                log(db, c, "INTENTOS_AGOTADOS", detalles={"documentos": agotados})
            else:
                cambiar_estado(c, "DOCUMENTOS_RECHAZADOS")
            db.commit()
            return JSONResponse(status_code=422, content={**ser_caso(c), "motivos": rechazos})

        dif = diferencias(c.documentos)
        if dif:
            c.caso_dudoso = True
            cambiar_estado(c, "REVISION_LEGAL")
            log(db, c, "CASO_DUDOSO", tarea="TB_GW_VALIDO", detalles={"campos_distintos": dif})
        else:
            cambiar_estado(c, "VERIFICACION_DESPACHO")
            log(db, c, "DOCUMENTOS_VALIDOS", tarea="TB_GW_VALIDO")
        db.commit()
        return ser_caso(c)

@router.get("/tareas")
def tareas(req: Request, rol: str | None = None):
    with db_session(req) as db:
        activas = [tarea_activa(c) for c in db.scalars(select(CredCaso).order_by(CredCaso.id)).all()]
        return [t for t in activas if t and (rol is None or t["role"] == rol)]

@router.post("/tareas/{key}/completar")
def completar(key: str, payload: CompletarCredito, req: Request):
    m = re.fullmatch(r"cred-(\d+)-(cliente|legal|despacho)-(\d+)", key)
    if not m: raise HTTPException(404, "Tarea no encontrada")
    with db_session(req) as db:
        c = obtener(db, int(m.group(1)))
        activa = tarea_activa(c)
        if not activa or activa["key"] != key:
            raise HTTPException(409, "La tarea ya no está activa (¿doble clic?)")
        rol = activa["role"]
        if rol == "cliente":
            raise HTTPException(422, "La tarea del cliente se completa cargando los documentos")
        if payload.resultado not in RESULTADOS[rol]:
            raise HTTPException(422, f"Resultado inválido para {rol}: use {' o '.join(RESULTADOS[rol])}")
        detalles = {"resultado": payload.resultado, "observacion": payload.observacion}
        if rol == "legal":
            c.decision_legal = payload.resultado
            cambiar_estado(c, "VERIFICACION_DESPACHO" if payload.resultado == "ACEPTA" else "RUTA_PAPEL")
            log(db, c, "REVISION_LEGAL_COMPLETADA", tarea="TB_ACT_REVISAR", actor=payload.actor, detalles=detalles)
        elif payload.resultado == "OK":
            c.resultado_despacho, c.verificado_en = "OK", now()
            cambiar_estado(c, "VERIFICADO")
            log(db, c, "EXPEDIENTE_VERIFICADO", tarea="TB_ACT_VERIF", actor=payload.actor, detalles=detalles)
        else:
            doc = next((d for d in c.documentos if d.tipo == payload.documento), None)
            if not doc: raise HTTPException(422, f"Indique el documento a corregir: {', '.join(TIPOS)}")
            # La corrección pedida por Despacho no suma intento (solo los rechazos de la validación lo hacen).
            doc.estado, doc.motivo_rechazo = "RECHAZADO", payload.observacion or "corrección pedida por Despacho"
            c.resultado_despacho = "CORREGIR"
            cambiar_estado(c, "ESPERANDO_CORRECCION")
            log(db, c, "CORRECCION_SOLICITADA", tarea="TB_ACT_VERIF", actor=payload.actor, detalles={**detalles, "documento": doc.tipo})
        db.commit()
        return {"ok": True, "caso": ser_caso(c)}

@router.get("/casos")
def casos(req: Request):
    with db_session(req) as db:
        return [ser_caso(c) for c in db.scalars(select(CredCaso).order_by(CredCaso.id.desc()).limit(100)).all()]

@router.get("/casos/{caso_id}")
def caso(caso_id: int, req: Request):
    with db_session(req) as db:
        return ser_caso(obtener(db, caso_id))

@router.get("/casos/{caso_id}/bitacora")
def bitacora(caso_id: int, req: Request):
    with db_session(req) as db:
        return [ser_evento(e) for e in obtener(db, caso_id).eventos]

@router.get("/export/{tabla}.csv")
def exportar(tabla: str, req: Request):
    with db_session(req) as db:
        if tabla == "casos":
            filas = [{k: v for k, v in ser_caso(c).items() if k != "documentos"} for c in db.scalars(select(CredCaso).order_by(CredCaso.id)).all()]
        elif tabla == "documentos":
            filas = [{"caso_id": d.caso_id, "id_solicitud": d.caso.id_solicitud, **ser_doc(d), "fuente_datos": "SINTETICO"}
                     for d in db.scalars(select(CredDocumento).order_by(CredDocumento.id)).all()]
        elif tabla == "eventos":
            filas = [{**ser_evento(e), "fuente_datos": "SINTETICO"} for e in db.scalars(select(CredEvento).order_by(CredEvento.id)).all()]
        else:
            raise HTTPException(404, "CSV desconocido")
    cols = list(filas[0].keys()) if filas else ["fuente_datos"]
    out = io.StringIO(); w = csv.DictWriter(out, fieldnames=cols); w.writeheader(); w.writerows(filas)
    return StreamingResponse(iter([out.getvalue()]), media_type="text/csv; charset=utf-8",
                             headers={"Content-Disposition": f'attachment; filename="credito_{tabla}_SINTETICO.csv"'})
