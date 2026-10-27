# Diccionario de datos ETL → Preset

Fuentes: `casos` y `eventos` de PostgreSQL local. El ETL normaliza zonas horarias a UTC. Los datos de ejemplo son sintéticos.

## Grano y claves

- `preset_casos.csv`: una fila por caso, `caso_id`. Incluye tiempo de ciclo observado **solo si el caso terminó dentro del MVP**.
- `preset_eventos.csv`: una fila por evento, `evento_id`; relacionar por `caso_id`. El nombre del actor es sustituido por una referencia pseudónima; no incluye detalles JSON.
- `preset_kpis_mensuales.csv`: una fila por mes de radicación y escenario; la tasa de cierre usa casos iniciados en ese mes, por lo que NO es una cohorte madura en meses recientes.
- `preset_actividades.csv`: recuento mensual por evento/acción en el mes en que ocurrió.

## Fórmulas auditables

| Métrica | Fórmula | Unidad | Precaución |
| --- | --- | --- | --- |
| Casos iniciados | `COUNT(casos.id)` | casos | Mes de creación |
| Casos finalizados | `COUNT(estado=FINALIZADO y cerrado_en IS NOT NULL)` | casos | En curso no cuenta |
| Tasa de cierre | `100 * finalizados / iniciados` | % | No identifica SLA |
| Tasa prevalidación | `100 * casos con validacion_previa_ok / iniciados` | % | Es una regla didáctica, no normativa |
| Tiempo de ciclo | `AVG(cerrado_en - creado_en)` | minutos | Medida de demo, NO trabajo humano |
| Eventos por actividad | `COUNT(eventos.id)` agrupado | eventos | No equivale a ahorro económico |

## Propuesta de cuatro widgets para Starter

1. Big Number: `SUM(casos_iniciados)`, filtro `escenario` y `mes`.
2. Barras: `mes` y `SUM(casos_finalizados)` por escenario.
3. Línea: `mes`, tasa de prevalidación (%); validar la agregación si hay varias filas.
4. Barras: eventos por `accion` usando `preset_actividades.csv`.

Los archivos CSV se suben manualmente. Preset Cloud no puede llegar a `db:5432` (hostname interno de Docker) ni a una BD que solo existe en `localhost` de la PC. Para conexión directa en un proyecto posterior se requiere una BD externamente accesible, usuarios de solo lectura, TLS y reglas de red apropiadas (p. ej. Supabase/Postgres cloud).

## Privacidad

Se oculta CHIP, radicado original y `detalles`. Las IDs y las áreas todavía pueden ser indirectamente identificables. Usar datos sintéticos en clase. No subir datos reales de ciudadanos o entidades sin autorización y revisión de privacidad. El pseudónimo usa salt de entrenamiento, no se debe interpretar como anonimización irreversible.
