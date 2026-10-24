# Diccionario de datos — Flujo de crédito preaprobado (SINTÉTICO)

**Fecha:** 2026-10-24 · **Skill:** `modelar-datos` · **Fuente de decisiones:** ronda 10 (DAT-1 a DAT-4) y fichas de `10-kpis/`.

> **Todos los datos son SINTÉTICOS** (DAT-1). Se generan con `09-datos/generar_sinteticos.js` (semilla fija 20261024) a partir de estimaciones de la fuente y de la entrevista. **No son mediciones** y no contienen datos personales: `id_par` es un código inventado (`SOL-00001`), sin nombres, cédulas, correos ni montos.

## 1. Archivos
| Archivo | Granularidad | Filas | Uso |
|---|---|---|---|
| `casos.csv` | 1 fila por **solicitud y escenario** | 16.000 (8.000 × 2) | KPI-01 a KPI-04, Preset |
| `actividades.csv` | 1 fila por **actividad del expediente, vuelta, solicitud y escenario** | 24.140 | Ver dónde se va el tiempo |
| `resumen_mensual.csv` | 1 fila por **mes y escenario** | 24 | Preset y Excel del ROI |
| `registro_calidad.md` | — | — | Pruebas de calidad (generado) |

**Regla de unión:** **no** unir `casos.csv` con `actividades.csv` para contar solicitudes: cada solicitud tiene varias actividades y se duplicarían. En el TO-BE varias actividades ocurren **en paralelo**: sumar `dias_habiles` de `actividades.csv` **no** da el ciclo. El ciclo es `dias_habiles_expediente` de `casos.csv`.

## 2. `casos.csv`
| Campo | Tipo | ¿Vacío? | Criterio de captura | Origen real (cuando exista) | Protección |
|---|---|---|---|---|---|
| `id_caso` | texto | No | `id_par` + escenario (`-asis` / `-tobe`) | ID de la instancia | Código sin datos personales |
| `id_par` | texto | No | Misma solicitud en los dos escenarios | Número de solicitud **seudonimizado** | No usar el número real |
| `escenario` | texto | No | `AS-IS` o `TO-BE` | — | — |
| `mes` | texto YYYY-MM | No | Mes de `fecha_inicio`. Usar como **categoría**, no como fecha | Sistema de solicitudes | — |
| `temporada` | texto | No | `feria` (febrero y noviembre) o `no feria` | Calendario de ferias | — |
| `fecha_inicio` | fecha | No | Creación de la solicitud (`ACT_001`) | Sistema de solicitudes: fecha de inicio (KPI-Q2b) | — |
| `fecha_aceptacion` | fecha | Sí, si no entró a expediente | Cliente acepta sin condiciones; inicio del expediente | TO-BE: Camunda (`TB_SND_ENLACE`). AS-IS: [PENDIENTE: el sistema solo tiene inicio y fin (DAT-2)] | — |
| `fecha_sobre_desembolso` | fecha | Sí, si no hubo sobre | Sobre sale a Desembolso; fin del expediente (KPI-Q4) | TO-BE: Camunda (`TB_GW_MERGE`). AS-IS: [PENDIENTE] | — |
| `fecha_fin` | fecha | No | Desembolso o cierre de la solicitud | Sistema de solicitudes: fecha de fin | — |
| `estado_final` | texto | No | Estado que deja la última actividad (DAT-3): `Desembolsada`, `Rechazada por Riesgo`, `Rechazada`, `Cliente no acepta`, `Cerrada por expediente incompleto` | Sistema de solicitudes | — |
| `entro_a_expediente` | 0/1 | No | 1 si el cliente aceptó sin condiciones | Derivado | — |
| `ruta` | texto | Sí, si no entró | `digital` o `papel`. En el AS-IS siempre `papel` | Camunda | — |
| `motivo_papel` | texto | Sí, si es digital o AS-IS | `falla portal` o `intentos agotados` | Camunda (`MSG_T01`, `TB_GW_CARGA`) | — |
| `llego_a_verificacion` | 0/1 | No | 1 si Despacho verificó al menos una vez | Camunda | — |
| `devuelta` | 0/1 | No | 1 si Despacho devolvió o pidió corrección al menos una vez | Camunda (`documentacionOk` / `expedienteOk = false`) | — |
| `n_devoluciones` | entero | No | Número de devoluciones | Camunda | — |
| `motivo_devolucion` | texto | Sí, si no hubo | Primer motivo: `vencido`, `ilegible`, `no cuadra` | Despacho (REQ-017 pendiente) | — |
| `cerrada_vencimiento` | 0/1 | No | 1 si se cerró por los 10 días hábiles | Camunda (`END_VENCIDA`) | — |
| `temporizador` | texto | Sí, si no se cerró | `papel` (`TMR_001`) o `carga` (`TMR_T01`) | Camunda | — |
| `sobre_enviado` | 0/1 | No | 1 si el sobre salió a Desembolso | Camunda | — |
| `recogida_fallida` | 0/1 | No | 1 si el mensajero no logró recoger (solo TO-BE digital) | Camunda (`recogidaLograda = false`) | — |
| `dias_habiles_expediente` | entero | Sí, si no hubo sobre | Días hábiles de la aceptación a la salida del sobre (KPI-01) | Derivado de las fechas | — |
| `dias_habiles_total` | entero | No | Días hábiles de inicio a fin | Derivado | — |
| `fuente_datos` | texto | No | Siempre `SINTETICO` en este archivo | — | Etiqueta obligatoria |

