#!/usr/bin/env node
// Inspección estructural preliminar de BPMN 2.0 (no reemplaza XSD, Camunda lint ni validación humana).
// Port en Node.js de scripts/validar_bpmn.py para equipos sin Python: mismas comprobaciones y mismo JSON de salida.
// Lectura del XML con expresiones regulares: pensada para BPMN generados por el kit o guardados por Camunda Modeler.
// Uso: node scripts/validar_bpmn.js archivo.bpmn [--json salida.json]
'use strict';
const fs = require('fs');
const path = require('path');

const FLOW_NODES = new Set(['task', 'userTask', 'serviceTask', 'manualTask', 'receiveTask', 'sendTask', 'scriptTask', 'businessRuleTask',
  'startEvent', 'endEvent', 'intermediateCatchEvent', 'intermediateThrowEvent', 'boundaryEvent',
  'exclusiveGateway', 'inclusiveGateway', 'parallelGateway', 'eventBasedGateway', 'subProcess', 'callActivity']);
const attr = (s, name) => { const m = new RegExp(`\\s${name}="([^"]*)"`).exec(s); return m ? m[1] : undefined; };

// Elementos hijos directos de primer nivel dentro de un bloque: devuelve {tag, attrs, body}
function children(block) {
  const res = [], re = /<(?:[\w-]+:)?([\w]+)(\s[^>]*?)?(\/?)>/g;
  let m;
  while ((m = re.exec(block))) {
    const tag = m[1], at = m[2] || '';
    if (m[3] === '/') { res.push({ tag, attrs: at, body: '' }); continue; }
    const close = new RegExp(`</(?:[\\w-]+:)?${tag}>`, 'g');
    close.lastIndex = re.lastIndex;
    const c = close.exec(block);
    if (!c) { res.push({ tag, attrs: at, body: '' }); continue; }
    res.push({ tag, attrs: at, body: block.slice(re.lastIndex, c.index) });
    re.lastIndex = close.lastIndex;
  }
  return res;
}

