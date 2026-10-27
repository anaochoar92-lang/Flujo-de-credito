| «El expediente termina cuando el sobre sale a Desembolso. Sí entran en el mismo promedio.» | Confirmado por entrevistado || «Mide el efecto feria, sí, pero igual valida y deja la traza de los otros meses.» Las metas no se comentaron | Confirmado (período). Metas: propuesta pendiente del Gerente || «¿Qué me sugieres? ¿A qué dato te refieres?» → Se propone: TO-BE con el historial de Camunda; AS-IS con estimaciones mientras se confirma si existe un sistema (KPI-Q2b) | Propuesta, por confirmar || «Gerente de crédito; exigir a IT la disponibilidad del portal.» | Confirmado por entrevistado |# Historial de entrevista — Solicitud de crédito Expomóvil

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

## Ronda 3 — 2026-10-24 (cadena de valor, skill `cadena-valor`)
**Hipótesis presentadas (no confirmadas):** el proceso entrega el producto **crédito vehicular Expomóvil**. Es una **actividad primaria** (operaciones / ventas del banco); Legal, Despacho y Desembolso son actividades de **apoyo** que habilitan el desembolso. Clientes: el **solicitante** (externo) y posiblemente el **concesionario** que vende el vehículo. El tramo de expediente es el que más se aleja del valor percibido por el cliente.

| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| CV-1 | ¿«Expomóvil» es una **feria o campaña con fechas** o un **producto permanente** del banco? | Si es una feria de una semana, un expediente de 12 días hace que el cliente compre con otro banco antes de que termine. | Define cuánto vale cada día ganado. | «Es una feria que se da en ciertas fechas del año.» | Confirmado por entrevistado |
| CV-2 | ¿A quién se le desembolsa: al **cliente** o al **concesionario**? ¿El concesionario participa en el proceso, por ejemplo entregando documentos? | El concesionario espera el pago para entregar el carro y presiona al banco. | Define quién es el cliente que recibe el valor y quién sufre la demora. | «Para términos prácticos, dejémoslo al concesionario. Sí participa en el proceso para entregar documentos.» | Confirmado por entrevistado |
| CV-3 | Desde el punto de vista del cliente, ¿qué paso le genera **más quejas o abandonos**? ¿Coincide con el expediente? | El cliente quizá se queja más de no saber en qué va su solicitud que del tiempo en sí. | Confirma si el objetivo clave es el punto crítico para el cliente. | «Le molesta más no saber cómo está su solicitud.» | Confirmado por entrevistado |
| CV-4 | ¿Qué **meta medible** tienen para el expediente? Por ejemplo, pasar de 12 a N días hábiles, o bajar la devolución del 20 % al X %, y en qué plazo. | Sin meta, cualquier mejora parece suficiente. | Será la meta del KPI principal y la base del ROI. | «Disminuir el tiempo de 12 días hábiles a N días para todo el proceso, y hacerlo por medio de una página web para reducir los tiempos de cargue de documentos.» | Confirmado en parte (N y alcance por confirmar) |

### Interpretación de la ronda 3
| ID | Decisión | Estado |
|---|---|---|
| CV-1 | Expomóvil es una **feria en fechas concretas del año**: la demanda llega en picos y cada día de demora pesa más | Confirmado por entrevistado |
| CV-2 | Se desembolsa al **concesionario**. El concesionario **entrega documentos** del expediente | Confirmado por entrevistado. Impacto en el AS-IS: es un actor externo que no está en el BPMN v02 (posible pool «Concesionario» en una próxima versión) |
| CV-3 | Lo que más molesta al cliente es **no saber el estado de su solicitud** | Confirmado por entrevistado. Nuevo dolor del cliente, distinto del tiempo |
| CV-4 | Meta: bajar de **12 días hábiles a N**, mediante una **página web de cargue de documentos** | Confirmado en parte. **Contradicción C-02:** 12 días es el tramo de expediente, no «todo el proceso» (17 días). N no está definido. La página web es una **propuesta TO-BE**, no AS-IS |

### Contradicción nueva C-01 (bloquea el nombre del proyecto)
- Ronda 1 (PREG-001): «El nombre quedó como preaprobado pero no lo es […]; aquí pasaría igual para todos.» → se renombró el repositorio a «Flujo-de-credito».
- Ronda 3: «Una acotación: el flujo sí es de preaprobado.»
- No se cambia nada hasta aclararlo (PREG-015).

