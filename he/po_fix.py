#!/usr/bin/env python3
"""Final touch-ups on au3/locale/he.po: drop bidi marks and restore the source's
line wrapping for entries whose translation lost its line breaks."""
import os
import re

import polib

HERE = os.path.dirname(os.path.abspath(__file__))
PO = os.path.join(HERE, '..', 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.po')
BIDI = dict.fromkeys(map(ord, '\u200e\u200f\u202a\u202b\u202c'))


def rewrap(src, he):
    """Redistribute the translation over the same number of lines as the source."""
    parts = src.split('\n')
    if he.count('\n') == len(parts) - 1:
        return he
    words = he.split()  # any whitespace, so stray \n from earlier passes go away
    if len(words) < len(parts):
        return he
    # target share of characters for each line
    total = sum(len(p) for p in parts) or 1
    out, idx = [], 0
    for i, p in enumerate(parts):
        if i == len(parts) - 1:
            out.append(' '.join(words[idx:]))
            break
        take = max(1, round(len(words) * len(p) / total))
        take = min(take, len(words) - idx - (len(parts) - i - 1))
        out.append(' '.join(words[idx:idx + take]))
        idx += take
    return '\n'.join(out)


def main():
    po = polib.pofile(PO)
    marks = rewrapped = 0
    for e in po:
        if e.msgstr and any(ch in e.msgstr for ch in '\u200e\u200f\u202a\u202b\u202c'):
            e.msgstr = e.msgstr.translate(BIDI)
            marks += 1
        if e.msgstr_plural:
            for k, v in list(e.msgstr_plural.items()):
                if any(ch in v for ch in '\u200e\u200f\u202a\u202b\u202c'):
                    e.msgstr_plural[k] = v.translate(BIDI)
                    marks += 1
        if not e.msgid_plural and e.msgstr and e.msgstr.count('\n') != e.msgid.count('\n'):
            new = rewrap(e.msgid, e.msgstr)
            if new != e.msgstr:
                e.msgstr = new
                rewrapped += 1
    po.save(PO)
    print(f'removed bidi marks in {marks} entries, restored wrapping in {rewrapped}')


if __name__ == '__main__':
    main()
