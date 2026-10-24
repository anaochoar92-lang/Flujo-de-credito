import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from crear_bpmn import build,validate_spec
from validar_bpmn import validate
from inspeccionar_bpmn import create
from extraer_docx import get_docx

class TallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((ROOT/'ejemplos/modelos/reexpedicion.json').read_text(encoding='utf-8'))
    def test_generador_crea_xml_y_di(self):
        tree,warnings=build(self.spec)
        root=tree.getroot()
        self.assertTrue(root.findall('.//{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape'))
        self.assertTrue(root.findall('.//{http://www.omg.org/spec/BPMN/20100524/DI}BPMNEdge'))
        self.assertEqual(len(root.findall('{http://www.omg.org/spec/BPMN/20100524/MODEL}process')),2)
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'x.bpmn';tree.write(file,encoding='utf-8',xml_declaration=True)
            result=validate(file)
            self.assertEqual([],result['errores'])
    def test_rechaza_messageflow_en_mismo_pool(self):
        spec=json.loads(json.dumps(self.spec))
        spec['messageFlows'].append({'id':'MF_errado','source':'S_Start','target':'S_Espera'})
        errors,_=validate_spec(spec)
        self.assertTrue(any('mismo pool' in m for m in errors))
    def test_rechaza_nodos_inexistentes(self):
        spec=json.loads(json.dumps(self.spec))
        spec['processes'][0]['flows'][0]['target']='inexistente'
        errors,_=validate_spec(spec)
        self.assertTrue(any('ambos nodos' in m for m in errors))
    def test_inventario_declarado(self):
        data=create(ROOT/'ejemplos/bpmn/reexpedicion-v01.bpmn')
        self.assertIn('¿Pago o vencimiento?',data)
        self.assertIn('Flujos de mensajes',data)
    def test_conversion_word(self):
        original=Path('/mnt/data/SOP_Reexpedicion_SDP.docx')
        if original.exists():
            converted=get_docx(original)
            self.assertIn('Procedimiento',converted)
            self.assertIn('reexpedici',converted.lower())
if __name__=='__main__':unittest.main()
