// Genera los CSV SINTÉTICOS del flujo de crédito (AS-IS y TO-BE) y el registro de calidad.
// Uso (desde la raíz del kit): node trabajos/mi-proceso/09-datos/generar_sinteticos.js
// Todos los parámetros vienen de la entrevista y la fuente; los marcados HIPÓTESIS o SUPUESTO
// están explicados en 09-datos/diccionario.md. Semilla fija: mismo resultado en cada corrida.
'use strict';
const fs = require('fs');
const path = require('path');

const OUT = __dirname;
const ANIO = 2026;
const MESES_FERIA = [2, 11];                       // PREG-018
const SOLICITUDES = { feria: 1000, 'no feria': 600 }; // PREG-018, DAT-4
const P_EXPEDIENTE = 0.40;                         // DG-3: 400 de 1.000
const P_NO_LLEGA = [                               // SUPUESTO D-1: reparto del 60 % que no llega a expediente
  ['Rechazada por Riesgo', 1 / 3, 2],
  ['Rechazada', 1 / 3, 4],
  ['Cliente no acepta', 1 / 3, 4],
];
const DIAS_PREVIOS = 4;    // Crear 1 + Evaluar 1 + Analizar 2 (fuente, hoja «Tiempos»)
const DIAS_DESEMBOLSO = 1; // fuente
const PLAZO = 10;          // REQ-012

const AS_IS = { p_cierre: 0.10, p_devolucion: 0.20, recopilar: 5, escanear: 3, verificar: 4 }; // PREG-007, PREG-014
const TO_BE = {            // HIPÓTESIS H-1 a H-6 (priorización y propuesta TO-BE)
  p_papel_falla: 0.05, p_papel_agotado: 0.10, p_cierre_digital: 0.025, // H-2b: 5 % → 2,5 % con recordatorios, llamada y carga asistida (ronda 14)
 
  p_devolucion: 0.05, p_recogida_fallida: 0.05,
  carga: 2, verificar: 1, pedir: 2, recoger: 1, escanear: 3, recopilar_orig: 2,
};
const MOTIVOS = [['vencido', 0.5], ['ilegible', 0.3], ['no cuadra', 0.2]]; // SUPUESTO D-2

