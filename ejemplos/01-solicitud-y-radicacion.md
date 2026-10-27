# Ejemplo 1: Solicitud / Radicación
**Objetivo:** registrar nueva solicitud en frontend y crear instancia TO-BE.
1. Contexto: cliente diligencia datos básicos y adjunta soportes.
2. EARS: "Cuando una solicitud esté completa y el usuario seleccione Radicar, el sistema deberá guardar el expediente e iniciar una instancia del proceso TO-BE, registrando su `processInstanceKey`."
3. Frontend: `/solicitudes/nueva`, botón `Radicar` (deshabilitar mientras espera respuesta, prevenir doble envío).
4. API: `POST /api/solicitudes`, `POST /api/solicitudes/{id}/iniciar` con Idempotency-Key.
5. DB: `solicitudes` + `instancias_bpmn` (unique local case + process + intento).
6. Camunda: inicia por BPMN process ID leído del archivo (no por nombre visual), envía variables definidas.
7. Pruebas: incompleta 422; válida 201; doble click no crea dos instancias; falla cloud registrada para reintento.
