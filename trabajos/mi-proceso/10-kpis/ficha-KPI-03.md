# Ficha KPI-03

**Nombre:** Tasa de cierre por vencimiento **Propietario:** Gerente de crédito **Decisión que habilita:** detectar solicitudes aprobadas que se pierden por los 10 días hábiles; si sube, reforzar el aviso al cliente o la capacidad de Legal en feria.
**Vínculo al AS-IS / TO-BE (ID ACT/REQ):** AS-IS v02 `TMR_001` → `END_VENCIDA`; TO-BE v02 `TMR_T01`, `TMR_T02`, `TMR_001` → `SVC_001` → `END_VENCIDA`. REQ-012, REQ-TOBE-013.
**Definición inequívoca:** porcentaje de solicitudes que entraron a expediente en el mes (cliente acepta sin condiciones) y que se **cerraron automáticamente** por no completar el expediente dentro de los 10 días hábiles.
**Fórmula:** `SUM(cerrada_vencimiento) / SUM(entro_a_expediente)`.
**Numerador:** solicitudes con `cerrada_vencimiento = 1`. **Denominador:** solicitudes con `entro_a_expediente = 1`. **Unidad:** %.
**Granularidad:** solicitud-escenario. **Dimensiones:** `mes` (de aceptación), `temporada`, `escenario`, `ruta`. **Periodicidad:** mensual.
**Campos CSV mínimos y tipos:** `solicitud_id`, `mes`, `temporada`, `escenario`, `ruta`, `entro_a_expediente` (0/1), `cerrada_vencimiento` (0/1), `temporizador` (texto: carga, correccion, papel).
**Fuente / linaje / método de registro:** TO-BE: Camunda, llegada a `END_VENCIDA` y temporizador que la disparó. AS-IS: **sistema de solicitudes de crédito** (tiene fecha de inicio y fecha de fin, KPI-Q2b) [PENDIENTE ronda 10: si guarda fechas por etapa y estados].
**Línea base:** 10 % (40 de 400 por mes de feria), declarado (PREG-014; AS-07 confirmado). **Meta TO-BE:** ≤ 5 %. Propuesta pendiente del acuerdo del Gerente. **Evidencia:** entrevista PREG-014, ronda 7.
**Responsable de medición:** IT. **Regla de calidad:** `cerrada_vencimiento = 1` implica `sobre_enviado = 0`. Los casos se asignan al **mes de aceptación** aunque el cierre ocurra el mes siguiente.
**Visualización en Preset:** barras por `mes` con series `escenario`; corte por `temporizador`.
**Limitaciones / riesgos de interpretación:** el mes recién terminado está incompleto: las solicitudes aceptadas al final del mes aún pueden vencer. Mostrarlo como provisional hasta 10 días hábiles después del cierre de mes.