// --- utilidades -----------------------------------------------------------
function mulberry32(a) {
  return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
// Una secuencia común (fecha, destino) y una propia por solicitud y escenario: así cambiar
// una hipótesis del TO-BE no altera los datos del AS-IS.
const comun = mulberry32(20261024);
let rnd = comun;
const pick = (pares, u) => { let acc = 0; for (const [v, p] of pares) { acc += p; if (u < acc) return v; } return pares[pares.length - 1][0]; };
// Duración en días hábiles: base −1 / 0 / +1 con probabilidad 25 / 50 / 25 %, mínimo 1
const dur = (base) => { const u = rnd(); return Math.max(1, base + (u < 0.25 ? -1 : u < 0.75 ? 0 : 1)); };
const esHabil = (d) => d.getUTCDay() !== 0 && d.getUTCDay() !== 6; // sin festivos (limitación L-1)
function sumarHabiles(d, n) { const r = new Date(d); let k = 0; while (k < n) { r.setUTCDate(r.getUTCDate() + 1); if (esHabil(r)) k++; } return r; }
const iso = (d) => d.toISOString().slice(0, 10);
function csv(file, headers, rows) {
  const esc = (v) => (v === null || v === undefined ? '' : /[",\n]/.test(String(v)) ? `"${String(v).replace(/"/g, '""')}"` : String(v));
  fs.writeFileSync(path.join(OUT, file), [headers.join(','), ...rows.map((r) => headers.map((h) => esc(r[h])).join(','))].join('\n') + '\n', 'utf8');
}

// --- simulación del expediente --------------------------------------------
function expedienteAsIs(act) {
  const r = { ruta: 'papel', motivo_papel: '', llego_a_verificacion: 0, devuelta: 0, n_devoluciones: 0, motivo_devolucion: '',
    cerrada_vencimiento: 0, temporizador: '', sobre_enviado: 0, recogida_fallida: 0, dias: 0 };
  if (rnd() < AS_IS.p_cierre) {
    act('ACT_006', 'Recopilar expediente', 'Legal', 1, PLAZO);
    return Object.assign(r, { cerrada_vencimiento: 1, temporizador: 'papel', dias: PLAZO });
  }
  r.llego_a_verificacion = 1;
  for (let vuelta = 1; ; vuelta++) {
    const a = dur(AS_IS.recopilar), b = dur(AS_IS.escanear), c = dur(AS_IS.verificar);
    act('ACT_006', 'Recopilar expediente', 'Legal', vuelta, a);
    act('ACT_007', 'Escanear documentación', 'Legal', vuelta, b);
    act('ACT_008', 'Verificar y autorizar expediente (Despacho)', 'Analista de crédito', vuelta, c);
    r.dias += a + b + c;
    if (vuelta < 4 && rnd() < AS_IS.p_devolucion) {
      r.n_devoluciones++; r.devuelta = 1; if (!r.motivo_devolucion) r.motivo_devolucion = pick(MOTIVOS, rnd());
    } else break;
  }
  r.sobre_enviado = 1;
  return r;
}

function expedienteToBe(act) {
  const u = rnd();
  if (u < TO_BE.p_papel_falla + TO_BE.p_papel_agotado) {           // ruta de respaldo = AS-IS
    const motivo = u < TO_BE.p_papel_falla ? 'falla portal' : 'intentos agotados';
    const previo = motivo === 'falla portal' ? 1 : TO_BE.carga;     // días en el portal antes de pasar a papel
    act('SUB_T01', 'Recibir y validar documentos en el portal', 'Sistema / cliente', 1, previo);
    const r = expedienteAsIs(act);
    r.dias += previo; r.motivo_papel = motivo;
    return r;
  }
  const r = { ruta: 'digital', motivo_papel: '', llego_a_verificacion: 0, devuelta: 0, n_devoluciones: 0, motivo_devolucion: '',
    cerrada_vencimiento: 0, temporizador: '', sobre_enviado: 0, recogida_fallida: 0, dias: 0 };
  if (rnd() < TO_BE.p_cierre_digital) {
    act('SUB_T01', 'Recibir y validar documentos en el portal', 'Sistema / cliente', 1, PLAZO);
    return Object.assign(r, { cerrada_vencimiento: 1, temporizador: 'carga', dias: PLAZO });
  }
  const carga = dur(TO_BE.carga);
  act('SUB_T01', 'Recibir y validar documentos en el portal', 'Sistema / cliente', 1, carga);
  r.llego_a_verificacion = 1;
  // Rama A (Despacho) y rama B (recogida y escaneo) corren en paralelo: el expediente espera la más larga.
  let ramaA = dur(TO_BE.verificar);
  act('TB_ACT_VERIF', 'Verificar expediente digital (Despacho)', 'Analista de crédito', 1, ramaA);
  if (rnd() < TO_BE.p_devolucion) {
    r.devuelta = 1; r.n_devoluciones = 1; r.motivo_devolucion = pick(MOTIVOS, rnd());
    const p = dur(TO_BE.pedir), v = dur(TO_BE.verificar);
    act('TB_ACT_PEDIR', 'Pedir documento corregido al cliente', 'Analista de crédito', 1, p);
    act('TB_ACT_VERIF', 'Verificar expediente digital (Despacho)', 'Analista de crédito', 2, v);
    ramaA += p + v;
  }
  let ramaB = dur(TO_BE.recoger);
  act('TB_ACT_RECOGER', 'Recoger originales a domicilio', 'Mensajero certificado', 1, ramaB);
  if (rnd() < TO_BE.p_recogida_fallida) {
    r.recogida_fallida = 1; const x = dur(TO_BE.recopilar_orig);
    act('TB_ACT_RECOP_ORIG', 'Recopilar originales por la ruta actual', 'Legal', 1, x); ramaB += x;
  }
  const esc = dur(TO_BE.escanear);
  act('TB_ACT_ESCANEAR', 'Escanear originales y enviar sobre', 'Legal', 1, esc); ramaB += esc;
  r.dias = carga + Math.max(ramaA, ramaB);
  r.sobre_enviado = 1;
  return r;
}

// --- generación -------------------------------------------------------------
const casos = [], actividades = [];
let n = 0;
for (let m = 1; m <= 12; m++) {
  const mes = `${ANIO}-${String(m).padStart(2, '0')}`;
  const temporada = MESES_FERIA.includes(m) ? 'feria' : 'no feria';
  const diasMes = new Date(Date.UTC(ANIO, m, 0)).getUTCDate();
  for (let i = 0; i < SOLICITUDES[temporada]; i++) {
    rnd = comun;
    const idPar = `SOL-${String(++n).padStart(5, '0')}`;
    let inicio; do { inicio = new Date(Date.UTC(ANIO, m - 1, 1 + Math.floor(rnd() * diasMes))); } while (!esHabil(inicio));
    const entra = rnd() < P_EXPEDIENTE;
    const destino = entra ? null : pick(P_NO_LLEGA, rnd());
    for (const escenario of ['AS-IS', 'TO-BE']) {
      const idCaso = `${idPar}-${escenario === 'AS-IS' ? 'asis' : 'tobe'}`;
      rnd = mulberry32(20261024 + 2 * n + (escenario === 'TO-BE' ? 1 : 0));
      const base = { id_caso: idCaso, id_par: idPar, escenario, mes, temporada, fecha_inicio: iso(inicio), fuente_datos: 'SINTETICO' };
      if (!entra) {
        const dias = P_NO_LLEGA.find(([e]) => e === destino)[2];
        casos.push(Object.assign(base, { fecha_aceptacion: '', fecha_sobre_desembolso: '', fecha_fin: iso(sumarHabiles(inicio, dias)),
          estado_final: destino, entro_a_expediente: 0, ruta: '', motivo_papel: '', llego_a_verificacion: 0, devuelta: 0, n_devoluciones: 0,
          motivo_devolucion: '', cerrada_vencimiento: 0, temporizador: '', sobre_enviado: 0, recogida_fallida: 0,
          dias_habiles_expediente: '', dias_habiles_total: dias }));
        continue;
      }
      // El par AS-IS / TO-BE comparte inicio, destino y aceptación: solo cambia el expediente.
      const aceptacion = sumarHabiles(inicio, DIAS_PREVIOS);
      const act = (id, nombre, resp, vuelta, dias) => actividades.push({ id_caso: idCaso, id_par: idPar, escenario, mes, temporada,
        actividad_id: id, actividad: nombre, responsable: resp, vuelta, dias_habiles: dias, fuente_datos: 'SINTETICO' });
      const r = escenario === 'AS-IS' ? expedienteAsIs(act) : expedienteToBe(act);
      const finExp = sumarHabiles(aceptacion, r.dias);
      const total = DIAS_PREVIOS + r.dias + (r.sobre_enviado ? DIAS_DESEMBOLSO : 0);
      casos.push(Object.assign(base, {
        fecha_aceptacion: iso(aceptacion), fecha_sobre_desembolso: r.sobre_enviado ? iso(finExp) : '',
        fecha_fin: iso(r.sobre_enviado ? sumarHabiles(finExp, DIAS_DESEMBOLSO) : finExp),
        estado_final: r.sobre_enviado ? 'Desembolsada' : 'Cerrada por expediente incompleto',
        entro_a_expediente: 1, ruta: r.ruta, motivo_papel: r.motivo_papel, llego_a_verificacion: r.llego_a_verificacion,
        devuelta: r.devuelta, n_devoluciones: r.n_devoluciones, motivo_devolucion: r.motivo_devolucion,
        cerrada_vencimiento: r.cerrada_vencimiento, temporizador: r.temporizador, sobre_enviado: r.sobre_enviado,
        recogida_fallida: r.recogida_fallida, dias_habiles_expediente: r.sobre_enviado ? r.dias : '', dias_habiles_total: total,
      }));
    }
  }
}

// --- resumen mensual (tasas = SUM/SUM, nunca promedio de tasas) -------------
const resumen = [];
for (let m = 1; m <= 12; m++) for (const escenario of ['AS-IS', 'TO-BE']) {
  const mes = `${ANIO}-${String(m).padStart(2, '0')}`;
  const c = casos.filter((x) => x.mes === mes && x.escenario === escenario);
  const s = (k) => c.reduce((a, x) => a + (Number(x[k]) || 0), 0);
  const div = (a, b) => (b ? +(a / b).toFixed(4) : '');
  const sobres = s('sobre_enviado'), exp = s('entro_a_expediente'), ver = s('llego_a_verificacion');
  const digital = c.filter((x) => x.ruta === 'digital').length;
  resumen.push({ mes, temporada: c[0].temporada, escenario, solicitudes: c.length, entraron_expediente: exp, sobres_enviados: sobres,
    dias_expediente_total: s('dias_habiles_expediente'), dias_expediente_promedio: div(s('dias_habiles_expediente'), sobres),
    llegaron_verificacion: ver, devueltas: s('devuelta'), tasa_devolucion: div(s('devuelta'), ver),
    cerradas_vencimiento: s('cerrada_vencimiento'), tasa_cierre_vencimiento: div(s('cerrada_vencimiento'), exp),
    ruta_digital: escenario === 'TO-BE' ? digital : '', tasa_uso_portal: escenario === 'TO-BE' ? div(digital, exp) : '',
    recogidas_fallidas: escenario === 'TO-BE' ? s('recogida_fallida') : '', fuente_datos: 'SINTETICO' });
}

const H_CASOS = ['id_caso', 'id_par', 'escenario', 'mes', 'temporada', 'fecha_inicio', 'fecha_aceptacion', 'fecha_sobre_desembolso', 'fecha_fin',
  'estado_final', 'entro_a_expediente', 'ruta', 'motivo_papel', 'llego_a_verificacion', 'devuelta', 'n_devoluciones', 'motivo_devolucion',
  'cerrada_vencimiento', 'temporizador', 'sobre_enviado', 'recogida_fallida', 'dias_habiles_expediente', 'dias_habiles_total', 'fuente_datos'];
const H_ACT = ['id_caso', 'id_par', 'escenario', 'mes', 'temporada', 'actividad_id', 'actividad', 'responsable', 'vuelta', 'dias_habiles', 'fuente_datos'];
csv('casos.csv', H_CASOS, casos);
csv('actividades.csv', H_ACT, actividades);
csv('resumen_mensual.csv', Object.keys(resumen[0]), resumen);

// --- pruebas de calidad -------------------------------------------------------
const checks = [];
const chk = (nombre, fallos) => checks.push([nombre, fallos.length, fallos.slice(0, 3).join('; ')]);
const ids = new Set(); const dup = [];
for (const c of casos) { if (ids.has(c.id_caso)) dup.push(c.id_caso); ids.add(c.id_caso); }
chk('id_caso duplicado', dup);
chk('Campos obligatorios vacíos (id_caso, escenario, mes, fecha_inicio, fecha_fin, estado_final)',
  casos.filter((c) => ['id_caso', 'escenario', 'mes', 'fecha_inicio', 'fecha_fin', 'estado_final'].some((k) => c[k] === '')).map((c) => c.id_caso));
chk('Fechas en orden (inicio ≤ aceptación ≤ sobre ≤ fin)', casos.filter((c) => {
  const f = [c.fecha_inicio, c.fecha_aceptacion, c.fecha_sobre_desembolso, c.fecha_fin].filter(Boolean); return f.some((x, i) => i && x < f[i - 1]);
}).map((c) => c.id_caso));
chk('mes coincide con fecha_inicio', casos.filter((c) => c.fecha_inicio.slice(0, 7) !== c.mes).map((c) => c.id_caso));
chk('sobre_enviado = 1 exige fecha_sobre_desembolso y días de expediente', casos.filter((c) => c.sobre_enviado === 1 && (!c.fecha_sobre_desembolso || c.dias_habiles_expediente === '')).map((c) => c.id_caso));
chk('cerrada_vencimiento = 1 implica sobre_enviado = 0', casos.filter((c) => c.cerrada_vencimiento === 1 && c.sobre_enviado === 1).map((c) => c.id_caso));
chk('devuelta = 1 exige llego_a_verificacion = 1 y motivo', casos.filter((c) => c.devuelta === 1 && (c.llego_a_verificacion !== 1 || !c.motivo_devolucion)).map((c) => c.id_caso));
chk('ruta = papel en TO-BE exige motivo_papel', casos.filter((c) => c.escenario === 'TO-BE' && c.ruta === 'papel' && !c.motivo_papel).map((c) => c.id_caso));
chk('Cada id_par tiene exactamente un AS-IS y un TO-BE', (() => { const k = {}; for (const c of casos) k[c.id_par] = (k[c.id_par] || 0) + 1; return Object.keys(k).filter((x) => k[x] !== 2); })());
chk('Actividades sin caso', actividades.filter((a) => !ids.has(a.id_caso)).map((a) => a.id_caso));
const exp = casos.filter((c) => c.dias_habiles_expediente !== '').map((c) => c.dias_habiles_expediente);
chk('AVISO (no es error): días de expediente > 40, casos con 3 o más devoluciones', exp.filter((d) => d > 40).map(String));

const tot = (esc, k) => casos.filter((c) => c.escenario === esc).reduce((a, c) => a + (Number(c[k]) || 0), 0);
const pct = (a, b) => (100 * a / b).toFixed(1).replace('.', ',') + ' %';
const kpi = (esc) => ({
  k1: (tot(esc, 'dias_habiles_expediente') / tot(esc, 'sobre_enviado')).toFixed(2).replace('.', ','),
  k2: pct(tot(esc, 'devuelta'), tot(esc, 'llego_a_verificacion')),
  k3: pct(tot(esc, 'cerrada_vencimiento'), tot(esc, 'entro_a_expediente')),
  k4: esc === 'TO-BE' ? pct(casos.filter((c) => c.escenario === esc && c.ruta === 'digital').length, tot(esc, 'entro_a_expediente')) : 'N/D',
});
const a = kpi('AS-IS'), b = kpi('TO-BE');
const md = `# Registro de calidad — datos SINTÉTICOS (generado)

> Generado por \`09-datos/generar_sinteticos.js\` (semilla 20261024). **No editar a mano**: volver a correr el script.
> Los datos son **SINTÉTICOS**. Los KPI de abajo solo comprueban que el generador respeta los parámetros; **no son mediciones**.

## Volumen
| Archivo | Filas | Granularidad |
|---|---|---|
| \`casos.csv\` | ${casos.length} | 1 fila por solicitud y escenario |
| \`actividades.csv\` | ${actividades.length} | 1 fila por actividad del expediente, vuelta, solicitud y escenario |
| \`resumen_mensual.csv\` | ${resumen.length} | 1 fila por mes y escenario |

## Pruebas
| Prueba | Fallos | Ejemplos |
|---|---|---|
${checks.map(([n, f, e]) => `| ${n} | ${f} | ${e || '—'} |`).join('\n')}

## Control de parámetros (año completo, SUM/SUM)
| KPI | AS-IS | TO-BE | Parámetro esperado |
|---|---|---|---|
| KPI-01 Ciclo del expediente (días hábiles) | ${a.k1} | ${b.k1} | AS-IS ≈ 15 (12 ÷ 0,8); TO-BE ≈ 6–7 (hipótesis) |
| KPI-02 Tasa de devolución | ${a.k2} | ${b.k2} | AS-IS 20 %; TO-BE ≈ 5 % digital + 20 % en papel |
| KPI-03 Cierre por vencimiento | ${a.k3} | ${b.k3} | AS-IS 10 %; TO-BE ≈ 5 % digital + 10 % en papel |
| KPI-04 Uso efectivo del portal | ${a.k4} | ${b.k4} | TO-BE 85 % (hipótesis H-1) |
`;
fs.writeFileSync(path.join(OUT, 'registro_calidad.md'), md, 'utf8');
console.log(`casos ${casos.length} · actividades ${actividades.length} · resumen ${resumen.length}`);
console.log(checks.map(([n, f]) => `${!f ? 'ok   ' : n.startsWith('AVISO') ? 'aviso' : 'FALLA'} ${n}`).join('\n'));
console.log('AS-IS', a, '\nTO-BE', b);
