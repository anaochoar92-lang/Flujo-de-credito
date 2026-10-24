# Interpretación del ROI — Flujo de crédito preaprobado (TO-BE, SINTÉTICO) · v02

**Fecha:** 2026-10-24 · **Skill:** `calcular-roi` · **Excel:** `12-roi/Modelo_ROI_Flujo_Credito.xlsx` (hojas `LEEME`, `Opciones`, `ROI`, `Supuestos`, `Conteos`, `FlujoMensual`).
**Modelo adoptado (rondas 12 y 13): Opción 3**, versión mínima del portal + mensajero de un tercero cobrado al cliente como comisión + tiempo liberado convertido en caja. La v01 (portal completo con mensajero, ROI −93 %) queda como «Modelo original» en la hoja `Opciones` y en el historial de git.

> **Un ROI con datos sintéticos no valida la inversión.** Sirve para comparar decisiones y ver qué hay que medir. Cifras en **pesos dominicanos (RD$)**.

## 1. Decisiones de la ronda 12
| Opción | Decisión | Qué cambia en el modelo |
|---|---|---|
| 1 | **Mensajero de un tercero, cobrado al cliente** como comisión del servicio (ronda 13, ROI-7). La recogida a domicilio se mantiene: acorta tiempos y evita perder créditos | Costo del mensajero para el banco = 0 (`Supuestos` fila 23). Las 2.550 recogidas siguen en el proceso |
| 2 | **Convertir el tiempo liberado en caja:** fuera de feria se liberan ≈ 520 h/mes (≈ 2,7 personas); no se reponen esos puestos cuando haya salidas, o se reasignan a áreas que hoy contratan | El valor del tiempo liberado cuenta como caja (`Supuestos` fila 24) |
| 3 | **Versión mínima del portal:** sobre Camunda 8.10 (ya preparado), sus formularios y la banca en línea; validación con reglas simples (fecha, documentos completos, datos que coinciden) | Inversión RD$ 1.000.000 y mantenimiento 15 % (`Supuestos` filas 20 y 21) |

## 2. Comparación de opciones (hoja `Opciones`, escenario base)
| | Modelo original | Opción 1 | Opción 2 | **Opción 3 (adoptada)** |
|---|---|---|---|---|
| Beneficio en caja | RD$ 335.987 | RD$ 335.987 | RD$ 1.342.177 | **RD$ 1.342.177** |
| Mensajero (costo para el banco) | RD$ 1.072.800 | 0 | 0 | **0** |
| Mantenimiento | RD$ 700.000 | RD$ 700.000 | RD$ 700.000 | **RD$ 150.000** |
| Inversión | RD$ 3.500.000 | RD$ 3.500.000 | RD$ 3.500.000 | **RD$ 1.000.000** |
| Beneficio neto anual | −RD$ 1.436.813 | −RD$ 364.013 | RD$ 642.177 | **RD$ 1.192.177** |
| **ROI año 1** | −93,6 % | −92,0 % | −68,0 % | **+16,7 %** |
| Meses de recuperación | No se recupera | No se recupera | 65 | **≈ 10** |

Cifras de la ronda 14: datos regenerados con las medidas 1 y 2 (H-2b) y con una secuencia aleatoria propia por escenario (ver `09-datos/diccionario.md`).

## 3. Sensibilidad del modelo adoptado (hoja `ROI`)
| | Conservador | Base | Optimista |
|---|---|---|---|
| Horas de trabajo por actividad | la mitad | H-R1 | 1,5 veces |
| % del tiempo liberado convertido en caja | 50 % | 100 % | 100 % |
| Inversión / mantenimiento | RD$ 1,5 M / 20 % | RD$ 1 M / 15 % | RD$ 0,7 M / 10 % |
| Beneficio total en caja | RD$ 419.541 | RD$ 1.342.177 | RD$ 2.013.265 |
| Beneficio neto anual | RD$ 119.541 | RD$ 1.192.177 | RD$ 1.943.265 |
| **ROI año 1** | **−76,7 %** | **+16,7 %** | **+161,5 %** |
| Meses de recuperación | 151 | 10,1 | 4,3 |
| ROI si no se ejecuta la Opción 2 (referencia) | −90,7 % | −70,8 % | −34,5 % |

**Flujo mensual (base):** el acumulado pasa de −RD$ 1.000.000 (mes 0) a **+RD$ 192.177** al mes 12.

