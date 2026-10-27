# Guía docente: despliegue Docker local, Camunda SaaS y Preset CSV (2 × 60 min)

## Preparación docente 1–2 días antes (FUERA del tiempo de aula)

- Verificar Docker Desktop y `docker compose version` en cada equipo, descarga de imágenes y espacio disponible.
- Ejecutar `scripts/levantar.ps1` y confirmar frontend, API, PostgreSQL `healthy`.
- Preparar 3 documentos mínimos: contexto de negocio, SOP actual y requerimientos EARS.
- Confirmar en Camunda 8 SaaS acceso REST v2, OAuth y procesos ya desplegados; un cluster gratuito puede tener condiciones de disponibilidad y cuota específicas del plan.
- Mantener un **camino de contingencia MOCK** para los alumnos sin acceso Camunda.
- Descargar el CSV de prueba y verificar que la interfaz Preset permite cargarlo.

## Sesión A — 60 min (STACK LOCAL)

| Minutos | Actividad | Evidencia |
| --- | --- | --- |
| 0–10 | /28-contenedores: reconocer 3 servicios y riesgos | Diagrama de contenedores |
| 10–22 | Arranque por script, healthchecks y Frontend | Captura de pantalla + `docker compose ps` |
| 22–35 | Sembrar 3 casos, completar tareas humanas | Estados finalizados, eventos |
| 35–47 | Modificar un campo o regla EARS y probar | Prueba local + resultado |
| 47–60 | Explicar persistencia, respaldar y reiniciar | `.dump` y caso conservado |

## Sesión B — 60 min (CLOUD Y MÉTRICAS)

| Minutos | Actividad | Evidencia |
| --- | --- | --- |
| 0–15 | Revisar Camunda 8 SaaS y credenciales locales (sin mostrarlas en pantalla) | `health/camunda`; proceso desplegado |
| 15–30 | Grupo preparado: instancia Camunda real. Resto: mock + formulario | `instance_key` y tarea humana |
| 30–42 | /29-etl-preset, extraer cuatro CSV y leer manifiesto | conteos, checksum, fórmula KPI |
| 42–52 | Subir CSV a Preset, crear KPI manual (o usar CSV local si no hay cuenta) | widget con numerador y denominador |
| 52–60 | /30-verificar-stack + entrevista adversarial | matriz de pruebas, hallazgos, backlog |

**Regla pedagógica**: no pedir a estudiantes novatos implementar todo el AS-IS/TO-BE. Un flujo demostrable de inicio, tarea humana y cierre + datos para indicador es un MVP adecuado.

## Cuatro preguntas que cada equipo debe responder

1. ¿Qué elemento BPMN y qué EARS justifican la pantalla que implementamos?
2. ¿Qué evento se guarda en PostgreSQL cuando se completa una tarea?
3. ¿Qué evidencia permite afirmar que el dato exportado a Preset se calcula bien?
4. ¿Qué sucede si no hay internet, Camunda falla o una tarea no está asignada?

## Condiciones de evaluación mínima

- Archivo `.env` privado y servicio web solo en localhost.
- Frontend creando caso, mostrando tarea y actualizando resultado.
- PostgreSQL persistente y un respaldo realizado.
- ETL ejecutada con `manifest.json` y cuatro CSV verificables.
- Al menos un requisito EARS trazado a endpoint, pantalla y prueba.
- Camunda real opcional en la práctica base; si se declara conectado, exigir evidencia en cluster cloud.

## Aspectos que NO están resueltos como producción

Autenticación/RBAC, migraciones Alembic, worker de tareas de servicio genérico, idempotencia transaccional Camunda–DB, reconciliación de estados remotos, observabilidad avanzada, PII y copias de seguridad cifradas. Convertir esos vacíos en backlog de proyecto y nunca exponer este stack a una red pública.
