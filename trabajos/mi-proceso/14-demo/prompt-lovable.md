# Prompt para Lovable — Demo del flujo de crédito Expomóvil sobre Camunda 8.10

**Fecha:** 2026-10-24 · **Estado:** borrador v01 · **Base:** `05-bpmn/proceso-v02.bpmn`, `08-tobe/proceso-to-be-v02.bpmn` y `06-revision/despliegue-camunda-8.10.md`.

## Antes de usarlo
1. **Desplegar los dos BPMN** en el clúster de Camunda 8.10 desde Camunda Modeler (*Deploy*): `proceso-v02.bpmn` y `proceso-to-be-v02.bpmn`.
2. **Camunda corre en SaaS** (decidido el 2026-10-24). El *API client* ya está creado. Tener a mano el archivo de credenciales que entregó la consola de Camunda al crearlo. De ese archivo salen los valores de la sección 1:
   - el **client id** y el **client secret**;
   - la **URL del token** y el **audience**;
   - el **cluster id** y la **región**.

   **Dirección REST:** en Camunda 8.10 el archivo de credenciales no trae una URL `…zeebe.camunda.io`. Los dominios `zeebe` se eliminaron en 8.10 y ahora responden 404. La dirección se arma así: `https://{CAMUNDA_CLUSTER_REGION}.api.camunda.io/{CAMUNDA_CLUSTER_ID}`. También se puede copiar de la consola: *Clusters → (el clúster) → API → Connection information → «Camunda REST API»*.

   Comprobar en la consola que el API client tenga acceso al Orchestration Cluster (*scope* Zeebe / Orchestration Cluster API). El clúster tiene las *authorizations* activadas: sin permisos explícitos, Camunda responde **403 FORBIDDEN** (confirmado el 2026-10-24 al desplegar). En *Admin* del clúster → *Authorizations*, crear autorizaciones con *Owner type* = Client y *Owner ID* = client id:
   - `RESOURCE` (`*`): `CREATE`, para desplegar, y `READ`;
   - `PROCESS_DEFINITION` (`*`, o `Process_Credito_ASIS` y `Process_Credito_TOBE`): `READ_PROCESS_DEFINITION`, `CREATE_PROCESS_INSTANCE`, `READ_PROCESS_INSTANCE`, `UPDATE_PROCESS_INSTANCE`, `READ_USER_TASK` y `UPDATE_USER_TASK`;
   - `MESSAGE` (`*`): `CREATE` y `READ`.

   Alternativa rápida para la demo: asignar el client al rol `admin`.
3. **Credenciales:** cuando Lovable pida los *secrets*, cargarlos directamente en Supabase. **Nunca pegarlos en el prompt, en el chat de Lovable ni en el código.**
4. **Datos:** la demo usa solo **datos sintéticos** (regla de AGENTS.md). No cargar clientes reales.
5. **Pegar en Lovable** el bloque de la sección siguiente, completo.

---

## Prompt (copiar desde aquí)

Construye una aplicación web en **español** llamada **«Demo Crédito Expomóvil — AS-IS vs TO-BE»**. Sirve para mostrar en clase cómo avanzan dos procesos BPMN ya desplegados en **Camunda 8.10**: el proceso actual (AS-IS) y el propuesto (TO-BE). La app permite iniciar casos, completar las tareas humanas de cada rol, simular las tareas automáticas y los mensajes del portal, y ver en qué paso va cada caso.

### 1. Arquitectura y seguridad
- Frontend: React + TypeScript + Tailwind + shadcn/ui.
- **Toda llamada a Camunda pasa por una Supabase Edge Function** (`camunda-proxy`). El navegador nunca llama a Camunda directamente ni ve credenciales.
- Camunda corre en **Camunda 8 SaaS**. Pídeme estos secrets de Supabase y no los pongas en el código:
  - `CAMUNDA_REST_ADDRESS`: dirección REST del clúster, sin `/v2` al final. En Camunda 8.10 el formato es `https://{region}.api.camunda.io/{clusterId}`, con el subdominio **`api`**. **No uses el formato antiguo `{region}.zeebe.camunda.io`**: en 8.10 responde 404.
  - `CAMUNDA_CLIENT_ID` y `CAMUNDA_CLIENT_SECRET`.
  - `CAMUNDA_OAUTH_URL`: el valor que trae el archivo de credenciales.
  - `CAMUNDA_TOKEN_AUDIENCE`: el valor que trae el archivo de credenciales (`ZEEBE_TOKEN_AUDIENCE` o `CAMUNDA_TOKEN_AUDIENCE`).
