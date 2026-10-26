# CSV para Preset — Flujo de crédito preaprobado (SINTÉTICO)

Generados con `python3 11-preset/preparar_csv_preset.py` (desde `trabajos/mi-proceso`) a partir de `09-datos/` y de la hoja `FlujoMensual` de `12-roi/Modelo_ROI_Flujo_Credito.xlsx`. Si cambian los datos o el Excel, volver a correr el script; no editar los CSV a mano.

## Carga en Preset (`+` → Data → Upload CSV)
Delimitador coma, encabezado en la fila 0, decimal `.`, UTF-8. Si la tabla ya existe: **Replace**.

| Archivo (`11-preset/csv/`) | Tabla sugerida | Filas | Granularidad |
|---|---|---|---|
| `preset_resumen_mensual.csv` | `credito_resumen_mensual` | 24 | mes × escenario |
| `preset_casos.csv` | `credito_casos` | 16.000 | solicitud × escenario |
| `preset_actividades.csv` | `credito_actividades` | 24.335 | actividad × vuelta × solicitud × escenario |
| `preset_roi_mensual.csv` | `credito_roi_mensual` | 12 | mes (escenario BASE, Opción 3, RD$) |

- `mes` (texto `YYYY-MM`) sirve como categoría; `mes_fecha` (`YYYY-MM-01`) como eje temporal. En **Columns to be parsed as dates** poner `mes_fecha` (y en `credito_casos` también `fecha_inicio,fecha_aceptacion,fecha_sobre_desembolso,fecha_fin`).
- Celdas vacías = **N/D** (por ejemplo, el portal en el AS-IS). No convertirlas en 0.
- **No** unir casos con actividades para contar solicitudes ni sumar `dias_habiles` de actividades para obtener el ciclo (ver `09-datos/diccionario.md`).

## Métricas (SUM/SUM, nunca promediar tasas mensuales)
| KPI | Tabla | Métrica personalizada | Control (año) AS-IS / TO-BE |
|---|---|---|---|
| KPI-01 Ciclo del expediente | `credito_resumen_mensual` | `SUM(dias_expediente_total) / SUM(sobres_enviados)` | 14,93 / 7,81 días |
| KPI-02 Tasa de devolución | `credito_resumen_mensual` | `SUM(devueltas) * 1.0 / SUM(llegaron_verificacion)` | 20,0 % / 6,9 % |
| KPI-03 Cierre por vencimiento | `credito_resumen_mensual` | `SUM(cerradas_vencimiento) * 1.0 / SUM(entraron_expediente)` | 10,5 % / 2,8 % |
| KPI-04 Uso efectivo del portal | `credito_resumen_mensual` | `SUM(ruta_digital) * 1.0 / SUM(entraron_expediente)` (filtro `escenario = 'TO-BE'`) | N/D / 85,4 % |
| Beneficio neto anual | `credito_roi_mensual` | `SUM(neto_caja_rd)` | RD$ 1.192.177 |
| Acumulado a diciembre | `credito_roi_mensual` | `MAX(acumulado_rd)` o línea por `mes_fecha` | RD$ 192.177 |

El `* 1.0` evita la división entera en la base de datos. Las tasas quedan como proporción 0–1: dar formato `%` en el gráfico.

Sugerencias de gráficos: KPI-01 a KPI-03 como líneas por `mes_fecha` con serie `escenario`; KPI-04 como Big Number; ROI como barras de `neto_caja_rd` más línea de `acumulado_rd` (cruza a positivo en noviembre); `credito_casos` para histograma de `dias_habiles_expediente` y cortes por `ruta` y `motivo_devolucion`. Poner la etiqueta **SINTÉTICO / DEMOSTRACIÓN** en el título del tablero.
