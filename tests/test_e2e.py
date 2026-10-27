import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL",f"sqlite:///{tmp_path/'test.sqlite3'}")
    monkeypatch.setenv("ENGINE_MODE","mock")
    with TestClient(app) as c: yield c

@pytest.mark.parametrize("esc,chip,expected_tasks", [("ASIS","ABC",3),("TOBE","ABC",2),("TOBE","",3)])
def test_case_full_lifecycle(client,esc,chip,expected_tasks):
    r=client.post("/api/cases",json={"radicado":"RAD-DEMO-001","escenario":esc,
      "area_terreno_m2":100.0,"area_construida_m2":200.0,"uso":"residencial","chip":chip})
    assert r.status_code==201, r.text
    case=r.json(); assert case["valor_referencia_demo"]==2_400_000
    cid=case["id"]
    labels=[]
    for i in range(expected_tasks):
        t=client.get(f"/api/cases/{cid}/tasks").json()
        assert len(t)==1
        labels.append(t[0]["name"])
        done=client.post(f"/api/cases/{cid}/tasks/{t[0]['key']}/complete",json={"actor":"estudiante","observacion":"OK"})
        assert done.status_code==200,done.text
    assert client.get(f"/api/cases/{cid}/tasks").json()==[]
    assert client.get(f"/api/cases/{cid}").json()["estado"]=="FINALIZADO"
    assert client.get("/api/export/casos.csv").status_code==200
    assert "PREVALIDACION_AUTOMATICA" in client.get("/api/export/eventos.csv").text
    assert client.get("/api/export/kpis.csv").status_code==200
    assert len(labels)==expected_tasks

def test_invalid_area(client):
    assert client.post('/api/cases',json={'radicado':'RAD1','area_terreno_m2':0,'area_construida_m2':5,'uso':'residencial','escenario':'ASIS'}).status_code==422

def test_safe_wrong_task(client):
    cid=client.post('/api/cases',json={'radicado':'RAD1','area_terreno_m2':100,'area_construida_m2':5,'uso':'residencial','escenario':'ASIS'}).json()['id']
    assert client.post(f'/api/cases/{cid}/tasks/mock-wrong/complete',json={'actor':'estudiante'}).status_code==409

def test_secondary_front_launch(client):
    original=client.post('/api/cases',json={'radicado':'RAD22','area_terreno_m2':200,'area_construida_m2':200,'uso':'comercial','escenario':'ASIS'}).json()
    other=client.post(f'/api/cases/{original["id"]}/rerun?escenario=TOBE').json()
    assert other['id']!=original['id'] and other['escenario']=='TOBE'
    assert other['radicado'].endswith('-R')
    assert len(client.get('/api/cases').json())==2

def test_camunda_adapter_contract_without_network(client, monkeypatch):
    monkeypatch.setenv('ENGINE_MODE','camunda')
    from app.camunda import CamundaClient
    calls=[]
    def start(self, pid, variables):
        calls.append(('start',pid,variables))
        return {'processInstanceKey':'2251799813686001'}
    def tasks(self, key):
        calls.append(('tasks',key))
        return [{'userTaskKey':'2251799813686201','name':'Revisar preliquidación','state':'CREATED'}]
    def complete(self,key,vars):
        calls.append(('complete',key,vars));return {}
    monkeypatch.setattr(CamundaClient,'start',start)
    monkeypatch.setattr(CamundaClient,'tasks',tasks)
    monkeypatch.setattr(CamundaClient,'complete',complete)
    c=client.post('/api/cases',json={'radicado':'CAM-DEMO','area_terreno_m2':200,'area_construida_m2':300,'uso':'residencial','escenario':'TOBE','chip':'FAKE'}).json()
    assert c['instance_key']=='2251799813686001'
    t=client.get(f'/api/cases/{c["id"]}/tasks').json()
    assert t[0]['key']=='2251799813686201'
    r=client.post(f'/api/cases/{c["id"]}/tasks/{t[0]["key"]}/complete',json={'actor':'profesional','observacion':'Verificado'})
    assert r.status_code==200
    assert any(x[0]=='complete' for x in calls)
