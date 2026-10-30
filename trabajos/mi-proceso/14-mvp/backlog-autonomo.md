# Backlog autónomo del MVP — paso 27 (`/27-iterar`)

**Fecha:** 2026-10-26 · **Skill:** `mvp-iterar` · **Estado:** **APROBADO** (ronda 20, 2026-10-26). Orden INC-1 → INC-2 → INC-3; días hábiles = lunes a viernes, sin feriados.
**Base:** `14-mvp/alcance-equipo.md` (exclusiones), `08-tobe/requisitos-ears-to-be.md`, `14-mvp/entrega-paso23-david-sergio.md`. Datos SINTÉTICOS.
**Condición previa:** que el paso 23 (MVP base) esté implementado y con las pruebas en verde. Cada incremento se hace **uno por vez** y, al terminar, se vuelve a auditar (paso 26).
**Efecto en los números:** ninguno sobre el ROI (16,7 %, 10,1 meses) ni sobre los KPI del tablero, que salen de `09-datos`. Los incrementos solo agregan medidas **del MVP** (casos de demostración).

## Cómo se eligieron
Se tomaron los requisitos TO-BE que el alcance dejó fuera y se ordenaron por valor para el usuario, tamaño y riesgo. Regla del skill: el primero debe caber en menos de 90 minutos y no tocar el BPMN.

| Opción | Requisito TO-BE | Valor | Tamaño | Riesgo | Decisión |
|---|---|---|---|---|---|
| Estado visible para el cliente | REQ-TOBE-014 | Alto: es el segundo dolor del cliente (CV-3) | **S** | Bajo | **INC-1** |
| Cierre a los 10 días hábiles | REQ-TOBE-013 | Alto: permite medir KPI-03 en el MVP | **M** | Medio (calendario) | **INC-2** |
| Recordatorios días 3 y 6, llamada día 8 | REQ-TOBE-017, 018 | Medio: reduce cierres por vencimiento | **M** | Medio (depende de INC-2) | **INC-3** |
| Recogida de originales con comisión | REQ-TOBE-009 (b), 016 | Medio | L | Alto: falta el monto de la comisión | Fuera por ahora |
| Ruta en papel completa | REQ-TOBE-007, 008 | Bajo para la demo | L | Alto: duplica el AS-IS | Fuera |

## INC-1 · Estado de la solicitud visible para el cliente (S, < 90 min) — **HECHO** (ronda 23, 2026-10-28)
- **EARS (ubicuo):** El portal deberá mostrar al cliente, con su `SOL-NNNNN`, el **hito actual** de su solicitud: «Enlace enviado», «Documentos con observaciones», «En revisión», «En verificación», «Expediente verificado» o «Pasa a atención presencial».
- **Archivos:** `app/credito.py` (nueva ruta `GET /api/credito/estado/{id_solicitud}`), `app/static/credito.html` (caja «Consultar mi solicitud»), `tests/test_credito.py`.
- **Criterio de aceptación:** cada estado interno se traduce a un hito; la respuesta trae **solo** `id_solicitud`, hito y fecha del último cambio.
- **Prueba negativa:** un `SOL-` inexistente devuelve 404 con el mismo mensaje que un formato inválido (no revela qué IDs existen); la respuesta **no** incluye correo, cédula ni montos.
- **Respaldo (fallback):** si falla, se oculta la caja; el resto del MVP no cambia.
- **No cambia:** BPMN, tablas, ni las 43 pruebas previas.

