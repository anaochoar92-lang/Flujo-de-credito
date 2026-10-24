# Módulo 2 — Automatización, KPI, ROI y tableros

Continúa **en un nuevo directorio del kit actualizado**, migrando sólo los contenidos de `trabajos/<equipo>/01-fuentes` a `06-revision` para no pisar el trabajo AS-IS. Instrucciones completas: `docs/continuidad-fase1-fase2-y-preset-zip.md`. Todos los comandos funcionan como instrucciones para OpenCode GUI; si el comando no aparece, pide al agente el skill por su nombre.

## Inicio guiado
1. Abre en OpenCode la carpeta raíz `taller-opencode-bpmn` (no la subcarpeta del equipo).
2. Completa fase 1 (SOP, EARS, BPMN AS-IS). Para la demo se incluye BPMN y SOP de reexpedición.
3. Ejecuta `/08-cadena-valor`, `/09-diagnosticar`, `/10-priorizar`, `/11-tobe` y espera aprobación del equipo antes de pasar a métricas.
4. Ejecuta `/12-kpis`, `/13-datos`, `/14-roi`; OpenCode primero pregunta si los datos son **reales, estimados o sintéticos**, no inventa una muestra real.
5. Para preparar la simulación desde la raíz con Python 3: `py scripts/taller_kpi.py todo` (macOS/Linux `python3`). **Los CSV y Excel están ya incluidos** para evitar bloquear a alumnos sin Python.
6. Abre `datos/Modelo_KPI_ROI_Reexpedicion.xlsx`: hoja **Supuestos** (celdas azules) → **Comparacion** → **ROI** → **FlujoMensual**. Muestra ecuaciones, no solo indicadores.
7. Lee `docs/preset-starter-paso-a-paso.md`, sube `datos/preset/preset_resumen_mensual.csv` y `datos/preset/preset_roi_mensual.csv` a Preset.io Starter, crea 2 dashboards siguiendo `tableros/widgets.json`.
8. Si faltan cuentas o falla la subida, abre `tableros/dashboard_local.html`, que permite cargar `preset_resumen_mensual.csv` y `preset_roi_mensual.csv` para seguir con la discusión; NO publica el tablero en Preset.
9. Ejecuta `/16-verificar` y entrega capturas, informe y reflexiones.

## Material nuevo
- **10 skills** adicionales (`08` a `17`; comandos `08` a `17`, ver carpeta `.opencode/commands/`).
- **Python estándar**: `scripts/taller_kpi.py`, con modos `demo`, `validar`, `preparar`, `todo`; sin dependencias para estudiantes.
- **Excel** con fórmulas trazables y escenarios editables: `datos/Modelo_KPI_ROI_Reexpedicion.xlsx`.
- **CSV listos** en `datos/preset/` y datos fuente simulados en `datos/demo/`.
- Guías docente, Preset Starter y vinculación a diapositivas en `docs/`.
- Modelo TO-BE conceptual en `ejemplos/tobe/` para observar cambios de tareas, sujeto a revisión.

## Ejecución para datos propios, sin cambiar el Excel distribuido
1. Crear `trabajos/mi-proceso/09-datos/casos.csv` con cabeceras equivalentes a `datos/demo/casos.csv`. Usar siempre IDs anónimos.
2. Editar `config/escenario_reexpedicion.json` con supuestos consensuados.
3. `py scripts/taller_kpi.py validar --input trabajos/mi-proceso/09-datos/casos.csv`
4. `py scripts/taller_kpi.py preparar --input trabajos/mi-proceso/09-datos/casos.csv --out trabajos/mi-proceso/11-preset`
5. Abrir los CSV preparados en Preset. Para adaptar el Excel a otros datos/volúmenes será necesario actualizar el libro (o generar otra versión con Excel/Google Sheets); no afirmar que Excel recalcula automáticamente desde CSV externo.

## Definiciones importantes
- El ROI del ejemplo incluye ahorro laboral **teórico** y costos evitados teóricos; NO equivale a un ahorro financiero confirmado.
- El dataset simula **165 pares** de casos, cada uno en AS-IS y TO-BE (330 filas), 3 meses, no registros SDP.
- Preset Starter recibe CSV por UI **y permite importar ZIP de dashboards mediante la UI**, siempre que se resuelvan fuentes de datos y referencias. La API de migración requiere Enterprise. Ver `docs/continuidad-fase1-fase2-y-preset-zip.md`.
- Se eligieron KPI por hora, calidad, volumen y costo para alinear la práctica con los conceptos en las diapositivas 69–82.

## Fuentes técnicas actualizadas
https://preset.io/pricing/
https://docs.preset.io/docs/using-csv-files
https://docs.preset.io/docs/migrating-dashboards
https://opencode.ai/docs/skills
https://dev.opencode.ai/docs/commands
