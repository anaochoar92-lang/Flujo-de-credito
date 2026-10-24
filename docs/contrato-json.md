# Contrato de JSON intermedio para el generador de clase

**No es un estándar BPMN:** es un formato didáctico para que OpenCode produzca un diagrama con una estructura repetible y que un script convierta a XML + BPMN DI.

## Archivo
Ejemplo funcional: `ejemplos/modelos/reexpedicion.json`.

### Campos principales
- `id`, `name`: identificación y nombre general.
- `processes`: lista de objetos `{id,name,isExecutable,lanes,nodes,flows}`; `isExecutable=false` por defecto.
- `participants`: lista `{id,name,processRef}`. Si falta, se genera un pool por proceso.
- `messageFlows`: `{id,name,source,target}` entre nodos de procesos **diferentes**.
- `messages`, `signals`, `errors`, `escalations`: declaraciones `{id,name}`.

### Proceso
- `lanes`: opcional, lista `{id,name,nodeIds}`. Cada ID de nodo puede asignarse a una lane. Si falta, se modela sin lanes.
- `nodes`: lista de nodos `{id,type,name,column?,event?,attachedTo?,cancelActivity?,default?}`.
- `flows`: `{id,source,target,name?,condition?}`. Una condición formal depende del motor y por defecto se omite.
- `column`: entero desde 0; posición aproximada para diagramación izquierda→derecha. Si falta se calcula por recorrido inicial.

### Tipos de nodo admitidos
`startEvent`, `endEvent`, `task`, `userTask`, `serviceTask`, `manualTask`, `sendTask`, `receiveTask`, `businessRuleTask`, `scriptTask`, `exclusiveGateway`, `inclusiveGateway`, `parallelGateway`, `eventBasedGateway`, `intermediateCatchEvent`, `intermediateThrowEvent`, `boundaryEvent`.

### Eventos
`event` es `{kind,ref?,timeDate?,timeDuration?,timeCycle?,condition?}`.
- `kind`: `message`, `timer`, `signal`, `error`, `escalation`, `terminate`, `conditional`.
- `ref`: ID declarado para mensajes/señales/errores/escalaciones.
- Para timer se puede usar ISO 8601 `timeDuration` (ej. `P1D`, **sólo un ejemplo**). El plazo real debe provenir de fuente validada; no inventar uno.
- `attachedTo` requerido para `boundaryEvent` y `cancelActivity` controla si interrumpe la tarea (por defecto sí).
- Los campos se escriben en XML BPMN; **esto no garantiza compatibilidad del evento con cada posición ni con Zeebe**. Debe revisarlo el modelador.

### IDs y trazabilidad
Usar IDs estables y únicos en todo el XML, empezando por letra; referencia EARS en documentos vecinos. XML BPMN no contiene la matriz EARS por defecto para no contaminar el estándar con extensiones ad hoc.

### Generación
```
py scripts/crear_bpmn.py trabajos/mi-proceso/04-modelo/especificacion.json trabajos/mi-proceso/05-bpmn/proceso-v01.bpmn
py scripts/validar_bpmn.py trabajos/mi-proceso/05-bpmn/proceso-v01.bpmn
```

### Limitaciones importantes
El algoritmo de diagramación es automático **aproximado**. Camunda Modeler debe usarse para ajustar tamaños, curvas, cruces y presentación final. Los diagramas grandes o cíclicos necesitarán retoques. Si se modifica el XML en Camunda, no se debe regenerar encima del archivo editado desde el JSON antiguo: se perderían posiciones y mejoras manuales.
