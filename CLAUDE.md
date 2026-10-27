# Instrucciones de Claude Code

Lee y cumple `AGENTS.md`, que es la constitución única compartida con OpenCode. Antes de escribir código, lee `contexto/01-negocio.md`, `especificaciones/01-requerimientos-EARS.md` y los contratos de API. Sigue el patrón Especificar → Clarificar → Planear → Implementar → Verificar, una historia EARS por iteración.

Los skills de este taller están en `.claude/skills/<nombre>/SKILL.md` y pueden invocarse en Claude Code como `/mvp-contexto`, `/mvp-ears`, `/mvp-datos`, `/mvp-frontend`, `/mvp-camunda`, `/mvp-preset`, `/mvp-auditar`, `/mvp-iterar`. No afirmes que probaste Camunda real ni Preset si solo corriste pruebas locales. Nunca cambies `.env` para apuntar a servicios externos sin autorización humana.


## Extensión v2.0 contenedores

Consultar `docs/06-docker-compose-estudiantes.md` y `docs/08-diccionario-etl-kpis.md`. Desplegar de forma guiada; no revelar `.env`, no borrar volúmenes ni dar como validada conexión Camunda/Preset externa sin evidencia.
