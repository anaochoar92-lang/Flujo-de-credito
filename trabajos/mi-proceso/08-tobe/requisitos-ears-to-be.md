# Requisitos EARS TO-BE — Flujo de crédito preaprobado Expomóvil (v01)

> **Son requisitos de una PROPUESTA, no de un proceso observado.** El AS-IS (`03-ears/requisitos.md` y `requisitos-v02.md`) se conserva sin cambios y sigue siendo la ruta de respaldo (TB-4).

**Versión:** v01 · 2026-10-24 · **Nivel:** TO-BE · **Skill:** `disenar-tobe`
**Fuentes:** paquete A (PRIO-1), PRIO-2, PRIO-3, DG-4, PREG-017 y la ronda 7 (TB-1 a TB-4) de `02-analisis/entrevista.md`.

## 1. Requisitos del sistema (REQ-TOBE-*)
| ID | Patrón | Requisito | Fuente | Estado |
|---|---|---|---|---|
| REQ-TOBE-001 | Por evento | Cuando se registre que el cliente **acepta la decisión** de un crédito aprobado sin condiciones, el sistema deberá enviar al cliente, **por correo**, el enlace al portal de carga de documentos. | TB-1; PREG-017 | Confirmado por entrevistado |
| REQ-TOBE-002 | Por evento | Cuando se envíe el enlace del REQ-TOBE-001, el sistema deberá iniciar el conteo de **10 días hábiles** del expediente. | TB-1; PREG-013; REQ-012 | Confirmado por entrevistado |
| REQ-TOBE-003 | Ubicuo | El portal deberá permitir que el cliente cargue los cuatro documentos obligatorios: documento de identidad, comprobante de ingresos, estado de cuenta bancario y pagaré. | PREG-003; PREG-017 | Confirmado por entrevistado |
| REQ-TOBE-004 | Por evento | Cuando el cliente cargue un documento, el sistema deberá validar que (a) estén los cuatro documentos, (b) cada uno esté **expedido hace 20 días o menos** y (c) sea **legible**. | TB-2; PRIO-2; RN-02 | Confirmado por entrevistado |
| REQ-TOBE-005 | Comportamiento no deseado | Si un documento no cumple el REQ-TOBE-004, entonces el sistema deberá avisar al cliente del motivo y pedirle que lo vuelva a cargar, hasta un máximo de **5 intentos por cada documento**. | TB-3; TB-6 | Confirmado por entrevistado |
| REQ-TOBE-006 | Comportamiento no deseado | Si el **nombre, la cédula, el salario o el monto** no son iguales entre los documentos (caso dudoso), entonces el sistema deberá enviar el expediente a **Legal** para que lo revise y decida. | TB-2; TB-3; TB-7; TB-8 | Confirmado por entrevistado |
| REQ-TOBE-007 | Comportamiento no deseado | Si el cliente agota los 5 intentos de un documento, entonces el sistema deberá pasar la solicitud a la **ruta actual en papel** (Legal recopila el expediente). | TB-3; TB-4; AS-T1 | Confirmado por entrevistado (ronda 8) |
| REQ-TOBE-008 | Comportamiento no deseado | Si el portal no está disponible o el cliente no puede usarlo, entonces el **área de IT** deberá registrar el paso de la solicitud a la **ruta actual en papel** (AS-IS v02 desde `ACT_006`). | TB-4; TB-9 | Confirmado por entrevistado |
| REQ-TOBE-009 | Por evento | Cuando los cuatro documentos sean válidos, el sistema deberá, **al mismo tiempo**, (a) enviar el expediente digital a Despacho para su verificación y (b) programar la recogida de los originales y avisar al cliente. | DG-4; OPP-04; RN-01 | Propuesta (paquete A) |
| REQ-TOBE-010 | Comportamiento no deseado | Si el mensajero certificado no logra recoger los originales, entonces **Legal** deberá recopilarlos por la ruta actual. | TB-4 | Confirmado por entrevistado |
| REQ-TOBE-011 | Por estado | Mientras se verifica el expediente digital, Legal deberá escanear los originales recogidos (el escaneo se mantiene). | PRIO-3 | Confirmado por entrevistado |
| REQ-TOBE-012 | Por evento | Cuando la verificación de Despacho esté OK **y** los originales estén escaneados, el sistema deberá habilitar el desembolso, con el expediente físico en camino a Desembolso. | RN-01; REQ-018 | Propuesta (paquete A) |
| REQ-TOBE-013 | Comportamiento no deseado | Si pasan **10 días hábiles** desde la aceptación sin documentos válidos, o desde que Despacho pidió un documento corregido sin recibirlo, entonces el sistema deberá cerrar la solicitud con estado «Cerrada por expediente incompleto». Cada corrección pedida por Despacho **reinicia** el conteo. | REQ-012; PREG-013; TB-5 | Confirmado por entrevistado |
| REQ-TOBE-014 | Ubicuo | El portal deberá mostrar al cliente el **estado de su solicitud** en cada hito: enlace enviado, documentos validados, en verificación, originales recogidos, desembolso. | CV-3; OPP-03 | Propuesta (paquete A) |
| REQ-TOBE-015 | Ubicuo | El área de **IT del banco** será la responsable de la operación y disponibilidad del portal. | TB-4 | Confirmado por entrevistado |

