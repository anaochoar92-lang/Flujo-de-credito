# Entrevista guiada aplicada al SOP de reexpedición — preguntas, no respuestas inventadas

## Objetivo de mejora hipotético
Reducir tiempos humanos y errores en: revisión de documentos, cotejo de datos, preparación de liquidación, notificaciones de vencimiento y solicitud de reexpedición. Este objetivo es **propuesta didáctica**, no decisión validada por la SDP.

## Preguntas adversariales — preguntar máximo cuatro cada ronda
1. ¿Qué parte del proceso de reexpedición se repite y cuántos casos se atienden por mes? ¿Dónde se registra ese volumen?
2. ¿En qué actividad exacta se inicia y termina el trabajo humano que queremos reducir? ¿Cuánto tiempo realmente ocupa, no cuánto tarda en el calendario?
3. Si la información de matrícula, CHIP, dirección y titular NO coincide, ¿qué control realiza un profesional y qué evidencia deja?
4. ¿Qué respuesta se produce cuando SIPA o BOG DATA está temporalmente indisponible? ¿Hay un SLA y un camino alternativo formal?
5. ¿Qué validaciones son deterministas y podrían implementarse como reglas, y cuáles exigen interpretación jurídica o técnica?
6. ¿El plazo de diez días es calendario o hábil? ¿Cuál evento lo inicia y qué norma o instrucción lo establece? **No asumir**.
7. ¿Se considera un error un rechazo, una devolución, un cálculo corregido o todos? Define una sola unidad de medición.
8. ¿Hay retrabajo si se reexpide un recibo? La reexpedición puede ser parte normal del proceso; no la clasificaremos como error por defecto.
9. ¿El titular debe verificación de identidad? ¿Se puede automatizar sin exponer datos personales?
10. ¿Cómo calcularemos los costos de error? ¿Se reduce gasto real o únicamente capacidad del profesional?
11. ¿Cuál riesgo normativo surge si la automatización clasifica mal un expediente? ¿Quién autoriza excepciones?
12. ¿La fuente de datos es auditable y sin información personal sensible para subirla a la nube?

## Cinco porqués (esqueleto)
Problema medido → por qué 1 → evidencia → por qué 2 → evidencia → por qué 3 → evidencia → por qué 4 → evidencia → por qué 5 → causa raíz *provisional*. No saltar a la solución de IA antes de descubrir la causa.

## TO-BE ilustrativo, por confirmar
- Validaciones deterministas de campos → tarea automática de reglas, con log y rechazo seguro.
- Documentos escaneados → extracción asistida (IDP) y revisión humana en casos de baja confianza.
- Preparación del recibo → integración controlada entre sistemas; retries limitados, timeout y ruta manual.
- Comunicación al titular → servicio de notificación con registro, reintentos controlados y acuse cuando exista.
- KPI → trabajo humano de cotejo, tasa de error, reexpediciones, cola de espera y beneficio anual estimado.

**No implementar un TO-BE en producción con esta información incompleta.**
