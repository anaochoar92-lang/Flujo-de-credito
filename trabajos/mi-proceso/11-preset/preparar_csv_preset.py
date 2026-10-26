"""Prepara los CSV del flujo de crédito para subirlos a Preset (Upload CSV).

Lee 09-datos/*.csv y la hoja FlujoMensual de 12-roi/Modelo_ROI_Flujo_Credito.xlsx
(valores guardados por Excel) y escribe 11-preset/csv/. Solo usa la biblioteca estándar.

Uso, desde trabajos/mi-proceso:  python3 11-preset/preparar_csv_preset.py
"""
import csv
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATOS = BASE / '09-datos'
EXCEL_ROI = BASE / '12-roi' / 'Modelo_ROI_Flujo_Credito.xlsx'
SALIDA = BASE / '11-preset' / 'csv'
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}


def leer_csv(ruta):
    with open(ruta, encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def primero_la_mas_completa(filas):
    """Pone primero la fila con menos celdas vacías (la primera que lo cumpla; el resto conserva su orden).

    Preset elimina las columnas que vienen vacías en la primera fila del CSV.
    """
    i = max(range(len(filas)), key=lambda j: (sum(v != '' for v in filas[j].values()), -j))
    return [filas[i]] + filas[:i] + filas[i + 1:]


def escribir_csv(nombre, filas):
    filas = primero_la_mas_completa(filas)
    vacias = [k for k, v in filas[0].items() if v == '']
    if vacias:
        print(f'  AVISO {nombre}: ninguna fila tiene todo lleno; en la primera quedan vacías {vacias}')
    # UTF-8 sin BOM: con BOM, Preset puede leer la primera columna como "﻿mes".
    with open(SALIDA / nombre, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(filas)
    print(f'{nombre}: {len(filas)} filas')


def con_mes_fecha(filas):
    """Agrega mes_fecha (YYYY-MM-01) para usar como eje temporal; mes queda como categoría."""
    salida = []
    for fila in filas:
        nueva = {}
        for k, v in fila.items():
            nueva[k] = v
            if k == 'mes':
                nueva['mes_fecha'] = f'{v}-01'
        salida.append(nueva)
    return salida


def leer_hoja(xlsx, nombre_hoja):
    """Devuelve las filas de una hoja como listas de valores (los guardados por Excel)."""
    with zipfile.ZipFile(xlsx) as z:
        compartidas = []
        if 'xl/sharedStrings.xml' in z.namelist():
            raiz = ET.fromstring(z.read('xl/sharedStrings.xml'))
            compartidas = [''.join(t.text or '' for t in si.iter(f"{{{NS['m']}}}t")) for si in raiz]
        libro = ET.fromstring(z.read('xl/workbook.xml'))
        rid = next(h.get(f"{{{NS['r']}}}id") for h in libro.iter(f"{{{NS['m']}}}sheet") if h.get('name') == nombre_hoja)
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        destino = next(r.get('Target') for r in rels if r.get('Id') == rid)
        hoja = ET.fromstring(z.read('xl/' + destino.lstrip('/').removeprefix('xl/')))
    filas = []
    for fila in hoja.iter(f"{{{NS['m']}}}row"):
        valores = []
        for c in fila:
            v = c.find('m:v', NS)
            en_linea = c.find('m:is', NS)
            if c.get('t') == 's' and v is not None:
                valores.append(compartidas[int(v.text)])
            elif v is not None:
                valores.append(v.text)
            elif en_linea is not None:
                valores.append(''.join(t.text or '' for t in en_linea.iter(f"{{{NS['m']}}}t")))
            else:
                valores.append('')
        filas.append(valores)
    return filas


def roi_mensual():
    filas = leer_hoja(EXCEL_ROI, 'FlujoMensual')
    encabezado = next(i for i, f in enumerate(filas) if f and f[0] == 'mes')
    esperado = ['mes', 'temporada', 'Horas AS-IS', 'Horas TO-BE', 'Horas ahorradas', 'Ahorro temporales (feria)',
                'Tiempo convertido en caja', 'Mensajero (banco)', 'Mantenimiento', 'Neto en caja', 'Acumulado']
    if filas[encabezado][:len(esperado)] != esperado:
        raise SystemExit(f'La hoja FlujoMensual cambió de columnas: {filas[encabezado]}')
    num = lambda x, d=2: round(float(x), d)
    salida = []
    for f in filas[encabezado + 1:]:
        if not f or f[0] == 'Mes 0':  # la inversión inicial ya está dentro de acumulado_rd
            continue
        salida.append({
            'mes': f[0], 'mes_fecha': f'{f[0]}-01', 'temporada': f[1],
            'horas_asis': num(f[2]), 'horas_tobe': num(f[3]), 'horas_ahorradas': num(f[4]),
            'ahorro_temporales_feria_rd': num(f[5]), 'tiempo_convertido_caja_rd': num(f[6]),
            'mensajero_banco_rd': num(f[7]), 'mantenimiento_rd': num(f[8]),
            'neto_caja_rd': num(f[9]), 'acumulado_rd': num(f[10]),
            'escenario_roi': 'BASE - Opcion 3', 'fuente_datos': 'SINTETICO',
        })
    return salida


def main():
    SALIDA.mkdir(exist_ok=True)
    escribir_csv('preset_resumen_mensual.csv', con_mes_fecha(leer_csv(DATOS / 'resumen_mensual.csv')))
    escribir_csv('preset_casos.csv', con_mes_fecha(leer_csv(DATOS / 'casos.csv')))
    escribir_csv('preset_actividades.csv', con_mes_fecha(leer_csv(DATOS / 'actividades.csv')))
    escribir_csv('preset_roi_mensual.csv', roi_mensual())


if __name__ == '__main__':
    main()
