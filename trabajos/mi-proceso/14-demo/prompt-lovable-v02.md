# Prompt para Lovable — Demo del flujo de crédito Expomóvil sobre Camunda 8.10 + Portal MVP

**Fecha:** 2026-10-27 · **Estado:** borrador v02 (reemplaza a `prompt-lovable.md`, v01, que se conserva sin cambios).
**Base:** `05-bpmn/proceso-v02.bpmn` (AS-IS), `08-tobe/proceso-to-be-v03.bpmn` (TO-BE vigente), `06-revision/despliegue-camunda-8.10.md` y `14-mvp/` (`alcance-equipo.md`, `ears-equipo.md`, `modelo-equipo.md`, `entrega-paso23-david-sergio.md`).
**Datos:** todo es **SINTÉTICO / DEMOSTRACIÓN**. **Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio). Lo que genere la app no se mezcla con `09-datos/`.

## Qué cambió respecto a la v01
| # | Cambio | Fuente |
|---|---|---|
| 1 | La app tiene **dos módulos**: (A) demo AS-IS vs TO-BE sobre Camunda real y (B) **Portal MVP** del tramo de documentos, que funciona sin Camunda | Decisión del 2026-10-27 (pregunta 1 = c) |
| 2 | El TO-BE desplegado es el **v03**: tipo de trabajo nuevo `enviar-correo-recordatorio`, tarea nueva `TB_ACT_LLAMAR`, temporizadores `R2/P4D` y `P11D`, y nombres de tareas actualizados | `08-tobe/revision-camunda.md` (ronda 14); decisión del 2026-10-27 (pregunta 2) |
| 3 | Formulario con **alias, correo y monto** (sin nombre, cédula, salario ni concesionario) e ID **`SOL-9NNNN`** al azar entre SOL-90000 y SOL-99999 | FE-1 (ronda 19), DAT-1 (ronda 18); decisión del 2026-10-27 (pregunta 3) |
| 4 | Validación **por documento** (4 documentos, 20 días calendario, legibilidad marcada por una persona, 5 intentos por documento, se vuelve a subir solo el rechazado) y botón **«Llenar ejemplo dudoso»** | REQ-MVP-01 a 03, DAT-2, FE-2, FE-3 |
| 5 | **Bitácora exportable a CSV** marcada `SINTETICO` (casos, documentos y eventos) para Preset | REQ-MVP-03, DAT-3; decisión del 2026-10-27 (pregunta 4) |

## Antes de usarlo
1. **Revisar y desplegar los dos BPMN** en el clúster de Camunda 8.10 desde Camunda Modeler (*Deploy*): `05-bpmn/proceso-v02.bpmn` y `08-tobe/proceso-to-be-v03.bpmn`.
   - **Al v03 no se le volvió a correr la revisión de Camunda (`bpmnlint`).** Antes de desplegar, abrirlo en Modeler y comprobar que el panel *Problems* no muestre errores. `despliegue-camunda-8.10.md` describe la v02; el v03 la copia y le **agrega** elementos, así que hereda esa configuración.
   - El v03 usa el mismo ID de proceso (`Process_Credito_TOBE`): Camunda lo registra como **versión nueva** y la app usará siempre la última.
2. **Camunda corre en SaaS** (decidido el 2026-10-24). El *API client* ya está creado. Tener a mano su archivo de credenciales; de ahí salen:
   - el **client id** y el **client secret**;
   - la **URL del token** y el **audience**;
   - el **cluster id** y la **región**.

   **Dirección REST:** en Camunda 8.10 los dominios `…zeebe.camunda.io` responden 404. La dirección se arma así: `https://{CAMUNDA_CLUSTER_REGION}.api.camunda.io/{CAMUNDA_CLUSTER_ID}`. También se copia de la consola: *Clusters → (el clúster) → API → Connection information → «Camunda REST API»*.

   El clúster tiene las *authorizations* activadas: sin permisos explícitos responde **403 FORBIDDEN** (confirmado el 2026-10-24). En *Admin* del clúster → *Authorizations*, con *Owner type* = Client y *Owner ID* = client id:
   - `RESOURCE` (`*`): `CREATE` y `READ`;
   - `PROCESS_DEFINITION` (`*`, o `Process_Credito_ASIS` y `Process_Credito_TOBE`): `READ_PROCESS_DEFINITION`, `CREATE_PROCESS_INSTANCE`, `READ_PROCESS_INSTANCE`, `UPDATE_PROCESS_INSTANCE`, `READ_USER_TASK` y `UPDATE_USER_TASK`;
   - `MESSAGE` (`*`): `CREATE` y `READ`.

   Alternativa rápida para la demo: asignar el client al rol `admin`.
