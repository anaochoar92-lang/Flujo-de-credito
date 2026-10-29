"""MVP didáctico. Sin autenticación de usuarios; limitar a localhost en demo."""
import csv, io, json, os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from .db import Caso, Evento, setup_db
from .schemas import CasoNuevo, CompletarTarea
from .camunda import CamundaClient, CamundaError
from . import db as db_module
from .credito import router as credito_router, crear_vista_preset

load_dotenv()
MOCK_TASKS = {
    "ASIS": [("Registrar y cotejar documentos", "curaduria"), ("Validar áreas manualmente", "sdp"), ("Aprobar liquidación", "superior")],
    "TOBE": [("Subsanar información", "curaduria"), ("Revisar preliquidación", "sdp"), ("Aprobar liquidación", "superior")]
}

def now(): return datetime.now(timezone.utc)
def log(db, caso, accion, tarea=None, actor="sistema", detalles=None):
    db.add(Evento(caso_id=caso.id, accion=accion, tarea=tarea, actor=actor, detalles=json.dumps(detalles or {}, ensure_ascii=False)))

def current_tasks(caso):
    if caso.estado == "FINALIZADO": return []
    if caso.escenario == "ASIS":
        idx = caso.etapa_mock
    else:
        # si la prevalidación pasa, omitir subsanación; si no, mostrarla
        idx = caso.etapa_mock + (1 if caso.validacion_previa_ok else 0)
    if idx >= 3: return []
    label, role = MOCK_TASKS[caso.escenario][idx]
    return [{"key":f"mock-{caso.id}-{caso.etapa_mock}", "name":label, "role":role, "state":"CREATED", "elementId":f"Task_{idx}"}]

def calculate_demo(input: CasoNuevo):
    # NO es fórmula de liquidación legal; es solamente una estimación sintética para el taller.
    factor = {"residencial": 1.0, "comercial": 1.3, "mixto": 1.15}[input.uso]
    monto = round(input.area_construida_m2 * 12000 * factor, 2)
    valida = bool(input.chip and input.chip.strip()) and input.area_construida_m2 <= input.area_terreno_m2 * 8
    return monto, valida

@asynccontextmanager
async def lifespan(app):
    app.state.session_factory = setup_db()
    crear_vista_preset(db_module.engine)
    app.state.camunda = CamundaClient()
    yield

app = FastAPI(title="MBA · Liquidación de cargas urbanísticas (MVP didáctico)", lifespan=lifespan)
app.include_router(credito_router)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

def serialize(c):
    return {"id":c.id,"radicado":c.radicado,"escenario":c.escenario,"estado":c.estado,
            "bpmn_id":c.bpmn_id,"instance_key":c.instance_key,"area_terreno_m2":c.area_terreno_m2,
            "area_construida_m2":c.area_construida_m2,"chip":c.chip,"uso":c.uso,
            "valor_referencia_demo":c.valor_referencia_demo,"validacion_previa_ok":c.validacion_previa_ok,
            "creado_en":c.creado_en.isoformat(),"cerrado_en":c.cerrado_en.isoformat() if c.cerrado_en else None}

def db_session(req: Request): return req.app.state.session_factory()
def mode(): return os.getenv("ENGINE_MODE", "mock").lower()

@app.get("/")
def home(): return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.get("/credito")
def credito_home(): return FileResponse(os.path.join(os.path.dirname(__file__), "static", "credito.html"))

@app.get("/api/health")
def health(req: Request):
    """Readiness local exclusivamente; no depende de la conectividad con Camunda Cloud."""
    try:
        with db_session(req) as db:
            db.execute(text("SELECT 1"))
        return {"status": "ok", "engine": mode(), "database": "ok", "camunda": "verificar_por_separado"}
    except Exception:
        raise HTTPException(503, "Base de datos no disponible")

@app.get("/api/health/camunda")
def health_camunda(req: Request):
    if mode() != "camunda":
        return {"status": "no_aplica", "engine": "mock"}
    try:
        return {"status": "ok", "topology": req.app.state.camunda.health()}
    except CamundaError as e:
        raise HTTPException(502, f"Camunda no accesible: {e}")

