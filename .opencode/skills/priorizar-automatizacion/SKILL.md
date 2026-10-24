---
name: priorizar-automatizacion
description: "Priorizar mejoras usando criticidad, matrices ponderadas, viabilidad y controles"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Objetivo
Identificar candidatas de automatización según diapositivas 69–80. Mantener pesos explícitos, no presentarlos como establecidos en PPT.

## Preguntas fundamentales
- ¿Qué actividad es repetitiva, masiva y basada en reglas estables?
- ¿Existen integraciones, importaciones manuales, documentos IDP o validaciones estructuradas?
- ¿Qué sucede ante excepciones, caídas de sistema y casos jurídicos/técnicos delicados?
- ¿Dónde están el cuello de botella y la causa raíz acreditada?
- ¿Qué costo real y costo de mantenimiento tendría automatizar?
- ¿Quién respalda cada hipótesis de horas, volumen, errores y probabilidad de éxito?

## Matriz didáctica (NO oficial)
Puntajes 1–5; ponderar (impacto cliente 25%, volumen 20%, urgencia 15%, factibilidad 20%, reducción de riesgos 20%). La complejidad técnica se invierte dentro de **factibilidad**, y el riesgo de automatización se documenta como veto incluso para una puntuación alta. Enseñar que los pesos son decisiones de diseño revisables del grupo.

## Salidas y control
`07-diagnostico/oportunidades.csv`, `07-diagnostico/priorizacion.md`: 3–5 alternativas, tecnologías alternativas (reglas/validación, APIs, RPA, BPM, IDP, IA) y decisiones conservar humano, eliminar o simplificar. Pedir al usuario aprobar una oportunidad. Si no hay beneficio claro, recomendar NO automatizar.
