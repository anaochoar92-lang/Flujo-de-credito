# Requisitos EARS del MVP — paso 21 (`/21-ears`)

**Fecha:** 2026-10-26 · **Skill:** `mvp-ears` · **Estado:** **BORRADOR — pendiente de aprobación (EARS-1 a EARS-3, ronda 17)**. No se escribe código hasta aprobarlo.
**Base:** `14-mvp/alcance-equipo.md` y `08-tobe/requisitos-ears-to-be.md`. Datos SINTÉTICOS.
**Efecto en los números:** ninguno (ROI 16,7 % y KPI sin cambio).

| ID | Tipo | EARS | Prueba positiva | Prueba adversarial | Endpoint (propuesto) | Elemento BPMN | Origen |
|---|---|---|---|---|---|---|---|
| REQ-MVP-01 | Comportamiento no deseado | Si un documento cargado tiene **fecha de expedición de más de 20 días calendario** respecto a la fecha de carga, o está marcado como **ilegible**, o falta alguno de los 4 documentos, entonces el sistema deberá rechazar la carga, indicar el motivo por documento y sumar **1 intento** a ese documento, hasta un máximo de **5**. | Carga de 4 documentos con fecha de hace 5 días y legibles → estado «Documentos válidos», 0 intentos sumados. | Pagaré con fecha de hace 25 días → respuesta 422 con motivo «vencido (> 20 días)», intento del pagaré = 1; al 6.º intento → 409 «intentos agotados, pasa a ruta en papel». | `POST /api/casos/{id}/documentos` | `TB_RCV_DOCS` → `TB_SVC_VALIDAR` → `TB_GW_VALIDO` | REQ-TOBE-004, 005, 007 |
| REQ-MVP-02 | Comportamiento no deseado | Si los 4 documentos son válidos pero el **nombre, la cédula, el salario o el monto** no coinciden entre ellos, entonces el sistema deberá crear la tarea **«Revisar documento dudoso»** para **Legal** y no enviar el caso a Despacho hasta que Legal decida. | Cédula distinta entre identidad y pagaré → aparece 1 tarea abierta de Legal; Despacho no tiene tarea. Legal acepta → se crea la tarea de Despacho. | Legal rechaza → caso «Pasa a ruta en papel», sin tarea de Despacho. Completar dos veces la misma tarea → la segunda devuelve 409. | `GET /api/tareas?rol=legal`, `POST /api/tareas/{id}/completar` | `TB_ACT_REVISAR`, `TB_GW_LEGAL` | REQ-TOBE-006 |
| REQ-MVP-03 | Por evento | Cuando los 4 documentos sean válidos (y, si hubo caso dudoso, Legal lo haya aceptado), el sistema deberá crear la tarea **«Verificar expediente digital»** para **Despacho**; cuando Despacho la complete con resultado **OK**, el caso deberá quedar en estado **«Expediente digital verificado»** con fecha y hora en la bitácora. | Caso sin diferencias → tarea de Despacho → completar OK → estado final y evento en la bitácora exportable a CSV. | Completar sin indicar resultado → 422. Resultado «pedir corrección» → caso vuelve a «Esperando documento corregido» y no queda verificado. | `GET /api/tareas?rol=despacho`, `POST /api/tareas/{id}/completar`, `GET /api/casos/{id}/bitacora`, `GET /api/export/eventos.csv` | `TB_ACT_VERIF`, `TB_GW_VERIF` | REQ-TOBE-009 (a) |

## Términos que se evitaron
«rápido», «automático», «correctamente»: se reemplazaron por reglas observables (20 días, 5 intentos, 4 campos comparados, estado final con fecha).

## Preguntas para aprobar (ronda 17)
- **EARS-1:** ¿Los 20 días se cuentan en días **calendario** desde la fecha de expedición hasta el día de la carga? (El AS-IS dice «20 días» sin especificar).
- **EARS-2:** En el MVP, la legibilidad la marca una persona con una casilla (no hay lectura automática). ¿De acuerdo?
- **EARS-3:** ¿Apruebas REQ-MVP-01 a 03 como están, o cambias algo?
