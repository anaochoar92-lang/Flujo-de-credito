# Reporte de validación Preset — Flujo de crédito preaprobado (SINTÉTICO)

**Fecha:** 2026-10-26 · **Comando:** `/19-verificar-importacion` · **Skill:** `verificar-importacion-preset`
**Workspace:** Preset Starter del equipo (anonimizado) · **Dashboard:** «Proceso preaprobado» (id 8), publicado
**Revisión:** lectura del dashboard y de la lista de datasets en el navegador; cifras recalculadas desde `11-preset/csv/`. No se modificó nada en Preset.

## Ruta usada
**Ruta C (manual):** los 4 CSV se subieron con *Upload CSV* y los gráficos se armaron a mano. No se usó ZIP, así que el nivel 1 (ZIP) no aplica.

## Cinco niveles
| Nivel | Resultado | Evidencia |
|---|---|---|
| 1. ZIP | No aplica | Ruta manual |
| 2. Dashboard visible | Cumple | 1 dashboard con 8 gráficos + 1 texto de conclusión |
| 3. Datos | Cumple | Datasets `preset_casos`, `preset_resumen_mensual`, `preset_actividades`, `preset_roi_mensual`; ningún gráfico con error |
| 4. Ecuaciones | Cumple, con observaciones | Todas las cifras coinciden con los CSV (tabla abajo) |
| 5. Decisión ROI | Cumple | ROI 16,7 % y 10,1 meses = `12-roi/interpretacion.md` (escenario base, Opción 3) |

## Cifras: Preset vs. CSV del repositorio
| Gráfico | Preset | Recalculado | Estado |
|---|---|---|---|
| Días hábiles promedio por solicitud | 9,72 / 7,14 | 9,72 / 7,14 | OK |
| Días hábiles en expediente (KPI-01) | 14,93 / 7,81 | 14,93 / 7,81 | OK |
| Tasa de devolución (KPI-02) | 20 % / 7 % | 20,0 % / 6,9 % | OK (redondeo a entero) |
| Cierre por vencimiento (KPI-03) | 10 % / 3 % | 10,5 % / 2,8 % | OK (redondeo a entero) |
| Horas de trabajo al año | 13.006 / 6.180 | 13.006 / 6.180 | OK |
| ROI año 1 | 16,7 % | 16,7 % | OK |
| Meses de recuperación | 10,1 | 10,1 | OK |
| Casos por escenario | — | 8.000 / 8.000 (pares, no 16.000 solicitudes distintas) | No visible en el tablero |

## Correcciones sugeridas (por prioridad)
1. **Eje mal rotulado:** «Días hábiles por actividad (AS-IS vs TO-BE)» dice «Horas por solicitud» en el eje X, pero los valores son días hábiles (Recopilar expediente ≈ 5,4 días).
2. **Falta KPI-04 (uso efectivo del portal, 85,4 % en TO-BE):** está en el catálogo de KPI y no aparece en el tablero. Sugerido: Big Number con filtro `escenario = 'TO-BE'`.
3. **Falta la etiqueta SINTÉTICO / DEMOSTRACIÓN** en el título del tablero (lo pide `11-preset/LEEME.md`).
4. **Redondeo de tasas:** mostrar un decimal (6,9 %, 10,5 %, 2,8 %) para que coincidan con la conclusión escrita.
5. **Datasets sobrantes:** `csv_storage` y `Preaprobado` (cargas anteriores) no los usa el tablero; conviene borrarlos o renombrarlos para evitar confusión.
6. El skill espera 2 dashboards; el equipo tiene 1 con los 8 gráficos. Confirmar con el docente si basta.

## Pendiente de confirmar por el equipo
- Quién construyó a mano al menos un KPI y cómo explica su cálculo (requisito del taller).
