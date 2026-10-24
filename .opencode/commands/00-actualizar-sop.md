---
description: Releer un DOCX actualizado, versionar, comparar y proponer cambios a EARS/BPMN sin sobrescribirlos
---

Aplica el skill `actualizar-sop` del proyecto. Trabaja en `trabajos/mi-proceso/` salvo que el usuario indique otra carpeta. Detecta el Word actualizado en `01-fuentes/`, ejecuta `scripts/actualizar_sop.py` para crear Markdown e historial de versiones y lee el informe de diferencias. Si hay varios DOCX, pregunta cuál usar. No cambies EARS, JSON, BPMN, TO-BE, datos ni KPI sin mostrar un análisis de impacto y obtener aprobación. Haz como máximo cuatro preguntas por turno. Sigue `AGENTS.md`. Argumentos adicionales: $ARGUMENTS
