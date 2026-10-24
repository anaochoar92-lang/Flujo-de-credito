#!/usr/bin/env python3
"""Inspección estructural preliminar de BPMN 2.0 (no reemplaza XSD, Camunda lint ni validación humana)."""
import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

NS={'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL',
    'bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI'}
FLOW_NODES={'task','userTask','serviceTask','manualTask','receiveTask','sendTask','scriptTask','businessRuleTask',
            'startEvent','endEvent','intermediateCatchEvent','intermediateThrowEvent','boundaryEvent',
            'exclusiveGateway','inclusiveGateway','parallelGateway','eventBasedGateway',
            'subProcess','callActivity'}
def taglocal(element):return element.tag.split('}')[-1]

def validate(file):
    errors=[];warnings=[];stats={}
    try:root=ET.parse(file).getroot()
    except (ET.ParseError,OSError) as e:return {'archivo':str(file),'errores':[f'No se puede analizar XML: {e}'],'advertencias':[],'estadisticas':{}}
    if taglocal(root)!='definitions':errors.append('Raíz debe ser bpmn:definitions')
    entities={};owners={};processes=[];flows_by_proc={};nodes_by_proc={}
    for element in root.iter():
        eid=element.get('id')
        if eid:
            if eid in entities:errors.append(f'ID duplicado: {eid}')
            entities[eid]=element
    for p in root.findall('bpmn:process',NS):
        pid=p.get('id','?');processes.append(pid)
        nodes={n.get('id'):n for n in list(p) if taglocal(n) in FLOW_NODES}
        flows={f.get('id'):f for f in p.findall('bpmn:sequenceFlow',NS)}
        nodes_by_proc[pid]=nodes;flows_by_proc[pid]=flows
        for id0 in nodes: owners[id0]=pid
        outgoing=defaultdict(list); incoming=defaultdict(list)
        for fid,f in flows.items():
            a=f.get('sourceRef');b=f.get('targetRef')
            if a not in nodes or b not in nodes:
                errors.append(f'{pid}: {fid} enlaza nodos inexistentes o en otro proceso ({a} → {b})')
                continue
            outgoing[a].append(b);incoming[b].append(a)
            if taglocal(nodes[a])=='endEvent':errors.append(f'{pid}: endEvent {a} tiene salida {fid}')
            if taglocal(nodes[b])=='startEvent':errors.append(f'{pid}: startEvent {b} tiene entrada {fid}')
        starts=[nid for nid,n in nodes.items() if taglocal(n)=='startEvent']
        ends=[nid for nid,n in nodes.items() if taglocal(n)=='endEvent']
        if not starts:warnings.append(f'{pid}: sin evento de inicio (puede ser un subproceso incompleto)')
        if not ends:warnings.append(f'{pid}: sin evento de fin')
        reachable=set(starts);todo=deque(starts)
        while todo:
            for v in outgoing[todo.popleft()]:
                if v not in reachable: reachable.add(v);todo.append(v)
        for nid,n in nodes.items():
            typ=taglocal(n)
            if typ=='boundaryEvent':
                attached=n.get('attachedToRef')
                if attached not in nodes:errors.append(f'{pid}: evento límite {nid} adjunto a nodo inexistente')
                continue
            if starts and nid not in reachable:warnings.append(f'{pid}: nodo no alcanzable desde el inicio: {nid} ({n.get("name",typ)})')
            if typ=='endEvent':continue
            if not outgoing[nid]:warnings.append(f'{pid}: nodo sin continuación: {nid} ({n.get("name",typ)})')
            if typ in {'exclusiveGateway','inclusiveGateway'} and len(outgoing[nid])>1:
                flows_out=[f for f in flows.values() if f.get('sourceRef')==nid]
                if not n.get('default') and not any(f.find('bpmn:conditionExpression',NS) is not None for f in flows_out):
                    warnings.append(f'{pid}: gateway de decisión {nid} sin flujo por defecto ni condiciones formales (apto solo para revisión conceptual)')
            if typ=='eventBasedGateway':
                for target in outgoing[nid]:
                    if taglocal(nodes[target]) not in {'intermediateCatchEvent','receiveTask'}:
                        errors.append(f'{pid}: evento basado en gateway {nid} apunta a tipo incorrecto {target}')
            if typ in {'intermediateCatchEvent','intermediateThrowEvent','boundaryEvent'}:
                if not any(taglocal(child).endswith('EventDefinition') for child in n):
                    warnings.append(f'{pid}: {nid} sin definición explícita de evento')
        for lane in p.findall('.//bpmn:lane',NS):
            for ref in lane.findall('bpmn:flowNodeRef',NS):
                if ref.text not in nodes:errors.append(f'{pid}: lane {lane.get("id")} refiere nodo inexistente {ref.text}')
        stats[pid]={'nodos':len(nodes),'flujos':len(flows),'inicios':len(starts),'fines':len(ends)}
    participants=root.findall('.//bpmn:participant',NS)
    for part in participants:
        if part.get('processRef') not in processes:
            errors.append(f'Participante {part.get("id")} con processRef inexistente')
    for mf in root.findall('.//bpmn:messageFlow',NS):
        a=mf.get('sourceRef');b=mf.get('targetRef');pa=owners.get(a);pb=owners.get(b)
        if a not in entities or b not in entities:errors.append(f'MessageFlow {mf.get("id")} tiene extremo inexistente')
        elif pa and pb and pa==pb:errors.append(f'MessageFlow {mf.get("id")} conecta el mismo proceso (use sequenceFlow)')
    shapes=root.findall('.//bpmndi:BPMNShape',NS)
    edges=root.findall('.//bpmndi:BPMNEdge',NS)
    shape_refs={s.get('bpmnElement') for s in shapes}
    edge_refs={e.get('bpmnElement') for e in edges}
    if not shapes:warnings.append('No hay BPMN DI: Camunda Modeler puede no visualizar el proceso como diagrama')
    for pid,nodes in nodes_by_proc.items():
        for nid in nodes:
            if nid not in shape_refs:warnings.append(f'{pid}: falta forma gráfica BPMN DI para {nid}')
        for fid in flows_by_proc[pid]:
            if fid not in edge_refs:warnings.append(f'{pid}: falta conector gráfico BPMN DI para {fid}')
    stats['global']={'procesos':len(processes),'participantes':len(participants),
                     'messageFlows':len(root.findall('.//bpmn:messageFlow',NS)),
                     'formasDI':len(shapes),'conectoresDI':len(edges)}
    return {'archivo':str(file),'errores':errors,'advertencias':warnings,'estadisticas':stats,
            'limitaciones':['No valida contra el XSD oficial BPMN 2.0.',
                            'No comprueba configuración Zeebe/Camunda para ejecución.',
                            'No verifica coherencia jurídica ni semántica de las decisiones.',
                            'El aspecto visual debe revisarse en Camunda Modeler.']}

def main():
    a=argparse.ArgumentParser();a.add_argument('archivo',type=Path);a.add_argument('--json',type=Path)
    args=a.parse_args();result=validate(args.archivo)
    print('ARCHIVO:',result['archivo']);print('ESTADÍSTICAS:',json.dumps(result['estadisticas'],ensure_ascii=False))
    for label,key in [('ERROR','errores'),('AVISO','advertencias')]:
        for err in result[key]:print(f'{label}: {err}')
    print(f"RESULTADO: {len(result['errores'])} error(es), {len(result['advertencias'])} advertencia(s).")
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    sys.exit(2 if result['errores'] else 0)
if __name__=='__main__':main()
