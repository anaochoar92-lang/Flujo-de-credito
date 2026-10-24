#!/usr/bin/env node
// Construye BPMN 2.0 + BPMN DI desde una especificación JSON declarativa.
// Port en Node.js de scripts/crear_bpmn.py para equipos sin Python (mismo contrato: docs/contrato-json.md).
// Sólo módulos estándar. No intenta desplegar procesos ni afirmar validez ejecutable.
// Uso: node scripts/crear_bpmn.js especificacion.json salida.bpmn
'use strict';
const fs = require('fs');
const path = require('path');

const VALID_TYPES = new Set(['startEvent', 'endEvent', 'task', 'userTask', 'serviceTask', 'manualTask', 'sendTask', 'receiveTask',
  'businessRuleTask', 'scriptTask', 'exclusiveGateway', 'inclusiveGateway', 'parallelGateway',
  'eventBasedGateway', 'intermediateCatchEvent', 'intermediateThrowEvent', 'boundaryEvent']);
const EVENT_DEF = { message: 'messageEventDefinition', timer: 'timerEventDefinition', signal: 'signalEventDefinition',
  error: 'errorEventDefinition', escalation: 'escalationEventDefinition',
  terminate: 'terminateEventDefinition', conditional: 'conditionalEventDefinition' };
const GATEWAYS = new Set(['exclusiveGateway', 'inclusiveGateway', 'parallelGateway', 'eventBasedGateway']);
const ID_PATTERN = /^[A-Za-z_][A-Za-z0-9_.-]*$/;
// Espaciado: carriles de 240 px y nodos apilados cada 110 px (las tareas miden 78 px de alto)
const LEFT = 140, SPACING = 200, LANE_H = 240, RANK_STEP = 110;

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const attrs = (o) => Object.entries(o).map(([k, v]) => ` ${k}="${esc(v)}"`).join('');

function validateSpec(spec) {
  const errors = [], warnings = [], allIds = new Set(), nodeOwners = {};
  const addId = (val, ctx) => {
    if (typeof val !== 'string' || !ID_PATTERN.test(val)) { errors.push(`ID inválido en ${ctx}: ${JSON.stringify(val)}`); return; }
    if (allIds.has(val)) errors.push(`ID repetido: ${val}`);
    allIds.add(val);
  };
  if (!(spec.processes || []).length) errors.push('Se requiere processes con al menos un proceso');
  for (const proc of spec.processes || []) {
    const pid = proc.id; addId(pid, 'proceso');
    const nodes = proc.nodes || [], flows = proc.flows || [];
    if (!nodes.length) errors.push(`${pid}: no contiene nodos`);
    const localIds = new Set(nodes.map((n) => n.id));
    for (const n of nodes) {
      addId(n.id, 'nodo');
      if (n.id in nodeOwners) errors.push(`Nodo repetido: ${n.id}`);
      nodeOwners[n.id] = pid;
      if (!VALID_TYPES.has(n.type)) errors.push(`${n.id}: tipo BPMN no soportado ${n.type}`);
      const ev = n.event;
      if (ev) {
        if (!(ev.kind in EVENT_DEF)) errors.push(`${n.id}: tipo evento no soportado`);
        if (['message', 'signal', 'error', 'escalation'].includes(ev.kind) && !ev.ref) errors.push(`${n.id}: evento necesita ref (declaración externa)`);
      }
      if (n.type === 'boundaryEvent' && !localIds.has(n.attachedTo)) errors.push(`${n.id}: boundaryEvent necesita attachedTo dentro de su proceso`);
      if (n.type === 'boundaryEvent' && !ev) errors.push(`${n.id}: boundaryEvent necesita event`);
    }
    for (const l of proc.lanes || []) {
      addId(l.id, 'lane');
      for (const nid of l.nodeIds || []) if (!localIds.has(nid)) errors.push(`${pid}: lane menciona nodo inexistente ${nid}`);
    }
    for (const f of flows) {
      addId(f.id, 'flujo');
      if (!localIds.has(f.source) || !localIds.has(f.target)) errors.push(`${pid}: flujo ${f.id} requiere ambos nodos en su proceso`);
      if (f.source === f.target) warnings.push(`${pid}: flujo reflexivo ${f.id}`);
    }
    const flowIds = new Set(flows.map((f) => f.id));
    for (const n of nodes) {
      if (n.default && !flowIds.has(n.default)) errors.push(`${n.id}: default referencia flujo inexistente`);
      if (n.type === 'eventBasedGateway') {
        for (const f of flows.filter((x) => x.source === n.id)) {
          const tgt = nodes.find((x) => x.id === f.target);
          if (tgt && !['intermediateCatchEvent', 'receiveTask'].includes(tgt.type)) errors.push(`${n.id}: flujo de gateway basado en eventos no llega a catch/receive`);
        }
      }
    }
    if (!nodes.some((n) => n.type === 'startEvent')) warnings.push(`${pid}: no tiene startEvent`);
    if (!nodes.some((n) => n.type === 'endEvent')) warnings.push(`${pid}: no tiene endEvent`);
  }
  const procIds = new Set((spec.processes || []).map((p) => p.id));
  for (const e of spec.participants || []) {
    addId(e.id, 'participante');
    if (!procIds.has(e.processRef)) errors.push(`Participante ${e.id} refiere proceso inexistente`);
  }
  for (const f of spec.messageFlows || []) {
    addId(f.id, 'messageFlow');
    const a = nodeOwners[f.source], b = nodeOwners[f.target];
    if (!a || !b) errors.push(`${f.id}: messageFlow apunta a nodo inexistente`);
    else if (a === b) errors.push(`${f.id}: messageFlow entre nodos del mismo pool/proceso`);
  }
  const kinds = ['messages', 'signals', 'errors', 'escalations'];
  const declared = new Set(kinds.flatMap((k) => (spec[k] || []).map((x) => x.id)));
  for (const k of kinds) for (const d of spec[k] || []) addId(d.id, k);
  for (const p of spec.processes || []) for (const n of p.nodes || []) {
    const ev = n.event || {};
    if (['message', 'signal', 'error', 'escalation'].includes(ev.kind) && !declared.has(ev.ref)) errors.push(`${n.id}: falta declaración de ${ev.ref}`);
  }
  return { errors, warnings };
}

