#!/usr/bin/env python3
"""Extract Audacity 4 Qt translation catalog into a flat, stable item list."""
import json, os, sys
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'audacity-4.0.1')
TS = os.path.join(ROOT, 'share', 'locale', 'audacity_he.ts')

def main():
    tree = ET.parse(TS)
    root = tree.getroot()
    items = []
    idx = 0
    for ctx in root.findall('context'):
        name = ctx.find('name').text
        for m in ctx.findall('message'):
            src_el = m.find('source')
            tr_el = m.find('translation')
            plural = m.get('numerus') == 'yes'
            cur = None
            if tr_el is not None:
                forms = tr_el.findall('numerusform')
                if forms:
                    cur = [f.text or '' for f in forms]
                else:
                    cur = tr_el.text or ''
            items.append({
                'idx': idx,
                'ctx': name,
                'src': src_el.text or '',
                'comment': (m.find('comment').text if m.find('comment') is not None else None),
                'extra': (m.find('extracomment').text if m.find('extracomment') is not None else None),
                'plural': plural,
                'old': cur,
                'loc': [ (l.get('filename'), l.get('line')) for l in m.findall('location') ],
            })
            idx += 1
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ts_items.json'), 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=0)
    print('items', len(items), 'unique sources', len({i['src'] for i in items}))

if __name__ == '__main__':
    main()
