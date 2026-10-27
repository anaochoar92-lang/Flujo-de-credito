"""Genera modelos Camunda 8 didácticos con BPMN DI editable."""
from pathlib import Path
from lxml import etree as ET
BASE=Path(__file__).resolve().parents[1]
B='http://www.omg.org/spec/BPMN/20100524/MODEL'
DI='http://www.omg.org/spec/BPMN/20100524/DI'
DC='http://www.omg.org/spec/DD/20100524/DC'
DII='http://www.omg.org/spec/DD/20100524/DI'
Z='http://camunda.org/schema/zeebe/1.0'
XSI='http://www.w3.org/2001/XMLSchema-instance'

def sub(parent,tag,**attrs):return ET.SubElement(parent, f'{{{B}}}{tag}',attrs)

def bpmn(name, tobe):
    id_='liquidacion_cargas_tobe_mba' if tobe else 'liquidacion_cargas_asis_mba'
    r=ET.Element(f'{{{B}}}definitions',nsmap={'bpmn':B,'bpmndi':DI,'dc':DC,'di':DII,'zeebe':Z,'xsi':XSI},id='Definitions_'+id_,targetNamespace='https://ejemplo.mba/bpmn')
    proc=sub(r,'process',id=id_,name=name,isExecutable='true')
    nodes=[('Start','startEvent','Inicio')]
    if tobe:
        nodes += [('Decision','exclusiveGateway','¿Prevalidación automática OK?'),('Subsanar','userTask','Subsanar información'),('Revisar','userTask','Revisar preliquidación'),('Aprobar','userTask','Aprobar preliquidación')]
        flows=[('Start','Decision',''),('Decision','Revisar','ok'),('Decision','Subsanar','falta'),('Subsanar','Revisar',''),('Revisar','Aprobar',''),('Aprobar','End','')]
    else:
        nodes += [('Cotejar','userTask','Cotejar radicación'),('Areas','userTask','Validar áreas'),('Aprobar','userTask','Aprobar preliquidación')]
        flows=[('Start','Cotejar',''),('Cotejar','Areas',''),('Areas','Aprobar',''),('Aprobar','End','')]
    nodes.append(('End','endEvent','Fin'))
    # create node types and Zeebe userTask markers
    node_map={}
    for nid,tag,label in nodes:
        el=sub(proc,tag,id='Node_'+nid,name=label)
        if tag=='userTask':
            ext=sub(el,'extensionElements')
            ET.SubElement(ext,f'{{{Z}}}userTask')
        node_map[nid]=el
    for i,(s,t,kind) in enumerate(flows):
        fid='Flow_'+str(i+1)
        sub(node_map[s],'outgoing').text=fid
        sub(node_map[t],'incoming').text=fid
        fl=sub(proc,'sequenceFlow',id=fid,sourceRef='Node_'+s,targetRef='Node_'+t)
        if s=='Decision' and kind=='ok':
            cond=sub(fl,'conditionExpression')
            cond.set(f'{{{XSI}}}type','bpmn:tFormalExpression')
            cond.text='=validacionPreviaOk = true'
        if s=='Decision' and kind=='falta':
            node_map[s].set('default',fid)
    diagram=ET.SubElement(r,f'{{{DI}}}BPMNDiagram',id='Diagram_1')
    plane=ET.SubElement(diagram,f'{{{DI}}}BPMNPlane',id='Plane_1',bpmnElement=id_)
    pos={}
    for k,(nid,tag,label) in enumerate(nodes):
        if tobe:
            coords={'Start':(100,210),'Decision':(250,195),'Subsanar':(420,350),'Revisar':(620,210),'Aprobar':(820,210),'End':(1050,220)}
        else:
            coords={'Start':(100,210),'Cotejar':(255,195),'Areas':(465,195),'Aprobar':(675,195),'End':(900,210)}
        x,y=coords[nid]
        size=(50,50) if tag.endswith('Event') else ((52,52) if tag.endswith('Gateway') else (160,82))
        pos[nid]=(x,y,*size)
        shape=ET.SubElement(plane,f'{{{DI}}}BPMNShape',id='Shape_'+nid,bpmnElement='Node_'+nid)
        ET.SubElement(shape,f'{{{DC}}}Bounds',x=str(x),y=str(y),width=str(size[0]),height=str(size[1]))
    for i,(s,t,kind) in enumerate(flows):
        sx,sy,sw,sh=pos[s];tx,ty,tw,th=pos[t]
        edge=ET.SubElement(plane,f'{{{DI}}}BPMNEdge',id=f'Edge_{i+1}',bpmnElement=f'Flow_{i+1}')
        points=[(sx+sw,sy+sh/2),(tx,ty+th/2)]
        if tobe and s=='Decision' and t=='Subsanar':points=[(sx+sw/2,sy+sh),(sx+sw/2,ty+sh/2),(tx,ty+th/2)]
        if tobe and s=='Subsanar' and t=='Revisar':points=[(sx+sw,sy+sh/2),(tx-30,sy+sh/2),(tx-30,ty+th/2),(tx,ty+th/2)]
        for x,y in points:ET.SubElement(edge,f'{{{DII}}}waypoint',x=str(round(x,1)),y=str(round(y,1)))
    f=BASE/'bpmn'/f'{id_}.bpmn';ET.ElementTree(r).write(str(f),encoding='UTF-8',xml_declaration=True,pretty_print=True)
    return f
if __name__=='__main__':
    for f in [bpmn('Liquidación AS-IS · MBA',False),bpmn('Liquidación TO-BE · MBA',True)]:print(f)