## INC-2 · Cierre por expediente incompleto a los 10 días hábiles (M)
- **EARS (no deseado):** Si pasan **10 días hábiles** desde el envío del enlace sin los 4 documentos válidos, o desde que Despacho pidió una corrección sin recibirla, entonces el sistema deberá cerrar el caso con estado «Cerrada por expediente incompleto». Cada corrección pedida por Despacho **reinicia** el conteo.
- **Archivos:** `app/credito.py` (función de días hábiles y ruta `POST /api/credito/vencimientos/revisar?fecha=AAAA-MM-DD` para simular el reloj), `cred_casos` (+ `inicio_conteo`), `credito.html` (estado nuevo), pruebas.
- **Criterio de aceptación:** con fecha simulada del día hábil 10 el caso sigue abierto; el día 11 se cierra y queda el evento `CERRADA_VENCIMIENTO` (`TMR_T01` / `TMR_T02`). El CSV permite calcular KPI-03 del MVP.
- **Prueba negativa:** un caso ya en «Revisión Legal» o «Verificación» **no** se cierra; revisar dos veces el mismo día no duplica el evento; un fin de semana no cuenta.
- **Respaldo:** la revisión es manual (botón o llamada), no un proceso automático en segundo plano; si falla, no cierra nada.
- **Días hábiles (ITER-2):** lunes a viernes, **sin feriados**, para no complicar el MVP. Los feriados de República Dominicana quedan fuera.

## INC-3 · Recordatorios de los días 3 y 6 y llamada del día 8 (M)
- **EARS (por estado):** Mientras el caso no tenga los 4 documentos válidos, el sistema deberá registrar un **recordatorio por correo** los días hábiles 3 y 6 y, el día 8, crear para el **Analista** la tarea «Llamar al cliente».
- **Archivos:** `app/credito.py` (reutiliza el conteo de INC-2), rol `analista` en las bandejas, `credito.html`, pruebas.
- **Criterio de aceptación:** con fechas simuladas aparecen los eventos `RECORDATORIO_ENVIADO` (`TB_SND_RECORDAR`) los días 3 y 6, y la tarea `TB_ACT_LLAMAR` el día 8; completarla deja evento.
- **Prueba negativa:** si el cliente completa sus documentos el día 5, no hay recordatorio del día 6 ni llamada; no se envían dos recordatorios el mismo día. El correo se **simula** (evento), no se envía.
- **Respaldo:** desactivar con una variable de entorno sin tocar INC-1 ni INC-2.

## Decisiones (ronda 20)
- **ITER-1:** se empieza por INC-1 (estado visible para el cliente).
- **ITER-2:** días hábiles de lunes a viernes, sin feriados.
- **ITER-3:** orden INC-1 → INC-2 → INC-3; la recogida con comisión queda fuera hasta conocer el monto.

## INC-4 · Buzón de correos simulado para el cliente y los funcionarios (S) — **HECHO** (2026-10-29, Sergio)
- **EARS (por evento):** Cuando el caso cambie de paso, el sistema deberá dejar en el **buzón simulado** del destinatario un correo con asunto `SOL-NNNNN · …` y un enlace al caso en el portal. Al **cliente**: enlace al portal (`TB_SND_ENLACE`), documentos rechazados con motivo e intento (`TB_SND_CORREGIR`), corrección pedida por Despacho (`TB_SND_CORREGIR`), expediente verificado (`END_VERIFICADO`) o paso a atención presencial (`END_PAPEL_AGOTADO`, `END_PAPEL_LEGAL`). A **Legal** y **Despacho**: aviso de tarea nueva en su bandeja (`TB_ACT_REVISAR`, `TB_ACT_VERIF`).
- **Archivos:** `app/credito.py` (tabla `cred_correos`, rutas `GET /api/credito/correos?rol=&para=` y `POST /api/credito/correos/{id}/leido`), `app/static/buzon.html` (página `/buzon` con pestañas Cliente / Legal / Despacho), `app/static/credito.html` (enlace al buzón; `/credito?caso=N` abre ese caso), `app/main.py` (+3 líneas), `tests/test_credito.py` (+6 pruebas).
- **Criterio de aceptación:** cada transición deja exactamente un correo al destinatario correcto; abrir un correo lo marca como leído; el buzón del cliente se filtra por su dirección.
- **Prueba negativa:** si Camunda rechaza completar una tarea, no queda correo (se revierte con el resto); rol desconocido → 422; correo inexistente → 404; el 5.º rechazo de un documento manda «atención presencial», no «vuelva a cargar».
- **Respaldo:** ningún correo sale de la app (no hay SMTP); si la página `/buzon` falla, el portal `/credito` no cambia.
- **No cambia:** BPMN, tablas existentes, vista de Preset ni las 48 pruebas previas (54 en verde).
