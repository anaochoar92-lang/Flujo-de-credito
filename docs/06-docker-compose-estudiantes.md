# MVP local con Docker Compose — Guía para equipos (v2.0)

## Idea central

**Local (Docker Desktop)**: navegador → Nginx (frontend) → FastAPI (backend) → PostgreSQL (datos persistentes).
**Externo (opcional)**: backend → Camunda 8 SaaS (solo API REST v2 con OAuth); archivos CSV generados localmente → carga en Preset Starter.
Los servicios de Camunda y Preset **no** se instalan dentro de Docker Compose.

## Prerrequisitos (preparar ANTES de las sesiones)

1. Docker Desktop con Docker Compose v2 en ejecución; memoria libre razonable (idealmente >=4 GB para el laboratorio), conexión a internet para descargar imágenes.
2. Puerto 8088 libre en la PC; si está ocupado cambiar `MVP_PORT` en `.env`.
3. Descomprimir el ZIP sin mezclarlo con otro repo, mantener las carpetas originales de SOP/EARS/BPMN del equipo.
4. No almacenar documentos confidenciales ni contraseñas en este repositorio de clase.
5. El kit no tiene inicio de sesión; se publica solamente en `127.0.0.1`. No abrir puertos al LAN ni internet.

## Paso 1. Un solo comando para iniciar

**Windows PowerShell**, dentro de la carpeta raíz:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\levantar.ps1
```
**macOS / Linux**:
```sh
sh scripts/levantar.sh
```
El script genera `.env` con contraseña aleatoria (si no existe), crea `backups/` y `exports/`, construye e inicia los servicios y espera comprobaciones de salud.
Abrir: **http://127.0.0.1:8088** y **http://127.0.0.1:8088/docs**.

## Paso 2. Tres expedientes de prueba

```sh
docker compose exec -T api python -m scripts.sembrar_contenedores
```
Solo funciona cuando `ENGINE_MODE=mock`. Genera tres casos ficticios, prueba validación, tarea humana y excepción. Es idempotente respecto de los radicados de demostración existentes dentro de los primeros 100 registros.

## Paso 3. Extraer y validar datos destinados a Preset

```sh
docker compose run --rm etl
```
O PowerShell: `powershell -ExecutionPolicy Bypass -File .\scripts\exportar_preset.ps1`.

Abrir `exports/manifest.json` para confirmar fecha UTC, archivos, número de filas y SHA-256. Los cuatro CSV se generan con cabeceras aun si la BD está vacía:

| Archivo | Granularidad | Uso en Preset |
| --- | --- | --- |
| `preset_casos.csv` | Un caso | Volumen, tasa de validación, comparaciones AS-IS/TO-BE |
| `preset_eventos.csv` | Un evento registrado | Auditoría y eventos por paso |
| `preset_kpis_mensuales.csv` | Mes + escenario | KPI, gráficos temporales y barras |
| `preset_actividades.csv` | Mes + escenario + acción | Ranking de actividad |

Subir CSV con la interfaz de Preset y crear los datasets. Para columnas `fecha_*_utc`, seleccionar tipo temporal y verificar formato ISO. En `preset_kpis_mensuales.csv`, `mes` es una cadena YYYY-MM; convertir a fecha real si el control temporal del gráfico lo requiere (agregar el día `-01` en la transformación de Preset). **Preset Starter no puede conectarse directamente a PostgreSQL en `localhost` de la PC.**

## Paso 4. Persistencia y respaldo

La base PostgreSQL utiliza el volumen Docker nombrado `pgdata`: sobrevive a `docker compose down`, `up` y reinicios de la PC. **NO ejecutar `docker compose down -v`**: eliminaría el volumen y los datos.

Hacer copia verificable:
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\respaldar.ps1
```
o `sh scripts/respaldar.sh`. Los archivos `.dump` se escriben en `backups/`. Las copias no contienen credenciales pero sí pueden contener datos personales: protegerlas. Probar restauración SOLO en una base descartable, nunca sobre la base de los demás equipos.

## Paso 5. Operaciones frecuentes

```sh
docker compose ps                          # Contenedores y estado
docker compose logs --tail=100 api        # Diagnóstico API
docker compose logs --tail=100 db         # Diagnóstico base de datos
docker compose restart api                # Recarga sin reconstruir
docker compose up -d --build --wait       # Cambios en código Python
docker compose down                       # Apaga sin borrar volumen
docker compose run --rm etl               # Actualiza CSV
```
El HTML/JS está enlazado con Nginx por volumen de solo lectura: al editar `app/static/index.html`, refrescar el navegador. Backend: `docker compose up -d --build --wait`. Opcional `compose.dev.yaml` permite `docker compose -f compose.yaml -f compose.dev.yaml up --watch` con Compose moderno.

## Migración a Camunda Cloud (opcional, siempre después de DEMO local)

- Desplegar y verificar los BPMN de cada equipo **primero** en su Camunda 8 SaaS. Registrar `processDefinitionId` real, tareas humanas de tipo Camunda user task y variables de gateway.
- Editar `.env` local sin compartir secretos: `ENGINE_MODE=camunda`, `CAMUNDA_BASE_URL` (raíz **sin** `/v2`), `CAMUNDA_AUTH_MODE=oauth`, token endpoint, client id, client secret, audiencia y `CAMUNDA_PROCESS_ASIS/TOBE`.
- `docker compose up -d --force-recreate api`, comprobar en `http://127.0.0.1:8088/api/health/camunda` y **crear un caso nuevo**. Los casos en MOCK permanecen en BD pero sus claves `DEMO-*` no corresponden a instancias cloud.
- El cluster SaaS debe ser accesible desde dentro del contenedor (salida HTTPS, VPN/proxy de Docker si procede). El backend nunca transmite la credencial al frontend.
- Si el BPMN requiere service task workers/Connectors no desplegados, el proceso puede quedar detenido: limitar la demostración a tareas humanas y gateways o configurar workers por separado.
- Un `POST` remoto exitoso seguido de un fallo de DB puede causar desincronización; no hay outbox/idempotencia robusta en este MVP didáctico.

## Solución de problemas

- Puerto usado: `MVP_PORT=8098` y reiniciar `docker compose up -d --wait`.
- Sin Docker: revisar Docker Desktop, WSL2 y permisos.
- Backend reiniciando: `docker compose logs api`; confirmar que `.env` tenga contraseña y que `db` esté `healthy`.
- Camunda `401/403`: revisar OAuth, audiencia, permisos de los procesos/tareas.
- Camunda `404`: revisar URL base y BPMN `processDefinitionId`, versión REST.
- No aparecen tareas: esperar indexación y contrastar Tasklist; confirmar que BPMN tenga user tasks reales, no tareas legacy.
- CSV vacíos: ejecutar primero semilla o crear casos desde frontend; correr ETL de nuevo.
- Cero actividad en KPI: medir solo hechos registrados; no inventar reducción de errores ni ROI.

**Sincronización de cierres Camunda:** tras completar la última tarea, usar el botón **Sincronizar estado** del frontend (`POST /api/cases/{id}/sync`). Actualiza el estado PostgreSQL desde `GET /v2/process-instances/{key}`. La API es eventualmente consistente y no hay sincronización automática ni outbox: sin esta acción, los KPI podrían seguir mostrando el caso como `EN_PROCESO`.
