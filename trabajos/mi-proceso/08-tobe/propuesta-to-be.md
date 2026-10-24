# Propuesta TO-BE — Flujo de crédito preaprobado Expomóvil (borrador v01)

> **Es una PROPUESTA, no un hecho observado.** Parte del AS-IS vigente (`05-bpmn/proceso-v02.bpmn`, que no se modifica) y del paquete A aprobado en la ronda 6 (`07-diagnostico/priorizacion.md`).

**Fecha:** 2026-10-24 · **Skill:** `disenar-tobe` · **Meta:** expediente de 12 a 6 días hábiles.
**Estado:** borrador con modelo. Respuestas TB-1 a TB-4 recibidas (ronda 7); generados `requisitos-ears-to-be.md`, `modelo-v01.json`, `proceso-to-be-v01.bpmn` y `revision-camunda.md`. Ronda 8 resuelta: versión vigente `proceso-to-be-v02.bpmn` (sección 4).

## 1. Explicación del cambio (paso 1 del skill)
| Aspecto | Contenido |
|---|---|
| Origen en el BPMN | Tramo de expediente: `ACT_006` Recopilar → `GW_005` → `ACT_007` Escanear → `ACT_008` Verificar y autorizar → `GW_006` |
| Problema | 12 días hábiles (≈ 15 con un 20 % de devoluciones). Los documentos se vencen o llegan ilegibles y solo se detecta en Despacho. El cliente no sabe en qué va su solicitud |
| Alternativa sin tecnología | Lista de verificación de vigencia y legibilidad en Legal al recibir, y entrega directa del cliente en oficina. Ataca parte de P-01, pero no la espera ni la visibilidad |
| Alternativa automatizada (paquete A) | Portal web: el cliente carga los documentos, el sistema los valida (completos, legibles y con margen de vigencia), el cliente consulta el estado y un mensajero certificado recoge los originales a domicilio en paralelo a la verificación digital |
| Riesgos | Datos personales en la web; la validación automática puede equivocarse con la legibilidad o la fecha; adopción por los clientes de la feria; cadena de custodia del pagaré original |
| Expectativa KPI (hipótesis) | Expediente ≈ 6 días hábiles; devoluciones de Despacho de 20 % a cerca de 5 %; cierres por vencimiento por debajo del 10 % actual |
| Responsabilidad humana | Legal revisa las excepciones de la validación. Despacho sigue decidiendo si los documentos «cuadran». Desembolso verifica el sobre físico |

## 2. Diferencias AS-IS ↔ TO-BE (por ID)
| AS-IS (v02) | TO-BE propuesto | Tipo de cambio | Oportunidad |
|---|---|---|---|
| `GW_004` «Sin condiciones» → `ACT_006` | `GW_004` → **enviar al cliente el enlace al portal** (tarea de envío del sistema) | Nuevo | OPP-01 |
| — | Pool **Cliente**: «Cargar documentos en el portal» y «Dejar originales para recogida» | Nuevo participante | OPP-01, OPP-04 |
| Concesionario como intermediario de documentos | Eliminado de la entrega de documentos | Eliminar | PREG-017 |
| `ACT_006` Recopilar expediente (Legal, papel) | **Validar documentos automáticamente** (sistema: completitud de los 4 documentos, legibilidad y margen de vigencia) → **«¿Documentos válidos?»** → si no, se avisa al cliente para corregir → si hay duda, **Legal revisa** | Automatizar + humano en el bucle | OPP-02 |
| `GW_005` ¿Documentación completa? | Lo resuelve la validación automática | Sustituido | OPP-02 |
| `ACT_007` Escanear (en serie, antes de Despacho) | **Se mantiene** (PRIO-3), pero sobre los originales recogidos y **en paralelo** a la verificación digital | Reordenar | OPP-04 |
| `ACT_008` Verificar y autorizar (sobre papel escaneado) + mensajero después | Verificar y autorizar **sobre los documentos digitales**, mientras el mensajero certificado recoge los originales a domicilio | Reordenar | OPP-04 |
| `GW_006` → `ACT_009` | **Unión** de las dos ramas: Desembolso empieza cuando la verificación está OK **y** los originales llegaron (RN-01) | Nuevo (gateway paralelo) | RN-01 |
| `TMR_001` 10 días hábiles | Se mantiene, desde la aceptación del cliente | Sin cambio | PREG-013 |
| — | El estado de la solicitud se publica en el portal en cada hito | Nuevo (requisito, no gateway) | OPP-03 |

## 3. Camino feliz estimado (hipótesis)
Aceptación → enlace → carga y validación (≈ 2 días) → en paralelo: verificación digital (≈ 1 día) y recogida + escaneo + traslado (≈ 4 días) → unión → Desembolso.
**Expediente ≈ 6 días hábiles** (antes 12). Sin margen si el escaneo sigue tardando 3 días.

## 4. Respuestas de la ronda 7 y pendientes
| ID | Decisión |
|---|---|
| TB-1 | Enlace **por correo** en cuanto el cliente acepta la decisión (inicio de los 10 días hábiles) |
| TB-2 | Documentos **expedidos hace 20 días o menos**; legibilidad la decide el sistema y, si hay duda, Legal |
| TB-3 | El cliente vuelve a cargar, **hasta 5 intentos**; los dudosos van a Legal |
| TB-4 | Si algo falla, **ruta actual en papel**. Responsable del portal: **IT del banco** |

**Ronda 8:** AS-T1 confirmado (5 intentos agotados → ruta en papel); TB-5 la corrección de Despacho reinicia los 10 días; TB-6 los 5 intentos son por documento; TB-7 «dudoso» = datos no coinciden. Versión vigente: **`proceso-to-be-v02.bpmn`** (`modelo-v02.json`); la v01 se conserva.

## 5. Siguiente paso
Revisar `proceso-to-be-v02.bpmn` en Camunda con `revision-camunda.md`, resolver los pendientes y seguir con los KPI (`10-kpis`, skill `definir-kpis`).
