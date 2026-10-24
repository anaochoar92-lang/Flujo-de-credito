# Inventario AS-IS — Solicitud de crédito Expomóvil (v01)

**Fecha:** 2026-10-23 · **Skill:** `analizar-sop` · **Nivel:** AS-IS.
**Fuente única:** `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx`
- Hoja «Proceso BPMN» (`PB`), filas 4–25, con el título en A1: «Proceso de Solicitud de Crédito – Expomóvil (insumo para diagrama BPMN)».
- Hoja «Tiempos» (`TI`), filas 1–9, y un gráfico de barras con los mismos datos.
- Un comentario sin autor en la hoja «Proceso BPMN»: «Suma sin reprocesos. Cada devolución (G1, G2, G3, G4) agrega el tiempo de las tareas que se repiten.»

**Referencias:** `PB-F6` = hoja Proceso BPMN, fila 6. Los IDs de la fuente (E1, T1, G1…) se conservan en la columna «ID fuente».
**Estados usados:** *Confirmado en fuente* · *Pendiente de confirmar* · *Contradictorio*. Todavía no hay nada *Confirmado por entrevistado*.

> **Alcance (confirmado en la ronda 1, PREG-001):** el repositorio se llamó al principio «Automatización Preaprobado», pero el proceso **no** es de preaprobado. Es el flujo de solicitud de crédito Expomóvil y todos los clientes siguen los mismos pasos. El repositorio se renombró «Flujo-de-credito».

## 1. Objetivo, inicio, fin y alcance
| Aspecto | Según la fuente | Fuente | Estado |
|---|---|---|---|
| Objetivo | Tramitar una solicitud de crédito del producto Expomóvil hasta su desembolso | PB-A1, PB-F5, PB-F18 | Confirmado en fuente |
| Inicio | «El cliente manifiesta interés en un crédito de Expomóvil» | PB-F5 | Confirmado en fuente (canal y evidencia sin definir) |
| Fin feliz | Crédito desembolsado | PB-F18 | Confirmado en fuente |
| Fin no feliz | Solicitud rechazada (solo desde el análisis de crédito) | PB-F11 | Confirmado en fuente |
| Alcance | Desde el interés del cliente hasta el desembolso y el «post-desembolso» | PB-F5 a PB-F18 | Pendiente: no se describe qué incluye el post-desembolso |
| Tiempo total | 17 días hábiles en el camino feliz, sin reprocesos | PB-H19, TI-F9, comentario | Confirmado en fuente (origen de las estimaciones sin definir) |

## 2. Responsables (carriles)
| ID | Rol | Elementos a su cargo | Fuente | Estado |
|---|---|---|---|---|
| ROL-001 | Persona de Negocio | E1, T1 | PB-B5, PB-B6 | Confirmado en fuente |
| ROL-002 | Persona de Riesgo | T2, G1 | PB-B7, PB-B8 | Confirmado en fuente |
| ROL-003 | Analista de crédito | T3, G2, E2, **T6, G4** | PB-B9 a B11, B15, B16 | Confirmado en fuente. Ojo: el mismo rol analiza **y** autoriza el expediente (ver VAC-012) |
| ROL-004 | Legal | T4, G3, T5 | PB-B12 a B14 | Confirmado en fuente |
| ROL-005 | Desembolso | T7, E3 | PB-B17, PB-B18 | Confirmado en fuente |
| — | Cliente | Inicia el proceso (E1), pero **no tiene carril** | PB-F5 | Pendiente: no se modela su interacción (entrega de documentos, aceptación, notificación) |

## 3. Eventos
| ID | ID fuente | Nombre | Tipo | Responsable | Fuente | Estado |
|---|---|---|---|---|---|---|
| EVT-001 | E1 | Cliente solicita crédito | Inicio | Persona de Negocio | PB-F5 | Confirmado en fuente; canal sin definir |
| EVT-002 | E2 | Solicitud rechazada | Fin | Analista de crédito | PB-F11 | Confirmado en fuente |
| EVT-003 | E3 | Crédito desembolsado | Fin | Desembolso | PB-F18 | Confirmado en fuente |

No hay temporizadores ni eventos de mensaje. Tampoco existe un fin por desistimiento o cancelación del cliente.

