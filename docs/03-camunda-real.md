# Integración al clúster Camunda existente

Este proyecto usa **Camunda 8 REST v2 (Orchestration Cluster API)**. Camunda 7 REST `/engine-rest` y tareas antiguas tipo job no funcionan con este adaptador.

## Secuencia segura

1. Ubicar la URL accesible **desde la PC donde corre FastAPI**, por ejemplo `http://localhost:8080` en un laboratorio; la URL debe ser la raíz anterior a `/v2`.
2. Verificar `/v2/topology` desde un entorno con conectividad y permisos. Si la API requiere OAuth, activar `CAMUNDA_AUTH_MODE=oauth` con URL de token, cliente, secreto y audiencia correctos. Mantener esto en `.env` local.
3. Abrir los modelos `bpmn/liquidacion_cargas_asis_mba.bpmn` y `bpmn/liquidacion_cargas_tobe_mba.bpmn` en Camunda Modeler. Son modelos de clase nuevos y simples; no modificar el BPMN institucional de referencia.
4. Desplegar los modelos en el clúster **una sola vez** como prerrequisito. Si no está permitido, utilizar los modelos ya desplegados de cada grupo y cambiar `CAMUNDA_PROCESS_ASIS` y `CAMUNDA_PROCESS_TOBE` a sus `processDefinitionId` reales.
5. Confirmar que los elementos userTask usan `zeebe:userTask`, que las variables `validacionPreviaOk` y demás nombres coinciden, y que el modelo publicado no espera workers adicionales.
6. Editar `.env` con `ENGINE_MODE=camunda`, detener e iniciar el servidor. No pegar secretos en OpenCode o Claude Code.
7. Probar `/api/health`, crear instancia desde formulario, comprobar `instance_key`, abrir Operate y localizarla.
8. Pedir `/api/cases/{id}/tasks` (puede requerir segundos para propagarse por el índice), completar una tarea, contrastar con Camunda Tasklist/Operate.

El backend nunca pasa la credencial al navegador. En Camunda real la finalización y las métricas de tiempo requieren sincronización adicional; la demo solo contabiliza desde la base local de eventos. Para producción implementar autenticación RBAC, conciliación por eventos, idempotencia, reintentos, trazas y gestión de incidentes.

## Si se integran BPMN propios

No se debe asumir que los `elementId` de un proceso arbitrario coinciden con el ejemplo ni que las variables definidas aquí habilitan sus gateways. Cada equipo debe registrar el mapa BPMN → formulario → variables EARS; si las tareas Camunda no están configuradas como Camunda user task, modificar el BPMN de manera controlada y redesplegarlo antes de reintentar.
