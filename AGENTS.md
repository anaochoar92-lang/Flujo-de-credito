# Laboratorio SOP → EARS → BPMN 2.0 | Instrucciones para OpenCode

## Objetivo y audiencia
Asiste a estudiantes de MBA sin conocimientos de programación para transformar descripciones de procesos en modelos BPMN 2.0 interpretables y verificables en Camunda Desktop Modeler. Toda interacción y artefacto explicativo deben estar en español claro.

## Fuente de verdad y trazabilidad
1. Lee primero `trabajos/mi-proceso/01-fuentes/` (o la carpeta de trabajo indicada), sin inventar hechos faltantes.
2. Distingue en cada salida: **confirmado en fuente**, **confirmado por entrevistado**, **propuesta** y **pendiente de confirmar**.
3. Conserva IDs estables `ACT-`, `DEC-`, `EVT-`, `REQ-`, `PREG-` e identifica el párrafo/paso fuente de cada requerimiento.
4. Nunca consideres una suposición del modelo como decisión validada por el dueño del proceso.
5. No sobrescribas documentos originales, BPMN aportados por el estudiante ni revisiones previas. Versiona v01, v02, etc.
6. Trabaja primero el proceso **AS-IS**, después propone automatizaciones **TO-BE** en artefacto separado. No mezcles los dos.
7. Cualquier dato personal o sensible debe ser anonimizado antes de usar un servicio externo de IA.

## Flujo de trabajo recomendado
A. Usa `analizar-sop` → inventario y dudas.
B. Usa `entrevista-adversarial` → preguntas por rondas y registro de respuestas; máximo cuatro preguntas prioritarias por ronda.
C. Usa `redactar-ears` → requisitos EARS + criterios de aceptación + matriz de trazabilidad.
D. Usa `arquitectura-bpmn` → especificación JSON de tareas, eventos, gateways, pools, lanes y flujos.
E. Usa `generar-bpmn` → genera XML BPMN y ejecuta validador; deja un archivo versionado.
F. Usa `auditar-bpmn` → errores, advertencias, semántica y revisión en Camunda.
G. Usa `reconciliar-bpmn` → integra correcciones autorizadas desde BPMN editado o instrucciones textuales; genera nueva versión.

## Convenciones de modelado
- `sequenceFlow` sólo entre nodos del **mismo proceso/pool**; `messageFlow` para comunicación **entre pools**.
- Pools = participantes independientes; lanes = roles dentro de un proceso.
- Gateways exclusivos para alternativas; paralelos para tareas simultáneas; inclusivos para una o más rutas; gateways basados en eventos para esperas alternativas.
- Un evento de temporizador no es una tarea manual; un evento de mensaje no es un correo enviado por arte de magia.
- Las actividades deben formularse con verbo + objeto. Condiciones de salida de XOR deben ser observables, idealmente exhaustivas y mutuamente excluyentes.
- Para eventos límite, identificar si interrumpen o no la actividad.
- No incluir conectores/expresiones ejecutables Zeebe, credenciales ni endpoints inventados.
- `isExecutable=false` por defecto; la validación visual **no** prueba que un proceso se pueda desplegar.
- El JSON es una especificación auxiliar del taller, **no** parte de la norma BPMN.
- Si una corrección hecha en Camunda altera el XML, prioriza el XML confirmado y solicita reconciliar el JSON; no lo regenere encima sin revisar diferencias.

## Generación y pruebas (si el entorno tiene Python 3)
```
python scripts/crear_bpmn.py ejemplos/modelos/reexpedicion.json ejemplos/bpmn/reexpedicion.bpmn
python scripts/validar_bpmn.py ejemplos/bpmn/reexpedicion.bpmn
python scripts/inspeccionar_bpmn.py ejemplos/bpmn/reexpedicion.bpmn trabajos/mi-proceso/06-revision/inventario.md
```
No afirmes que un archivo pasó la validación si no ejecutaste la herramienta. Si la herramienta no está disponible, documenta la limitación y entrega el XML como borrador no validado.


