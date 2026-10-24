# Registro de calidad — datos SINTÉTICOS (generado)

> Generado por `09-datos/generar_sinteticos.js` (semilla 20261024). **No editar a mano**: volver a correr el script.
> Los datos son **SINTÉTICOS**. Los KPI de abajo solo comprueban que el generador respeta los parámetros; **no son mediciones**.

## Volumen
| Archivo | Filas | Granularidad |
|---|---|---|
| `casos.csv` | 16000 | 1 fila por solicitud y escenario |
| `actividades.csv` | 24335 | 1 fila por actividad del expediente, vuelta, solicitud y escenario |
| `resumen_mensual.csv` | 24 | 1 fila por mes y escenario |

## Pruebas
| Prueba | Fallos | Ejemplos |
|---|---|---|
| id_caso duplicado | 0 | — |
| Campos obligatorios vacíos (id_caso, escenario, mes, fecha_inicio, fecha_fin, estado_final) | 0 | — |
| Fechas en orden (inicio ≤ aceptación ≤ sobre ≤ fin) | 0 | — |
| mes coincide con fecha_inicio | 0 | — |
| sobre_enviado = 1 exige fecha_sobre_desembolso y días de expediente | 0 | — |
| cerrada_vencimiento = 1 implica sobre_enviado = 0 | 0 | — |
| devuelta = 1 exige llego_a_verificacion = 1 y motivo | 0 | — |
| ruta = papel en TO-BE exige motivo_papel | 0 | — |
| Cada id_par tiene exactamente un AS-IS y un TO-BE | 0 | — |
| Actividades sin caso | 0 | — |
| AVISO (no es error): días de expediente > 40, casos con 3 o más devoluciones | 30 | 51; 51; 48 |

## Control de parámetros (año completo, SUM/SUM)
| KPI | AS-IS | TO-BE | Parámetro esperado |
|---|---|---|---|
| KPI-01 Ciclo del expediente (días hábiles) | 14,93 | 7,81 | AS-IS ≈ 15 (12 ÷ 0,8); TO-BE ≈ 6–7 (hipótesis) |
| KPI-02 Tasa de devolución | 20,0 % | 6,9 % | AS-IS 20 %; TO-BE ≈ 5 % digital + 20 % en papel |
| KPI-03 Cierre por vencimiento | 10,5 % | 2,8 % | AS-IS 10 %; TO-BE ≈ 5 % digital + 10 % en papel |
| KPI-04 Uso efectivo del portal | N/D | 85,4 % | TO-BE 85 % (hipótesis H-1) |
