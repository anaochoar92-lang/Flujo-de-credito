from pathlib import Path
root=Path(__file__).resolve().parents[1]
def block(name,summary,question,inputs,work,deliver,verification):
 return f'''---
name: {name}
description: {summary}
metadata:
  opencode/slash: "true"
---
# {name}

**Finalidad:** {summary}

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa {inputs}.

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

{question}

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

{work}

## Salida verificable

{deliver}

## Control de calidad / límite

{verification}

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
'''
skills=[
('mvp-contexto','Reducir el SOP y BPMN a un MVP de una sola historia de negocio.','1. ¿Qué actor inicia el proceso y qué recibe al terminar?\n2. ¿Qué máximo de tres user tasks mostrarán en el frontend?\n3. ¿Cuáles son los límites legales y las tareas que aún NO automatizaremos?','`contexto/01-negocio.md`, el SOP y los BPMN AS-IS/TO-BE.','Selecciona una porción de proceso (vertical slice) con un evento inicial y final. Construye una tabla de actividad, responsable, dato de entrada, resultado, elementId BPMN y modo manual/automático. Separa dato fuente y supuesto.','Registra en `especificaciones/alcance-equipo.md` la historia de usuario, definición de terminado y 3 exclusiones.','No incluir todo el flujo institucional: el taller solo valida un segmento operable.'),
('mvp-ears','Convertir necesidades del negocio en tres requisitos EARS con aceptación comprobable.','1. ¿Cuál es el disparador exacto del requisito?\n2. ¿Qué debería ocurrir si el dato falta?\n3. ¿Qué API, tarea o evidencia puede demostrar el resultado?','`especificaciones/01-requerimientos-EARS.md` y `especificaciones/alcance-equipo.md` si existe.','Elige tres requisitos y usa patrón ubicuo, evento, estado, condicional o indeseado. Revisa expresiones ambiguas: rápido, seguro, automático, correctamente. Genera al menos un caso negativo y un mapeo hacia userTask o gateway.','Escribe `especificaciones/ears-equipo.md` con ID, EARS, prueba positiva, prueba adversarial, endpoint, elemento BPMN.','No crear código antes de la aprobación de EARS.'),
('mvp-datos','Diseñar y validar dos entidades mínimas, relaciones y persistencia SQLite/Postgres.','1. ¿Qué identificación única tendrá un caso?\n2. ¿Cuántos eventos puede tener un caso?\n3. ¿Qué atributos no deben mostrarse en Preset?','`especificaciones/03-modelo-datos.md`, `app/db.py` y EARS.','Revisa el modelo caso/evento y crea una versión Mermaid ER simplificada con PK, FK, tipos, timestamps y razón de cada atributo. Primero SQLite y pruebas; PostgreSQL/Supabase solo si se tiene conexión válida en servidor. Nunca incluir credenciales en SQL o frontend.','Actualiza `especificaciones/modelo-equipo.md` sin alterar ORM hasta confirmación. Da pasos para `DATABASE_URL` y vistas solo lectura.','No afirmar que SQLite es accesible directamente desde Preset Cloud; no abrir PostgreSQL al público sin controles.'),
('mvp-frontend','Integrar un formulario, lista de tareas humanas y evidencia desde el navegador.','1. ¿Qué campos van en el formulario inicial?\n2. ¿Qué ve el operador cuando una tarea aún no existe?\n3. ¿Qué acción humana cambia el proceso?','`app/static/index.html`, API y EARS.','Demuestra vertical slice: crear instancia, mostrar processInstanceKey, consultar user tasks, completar una, consultar bitácora. Usa `ENGINE_MODE=mock` primero. Mantén JS simple y backend para secretos.','Capturas o texto con URL, instancia creada, tarea activa, tarea completada y CSV. Si se modifica código, conservar test verde.','No exponer la app en Internet sin autenticación. No autocompletar en nombre de un funcionario real.'),
('mvp-camunda','Conectar la aplicación al clúster Camunda 8 existente usando REST API v2.','1. ¿Camunda 8.8+ REST v2 o Camunda 7?\n2. ¿Cuáles son los processDefinitionId publicados?\n3. ¿Las userTask son Camunda user tasks y el backend tiene permisos?','`docs/03-camunda-real.md`, `bpmn/`, `.env.example` y API.','Verifica URL raíz, token, processDefinitionId, variables FEEL, tareas publicadas. Cambia `ENGINE_MODE=camunda` solo con consentimiento humano. Inicia 1 instancia real, consulta tareas, completa 1. Si falla, identifica 401/403/404/422/503 o latencia de índice; no reescribe todo el BPMN por intuición.','Evidencia de HTTP, clave de instancia y dos tareas en Camunda, o informe explícito de bloqueo y contingencia.','No mostrar credenciales al agente, no desplegar sobre cluster productivo, no afirmar que mock equivale a prueba real.'),
('mvp-preset','Crear KPI trazables y llevar los CSV o PostgreSQL de solo lectura a Preset.','1. ¿Qué mejora promete el TO-BE y cómo se mide?\n2. ¿Qué columnas se necesitan para el numerador y denominador?\n3. ¿Los datos son reales o sintéticos?','`preset/GUIA.md`, los endpoints CSV y el diccionario ER.','Comienza con export CSV sin servicios externos, define tasa de cierre y tiempo de ciclo, carga CSV en Preset manualmente si la cuenta lo permite. Para Postgres usar vistas + rol solo lectura y SSL. Prepara un widget creado manualmente por el estudiante.','KPI en formato nombre/fórmula/unidad/fuente/granularidad/meta/limitación, CSV y captura/estado de widget Preset.','No transformar tiempo de ciclo en ROI sin horas efectivas, volumen y supuesto de monetización.'),
('mvp-auditar','Ejecutar pruebas técnicas y cuestionar consistencia SOP-EARS-BPMN-API-DB.','1. ¿Qué prueba demostraría que la mejora funciona?\n2. ¿Qué ocurre cuando un usuario completa dos veces la misma tarea?\n3. ¿Qué integración externa no ha sido probada todavía?','`tests/`, EARS, `app/`, el estado del entorno.','Corre `python -m pytest -q`, verifica formatos BPMN y evalúa: variables, actor, error de red, task ajena, duplicación, falta de CHIP, uso de datos sensibles, permisos. Contrasta resultado esperado vs observado.','Crear `especificaciones/auditoria-equipo.md` con pruebas, fallos, riesgos, bloqueos y plan de corrección.','No marcar como superado nada que no tenga evidencia. Diferenciar pruebas offline de integración real.'),
('mvp-iterar','Planear una mejora autónoma a partir de las pruebas sin romper el MVP demo.','1. ¿Cuál es el cambio más pequeño que aumenta valor al usuario?\n2. ¿Qué EARS/BPMN/tablas/endpoints se verán afectados?\n3. ¿Cómo se comprobará sin perder funcionamiento previo?','`especificaciones/`, `AGENTS.md`, `docs/02-sesiones-60-min.md`.','Ordena cambios en tamaño S/M/L y riesgo. Prioriza 1 historia de menos de 90 minutos. Escribe EARS, plan con archivos involucrados, test negativo y fallback. Espera confirmación. Al terminar, regresa a `mvp-auditar`.','Crear `especificaciones/backlog-autonomo.md` con siguientes 3 incrementos y criterio de aceptación para cada uno.','Nunca rehacer todo el proyecto ni introducir agentes autónomos en producción como atajo.'),
]
for i,(name,summary,qs,inputs,work,deliver,verification) in enumerate(skills,20):
 sdir=root/'.claude'/'skills'/name;sdir.mkdir(parents=True,exist_ok=True)
 (sdir/'SKILL.md').write_text(block(name,summary,qs,inputs,work,deliver,verification),encoding='utf8')
 cmd=root/'.opencode'/'commands'/f'{i}-{name.removeprefix("mvp-")}.md'
 cmd.write_text(f'---\ndescription: {summary}\n---\n\nLee las instrucciones del skill `.claude/skills/{name}/SKILL.md` y ejecútalo como tutor para el equipo. La solicitud del participante es: $ARGUMENTS\n',encoding='utf8')
 print(i,name)
