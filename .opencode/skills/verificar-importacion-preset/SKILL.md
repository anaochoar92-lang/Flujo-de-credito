---
name: verificar-importacion-preset
description: "Interrogar y registrar por pasos los resultados reales de importación y ejecución de dashboards en Preset Starter."
compatibility: opencode
metadata:
  audience: mba
  language: es
---

## Método adversarial
Nunca confundas: (1) archivo ZIP estructuralmente válido; (2) objeto dashboard visible; (3) chart que ejecuta la consulta; (4) KPI bien definido; (5) ROI respaldado por datos. Exige las cinco verificaciones.

## Preguntas, de tres en tres
1. ¿La interfaz mostró importación completada? Copia el mensaje exacto sin datos privados.
2. ¿Aparecen dos dashboards y ocho charts? Si no, ¿cuáles faltan?
3. ¿Los charts devuelven números y no error de dataset/conexión?
4. ¿El total de casos en la muestra suma 330 registros, de los cuales 165 corresponden a cada escenario, sin confundirlos con 330 casos distintos?
5. ¿Los KPI de tiempo se basan en sumas ponderadas y las tasas se muestran como porcentaje 0–100%?
6. ¿El beneficio operativo es un flujo antes de la inversión inicial y el ROI año 1 sí la considera?
7. ¿El estudiante construyó o modificó manualmente al menos un KPI?

## Errores típicos
- `dataset not found`: dataset UUID no presente en destino; exportar datasets desde el workspace destino.
- `database connection failed`: la base exportada requiere conectividad/credenciales; no intentar trucos de acceso ni pedir secretos.
- `column not found`: CSV importado con campo renombrado o tipo incorrecto.
- `chart is blank`: configurar definición de tiempo, dimensiones, métricas o revisar versión del tipo de visualización.
- ZIP rechazado por formato YAML: guardar el mensaje literal, no prometer que la plantilla es compatible universalmente.

## Salidas
Guardar `trabajos/<equipo>/11-preset/reporte-validacion.md` con fecha, workspace anonimizado, estado de cada widget, capturas referidas, y lista priorizada de correcciones. Si no funciona, activar `tableros/dashboard_local.html` y registrar que es contingencia local.
