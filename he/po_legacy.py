#!/usr/bin/env python3
"""Classify au3/locale/he.po entries against the pristine 4.0.1 catalogue.

Outputs he/po_legacy.json with every active entry that has not yet been aligned
with the new Qt translation memory, plus stats on stdout.
"""
import json
import os
import subprocess
import sys
import tarfile

import polib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
NEW = os.path.join(ROOT, 'src', 'audacity-4.0.1', 'au3', 'locale', 'he.po')
PRISTINE = os.path.join(HERE, 'pristine', 'he.po')
TARBALL = os.path.join(ROOT, 'audacity-sources-4.0.1.tar.xz')
MEMBER = 'audacity-4.0.1/au3/locale/he.po'
OUT = os.path.join(HERE, 'po_legacy.json')


def ensure_pristine():
    if os.path.exists(PRISTINE):
        return
    os.makedirs(os.path.dirname(PRISTINE), exist_ok=True)
    with tarfile.open(TARBALL) as tf:
        data = tf.extractfile(MEMBER).read()
    open(PRISTINE, 'wb').write(data)


def key(e):
    return (e.msgstr, tuple(sorted(e.msgstr_plural.items())))


def main():
    ensure_pristine()
    new = polib.pofile(NEW)
    old = polib.pofile(PRISTINE)
    before = {e.msgid: e for e in old}
    act = [e for e in new if not e.obsolete]

    updated, legacy, untranslated = [], [], []
    for e in act:
        cur = key(e)
        prev = before.get(e.msgid)
        if not (e.msgstr.strip() or e.msgstr_plural):
            untranslated.append(e)
            continue
        if prev is not None and key(prev) != cur:
            updated.append(e)
        elif prev is not None:
            legacy.append(e)
        else:
            legacy.append(e)

    print(f'active={len(act)} updated_vs_pristine={len(updated)} '
          f'still_old_wording={len(legacy)} untranslated={len(untranslated)}')

    json.dump(
        [
            {
                'msgid': e.msgid,
                'msgid_plural': e.msgid_plural,
                'msgstr': e.msgstr,
                'msgstr_plural': e.msgstr_plural or None,
                'refs': e.occurrences[:1],
            }
            for e in legacy
        ],
        open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1,
    )
    print('wrote', OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
