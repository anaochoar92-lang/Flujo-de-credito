---
name: verificar-tablero
description: "Validar trazabilidad de KPI, consistencia de CSV, Excel y dashboards con ejemplos de errores"
compatibility: opencode
metadata:
  audience: "mba"
  language: "es"
---

## Criterios
1. Ejecutar `py scripts/taller_kpi.py validar --input datos/demo/casos.csv` y revisar salida.
2. Conciliar `datos/preset/preset_resumen_mensual.csv` frente al Excel: mismo escenario, mismos meses, volumen, unidades, promedio ponderado según volumen y costos en COP.
3. Detectar y corregir: sumar tasas, contar filas de actividades como casos, tiempo ciclo confundido con trabajo humano, inversión omitida y mezcla de datos reales/sintéticos.
4. Verificar 2 widgets y 1 dashboard como mínimo, revisar títulos, filtros, medidas y explicaciones; nunca asegurar éxito cloud sin captura o confirmación del estudiante.
5. Pedir al participante el contraejemplo: «¿Qué haría que este ROI fuera falso?» y registrar la respuesta.
6. Generar `13-retroalimentacion/auditoria.md` con: validado, faltante, acción correctiva, evidencia, propietario.

## Salida
Un reporte comprensible para directivo; limitaciones, sensibilidad e hipótesis pendientes.
