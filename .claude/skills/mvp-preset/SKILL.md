---
name: mvp-preset
description: Crear KPI trazables y llevar los CSV o PostgreSQL de solo lectura a Preset.
metadata:
  opencode/slash: "true"
---
# mvp-preset

**Finalidad:** Crear KPI trazables y llevar los CSV o PostgreSQL de solo lectura a Preset.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `preset/GUIA.md`, los endpoints CSV y el diccionario ER..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Qué mejora promete el TO-BE y cómo se mide?
2. ¿Qué columnas se necesitan para el numerador y denominador?
3. ¿Los datos son reales o sintéticos?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Comienza con export CSV sin servicios externos, define tasa de cierre y tiempo de ciclo, carga CSV en Preset manualmente si la cuenta lo permite. Para Postgres usar vistas + rol solo lectura y SSL. Prepara un widget creado manualmente por el estudiante.

## Salida verificable

KPI en formato nombre/fórmula/unidad/fuente/granularidad/meta/limitación, CSV y captura/estado de widget Preset.

## Control de calidad / límite

No transformar tiempo de ciclo en ROI sin horas efectivas, volumen y supuesto de monetización.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
