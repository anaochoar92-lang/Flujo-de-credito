# Manifiesto — Kit MBA MVP Docker + Camunda Cloud + Preset ETL v2.0

## Compatibilidad

- Conserva los 8 skills anteriores `.claude/skills/mvp-*` y comandos `/20`–`/27`.
- Añade tres skills: `mvp-docker-local`, `mvp-etl-preset`, `mvp-verificar-stack`; tres comandos `/28-contenedores`, `/29-etl-preset`, `/30-verificar-stack`.
- Conserva el SOP, EARS, BPMN y código frontend/backend iniciales. `app/db.py` incorpora configuración Postgres con credenciales seguras para URL y `app/main.py` separa el healthcheck local de Camunda Cloud.
- Añade 3 servicios por defecto: Nginx, FastAPI y Postgres; servicio ETL bajo demanda y Adminer opcional.

## Artefactos añadidos
`Dockerfile`, `compose.yaml`, `compose.dev.yaml`, `.dockerignore`, `.env.docker.example`, `infra/nginx.conf`, scripts de levantar/exportar/respaldar/sembrar/diagnosticar, `scripts/etl_preset.py`, guía de equipos/docentes, diccionario CSV, EARS de despliegue, skills y pruebas.

## Comprobación de calidad
`python -m pytest -q` y `python -m scripts.demo_automatica` verifican endpoints y ETL con SQLite.
**Limitación de comprobación:** en este entorno no hay Docker Engine: no se ha construido/levantado la imagen ni probado Postgres y Camunda SaaS reales. Cada equipo debe correr los smoke tests en Docker Desktop.

## Ruta a Preset
`docker compose run --rm etl` genera `exports/preset_casos.csv`, `preset_eventos.csv`, `preset_kpis_mensuales.csv`, `preset_actividades.csv` y `manifest.json`. Son cargables manualmente como CSV; NO son un ZIP de dashboards Preset. Para importar una plantilla de dashboard aparte se requiere un ZIP exportado compatible desde Preset.

## Seguridad
`.env` es privado, el frontend escucha en `127.0.0.1`, Postgres no tiene puerto publicado, el backend no publica credenciales. No usar para datos sensibles/productivos sin controles adicionales.
