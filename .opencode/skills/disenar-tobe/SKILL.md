---
name: disenar-tobe
description: "Rediseñar el BPMN TO-BE conservando trazabilidad, excepciones y supervisión humana"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Entrada obligatoria
AS-IS v01/v02, inventario, oportunidades priorizadas y EARS. La propuesta TO-BE NO es un hecho observado.

## Flujo
1. Explicar para la actividad seleccionada: origen BPMN, problema, alternativa sin tecnología, alternativa automatizada, riesgo, expectativa KPI y responsabilidad humana.
2. Hacer cuatro preguntas: disparador, criterios de decisión explícitos, tratamiento de casos anómalos, plan de contingencia/usuario responsable.
3. Producir `08-tobe/propuesta-to-be.md` con diferencias **AS-IS ↔ TO-BE** por IDs; redactar EARS nuevos como `REQ-TOBE-*` en `08-tobe/requisitos-ears-to-be.md`.
4. Solicitar autorización para modificar el modelo. Usar `arquitectura-bpmn`, `generar-bpmn`, `auditar-bpmn` del kit 1. Emitir `08-tobe/modelo-v02.json` y `08-tobe/proceso-to-be-v02.bpmn`, NUNCA sobrescribir original.
5. Comprobar en Camunda Modeler: límites pool-lane, mensajes entre pools, timer/error/boundary, eventos finales, merges, ruta manual ante fallo, tareas no automatizadas.
6. Entregar checklist `08-tobe/revision-camunda.md`. Marcar suposición de regla sin decisión como pendiente de revisión, no inventar un gateway.

## Condición de aprobado
El estudiante compara caminos feliz/excepción/timeout con un experto. **No** afirmar BPMN ejecutable sin configuración Camunda y validaciones formales adicionales.
