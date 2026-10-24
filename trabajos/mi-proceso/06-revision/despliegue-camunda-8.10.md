# Despliegue en Camunda 8.10 — AS-IS v02 y TO-BE v02

**Fecha:** 2026-10-24 · **Archivos:** `05-bpmn/proceso-v02.bpmn` (AS-IS) y `08-tobe/proceso-to-be-v02.bpmn` (TO-BE).
Las v01 solo se marcaron como diagramas de Camunda 8.10 y **no** se pueden desplegar. Se conservan como historial.

> Los nombres de variables, las condiciones FEEL, los tipos de trabajo y los mensajes son **[PROPUESTA TÉCNICA]**: los asumimos para poder desplegar y se ajustan después con IT. No son decisiones del dueño del proceso.

## 1. Qué se cambió
| Ajuste | AS-IS v02 | TO-BE v02 |
|---|---|---|
| Plataforma Camunda 8.10 (`modeler:executionPlatformVersion="8.10.0"`) | ✔ | ✔ |
| Proceso ejecutable (`isExecutable="true"`). El pool Cliente queda no ejecutable | ✔ | ✔ |
| ID del proceso propio, para que el TO-BE no se despliegue como versión nueva del AS-IS | `Process_Credito_ASIS` | `Process_Credito_TOBE` |
| Tareas de usuario de Camunda (`zeebe:userTask`) | 9 | 15 |
| Condiciones FEEL en las salidas de las decisiones | 13 salidas | 24 salidas + 1 por defecto |
| Temporizadores con `P14D` (10 días hábiles ≈ 14 días calendario, aproximación aprobada) | `TMR_001` | `TMR_001`, `TMR_T01`, `TMR_T02` |
| Tipos de trabajo en las tareas de servicio y de envío | 1 | 5 |
| Mensajes con clave de correlación `=solicitudId` | — | 2 |

### Cambios de diseño del TO-BE (aprobados el 2026-10-24)
- **B1 · Falla del portal:** el evento de error `ERR_T01` se cambió por el evento de mensaje `MSG_T01` «IT reporta falla del portal o cliente sin acceso». Una tarea de recepción no puede lanzar errores; según TB-9, quien detecta la falla es IT. El caso sigue yendo a la ruta en papel (`ACT_006`).
- **B2 · Plazo de 10 días que no se reinicia:** la carga, la validación, la corrección y la revisión de Legal quedaron dentro del subproceso `SUB_T01` «Recibir y validar documentos en el portal». El temporizador `TMR_T01` y el mensaje `MSG_T01` cuelgan del subproceso. Así el plazo corre desde el envío del enlace y no vuelve a empezar con cada carga (TB-1).
  - A la salida del subproceso hay una nueva decisión, `TB_GW_CARGA` «¿Resultado de la carga?». Si `resultadoValidacion = "agotado"`, el caso va a la ruta en papel. En cualquier otro caso (salida por defecto) va a la verificación y la recogida.
  - «Revisar documento dudoso (Legal)» quedó dentro del subproceso, en el carril Sistema. Por eso su nombre ahora indica que la hace Legal.
- `TB_ACT_RECOGER` «Recoger originales a domicilio» pasó de tarea manual a **tarea de usuario**. En Camunda una tarea manual no registra datos, y la decisión `TB_GW_RECOGIDA` necesita que el mensajero reporte `recogidaLograda`.

## 2. Variables que mueven las decisiones
Quien completa cada tarea debe registrar la variable correspondiente. Sin formularios, se agrega como variable desde Tasklist.

