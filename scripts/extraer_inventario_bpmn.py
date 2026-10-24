#!/usr/bin/env python3
"""Inventario de tareas por proceso y lane desde BPMN XML (sin dependencias). Sin tiempos inventados."""
import argparse,csv,xml.etree.ElementTree as ET
from pathlib import Path
N='http://www.omg.org/spec/BPMN/20100524/MODEL'
TAG=lambda x:f'{{{N}}}{x}'
TYPES={'task','manualTask','userTask','serviceTask','sendTask','receiveTask','businessRuleTask','scriptTask','callActivity','subProcess'}
COLUMNS=['id_bpmn','pool','lane','tipo_bpmn','nombre_actividad','minutos_humanos_asis','minutos_humanos_tobe',
         'volumen_mensual','tasa_error_asis','tasa_error_tobe','fuente_evidencia','candidata_automatizacion','riesgo_control','estado']

def extract(file):
 root=ET.parse(file).getroot();participants={p.get('processRef'):p.get('name','') for p in root.findall('.//'+TAG('participant'))};out=[]
 for proc in root.findall('./'+TAG('process')):
    names={ref.text:lane.get('name','') for lane in proc.findall('.//'+TAG('lane')) for ref in lane.findall(TAG('flowNodeRef'))}
    for item in proc.iter():
        typ=item.tag.split('}')[-1]
        if typ not in TYPES:continue
        id_=item.get('id','')
        out.append({'id_bpmn':id_,'pool':participants.get(proc.get('id'),proc.get('name','')),
            'lane':names.get(id_,'SIN_ASIGNAR'),'tipo_bpmn':typ,'nombre_actividad':item.get('name',''),
            'minutos_humanos_asis':'','minutos_humanos_tobe':'','volumen_mensual':'','tasa_error_asis':'',
            'tasa_error_tobe':'','fuente_evidencia':'','candidata_automatizacion':'POR_EVALUAR',
            'riesgo_control':'','estado':'NO_MEDIDO'})
 return out

def main():
 p=argparse.ArgumentParser();p.add_argument('bpmn',type=Path);p.add_argument('salida',type=Path);a=p.parse_args()
 result=extract(a.bpmn);a.salida.parent.mkdir(parents=True,exist_ok=True)
 with a.salida.open('w',newline='',encoding='utf-8-sig') as f:
  wr=csv.DictWriter(f,fieldnames=COLUMNS);wr.writeheader();wr.writerows(result)
 print(f'OK: {len(result)} tareas/supbrocesos extraidos de {a.bpmn}; campos a completar en {a.salida}')
if __name__=='__main__':main()