3. **Credenciales:** cuando Lovable pida los *secrets*, cargarlos directamente en Supabase. **Nunca pegarlos en el prompt, en el chat de Lovable ni en el código.**
4. **Datos:** solo **datos sintéticos** (AGENTS.md). No cargar clientes reales. Si algún día entra un caso real, el CSV para Preset debe excluir `correo_cliente`, `cliente_alias` y los campos `*_declarado` (riesgo aceptado en la ronda 18, AGENTS.md regla 7).
5. **Pegar en Lovable** el bloque de la sección siguiente, completo.

---

## Prompt (copiar desde aquí)

Construye una aplicación web en **español** llamada **«Demo Crédito Expomóvil — AS-IS vs TO-BE»**. Tiene dos módulos, accesibles desde un menú lateral:

- **Módulo A — Demo en Camunda:** muestra cómo avanzan dos procesos BPMN ya desplegados en **Camunda 8.10**, el actual (AS-IS) y el propuesto (TO-BE). Permite iniciar casos, completar las tareas humanas de cada rol, simular las tareas automáticas y los mensajes del portal, y ver en qué paso va cada caso.
- **Módulo B — Portal MVP (sin Camunda):** implementa con reglas reales solo el tramo del portal de documentos: el cliente carga 4 documentos, el sistema los valida, Legal revisa los casos dudosos y Despacho verifica el expediente. Guarda todo en Supabase y exporta la bitácora a CSV.

Aviso fijo en todas las pantallas: **«SINTÉTICO / DEMOSTRACIÓN — no usar datos reales»**.

### 1. Arquitectura y seguridad
- Frontend: React + TypeScript + Tailwind + shadcn/ui.
- **No hay login.** Es una demo; el usuario elige su rol en un selector.
- El navegador **nunca** llama a Camunda ni a las tablas directamente. Todo pasa por dos **Supabase Edge Functions**:
  - `camunda-proxy` para el módulo A;
  - `portal-mvp` para el módulo B y para el registro de IDs del módulo A.
- Las tablas de Supabase tienen **RLS activado y ninguna política para `anon`**. Solo las Edge Functions las leen y escriben, con la *service role key*, que nunca llega al navegador.

#### 1.1 Conexión con Camunda (`camunda-proxy`)
- Camunda corre en **Camunda 8 SaaS**. Pídeme estos secrets de Supabase y no los pongas en el código:
  - `CAMUNDA_REST_ADDRESS`: dirección REST del clúster, sin `/v2` al final. En Camunda 8.10 el formato es `https://{region}.api.camunda.io/{clusterId}`, con el subdominio **`api`**. **No uses el formato antiguo `{region}.zeebe.camunda.io`**: en 8.10 responde 404.
  - `CAMUNDA_CLIENT_ID` y `CAMUNDA_CLIENT_SECRET`.
  - `CAMUNDA_OAUTH_URL`: el valor que trae el archivo de credenciales.
  - `CAMUNDA_TOKEN_AUDIENCE`: el valor que trae el archivo de credenciales (`ZEEBE_TOKEN_AUDIENCE` o `CAMUNDA_TOKEN_AUDIENCE`).
