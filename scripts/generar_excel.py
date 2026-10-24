#!/usr/bin/env python3
"""Genera libro didactico XLSX a partir de casos.csv con artifact_tool.
Esta dependencia NO es necesaria para el taller: el .xlsx generado ya se distribuye.
No importa openpyxl, pandas ni herramientas de ofimatica.
"""
import argparse,csv,json
from pathlib import Path
from artifact_tool import Workbook,SpreadsheetFile
ROOT=Path(__file__).resolve().parents[1]
BASIC=ROOT/'datos/demo/casos.csv';CONFIG=ROOT/'config/escenario_reexpedicion.json'
OUTPUT=ROOT/'datos/Modelo_KPI_ROI_Reexpedicion.xlsx'
BLUE='#17619F';NAVY='#193656';TEAL='#137B84';MID='#EDF4F7';WHITE='#FFFFFF';DARK='#14263C'
HEAD={'fill':NAVY,'font':{'bold':True,'color':WHITE},'row_height':28,'wrap_text':True}
SUB={'fill':TEAL,'font':{'bold':True,'color':WHITE},'row_height':24}
MONEY='#,##0;[Red](#,##0);–'
NUMBER='#,##0.00;[Red](#,##0.00);–'
PCT='0.0%;[Red](0.0%);–'

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def header(sheet,cell_range,values):
    sheet.get_range(cell_range).values=[values];sheet.get_range(cell_range).format=HEAD

