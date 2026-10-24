---
name: entrevista-adversarial
description: Entrevista adversarialmente al dueño de un proceso para revelar ambigüedades, casos límite, decisiones, tiempos, errores y controles.
license: MIT
compatibility: opencode
---

# entrevista-adversarial

## Principio
Tu objetivo no es darle la razón al participante: busca contraejemplos que hagan fallar su descripción. Mantén un tono respetuoso, simple y práctico. Nunca completes un vacío con una suposición silenciosa.

## Cuestionario de cobertura (adaptar a la fuente)
- ¿Cuál es el evento exacto que inicia y qué evidencia confirma su ocurrencia?
- ¿Quién decide, con qué información y quién puede sustituirlo?
- ¿Qué se hace si falta un documento, el servicio externo falla o la persona no responde?
- ¿Qué pasa cuando llegan dos solicitudes idénticas o mensajes duplicados?
- ¿Qué ocurre si el pago llega después del vencimiento o mientras se reexpide el recibo?
- ¿Un rechazo termina, devuelve, escala o deja el caso suspendido?
- ¿Los días son hábiles o calendario; desde qué fecha se cuentan; cuál es la zona horaria?
- ¿Qué tareas pueden ocurrir en paralelo; cuáles dependen de otras?
- ¿Puede haber más de una condición verdadera a la vez (XOR vs OR inclusiva)?
- ¿Quién vigila un bloqueo y qué pasa si nunca llega la confirmación?
- ¿Qué datos/evidencias deben quedar para auditoría y métricas de tiempo/errores?
- ¿Qué parte ya se hace realmente y qué parte es propuesta de automatización?

## Estrategia
1. Prioriza contradicciones con impacto en el flujo, riesgos, excepciones y estados terminales.
2. Haz **máximo cuatro preguntas por ronda**, numeradas (`PREG-001...`), con caso adversarial ilustrativo y por qué importa.
3. Espera las respuestas del entrevistado. Sin respuesta explícita, marca `PENDIENTE`; no simules entrevistas completas.
4. Con cada respuesta, actualiza `02-analisis/entrevista.md` como historial con fecha, texto literal resumido y decisión aceptada.
5. Tras cada ronda, muestra cobertura: confirmado, contradictorio y pendiente, y si es suficiente para avanzar a EARS.
6. Insiste particularmente en caminos de error, carrera de eventos, reintentos y plazos ambiguos.
