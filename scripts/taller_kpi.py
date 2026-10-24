#!/usr/bin/env python3
"""Motor reproducible sin dependencias: generar casos simulados, validar, exportar CSV de Preset y ROI.
Este módulo NO interactúa con cuentas Preset ni contiene credenciales.
"""
import argparse, csv, json, random, shutil
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta
from statistics import mean

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_CONFIG=ROOT/'config'/'escenario_reexpedicion.json'
DEFAULT_OUT=ROOT/'datos'/'demo'
CASE_COLS=['id_caso','id_par','escenario','proceso','fecha_inicio','fecha_fin','mes','canal',
           'horas_humanas','horas_espera','horas_ciclo','error','reproceso','automatizado',
           'reexpedicion','costo_laboral_cop','costo_error_cop','fuente_datos']
ACT_COLS=['id_caso','id_par','escenario','mes','actividad','tipo_tarea','horas_humanas',
          'automatizable','intervencion_humana','fuente_datos']
METRIC_COLS=['mes','escenario','casos','horas_humanas_totales','horas_humanas_promedio',
             'horas_espera_promedio','horas_ciclo_promedio','errores','tasa_error',
             'reprocesos','tasa_reproceso','casos_automatizados','tasa_automatizacion',
             'costo_laboral_total_cop','costo_errores_total_cop','costo_variable_total_cop']
ROI_COLS=['mes','casos_pareados','ahorro_horas_total','ahorro_laboral_potencial_cop','ahorro_laboral_cop',
          'ahorro_errores_cop','beneficio_bruto_cop','mantenimiento_cop',
          'beneficio_neto_operativo_cop','fuente_datos']

def write_csv(path,headers,records):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=headers,extrasaction='ignore',lineterminator='\n')
        writer.writeheader(); writer.writerows(records)

def read_csv(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))

def f(x):return float(x)
def rnd(x):return round(x,3)

def make_demo(out,config):
    rng=random.Random(int(config['semilla'])); cases=[]; activities=[]
    stages=[('Revisar solicitud','Revision humana',0.25),('Cotejar soportes','IDP o revision documental',0.32),
            ('Preparar liquidacion','Reglas y calculo',0.29),('Notificar y registrar','Workflow',0.14)]
    # Parear casos para garantizar muestras comparables; AS-IS y TO-BE son escenarios, no mediciones antes/despues.
    index=0
    for ym in config['meses']:
        y,m=map(int,ym.split('-'))
        for _ in range(int(config['casos_por_mes'])):
            index+=1; pair=f'CASO-{index:04d}'
            day=rng.randint(1,25); hr=rng.randint(8,16)
            start=datetime(y,m,day,hr,0)
            channel=rng.choice(['Portal','Correo','Ventanilla'])
            reexp=(rng.random()<0.32)
            difficulty=rng.uniform(.75,1.27)
            # Usa la misma complejidad de caso pero variaciones estocasticas independientes por escenario.
            for scenario,key in [('AS-IS','as_is'),('TO-BE','to_be')]:
                opt=config[key]; id_case=f'{pair}-{key.replace("-", "")}'
                hh=rnd(max(.12,opt['horas_humanas_media']*difficulty*rng.uniform(.86,1.17)))
                wait=rnd(max(.2,opt['horas_espera_media']*difficulty*rng.uniform(.7,1.3)))
                cycle=rnd(hh+wait)
                error=int(rng.random()<opt['prob_error']);redo=int(rng.random()<opt['prob_reproceso'])
                auto=int(rng.random()<opt['fraccion_automatizada'])
                end=start+timedelta(hours=cycle)
                cost=rnd(hh*config['costo_hora_cop']);cost_err=rnd(error*config['costo_error_cop'])
                cases.append(dict(id_caso=id_case,id_par=pair,escenario=scenario,proceso=config['proceso'],
                    fecha_inicio=start.isoformat(timespec='seconds'),fecha_fin=end.isoformat(timespec='seconds'),
                    mes=ym,canal=channel,horas_humanas=hh,horas_espera=wait,horas_ciclo=cycle,
                    error=error,reproceso=redo,automatizado=auto,reexpedicion=int(reexp),
                    costo_laboral_cop=cost,costo_error_cop=cost_err,fuente_datos='SINTETICO'))
                for act_name,act_type,share in stages:
                    activities.append(dict(id_caso=id_case,id_par=pair,escenario=scenario,mes=ym,
                        actividad=act_name,tipo_tarea=act_type,horas_humanas=rnd(hh*share),
                        automatizable='Si' if act_name!='Revisar solicitud' else 'Parcial',
                        intervencion_humana='Si' if act_name=='Revisar solicitud' or (scenario=='AS-IS') else 'Segun excepcion',
                        fuente_datos='SINTETICO'))
    write_csv(out/'casos.csv',CASE_COLS,cases)
    write_csv(out/'actividades.csv',ACT_COLS,activities)
    shutil.copyfile(out/'casos.csv',out/'casos_para_Excel_y_Preset.csv')
    print(f'DEMO OK: {len(cases)} filas escenario-caso, {len(activities)} actividades; {out}')
    return cases,activities

