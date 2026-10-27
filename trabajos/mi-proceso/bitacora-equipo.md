# Bitácora del equipo — Flujo de crédito preaprobado

Registro de lo que se hizo por sesión y de los pendientes, con su responsable. Las decisiones de negocio confirmadas se siguen anotando en `02-analisis/entrevista.md` (rondas). Datos: SINTÉTICOS.

---

## 2026-10-27 — Sergio (con Claude)

### Qué se hizo
| # | Qué | Archivos |
|---|---|---|
| 1 | Actualización desde GitHub (17 commits). Los cambios locales de Sergio eran solo de dibujo (posición de flechas y etiquetas, sin cambios de contenido): se recuperó el ajuste del AS-IS v02 y la disposición local del TO-BE v02 se guardó aparte | `05-bpmn/proceso-v02.bpmn`, `08-tobe/proceso-to-be-v02-local.bpmn` |
| 2 | Prompt de Lovable **v02**: módulo A (demo AS-IS vs TO-BE **v03** sobre Camunda real) + módulo B (Portal MVP con las reglas de `14-mvp`), formulario con alias/correo/monto, ID `SOL-9NNNN` y CSV `SINTETICO` para Preset. El v01 se conserva | `14-demo/prompt-lovable-v02.md` |
| 3 | Revisión de **todos** los BPMN con las reglas de compatibilidad de Camunda 8.10 (las mismas de Modeler): AS-IS v02 y TO-BE v02/v03 con **0 errores**; no hubo que convertir ninguno. Los v01 fallan por ser descriptivos (esperado; no se tocan) | `14-mvp/proceso-mvp-v01.md` §5 |
| 4 | **BPMN del MVP (paso 24)** generado: tramo del portal del v03, ejecutable, Camunda 8.10. 0 errores en el validador del kit y en las reglas 8.10. **Todavía no se abrió en Modeler ni se desplegó** | `14-mvp/proceso-mvp-v01.bpmn`, `14-mvp/proceso-mvp-v01.md` |

Decisiones de Sergio en esta sesión: Lovable cumple los dos papeles (demo y portal MVP); se despliega el TO-BE v03; se alinea el formulario y el ID con FE-1 y DAT-1; se agrega el CSV para Preset.

### Pendientes — preguntas de negocio (responde **Ana**)
| ID | Pregunta | Qué afecta | Propuesta mientras tanto |
|---|---|---|---|
| PEND-01 | Cuando **Legal rechaza** un documento dudoso, ¿el caso pasa a la **ruta en papel** (REQ-MVP-02, supuesto de `14-mvp/alcance-equipo.md`) o se le **vuelve a pedir el documento** al cliente (TO-BE v03, `legalAcepta = false` → `TB_SND_CORREGIR`)? | TO-BE (posible v04) o REQ-MVP-02; `14-mvp/proceso-mvp-v01.bpmn`; módulos A y B del prompt de Lovable | El MVP y el módulo B siguen REQ-MVP-02 (ruta en papel); el módulo A sigue el v03. La app lo explica en la ayuda |
| PEND-02 | Cuando **Despacho pide corrección**, ¿basta con registrarlo al completar la verificación (el caso vuelve a esperar documentos) o hace falta la tarea humana aparte «Pedir documento corregido» (`TB_ACT_PEDIR`, como en el v03)? | `14-mvp/proceso-mvp-v01.bpmn` | Sin tarea aparte, como en el contrato del paso 23 (`CORREGIR` + documento) |
| PEND-03 | Para la regla de 20 días: ¿un documento con **20 días exactos** es válido? ¿Las fechas se cuentan en hora de **República Dominicana** (America/Santo_Domingo)? | REQ-MVP-01; módulo B de Lovable; `app/credito.py` | Sí y sí ([PROPUESTA TÉCNICA]) |
| PEND-04 | ¿Aprueba que la app de Lovable tenga los dos módulos (demo en Camunda + Portal MVP)? | `14-demo/prompt-lovable-v02.md` | Decidido por Sergio; falta el visto bueno de Ana |

### Pendientes — tareas técnicas (**David / Sergio**, o quien tenga las credenciales de Camunda)
| ID | Tarea | Detalle |
|---|---|---|
| TEC-01 | Abrir `14-mvp/proceso-mvp-v01.bpmn` en Camunda Modeler y revisar el panel *Problems* | Si se mueve algo, **guardar como `proceso-mvp-v02.bpmn`** (no sobrescribir) |
| TEC-02 | Paso 24: desplegar el BPMN del MVP y probar 1 instancia con 2 tareas | Pasos en `14-mvp/proceso-mvp-v01.md` §4. Si las autorizaciones se dieron por ID de proceso, agregar `Process_Credito_MVP`. No poner credenciales en el repo |
| TEC-03 | Desplegar el **TO-BE v03** en el clúster (queda como versión nueva de `Process_Credito_TOBE`) | Necesario para el módulo A de Lovable |
| TEC-04 | Pegar `14-demo/prompt-lovable-v02.md` en Lovable, cargar los *secrets* en Supabase y comprobar la lista «Verificar en Lovable» | Incluye las 10 comprobaciones del módulo B (§6.5) |
| TEC-05 | Paso 23: implementar `app/credito.py` y `credito.html` y dejar en verde las 32 + 11 pruebas | Ya estaba pendiente: `14-mvp/entrega-paso23-david-sergio.md` |
| TEC-06 | Cuando Ana responda PEND-01 y PEND-02, actualizar el BPMN del MVP (v02), el prompt de Lovable (v03) y, si aplica, crear el TO-BE v04 | En la v04, corregir también el nombre de la colaboración, que todavía dice «TO-BE PROPUESTA v02» |

**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio).
