# Ejemplo 3: formulario humano de validación de áreas
Pantalla `/tareas/{taskKey}` renderizada según `bpmnElementId` y esquema de campos aprobado.
Botones `Guardar borrador`, `Aprobar`, `Solicitar corrección` (solo mostrar los caminos admitidos por BPMN).
EARS: "Cuando el profesional confirme áreas válidas, el sistema deberá validar unidades y valores, guardar evidencia y completar la user task con las variables esperadas."
API `POST /api/tareas/{taskKey}/completar`; solo backend llama a Camunda REST v2. Antes de completar, validar permisos y el estado actual. 
DB `validaciones_area` con expediente FK, m² y usuario lógico; evento de auditoría.
Prueba: área negativa 422, duplicación idempotente, variable Camunda de salida correcta y avance al siguiente nodo.