def validate(cases,activities):
    errors=[]; seen=set();pairs=defaultdict(set)
    if not cases:errors.append('No se encontraron casos')
    for n,c in enumerate(cases,2):
        id_=c.get('id_caso'); scen=c.get('escenario');pr=c.get('id_par')
        if not all(c.get(k,'') for k in CASE_COLS):errors.append(f'Fila {n}: campo faltante')
        if id_ in seen:errors.append(f'Fila {n}: identificador duplicado {id_}')
        seen.add(id_);pairs[pr].add(scen)
        if scen not in ('AS-IS','TO-BE'):errors.append(f'Fila {n}: escenario desconocido {scen}')
        try:
            for col in ('horas_humanas','horas_espera','horas_ciclo','costo_laboral_cop','costo_error_cop'):
                if f(c[col])<0:errors.append(f'Fila {n}: {col} negativo')
            if abs(f(c['horas_ciclo'])-f(c['horas_humanas'])-f(c['horas_espera']))>.02:errors.append(f'Fila {n}: horas_ciclo inconsistente')
            for col in ('error','reproceso','automatizado','reexpedicion'):
                if c[col] not in ('0','1',0,1):errors.append(f'Fila {n}: {col} no es binario')
            start=datetime.fromisoformat(c['fecha_inicio']);end=datetime.fromisoformat(c['fecha_fin'])
            if end<start:errors.append(f'Fila {n}: fecha_fin anterior a inicio')
            if start.strftime('%Y-%m')!=c['mes']:errors.append(f'Fila {n}: mes incorrecto')
        except (ValueError,KeyError) as ex:errors.append(f'Fila {n}: {ex}')
    for p,sc in pairs.items():
        if sc!={'AS-IS','TO-BE'}:errors.append(f'Par {p}: no tiene ambos escenarios')
    ids={x['id_caso'] for x in cases}
    for a in activities:
        if a['id_caso'] not in ids:errors.append(f'Actividad {a["id_caso"]} sin caso')
    if not errors:print(f'VALIDACION OK: {len(cases)} casos-escenario; {len(pairs)} pares; {len(activities)} actividades')
    else:print('ERRORES:',*errors[:15],sep='\n- ')
    return errors

def summarize(cases):
    groups=defaultdict(list)
    for c in cases:groups[(c['mes'],c['escenario'])].append(c)
    output=[]
    for (mes,scen),rows in sorted(groups.items()):
        count=len(rows);s=lambda field:sum(f(v[field]) for v in rows)
        output.append(dict(mes=mes,escenario=scen,casos=count,
            horas_humanas_totales=rnd(s('horas_humanas')),
            horas_humanas_promedio=rnd(s('horas_humanas')/count),
            horas_espera_promedio=rnd(s('horas_espera')/count),
            horas_ciclo_promedio=rnd(s('horas_ciclo')/count),errores=int(s('error')),
            tasa_error=rnd(s('error')/count),reprocesos=int(s('reproceso')),
            tasa_reproceso=rnd(s('reproceso')/count),casos_automatizados=int(s('automatizado')),
            tasa_automatizacion=rnd(s('automatizado')/count),
            costo_laboral_total_cop=rnd(s('costo_laboral_cop')),
            costo_errores_total_cop=rnd(s('costo_error_cop')),
            costo_variable_total_cop=rnd(s('costo_laboral_cop')+s('costo_error_cop'))))
    return output

def roi_monthly(summary,config):
    idx={(r['mes'],r['escenario']):r for r in summary};result=[]
    for mes in sorted({r['mes'] for r in summary}):
        a=idx[(mes,'AS-IS')];t=idx[(mes,'TO-BE')]
        if a['casos']!=t['casos']:raise ValueError(f'Mes {mes}: cohortes diferentes, compare tasas no totales')
        sh=rnd(a['horas_humanas_totales']-t['horas_humanas_totales'])
        lab_pot=rnd(a['costo_laboral_total_cop']-t['costo_laboral_total_cop'])
        lab=rnd(lab_pot*config.get('fraccion_horas_monetizables',1.0))
        err=rnd(a['costo_errores_total_cop']-t['costo_errores_total_cop'])
        maint=f(config['mantenimiento_mensual_cop']);gross=rnd(lab+err)
        result.append(dict(mes=mes,casos_pareados=a['casos'],ahorro_horas_total=sh,
             ahorro_laboral_potencial_cop=lab_pot,ahorro_laboral_cop=lab,ahorro_errores_cop=err,beneficio_bruto_cop=gross,
             mantenimiento_cop=maint,beneficio_neto_operativo_cop=rnd(gross-maint),fuente_datos='SINTETICO'))
    return result

