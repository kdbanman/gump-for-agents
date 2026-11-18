#!/usr/bin/env python3
"""Tails of the stationary face population of living tubes against length: -ln P(pop >= x A) and -ln P(pop <= x A)
per cell, and their local prices between consecutive lengths (is the falling price already in the living state?).
    python3 tails.py FILE1 FILE2 ...   (outputs of `tube1d pophist`, increasing length)"""
import sys, math
import numpy as np
D = []
for fn in sys.argv[1:]:
    hdr = open(fn).readline(); A = int(hdr.split('A=')[1].split()[0]); L = float(hdr.split('length=')[1].split()[0])
    h = np.zeros(A + 1)
    for l in open(fn):
        if l[0].isdigit(): k, c = l.split(); h[int(k)] = float(c)
    D.append((L, A, h))
print("# stationary mean density and variance per cell:", ' '.join(f"L={L:.0f}: {(np.arange(A+1)*h).sum()/h.sum()/A:.4f}, {(((np.arange(A+1)-(np.arange(A+1)*h).sum()/h.sum())**2)*h).sum()/h.sum()/A:.4f}" for L, A, h in D))
for name, thr, up in (('upper tail P(pop >= x A)', (7/12, 2/3, 3/4), True), ('lower tail P(pop <= x A)', (5/12, 1/3, 1/4, 1/6), False)):   # thresholds exact at every A = 12 L
    print(f"# {name}: -ln P (events), then local price per cell between consecutive lengths")
    for x in thr:
        vals = []
        for L, A, h in D:
            k = int(round(x * A))
            n = h[k:].sum() if up else h[:k + 1].sum()
            vals.append((L, A, -math.log(n / h.sum()) if n > 0 else float('nan'), n, k))
        line = f"x = {x:.4f}: " + '  '.join(f"L={L:.0f} k={k}: {v:.3f} ({n:.0f})" for L, A, v, n, k in vals)
        line += '   | prices: ' + ' '.join(f"{(vals[i+1][2]-vals[i][2])/(vals[i+1][1]-vals[i][1]):.4f}+-{math.hypot(1/math.sqrt(max(vals[i][3],1)), 1/math.sqrt(max(vals[i+1][3],1)))/(vals[i+1][1]-vals[i][1]):.4f}" for i in range(len(vals) - 1))
        print(line)
