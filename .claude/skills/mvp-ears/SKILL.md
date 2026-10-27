---
name: mvp-ears
description: Convertir necesidades del negocio en tres requisitos EARS con aceptación comprobable.
metadata:
  opencode/slash: "true"
---
# mvp-ears

**Finalidad:** Convertir necesidades del negocio en tres requisitos EARS con aceptación comprobable.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `especificaciones/01-requerimientos-EARS.md` y `especificaciones/alcance-equipo.md` si existe..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Cuál es el disparador exacto del requisito?
2. ¿Qué debería ocurrir si el dato falta?
3. ¿Qué API, tarea o evidencia puede demostrar el resultado?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Elige tres requisitos y usa patrón ubicuo, evento, estado, condicional o indeseado. Revisa expresiones ambiguas: rápido, seguro, automático, correctamente. Genera al menos un caso negativo y un mapeo hacia userTask o gateway.

## Salida verificable

Escribe `especificaciones/ears-equipo.md` con ID, EARS, prueba positiva, prueba adversarial, endpoint, elemento BPMN.

## Control de calidad / límite

No crear código antes de la aprobación de EARS.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
