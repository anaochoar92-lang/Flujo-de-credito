# Ingeniería basada en agentes en 2026: prácticas del taller

1. **Contexto minimizado y verificable:** usar `AGENTS.md` / `CLAUDE.md`, contratos EARS y BPMN, no introducir documentos enormes en cada solicitud. Separar hechos del SOP de hipótesis del estudiante.
2. **Spec Driven Development:** especificar → clarificar → diseñar → tareas → implementar → verificar. Github Spec Kit utiliza una secuencia equivalente.
3. **Vertical slices:** integrar un endpoint, una tarea humana, un registro y una prueba antes de añadir más funciones.
4. **Roles separados (lógicamente):** analista descubre requisitos, arquitecto modela, desarrollador implementa, revisor adversarial intenta romper flujos, probador comprueba. No son necesariamente cinco modelos/agentes distintos.
5. **Cambios pequeños con puertas de aprobación humana:** cada iteración comienza con EARS y plan de impacto. Dejar pasar los tests y lectura de BPMN antes del siguiente paso.
6. **Herramientas de mínima autoridad:** la IA puede modificar archivos del proyecto; no tiene permiso para mover dinero, crear usuarios admin, desplegar producción o publicar secretos.
7. **Pruebas deterministas más pruebas de integración reales:** mock es evidencia de lógica local; no demuestra que la API real Camunda, Supabase o Preset esté disponible.
8. **Observabilidad y auditoría:** correlación `caso_id`, `radicado`, `processInstanceKey`, `eventos`, timestamps y nombres de actividades. No guardar PII.
9. **Trazabilidad y versionado:** SOP/AS-IS → EARS → arquitectura de datos/API → TO-BE → pruebas → KPI/CSV. Registrar qué cambió y por qué.
10. **Fallos y excepciones deliberados:** CHIP ausente, task ya completada, token caducado, falta de permisos, error de red, doble clic. Diseñar al menos un caso negativo.
11. **Seguridad primero:** `ENGINE_MODE=mock` por defecto, `.env` ignorado por Git, backend local, RLS en Supabase si se añade cliente público. Preset usa usuario SQL separado de solo lectura.
12. **Veracidad del resultado:** un agente debe indicar si realmente ejecutó una prueba; capturas y logs no equivalen a garantía de producción.

**Fuentes de apoyo para el docente (verificar versiones):**
- https://github.com/github/spec-kit
- https://docs.opencode.ai/docs/skills/
- https://code.claude.com/docs/en/skills
- https://docs.camunda.io/docs/apis-tools/orchestration-cluster-api-rest/orchestration-cluster-api-rest-overview/
- https://docs.preset.io/docs/postgres-connection
