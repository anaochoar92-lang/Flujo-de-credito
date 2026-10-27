# Contexto de negocio · Caso demostrativo

**Organización:** Secretaría Distrital de Planeación de Bogotá, interacción con Curaduría, titular y sistemas SIPA, BOG DATA, MOOC/SIIC según el BPMN de referencia.

**Problema de negocio (hipótesis pedagógica, no afirmación institucional):** la liquidación urbanística contiene verificaciones manuales, transferencias de datos y revisiones que podrían beneficiarse de prevalidaciones y trazabilidad. El BPMN base también contempla expedición y reexpedición de recibos; el MVP de dos horas **no** cubre esos ciclos completos.

**Valor buscado:** registrar una solicitud, mostrar validaciones, iniciar una instancia BPMN, permitir completar tareas humanas y conservar eventos para construir KPI de ciclo.

**Proceso fuente:** `SOP_Liquidacion_SDP_referencia.md` (interpretación previa) y `BPMN_REFERENCIA_COMPLEJO_ASIS.xml`. Para el taller se usan dos modelos BPMN **simplificados**, expresamente didácticos, en `bpmn/`. NO se ejecuta el BPMN completo de 6 participantes.

**Actores demo:** solicitante/Curaduría, profesional SDP, superior SDP. Sin autenticación ni permisos reales: los nombres son roles de simulación.

**Alcance confirmado:** un formulario, prevalidación simple, cálculo sintético no jurídico, inicio de instancia, tareas humanas, persistencia de auditoría, indicadores y exportación de CSV.

**Fuera de alcance:** validación de licencias reales, reglas normativas de liquidación, firma digital, facturación, cobro efectivo, SIPA/BOG DATA reales, RBAC productivo, conciliación asíncrona completa y gestión de incidentes Camunda.

**Riesgo:** nunca presentar el cálculo de `valor_referencia_demo` como liquidación oficial. No usar CHIP, radicados ni datos personales verdaderos en cuentas gratuitas compartidas.
