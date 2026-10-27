"""Poblar tres expedientes 100% sintéticos llamando a FastAPI por HTTP.
Ejecutar: docker compose exec -T api python -m scripts.sembrar_contenedores
NO invocar en ENGINE_MODE=camunda: crearía instancias reales cloud.
"""
import os
import httpx

def main():
    if os.getenv('ENGINE_MODE', 'mock') != 'mock':
        raise SystemExit('Carga de demostración prohibida con Camunda real')
    base = os.getenv('DEMO_API_URL','http://127.0.0.1:8000')
    with httpx.Client(base_url=base, timeout=20.0) as http:
        existing = {c['radicado'] for c in http.get('/api/cases').raise_for_status().json()}
        for esc, chip, rad in [('ASIS','DEMO-CHIP-A','MBA-DOCKER-ASIS'),('TOBE','DEMO-CHIP-B','MBA-DOCKER-TOBE'),('TOBE','', 'MBA-DOCKER-EXCEPCION')]:
            if rad in existing:
                print('Ya existe:',rad);continue
            payload = {'radicado':rad,'escenario':esc,'chip':chip,'area_terreno_m2':450,'area_construida_m2':700,'uso':'residencial'}
            res=http.post('/api/cases',json=payload);res.raise_for_status();case=res.json()
            tasks_done=0
            for _ in range(5):
                tareas=http.get(f"/api/cases/{case['id']}/tasks").raise_for_status().json()
                if not tareas:break
                res=http.post(f"/api/cases/{case['id']}/tasks/{tareas[0]['key']}/complete",json={'actor':'docente-demo','observacion':'Evidencia sintética'})
                res.raise_for_status();tasks_done+=1
            else: raise AssertionError('Más de cinco pasos')
            status=http.get(f"/api/cases/{case['id']}").json()['estado']
            assert status=='FINALIZADO',status
            print('Caso',rad,'finalizado; tareas',tasks_done)

if __name__=='__main__': main()