## Segunda fase del proyecto — Sesión 3: AS-IS → TO-BE → KPI → Excel → Preset → ROI
1. Seguir `docs/readme-fase2.md` y `docs/origen-presentacion-sesion3.md`; usar skills 08–17. **No** volver a generar AS-IS sobre TO-BE.
2. Diagnóstico guiado por cadena de valor, 5 porqués, matriz de criticidad y costo/beneficio; distinguir supuestos de mediciones.
3. Realizar entrevistas de **máximo 4 preguntas por turno** y esperar respuesta/confirmación; no hacer 16 fases sin interacción.
4. Trazar actividad BPMN ↔ oportunidad ↔ requerimiento EARS TO-BE ↔ KPI ↔ campo CSV ↔ fórmula Excel ↔ widget ↔ decisión.
5. Datos de ejemplo: `datos/demo` y `datos/preset` son **SINTÉTICOS**. Nunca afirmar que corresponden a expedientes reales SDP. Solicitar anonimizar toda evidencia real antes de nube.
6. Preset Starter: cargas CSV manuales mediante UI; los dashboards se diseñan paso a paso. No prometer API cloud Enterprise en cuentas gratis.
7. ROI: separar ahorro de capacidad de ahorro financiero. No asumir que horas liberadas equivalen a menor gasto.
8. Scripts `scripts/taller_kpi.py` sin dependencias; archivos Excel ya generados para estudiantes. Si el usuario cambia CSV, **NO** asumir refresco automático del Excel.
9. Para ciclo de 50 minutos priorizar un proceso, una mejora, tres KPI, un CSV principal, dos gráficos, un dashboard y un razonamiento sobre ROI.

## Fase 2.2 — Dashboard maestro Preset ZIP local (comandos /18 y /19)
- Mantener `/01` a `/17` sin renombrarlos; nuevos comandos `/18-dashboard-maestro` y `/19-verificar-importacion`.
- El script `scripts/generar_bundle_preset.py` genera **un CANDIDATO** de importación con UUIDs procedentes de un **export real de datasets del propio workspace**, no una importación validada en Preset.
- Se permite la ruta A (ZIP oficial exportado y probado por docente), B (candidato generado desde los datasets), C (crear al menos un KPI a mano) y D (dashboard HTML local). Guía completa en `docs/dashboard-maestro-preset-v22.md`.
- Ni la API de Preset Starter ni el acceso web a una cuenta del alumno están disponibles: no aseverar importación o despliegue remoto sin que el alumno confirme resultados.
- Preguntar y esperar respuesta, máximo 3 tareas técnicas o 4 preguntas por turno. El alumno debe construir manualmente por lo menos un KPI y explicar su cálculo.
- Evitar doble conteo AS-IS/TO-BE de casos pareados. Horas por caso: `SUM(horas_humanas_totales)/SUM(casos)`; tasas de error `SUM(errores)/SUM(casos)`. Horas liberadas no son automáticamente ahorro monetario.

## Actualización de Word (v2.3, comando /00)
- Cuando el estudiante cambia el DOCX original, prioriza `/00-actualizar-sop`; el comando preexistente `/01-analizar` continúa siendo válido para el análisis inicial.
- Ejecuta el script local `scripts/actualizar_sop.py` para generar y versionar el Markdown y un diff textual; solicita selección expresa si hay varios Word en la carpeta.
- Considera `01-fuentes/SOP_ACTUAL.md` la versión textual vigente; no analices como actuales archivos anteriores bajo `.historial_sop`.
- El diff no significa que las decisiones de negocio cambiaron: interroga y confirma antes de actualizar EARS/JSON/BPMN.
- No borrar las versiones originales, no sustituir el AS-IS con TO-BE, ni invalidar KPI sin analizar impacto.
