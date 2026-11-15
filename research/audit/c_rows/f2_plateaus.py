#!/usr/bin/env python3
"""F2 (CLAIMS.md): plateau heights of the legacy side-11 cube from research/experiments/kymo11.py's output.

    python3 research/experiments/kymo11.py          # writes research/scratch/kymo11.npz (oracle, ~2 min)
    python3 research/audit/c_rows/f2_plateaus.py [NPZ]

Hull radius R(t) = largest |s| over live (1,1,1) layers (doubled units about the centre), as in the notebook entry of
2026-11-12; a plateau is a maximal run of generations with the same R (generation >= 5, population > 0).
Prints each plateau's span, mean population, ratio to the first, and the hull-volume ratio (R/27)^3.
"""
import sys
import numpy as np

f = sys.argv[1] if len(sys.argv) > 1 else 'research/scratch/kymo11.npz'
d = np.load(f)
K, pop, layers = d['K'], d['pop'], d['layers']
R = np.array([np.abs(layers[k > 0]).max() if (k > 0).any() else 0 for k in K])
runs = []
g = 5
while g < len(R) and pop[g] > 0:
    h = g
    while h + 1 < len(R) and R[h + 1] == R[g] and pop[h + 1] > 0:
        h += 1
    runs.append((int(R[g]), g, h, float(pop[g:h + 1].mean())))
    g = h + 1
print('hull R by generation: first gens', list(R[:8]), '; last live gen', int(np.nonzero(pop)[0].max()))
first = runs[0][3]
for r, a, b, m in runs:
    print(f'R={r:2d} gens {a}-{b} ({b - a + 1} gens): mean pop {m:.0f}  ratio {m / first:.3f}  (R/27)^3 = {(r / 27) ** 3:.3f}')
