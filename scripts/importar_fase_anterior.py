"""Copia SOP/EARS/BPMN de fase previa sin sustituir material de la demostración."""
import argparse, shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--origen',required=True,help='Carpeta trabajos/<nombre-proyecto> del kit previo')
a=p.parse_args();src=Path(a.origen);dst=Path('contexto/fuentes-previas');dst.mkdir(parents=True,exist_ok=True)
for d in ['01-fuentes','02-analisis','03-ears','04-modelo','05-bpmn','06-revision','08-tobe']:
 s=src/d
 if not s.exists():continue
 for x in s.rglob('*'):
  if not x.is_file():continue
  rel=Path(d)/x.relative_to(s);out=dst/rel
  if out.exists():print('YA EXISTE, NO SE SOBRESCRIBE:',out);continue
  out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(x,out);print('COPIADO',out)
