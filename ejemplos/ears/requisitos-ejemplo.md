# EARS de ejemplo — Reexpedición de recibos de la SDP

> **Procedencia:** interpretación didáctica del borrador de SOP anterior, etapas F y G. No constituye especificación oficial de la SDP ni incluye reglas legales no validadas. Se presentan requisitos orientados a un **sistema futuro**; el SOP original no prueba que todos estén implementados.

| ID | Patrón | Requisito en español | Fuente | Estado |
|---|---|---|---|---|
| REQ-001 | Evento | Cuando se registre la confirmación de pago de un recibo, el sistema de seguimiento deberá finalizar el seguimiento de ese recibo con estado «pagado». | F2 | Derivado, validar |
| REQ-002 | Evento | Cuando un recibo llegue a su vencimiento sin pago confirmado, el sistema deberá enviar al interesado una comunicación que permita solicitar su reexpedición. | F4 | Derivado, validar |
| REQ-003 | Evento | Cuando se reciba una solicitud de reexpedición, el sistema deberá verificar la vigencia del vínculo utilizado y su asociación con un recibo vencido. | G2 | Derivado, validar |
| REQ-004 | Estado + evento | Mientras la solicitud esté validada, cuando se confirme su elegibilidad para reexpedición, el sistema deberá solicitar la reexpedición del recibo a la SDP. | G3 | Derivado, validar |
| REQ-005 | Evento | Cuando se reciba la confirmación de reexpedición, el sistema deberá comunicar el nuevo recibo al interesado y reiniciar su seguimiento. | G4–G5 | Derivado, validar |
| REQ-006 | Error | Si el vínculo no está vigente, entonces el sistema deberá bloquear la reexpedición y dejar un resultado verificable. | G2 | **Propuesta TO-BE**, respuesta exacta no definida |
| REQ-007 | Evento | Cuando se registre el desistimiento, el sistema deberá concluir el seguimiento de esa solicitud con estado «desistimiento». | G, ruta alternativa | Derivado, validar |

## Criterios de aceptación ilustrativos

### REQ-002
**Dado** un recibo cuyo vencimiento fue alcanzado y sin confirmación de pago,
**cuando** el componente responsable procese el evento de vencimiento,
**entonces** deberá quedar registrada una comunicación con un vínculo de solicitud de reexpedición.

### REQ-003
**Dada** una solicitud vinculada con un recibo,
**cuando** el interesado envíe el vínculo de reexpedición,
**entonces** el sistema deberá comprobar vigencia y asociación con el recibo vencido, y dejar constancia del resultado.

## Preguntas adversariales críticas

- **PREG-001:** Si el pago se confirma justo cuando se detecta el vencimiento, ¿qué evento tiene precedencia? **Pendiente**.
- **PREG-002:** ¿La reexpedición exige un plazo mínimo o máximo y un límite de intentos? **Pendiente**.
- **PREG-003:** Si BOG DATA no responde, ¿hay reintento, escalamiento o finalización por error? **Pendiente**.
- **PREG-004:** Si el vínculo no es válido, ¿qué comunicación debe recibir el solicitante? **Pendiente**.

El modelo BPMN del ejemplo contiene una salida conceptual de «solicitud no válida» marcada como **propuesta**, que no debe confundirse con el procedimiento institucional confirmado.
