---
name: auditar-bpmn
description: Revisa BPMN 2.0 aportados o generados: estructura XML, semántica, trazabilidad EARS, excepciones y cambios visuales en Camunda Modeler.
license: MIT
compatibility: opencode
---

# auditar-bpmn

## Entrada
Archivo `*.bpmn` o `*.xml` y, si existe, su EARS, SOP y JSON. Primero ejecuta `scripts/validar_bpmn.py` y `scripts/inspeccionar_bpmn.py`.

## Auditorías independientes
A. **Técnica:** XML legible; IDs; referencias source/target; límites de pool; DI; nodos muertos; inicios/fines; gateways y condiciones. Señala que no sustituye XSD ni lint Camunda.
B. **Semántica:** ¿después de cada compuerta existe un camino concreto? ¿una aprobación rechazada retorna? ¿eventos de espera con fin? ¿timeouts y errores? ¿finales ambiguos? ¿carreras pago-vencimiento? ¿loops sin salida? ¿paralelo sin sincronización?
C. **Trazabilidad:** vincula cada nodo al `REQ-###` o `PROC-###`; identifica EARS sin representación y nodos sin requisito trazable. Reconoce requisitos no modelables en BPMN.
D. **Usabilidad:** nombres legibles, pools/lanes adecuados, flechas no confusas, leyenda de abreviaturas.

## Resultado
Crea `06-revision/auditoria-vXX.md` con severidad BLOQUEANTE, IMPORTANTE o EDITORIAL; ubicación (ID), evidencia, impacto y corrección sugerida. Crea checklist para revisión **visual** en Camunda Modeler. Nunca corrijas silenciosamente ni asegures que un diagrama es ejecutable porque se visualiza.
