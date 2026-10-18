#!/usr/bin/env python3
"""Apply the Hebrew translation memory to the upstream master audacity_he.ts."""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'upstream', 'audacity_he_master.ts')
OUT = os.path.join(HERE, '..', 'upstream', 'audacity_he.ts')

MSG = re.compile(r'<message\b[^>]*>.*?</message>', re.S)
CTX = re.compile(r'<context>.*?</context>', re.S)
TR = re.compile(r'<translation\b[^>]*?/>|<translation\b[^>]*>.*?</translation>', re.S)
SRC_RE = re.compile(r'<source>(.*?)</source>', re.S)


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&apos;'))


def render(value):
    if isinstance(value, list):
        return '<translation>' + ''.join(
            f'<numerusform>{esc(v)}</numerusform>' for v in value) + '</translation>'
    return f'<translation>{esc(value)}</translation>'


def main():
    queue = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
    tm = json.load(open(os.path.join(HERE, 'tm.json'), encoding='utf-8'))
    by_src = {rec['src']: tm.get(str(rec['u'])) for rec in queue}

    text = open(SRC, encoding='utf-8').read()
    stats = {'ok': 0, 'missing': 0}

    def do_ctx(cm):
        body = cm.group(0)

        def do_msg(mm):
            block = mm.group(0)
            sm = SRC_RE.search(block)
            if not sm:
                return block
            src = html.unescape(sm.group(1))
            val = by_src.get(src)
            if val is None:
                stats['missing'] += 1
                return block
            trm = TR.search(block)
            if trm is None:
                stats['missing'] += 1
                return block
            stats['ok'] += 1
            return block[:trm.start()] + render(val) + block[trm.end():]

        return MSG.sub(do_msg, body)

    out = CTX.sub(do_ctx, text)
    open(OUT, 'w', encoding='utf-8', newline='\n').write(out)
    print(f'master catalog: translated {stats["ok"]}, missing {stats["missing"]} -> {OUT}')


if __name__ == '__main__':
    main()
