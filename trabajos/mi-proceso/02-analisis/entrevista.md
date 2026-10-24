# Historial de entrevista — Solicitud de crédito Expomóvil

**Skill:** `entrevista-adversarial` · **Fuente analizada:** `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx` (ver `inventario.md` y `vacios.md`).
Regla: máximo cuatro preguntas por ronda. Sin respuesta explícita, la pregunta queda **PENDIENTE**.

## Ronda 1 — 2026-10-23
| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| PREG-001 | La fuente describe la solicitud de crédito **Expomóvil** y no menciona «preaprobado». ¿Este es el proceso de preaprobado, uno distinto, o el preaprobado es una variante dentro de él? Si un cliente ya viene preaprobado, ¿qué pasos se salta (Riesgo T2, Análisis T3)? | Un cliente preaprobado llega a Expomóvil: según el Excel pasaría igual por Riesgo y por Análisis (3 días). | Define el alcance del proyecto y del diagrama. | «El nombre quedó como preaprobado pero no lo es […]. Sí, aquí pasaría igual para todos.» | Confirmado por entrevistado |
| PREG-002 | En «¿Cliente apto?» (G1), el «No» devuelve a Negocio para corregir. ¿Riesgo puede **rechazar** la solicitud, o el único rechazo es el del Analista (G2)? | Un cliente con buró negativo: no hay dato que corregir, pero el flujo lo devuelve a Negocio una y otra vez. | Falta un fin del proceso. | «Riesgo sí podría rechazar y en ese caso se cierra el flujo.» | Confirmado por entrevistado |
| PREG-003 | En «Recopilar expediente» (T4): ¿qué documentos son obligatorios, quién los entrega (cliente, concesionario) y qué pasa si nunca se completan? Y si Legal ya lo dio por completo (G3), ¿por qué Despacho (G4) lo devuelve? ¿Qué revisa cada uno? | El cliente no trae un documento durante semanas; o Despacho rechaza un expediente que Legal dio por bueno, y se repiten unos 12 días (T4 + T5 + T6). | Es el tramo más largo (12 de 17 días) y tiene dos bucles sin límite. | «Documento de identidad, comprobante de ingresos, estado de cuenta bancario y el pagaré. Si no se completan después de 10 días se cierra la solicitud de forma automática. [Despacho devuelve] porque se pudo dar cuenta de que algo no cuadra.» | Confirmado por entrevistado (cómputo de los 10 días por confirmar) |
| PREG-004 | ¿Cuándo y quién informa al cliente de la decisión (aprobación, condiciones o rechazo)? Con «Aprobar con condiciones», ¿el cliente debe aceptarlas? Y después de que Negocio modifica los datos, ¿la solicitud vuelve a pasar por Riesgo y por Análisis? | El cliente no acepta el monto menor: el Excel no tiene salida para eso. | Falta la interacción con el cliente y el fin por desistimiento; el reproceso puede sumar 4 días. | «La información se la pasa el analista de crédito para saber si continúa con la recopilación de expediente. Si se aprueba con condiciones sigue el flujo normal; si no acepta se cierra la solicitud. Si se modifican los datos sí vuelve a pasar por negocio y análisis.» | Confirmado por entrevistado (si repite Riesgo, por confirmar) |

### Preguntas para rondas siguientes (no enviadas aún)
PREG-005 canal de inicio · PREG-013 cómputo de los 10 días (hábiles o calendario, desde cuándo) · PREG-006 diferencia entre Riesgo y Análisis · PREG-007 origen de los tiempos y por qué escanear tarda 3 días · PREG-008 para qué sirve el sobre físico · PREG-009 sobre incorrecto, post-desembolso y cuenta · PREG-010 segregación de funciones · PREG-011 sistemas · PREG-012 garantía, contrato, firma y seguros.

