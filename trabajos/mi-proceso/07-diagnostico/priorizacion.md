# Priorización de oportunidades — Flujo de crédito preaprobado Expomóvil

**Fecha:** 2026-10-24 · **Skill:** `priorizar-automatizacion` · **Base:** `diagnostico.md`, `cadena-valor.md`, `objetivo-proyecto.md`.
**Meta:** expediente de 12 a **6 días hábiles**. **Restricción:** originales en físico a Desembolso (RN-01).

## 1. Matriz (didáctica, NO oficial)
Pesos propuestos por el kit, revisables por el grupo: impacto en el cliente 25 %, volumen 20 %, urgencia 15 %, factibilidad 20 % (incluye la complejidad técnica invertida) y reducción de riesgos 20 %. Puntajes de 1 a 5, asignados por el modelo: son **hipótesis** para discutir, no mediciones.

| ID | Oportunidad | Cliente | Volumen | Urgencia | Factib. | Riesgo | **Puntaje** | Días ahorrados (hipótesis) |
|---|---|---|---|---|---|---|---|---|
| OPP-02 | Validación automática de completitud y vigencia al cargar | 4 | 4 | 4 | 4 | 5 | **4,20** | ≈ 3 en promedio (quita gran parte del reproceso) |
| OPP-01 | Portal web de carga de documentos por el cliente | 5 | 4 | 5 | 3 | 3 | **4,00** | 3 a 5 (espera del cliente y escaneo) |
| OPP-03 | Consulta del estado en la web y avisos | 4 | 5 | 3 | 4 | 2 | **3,65** | 0 (experiencia del cliente) |
| OPP-04 | Recogida de originales a domicilio, en paralelo | 3 | 4 | 4 | 4 | 3 | **3,55** | ≈ 2 (traslado fuera de la ruta crítica) |
| OPP-05 | RPA para el escaneo actual | 2 | 4 | 3 | 3 | 2 | **2,75** | ≈ 1 |

Volumen de referencia: 400 expedientes por mes de feria (800 al año), 80 devoluciones y 40 cierres por vencimiento (datos de ejemplo).

## 2. Lectura
- **OPP-02 y OPP-01 se necesitan entre sí.** La validación automática solo es posible si los documentos llegan en digital (OPP-01). Y la web sin validación seguiría dejando pasar documentos que se vencen antes de Despacho.
- **OPP-04 es la que permite cumplir RN-01 sin volver a la ruta lenta.** El original viaja mientras se verifica la copia digital, no después.
- **OPP-03 no reduce días**, pero ataca el dolor principal del cliente (CV-3). Es de bajo costo una vez que exista el portal.
- **OPP-05 no se recomienda.** Acelera un escaneo que el portal puede volver innecesario.

## 3. Estimación gruesa frente a la meta (hipótesis)
| Tramo | AS-IS | Con OPP-01 + OPP-02 + OPP-04 | Supuesto |
|---|---|---|---|
| Recopilar expediente | 5 | ≈ 2 | El cliente carga todo de una vez; Legal revisa en digital |
| Escanear | 3 | ≈ 0 | No se escanea si el documento llega digital (**pendiente**, DG-4) |
| Verificar, autorizar y trasladar | 4 | ≈ 2 | Verificación digital; recogida a domicilio en paralelo |
| Reproceso promedio | +3 | ≈ +0,5 | La validación de vigencia y completitud evita la mayoría de devoluciones |
| **Total expediente** | **12 (≈ 15 con reproceso)** | **≈ 4 a 5** | Cumpliría la meta de 6, **si** se confirman los supuestos |

## 4. Decisiones complementarias
| Decisión | Actividad | Motivo |
|---|---|---|
| **Conservar humano** | Verificar que los documentos «cuadren» (Despacho) | Juicio sobre coherencia de ingresos y estado de cuenta; riesgo de crédito |
| **Conservar humano** | Evaluación de Riesgo y análisis de crédito | Fuera del objetivo; decisiones de riesgo |
| **Simplificar** | Escanear documentación | Puede desaparecer con el documento digital desde el origen |
| **Eliminar intermediario** | Concesionario en la entrega de documentos | Indicado por el entrevistado (PREG-017) |
| **No eliminar** | Traslado físico del expediente | Obligatorio (RN-01); solo se saca de la ruta crítica |

## 5. Recomendación
**Paquete A (recomendado): OPP-01 + OPP-02**, portal web con validación automática, **con OPP-04** como complemento para cumplir RN-01. OPP-03 entra como mejora rápida sobre el mismo portal.

**Necesita tu aprobación.** Elige el alcance del TO-BE (pregunta PRIO-1 en la entrevista).