- La función obtiene el token OAuth 2.0 con *client credentials* (`grant_type=client_credentials`, `client_id`, `client_secret`, `audience`). Lo guarda en memoria hasta poco antes de que venza y lo envía como `Authorization: Bearer …`. Si Camunda responde 401, pide un token nuevo y reintenta una sola vez.
- Expone solo operaciones concretas (lista blanca), no un proxy abierto: `topology`, `startInstance`, `searchInstances`, `getInstance`, `searchUserTasks`, `completeUserTask`, `activateJobs`, `completeJob`, `publishMessage`, `searchIncidents`, `searchVariables`, `searchElementInstances`, `searchProcessDefinitions`.
- Usa la **Orchestration Cluster REST API v2** de Camunda 8.10: `POST /v2/process-instances`, `POST /v2/process-instances/search`, `POST /v2/user-tasks/search`, `POST /v2/user-tasks/{userTaskKey}/completion`, `POST /v2/jobs/activation`, `POST /v2/jobs/{jobKey}/completion`, `POST /v2/messages/publication`, `POST /v2/incidents/search`, `POST /v2/variables/search`, `POST /v2/element-instances/search`, `POST /v2/process-definitions/search` y `GET /v2/topology`. **Verifica los nombres exactos de rutas y campos en la documentación oficial de Camunda 8.10** antes de implementarlos y ajústalos si difieren. En la documentación las rutas aparecen sin el prefijo `/v2` (por ejemplo `POST /process-instances`), porque es parte de la URL base. Los esquemas de cada cuerpo están en *Orchestration Cluster API → Try with Swagger*. Al crear una instancia, identifica el proceso por su ID BPMN (`Process_Credito_ASIS` / `Process_Credito_TOBE`) sin versión, para que Camunda use la última versión desplegada.
- Muestra los errores en español y en lenguaje claro, por ejemplo: «No hay conexión con Camunda» o «La tarea ya fue completada por otra persona». Si Camunda responde **403**: «El API client no tiene permiso para esta acción; revisar sus permisos en la consola de Camunda».

#### 1.2 Identificador de la solicitud (los dos módulos)
- Formato **`SOL-9NNNN`**: «SOL-» seguido de un número al azar entre **90000 y 99999**. Antes de usarlo, verifica que no exista en `cred_casos` ni en `demo_casos_camunda`; si existe, genera otro.
- Este rango no choca con los datos sintéticos del tablero (SOL-00001 a SOL-08000). No uses otro formato.

#### 1.3 Tablas de Supabase
Crea estas tablas (nombres y valores exactamente así):

**`demo_casos_camunda`** (módulo A): `id` (PK), `id_solicitud`, `proceso` (`AS-IS` / `TO-BE`), `instance_key`, `gemelo` (bool), `cliente_alias`, `correo_cliente`, `monto`, `fuente_datos` (siempre `SINTETICO`), `creado_en`. Única por (`id_solicitud`, `proceso`): un caso gemelo usa el **mismo** `id_solicitud` en los dos procesos.

**`cred_casos`** (módulo B): `id` (PK), `id_solicitud` (único), `bpmn_id` (`Process_Credito_TOBE`), `instance_key` (siempre nulo en este módulo), `cliente_alias`, `correo_cliente`, `monto`, `estado`, `caso_dudoso` (bool), `decision_legal` (`ACEPTA` / `RECHAZA` / nulo), `resultado_despacho` (`OK` / `CORREGIR` / nulo), `etapa` (entero, sube en cada cambio de estado), `fuente_datos` (siempre `SINTETICO`), `creado_en` (envío del enlace), `verificado_en`, `cerrado_en`.
Valores de `estado`: `ENLACE_ENVIADO`, `DOCUMENTOS_RECHAZADOS`, `REVISION_LEGAL`, `VERIFICACION_DESPACHO`, `ESPERANDO_CORRECCION`, `VERIFICADO`, `RUTA_PAPEL`.

**`cred_documentos`** (módulo B, una fila por tipo y caso): `id` (PK), `caso_id` (FK), `tipo` (`IDENTIDAD` / `INGRESOS` / `ESTADO_CUENTA` / `PAGARE`), `fecha_expedicion`, `legible` (bool), `intentos` (0 a 5), `estado` (`PENDIENTE` / `VALIDO` / `RECHAZADO` / `AGOTADO`), `motivo_rechazo`, `nombre_declarado`, `cedula_declarada`, `salario_declarado`, `monto_declarado`, `cargado_en`.

**`cred_eventos`** (módulo B): `id` (PK), `caso_id` (FK), `momento`, `accion`, `tarea` (elementId BPMN), `actor` (`cliente` / `legal` / `despacho` / `sistema`), `detalles` (JSON).

Zona horaria para fechas y días: **America/Santo_Domingo**.

### 2. Los dos procesos (módulo A)
| Proceso | `processDefinitionId` | Versión del archivo |
|---|---|---|
| AS-IS (actual) | `Process_Credito_ASIS` | `proceso-v02.bpmn` |
| TO-BE (propuesto) | `Process_Credito_TOBE` | `proceso-to-be-v03.bpmn` |

### 3. Módulo A — Pantallas

