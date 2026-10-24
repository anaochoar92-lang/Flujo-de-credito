# Registro de versiones BPMN — Flujo de crédito (AS-IS)

| Versión | Fecha | Archivo | Origen | Estado |
|---|---|---|---|---|
| v01 | 2026-10-23 | `proceso-v01.bpmn` | Generado desde `04-modelo/especificacion.json` con `scripts/crear_bpmn.js` | **BORRADOR** sin revisar en Camunda · 0 errores, 8 advertencias (`validacion-v01.json`) |
| v02 | 2026-10-24 | `proceso-v02.bpmn` | `04-modelo/especificacion-v02.json`: ronda 2 (temporizador de 10 días hábiles, motivo de devolución). Ver `06-revision/cambios-v02.md` | **BORRADOR** sin revisar en Camunda · 0 errores, 8 advertencias (`validacion-v02.json`). **Versión vigente** |

## v01 — 2026-10-23
- **Fuentes:** `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx` y la ronda 1 de la entrevista (PREG-001 a PREG-004).
- **Contenido:** 1 pool (Banco), 6 carriles, 23 nodos (1 inicio, 5 fines, 10 tareas, 6 decisiones, 1 temporizador) y 25 flujos.
- **Herramientas:** este equipo no tiene Python. Se usaron `scripts/crear_bpmn.js` y `scripts/validar_bpmn.js`, que son ports en Node.js de `crear_bpmn.py` y `validar_bpmn.py`. Antes de usarlos se comprobó que dan **el mismo resultado** que los scripts de Python en los dos ejemplos del kit: `ejemplos/bpmn/reexpedicion-v01.bpmn` y `ejemplos/tobe/reexpedicion-to-be-v02.bpmn`.
- **Validación:** 0 errores, 8 advertencias.
  - 6 son de gateways sin condiciones formales, algo esperado en un modelo descriptivo.
  - Las otras 2 dicen que `SVC_001` y `END_VENCIDA` son «no alcanzables». Es un falso positivo: se llega a ellos desde el temporizador `TMR_001`, y el validador (igual que el de Python) no recorre los eventos límite.
- **Dibujo:** se comprobó por código que no hay cajas solapadas. Hay **una** línea que pasa sobre una caja ajena: `F_015` («Volver a análisis») cruza «Informar decisión al cliente». Se ajusta a mano en Camunda.
- **Pendientes que se ven en el diagrama:** el temporizador de 10 días no tiene expresión de tiempo (PREG-013), y AS-01 (no se repite Riesgo tras modificar datos).

## Cómo abrir y revisar
1. Abrir Camunda Desktop Modeler → *File → Open File…* → `trabajos/mi-proceso/05-bpmn/proceso-v01.bpmn`.
2. Seguir `06-revision/checklist-camunda-v01.md`.
3. Si se ajusta el dibujo, **guardar con otro nombre** (`proceso-v02.bpmn`) y no regenerar desde el JSON encima del archivo editado.

## Regenerar (sin Python)
```
node scripts/crear_bpmn.js trabajos/mi-proceso/04-modelo/especificacion.json trabajos/mi-proceso/05-bpmn/proceso-vNN.bpmn
node scripts/validar_bpmn.js trabajos/mi-proceso/05-bpmn/proceso-vNN.bpmn --json trabajos/mi-proceso/05-bpmn/validacion-vNN.json
```
El generador no sobrescribe un archivo que ya existe.

## v02 preparada para Camunda 8.10 — 2026-10-24
- `proceso-v02.bpmn` se modificó **en su lugar**, por decisión del equipo, para poder desplegarlo en Camunda 8.10. El proceso ahora es ejecutable, con ID `Process_Credito_ASIS`, tareas de usuario de Camunda, condiciones FEEL, temporizador `P14D` y tipo de trabajo en `SVC_001`. El flujo del proceso no cambió.
- `proceso-v01.bpmn` solo se marcó como diagrama de Camunda 8.10 y no se puede desplegar.
- Detalle, variables y verificación: `06-revision/despliegue-camunda-8.10.md`.
- **No regenerar desde `04-modelo/especificacion-v02.json`**: el JSON ya no coincide con el XML.