function validate(file) {
  const errors = [], warnings = [], stats = {};
  let xml;
  try { xml = fs.readFileSync(file, 'utf8'); } catch (e) { return { archivo: file, errores: [`No se puede leer: ${e.message}`], advertencias: [], estadisticas: {} }; }
  if (!/<(?:[\w-]+:)?definitions[\s>]/.test(xml)) errors.push('Raíz debe ser bpmn:definitions');
  const ids = {};
  for (const m of xml.matchAll(/<[\w:-]+[^>]*?\sid="([^"]+)"/g)) { if (ids[m[1]]) errors.push(`ID duplicado: ${m[1]}`); ids[m[1]] = true; }
  const owners = {}, processes = [], nodesByProc = {}, flowsByProc = {};
  for (const pm of xml.matchAll(/<(?:[\w-]+:)?process(\s[^>]*)>([\s\S]*?)<\/(?:[\w-]+:)?process>/g)) {
    const pid = attr(pm[1], 'id') || '?'; processes.push(pid);
    const kids = children(pm[2]);
    const nodes = {}, flows = {};
    for (const k of kids) {
      const id = attr(k.attrs, 'id');
      if (FLOW_NODES.has(k.tag)) nodes[id] = k;
      if (k.tag === 'sequenceFlow') flows[id] = k;
    }
    nodesByProc[pid] = nodes; flowsByProc[pid] = flows;
    Object.keys(nodes).forEach((n) => { owners[n] = pid; });
    const out = {}, inc = {};
    for (const [fid, f] of Object.entries(flows)) {
      const a = attr(f.attrs, 'sourceRef'), b = attr(f.attrs, 'targetRef');
      if (!nodes[a] || !nodes[b]) { errors.push(`${pid}: ${fid} enlaza nodos inexistentes o en otro proceso (${a} → ${b})`); continue; }
      (out[a] = out[a] || []).push(b); (inc[b] = inc[b] || []).push(a);
      if (nodes[a].tag === 'endEvent') errors.push(`${pid}: endEvent ${a} tiene salida ${fid}`);
      if (nodes[b].tag === 'startEvent') errors.push(`${pid}: startEvent ${b} tiene entrada ${fid}`);
    }
    const starts = Object.keys(nodes).filter((n) => nodes[n].tag === 'startEvent');
    const ends = Object.keys(nodes).filter((n) => nodes[n].tag === 'endEvent');
    if (!starts.length) warnings.push(`${pid}: sin evento de inicio (puede ser un subproceso incompleto)`);
    if (!ends.length) warnings.push(`${pid}: sin evento de fin`);
    const reach = new Set(starts), todo = [...starts];
    while (todo.length) for (const v of out[todo.shift()] || []) if (!reach.has(v)) { reach.add(v); todo.push(v); }
    for (const [nid, n] of Object.entries(nodes)) {
      const typ = n.tag, name = attr(n.attrs, 'name') || typ;
      if (typ === 'boundaryEvent') {
        if (!nodes[attr(n.attrs, 'attachedToRef')]) errors.push(`${pid}: evento límite ${nid} adjunto a nodo inexistente`);
        continue;
      }
      if (starts.length && !reach.has(nid)) warnings.push(`${pid}: nodo no alcanzable desde el inicio: ${nid} (${name})`);
      if (typ === 'endEvent') continue;
      if (!(out[nid] || []).length) warnings.push(`${pid}: nodo sin continuación: ${nid} (${name})`);
      if ((typ === 'exclusiveGateway' || typ === 'inclusiveGateway') && (out[nid] || []).length > 1) {
        const fo = Object.values(flows).filter((f) => attr(f.attrs, 'sourceRef') === nid);
        if (!attr(n.attrs, 'default') && !fo.some((f) => /conditionExpression/.test(f.body)))
          warnings.push(`${pid}: gateway de decisión ${nid} sin flujo por defecto ni condiciones formales (apto solo para revisión conceptual)`);
      }
      if (typ === 'eventBasedGateway')
        for (const t of out[nid] || []) if (!['intermediateCatchEvent', 'receiveTask'].includes(nodes[t].tag)) errors.push(`${pid}: evento basado en gateway ${nid} apunta a tipo incorrecto ${t}`);
      if (['intermediateCatchEvent', 'intermediateThrowEvent'].includes(typ) && !/EventDefinition/.test(n.body))
        warnings.push(`${pid}: ${nid} sin definición explícita de evento`);
    }
    for (const lm of pm[2].matchAll(/<(?:[\w-]+:)?lane(\s[^>]*)>([\s\S]*?)<\/(?:[\w-]+:)?lane>/g))
      for (const r of lm[2].matchAll(/<(?:[\w-]+:)?flowNodeRef>([^<]+)</g))
        if (!nodes[r[1].trim()]) errors.push(`${pid}: lane ${attr(lm[1], 'id')} refiere nodo inexistente ${r[1].trim()}`);
    stats[pid] = { nodos: Object.keys(nodes).length, flujos: Object.keys(flows).length, inicios: starts.length, fines: ends.length };
  }
  const participants = [...xml.matchAll(/<(?:[\w-]+:)?participant(\s[^>]*?)\/?>/g)];
  for (const p of participants) if (!processes.includes(attr(p[1], 'processRef'))) errors.push(`Participante ${attr(p[1], 'id')} con processRef inexistente`);
  const mflows = [...xml.matchAll(/<(?:[\w-]+:)?messageFlow(\s[^>]*?)\/?>/g)];
  for (const mf of mflows) {
    const a = attr(mf[1], 'sourceRef'), b = attr(mf[1], 'targetRef');
    if (!ids[a] || !ids[b]) errors.push(`MessageFlow ${attr(mf[1], 'id')} tiene extremo inexistente`);
    else if (owners[a] && owners[a] === owners[b]) errors.push(`MessageFlow ${attr(mf[1], 'id')} conecta el mismo proceso (use sequenceFlow)`);
  }
  const shapes = [...xml.matchAll(/<(?:[\w-]+:)?BPMNShape(\s[^>]*?)>/g)].map((m) => attr(m[1], 'bpmnElement'));
  const edges = [...xml.matchAll(/<(?:[\w-]+:)?BPMNEdge(\s[^>]*?)>/g)].map((m) => attr(m[1], 'bpmnElement'));
  if (!shapes.length) warnings.push('No hay BPMN DI: Camunda Modeler puede no visualizar el proceso como diagrama');
  const sset = new Set(shapes), eset = new Set(edges);
  for (const [pid, nodes] of Object.entries(nodesByProc)) {
    for (const nid of Object.keys(nodes)) if (!sset.has(nid)) warnings.push(`${pid}: falta forma gráfica BPMN DI para ${nid}`);
    for (const fid of Object.keys(flowsByProc[pid])) if (!eset.has(fid)) warnings.push(`${pid}: falta conector gráfico BPMN DI para ${fid}`);
  }
  stats.global = { procesos: processes.length, participantes: participants.length, messageFlows: mflows.length, formasDI: shapes.length, conectoresDI: edges.length };
  return { archivo: file, errores: errors, advertencias: warnings, estadisticas: stats,
    limitaciones: ['No valida contra el XSD oficial BPMN 2.0.', 'No comprueba configuración Zeebe/Camunda para ejecución.',
      'No verifica coherencia jurídica ni semántica de las decisiones.', 'El aspecto visual debe revisarse en Camunda Modeler.',
      'Port en Node.js de validar_bpmn.py: lee el XML con expresiones regulares, no con un analizador XML completo.'] };
}

function main() {
  const args = process.argv.slice(2);
  const file = args[0], ji = args.indexOf('--json');
  if (!file) { console.error('Uso: node scripts/validar_bpmn.js archivo.bpmn [--json salida.json]'); process.exit(1); }
  const r = validate(file);
  console.log('ARCHIVO:', r.archivo); console.log('ESTADÍSTICAS:', JSON.stringify(r.estadisticas));
  r.errores.forEach((e) => console.log('ERROR:', e)); r.advertencias.forEach((w) => console.log('AVISO:', w));
  console.log(`RESULTADO: ${r.errores.length} error(es), ${r.advertencias.length} advertencia(s).`);
  if (ji > 0) { const o = args[ji + 1]; fs.mkdirSync(path.dirname(o), { recursive: true }); fs.writeFileSync(o, JSON.stringify(r, null, 2), 'utf8'); }
  process.exit(r.errores.length ? 2 : 0);
}
if (require.main === module) main();
module.exports = { validate };
