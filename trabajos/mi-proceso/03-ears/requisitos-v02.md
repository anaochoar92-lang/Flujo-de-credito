# Requisitos EARS v02 — AS-IS · Flujo de crédito (cambios sobre v01)

**Versión:** v02 · 2026-10-24 · **Nivel:** AS-IS · **Fuente nueva:** entrevista, ronda 2 (PREG-007, PREG-008, PREG-013, PREG-014).
`requisitos.md` (v01) **se conserva** y sigue vigente en todo lo que no aparece aquí.

## 1. REQ modificados
| ID | Patrón | Requisito v02 | Fuente | Estado |
|---|---|---|---|---|
| REQ-012 | Comportamiento no deseado | Si el expediente no está completo **10 días hábiles** después de que el cliente aceptó la decisión, entonces el sistema deberá cerrar la solicitud automáticamente con estado «Cerrada por expediente incompleto». Cada devolución de Despacho a Legal **reinicia** el conteo. | ENT PREG-003, PREG-013 | Confirmado por entrevistado (se quita el [PENDIENTE]) |
| REQ-017 | Complejo | (Sin cambio de texto.) El motivo de devolución más frecuente es que algún documento tiene **más de 1 mes** desde su expedición. [PENDIENTE: si el motivo se registra en el sistema] | PB-F16; ENT PREG-003, PREG-014 | Confirmado en fuente y por entrevistado |

## 2. Procedimientos humanos modificados y nuevos
| ID | Procedimiento | Fuente | Estado |
|---|---|---|---|
| PROC-006 (mod.) | Legal reunirá los cuatro documentos obligatorios. Aproximadamente la mitad del tiempo (≈ 2,5 de 5 días hábiles) es espera de los documentos del cliente y la otra mitad, trabajo de Legal. | ENT PREG-003, PREG-007 | Confirmado por entrevistado (tiempos estimados) |
| PROC-007 (mod.) | Legal digitalizará el expediente completo. El método actual de escaneo es lento (≈ 3 días hábiles). | ENT PREG-007 | Confirmado por entrevistado |
| PROC-008 (mod.) | El Analista (Despacho) verificará y autorizará el expediente y lo enviará **en físico** a Desembolso mediante mensajero. El soporte físico es **obligatorio** por ser sector bancario y estatal. La espera del mensajero y el traslado forman parte de los ≈ 4 días de Despacho. | ENT PREG-007, PREG-008 | Confirmado por entrevistado |
| PROC-010 (nuevo) | El Analista (Despacho) verificará que cada documento del expediente tenga **1 mes o menos** desde su fecha de expedición y, si alguno lo supera, devolverá el expediente a Legal. | ENT PREG-014 | Confirmado por entrevistado |

## 3. Restricciones de negocio (no son requisitos del sistema)
| ID | Restricción | Fuente | Uso |
|---|---|---|---|
| RN-01 | El expediente debe llegar en **físico** a Desembolso. | ENT PREG-008 | El TO-BE no puede eliminar el sobre; solo acelerarlo o hacerlo en paralelo |
| RN-02 | Los documentos del expediente deben tener **1 mes o menos** desde su expedición. | ENT PREG-014 | Candidata a validación temprana en el TO-BE |

## 4. Datos de ejemplo para la línea base (no son requisitos)
1.000 solicitudes (periodo por confirmar; se asume mensual) · 20 % devueltas de Despacho a Legal · 10 % cerradas por los 10 días hábiles. Fuente: ENT PREG-014. Son **datos de ejemplo**, no una medición.

## 5. Resumen v02
| Indicador | v01 | v02 |
|---|---|---|
| REQ | 18 | 18 (1 modificado) |
| PROC | 9 | 10 (3 modificados, 1 nuevo) |
| REQ con [PENDIENTE] | 6 | 5 |
