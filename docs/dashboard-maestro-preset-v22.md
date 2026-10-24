# Fase 2.2 — Dashboard maestro: automatización local + Preset Starter

**Audiencia:** estudiantes de MBA que trabajan en OpenCode Desktop sin conocimientos de programación.  
**Ejemplo:** reexpedición de recibos (SDP) sobre datos enteramente **SINTÉTICOS**.  
**Meta pedagógica:** contrastar AS-IS vs. TO-BE, construir métricas con sus ecuaciones y defender una decisión económica.

## Lo que está probado y lo que NO

- Probado localmente: generación de los cuatro CSV, inspección de columnas, lectura de dos ZIP de datasets con YAML, integridad de referencias UUID en el ZIP generado, construcción de dos dashboards con ocho charts, pruebas automatizadas del kit.
- Documentado por Preset (2026): carga de CSV desde UI y exportación/importación de ZIP de dashboards, disponible para roles autorizados. API programática de migración no se presupone en Starter.
- **NO probado aquí:** importar efectivamente un ZIP sintetizado por el script a un workspace Preset Starter. El archivo se llama **CANDIDATO**; su aceptación real depende de versiones, serialización de gráficos y base conectada. Requiere prueba del docente antes de repartir como solución lista.
- **NO** se incluyen credenciales, enlaces de acceso, filas CSV dentro del dashboard ZIP ni automatización web con login.

## Opciones de uso: cuál conviene

| Modalidad | Trabajo del equipo | Riesgo | Recomendación |
|---|---|---|---|
| **A. Dashboard maestro exportado REAL** | Importar ZIP certificado por docente; resolver conexión si aplica; personalizar 1 KPI. | Menor, *si* ya se probó en la cuenta destino. | Principal para clase de 50 min. |
| **B. Generador local desde datasets exportados** | Subir dos CSV, exportar sus datasets, correr 1 comando Python, importar ZIP candidato, verificar. | Medio: plantilla todavía sin prueba en Starter. | Demostración avanzada/docente; piloto previo. |
| **C. Ruta manual garantizable** | Subir dos CSV, construir 2–3 widgets de forma guiada y capturar evidencia. | Depende de permisos/cuenta; no requiere formato ZIP. | Respaldo para todos los equipos. |
| **D. HTML local** | Abrir `tableros/dashboard_local.html` y cargar CSV. | No depende de Preset; no equivale a entregar un dashboard cloud. | Plan de contingencia. |

## A. Preparación inicial del docente — una sola vez (fuera de clase)

1. Iniciar sesión en Preset Starter y confirmar rol **Primary Creator / Secondary Creator** o superior.
2. Cargar `datos/preset/preset_resumen_mensual.csv` como tabla **`mba_resumen_mensual`**.
3. Cargar `datos/preset/preset_roi_mensual.csv` como tabla **`mba_roi_mensual`**. Escribir los nombres exactamente; no usar nombres con espacios.
4. En `Data > Datasets`, comprobar ambas tablas y tipos. `mes` es texto `YYYY-MM`, COP numérico, tasas decimales de 0 a 1.
5. Construir los ocho widgets de `tableros/widgets.json` en dos tableros, o probar primero el procedimiento automatizado B.
6. `Dashboards > Export`: guardar el ZIP auténtico de los dos dashboards, p.ej. `MASTER_PRESET_EXPORT_REAL.zip`.
7. **Probar en otra cuenta Starter** (con permisos adecuados), con sus CSV cargados. Verificar que los ocho charts muestran datos y que se pueden editar.
8. Solo entonces ejecutar `py scripts/preparar_distribucion_preset.py --datos datos/preset --export "RUTA\MASTER_PRESET_EXPORT_REAL.zip" --salida distribucion-preset` y compartir esa carpeta.
9. No compartir el ZIP antes de inspeccionar que no incluya secretos/URIs privadas ni datos personales; los ZIP pueden incluir metadatos de conexión.

**Advertencia:** los ZIP exportados no contienen filas CSV. Cuando la conexión del destino es distinta, importar el dashboard no garantiza que quede funcionando. Las referencias UUID deben corresponder a las del workspace destino o resolverse antes; véase método B.

## B. Automatización local con dos datasets reales del workspace

**Prerequisito:** Python 3 y PyYAML (`py -m pip install -r requirements-preset.txt`). Este comando instala un paquete Python, pero el script no accede a Internet, no inicia sesión en Preset ni usa la API empresarial.

1. En el mismo workspace donde deseas importar el dashboard, sube los dos CSV con nombres de tabla exactos.
2. Ve a `Data > Datasets`, selecciónalos y utiliza **Export**. Descarga un ZIP que contenga ambos o un ZIP por dataset. Guarda los archivos en tu computador; por ejemplo `C:\MBA\datasets_exportados.zip`.
3. En OpenCode (con la raíz del kit abierta), ejecuta:

```powershell
py -m pip install -r requirements-preset.txt
py scripts/generar_bundle_preset.py --export-datasets "C:\MBA\datasets_exportados.zip" --salida "resultados\dashboard_mba_CANDIDATO.zip"
```

Si descargaste dos ZIP independientes:

```powershell
py scripts/generar_bundle_preset.py `
  --export-datasets "C:\MBA\resumen_export.zip" `
  --export-datasets "C:\MBA\roi_export.zip" `
  --salida "resultados\dashboard_mba_CANDIDATO.zip"
