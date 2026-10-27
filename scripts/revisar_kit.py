from pathlib import Path
from lxml import etree
r=Path(__file__).resolve().parents[1]
a=list((r/'.claude/skills').glob('*/SKILL.md'))
b=list((r/'.opencode/commands').glob('*.md'))
assert len(a)==8,len(a)
assert len(b)==8,len(b)
for p in a:
 t=p.read_text(encoding='utf8');assert t.startswith('---\n') and 'description:' in t and f'name: {p.parent.name}' in t
for p in (r/'bpmn').glob('*.bpmn'):
 doc=etree.parse(str(p))
 ids={e.get('id') for e in doc.getroot().iter() if e.get('id')}
 flows=doc.xpath('//*[local-name()="sequenceFlow"]')
 for f in flows:assert f.get('sourceRef') in ids and f.get('targetRef') in ids
 assert doc.xpath('//*[local-name()="BPMNPlane"]')
for f in ['AGENTS.md','CLAUDE.md','README.md','.env.example','especificaciones/01-requerimientos-EARS.md','docs/02-sesiones-60-min.md']:
 assert (r/f).exists(),f
print('OK: 8 skills, 8 comandos, modelos BPMN con DI y artefactos esenciales')
