# Catálogo de KPI, fórmula, fuente y aplicación

Todos los indicadores siguientes son **propuestas para el ejemplo SOP de reexpedición**, no cifras propias de la SDP. Cada estudiante debe modificar o descartar KPI que no correspondan a su proceso.

| ID | KPI | Numerador / fórmula | Denominador | Unidad | Datos necesarios | Responsabilidad / decisión | Widget |
|---|---|---|---|---|---|---|---|
| KPI-01 | Tiempo humano medio | `SUM(horas_humanas)` | `COUNT(DISTINCT id_caso)` | horas/caso | Inicio-fin de trabajo humano | Líder del proceso: dimensionar capacidad | Barra AS-IS/TO-BE |
| KPI-02 | Tiempo de ciclo medio | `SUM(horas_ciclo)` | `COUNT(DISTINCT id_caso)` | horas/caso | marcas de inicio/fin | Líder: acuerdos de servicio | Línea mes |
| KPI-03 | Espera media | `SUM(horas_espera)` | `COUNT(DISTINCT id_caso)` | horas/caso | intervalos inactivos | Líder: botella de espera | Barra |
| KPI-04 | Tasa de error | `SUM(error)` | `COUNT(DISTINCT id_caso)` | % (proporción ×100) | bandera error 0/1 | Calidad: controles | Barra |
| KPI-05 | Tasa de reproceso | `SUM(reproceso)` | `COUNT(DISTINCT id_caso)` | % | bandera reproceso 0/1 | Calidad: 5 porqués | Barra |
| KPI-06 | Automatización efectiva | `SUM(automatizado)` | `COUNT(DISTINCT id_caso)` | % | casos con al menos una etapa sin intervención | Gestor de automatización | Big number |
| KPI-07 | Horas humanas evitadas | `AVG(h_as_is)-AVG(h_to_be)` | Por caso (cohortes equiparables) | horas/caso | dos escenarios comparables | Finanzas/operaciones | Big number |
| KPI-08 | Ahorro monetizable | `casos_año × horas_ahorradas/caso × costo_hora` | no aplica | COP/año | volumen, costo incremental o costo evitado | Finanzas: ahorro vs capacidad | Big number |
| KPI-09 | Costos de error evitados | `casos_año × (tasa_error_as_is - tasa_error_to_be) × costo_error` | no aplica | COP/año | tasas, costo por error | Calidad/finanzas | Big number |
| KPI-10 | ROI del primer año | `(beneficios_1er_año - opex_1er_año - inversion_inicial) / (opex_1er_año + inversion_inicial)` | inversión + opex | % | costos de implementación + beneficios | Sponsor: conveniencia financiera | Big number |
| KPI-11 | Meses recuperación | `inversion_inicial / ((beneficio_anual-opex_anual)/12)` | no aplica | meses | flujo estimado | Sponsor | Big number |

**Definiciones operativas:** `horas_ciclo=horas_humanas+horas_espera` es una simplificación de la simulación, no una ley universal (pueden existir trabajos paralelos). `automatizado` es un marcador didáctico, NO equivale a porcentaje de actividades automatizadas. `error` y `reproceso` pueden solaparse y NO deben sumarse como si fueran poblaciones disjuntas. 

## Reglas de modelado analítico
- Primero preguntar de dónde saldrá el dato, quién lo registrará, fecha, condición de captura y control de calidad.
- Evitar dividir entre cero; para casos reales sin observaciones mostrar **N/D**.
- Tasas agregadas: `SUM(errores)/SUM(casos)`; jamás `SUM(tasa_error)`.
- `mes` es de inicio del caso y una dimensión de texto; son necesarios cuidados especiales si un ciclo cruza de mes.
- Datos por actividad son de granularidad **actividad-caso-escenario**; `casos.csv` tiene granularidad **caso-escenario**; evitar join que duplique costos y volúmenes.
- ROI no prueba causalidad, y una reducción de horas no necesariamente libera presupuesto.
- Segmentar por canal, prioridad y tipo de trámite solo si se recolectan esos campos y hay muestra suficiente.

## Comparación entre implementación y hipótesis
`AS-IS observado → TO-BE estimado` = **business case**, no evaluación causal. `AS-IS observado → TO-BE observado` = comparación que todavía requiere vigilar estacionalidad, mezcla de casos y sesgos.
