#!/usr/bin/env python3
"""Quality checks on the finished legacy gettext catalogue au3/locale/he.po."""
import os
import re
import sys

import polib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
PO = os.path.join(ROOT, 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.po')
HEB = re.compile(r'[\u0590-\u05FF]')

# printf placeholders; the trailing lookahead keeps "% of" and "%Length" from
# being read as conversion specifiers
PH = re.compile(r'%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?(?:hh|h|ll|l|L|z|j|t)?'
                r'[diouxXeEfgGaAcspn%](?![a-z])')


def main():
    po = polib.pofile(PO)
    act = [e for e in po if not e.obsolete]
    problems = {'empty': [], 'placeholder': [], 'newline': [], 'no_hebrew': []}

    for e in act:
        if e.msgid_plural:
            forms = e.msgstr_plural or {}
            if not forms or any(not v.strip() for v in forms.values()):
                problems['empty'].append(e.msgid)
                continue
            allowed = set(PH.findall(e.msgid)) | set(PH.findall(e.msgid_plural))
            for k, v in forms.items():
                if set(PH.findall(v)) - allowed:
                    problems['placeholder'].append((e.msgid, k, v))
            if not PH.findall(forms.get(max(forms), '')) and PH.findall(e.msgid_plural):
                problems['placeholder'].append((e.msgid, 'many', forms.get(max(forms), '')))
            if any(v.count('\n') not in (0, e.msgid_plural.count('\n')) for v in forms.values()):
                problems['newline'].append((e.msgid, forms))
            continue
        if not e.msgstr.strip():
            problems['empty'].append(e.msgid)
            continue
        if sorted(PH.findall(e.msgid)) != sorted(PH.findall(e.msgstr)):
            problems['placeholder'].append((e.msgid, e.msgstr))
        if e.msgid.count('\n') != e.msgstr.count('\n'):
            problems['newline'].append((e.msgid, e.msgstr))

    lines = [f'active entries: {len(act)}',
             f'translated: {len(po.translated_entries())}',
             f'untranslated: {len(po.untranslated_entries())}',
             f'fuzzy: {len(po.fuzzy_entries())}']
    for key, rows in problems.items():
        lines.append(f'{key}: {len(rows)}')
        for r in rows[:20]:
            lines.append(f'   {r!r}')
    text = '\n'.join(lines) + '\n'
    print(text)
    open(os.path.join(HERE, 'po_qa_report.txt'), 'w', encoding='utf-8').write(text)

    # compile to .mo as the final syntax check
    mo = os.path.join(ROOT, 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.mo')
    po.save_as_mofile(mo)
    print('wrote', mo, os.path.getsize(mo), 'bytes')
    return 1 if sum(len(v) for v in problems.values()) else 0


if __name__ == '__main__':
    sys.exit(main())
