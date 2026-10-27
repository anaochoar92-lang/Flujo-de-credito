"""Prueba de humo HTTP de frontend, API, DB local y exportación; sin credenciales."""
import json
import os
import urllib.request
base=os.getenv('MVP_URL','http://127.0.0.1:8088').rstrip('/')
for path in ('/healthz','/api/health','/api/kpis','/api/export/casos.csv'):
    with urllib.request.urlopen(base+path,timeout=8) as result:
        body=result.read(200)
        print(f'{path}: HTTP {result.status} - {body[:90]!r}')