- La Edge Function obtiene el token OAuth 2.0 con *client credentials* (`grant_type=client_credentials`, `client_id`, `client_secret`, `audience`). Lo guarda en memoria hasta poco antes de que venza y lo envía como `Authorization: Bearer …`. Si Camunda responde 401, pide un token nuevo y reintenta una sola vez.
- La Edge Function expone solo operaciones concretas (lista blanca), no un proxy abierto: `topology`, `startInstance`, `searchInstances`, `getInstance`, `searchUserTasks`, `completeUserTask`, `activateJobs`, `completeJob`, `publishMessage`, `searchIncidents`, `searchVariables`, `searchElementInstances`, `searchProcessDefinitions`.
- Usa la **Orchestration Cluster REST API v2** de Camunda 8.10: `POST /v2/process-instances`, `POST /v2/process-instances/search`, `POST /v2/user-tasks/search`, `POST /v2/user-tasks/{userTaskKey}/completion`, `POST /v2/jobs/activation`, `POST /v2/jobs/{jobKey}/completion`, `POST /v2/messages/publication`, `POST /v2/incidents/search`, `POST /v2/variables/search`, `POST /v2/element-instances/search` y `GET /v2/topology`. **Verifica los nombres exactos de rutas y campos en la documentación oficial de Camunda 8.10** antes de implementarlos y ajústalos si difieren. En la documentación las rutas aparecen sin el prefijo `/v2` (por ejemplo `POST /process-instances`), porque es parte de la URL base. Los esquemas de cada cuerpo están en la página *Orchestration Cluster API → Try with Swagger*. Al crear una instancia, identifica el proceso por su ID BPMN (`Process_Credito_ASIS` / `Process_Credito_TOBE`) sin versión, para que Camunda use la última versión desplegada.
- Muestra los errores de Camunda en español y en lenguaje claro, por ejemplo: «No hay conexión con Camunda» o «La tarea ya fue completada por otra persona». Si Camunda responde **403**, muestra: «El API client no tiene permiso para esta acción; revisar sus permisos en la consola de Camunda».
- **No hay login.** Es una demo; el usuario elige su rol en un selector. Agrega un aviso fijo: «Demo con datos sintéticos — no usar datos reales».

### 2. Los dos procesos
| Proceso | `processDefinitionId` |
|---|---|
| AS-IS (actual) | `Process_Credito_ASIS` |
| TO-BE (propuesto) | `Process_Credito_TOBE` |

### 3. Pantallas

**3.1 Conexión.** Muestra el estado con `GET /v2/topology` (verde o rojo), la versión del clúster y si los procesos `Process_Credito_ASIS` y `Process_Credito_TOBE` están desplegados. Esto último se puede comprobar con `POST /v2/process-definitions/search`. Si falta alguno, muestra: «Despliega el BPMN desde Camunda Modeler».

**3.2 Nuevo caso.** Formulario: proceso (AS-IS / TO-BE), nombre del cliente, cédula ficticia, monto solicitado, salario y concesionario. Incluye un botón «Generar datos de ejemplo» que llena valores sintéticos.
- La app genera `solicitudId` con el formato `SOL-AAAAMMDD-####`.
- Inicia la instancia con estas variables: `solicitudId`, `cliente` (objeto con los datos del formulario), `proceso` (`"AS-IS"` o `"TO-BE"`) y `fechaInicioDemo`.
- Opción «Crear caso gemelo»: inicia el mismo cliente en los dos procesos a la vez, para compararlos.

