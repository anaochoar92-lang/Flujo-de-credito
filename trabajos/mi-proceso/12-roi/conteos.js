// Resume 09-datos/*.csv en conteos mensuales por escenario para el Excel del ROI.
// Uso: node trabajos/mi-proceso/12-roi/conteos.js  → 12-roi/conteos_mensuales.csv
'use strict';
const fs = require('fs');
const path = require('path');
const DATOS = path.join(__dirname, '..', '09-datos');
const leer = (f) => { const l = fs.readFileSync(path.join(DATOS, f), 'utf8').trim().split('\n'); const h = l[0].split(',');
  return l.slice(1).map((x) => Object.fromEntries(x.split(',').map((v, i) => [h[i], v]))); };
const ACTS = ['ACT_006', 'ACT_007', 'ACT_008', 'TB_ACT_VERIF', 'TB_ACT_PEDIR', 'TB_ACT_RECOP_ORIG', 'TB_ACT_ESCANEAR', 'TB_ACT_RECOGER'];
const casos = leer('casos.csv'), acts = leer('actividades.csv');
const filas = [];
for (const mes of [...new Set(casos.map((c) => c.mes))].sort()) for (const esc of ['AS-IS', 'TO-BE']) {
  const c = casos.filter((x) => x.mes === mes && x.escenario === esc);
  const a = acts.filter((x) => x.mes === mes && x.escenario === esc);
  const f = { mes, temporada: c[0].temporada, escenario: esc };
  for (const id of ACTS) f[id] = a.filter((x) => x.actividad_id === id).length;
  f.entraron_expediente = c.filter((x) => x.entro_a_expediente === '1').length;
  f.cerradas_vencimiento = c.filter((x) => x.cerrada_vencimiento === '1').length;
  f.sobres_enviados = c.filter((x) => x.sobre_enviado === '1').length;
  filas.push(f);
}
const h = Object.keys(filas[0]);
fs.writeFileSync(path.join(__dirname, 'conteos_mensuales.csv'), [h.join(','), ...filas.map((f) => h.map((k) => f[k]).join(','))].join('\n') + '\n');
console.log(h.join(',')); filas.slice(0, 4).forEach((f) => console.log(h.map((k) => f[k]).join(',')));
