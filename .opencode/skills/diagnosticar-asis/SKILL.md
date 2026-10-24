---
name: diagnosticar-asis
description: "Medir el AS-IS mediante entrevistas adversariales, análisis de cuellos de botella y cinco porqués"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Objetivo
Traducir las diapositivas 45–62 (BPA, Value Stream Mapping, Stakeholders, Root Cause y 5 Whys) a diagnóstico verificable.

## Procedimiento
1. No alterar BPMN AS-IS; leer paso SOP, requisitos EARS y diagrama actual antes de sugerir cambios.
2. Construir inventario actividad por actividad: ID BPMN, responsable, tiempo de trabajo, espera, volumen/periodo, frecuencia de error, retrabajo, fuente, aporte al cliente (valor / necesario por control / desperdicio), tecnología y excepciones.
3. Preguntar máximo 4 preguntas adversariales por ronda, evitando respuestas sugeridas: ¿cómo se mide?, ¿qué casos quedan fuera?, ¿quién valida el dato?, ¿qué sucede si falla un sistema?
4. Aplicar cinco porqués **interactivamente**, una causa con evidencia por nivel; pedir confirmación antes de concluir causa raíz.
5. Generar `07-diagnostico/diagnostico.md` y `07-diagnostico/actividades.csv` (columnas ID, nombre, costo, tiempos, volumen, evidencia, control, oportunidad).
6. Clasificar observaciones como medido, declarado, estimado, hipotético; marcar vacíos `PENDIENTE`.

## Seguridad
No subir registros con PII a servicios cloud. Un cuello de botella no es evidencia suficiente para recomendar IA.
