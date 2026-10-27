"""Pruebas ejecutables SIN Docker. La prueba real del contenedor necesita Docker Desktop."""
import csv
import hashlib
import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from scripts.etl_preset import produce, pseudo


def test_export_includes_no_sensitive_fields(tmp_path, monkeypatch):
    monkeypatch.setenv('DATABASE_URL',f'sqlite:///{tmp_path / "etl.sqlite3"}')
    monkeypatch.delenv('DB_HOST',raising=False)
    monkeypatch.setenv('ENGINE_MODE','mock')
    with TestClient(app) as client:
        payload={'radicado':'RAD-SENSIBLE-123','escenario':'TOBE','chip':'CHIP-MUY-PRIVADO',
                 'area_terreno_m2':100,'area_construida_m2':250,'uso':'comercial'}
        r=client.post('/api/cases',json=payload)
        assert r.status_code==201,r.text
        case=r.json()
        tasks=client.get(f'/api/cases/{case["id"]}/tasks').json()
        assert tasks
        r=client.post(f'/api/cases/{case["id"]}/tasks/{tasks[0]["key"]}/complete',json={'actor':'NOMBRE_PERSONAL_REAL'})
        assert r.status_code==200
        report=produce(client.app.state.session_factory,tmp_path/'exports')
        assert report['csv']['preset_casos.csv']['filas']==1
        assert report['csv']['preset_eventos.csv']['filas']>=3
        assert report['csv']['preset_kpis_mensuales.csv']['filas']==1
        out=tmp_path/'exports'
        for f,details in report['csv'].items():
            data=(out/f).read_bytes()
            assert hashlib.sha256(data).hexdigest()==details['sha256']
            assert 'CHIP-MUY-PRIVADO'.encode() not in data
            assert 'RAD-SENSIBLE-123'.encode() not in data
            assert 'NOMBRE_PERSONAL_REAL'.encode() not in data
        with (out/'preset_casos.csv').open(encoding='utf-8-sig',newline='') as fp:
            row=list(csv.DictReader(fp))[0]
        assert row['radicado_pseudo']==pseudo('RAD-SENSIBLE-123','RAD')
        with (out/'preset_kpis_mensuales.csv').open(encoding='utf-8-sig',newline='') as fp:
            summary=list(csv.DictReader(fp))[0]
        assert summary['casos_iniciados']=='1'
        assert summary['casos_finalizados']=='0'
        assert summary['tasa_finalizacion_pct']=='0.0'
        assert summary['tasa_prevalidacion_pct']=='100.0'
        assert json.loads((out/'manifest.json').read_text())['esquema_exportacion']=='mba-etl-v1'


def test_empty_database_etl_has_headers(tmp_path,monkeypatch):
    monkeypatch.setenv('DATABASE_URL',f'sqlite:///{tmp_path / "empty.sqlite3"}')
    monkeypatch.delenv('DB_HOST',raising=False)
    from app.db import setup_db
    report=produce(setup_db(),tmp_path/'exports')
    assert all(detail['filas']==0 for detail in report['csv'].values())
    for name in report['csv']:
        assert len((tmp_path/'exports'/name).read_text(encoding='utf-8-sig').splitlines())==1


def test_compose_services_local_only():
    text=(Path(__file__).parents[1]/'compose.yaml').read_text(encoding='utf8')
    assert '127.0.0.1:${MVP_PORT:-8088}:80' in text
    assert 'service_healthy' in text
    assert 'profile' in text  # etl optional
    import yaml
    spec=yaml.safe_load(text)
    assert {'db','api','web','etl'}.issubset(spec['services'])
    assert 'ports' not in spec['services']['db']
    assert 'ports' not in spec['services']['api']
    assert spec['services']['etl']['profiles']==['herramientas']


def test_export_csv_injection_protection():
    from scripts.etl_preset import safe_text
    assert safe_text('=1+2')=="'=1+2"
    assert safe_text('@cmd')=="'@cmd"
    assert safe_text('normal')=='normal'


def test_camunda_sync_updates_local_metrics(tmp_path,monkeypatch):
    from app.camunda import CamundaClient
    monkeypatch.setenv('DATABASE_URL',f'sqlite:///{tmp_path / "camunda_sync.sqlite3"}')
    monkeypatch.setenv('ENGINE_MODE','camunda')
    def start(self, process_id, variables):
        return {'processInstanceKey':'2251799813686021'}
    def status(self,key):
        assert key=='2251799813686021'
        return {'state':'COMPLETED','endDate':'2026-10-21T12:00:00Z'}
    monkeypatch.setattr(CamundaClient,'start',start)
    monkeypatch.setattr(CamundaClient,'status',status)
    with TestClient(app) as cli:
        case=cli.post('/api/cases',json={'radicado':'SYNC-001','escenario':'ASIS',
             'area_terreno_m2':100,'area_construida_m2':150,'uso':'residencial','chip':'A'}).json()
        assert case['estado']=='EN_PROCESO'
        done=cli.post(f"/api/cases/{case['id']}/sync")
        assert done.status_code==200,done.text
        assert done.json()['caso']['estado']=='FINALIZADO'
        assert cli.get('/api/kpis').json()['escenarios']['ASIS']['terminados']==1
