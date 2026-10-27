# Cómo vincular Camunda y la aplicación
| BPMN | Frontend | API backend | PostgreSQL | Contrato mínimo |
|---|---|---|---|---|
| Start event | botón Iniciar | POST /api/solicitudes/{id}/iniciar | instancia + expediente | processDefinitionId, business id, variables |
| User task Cotejo | /tareas/{key}/cotejo | GET tareas + POST completar | evidencia de cotejo | taskKey, elementId, variables |
| User task Validar áreas | /tareas/{key}/areas | GET tareas + POST completar | tabla áreas | área_m2, resultado_validacion |
| User task Aprobar | /tareas/{key}/aprobacion | GET tareas + POST completar | decisiones | aprobado, observaciones |
| Timer/intermediate | widget SLA / alerta | GET caso + eventos | auditoría, plazos | timers viven en Camunda |
| Service task | indicador de integración | worker dedicado o conector | log de ejecución | jobType / retries / incidentes |
| End event | estado expediente | GET instancia / reconciliar | conclusión local | instancia completada en Camunda |

**Importante:** las URLs son convenciones propuestas, NO endpoints que ya existan en el kit original. Los nombres de variables son ejemplos; deben salir de BPMN/EARS reales. Los gateways se resuelven en Camunda, no mediante botones que manipulen el estado arbitrariamente. La capa media expone una API funcional protegida, no un proxy público a Camunda.
