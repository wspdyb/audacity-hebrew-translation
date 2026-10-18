#!/usr/bin/env python3
"""Write Hebrew translations into share/locale/audacity_he.ts, preserving the
original lupdate formatting (only <translation> elements are rewritten)."""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', 'src', 'audacity-4.0.1')
TS = os.path.join(ROOT, 'share', 'locale', 'audacity_he.ts')

MSG = re.compile(r'<message\b[^>]*>.*?</message>', re.S)
CTX = re.compile(r'<context>.*?</context>', re.S)
TR = re.compile(r'<translation\b[^>]*?/>|<translation\b[^>]*>.*?</translation>', re.S)
SRC = re.compile(r'<source>(.*?)</source>', re.S)


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&apos;'))


def load_tr():
    q = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
    tm = json.load(open(os.path.join(HERE, 'tm.json'), encoding='utf-8'))
    over = {}
    p = os.path.join(HERE, 'tm_override.json')
    if os.path.exists(p):
        over = json.load(open(p, encoding='utf-8'))
    return q, tm, over


def render(value):
    if isinstance(value, list):
        inner = ''.join(f'<numerusform>{esc(v)}</numerusform>' for v in value)
        return f'<translation>{inner}</translation>'
    return f'<translation>{esc(value)}</translation>'


def main(write=True):
    q, tm, over = load_tr()
    by_u = {r['u']: r for r in q}
    src2u = {r['src']: r['u'] for r in q}
    text = open(TS, encoding='utf-8').read()

    stats = {'done': 0, 'missing': 0, 'obsolete': 0}
    missing_src = []

    def do_ctx(m):
        name = re.search(r'<name>(.*?)</name>', m.group(0), re.S).group(1)
        body = m.group(0)

        def do_msg(mm):
            block = mm.group(0)
            sm = SRC.search(block)
            if not sm:
                return block
            src = html.unescape(sm.group(1))
            key = f'{name}\x00{src}'
            if key in over:
                val = over[key]
            else:
                u = src2u.get(src)
                val = tm.get(str(u)) if u is not None else None
            trm = TR.search(block)
            if trm is None:
                return block
            if val is None:
                stats['missing'] += 1
                if len(missing_src) < 40:
                    missing_src.append(src)
                return block
            if 'type="obsolete"' in trm.group(0):
                stats['obsolete'] += 1
                return block
            stats['done'] += 1
            return block[:trm.start()] + render(val) + block[trm.end():]

        return MSG.sub(do_msg, body)

    out = CTX.sub(do_ctx, text)
    print(f"translated messages: {stats['done']}, still untranslated: {stats['missing']}, "
          f"obsolete skipped: {stats['obsolete']}")
    if missing_src:
        print('first missing:', missing_src[:5])
    if write:
        open(TS, 'w', encoding='utf-8').write(out)
        print('wrote', TS)


if __name__ == '__main__':
    main(write='--dry' not in sys.argv)
