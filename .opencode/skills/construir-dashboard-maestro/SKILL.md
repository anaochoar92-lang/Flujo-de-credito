---
name: construir-dashboard-maestro
description: "Preparar y generar localmente un ZIP candidato con 2 dashboards, 8 gráficos y referencias a datasets exportados del workspace Preset; no usa API empresarial."
compatibility: opencode
metadata:
  audience: mba
  language: es
---

## Objetivo
Asiste al participante paso a paso (máximo 3 instrucciones o 4 preguntas por interacción) para preparar un dashboard maestro de AS-IS/TO-BE y ROI. No sustituir datos reales por cifras inventadas.

## Consultar primero
- `docs/dashboard-maestro-preset-v22.md`
- `config/preset_dashboard_maestro.json`
- `datos/preset/preset_resumen_mensual.csv`, `datos/preset/preset_roi_mensual.csv`
- `tableros/widgets.json`

## Secuencia
1. Preguntar al alumno si ya tiene los dos CSV cargados como `mba_resumen_mensual` y `mba_roi_mensual`; si no, explicar Upload CSV sin pedir credenciales.
2. Preguntar si ya exportó los datasets desde su propio workspace Preset; si no, indicar los clics para la exportación. No asumir que un ZIP de dashboard contiene datos.
3. Ayudar a ejecutar `py -m pip install -r requirements-preset.txt` si es necesario.
4. Pedir el nombre del ZIP real de datasets e invocar:
`py scripts/generar_bundle_preset.py --export-datasets "<RUTA_ZIP>" --salida "trabajos/mi-proceso/11-preset/dashboard_mba_CANDIDATO.zip"`.
5. Leer el `.reporte.json`. Si falla, no fabricar UUID ni credenciales; solicitar al estudiante resolver la exportación y repetir.
6. Instruir Dashboards > Import (UI). Solicitar verificar cada gráfico o enviar error de importación sin datos sensibles.
7. Si la importación no funciona en 5 minutos, cambiar a la ruta manual de `docs/dashboard-maestro-preset-v22.md`.

## Restricciones
- El ZIP es **CANDIDATO** hasta pasar importación y consulta de datos en Preset. Nunca afirmar éxito cloud por pruebas locales.
- No generar una conexión ficticia ni recomendar publicar una base SQLite local a Internet.
- No incluir ni pedir passwords, JWT, cookies o tokens.
- No sobreescribir versiones previas. Cualquier archivo de alumno debe guardarse bajo `trabajos/<equipo>/11-preset/`.
- Una métrica ponderada por volumen se usa en lugar de promediar promedios de tasas mensuales sin pesos.
