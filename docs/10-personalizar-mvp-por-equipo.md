# Personalización autónoma por equipos de estudiantes

## Invariantes del kit
Mantener la separación `web`, `api`, `db` y la ETL. Mantener que Camunda y Preset sean servicios externos, no instalar Camunda local. Proteger `.env`.

## Una iteración SDD para implementar una sola user task

1. Incluir en `contexto/` objetivo de negocio, participantes, producto o servicio, restricciones y fuente legal cuando proceda.
2. Registrar SOP de la tarea, EARS identificable `REQ-NN` y su relación con `bpmnElementId`.
3. Describir formulario: campos, tipo, validación, evento de envío, datos guardados, errores previstos.
4. Actualizar `especificaciones/03-modelo-datos.md` y las clases SQLAlchemy con una migración controlada (no editar DB real sin copia).
5. Crear un test primero, adaptar endpoint Python y formulario HTML/JS. No generar el proyecto entero otra vez.
6. Verificar el nuevo comportamiento en `ENGINE_MODE=mock`; conservar pruebas previas.
7. Si procede, desplegar BPMN corregido en Camunda SaaS, configurar API real y verificar sus tareas humanas.
8. Modificar `scripts/etl_preset.py` solamente para columnas justificadas por un KPI; exportar de nuevo y validar calidad del CSV.
9. Crear widget en Preset Starter y documentar fórmula, fuente, valor y limitación.

## Preguntas obligatorias a los participantes
- ¿La tarea tiene un responsable real y un nivel de autorización definido?
- ¿Qué variable BPMN recibe el resultado de la tarea? ¿Es tipo número, texto o booleano?
- ¿Qué diferencia hay entre información de la UI, hechos de auditoría y variables del motor Camunda?
- ¿Cómo se detecta doble clic o actualización simultánea en la misma tarea?
- ¿Qué eventos, KPI y reglas de confidencialidad cambian al añadir este formulario?

## Estructura sugerida
`contexto/`, `especificaciones/`, `bpmn/`, `app/`, `tests/`, `docs/`, `exports/`.
Entrega iterativa: `README` de la tarea, requisito EARS, diagrama ER actualizado, formulario, endpoint, test, evidencia, CSV, widget o captura.