## 2. Procedimientos humanos (PROC-TOBE-*)
| ID | Procedimiento | Fuente | Estado |
|---|---|---|---|
| PROC-TOBE-001 | Legal revisará los documentos dudosos y decidirá si se aceptan o se pide al cliente cargarlos de nuevo. | TB-2; TB-3 | Confirmado por entrevistado |
| PROC-TOBE-002 | El Analista (Despacho) verificará que el expediente digital «cuadre». Si algo no cuadra, pedirá al cliente el documento corregido por el portal. | PROC-008; PROC-010 | Propuesta. La corrección reinicia los 10 días hábiles (TB-5, confirmado) |
| PROC-TOBE-003 | El mensajero certificado recogerá los originales en la casa del cliente y los entregará a Legal. | DG-4 | Confirmado por entrevistado |
| PROC-TOBE-004 | Legal escaneará los originales recogidos y enviará el sobre físico a Desembolso. | PRIO-3; RN-01 | Confirmado por entrevistado |

## 3. Requisitos AS-IS que cambian
| AS-IS | Qué pasa en el TO-BE |
|---|---|
| REQ-010, REQ-011, PROC-006 (Legal recopila) | Pasan a la **ruta de respaldo** (REQ-TOBE-007, 008 y 010) |
| REQ-013, REQ-014 (`GW_005` ¿Documentación completa?) | Los sustituye la validación automática (REQ-TOBE-004) en la ruta digital; siguen en la de respaldo |
| PROC-007 (escaneo en serie) | Se hace en paralelo a la verificación (REQ-TOBE-011) |
| PROC-010 (vigencia ≤ 1 mes en Despacho) | Se anticipa a la carga con un margen de 20 días (REQ-TOBE-004) |
| REQ-012 (10 días hábiles) | Se mantiene (REQ-TOBE-002 y 013) |

## 4. Ronda 8 (resuelta) y pendientes
- **AS-T1:** confirmado: al agotar los 5 intentos se va por la ruta en papel.
- **TB-5:** sí, la corrección pedida por Despacho reinicia los 10 días hábiles.
- **TB-6:** los 5 intentos son **por cada documento**.
- **TB-7:** «dudoso» = **los datos no coinciden**.
- **TB-8:** se comparan entre documentos el **nombre, la cédula, el salario y el monto**.
- **TB-9:** si el portal falla, **IT** lo detecta y registra el paso a la ruta en papel.
- **Sin pendientes abiertos** en los requisitos TO-BE.
