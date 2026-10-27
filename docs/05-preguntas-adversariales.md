# Entrevista adversarial interactiva

Estas preguntas se hacen por tandas, como máximo tres en cada interacción. Para el docente, las respuestas pueden ser hipotéticas si se marcan como tales.

**Negocio:** ¿Qué persona obtiene valor si este proceso se completa? ¿Qué impacto tiene un error? ¿Cuál de todas las actividades TO-BE puede medirse durante un MVP de una semana?

**SOP/EARS:** ¿Quién decide que los documentos son válidos? ¿Qué pasa cuando el radicado o el CHIP es inconsistente? ¿Qué constituye el término "aprobado"? ¿Qué evidencia comprobaría el requisito?

**BPMN:** ¿Qué variable FEEL separa una ruta de otra? ¿Qué tarea requiere decisión humana y cuál es candidata a servicio automático? ¿El `processDefinitionId` coincide exactamente con el publicado? ¿Se espera un callback/webhook no implementado?

**Datos y ER:** ¿Se puede repetir radicado? ¿Hay varios recibos por expediente? ¿Qué datos deben auditarse? ¿Cuáles son sensibles? ¿Quién puede leerlos en Preset?

**Frontend:** ¿Qué verá el estudiante al iniciar una instancia, esperar una tarea o recibir error? ¿Es accesible el ID de instancia? ¿Cómo se evita completar tareas ajenas o duplicadas?

**ROI:** ¿Reducción de tiempo de ciclo es igual a horas humanas ahorradas? ¿Qué volumen y costos respaldan el ahorro? ¿Cómo se contabilizan los casos excepcionales?

**Integración:** ¿Camunda 8 v2 o Camunda 7? ¿Cuenta el clúster con licencia/permisos? ¿Qué hará el grupo si Camunda, Supabase o Preset están inaccesibles?

**Evaluación:** cada equipo debe presentar 1 EARS aceptado, 1 instancia con clave, 2 tareas completadas, 1 CSV, 1 KPI interpretado y 1 limitación reconocida.
