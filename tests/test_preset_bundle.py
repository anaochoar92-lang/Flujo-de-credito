"""Pruebas LOCALES del constructor; NO sustituyen una importación Preset Starter."""
from pathlib import Path
import io, json, sys, tempfile, unittest, zipfile, yaml
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from generar_bundle_preset import generate, safe_entries, ErrorPaquete, audit_bundle

class PresetBundleTests(unittest.TestCase):
    def create_export(self,base,role='all'):
        p=Path(base)/f'export_{role}.zip'
        db={'uuid':'d0000000-0000-4000-8000-000000000001','database_name':'BaseCSV_Prueba','sqlalchemy_uri':'sqlite:///NO_EXISTE.db','version':'1.0.0'}
        tables=[('resumen','mba_resumen_mensual'),('roi','mba_roi_mensual')]
        if role!='all':tables=[t for t in tables if t[0]==role]
        with zipfile.ZipFile(p,'w') as z:
            z.writestr('metadata.yaml','version: 1.0.0\ntype: dataset\n')
            z.writestr('databases/BaseCSV_Prueba.yaml',yaml.safe_dump(db))
            for i,(k,n) in enumerate(tables):
                ds={'uuid':f'c0000000-0000-4000-8000-00000000000{1 if k=="resumen" else 2}',
                    'database_uuid':db['uuid'],'table_name':n,'schema':'public',
                    'columns':[],'metrics':[],'version':'1.0.0'}
                z.writestr(f'datasets/BaseCSV_Prueba/{n}.yaml',yaml.safe_dump(ds))
        return p
    def test_generate_two_dashboards_eight_charts(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.create_export(d,'resumen');b=self.create_export(d,'roi');out=Path(d)/'dashboard.zip'
            r=generate([a,b],out)
            self.assertTrue(out.exists());self.assertEqual(r['recursos']['charts'],8)
            self.assertEqual(r['recursos']['dashboards'],2)
            self.assertEqual(r['recursos']['datasets'],2)
            self.assertEqual(r['recursos']['databases'],1)
            self.assertEqual(r['recursos']['errores'],[])
            with zipfile.ZipFile(out) as z:
                info=yaml.safe_load(z.read('metadata.yaml'))
                self.assertEqual(info['type'],'dashboard')
                self.assertEqual(len([p for p in z.namelist() if p.startswith('charts/')]),8)
                self.assertEqual(len([p for p in z.namelist() if p.startswith('dashboards/')]),2)
                self.assertIn('CANDIDATO_NO_VERIFICADO',r['estado'])
    def test_fails_without_dataset(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.create_export(d,'resumen')
            with self.assertRaisesRegex(ErrorPaquete,'No está el dataset'):
                generate([a],Path(d)/'bad.zip')
    def test_visible_db_password_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'dangerous.zip'
            db={'uuid':'d0000000-0000-4000-8000-000000000001',
                'database_name':'Prueba','sqlalchemy_uri':'postgresql://user:VERY_SECRET@db.local:5432/test'}
            ds={'uuid':'c0000000-0000-4000-8000-000000000001',
                'database_uuid':db['uuid'],'table_name':'mba_resumen_mensual'}
            with zipfile.ZipFile(p,'w') as z:
                z.writestr('databases/Prueba.yaml',yaml.safe_dump(db))
                z.writestr('datasets/Prueba/resumen.yaml',yaml.safe_dump(ds))
            with self.assertRaisesRegex(ErrorPaquete,'contraseña visible'):
                generate([p],Path(d)/'out.zip')
    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'bad.zip'
            with zipfile.ZipFile(f,'w') as z:z.writestr('../metadata.yaml','type: dataset')
            with self.assertRaisesRegex(ErrorPaquete,'insegura'):safe_entries(f)
    def test_errors_for_missing_csv_columns(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.create_export(d,'all')
            cfg=json.loads((ROOT/'config/preset_dashboard_maestro.json').read_text(encoding='utf-8'))
            cfg['datasets']['roi']['columns'].append('columna_inexistente')
            cp=Path(d)/'cfg.json';cp.write_text(json.dumps(cfg),encoding='utf-8')
            with self.assertRaisesRegex(ErrorPaquete,'Columnas ausentes'):
                generate([a],Path(d)/'bad.zip',configpath=cp)
if __name__=='__main__': unittest.main()
