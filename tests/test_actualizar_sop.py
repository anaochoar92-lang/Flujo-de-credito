"""Comprobar versionado y comparación de Word con solo stdlib."""
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from actualizar_sop import run


def make_docx(path, text):
    xml = ("<?xml version='1.0' encoding='UTF-8'?>"
           "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"
           "<w:body><w:p><w:r><w:t>" + text + "</w:t></w:r></w:p>"
           "<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Responsable</w:t></w:r></w:p></w:tc>"
           "<w:tc><w:p><w:r><w:t>Curaduría</w:t></w:r></w:p></w:tc></w:tr></w:tbl>"
           "</w:body></w:document>")
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('word/document.xml', xml)


class SOPVersioningTest(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.proj = Path(self.t.name) / 'mi-proceso'
        (self.proj / '01-fuentes').mkdir(parents=True)
        self.doc = self.proj / '01-fuentes' / 'ejemplo.docx'
        make_docx(self.doc, 'Solicitud de licencia desde la curaduria a SDP')

    def tearDown(self):
        self.t.cleanup()

    def test_primera_version_y_repeticion_no_modifica(self):
        self.assertEqual(run(self.proj, self.doc), 0)
        hist = self.proj/'01-fuentes'/'.historial_sop'
        self.assertTrue((hist/'SOP-v01.docx').is_file())
        self.assertTrue((hist/'SOP-v01.md').is_file())
        self.assertTrue((self.proj/'01-fuentes'/'SOP_ACTUAL.md').is_file())
        self.assertTrue((self.proj/'02-analisis'/'impacto-sop-v01.md').is_file())
        self.assertEqual(run(self.proj, self.doc), 0)
        self.assertFalse((hist/'SOP-v02.md').exists())

    def test_cambios_versionados(self):
        run(self.proj, self.doc)
        make_docx(self.doc, 'Solicitud de licencia revisada y validada por profesional SDP')
        self.assertEqual(run(self.proj, self.doc), 0)
        self.assertTrue((self.proj/'01-fuentes'/'.historial_sop'/'SOP-v02.docx').exists())
        diff = (self.proj/'02-analisis'/'impacto-sop-v02.md').read_text(encoding='utf-8')
        self.assertIn('-Solicitud de licencia desde', diff)
        self.assertIn('+Solicitud de licencia revisada', diff)
        self.assertIn('PENDIENTE DE VALIDACIÓN', diff)

    def test_dry_run_no_escribe(self):
        self.assertEqual(run(self.proj, self.doc, True), 0)
        self.assertFalse((self.proj/'01-fuentes'/'.historial_sop').exists())

    def test_varios_docx_requiere_identificacion(self):
        make_docx(self.proj/'01-fuentes'/'segundo.docx', 'Otro proceso con diferentes datos y validaciones')
        with self.assertRaises(ValueError):
            run(self.proj, None)


if __name__ == '__main__':
    unittest.main()
