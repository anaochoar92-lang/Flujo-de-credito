# Requisitos EARS v01 — AS-IS · Flujo de crédito (Expomóvil)

**Versión:** v01 · 2026-10-23 · **Nivel:** AS-IS · **Skill:** `redactar-ears`.
**Fuentes:** `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx` (XLS, hoja «Proceso BPMN» = `PB`) y entrevista, ronda 1 (`ENT`, PREG-001 a PREG-004).
**Sistema:** la fuente no nombra ningún sistema. En los REQ se usa «el sistema» para referirse al sistema donde se registra la solicitud. [PENDIENTE: nombre del sistema, PREG-011]
**Matriz:** `matriz-trazabilidad.csv` · **Pruebas:** `escenarios-gherkin.md` · **Pendientes:** `pendientes.md`.

## 1. Requisitos del sistema (REQ)
| ID | Patrón | Requisito | Fuente | Estado |
|---|---|---|---|---|
| REQ-001 | Dirigido por evento | Cuando el cliente manifieste interés en un crédito Expomóvil, el sistema deberá permitir a la Persona de Negocio registrar una solicitud con los datos del cliente, el monto, el plazo y el vehículo. [PENDIENTE: canal de inicio, PREG-005] | PB-F5, PB-F6 | Confirmado en fuente |
| REQ-002 | Dirigido por evento | Cuando la Persona de Negocio envíe la solicitud, el sistema deberá asignar la actividad «Evaluar solicitud» a la Persona de Riesgo. | PB-F6 | Confirmado en fuente |
| REQ-003 | Complejo | Mientras la solicitud esté en «Evaluar solicitud», cuando la Persona de Riesgo registre la decisión «Apto», el sistema deberá asignar la actividad «Analizar crédito» al Analista de crédito. | PB-F8 | Confirmado en fuente |
| REQ-004 | Complejo | Mientras la solicitud esté en «Evaluar solicitud», cuando la Persona de Riesgo registre la decisión «Corregir», el sistema deberá devolver la solicitud a la Persona de Negocio en «Crear solicitud». | PB-F8 | Confirmado en fuente |
| REQ-005 | Complejo | Mientras la solicitud esté en «Evaluar solicitud», cuando la Persona de Riesgo registre la decisión «Rechazar», el sistema deberá cerrar la solicitud con estado «Rechazada por Riesgo» y no crear ninguna actividad siguiente. | ENT PREG-002 | Confirmado por entrevistado |
| REQ-006 | Complejo | Mientras la solicitud esté en «Analizar crédito», cuando el Analista registre la decisión «Rechazar», el sistema deberá cerrar la solicitud con estado «Rechazada» y no crear ninguna actividad siguiente. [PENDIENTE: si se informa al cliente del rechazo, PREG-004 b] | PB-F10, PB-F11 | Confirmado en fuente |
| REQ-007 | Complejo | Mientras la solicitud esté en «Analizar crédito», cuando el Analista registre la decisión «Aprobar» o «Aprobar con condiciones», el sistema deberá asignar al Analista la actividad «Informar decisión al cliente». | ENT PREG-004 | Confirmado por entrevistado |
| REQ-008 | Dirigido por evento | Cuando el Analista registre que el cliente no acepta la decisión o no continúa, el sistema deberá cerrar la solicitud con estado «Cerrada por no aceptación del cliente». | ENT PREG-004 | Confirmado por entrevistado |
| REQ-009 | Dirigido por evento | Cuando el Analista registre que el cliente acepta una aprobación con condiciones, el sistema deberá asignar a la Persona de Negocio la actividad «Modificar datos del crédito» y, al completarla, volver a asignar «Analizar crédito» al Analista. | PB-F10; ENT PREG-004 | Confirmado por entrevistado (AS-01: no se repite Riesgo) |
| REQ-010 | Dirigido por evento | Cuando el Analista registre que el cliente acepta una aprobación sin condiciones, el sistema deberá asignar a Legal la actividad «Recopilar expediente». | PB-F10; ENT PREG-004 | Confirmado por entrevistado |
| REQ-011 | Ubicuo | El sistema deberá exigir en el expediente los cuatro documentos obligatorios: documento de identidad, comprobante de ingresos, estado de cuenta bancario y pagaré. | ENT PREG-003 | Confirmado por entrevistado |
| REQ-012 | Comportamiento no deseado | Si el expediente no está completo 10 días después de [PENDIENTE: momento desde el que se cuenta y si son días hábiles o calendario, PREG-013], entonces el sistema deberá cerrar la solicitud automáticamente con estado «Cerrada por expediente incompleto». | ENT PREG-003 | Confirmado por entrevistado (cómputo pendiente) |
| REQ-013 | Complejo | Mientras la solicitud esté en «Recopilar expediente», cuando Legal registre «Documentación completa», el sistema deberá asignar a Legal la actividad «Escanear documentación». | PB-F13 | Confirmado en fuente |
| REQ-014 | Complejo | Mientras la solicitud esté en «Recopilar expediente», cuando Legal registre «Documentación incompleta», el sistema deberá mantener la actividad «Recopilar expediente» abierta. | PB-F13 | Confirmado en fuente |
| REQ-015 | Dirigido por evento | Cuando Legal termine «Escanear documentación», el sistema deberá asignar al Analista de crédito la actividad «Verificar y autorizar expediente» (Despacho). | PB-F14, PB-F15 | Confirmado en fuente |
| REQ-016 | Complejo | Mientras la solicitud esté en «Verificar y autorizar expediente», cuando el Analista registre «Documentación OK», el sistema deberá asignar a Desembolso la actividad «Desembolsar crédito». | PB-F16 | Confirmado en fuente |
| REQ-017 | Complejo | Mientras la solicitud esté en «Verificar y autorizar expediente», cuando el Analista registre que la documentación falta, se rechaza o no cuadra, el sistema deberá devolver la solicitud a Legal en «Recopilar expediente». [PENDIENTE: si se registra un motivo de devolución] | PB-F16; ENT PREG-003 | Confirmado en fuente y por entrevistado |
| REQ-018 | Dirigido por evento | Cuando Desembolso registre el desembolso, el sistema deberá cerrar la solicitud con estado «Crédito desembolsado». [PENDIENTE: titular de la cuenta y gestiones post-desembolso, PREG-009] | PB-F17, PB-F18 | Confirmado en fuente |

