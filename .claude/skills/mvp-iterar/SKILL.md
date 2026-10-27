---
name: mvp-iterar
description: Planear una mejora autónoma a partir de las pruebas sin romper el MVP demo.
metadata:
  opencode/slash: "true"
---
# mvp-iterar

**Finalidad:** Planear una mejora autónoma a partir de las pruebas sin romper el MVP demo.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `especificaciones/`, `AGENTS.md`, `docs/02-sesiones-60-min.md`..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Cuál es el cambio más pequeño que aumenta valor al usuario?
2. ¿Qué EARS/BPMN/tablas/endpoints se verán afectados?
3. ¿Cómo se comprobará sin perder funcionamiento previo?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Ordena cambios en tamaño S/M/L y riesgo. Prioriza 1 historia de menos de 90 minutos. Escribe EARS, plan con archivos involucrados, test negativo y fallback. Espera confirmación. Al terminar, regresa a `mvp-auditar`.

## Salida verificable

Crear `especificaciones/backlog-autonomo.md` con siguientes 3 incrementos y criterio de aceptación para cada uno.

## Control de calidad / límite

Nunca rehacer todo el proyecto ni introducir agentes autónomos en producción como atajo.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
