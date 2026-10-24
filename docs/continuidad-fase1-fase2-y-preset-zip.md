# Continuidad exacta de Fase 1 a Fase 2 + Importación de dashboards en Preset Starter

## A. ¿Hay conflicto con /07?
No. **`/07-corregir`** se mantiene en ambos kits y es el último comando de la **fase 1**. Los nuevos comandos empiezan en **`/08-cadena-valor`** y llegan a `/17-iterar`. La carpeta `trabajos/mi-proceso/07-diagnostico/` no es un comando.

La comparación realizada entre los ZIP del curso confirma que el segundo contiene todos los 41 archivos originales (los únicos modificados fueron `AGENTS.md` y `README.md`) y agrega 60 archivos nuevos. Debe utilizarse el kit más reciente como carpeta raíz de OpenCode.

## B. Migración manual (Windows, sin Python)
1. Cierra ambos proyectos en OpenCode y Camunda. **NO descomprimas el nuevo ZIP encima de la carpeta antigua.**
2. Descomprime el nuevo kit en una ruta diferente, por ejemplo `C:\\MBA\\fase2\\taller-opencode-bpmn`.
3. En el Explorador de archivos abre las dos ubicaciones: carpeta anterior y nueva.
4. Para **cada equipo** en `trabajos/` (por ejemplo `mi-proceso`, `equipo-1`), copia el **contenido** de las subcarpetas `01-fuentes`, `02-analisis`, `03-ears`, `04-modelo`, `05-bpmn`, `06-revision` a las carpetas de igual nombre de la fase 2.
5. Si un archivo ya existe en destino y no es idéntico, **no lo reemplaces**; compara ambos. Conservar el original y guardar la nueva versión con otro nombre.
6. **NO copies** desde el kit viejo `.opencode/`, `AGENTS.md`, `opencode.json`, `scripts/`, `docs/`, `plantillas/`, `ejemplos/`. El nuevo kit ya trae sus versiones; si creaste skills propios, trasládalos uno por uno después de revisarlos.
7. Inicia OpenCode y abre **la raíz nueva** `taller-opencode-bpmn/`, no solamente `trabajos/mi-proceso`.
8. Verifica `/07-corregir` y `/08-cadena-valor`. Continúa con `/08` sin repetir la fase 1 si ya quedó aprobada.

## C. Migración automática y segura (Windows + Python)
Desde la **raíz del kit nuevo**, abre una terminal en OpenCode, PowerShell o cmd:

```powershell
py scripts/migrar_trabajos_fase1.py --origen "C:\\MBA\\fase1\\taller-opencode-bpmn" --destino . --dry-run
```

Comprueba el listado: sólo deben aparecer archivos de los equipos en las seis carpetas antiguas. Si está bien:

```powershell
py scripts/migrar_trabajos_fase1.py --origen "C:\\MBA\\fase1\\taller-opencode-bpmn" --destino . --reporte "migracion-reporte.json"
```

El script no sobrescribe archivos; si detecta una colisión distinta, se detiene **antes de copiar nada**. Ignora `.gitkeep`. Conserva fechas de archivos originales y verifica SHA-256 tras cada copia. Para Linux/macOS, reemplaza `py` por `python3`.

## D. La importación de dashboards ZIP en Preset **sí existe en Starter mediante UI**
La documentación oficial distingue dos funcionalidades distintas:

- **Dashboard > Import (UI):** admite ZIP exportado desde Preset/Superset y **no exige Preset API Enterprise**. Contiene definición del dashboard, charts, datasets y referencias a databases.
- **Preset API de migración:** requiere Enterprise; no se usará en Starter.

Fuentes: https://docs.preset.io/docs/migrating-dashboards ; https://docs.preset.io/docs/free-tier-limits ; https://docs.preset.io/docs/using-csv-files

**Límite fundamental:** el ZIP de dashboard **no incluye los registros de los archivos CSV ni contraseñas de la base de datos**. Las tablas y la conexión deben estar disponibles en el workspace destino. Cargar un CSV previamente crea una tabla física y dataset, pero **no garantiza** coincidencia automática con UUID/referencias de otro export: es necesario probar mapeo/dependencias con una cuenta Starter distinta.

### Opción recomendada (repetible para el MBA)

