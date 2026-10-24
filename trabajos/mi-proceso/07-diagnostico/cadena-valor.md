# Cadena de valor — Flujo de crédito preaprobado Expomóvil

**Fecha:** 2026-10-24 · **Skill:** `cadena-valor` · **Base:** `05-bpmn/proceso-v02.bpmn`, entrevista rondas 1 a 3.
**Estado:** C-01 resuelta (ronda 4: «preaprobado» es solo la etiqueta del proceso). Meta: N = 6 días hábiles (PREG-016).

## 1. Producto, cliente y valor
| Proceso | Producto o servicio | Cliente | Actividad (Porter) | Contribución al valor | Evidencia |
|---|---|---|---|---|---|
| Solicitud de crédito Expomóvil | Crédito vehicular otorgado durante la **feria Expomóvil** (fechas concretas del año) | **Solicitante** (externo): recibe el crédito · **Concesionario** (externo): recibe el desembolso y entrega documentos | **Primaria**: operaciones y ventas del banco | Convertir el interés de la feria en un vehículo vendido y pagado | ENT CV-1, CV-2 |

## 2. Contribución de cada tramo del BPMN
| Tramo (BPMN v02) | Responsable | Tipo | Valor para el cliente | Días hábiles | Clasificación |
|---|---|---|---|---|---|
| Crear y evaluar solicitud (`ACT_001`, `ACT_002`, `GW_001`) | Negocio, Riesgo | Primaria | El cliente obtiene una respuesta | 2 | Declarado |
| Analizar e informar (`ACT_003`, `ACT_004`, `GW_002`, `GW_003`) | Analista | Primaria | El cliente sabe si tiene crédito y en qué condiciones | 2 | Declarado |
| **Recopilar expediente** (`ACT_006`, `GW_005`) | Legal, con documentos del cliente y del concesionario | Apoyo (control) | Necesario por control; el cliente no lo percibe como valor | **5** (≈ 2,5 de espera del cliente) | Estimado (PREG-007) |
| **Escanear documentación** (`ACT_007`) | Legal | Apoyo | Ninguno directo; necesario por control | **3** | Estimado |
| **Verificar y autorizar expediente** (`ACT_008`, `GW_006`) | Analista (Despacho) + mensajero | Apoyo (control + traslado físico obligatorio) | Ninguno directo; obligatorio (RN-01) | **4** (incluye espera del mensajero y traslado) | Estimado |
| Desembolsar (`ACT_009`) | Desembolso | Primaria | El concesionario recibe el pago y entrega el vehículo | 1 | Declarado |

**Tramo de expediente: 12 de 17 días hábiles (71 %).** Es el tramo con menos valor percibido por el cliente y el que concentra el reproceso (20 % de devoluciones, sobre todo por documentos con más de 1 mes).

## 3. Dolores del cliente
| Dolor | Fuente | Clasificación |
|---|---|---|
| **No saber el estado de su solicitud** (el más molesto) | ENT CV-3 | Declarado |
| Tiempo total: en una feria con fechas, la demora puede hacer perder la venta | ENT CV-1; hipótesis sobre el efecto | Declarado / hipótesis |
| Tener que volver a traer documentos cuando se vencen (más de 1 mes) | ENT PREG-014 | Declarado |

## 4. Objetivo estratégico
Reducir el tiempo de expediente de **12 a 6 días hábiles** (PREG-016) mediante una **página web de cargue de documentos** (ENT CV-4).
- **Interpretación por confirmar:** la meta de 6 días aplica al tramo de expediente; el proceso completo pasaría de 17 a 11 días hábiles.
- **Restricción:** el soporte físico es obligatorio (RN-01). La web puede acelerar la recopilación, el escaneo y la validación, pero los originales siguen llegando en físico a Desembolso (PREG-017).

## 5. Actividad prioritaria (criterio de salida del skill)
**Propuesta:** el tramo de expediente, «Recopilar expediente» + «Escanear documentación» + «Verificar y autorizar expediente», vinculado al producto «crédito vehicular Expomóvil».
**Estado:** propuesta coherente con la meta (12 → 6 días) y con el dolor del cliente (CV-3). Falta la aprobación formal en la priorización.

## 6. Qué es observado, declarado o hipótesis
- **Observado en la fuente:** tiempos estimados por actividad (Excel).
- **Declarado en entrevista:** feria, concesionario, dolor del cliente, meta, composición de los 5 días, volumen y tasas de ejemplo.
- **Hipótesis:** que la demora haga perder ventas en la feria, y la clasificación de Porter.
- **No se asume** que el traslado físico se pueda eliminar: es obligatorio.
