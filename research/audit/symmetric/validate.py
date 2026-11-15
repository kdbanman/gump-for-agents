#!/usr/bin/env python3
"""validate.py: st.c (lane 0, symmetric soup) against reference/oracle.py on the legacy array torus.
    python3 validate.py SYS GROUP GENS SEED
Vessels are placed in an H = 32 array torus (outside dead; T2 says it stays dead, checked here too).
Slabs s<P>x<Q> are lifted to an H = 96 array torus: the slab torus repeated with the out-of-plane period (24,0,0),
leaving 4 dead layers between copies (a firewall), so each copy evolves as the slab torus.
Compares the full live-cell set every generation."""
import sys, os, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, geo
ST = os.path.join(ROOT, 'research', 'scratch', 'audit_symmetric', 'st')
sysname, gname, G, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
S, nb, orb, gens = geo.build(sysname, gname)
_, fg = geo.summary(S, nb, orb, gens, gname)
gf = os.path.join(ROOT, 'research', 'scratch', 'audit_symmetric', f'val_{sysname}_{gname}.txt')
geo.write(S, nb, orb, gf, fg)
tr = subprocess.run([ST, gf, 'trace', seed, '0.4', str(G + 1)], capture_output=True, text=True, check=True).stdout.splitlines()
sets = [set(map(int, l.split()[1:])) for l in tr]
if sysname.startswith('v'):
    H = 32; off = 16
    def lift(live):
        h = np.zeros((H, H, H), np.int8)
        for i in live:
            p = S.cells[i]; h[p[0] + off, p[1] + off, p[2] + off] = 1
        return h
    def back(h):
        out = set(); extra = 0
        for q in zip(*np.nonzero(h)):
            p = tuple(int(v) - off for v in q)
            if p in S.idx: out.add(S.idx[p])
            else: extra += 1
        return out, extra
else:
    H = 96; T = 24
    m = oracle.masks(H); valid = m[0] | m[1] | m[2]
    pts = np.argwhere(valid)
    lifted = []   # (array point, slab cell index)
    for q in pts:
        s = int(q.sum()); k = (s - 1) // T
        if 1 <= s - k * T <= 15:
            r = q - np.array([k * T, 0, 0]); key = S.key(r)
            lifted.append((tuple(int(v) for v in q), S.idx[key]))
    def lift(live):
        h = np.zeros((H, H, H), np.int8)
        for q, i in lifted:
            if i in live: h[q] = 1
        return h
    inslab = np.zeros((H, H, H), bool)
    for q, i in lifted: inslab[q] = True
    def back(h):
        # every copy must agree with the slab state; return the set from copy consistency
        out = set(); bad = 0
        live = h.astype(bool)
        extra = int((live & ~inslab).sum())
        per = {}
        for q, i in lifted:
            per.setdefault(i, set()).add(int(h[q]))
        for i, v in per.items():
            if len(v) > 1: bad += 1
            if 1 in v: out.add(i)
        return out, extra + bad
m = oracle.masks(H)
h = lift(sets[0]); bad = 0
for g in range(1, G + 1):
    h = oracle.step(h, m, birth=(4,)) if os.environ.get("NEGCTRL") else oracle.step(h, m)
    got, extra = back(h)
    if got != sets[g] or extra:
        print(f'MISMATCH at generation {g}: st {len(sets[g])} oracle {len(got)} outside/inconsistent {extra}'); bad = 1; break
print(sysname, gname, 'seed', seed, 'gens', G, 'population at end', len(sets[G]), 'OK' if not bad else 'FAIL')
