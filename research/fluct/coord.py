#!/usr/bin/env python3
"""Is n the right reaction coordinate? From the committor tallies Cm[n, n2, outcome] of qsd.py (visits at
1 <= n < KMAX, outcome = reach n = 0 before n >= A/2), the outcome entropy that remains given
  n alone; xi = n + alpha * n2 (best alpha, xi binned to integers); (n, n2) jointly (saturated),
as a fraction of the entropy given nothing (all visits with n <= NMAX).   python3 research/fluct/coord.py R [NMAX]
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl
R = sys.argv[1]; NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 12
tag = f'R{R}' if R.isdigit() else R
z = np.load(os.path.join(fl.SCR, f'qsd_{tag}.npz')); C = z['Cm'][1:NMAX + 1].astype(float)   # n = 1..NMAX
def H(c):     # c: (..., 2) tallies -> total conditional entropy (nats)
    c = c.reshape(-1, 2); t = c.sum(1); m = t > 0; p = c[m, 1] / t[m]
    e = -(p * np.log(np.where(p > 0, p, 1)) + (1 - p) * np.log(np.where(p < 1, 1 - p, 1)))
    return float((t[m] * e).sum())
tot = C.sum((0, 1)); h0 = H(tot[None]); hn = H(C.sum(1)); hnn = H(C)
n_idx, s_idx = np.meshgrid(np.arange(1, NMAX + 1), np.arange(C.shape[1]), indexing='ij')
best = None
for al in np.linspace(-1, 1, 81):
    xi = np.round(n_idx + al * s_idx).astype(int); xi -= xi.min()
    acc = np.zeros((xi.max() + 1, 2)); np.add.at(acc, xi.ravel(), C.reshape(-1, 2))
    h = H(acc)
    if best is None or h < best[1]: best = (al, h)
N = tot.sum()
print(f'{tag}: {int(N)} visits with 1 <= n <= {NMAX}; outcome entropy per visit: none {h0 / N:.4f}, n {hn / N:.4f} '
      f'({1 - hn / h0:.1%} explained), n + {best[0]:+.3f} n2 {best[1] / N:.4f} ({1 - best[1] / h0:.1%}), (n, n2) {hnn / N:.4f} ({1 - hnn / h0:.1%})')