### Cobertura tras el análisis (antes de respuestas)
- Confirmado en fuente: 5 roles, 3 eventos, 7 actividades, 4 decisiones y los tiempos estimados.
- Pendiente: 16 vacíos (`vacios.md`), de ellos 7 de prioridad A.
- Contradictorio: ninguno dentro de la fuente.
- ¿Suficiente para EARS? **No todavía**: faltan fines del proceso (rechazo por Riesgo, desistimiento) y el alcance respecto a preaprobado.

### Interpretación de la ronda 1 (decisiones aceptadas)
| ID | Decisión para el modelo | Estado |
|---|---|---|
| PREG-001 | El proceso **no** es de preaprobado: es el **flujo de solicitud de crédito** (producto Expomóvil). Todos los clientes siguen los mismos pasos; no hay variante preaprobada. El proyecto y el repositorio pasan a llamarse «Flujo de crédito». | Confirmado por entrevistado |
| PREG-002 | «¿Cliente apto?» (G1) tiene tres salidas: *Apto* → Analizar crédito; *Corregir* → vuelve a Negocio (fuente); *Rechazar* → **fin «Rechazada por Riesgo»** (nuevo). | Confirmado por entrevistado |
| PREG-003 | Expediente obligatorio: **documento de identidad, comprobante de ingresos, estado de cuenta bancario y pagaré**. Si no se completa en **10 días**, la solicitud **se cierra automáticamente** (temporizador). Despacho (G4) devuelve a Legal cuando detecta algo que **no cuadra** aunque los documentos estén completos. | Confirmado por entrevistado. Pendiente: días hábiles o calendario y desde cuándo se cuentan (PREG-013) |
| PREG-004 | Tras aprobar (con o sin condiciones), el **Analista de crédito informa al cliente** y el cliente decide si continúa. *No acepta* → **fin «Cerrada por no aceptación»**. *Acepta sin condiciones* → Recopilar expediente. *Acepta con condiciones* → Negocio modifica los datos → vuelve a **Analizar crédito**. | Confirmado por entrevistado. Asunción AS-01: tras modificar datos **no** se repite Riesgo («vuelve a pasar por negocio y análisis») |

### Objetivo clave del proyecto (indicado por el entrevistado, 2026-10-23)
**Disminuir los tiempos de las actividades de expediente.** Debe guiar el diagnóstico, la priorización, el TO-BE y los KPI. Ver `../objetivo-proyecto.md`.

### Cobertura tras la ronda 1
- Confirmado: alcance (flujo de crédito, sin variante preaprobada), rechazo por Riesgo, documentos obligatorios, cierre automático a los 10 días, motivo de la devolución de Despacho, notificación y aceptación del cliente.
- Pendiente (no bloquea el AS-IS): PREG-005 a PREG-013 (canal, sistemas, origen de los tiempos, sobre físico, desembolso, segregación, garantías, cómputo de los 10 días).
- Contradictorio: ninguno.
- ¿Suficiente para EARS y BPMN v01? **Sí**, marcando los pendientes.

