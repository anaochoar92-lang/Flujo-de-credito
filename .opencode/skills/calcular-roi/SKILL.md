---
name: calcular-roi
description: "Traducir métricas a fórmulas Excel y ROI trazable, con inversión, mantenimiento y supuestos"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Objetivo
Interpretar ecuaciones y sensibilidad. Leer `datos/Modelo_KPI_ROI_Reexpedicion.xlsx` y `docs/diccionario-kpis-y-ecuaciones.md`.

## Protocolo
1. Abrir Excel con el participante. Señalar hoja `Supuestos` (cifras editables), `Base_Casos`, `Comparacion` (AVERAGE/SUMIF), `ROI` y `FlujoMensual`.
2. Hacer máximo cuatro preguntas: costo hora realmente evitable, volumen anual representativo, costo efectivo de errores, costo implementación + mantenimiento. Si no se conocen, mantener escenario hipotético y documentar rango de sensibilidad.
3. Revisar ecuaciones: ahorro_horas_por_caso = media AS-IS - media TO-BE; beneficio_bruto = casos × (ahorro_horas × costo_hora + reducción_error × costo_error); ROI año1 = (beneficio_bruto - mantenimiento - inversión)/(mantenimiento + inversión); payback condicional.
4. Advertir sin excepción: capacidad liberada **no** es ahorro financiero materializado si no existe reducción de gasto o producción adicional monetizable. Preparar dos cifras cuando sea posible: capacidad vs caja.
5. Entregar `12-roi/interpretacion.md`: variables, ecuaciones en notación humana y Excel, escenarios optimista/base/conservador y decisiones.

## Resultados
No validar una inversión por ROI sintético. Mostrar tasas en %, dinero COP, duración meses. ROI negativo también es resultado útil.
