# Ejemplo didáctico TO-BE, pendiente de aprobación

**Fuente:** SOP de reexpedición; el BPMN original es AS-IS conceptual. Este TO-BE se propuso para enseñar el diseño y NO corresponde a un despliegue ni una decisión de la SDP.

| Origen AS-IS | Cambio TO-BE propuesto | Tipo | Verificación pendiente |
|---|---|---|---|
| `S_ValidarEnlace`: tarea genérica de verificación | `serviceTask` con reglas automáticas | automatizar | Campos, reglas legales, logs, privacidad |
| `S_NoValida`: registrar rechazo | revisión humana del caso excepcional antes de rechazar | humano en el bucle | rol, autorizaciones, tiempo máximo |
| Nueva decisión `S_DecisionHumana` | resolver excepción por aprobación/rechazo | gateway exclusivo | condiciones y evidencia jurídica |
| Nuevo envío `S_RechazoFormal` | notificar rechazo motivado | comunicación | contenido, canal y normas |

## Requisitos EARS propuestos, no aprobados
- **REQ-TOBE-001 (evento):** Cuando se reciba solicitud de reexpedición, el sistema deberá verificar automáticamente los campos obligatorios según reglas **pendientes de especificar**.
- **REQ-TOBE-002 (no deseado):** Si no se cumple una validación, el sistema deberá remitir el caso a revisión humana y conservar evidencia verificable.
- **REQ-TOBE-003 (opcional):** Cuando el profesional autorice la continuación, el proceso deberá solicitar la reexpedición al servicio correspondiente.
- **REQ-TOBE-004 (no deseado):** Si se rechaza el caso, el sistema deberá generar una comunicación motivada **según criterios que falta validar**.

## Advertencias
Ninguna regla legal, SLA, integración o permiso está confirmada. Exigir revisión en Camunda Modeler: semántica de tareas, coordinación por mensajes, gateway y ruta de excepción. No es ejecutable Camunda.
