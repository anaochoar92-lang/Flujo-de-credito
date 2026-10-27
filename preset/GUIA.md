# Preset.io: datos de este MVP

## Ruta A, sin infraestructura pública (recomendada en 2 horas)
1. Abrir el MVP en `http://127.0.0.1:8000`.
2. Generar varias instancias AS-IS y TO-BE de ejemplo, completando algunas tareas.
3. Descargar `/api/export/casos.csv`, `/api/export/eventos.csv`, `/api/export/kpis.csv`.
4. En Preset Workspace, cargar CSV y crear tres widgets: número de casos, porcentaje de cierre por escenario y acciones por tipo.
5. Registrar una captura y la explicación de la fórmula usada.

## Ruta B, integración directa de PostgreSQL de Supabase
1. Usar el `DATABASE_URL` para la aplicación **solo en el servidor**; no compartir credenciales entre app y Preset.
2. Con la app ya iniciada, ejecutar `sql/vistas_preset.sql` en PostgreSQL como propietario del esquema.
3. Crear usuario de lectura que solamente pueda consultar `vw_preset_casos`, `vw_preset_resumen_mensual`, `vw_preset_eventos`.
4. Verificar acceso desde la red de Preset y TLS/SSL. El Postgres local o SQLite **no es accesible directamente** desde Preset Cloud.
5. Crear conexión PostgreSQL en Preset con usuario exclusivo de lectura, como explica la documentación oficial.
6. Construir datasets sobre esas vistas. Nunca subir claves de API o contraseñas al repositorio.

Preset Cloud **no es una base de datos transaccional** para hospedar nuestra aplicación: es capa de exploración/dashboard. SQLite funciona para MVP local; PostgreSQL/Supabase da la opción de integración por conexión SQL, sujeto a accesibilidad de red, permisos y restricciones del plan vigente.

Tasa de cierre = 100 × casos_finalizados / casos_iniciados. Minutos de ciclo demo = cerrado_en - creado_en. No equivale a horas de trabajo humano ni calcula ROI fiable sin datos reales de tiempo, volumen, costo y monetización.
