---
name: mvp-camunda
description: Conectar la aplicación al clúster Camunda 8 existente usando REST API v2.
metadata:
  opencode/slash: "true"
---
# mvp-camunda

**Finalidad:** Conectar la aplicación al clúster Camunda 8 existente usando REST API v2.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `docs/03-camunda-real.md`, `bpmn/`, `.env.example` y API..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Camunda 8.8+ REST v2 o Camunda 7?
2. ¿Cuáles son los processDefinitionId publicados?
3. ¿Las userTask son Camunda user tasks y el backend tiene permisos?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Verifica URL raíz, token, processDefinitionId, variables FEEL, tareas publicadas. Cambia `ENGINE_MODE=camunda` solo con consentimiento humano. Inicia 1 instancia real, consulta tareas, completa 1. Si falla, identifica 401/403/404/422/503 o latencia de índice; no reescribe todo el BPMN por intuición.

## Salida verificable

Evidencia de HTTP, clave de instancia y dos tareas en Camunda, o informe explícito de bloqueo y contingencia.

## Control de calidad / límite

No mostrar credenciales al agente, no desplegar sobre cluster productivo, no afirmar que mock equivale a prueba real.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
