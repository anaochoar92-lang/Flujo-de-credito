# Revisión en Camunda Modeler — TO-BE v01, v02 y v03

## Cambios v03 (ronda 14) — versión vigente
**Archivos:** `proceso-to-be-v03.bpmn` · `validacion-to-be-v03.json` → **0 errores, 6 advertencias**: las 2 de siempre más 4 del mismo falso positivo (`TB_END_REC`, `TB_ACT_LLAMAR`, `TB_END_LLAM` y la tarea de recordatorio solo se alcanzan desde eventos de tiempo). Se creó copiando la v02 (Camunda 8.10) y **agregando** elementos; la v02 no se modificó. No se volvió a correr `bpmnlint` de Camunda.
| Cambio | Elemento | Fuente |
|---|---|---|
| Recordatorio por correo los días hábiles 3 y 6 (temporizador **que no interrumpe** el subproceso, `R2/P4D` [PROPUESTA TÉCNICA]) | `TMR_REC` → `TB_SND_RECORDAR` (tipo `enviar-correo-recordatorio`) → `TB_END_REC` | REQ-TOBE-017 |
| Día hábil 8: el Analista llama al cliente (`P11D` [PROPUESTA TÉCNICA]) | `TMR_LLAM` → `TB_ACT_LLAMAR` → `TB_END_LLAM`; mensaje `MF_Llamada` al cliente | REQ-TOBE-018 |
| Lista de documentos al crear la solicitud | `ACT_001` (nombre y documentación) | REQ-TOBE-019 |
| Carga asistida en el stand | `CL_CARGAR` (nombre y documentación) | PROC-TOBE-005 |

Por revisar en Camunda: que `R2/P4D` y `P11D` se aproximen bien a días hábiles (mismo criterio que `P14D`) y que IT atienda el tipo de trabajo nuevo `enviar-correo-recordatorio`.

---


## Cambios v02 (ronda 8) — versión vigente
**Archivos:** `proceso-to-be-v02.bpmn` · `modelo-v02.json` · `validacion-to-be-v02.json` → **0 errores, 12 advertencias** (las mismas de la v01). La v01 se conserva.
| Cambio | Elemento | Fuente |
|---|---|---|
| Se quita la marca [SUPUESTO] del paso a la ruta en papel | `F_T08` «5 intentos agotados en un documento» | AS-T1 |
| Los intentos se cuentan por documento | `F_T06` «Rechazado (menos de 5 intentos del documento)» | TB-6 |
| «Dudoso» significa que los datos no coinciden | `F_T07` «Dudoso: datos no coinciden» | TB-7 |
| **Nuevo temporizador** de 10 días hábiles sobre la corrección pedida por Despacho (el conteo se reinicia) | `TMR_T02` en `TB_ACT_PEDIR` → `SVC_001` | TB-5 |
| El cierre por vencimiento pasa a evento final de **terminación**, para que también cierre la rama paralela del mensajero | `END_VENCIDA` | TB-5 (consecuencia del modelo) |

Con `TMR_T02` se resuelve el riesgo del punto 6 de la lista (la unión ya no puede esperar sin fin). El punto 8 ya no tiene supuestos.

---

## Versión v01

> **Propuesta, no aprobada.** El diagrama es descriptivo: **no es ejecutable** sin configuración de Camunda (condiciones, expresiones de tiempo, conectores de correo y portal) y sin validaciones formales adicionales.

**Archivo:** `08-tobe/proceso-to-be-v01.bpmn` · **Modelo:** `08-tobe/modelo-v01.json` · **Fecha:** 2026-10-24
**Generado con:** `scripts/crear_bpmn.js` · **Validado con:** `scripts/validar_bpmn.js` → **0 errores, 12 advertencias** (`validacion-to-be-v01.json`). El AS-IS (`05-bpmn/proceso-v02.bpmn`) no se modificó.

## 1. Contenido
- **2 pools:** Cliente (4 nodos) y Banco (43 nodos, 7 carriles). **6 flujos de mensaje** entre los dos.
- **Carriles nuevos:** «Sistema / portal (IT del banco)» y «Mensajero certificado».
- **Ruta digital (nueva):** `TB_SND_ENLACE` → `TB_RCV_DOCS` → `TB_SVC_VALIDAR` → `TB_GW_VALIDO` → `TB_GW_SPLIT` (paralelo) → [Despacho verifica ‖ mensajero recoge y Legal escanea] → `TB_GW_JOIN` → `TB_GW_MERGE` → `ACT_009`.
- **Ruta de respaldo (TB-4):** la del AS-IS v02 sin cambios, desde `ACT_006` hasta `GW_006`, y se une en `TB_GW_MERGE`.

## 2. Advertencias del validador
| Advertencia | Lectura |
|---|---|
| 10 gateways sin condiciones formales | Esperado en un modelo descriptivo. Las reglas están en los nombres de los flujos y en `requisitos-ears-to-be.md` |
| `SVC_001` y `END_VENCIDA` «no alcanzables» | Falso positivo, igual que en el AS-IS: se llega a ellos desde los temporizadores `TMR_T01` y `TMR_001`, y el validador no recorre los eventos límite |

