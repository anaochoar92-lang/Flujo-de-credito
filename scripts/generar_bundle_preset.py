#!/usr/bin/env python3
"""Crea un candidato de importación Preset/Superset con 2 dashboards/8 gráficos.

IMPORTANTE: no tiene acceso a Preset Starter y NO prueba la importación cloud.
Usa los YAML de datasets y bases exportados por el MISMO workspace para
anclar las referencias. NO requiere tokens, API, ni credenciales.

Uso:
  py scripts/generar_bundle_preset.py --export-datasets resumen.zip --export-datasets roi.zip --salida resultados/dashboard_candidato.zip
  py scripts/generar_bundle_preset.py --export-datasets datasets.zip --salida resultados/dashboard_candidato.zip --verificar

No generar exportes de bases falsos ni modificar credenciales.
"""
from __future__ import annotations
import argparse, collections, csv, datetime as dt, hashlib, io, json, os, re, sys, uuid, zipfile
from pathlib import Path
from typing import Any
try:
    import yaml
except ImportError:
    raise SystemExit('Falta PyYAML: instalar con py -m pip install -r requirements-preset.txt')

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / 'config' / 'preset_dashboard_maestro.json'
TABLES = {'resumen':'mba_resumen_mensual','roi':'mba_roi_mensual'}

class ErrorPaquete(ValueError): pass

def safe_entries(path:Path):
    if not zipfile.is_zipfile(path): raise ErrorPaquete(f'No es ZIP: {path}')
    with zipfile.ZipFile(path) as z:
        result=[]
        for item in z.infolist():
            p=item.filename.replace('\\','/')
            if item.is_dir():continue
            if p.startswith('/') or '..' in p.split('/') or (p and ':' in p.split('/')[0]):
                raise ErrorPaquete(f'Ruta insegura dentro del ZIP: {p}')
            if item.file_size>4_000_000:raise ErrorPaquete(f'Archivo YAML excesivo: {p}')
            if not p.endswith(('.yml','.yaml')):continue
            try: obj=yaml.safe_load(z.read(item))
            except yaml.YAMLError as exc: raise ErrorPaquete(f'YAML inválido en {p}: {exc}') from exc
            if isinstance(obj,dict): result.append((p,obj))
        return result

def load_sources(paths):
    resources={'datasets':{},'databases':{},'metadata':[]}
    for path in paths:
        for filename,obj in safe_entries(path):
            clean=filename.split('/')
            if filename.endswith('/metadata.yaml') or filename=='metadata.yaml':
                resources['metadata'].append(obj)
            for category in ('databases','datasets'):
                if category not in clean:continue
                idx=clean.index(category); relative='/'.join(clean[idx:])
                if 'uuid' not in obj:raise ErrorPaquete(f'{relative} no tiene UUID; use un ZIP real exportado desde Preset.')
                uid=str(obj['uuid'])
                if uid in resources[category] and resources[category][uid][1]!=obj:
                    raise ErrorPaquete(f'UUID repetido con definiciones diferentes: {uid}')
                resources[category][uid]=(relative,obj)
    return resources

def guard_connection_secrets(resources):
    """No distribuye accidentalmente secretos visibles en un ZIP del curso."""
    from urllib.parse import urlsplit
    masked = {'xxx','xxxxx','********','*****','<masked>','<password>','redacted',''}
    for _, obj in resources['databases'].values():
        if obj.get('password') not in (None, '', '********', 'XXXXX'):
            raise ErrorPaquete('Una base exportada contiene un campo password visible; NO se genera ZIP para estudiantes.')
        uri=str(obj.get('sqlalchemy_uri') or '')
        try:
            info=urlsplit(uri)
            password=info.password
        except ValueError:
            password=None
        if password is not None and password.lower() not in masked and set(password) not in ({'*'},{'x'},{'X'}):
            raise ErrorPaquete('La URI de una base contiene una contraseña visible; NO distribuya este export.')
        # Ciertas exportaciones incluyen campos adicionales sensibles que no deben distribuirse.
        for key in ('encrypted_extra','masked_encrypted_extra','ssh_tunnel'):
            if key in obj and obj[key] not in (None, '', {}):
                raise ErrorPaquete(f'La base incluye {key}; revise/remueva secretos ANTES de distribuir el ZIP.')