## 2. Procedimientos humanos (PROC)
| ID | Procedimiento | Actor | Fuente |
|---|---|---|---|
| PROC-001 | La Persona de Negocio capturará la información del cliente y del producto Expomóvil (monto, plazo y vehículo). | Persona de Negocio | PB-E6 |
| PROC-002 | La Persona de Riesgo evaluará si el cliente es apto según su perfil, el buró y las políticas. [PENDIENTE: criterios concretos, PREG-006] | Persona de Riesgo | PB-E7 |
| PROC-003 | El Analista de crédito analizará la capacidad de pago, el riesgo y las garantías y emitirá una recomendación. | Analista de crédito | PB-E9 |
| PROC-004 | El Analista de crédito informará la decisión al cliente y registrará si el cliente continúa. [PENDIENTE: canal y plazo de respuesta] | Analista de crédito | ENT PREG-004 |
| PROC-005 | La Persona de Negocio modificará los datos del crédito según las condiciones aprobadas. | Persona de Negocio | PB-F10; ENT PREG-004 |
| PROC-006 | Legal reunirá los cuatro documentos obligatorios del expediente. [PENDIENTE: quién los entrega] | Legal | PB-E12; ENT PREG-003 |
| PROC-007 | Legal digitalizará el expediente completo y lo enviará a Despacho. | Legal | PB-E14 |
| PROC-008 | El Analista de crédito verificará que la documentación sea correcta y cuadre, la autorizará y la enviará en sobre físico a Desembolso. [PENDIENTE: para qué se usa el sobre, PREG-008] | Analista de crédito | PB-E15; ENT PREG-003 |
| PROC-009 | Desembolso verificará el sobre, desembolsará en la cuenta indicada y realizará las gestiones post-desembolso. | Desembolso | PB-E17 |

## 3. Cobertura fuente → requisitos
| Elemento fuente | Cubierto por | Estado |
|---|---|---|
| E1 Inicio | REQ-001 | Cubierto |
| T1 Crear solicitud | REQ-001, REQ-002, PROC-001 | Cubierto |
| T2 Evaluar solicitud | REQ-002, PROC-002 | Cubierto |
| G1 ¿Cliente apto? | REQ-003, REQ-004, REQ-005 | Cubierto |
| T3 Analizar crédito | REQ-003, PROC-003 | Cubierto |
| G2 ¿Decisión del análisis? | REQ-006, REQ-007, REQ-009 | Cubierto |
| E2 Fin rechazo | REQ-006 | Cubierto |
| T4 Recopilar expediente | REQ-010, REQ-011, REQ-012, PROC-006 | Cubierto |
| G3 ¿Documentación completa? | REQ-013, REQ-014 | Cubierto |
| T5 Escanear documentación | REQ-015, PROC-007 | Cubierto |
| T6 Despacho y expediente | REQ-015, REQ-016, REQ-017, PROC-008 | Cubierto |
| G4 ¿Documentación OK? | REQ-016, REQ-017 | Cubierto |
| T7 Desembolso y post-desembolso | REQ-016, REQ-018, PROC-009 | Cubierto (post-desembolso pendiente) |
| E3 Fin desembolsado | REQ-018 | Cubierto |
| Hoja «Tiempos» | — | Informativo: es la base de los KPI, no un requisito |

## 4. Resumen
18 REQ (13 confirmados en fuente, 5 confirmados por entrevistado) y 9 PROC. Seis REQ llevan un dato [PENDIENTE] que no cambia la regla.