**3.1 Conexión.** Muestra el estado con `GET /v2/topology` (verde o rojo), la versión del clúster y si `Process_Credito_ASIS` y `Process_Credito_TOBE` están desplegados (`POST /v2/process-definitions/search`), con el número de versión. Si falta alguno: «Despliega el BPMN desde Camunda Modeler».

**3.2 Nuevo caso.** Formulario: proceso (AS-IS / TO-BE), **alias del cliente** (mínimo 2 caracteres), **correo** (formato válido) y **monto solicitado** (mayor que 0). Botón «Generar datos de ejemplo» que llena valores sintéticos (correo con dominio `@ejemplo.test`).
- Genera el `solicitudId` según 1.2 y lo registra en `demo_casos_camunda` con el `instance_key` devuelto.
- Inicia la instancia con estas variables: `solicitudId`, `cliente` (objeto `{ alias, correo, monto }`), `proceso` (`"AS-IS"` o `"TO-BE"`) y `fechaInicioDemo`.
- Opción «Crear caso gemelo»: inicia el mismo cliente, con el mismo `solicitudId`, en los dos procesos a la vez, para compararlos.

**3.3 Casos.** Tabla de instancias activas y terminadas de los dos procesos, con estas columnas: `solicitudId`, alias, proceso, estado, **paso actual** (elementos activos, con su nombre legible) e incidentes (badge rojo). Filtros por proceso y estado.

**3.4 Detalle del caso.** Muestra:
- una línea de tiempo con los pasos recorridos (element instances con fechas);
- las variables actuales;
- los incidentes, con su mensaje explicado en español (ver 3.8);
- botones contextuales según el paso: completar la tarea, simular la tarea automática o enviar un mensaje.
- Opcional, si es sencillo: el diagrama con bpmn-js (`NavigatedViewer`), resaltando los elementos activos. Carga los XML desde `public/bpmn/` (`proceso-v02.bpmn` y `proceso-to-be-v03.bpmn`); yo subiré los archivos.

**3.5 Bandeja de tareas por rol.** Un selector de rol filtra las tareas de usuario pendientes (`POST /v2/user-tasks/search`, estado `CREATED`). Cada tarea abre un formulario. Al enviarlo, la tarea se completa con las variables de la sección 4. Si la tarea no pide variables, muestra solo un botón «Marcar como hecha». Si un rol no tiene tareas, la bandeja queda vacía, sin mensaje.

**3.6 Tareas automáticas y portal (simulador).** Este panel reemplaza a los sistemas que todavía no existen.
- **Tareas automáticas:** para cada tipo de trabajo de la sección 5, un botón «Buscar y ejecutar» activa los trabajos pendientes de ese tipo (`POST /v2/jobs/activation`, `worker: "demo-lovable"`, timeout de 60 s). Muestra cada trabajo con su `solicitudId` y deja elegir el resultado antes de completarlo.
- **Ayuda para `validar-documentos`:** además del selector manual, un botón **«Proponer con las reglas del portal»** abre el formulario de 4 documentos del módulo B (sección 6.3), aplica las mismas reglas **sin guardar nada** y preselecciona el resultado: todos válidos y datos iguales → `"valido"`; algún rechazo → `"rechazado"`; todos válidos pero datos distintos → `"dudoso"`. `"agotado"` (5 intentos fallidos en un documento) se elige a mano. La persona confirma antes de completar el trabajo.
- **Portal del cliente (solo TO-BE):** para cada caso que espera documentos:
  - botón «El cliente cargó documentos»: publica el mensaje `documentos-cargados` con `correlationKey = solicitudId`;
  - botón «IT reporta falla del portal»: publica `falla-portal-reportada`, con la misma clave.
- Interruptor «Modo automático»: cada 10 s ejecuta los trabajos pendientes con el resultado «camino feliz».

**3.7 Comparación AS-IS vs TO-BE.** Para los casos terminados muestra:
- número de pasos humanos;
- número de devoluciones o correcciones;
- duración de la demo;
- ruta final (desembolsado, rechazado, no acepta, vencido, ruta en papel).

En los casos gemelos los muestra lado a lado. Nota: «La duración de la demo no representa días reales; los tiempos reales del proceso están en el diagnóstico.»

**3.8 Incidentes.** Si falta una variable, Camunda crea un incidente. Muestra cuál variable falta según la decisión donde quedó detenido el caso (sección 4).