## Ronda 4 — 2026-10-24 (aclaraciones)
| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| PREG-015 | En la ronda 1 se indicó que el flujo **no** era de preaprobado y que todos siguen los mismos pasos; ahora se indica que **sí** lo es. ¿Qué significa aquí «preaprobado»? ¿El cliente sale de la feria **preaprobado** (Riesgo + Análisis) y luego completa el expediente para el desembolso? ¿O hay clientes que llegan ya preaprobados y se saltan pasos? ¿Volvemos a llamar el proyecto «preaprobado»? | Un cliente preaprobado en la feria que no entrega documentos en 10 días: ¿pierde la preaprobación? | Define el alcance, el nombre y si hay una variante en el BPMN. | «El nombre de preaprobado no cambia nada el flujo, solo es para que lo agregues en títulos, etc. No cambies más nombres, ya déjalo así.» | Confirmado por entrevistado |
| PREG-016 | ¿Cuál es el valor de **N**? ¿La meta es para el tramo de expediente (hoy 12 días hábiles) o para todo el proceso (hoy 17)? | Bajar el total a 12 ya sería una mejora de 5 días; bajar el expediente a 12 no cambia nada. | Es la meta del KPI principal y la base del ROI. | «El valor N sería 6.» | Confirmado por entrevistado (tramo interpretado: expediente) |
| PREG-017 | En la página web, ¿quién carga los documentos: el cliente, el concesionario o ambos? Como el soporte físico es obligatorio (RN-01), ¿los originales siguen viajando en físico a Desembolso después de cargarlos en la web? | Si la web elimina el escaneo pero el original llega tarde, Desembolso sigue esperando. | Define el alcance real del TO-BE. | «Que los cargue el cliente y que el concesionario deje de ser un intermediario, para reducir ese tiempo.» | Confirmado por entrevistado (originales físicos por confirmar) |
| PREG-018 | ¿Las 1.000 solicitudes son **por feria**, por mes o por año? ¿Cuántas ferias hay al año? | 1.000 por feria con 2 ferias al año es muy distinto de 1.000 al mes para el ROI. | Volumen para los KPI y el ROI (AS-06). | «Las 1000 son por mes cuando se hace la feria, que son febrero y noviembre.» | Confirmado por entrevistado |

### Interpretación de la ronda 4
| ID | Decisión | Estado |
|---|---|---|
| PREG-015 / C-01 | «Preaprobado» es solo la **etiqueta** del proceso: se añade en los títulos. **No cambia el flujo** (sigue siendo igual para todos) y **no se cambian más nombres** de repositorio ni de carpeta. Resuelve C-01 | Confirmado por entrevistado |
| PREG-016 / C-02 | **N = 6 días hábiles.** Se interpreta para el **tramo de expediente** (12 → 6), porque el resto del proceso ya suma 5 días y un total de 6 no sería alcanzable. Con esa meta, el proceso completo pasaría de 17 a 11 días hábiles | Confirmado por entrevistado; la interpretación del tramo queda **por confirmar** |
| PREG-017 | En el TO-BE, el **cliente carga sus documentos en la página web** y el concesionario **deja de ser intermediario** en la entrega de documentos | Confirmado por entrevistado (propuesta TO-BE). Pendiente: cómo llegan los originales físicos (RN-01) |
| PREG-018 | **1.000 solicitudes por mes de feria**; hay feria en **febrero y noviembre** → unas **2.000 solicitudes al año** | Confirmado por entrevistado (datos de ejemplo). AS-06 cambia: no son mensuales todo el año |

