#!/usr/bin/env python3
"""Validate and store Hebrew translations produced for the Audacity .ts catalogue.

Batch file format (UTF-8):
    U0012<TAB>תרגום
    U0035<TAB>form_one|||form_two|||form_three     # plural (3 numerus forms)
Lines starting with '#' and blank lines are ignored.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TM = os.path.join(HERE, 'tm.json')

PH = re.compile(r'%(?:L?\d+|L?[nsdif]|\.\d+[fdi])')
LISP = re.compile(r'~[a%&|~]')
TAG = re.compile(r'</?[A-Za-z][^>]*>')


def load():
    if os.path.exists(TM):
        return json.load(open(TM, encoding='utf-8'))
    return {}


def check(u, src, he, plural, errors, subset=False):
    def bad(msg):
        errors.append(f'U{u:04d}: {msg} | src={src!r} | he={he!r}')

    if he != he.strip() and src == src.strip():
        bad('leading/trailing whitespace')
    if '  ' not in src and any('  ' in ln.strip(' ') for ln in he.split('\n')):
        bad('double space')
    if '...' in he:
        bad('three dots — use …')
    he_nt = TAG.sub('', he)
    if '"' in he_nt:
        bad('straight double quote')
    if re.search(r"(?<![א-ת])'|'(?![א-ת])", he_nt):
        bad('straight single quote')
    if '\t' in he:
        bad('tab inside translation')

    # placeholders must match exactly (multiset)
    sp, hp = sorted(PH.findall(src)), sorted(PH.findall(he))
    if subset:
        if set(hp) - set(sp):
            bad(f'unknown placeholders in translation: {sorted(set(hp) - set(sp))}')
    elif sp != hp:
        bad(f'placeholders differ: src={sp} he={hp}')

    sl, hl = sorted(LISP.findall(src)), sorted(LISP.findall(he))
    if sl != hl:
        bad(f'Nyquist/Lisp format directives differ: src={sl} he={hl}')

    # newlines
    if src.count('\n') and he.count('\n') == 0:
        bad('source is multi-line but translation is single-line')

    # rich-text tags
    st, ht = sorted(TAG.findall(src)), sorted(TAG.findall(he))
    if re.fullmatch(r'<[a-z]+>', src):
        st = []
    if st != ht:
        bad(f'rich-text tags differ: src={st} he={ht}')

    # mnemonic marker
    if '&' in src.replace('&&', '') and '&' not in he:
        bad('source has mnemonic (&) but translation has none')


def main(paths):
    q = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
    by_u = {r['u']: r for r in q}
    tm = load()
    added = errors = 0
    for path in paths:
        for lineno, line in enumerate(open(path, encoding='utf-8'), 1):
            line = line.rstrip('\n')
            if not line.strip() or line.lstrip().startswith('#'):
                continue
            if '\t' not in line:
                errors += 1
                print(f'{path}:{lineno}: missing TAB separator: {line[:60]!r}')
                continue
            uid, he = line.split('\t', 1)
            he = he.replace('\\n', '\n')  # \n escape for multi-line strings
            m = re.fullmatch(r'U(\d+)', uid.strip())
            if not m:
                errors += 1
                print(f'{path}:{lineno}: bad id {uid!r}')
                continue
            u = int(m.group(1))
            rec = by_u.get(u)
            if rec is None:
                errors += 1
                print(f'{path}:{lineno}: unknown id U{u:04d}')
                continue
            if rec['plural']:
                forms = he.split('|||')
                if len(forms) != 3:
                    errors += 1
                    print(f'{path}:{lineno}: plural U{u:04d} needs 3 forms, got {len(forms)}')
                    continue
                allph = set()
                for f in forms:
                    allph |= set(PH.findall(f))
                if allph != set(PH.findall(rec['src'])):
                    errors += 1
                    print(f"U{u:04d}: plural placeholders differ: src={sorted(set(PH.findall(rec['src'])))} he={sorted(allph)}")
                    continue
                for f in forms:
                    if not f.strip():
                        errors += 1
                        print(f'{path}:{lineno}: empty plural form for U{u:04d}')
                        break
                else:
                    for f in forms:
                        check(u, rec['src'], f, True, errors_list := [], subset=True)
                        for e in errors_list:
                            errors += 1
                            print(e)
                    tm[str(u)] = forms
                    added += 1
                continue
            if not he.strip():
                errors += 1
                print(f'{path}:{lineno}: empty translation for U{u:04d}')
                continue
            errs = []
            check(u, rec['src'], he, False, errs)
            if errs:
                errors += len(errs)
                for e in errs:
                    print(e)
                continue
            tm[str(u)] = he
            added += 1
    json.dump(tm, open(TM, 'w', encoding='utf-8'), ensure_ascii=False, indent=0, sort_keys=True)
    print(f'applied {added} entries, {errors} problems, TM size {len(tm)} / {len(q)}')


if __name__ == '__main__':
    main(sys.argv[1:])
