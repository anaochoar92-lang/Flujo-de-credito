# Procedimiento Operativo Estándar (SOP)
## Gestión de solicitudes de liquidación urbanística, expedición de recibos y reexpedición por vencimiento

**Estado:** Borrador de interpretación del proceso modelado.  
**Fuente:** Archivo BPMN «Reto SDP - AsIs», con seis participantes.  
**Propósito:** Explicar el flujo de principio a fin en términos sencillos, sin sustituir las reglas jurídicas ni las instrucciones institucionales que deban validarse.

### 1. Objetivo

Describir cómo se recibe una solicitud relacionada con una licencia urbanística, cómo la Curaduría prepara y remite la información, cómo la Secretaría Distrital de Planeación (SDP) revisa y calcula las obligaciones urbanísticas, cómo se aprueba y emite el recibo y qué ocurre cuando se paga, vence o debe reexpedirse.

### 2. ¿Quiénes intervienen?

- **Titular de la licencia:** inicia la solicitud, recibe comunicaciones y puede solicitar recibos o reexpediciones.
- **Curaduría urbana:** captura y verifica información del trámite, prepara documentos y radica la solicitud de liquidación.
- **SIPA:** sistema que participa en la radicación y el intercambio de información; el diagrama no explica su nombre completo.
- **Líder SEUR:** asigna la solicitud a un profesional de la SDP.
- **Profesional SDP (liquidador):** revisa documentos y datos, realiza la liquidación, prepara los resultados y tramita su envío.
- **SDP superior:** revisa la solicitud y el valor de referencia, firma digitalmente y notifica al destinatario.
- **«Desarrollador»:** participante así denominado en el BPMN que gestiona avisos, seguimiento al pago, vencimientos, reexpediciones y desistimientos. El diagrama no precisa si representa a una persona, un área o un componente informático.
- **BOG DATA y MOOC/SIIC:** sistemas o fuentes utilizados en la emisión de recibos y en la consulta de valores de referencia, respectivamente; sus definiciones funcionales no están desarrolladas en el archivo.

### 3. Información que debe estar disponible

De acuerdo con las actividades del diagrama, se necesita la información geográfica y del inmueble, los datos de la solicitud y de la licencia, el formulario de áreas, el oficio de la Curaduría, el formato Minvivienda y los demás anexos que correspondan. Durante la revisión se utilizan números de radicado y expediente, CHIP, dirección, matrícula inmobiliaria, propietario, tratamiento urbanístico, áreas y datos de la persona responsable de la solicitud.

El BPMN no presenta una lista oficial y exhaustiva de documentos obligatorios; por tanto, esta sección describe datos utilizados, no una lista de requisitos normativos.

### 4. Desarrollo del procedimiento

#### Etapa A. Preparación y radicación por la Curaduría

**Paso A1. Iniciar la solicitud.** El titular de la licencia presenta una solicitud. A partir de ella, la Curaduría empieza a diligenciar la información geográfica del trámite.

**Paso A2. Identificar si se trata de un trámite simple.** El proceso pregunta si el trámite es simple. Si lo es, continúa directamente con la selección del tratamiento urbanístico. Si no lo es, se invoca la interfaz de SIPA y se muestra información geográfica relevante antes de continuar.

**Paso A3. Completar los datos del proyecto.** La Curaduría selecciona el tratamiento, diligencia el formulario web de áreas y valida la información ingresada. Después comprueba si corresponde a una modificación de licencia y realiza la anotación en el sistema cuando aplique.

**Paso A4. Cargar y validar los documentos.** La Curaduría incorpora los documentos que respaldan la solicitud. El modelo ofrece dos alternativas: clasificación y validación automáticas con IA, o validación manual. Si los documentos no son válidos, se vuelve al paso de carga para corregirlos y revisarlos nuevamente. Si son válidos, se continúa.

**Paso A5. Verificar la coherencia de la solicitud.** Se efectúa el cotejo de los datos y documentos. Luego se genera la solicitud y se carga el documento firmado.

**Paso A6. Radicar la solicitud de liquidación.** El modelo contempla la radicación en SIPA, tanto automática como manual, y el traspaso de la solicitud a la SDP. La elección exacta entre las dos modalidades requiere confirmación porque ambas rutas no están completamente conectadas en el archivo.

**Resultado de la etapa:** Solicitud de liquidación preparada y enviada para su atención en la SDP.

#### Etapa B. Recepción y revisión inicial en la SDP

**Paso B1. Registrar la entrada.** La SDP recibe la solicitud procedente de la Curaduría y genera o sincroniza el radicado de SIPA.

**Paso B2. Asignar a un responsable.** El líder SEUR debe asignar un profesional de la SDP. El diagrama incorpora una espera de cuatro horas asociada a esta asignación; al cumplirse, el flujo sigue a recepción y análisis. Esto no demuestra por sí solo que exista una aprobación automática o una regla institucional de tiempo máximo.

**Paso B3. Revisar la solicitud y descargar los documentos.** El profesional recibe y analiza la información, revisa la solicitud y descarga los archivos de soporte.

