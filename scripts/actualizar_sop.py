#!/usr/bin/env python3
"""Versiona un SOP .docx y extrae Markdown actualizado sin borrar fuentes ni derivados.

Biblioteca estándar. Conserva los originales .docx como snapshots, historial Markdown y
reporte de diferencias. No modifica EARS, JSON, BPMN, KPI o TO-BE automáticamente.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from difflib import unified_diff
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
from extraer_docx import get_docx


def run(proyecto: Path, documento: Path | None, dry_run: bool = False) -> int:
    proyecto = proyecto.resolve()
    fuentes = proyecto / '01-fuentes'
    if not fuentes.is_dir():
        raise ValueError(f'No existe la carpeta del proyecto: {fuentes}')
    if documento is None:
        candidatas = sorted(x for x in fuentes.glob('*.docx') if not x.name.startswith('~$'))
        if len(candidatas) != 1:
            raise ValueError('Indica --docx: se encontraron ' + str(len(candidatas)) +
                             ' documentos DOCX en 01-fuentes. ' + ', '.join(x.name for x in candidatas))
        documento = candidatas[0]
    else:
        documento = documento.resolve()
    if not documento.is_file() or documento.suffix.lower() != '.docx':
        raise ValueError(f'No es un documento DOCX válido: {documento}')
    if fuentes not in documento.parents:
        raise ValueError('El DOCX debe estar dentro de la carpeta 01-fuentes del proyecto')
    if '.historial_sop' in documento.parts:
        raise ValueError('Selecciona el DOCX original, no una copia del historial')

    data = documento.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    # Comprobar legibilidad ANTES de crear archivos.
    texto = get_docx(documento)
    if len(texto.strip()) < 70:
        raise ValueError('El documento extraído está prácticamente vacío; revisa el DOCX')

    historial = fuentes / '.historial_sop'
    manifiesto = historial / 'manifest.json'
    registros = json.loads(manifiesto.read_text(encoding='utf-8')) if manifiesto.is_file() else []
    if not isinstance(registros, list):
        raise ValueError('El manifiesto del historial no es válido')
    previo = registros[-1] if registros else None
    if previo and previo.get('sha256') == digest:
        print('SIN CAMBIOS: el DOCX coincide con la última versión registrada.')
        print('Comando sugerido en OpenCode: /01-analizar (si necesitas continuar un análisis pendiente)')
        return 0
    version = len(registros) + 1
    etiqueta = f'v{version:02d}'
    antiguo = ''
    if previo:
        ultima = historial / previo['markdown']
        if not ultima.is_file():
            raise ValueError(f'Falta versión anterior para comparar: {ultima}')
        antiguo = ultima.read_text(encoding='utf-8')
    diff = list(unified_diff(antiguo.splitlines(), texto.splitlines(),
                             fromfile=previo['markdown'] if previo else 'SIN VERSION PREVIA',
                             tofile=f'SOP-{etiqueta}.md', lineterm=''))
    informe = (f'# Actualización del SOP — {etiqueta}\n\n'
               f'- Archivo fuente: `{documento.name}`\n'
               f'- Huella SHA-256: `{digest}`\n'
               f'- Estado: **PENDIENTE DE VALIDACIÓN DEL PARTICIPANTE**\n'
               f'- No se modificaron los requerimientos EARS, JSON, BPMN, TO-BE ni KPI.\n\n'
               '## Diferencias textuales\n\n'
               'Las diferencias siguientes son textuales, no equivalen a una decisión aprobada.\n\n'
               '```diff\n' + ('\n'.join(diff) if diff else 'Sin diferencias textuales.') + '\n```\n\n'
               '## Revisión guiada pendiente\n\n'
               '- [ ] Confirmar qué cambios del DOCX alteran el proceso.\n'
               '- [ ] Revisar responsabilidades, tiempos, condiciones, excepciones y eventos.\n'
               '- [ ] Reconciliar inventario y preguntas de 02-analisis.\n'
               '- [ ] Actualizar solamente los REQ EARS impactados y su trazabilidad.\n'
               '- [ ] Regenerar o editar modelo AS-IS solo si procede, conservando versiones.\n'
               '- [ ] Evaluar si TO-BE, KPI, CSV o ROI requieren cambios.\n')
    print(f'Propuesta: actualizar {documento.name} como {etiqueta}.')
    print(f'Cambios de texto (líneas diff): {len(diff)}')
    if dry_run:
        print('DRY RUN: no se escribió ningún archivo.')
        return 0
    historial.mkdir(parents=True, exist_ok=True)
    (proyecto / '02-analisis').mkdir(parents=True, exist_ok=True)
    docx_snapshot = f'SOP-{etiqueta}.docx'
    md_snapshot = f'SOP-{etiqueta}.md'
    for ruta in [historial / docx_snapshot, historial / md_snapshot,
                 proyecto / '02-analisis' / f'impacto-sop-{etiqueta}.md']:
        if ruta.exists():
            raise FileExistsError(f'La versión no se puede sobrescribir: {ruta}')
    shutil.copy2(documento, historial / docx_snapshot)
    (historial / md_snapshot).write_text(texto, encoding='utf-8')
    (fuentes / 'SOP_ACTUAL.md').write_text(texto, encoding='utf-8')
    (proyecto / '02-analisis' / f'impacto-sop-{etiqueta}.md').write_text(informe, encoding='utf-8')
    registros.append({'version': etiqueta, 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
                      'archivo_fuente': documento.name, 'sha256': digest,
                      'docx': docx_snapshot, 'markdown': md_snapshot})
    manifiesto.write_text(json.dumps(registros, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'ACTUALIZADO: {fuentes / "SOP_ACTUAL.md"}')
    print(f'HISTORIAL: {historial} ({etiqueta})')
    print(f'IMPACTO: {proyecto / "02-analisis" / f"impacto-sop-{etiqueta}.md"}')
    print('SIGUIENTE PASO: revisar cambios con el participante; NO actualizar EARS/BPMN sin confirmar.')
    return 0


def main():
    p = argparse.ArgumentParser(description='Actualizar Word original y versionar SOP')
    p.add_argument('--proyecto', type=Path, default=Path('trabajos/mi-proceso'))
    p.add_argument('--docx', type=Path, help='Ruta DOCX dentro de 01-fuentes; opcional cuando hay uno solo')
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    try:
        return run(a.proyecto, a.docx, a.dry_run)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
