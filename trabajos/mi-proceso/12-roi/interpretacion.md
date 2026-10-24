# Interpretación del ROI — Flujo de crédito preaprobado (TO-BE, SINTÉTICO) · v02

**Fecha:** 2026-10-24 · **Skill:** `calcular-roi` · **Excel:** `12-roi/Modelo_ROI_Flujo_Credito.xlsx` (hojas `LEEME`, `Opciones`, `ROI`, `Supuestos`, `Conteos`, `FlujoMensual`).
**Modelo adoptado (ronda 12): Opción 3**, versión mínima del portal + sin mensajero + tiempo liberado convertido en caja. La v01 (portal completo con mensajero, ROI −93 %) queda como «Modelo original» en la hoja `Opciones` y en el historial de git.

> **Un ROI con datos sintéticos no valida la inversión.** Sirve para comparar decisiones y ver qué hay que medir. Cifras en **pesos dominicanos (RD$)**.

## 1. Decisiones de la ronda 12
| Opción | Decisión | Qué cambia en el modelo |
|---|---|---|
| 1 | **Sin mensajero:** el cliente entrega los originales en una sucursal o en el stand de la feria | Costo del mensajero = 0 (`Supuestos` fila 23) |
| 2 | **Convertir el tiempo liberado en caja:** fuera de feria se liberan ≈ 520 h/mes (≈ 2,7 personas); no se reponen esos puestos cuando haya salidas, o se reasignan a áreas que hoy contratan | El valor del tiempo liberado cuenta como caja (`Supuestos` fila 24) |
| 3 | **Versión mínima del portal:** sobre Camunda 8.10 (ya preparado), sus formularios y la banca en línea; validación con reglas simples (fecha, documentos completos, datos que coinciden) | Inversión RD$ 1.000.000 y mantenimiento 15 % (`Supuestos` filas 20 y 21) |

## 2. Comparación de opciones (hoja `Opciones`, escenario base)
| | Modelo original | Opción 1 | Opción 2 | **Opción 3 (adoptada)** |
|---|---|---|---|---|
| Beneficio en caja | RD$ 351.619 | RD$ 351.619 | RD$ 1.373.785 | **RD$ 1.373.785** |
| Mensajero | RD$ 1.020.000 | 0 | 0 | **0** |
| Mantenimiento | RD$ 700.000 | RD$ 700.000 | RD$ 700.000 | **RD$ 150.000** |
| Inversión | RD$ 3.500.000 | RD$ 3.500.000 | RD$ 3.500.000 | **RD$ 1.000.000** |
| Beneficio neto anual | −RD$ 1.368.381 | −RD$ 348.381 | RD$ 673.785 | **RD$ 1.223.785** |
| **ROI año 1** | −93,3 % | −91,6 % | −67,3 % | **+19,5 %** |
| Meses de recuperación | No se recupera | No se recupera | 62 | **≈ 10** |

## 3. Sensibilidad del modelo adoptado (hoja `ROI`)
| | Conservador | Base | Optimista |
|---|---|---|---|
| Horas de trabajo por actividad | la mitad | H-R1 | 1,5 veces |
| % del tiempo liberado convertido en caja | 50 % | 100 % | 100 % |
| Inversión / mantenimiento | RD$ 1,5 M / 20 % | RD$ 1 M / 15 % | RD$ 0,7 M / 10 % |
| Beneficio total en caja | RD$ 431.351 | RD$ 1.373.785 | RD$ 2.060.677 |
| Beneficio neto anual | RD$ 131.351 | RD$ 1.223.785 | RD$ 1.990.677 |
| **ROI año 1** | **−76,0 %** | **+19,5 %** | **+167,6 %** |
| Meses de recuperación | 137 | 9,8 | 4,2 |
| ROI si no se ejecuta la Opción 2 (referencia) | −90,2 % | −69,4 % | −31,5 % |

**Flujo mensual (base):** el acumulado pasa de −RD$ 1.000.000 (mes 0) a **+RD$ 223.785** al mes 12.