**Paso B4. Identificar el trámite y contrastar los documentos.** Revisa el tipo de trámite, el oficio enviado por la Curaduría y el formato Minvivienda. Después verifica que coincidan el número de radicado, la dirección y el propietario.

**Paso B5. Caracterizar el proceso y crear el expediente.** Registra la información necesaria para identificar y clasificar el caso; el flujo incluye la creación del expediente. Una anotación del diagrama advierte que se debe verificar si esa creación corresponde realmente a una función disponible en SIPA.

**Paso B6. Comprobar la radicación y el inmueble.** Valida la fecha del radicado, el número de expediente, la radicación de la Curaduría y que se haya realizado «en legal y debida forma». A continuación tipifica el bien y registra CHIP, dirección, matrícula inmobiliaria y propietario.

**Resultado de la etapa:** Solicitud revisada y datos básicos listos para calcular las obligaciones.

#### Etapa C. Determinación del valor y liquidación

**Paso C1. Consultar el valor de referencia.** Se solicita un valor de referencia en MOOC. Si el dato es válido y está habilitada esa ruta, se usa; en caso contrario, el profesional consulta la información de SIIC, correspondiente al valor de referencia o catastral, y carga una captura de pantalla como soporte.

**Paso C2. Revisar las áreas del proyecto.** Se valida el área del terreno con información SIIC y se diligencian el área total construida y el área total construida que se tomará para la liquidación de cargas urbanísticas.

**Paso C3. Aplicar controles.** Se revisan las excepciones, la suma de las áreas construidas, la norma aplicable y la relación entre la información SIIC y el año de radicación.

**Paso C4. Registrar el responsable.** Se diligencian los datos de la persona responsable de la solicitud, también en la base de datos.

**Paso C5. Calcular las obligaciones.** Se realiza la liquidación de las obligaciones urbanísticas, mediante una operación automática o un procedimiento manual, según la modalidad habilitada.

**Paso C6. Preparar y revisar el resultado.** Se unifica la información de la liquidación, se caracteriza el texto del resultado y se presenta la liquidación para revisión, de forma automática o manual.

**Paso C7. Aprobar la preliquidación.** El diagrama exige una aprobación denominada «doble confirmación». No aclara si deben intervenir dos personas distintas ni cuáles son los criterios de aprobación.

**Resultado de la etapa:** Preliquidación revisada y aprobada para emitir el recibo.

#### Etapa D. Emisión del recibo, oficio y envío para aprobación

**Paso D1. Expedir el recibo.** El procedimiento contempla utilizar BOG DATA para expedir y registrar el recibo, por una ruta automática o manual. Al finalizar, el resultado previsto es un recibo expedido y guardado.

**Paso D2. Preparar el oficio de salida.** El profesional descarga una plantilla de oficio, elabora el oficio de salida y lo somete a aprobación.

**Paso D3. Finalizar el trámite en SIPA.** Después de aprobar el oficio de salida, se registra la finalización del trámite en SIPA y se envía a un superior.

**Paso D4. Incorporar soportes.** El modelo incluye adjuntar el oficio, adjuntar el recibo de pago e identificar el expediente asociado. La expresión «recibo de pago» se conserva tal como aparece en el diagrama; debe comprobarse si se refiere al recibo emitido o a un comprobante ya pagado.

**Paso D5. Remitir el expediente.** Se avanza con el envío por una modalidad automática o manual, lo que inicia las actividades del superior en la SDP.

**Resultado de la etapa:** Recibo y oficio preparados, con soportes asociados y solicitud enviada para revisión superior.

#### Etapa E. Revisión superior y comunicación al destinatario

**Paso E1. Recibir la solicitud en la instancia superior.** Se realiza una invocación a SIPA y se revisa la solicitud recibida.

**Paso E2. Revisar el valor de referencia.** El superior comprueba el valor utilizado para el cálculo.

**Paso E3. Completar la gestión documental.** El diagrama dispone eliminar un archivo Excel, firmar digitalmente, generar un número de radicado y notificar al destinatario. Antes de adoptar la instrucción de eliminación debe precisarse qué archivo se elimina y cómo se preserva el expediente.

**Paso E4. Informar el resultado y el pago.** La comunicación al destinatario inicia otro ciclo en el que se genera el aviso con el resultado y un vínculo para realizar el pago.

**Resultado de la etapa:** Destinatario informado y recibo sujeto a seguimiento hasta su pago o vencimiento.

#### Etapa F. Seguimiento al recibo, pago y recordatorios

**Paso F1. Esperar el pago o un cambio de estado.** Después de comunicar el resultado, el procedimiento permanece a la espera de una de tres situaciones: confirmación del pago, momento de enviar un recordatorio o vencimiento del recibo.

**Paso F2. Confirmar el pago.** Cuando un proceso de integración de datos (ETL) reporta que el recibo fue pagado, se da por terminado el seguimiento del recibo con el estado «pagado».

