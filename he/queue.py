#!/usr/bin/env python3
"""Build a de-duplicated queue of source strings, and print slices for translation."""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
items = json.load(open(os.path.join(HERE, 'ts_items.json'), encoding='utf-8'))

def build():
    q, seen = [], {}
    for it in items:
        s = it['src']
        if s in seen:
            seen[s]['idx'].append(it['idx'])
            seen[s]['ctxs'].add(it['ctx'])
            if it['extra'] and not seen[s]['extra']:
                seen[s]['extra'] = it['extra']
            continue
        rec = {'u': len(q), 'src': s, 'ctx': it['ctx'], 'ctxs': {it['ctx']},
               'extra': it['extra'], 'comment': it['comment'],
               'plural': it['plural'], 'idx': [it['idx']]}
        seen[s] = rec
        q.append(rec)
    for r in q:
        r['ctxs'] = sorted(r['ctxs'])
    json.dump(q, open(os.path.join(HERE, 'queue.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    return q

def show(a, b, q):
    for r in q[a:b]:
        extra = f"  ⟪{r['extra']}⟫" if r['extra'] and 'Action' in (r['extra'] or '') else ''
        src = r['src'].replace('\n', '⏎')
        flag = ' [PLURAL]' if r['plural'] else ''
        print(f"U{r['u']:04d} [{r['ctx']}]{flag} {src}{extra}")

if __name__ == '__main__':
    q = build()
    if len(sys.argv) == 1:
        print('unique', len(q))
    else:
        show(int(sys.argv[1]), int(sys.argv[2]), q)
