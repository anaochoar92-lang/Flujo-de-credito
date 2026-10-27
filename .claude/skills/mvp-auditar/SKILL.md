---
name: mvp-auditar
description: Ejecutar pruebas técnicas y cuestionar consistencia SOP-EARS-BPMN-API-DB.
metadata:
  opencode/slash: "true"
---
# mvp-auditar

**Finalidad:** Ejecutar pruebas técnicas y cuestionar consistencia SOP-EARS-BPMN-API-DB.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `tests/`, EARS, `app/`, el estado del entorno..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Qué prueba demostraría que la mejora funciona?
2. ¿Qué ocurre cuando un usuario completa dos veces la misma tarea?
3. ¿Qué integración externa no ha sido probada todavía?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Corre `python -m pytest -q`, verifica formatos BPMN y evalúa: variables, actor, error de red, task ajena, duplicación, falta de CHIP, uso de datos sensibles, permisos. Contrasta resultado esperado vs observado.

## Salida verificable

Crear `especificaciones/auditoria-equipo.md` con pruebas, fallos, riesgos, bloqueos y plan de corrección.

## Control de calidad / límite

No marcar como superado nada que no tenga evidencia. Diferenciar pruebas offline de integración real.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
