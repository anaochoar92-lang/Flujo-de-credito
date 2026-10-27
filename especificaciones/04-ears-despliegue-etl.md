# Requerimientos EARS — Contenedores locales + ETL (v2)

Supuestos del laboratorio: Docker Desktop, un usuario sobre localhost, sin información sensible de terceros. Los requisitos son para el MVP, no para producción.

| ID | Patrón EARS | Requerimiento verificable | Prueba |
| --- | --- | --- | --- |
| DEP-01 | Ubiquitous | El sistema deberá servir el frontend desde el puerto local configurado sin publicar el puerto de PostgreSQL. | Inspeccionar `docker compose ps`/`ports`. |
| DEP-02 | Event-driven | Cuando el estudiante ejecute el script de arranque por primera vez, el sistema deberá generar un `.env` privado con contraseña de DB aleatoria. | Verificar que existe `.env` fuera del control de versiones. |
| DEP-03 | State-driven | Mientras PostgreSQL no esté preparado, el servicio de API no deberá declararse sano. | Parar DB y consultar estados de salud. |
| DEP-04 | Event-driven | Cuando se reinicie la API, los casos previamente confirmados deberán conservarse en el volumen PostgreSQL. | Crear caso, reiniciar api, consultar caso. |
| DEP-05 | Optional feature | Si `ENGINE_MODE=mock`, el estudiante podrá terminar un caso sin conectividad hacia Camunda SaaS. | Prueba completa mock. |
| DEP-06 | Optional feature | Si `ENGINE_MODE=camunda`, el backend deberá intentar iniciar el `processDefinitionId` configurado por REST v2 con OAuth y nunca exponer el secreto al frontend. | Probar en cluster real autorizado. |
| DEP-07 | Event-driven | Cuando se invoque `docker compose run --rm etl`, el contenedor deberá producir cuatro CSV y un manifiesto con cantidad de filas y SHA-256. | Ejecutar ETL e inspeccionar archivos. |
| DEP-08 | Unwanted behavior | Si un caso incluye CHIP, radicado original o actor, el ETL no deberá incluir estos textos en los CSV para Preset. | Test de datos sensibles. |
| DEP-09 | Event-driven | Cuando se ejecuta el respaldo, el sistema deberá escribir un `.dump` PostgreSQL en carpeta persistente del host. | Ejecutar script y comprobar tamaño del dump. |
| DEP-10 | Unwanted behavior | Mientras no exista evidencia de despliegue real, ningún reporte deberá declarar que Camunda y Preset están conectados. | Revisar reporte de pruebas. |

## Trazabilidad mínima

`DEP-01..03` → `compose.yaml`, Nginx, `scripts/levantar.*`. `DEP-04..06` → `app/db.py`, `app/main.py`, `app/camunda.py`.
`DEP-07..08` → `scripts/etl_preset.py`, `tests/test_docker_etl.py`. `DEP-09` → `scripts/respaldar.*`.

### Pendientes de escalamiento

Autorizaciones y roles, protección de datos, API rate limiting, export incremental/CDC, migraciones de DB, reconciliación de instancias Camunda y métricas de errores reales. La solución actual es para demostración no productiva.
