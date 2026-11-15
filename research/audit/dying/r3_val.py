#!/usr/bin/env python3
"""r3_val.py: r3_ex.c against reference/oracle.py on every system of the round-3 review, and against st.c.

    python3 research/audit/dying/r3_val.py      # -> r3_val_out.txt (a few minutes)

Trace mode (lane 0, the whole live set at every generation) against the oracle for v9c, v11c, v13c, v15c c1, v11c
csz, and the slab torus of r3_geo.py. A vessel sits in an open box; the slab is replicated periodically on the
oracle's 42^3 array torus (42(1,-1,0) and 42(0,1,-1) lie in the slab lattice; 13 dead layers separate the slab from
its image across the [111] wrap, so T2 keeps them dead). Run mode: r3_ex's lives file byte-identical to st.c's.
A short run also checks the excursion table against the dumps (in r3_ana.py).
"""
import sys, os, subprocess, filecmp
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'symmetric')); sys.path.insert(0, HERE)
import oracle, geo, r3_geo
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_dying', 'r3'); EX = os.path.join(SCR, 'r3_ex'); ST = os.path.join(SCR, 'st')
os.makedirs(SCR, exist_ok=True)
subprocess.run(['gcc', '-O3', '-march=native', '-o', EX, os.path.join(HERE, 'r3_ex.c')], check=True)
subprocess.run(['gcc', '-O3', '-march=native', '-o', ST, os.path.join(ROOT, 'research', 'audit', 'symmetric', 'st.c')], check=True)
out = open(os.path.join(HERE, 'r3_val_out.txt'), 'a' if sys.argv[1:] else 'w')


def say(s):
    print(s, flush=True); out.write(s + '\n'); out.flush()


def graph(name):
    gf = os.path.join(SCR, f'g_{name}.txt')
    if name == 'slab21':
        S, nb, orb = r3_geo.build(); geo.write(S, nb, orb, gf, [[0], [1]])
    elif name == 'slab44':
        S, nb, orb = r3_geo.build((8, 0, -8), (0, 8, -8)); geo.write(S, nb, orb, gf, [[0], [1]])
    else:
        sysname, gname = name.split('_'); S, nb, orb, gens = geo.build(sysname, gname); _, fg = geo.summary(S, nb, orb, gens, gname)
        geo.write(S, nb, orb, gf, fg)
    return S, gf


ok = True
ONLY = sys.argv[1:]          # optional subset (the 4x4 calibration torus slab44 was added after the first runs)
for name, G in [('v9c_c1', 600), ('v11c_c1', 600), ('v13c_c1', 600), ('v15c_c1', 400), ('v11c_csz', 600), ('slab21', 600), ('slab44', 600)]:
    if ONLY and name not in ONLY: continue
    S, gf = graph(name)
    tr = subprocess.run([EX, gf, 'trace', '77', '0.4', str(G + 1)], capture_output=True, text=True, check=True).stdout.splitlines()
    sets = [set(map(int, l.split()[1:])) for l in tr]
    if name.startswith('slab'):
        H = 42 if name == 'slab21' else 24; off = 0
        m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
        alls = np.argwhere(m[0] | m[1] | m[2]); rep = {}
        for q in alls:
            x, y, z = (int(v) for v in q); s = x + y + z; sm = s % H
            if 1 <= sm <= 15:
                p = (x - (s - sm), y, z); rep[(x, y, z)] = S.idx[S.key(p)]
        cellof = rep
        for q, i in rep.items():
            if i in sets[0]: h[q] = 1
    else:
        H = 2 * (int(name[1:3].rstrip('c')) + 6); H += (-H) % 4; off = H // 2   # off even: parity kept
        m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
        for i in sets[0]:
            p = S.cells[i]; h[p[0] + off, p[1] + off, p[2] + off] = 1
        cellof = None
    bad = None
    for g in range(1, G + 1):
        h = oracle.step(h, m); got = set(); extra = 0
        for q in zip(*np.nonzero(h)):
            if cellof is not None:
                k = tuple(int(v) for v in q)
                if k in cellof: got.add(cellof[k])
                else: extra += 1
            else:
                p = tuple(int(v) - off for v in q)
                if p in S.idx: got.add(S.idx[p])
                else: extra += 1
        if got != sets[g] or extra:
            bad = g; break
    a = os.path.join(SCR, f'vl_st_{name}.bin'); b = os.path.join(SCR, f'vl_ex_{name}.bin')
    subprocess.run([ST, gf, 'run', '5', '0.4', '20000', a], check=True, capture_output=True)
    pb = {'slab21': '32.57'}.get(name, '31.29')
    subprocess.run([EX, gf, 'run', '5', '0.4', '20000', b, b + '.ext', b + '.smp', '1000', b + '.dmp', '50', '512', '512', pb, b + '.x', '9', b + '.dx'],
                   check=True, capture_output=True)
    same = filecmp.cmp(a, b, shallow=False); nrec = os.path.getsize(a) // 16
    say(f'{name}: oracle {G} gens ' + ('OK' if bad is None else f'MISMATCH at {bad}') + f' (final pop {len(sets[G])}, cells {len(S.cells)}); '
        f'lives file vs st.c 20000 gens x 256 lanes, {nrec} records: ' + ('identical' if same else 'DIFFERENT'))
    ok &= bad is None and same
say('ALL OK' if ok else 'FAIL')
