# Ejemplo 4: corrección de documentos
BPMN: gateway condicional -> user task Subsanar información.
Frontend `/solicitudes/{id}/subsanar`; botones Adjuntar y Enviar subsanación.
API `POST /api/solicitudes/{id}/documentos`, `POST /api/tareas/{taskKey}/completar`.
DB `documentos` (metadatos y referencias a archivos), `revisiones` (resultado, motivo, timestamp).
EARS: "Cuando la prevalidación detecte ausencia de CHIP, el proceso deberá requerir subsanación antes de la revisión de liquidación."
Prueba sin CHIP -> aparece tarea; con CHIP -> no aparece; no almacenar datos personales en CSV Preset.
