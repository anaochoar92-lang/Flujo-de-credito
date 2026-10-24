# Flujo de crédito preaprobado

Análisis del flujo de solicitud de crédito (producto Expomóvil) para identificar qué partes del proceso se pueden automatizar. Objetivo clave: disminuir los tiempos de las actividades de expediente.

---

# Taller MBA — SOP → EARS → BPMN 2.0 con OpenCode + Camunda Modeler

**Kit listo para trabajar por equipos.** Idioma: español. Prioriza a personas sin formación en software. Incluye 7 skills para OpenCode, 7 comandos, plantillas, un ejemplo de reexpedición basado en el SOP trabajado y scripts Python sin dependencias adicionales.

## Inicio rápido (interfaz gráfica de OpenCode)

1. Descarga y descomprime este kit en una carpeta propia, por ejemplo `Documentos\\MBA-Procesos`.
2. Abre **OpenCode Desktop** y selecciona esa carpeta como proyecto. Espera a que cargue las reglas y las carpetas del proyecto.
3. Copia tu Word `.docx` o SOP `.md`/`.txt` dentro de `trabajos/mi-proceso/01-fuentes/`. No alteres el original.
4. **Para Word**: pide a OpenCode «extrae el texto del Word [archivo] a un Markdown de la carpeta 01-fuentes usando `scripts/extraer_docx.py`». Si no es posible usar Python, en Word haz **Guardar como → Texto sin formato**, revisa y copia el `.txt` a la carpeta. La lectura básica de Word no preserva ilustraciones.
5. En el chat de OpenCode escribe `/01-analizar`. En interfaces donde no aparezcan los comandos personalizados, escribe: «Aplica el skill `analizar-sop` al procedimiento de `trabajos/mi-proceso/01-fuentes/` y escribe el inventario».
6. Escribe `/02-entrevistar` y **responde personalmente** la primera ronda de preguntas. Repite por segunda ronda.
7. Escribe `/03-ears`. Revisa que ningún requisito haya sido inventado; comprueba las referencias al SOP.
8. Escribe `/04-modelar` y después `/05-generar`. OpenCode construirá el JSON y, si hay Python 3 disponible, ejecutará los scripts para producir `proceso-v01.bpmn`.
9. Abre `proceso-v01.bpmn` en **Camunda Desktop Modeler** (menú abrir archivo) y comprueba visualmente piscinas, carriles, tareas, eventos, flechas y decisiones.
10. Guarda los cambios como `proceso-v02.bpmn` (**Guardar como**, no sobreescribir) y vuelve a OpenCode con `/06-auditar` y `/07-corregir`. Indica el archivo editado y las correcciones; no regeneres desde un JSON desactualizado sobre el archivo editado.

### Comandos en OpenCode
`/01-analizar` · `/02-entrevistar` · `/03-ears` · `/04-modelar` · `/05-generar` · `/06-auditar` · `/07-corregir`.

### Material para demostración inmediata
Abre directamente `ejemplos/bpmn/reexpedicion-v01.bpmn` en Camunda Modeler. Procede del ejemplo `ejemplos/modelos/reexpedicion.json`, inspirado en las etapas **F y G** del SOP previo. **No es versión institucional aprobada.**

## Vista de carpetas
```
MBA-Procesos/
├── AGENTS.md                    # Reglas globales del proyecto para OpenCode
├── opencode.json                # Habilita carga de skills del proyecto
├── .opencode/
│   ├── skills/                  # 7 directorios, cada uno con SKILL.md
│   └── commands/                # 7 comandos del taller
├── trabajos/mi-proceso/
│   ├── 01-fuentes/              # Word, MD, TXT, BPMN previo
│   ├── 02-analisis/             # Inventario y entrevista
│   ├── 03-ears/                 # Requisitos y criterios
│   ├── 04-modelo/               # JSON intermedio
│   ├── 05-bpmn/                 # XML BPMN versionado
│   └── 06-revision/             # Auditores y correcciones
├── ejemplos/
│   ├── sop/                     # SOP usado como ejemplo
│   ├── ears/                    # Requisitos EARS ilustrativos
│   ├── modelos/                 # JSON ejemplo
│   └── bpmn/                    # Diagrama y reporte de validación
├── plantillas/
├── docs/                        # Material docente y referencia
├── scripts/                     # Extraer Word, generar, inspeccionar, validar
└── tests/
```

## Herramientas
- **OpenCode Desktop** (interfaz gráfica): https://opencode.ai/ . Consultar https://docs.opencode.ai/docs/skills/ y https://docs.opencode.ai/docs/commands/ .
- **Camunda Desktop Modeler**: https://camunda.com/download/ . Guía: https://docs.camunda.io/docs/components/modeler/desktop-modeler/ .
- **Python 3** opcional para generar/validar XML: comprobar `py --version` en Windows o `python3 --version` en Linux/macOS. Scripts sólo usan biblioteca estándar.

