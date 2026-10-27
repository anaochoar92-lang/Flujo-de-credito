# Preguntas adversariales en el ciclo SDD → Docker → ETL

### Negocio y alcance
1. ¿Cuál es el evento de negocio que crea un nuevo caso y cuál evidencia lo confirma?
2. ¿La validación del CHIP es requisito formal EARS o una hipótesis del prototipo?
3. ¿Cómo sabe el equipo que las áreas introducidas no violan los límites de su modelo?

### Arquitectura
4. ¿Dónde persisten los casos al apagar un contenedor? ¿Y al eliminar volúmenes?
5. ¿Qué ruta sigue una petición del navegador antes de llegar a Camunda Cloud?
6. ¿Pueden abrir PostgreSQL desde internet? ¿Por qué sería inadecuado en clase?
7. ¿Qué sucede si la API está sana pero Camunda está caído?

### Camunda
8. ¿Existe el processDefinitionId publicado? ¿Corresponde al AS-IS o TO-BE?
9. ¿Qué variable mueve el gateway? ¿Tiene el nombre y tipo esperados?
10. ¿Se comprueba el permiso para completar tareas? (En este demo NO hay RBAC propio.)
11. ¿Qué ocurre si Camunda creó la instancia pero PostgreSQL falló al guardar el ID? (Riesgo de consistencia.)

### ETL, Preset y ROI
12. ¿Cuál es la unidad de cada métrica? ¿Hay fechas en UTC?
13. ¿Cuál es el numerador y denominador de la tasa de cierre? ¿Evita dividir por cero?
14. ¿El valor sintético de referencia equivale a un ingreso, ahorro o beneficio? No.
15. ¿Se filtraron CHIP, nombres, documentos y secretos antes de subir un CSV?
16. ¿Qué control confirma que no faltaron filas al exportar? Manifiesto, conteos, SHA-256.
17. ¿Cómo reconstruirías los KPI después de reiniciar el equipo?
