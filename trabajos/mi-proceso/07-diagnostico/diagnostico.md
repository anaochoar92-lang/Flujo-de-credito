# Diagnóstico AS-IS — Flujo de crédito preaprobado Expomóvil

**Fecha:** 2026-10-24 · **Skill:** `diagnosticar-asis` · **Base:** `05-bpmn/proceso-v02.bpmn`, EARS v01–v02, entrevista rondas 1 a 4, `cadena-valor.md`.
**Estado:** completo tras la ronda 5. Falta confirmar la causa raíz de P-01 (nivel 5). No se modificó el BPMN AS-IS.
**Clasificación de los datos:** *Estimado* (Excel fuente) · *Declarado* (entrevista) · *Hipótesis*. Nada está **medido**. Los volúmenes y tasas son **datos de ejemplo** (PREG-014, PREG-018).

## 1. Ficha
| Campo | Valor | Estado del dato |
|---|---|---|
| Producto | Crédito vehicular de la feria Expomóvil (febrero y noviembre) | Declarado |
| Cliente y valor esperado | Solicitante: crédito rápido y saber cómo va su solicitud. Concesionario: cobrar para entregar el vehículo | Declarado |
| Tramo foco | Expediente: `ACT_006` → `GW_005` → `ACT_007` → `ACT_008` → `GW_006` | Declarado (objetivo clave) |
| Volumen | 1.000 solicitudes por mes de feria, unas 2.000 al año. **400 por mes de feria llegan a expediente** (800 al año) | Declarado (ejemplo, DG-3) |
| Reproceso | 20 % devueltas de Despacho a Legal → **80 por mes de feria**. 10 % cerradas por los 10 días hábiles → **40** (el 10 % es sobre las 400; AS-07 confirmado en la ronda 7) | Declarado (ejemplo) |
| Meta | Expediente de 12 a **6** días hábiles | Declarado |

## 2. Mapa de flujo de valor (días hábiles por caso)
| Tramo | Trabajo | Espera | Total | Valor para el cliente |
|---|---|---|---|---|
| Crear y evaluar solicitud | ? | ? | 2 | Valor / control |
| Analizar crédito | ? | ? | 2 | Valor |
| **Recopilar expediente** | **≈ 2,5** (Legal) | **≈ 2,5** (cliente / concesionario) | **5** | Control |
| **Escanear documentación** | ? («lento y pausado») | ? | **3** | Control, sin valor directo |
| **Verificar y autorizar + traslado** | ? | ? (mensajero y viaje) | **4** | Control + traslado obligatorio |
| Desembolsar | ? | ? | 1 | Valor |
| **Camino feliz** | | | **17** | |

**Efecto del reproceso.** Cada devolución repite Recopilar, Escanear y Verificar (12 días). Con un 20 % de devoluciones en cada vuelta, el expediente dura en promedio **12 ÷ (1 − 0,20) = 15 días hábiles**, y el proceso completo, **≈ 20 días**: 3 más que el camino feliz.
Es un cálculo con datos de ejemplo y **supone** que cada vuelta tiene la misma probabilidad de devolución (hipótesis).

**Lectura.** De los 12 días de expediente, solo unos 2,5 están identificados como trabajo. El resto es espera del cliente, un escaneo lento o el traslado físico. Para llegar a 6 días hay que atacar las **esperas y el reproceso**, no solo el trabajo de Legal.

## 3. Partes interesadas
| Parte | Interés | Cómo le afecta el problema | Fuente |
|---|---|---|---|
| Solicitante | Crédito rápido; saber el estado | No sabe cómo va su solicitud (CV-3); debe repetir documentos vencidos | ENT CV-3, PREG-014 |
| Concesionario | Cobrar y entregar el vehículo durante la feria | Hoy hace de intermediario de documentos; espera el desembolso | ENT CV-2, PREG-017 |
| Legal | Expediente completo a la primera | Recibe el 20 % de devoluciones | ENT PREG-014 |
| Analista (Despacho) | Expediente correcto | Revisa dos veces el mismo expediente | ENT PREG-003 |
| Desembolso | Sobre físico correcto | Depende del mensajero | ENT PREG-007, PREG-008 |
| Banco (negocio) | Convertir la feria en créditos | 10 % se pierde por vencimiento de los 10 días | ENT PREG-014 |