### 4. Módulo A — Tareas de usuario: rol, formulario y variables
Identifica cada tarea por su `elementId`. Los valores de las variables deben coincidir **exactamente**; si no, el proceso cae en un incidente.

| `elementId` | Nombre | Rol | Proceso | Campos del formulario → variables |
|---|---|---|---|---|
| `ACT_001` | Crear solicitud y entregar lista de los 4 documentos (en el AS-IS: Crear solicitud) | Persona de Negocio | Ambos | Ninguno (solo confirmar). En el TO-BE, muestra la lista: cédula, comprobante de ingresos, estado de cuenta y pagaré |
| `ACT_002` | Evaluar solicitud | Persona de Riesgo | Ambos | Radio `resultadoRiesgo`: `"apto"`, `"corregir"`, `"rechazar"` |
| `ACT_003` | Analizar crédito | Analista de crédito (Despacho) | Ambos | Radio `decisionAnalisis`: `"aprobar"`, `"rechazar"`. Si aprueba: casilla `conCondiciones` (`true`/`false`). Si rechaza, enviar `conCondiciones: false` |
| `ACT_004` | Informar decisión al cliente | Analista de crédito (Despacho) | Ambos | Radio `clienteAcepta`: `true` / `false` |
| `ACT_005` | Modificar datos del crédito | Persona de Negocio | Ambos | Ninguno (opcional: editar el monto en `cliente.monto`) |
| `ACT_006` | Recopilar expediente en papel (ruta de respaldo) (en el AS-IS: Recopilar expediente) | Legal | Ambos | Radio `documentacionCompleta`: `true` / `false` |
| `ACT_007` | Escanear documentación | Legal | Ambos | Ninguno |
| `ACT_008` | Verificar y autorizar expediente (Despacho) | Analista de crédito (Despacho) | Ambos | Radio `documentacionOk`: `true` / `false` |
| `ACT_009` | Desembolsar crédito y gestionar post-desembolso (en el AS-IS: Desembolsar crédito) | Desembolso | Ambos | Ninguno |
| `TB_ACT_REVISAR` | Revisar documento dudoso (Legal) | Legal | TO-BE | Radio `legalAcepta`: `true` / `false` |
| `TB_ACT_VERIF` | Verificar expediente digital (Despacho) | Analista de crédito (Despacho) | TO-BE | Radio `expedienteOk`: `true` / `false` |
| `TB_ACT_PEDIR` | Pedir documento corregido al cliente | Analista de crédito (Despacho) | TO-BE | Ninguno |
| `TB_ACT_LLAMAR` | Llamar al cliente y enviar último aviso | Analista de crédito (Despacho) | TO-BE | Ninguno (opcional: campo de nota, solo para mostrar en pantalla) |
| `TB_ACT_RECOGER` | Recoger originales a domicilio | Mensajero certificado | TO-BE | Radio `recogidaLograda`: `true` / `false` |
| `TB_ACT_RECOP_ORIG` | Recopilar originales por la ruta actual | Legal | TO-BE | Ninguno |
| `TB_ACT_ESCANEAR` | Escanear originales y enviar sobre | Legal | TO-BE | Ninguno |

Muestra el nombre que Camunda devuelva para la tarea; los textos entre paréntesis son solo referencia.

Roles del selector: Persona de Negocio, Persona de Riesgo, Analista de crédito (Despacho), Legal, Mensajero certificado, Desembolso y «Todos» (vista del profesor).

### 5. Módulo A — Tareas automáticas (tipos de trabajo)
| Tipo | Proceso | Resultado que se elige al simular → variables con que se completa |
|---|---|---|
| `cerrar-solicitud` | Ambos | Sin opciones → `{ "cierreAutomatico": true }` |
| `enviar-correo-enlace` | TO-BE | Sin opciones. Muestra una vista previa del correo ficticio con el enlace al portal → `{ "enlaceEnviado": true }` |
| `validar-documentos` | TO-BE | Radio `resultadoValidacion`: `"valido"` (camino feliz), `"rechazado"`, `"dudoso"`, `"agotado"`, o «Proponer con las reglas del portal» (3.6). Ayuda: «rechazado = vencido (más de 20 días calendario desde la expedición), ilegible o falta; dudoso = nombre, cédula, salario o monto no coinciden entre documentos; agotado = 5 intentos fallidos en un mismo documento» |
| `enviar-correo-correccion` | TO-BE | Sin opciones → `{ "correccionSolicitada": true }` |
| `enviar-correo-recordatorio` | TO-BE | Sin opciones. Muestra una vista previa del recordatorio ficticio → `{ "recordatorioEnviado": true }` |
| `programar-recogida` | TO-BE | Fecha de recogida (por defecto, mañana) → `{ "fechaRecogida": "AAAA-MM-DD" }` |

