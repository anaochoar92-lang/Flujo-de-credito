---
name: modelar-datos
description: "Construir diccionario de datos, CSV comparables y pruebas de calidad sin PII"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Objetivo
Pasar de preguntas de KPI a campos en una tabla de casos/actividades. Si hay datos reales verificar permisos y anonimizar antes de subir a Preset.

## Acciones
1. Leer `datos/demo/casos.csv`, `datos/demo/actividades.csv`, `docs/diccionario-kpis-y-ecuaciones.md` y KPI elegidos.
2. Preguntar: ¿hay datos reales, entrevista, estimaciones o simulación? ¿cuántas observaciones? ¿están consentidas/anonimizadas?
3. Explicar granularidad: 1 fila/caso/escenario en `casos.csv`, 1 fila/actividad/caso/escenario en `actividades.csv`; `id_par` permite comparaciones hipotéticas del mismo caso.
4. Si quieren demostración ejecutar `py scripts/taller_kpi.py todo` (Windows) o `python3 scripts/taller_kpi.py todo`. Los CSV generados son **SINTETICOS**. Si usan datos propios, crear encabezados como en `datos/demo/casos.csv`, validar con `taller_kpi.py validar`, preparar con `preparar`.
5. Producir `09-datos/diccionario.md` con nombre/tipo/nullable/criterio captura/origen/protección; `09-datos/registro_calidad.md` con duplicados, nulos, outliers, fecha e inconsistencias.
6. Sugerir fuentes de proceso: log de BPMN, sistema transaccional, formularios, bitácora de aprobaciones. No simular que existe un log si no existe.

## Criterio de aprobación
Todos los KPIs tienen campos calculables, unidades homogéneas y denominador confiable. No unirse tabla de casos y tabla de actividades sumando casos duplicados.
