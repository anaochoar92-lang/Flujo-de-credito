---
name: arquitectura-bpmn
description: Diseña el mapeo EARS→BPMN identificando pools, lanes, tareas, compuertas, eventos y flujos antes de generar XML.
license: MIT
compatibility: opencode
---

# arquitectura-bpmn

## Toma de decisiones BPMN
Usa la tabla `docs/mapa-ears-bpmn.md` y la referencia `docs/contrato-json.md`.
- Eventos que disparan instancias → `startEvent` (plain/message/timer según el caso).
- Intervención humana → `userTask` si se usa motor de tareas; `task` si el mapa es descriptivo.
- Servicio automático → `serviceTask` conceptual, **sin** binding técnico simulado.
- Decisión por condiciones → `exclusiveGateway` si son excluyentes, `inclusiveGateway` si varias pueden cumplirse.
- Trabajos simultáneos → `parallelGateway` con bifurcación y convergencia semánticamente revisadas.
- Espera de **uno entre varios eventos** → `eventBasedGateway` y eventos intermedios `intermediateCatchEvent`.
- Plazo que afecta una tarea en curso → `boundaryEvent` timer, con `cancelActivity` explícito.
- Interacción entre actores institucionalmente independientes → pools y `messageFlow`.
- Roles internos de una entidad → lanes.
- Lógica extensa → considerar `subProcess` / `callActivity` en revisión manual; la herramienta incluida no genera subprocesos anidados.

## Salida
Redacta `04-modelo/diseno-logico.md` con decisiones de modelado y alternativas descartadas.
Escribe `04-modelo/especificacion.json` que cumpla el contrato del kit. Cada nodo debe usar nombre entendible (verbo+objeto para tareas, pregunta para gateway). Etiqueta los flujos salientes de cada decisión. Reutiliza nombres/IDs estables. No generes XML hasta documentar y validar la coherencia del JSON.

## Política de dudas
Se permiten diagramas `DRAFT` que indiquen «Por confirmar» y propuestas, pero nunca presentan una regla hipotética como operativa. Añade `04-modelo/asunciones.md` y evita condiciones ejecutables no confirmadas.
