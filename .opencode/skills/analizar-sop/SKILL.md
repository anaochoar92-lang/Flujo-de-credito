---
name: analizar-sop
description: Analiza descripciones SOP en español, inventaría actores, entradas, actividades, decisiones, excepciones y vacíos sin inventar reglas.
license: MIT
compatibility: opencode
---

# analizar-sop

## Entrada
Lee todos los `.md` y `.txt` de `trabajos/mi-proceso/01-fuentes/` y cualquier documento Word convertido a texto por herramientas disponibles. Si el participante aporta un BPMN, inspecciona su XML con `scripts/inspeccionar_bpmn.py` antes de interpretarlo.

## Método
1. Define objetivo, inicio, fin y alcance del proceso **AS-IS**.
2. Identifica participantes/roles, sistemas, documentos, estados, actividades, decisiones, temporizadores y eventos de comunicación.
3. Da IDs estables `ACT-001`, `DEC-001`, `EVT-001`; apunta cada elemento a sección/fragmento de fuente.
4. Detecta verbos vagos (`gestionar`, `validar`, `revisar`) que carecen de criterios verificables.
5. Identifica caminos felices, excepciones, bucles, aprobaciones, interrupciones y casos de desistimiento.
6. Si existen fuentes contradictorias, anota las dos versiones; no decidas por tu cuenta.

## Entregables
Escribe `02-analisis/inventario.md`, `02-analisis/vacios.md` y `02-analisis/glosario.md`. Tablas con ID, descripción, fuente, estado, responsable y pregunta abierta. No redactes aún requisitos EARS ni BPMN definitivo.
