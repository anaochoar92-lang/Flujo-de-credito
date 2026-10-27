# BPMN del MVP — paso 24 (`/24-camunda`) y estado de todos los BPMN para Camunda 8.10

**Fecha:** 2026-10-27 · **Archivo:** `14-mvp/proceso-mvp-v01.bpmn` · **Estado:** **PROPUESTA**, sin abrir todavía en Camunda Modeler.
**Base:** `08-tobe/proceso-to-be-v03.bpmn`, `14-mvp/alcance-equipo.md`, `14-mvp/ears-equipo.md` (REQ-MVP-01 a 03, aprobados). Datos SINTÉTICOS.
**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio).

## 1. Qué contiene el BPMN del MVP
El tramo del TO-BE v03 que cubre el MVP, desde el envío del enlace al portal hasta que Despacho verifica el expediente digital. Se conservan los **mismos IDs del v03**, que coinciden con el contrato de la API del paso 23 (`CL_CARGAR`, `TB_ACT_REVISAR`, `TB_ACT_VERIF`).

| Elemento | Tipo | Configuración para Camunda 8.10 | Origen |
|---|---|---|---|
| `Process_Credito_MVP` | Proceso del banco, **ejecutable** | `isExecutable="true"`, plataforma Camunda Cloud 8.10.0 | Paso 24 |
| `Process_Cliente_MVP` (`CL_START`, `CL_CARGAR`, `CL_END`) | Pool del cliente, **no ejecutable** | — (el cliente actúa en el portal) | v03 |
| `TB_SND_ENLACE` | Tarea de envío | Tipo de trabajo `enviar-correo-enlace` | REQ-TOBE-001, 002 |
| `TB_RCV_DOCS` | Tarea de recepción | Mensaje `documentos-cargados`, `correlationKey = solicitudId` | REQ-TOBE-003 |
| `TB_SVC_VALIDAR` | Tarea de servicio | Tipo de trabajo `validar-documentos` → variable `resultadoValidacion` | REQ-MVP-01 |
| `TB_GW_VALIDO` | Decisión exclusiva | `"valido"` → Despacho · `"dudoso"` → Legal · `"rechazado"` → corrección · `"agotado"` → ruta en papel | REQ-MVP-01, 02 |
| `TB_SND_CORREGIR` | Tarea de envío | Tipo de trabajo `enviar-correo-correccion` | REQ-MVP-01 |
| `TB_ACT_REVISAR` → `TB_GW_LEGAL` | Tarea de usuario (Legal) | `zeebe:userTask`; `legalAcepta` (`true` / `false`) | REQ-MVP-02 |
| `TB_ACT_VERIF` → `TB_GW_VERIF` | Tarea de usuario (Despacho) | `zeebe:userTask`; `expedienteOk` (`true` / `false`) | REQ-MVP-03 |
| `END_VERIFICADO`, `END_PAPEL_AGOTADO`, `END_PAPEL_LEGAL` | Eventos de fin | — | REQ-MVP-01 a 03 |

**Variables al iniciar una instancia:** `solicitudId` (formato `SOL-9NNNN`, DAT-1). Sin ella, el mensaje `documentos-cargados` no se puede correlacionar.

## 2. Diferencias con el TO-BE v03 (y por qué)
| Punto | TO-BE v03 | MVP v01 | Fuente |
|---|---|---|---|
| Legal **rechaza** un documento dudoso | Vuelve a pedir el documento al cliente (`TB_SND_CORREGIR`) | Pasa a la ruta en papel (`END_PAPEL_LEGAL`) | REQ-MVP-02 y supuesto de `alcance-equipo.md`. **[PENDIENTE DE CONFIRMAR]** cuál regla vale para el TO-BE |
| Despacho pide corrección | Tarea humana `TB_ACT_PEDIR` | Vuelve directo a esperar documentos: el pedido se registra al completar `TB_ACT_VERIF` con `expedienteOk = false` | Contrato del paso 23 (`CORREGIR` + documento) |
| Temporizadores, recordatorios, llamada, falla del portal, recogida, ruta en papel completa y desembolso | Sí | No | Exclusiones CTX-3 |
| Subproceso `SUB_T01` | Sí | No: los pasos van sueltos, sin subproceso | Simplificación del MVP |

