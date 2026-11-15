#!/usr/bin/env python3
"""K1 (CLAIMS.md): mean lifetimes of m-layer slab soups vs the notebook's table, from thickness.py JSON records.
    python3 research/audit/c_rows/k1_thickness.py JSONL
Prints mean +- standard error per (N, m, seed) and, for m = 3, the slopes of ln(mean) per unit N."""
import json, sys, math
import numpy as np
CLAIM = {(1, 4): 4.6, (1, 6): 6.5, (1, 8): 8.3, (1, 12): 10.2, (1, 16): 11.9,
         (2, 4): 44, (2, 6): 53, (2, 8): 61, (2, 12): 74, (2, 16): 82, (2, 24): 92, (2, 32): 101,
         (3, 3): 75, (3, 4): 488, (3, 5): 2592, (3, 6): 13598, (3, 7): 76458}
m3 = {}
for l in open(sys.argv[1]):
    r = json.loads(l); mu = np.array(r['mu'], float); n = len(mu)
    se = mu.std(ddof=1) / math.sqrt(n); c = CLAIM.get((r['m'], r['N']))
    z = (mu.mean() - c) / se if c else float('nan')
    print(f"N={r['N']:2d} m={r['m']} seed={r['seed']:4d} n={n}: mean {mu.mean():.1f} +- {se:.1f}  claimed {c}  z {z:+.1f}")
    if r['m'] == 3 and r['seed'] >= 2000: m3[r['N']] = mu.mean()
Ns = sorted(m3)
print('m=3 slopes of ln(mean) per unit N:', [round(math.log(m3[b] / m3[a]), 2) for a, b in zip(Ns, Ns[1:])])
