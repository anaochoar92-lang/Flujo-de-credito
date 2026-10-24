---
name: definir-kpis
description: "Crear fichas de KPI medibles, objetivos y origen de datos usando AS-IS y TO-BE"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Antes de proponer KPI
Leer el SOP, AS-IS, TO-BE aprobado, `docs/diccionario-kpis-y-ecuaciones.md` y `docs/origen-presentacion-sesion3.md`. La presentación trata tiempos, costos, volumen, seguimiento, indicadores y ROI; no impone KPI específicos.

## Entrevista interactiva (máximo 4 por ronda)
1. ¿Qué decisión gerencial toma el equipo con este KPI?
2. ¿De qué evento/campo se obtiene numerador y denominador y quién lo registra?
3. ¿Cuál es el período, unidad, segmento y meta realista? ¿Se mide una situación real o escenario?
4. ¿Qué interpreta erróneamente alguien si compara casos distintos o promedio de porcentajes?

## Fichas
Crear `10-kpis/catalogo.md` (3–6 KPI, no lista interminable), una ficha como `plantillas/ficha-kpi.md` por KPI: ID, definición inequívoca, fórmula, unidad, granularidad, fuente, dueño, línea base/objetivo, error permitido, widget y trazabilidad a `REQ-TOBE`/tarea BPMN.

## Métrica vs KPI
Métrica = medida operacional; KPI = métrica elegida para evaluar objetivo clave. No confundir volumen de casos con éxito. Recomendados cuando aplican: horas trabajo/caso, ciclo/caso, tasa error, reproceso, costo variable/caso, capacidad y satisfacción. ROI requiere inversiones y monetización legítima.
