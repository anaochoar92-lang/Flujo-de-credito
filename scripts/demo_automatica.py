"""Evidencia offline de fin a fin sin servicios externos ni credenciales."""
import os, sys, tempfile, json
from pathlib import Path
from fastapi.testclient import TestClient
os.environ['ENGINE_MODE']='mock'
with tempfile.TemporaryDirectory(prefix='mba-demo-') as td:
    os.environ['DATABASE_URL']=f'sqlite:///{Path(td)/"demo.db"}'
    from app.main import app
    with TestClient(app) as c:
        cases=[]
        for esc,chip in [('ASIS','AAA-111'),('TOBE','AAA-222'),('TOBE',None)]:
            p={'radicado':f'MBA-{esc}-{len(cases)+1:03}','escenario':esc,'chip':chip,
            'area_terreno_m2':450,'area_construida_m2':700,'uso':'residencial'}
            r=c.post('/api/cases',json=p);assert r.status_code==201,r.text
            case=r.json();cnt=0
            while 1:
                ts=c.get(f'/api/cases/{case["id"]}/tasks').json()
                if not ts:break
                result=c.post(f'/api/cases/{case["id"]}/tasks/{ts[0]["key"]}/complete',json={'actor':'docente','observacion':'Demo offline'})
                assert result.status_code==200,result.text
                cnt+=1
                assert cnt<=3,'Bucle inesperado'
            case=c.get(f'/api/cases/{case["id"]}').json()
            assert case['estado']=='FINALIZADO'
            cases.append({'caso_id':case['id'],'escenario':esc,'instancia':case['instance_key'],'tareas':cnt,'estado':case['estado']})
        root=Path('examples/exports');root.mkdir(parents=True,exist_ok=True)
        for table in ['casos','eventos','kpis']:
            response=c.get(f'/api/export/{table}.csv'); assert response.status_code==200
            (root/f'mba_{table}_sintetico.csv').write_text(response.text,encoding='utf8')
        (root/'evidencia_demo.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf8')
        print('RESULTADO: 3 casos FINALIZADOS; tareas completadas:',[c['tareas'] for c in cases])
        print('Archivos CSV sintéticos y evidencia:',root.resolve())
        print('NOTA: solo motor mock; no demuestra integración real Camunda ni Preset.')