@app.post("/api/cases",status_code=201)
def create_case(payload: CasoNuevo, req: Request):
    if mode() not in ("mock","camunda"): raise HTTPException(500,"ENGINE_MODE debe ser mock o camunda")
    amount, valid = calculate_demo(payload)
    process_id = os.getenv("CAMUNDA_PROCESS_ASIS" if payload.escenario=="ASIS" else "CAMUNDA_PROCESS_TOBE", "liquidacion_cargas_asis_mba" if payload.escenario=="ASIS" else "liquidacion_cargas_tobe_mba")
    with db_session(req) as db:
        c = Caso(radicado=payload.radicado, escenario=payload.escenario,bpmn_id=process_id,
                 area_terreno_m2=payload.area_terreno_m2,area_construida_m2=payload.area_construida_m2,
                 uso=payload.uso,chip=payload.chip,validacion_previa_ok=valid,
                 valor_referencia_demo=amount)
        db.add(c);db.flush()
        log(db,c,"RADICADO_CREADO",detalles={"origen":"front"})
        log(db,c,"PREVALIDACION_AUTOMATICA",detalles={"ok":valid,"valor_sintetico":amount})
        if mode()=="camunda":
            vars_ = {"casoId":str(c.id),"radicado":c.radicado,"escenario":c.escenario,
                     "areaTerrenoM2":c.area_terreno_m2,"areaConstruidaM2":c.area_construida_m2,
                     "uso":c.uso,"chip":c.chip or "", "validacionPreviaOk":valid,
                     "valorReferenciaDemo":amount}
            try:
                result=req.app.state.camunda.start(process_id,vars_)
                c.instance_key=str(result["processInstanceKey"])
            except (CamundaError,KeyError) as ex:
                # NO se confirma la transacción local si falla la orquestación.
                db.rollback();raise HTTPException(502, f"No se pudo iniciar Camunda: {ex}")
        else: c.instance_key=f"DEMO-{c.id}"
        log(db,c,"INSTANCIA_INICIADA",detalles={"instance_key":c.instance_key,"bpmn":process_id})
        db.commit();return serialize(c)

@app.get("/api/cases")
def cases(req:Request):
    with db_session(req) as db:
        return [serialize(c) for c in db.scalars(select(Caso).order_by(Caso.id.desc()).limit(100)).all()]

@app.get("/api/cases/{case_id}")
def case(case_id:int,req:Request):
    with db_session(req) as db:
        c=db.get(Caso,case_id)
        if not c: raise HTTPException(404,"Caso no encontrado")
        return serialize(c)

@app.post("/api/cases/{case_id}/sync")
def sync_case(case_id: int, req: Request):
    """Conciliación explícita Camunda→DB para métricas locales. No es una suscripción a eventos."""
    with db_session(req) as db:
        c=db.get(Caso,case_id)
        if not c: raise HTTPException(404,"Caso no encontrado")
        if mode() != "camunda":
            return {"caso":serialize(c), "sincronizado":False, "detalle":"Modo DEMO no requiere sincronización"}
        if not c.instance_key or not c.instance_key.isdigit():
            raise HTTPException(409,"Este caso no tiene clave de instancia Camunda real")
        try:
            remote=req.app.state.camunda.status(c.instance_key)
        except CamundaError as e:
            raise HTTPException(502, f"No se pudo consultar el proceso en Camunda: {e}")
        state=remote.get("state")
        if state in ("COMPLETED","TERMINATED") and c.estado not in ("FINALIZADO","CANCELADO"):
            c.estado="FINALIZADO" if state=="COMPLETED" else "CANCELADO"
            ended=remote.get("endDate")
            c.cerrado_en=(datetime.fromisoformat(ended.replace("Z","+00:00")) if ended else now())
            log(db,c,"ESTADO_CONCILIADO_CAMUNDA",detalles={"estado_remoto":state})
            db.commit()
        return {"caso":serialize(c), "sincronizado":True,"estado_remoto":state,
                "nota":"Camunda REST v2 es eventualmente consistente; repetir consulta si el estado aún no aparece."}

@app.get("/api/cases/{case_id}/tasks")
def tasks(case_id:int,req:Request):
    with db_session(req) as db:
        c=db.get(Caso,case_id)
        if not c: raise HTTPException(404,"Caso no encontrado")
        if mode()=="mock":return current_tasks(c)
        try:
            result=req.app.state.camunda.tasks(c.instance_key)
            return [{"key":str(t.get("userTaskKey")),"name":t.get("name") or t.get("elementId") or "Tarea humana",
                     "role":t.get("assignee") or "Por asignar", "state":t.get("state"),"elementId":t.get("elementId")}
                    for t in result]
        except CamundaError as e: raise HTTPException(502,str(e))