**3.3 Casos.** Tabla de instancias activas y terminadas de los dos procesos, con estas columnas: `solicitudId`, cliente, proceso, estado, **paso actual** (elementos activos, con su nombre legible) e incidentes (badge rojo). Permite filtrar por proceso y estado.

**3.4 Detalle del caso.** Muestra:
- una línea de tiempo con los pasos recorridos (element instances con fechas);
- las variables actuales;
- los incidentes, con su mensaje explicado en español (ver 3.7);
- botones contextuales según el paso en que esté el caso: completar la tarea, simular la tarea automática o enviar un mensaje.
- Opcional, si es sencillo: mostrar el diagrama con bpmn-js (`NavigatedViewer`) y resaltar los elementos activos. Para eso se cargan los XML desde `public/bpmn/`; yo subiré los archivos.

**3.5 Bandeja de tareas por rol.** Un selector de rol filtra las tareas de usuario pendientes (`POST /v2/user-tasks/search`, estado `CREATED`). Cada tarea abre un formulario. Al enviarlo, la tarea se completa con las variables indicadas (ver la tabla de la sección 4). Si la tarea no pide variables, muestra solo un botón «Marcar como hecha».

**3.6 Tareas automáticas y portal (simulador).** Este panel reemplaza a los sistemas que todavía no existen.
- **Tareas automáticas:** para cada tipo de trabajo de la sección 5, un botón «Buscar y ejecutar» activa los trabajos pendientes de ese tipo (`POST /v2/jobs/activation`, `worker: "demo-lovable"`, timeout de 60 s). Muestra cada trabajo con su `solicitudId` y deja elegir el resultado antes de completarlo.
- **Portal del cliente (solo TO-BE):** para cada caso que espera documentos:
  - botón «El cliente cargó documentos»: publica el mensaje `documentos-cargados` con `correlationKey = solicitudId`;
  - botón «IT reporta falla del portal»: publica `falla-portal-reportada`, con la misma clave.
- Interruptor «Modo automático»: cada 10 s ejecuta los trabajos pendientes con el resultado «camino feliz».

**3.7 Comparación AS-IS vs TO-BE.** Para los casos terminados muestra:
- número de pasos humanos;
- número de devoluciones o correcciones;
- duración de la demo;
- ruta final (desembolsado, rechazado, no acepta, vencido).

En los casos gemelos los muestra lado a lado. Incluye la nota: «La duración de la demo no representa días reales; los tiempos reales del proceso están en el diagnóstico.»

### 4. Tareas de usuario: rol, formulario y variables
Identifica cada tarea por su `elementId`. Los valores de las variables deben coincidir **exactamente** con estos; si no, el proceso cae en un incidente.

| `elementId` | Nombre | Rol | Proceso | Campos del formulario → variables |
|---|---|---|---|---|
| `ACT_001` | Crear solicitud | Persona de Negocio | Ambos | Ninguno (solo confirmar) |
| `ACT_002` | Evaluar solicitud | Persona de Riesgo | Ambos | Radio `resultadoRiesgo`: `"apto"`, `"corregir"`, `"rechazar"` |
| `ACT_003` | Analizar crédito | Analista de crédito | Ambos | Radio `decisionAnalisis`: `"aprobar"`, `"rechazar"`. Si aprueba: casilla `conCondiciones` (`true`/`false`). Si rechaza, enviar `conCondiciones: false` |
| `ACT_004` | Informar decisión al cliente | Analista de crédito | Ambos | Radio `clienteAcepta`: `true` / `false` |
| `ACT_005` | Modificar datos del crédito | Persona de Negocio | Ambos | Ninguno (opcional: editar el monto en `cliente.monto`) |
| `ACT_006` | Recopilar expediente (en el TO-BE: ruta de respaldo en papel) | Legal | Ambos | Radio `documentacionCompleta`: `true` / `false` |
| `ACT_007` | Escanear documentación | Legal | Ambos | Ninguno |
| `ACT_008` | Verificar y autorizar expediente | Analista de crédito (Despacho) | Ambos | Radio `documentacionOk`: `true` / `false` |
| `ACT_009` | Desembolsar crédito | Desembolso | Ambos | Ninguno |
| `TB_ACT_REVISAR` | Revisar documento dudoso | Legal | TO-BE | Radio `legalAcepta`: `true` / `false` |
| `TB_ACT_VERIF` | Verificar expediente digital | Analista de crédito (Despacho) | TO-BE | Radio `expedienteOk`: `true` / `false` |
| `TB_ACT_PEDIR` | Pedir documento corregido al cliente | Analista de crédito (Despacho) | TO-BE | Ninguno |
| `TB_ACT_RECOGER` | Recoger originales a domicilio | Mensajero certificado | TO-BE | Radio `recogidaLograda`: `true` / `false` |
| `TB_ACT_RECOP_ORIG` | Recopilar originales por la ruta actual | Legal | TO-BE | Ninguno |
| `TB_ACT_ESCANEAR` | Escanear originales y enviar sobre | Legal | TO-BE | Ninguno |