## 3. `actividades.csv`
| Campo | Tipo | Criterio |
|---|---|---|
| `id_caso`, `id_par`, `escenario`, `mes`, `temporada` | como en `casos.csv` | — |
| `actividad_id` | texto | ID del BPMN (`ACT_006`, `ACT_007`, `ACT_008`, `SUB_T01`, `TB_ACT_VERIF`, `TB_ACT_PEDIR`, `TB_ACT_RECOGER`, `TB_ACT_RECOP_ORIG`, `TB_ACT_ESCANEAR`) |
| `actividad`, `responsable` | texto | Nombre y carril del BPMN |
| `vuelta` | entero | 1 la primera vez; 2 o más tras cada devolución |
| `dias_habiles` | entero | Duración de la actividad (trabajo + espera). Solo el tramo de expediente |
| `fuente_datos` | texto | `SINTETICO` |

## 4. `resumen_mensual.csv`
Una fila por mes y escenario. Las tasas se calculan como `SUM(eventos) / SUM(casos)` del mes y se guardan como **proporción 0–1** con punto decimal. En el AS-IS, `ruta_digital`, `tasa_uso_portal` y `recogidas_fallidas` quedan vacíos (N/D). Campos: `solicitudes`, `entraron_expediente`, `sobres_enviados`, `dias_expediente_total`, `dias_expediente_promedio`, `llegaron_verificacion`, `devueltas`, `tasa_devolucion`, `cerradas_vencimiento`, `tasa_cierre_vencimiento`, `ruta_digital`, `tasa_uso_portal`, `recogidas_fallidas`.

## 5. Parámetros de la simulación
| ID | Parámetro | Valor | Estado |
|---|---|---|---|
| — | Solicitudes por mes | 1.000 en feria (febrero y noviembre); 600 los otros 10 meses | Declarado (PREG-018, DAT-4) |
| — | Llegan a expediente | 40 % | Declarado (DG-3) |
| — | Días antes del expediente | 4 (crear 1, evaluar 1, analizar 2) | Estimado (fuente, hoja «Tiempos») |
| — | AS-IS: recopilar / escanear / verificar | 5 / 3 / 4 días hábiles, ± 1 día al azar | Estimado (fuente) |
| — | AS-IS: devolución por vuelta | 20 %, hasta 3 devoluciones; cada una repite las 3 actividades | Declarado (PREG-014) |
| — | AS-IS: cierre por vencimiento | 10 % de los que entran | Declarado (PREG-014, AS-07) |
| — | Desembolso | 1 día hábil | Estimado (fuente) |
| D-1 | Reparto del 60 % que no llega a expediente | 1/3 rechazada por Riesgo, 1/3 rechazada en análisis, 1/3 cliente no acepta | **SUPUESTO** (no se preguntó; no afecta los KPI) |
| D-2 | Motivo de la devolución | 50 % vencido, 30 % ilegible, 20 % no cuadra | **SUPUESTO** |
| H-1 | TO-BE: pasan a papel | 5 % por falla del portal + 10 % por intentos agotados = 15 % | **HIPÓTESIS** |
| H-2 | TO-BE digital: cierre por vencimiento | 5 % | **HIPÓTESIS** (priorización) |
| H-3 | TO-BE digital: devolución de Despacho | 5 % | **HIPÓTESIS** (propuesta TO-BE) |
| H-4 | TO-BE digital: carga y validación / verificación / corrección | 2 / 1 / 2 días hábiles | **HIPÓTESIS** |
| H-5 | TO-BE: recogida / escaneo (sigue, PRIO-3) / recogida fallida | 1 / 3 días hábiles; 5 % fallida (+ 2 días) | **HIPÓTESIS** |
| H-6 | TO-BE en papel | Mismos tiempos y tasas que el AS-IS | Declarado (TB-4) |

## 6. Limitaciones
- **L-1:** los días hábiles solo excluyen sábados y domingos; **no** hay festivos.
- **L-2:** el TO-BE es un **escenario estimado**: comparar AS-IS con TO-BE aquí es un *business case*, no una prueba de que el portal funciona.
- **L-3:** para medir el AS-IS real, el sistema de solicitudes tiene inicio y fin **de toda la solicitud** (DAT-2). Para KPI-01 harían falta también la fecha de aceptación y la de salida del sobre; para KPI-02, las devoluciones.
- **L-4:** los casos con 3 devoluciones superan los 40 días (aviso en `registro_calidad.md`). Son posibles en el modelo AS-IS, pero conviene confirmar si en la realidad existen.