**Paso F3. Recordar el vencimiento.** Si aún no se ha registrado el pago, se genera un aviso cuando faltan tres días para el vencimiento o en la siguiente fecha de recordatorio diario prevista por el sistema. Después se vuelve a esperar el pago o el siguiente evento.

**Paso F4. Atender el vencimiento.** Si llega la fecha de vencimiento sin que se registre el pago, se genera una comunicación que incluye un vínculo para solicitar la reexpedición del recibo.

**Resultado de la etapa:** Recibo pagado, o bien vencido y disponible para solicitar su reexpedición o registrar un desistimiento.

#### Etapa G. Reexpedición de un recibo vencido

**Paso G1. Solicitar la reexpedición.** El interesado utiliza el vínculo de la comunicación de vencimiento o, según las rutas del titular incluidas en el modelo, solicita la reexpedición de un recibo de espacio público o de redes locales.

**Paso G2. Validar la solicitud.** El componente denominado «Desarrollador» comprueba que el token o vínculo siga vigente y que la solicitud esté asociada a un recibo vencido. El BPMN no define todas las reglas adicionales de elegibilidad o seguridad.

**Paso G3. Enviar la petición a SDP.** Si la validación es satisfactoria, se realiza una solicitud automática de reexpedición a la SDP, que se comunica con el proceso de expedición y registro del recibo en BOG DATA.

**Paso G4. Esperar el nuevo recibo.** El flujo queda a la espera de recibir una comunicación que indique que se expidió nuevamente el recibo.

**Paso G5. Reiniciar el seguimiento.** Al obtener el recibo reexpedido, se genera una nueva comunicación con el resultado y vínculo de pago, y vuelve a comenzar el ciclo de confirmación de pago, recordatorios y vencimiento.

**Ruta alternativa — Desistimiento:** Tras el vencimiento, el proceso también puede recibir un desistimiento, registrarlo y concluir con el estado «desistimiento».

**Resultado de la etapa:** Recibo reexpedido y nuevo ciclo de pago, o cierre por desistimiento.

### 5. Trámites relacionados que aparecen en el diagrama

El BPMN también representa una ruta de la Curaduría para **expedir la licencia urbanística**, notificar al titular y decidir si aplica el pago por servicios públicos. Si aplica, se solicita el recibo a través de SIPA; de lo contrario, esa ruta finaliza. El titular puede recibir notificaciones, evaluar si pagó dentro de un plazo de diez días y solicitar la reexpedición de recibos de espacio público o redes locales cuando corresponda. Estas actividades están dibujadas, pero **no todas se encuentran conectadas de forma completa al flujo principal**. Por eso no se presentan aquí como una secuencia institucional única y ya verificada.

### 6. Comprobaciones mínimas al ejecutar el procedimiento

1. Que la solicitud contenga los datos de identificación y áreas necesarios para la revisión.
2. Que la información del inmueble y su propietario sea consistente entre formulario y documentos.
3. Que el radicado y expediente estén correctamente identificados.
4. Que se conserve la evidencia de la revisión documental, el valor de referencia usado, las áreas, las excepciones y el cálculo realizado.
5. Que la preliquidación y el oficio hayan pasado por las aprobaciones previstas en el modelo.
6. Que el recibo y sus comunicaciones estén asociados al expediente correspondiente.
7. Que el pago, vencimiento, reexpedición o desistimiento queden registrados con un estado identificable.

Estas comprobaciones son una **síntesis operativa de las actividades del diagrama**, no requisitos jurídicos adicionales.

### 7. Aspectos por aclarar antes de convertir el borrador en SOP oficial

- **Conexiones del flujo:** hay actividades que no están enlazadas mediante secuencias completas, especialmente en la expedición de licencia, las modalidades de radicación SIPA, la emisión BOG DATA y las notificaciones a las partes. Esto impide asegurar que todos los pasos ocurran exactamente en el orden aquí descrito.
- **Vencimientos y plazos:** el diagrama menciona diez días para el pago, un temporizador de cuatro horas para la asignación y recordatorios tres días antes de vencer; no define de modo suficiente el punto de inicio del conteo, si se trata de días hábiles o calendario, ni todas las consecuencias del incumplimiento.
- **Aprobaciones:** hace falta precisar qué significa la «doble confirmación» de la preliquidación, quién la otorga y qué sucede ante un rechazo.
- **Reglas de negocio:** el diagrama no detalla fórmulas de liquidación, causales de excepción, criterios documentales, reglas específicas de reexpedición ni validación legal de trámites.
- **Integraciones y documentos:** deben confirmarse el significado preciso de MOOC, SIIC, SIPA y BOG DATA para el personal operativo; el manejo del archivo Excel y de las copias de soporte; y si «recibo de pago» es recibo emitido o comprobante pagado.
- **Tratamiento de errores y devoluciones:** existen referencias a subsanación documental, pero no un circuito plenamente detallado para rechazos, devoluciones, solicitudes incompletas y fallas técnicas.

**Nota de uso:** Este texto puede emplearse como borrador de capacitación o base de trabajo para entrevistas con los responsables. No debe publicarse como instrucción institucional definitiva hasta verificar los puntos anteriores.
