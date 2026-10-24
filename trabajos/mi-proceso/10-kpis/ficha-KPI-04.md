# Ficha KPI-04

**Nombre:** Uso efectivo del portal **Propietario:** Gerente de crédito **Decisión que habilita:** **exigir a IT la disponibilidad del portal** (KPI-Q1) y decidir si el cliente necesita más ayuda para cargar documentos.
**Vínculo al AS-IS / TO-BE (ID ACT/REQ):** TO-BE v02 `SUB_T01`, `TB_GW_CARGA` («agotado» → `ACT_006`), `MSG_T01` → `ACT_006`. REQ-TOBE-003 a 008, REQ-TOBE-015.
**Definición inequívoca:** porcentaje de solicitudes que entraron a expediente en el mes y que **no pasaron a la ruta en papel** (ni por falla del portal reportada por IT ni por 5 intentos agotados en un documento).
**Fórmula:** `SUM(ruta_digital_completa) / SUM(entro_a_expediente)`.
**Numerador:** solicitudes con `ruta = "digital"`. **Denominador:** solicitudes con `entro_a_expediente = 1`. **Unidad:** %.
**Granularidad:** solicitud-escenario (solo TO-BE). **Dimensiones:** `mes`, `temporada`, `motivo_papel` (falla portal, intentos agotados). **Periodicidad:** mensual.
**Campos CSV mínimos y tipos:** `solicitud_id`, `mes`, `temporada`, `escenario`, `entro_a_expediente` (0/1), `ruta` (texto: digital, papel), `motivo_papel` (texto, vacío si digital), `recogida_fallida` (0/1).
**Fuente / linaje / método de registro:** Camunda: salida de `TB_GW_CARGA` con `resultadoValidacion = "agotado"` o disparo de `MSG_T01`. IT registra la falla (TB-9).
**Línea base:** N/D: el portal no existe en el AS-IS. **Meta TO-BE:** ≥ 80 %. Propuesta pendiente del acuerdo del Gerente. **Evidencia:** PRIO-1, TB-3, TB-4, TB-9.
**Responsable de medición:** IT. **Regla de calidad:** si `ruta = "papel"`, `motivo_papel` no puede estar vacío.
**Visualización en Preset:** número grande con el % del mes; barras por `motivo_papel`.
**Limitaciones / riesgos de interpretación:** una recogida fallida (`TB_GW_RECOGIDA` → Legal recopila originales) **no** cuenta como ruta en papel, porque los documentos ya se validaron en digital; se mide aparte con `recogida_fallida`. Una solicitud cerrada por vencimiento dentro del portal cuenta en el denominador y no en el numerador.
