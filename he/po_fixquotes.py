#!/usr/bin/env python3
"""Normalise straight quotes in translated .po batches to typographic ones."""
import re
import sys

for path in sys.argv[1:]:
    out = []
    for line in open(path, encoding='utf-8'):
        if '\t' not in line or line.lstrip().startswith('#'):
            out.append(line)
            continue
        pid, he = line.rstrip('\n').split('\t', 1)
        while re.search(r'"([^"]*)"', he):
            he = re.sub(r'"([^"]*)"', '“\\1”', he, count=1)
        he = he.replace('"', '”')
        out.append(f'{pid}\t{he}\n')
    open(path, 'w', encoding='utf-8').write(''.join(out))
    print('normalised', path)
