# Taller iterativo 2 × 60 minutos

## Sesión 1 — MVP sin Camunda cloud (mock)
- 0–10: importar SOP/EARS/BPMN, contexto y alcance.
- 10–20: `/31-descubrir` y priorizar una historia vertical.
- 20–30: `/32-trazar-bpmn` y validar identidad de tarea/variables.
- 30–48: `/33-slice` implementar registro de solicitudes (pantalla + POST + DB + inicio mock).
- 48–60: `/34-verificar-slice` tests, docker compose, evidencia de persistencia.

## Sesión 2 — tareas y nube
- 0–10: seleccionar segunda actividad de user task.
- 10–30: implementar bandeja y formulario, vista según `bpmnElementId`.
- 30–43: conectividad cloud Camunda, cliente OAuth de backend, correlación y prueba sin secretos en navegador.
- 43–52: `docker compose run --rm etl`, inspección CSV, Preset o visor local.
- 52–60: auditoría, evidencia, siguiente iteración autónoma.

**Camunda cloud es opcional para aprobar demo local, pero obligatorio para comprobar integración real.** La disponibilidad del clúster y el despliegue BPMN deben estar preparados antes de clase.