## Ronda 5 — 2026-10-24 (diagnóstico, skill `diagnosticar-asis`)
| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| DG-1 | (Cinco porqués de P-01, nivel 2) Los documentos con más de 1 mes, ¿**ya llegan así** cuando el cliente o el concesionario los entrega, o **se vencen mientras** el expediente está en proceso? | Un comprobante de ingresos expedido hace 25 días se vence en el día 6 del expediente. | Define si la solución es validar al recibir o acortar el proceso. | «Puede que se venzan durante el proceso; no pasa mucho, pero sí está la posibilidad.» | Confirmado por entrevistado |
| DG-2 | ¿Legal revisa la fecha de expedición cuando recibe los documentos? Si no, ¿por qué esa revisión la hace solo Despacho, al final? | Legal da por completo un expediente con un documento vencido y se pierden 12 días. | Nivel 3 de los cinco porqués; apunta a la validación temprana. | «La revisa Legal, pero en el transcurso de que llegue a Despacho se pudieron haber vencido.» | Confirmado por entrevistado |
| DG-3 | De las 1.000 solicitudes de un mes de feria, ¿cuántas llegan a la etapa de expediente (no rechazadas y con el cliente que acepta)? | Si solo 400 llegan a expediente, el 20 % son 80 devoluciones, no 200. | Volumen real del tramo que se quiere mejorar (KPI y ROI). | «Correcto, serían 20 %, es decir 80.» | Confirmado por entrevistado |
| DG-4 | Si el cliente carga sus documentos en la web, ¿cómo llegarían los **originales físicos** a Desembolso (RN-01)? ¿El cliente los lleva a una oficina, se recogen o los entrega en la feria? ¿Hace falta seguir escaneando si el documento ya llega digital? | La web elimina el escaneo, pero el original llega tarde y Desembolso sigue esperando. | Decide cuánto del objetivo de 6 días es alcanzable. | «Los puede dejar en la puerta de su casa y pasa un mensajero certificado y los recoge.» | Confirmado por entrevistado (escaneo sin responder) |

## Ronda 6 — 2026-10-24 (priorización, skill `priorizar-automatizacion`)
| ID | Pregunta | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|
| PRIO-1 | ¿Qué alcance tiene el TO-BE? (A) Paquete recomendado: portal web con validación automática (OPP-01 + OPP-02) + recogida a domicilio (OPP-04) + consulta de estado (OPP-03). (B) Solo portal + validación. (C) Otra combinación | Define qué se diseña en el TO-BE, los KPI y el ROI | «A.» | Confirmado por entrevistado |
| PRIO-2 | ¿Confirmas la causa raíz de P-01? «El expediente se arma en papel y en serie, la vigencia se consume en esperas y no hay ninguna regla que exija un margen de vigencia al recibir» | El skill pide confirmar la causa raíz antes de concluir | «Sí, y también es devuelto porque no es visible, para que la agregues.» | Confirmado por entrevistado |
| PRIO-3 | Si el documento llega en digital por la web, ¿hace falta seguir escaneando el original físico? | Decide si el escaneo (3 días) desaparece | «Sí.» | Confirmado por entrevistado |

## Ronda 7 — 2026-10-24 (diseño TO-BE, skill `disenar-tobe`)
| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| TB-1 | **Disparador:** ¿en qué momento se le envía al cliente el enlace al portal (al registrar que acepta la decisión) y por qué canal (correo, SMS, WhatsApp)? | El cliente acepta en la feria, pero el enlace le llega dos días después. | Es el inicio del tramo nuevo y el arranque de los 10 días hábiles. | «Correo. Sí, una vez se acepta la decisión.» | Confirmado por entrevistado |
| TB-2 | **Criterios:** si los documentos deben tener 1 mes o menos al llegar a Despacho, ¿qué margen exigimos al cargarlos? Por ejemplo, expedidos hace 20 días o menos. ¿Y quién decide si un documento es legible: el sistema, y en caso de duda Legal? | Un comprobante con 28 días pasa la validación y se vence antes de Despacho. | Son las reglas de la validación automática. | «Expedido hace 20 días. Legibilidad: sí.» | Confirmado por entrevistado |
| TB-3 | **Casos anómalos:** si la validación rechaza un documento (vencido o ilegible), ¿se le pide al cliente que lo vuelva a cargar? ¿Cuántas veces puede intentarlo? ¿Los casos dudosos van a Legal? | El cliente carga 5 veces la misma foto borrosa. | Define la ruta de excepción y el papel humano. | «Lo vuelve a cargar y tiene hasta 5 oportunidades para cargarlo; sí, los dudosos a Legal.» | Confirmado por entrevistado |
| TB-4 | **Contingencia y responsable:** si el portal falla, el cliente no sabe usarlo o el mensajero no logra recoger los originales, ¿se mantiene la ruta actual (Legal recopila en papel) como respaldo? ¿Quién es el responsable del portal? | El portal se cae el primer día de la feria de noviembre. | Plan de contingencia y responsable. | «Sí, si algo falla mantenemos el proceso actual. El responsable del portal es el área de IT del banco.» | Confirmado por entrevistado |

