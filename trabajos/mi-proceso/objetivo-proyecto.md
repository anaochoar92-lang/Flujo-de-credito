# Objetivo del proyecto — Flujo de crédito preaprobado

**Fecha:** 2026-10-23 · **Fuente:** entrevistado, ronda 1 (`02-analisis/entrevista.md`).

## Objetivo clave
**Disminuir los tiempos de las actividades de expediente.**

## Línea base según la fuente (estimada, no medida)
Tomada de `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx`, hoja «Tiempos». El origen de estas estimaciones está pendiente (PREG-007).

| Actividad de expediente | Responsable | Días hábiles | % del total (17) |
|---|---|---|---|
| Recopilar expediente (T4) | Legal | 5 | 29 % |
| Escanear documentación (T5) | Legal | 3 | 18 % |
| Despacho y expediente (T6) | Analista de crédito | 4 | 24 % |
| **Total expediente** | | **12** | **71 %** |

A esto se suma el reproceso: cada devolución de Despacho a Legal (G4 → T4) repite T4, T5 y T6, es decir, unos 12 días más.

## Cómo se usa en los pasos siguientes
- **Diagnóstico (paso 09):** foco en el tramo T4 → G3 → T5 → T6 → G4, y en sus dos bucles.
- **Priorización (paso 10):** las oportunidades que reduzcan este tramo pesan más.
- **TO-BE (paso 11):** la mejora elegida debe atacar los tiempos de expediente.
- **KPI (paso 12):** como mínimo, el tiempo del tramo de expediente por solicitud, la tasa de devolución de Despacho a Legal y el porcentaje de solicitudes cerradas por vencimiento de los 10 días. Las metas no se fijan sin acuerdo del dueño del proceso.

## Meta (ronda 4, 2026-10-24)
- **Expediente: de 12 a 6 días hábiles** (PREG-016). Así se interpretó; falta confirmar que la meta es del tramo y no del proceso completo. Con esa meta, el proceso pasaría de 17 a 11 días hábiles.
- **Medio propuesto (TO-BE):** página web donde el **cliente carga sus documentos** y el concesionario deja de ser intermediario (PREG-017).
- **Segundo dolor del cliente:** no saber el estado de su solicitud (CV-3).
- **Volumen de ejemplo:** 1.000 solicitudes por mes de feria (febrero y noviembre), unas 2.000 al año (PREG-018).
- **Restricción:** los originales deben llegar en físico a Desembolso (RN-01).