## Ronda 2 — 2026-10-23 (enfocada en el objetivo clave: tiempos de expediente)
| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| PREG-013 | Los 10 días para completar el expediente: ¿son hábiles o calendario? ¿Se cuentan desde que el cliente acepta, desde que Legal empieza a recopilar u otro momento? Si Despacho devuelve el expediente a Legal, ¿el plazo vuelve a empezar? | Un expediente devuelto dos veces por Despacho podría estar abierto 30 días sin cerrarse nunca. | Decide cómo se dibuja el temporizador (auditoría S-01) y el KPI de cierres por vencimiento. | «Días hábiles. Cuenta desde que el cliente acepta. Sí vuelve a empezar.» | Confirmado por entrevistado |
| PREG-007 | Los 17 días de la hoja «Tiempos», ¿son medidos o estimados? De los 5 días de «Recopilar expediente», ¿cuánto es esperar al cliente y cuánto es trabajo de Legal? ¿Por qué escanear tarda 3 días y Despacho 4? | Si 4 de los 5 días son esperar al cliente, automatizar Legal no reduce casi nada. | Separa trabajo de espera: es la base del diagnóstico y de los KPI. | «De los 5 días, mitad es esperar al cliente y mitad trabajo de Legal. El escaneo es lento y pausado. En Despacho, mientras se recopilan todos los datos, llega el mensajero a recoger la documentación y viaja a Desembolso.» | Confirmado por entrevistado (los tiempos siguen siendo estimados) |
| PREG-008 | Si el expediente ya está escaneado, ¿por qué Despacho envía un sobre físico a Desembolso? ¿Desembolso necesita el pagaré original u otro documento en papel? | El sobre se pierde o tarda: el crédito aprobado espera aunque todo esté digitalizado. | Candidato claro para reducir el tiempo de expediente. | «Por ser sector bancario y del Estado, todo debe tener soporte físico y debe llegar al área de Desembolso de forma física.» | Confirmado por entrevistado |
| PREG-014 | ¿Cuántas solicitudes hay al mes? De ellas, ¿qué porcentaje devuelve Despacho a Legal, cuántas se cierran por los 10 días y cuáles son los motivos de devolución más comunes? | Si la mitad de los expedientes vuelve de Despacho, el tiempo real es casi el doble de 17 días. | Volumen y reproceso: insumo para priorizar, para los KPI y para el ROI. | «Para el caso del ejemplo hay 1000 solicitudes. Se devuelve a Legal el 20 %. Se cierran por los 10 días el 10 %. El motivo de devolución más común: la fecha de los documentos supera 1 mes desde que fueron expedidos.» | Confirmado por entrevistado (datos de ejemplo) |

### Interpretación de la ronda 2 (decisiones aceptadas)
| ID | Decisión | Impacto | Estado |
|---|---|---|---|
| PREG-013 | El plazo es de **10 días hábiles**, cuenta **desde que el cliente acepta** y **se reinicia** cuando Despacho devuelve el expediente a Legal | El dibujo del temporizador sobre «Recopilar expediente» es **correcto**: resuelve el hallazgo S-01 y la asunción AS-02. BPMN v02: el temporizador pasa a llamarse «10 días hábiles sin expediente completo». No se escribe expresión ISO, porque `P10D` son días calendario | Confirmado por entrevistado |
| PREG-007 | Los 5 días de Recopilar son **≈ 2,5 de espera del cliente + ≈ 2,5 de trabajo de Legal**. El escaneo (3 días) es lento por el método de trabajo. Despacho (4 días) incluye la **espera del mensajero y el traslado físico** a Desembolso | El tiempo de expediente mezcla trabajo, espera del cliente y transporte. Insumo directo para el diagnóstico | Confirmado por entrevistado; las cifras siguen siendo **estimaciones** |
| PREG-008 | El soporte físico es **obligatorio** (sector bancario y estatal): el expediente debe llegar en físico a Desembolso | **Restricción del TO-BE**: no se puede eliminar el sobre; se puede acelerar o hacer en paralelo | Confirmado por entrevistado |
| PREG-014 | Ejemplo: **1.000 solicitudes** (periodo por confirmar; se asume **mensual**). **20 %** se devuelven de Despacho a Legal y **10 %** se cierran por los 10 días. Motivo principal de devolución: **documentos expedidos hace más de 1 mes** | Primera línea base para KPI y ROI. Regla nueva: los documentos del expediente deben tener **1 mes o menos** desde su expedición | Confirmado por entrevistado; **datos de ejemplo**, no medición real |

### Cobertura tras la ronda 2
- Confirmado: cómputo del plazo, composición de los tiempos de expediente, obligación del soporte físico, volumen y tasas de ejemplo, motivo principal de devolución.
- Pendiente (no bloquea): periodo de las 1.000 solicitudes (mes o año), AS-01 (si se repite Riesgo), canal, sistemas, segregación, garantías.
- Suficiente para la fase 2 (diagnóstico, priorización, TO-BE y KPI).
