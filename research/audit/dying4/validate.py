#!/usr/bin/env python3
"""validate.py: st4.c's lane 0 against reference/oracle.py, generation by generation, on the R = 11 and R = 13
vessels (c1 soups, open box, no restarts in trace mode).

    python3 research/audit/dying4/validate.py      # -> research/audit/dying4/validate_out.txt
"""
import os, sys, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, geom
SCR = os.path.join(ROOT, 'research', 'scratch', 'dying4'); os.makedirs(SCR, exist_ok=True)
EXE = os.path.join(SCR, 'st4')
subprocess.run(['gcc', '-O3', '-march=native', '-o', EXE, os.path.join(HERE, 'st4.c')], check=True)
out = open(os.path.join(HERE, 'validate_out.txt'), 'w')
allok = True
for R, G, seed in [(11, 600, 7), (13, 400, 8)]:
    V = geom.Vessel(R); gf = os.path.join(SCR, f'g{R}.txt'); V.write(gf)
    tr = subprocess.run([EXE, gf, 'trace', str(seed), str(G)], capture_output=True, text=True, check=True).stdout.splitlines()
    sets = [set(map(int, ln.split()[1:])) for ln in tr]
    off = R + 3 + (R + 3) % 2; H = 2 * off + 2
    m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
    for i in sets[0]:
        p = V.cells[i]; h[p[0] + off, p[1] + off, p[2] + off] = 1
    bad = None; pops = []
    for gq in range(G):
        mine = np.zeros_like(h)
        for i in sets[gq]:
            p = V.cells[i]; mine[p[0] + off, p[1] + off, p[2] + off] = 1
        if not (mine == h).all():
            bad = gq; break
        pops.append(int(h.sum()))
        h = oracle.step(h, m)
    ok = bad is None; allok &= ok
    s = f'R {R} seed {seed}: {G} generations, first mismatch {bad}; populations {pops[0]} -> {pops[-1]}  {"OK" if ok else "FAIL"}'
    print(s); out.write(s + '\n')
s = 'ALL OK' if allok else 'FAILED'; print(s); out.write(s + '\n')