Si un trabajo no se puede completar, muestra el error y no reintentes en bucle.

### 6. Módulo B — Portal MVP (sin Camunda)
Este módulo **no** llama a Camunda. Las tareas humanas no se guardan en una tabla: se **derivan del estado del caso**. Cada paso deja un evento con fecha y hora en `cred_eventos`.

**Inicio y fin del tramo.** Empieza cuando el cliente ya aceptó la decisión y el sistema envía el enlace al portal (`TB_SND_ENLACE`). Termina cuando Despacho verifica el expediente digital (`TB_ACT_VERIF` con resultado OK). Quedan fuera: riesgo, análisis y decisión de crédito; recogida de originales, comisión y desembolso; ruta en papel y temporizadores.

#### 6.1 Operaciones de `portal-mvp` y respuestas
Usa estos códigos HTTP y mensajes; la pantalla los traduce a español claro.

| Operación | Qué hace | Errores |
|---|---|---|
| Crear caso `{cliente_alias, correo_cliente, monto}` | Crea el caso con `id_solicitud` según 1.2 y estado `ENLACE_ENVIADO`, los 4 documentos en `PENDIENTE` (0 intentos), `fuente_datos = SINTETICO` y el evento `ENLACE_ENVIADO` con tarea `TB_SND_ENLACE` y actor `sistema`. El correo **no** se envía: solo queda el evento. Responde 201 | 422 si el correo no es válido, el alias tiene menos de 2 caracteres o el monto es ≤ 0 |
| Cargar documentos `{caso_id, documentos: [ {tipo, fecha_expedicion, legible, nombre?, cedula?, salario?, monto?} ]}` | Aplica las reglas de 6.2 | 200 si quedan los 4 válidos. **422 con el caso y los motivos** si hubo algún rechazo (los intentos sí se guardan). 409 si se reenvía un documento ya válido, si el caso no está esperando documentos o si los intentos están agotados («intentos agotados»). 404 si el caso no existe |
| Listar tareas `{rol: cliente \| legal \| despacho}` | Tareas abiertas: `{key, name, role, elementId, caso_id, id_solicitud}` (ver 6.4) | — |
| Completar tarea `{key, actor, resultado, documento?, observacion?}` | Ver 6.4 | 422 sin resultado, con resultado de otro rol, o `CORREGIR` sin documento. **409 si la clave ya no corresponde a la tarea activa** (doble clic). 404 si el caso no existe |
| Consultar casos, un caso (con sus documentos) y su bitácora | Lectura | 404 |
| Exportar `casos.csv`, `documentos.csv` o `eventos.csv` | CSV con **todas** las columnas de la tabla, incluidos `correo_cliente` y `fuente_datos = SINTETICO` en cada fila | 404 si la tabla no existe |

#### 6.2 Reglas de los documentos (REQ-MVP-01 y 02)
Para cada documento enviado en la carga, revisa en este orden y guarda el **primer** motivo que aplique:
1. `fecha futura`: la fecha de expedición es posterior a hoy.
2. `vencido (> 20 días)`: pasaron **más de 20 días calendario** entre la fecha de expedición y el día de la carga (20 días exactos todavía es válido).
3. `ilegible`: la persona desmarcó la casilla «Legible» (no hay lectura automática).

Los documentos que no se enviaron y que todavía no son válidos se rechazan con el motivo `falta`.

Cada rechazo suma **1 intento a ese documento**. Al llegar a **5 intentos**, el documento queda `AGOTADO` y el caso pasa a `RUTA_PAPEL` (evento con `cerrado_en`). Los documentos válidos se conservan: el cliente vuelve a subir **solo** los rechazados.

Si después de la carga los **4 documentos son válidos**, compara entre documentos el **nombre, la cédula, el salario y el monto**, usando solo los valores que estén presentes:
- algún valor distinto → `caso_dudoso = true` y estado `REVISION_LEGAL`;
- todos iguales → estado `VERIFICACION_DESPACHO`.

