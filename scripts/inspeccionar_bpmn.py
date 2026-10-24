#!/usr/bin/env python3
"""Convierte un BPMN existente a un inventario textual para revisión con OpenCode."""
import argparse
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET
BPMN='{http://www.omg.org/spec/BPMN/20100524/MODEL}'
NODES={'startEvent','endEvent','task','userTask','serviceTask','manualTask','sendTask',
       'receiveTask','businessRuleTask','scriptTask','exclusiveGateway','inclusiveGateway',
       'parallelGateway','eventBasedGateway','intermediateCatchEvent','intermediateThrowEvent','boundaryEvent',
       'subProcess','callActivity'}
def loc(x):return x.tag.rsplit('}',1)[-1]
def create(path):
    tree=ET.parse(path);root=tree.getroot();lines=['# Inventario del BPMN','',f'**Archivo:** {path.name}','',
        '> Inventario técnico de lo declarado en XML; no confirma la corrección del proceso.','']
    for proc in root.findall(f'{BPMN}process'):
        nodes={e.get('id'):e for e in proc if loc(e) in NODES}
        flows=[e for e in proc if loc(e)=='sequenceFlow']
        lines.extend([f'## Proceso: {proc.get("name",proc.get("id"))}',
                      f'- ID: `{proc.get("id")}`; ejecutable declarado: `{proc.get("isExecutable", "no especificado")}`',
                      f'- Nodos: {len(nodes)}; flujos: {len(flows)}','',
                      '### Actividades, compuertas y eventos',''])
        for id0,node in nodes.items():
            kind=loc(node);name=node.get('name') or '(sin nombre)'
            lines.append(f'- `{id0}` | {kind} | {name}')
        lines.extend(['','### Conectores de secuencia',''])
        for f in flows:
            name=f.get('name') or '(sin etiqueta)'
            lines.append(f'- `{f.get("id")}`: {f.get("sourceRef")} → {f.get("targetRef")} | {name}')
        lines.append('')
    lines.extend(['## Flujos de mensajes entre participantes',''])
    for mf in root.iter(f'{BPMN}messageFlow'):
        lines.append(f'- `{mf.get("id")}`: {mf.get("sourceRef")} → {mf.get("targetRef")}')
    if lines[-1]=='':lines.append('_(Ninguno declarado)_')
    return '\n'.join(lines)+'\n'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('entrada',type=Path);p.add_argument('salida',type=Path);args=p.parse_args()
    args.salida.parent.mkdir(parents=True,exist_ok=True)
    args.salida.write_text(create(args.entrada),encoding='utf-8');print(args.salida)
