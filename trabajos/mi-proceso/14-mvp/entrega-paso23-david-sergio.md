# Paso 23 (frontend) y siguientes — encargo para David y Sergio

**Fecha:** 2026-10-26 · **De:** Ana (con Claude) · **Estado:** especificación aprobada; **código sin escribir**. En la máquina de Ana no se corre Python (decisión de la ronda 19), así que la implementación y las pruebas las hacen David y Sergio.
**Datos:** SINTÉTICOS. **Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio).

## Qué leer primero (en este orden)
1. `14-mvp/alcance-equipo.md` — porción del proceso, 3 tareas humanas y exclusiones (ronda 16).
2. `14-mvp/ears-equipo.md` — REQ-MVP-01 a 03 aprobados (ronda 17).
3. `14-mvp/modelo-equipo.md` — tablas casos / documentos / eventos e IDs (ronda 18).
4. `14-mvp/pruebas-propuestas/test_credito.py` — **11 pruebas escritas antes del código**; definen el contrato de la API. Al implementar, copiarlo a `tests/` (raíz del repo) y dejar todo en verde.

## Estado de la línea base (comprobado el 2026-10-26)
Con Python 3.12 y `pip install -r requirements.txt` **más `pyyaml`**, el kit pasó **32 pruebas** (`python -m pytest -q`). Sin `pyyaml` falla `tests/test_preset_bundle.py` al importar: conviene agregar `pyyaml` a `requirements.txt`.

## Decisiones de pantalla (ronda 19)
- **FE-1:** formulario inicial con **alias**, **correo** del cliente y **monto**; al enviarlo se registra el envío del enlace (`TB_SND_ENLACE`). Los 4 documentos se cargan después, en la tarea del cliente.
- **FE-2:** si un rol no tiene tareas, la bandeja queda **vacía**, sin mensaje.
- **FE-3:** botón **«Llenar ejemplo dudoso»** que llena los documentos con una **cédula distinta** en el pagaré, para mostrar la tarea de Legal.

## Diseño propuesto (para no romper la demo del kit)
- **Módulo aparte:** `app/credito.py` con un `APIRouter` en `/api/credito` y modelos SQLAlchemy sobre el mismo `Base` de `app/db.py`, en tablas **`cred_casos`, `cred_documentos`, `cred_eventos`** (las tablas `casos`/`eventos` del kit tienen otro esquema). Registrar el router en `app/main.py` con `app.include_router(...)`; no tocar los endpoints existentes.
- **Pantalla:** `app/static/credito.html`, servida en `/credito`, con el mismo estilo que `index.html`, etiqueta **SINTÉTICO / DEMOSTRACIÓN** y 4 secciones: (1) formulario FE-1, (2) carga de documentos del cliente (solo los no válidos) + botón FE-3, (3) bandejas Legal y Despacho, (4) bitácora y botones de CSV.
- **Modo:** `ENGINE_MODE=mock`. Las tareas se derivan del estado del caso; Camunda real es el paso 24.

### Contrato de la API (lo que exigen las pruebas)
| Método y ruta | Qué hace | Errores |
|---|---|---|
| `POST /api/credito/casos` `{cliente_alias, correo_cliente, monto}` | Crea caso `SOL-9NNNN` al azar (verificar que no exista), estado `ENLACE_ENVIADO`, 4 documentos `PENDIENTE`, evento `ENLACE_ENVIADO` con tarea `TB_SND_ENLACE`, `fuente_datos = SINTETICO` | 422 si correo inválido, alias < 2 caracteres o monto ≤ 0 |
| `POST /api/credito/casos/{id}/documentos` `[ {tipo, fecha_expedicion, legible, nombre?, cedula?, salario?, monto?} ]` | Valida cada documento enviado: `fecha futura`, `vencido (> 20 días)` (calendario), `ilegible`; los no enviados que no estén válidos → `falta`. Cada rechazo suma 1 intento a ese documento; al 5.º → `AGOTADO` y caso `RUTA_PAPEL`. Si los 4 son válidos, compara nombre/cédula/salario/monto entre documentos (solo valores presentes): distintos → `REVISION_LEGAL` (`caso_dudoso = true`), iguales → `VERIFICACION_DESPACHO` | 200 si quedan los 4 válidos; **422 con el caso y los motivos** si hubo rechazo (guardando los intentos); 409 si se reenvía un documento ya válido, si el caso no espera documentos o «intentos agotados»; 404 caso inexistente |
| `GET /api/credito/tareas?rol=cliente\|legal\|despacho` | Tareas abiertas: `{key, name, role, elementId, caso_id, id_solicitud}`; `elementId` = `CL_CARGAR`, `TB_ACT_REVISAR` o `TB_ACT_VERIF` | — |
| `POST /api/credito/tareas/{key}/completar` `{actor, resultado, documento?, observacion?}` | Legal: `ACEPTA` → `VERIFICACION_DESPACHO`; `RECHAZA` → `RUTA_PAPEL`. Despacho: `OK` → `VERIFICADO` + `verificado_en` + evento `EXPEDIENTE_VERIFICADO`; `CORREGIR` + `documento` → `ESPERANDO_CORRECCION` y ese documento vuelve a rechazado (sin sumar intento) | 422 sin resultado, resultado de otro rol o `CORREGIR` sin documento; **409 si la clave ya no es la tarea activa (doble clic)**; 404 caso inexistente |
| `GET /api/credito/casos`, `/casos/{id}`, `/casos/{id}/bitacora` | Consulta; el caso incluye sus `documentos` | 404 |
| `GET /api/credito/export/{casos\|documentos\|eventos}.csv` | CSV para Preset con **todos** los campos (DAT-3 = c), incluido `correo_cliente`, y `fuente_datos = SINTETICO` | 404 tabla desconocida |

Clave de tarea sugerida: `cred-{caso_id}-{rol}-{etapa}`, donde `etapa` sube en cada cambio de estado; así una clave vieja da 409.

## Pasos que siguen y quién los hace
| Paso | Qué | Quién / requisito |
|---|---|---|
| 23 | Implementar el diseño anterior y dejar verdes las 32 + 11 pruebas; capturas de: caso creado, tarea activa, tarea completada, CSV | David / Sergio (Python) |
| 24 | Camunda real: desplegar el BPMN del MVP y probar 1 instancia con 2 tareas | Quien tenga las credenciales del clúster; no poner credenciales en el repo |
| 25 | Preset: subir los CSV del MVP y crear un KPI a mano (p. ej. % de casos dudosos o intentos promedio por caso) | Equipo, en la UI de Preset |
| 26 | Auditoría: `python -m pytest -q` + revisión SOP–EARS–BPMN–API–DB; revisar la regla de datos reales de DAT-3 | David / Sergio, con Claude para el informe |
| 27 | Backlog de 3 incrementos | Ana con Claude (no requiere Python) |