**Pendiente menor (AS-07):** el 10 % de cierres por vencimiento es sobre las 400 solicitudes que llegan a expediente, es decir **40 por mes de feria**. «Sí.» → Confirmado por entrevistado.

### Interpretación de la ronda 7
| ID | Decisión | Estado |
|---|---|---|
| TB-1 | El sistema envía el enlace al portal **por correo** en cuanto se registra que el cliente **acepta la decisión**. Ese momento es también el inicio de los 10 días hábiles (PREG-013) | Confirmado por entrevistado |
| TB-2 | Al cargar, cada documento debe estar **expedido hace 20 días o menos** (margen de ≈ 10 días frente al mes que exige Despacho, RN-02). El sistema decide la legibilidad y, si hay duda, decide Legal | Confirmado por entrevistado |
| TB-3 | Si un documento se rechaza, el cliente lo vuelve a cargar, con **hasta 5 intentos**. Los casos dudosos van a Legal. **Qué pasa al agotar los 5 intentos no se dijo:** se modela como paso a la ruta actual en papel (por TB-4) y queda **[SUPUESTO AS-T1, por confirmar]** | Confirmado en parte |
| TB-4 | Si algo falla (portal caído, cliente que no puede usarlo, recogida fallida), se usa **la ruta actual** como respaldo: Legal recopila en papel. Responsable del portal: **IT del banco** | Confirmado por entrevistado |

## Ronda 8 — 2026-10-24 (pendientes del TO-BE, skill `disenar-tobe`)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| AS-T1 | ¿Qué pasa cuando el cliente agota los 5 intentos? (se modeló como paso a la ruta en papel) | «El supuesto que hiciste está bien, se va por la ruta en papel.» | Confirmado por entrevistado |
| TB-5 | Si Despacho pide al cliente un documento corregido, ¿se reinician los 10 días hábiles, como hoy con cada devolución? | «Sí.» | Confirmado por entrevistado |
| TB-6 | ¿Los 5 intentos son por documento o por expediente? | «Por cada documento.» | Confirmado por entrevistado |
| TB-7 | ¿Qué hace que el sistema considere «dudoso» un documento y lo envíe a Legal? | «Datos no coinciden.» | Confirmado por entrevistado (detalle en TB-8) |
| TB-8 | ¿Qué datos se comparan para decidir que «no coinciden»? | «El nombre, la cédula, el salario o el monto no son iguales entre documentos.» | Confirmado por entrevistado |
| TB-9 | Si el portal falla, ¿quién lo detecta y registra el paso a la ruta en papel? | «El área de IT.» | Confirmado por entrevistado |

## Ronda 9 — 2026-10-24 (KPI, skill `definir-kpis`)
KPI candidatos (propuesta, sin fichas todavía): **KPI-01** ciclo del expediente (días hábiles por solicitud), **KPI-02** tasa de corrección/devolución de Despacho, **KPI-03** tasa de cierre por vencimiento, **KPI-04** uso efectivo del portal (solicitudes que terminan por la ruta digital). Métricas de apoyo: intentos por documento, % de casos dudosos a Legal y días de recogida de originales.
Nota: `docs/origen-presentacion-sesion3.md`, que pide leer el skill, no existe en el kit.