def report(summary,roi,config):
    bysc=defaultdict(list)
    for v in summary:bysc[v['escenario']].append(v)
    def avg(field,scen):
        vals=bysc[scen];n=sum(x['casos'] for x in vals)
        return (sum(x['horas_humanas_totales'] for x in vals)/n if field=='horas_humanas_promedio'
                else sum(x['errores'] for x in vals)/n if field=='tasa_error'
                else sum(x[field]*x['casos'] for x in vals)/n)
    ha=avg('horas_humanas_promedio','AS-IS');ht=avg('horas_humanas_promedio','TO-BE')
    ea=avg('tasa_error','AS-IS');et=avg('tasa_error','TO-BE')
    save_h=ha-ht;per=save_h*config['costo_hora_cop']+(ea-et)*config['costo_error_cop']
    benefit=(save_h*config['costo_hora_cop']*config.get('fraccion_horas_monetizables',1.0)+(ea-et)*config['costo_error_cop'])*config['volumen_anual_proyectado'];oper=12*config['mantenimiento_mensual_cop']
    invest=config['inversion_inicial_cop'];net=benefit-oper-invest
    roi_pct=100*net/(invest+oper) if invest+oper else 0
    payback=invest/((benefit-oper)/12) if benefit>oper else None
    return f'''# Informe de KPI y ROI — Escenario sintético, NO observado\n\n**Fuente:** {config['naturaleza']}. Las cifras son hipótesis editables, no mediciones oficiales.\n\n| Métrica | AS-IS | TO-BE |\n|---|---:|---:|\n| Horas humanas por caso | {ha:.2f} | {ht:.2f} |\n| Tasa de error | {ea:.1%} | {et:.1%} |\n| Horas humanas evitadas/caso | — | {save_h:.2f} |\n\n## ROI ilustrativo anual\n\n- Volumen anual proyectado (hipótesis): **{config['volumen_anual_proyectado']:,} casos**.\n- Costo por hora humana (hipótesis): **{config['costo_hora_cop']:,.0f} COP**.
- Fracción monetizable (hipótesis): **{config.get('fraccion_horas_monetizables',1):.0%}**; capacidad no monetizable excluida del ROI.\n- Ahorro laboral y de errores anualizado: **{benefit:,.0f} COP**.\n- Mantenimiento anual: **{oper:,.0f} COP**.\n- Inversión inicial: **{invest:,.0f} COP**.\n- Beneficio neto año 1: **{net:,.0f} COP**.\n- ROI año 1 = (beneficio bruto - mantenimiento - inversión) / (mantenimiento + inversión): **{roi_pct:.1f}%**.\n- Recuperación estimada: **{payback:.1f} meses**.\n\n> Ahorro de horas es capacidad liberada y NO necesariamente ahorro de caja. Si no se evita realmente un desembolso o se monetiza capacidad, presentar por separado ahorro potencial de capacidad y ahorro financiero realizado.\n\n## Precauciones\n\n1. No atribuir causalidad a estas cifras sintéticas.\n2. Los tiempos humanos no se suman directamente al tiempo de espera para estimar ahorro financiero.\n3. Comparar igual alcance, periodo y denominadores para AS-IS y TO-BE.\n4. Explicar inflación, inversión, mantenimiento y costos no incluidos antes de decidir en la realidad.\n5. Confirmar con expertos las actividades y el diseño TO-BE antes de implementar.\n'''

def run_pipeline(input_file,out,config):
    cases=read_csv(input_file)
    actpath=Path(input_file).with_name('actividades.csv')
    acts=read_csv(actpath) if actpath.is_file() else []
    errors=validate(cases,acts)
    if errors:raise SystemExit(f'Validacion fallida ({len(errors)} errores); no se preparan datasets.')
    summary=summarize(cases);roi=roi_monthly(summary,config)
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'preset_casos.csv',CASE_COLS,cases)
    if acts:write_csv(out/'preset_actividades.csv',ACT_COLS,acts)
    write_csv(out/'preset_resumen_mensual.csv',METRIC_COLS,summary)
    write_csv(out/'preset_roi_mensual.csv',ROI_COLS,roi)
    (out/'informe_roi.md').write_text(report(summary,roi,config),encoding='utf-8')
    print(f'PRESET OK: 4 archivos CSV (si hay actividades), informe ROI: {out}')
    return summary,roi

def main():
    p=argparse.ArgumentParser(description='MBA - datos de procesos y Preset CSV sin dependencias')
    p.add_argument('accion',choices=['demo','validar','preparar','todo'])
    p.add_argument('--config',type=Path,default=DEFAULT_CONFIG)
    p.add_argument('--input',type=Path,default=DEFAULT_OUT/'casos.csv')
    p.add_argument('--out',type=Path,default=None)
    args=p.parse_args();config=json.loads(args.config.read_text(encoding='utf-8'))
    if args.accion in ('demo','todo'):
        output=args.out or DEFAULT_OUT
        make_demo(output,config)
        if args.accion=='todo':run_pipeline(output/'casos.csv',ROOT/'datos'/'preset',config)
    elif args.accion=='validar':
        acts=args.input.with_name('actividades.csv')
        raise SystemExit(1 if validate(read_csv(args.input),read_csv(acts) if acts.exists() else []) else 0)
    elif args.accion=='preparar':run_pipeline(args.input,args.out or ROOT/'datos'/'preset',config)
if __name__=='__main__':main()
