#!/usr/bin/env python3
"""Refresh the legacy gettext catalogue (au3/locale/he.po) from the new Qt translation memory."""
import json, os, sys
import polib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', 'src', 'audacity-4.0.1')
PO = os.path.join(ROOT, 'au3', 'locale', 'he.po')

tm = json.load(open(os.path.join(HERE, 'tm.json'), encoding='utf-8'))
by_src = {}
for u, val in tm.items():
    by_src.setdefault(None, None)
queue = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
for rec in queue:
    val = tm.get(str(rec['u']))
    if val is not None:
        by_src[rec['src']] = val

po = polib.pofile(PO)
changed = same = 0
for e in po:
    if e.obsolete:
        continue
    val = by_src.get(e.msgid)
    if val is None:
        continue
    if e.msgid_plural:
        forms = val if isinstance(val, list) else [val]
        n = max(3, len(forms))
        # Hebrew: 3 PO plural forms (one / two / many)
        mapping = {0: forms[0], 1: forms[1] if len(forms) > 1 else forms[0]}
        for i in range(n):
            mapping.setdefault(i, forms[-1])
        if e.msgstr_plural != mapping:
            e.msgstr_plural = mapping
            changed += 1
    else:
        val = val if isinstance(val, str) else val[0]
        if e.msgstr != val:
            e.msgstr = val
            changed += 1
    if 'fuzzy' in e.flags:
        e.flags.remove('fuzzy')
    same += 1

po.metadata['Language'] = 'he'
po.metadata['Plural-Forms'] = 'nplurals=3; plural=(n == 1 && n % 1 == 0) ? 0 : (n == 2 && n % 1 == 0) ? 1: 2;'
po.save(PO)
print(f'matched {same} of {len([e for e in po if not e.obsolete])} entries, updated {changed}')
print('po total', len(po), 'translated', len(po.translated_entries()), 'untranslated', len(po.untranslated_entries()))