Si hubo algún rechazo y no hay documentos agotados → estado `DOCUMENTOS_RECHAZADOS`.

Qué datos pide cada documento en el formulario: **todos** piden tipo, fecha de expedición, casilla «Legible» y nombre; `IDENTIDAD` y `PAGARE` piden además cédula; `INGRESOS` pide salario; `PAGARE` pide monto.

#### 6.3 Pantallas del módulo B
1. **Nueva solicitud:** alias, correo y monto. Al enviarla, queda registrado el envío del enlace.
2. **Cargar documentos (cliente):** elige el caso y muestra **solo los documentos que no están válidos**, con su motivo de rechazo y el número de intentos usados («2 de 5»). Botones:
   - «Llenar ejemplo válido»: 4 documentos legibles, expedidos hace 5 días, con los mismos datos.
   - **«Llenar ejemplo dudoso»**: igual, pero con una **cédula distinta en el pagaré**, para que aparezca la tarea de Legal.
3. **Bandejas de Legal y de Despacho:** tareas abiertas por rol. Si no hay tareas, la bandeja queda vacía, sin mensaje.
4. **Bitácora y CSV:** eventos del caso en orden, con fecha y hora, y tres botones de descarga: casos, documentos y eventos.

#### 6.4 Tareas derivadas del estado y su cierre
| Estado del caso | Tarea abierta | `elementId` | Rol |
|---|---|---|---|
| `ENLACE_ENVIADO`, `DOCUMENTOS_RECHAZADOS`, `ESPERANDO_CORRECCION` | Cargar documentos en el portal | `CL_CARGAR` | cliente |
| `REVISION_LEGAL` | Revisar documento dudoso | `TB_ACT_REVISAR` | legal |
| `VERIFICACION_DESPACHO` | Verificar expediente digital | `TB_ACT_VERIF` | despacho |

- **Clave de la tarea:** `cred-{caso_id}-{rol}-{etapa}`. Como `etapa` sube en cada cambio de estado, una clave vieja ya no coincide y devuelve 409.
- **Legal:** `ACEPTA` → `VERIFICACION_DESPACHO`. `RECHAZA` → `RUTA_PAPEL` (con `cerrado_en`), sin tarea de Despacho.
- **Despacho:** `OK` → `VERIFICADO`, con `verificado_en` y el evento `EXPEDIENTE_VERIFICADO`. `CORREGIR` + `documento` → `ESPERANDO_CORRECCION`; ese documento vuelve a `RECHAZADO` con la observación como motivo, **sin sumar intento**.
- Cada cierre deja un evento con la `accion`, la `tarea`, el `actor` (rol) y los `detalles` (resultado y observación).

#### 6.5 Comprobaciones de aceptación (hazlas funcionar todas)
1. Al crear un caso, su ID empieza por `SOL-9` y tiene 9 caracteres; el estado es `ENLACE_ENVIADO`; hay una tarea `CL_CARGAR` y el primer evento de la bitácora tiene la tarea `TB_SND_ENLACE`.
2. Cuatro documentos válidos con los mismos datos → `VERIFICACION_DESPACHO`, 0 intentos y ninguna tarea de Legal.
3. Pagaré expedido hace 25 días → 422, motivo `vencido (> 20 días)` e intento 1 en el pagaré; los otros quedan `VALIDO`. Reenviar la cédula ya válida → 409. Reenviar un pagaré válido → `VERIFICACION_DESPACHO`.
4. Enviar solo 2 documentos, uno de ellos ilegible → 422, motivo `ilegible` en el ilegible y `falta` (1 intento) en los no enviados.
5. Cinco pagarés vencidos seguidos → pagaré `AGOTADO` y caso `RUTA_PAPEL`; un sexto envío → 409 «intentos agotados».
6. «Llenar ejemplo dudoso» → `REVISION_LEGAL` y ninguna tarea de Despacho. Legal acepta → aparece `TB_ACT_VERIF`; repetir el mismo clic → 409.
7. Legal rechaza → `RUTA_PAPEL` y ninguna tarea de Despacho.
8. Despacho completa sin resultado → 422; con `ACEPTA` → 422; con `OK` → `VERIFICADO`, con `verificado_en`, y el último evento es `EXPEDIENTE_VERIFICADO`. Los 3 CSV se descargan; el de casos incluye la columna `correo_cliente` y el valor `SINTETICO`.
9. Despacho pide `CORREGIR` sin documento → 422; con `INGRESOS` → `ESPERANDO_CORRECCION`, sin `verificado_en`, y reaparece `CL_CARGAR`. Reenviar el comprobante de ingresos → `VERIFICACION_DESPACHO`.
10. Correo no válido o monto 0 → 422. Fecha de expedición futura → motivo `fecha futura`. Caso inexistente → 404.

