---
name: generar-bpmn
description: Genera archivos BPMN 2.0 XML con DI desde especificaciones JSON del taller y comprueba automáticamente su estructura básica.
license: MIT
compatibility: opencode
---

# generar-bpmn

## Flujo
1. Lee `04-modelo/especificacion.json` y `docs/contrato-json.md`.
2. Revisa IDs, procesos, flujos, decisiones, eventos y mensajes. Solicita aclaración sólo para contradicciones bloqueantes; en otros casos crea `pendientes.md`.
3. Ejecuta `python scripts/crear_bpmn.py trabajos/mi-proceso/04-modelo/especificacion.json trabajos/mi-proceso/05-bpmn/proceso-v01.bpmn` o `py` en Windows.
4. Ejecuta `python scripts/validar_bpmn.py .../proceso-v01.bpmn --json .../validacion-v01.json`.
5. Reporta cifras de errores y advertencias, sin afirmar «validación BPMN formal completa»; una revisión con Camunda Modeler es obligatoria.
6. Escribe `05-bpmn/registro-versiones.md` con origen JSON, fecha, pendientes y acciones para abrir el archivo.
7. No sobrescribas `proceso-v01.bpmn`; incrementa versión si existe.

## Controles
Valida que todos los nodos estén conectados, que eventos tengan tipo, que un `messageFlow` cruce pools y que un `eventBasedGateway` conduzca a esperas apropiadas. No agregues extensiones Camunda/Zeebe ni marques ejecutable sin solicitud expresa y evidencias suficientes. BPMN DI debe tener formas y conectores visibles.
