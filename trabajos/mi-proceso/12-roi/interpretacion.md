# Interpretación del ROI — Flujo de crédito preaprobado (TO-BE, SINTÉTICO)

**Fecha:** 2026-10-24 · **Skill:** `calcular-roi` · **Excel:** `12-roi/Modelo_ROI_Flujo_Credito.xlsx` (hojas `LEEME`, `Supuestos`, `Conteos`, `ROI`, `FlujoMensual`).

> **Un ROI con datos sintéticos no valida la inversión.** Sirve para ver qué variables mueven el resultado y qué hay que medir o confirmar. Todas las cifras están en **pesos dominicanos (RD$)**.

## 1. Variables (hoja `Supuestos`, celdas amarillas editables)
| Variable | Conservador | Base | Optimista | Estado |
|---|---|---|---|---|
| Salario mínimo, empresa grande | RD$ 29.988/mes | igual | igual | Declarado (ROI-1). Res. CNS-01-2025, vigente desde el 01-02-2026 |
| Factor de costo del empleador (TSS + regalía) | 1,25 | 1,25 | 1,25 | SUPUESTO S-1 |
| Jornada | 23,83 días × 8 h | igual | igual | Declarado (ROI-2) |
| **Costo por hora** | **RD$ 196,64** | igual | igual | Fórmula |
| Horas de trabajo real por ejecución (recopilar / escanear / verificar en papel) | 0,75 / 0,5 / 0,5 | 1,5 / 1 / 1 | 2,25 / 1,5 / 1,5 | HIPÓTESIS H-R1 |
| Horas TO-BE (verificar digital / pedir corrección / escanear originales) | 0,25 / 0,125 / 0,5 | 0,5 / 0,25 / 1 | 0,75 / 0,375 / 1,5 | HIPÓTESIS H-R1 |
| Costo por recogida del mensajero | RD$ 500 | RD$ 400 | RD$ 300 | SUPUESTO S-2 (ROI-3) |
| Inversión inicial (portal + validación, IT del banco) | RD$ 6.000.000 | RD$ 3.500.000 | RD$ 2.000.000 | SUPUESTO S-3 (ROI-3) |
| Mantenimiento anual | 25 % | 20 % | 15 % de la inversión | SUPUESTO S-4 (ROI-3) |

**Sobre ROI-2 («ambas áreas trabajan 8 horas diarias»):** se usó para el costo por hora. Los días de cada actividad (5, 3 y 4) **no** se convirtieron en 8 horas de trabajo por expediente: con 400 expedientes al mes saldrían unas 38.000 horas, unas 200 personas solo en Legal y Despacho. Esos días incluyen mucha espera. Por eso las horas de trabajo real por expediente son la hipótesis H-R1, con rangos.

## 2. Ecuaciones
| Concepto | En palabras | En Excel (hoja `ROI`, columna D = base) |
|---|---|---|
| Horas por escenario | Σ ejecuciones de cada actividad × horas por ejecución | `=SUMPRODUCT((Conteos!$C$4:$C$27="AS-IS")*(Conteos!$B$4:$B$27="feria")*(Conteos!$D$4:$D$27*Supuestos!D$11+…))` |
| Horas ahorradas en feria | Horas AS-IS − horas TO-BE, solo febrero y noviembre | `=D5-D6` |
| Personal temporal evitado | Horas ahorradas ÷ (23,83 × 8) | `=D7/(Supuestos!D6*Supuestos!D7)` |
| **Ahorro en caja** | Horas ahorradas en feria × costo por hora (ROI-4) | `=D7*Supuestos!D8` |
| Capacidad liberada (no es caja) | Horas ahorradas fuera de feria × costo por hora | `=D13*Supuestos!D8` |
| Opex | Recogidas × costo por recogida + mantenimiento | `=D17+D18` |
| **ROI año 1** | (ahorro en caja − opex − inversión) ÷ (opex + inversión) | `=(D9-D19-D20)/(D19+D20)` |
| Meses de recuperación | Inversión ÷ beneficio neto mensual, si es positivo | `=IF(D22>0,D20/(D22/12),"No se recupera")` |

