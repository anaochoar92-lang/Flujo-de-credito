---
name: reconciliar-bpmn
description: Integra correcciones escritas o BPMN editados en Camunda preservando versiones, diferencias, decisiones y trazabilidad SOP–EARS–JSON–BPMN.
license: MIT
compatibility: opencode
---

# reconciliar-bpmn

## Reglas de ida y vuelta
1. Determina si la fuente nueva es (a) instrucciones en lenguaje natural, (b) XML BPMN modificado en Camunda, o (c) ambas.
2. Nunca sobreescribas la versión anterior. Genera un informe `06-revision/cambios-vXX.md` con qué cambia, qué permanece y por qué.
3. Si el usuario modifica BPMN en Camunda, ejecuta `inspeccionar_bpmn.py` y `validar_bpmn.py`; compara nodos y flujos con la versión anterior. Documenta cambios no expresables en el JSON auxiliar, como subprocesos, DI ajustado y extensiones.
4. Confirma con el participante las decisiones de negocio afectadas: actualiza SOP/EARS sólo después de validación humana.
5. Evita «regenere desde JSON» sobre un BPMN editado: perdería geometría y constructos no soportados. Antes reconcilia cambios al JSON o conserva el XML editado como maestro.
6. Si la corrección parte del texto, edita fuente derivada y EARS, actualiza JSON y genera `proceso-v(N+1).bpmn` dejando intacto el anterior.
7. Ejecuta validación y produce tabla de trazabilidad bidireccional de cambios.

## Entrega
`06-revision/cambios-vXX.md`, `06-revision/preguntas-abiertas.md`, `05-bpmn/proceso-vXX.bpmn` (si cambió XML), revisiones EARS y un resumen comprensible del nuevo comportamiento.