## 4. Lectura
1. **El ROI es positivo en el escenario base**, pero **no en el conservador**. El resultado depende sobre todo de dos cosas que hoy son supuestos: las horas reales de trabajo por expediente y que la gerencia **de verdad** no reponga los ≈ 2,7 puestos.
2. **La Opción 2 es la que más mueve el resultado.** Sin ella, incluso con la versión mínima, el ROI base es −69 %: el ahorro en personal temporal de feria no basta.
3. **Quitar el mensajero** ahorra RD$ 1,02 millones al año, pero traslada el esfuerzo al cliente. Hay que vigilar KPI-01: si la entrega en sucursal tarda más que la recogida, la rama de originales puede pasar de 4 días.
4. **El beneficio más grande sigue sin contarse:** ≈ 153 créditos al año que dejan de perderse por vencimiento. Con cualquier margen por crédito, el ROI sube más.
5. Las horas liberadas son caja **solo** si se ejecuta la decisión de no reponer o reasignar puestos. Si no, vuelven a ser capacidad.

## 5. Decisiones que habilita
- **Aprobar una prueba piloto** de la versión mínima en la feria de febrero, no el portal completo.
- **Comprometer la Opción 2 por escrito** (Gerente de crédito y Recursos Humanos): sin ella el caso no se sostiene.
- **Medir en el piloto** KPI-01 a KPI-04 y las horas reales por expediente. Con esos datos se reemplazan las hipótesis H-R1 y S-3b y se decide si escalar.

## 6. Pendiente por coherencia
El BPMN TO-BE v02, los requisitos (PROC-TOBE-003, REQ-TOBE-009 y 010) y los datos sintéticos **todavía modelan el mensajero a domicilio**. Si se confirma la Opción 1, hay que actualizarlos: la recogida pasa a «el cliente entrega los originales en sucursal». El BPMN v02 es el que Sergio preparó para Camunda 8.10, así que el cambio debe hacerse en una versión nueva.

## 7. Variables y ecuaciones
| Concepto | En palabras | En Excel (hoja `ROI`, columna D = base) |
|---|---|---|
| Costo por hora | Salario mínimo × 1,25 ÷ (23,83 × 8) = RD$ 196,64 | `=D4*D5/(D6*D7)` (hoja `Supuestos`) |
| Horas por escenario | Σ ejecuciones de cada actividad × horas por ejecución | `=SUMPRODUCT((Conteos!$C$4:$C$27="AS-IS")*(Conteos!$B$4:$B$27="feria")*(…))` |
| Ahorro de temporales | Horas ahorradas en feria × costo por hora | `=D7*Supuestos!D8` |
| Tiempo convertido en caja | Horas liberadas fuera de feria × costo por hora × % convertido | `=D14*Supuestos!D24` |
| Mensajero | Recogidas × costo × (1 si hay mensajero) | `=D16*Supuestos!D19` |
| **ROI año 1** | (beneficio en caja − opex − inversión) ÷ (opex + inversión) | `=(D21-D19-D20)/(D19+D20)` |
| Meses de recuperación | Inversión ÷ beneficio neto mensual | `=IF(D22>0,D20/(D22/12),"No se recupera")` |

Los supuestos de horas (H-R1), costo del empleador (S-1), mensajero (S-2), inversión y mantenimiento (S-3b, S-4b) y conversión en el conservador (S-5) están en la hoja `Supuestos`, en celdas amarillas editables.

## 8. Cómo regenerar
```
node trabajos/mi-proceso/12-roi/conteos.js
powershell -ExecutionPolicy Bypass -File trabajos/mi-proceso/12-roi/crear_excel_roi.ps1
```
Requiere Excel instalado.

Fuentes del salario mínimo (RD$ 29.988, empresas grandes, desde el 01-02-2026): [Ministerio de Trabajo vía Presidencia](https://presidencia.gob.do/noticias/ministerio-de-trabajo-llama-empresarios-cumplir-con-el-pago-del-aumento-del-8-del-salario) · [EY: salario mínimo 2026](https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026).
