---
name: mvp-frontend
description: Integrar un formulario, lista de tareas humanas y evidencia desde el navegador.
metadata:
  opencode/slash: "true"
---
# mvp-frontend

**Finalidad:** Integrar un formulario, lista de tareas humanas y evidencia desde el navegador.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `app/static/index.html`, API y EARS..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Qué campos van en el formulario inicial?
2. ¿Qué ve el operador cuando una tarea aún no existe?
3. ¿Qué acción humana cambia el proceso?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Demuestra vertical slice: crear instancia, mostrar processInstanceKey, consultar user tasks, completar una, consultar bitácora. Usa `ENGINE_MODE=mock` primero. Mantén JS simple y backend para secretos.

## Salida verificable

Capturas o texto con URL, instancia creada, tarea activa, tarea completada y CSV. Si se modifica código, conservar test verde.

## Control de calidad / límite

No exponer la app en Internet sin autenticación. No autocompletar en nombre de un funcionario real.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
