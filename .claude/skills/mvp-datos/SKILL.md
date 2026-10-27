---
name: mvp-datos
description: Diseñar y validar dos entidades mínimas, relaciones y persistencia SQLite/Postgres.
metadata:
  opencode/slash: "true"
---
# mvp-datos

**Finalidad:** Diseñar y validar dos entidades mínimas, relaciones y persistencia SQLite/Postgres.

Lee `AGENTS.md` y `CLAUDE.md`. Antes de programar, revisa `especificaciones/03-modelo-datos.md`, `app/db.py` y EARS..

## Conversación guiada

Pregunta al equipo, sin presuponer su respuesta:

1. ¿Qué identificación única tendrá un caso?
2. ¿Cuántos eventos puede tener un caso?
3. ¿Qué atributos no deben mostrarse en Preset?

Formula una pregunta por turno, máximo tres simultáneas. Resume la respuesta y pide validación humana.

## Procedimiento

Revisa el modelo caso/evento y crea una versión Mermaid ER simplificada con PK, FK, tipos, timestamps y razón de cada atributo. Primero SQLite y pruebas; PostgreSQL/Supabase solo si se tiene conexión válida en servidor. Nunca incluir credenciales en SQL o frontend.

## Salida verificable

Actualiza `especificaciones/modelo-equipo.md` sin alterar ORM hasta confirmación. Da pasos para `DATABASE_URL` y vistas solo lectura.

## Control de calidad / límite

No afirmar que SQLite es accesible directamente desde Preset Cloud; no abrir PostgreSQL al público sin controles.

Nunca inventes que se ejecutó una prueba externa. No modifiques BPMN, tablas ni datos sensibles sin aprobación explícita. Si el equipo usa su proceso real, no le atribuyas las reglas de la demostración.
