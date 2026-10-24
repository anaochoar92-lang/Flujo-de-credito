#!/usr/bin/env python3
"""Migra SOLO los archivos de trabajo de fase 1 a fase 2, sin sobreescrituras.
Uso: py scripts/migrar_trabajos_fase1.py --origen C:\\ruta\\kit-anterior --destino . --dry-run
     py scripts/migrar_trabajos_fase1.py --origen C:\\ruta\\kit-anterior --destino .
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

FOLDERS = {f"{i:02d}-{name}" for i, name in enumerate(
    ['fuentes', 'analisis', 'ears', 'modelo', 'bpmn', 'revision'], start=1)}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origen', required=True, type=Path, help='Raíz del kit antiguo que contiene trabajos/')
    p.add_argument('--destino', default=Path('.'), type=Path, help='Raíz del kit nuevo que contiene trabajos/')
    p.add_argument('--dry-run', action='store_true', help='Simular sin copiar nada')
    p.add_argument('--reporte', type=Path, help='Guardar reporte JSON (sólo al copiar)')
    a=p.parse_args()
    root_from=a.origen.expanduser().resolve();root_to=a.destino.expanduser().resolve()
    src=root_from/'trabajos';dst=root_to/'trabajos'
    if root_from==root_to:
        print('ERROR: --origen y --destino deben ser carpetas diferentes; evita mezclar kits.', file=sys.stderr);return 2
    if not src.is_dir():
        print(f'ERROR: no se encuentra {src}', file=sys.stderr);return 2
    if not dst.is_dir() or not (root_to/'.opencode'/'skills').is_dir():
        print(f'ERROR: el destino {root_to} no parece el kit nuevo completo.', file=sys.stderr);return 2
    projects=[d for d in sorted(src.iterdir()) if d.is_dir()]
    if not projects:
        print('ERROR: no hay proyectos en el origen.', file=sys.stderr);return 2
    found=[];same=[];conflicts=[]
    for pr in projects:
        for folder in sorted(FOLDERS):
            sub=pr/folder
            if not sub.exists():continue
            for f in sorted(sub.rglob('*')):
                if not f.is_file() or f.name == '.gitkeep':continue
                relative=f.relative_to(src);target=dst/relative
                entry={'origen':str(f), 'destino':str(target), 'sha256':digest(f)}
                if target.is_file():
                    (same if digest(target)==entry['sha256'] else conflicts).append(entry)
                elif target.exists():
                    conflicts.append(entry)
                else:
                    found.append(entry)
    print('Proyectos detectados:', ', '.join(pr.name for pr in projects))
    print('Archivos nuevos:',len(found),'| Ya presentes e idénticos:',len(same),'| Conflictos:',len(conflicts))
    for v in found:print(' +',Path(v['destino']).relative_to(root_to))
    for v in conflicts:print(' ! COLISIÓN:',Path(v['destino']).relative_to(root_to))
    if conflicts:
        print('No se copia nada: existe al menos un archivo destino diferente. Revisar manualmente las colisiones.',file=sys.stderr)
        return 3
    if a.dry_run:
        print('Simulación terminada: NO se han cambiado archivos. Quita --dry-run para copiar.');return 0
    for entry in found:
        src_file=Path(entry['origen']);dest_file=Path(entry['destino'])
        dest_file.parent.mkdir(parents=True,exist_ok=True)
        # Extra safety when another process created the target after the dry run.
        if dest_file.exists():
            print(f'ERROR: apareció un destino durante la copia: {dest_file}',file=sys.stderr);return 4
        shutil.copy2(src_file,dest_file)
        if digest(dest_file)!=entry['sha256']:
            print(f'ERROR: verificación de copia fallida: {dest_file}',file=sys.stderr);return 5
    report={'desde':str(root_from),'hacia':str(root_to),'copiados':found,'identicos':same,'conflictos':[]}
    if a.reporte:
        rp=a.reporte.expanduser().resolve();rp.parent.mkdir(parents=True,exist_ok=True)
        rp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Migración completada. Skills y comandos del kit nuevo se conservaron sin cambios.');return 0

if __name__=='__main__':raise SystemExit(main())