@app.post("/api/cases/{case_id}/tasks/{task_key}/complete")
def complete(case_id:int,task_key:str,payload:CompletarTarea,req:Request):
    with db_session(req) as db:
        c=db.get(Caso,case_id)
        if not c:raise HTTPException(404,"Caso no encontrado")
        if c.estado=="FINALIZADO": raise HTTPException(409,"Caso ya finalizado")
        variables={"aprobado":payload.aprobado,"observacion":payload.observacion,"actorDemo":payload.actor}
        if mode()=="mock":
            offered=current_tasks(c)
            if not offered or offered[0]["key"]!=task_key:raise HTTPException(409,"Tarea desactualizada")
            if c.escenario=="TOBE" and not c.validacion_previa_ok and c.etapa_mock==0:
                log(db,c,"SUBSANACION_REALIZADA",actor=payload.actor)
            c.etapa_mock+=1
            done=not current_tasks(c)
            if done:
                c.estado="FINALIZADO";c.cerrado_en=now()
        else:
            try:
                allowed={str(t.get("userTaskKey")) for t in req.app.state.camunda.tasks(c.instance_key)}
                if task_key not in allowed:raise HTTPException(409,"La tarea no pertenece al caso o no está activa")
                req.app.state.camunda.complete(task_key,variables)
            except CamundaError as e: raise HTTPException(502,str(e))
        log(db,c,"TAREA_COMPLETADA",tarea=task_key,actor=payload.actor,detalles=variables)
        db.commit()
        return {"ok":True,"caso":serialize(c)}

@app.get("/api/events")
def events(req:Request):
    with db_session(req) as db:
        rows=db.scalars(select(Evento).order_by(Evento.id.desc()).limit(150)).all()
        return [{"id":e.id,"caso_id":e.caso_id,"momento":e.momento.isoformat(),"accion":e.accion,"tarea":e.tarea,"actor":e.actor} for e in rows]

@app.get("/api/kpis")
def kpis(req:Request):
    with db_session(req) as db:
        casos=db.scalars(select(Caso)).all()
        by={}
        for esc in ("ASIS","TOBE"):
            cc=[c for c in casos if c.escenario==esc]
            cerrados=[c for c in cc if c.cerrado_en]
            durations=[(c.cerrado_en.replace(tzinfo=timezone.utc) if c.cerrado_en.tzinfo is None else c.cerrado_en).__sub__(c.creado_en.replace(tzinfo=timezone.utc) if c.creado_en.tzinfo is None else c.creado_en).total_seconds()/60 for c in cerrados]
            by[esc]={"casos":len(cc),"terminados":len(cerrados),"porcentaje_cierre":round(100*len(cerrados)/len(cc),2) if cc else 0,
                     "minutos_promedio":round(sum(durations)/len(durations),2) if durations else None,
                     "casos_prevalidacion_ok":sum(c.validacion_previa_ok for c in cc)}
        return {"escenarios":by,"nota":"Duración observada de la demo, no tiempo productivo ni ROI empresarial."}

@app.get("/api/export/{table}.csv")
def export(table:str,req:Request):
    if table not in ("casos","eventos","kpis"):raise HTTPException(404,"CSV desconocido")
    if table=="kpis":
        data=kpis(req)["escenarios"]
        cols=["escenario","casos","terminados","porcentaje_cierre","minutos_promedio","casos_prevalidacion_ok"]
        rows=[{"escenario":k,**v} for k,v in data.items()]
    elif table=="casos":
        rows=cases(req);cols=["id","radicado","escenario","estado","area_terreno_m2","area_construida_m2","uso","valor_referencia_demo","creado_en","cerrado_en"]
    else:
        rows=events(req);cols=["id","caso_id","momento","accion","tarea","actor"]
    out=io.StringIO();w=csv.DictWriter(out,fieldnames=cols,extrasaction="ignore");w.writeheader();w.writerows(rows)
    return StreamingResponse(iter([out.getvalue()]),media_type="text/csv; charset=utf-8",headers={"Content-Disposition":f'attachment; filename="mba_{table}.csv"'})

@app.post("/api/cases/{case_id}/rerun",status_code=201)
def rerun(case_id:int,req:Request,escenario:str="TOBE"):
    """Inicia otra instancia desde la ficha del caso, sin mutar ni pisar la anterior."""
    if escenario not in ("ASIS","TOBE"): raise HTTPException(422,"Escenario inválido")
    with db_session(req) as db:
        c=db.get(Caso,case_id)
        if not c: raise HTTPException(404,"Caso no encontrado")
        payload=CasoNuevo(radicado=c.radicado+"-R",escenario=escenario,area_terreno_m2=c.area_terreno_m2,
            area_construida_m2=c.area_construida_m2,uso=c.uso,chip=c.chip)
    return create_case(payload,req)