## 3b. Medidas 1 y 2 contra la pérdida de créditos (ronda 14)
| Créditos cerrados por vencimiento al año | AS-IS | TO-BE sin medidas | **TO-BE con medidas 1 y 2** |
|---|---|---|---|
| En el portal (el cliente no carga en 10 días) | — | 111 | **54** |
| En papel por intentos agotados | — | 26 | 26 |
| En papel por falla del portal | — | 11 | 11 |
| En papel (AS-IS) | 336 | — | — |
| **Total** | **336** | **148** | **91** |
| **Créditos que dejan de perderse frente al AS-IS** | | 188 | **245** |

Las medidas (recordatorios los días hábiles 3 y 6, llamada el día 8, lista de documentos al crear la solicitud y carga asistida en el stand) recuperan **≈ 57 créditos más al año**. Es la **HIPÓTESIS H-2b**: la mitad de los cierres en el portal se evitan.
**Decisión (ronda 15, ROI-9):** el ROI se mantiene solo con el ahorro de personal; los créditos recuperados se reportan como **beneficio aparte, no monetizado** (fila 28 de la hoja `ROI`).
Efecto en el ROI en caja: **ninguno directo**, porque el margen por crédito no se cuenta (ROI-5). Al contrario, cada crédito que no se pierde agrega trabajo de verificación y escaneo, y el ahorro de horas baja un poco. El costo de las llamadas y de la asistencia en el stand tampoco se modeló: se estima menor a RD$ 20.000 al año (≈ 0,25 h por llamada, unas 270 llamadas).

## 4. Lectura
1. **El ROI es positivo en el escenario base**, pero **no en el conservador**. El resultado depende sobre todo de dos cosas que hoy son supuestos: las horas reales de trabajo por expediente y que la gerencia **de verdad** no reponga los ≈ 2,7 puestos.
2. **La Opción 2 es la que más mueve el resultado.** Sin ella, incluso con la versión mínima, el ROI base es −69 %: el ahorro en personal temporal de feria no basta.
3. **Cobrar el mensajero al cliente** ahorra al banco ≈ RD$ 1,07 millones al año sin quitar la recogida a domicilio, que es la que acorta la rama de originales (≈ 4 días) y evita cierres por vencimiento. Riesgo: la comisión puede desanimar a algunos clientes; conviene ofrecer como respaldo gratuito la entrega de originales en sucursal y medir cuántos la eligen.
4. **El beneficio más grande sigue sin contarse:** ≈ 245 créditos al año que dejan de perderse por vencimiento (con las medidas 1 y 2). Con cualquier margen por crédito, el ROI sube más.
5. Las horas liberadas son caja **solo** si se ejecuta la decisión de no reponer o reasignar puestos. Si no, vuelven a ser capacidad.

## 5. Decisiones que habilita
- **Aprobar una prueba piloto** de la versión mínima en la feria de febrero, no el portal completo.
- **Comprometer la Opción 2 por escrito** (Gerente de crédito y Recursos Humanos): sin ella el caso no se sostiene.
- **Medir en el piloto** KPI-01 a KPI-04 y las horas reales por expediente. Con esos datos se reemplazan las hipótesis H-R1 y S-3b y se decide si escalar.

## 6. Coherencia con el resto del proyecto
Como el mensajero se mantiene (ronda 13), **el BPMN TO-BE v02 y los datos sintéticos no cambian**. En los requisitos se añadió REQ-TOBE-016 (comisión de recogida cobrada al cliente) y se ajustó PROC-TOBE-003 (mensajero de un tercero).

## 7. Variables y ecuaciones
| Concepto | En palabras | En Excel (hoja `ROI`, columna D = base) |
|---|---|---|
| Costo por hora | Salario mínimo × 1,25 ÷ (23,83 × 8) = RD$ 196,64 | `=D4*D5/(D6*D7)` (hoja `Supuestos`) |
| Horas por escenario | Σ ejecuciones de cada actividad × horas por ejecución | `=SUMPRODUCT((Conteos!$C$4:$C$27="AS-IS")*(Conteos!$B$4:$B$27="feria")*(…))` |
| Ahorro de temporales | Horas ahorradas en feria × costo por hora | `=D7*Supuestos!D8` |
| Tiempo convertido en caja | Horas liberadas fuera de feria × costo por hora × % convertido | `=D14*Supuestos!D24` |
| Mensajero (costo para el banco) | Recogidas × costo × (1 si lo paga el banco; 0 si se cobra al cliente) | `=D16*Supuestos!D19*Supuestos!D23` |
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
