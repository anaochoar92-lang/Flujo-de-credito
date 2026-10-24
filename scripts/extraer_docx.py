#!/usr/bin/env python3
"""Extrae texto básico de Word .docx a Markdown sin dependencias externas.
Conserva orden general de párrafos y tablas; las imágenes/gráficos necesitan revisión humana.
"""
import argparse
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
NS={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W='{'+NS['w']+'}'
def text_run(e):
    return ''.join((n.text or '') for n in e.iter() if n.tag==W+'t')
def get_docx(path):
    with zipfile.ZipFile(path) as z:xml=z.read('word/document.xml')
    doc=ET.fromstring(xml);body=doc.find('w:body',NS)
    output=['# Texto extraído de '+path.name,'','> Revisar encabezados, tablas y gráficos: la conversión automática simplifica el formato.','']
    for block in body:
        if block.tag==W+'p':
            phrase=text_run(block).strip()
            if not phrase:continue
            style=block.find('.//w:pStyle',NS)
            sty=style.get(W+'val','') if style is not None else ''
            import re
            match=re.search(r'(?:Heading|T[ií]tulo)([1-6])',sty,re.I)
            output.append(('## '*1 if not match else '#' * min(6,int(match.group(1))))+' '+phrase if match else phrase)
            output.append('')
        elif block.tag==W+'tbl':
            output.append('**Tabla del documento:**')
            for row in block.findall('w:tr',NS):
                cells=[text_run(cell).strip().replace('|','/') for cell in row.findall('w:tc',NS)]
                if cells:output.append(' | '.join(cells))
            output.append('')
    return '\n'.join(output)+'\n'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('documento',type=Path);p.add_argument('salida',type=Path)
    a=p.parse_args();a.salida.parent.mkdir(parents=True,exist_ok=True)
    a.salida.write_text(get_docx(a.documento),encoding='utf-8');print('Texto extraído en',a.salida)