| Variable | Valores | La registra | Decisión |
|---|---|---|---|
| `solicitudId` | texto | Al iniciar la instancia | Clave de correlación de los mensajes (solo TO-BE) |
| `resultadoRiesgo` | `"apto"`, `"corregir"`, `"rechazar"` | `ACT_002` Evaluar solicitud | `GW_001` |
| `decisionAnalisis` | `"aprobar"`, `"rechazar"` | `ACT_003` Analizar crédito | `GW_002` |
| `clienteAcepta` | `true` / `false` | `ACT_004` Informar decisión | `GW_003` |
| `conCondiciones` | `true` / `false` | `ACT_003` o `ACT_004` | `GW_004` |
| `documentacionCompleta` | `true` / `false` | `ACT_006` Recopilar expediente | `GW_005` |
| `documentacionOk` | `true` / `false` | `ACT_008` Verificar y autorizar | `GW_006` |
| `resultadoValidacion` | `"valido"`, `"rechazado"`, `"dudoso"`, `"agotado"` | Trabajo `validar-documentos` (lleva la cuenta de los 5 intentos por documento) | `TB_GW_VALIDO`, `TB_GW_CARGA` |
| `legalAcepta` | `true` / `false` | `TB_ACT_REVISAR` | `TB_GW_LEGAL` |
| `expedienteOk` | `true` / `false` | `TB_ACT_VERIF` | `TB_GW_VERIF` |
| `recogidaLograda` | `true` / `false` | `TB_ACT_RECOGER` Recoger originales (mensajero) | `TB_GW_RECOGIDA` |

Si falta la variable al llegar a una decisión, Camunda crea un **incidente** en Operate. Es intencional: así se ve qué dato no se registró.

## 3. Tipos de trabajo (los atiende un job worker o un conector que define IT)
| Tarea | Tipo |
|---|---|
| `SVC_001` Cerrar solicitud automáticamente | `cerrar-solicitud` |
| `TB_SVC_VALIDAR` Validar documentos | `validar-documentos` |
| `TB_SND_ENLACE` Enviar enlace al portal por correo | `enviar-correo-enlace` |
| `TB_SND_CORREGIR` Pedir al cliente que vuelva a cargar | `enviar-correo-correccion` |
| `TB_SND_RECOGIDA` Programar recogida y avisar al cliente | `programar-recogida` |

Mientras no haya un programa atendiendo un tipo, la instancia se queda esperando en esa tarea. No se configuraron conectores de correo, credenciales ni direcciones de servidores (regla de AGENTS.md).

## 4. Mensajes que publica el portal o IT (solo TO-BE)
| Mensaje (`name`) | Lo espera | Clave |
|---|---|---|
| `documentos-cargados` | `TB_RCV_DOCS` Recibir documentos cargados | `=solicitudId` |
| `falla-portal-reportada` | `MSG_T01`, sobre el subproceso `SUB_T01` | `=solicitudId` |

## 5. Verificación realizada
- `scripts/validar_bpmn.py`: **0 errores** en los dos archivos. Las 2 advertencias que quedan son el falso positivo conocido de `SVC_001` y `END_VENCIDA`, a los que solo se llega desde los temporizadores.
- Reglas de Camunda Modeler para 8.10 (`bpmnlint-plugin-camunda-compat`, configuración `camunda-cloud-8-10`, con las extensiones Zeebe cargadas): **0 errores**. Hay 9 advertencias en el AS-IS y 15 en el TO-BE; todas dicen que las tareas de usuario no tienen formulario.
- Dibujo del TO-BE: no hay cajas encimadas. Las líneas que cruzan cajas son las mismas que ya estaban anotadas en `08-tobe/revision-camunda.md`; ninguna toca los elementos nuevos.
- **No se probó un despliegue real** contra un motor Camunda 8.10. El primer despliegue en el clúster es la prueba final.

## 6. Pendiente
- Que IT confirme o cambie los nombres técnicos de las secciones 2 a 4.
- Si se quiere usar Tasklist con comodidad: formularios para las decisiones.
- Reemplazar `P14D` por una fecha calculada con festivos si se necesita exactitud en días hábiles.
- **Reconciliar el JSON:** `04-modelo/especificacion-v02.json` y `08-tobe/modelo-v02.json` ya no coinciden con el XML, y el generador del kit no maneja extensiones Zeebe ni subprocesos. **No regenerar los BPMN desde esos JSON**: se perderían estos cambios.
