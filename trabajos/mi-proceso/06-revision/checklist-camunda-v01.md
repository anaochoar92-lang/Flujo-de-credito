# Checklist de revisión visual en Camunda Modeler — proceso-v01.bpmn

Marcar cada punto al revisar. Si se cambia algo, guardar como `proceso-v02.bpmn`.

- [ ] El archivo abre sin errores y se ven 1 pool y 6 carriles: Negocio, Riesgo, Analista de crédito, Legal, Sistema y Desembolso.
- [ ] El inicio «Cliente solicita crédito» está en el carril de Negocio.
- [ ] «¿Cliente apto?» tiene 3 salidas con nombre: Apto, Corregir datos y Rechazar.
- [ ] «¿Decisión del análisis?» tiene 2 salidas: Aprobar (con o sin condiciones) y Rechazar.
- [ ] «Informar decisión al cliente» → «¿Cliente acepta y continúa?» → «¿Aprobada con condiciones?» se leen en orden.
- [ ] La línea «Volver a análisis» (Modificar datos → Analizar crédito) no tapa «Informar decisión al cliente». Si la tapa, arrastrarla (T-03).
- [ ] El temporizador «10 días sin expediente completo» aparece pegado al borde de «Recopilar expediente» y es **interruptor** (borde continuo, no discontinuo).
- [ ] El temporizador lleva a «Cerrar solicitud automáticamente» en el carril Sistema.
- [ ] Los bucles «Incompleta: seguir recopilando» y «Falta, se rechaza o no cuadra» vuelven a «Recopilar expediente».
- [ ] Hay 5 fines con nombre distinto: rechazada por Riesgo, rechazada, cliente no acepta, expediente incompleto y crédito desembolsado.
- [ ] Ningún texto queda encima de otro. Si pasa, mover la etiqueta.
- [ ] Exportar la imagen: *File → Export As → PNG* → `05-bpmn/proceso-v01.png`.
