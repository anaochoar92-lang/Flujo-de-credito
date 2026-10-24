# Asunciones del modelo AS-IS v01 — Flujo de crédito

Ninguna es una regla validada. Cada una se debe confirmar con el dueño del proceso.

| ID | Asunción | Elemento | Fuente | Cómo confirmar |
|---|---|---|---|---|
| AS-01 | Tras «Modificar datos del crédito» la solicitud vuelve a «Analizar crédito» **sin** repetir la evaluación de Riesgo | `ACT_005 → ACT_003` | ENT PREG-004 («vuelve a pasar por negocio y análisis») | Pregunta de aclaración (P-02) |
| AS-02 | El plazo de 10 días aplica a la tarea «Recopilar expediente» y se reinicia en cada vuelta del bucle | `TMR_001` | ENT PREG-003 | PREG-013 |
| AS-03 | La respuesta del cliente la registra el Analista; el cliente no se modela como pool | `ACT_004`, `GW_003` | ENT PREG-004 | Canal de comunicación con el cliente |
| AS-04 | En los rechazos no se modela una notificación al cliente | `END_RECH_RIESGO`, `END_RECHAZADA` | No aparece en la fuente | P-03 |
| AS-05 | El cierre automático lo ejecuta el sistema donde se registra la solicitud | `SVC_001` | ENT PREG-003 («de forma automática») | PREG-011 |
