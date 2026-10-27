# Ejemplo 2: Bandeja de tareas humanas
**Objetivo:** listar tareas pendientes en frontend.
EARS: "Mientras existan tareas pendientes autorizadas para el actor, el sistema deberá presentarlas con el expediente y su actividad BPMN, sin mostrar tareas ajenas."
Frontend `/tareas`, filtro actividad / expediente, botón `Atender`.
API `GET /api/tareas?estado=CREATED`; backend consulta Camunda `POST /v2/user-tasks/search`, con paginación y autorización adecuada; cruzar correlaciones del DB.
DB: no guardar una copia mutable como verdad definitiva; registrar `taskKey`, correlación, fecha consulta.
Prueba: 2 tareas pendientes -> 2 tarjetas; completar una -> deja de figurar después de sincronizar; sin autorización -> nada.