def export(inp,out,con):
    data=rows(inp);cfg=json.loads(con.read_text(encoding='utf-8')); wb=Workbook.create()
    s=wb.worksheets.add('Guia'); su=wb.worksheets.add('Supuestos'); base=wb.worksheets.add('Base_Casos')
    comp=wb.worksheets.add('Comparacion');roi=wb.worksheets.add('ROI');flow=wb.worksheets.add('FlujoMensual')
    cat=wb.worksheets.add('Catalogo_KPIs');prio=wb.worksheets.add('Priorizacion')
    # GUÍA
    s.get_range('A1:H1').merge();s.get_range('A1').values=[['LABORATORIO MBA | KPI, TO-BE Y ROI']];s.get_range('A1:H1').format=HEAD
    guide=[['Objetivo','Comparar un proceso AS-IS y un TO-BE simulado sin confundir capacidad con caja.'],
           ['Estado de datos','SINTÉTICO; ejemplo pedagógico, no cifras de la SDP.'],
           ['Paso 1','Abra Supuestos y cambie solo cifras editables en AZUL; note como cambian los resultados.'],
           ['Paso 2','Revise Base_Casos, que contiene una fila por caso y escenario.'],
           ['Paso 3','Abra Comparacion; observe las fórmulas para horas, errores y reprocesos.'],
           ['Paso 4','Abra ROI; revise numeradores, denominadores, inversión y mantenimiento.'],
           ['Paso 5','Abra FlujoMensual; una inversión inicial causa flujo negativo al principio.'],
           ['Paso 6','Importe los CSV de datos/preset en Preset y cree widgets según la guía.'],
           ['Precaución','Hora ahorrada = capacidad liberada; solo el porcentaje monetizable se incluye como caja.'],
           ['Fuentes','Material sesión 3, diapositivas 69–82; Preset docs https://docs.preset.io/docs/using-csv-files'],
           ['Archivos','docs/diccionario-kpis-y-ecuaciones.md; config/escenario_reexpedicion.json']]
    s.get_range('A3:B13').values=guide;s.get_range('A3:A13').format.font.bold=True
    s.get_range('A:A').format.column_width=24;s.get_range('B:B').format.column_width=85
    s.get_range('B3:B13').format.wrap_text=True
    # ASSUMPTIONS
    su.get_range('A1:D1').merge();su.get_range('A1').values=[['SUPUESTOS EDITABLES — DEMOSTRACIÓN']];su.get_range('A1:D1').format=HEAD
    su.get_range('A3:D3').values=[['Variable','Valor editable','Unidad','Fuente / estado']];su.get_range('A3:D3').format=SUB
    vals=[
    ('Volumen anual proyectado',int(cfg['volumen_anual_proyectado']),'casos/año','Hipótesis docente, config JSON'),
    ('Costo hora evitada',float(cfg['costo_hora_cop']),'COP/hora','Hipótesis docente; verificar costeo real'),
    ('Costo unitario de error',float(cfg['costo_error_cop']),'COP/error','Hipótesis docente; verificar incidencia y alcance'),
    ('Inversión inicial',float(cfg['inversion_inicial_cop']),'COP','Hipótesis docente; incluir integración y formación'),
    ('Mantenimiento mensual',float(cfg['mantenimiento_mensual_cop']),'COP/mes','Hipótesis docente; opex recurrente'),
    ('Fracción de horas monetizables',float(cfg.get('fraccion_horas_monetizables',.70)),'proporción 0–1','Hipótesis docente, no confundir ahorro de capacidad con caja')]
    su.get_range('A4:D9').values=[list(z) for z in vals]
    su.get_range('A4:A9').format.font.bold=True;su.get_range('B4:B9').format.font.color='#0000FF'
    su.get_range('B4:B9').format.fill='#FFF6D8';su.get_range('B9').set_number_format(PCT)
    su.get_range('B5:B8').set_number_format(MONEY)
    su.get_range('A:A').format.column_width=36;su.get_range('B:B').format.column_width=24
    su.get_range('C:C').format.column_width=22;su.get_range('D:D').format.column_width=63
    su.get_range('D3:D9').format.wrap_text=True
    # BASE CASES
    bcols=['id_caso','escenario','mes','horas_humanas','horas_espera','horas_ciclo','error','reproceso',
           'automatizado','costo_laboral_cop','costo_error_cop','reexpedicion','fuente_datos']
    header(base,'A1:M1',bcols)
    numeric={'horas_humanas','horas_espera','horas_ciclo','costo_laboral_cop','costo_error_cop','error','reproceso','automatizado','reexpedicion'}
    def cv(col,row):return float(row[col]) if col in numeric else row[col]
    matrix=[[cv(col,row) for col in bcols] for row in data]
    n=len(matrix);end=n+1
    if matrix:base.get_range(f'A2:M{end}').values=matrix
    base.get_range('A:A').format.column_width=24;base.get_range('B:C').format.column_width=14
    base.get_range('D:K').format.column_width=17;base.get_range('L:M').format.column_width=18
    base.get_range(f'D2:F{end}').set_number_format(NUMBER)
    base.get_range(f'J2:K{end}').set_number_format(MONEY)
    base.freeze_panes.freeze_rows(1)
    # comparison sheet; formulas linked to raw observations
    comp.get_range('A1:D1').merge();comp.get_range('A1').values=[['COMPARACIÓN DE ESCENARIOS (MISMA MUESTRA PAREADA)']];comp.get_range('A1:D1').format=HEAD
    comp.get_range('A3:D3').values=[['Métrica','AS-IS','TO-BE','Diferencia (AS-IS - TO-BE)']];comp.get_range('A3:D3').format=SUB
    metrics=[('Número casos','COUNTIF',''),('Horas humanas medias/caso','D','horas'),('Espera media/caso','E','horas'),
             ('Ciclo medio/caso','F','horas'),('Tasa de error','G','%'),('Tasa de reproceso','H','%'),
             ('Tasa casos automatizados','I','%'),('Costo laboral medio/caso','J','COP')]
    comp.get_range('A4:A11').values=[[m[0]] for m in metrics]
    for col,tag in [('B','AS-IS'),('C','TO-BE')]:
        comp.get_range(f'{col}4').formulas=[[f'=COUNTIF(Base_Casos!$B$2:$B${end},"{tag}")']]
        for rownum,src in [(5,'D'),(6,'E'),(7,'F'),(8,'G'),(9,'H'),(10,'I'),(11,'J')]:
            comp.get_range(f'{col}{rownum}').formulas=[[f'=IF({col}$4=0,0,SUMIF(Base_Casos!$B$2:$B${end},"{tag}",Base_Casos!${src}$2:${src}${end})/{col}$4)']]
    for rr in range(4,12):comp.get_range(f'D{rr}').formulas=[[f'=B{rr}-C{rr}']]
    comp.get_range('B5:D7').set_number_format(NUMBER)
    comp.get_range('B8:D10').set_number_format(PCT)
    comp.get_range('B11:D11').set_number_format(MONEY)
    comp.get_range('A:A').format.column_width=40;comp.get_range('B:D').format.column_width=25
    comp.get_range('A14:D15').values=[['Advertencia','Comparar cohortes y alcance equivalentes.','Cifras sintéticas.','Las tasas están en escala 0–1.'],['No concluir','La diferencia no prueba causalidad.','La reducción de horas puede NO ahorrar caja.','']]
    comp.get_range('A14:D15').format.wrap_text=True
    # ROI
    roi.get_range('A1:D1').merge();roi.get_range('A1').values=[['ROI SIMULADO — FÓRMULAS TRANSPARENTES']];roi.get_range('A1:D1').format=HEAD
    roi.get_range('A3:D3').values=[['Concepto','Valor o fórmula','Unidad','Interpretación']];roi.get_range('A3:D3').format=SUB
    entries=[
     (4,'Volumen anual','=Supuestos!B4','casos/año','Hipótesis en Supuestos'),
     (5,'Horas humanas evitadas por caso','=Comparacion!D5','h/caso','Misma cohorte'),
     (6,'Disminución tasa de error','=Comparacion!D8','proporción','AS-IS menos TO-BE'),
     (7,'Capacidad liberada/caso expresada en COP','=B5*Supuestos!B5','COP/caso','No es necesariamente caja'),
     (8,'Costo de errores evitados/caso','=B6*Supuestos!B6','COP/caso','Hipótesis costo por evento'),
     (9,'Capacidad liberada anual (valor teórico)','=B7*B4','COP/año','Valor bruto de las horas liberadas'),
     (10,'Ahorro laboral anual monetizable','=B9*Supuestos!B9','COP/año','Aplica fracción monetizable explícita'),
     (11,'Costo de errores anual evitado','=B8*B4','COP/año','No duplicar costos'),
     (12,'Beneficio anual monetizado','=B10+B11','COP/año','Labor monetizable + errores'),
     (13,'Mantenimiento anual','=Supuestos!B8*12','COP/año','Costo recurrente'),
     (14,'Inversión inicial','=Supuestos!B7','COP','Desembolso inicial'),
     (15,'Beneficio neto año 1','=B12-B13-B14','COP/año','Incluye inversión inicial'),
     (16,'ROI año 1','=IF(B13+B14=0,0,B15/(B13+B14))','%','Beneficio neto / costo total año 1'),
     (17,'Meses para recuperar inversión','=IF(B12<=B13,"N/D",B14/((B12-B13)/12))','meses','Recuperación simple, no descontada'),
     (18,'Volumen anual para punto de equilibrio','=IF(B7*Supuestos!B9+B8=0,"N/D",(B13+B14)/(B7*Supuestos!B9+B8))','casos/año','Supone costos y ahorro promedio constantes'),
     (19,'Horas humanas liberadas anuales','=B5*B4','horas/año','Capacidad, no caja por definición')]
    roi.get_range('A4:A19').values=[[e[1]] for e in entries]
    roi.get_range('C4:D19').values=[[e[3],e[4]] for e in entries]
    for rr,name,formula,unit,note in entries:roi.get_range(f'B{rr}').formulas=[[formula]]
    roi.get_range('B6').set_number_format(PCT);roi.get_range('B16').set_number_format(PCT)
    for rr in list(range(7,16)):roi.get_range(f'B{rr}').set_number_format(MONEY)
    roi.get_range('A:A').format.column_width=47;roi.get_range('B:B').format.column_width=27
    roi.get_range('C:C').format.column_width=22;roi.get_range('D:D').format.column_width=55
    roi.get_range('D4:D19').format.wrap_text=True
    roi.get_range('A21:D21').merge();roi.get_range('A21').values=[['No sustituye una evaluación financiera: no se incluyen impuestos, riesgos, ajuste de inflación ni descuento de flujos.']]
    roi.get_range('A21:D21').format.fill='#FFF1CF';roi.get_range('A21:D21').format.wrap_text=True
    # Monthly flows
    flow.get_range('A1:H1').merge();flow.get_range('A1').values=[['FLUJO 12 MESES — SENSIBILIDAD DEL NEGOCIO']];flow.get_range('A1:H1').format=HEAD
    flow.get_range('A4:H4').values=[['Mes','Casos/año / 12','Ahorro laboral COP','Error evitado COP','Opex COP','Inversión COP','Flujo neto COP','Acumulado COP']]
    flow.get_range('A4:H4').format=SUB
    flow.get_range('A5:A16').values=[[i] for i in range(1,13)]
    for rr in range(5,17):
        formulas={'B': '=ROI!$B$4/12','C':f'=B{rr}*ROI!$B$7*Supuestos!$B$9',
                  'D':f'=B{rr}*ROI!$B$8','E':'=Supuestos!$B$8',
                  'F':f'=IF(A{rr}=1,ROI!$B$14,0)',
                  'G':f'=C{rr}+D{rr}-E{rr}-F{rr}',
                  'H':f'=SUM($G$5:G{rr})'}
        for col,formula in formulas.items():flow.get_range(f'{col}{rr}').formulas=[[formula]]
    flow.get_range('B5:B16').set_number_format('0.0');flow.get_range('C5:H16').set_number_format(MONEY)
    flow.get_range('A:A').format.column_width=14;flow.get_range('B:H').format.column_width=23
    # KPI catalog
    cat.get_range('A1:F1').merge();cat.get_range('A1').values=[['CATÁLOGO Y ECUACIONES DE KPI']];cat.get_range('A1:F1').format=HEAD
    kpis=[
    ['KPI-01','Horas humanas por caso','SUM(horas_humanas) / COUNT(id_caso)','horas/caso','casos.csv; escenario','Barra'],
    ['KPI-02','Tiempo ciclo','SUM(horas_ciclo) / COUNT(id_caso)','horas/caso','casos.csv; mes','Serie temporal'],
    ['KPI-03','Tasa error','SUM(error) / COUNT(id_caso)','%','casos.csv; escenario','Barra'],
    ['KPI-04','Tasa reproceso','SUM(reproceso) / COUNT(id_caso)','%','casos.csv; escenario','Barra'],
    ['KPI-05','Horas evitadas','media horas ASIS - media horas TOBE','horas/caso','Comparacion!D5','Big number'],
    ['KPI-06','ROI año 1','(beneficios - opex - inversion) / (opex + inversion)','%','ROI!B16','Big number'],
    ['KPI-07','Costo de error evitado','volumen × diferencia en tasa_error × costo_error','COP/año','ROI!B11','Big number']]
    cat.get_range('A3:F3').values=[['ID','KPI','Fórmula','Unidad','Fuente','Widget']];cat.get_range('A3:F3').format=SUB
    cat.get_range('A4:F10').values=kpis
    for col,width in [('A',12),('B',28),('C',64),('D',22),('E',30),('F',22)]:cat.get_range(f'{col}:{col}').format.column_width=width
    cat.get_range('C4:C10').format.wrap_text=True
    # Priorización, data are didactic hypotheses (not scores from PPT)
    prio.get_range('A1:H1').merge();prio.get_range('A1').values=[['MATRIZ DE PRIORIZACIÓN — HIPÓTESIS PARA CLASE']];prio.get_range('A1:H1').format=HEAD
    prio.get_range('A3:H3').values=[['Oportunidad','Actividad BPMN','Impacto 25%','Volumen 20%','Urgencia 15%','Factibilidad 20%','Mitigar riesgo 20%','Puntuación / 5']];prio.get_range('A3:H3').format=SUB
    priorities=[['Validar campos automáticamente','Cotejo SOP',5,5,4,4,4,None],
                ['Extraer documentos IDP','Carga documental',4,4,4,3,3,None],
                ['Notificar vencimiento por API','Notificación',4,5,4,5,4,None],
                ['Aprobar caso complejo sin humano','Revisión superior',3,2,2,1,1,None]]
    prio.get_range('A4:H7').values=priorities
    prio.get_range('A12').values=[['PESOS EDITABLES']]
    prio.get_range('C12:G12').values=[[0.25,0.20,0.15,0.20,0.20]]
    prio.get_range('C12:G12').format.fill='#FFF6D8'
    prio.get_range('C12:G12').format.font.color='#0000FF'
    prio.get_range('C12:G12').set_number_format(PCT)
    prio.get_range('H12').formulas=[['=SUM(C12:G12)']]
    prio.get_range('H12').set_number_format(PCT)
    for rr in range(4,8):prio.get_range(f'H{rr}').formulas=[[f'=C{rr}*$C$12+D{rr}*$D$12+E{rr}*$E$12+F{rr}*$F$12+G{rr}*$G$12']]
    prio.get_range('A9:H9').merge();prio.get_range('A9').values=[['Pesos y puntuaciones son ejemplos docentes; comprobar riesgo residual y restricciones legales antes de elegir.']]
    prio.get_range('A9:H9').format.fill='#FFF1CF';prio.get_range('A9:H9').format.wrap_text=True
    for col,wid in [('A',42),('B',23),('C',20),('D',20),('E',20),('F',22),('G',24),('H',22)]:prio.get_range(f'{col}:{col}').format.column_width=wid
    # Charts (manual single series chart on monthly flow to avoid covering data)
    try:
        chart=flow.charts.add('line',{'title':'Flujo acumulado (COP)','has_legend':False})
        seri=chart.series.add('Flujo acumulado')
        seri.category_formula="'FlujoMensual'!$A$5:$A$16"
        seri.formula="'FlujoMensual'!$H$5:$H$16"
        chart.set_position('J4','R20')
    except Exception as exc:
        print('CHART aviso (hojas y fórmulas no afectadas):',exc)
    # Export and check
    out.parent.mkdir(parents=True,exist_ok=True)
    SpreadsheetFile.export_xlsx(wb).save(str(out))
    print('XLSX generado:',out,'filas casos',n)
    try:
        sample=wb.inspect({'kind':'table','range':'ROI!A4:D19','include':'values,formulas','table_max_rows':18,'table_max_cols':4})
        print('COMPROBACION ROI',sample.ndjson[:1400])
        errors=wb.inspect({'kind':'match','search_term':'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A','options':{'use_regex':True,'max_results':20}})
        print('ERRORES',errors.ndjson[:500])
    except Exception as exc:print('INSPECT aviso',exc)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=BASIC)
    ap.add_argument('--out',type=Path,default=OUTPUT);ap.add_argument('--config',type=Path,default=CONFIG)
    ar=ap.parse_args();export(ar.input,ar.out,ar.config)
