# Guía de decisión EARS → BPMN 2.0

## Importante
EARS es una técnica de redacción de requisitos; BPMN 2.0 es una notación para flujos de trabajo. **No existe una correspondencia automática uno a uno**. Las actividades procedimentales humanas se mantienen como tales; un requisito de seguridad o auditoría no se traduce forzosamente a una compuerta.

| Evidencia en SOP/EARS | Pregunta al dueño del proceso | BPMN candidato | Advertencia de modelado |
|---|---|---|---|
| Inicio por solicitud | ¿Qué recibe quién? | `startEvent` (tipo mensaje si aplica) | Un mensaje de inicio crea instancia; no equivale a una tarea |
| Trabajo humano | ¿Quién ejecuta y dónde? | `userTask` o `task` | `userTask` puede requerir implementación para ejecución |
| Automatización | ¿Qué sistema invoca? | `serviceTask` | No inventar endpoint ni worker |
| Decisión sí/no | ¿Son excluyentes/exhaustivas? | `exclusiveGateway` | Rotular cada salida, documentar condición |
| Varias alternativas posibles | ¿Se pueden activar varias? | `inclusiveGateway` | Revisar cuidadosamente convergencia |
| Actividades simultáneas | ¿Deben completarse todas antes de avanzar? | `parallelGateway` de bifurcación y unión | Dos flujos no implican siempre paralelo |
| Compite pago con vencimiento | ¿Se activa sólo el primero que ocurre? | `eventBasedGateway` → catch events | Cada salida debe conducir a catch event o receive task válido |
| Recordatorio en fecha | ¿Es fecha, intervalo, calendario laboral? | `intermediateCatchEvent` timer | Expresión técnica no se inventa |
| Plazo de tarea | ¿Interrumpe el trabajo al vencer? | `boundaryEvent` timer | Definir interruptivo/no interruptivo |
| Envío de aviso | ¿Hay sistema emisor? | `sendTask` o `intermediateThrowEvent` mensaje | Delimitación de pool importa |
| Recepción de aviso | ¿Qué mensaje se espera? | `intermediateCatchEvent` mensaje | Si no llega, modelar timeout cuando se conozca |
| Coordinación entre organizaciones | ¿Se comunican sin compartir el mismo proceso? | Dos pools + `messageFlow` | Nunca sequenceFlow cruzando pools |
| Roles internos | ¿Actúan en el mismo proceso? | `lane` | Nunca messageFlow entre lanes del mismo pool |
| Error durante una actividad | ¿Se interrumpe, reintenta, escala? | `boundaryEvent` / ruta alternativa | Especificar semántica, no dibujar error genérico |
| Cancelación/desistimiento | ¿Termina instancia o sólo rama? | `endEvent` / evento específico | Terminate end cancela todo el alcance, no es un fin normal |
| Variantes de proceso | ¿Se repite un bloque reutilizable? | Subproceso/call activity | Generador de clase no implementa anidamiento |

## Tipos BPMN: qué muestra el taller y qué soporta el generador
La **metodología** exige evaluar tareas, secuencias, flujos de mensajes, eventos de inicio, intermedios, finales y límite; compuertas exclusivas, paralelas, inclusivas y basadas en eventos; errores, escalaciones, señales, condiciones y tiempos.

El **generador estándar incluido** cubre tareas básicas, start/end, catch/throw/boundary, compuertas XOR/AND/OR/basadas en eventos, temporizadores y eventos mensaje/señal/error/escalación/terminate, pools, lanes, secuencias y mensajes. No construye automáticamente subprocesos anidados, multi-instance, transacciones, compensación, event subprocess, coreografía ni las extensiones específicas de ejecución de Camunda. Esos modelos avanzados pueden editarse en Camunda y revisarse con el skill `reconciliar-bpmn` sin pretender que el generador los soporte.

## Formulación de condiciones
- «Si monto > X» es una **regla de decisión**, no por sí sola un gateway válido si X no está definido.
- «Validar datos» describe actividad, pero falta decidir exactamente cuáles son válidos.
- «Si nadie contesta» requiere definir un evento observable y un periodo de espera.
- Las ramas deben tener nombres legibles; expresiones `conditionExpression` ejecutables requieren sintaxis compatible con el motor elegido, no se deducen del texto.

## Etapas de validación
1. Sintaxis XML parseable.
2. Integridad de IDs, referencias, estructura BPMN DI (script del kit).
3. Comprobación BPMN 2.0 XSD con validador formal externo, si se incorpora a la infraestructura (no incluido).
4. Revisión visual y lint del perfil Camunda Modeler.
5. Revisión semántica por participante y docente.
6. Validación de despliegue/ejecución sólo si explícitamente se decide construir automatización ejecutable.
