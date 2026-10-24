from pathlib import Path
import tempfile,sys,unittest,csv,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from taller_kpi import make_demo,validate,summarize,roi_monthly,read_csv,run_pipeline,report
from extraer_inventario_bpmn import extract

class KPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.config=json.loads((ROOT/'config/escenario_reexpedicion.json').read_text(encoding='utf-8'))
    def test_synthetic_pairs_and_totals(self):
        with tempfile.TemporaryDirectory() as d:
            cases,acts=make_demo(Path(d),self.config)
            self.assertEqual(len(cases),330);self.assertEqual(len(acts),1320)
            self.assertEqual(validate(read_csv(Path(d)/'casos.csv'),read_csv(Path(d)/'actividades.csv')),[])
            sm=summarize(cases)
            self.assertEqual(len(sm),6)
            rv=roi_monthly(sm,self.config)
            self.assertEqual(len(rv),3)
            self.assertAlmostEqual(sum(v['ahorro_laboral_cop']+v['ahorro_errores_cop'] for v in rv),sum(v['beneficio_bruto_cop'] for v in rv),places=2)
    def test_bad_data_rejected(self):
        cases=read_csv(ROOT/'datos/demo/casos.csv');cases[0]['horas_humanas']='-1'
        self.assertTrue(validate(cases,[]))
    def test_roi_matches_excel_assumptions(self):
        cases=read_csv(ROOT/'datos/demo/casos.csv');sm=summarize(cases)
        cfg=self.config
        text=report(sm,roi_monthly(sm,cfg),cfg)
        self.assertIn('Fracción monetizable',text)
        self.assertIn('70%',text)
        self.assertIn('19,172,592 COP',text)
    def test_uploaded_bpmn_inventory(self):
        all_=extract(ROOT/'ejemplos/bpmn/reexpedicion-v01.bpmn')
        self.assertTrue(any(x['id_bpmn']=='S_ValidarEnlace' for x in all_))
        self.assertTrue(all(x['estado']=='NO_MEDIDO' for x in all_))
    def test_workbook_exists_with_formulas(self):
        path=ROOT/'datos/Modelo_KPI_ROI_Reexpedicion.xlsx'
        with zipfile.ZipFile(path) as z:
            strings='\n'.join(z.read(n).decode(errors='ignore') for n in z.namelist() if n.startswith('xl/worksheets/sheet'))
            self.assertIn(':f>',strings)
            self.assertIn('Supuestos!',strings)
    def test_preset_output_schema(self):
        r=read_csv(ROOT/'datos/preset/preset_resumen_mensual.csv');rv=read_csv(ROOT/'datos/preset/preset_roi_mensual.csv')
        self.assertEqual(len(r),6);self.assertEqual(len(rv),3)
        self.assertTrue(all(0<=float(x['tasa_error'])<=1 for x in r))
        self.assertTrue(all(float(x['beneficio_bruto_cop'])==float(x['ahorro_laboral_cop'])+float(x['ahorro_errores_cop']) for x in rv))
if __name__=='__main__':unittest.main()
