---
name: mvp-contexto
description: Reducir el SOP y BPMN a un MVP de una sola historia de negocio.
metadata:
  opencode/slash: "true"
---
# mvp-contexto

**Finalidad:** Reducir el SOP y BPMN a un MVP de una sola historia de negocio.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `contexto/01-negocio.md`, el SOP y los BPMN AS-IS/TO-BE..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Qué actor inicia el proceso y qué recibe al terminar?
2. ¿Qué máximo de tres user tasks mostrarán en el frontend?
3. ¿Cuáles son los límites legales y las tareas que aún NO automatizaremos?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Selecciona una porción de proceso (vertical slice) con un evento inicial y final. Construye una tabla de actividad, responsable, dato de entrada, resultado, elementId BPMN y modo manual/automático. Separa dato fuente y supuesto.

## Salida verificable

Registra en `especificaciones/alcance-equipo.md` la historia de usuario, definición de terminado y 3 exclusiones.

## Control de calidad / límite

No incluir todo el flujo institucional: el taller solo valida un segmento operable.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
