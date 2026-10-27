# Preguntas para cada equipo
1. ¿Quién inicia el caso y con qué autorización? ¿Qué pasa si pulsa dos veces?
2. ¿Cuál tarea BPMN activa esta página? ¿Cómo identificas `bpmnElementId` y `taskKey`?
3. ¿Qué datos son obligatorios y qué valores inválidos podrían ingresar?
4. ¿Qué sucede si el backend guarda el expediente pero Camunda no responde?
5. ¿Qué ocurre si dos usuarios completan la misma tarea? ¿Hay control de acceso?
6. ¿Qué datos permanecen en PostgreSQL y cuáles solo son variables Camunda?
7. ¿Qué mensaje recibe el usuario si hay timeout o el proceso termina?
8. ¿Cómo probaremos que una aprobación movió la instancia en Camunda?
9. ¿Qué cambios exige el ER? ¿Existe migración reversible?
10. ¿Cuáles datos no pueden exportarse a Preset? ¿Qué KPI sería verificable?
