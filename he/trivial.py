#!/usr/bin/env python3
"""Auto-copy items that must not be translated (note names, units, symbols, product names)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
q = json.load(open(os.path.join(HERE, 'queue.json'), encoding='utf-8'))
TECH = {'VST','VST3','VST2','LV2','LADSPA','AU','MIDI','MP3','WAV','FLAC','OGG','OPUS','AIFF',
        'AAC','WMA','AC3','M4A','WavPack','FFmpeg','Nyquist','BPM','dB','Hz','kHz','RPM','EQ',
        'MIDI','Audio Unit','audio.com','SBSMS','SoundTouch','Qt','GPU','CPU','RAM','USB','ASIO',
        'WASAPI','Core Audio','ALSA','PulseAudio','PortAudio','LAME','Ogg Opus','LPC','VBL','MEI','LC','LTP','ERB','Mel','RMS'}
out = []
for r in q:
    s = r['src']
    if r['ctx'] == 'global/pitchName':
        out.append(r['u']); continue
    if s in TECH:
        out.append(r['u']); continue
    if not re.search(r'[A-Za-z\u0590-\u05FF]', s):      # no letters at all
        out.append(r['u']); continue
    if re.fullmatch(r'[\d.,\-+/×xX*: ]+\s*(kHz|Hz|dB|s|ms|px|%|cm|mm|in)?', s):
        out.append(r['u']); continue
    if re.fullmatch(r'%\d+( ?[-–,/] ?%\d+)+', s):
        out.append(r['u'])
uniq = sorted(set(out))
json.dump(uniq, open(os.path.join(HERE, 'trivial.json'), 'w'), indent=0)
print('auto-copy candidates:', len(uniq), 'of', len(q))
# preview non-pitch ones
for u in uniq:
    if q[u]['ctx'] != 'global/pitchName':
        print(f"U{u:04d} {q[u]['src']!r}")
