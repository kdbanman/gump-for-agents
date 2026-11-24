#!/usr/bin/env python3
"""ref-chain: a sharper constant for Theorem 1 on wrapped faces, and a brute-force check.

  python3 research/blast/ref-chain/emax_bound.py

On paper: let S = cells alive with k = 3 (the only (state, k) with cost eps_max).  Each has 3 dead in-layer
neighbour slots, all outside S; each cell outside S receives at most 6 slots (in-layer multiplicities are
symmetric), so 3|S| <= 6(A - |S|), |S| <= 2A/3, and E(x) <= (2 eps_max + eps_2) A / 3, eps_2 the largest cost
of any other (state, k).  Hence ln tau <= E_mu E <= max_x E(x) <= (2 eps_max + eps_2)/3 * A.
"""
import math, numpy as np
from chain_numbers import alive_table, build
a = alive_table(0.44, 0.42)
cost = -np.log(1 - a)
order = sorted(((cost[s, k], s, k) for s in (0, 1) for k in range(7)), reverse=True)
print("largest one-cell costs (cost, state, k):", [(round(c, 4), s, k) for c, s, k in order[:4]])
e1, e2 = order[0][0], order[1][0]
print(f"bound (2 eps_max + eps_2)/3 = {(2*e1 + e2)/3:.4f} per cell  (eps_max = {e1:.4f})")
for t in ((2, 0, 2), (1, 1, 4), (1, 0, 4), (1, 1, 3), (1, 0, 3)):
    cs, N, X, aa, P = build(*t)
    E = (-np.log(1 - aa)).sum(1)[1:]
    print(f"torus {t}: max_x E(x)/A = {E.max()/len(cs):.4f}  (E_mu E / A from chain_numbers.out is smaller)")
