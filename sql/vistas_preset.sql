-- PostgreSQL/Supabase (solo lectura). Ejecutar luego del arranque del backend.
-- Los valores monetarios son puramente sintéticos; los campos carecen de validez normativa.
CREATE OR REPLACE VIEW vw_preset_resumen_mensual AS
SELECT to_char(date_trunc('month',creado_en),'YYYY-MM') AS mes,
       escenario, COUNT(*) AS casos_iniciados,
       SUM(CASE WHEN estado = 'FINALIZADO' THEN 1 ELSE 0 END) AS casos_finalizados,
       AVG(valor_referencia_demo) AS referencia_demo_promedio
FROM casos GROUP BY 1,2;

CREATE OR REPLACE VIEW vw_preset_eventos AS
SELECT e.id, e.caso_id, c.escenario, e.momento, e.accion, e.tarea, e.actor
FROM eventos e JOIN casos c ON c.id=e.caso_id;

-- Nunca conceder acceso general a todas las tablas desde Preset.
-- Crear un usuario PostgreSQL exclusivo, de SOLO LECTURA, limitado al esquema/vistas elegidas.
