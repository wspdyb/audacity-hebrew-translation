#!/usr/bin/env python3
"""Strip keyboard-accelerator '&' mnemonics from the Hebrew translations.

No format/placeholder variable in this project uses '&' — verified: the only
'&' sequences that must survive are HTML entities in rich-text strings
(&nbsp; …) and a literal '&&' where the *source* displays '&'. Every other
'&' (Alt+letter mnemonics) is dropped from the Hebrew side only; sources are
never touched.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(HERE, 'pylib'))
import polib  # noqa: E402

TS_FILES = [
    os.path.join(ROOT, 'src', 'audacity-4.0.1', 'share', 'locale', 'audacity_he.ts'),
    os.path.join(ROOT, 'upstream', 'audacity_he.ts'),
]
PO_FILE = os.path.join(ROOT, 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.po')
TM_FILE = os.path.join(HERE, 'tm.json')
QUEUE_FILE = os.path.join(HERE, 'queue.json')

# HTML/XML entities that are content, not mnemonics
ENTITY = re.compile(r'&(?:nbsp|amp|lt|gt|quot|apos|hellip|mdash|ndash|copy|reg|trade|#\d+|#x[0-9a-fA-F]+);')
UNKNOWN = re.compile(r'&[A-Za-z][A-Za-z0-9]*;')
TAG = re.compile(r'<[^>]+>')


def strip_logical(s, src='', stats=None):
    """Remove mnemonic '&' from a logical string; keep entities and src's '&&'."""
    if not s or '&' not in s:
        return s
    park = []

    def keep(tok):
        park.append(tok)
        return '\x00%d\x00' % (len(park) - 1)

    out = ENTITY.sub(lambda m: keep(m.group(0)), s)
    out = re.sub(r'&&', lambda m: keep('&&'), out)
    for m in UNKNOWN.finditer(out):
        if stats is not None:
            stats.setdefault('unknown_entity', []).append((m.group(0), src[:60], s[:80]))
    dropped = out.count('&')
    out = out.replace('&', '')
    out = re.sub(r'\x00(\d+)\x00', lambda m: park[int(m.group(1))], out)
    if stats is not None and dropped:
        stats['dropped'] = stats.get('dropped', 0) + dropped
    return out


def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&apos;'))


def strip_ts(path, stats):
    text = open(path, encoding='utf-8').read()
    n_before = text.count('&amp;')

    def do(m):
        whole, attrs, inner = m.group(0), m.group(1), m.group(2)
        if not inner or '&' not in inner:
            return whole
        # split so real XML tags (<numerusform>) stay byte-identical; rich text
        # like &lt;b&gt; lives escaped in the file and must stay escaped
        parts = re.split(r'(<[^>]+>)', inner)
        out_parts = []
        for p in parts:
            if p.startswith('<'):
                out_parts.append(p)  # real XML tag
            else:
                out_parts.append(esc(strip_logical(html.unescape(p), '', stats)))
        return '<translation%s>%s</translation>' % (attrs, ''.join(out_parts))

    out = re.sub(r'<translation(\b[^>]*)>(.*?)</translation>', do, text, flags=re.S)
    if out != text:
        open(path, 'w', encoding='utf-8', newline='\n').write(out)
    print(f'{os.path.relpath(path, ROOT)}: &amp; {n_before} -> {out.count("&amp;")}')


def strip_po(stats):
    po = polib.pofile(PO_FILE)
    changed = 0
    for e in po:
        if e.obsolete:
            continue
        src = e.msgid + '\n' + (e.msgid_plural or '')
        if e.msgstr:
            new = strip_logical(e.msgstr, src, stats)
            if new != e.msgstr:
                e.msgstr = new
                changed += 1
        for k, v in list(e.msgstr_plural.items()):
            new = strip_logical(v, src, stats)
            if new != v:
                e.msgstr_plural[k] = new
                changed += 1
    po.save(PO_FILE)
    print(f'{os.path.relpath(PO_FILE, ROOT)}: {changed} msgstr cleaned, & left: '
          f'{open(PO_FILE, encoding="utf-8").read().count("&")}')


def strip_tm(stats):
    if not os.path.exists(TM_FILE):
        return
    queue = {r['u']: r['src'] for r in json.load(open(QUEUE_FILE, encoding='utf-8'))}
    tm = json.load(open(TM_FILE, encoding='utf-8'))
    changed = 0
    for key, val in tm.items():
        src = queue.get(int(key), '') if str(key).isdigit() else ''
        if isinstance(val, list):
            new = [strip_logical(v, src, stats) for v in val]
        else:
            new = strip_logical(val, src, stats)
        if new != val:
            tm[key] = new
            changed += 1
    json.dump(tm, open(TM_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'tm.json: {changed} values cleaned')


def main():
    stats = {}
    strip_tm(stats)
    for p in TS_FILES:
        strip_ts(p, stats)
    strip_po(stats)
    print('mnemonic & dropped:', stats.get('dropped', 0))
    for row in stats.get('unknown_entity', [])[:20]:
        print('  unknown &entity; kept:', row)
    if stats.get('unknown_entity'):
        print('  total unknown entities kept:', len(stats['unknown_entity']))


if __name__ == '__main__':
    main()
