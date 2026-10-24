#!/usr/bin/env python3
"""Prepara archivos de clase para importar en Preset; no crea exports falsos.

Si se entrega un ZIP real exportado desde Preset/Superset, verifica la estructura,
lo copia sin alterarlo y adjunta los CSV por separado. NO garantiza conexión de BD.

py scripts/preparar_distribucion_preset.py --datos datos/preset --salida distribucion-preset
py scripts/preparar_distribucion_preset.py --datos datos/preset --export C:\\dashboard-export.zip --salida distribucion-preset
"""
from __future__ import annotations
import argparse,csv,hashlib,json,shutil,sys,zipfile
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect_export(path):
    if not zipfile.is_zipfile(path):raise ValueError('El archivo no es ZIP válido.')
    with zipfile.ZipFile(path) as z:
        names=[i.filename.replace('\\','/') for i in z.infolist() if not i.is_dir()]
        if not names: raise ValueError('ZIP vacío')
        if any(n.startswith('/') or '..' in n.split('/') or ':' in n.split('/')[0] for n in names):
            raise ValueError('ZIP contiene rutas inseguras')
        def matches(key):return [n for n in names if '/'+key+'/' in '/'+n and n.lower().endswith(('.yaml','.yml'))]
        groups={x:matches(x) for x in ['databases','datasets','charts','dashboards']}
        metadata=[n for n in names if n.split('/')[-1]=='metadata.yaml']
        if not groups['dashboards'] or not groups['charts']:
            raise ValueError('No parece un export de dashboard de Preset/Superset: faltan dashboards/*.yaml o charts/*.yaml')
        if not metadata:raise ValueError('No se encontró metadata.yaml en el ZIP exportado.')
        forbidden=['.exe','.dll','.bat','.ps1','.js','.sh']
        if any(n.lower().endswith(tuple(forbidden)) for n in names):
            raise ValueError('Export sospechoso: contiene archivos ejecutables no habituales en un ZIP de dashboard')
        return {'recursos':{k:len(v) for k,v in groups.items()},'metadata':metadata,'archivos':len(names)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--datos',type=Path, default=Path('datos/preset'))
    p.add_argument('--export',type=Path, help='ZIP real de dashboards exportado por Preset/Superset')
    p.add_argument('--salida',type=Path,default=Path('distribucion-preset'))
    a=p.parse_args()
    if not a.datos.is_dir():p.error(f'No existe carpeta de CSV {a.datos}')
    csvfiles=sorted(a.datos.glob('*.csv'))
    if not csvfiles:p.error('No se encontraron CSV')
    dest=a.salida.resolve();dest.mkdir(parents=True,exist_ok=True)
    summary={'csv':[],'dashboard_zip':None,'estado_importacion':'pendiente de plantilla ZIP oficial exportada'}
    for f in csvfiles:
        with f.open('r',encoding='utf-8-sig',newline='') as h:
            data=csv.DictReader(h);header=data.fieldnames;rows=sum(1 for _ in data)
        copy=dest/f.name
        if copy.resolve()!=f.resolve():shutil.copy2(f,copy)
        summary['csv'].append({'nombre':f.name,'columnas':header,'filas':rows,'sha256':sha(copy)})
    if a.export:
        if not a.export.is_file():p.error(f'No existe {a.export}')
        try:inf=inspect_export(a.export)
        except ValueError as e:p.error(str(e))
        exportfile=dest/'dashboard_preset_importable.zip'
        if a.export.resolve()!=exportfile.resolve():shutil.copy2(a.export,exportfile)
        summary['dashboard_zip']={'nombre':exportfile.name,'sha256':sha(exportfile),'estructura':inf}
        summary['estado_importacion']='ZIP exportado real preparado; aún falta validar datasets y conexión en el workspace destino'
    (dest/'manifest.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    (dest/'LEEME.md').write_text('''# Distribución para Preset Starter\n\n1. Los CSV contienen registros y se suben por **Upload CSV**, no por Import Dashboard.\n2. Si existe `dashboard_preset_importable.zip`, fue copiado **sin modificar** desde un export Preset/Superset provisto por el docente. Se sube por **Dashboards > Import**.\n3. El ZIP de dashboard contiene definiciones (gráficos, datasets y conexiones), pero NO contiene las filas CSV ni las contraseñas de conexión.\n4. Si en el nuevo workspace no existen las tablas o la conexión, configurar sus dependencias. Un ZIP válido no garantiza que los gráficos puedan consultar datos.\n5. Validar en una cuenta Starter limpia ANTES de distribuir a la clase.\n6. Si no existe `dashboard_preset_importable.zip`, falta realizar una única vez la creación y exportación del tablero de referencia en Preset o Superset. NO se fabrica un ZIP falso.\n\nDocumentación: https://docs.preset.io/docs/migrating-dashboards\n''',encoding='utf-8')
    print(json.dumps({'salida':str(dest),'csv':len(csvfiles),'zip_preset':bool(a.export)},ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
