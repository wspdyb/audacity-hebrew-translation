import json, sys, os
q=json.load(open('he/queue.json')); tr=set(json.load(open('he/trivial.json')))
a,b=int(sys.argv[1]),int(sys.argv[2]); last=None
for r in q[a:b]:
    u=r['u']
    if u in tr: continue
    if r['ctx']!=last:
        print(f"── {r['ctx']}"); last=r['ctx']
    tag=''
    e=r['extra'] or ''
    if 'Action title' in e: tag=' ⟨title⟩'
    elif 'Action description' in e: tag=' ⟨desc⟩'
    if r['plural']: tag+=' ⟨plural×3⟩'
    print(f"U{u:04d}{tag} {r['src'].replace(chr(10),'⏎')}")