## 4. Actividades
| ID | ID fuente | Actividad | Responsable | Qué hace (texto de la fuente) | Días hábiles | Fuente | Observación |
|---|---|---|---|---|---|---|---|
| ACT-001 | T1 | Crear solicitud | Persona de Negocio | Captura la información del cliente y del producto Expomóvil (monto, plazo, vehículo) y envía la solicitud a Riesgo | 1 | PB-F6, TI-F2 | También recibe las devoluciones de G1 y G2 |
| ACT-002 | T2 | Evaluar solicitud | Persona de Riesgo | Evalúa si el cliente es apto (perfil, buró, políticas) | 1 | PB-F7, TI-F3 | Verbo «evaluar» sin criterio verificable |
| ACT-003 | T3 | Analizar crédito | Analista de crédito | Analiza capacidad de pago, riesgo y garantías, y emite una recomendación | 2 | PB-F9, TI-F4 | «Riesgo» se evalúa dos veces (T2 y T3) |
| ACT-004 | T4 | Recopilar expediente | Legal | Reúne todos los documentos del expediente necesarios para gestionar el crédito | 5 | PB-F12, TI-F5 | No dice qué documentos ni quién los entrega. Es la tarea más larga (29 %) |
| ACT-005 | T5 | Escanear documentación | Legal | Digitaliza todo el expediente y lo envía a Despacho | 3 | PB-F14, TI-F6 | 3 días para escanear: no se explica por qué |
| ACT-006 | T6 | Despacho y expediente | Analista de crédito | Verifica que la documentación sea correcta, la autoriza y la envía **en sobre** a Desembolso | 4 | PB-F15, TI-F7 | Nombre sin verbo; mezcla verificar, autorizar y enviar. El expediente ya escaneado viaja además en sobre físico |
| ACT-007 | T7 | Desembolso y post-desembolso | Desembolso | Verifica el sobre, desembolsa en la cuenta indicada y realiza las gestiones post-desembolso | 1 | PB-F17, TI-F8 | Nombre sin verbo; agrupa tres acciones. No hay salida si el sobre está mal |

## 5. Decisiones
| ID | ID fuente | Pregunta | Quién decide | Salidas según la fuente | Fuente | Observación |
|---|---|---|---|---|---|---|
| DEC-001 | G1 | ¿Cliente apto? | Persona de Riesgo | Sí → T3 · No → devuelve a Negocio para corregir o recapturar (T1) | PB-F8 | **No tiene salida de rechazo**: un cliente no apto vuelve a Negocio sin límite (VAC-003) |
| DEC-002 | G2 | ¿Decisión del análisis? | Analista de crédito | Aprobar → T4 · Aprobar con condiciones → T1 (Negocio modifica datos) · Rechazar → E2 | PB-F10 | Tras modificar, ¿vuelve a pasar por Riesgo y por análisis? (VAC-005) |
| DEC-003 | G3 | ¿Documentación completa? | Legal | Sí → T5 · No → sigue recopilando (T4, bucle) | PB-F13 | Bucle sin límite ni plazo |
| DEC-004 | G4 | ¿Documentación OK? | Analista de crédito | Sí → T7 · No (falta o se rechaza) → devuelve a Legal (T4) | PB-F16 | Repite la revisión de G3 con otro criterio no descrito |

## 6. Caminos
| Camino | Recorrido | Fuente |
|---|---|---|
| Feliz | E1 → T1 → T2 → G1 Sí → T3 → G2 Aprobar → T4 → G3 Sí → T5 → T6 → G4 Sí → T7 → E3 (17 días hábiles) | PB-F5 a F18, PB-H19 |
| Rechazo | … → T3 → G2 Rechazar → E2 | PB-F10, F11 |
| Bucle 1 (no apto) | G1 No → T1 → T2 → G1 … | PB-F8 |
| Bucle 2 (condiciones) | G2 Con condiciones → T1 → T2 → G1 → T3 → G2 … | PB-F10 |
| Bucle 3 (expediente incompleto) | G3 No → T4 → G3 … | PB-F13 |
| Bucle 4 (expediente con errores) | G4 No → T4 → G3 → T5 → T6 → G4 … (repite 12 días de T4+T5+T6) | PB-F16; tiempos TI |

## 7. Sistemas, documentos y datos
| Elemento | Mención en la fuente | Fuente | Estado |
|---|---|---|---|
| Sistemas | **Ninguno nombrado** (no se dice dónde se crea la solicitud ni si hay motor o buró automatizado) | — | Pendiente |
| Datos de la solicitud | Información del cliente; producto Expomóvil: monto, plazo, vehículo | PB-E6 | Confirmado en fuente |
| Buró | Se consulta en T2 (sin indicar cómo) | PB-E7 | Confirmado en fuente |
| Expediente | «Todos los documentos necesarios»; sin lista | PB-E12 | Pendiente |
| Sobre físico | Va de Despacho a Desembolso | PB-E15, E17 | Confirmado en fuente |
| Cuenta de desembolso | «La cuenta indicada»; no se dice de quién (¿cliente o concesionario?) | PB-E17 | Pendiente |

## 8. Excepciones y casos sin tratar
Ninguno aparece en la fuente; todos quedan como vacíos en `vacios.md`:
- el cliente desiste o no entrega documentos;
- el cliente no acepta las condiciones;
- falla el buró o el sistema;
- el sobre llega incompleto a Desembolso;
- el desembolso falla;
- hay solicitudes duplicadas.
