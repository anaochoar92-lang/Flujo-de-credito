"""ETL reproducible a archivos CSV para Preset Starter.

Ejecución: docker compose run --rm etl
O Python local: python -m scripts.etl_preset --out ./exports

Los CSV no incluyen CHIP, radicado real, detalles privados ni secretos.
Métricas calculadas sobre hechos registrados en la BD; no inventan horas liberadas.
"""
import argparse
import csv
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select
from app.db import Caso, Evento, setup_db

FIELDS = {
    'preset_casos.csv': ['caso_id','radicado_pseudo','escenario','estado','uso','area_terreno_m2',
                         'area_construida_m2','prevalidacion_ok','valor_referencia_sintetico_cop',
                         'fecha_creacion_utc','fecha_cierre_utc','duracion_ciclo_min'],
    'preset_eventos.csv': ['evento_id','caso_id','escenario','momento_utc','accion','tarea','actor_pseudo'],
    'preset_kpis_mensuales.csv': ['mes','escenario','casos_iniciados','casos_finalizados','tasa_finalizacion_pct',
                                'casos_prevalidacion_ok','tasa_prevalidacion_pct','duracion_media_ciclo_min',
                                'monto_referencia_sintetico_medio_cop'],
    'preset_actividades.csv': ['mes','escenario','accion','numero_eventos'],
}

def iso(d):
    if not d: return ''
    if d.tzinfo is None: d=d.replace(tzinfo=timezone.utc)
    return d.astimezone(timezone.utc).isoformat(timespec='seconds')

def minutes(a,b):
    if not a or not b: return ''
    if a.tzinfo is None: a=a.replace(tzinfo=timezone.utc)
    if b.tzinfo is None: b=b.replace(tzinfo=timezone.utc)
    return round((b-a).total_seconds()/60,3)

def pseudo(value,prefix='REF'):
    seed=os.getenv('EXPORT_PSEUDO_SALT','mba-demo-ETL')
    return prefix+'-'+hashlib.sha256((seed+'|'+str(value)).encode()).hexdigest()[:12].upper()

def safe_text(v):
    s=str(v if v is not None else '')
    # Protección básica contra CSV injection si se abre en hojas de cálculo.
    return "'"+s if s and s.lstrip().startswith(('=','+','-','@')) else s

def produce(session_factory, out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with session_factory() as db:
        casos=db.scalars(select(Caso).order_by(Caso.id)).all()
        eventos=db.scalars(select(Evento).order_by(Evento.id)).all()
    by_id={c.id:c for c in casos}
    result={name:[] for name in FIELDS}
    month=defaultdict(list)
    activities=defaultdict(int)
    for c in casos:
        m=iso(c.creado_en)[:7]
        duration=minutes(c.creado_en,c.cerrado_en)
        result['preset_casos.csv'].append({
            'caso_id':c.id,'radicado_pseudo':pseudo(c.radicado,'RAD'),
            'escenario':c.escenario,'estado':c.estado,'uso':c.uso,
            'area_terreno_m2':c.area_terreno_m2,'area_construida_m2':c.area_construida_m2,
            'prevalidacion_ok':int(bool(c.validacion_previa_ok)),
            'valor_referencia_sintetico_cop':c.valor_referencia_demo,
            'fecha_creacion_utc':iso(c.creado_en),'fecha_cierre_utc':iso(c.cerrado_en),
            'duracion_ciclo_min':duration})
        month[(m,c.escenario)].append(c)
    for e in eventos:
        c=by_id.get(e.caso_id)
        if c is None: continue
        m=iso(e.momento)[:7]
        result['preset_eventos.csv'].append({
            'evento_id':e.id,'caso_id':e.caso_id,'escenario':c.escenario,
            'momento_utc':iso(e.momento),'accion':safe_text(e.accion),
            'tarea':safe_text(e.tarea),'actor_pseudo':pseudo(e.actor,'USR')})
        activities[(m,c.escenario,e.accion)] += 1
    for (m,esc), cc in sorted(month.items()):
        ended=[c for c in cc if c.estado=='FINALIZADO' and c.cerrado_en]
        durations=[minutes(c.creado_en,c.cerrado_en) for c in ended]
        amounts=[c.valor_referencia_demo or 0 for c in cc]
        valid=sum(bool(c.validacion_previa_ok) for c in cc)
        result['preset_kpis_mensuales.csv'].append({
            'mes':m,'escenario':esc,'casos_iniciados':len(cc),'casos_finalizados':len(ended),
            'tasa_finalizacion_pct':round(100*len(ended)/len(cc),2),
            'casos_prevalidacion_ok':valid,'tasa_prevalidacion_pct':round(100*valid/len(cc),2),
            'duracion_media_ciclo_min':round(sum(durations)/len(durations),3) if durations else '',
            'monto_referencia_sintetico_medio_cop':round(sum(amounts)/len(amounts),2)})
    for (m,esc,accion),count in sorted(activities.items()):
        result['preset_actividades.csv'].append({'mes':m,'escenario':esc,'accion':safe_text(accion),'numero_eventos':count})

    # Ficheros transitorios para que un error no deje CSV truncado.
    files=[]
    for filename,rows in result.items():
        fd,tmp=tempfile.mkstemp(prefix='.tmp-', suffix='.csv',dir=out)
        with os.fdopen(fd,'w',encoding='utf-8-sig',newline='') as fp:
            writer=csv.DictWriter(fp, fieldnames=FIELDS[filename], extrasaction='ignore')
            writer.writeheader();writer.writerows(rows)
        files.append((tmp,out/filename))
    for temp,final in files: os.replace(temp,final)
    manifest={
        'generado_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'esquema_exportacion':'mba-etl-v1','escenario':os.getenv('ENGINE_MODE','mock'),
        'fuente':'base de datos local del MVP',
        'anonimizacion':'pseudonimizacion de radicados y actores; CHIP y detalles excluidos',
        'advertencia':'Datos demo: valor_referencia_sintetico no es una liquidacion legal. No calcular ROI observado sin bases reales.',
        'csv':{filename:{'filas':len(rows),'sha256':hashlib.sha256((out/filename).read_bytes()).hexdigest(),
                          'columnas':FIELDS[filename]} for filename,rows in result.items()}
    }
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest

def main():
    ap=argparse.ArgumentParser(description='ETL Postgres/SQLite → CSV para Preset Starter')
    ap.add_argument('--out',default='./exports')
    args=ap.parse_args()
    session_factory=setup_db()
    report=produce(session_factory,args.out)
    for name,details in report['csv'].items():print(f'{name}: {details["filas"]} filas')
    print('Exportación finalizada:',Path(args.out).resolve())
if __name__=='__main__':main()
