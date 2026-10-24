# Catálogo de KPI — Flujo de crédito preaprobado Expomóvil (v01)

**Fecha:** 2026-10-24 · **Skill:** `definir-kpis` · **Fuente:** ronda 9 de `02-analisis/entrevista.md`, `objetivo-proyecto.md`, `07-diagnostico/`, `08-tobe/` (BPMN TO-BE v02 para Camunda 8.10).
**Objetivo clave:** disminuir el tiempo del tramo de expediente, de 12 a 6 días hábiles.
**Dueño de los KPI:** Gerente de crédito (KPI-Q1).

> Las líneas base son **estimaciones declaradas** (Excel de la fuente y entrevista), **no mediciones**. Las metas son **propuestas** pendientes del acuerdo del Gerente de crédito. Comparar AS-IS estimado con TO-BE estimado es un *business case*, no una prueba de causalidad.

## 1. KPI
| ID | KPI | Fórmula | Unidad | Línea base AS-IS (estimada) | Meta TO-BE (propuesta) | Ficha |
|---|---|---|---|---|---|---|
| KPI-01 | Ciclo del expediente | `SUM(dias_habiles_expediente) / COUNT(solicitudes con sobre enviado)` | días hábiles / solicitud | 12 sin devoluciones; **≈ 15** con un 20 % de devoluciones | **≤ 6** | `ficha-KPI-01.md` |
| KPI-02 | Tasa de devolución de Despacho | `SUM(devuelta) / SUM(llego_a_verificacion)` | % | **20 %** (80 de 400) | ≤ 5 % | `ficha-KPI-02.md` |
| KPI-03 | Tasa de cierre por vencimiento | `SUM(cerrada_vencimiento) / SUM(entro_a_expediente)` | % | **10 %** (40 de 400) | ≤ 5 % | `ficha-KPI-03.md` |
| KPI-04 | Uso efectivo del portal | `SUM(ruta_digital_completa) / SUM(entro_a_expediente)` | % | N/D (el portal no existe) | ≥ 80 % | `ficha-KPI-04.md` |

## 2. Métricas de apoyo (no son KPI)
| Métrica | Para qué sirve | Elemento BPMN |
|---|---|---|
| Fallas del portal reportadas por IT y solicitudes desviadas a papel por esa causa | Decisión del Gerente: **exigir a IT la disponibilidad del portal** (KPI-Q1) | `MSG_T01` |
| Intentos promedio por documento y % de documentos con 5 intentos agotados | Ajustar las instrucciones de carga o el margen de 20 días | `TB_SVC_VALIDAR`, `TB_GW_CARGA` |
| % de casos dudosos enviados a Legal | Carga de trabajo de Legal en feria | `TB_ACT_REVISAR` |
| Días de recogida de originales y % de recogidas fallidas | Desempeño del mensajero certificado | `TB_ACT_RECOGER`, `TB_GW_RECOGIDA` |
| Solicitudes que entran a expediente por mes | Volumen. **No es éxito**: solo contexto | Aceptación |

## 3. Reglas comunes
- **Período:** mensual. Dimensión `temporada` = `feria` (febrero y noviembre) o `no feria`. El efecto de la feria se mide comparando temporadas, pero **se conservan todos los meses** (KPI-Q3).
- **Población:** la ruta digital y la ruta en papel entran en el **mismo** cálculo (KPI-Q4). Se muestra además el corte por `ruta` para leer la mezcla.
- **Fin del expediente:** cuando el **sobre sale a Desembolso** (KPI-Q4). En el BPMN TO-BE v02 es la llegada a `TB_GW_MERGE`; en el AS-IS v02, la salida «OK» de `GW_006`.
- **Mes del caso:** el mes en que el cliente **acepta** (inicio del expediente), aunque termine el mes siguiente.
- **Tasas agregadas:** siempre `SUM(eventos) / SUM(casos)`. Nunca promediar ni sumar porcentajes mensuales.
- **Días hábiles:** se cuentan con el calendario laboral del banco. Camunda usa hoy `P14D` (14 días calendario) solo para el temporizador; **el KPI no debe calcularse con esa aproximación**.
- Sin casos en el período → **N/D**, no 0.

## 4. Fuente de datos (KPI-Q2) — PROPUESTA, por confirmar
| Escenario | Fuente propuesta | Estado |
|---|---|---|
| **TO-BE** | **Camunda 8.10** registra solo la fecha y hora de inicio y fin de cada tarea y evento de cada instancia (historial en Operate u Optimize, o exportación). Nadie tiene que digitar fechas | Propuesta. Requiere que IT habilite la exportación del historial |
| **AS-IS** | No se sabe si hoy existe un sistema que guarde la fecha de aceptación, la salida del sobre, las devoluciones y los cierres. Mientras tanto se usan las **estimaciones declaradas** de la fuente y la entrevista | [PENDIENTE KPI-Q2b] |
| **Datos para el taller** | CSV **sintéticos** construidos con esas estimaciones (paso 13, `09-datos/`). Sin datos personales | Siguiente paso |

## 5. Trazabilidad
| KPI | Requisitos | Elementos BPMN (TO-BE v02) |
|---|---|---|
| KPI-01 | REQ-TOBE-002, 009, 011, 012; RN-01 | `TB_SND_ENLACE` → `TB_GW_MERGE` |
| KPI-02 | PROC-TOBE-002; PROC-010; REQ-017 | `TB_GW_VERIF` → `TB_ACT_PEDIR`; `GW_006` → `ACT_006` |
| KPI-03 | REQ-TOBE-013; REQ-012 | `TMR_T01`, `TMR_T02`, `TMR_001` → `END_VENCIDA` |
| KPI-04 | REQ-TOBE-003 a 008, 015 | `TB_GW_CARGA`, `MSG_T01`, `ACT_006` |
