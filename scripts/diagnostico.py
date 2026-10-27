import os,sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
load_dotenv()
mode=os.getenv('ENGINE_MODE','mock')
checks=[('Python >=3.11',sys.version_info>=(3,11)), ('Modelos BPMN de ejemplo',len(list(Path('bpmn').glob('*.bpmn')))>=2), ('Reglas EARS',Path('especificaciones/01-requerimientos-EARS.md').exists()), ('Entorno (archivo .env)',Path('.env').exists())]
for label,good in checks:print(('OK' if good else 'FALTA'),label)
print('Modo:',mode)
if mode=='camunda':
 url=os.getenv('CAMUNDA_BASE_URL','').rstrip('/')+'/v2/topology'
 print('Comprobación sin credenciales:',url)
 print('Si usa OAuth, consultar /api/health desde backend para verificar token.')
if any(not good for _,good in checks):sys.exit(1)