def map_datasets(resources, expected):
    mapping={}
    for key,table in expected.items():
        matches=[(name,obj) for name,obj in resources['datasets'].values()
                 if str(obj.get('table_name','')).lower()==table.lower()]
        if not matches:
            found=[x[1].get('table_name') for x in resources['datasets'].values()]
            raise ErrorPaquete(f'No está el dataset {table!r} en la exportación. Encontrados: {found}')
        if len(matches)!=1:raise ErrorPaquete(f'Nombre ambiguo: {table} coincide con {len(matches)} datasets')
        mapping[key]=matches[0]
    if not resources['databases']:
        raise ErrorPaquete('Faltan las dependencias databases/*.yaml. Exportar datasets CON sus bases.')
    for role,(fname,obj) in mapping.items():
        uid=str(obj.get('database_uuid') or '')
        if uid not in resources['databases']:
            raise ErrorPaquete(f'El dataset {role} hace referencia a una base UUID {uid!r} que NO está exportada.')
    return mapping

def check_csv(config:dict, folder:Path):
    report=[]
    for key,spec in config['datasets'].items():
        path=folder/spec['csv']
        if not path.exists():raise ErrorPaquete(f'CSV no encontrado: {path}')
        with path.open('r',encoding='utf-8-sig',newline='') as h:
            reader=csv.DictReader(h);found=reader.fieldnames or [];n=sum(1 for _ in reader)
        missing=sorted(set(spec['columns'])-set(found))
        if missing:raise ErrorPaquete(f'Columnas ausentes en {path.name}: {missing}')
        report.append({'csv':str(path),'filas':n,'columnas':len(found),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    return report

def metric(sql,label):
    return {'expressionType':'SQL','sqlExpression':sql,'label':label,'hasCustomLabel':True,'optionName':'metric_'+hashlib.md5(sql.encode()).hexdigest()[:12]}

def chart_params(spec, role):
    col=spec.get('dimension'); kind=spec['tipo']; sql=spec['sql']; expr=metric(sql,spec['nombre'])
    if kind=='big_number_total':
        return {'viz_type':'big_number_total','metric':expr,'header_font_size':0.38,'subheader':'DEMOSTRACIÓN • DATOS SINTÉTICOS','time_range':'No filter','y_axis_format':',.0f','show_timestamp':False}
    if kind=='echarts_timeseries_bar':
        # Un eje temporal auténtico requeriría columna DATE. Esta variante usa barra categórica,
        # y su portabilidad depende de la versión de ECharts de la instancia.
        return {'viz_type':'echarts_timeseries_bar','x_axis':col,'metrics':[expr],
                'groupby':spec.get('serie',[]),'time_range':'No filter','row_limit':10000,
                'show_legend':bool(spec.get('serie')),'rich_tooltip':True,'show_value':False,
                'orientation':'vertical','x_axis_sort_asc':True}
    raise ErrorPaquete('Gráfico no soportado '+str(kind))

def construct_chart(spec, dataset_obj):
    params=chart_params(spec,spec['dataset'])
    return {'slice_name':spec['nombre']+' — SINTÉTICO','description':spec['descripcion'],
            'viz_type':spec['tipo'],'params':params,'cache_timeout':None,
            'dataset_uuid':str(dataset_obj['uuid']),'uuid':str(uuid.uuid4()),'version':'1.0.0'}

def construct_dashboard(name, charts):
    """Dashboard grid 2 cols x 2 rows, basado en la estructura exportada por Superset."""
    dash_uuid=str(uuid.uuid4())
    position={'DASHBOARD_VERSION_KEY':'v2','ROOT_ID':{'type':'ROOT','id':'ROOT_ID','children':['GRID_ID']},
              'GRID_ID':{'type':'GRID','id':'GRID_ID','children':[]},
              'HEADER_ID':{'id':'HEADER_ID','type':'HEADER','meta':{'text':name}}}
    for row_num in (0,1):
        rid=f'ROW-{row_num+1:02d}';position['GRID_ID']['children'].append(rid)
        position[rid]={'type':'ROW','id':rid,'children':[], 'meta':{'background':'BACKGROUND_TRANSPARENT'},'parents':['ROOT_ID','GRID_ID']}
        for c in range(2):
            index=row_num*2+c;chart=charts[index]; cid=f'CHART-{index+1:02d}'
            position[rid]['children'].append(cid)
            position[cid]={'type':'CHART','id':cid,'children':[], 'meta':{'chartId':index+1,'width':6,'height':40,
                           'sliceName':chart['slice_name'],'uuid':chart['uuid']},
                           'parents':['ROOT_ID','GRID_ID',rid]}
    return {'dashboard_title':name,'description':'Práctica MBA con datos sintéticos; validar tablas/consultas tras importar.',
            'css':'','slug':None,'uuid':dash_uuid,'published':False,'version':'1.0.0',
            'position':position,
            'metadata':{'chart_configuration':{},'color_scheme':'','default_filters':'{}',
                        'native_filter_configuration':[],'refresh_frequency':0,'cross_filters_enabled':False,
                        'label_colors':{},'expanded_slices':{}}}

def audit_bundle(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        files={p:yaml.safe_load(z.read(p)) for p in z.namelist() if p.endswith('.yaml')}
    groups=collections.defaultdict(list)
    for p,obj in files.items():
        for t in ('dashboards','charts','datasets','databases'):
            if '/'+t+'/' in '/'+p:groups[t].append((p,obj))
    errs=[]; dsets={str(o.get('uuid')) for _,o in groups['datasets']}
    dbs={str(o.get('uuid')) for _,o in groups['databases']}
    charts={str(o.get('uuid')) for _,o in groups['charts']}
    for _,o in groups['datasets']:
        if str(o.get('database_uuid')) not in dbs:errs.append('Dataset carece de database UUID')
    for _,o in groups['charts']:
        if str(o.get('dataset_uuid')) not in dsets:errs.append('Chart carece de dataset UUID')
    for _,o in groups['dashboards']:
        for key,part in o['position'].items():
            if isinstance(part,dict) and part.get('type')=='CHART' and part.get('meta',{}).get('uuid') not in charts:
                errs.append('Dashboard carece de chart UUID '+str(key))
    if len(groups['charts'])!=8 or len(groups['dashboards'])!=2:errs.append('Conteo inesperado de charts/dashboards')
    return {'errores':errs,'dashboards':len(groups['dashboards']),'charts':len(groups['charts']),
            'datasets':len(groups['datasets']),'databases':len(groups['databases'])}

def generate(source_paths, output, configpath=DEFAULT_CONFIG, folder=ROOT/'datos'/'preset'):
    config=json.loads(Path(configpath).read_text(encoding='utf-8'))
    files_report=check_csv(config,Path(folder))
    sources=load_sources(source_paths);guard_connection_secrets(sources);mapped=map_datasets(sources, {k:v['tabla'] for k,v in config['datasets'].items()})
    bundle={'metadata.yaml':{'version':'1.0.0','type':'dashboard','timestamp':dt.datetime.now(dt.timezone.utc).isoformat()}}
    # Mantener fielmente los YAML exportados de Preset, salvo potenciales credenciales.
    # La exportación normalmente incluye URI enmascarada; nunca registrar / imprimir el valor.
    for key in ('databases','datasets'):
        for rel,obj in sources[key].values():
            if rel in bundle and bundle[rel]!=obj:raise ErrorPaquete(f'Colisión de ruta {rel}')
            bundle[rel]=obj
    chart_count=0
    for dashboard_spec in config['dashboards']:
        chartobjs=[]
        for spec in dashboard_spec['widgets']:
            chart_count+=1
            obj=construct_chart(spec,mapped[spec['dataset']][1]);chartobjs.append(obj)
            bundle[f"charts/mba_{chart_count:02d}.yaml"]=obj
        dash=construct_dashboard(dashboard_spec['titulo'],chartobjs)
        bundle[f"dashboards/mba_{len([x for x in bundle if x.startswith('dashboards/')])+1:02d}.yaml"]=dash
    outfile=Path(output);outfile.parent.mkdir(parents=True,exist_ok=True)
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for rel,obj in sorted(bundle.items()):
            z.writestr(rel,yaml.safe_dump(obj,allow_unicode=True,sort_keys=False,width=120))
    buf=stream.getvalue();audit=audit_bundle(buf)
    if audit['errores']:raise ErrorPaquete('Validación local falló: '+'; '.join(audit['errores']))
    outfile.write_bytes(buf)
    report={'estado':'CANDIDATO_NO_VERIFICADO_EN_PRESET',
            'nota':'Estructura comprobada localmente, requiere importación de prueba en Preset Starter y conexión de base de datos.',
            'exportaciones_fuente':[str(p) for p in source_paths], 'zip':str(outfile),
            'sha256':hashlib.sha256(buf).hexdigest(),'recursos':audit,'csv':files_report}
    outfile.with_suffix('.reporte.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--export-datasets',action='append',type=Path,required=True,help='ZIP real de datasets exportado de Preset; se puede repetir')
    ap.add_argument('--salida',type=Path,default=Path('resultados/dashboard_mba_CANDIDATO.zip'))
    ap.add_argument('--config',type=Path,default=DEFAULT_CONFIG)
    ap.add_argument('--csv',type=Path,default=ROOT/'datos'/'preset')
    args=ap.parse_args()
    try: report=generate(args.export_datasets,args.salida,args.config,args.csv)
    except (ErrorPaquete,FileNotFoundError,KeyError) as e:ap.error(str(e))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':sys.exit(main())
