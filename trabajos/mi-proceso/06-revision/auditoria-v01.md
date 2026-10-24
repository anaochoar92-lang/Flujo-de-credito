# Auditoría del BPMN v01 — Flujo de crédito (AS-IS)

**Fecha:** 2026-10-23 · **Skill:** `auditar-bpmn` · **Archivo:** `05-bpmn/proceso-v01.bpmn` · **Validación:** `05-bpmn/validacion-v01.json`.
Esta auditoría no sustituye la validación XSD ni el lint de Camunda. No se corrigió nada en silencio: los hallazgos quedan para decidir.

## A. Técnica
| ID | Severidad | Elemento | Evidencia | Impacto | Corrección sugerida |
|---|---|---|---|---|---|
| T-01 | EDITORIAL | `GW_001` a `GW_006` | 6 advertencias: gateways sin flujo por defecto ni condiciones formales | Ninguno en un modelo descriptivo; impide ejecutarlo | Ninguna en AS-IS. Definir condiciones solo si se llega a ejecutar |
| T-02 | EDITORIAL | `SVC_001`, `END_VENCIDA` | Avisos de «no alcanzable» | Falso positivo: se llega desde `TMR_001` | Ninguna |
| T-03 | EDITORIAL | `F_015` | La línea cruza `ACT_004` | Lectura más difícil | Arrastrar la línea en Camunda |
| T-04 | — | XML | XML bien formado; IDs únicos; 30 formas y 25 conectores DI; ningún flujo cruza pools | — | — |

## B. Semántica
| ID | Severidad | Elemento | Hallazgo | Impacto | Corrección sugerida |
|---|---|---|---|---|---|
| S-01 | IMPORTANTE | `TMR_001` + bucles `F_018` y `F_024` | Cada vez que el expediente vuelve a «Recopilar expediente», la tarea empieza de nuevo y el temporizador de 10 días **se reinicia**. Si el plazo real se cuenta una sola vez, el diagrama lo alarga sin límite | Afecta directamente al **objetivo clave** (tiempos de expediente) | Confirmar PREG-013. Si el plazo es único, envolver T4–G4 en un subproceso con el temporizador sobre el subproceso (requiere edición en Camunda) |
| S-02 | IMPORTANTE | `GW_006 → ACT_006` | La devolución de Despacho repite T4 + T5 + T6 (unos 12 días) y no tiene límite de vueltas ni motivo registrado | Es el mayor reproceso del flujo | Medir cuántas devoluciones hay y por qué (insumo para el diagnóstico) |
| S-03 | IMPORTANTE | `ACT_005 → ACT_003` | Se asumió que tras modificar datos no se repite Riesgo (AS-01) | Si sí se repite, el flujo es otro | Confirmar AS-01 |
| S-04 | IMPORTANTE | `ACT_009` | No hay salida si el sobre llega mal o si el desembolso falla | Fin feliz sin alternativa | PREG-009 |
| S-05 | EDITORIAL | `END_RECH_RIESGO`, `END_RECHAZADA` | No se informa al cliente del rechazo (AS-04) | Posible paso que falta | P-03 |
| S-06 | EDITORIAL | `GW_001 → ACT_001` | «Corregir datos» puede repetirse sin límite | Bucle sin salida propia (aunque ahora existe el rechazo) | Preguntar si hay un límite de correcciones |
| S-07 | EDITORIAL | Pool único | El cliente no está modelado como participante | Las esperas por el cliente (aceptación, documentos) no se ven como esperas | Añadir pool «Cliente» cuando se conozca el canal (PREG-005) |

No hay gateways paralelos ni basados en eventos, por lo que no hay problemas de sincronización.

## C. Trazabilidad
- Los 23 nodos tienen un `trace` en el JSON que apunta a la fuente (T1…T7, G1…G4, E1…E3) o a una respuesta PREG.
- Los 18 REQ tienen al menos un nodo o flujo en `03-ears/matriz-trazabilidad.csv`.
- REQ-011 (documentos obligatorios) se representa solo dentro de `ACT_006`: no es una decisión del flujo.
- Ningún nodo queda sin requisito.

## D. Usabilidad
- Todas las tareas usan verbo + objeto. «Despacho y expediente» se renombró como «Verificar y autorizar expediente (Despacho)».
- Las 6 decisiones están formuladas como pregunta y todas sus salidas tienen nombre.
- Carril «Sistema»: deja claro que el cierre por vencimiento no lo hace una persona.

## Resumen
0 bloqueantes · 4 importantes (S-01 a S-04) · 6 editoriales. El v01 es **apto como borrador AS-IS** para la revisión visual en Camunda. S-01 y S-02 son el punto de partida del diagnóstico, porque tocan el objetivo clave.
