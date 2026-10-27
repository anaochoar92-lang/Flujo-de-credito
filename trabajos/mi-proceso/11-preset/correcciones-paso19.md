# Correcciones al tablero Preset — paso 19 (SINTÉTICO)

**Fecha:** 2026-10-26 · **Origen:** `11-preset/reporte-validacion.md` · **Tablero:** «Proceso preaprobado» (id 8).
**Estado:** guía lista para aplicar a mano. Claude no pudo aplicarla porque la extensión de Chrome no estaba conectada en la sesión; **nada se ha cambiado todavía en Preset**.
**Efecto en los números:** ninguno. Son cambios de presentación; el ROI (16,7 %, 10,1 meses) y los KPI quedan iguales. Las cifras de control se recalcularon desde `11-preset/csv/preset_resumen_mensual.csv`.

Orden recomendado: 3 → 1 → 4 → 2 → 5. Al final, **Save** en el tablero.

## 1. Rótulo del eje (prioridad 1)
Gráfico «Días hábiles por actividad (AS-IS vs TO-BE)».
1. En el tablero, menú `⋮` del gráfico → **Edit chart**.
2. Pestaña **Customize** → sección del eje X (en barras horizontales, el eje de valores) → **X Axis Title**: `Días hábiles por solicitud`.
3. **Save** → *Save (Overwrite)*, marcando «Proceso preaprobado».
- Control: «Recopilar expediente» sigue mostrando ≈ 5,4 en AS-IS.

## 2. Agregar KPI-04 · Uso efectivo del portal (prioridad 2)
1. **+ Chart** → dataset `preset_resumen_mensual` → tipo **Big Number** (sin tendencia).
2. **Metric** → *Custom SQL*: `SUM(ruta_digital) * 1.0 / SUM(entraron_expediente)` · etiqueta `Uso efectivo del portal`.
3. **Filters** → `escenario` *equal to* `TO-BE`.
4. **Customize** → **Number format**: `.1%`. Subtítulo: `TO-BE · proporción de expedientes por ruta digital`.
5. Nombre del gráfico: `KPI-04 Uso efectivo del portal (TO-BE)` → **Save** → *Add to dashboard*: «Proceso preaprobado».
6. En el tablero, **Edit dashboard**, ubicarlo junto a KPI-02 y KPI-03.
- Control: **85,4 %**. En AS-IS no aplica (N/D: no hay portal), por eso va filtrado.

## 3. Etiqueta SINTÉTICO en el título (prioridad 3)
1. **Edit dashboard** → clic en el título.
2. Nuevo título: `Proceso preaprobado — SINTÉTICO / DEMOSTRACIÓN`.
3. **Save**.

## 4. Tasas con un decimal (prioridad 4)
En los gráficos de KPI-02 (devolución) y KPI-03 (cierre por vencimiento): **Edit chart** → **Customize** → **Number format** (o *Y Axis Format* y formato de etiquetas, según el tipo de gráfico) → `.1%` → *Save (Overwrite)*.
- Control KPI-02: AS-IS **20,0 %**, TO-BE **6,9 %**.
- Control KPI-03: AS-IS **10,5 %**, TO-BE **2,8 %**.
- Si en vez de `.1%` aparece el valor ×100 (p. ej. 690 %), la métrica no está como proporción: revisar que sea `SUM(...) * 1.0 / SUM(...)`.

## 5. Datasets sobrantes (prioridad 5)
`csv_storage` y `Preaprobado` no los usa el tablero.
1. **Data → Datasets** → en cada uno, revisar la columna/acción de gráficos asociados (al pulsar el ícono de borrar, Preset muestra cuántos gráficos y tableros lo usan).
2. Solo si dice **0 charts / 0 dashboards**, escribir `DELETE` y confirmar. Si algún gráfico lo usa, no borrar: renombrarlo con prefijo `zz_obsoleto_`.

## Pendientes que no son de Preset
6. Confirmar con el docente si basta **1 tablero** con los 8 gráficos (el skill espera 2).
7. Definir quién del equipo construyó a mano al menos un KPI y cómo explica su cálculo. Sugerencia: quien cree el KPI-04 del punto 2 puede explicarlo: numerador `ruta_digital` (expedientes que terminan por el portal), denominador `entraron_expediente`, solo TO-BE.

## Verificación al terminar
| Elemento | Esperado |
|---|---|
| Título del tablero | Contiene «SINTÉTICO / DEMOSTRACIÓN» |
| Eje del gráfico de actividades | «Días hábiles por solicitud» |
| KPI-04 | 85,4 % |
| KPI-02 / KPI-03 | 20,0 % / 6,9 % y 10,5 % / 2,8 % |
| Datasets | Sin `csv_storage` ni `Preaprobado` (o renombrados) |
| ROI / recuperación | 16,7 % / 10,1 meses (sin cambio) |
