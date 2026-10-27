# API contractual

Swagger interactivo: `http://127.0.0.1:8000/docs`.

| Método | Ruta | Qué permite |
|---|---|---|
| GET | `/api/health` | saber si el modo es `mock` o `camunda` |
| POST | `/api/cases` | iniciar un proceso AS-IS/TO-BE |
| GET | `/api/cases` | listar expedientes demo |
| GET | `/api/cases/{id}` | consultar caso |
| GET | `/api/cases/{id}/tasks` | listar user tasks de esa instancia |
| POST | `/api/cases/{id}/tasks/{key}/complete` | completar tarea |
| POST | `/api/cases/{id}/rerun?escenario=TOBE` | lanzar TO-BE desde una segunda zona del front |
| GET | `/api/events` | consultar bitácora |
| GET | `/api/kpis` | indicadores por escenario |
| GET | `/api/export/casos.csv` | CSV casos |
| GET | `/api/export/eventos.csv` | CSV eventos |
| GET | `/api/export/kpis.csv` | CSV agregados |

## Ejemplo JSON para empezar

```json
{"radicado":"DEMO-SDP-001", "escenario":"TOBE", "area_terreno_m2":450, "area_construida_m2":700, "uso":"residencial", "chip":"AAA0000DEMO"}
```

## Contrato Camunda real (versión 8.8+ con API v2)

- Inicio: `POST /v2/process-instances`, `processDefinitionId`, `variables`.
- Tareas: `POST /v2/user-tasks/search`, filtro `processInstanceKey`.
- Completar: `POST /v2/user-tasks/{userTaskKey}/completion`, variables JSON.
- Se requieren **Camunda user tasks**, no las implementaciones antiguas basadas en trabajos/Tasklist. El adaptador comprueba pertenencia de una tarea a la instancia antes de completarla.
- Si el clúster requiere OAuth, configurar credenciales del backend en `.env`. Nunca conectar directamente desde JavaScript con credenciales.
- La lectura desde los índices de Camunda puede tardar tras iniciar/completar; pulsar actualizar en vez de suponer fallo instantáneo.

**Límites conocidos del kit:** el estado `FINALIZADO` se actualiza en modo mock; con Camunda real debe implementarse una sincronización posterior de estados/errores. No afirmar consistencia distribuida sin mecanismo adicional.