## 3. Ajustes de dibujo
- `ERR_T01` se movió 60 px a la izquierda porque caía encima de `TMR_T01` (los dos están sobre `TB_RCV_DOCS`).
- Se comprobó por código que **no hay cajas solapadas**.
- Hay **líneas que pasan sobre cajas ajenas**, sobre todo los retornos largos de la ruta de respaldo (`F_024`, `F_T12`), la salida de la verificación hacia la unión (`F_T18`, `F_023`) y los flujos de mensaje verticales. Se ajustan a mano en Camunda; si se edita el dibujo, **guardar como `proceso-to-be-v02.bpmn`**.

## 4. Lista de revisión (paso 5 del skill)
| # | Qué comprobar | Dónde | Estado |
|---|---|---|---|
| 1 | Cada nodo queda dentro de su pool y carril | Todo el diagrama | Por revisar |
| 2 | Los flujos de mensaje van **solo** entre pools (Cliente ↔ Banco) | `MF_*` | Por revisar |
| 3 | Temporizador `TMR_T01`: falta la expresión de 10 días hábiles (calendario laboral) | `TB_RCV_DOCS` | Pendiente de configuración |
| 4 | Error `ERR_T01` (portal caído o cliente sin acceso) lleva a la ruta de respaldo | `TB_RCV_DOCS` → `ACT_006` | Por revisar. Lo detecta y registra **IT** (TB-9) |
| 5 | Eventos finales: desembolsado, rechazos (3), cliente no acepta, vencida | 5 fines en Banco, 1 en Cliente | Por revisar |
| 6 | **Paralelo:** `TB_GW_SPLIT` abre dos ramas y `TB_GW_JOIN` las cierra; ninguna rama sale sin volver | Ramas Despacho y mensajero | Por revisar. Riesgo: si `TB_GW_VERIF` → `TB_ACT_PEDIR` se repite sin fin, la unión espera indefinidamente (ver TB-5) |
| 7 | **Merge exclusivo** `TB_GW_MERGE`: solo una ruta (digital o respaldo) llega por solicitud | Antes de `ACT_009` | Por revisar |
| 8 | Ruta manual ante fallo: 5 intentos agotados, portal caído y recogida fallida | `F_T08`, `ERR_T01`, `F_T24` | `F_T08` es **[SUPUESTO AS-T1]** |
| 9 | Tareas que **no** se automatizan: revisar dudoso (Legal), verificar (Despacho), recoger (mensajero), escanear (Legal), desembolsar | Tareas de usuario y manuales | Por revisar |
| 10 | El conteo de 10 días hábiles no se duplica entre `TMR_T01` y `TMR_001` cuando una solicitud pasa a la ruta de respaldo | Ambos temporizadores | [PENDIENTE: ¿se reinicia o sigue el mismo conteo?] |

## 5. Caminos para comparar con un experto (condición de aprobado)
| Camino | Recorrido |
|---|---|
| Feliz | Acepta → correo → carga → válidos → (verifica OK ‖ recogida → escaneo) → unión → desembolso |
| Excepción: documento rechazado | `TB_GW_VALIDO` → pedir nueva carga → hasta 5 intentos |
| Excepción: dudoso | `TB_GW_VALIDO` → Legal revisa → acepta (sigue) o pide nueva carga |
| Excepción: recogida fallida | `TB_GW_RECOGIDA` → Legal recopila los originales → escaneo |
| Contingencia | Portal caído o 5 intentos agotados → ruta AS-IS en papel |
| Timeout | 10 días hábiles sin documentos válidos → cierre automático |

## 6. Cómo abrirlo
Camunda Desktop Modeler → *File → Open File…* → `trabajos/mi-proceso/08-tobe/proceso-to-be-v01.bpmn`.

## 7. v02 preparada para Camunda 8.10 — 2026-10-24
`proceso-to-be-v02.bpmn` se modificó **en su lugar** para desplegarlo en Camunda 8.10, con el ID `Process_Credito_TOBE`. Además de la configuración técnica, tiene tres cambios de diseño aprobados:
- **Subproceso `SUB_T01`** «Recibir y validar documentos en el portal». Ahora el plazo `TMR_T01` corre una sola vez desde el envío del enlace (TB-1). A la salida, la decisión `TB_GW_CARGA` manda los casos con intentos agotados a la ruta en papel.
- **`ERR_T01` cambió a `MSG_T01`**: la falla del portal la reporta IT por mensaje (TB-9).
- **`TB_ACT_RECOGER`** pasó de tarea manual a tarea de usuario, para que el mensajero registre `recogidaLograda`.

`proceso-to-be-v01.bpmn` solo se marcó como diagrama de Camunda 8.10. Detalle completo: `06-revision/despliegue-camunda-8.10.md`. **No regenerar desde `modelo-v02.json`.**
