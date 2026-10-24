# Cambios v01 → v02 — Flujo de crédito (AS-IS)

**Fecha:** 2026-10-24 · **Skill:** `reconciliar-bpmn` · **Tipo de fuente:** (a) instrucciones en lenguaje natural, respuestas de la ronda 2. Nadie editó el v01 en Camunda.

## Resultado
Las respuestas **confirman la estructura** del v01. Cambian solo textos:

| Elemento | v01 | v02 | Disparador |
|---|---|---|---|
| `TMR_001` | 10 días sin expediente completo | **10 días hábiles** sin expediente completo | PREG-013 |
| `F_024` | Falta, se rechaza o no cuadra | Falta, no cuadra o **documentos con más de 1 mes** | PREG-014 |
| Trazas JSON de `TMR_001`, `ACT_008`, `GW_006` | — | Añaden PREG-007, PREG-008, PREG-013, PREG-014 y PROC-010 | — |

El temporizador sigue **sin expresión ISO**, porque `P10D` serían días calendario. Los días hábiles necesitan un calendario laboral del motor que se use, y eso se define solo si se llega a ejecutar el proceso.

## Hallazgos de la auditoría v01 que cambian
| ID | Estado |
|---|---|
| S-01 (el temporizador se reinicia en cada vuelta) | **Resuelto**: es el comportamiento real (PREG-013). El dibujo es correcto |
| S-02 (devolución de Despacho sin límite) | Sigue. Ahora hay datos: 20 % de devoluciones, por documentos de más de 1 mes. Pasa al diagnóstico |
| S-03 (AS-01) | Sigue por confirmar |
| S-04 (sin salida si el desembolso falla) | Sigue |

## Verificación
- `especificacion-v02.json` → `proceso-v02.bpmn` con `scripts/crear_bpmn.js`.
- `validar_bpmn.js`: 0 errores y 8 advertencias, las mismas del v01.
- Sin contar los nombres, el v02 es idéntico al v01: 0 líneas distintas.
- Los archivos v01 no se modificaron.