function inferColumns(nodes, flows) {
  const adj = {};
  for (const f of flows) (adj[f.source] = adj[f.source] || []).push(f.target);
  let starts = nodes.filter((n) => n.type === 'startEvent').map((n) => n.id);
  if (!starts.length && nodes.length) starts = [nodes[0].id];
  const dist = Object.fromEntries(nodes.map((n) => [n.id, 0]));
  const seen = new Set(starts), queue = [...starts];
  while (queue.length) {
    const u = queue.shift();
    for (const v of adj[u] || []) if (!seen.has(v)) { dist[v] = dist[u] + 1; seen.add(v); queue.push(v); }
  }
  let nmax = Math.max(0, ...Object.values(dist));
  for (const n of nodes) if (!seen.has(n.id)) { nmax += 1; dist[n.id] = nmax; }
  return dist;
}

function computeBoxes(proc, ybase) {
  const nodes = proc.nodes, flows = proc.flows || [];
  const lanes = (proc.lanes && proc.lanes.length) ? proc.lanes : [{ id: '_internal', name: 'Proceso', nodeIds: nodes.map((n) => n.id) }];
  const laneFor = {};
  lanes.forEach((l, i) => (l.nodeIds || []).forEach((nid) => { laneFor[nid] = i; }));
  const depths = inferColumns(nodes, flows);
  const occupied = {}, boxes = {};
  const top = ybase + 10;
  for (const n of nodes) {
    if (n.type === 'boundaryEvent') continue;
    const col = n.column ?? depths[n.id], lane = laneFor[n.id] ?? 0, key = `${lane},${col}`;
    const rank = occupied[key] || 0; occupied[key] = rank + 1;
    const [w, h] = GATEWAYS.has(n.type) ? [50, 50] : (n.type.endsWith('Event') ? [36, 36] : [148, 78]);
    const x = LEFT + Number(col) * SPACING;
    const cy = top + lane * LANE_H + 80 + rank * RANK_STEP;
    boxes[n.id] = [x, Math.round(cy - h / 2), w, h];
  }
  for (const n of nodes) {
    if (n.type !== 'boundaryEvent') continue;
    const host = boxes[n.attachedTo];
    if (host) { const [x, y, w, h] = host; boxes[n.id] = [x + w - 20, y + h - 18, 36, 36]; }
  }
  const maxX = Math.max(600, ...Object.values(boxes).map((b) => b[0] + b[2]));
  const width = Math.max(760, maxX - LEFT + 260);
  const height = Math.max(lanes.length * LANE_H + 40, 240);
  return { boxes, lanes, pool: [70, ybase, width, height] };
}

