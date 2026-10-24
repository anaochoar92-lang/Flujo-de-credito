#!/usr/bin/env python3
"""Construye BPMN 2.0 + BPMN DI desde una especificación JSON declarativa.
Sólo biblioteca estándar. No intenta desplegar procesos ni afirmar validez ejecutable.
"""
import argparse
from collections import defaultdict, deque
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

BPMN='http://www.omg.org/spec/BPMN/20100524/MODEL'
BPMNDI='http://www.omg.org/spec/BPMN/20100524/DI'
DC='http://www.omg.org/spec/DD/20100524/DC'
DI='http://www.omg.org/spec/DD/20100524/DI'
XSI='http://www.w3.org/2001/XMLSchema-instance'
for prefix, uri in [('bpmn',BPMN),('bpmndi',BPMNDI),('dc',DC),('di',DI),('xsi',XSI)]:
    ET.register_namespace(prefix,uri)
def q(uri,local):return '{%s}%s'%(uri,local)
def b(local):return q(BPMN,local)
def child(parent,tag,attrs=None,txt=None):
    obj=ET.SubElement(parent,tag,attrs or {})
    if txt is not None:obj.text=str(txt)
    return obj
VALID_TYPES={'startEvent','endEvent','task','userTask','serviceTask','manualTask','sendTask','receiveTask',
             'businessRuleTask','scriptTask','exclusiveGateway','inclusiveGateway','parallelGateway',
             'eventBasedGateway','intermediateCatchEvent','intermediateThrowEvent','boundaryEvent'}
EVENT_DEF={'message':'messageEventDefinition','timer':'timerEventDefinition','signal':'signalEventDefinition',
           'error':'errorEventDefinition','escalation':'escalationEventDefinition',
           'terminate':'terminateEventDefinition','conditional':'conditionalEventDefinition'}
GATEWAYS={'exclusiveGateway','inclusiveGateway','parallelGateway','eventBasedGateway'}
ID_PATTERN=re.compile(r'^[A-Za-z_][A-Za-z0-9_.-]*$')

def validate_spec(spec):
    errors=[];warnings=[];all_ids=set();node_owners={}
    def add_id(val,ctx):
        if not isinstance(val,str) or not ID_PATTERN.fullmatch(val):errors.append(f'ID inválido en {ctx}: {val!r}');return
        if val in all_ids:errors.append(f'ID repetido: {val}')
        all_ids.add(val)
    if not spec.get('processes'):errors.append('Se requiere processes con al menos un proceso')
    for proc in spec.get('processes',[]):
        pid=proc.get('id');add_id(pid,'proceso')
        nodes=proc.get('nodes',[]); flows=proc.get('flows',[])
        if not nodes: errors.append(f'{pid}: no contiene nodos')
        local_ids={n.get('id') for n in nodes}
        for n in nodes:
            nid=n.get('id');add_id(nid,'nodo')
            if nid in node_owners:errors.append(f'Nodo repetido: {nid}')
            node_owners[nid]=pid
            if n.get('type') not in VALID_TYPES:errors.append(f'{nid}: tipo BPMN no soportado {n.get("type")}')
            ev=n.get('event')
            if ev:
                if ev.get('kind') not in EVENT_DEF:errors.append(f'{nid}: tipo evento no soportado')
                if ev.get('kind') in ('message','signal','error','escalation') and not ev.get('ref'):
                    errors.append(f'{nid}: evento necesita ref (declaración externa)')
            if n.get('type')=='boundaryEvent' and n.get('attachedTo') not in local_ids:
                errors.append(f'{nid}: boundaryEvent necesita attachedTo dentro de su proceso')
            if n.get('type')=='boundaryEvent' and not ev:
                errors.append(f'{nid}: boundaryEvent necesita event')
        for l in proc.get('lanes',[]):
            add_id(l.get('id'),'lane')
            for nid in l.get('nodeIds',[]):
                if nid not in local_ids:errors.append(f'{pid}: lane menciona nodo inexistente {nid}')
        for f in flows:
            add_id(f.get('id'),'flujo')
            if f.get('source') not in local_ids or f.get('target') not in local_ids:
                errors.append(f'{pid}: flujo {f.get("id")} requiere ambos nodos en su proceso')
            if f.get('source')==f.get('target'):warnings.append(f'{pid}: flujo reflexivo {f.get("id")}')
        flowids={f.get('id') for f in flows}
        for n in nodes:
            if n.get('default') and n['default'] not in flowids:
                errors.append(f'{n.get("id")}: default referencia flujo inexistente')
            if n.get('type')=='eventBasedGateway':
                for f in flows:
                    if f.get('source')==n.get('id'):
                        tgt=next((x for x in nodes if x.get('id')==f.get('target')),None)
                        if tgt and tgt.get('type') not in ('intermediateCatchEvent','receiveTask'):
                            errors.append(f'{n.get("id")}: flujo de gateway basado en eventos no llega a catch/receive')
        if not any(n.get('type')=='startEvent' for n in nodes):warnings.append(f'{pid}: no tiene startEvent')
        if not any(n.get('type')=='endEvent' for n in nodes):warnings.append(f'{pid}: no tiene endEvent')
    for entry in spec.get('participants',[]):
        add_id(entry.get('id'),'participante')
        if entry.get('processRef') not in {p.get('id') for p in spec.get('processes',[])}:
            errors.append(f'Participante {entry.get("id")} refiere proceso inexistente')
    for f in spec.get('messageFlows',[]):
        add_id(f.get('id'),'messageFlow')
        a,b0=node_owners.get(f.get('source')),node_owners.get(f.get('target'))
        if not a or not b0:errors.append(f'{f.get("id")}: messageFlow apunta a nodo inexistente')
        elif a==b0:errors.append(f'{f.get("id")}: messageFlow entre nodos del mismo pool/proceso')
    ids_declared={x.get('id') for kind in ('messages','signals','errors','escalations') for x in spec.get(kind,[])}
    for kind in ('messages','signals','errors','escalations'):
        for declaration in spec.get(kind,[]):add_id(declaration.get('id'),kind)
    for p in spec.get('processes',[]):
        for n in p.get('nodes',[]):
            ev=n.get('event') or {}
            if ev.get('kind') in ('message','signal','error','escalation') and ev.get('ref') not in ids_declared:
                errors.append(f'{n.get("id")}: falta declaración de {ev.get("ref")}')
    return errors,warnings

