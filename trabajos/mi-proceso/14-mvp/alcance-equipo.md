# Alcance del MVP — Flujo de crédito preaprobado (paso 20, `/20-contexto`)

**Fecha:** 2026-10-26 · **Skill:** `mvp-contexto` · **Fuente:** BPMN TO-BE v03 (`08-tobe/proceso-to-be-v03.bpmn`), `08-tobe/requisitos-ears-to-be.md`, ronda 16 (`02-analisis/entrevista.md`).
**Datos:** todo lo que use el MVP es **SINTÉTICO / DEMOSTRACIÓN**; no corresponde a expedientes reales.

## Historia de usuario
**Como** cliente con un crédito preaprobado que aceptó la decisión, **quiero** cargar mis cuatro documentos en un portal y que Legal y Despacho los revisen en línea, **para** que mi expediente quede verificado sin pasar por el concesionario y en menos días hábiles.

Objetivo de negocio al que apunta: bajar el tramo de expediente de 12 a 6 días hábiles (`objetivo-proyecto.md`, PREG-016).

## Porción del proceso (vertical slice)
**Inicio:** el cliente acepta la decisión y el sistema envía el enlace al portal (CTX-1).
**Fin:** el expediente digital queda verificado por Despacho (CTX-1).

| # | Actividad | Responsable | Dato de entrada | Resultado | elementId BPMN | Modo | Origen |
|---|---|---|---|---|---|---|---|
| Inicio | Enviar enlace al portal | Sistema | Solicitud aceptada (id, correo del cliente) | Enlace enviado, conteo de días iniciado | `TB_SND_ENLACE` | Automático | REQ-TOBE-001, 002 |
| UT-1 | Cargar los 4 documentos en el portal | Cliente | Cédula, comprobante de ingresos, estado de cuenta, pagaré (con fecha de expedición) | Documentos recibidos | `CL_CARGAR` / `TB_RCV_DOCS` | Humano | REQ-TOBE-003 |
| – | Validar: completos, ≤ 20 días, legibles; datos iguales entre documentos | Sistema | Documentos cargados | Válido / reintentar / dudoso | `TB_SVC_VALIDAR`, `TB_GW_VALIDO` | Automático (**simulado** en el MVP) | REQ-TOBE-004, 005, 006 |
| UT-2 | Revisar documento dudoso | Legal | Expediente con diferencia de nombre, cédula, salario o monto | Acepta / rechaza | `TB_ACT_REVISAR`, `TB_GW_LEGAL` | Humano | REQ-TOBE-006 |
| UT-3 | Verificar expediente digital | Despacho | Expediente con 4 documentos válidos | OK / pedir corrección | `TB_ACT_VERIF`, `TB_GW_VERIF` | Humano | REQ-TOBE-009 (a) |
| Fin | Expediente digital verificado | – | – | Fin del MVP | (sin evento propio en v03; el MVP termina tras `TB_GW_VERIF` = OK) | – | – |

### Dato fuente vs. supuesto
- **Fuente / confirmado:** los 4 documentos, la regla de 20 días, los 5 intentos por documento, la revisión de Legal en casos dudosos y la verificación de Despacho (rondas 6 a 8; estado «Confirmado por entrevistado» en los REQ-TOBE).
- **Supuesto del MVP:** la validación de legibilidad la hace una persona en el formulario o se simula con una casilla; no hay OCR. El envío del correo se simula (se registra un evento, no se manda correo).
- **Supuesto del MVP:** si Legal rechaza un documento dudoso, el caso se marca «pasa a ruta en papel» y termina ahí (la ruta en papel está excluida).

## Definición de terminado
1. Desde el navegador se crea una solicitud aceptada y queda registrado el envío del enlace.
2. El cliente carga los 4 documentos; un documento vencido (> 20 días) o ilegible se rechaza con el motivo y cuenta un intento.
3. Un caso con datos distintos entre documentos aparece como tarea de **Legal**; uno sin diferencias pasa directo a **Despacho**.
4. Despacho completa la verificación y el caso queda «Expediente digital verificado».
5. Cada paso deja un evento con fecha y hora en la bitácora, y la bitácora se exporta a CSV marcado como SINTÉTICO.
6. Las pruebas automáticas pasan en modo `ENGINE_MODE=mock`. La conexión con Camunda real **no** forma parte de este terminado.

## Exclusiones (CTX-3)
1. **Riesgo, análisis y decisión de crédito** (`ACT_002` a `ACT_005`, `GW_001` a `GW_004`): el MVP parte de una solicitud ya aceptada.
2. **Recogida de originales por mensajero, comisión al cliente y desembolso** (`TB_SND_RECOGIDA`, `TB_ACT_RECOGER`, `TB_ACT_ESCANEAR`, `ACT_009`; REQ-TOBE-009 (b), 010, 011, 012, 016).
3. **Ruta en papel y temporizadores** (`ACT_006` a `ACT_008`, `TMR_001`, `TMR_T01`, `TMR_T02`, `MSG_T01`, recordatorios de los días 3 y 6, y la llamada del día 8; REQ-TOBE-007, 008, 013, 017, 018).

## Efecto en los números
Ninguno. El MVP es una demostración y no cambia el ROI (+16,7 %, 10,1 meses) ni los KPI del tablero. Los datos que genere el MVP no se mezclan con los de `09-datos/`.

## Siguiente paso
Paso 21 (`/21-ears`): tres requisitos EARS del MVP con prueba positiva y adversarial, tomados de REQ-TOBE-003 a 006 y 009.
