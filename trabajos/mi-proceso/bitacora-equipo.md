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

---

## 2026-10-27 — Ana (con Claude)

### Qué se hizo
| # | Qué | Archivos |
|---|---|---|
| 1 | Ana respondió PEND-01 a PEND-04: **todas quedan como la propuesta** (ronda 21) | `02-analisis/entrevista.md` |

### Estado de los pendientes
| ID | Estado |
|---|---|
| PEND-01 | Cerrado: ruta en papel en el MVP y el módulo B; el módulo A sigue el v03 |
| PEND-02 | Cerrado: sin tarea aparte |
| PEND-03 | Cerrado: 20 días exactos es válido; hora America/Santo_Domingo |
| PEND-04 | Cerrado: aprobada la app con los dos módulos |
| TEC-06 | Sin efecto: no hay que crear BPMN del MVP v02, prompt de Lovable v03 ni TO-BE v04 por estas respuestas (el nombre de la colaboración del v03 se corrige en la próxima versión que se haga) |
| TEC-01 a TEC-05 | Siguen abiertos (David / Sergio) |

**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio).

---

## 2026-10-28 — Ana (con Claude)

### Qué se hizo
| # | Qué | Archivos |
|---|---|---|
| 1 | **Paso 23 / TEC-05 hecho.** API del MVP en `/api/credito` (tablas `cred_casos`, `cred_documentos`, `cred_eventos` y vista `vw_preset_mvp_casos`) y pantalla en `/credito`. No se tocaron los endpoints del kit | `app/credito.py`, `app/static/credito.html`, `app/main.py` (+7 líneas) |
| 2 | Pruebas copiadas a `tests/` y `pytest.ini` con `testpaths = tests` (la copia de `pruebas-propuestas` queda como registro y ya no se ejecuta dos veces). **42 en verde** | `tests/test_credito.py`, `pytest.ini` |
| 3 | `requirements.txt`: se agregan `PyYAML` (faltaba para `test_preset_bundle.py`) y `tzdata` (zona `America/Santo_Domingo` en Windows, PEND-03) | `requirements.txt` |
| 4 | `.gitignore`: `.venv/`, `__pycache__/`, `.pytest_cache/`, `mvp.sqlite3` | `.gitignore` |
| 5 | Presentación ejecutiva del proceso | `Automatización PPT.pptx` |

### Cómo probarlo
```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m uvicorn app.main:app --reload   # abrir http://localhost:8000/credito
```

### Estado de los pendientes
| ID | Estado |
|---|---|
| TEC-05 | **Cerrado** (falta solo tomar las 4 capturas del paso 23: caso creado, tarea activa, tarea completada, CSV) |
| TEC-01 a TEC-04 | Siguen abiertos (David / Sergio): necesitan Camunda Modeler, credenciales del clúster o Lovable/Supabase |
| Siguiente | Paso 25 (CSV del MVP a Preset), paso 26 (auditoría) e INC-1 del backlog |

**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio). Los datos del MVP no se mezclan con `09-datos/`.

---

## 2026-10-29 — Sergio (con Claude)

### Qué se hizo
| # | Qué | Archivos |
|---|---|---|
| 1 | `scripts/prueba_manual_credito.py` corrido contra el clúster SaaS del equipo: crea caso, carga documentos y aparece la tarea de Despacho; **falla al completar Despacho (502)** porque el cliente API de Sergio no tiene permisos de lectura (403 en `process-instances`, búsquedas de tareas vacías) | — |
| 2 | Bug corregido: el trabajador automático de Camunda bloqueaba el servidor (~10 s por cada `jobs/activation`); ahora corre en un hilo aparte | `app/credito.py` (commit `49d4766`) |
| 3 | **INC-4: buzón de correos simulado** en `/buzon` (cliente, Legal, Despacho). Ver `14-mvp/backlog-autonomo.md` | `app/credito.py`, `app/static/buzon.html`, `app/static/credito.html`, `app/main.py`, `tests/test_credito.py` |

### Pendientes nuevos
| ID | Pregunta | Qué afecta | Propuesta mientras tanto |
|---|---|---|---|
| PEND-05 | ¿Están bien los correos del buzón simulado (cuáles se mandan y su texto)? Hoy: al cliente enlace, rechazo, corrección, verificado y atención presencial; a Legal y Despacho aviso de tarea nueva | INC-4; textos en `app/credito.py` | Quedan como están |
| TEC-07 | Dar al cliente API de Sergio permisos de lectura de instancias y de lectura/actualización de tareas de usuario en `Process_Credito_MVP` (Identity → Authorizations), o compartir el cliente que usa Ana. Cancelar en Operate las instancias de prueba `4503599627375176` y `6755399441060640` | Prueba end-to-end con Camunda real | Owner del clúster |

**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio). Los correos son SINTÉTICOS y no salen de la app.

---

## 2026-10-30 — Sergio (con Claude)

### Qué se hizo
| # | Qué | Archivos |
|---|---|---|
| 1 | **Prueba end-to-end contra el clúster real superada**: SOL-94181 (dudoso → Legal → corrección → Despacho) y SOL-94406 (válido → Despacho) terminaron `COMPLETED` en `END_VERIFICADO`, igual que en la app | — |
| 2 | Para lograrlo, el Owner dio al cliente API: tenant `<default>`, `Message: CREATE`, en *Process Definition* lectura de definición/instancias y `READ_USER_TASK`/`UPDATE_USER_TASK`, y `CANCEL_PROCESS_INSTANCE`. Además se desplegaron los formularios `revision-legal` y `verificacion-expediente`: el BPMN desplegado los referencia y sin ellos la tarea no se crea (incidente `FORM_NOT_FOUND`) | Clúster |
| 3 | **Sincronización estricta**: la carga de documentos usa `messages/correlation` (falla si la instancia no espera el mensaje) y se verifica que llegó a la instancia del caso; si Camunda no confirma, no se guarda nada local. Reintentos breves y un trabajador automático por tipo de trabajo en paralelo | `app/credito.py`, `app/camunda.py`, `tests/test_credito.py` |
| 4 | Carga de documentos con botón "Buscar archivo…" (selector del sistema operativo; solo se muestra el nombre, el archivo no se envía) y CSV "todos los casos en Camunda" (`/api/credito/export/camunda.csv`, cruza instancias del clúster con los casos locales) | `app/static/credito.html`, `app/credito.py` |
| 5 | Limpieza: se cancelaron 2 instancias iniciadas desde la consola (sin `solicitudId`, la app no puede seguirlas) y se borraron de la base local los casos que no coincidían con Camunda | — |

### Pendientes
| ID | Estado |
|---|---|
| TEC-07 | **Cerrado** (permisos y formularios listos) |
| Nota | Las solicitudes de prueba se crean siempre desde el portal; las iniciadas desde la consola de Camunda quedan sin `solicitudId` |

**Efecto en los números:** ninguno (ROI 16,7 %, 10,1 meses; KPI sin cambio).