def infer_columns(nodes,flows):
    adjacency=defaultdict(list);indegree=defaultdict(int)
    for f in flows:
        adjacency[f['source']].append(f['target']); indegree[f['target']]+=1
    starts=[n['id'] for n in nodes if n['type']=='startEvent']
    starts=starts or ([nodes[0]['id']] if nodes else [])
    dist={n['id']:0 for n in nodes}
    # BFS acotado por número de nodos. Al encontrar ciclos evitamos incrementar indefinidamente.
    queue=deque(starts);seen=set(starts)
    while queue:
        u=queue.popleft()
        for v in adjacency[u]:
            if v not in seen:
                dist[v]=dist[u]+1;seen.add(v);queue.append(v)
    nmax=max(dist.values(),default=0)
    for node in nodes:
        if node['id'] not in seen: nmax+=1;dist[node['id']]=nmax
    return dist

def compute_boxes(proc,ybase):
    nodes=proc['nodes']; flows=proc.get('flows',[])
    lanes=proc.get('lanes') or [{'id':'_internal','name':'Proceso','nodeIds':[n['id'] for n in nodes]}]
    lane_for={nid:i for i,l in enumerate(lanes) for nid in l.get('nodeIds',[])}
    depths=infer_columns(nodes,flows)
    occupied=defaultdict(int); boxes={}
    left=140; top=ybase+10; lane_h=220; spacing=200
    for n in nodes:
        if n['type']=='boundaryEvent':continue
        col=n.get('column',depths[n['id']]); lane=lane_for.get(n['id'],0)
        rank=occupied[(lane,col)];occupied[(lane,col)]+=1
        width,height=(50,50) if n['type'] in GATEWAYS else ((36,36) if n['type'].endswith('Event') else (148,78))
        x=left+int(col)*spacing
        center_y=top+lane*lane_h+80+rank*80
        boxes[n['id']]=(x,round(center_y-height/2),width,height)
    for n in nodes:
        if n['type']!='boundaryEvent':continue
        host=boxes.get(n.get('attachedTo'))
        if host:
            x,y,w,h=host;boxes[n['id']]=(x+w-20,y+h-18,36,36)
    max_x=max((box[0]+box[2] for box in boxes.values()),default=600)
    width=max(760,max_x-left+260)
    height=max(len(lanes)*lane_h+40,240)
    return boxes,lanes,(70,ybase,width,height),lane_h