function edgePoints(a, b, routeIndex = 0) {
  const [sx, sy, sw, sh] = a, [tx, ty, tw, th] = b;
  const cy = sy + sh / 2, tmid = ty + th / 2;
  if (tx > sx + sw + 12) { const mx = (sx + sw + tx) / 2; return [[sx + sw, cy], [mx, cy], [mx, tmid], [tx, tmid]]; }
  if (tx === sx && ty > sy + sh) { const c = sx + sw / 2; return [[c, sy + sh], [c, ty]]; }
  const detour = Math.max(sy + sh, ty + th) + 65 + routeIndex * 22;
  return [[sx + sw / 2, sy + sh], [sx + sw / 2, detour], [tx + tw / 2, detour], [tx + tw / 2, ty + th]];
}

function build(spec) {
  const { errors, warnings } = validateSpec(spec);
  if (errors.length) throw new Error(errors.join('\n'));
  const out = [];
  const L = (s, d = 1) => out.push('  '.repeat(d) + s);
  out.push("<?xml version='1.0' encoding='utf-8'?>");
  out.push(`<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"${attrs({ id: spec.id || 'Definitions_Laboratorio', targetNamespace: 'https://laboratorio.example.org/bpmn', exporter: 'Taller OpenCode BPMN (Node.js)', exporterVersion: '1.0' })}>`);
  for (const [plural, tag] of [['messages', 'message'], ['signals', 'signal'], ['errors', 'error'], ['escalations', 'escalation']])
    for (const d of spec[plural] || []) L(`<bpmn:${tag}${attrs({ id: d.id, name: d.name || d.id })} />`);
  const processes = spec.processes;
  const participants = (spec.participants && spec.participants.length) ? spec.participants
    : processes.map((p) => ({ id: 'Participant_' + p.id, name: p.name || p.id, processRef: p.id }));
  L(`<bpmn:collaboration${attrs({ id: 'Collaboration_Lab', name: spec.name || 'Proceso' })}>`);
  for (const part of participants) L(`<bpmn:participant${attrs({ id: part.id, name: part.name, processRef: part.processRef })} />`, 2);
  for (const f of spec.messageFlows || []) L(`<bpmn:messageFlow${attrs({ id: f.id, name: f.name || '', sourceRef: f.source, targetRef: f.target })} />`, 2);
  L('</bpmn:collaboration>');
  const boxesAll = {}, bounds = {}, laneInfo = {};
  let ybase = 90;
  for (const p of processes) {
    const { boxes, lanes, pool } = computeBoxes(p, ybase);
    bounds[p.id] = pool; Object.assign(boxesAll, boxes); laneInfo[p.id] = lanes;
    L(`<bpmn:process${attrs({ id: p.id, name: p.name || p.id, isExecutable: String(Boolean(p.isExecutable)) })}>`);
    if (p.lanes && p.lanes.length) {
      L(`<bpmn:laneSet${attrs({ id: 'LaneSet_' + p.id })}>`, 2);
      for (const lane of lanes) {
        L(`<bpmn:lane${attrs({ id: lane.id, name: lane.name || lane.id })}>`, 3);
        for (const nid of lane.nodeIds || []) L(`<bpmn:flowNodeRef>${esc(nid)}</bpmn:flowNodeRef>`, 4);
        L('</bpmn:lane>', 3);
      }
      L('</bpmn:laneSet>', 2);
    }
    const fin = {}, fout = {};
    for (const f of p.flows || []) { (fout[f.source] = fout[f.source] || []).push(f.id); (fin[f.target] = fin[f.target] || []).push(f.id); }
    for (const n of p.nodes) {
      const a = { id: n.id, name: n.name || n.id };
      if (n.default) a.default = n.default;
      if (n.type === 'boundaryEvent') { a.attachedToRef = n.attachedTo; if (n.cancelActivity === false) a.cancelActivity = 'false'; }
      const inner = [];
      for (const fid of fin[n.id] || []) inner.push(`<bpmn:incoming>${esc(fid)}</bpmn:incoming>`);
      for (const fid of fout[n.id] || []) inner.push(`<bpmn:outgoing>${esc(fid)}</bpmn:outgoing>`);
      const ev = n.event;
      if (ev) {
        const tag = EVENT_DEF[ev.kind], ea = {};
        if (ev.ref && !['timer', 'conditional'].includes(ev.kind)) ea[ev.kind + 'Ref'] = ev.ref;
        const parts = [];
        for (const t of ['timeDate', 'timeDuration', 'timeCycle'])
          if (ev[t] != null) parts.push(`<bpmn:${t} xsi:type="bpmn:tFormalExpression">${esc(ev[t])}</bpmn:${t}>`);
        if (ev.kind === 'conditional' && ev.condition) parts.push(`<bpmn:condition xsi:type="bpmn:tFormalExpression">${esc(ev.condition)}</bpmn:condition>`);
        inner.push(parts.length ? `<bpmn:${tag}${attrs(ea)}>${parts.join('')}</bpmn:${tag}>` : `<bpmn:${tag}${attrs(ea)} />`);
      }
      if (inner.length) { L(`<bpmn:${n.type}${attrs(a)}>`, 2); inner.forEach((s) => L(s, 3)); L(`</bpmn:${n.type}>`, 2); }
      else L(`<bpmn:${n.type}${attrs(a)} />`, 2);
    }
    for (const f of p.flows || []) {
      const a = { id: f.id, sourceRef: f.source, targetRef: f.target };
      if (f.name) a.name = f.name;
      if (f.condition) {
        L(`<bpmn:sequenceFlow${attrs(a)}>`, 2);
        L(`<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression">${esc(f.condition)}</bpmn:conditionExpression>`, 3);
        L('</bpmn:sequenceFlow>', 2);
      } else L(`<bpmn:sequenceFlow${attrs(a)} />`, 2);
    }
    L('</bpmn:process>');
    ybase += pool[3] + 80;
  }
  L('<bpmndi:BPMNDiagram id="BPMNDiagram_Lab">');
  L('<bpmndi:BPMNPlane id="BPMNPlane_Lab" bpmnElement="Collaboration_Lab">', 2);
  const shape = (id, el, [x, y, w, h], extra = {}) => {
    L(`<bpmndi:BPMNShape${attrs({ id: id + '_di', bpmnElement: el, ...extra })}>`, 3);
    L(`<dc:Bounds${attrs({ x, y, width: w, height: h })} />`, 4);
    L('</bpmndi:BPMNShape>', 3);
  };
  for (const part of participants) shape(part.id, part.id, bounds[part.processRef], { isHorizontal: 'true' });
  for (const p of processes) {
    const [x, y, w, h] = bounds[p.id], lanes = laneInfo[p.id];
    if (p.lanes && p.lanes.length) lanes.forEach((lane, i) => shape(lane.id, lane.id,
      [x + 30, y + i * LANE_H, w - 30, i < lanes.length - 1 ? LANE_H : h - i * LANE_H], { isHorizontal: 'true' }));
    for (const n of p.nodes) if (boxesAll[n.id]) shape(n.id, n.id, boxesAll[n.id]);
  }
  let idx = 0;
  const edge = (f, ri) => {
    L(`<bpmndi:BPMNEdge${attrs({ id: f.id + '_di', bpmnElement: f.id })}>`, 3);
    for (const [x, y] of edgePoints(boxesAll[f.source], boxesAll[f.target], ri)) L(`<di:waypoint${attrs({ x: Math.round(x), y: Math.round(y) })} />`, 4);
    L('</bpmndi:BPMNEdge>', 3);
  };
  for (const p of processes) for (const f of p.flows || []) {
    if (!boxesAll[f.source] || !boxesAll[f.target]) continue;
    edge(f, idx % 3); idx += 1;
  }
  for (const f of spec.messageFlows || []) if (boxesAll[f.source] && boxesAll[f.target]) edge(f, 0);
  L('</bpmndi:BPMNPlane>', 2);
  L('</bpmndi:BPMNDiagram>');
  out.push('</bpmn:definitions>');
  return { xml: out.join('\n') + '\n', warnings };
}

function main() {
  const [jsonPath, outPath] = process.argv.slice(2);
  if (!jsonPath || !outPath) { console.error('Uso: node scripts/crear_bpmn.js especificacion.json salida.bpmn'); process.exit(1); }
  const spec = JSON.parse(fs.readFileSync(jsonPath, 'utf8').replace(/^﻿/, ''));
  let res;
  try { res = build(spec); } catch (e) { console.error('ERRORES EN JSON:\n' + e.message); process.exit(2); }
  if (fs.existsSync(outPath)) { console.error('Ya existe (no se sobrescribe): ' + outPath); process.exit(3); }
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, res.xml, 'utf8');
  console.log('Creado:', outPath);
  for (const w of res.warnings) console.log('ADVERTENCIA:', w);
}
if (require.main === module) main();
module.exports = { build, validateSpec };
