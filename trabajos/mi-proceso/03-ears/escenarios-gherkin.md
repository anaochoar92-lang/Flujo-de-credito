# Escenarios de aceptación (Gherkin) — AS-IS v01 · Flujo de crédito

Un escenario por REQ. Los datos de ejemplo son ficticios.

```gherkin
Característica: Solicitud de crédito Expomóvil (AS-IS)

  Escenario: REQ-001 / REQ-002 — registro y envío a Riesgo
    Dado un cliente interesado en un crédito Expomóvil
    Cuando la Persona de Negocio registra la solicitud con monto, plazo y vehículo, y la envía
    Entonces la Persona de Riesgo tiene asignada «Evaluar solicitud»

  Escenario: REQ-003 — cliente apto
    Dado una solicitud en «Evaluar solicitud»
    Cuando Riesgo registra «Apto»
    Entonces el Analista de crédito tiene asignada «Analizar crédito»

  Escenario: REQ-004 — Riesgo pide corregir
    Dado una solicitud en «Evaluar solicitud» con un dato de ingresos mal capturado
    Cuando Riesgo registra «Corregir»
    Entonces la solicitud vuelve a «Crear solicitud» de la Persona de Negocio

  Escenario: REQ-005 — Riesgo rechaza
    Dado una solicitud en «Evaluar solicitud» de un cliente con buró negativo
    Cuando Riesgo registra «Rechazar»
    Entonces la solicitud queda «Rechazada por Riesgo» y no se crea otra actividad

  Escenario: REQ-006 — el Analista rechaza
    Dado una solicitud en «Analizar crédito»
    Cuando el Analista registra «Rechazar»
    Entonces la solicitud queda «Rechazada» y no se crea otra actividad

  Escenario: REQ-007 — aprobación e información al cliente
    Dado una solicitud en «Analizar crédito»
    Cuando el Analista registra «Aprobar con condiciones»
    Entonces el Analista tiene asignada «Informar decisión al cliente»

  Escenario: REQ-008 — el cliente no acepta
    Dado una solicitud en «Informar decisión al cliente»
    Cuando el Analista registra que el cliente no acepta el monto menor
    Entonces la solicitud queda «Cerrada por no aceptación del cliente»

  Escenario: REQ-009 — el cliente acepta las condiciones
    Dado una aprobación con condiciones informada al cliente
    Cuando el Analista registra que el cliente acepta
    Entonces la Persona de Negocio tiene asignada «Modificar datos del crédito»
    Y al completarla, el Analista vuelve a tener asignada «Analizar crédito»

  Escenario: REQ-010 — el cliente acepta sin condiciones
    Dado una aprobación sin condiciones informada al cliente
    Cuando el Analista registra que el cliente acepta
    Entonces Legal tiene asignada «Recopilar expediente»

  Escenario: REQ-011 — documentos obligatorios
    Dado un expediente con documento de identidad, comprobante de ingresos y estado de cuenta, pero sin pagaré
    Cuando Legal intenta registrar «Documentación completa»
    Entonces el sistema no lo permite porque falta el pagaré

  Escenario: REQ-012 — cierre automático a los 10 días
    Dado una solicitud en «Recopilar expediente» sin el comprobante de ingresos
    Cuando pasan 10 días sin completar el expediente
    Entonces la solicitud queda «Cerrada por expediente incompleto» automáticamente

  Escenario: REQ-013 / REQ-014 — expediente completo o incompleto
    Dado una solicitud en «Recopilar expediente»
    Cuando Legal registra «Documentación incompleta»
    Entonces «Recopilar expediente» sigue abierta
    Cuando Legal registra «Documentación completa»
    Entonces Legal tiene asignada «Escanear documentación»

  Escenario: REQ-015 — envío a Despacho
    Dado un expediente escaneado
    Cuando Legal termina «Escanear documentación»
    Entonces el Analista tiene asignada «Verificar y autorizar expediente»

  Escenario: REQ-016 / REQ-017 — verificación del expediente
    Dado un expediente en «Verificar y autorizar expediente» cuyo ingreso no cuadra con el estado de cuenta
    Cuando el Analista registra «No cuadra»
    Entonces la solicitud vuelve a «Recopilar expediente» de Legal
    Cuando, en otro caso, el Analista registra «Documentación OK»
    Entonces Desembolso tiene asignada «Desembolsar crédito»

  Escenario: REQ-018 — desembolso
    Dado una solicitud en «Desembolsar crédito»
    Cuando Desembolso registra el desembolso
    Entonces la solicitud queda «Crédito desembolsado»
```
