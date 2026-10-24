---
name: preparar-preset
description: "Guiar importación manual CSV y creación de widgets en Preset Starter por pasos verificados"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Fuentes a consultar
`docs/preset-starter-paso-a-paso.md`, `docs/continuidad-fase1-fase2-y-preset-zip.md`, `tableros/widgets.json`, `datos/preset/preset_resumen_mensual.csv`, `datos/preset/preset_roi_mensual.csv`.

## Reglas estrictas
- El plan Starter permite carga CSV desde UI si usuario y conexión tienen permisos. **SÍ** puede importarse un ZIP de dashboard exportado por Preset/Superset usando `Dashboards > Import` de la interfaz, si existen datos/conexiones válidos; **NO PROMETER** importación por Preset API Enterprise en Starter.
- No solicitar tokens, contraseñas ni datos personales al chat.
- Guiar de uno en uno y **esperar confirmación** tras cada pantalla. Usar sólo datos sintéticos para la demo.
- Al importar tablas, comprobar el tipo del campo, `.` decimal, encabezados, UTF-8 y que no se interpretó `mes` incorrectamente.

## Pasos conversacionales
1. Verifica: cuenta Preset, acceso workspace, rol Creator y posibilidad de Upload CSV.
2. Pregunta si el docente suministró un `dashboard_preset_importable.zip` (NO el ZIP completo del taller). Si existe, ofrece la vía `Dashboards > Import` y comprueba sus conexiones/datasets. Si no existe, guía carga `preset_resumen_mensual.csv` y nómbralo `mba_resumen_mensual`.
3. Guía widget 1 (horas por escenario). Espera confirmación.
4. Guía widget 2 (errores por escenario). Crea `MBA - Eficiencia del proceso`.
5. Guía carga `preset_roi_mensual.csv`, crea widget de ahorro de horas y/o beneficio operativo.
6. Pide imagen/captura y anota discrepancias, unidades y significados. Guarda `11-preset/instrucciones.md` y `11-preset/evidencia.md`.
7. En caso de bloqueo usa `tableros/dashboard_local.html` como alternativa de visualización, sin pretender que sea Preset cloud.
