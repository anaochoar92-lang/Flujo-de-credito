# Ejemplo 5: seguimiento y KPI
Frontend `/indicadores` con widgets conteo casos, tiempos por estado y errores; CSV exportable.
API `GET /api/kpis`, `GET /api/exportaciones`; DB vista sobre solicitudes+instancias+eventos.
EARS: "Mientras existan datos válidos, el sistema deberá presentar el volumen y tiempo mediano de ciclo por mes, indicando el periodo y fuente."
ETL `docker compose run --rm etl`; probar nombres/columnas, sin PII, con manifiesto y conteos consistentes.
Distinguir tiempos de tareas humanas vs tiempo total del proceso; datos mock rotulados simulados.