## Si deseas ejecutar los scripts manualmente
Desde la carpeta raíz del kit en Windows PowerShell:
```
py scripts/extraer_docx.py "trabajos/mi-proceso/01-fuentes/mi-proceso.docx" "trabajos/mi-proceso/01-fuentes/mi-proceso.md"
py scripts/crear_bpmn.py ejemplos/modelos/reexpedicion.json ejemplos/bpmn/reexpedicion-v01.bpmn
py scripts/validar_bpmn.py ejemplos/bpmn/reexpedicion-v01.bpmn
py scripts/inspeccionar_bpmn.py ejemplos/bpmn/reexpedicion-v01.bpmn ejemplos/bpmn/inventario.md
```
Para macOS/Linux sustituye `py` por `python3`.

## Importante: qué garantiza el kit
`crear_bpmn.py` produce una **primera versión gráfica XML BPMN 2.0 con BPMN DI** basada en un JSON revisable. `validar_bpmn.py` detecta muchos errores de estructura y referencias, pero **no realiza validación contra XSD oficial** ni comprueba configuración del motor Camunda. El modelo debe revisarse por expertos y en el Modeler; la diagramación automática es aproximada. No desplegar el ejemplo como ejecutable.

## Fuentes técnicas
- OpenCode Skills: https://docs.opencode.ai/docs/skills/
- OpenCode Commands: https://docs.opencode.ai/docs/commands/
- OpenCode Rules: https://docs.opencode.ai/docs/rules/
- Camunda Desktop Modeler: https://docs.camunda.io/docs/components/modeler/desktop-modeler/
- EARS, A. Mavin et al.: https://alistairmavin.com/ears/


---
## NUEVO: continuación Sesión 3 — TO-BE, KPIs, ROI y Preset
El mismo ZIP ahora incluye la fase 2 completa. Ver **[`docs/readme-fase2.md`](docs/readme-fase2.md)** y la agenda de **[`docs/guia-50-minutos.md`](docs/guia-50-minutos.md)**. Incluye diez skills/comandos nuevos, CSV sintéticos, libro Excel de ecuaciones, scripts Python y recetas de tableros Preset Starter.


### Migración desde el ZIP de la fase 1 y dashboards ZIP de Preset Starter
Consulta [`docs/continuidad-fase1-fase2-y-preset-zip.md`](docs/continuidad-fase1-fase2-y-preset-zip.md). Los primeros 7 comandos se conservan; la fase 2 inicia en `/08-cadena-valor`. Copia **solo** `trabajos/<equipo>/01-fuentes` a `06-revision` mediante el script seguro `scripts/migrar_trabajos_fase1.py`, no sobreescribas `.opencode/`. Preset Starter **sí admite** importación de un ZIP de dashboard exportado por interfaz, aunque los datos y credenciales se aprovisionan por separado. Se incluye `scripts/preparar_distribucion_preset.py` para distribuir esos archivos.

---
## ACTUALIZACIÓN v2.2 — Dashboard maestro y opción de ZIP local

- Guía central: [`docs/dashboard-maestro-preset-v22.md`](docs/dashboard-maestro-preset-v22.md).
- Comandos nuevos **`/18-dashboard-maestro`** y **`/19-verificar-importacion`**. Se conservan intactos `/01` a `/17`, incluido `/07-corregir`.
- Script `scripts/generar_bundle_preset.py`: crea un **ZIP candidato** con dos dashboards y ocho charts, utilizando bases y datasets exportados del propio workspace Preset. Requiere PyYAML (`py -m pip install -r requirements-preset.txt`).
- No es una solución de un clic universal: primero se cargan datos CSV y se exportan sus datasets, y después hay que probar la importación generada desde la interfaz Preset Starter.
- Ruta segura para clase: el docente importa y valida en otro workspace un **ZIP exportado real** y lo distribuye como plantilla; cada estudiante crea al menos una métrica de forma manual. Plan B: dashboard HTML local incluido.

---
## Actualización v2.3 — Si un alumno modifica su DOCX

**Nuevo comando:** `/00-actualizar-sop` (se conserva `/01-analizar` para el inicio normal, y `/07-corregir` para reconciliar BPMN). Guardar el DOCX en `trabajos/mi-proceso/01-fuentes/`, abrir OpenCode y escribir `/00-actualizar-sop`. OpenCode debe ejecutar `scripts/actualizar_sop.py` (requiere Python 3); conserva snapshots en `.historial_sop`, crea `SOP_ACTUAL.md` y un informe `02-analisis/impacto-sop-vNN.md`.

Si se quiere ejecutar manualmente desde la raíz del proyecto:

```powershell
py scripts/actualizar_sop.py --proyecto trabajos/mi-proceso --docx "trabajos/mi-proceso/01-fuentes/mi-proceso.docx" --dry-run
py scripts/actualizar_sop.py --proyecto trabajos/mi-proceso --docx "trabajos/mi-proceso/01-fuentes/mi-proceso.docx"
```

No hay sincronización automática con el DOCX si este se vuelve a modificar: volver a ejecutar el comando. Si un estudiante tiene varios `.docx`, especificar explícitamente cuál corresponde al proceso. La conversión no incluye el contenido visual de figuras o diagramas; estos requieren revisión humana.

Guía de intervenciones en diapositivas: `docs/plan-micropracticas-sesion3.md`.
