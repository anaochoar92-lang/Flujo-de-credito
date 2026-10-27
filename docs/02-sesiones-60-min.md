# Guía docente · 2 sesiones de 60 minutos

**Prerrequisitos antes del cronómetro:** Python 3.11+ instalado y entorno virtual con dependencias; OpenCode o Claude Code abierto; Camunda 8.8+ Orchestration REST API accesible, modelos AS-IS/TO-BE ya desplegados (en demo docente se pueden desplegar los del kit); credenciales y URL Camunda validadas por docente. Para estudiantes sin cuenta externa, `ENGINE_MODE=mock`. Nunca usar documentos reales ni secretos en la plataforma IA sin política de datos.

## Sesión 1 — especificación → vertical slice local

| Minutos | Actividad | Comando/salida |
|---|---|---|
| 00–08 | Alcance: negocio, SOP, AS-IS/TO-BE desplegados, delimitar 2–3 tareas | `/mvp-contexto`; aceptar solo el subproceso de revisión |
| 08–18 | EARS adversarial, traza a tareas humanas y cálculo demo | `/mvp-ears` → 3 requisitos priorizados |
| 18–28 | Modelo ER y datos: comparar SQLite vs Supabase | `/mvp-datos` → mermaid + dos tablas |
| 28–42 | Arrancar FastAPI y navegador en modo `mock`, crear dos casos | `scripts/arrancar.ps1` o `.sh` |
| 42–54 | Completar dos user tasks y explicar bitácora | `/mvp-frontend` → evidencias |
| 54–60 | Test + commit/capturas del MVP local | `python -m pytest -q` |

**Resultado demostrable:** front accesible, caso TO-BE creado y tareas de revisión/aprobación completadas; JSON y CSV exportados. Si el equipo no termina el análisis EARS, usa el ejemplo y conserva sus preguntas abiertas.

## Sesión 2 — Camunda real → datos → Preset

| Minutos | Actividad | Comando/salida |
|---|---|---|
| 00–10 | Verificar Camunda 8, processDefinitionId, acceso token, BPMN tareas de usuario | `/mvp-camunda` |
| 10–25 | Cambiar ENGINE_MODE a camunda, iniciar instancia real, observar en Operate/Tasklist | `/api/health` y Swagger `/docs` |
| 25–37 | Completar desde el front dos user tasks y verificar la instancia en Camunda | Front + refresh (indexación asíncrona) |
| 37–45 | Revisión del ER; escoger SQLite local o PostgreSQL/Supabase (el segundo es extensión) | `/mvp-datos` |
| 45–53 | Exportar CSV a Preset y crear un widget | `/mvp-preset` |
| 53–60 | Revisar evidencias, preguntas adversariales y backlog autónomo | `/mvp-auditar`, `/mvp-iterar` |

**Contingencia:** si la API real no está lista antes de clase, ejecutar el recorrido completo en `mock` y dejar la integración como trabajo autónomo. El funcionamiento de Camunda externo NO se deduce de las pruebas mock.

## Guion docente (liquidación urbanística)

1. Mostrar `contexto/SOP_Liquidacion_SDP_referencia.md`, resaltar que la SDP registra CHIP, áreas y la revisión del profesional. El modelo completo es mucho más amplio.
2. Mostrar `bpmn/liquidacion_cargas_tobe_mba.bpmn` en Camunda Modeler: una prevalidación, un gateway, subsanación si falla, revisión, aprobación.
3. Desde la web crear expediente `SDP-DEMO-001` con CHIP y enseñar que omite subsanación en TO-BE.
4. Completar las dos tareas humanas desde la web. Mostrar eventos en `/api/events` y KPI en pantalla.
5. Crear expediente TO-BE SIN CHIP. Explicar la bifurcación EARS-04.
6. Cambiar a Camunda real y repetir con instancias desplegadas, si cuentas con conectividad.
7. Descargar CSV, cargar en Preset, construir un KPI de cierre por escenario.

## Puntos de control: el grupo no debe continuar si...

- desconoce el ID BPMN desplegado o la versión API de su clúster;
- hay secretos en JS o documentos que subirán a IA;
- el requisito EARS no define comportamiento observable;
- los datos del CSV son sensibles;
- Camunda usa user tasks legadas incompatibles con API v2;
- un agente afirma haber probado conectividad sin haberla verificado.

## Evaluación propuesta (100 puntos)

| Dimensión | Puntos | Evidencia |
|---|---:|---|
| Entender negocio y seleccionar historia vertical | 15 | alcance validado |
| EARS y entrevista adversarial | 20 | 3 requisitos y un caso negativo |
| BPMN + user tasks + instancia | 25 | IDs, clave y dos transiciones |
| Front + API + SQLite/Postgres | 20 | acciones y registro de auditoría |
| KPI + CSV + interpretación (o widget) | 10 | fórmula, fuente y limitación |
| Pruebas, seguridad y transferencia | 10 | tests, límites y backlog |

Mínimo para aprobar: resultado visible en modo mock; para calificación de integración Camunda, exigir una captura verificable y prueba real. El docente puede sustituir la ponderación según el nivel técnico del grupo.