## 4. Problemas y cinco porqués (en construcción)
### P-01 — El 20 % de los expedientes vuelve de Despacho a Legal
| Nivel | ¿Por qué? | Evidencia | Estado |
|---|---|---|---|
| 1 | Algún documento tiene **más de 1 mes** desde su expedición | ENT PREG-014 | Declarado |
| 2 | Los documentos **se vencen durante el proceso**. No es lo más frecuente, pero ocurre | ENT DG-1 | Declarado |
| 3 | Legal revisa la fecha **solo al recibir**: comprueba que el documento esté vigente ese día, no que lo siga estando cuando llegue a Despacho | ENT DG-2 | Declarado |
| 4 | Entre Legal y Despacho pasan varios días hábiles (escaneo de 3 días y espera de Despacho), y el documento puede llegar con poca vigencia | ENT PREG-007; XLS Tiempos | Estimado |
| 5 | **Causa raíz:** el expediente se arma en papel y en serie (recopilar → escanear → verificar → trasladar), así que la vigencia se consume en esperas y no hay ninguna regla que exija un margen de vigencia al recibir | Deducido de los niveles 1–4 | **Confirmada** (ENT PRIO-2) |

**Segunda causa de devolución (ENT PRIO-2):** el documento **no es visible**, es decir, es ilegible (borroso, cortado u oscuro). Igual que la vigencia, hoy solo se detecta en Despacho, al final del tramo.

Nota (C-03): en la ronda 2 el vencimiento fue el motivo **más común** de devolución, y en la ronda 5 «no pasa mucho» que se venza durante el proceso. Parte de las devoluciones pueden ser documentos que ya llegaban casi vencidos u otros casos de «no cuadra».

### P-02 — El tramo de expediente tarda 12 días hábiles
| Nivel | ¿Por qué? | Evidencia | Estado |
|---|---|---|---|
| 1 | Mitad del tiempo de recopilación es **esperar los documentos** del cliente o del concesionario; el escaneo es lento; Despacho espera al mensajero | ENT PREG-007 | Declarado |
| 2 | Hipótesis: los documentos llegan en papel, por un intermediario y en momentos distintos, y por eso hay que escanearlos después | ENT PREG-017 (concesionario intermediario) | Hipótesis |
| 3–5 | — | — | Pendiente |

### P-03 — El cliente no sabe el estado de su solicitud
| Nivel | ¿Por qué? | Evidencia | Estado |
|---|---|---|---|
| 1 | Solo se le informa cuando el Analista comunica la decisión (`ACT_004`); no hay otro punto de contacto en el AS-IS | BPMN v02; ENT CV-3 | Declarado / observado en el modelo |
| 2–5 | — | — | Pendiente |

## 5. Reglas y restricciones que condicionan la mejora
- RN-01: los originales deben llegar en **físico** a Desembolso.
- RN-02: documentos de **1 mes o menos** desde su expedición.
- 4 documentos obligatorios; cierre automático a los **10 días hábiles**, que se reinicia con cada devolución.

## 6. Candidatas que salen del diagnóstico (se puntúan en la priorización)
Son hipótesis, todavía sin priorizar:
1. **Carga web de documentos por el cliente**, sin el concesionario como intermediario (ENT PREG-017).
2. **Validación automática de la fecha de expedición** al cargar cada documento, para que se rechace antes de llegar a Despacho (ataca P-01).
3. **Consulta del estado de la solicitud en la web** (ataca P-03).
4. Documento digital desde el origen, para reducir el escaneo (pendiente: si se sigue escaneando).
5. **Recogida de originales a domicilio por mensajero certificado**, en paralelo a la verificación digital (ENT DG-4; cumple RN-01).

Puntuación y recomendación: `priorizacion.md` y `oportunidades.csv`.

## 7. Preguntas abiertas
- Confirmar la causa raíz de P-01 (nivel 5).
- Si se sigue escaneando cuando el documento ya llega en digital (DG-4).
- Base del 10 % de cierres por vencimiento (AS-07).