## 3. Resultados (año 1)
| Concepto | Conservador | Base | Optimista |
|---|---|---|---|
| Horas ahorradas en feria | 894 | 1.788 | 2.682 |
| Personal temporal evitado (personas-mes) | 4,7 | 9,4 | 14,1 |
| **Ahorro en caja** | RD$ 175.809 | **RD$ 351.619** | RD$ 527.428 |
| Capacidad liberada fuera de feria (no es caja) | RD$ 511.083 | RD$ 1.022.166 | RD$ 1.533.249 |
| Mensajero certificado (2.550 recogidas) | RD$ 1.275.000 | RD$ 1.020.000 | RD$ 765.000 |
| Mantenimiento | RD$ 1.500.000 | RD$ 700.000 | RD$ 300.000 |
| Beneficio neto operativo anual (caja) | −RD$ 2.599.191 | **−RD$ 1.368.381** | −RD$ 537.572 |
| **ROI año 1 (caja)** | −98 % | **−93 %** | −83 % |
| Meses de recuperación | No se recupera | No se recupera | No se recupera |
| ROI si la capacidad se monetizara (referencia, NO caja) | −92 % | −74 % | −33 % |
| **No incluido:** créditos que dejan de perderse por vencimiento | 153 al año | 153 | 153 |

## 4. Lectura
1. **Con el ahorro de personal temporal solo, el TO-BE no se paga.** Es un resultado útil: el ahorro en feria (≈ RD$ 350.000 en el escenario base) no alcanza ni para el **mensajero**, que es un costo nuevo (hoy el concesionario lleva los documentos), ni para el mantenimiento.
2. **El costo más pesado es el mensajero**: unas 2.550 recogidas al año. Cada RD$ 100 menos por recogida mejora el resultado en RD$ 255.000 al año.
3. **El valor grande no está en las horas, sino en los créditos que no se pierden.** El TO-BE evita que se cierren por vencimiento unas **153 solicitudes al año** que ya estaban aprobadas. Con el escenario base:
   - si cada crédito deja al banco **más de ≈ RD$ 8.950** de margen, la operación anual ya da positivo ((1.720.000 − 351.619) ÷ 153);
   - si deja **más de ≈ RD$ 31.800**, la inversión se recupera en el primer año ((1.720.000 + 3.500.000 − 351.619) ÷ 153).
4. Las horas liberadas fuera de feria valen ≈ RD$ 1 millón al año, pero **no son caja**: el personal fijo sigue cobrando. Solo serían dinero si se reduce gasto o se atienden más solicitudes con el mismo equipo.
5. El beneficio para el cliente (saber el estado y cargar documentos sin intermediarios) no está monetizado.

## 5. Decisiones que habilita
- **No aprobar la inversión solo por ahorro de personal.** El caso de negocio debe incluir el margen de los créditos que hoy se pierden (pedir el dato a Finanzas).
- **Negociar el mensajero**, o evaluar que el cliente entregue los originales en una oficina, como alternativa más barata en meses sin feria.
- **Medir antes de invertir** (KPI-01 a KPI-04): sobre todo, la tasa real de cierres por vencimiento y las horas reales de trabajo por expediente.

## 6. Cómo regenerar
```
node trabajos/mi-proceso/12-roi/conteos.js
powershell -ExecutionPolicy Bypass -File trabajos/mi-proceso/12-roi/crear_excel_roi.ps1
```
Requiere Excel instalado. Los conteos salen de `09-datos/` (sintéticos).

Fuentes del salario mínimo: [Ministerio de Trabajo vía Presidencia](https://presidencia.gob.do/noticias/ministerio-de-trabajo-llama-empresarios-cumplir-con-el-pago-del-aumento-del-8-del-salario) · [EY: salario mínimo 2026](https://www.ey.com/es_ce/technical/tax/tax-alerts/republica-dominicana-salario-minimo-2026).
