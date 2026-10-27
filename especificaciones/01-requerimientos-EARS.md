# Contrato EARS · MVP didáctico de cargas urbanísticas

Las claves EARS son los criterios de aceptación; antes de programar nuevos cambios hay que revisar su impacto.

| ID | Patrón | Requerimiento verificable | Prueba | BPMN / API |
|---|---|---|---|---|
| E-01 | Ubicuo | El MVP deberá permitir introducir un radicado, escenario, áreas, uso y CHIP de prueba. | POST `/api/cases` devuelve 201 | inicio AS-IS / TO-BE |
| E-02 | Dirigido por evento | Cuando un usuario envíe la solicitud, el backend deberá almacenar un caso y crear la instancia correspondiente en el orquestador configurado. | POST con `ENGINE_MODE=mock` o `camunda` | startEvent |
| E-03 | Dirigido por evento | Cuando se registre un caso, el backend deberá ejecutar una prevalidación determinista de los campos definidos. | evento `PREVALIDACION_AUTOMATICA` | antes de startEvent TO-BE |
| E-04 | Condicional | Si el CHIP está vacío, el escenario TO-BE deberá dirigir el caso a subsanación. | primer user task en modo mock; variable `validacionPreviaOk=false` | exclusiveGateway |
| E-05 | Condicional | Si la prevalidación es satisfactoria, TO-BE deberá omitir la tarea de subsanación. | primer user task de revisión | exclusiveGateway |
| E-06 | Dirigido por evento | Cuando exista una tarea humana activa, la interfaz deberá mostrarla con su clave y permitir completarla. | GET y POST de tareas | userTask |
| E-07 | Estado | Mientras un caso permanezca activo, la aplicación deberá preservar su radicado, identificador de instancia y eventos de tarea. | consultar DB | casos/eventos |
| E-08 | Dirigido por evento | Cuando una tarea se complete, el sistema deberá registrar responsable demo, instante y observaciones. | registro `TAREA_COMPLETADA` | API |
| E-09 | Ubicuo | El MVP deberá exponer CSV de casos, eventos e indicadores con encabezados consistentes. | GET export CSV | Preset |
| E-10 | Indeseado | Si Camunda no acepta la creación de instancia, el backend no deberá confirmar la persistencia local como caso exitoso. | error 502 y rollback | API |
| E-11 | Opcional | Cuando el docente configure PostgreSQL/Supabase, el MVP deberá utilizarlo mediante `DATABASE_URL`, sin cambios en los endpoints. | smoke test con instancia externa | almacenamiento |
| E-12 | Restricción | El MVP no deberá atribuir validez jurídica al valor monetario del ejemplo. | interfaz y contexto muestran advertencia | cálculo demo |

## Traza: flujo mínimo de demostración

`E-01 → E-02 → E-03 → (E-04 | E-05) → E-06 → E-08 → E-09`

## Preguntas adversariales por resolver antes de un MVP real

1. ¿En qué estado se debe bloquear la aprobación si hay documentos faltantes?
2. ¿Las tres tareas tienen autorizaciones institucionales diferentes? (En este kit NO).
3. ¿Qué variables del BPMN real y cuáles `elementId` coinciden con los formularios?
4. ¿Qué se hace si Camunda completó una tarea pero falló la escritura de auditoría local?
5. ¿Cuál es la fuente normativa aprobada del valor de referencia (no la fórmula de ejemplo)?
6. ¿Cómo se correlaciona cada expediente, cada radicado SIPA y la clave Camunda, sin duplicados?
