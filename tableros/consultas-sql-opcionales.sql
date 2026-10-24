-- Consultas de referencia si está disponible SQL Lab sobre los CSV cargados.
-- Si el esquema o tabla es distinto, ajusta los nombres. NO forman automáticamente los dashboards.
SELECT escenario, SUM(casos) casos, SUM(horas_humanas_totales)/NULLIF(SUM(casos),0) horas_humanas_por_caso,
       SUM(errores)*1.0/NULLIF(SUM(casos),0) tasa_error,
       SUM(reprocesos)*1.0/NULLIF(SUM(casos),0) tasa_reproceso
FROM mba_resumen_mensual GROUP BY escenario ORDER BY escenario;

SELECT mes, SUM(beneficio_bruto_cop) AS beneficio_bruto_cop,
       SUM(mantenimiento_cop) AS mantenimiento_cop,
       SUM(beneficio_neto_operativo_cop) AS beneficio_neto_operativo_cop
FROM mba_roi_mensual GROUP BY mes ORDER BY mes;