```

4. El programa valida que estén ambas tablas, que cada dataset tenga su conexión de base exportada y que los CSV de ejemplo tengan las columnas esperadas. Genera el ZIP y `dashboard_mba_CANDIDATO.reporte.json`.
5. Antes de importar: revisa los archivos YAML de la exportación original; **no compartas cadenas de conexión con credenciales**, datos personales ni secretos. No ejecutes un ZIP de procedencia desconocida.
6. En Preset: `Dashboards > Import`, selecciona **solo** `resultados/dashboard_mba_CANDIDATO.zip`. No selecciones el ZIP del taller ni los CSV.
7. Si Preset lo rechaza, registra **el texto exacto** del error en `trabajos/mi-proceso/11-preset/errores-importacion.md` (sin secretos), no afirmes que fue exitoso. Ejecuta `/19-verificar-importacion` en OpenCode.
8. Si se importa, abre cada gráfico y verifica que consulta datos. Un icono dibujado o una tarjeta vacía no es una prueba de ejecución.
9. Si el import falla, utiliza de inmediato la ruta C o D; el objetivo de la clase no debe depender de este paso experimental.

**Diseño del generador:** usa los UUID de datasets y bases extraídos de un export del propio workspace; crea nuevos UUID para ocho charts y dos dashboards; valida vínculos internos. No sobrescribe activos existentes intencionalmente (si repites el comando, crea nuevos UUID). **No incluye ni inventa filas o credenciales.**

## C. Ruta manual: cada equipo aprende a crear un KPI

1. Upload CSV `preset_resumen_mensual.csv` a tabla `mba_resumen_mensual`.
2. `Data > Datasets` → abrir tabla → Chart Builder.
3. **Nombre del gráfico:** `Horas humanas por caso`.
4. **Tipo:** Bar Chart; dimensión `escenario`.
5. **Métrica:** crear una *custom SQL metric* con esta expresión:

```sql
SUM(horas_humanas_totales) / NULLIF(SUM(casos), 0)
```

6. Guardar el gráfico en `MBA - Desempeño AS-IS vs TO-BE`.
7. Leer los valores de AS-IS y TO-BE; discutir por qué **no conviene AVG(horas_humanas_promedio) si los meses tienen diferente número de casos**.
8. Segundo KPI recomendado: tasa de error `SUM(errores) / NULLIF(SUM(casos),0)`; visualización barra o métrica numérica por escenario. Formatear como porcentaje.
9. Tercer KPI recomendado: horas evitadas desde `mba_roi_mensual`, métrica `SUM(ahorro_horas_total)` por mes.
10. Volver al Excel `datos/Modelo_KPI_ROI_Reexpedicion.xlsx` y diferenciar ahorro laboral *potencial* de ahorro *monetizable*.

## Ecuaciones clave

- Horas promedio de trabajo humano por caso: `SUM(horas_humanas_totales) / SUM(casos)`.
- Reducción porcentual de horas: `(horas_ASIS - horas_TOBE) / horas_ASIS × 100`.
- Tasa de errores: `SUM(errores) / SUM(casos)` (proporción).
- Horas evitadas: `horas_ASIS - horas_TOBE` para volumen comparable.
- Beneficio laboral monetizable: `horas_evitadas × costo_hora × fracción_monetizable`.
- Beneficio operativo neto: `ahorro_laboral_monetizable + ahorro_errores - mantenimiento`.
- ROI año 1: `(beneficio_neto_operativo_anual - inversion_inicial) / inversion_inicial × 100`.

**Ojo:** el ROI del primer año no debe calcularse sumando dos veces la inversión. Ninguna hora liberada es automáticamente una reducción del presupuesto.

## Plan de 50 minutos por equipo

| Minutos | Acción y evidencia |
|---:|---|
| 0–5 | Recuperar versión TO-BE y confirmar oportunidad de mejora y tres KPI. |
| 5–12 | Modificar los supuestos del Excel (conservar una copia); revisar columnas CSV. |
| 12–20 | Subir dos CSV a Preset o verificar que ya existen. |
| 20–30 | **Ruta A/B**: importación de ZIP que el docente haya probado. **Ruta C**: crear 1 KPI manual. |
| 30–39 | Construir un KPI personalizado adicional y capturar el gráfico. |
| 39–45 | Mostrar tendencia, reducción de errores/horas y ROI calculado en Excel. |
| 45–50 | Presentación de 2 minutos: conclusión, supuestos, riesgo y decisión recomendada. |

## Evidencias para evaluación

- BPMN TO-BE versionado y actividad automatizada identificada.
- 3 KPI con ecuaciones, campos, unidades, frecuencia y responsable.
- CSV con marca SINTÉTICO o con datos empresariales debidamente anonimizados.
- Excel con supuestos explícitos y sin doble conteo.
- 2 capturas de Preset (o demostración HTML de contingencia, señalada como tal).
- Una recomendación fundamentada (qué automatizar, por qué, con qué riesgo y cómo medirlo).

## URLs de referencia

- Preset CSV: https://docs.preset.io/docs/using-csv-files
- Migrar dashboards ZIP: https://docs.preset.io/docs/migrating-dashboards
- Migrar datasets ZIP: https://docs.preset.io/docs/migrating-datasets
- Mapeo de UUIDs: https://docs.preset.io/docs/managing-content-across-workspaces
- Ejemplos YAML reales de Preset: https://github.com/preset-io/public-examples
- Apache Superset dashboard import: https://superset.apache.org/developer-docs/api/import-dashboard-s-with-associated-charts-datasets-databases/