**Una sola vez, docente:**
1. Crear un workspace Preset Starter de referencia.
2. Cargar `datos/preset/preset_resumen_mensual.csv` y `datos/preset/preset_roi_mensual.csv` como datasets (idealmente con nombres de tabla fijos: `mba_resumen_mensual`, `mba_roi_mensual`).
3. Construir los gráficos y dashboards según `tableros/widgets.json`.
4. Desde `Dashboards` usar Export para obtener el ZIP real del dashboard.
5. Ejecutar el script abajo para preparar una distribución que contenga el ZIP de exportación y los CSV.
6. Probar **en una cuenta Starter nueva** la importación y resolver cualquier conexión/dataset faltante. No asumir portabilidad sin esta prueba.

**Cada estudiante:**
1. Ingresar a un workspace Starter de Preset. Confirmar permisos para importar.
2. Abrir `Dashboards > Import`, seleccionar `dashboard_preset_importable.zip` y confirmar.
3. Cargar los CSV en caso de que las tablas necesarias aún no existan y resolver la conexión de datos solicitada; el orden de importación puede variar según dependencias.
4. Confirmar que cada widget muestra datos; no basta con que aparezca el objeto dashboard.
5. Capturar evidencia y documentar los parámetros modificados de AS-IS / TO-BE.

### Preparar carpeta de distribución (docente)

Si todavía NO tienes el export oficial del tablero, prepara los CSV solamente:

```powershell
py scripts/preparar_distribucion_preset.py --datos datos/preset --salida distribucion-preset
```

Después de exportar el dashboard desde tu workspace Preset:

```powershell
py scripts/preparar_distribucion_preset.py --datos datos/preset --export "C:\\MBA\\dashboard_export.zip" --salida distribucion-preset
```

`distribucion-preset/dashboard_preset_importable.zip` será **el archivo que se importa en Dashboards > Import**; los CSV distribuidos se usan en Upload CSV. El script sólo valida estructura básica del ZIP de exportación y prepara archivos; **no fabrica** dashboards ni asegura compatibilidad semántica entre workspaces.

### ¿Puedo generarlo 100 % local sin crear un tablero primero en Preset?

Técnicamente, Apache Superset utiliza un bundle ZIP con `metadata.yaml`, y recursos YAML de `databases/`, `datasets/`, `charts/`, `dashboards/`. Es posible **generarlo con Python** a partir de modelos y parámetros; pero conformidad estructural con ese formato **no basta** para garantizar que Preset acepte una versión localmente sintetizada ni que pueda ejecutar sus consultas sin una base accesible. Para garantizarlo en clase haría falta:
- Tomar un ZIP exportado de una versión compatible de Preset/Superset como **plantilla real**.
- Resolver UUID/referencias, tipos de métricas y layouts.
- Garantizar que la base y tablas estén accesibles (Preset cloud no puede consultar un SQLite local del alumno sin publicarlo/conectarlo).
- Hacer una **prueba de importación real en una cuenta Starter limpia**.

La ruta de exportación real del docente es de menor riesgo para una práctica de 50 minutos. Si se quiere un generador genérico en una fase posterior, es viable, pero antes se necesita un ZIP exportado de referencia y una validación en Preset para no prometer resultados no comprobados.

## E. Preguntas útiles para el docente antes de distribuir
1. ¿Habrá una **cuenta Preset por equipo**, o todos usarán una cuenta compartida? Starter admite **máximo cinco usuarios** por workspace.
2. ¿Se podrán usar CSV **sintéticos** compartidos para importar un tablero común y posteriormente recalcular las métricas particulares de cada equipo?
3. ¿Queremos **dos dashboards de referencia** iguales para todos, o generar dashboards distintos con métricas por proyecto? Para 50 minutos recomiendo dos dashboards de referencia, más una métrica personalizada por equipo.

---
## F. Novedad v2.2: generador de dashboards ZIP candidato
El nuevo kit conserva íntegramente `/01`–`/17` y añade `/18-dashboard-maestro` y `/19-verificar-importacion`. Ve `docs/dashboard-maestro-preset-v22.md` para preparar dos datasets exportados de un workspace real y ejecutar `scripts/generar_bundle_preset.py`. La generación local ya se prueba; la importación real **se debe verificar en Preset antes de clase**. Si se rechaza, usar manualmente al menos un KPI o el visor HTML local.
