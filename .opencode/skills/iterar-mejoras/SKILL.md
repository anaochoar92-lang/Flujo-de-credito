---
name: iterar-mejoras
description: "Reincorporar evidencia de tableros al SOP, requisitos EARS y BPMN TO-BE sin destruir versiones"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Ciclo iterativo
1. Revisar observaciones de un tablero o entrevista, no inventar hallazgos empíricos.
2. Preguntar: ¿qué KPI se desvió?, ¿qué causa sugiere?, ¿qué etapa BPMN se relaciona?, ¿qué evidencia adicional confirmaría esa causa?
3. Describir cambio propuesto con decisión, riesgo, impacto, responsables, necesidad de aprobación.
4. Si se aprueba, actualizar `08-tobe` con nueva versión; usar skills de la fase 1 `redactar-ears`, `reconciliar-bpmn`, `auditar-bpmn`. No sobrescribir versión anterior ni perder IDs rastreables.
5. Actualizar fichas KPI, dataset/CSV si cambia definición o granularidad, ROI, widgets y captura; mantener log de cambios `13-retroalimentacion/bitacora.md`.
6. Volver a preguntar si AS-IS necesita medirse más antes de defender una mejora.

## Criterio de éxito
Trazabilidad continua desde SOP → AS-IS → causa raíz → TO-BE/EARS/BPMN → campo de dato → KPI → gráfico → decisión → revisión.
