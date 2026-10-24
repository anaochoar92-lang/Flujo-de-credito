---
name: actualizar-sop
description: Recibe una nueva versión del DOCX del proceso, conserva histórico, extrae Markdown, compara cambios y conduce una revisión de impacto EARS-BPMN-KPI sin sobrescrituras.
compatibility: opencode
---

# actualizar-sop — actualizar el Word y reabrir las decisiones correctas

## Paso 0 — detectar y conservar el original
1. Trabaja en `trabajos/mi-proceso/` salvo que el estudiante indique el nombre de otra carpeta.
2. Identifica los DOCX de `01-fuentes/`, pregunta cuál analizar si hay más de uno. No adivines ni mezcles diferentes procedimientos.
3. El alumno conserva su archivo Word. Pide que primero guarde todos los cambios desde Word.
4. Ejecuta `py scripts/actualizar_sop.py --proyecto trabajos/mi-proceso --docx "trabajos/mi-proceso/01-fuentes/NOMBRE.docx"` en Windows; usa `python3` en Linux/macOS. Si no puedes ejecutar comandos locales, explica que es necesario ejecutar el script manualmente y **no afirmes que los archivos fueron actualizados**.
5. El script conserva instantáneas DOCX/MD en `01-fuentes/.historial_sop/`, actualiza el Markdown derivado `01-fuentes/SOP_ACTUAL.md` y genera `02-analisis/impacto-sop-vNN.md`; nunca modifica ni elimina fuentes originales.

## Paso 1 — revisión adversarial
1. Lee `SOP_ACTUAL.md` **como fuente vigente**, el informe de cambios y las salidas previas del proyecto.
2. Resume cambios por actividades, participantes, eventos, decisiones, datos, excepciones y criterios de aceptación. Etiqueta: agregado/eliminado/modificado/sin cambio.
3. No confundas un cambio editorial con un nuevo requisito de negocio. Conserva IDs EARS/BPMN cuando las actividades no cambiaron.
4. Plantea máximo cuatro preguntas en un turno. Espera respuestas y confirmación del dueño del proceso.
5. Explica qué artefactos quedarían afectados y cuáles pueden permanecer intactos.

## Paso 2 — reconstrucción selectiva, no un reinicio destructivo
Tras autorización explícita, aplicar skills `analizar-sop`, `entrevista-adversarial` y `redactar-ears` **solo a cambios aprobados**. Si corresponde, usar `arquitectura-bpmn`, `generar-bpmn` y `auditar-bpmn`, pero no sobrescribir un XML editado manualmente en Camunda: usar `reconciliar-bpmn` primero. Versionar cada revisión (v01, v02...). Si existe TO-BE/KPI/ROI, marcar potencial impacto; solo actualizar con `iterar-mejoras` una vez validado.

## Límite
Extraer DOCX a Markdown preserva el texto general de párrafos y tablas, pero **no extrae semánticamente imágenes, diagramas, tablas complejas, comentarios o cambios controlados de Word**. Solicita confirmación visual cuando existan.