Roles del selector: Persona de Negocio, Persona de Riesgo, Analista de crédito (Despacho), Legal, Mensajero certificado, Desembolso y «Todos» (vista del profesor).

### 5. Tareas automáticas (tipos de trabajo)
| Tipo | Proceso | Resultado que se elige al simular → variables con que se completa |
|---|---|---|
| `cerrar-solicitud` | Ambos | Sin opciones → `{ "cierreAutomatico": true }` |
| `enviar-correo-enlace` | TO-BE | Sin opciones. Muestra una vista previa del correo ficticio con el enlace al portal → `{ "enlaceEnviado": true }` |
| `validar-documentos` | TO-BE | Radio `resultadoValidacion`: `"valido"` (camino feliz), `"rechazado"`, `"dudoso"`, `"agotado"`. Muestra una ayuda: «rechazado = vencido (más de 20 días) o ilegible; dudoso = nombre, cédula, salario o monto no coinciden; agotado = 5 intentos fallidos en un documento» |
| `enviar-correo-correccion` | TO-BE | Sin opciones → `{ "correccionSolicitada": true }` |
| `programar-recogida` | TO-BE | Fecha de recogida (por defecto, mañana) → `{ "fechaRecogida": "AAAA-MM-DD" }` |

Si un trabajo no se puede completar, muestra el error y no reintentes en bucle.

### 6. Limitaciones que la app debe explicar (en un ícono de ayuda)
- Los temporizadores de 10 días hábiles están configurados como **14 días calendario** (`P14D`) y **no se pueden acelerar desde la app**. Las rutas por vencimiento no se ven en una demo en vivo.
- En el TO-BE, después de «El cliente cargó documentos» hay que ejecutar `validar-documentos` para que el caso avance.
- Si falta una variable, Camunda crea un incidente. La app debe mostrar cuál variable falta, según la decisión donde quedó detenido el caso.

### 7. Estilo
- Interfaz limpia y profesional, con colores sobrios de banca.
- **AS-IS en gris azulado y TO-BE en verde**, de forma consistente en toda la app.
- Textos cortos para personas sin formación técnica. Diseño adaptable a celular.

---

## Pendientes y supuestos
- **[PROPUESTA TÉCNICA]** Las variables, los tipos de trabajo y los mensajes son los de `06-revision/despliegue-camunda-8.10.md`. Si IT los cambia, hay que actualizar este prompt.
- **Verificar en Lovable:**
  - que las rutas de la REST API v2 coincidan con la documentación de Camunda 8.10;
  - que la Edge Function obtenga el token y llegue al clúster SaaS (pantalla de conexión en verde);
  - que un caso AS-IS llegue a «Crédito desembolsado» completando las tareas en orden.
- Este prompt no reemplaza el **simulador de tareas automáticas** acordado para más adelante, aunque el panel 3.6 cubre lo básico para la demo.
- Para ver los vencimientos en una demo habría que parametrizar el plazo de los temporizadores, por ejemplo con una variable. Eso cambia los BPMN y queda por decidir.
