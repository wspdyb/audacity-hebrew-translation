#!/usr/bin/env python3
"""Plan the work for the legacy gettext catalogue au3/locale/he.po.

Every active entry that cannot be filled from the new Qt translation memory is
turned into a work item  P####  and dumped in numbered batches under he/po_batches/.
"""
import json
import os
import re
import sys

import polib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
PO = os.path.join(ROOT, 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.po')
WORK = os.path.join(HERE, 'po_work.json')
OUTDIR = os.path.join(HERE, 'po_batches')

BATCH = int(os.environ.get('BATCH', '300'))


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def tm_index():
    q = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
    tm = json.load(open(os.path.join(HERE, 'tm.json'), encoding='utf-8'))
    exact, soft = {}, {}
    for r in q:
        v = tm.get(str(r['u']))
        if v is None:
            continue
        exact[r['src']] = v
        soft.setdefault(norm(r['src']), v)
    return exact, soft


def wrap(value, msgid):
    """Keep the leading/trailing whitespace the .po entry expects."""
    if isinstance(value, list):
        return value
    lead = re.match(r'^\s*', msgid).group(0)
    trail = re.search(r'\s*$', msgid).group(0)
    return lead + value.strip() + trail


def esc(s):
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')


def main():
    po = polib.pofile(PO)
    exact, soft = tm_index()
    act = [e for e in po if not e.obsolete]

    work, filled = [], 0
    for e in act:
        v = exact.get(e.msgid)
        if v is None:
            v = soft.get(norm(e.msgid))
        if v is not None:
            e.msgstr = wrap(v, e.msgid)
            if 'fuzzy' in e.flags:
                e.flags.remove('fuzzy')
            filled += 1
            continue
        work.append({
            'id': None,
            'msgid': e.msgid,
            'msgid_plural': e.msgid_plural,
            'old': e.msgstr,
            'old_plural': e.msgstr_plural or None,
        })
    for i, r in enumerate(work, 1):
        r['id'] = f'P{i:04d}'

    po.save(PO)
    json.dump(work, open(WORK, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        os.remove(os.path.join(OUTDIR, f))
    n = 0
    for start in range(0, len(work), BATCH):
        n += 1
        chunk = work[start:start + BATCH]
        lines = [f'# batch {n} — items {chunk[0]["id"]}..{chunk[-1]["id"]} '
                 f'({len(chunk)} of {len(work)})']
        for r in chunk:
            src = esc(r['msgid'])
            if r['msgid_plural']:
                src += ' [PLURAL: ' + esc(r['msgid_plural']) + ']'
            lines.append(f'{r["id"]}|{src}')
        open(os.path.join(OUTDIR, f'{n:02d}.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    print(f'active={len(act)} filled_from_qt_tm={filled} work_items={len(work)} batches={n} batch_size={BATCH}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
