#!/usr/bin/env python3
"""Quality checks on the finished Hebrew Qt catalogue."""
import html
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', 'src', 'audacity-4.0.1')
TS = os.path.join(ROOT, 'share', 'locale', 'audacity_he.ts')

MSG = re.compile(r'<message\b[^>]*>.*?</message>', re.S)
CTX = re.compile(r'<context>.*?</context>', re.S)
HEB = re.compile(r'[\u0590-\u05FF]')
LAT = re.compile(r'[A-Za-z]{2,}')
ALLOW = {'Audacity', 'audio.com', 'Audio.com', 'MuseScore', 'MuseHub', 'Nyquist', 'FFmpeg', 'LAME',
         'WAV', 'MP3', 'FLAC', 'Ogg', 'Vorbis', 'Opus', 'AAC', 'AIFF', 'MIDI', 'VST', 'VST3', 'LV2',
         'LADSPA', 'AU', 'ASIO', 'Qt', 'API', 'UUID', 'BPM', 'Hz', 'kHz', 'dB', 'kbps', 'Kbps',
         'kbit', 'bps', 'fps', 'PCM', 'DTMF', 'SAL', 'LISP', 'Lisp', 'XML', 'HTML', 'CSV', 'WebVTT',
         'SubRip', 'SQ', 'EQ', 'RMS', 'LPC', 'PdO', 'PtO', 'MPEG', 'MPEG1', 'MPEG2', 'WMA', 'AC3',
         'AMR', 'M4A', 'WavPack', 'Musepack', 'Speex', 'RealPlayer', 'CDDA', 'NTSC', 'PAL', 'SQL',
         'SQLite', 'SQLite3', 'IOGG', 'OGG', 'blob', 'BLOB', 'Portmixer', 'RIAA', 'GSM', 'WAVEX',
         'AIFF', 'Test', 'flow', 'Soap', 'Voice', 'Cleaner', 'Mastering', 'Google', 'Facebook',
         'Finder', 'Explorer', 'X11', 'Testflow', 'Scriptables1', 'Scriptables2', 'src', 'Hz.'}

GLOSSARY = [
    (r'\btracks?\b', ['רצוע']),
    (r'\bclips?\b', ['קטע']),
    (r'\bsample rate\b', ['קצב דגימ', 'קצב הדגימ']),
    (r'\bbit depth\b', ['עומק סיביות']),
    (r'\bplayhead\b', ['ראש ה']),
    (r'\bwaveform\b', ['צורת גל']),
    (r'\bfade in\b', ['עלייה הדרגתית']),
    (r'\bfade out\b', ['דעיכה הדרגתית']),
    (r'\bpresets?\b', ['פריסט']),
    (r'\bmetadata\b', ['מטא']),
    (r'\btrim\b', ['קיצוץ']),
    (r'\bsnap(ping)?\b', ['הצמד']),
    (r'\breverb\b', ['הדהוד']),
    (r'\bundo\b', ['ביטול']),
    (r'\bredo\b', ['ביצוע מחדש']),
]


def load():
    text = open(TS, encoding='utf-8').read()
    out = []
    for cm in CTX.finditer(text):
        ctx = re.search(r'<name>(.*?)</name>', cm.group(0), re.S).group(1)
        for mm in MSG.finditer(cm.group(0)):
            b = mm.group(0)
            src = html.unescape(re.search(r'<source>(.*?)</source>', b, re.S).group(1))
            trm = re.search(r'<translation\b[^>]*>(.*?)</translation>', b, re.S)
            if trm:
                forms = [html.unescape(x) for x in re.findall(r'<numerusform>(.*?)</numerusform>', trm.group(1), re.S)]
                txt = ' '.join(forms) if forms else html.unescape(trm.group(1))
            else:
                forms, txt = [], ''
            out.append((ctx, src, txt, forms, b))
    return out


def main():
    items = load()
    problems = defaultdict(list)

    for ctx, src, txt, forms, block in items:
        if not txt:
            problems['empty'].append(src)
            continue
        if forms and len(forms) != 2:
            problems['plural_forms'].append((src, len(forms)))
        if HEB.search(src) is None and txt == src:
            # untranslated copy: only acceptable for symbols / technical tokens
            if LAT.search(src) or HEB.search(txt):
                problems['copy'].append((ctx, src))
        # leftover English words inside a Hebrew translation
        plain = re.sub(r'<[^>]*>', '', txt)
        words = [w for w in LAT.findall(plain) if w not in ALLOW and not re.search(w + r'\d', plain)]
        if HEB.search(txt) and words:
            problems['latin'].append((src, txt, words))
        # punctuation mirrored
        for ch in (':', '?', '…'):
            if src.rstrip().endswith(ch) and not txt.rstrip().endswith(ch):
                problems['punct'].append((src, txt, ch))
        # glossary
        for pat, need in GLOSSARY:
            if re.search(pat, src, re.I) and not any(n in txt for n in need):
                problems['glossary'].append((src, txt, pat))
        # hyphen / dash sanity: no space before punctuation
        if re.search(r'\s+[.,;:!?]', txt) and not re.search(r'\s+[.,;:!?]', src):
            problems['spacing'].append((src, txt))

    # mnemonic collisions per context
    mn = defaultdict(list)
    for ctx, src, txt, forms, block in items:
        m = re.search(r'&(.)', txt.replace('&nbsp;', '')) if txt else None
        if m:
            mn[(ctx, m.group(1))].append(src)
    for (ctx, ch), srcs in mn.items():
        if len(srcs) > 1:
            problems['mnemonic'].append((ctx, ch, srcs[:6]))

    print(f'messages: {len(items)}')
    for k, v in problems.items():
        print(f'\n== {k}: {len(v)}')
        for row in v[:25]:
            print('  ', row)

    json.dump({k: v for k, v in problems.items()}, open(os.path.join(HERE, 'qa-issues.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    return problems


if __name__ == '__main__':
    main()