## 3. Validación
| Herramienta | Resultado |
|---|---|
| `scripts/validar_bpmn.py` (kit) | **0 errores, 0 advertencias** |
| `bpmnlint` con las reglas de compatibilidad **Camunda 8.10** (`bpmnlint-plugin-camunda-compat` 2.63.0, las mismas que usa Modeler) | **0 errores**, 2 avisos: `TB_ACT_REVISAR` y `TB_ACT_VERIF` no tienen formulario de Camunda (se completan desde la app, no desde Tasklist) |
| `bpmnlint:recommended` | 0 errores, 0 avisos |
| Solape de figuras (por código) | Ninguno |

**No comprobado:** que se vea bien en Camunda Modeler ni que se despliegue en el clúster. Eso lo confirma quien tenga las credenciales (paso 24).

## 4. Cómo probarlo (paso 24)
1. Abrir `proceso-mvp-v01.bpmn` en Camunda Modeler y revisar el panel *Problems*. Si se mueve algo, **guardar como `proceso-mvp-v02.bpmn`**.
2. *Deploy* al clúster 8.10. Las autorizaciones son las de `06-revision/despliegue-camunda-8.10.md`; agregar `Process_Credito_MVP` si se dieron por ID de proceso.
3. Iniciar 1 instancia con `{"solicitudId": "SOL-9xxxx"}` y completar el trabajo `enviar-correo-enlace`.
4. Publicar `documentos-cargados` con esa clave y completar `validar-documentos` con `{"resultadoValidacion": "dudoso"}`.
5. Completar las **2 tareas**: `TB_ACT_REVISAR` con `{"legalAcepta": true}` y `TB_ACT_VERIF` con `{"expedienteOk": true}` → la instancia termina en «Expediente digital verificado».
6. No poner credenciales en el repositorio.

## 5. Estado de todos los BPMN frente a Camunda 8.10 (revisión del 2026-10-27)
Revisados con las mismas reglas de compatibilidad 8.10 que usa Camunda Modeler.

| Archivo | Para qué | Errores 8.10 | Lectura |
|---|---|---|---|
| `05-bpmn/proceso-v01.bpmn` | AS-IS descriptivo (histórico) | 1: el proceso no es ejecutable | **Esperado.** Lo reemplaza la v02; no se toca (regla de versionado) |
| `05-bpmn/proceso-v02.bpmn` | **AS-IS vigente** | **0** | Listo. 9 avisos: tareas sin formulario de Camunda |
| `08-tobe/proceso-to-be-v01.bpmn` | TO-BE descriptivo (histórico) | 2: pools no ejecutables | **Esperado.** Lo reemplazan la v02 y la v03 |
| `08-tobe/proceso-to-be-v02.bpmn` y `-v02-local.bpmn` | TO-BE anterior | **0** | Listos; los reemplaza la v03 |
| `08-tobe/proceso-to-be-v03.bpmn` | **TO-BE vigente** | **0** | Listo. 16 avisos: tareas sin formulario de Camunda. Queda resuelto el pendiente «no se volvió a correr `bpmnlint`» de `revision-camunda.md` |
| `14-mvp/proceso-mvp-v01.bpmn` | **MVP (nuevo)** | **0** | Ver la sección 3 |
| `bpmn/liquidacion_cargas_*_mba.bpmn` | Ejemplo del kit (otro proceso, SDP) | 0 | No es de este proceso; no se modifica |
| `contexto/BPMN_REFERENCIA_COMPLEJO_ASIS.xml`, `ejemplos/**` | Referencia y ejemplos del kit | — | No se modifican (material docente) |

**Avisos comunes, ninguno bloquea el despliegue:**
- **«Tarea sin formulario de Camunda»:** las tareas se completan desde la app (Lovable o FastAPI), no desde Tasklist.
- **«Uniones implícitas» (`fake-join`):** varias flechas llegan a una misma tarea sin una compuerta que las una. Camunda lo acepta; es una mejora de estilo para una versión futura.

**Detalle menor del v03:** el nombre de la colaboración dice «TO-BE PROPUESTA v02». Corregirlo en una v04 si se hace otra versión.