| ID | Pregunta | Caso adversarial | Por qué importa | Respuesta | Estado |
|---|---|---|---|---|---|
| KPI-Q1 | **Decisión y dueño:** ¿quién es el dueño de estos KPI y qué decisión tomaría con ellos? Por ejemplo, reforzar Legal en febrero y noviembre, ajustar el margen de 20 días o exigir a IT disponibilidad del portal. | Un KPI que nadie revisa no cambia nada. | Sin dueño ni decisión no es KPI, es métrica. | — | PENDIENTE |
| KPI-Q2 | **Fuente del dato:** ¿en qué sistema quedan hoy la fecha de aceptación del cliente, la fecha en que el sobre sale a Desembolso, las devoluciones y los cierres por vencimiento? ¿Quién las registra? | Si la devolución solo queda en un correo, no se puede contar. | Sin fecha de inicio y fin no hay KPI-01 medible (REQ-017 sigue pendiente). | — | PENDIENTE |
| KPI-Q3 | **Período y metas:** ¿medimos por mes de feria (febrero y noviembre)? Metas propuestas: expediente ≤ 6 días hábiles, devoluciones ≤ 5 %, cierres por vencimiento ≤ 5 %, uso del portal ≥ 80 %. ¿Te parecen realistas? | Una meta impuesta sin el dueño del proceso no se cumple. | El objetivo dice que las metas no se fijan sin acuerdo del dueño. | — | PENDIENTE |
| KPI-Q4 | **Interpretación:** ¿el expediente termina cuando el sobre sale a Desembolso o cuando se desembolsa? ¿Las solicitudes que pasan a la ruta en papel cuentan en el mismo promedio? | Si las de papel se excluyen, el promedio mejora aunque el proceso no. | Define el inicio, el fin y la población del KPI principal. | — | PENDIENTE |

**Resultado ronda 9:** catálogo y fichas en `10-kpis/`. Queda KPI-Q2b (¿existe hoy un sistema con fechas de aceptación, salida del sobre, devoluciones y cierres?) y el acuerdo de metas con el Gerente de crédito.

| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| KPI-Q2b | ¿Existe hoy un sistema donde queden las fechas del AS-IS? | «Sí, todo ese proceso se hace por medio de solicitudes de crédito, donde se tiene una fecha de inicio y una fecha de fin.» | Confirmado por entrevistado |
| KPI-Q3b | ¿Las metas quedan como propuesta para validar con el Gerente de crédito? | «Sí.» | Confirmado por entrevistado |

## Ronda 10 — 2026-10-24 (datos, skill `modelar-datos`)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| DAT-1 | ¿Datos reales o sintéticos? | «Sintéticos.» | Confirmado por entrevistado |
| DAT-2 | ¿La fecha de inicio y fin cubre toda la solicitud o hay fechas por etapa? | «Sí, desde que se crea hasta el desembolso. El tiempo de cada actividad te lo pasé en fuentes.» | Confirmado. Se usan los días por actividad de la fuente |
| DAT-3 | ¿El sistema guarda estados y devoluciones? | «Deja el estado que se da por la actividad, pero para el ejercicio lo vamos a dejar sencillo.» | Confirmado: `estado_final` según la última actividad |
| DAT-4 | ¿Cuántas solicitudes hay fuera de la feria? | «600 los otros 10 meses, con los mismos porcentajes de devoluciones, etc.» | Confirmado por entrevistado |

**Resultado ronda 10:** `09-datos/` con `casos.csv`, `actividades.csv`, `resumen_mensual.csv`, `diccionario.md` y `registro_calidad.md`.

## Ronda 11 — 2026-10-24 (ROI, skill `calcular-roi`)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| ROI-1 | Moneda y costo del personal | «Pesos dominicanos. Asume que es el salario mínimo de una empresa grande en República Dominicana.» → RD$ 29.988/mes (Res. CNS-01-2025, desde 01-02-2026) | Confirmado por entrevistado |
| ROI-2 | Horas reales de trabajo por expediente | «Ambas áreas trabajan 8 horas diarias.» → se usa para el costo por hora; las horas por expediente quedan como HIPÓTESIS H-R1 | Confirmado en parte |
| ROI-3 | Inversión, mantenimiento y mensajero | «¿Podrías sacar esos datos de supuestos?» → SUPUESTOS S-2 a S-4 con tres escenarios | Supuesto |
| ROI-4 | ¿Qué se gana en dinero? | «Menos personal temporal en feria.» | Confirmado por entrevistado |

**Resultado ronda 11:** `12-roi/` con el Excel y `interpretacion.md`. ROI año 1 en caja negativo en los tres escenarios; el margen de los ≈ 153 créditos al año que dejan de perderse no está incluido.

