---
name: redactar-ears
description: Convierte un SOP confirmado y entrevistas en requisitos EARS verificables, sus pruebas Given/When/Then y matriz de trazabilidad.
license: MIT
compatibility: opencode
---

# redactar-ears

## Patrones EARS (Mavin et al.)
- Universal: «El sistema deberá [respuesta verificable]».
- Dirigido por evento: «Cuando [evento], el sistema deberá [respuesta]».
- Dirigido por estado: «Mientras [estado], el sistema deberá [respuesta]».
- Comportamiento no deseado: «Si [condición anómala], entonces el sistema deberá [respuesta segura]».
- Función opcional: «Cuando esté habilitada la función [X], el sistema deberá [respuesta]» (adaptación española del patrón `Where`).
- Complejo: combinación controlada, por ejemplo «Mientras [estado], cuando [evento], el sistema deberá [respuesta]».

## Reglas estrictas
1. Expresa respuesta específica, observable, medible y una sola obligación principal por `REQ-###`.
2. Distingue obligación **del sistema** de procedimiento **humano**. Las tareas humanas pueden representarse en BPMN, pero no atribuirse falsamente a un sistema automatizado.
3. Para humanos usa `PROC-###` separado, por ejemplo «La persona revisora verificará ...».
4. A cada EARS agrega fuente (`SOP etapa y paso`, o respuesta `PREG-###`), evento, precondición, resultado, actor, dato/evidencia, tipo de patrón, nivel AS-IS / TO-BE, estado y criterio de aceptación Gherkin.
5. Jamás deduzcas plazos, montos o reglas legales ausentes; marca `[PENDIENTE: ...]` y colócalos en backlog, no como regla aprobada.
6. No conviertas EARS no funcionales (seguridad, disponibilidad, accesibilidad) automáticamente en gateways.

## Archivos
Genera `03-ears/requisitos.md`, `03-ears/matriz-trazabilidad.csv`, `03-ears/escenarios-gherkin.md`, `03-ears/pendientes.md`. Incluye cobertura SOP→REQ; cada paso de SOP debe tener al menos estado documentado: cubierto, informativo o pendiente.
