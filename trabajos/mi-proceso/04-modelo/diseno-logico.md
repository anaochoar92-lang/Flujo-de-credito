# Diseño lógico — AS-IS v01 · Flujo de crédito

**Fecha:** 2026-10-23 · **Skill:** `arquitectura-bpmn` · **JSON:** `especificacion.json` · **Requisitos:** `../03-ears/requisitos.md`.

## Decisiones de modelado
| Tema | Decisión | Alternativa descartada y por qué |
|---|---|---|
| Pools | Un solo pool, «Banco», con 6 carriles | Pool «Cliente» con flujos de mensaje: la fuente no describe qué envía ni qué recibe el cliente; su respuesta la registra el Analista (PREG-004). Se puede añadir cuando se conozca el canal |
| Carriles | Los 5 roles de la fuente, más «Sistema» para el cierre automático | Poner el cierre dentro de Legal: lo ejecuta el sistema, no una persona (PREG-003) |
| Tareas humanas | `userTask` (la fuente indica que se envía la solicitud entre áreas) | `task` genérico: menos claro sobre quién actúa |
| Rechazo de Riesgo | Tercera salida de `GW_001`, con fin propio | — (nuevo, PREG-002) |
| Aprobación | `GW_002` con dos salidas: «Aprobar (con o sin condiciones)» y «Rechazar». La diferencia entre aprobar con o sin condiciones se resuelve después, en `GW_004` | Tres salidas en `GW_002`, dos de ellas hacia la misma tarea «Informar decisión»: duplicaba flechas |
| Cliente | «Informar decisión al cliente» (`ACT_004`) y la decisión «¿Cliente acepta y continúa?» (`GW_003`) en el carril del Analista | Evento de espera de mensaje: no se conoce el canal ni el plazo |
| Condiciones | Acepta con condiciones → «Modificar datos del crédito» (`ACT_005`, Negocio) → vuelve a «Analizar crédito». **No** repite Riesgo (AS-01) | Volver a «Crear solicitud» (`ACT_001`): obligaría a repetir Riesgo, y el entrevistado dijo «negocio y análisis» |
| Plazo de 10 días | Evento límite de temporizador **interruptor** (`TMR_001`) sobre «Recopilar expediente», que lleva a un cierre automático | Temporizador intermedio: no representa un plazo sobre una tarea en curso. **No** se escribe expresión de tiempo (`P10D`), porque falta saber si son días hábiles o calendario (PREG-013) |
| Bucles de expediente | `GW_005` «Incompleta» y `GW_006` «Falta / no cuadra» vuelven a `ACT_006` | — (fuente) |
| Despacho | Se renombra «Despacho y expediente» como **«Verificar y autorizar expediente (Despacho)»** (verbo + objeto) | Conservar el nombre original: no tiene verbo |
| Desembolso | «Desembolsar crédito y gestionar post-desembolso» en una sola tarea | Separar en dos: la fuente no describe el post-desembolso |

## Advertencia semántica conocida
Cuando un bucle (`F_018` o `F_024`) vuelve a «Recopilar expediente», la tarea **empieza de nuevo** y el temporizador `TMR_001` **se reinicia**. Si el plazo real de 10 días se cuenta una sola vez desde el inicio, este dibujo no lo representa. Se pregunta en PREG-013 y se registra en la auditoría.
