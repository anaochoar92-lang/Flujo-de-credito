# Vacíos y puntos sin definir — Solicitud de crédito Expomóvil (v01)

**Fecha:** 2026-10-23 · **Fuente:** `01-fuentes/Proceso_Solicitud_Credito_BPMN.xlsx` · Ver `inventario.md`.
**Prioridad:** A = cambia el flujo o un fin del proceso · B = cambia una regla o un responsable · C = dato o detalle.

| ID | Vacío | Elementos | Por qué importa | Prioridad | Fuente | Pregunta |
|---|---|---|---|---|---|---|
| VAC-001 | La fuente no menciona «preaprobado». No se sabe si este proceso **es** el de preaprobado, si lo incluye como una variante o si es otro proceso | Todo | Define el alcance del proyecto | A | PB-A1; nombre del repositorio | PREG-001 |
| VAC-002 | Canal y evidencia del inicio: cómo «manifiesta interés» el cliente (oficina, concesionario, feria, web) y qué lo registra | EVT-001 | Define el evento de inicio | B | PB-F5 | PREG-005 |
| VAC-003 | G1 «No apto» devuelve a Negocio para corregir. No hay rechazo por Riesgo: un cliente con mal buró daría vueltas sin fin | DEC-001 | Falta un estado terminal | A | PB-F8 | PREG-002 |
| VAC-004 | Riesgo (T2) y el Analista (T3) evalúan ambos «riesgo». No se sabe en qué se diferencian ni si alguno es automático | ACT-002, ACT-003 | Posible doble trabajo y candidato a automatizar | B | PB-E7, E9 | PREG-006 |
| VAC-005 | «Aprobar con condiciones» vuelve a T1. ¿Repite Riesgo y análisis? ¿Debe aceptar el cliente las condiciones? | DEC-002, ACT-001 | Puede añadir días al proceso y falta el paso del cliente | A | PB-F10 | PREG-004 |
| VAC-006 | No hay notificación al cliente: ni de la aprobación, ni de las condiciones, ni del rechazo | E2, G2 | Falta una interacción clave con el cliente | A | — | PREG-004 |
| VAC-007 | Expediente: qué documentos, quién los entrega (cliente, concesionario) y qué pasa si nunca se completan (G3 es un bucle sin límite) | ACT-004, DEC-003 | Es la tarea más larga (5 días) y no tiene salida | A | PB-F12, F13 | PREG-003 |
| VAC-008 | G4 devuelve a Legal un expediente que Legal ya dio por completo en G3. No se sabe qué criterio distinto aplica cada uno | DEC-003, DEC-004 | Reproceso de unos 12 días | A | PB-F13, F16 | PREG-003 |
| VAC-009 | «Escanear documentación» tarda 3 días; no se explica la causa | ACT-005 | Posible espera, no trabajo real | C | PB-F14, TI-F6 | PREG-007 |
| VAC-010 | El expediente se escanea **y** se envía en sobre físico. No se sabe para qué sirve el sobre si ya existe la copia digital | ACT-005, ACT-006, ACT-007 | Candidato claro a automatizar | B | PB-E14, E15, E17 | PREG-008 |
| VAC-011 | Desembolso «verifica el sobre», pero no tiene decisión si el sobre está mal. «Post-desembolso» no está descrito. No se sabe de quién es la «cuenta indicada» | ACT-007 | Falta una salida y el alcance final | B | PB-F17 | PREG-009 |
| VAC-012 | El Analista de crédito analiza (T3) y también autoriza el expediente (T6). ¿Es la misma persona? ¿Hay segregación de funciones? | ROL-003 | Control interno | B | PB-B9, B15 | PREG-010 |
| VAC-013 | No hay sistemas nombrados: dónde se registra la solicitud, cómo se consulta el buró y cómo se desembolsa | Todo | Necesario para automatizar | B | — | PREG-011 |
| VAC-014 | Origen de los tiempos (17 días hábiles): ¿medición real o estimación? No hay plazos máximos ni qué pasa al vencerse | Hoja Tiempos | Base de KPI y ROI | B | TI; comentario PB-H19 | PREG-007 |
| VAC-015 | Garantías: T3 las analiza, pero no hay ningún paso para registrar la garantía del vehículo, ni contrato, firma o seguros | ACT-003, ACT-004 | Posibles pasos que faltan | B | PB-E9 | PREG-012 |
| VAC-016 | No hay fin por desistimiento o cancelación del cliente en ningún punto | Todo | Falta un estado terminal | B | — | PREG-003, PREG-004 |

## Verbos vagos detectados
| Elemento | Verbo | Qué falta para que sea verificable |
|---|---|---|
| T2 | Evaluar | Criterios de «apto»: puntaje de buró, políticas concretas |
| T3 | Analizar | Umbrales de capacidad de pago y tipo de garantía |
| T4 | Recopilar | Lista de documentos y de quién se obtienen |
| T6 | Verificar / autorizar | Qué se revisa y con qué atribución se autoriza |
| T7 | Gestiones post-desembolso | Cuáles son |