## Ronda 12 — 2026-10-24 (decisión para subir el ROI)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| ROI-5 | ¿Se agrega el margen por crédito como beneficio? | «No, quiero que el ROI suba; ¿qué decisión podríamos tomar?» | Confirmado: el margen no se incluye |
| ROI-6 | Opciones propuestas: (1) sin mensajero, el cliente entrega originales en sucursal; (2) además, convertir el tiempo liberado en caja (no reponer ≈ 2,7 puestos); (3) además, versión mínima del portal sobre Camunda. Recomendada: 3 | «Sí, agrégalas al Excel y súbelo a GitHub y reemplaza los archivos con el nuevo modelo para tener un ROI positivo.» | **Adoptada la Opción 3** como modelo del ROI (v02) |

**Resultado ronda 12:** ROI año 1 base +19,5 % (recuperación ≈ 10 meses); conservador −76 %. **Pendiente:** actualizar BPMN TO-BE, requisitos y datos sintéticos si se confirma quitar el mensajero (Opción 1).

## Ronda 13 — 2026-10-24 (mensajero)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| ROI-7 | ¿Se quita el mensajero (Opción 1)? | «El mensajero queda, pero no lo va a pagar el banco: lo hace un tercero y se cobra como comisión del servicio al cliente; de esa forma no genera costo, hace que no se pierdan créditos y corta tiempos.» | Confirmado por entrevistado. La Opción 1 pasa a ser «mensajero cobrado al cliente» |
| ROI-8 | ¿Qué opción genera más ROI? | «Escoge la opción que más ROI genere.» → Opción 3 (+19,5 % base) | Confirmado |

**Resultado ronda 13:** BPMN TO-BE v02 y datos sin cambios (el mensajero sigue). Nuevo REQ-TOBE-016 (comisión) y PROC-TOBE-003 ajustado. ROI sin cambio respecto a la ronda 12: el mensajero ya costaba 0 al banco en la Opción 3.

## Ronda 14 — 2026-10-24 (pérdida de créditos)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| CRED-1 | ¿Cómo reducir la pérdida de créditos por vencimiento? Propuestas: (1) recordatorios y llamada; (2) lista de documentos al crear la solicitud y carga asistida en el stand; (3) ayuda antes de agotar intentos; (4) disponibilidad del portal exigida a IT; (5) prórroga | «Sí, hazlo con las medidas 1 y 2 y súbelo a GitHub.» | Confirmado: medidas 1 y 2 |

**Resultado ronda 14:** BPMN TO-BE v03, REQ-TOBE-017 a 019, PROC-TOBE-005, hipótesis H-2b. Créditos perdidos en el TO-BE: 148 → 91 al año; créditos que dejan de perderse frente al AS-IS: 245. ROI base +16,7 %.

## Ronda 15 — 2026-10-24 (ROI y créditos)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| ROI-9 | Las medidas 1 y 2 no suben el ROI porque los créditos no están monetizados. ¿(1) Agregar el margen por crédito como supuesto editable o (2) dejar el ROI solo con ahorro de personal y mostrar los créditos aparte? | «2.» | Confirmado: ROI base +16,7 %; 245 créditos recuperados al año como beneficio no monetizado |

## Ronda 16 — 2026-10-26 (alcance del MVP, skill `mvp-contexto`, paso 20)
| ID | Pregunta | Respuesta | Estado |
|---|---|---|---|
| CTX-1 | ¿El MVP empieza al enviar el enlace tras la aceptación del cliente y termina con el expediente digital verificado por Despacho? | «Sí.» | Confirmado |
| CTX-2 | ¿Tres tareas humanas: cliente carga (`CL_CARGAR`), Legal revisa dudoso (`TB_ACT_REVISAR`), Despacho verifica (`TB_ACT_VERIF`)? | «Sí.» | Confirmado |
| CTX-3 | ¿Excluir (a) Riesgo/análisis/decisión, (b) recogida por mensajero, comisión y desembolso, (c) ruta en papel y temporizadores? | «Sí.» | Confirmado |
| P19 | ¿Quién aplica las correcciones del tablero Preset del reporte de validación? | «Sí, córrelo tú con la mejor propuesta y lo más acertado que puedas.» | Autorizado. No aplicado: la extensión de Chrome no estaba conectada; guía en `11-preset/correcciones-paso19.md` |

**Resultado ronda 16:** `14-mvp/alcance-equipo.md` y `11-preset/correcciones-paso19.md`. Sin efecto en ROI ni KPI.
