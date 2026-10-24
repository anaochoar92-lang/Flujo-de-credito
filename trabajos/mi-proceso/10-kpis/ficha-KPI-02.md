# Ficha KPI-02

**Nombre:** Tasa de devolución de Despacho **Propietario:** Gerente de crédito **Decisión que habilita:** comprobar si la validación automática (completos, ≤ 20 días, legibles y datos coincidentes) evita las devoluciones; si no, ajustar las reglas de validación con IT y Legal.
**Vínculo al AS-IS / TO-BE (ID ACT/REQ):** AS-IS v02 `GW_006` → `ACT_006`; TO-BE v02 `TB_GW_VERIF` → `TB_ACT_PEDIR`. PROC-010, PROC-TOBE-002, REQ-017, REQ-TOBE-004.
**Definición inequívoca:** porcentaje de solicitudes que llegaron a la verificación de Despacho en el período y que tuvieron **al menos una** devolución o corrección pedida por Despacho.
**Fórmula:** `SUM(devuelta) / SUM(llego_a_verificacion)`.
**Numerador:** solicitudes con `devuelta = 1`. **Denominador:** solicitudes con `llego_a_verificacion = 1`. **Unidad:** %.
**Granularidad:** solicitud-escenario. **Dimensiones:** `mes`, `temporada`, `escenario`, `ruta`. **Periodicidad:** mensual.
**Campos CSV mínimos y tipos:** `solicitud_id`, `mes`, `temporada`, `escenario`, `ruta`, `llego_a_verificacion` (0/1), `devuelta` (0/1), `n_devoluciones` (entero), `motivo_devolucion` (texto: vencido, ilegible, no cuadra).
**Fuente / linaje / método de registro:** TO-BE: Camunda, variable `expedienteOk = false` en `TB_ACT_VERIF` (o `documentacionOk = false` en `ACT_008` por la ruta en papel). AS-IS: **sistema de solicitudes de crédito** (tiene fecha de inicio y fecha de fin, KPI-Q2b) [PENDIENTE ronda 10: si guarda fechas por etapa y estados]; REQ-017 sigue pendiente de si el motivo se registra.
**Línea base:** 20 % (80 de 400 por mes de feria), declarado (PREG-014, DG-3). **Meta TO-BE:** ≤ 5 %. Propuesta pendiente del acuerdo del Gerente. **Evidencia:** entrevista PREG-014, DG-3, PRIO-2.
**Responsable de medición:** IT (historial de Camunda); Despacho registra el motivo. **Regla de calidad:** `devuelta = 1` exige `llego_a_verificacion = 1` y un motivo; `n_devoluciones ≥ devuelta`.
**Visualización en Preset:** barras por `mes` con series `escenario`; barras apiladas por `motivo_devolucion`.
**Limitaciones / riesgos de interpretación:** cuenta solicitudes, no devoluciones: una solicitud devuelta dos veces cuenta una vez (ver `n_devoluciones`). No sumar con KPI-03: las poblaciones se solapan.