def edge_points(boxA,boxB,route_index=0,diagram_limit=None):
    sx,sy,sw,sh=boxA; tx,ty,tw,th=boxB
    cy=sy+sh/2;tymid=ty+th/2
    if tx>sx+sw+12:
        # Ruta ortogonal simple (adecuada como borrador para ajustar en Modeler)
        mx=(sx+sw+tx)/2
        return [(sx+sw,cy),(mx,cy),(mx,tymid),(tx,tymid)]
    if tx==sx and ty>sy+sh:
        center=sx+sw/2
        return [(center,sy+sh),(center,ty)]
    detour=max(sy+sh,ty+th)+65+route_index*22
    return [(sx+sw/2,sy+sh),(sx+sw/2,detour),(tx+tw/2,detour),(tx+tw/2,ty+th)]

def build(spec):
    errors,warnings=validate_spec(spec)
    if errors:raise ValueError('\n'.join(errors))
    root=ET.Element(b('definitions'),{'id':spec.get('id','Definitions_Laboratorio'),
                                     'targetNamespace':'https://laboratorio.example.org/bpmn',
                                     'exporter':'Taller OpenCode BPMN','exporterVersion':'1.0'})
    kinds={'messages':'message','signals':'signal','errors':'error','escalations':'escalation'}
    for plural,tag in kinds.items():
        for d in spec.get(plural,[]):child(root,b(tag),{'id':d['id'],'name':d.get('name',d['id'])})
    processes=spec['processes']
    participants=spec.get('participants') or [{'id':'Participant_'+p['id'],'name':p.get('name',p['id']),
                                                'processRef':p['id']} for p in processes]
    collaboration=child(root,b('collaboration'),{'id':'Collaboration_Lab','name':spec.get('name','Proceso')})
    for part in participants:child(collaboration,b('participant'),{k:str(part[k]) for k in ('id','name','processRef')})
    for f in spec.get('messageFlows',[]):child(collaboration,b('messageFlow'),{'id':f['id'],
                        'name':f.get('name',''),'sourceRef':f['source'],'targetRef':f['target']})
    boxes_all={}; bounds={}; lane_infos={}; ybase=90
    for p in processes:
        pid=p['id']; pel=child(root,b('process'),{'id':pid,'name':p.get('name',pid),
                                                 'isExecutable':str(bool(p.get('isExecutable',False))).lower()})
        boxes,lanes,pool,lh=compute_boxes(p,ybase)
        bounds[pid]=pool; boxes_all.update(boxes);lane_infos[pid]=(lanes,lh)
        if p.get('lanes'):
            lset=child(pel,b('laneSet'),{'id':'LaneSet_'+pid})
            for lane in lanes:
                l=child(lset,b('lane'),{'id':lane['id'],'name':lane.get('name',lane['id'])})
                for nodeid in lane.get('nodeIds',[]):child(l,b('flowNodeRef'),txt=nodeid)
        flow_in=defaultdict(list);flow_out=defaultdict(list)
        for f in p.get('flows',[]):flow_out[f['source']].append(f['id']);flow_in[f['target']].append(f['id'])
        for n in p['nodes']:
            typ=n['type'];attrs={'id':n['id'],'name':n.get('name',n['id'])}
            if n.get('default'):attrs['default']=n['default']
            if typ=='boundaryEvent':
                attrs['attachedToRef']=n['attachedTo']
                if n.get('cancelActivity') is False:attrs['cancelActivity']='false'
            el=child(pel,b(typ),attrs)
            for fid in flow_in[n['id']]:child(el,b('incoming'),txt=fid)
            for fid in flow_out[n['id']]:child(el,b('outgoing'),txt=fid)
            ev=n.get('event')
            if ev:
                tag=EVENT_DEF[ev['kind']]; attrs={}
                if ev.get('ref') and ev['kind'] not in ('timer','conditional'):
                    attrs[ev['kind']+'Ref']=ev['ref']
                ev_el=child(el,b(tag),attrs)
                for t in ('timeDate','timeDuration','timeCycle'):
                    if ev.get(t) is not None:
                        expr=child(ev_el,b(t),{q(XSI,'type'):'bpmn:tFormalExpression'},ev[t])
                if ev['kind']=='conditional' and ev.get('condition'):
                    child(ev_el,b('condition'),{q(XSI,'type'):'bpmn:tFormalExpression'},ev['condition'])
        for f in p.get('flows',[]):
            at={'id':f['id'],'sourceRef':f['source'],'targetRef':f['target']}
            if f.get('name'):at['name']=f['name']
            fe=child(pel,b('sequenceFlow'),at)
            if f.get('condition'):
                child(fe,b('conditionExpression'),{q(XSI,'type'):'bpmn:tFormalExpression'},f['condition'])
        ybase+=pool[3]+80
    diagram=child(root,q(BPMNDI,'BPMNDiagram'),{'id':'BPMNDiagram_Lab'})
    plane=child(diagram,q(BPMNDI,'BPMNPlane'),{'id':'BPMNPlane_Lab','bpmnElement':'Collaboration_Lab'})
    for part in participants:
        pid=part['processRef'];x,y,w,h=bounds[pid]
        shape=child(plane,q(BPMNDI,'BPMNShape'),{'id':part['id']+'_di','bpmnElement':part['id'],'isHorizontal':'true'})
        child(shape,q(DC,'Bounds'),{'x':str(x),'y':str(y),'width':str(w),'height':str(h)})
    for p in processes:
        pid=p['id'];x,y,w,h=bounds[pid];lanes,lh=lane_infos[pid]
        if p.get('lanes'):
            for i,lane in enumerate(lanes):
                shape=child(plane,q(BPMNDI,'BPMNShape'),{'id':lane['id']+'_di','bpmnElement':lane['id'],'isHorizontal':'true'})
                child(shape,q(DC,'Bounds'),{'x':str(x+30),'y':str(y+i*lh),
                      'width':str(w-30),'height':str(lh if i<len(lanes)-1 else h-i*lh)})
        for n in p['nodes']:
            if n['id'] not in boxes_all:continue
            node_shape=child(plane,q(BPMNDI,'BPMNShape'),{'id':n['id']+'_di','bpmnElement':n['id']})
            a,b0,c,d=boxes_all[n['id']]
            child(node_shape,q(DC,'Bounds'),{'x':str(a),'y':str(b0),'width':str(c),'height':str(d)})
    idx=0
    for p in processes:
        for f in p.get('flows',[]):
            if f['source'] not in boxes_all or f['target'] not in boxes_all:continue
            edge=child(plane,q(BPMNDI,'BPMNEdge'),{'id':f['id']+'_di','bpmnElement':f['id']})
            for x,y in edge_points(boxes_all[f['source']],boxes_all[f['target']],idx%3):
                child(edge,q(DI,'waypoint'),{'x':str(round(x)),'y':str(round(y))})
            idx+=1
    for f in spec.get('messageFlows',[]):
        if f['source'] not in boxes_all or f['target'] not in boxes_all:continue
        edge=child(plane,q(BPMNDI,'BPMNEdge'),{'id':f['id']+'_di','bpmnElement':f['id']})
        for x,y in edge_points(boxes_all[f['source']],boxes_all[f['target']]):
            child(edge,q(DI,'waypoint'),{'x':str(round(x)),'y':str(round(y))})
    ET.indent(root,space='  ')
    return ET.ElementTree(root), warnings

def main():
    ap=argparse.ArgumentParser(description='Generar BPMN 2.0 con elementos gráficos desde JSON')
    ap.add_argument('json',type=Path);ap.add_argument('salida',type=Path)
    args=ap.parse_args()
    with args.json.open(encoding='utf-8') as fh:spec=json.load(fh)
    try: tree,warnings=build(spec)
    except ValueError as e: print('ERRORES EN JSON:\n'+str(e),file=sys.stderr);sys.exit(2)
    args.salida.parent.mkdir(parents=True,exist_ok=True)
    tree.write(args.salida,encoding='utf-8',xml_declaration=True)
    print('Creado:',args.salida)
    for w in warnings:print('ADVERTENCIA:',w)
if __name__=='__main__':main()