### 7. Limitaciones que la app debe explicar (en un ícono de ayuda)
- **Módulo A:** los plazos de días hábiles están configurados en días calendario y **no se pueden acelerar desde la app**:
  - 10 días hábiles sin documentos o sin corrección → `P14D`, cierre por vencimiento;
  - recordatorios de los días hábiles 3 y 6 → `R2/P4D`, sin interrumpir la carga;
  - llamada del día hábil 8 → `P11D`, sin interrumpir la carga.

  Por eso los recordatorios, la llamada y los vencimientos no se ven en una demo en vivo.
- **Módulo A:** en el TO-BE, después de «El cliente cargó documentos» hay que ejecutar `validar-documentos` para que el caso avance.
- **Módulos A y B:** cuando Legal **rechaza** un documento dudoso, el módulo A sigue el BPMN v03 (se le pide al cliente que vuelva a cargar) y el módulo B sigue el MVP aprobado (el caso pasa a la ruta en papel). Explícalo así en la ayuda: «Regla pendiente de confirmar; cada módulo sigue su propia fuente».
- **Módulo B:** no tiene temporizadores, recordatorios ni cierre por vencimiento. La legibilidad la marca una persona y el correo se simula.

### 8. Estilo
- Interfaz limpia y profesional, con colores sobrios de banca.
- **AS-IS en gris azulado y TO-BE en verde**, de forma consistente en toda la app. El módulo B usa el verde del TO-BE.
- Textos cortos para personas sin formación técnica. Diseño adaptable a celular.

---

## Pendientes y supuestos
- **[PENDIENTE DE CONFIRMAR] Legal rechaza un documento dudoso:** el BPMN v03 vuelve a pedir el documento al cliente (`legalAcepta = false` → `TB_SND_CORREGIR`), pero REQ-MVP-02 y el supuesto de `14-mvp/alcance-equipo.md` lo mandan a la ruta en papel. Hay que decidir cuál vale y alinear el otro (BPMN v04 o ajuste del REQ-MVP-02).
- **[PROPUESTA TÉCNICA]** Las variables, los tipos de trabajo y los mensajes son los de `06-revision/despliegue-camunda-8.10.md`, más `enviar-correo-recordatorio` del v03. Si IT los cambia, hay que actualizar este prompt. La variable `recordatorioEnviado` es nueva: ningún gateway la usa.
- **[PROPUESTA TÉCNICA]** La regla «20 días exactos todavía es válido» y el orden de los motivos (fecha futura → vencido → ilegible) siguen el contrato de `entrega-paso23-david-sergio.md`; la zona horaria America/Santo_Domingo es un supuesto.
- **El módulo B no reemplaza el MVP en Python** (paso 23, `app/credito.py`) ni sus 11 pruebas automáticas; replica las mismas reglas para la demo. Las comprobaciones de 6.5 se hacen a mano en Lovable.
- Los incrementos INC-1 a INC-3 de `14-mvp/backlog-autonomo.md` (estado visible para el cliente, cierre a los 10 días hábiles y recordatorios) **no** están en este prompt.
- **Verificar en Lovable:**
  - que las rutas de la REST API v2 coincidan con la documentación de Camunda 8.10;
  - que la pantalla de conexión salga en verde y muestre las dos definiciones desplegadas, con el TO-BE en su versión más reciente (la del v03);
  - que un caso AS-IS llegue a «Crédito desembolsado» completando las tareas en orden;
  - que el módulo B pase las 10 comprobaciones de 6.5 y que los CSV se carguen en Preset (paso 25).
- Las tablas de Supabase guardan correos y datos declarados **sintéticos**. Si algún día entra un caso real, hay que excluir esos campos antes de cargar a Preset (ronda 18).
- Este prompt no reemplaza el **simulador de tareas automáticas** acordado para más adelante.
- Para ver los vencimientos en una demo habría que parametrizar el plazo de los temporizadores, por ejemplo con una variable. Eso cambia los BPMN y queda por decidir.
