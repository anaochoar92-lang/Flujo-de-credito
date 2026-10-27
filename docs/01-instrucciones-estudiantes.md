# Instrucciones para participantes (sin conocimientos de programación)

## Antes de la sesión

Tener el ZIP descomprimido, Python 3.11+, acceso a una terminal PowerShell y una cuenta funcional de OpenCode o Claude Code. No se requieren Node, Docker ni un servidor PostgreSQL para completar la ruta mínima.

## Trabajo en 10 pasos

1. Abrir `README.md` del ZIP. Elegir **OpenCode** o **Claude Code** y abrir en la herramienta la carpeta del proyecto.
2. Hablar con el agente y usar `/20-contexto` (OpenCode) o `/mvp-contexto` (Claude Code). Explicar el negocio con sus propias palabras.
3. Repetir con `/21-ears` o `/mvp-ears` y confirmar tres requisitos EARS.
4. Abrir la carpeta `bpmn`, identificar evento inicial y las dos tareas humanas.
5. Ver diagrama ER `especificaciones/03-modelo-datos.md`; responder quién usa cada dato.
6. Abrir PowerShell en la carpeta del proyecto y ejecutar `powershell -ExecutionPolicy Bypass -File .\scripts\arrancar.ps1`.
7. En `http://127.0.0.1:8000`, crear un expediente TO-BE. Guardar captura de la clave de instancia.
8. Seleccionar el caso, consultar sus tareas y completar por lo menos dos. Registrar dos observaciones distintas.
9. Descargar los tres CSV, explicar el indicador `tasa de cierre` y cargar uno en Preset si hay conectividad.
10. Ejecutar `python -m pytest -q` dentro del entorno virtual y solicitar al agente `/26-auditar` o `/mvp-auditar`.

La ruta real Camunda (si ya se publicó proceso en el clúster y hay permisos) se prepara siguiendo `docs/03-camunda-real.md`. Si falta acceso, la demostración en mock es la ruta mínima válida.

## Entregable de cada grupo

Una carpeta con contexto de negocio, tres EARS, BPMN AS-IS y TO-BE referenciados, mermaid ER, captura del frontend con clave, evidencia de dos tareas, un CSV, un indicador y una lista de pendientes honestos.

## Errores frecuentes

- No abre el puerto 8000: verificar si hay otro programa ocupándolo.
- La IA pregunta por tokens: mantener el modo mock para empezar y no compartir secretos.
- No aparece una tarea de Camunda: confirmar que el proceso está desplegado, revisar la indexación, refresh y la ruta REST v2.
- No se conecta Preset a SQLite: SQLite está en disco local; exportar CSV.
- Una variable de BPMN es desconocida: revisar el nombre exacto y su tipo en Modeler y `app/main.py`.
