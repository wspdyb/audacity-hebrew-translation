#!/usr/bin/env python3
"""Validate and write Hebrew translations for the legacy .po work items.

Batch file format (UTF-8, one item per line):
    P0123<TAB>תרגום עם \\n     (\\n is a literal escape for a newline)
Plural items take three forms separated by |||  (one / two / many).
Lines starting with '#' and blank lines are ignored.
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

# printf / gettext placeholders, including positional and length modifiers
PH = re.compile(r'%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?(?:hh|h|ll|l|L|z|j|t)?[diouxXeEfgGaAcspn%]')
HEB = re.compile(r'[\u0590-\u05FF]')


def main(paths):
    work = {r['id']: r for r in json.load(open(WORK, encoding='utf-8'))}
    po = polib.pofile(PO)
    by_id = {r['id']: index(po)[r['msgid']] for r in work.values()}

    done, problems = {}, []

    for path in paths:
        for lineno, line in enumerate(open(path, encoding='utf-8'), 1):
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if '\t' not in line:
                problems.append(f'{path}:{lineno}: missing TAB')
                continue
            pid, he = line.split('\t', 1)
            pid = pid.strip()
            rec = work.get(pid)
            if rec is None:
                problems.append(f'{path}:{lineno}: unknown id {pid}')
                continue
            he = he.replace('\\n', '\n').replace('\\t', '\t')
            if rec['msgid_plural']:
                forms = he.split('|||')
                if len(forms) != 3:
                    problems.append(f'{pid}: plural needs 3 forms, got {len(forms)}')
                    continue
                if any(not f.strip() for f in forms):
                    problems.append(f'{pid}: empty plural form')
                    continue
                # one / two / many: the "two" form legitimately omits the number
                problems += [f'{pid}: {m}' for m in check(rec['msgid'], forms[0], subset=True)]
                for f in forms[1:]:
                    problems += [f'{pid}: {m}' for m in check(rec['msgid_plural'], f, subset=True)]
                if not PH.findall(forms[-1]) and PH.findall(rec['msgid_plural']):
                    problems.append(f'{pid}: the many-form must keep the placeholder {PH.findall(rec["msgid_plural"])}')
                done[pid] = forms
            else:
                if not he.strip():
                    problems.append(f'{pid}: empty translation')
                    continue
                problems += [f'{pid}: {m}' for m in check(rec['msgid'], he)]
                done[pid] = he

    for pid, val in sorted(done.items()):
        e = by_id[pid]
        if isinstance(val, list):
            e.msgstr_plural = {i: v for i, v in enumerate(val)}
            e.msgstr = ''
        else:
            e.msgstr = val
        if 'fuzzy' in e.flags:
            e.flags.remove('fuzzy')

    if problems:
        print('\n'.join(problems[:60]))
        print(f'{len(problems)} problems — catalogue NOT written')
        return 1

    po.save(PO)
    left = [p for p in work if p not in done]
    print(f'wrote {len(done)} entries; {len(left)} work items still pending')
    if left:
        open(os.path.join(HERE, 'po_pending.txt'), 'w', encoding='utf-8').write(
            '\n'.join(f'{p}|{work[p]["msgid"]!r}' for p in left) + '\n')
    return 0


def index(po):
    return {e.msgid: e for e in po if not e.obsolete}


def letters(s):
    return re.sub(r'[^A-Za-z]', '', s).lower()


def check(src, he, subset=False):
    errs = []
    if subset:
        if set(PH.findall(he)) - set(PH.findall(src)):
            errs.append(f'unknown placeholders in translation: {sorted(set(PH.findall(he)) - set(PH.findall(src)))}')
    elif sorted(PH.findall(src)) != sorted(PH.findall(he)):
        errs.append(f'placeholders differ: src={PH.findall(src)} he={PH.findall(he)}')
    if src.count('\n') != he.count('\n'):
        errs.append(f'newline count {src.count(chr(10))} -> {he.count(chr(10))}')
    lead_s, trail_s = re.match(r'^\s*', src).group(0), re.search(r'\s*$', src).group(0)
    lead_h, trail_h = re.match(r'^\s*', he).group(0), re.search(r'\s*$', he).group(0)
    if (lead_s, trail_s) != (lead_h, trail_h):
        errs.append(f'edge whitespace changed: {lead_s!r}{trail_s!r} -> {lead_h!r}{trail_h!r}')
    if '...' in he:
        errs.append('three dots — use …')
    if (not HEB.search(he) and HEB.search(src) is None
            and re.search(r'[A-Za-z]{3}', src)
            and he.strip() != src.strip() and letters(he) != letters(src)):
        errs.append('no Hebrew in translation')
    if '"' in he:
        errs.append('straight double quote')
    return errs


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
