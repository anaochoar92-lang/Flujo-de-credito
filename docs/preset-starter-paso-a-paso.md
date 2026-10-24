# Preset.io Starter — instructivo verificado, sin API empresarial

## Lo que realmente permite esta ruta
- Plan Starter público: USD 0, hasta 5 usuarios/1 workspace, gráficos/tableros ilimitados según página de precios consultada el 2026-10-16. Verificar condiciones en la cuenta: https://preset.io/pricing/.
- Carga CSV documentada para roles **Primary Creator / Secondary Creator** y administradores; permisos y configuración del workspace pueden variar: https://docs.preset.io/docs/using-csv-files.
- **Sí se puede importar un ZIP de dashboard mediante la interfaz de Preset Starter** (`Dashboards` > `Import`), preparado desde un export Preset/Superset. No incluye las filas CSV ni credenciales y requiere que sus fuentes de datos existan o sean conectadas. No se debe confundir el ZIP completo de este taller con el ZIP especial de dashboard. Guía: `docs/continuidad-fase1-fase2-y-preset-zip.md`. Fuente: https://docs.preset.io/docs/migrating-dashboards.
- La **Preset API** de exportar/importar dashboards se indica como disponible en Enterprise, NO se utiliza ni se promete en Starter. No es correcto enviar credenciales a scripts no verificados.

## Preparación previa del docente (idealmente antes del taller)
1. Entrar en https://preset.io/ e iniciar sesión/crear workspace Starter. Cada equipo debe respetar hasta cinco usuarios por workspace. Preferible un workspace por equipo, con un usuario de rol Creator.
2. Abrir la sección de configuración de conexiones de base de datos. Si no existe base apta para subir CSV, revisar la guía de Preset sobre CSV; en workspaces modernos suele venir lista la conexión de carga. Si no se permite cargar, pedir al administrador que habilite **Allow data upload** y el esquema correspondiente, o usar plan B.
3. Nunca subir información identificable real de titulares, propietarios, direcciones, correos, matrículas u otros datos protegidos. Usar los datos sintéticos incluidos.
4. Ejecutar desde la raíz `py scripts/taller_kpi.py todo`. Esto prepara los CSV (si no hay Python en el equipo usar los CSV ya incluidos).

## Receta de importación 1 — conjunto esencial (aprox. 3 minutos)
1. En el workspace, elegir `+` → Data → **Upload CSV** (la etiqueta exacta puede variar) o el menú `Upload file to database` → `Upload CSV`.
2. Seleccionar `datos/preset/preset_resumen_mensual.csv`. Tabla: `mba_resumen_mensual`; delimitador coma, encabezados en la primera fila (índice 0); decimal `.`; codificación UTF-8; tabla existente = **Replace** solo si es un archivo de práctica que puedes reemplazar.
3. Confirmar que en Datasets aparece `mba_resumen_mensual`, con campos `mes` (texto YYYY-MM), `escenario` (categoría), `casos` (número entero), `tasa_error` (decimal 0–1), `horas_humanas_promedio` (numérico). `mes` puede ser dimensión categórica para evitar problemas de conversión de fechas.
4. **Nunca** sumar porcentajes ni promediar las tasas mensuales sin ponderarlas; para la demo hay 55 casos por mes y escenario; para datos reales, usar `SUM(errores)/SUM(casos)` o SQL equivalente.

## Crear widgets del tablero 1 — `01 Desempeño AS-IS frente a TO-BE`
1. Abrir dataset `mba_resumen_mensual` → Create Chart / Explore.
2. **Gráfico 1:** barras agrupadas. Eje X: `escenario`; medida: `AVG(horas_humanas_promedio)`; nombre `Horas humanas por caso`. Guardar al dashboard nuevo `MBA - Eficiencia del proceso`.
3. **Gráfico 2:** barras agrupadas. X: `escenario`; medida: `SUM(errores)`; nombre `Casos con error`. Guardar en el mismo dashboard. **Nota:** si muestras tasas, calcula `SUM(errores)/SUM(casos)`.
4. **Gráfico 3:** serie temporal o barras por `mes` con series según `escenario`; medida `AVG(horas_ciclo_promedio)`; nombre `Tiempo de ciclo`. Si la herramienta exige fecha, mantener `mes` como categoría/barra o crear columna fecha `YYYY-MM-01` a partir del CSV.
5. **Gráfico 4:** Big Number `SUM(casos)` con filtro escenario = TO-BE; nombre `Casos en la muestra TO-BE`. Para horas evitadas, usa dataset ROI.

## Receta de importación 2 — ROI (aprox. 3 minutos)
1. Upload CSV `datos/preset/preset_roi_mensual.csv`. Tabla `mba_roi_mensual`.
2. **Widget 5:** Big Number, `SUM(beneficio_neto_operativo_cop)`; nombre `Beneficio operativo simulado (COP)`.
3. **Widget 6:** barras por `mes`, medida `SUM(ahorro_horas_total)`; nombre `Horas humanas evitadas / mes`.
4. **Widget 7:** barras por `mes`, medida `SUM(ahorro_laboral_cop)` junto a `SUM(ahorro_errores_cop)` si el tipo de gráfico permite dos series; nombre `Composición de ahorro (COP)`.
5. Ordenar los widgets en el dashboard 2: `MBA - ROI del proceso TO-BE`.

## Tercer dataset opcional — detalles
Upload CSV `datos/preset/preset_casos.csv` como `mba_casos` para un histograma de `horas_humanas`, filtros por `canal` y porcentajes calculados sobre casos sin duplicar. Si cargas también `preset_actividades.csv`, **son varias filas por caso**: NO sumes casos contando filas de actividades.

## Filtros y verificación final
- Comparar AS-IS y TO-BE en los mismos meses; usar los nombres exactamente `AS-IS` y `TO-BE`.
- Los costos están en **COP**, horas en **h** y las tasas se almacenan **como proporciones 0–1**.
- Visualizar la etiqueta `SINTÉTICO / DEMOSTRACIÓN` en títulos o descripciones.
- Guardar captura del tablero y anotar: nombre del workspace, URL privada, datasets subidos, problemas ocurridos y dos decisiones de negocio que sugiere el tablero.
- Si `Upload CSV` no aparece, verificar rol Creator, base y permiso de carga; no improvisar pasos ocultos ni prometas solución instantánea.

## Automatización programática: decisión de arquitectura
El código del kit **sí** genera/prepara/valida las cuatro tablas CSV por Python estándar. El tramo **Preset Starter cloud** se efectúa por su interfaz gráfica, incluyendo `Dashboards > Import` cuando el docente proporciona un ZIP de dashboard exportado. La Preset API programática de migración requiere Enterprise. El material permite preparar CSV y distribuir el ZIP oficial mediante `scripts/preparar_distribucion_preset.py`. Para uso profesional posterior, evaluar integración certificada contra un backend Superset propio o un plan Preset con API habilitada.

## Extensión v2.2 — Dashboard maestro generado desde export de datasets
Ahora hay un prototipo real de generador YAML/ZIP local que usa UUID de las tablas exportadas desde el workspace del estudiante y no requiere Enterprise: `/18-dashboard-maestro`. El archivo resultante sigue siendo **CANDIDATO** hasta que se realice una importación real en Preset Starter y se verifiquen los ocho widgets. Instrucciones: `docs/dashboard-maestro-preset-v22.md`. La creación manual de un KPI continúa siendo obligatoria para la evaluación.
