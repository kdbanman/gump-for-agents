#!/usr/bin/env python3
"""ref-chain: the constants of ChainCoins.lean and the Dobrushin coefficients quoted in notes/chain.md.

  python3 research/blast/ref-chain/constants_check.py      (about 10 s)

1. eps_max = -ln min(rho1^2 rho2, (1-rho1)^2 (1-rho2)): the smallest one-cell death probability over
   (state, k = 0..6), from the rule and the coin law (own enumeration, not the Lean case split), against 2.51
   and 2.509; the Taylor certificate used by emax_main (0.081312 * sum_{i<16} 2.51^i/i! >= 1); fair coins.
2. Dobrushin's interaction coefficient of the one-step product kernel: alpha = max_i sum_j C_ij with
   C_ij = sup over x, x' differing only at j of |a_i(x) - a_i(x')|; for a cell with six distinct in-layer
   neighbours and its own state this is 6*max_{s,k<=5}|a(s,k)-a(s,k+1)| + max_{k<=6}|a(0,k)-a(1,k)|.
   At (0.44, 0.42), on a 199 x 199 grid, and refined by a local search near the grid minimum.
"""
import math, itertools
import numpy as np
from chain_numbers import alive_table, coin_law

r1, r2 = 0.44, 0.42
a = alive_table(r1, r2)
dmin = (1 - a).min()
arg = np.unravel_index((1 - a).argmin(), a.shape)
emax = -math.log(dmin)
print(f"smallest one-cell death probability over (state, k<=6): {dmin:.10f} at (state, k) = {tuple(int(v) for v in arg)};"
      f"  0.44^2*0.42 = {r1**2*r2:.10f}, (0.56)^2*0.58 = {(1-r1)**2*(1-r2):.10f}")
print(f"eps_max = {emax:.10f}:  <= 2.51: {emax <= 2.51};  <= 2.509: {emax <= 2.509}")
cert = r1 ** 2 * r2 * sum(2.51 ** i / math.factorial(i) for i in range(16))
print(f"emax_main certificate: 0.081312 * sum_(i<16) 2.51^i/i! = {cert:.6f} >= 1: {cert >= 1};  "
      f"0.081312 * e^2.509 = {r1**2*r2*math.exp(2.509):.6f} (< 1, so ln tau <= 2.509 A does not follow)")
af = alive_table(0.5, 0.5)
print(f"fair coins: smallest death probability {(1-af).min():.6f} = 1/8; eps_max = ln 8 = {math.log(8):.6f} <= 2.08: "
      f"{math.log(8) <= 2.08};  certificate {(1/8)*sum(2.08**i/math.factorial(i) for i in range(14)):.6f} >= 1")
# every death event contains b = 0 or b = 3 (threeCoins_death_ge's case split, recomputed)
from oracle import BIRTH, SURVIVE
ok = all(any(not ((k + b) in (SURVIVE if s else BIRTH)) for b in (0, 3)) for s in (0, 1) for k in range(7))
print(f"every (state, k<=6) has b = 0 or b = 3 among its deaths: {ok}")
# the two-coin cell (hull corner, k <= 2)
p2 = lambda r: np.array([(1 - r) ** 2, 2 * r * (1 - r), r ** 2])
d2 = min(sum(p2(r1)[b] for b in range(3) if not ((k + b) in (SURVIVE if s else BIRTH))) for s in (0, 1) for k in range(3))
print(f"two coins (2,0), k <= 2: smallest death probability {d2:.6f} >= atomMin {min(r1**2*r2,(1-r1)**2*(1-r2)):.6f}: "
      f"{d2 >= min(r1**2*r2,(1-r1)**2*(1-r2))}")


def alpha(x, y):
    t = alive_table(x, y)
    nb = max(abs(t[s, k] - t[s, k + 1]) for s in (0, 1) for k in range(6))
    own = max(abs(t[0, k] - t[1, k]) for k in range(7))
    return 6 * nb + own, nb, own


v, nb, own = alpha(r1, r2)
print(f"Dobrushin alpha(0.44, 0.42) = {v:.6f}  (neighbour term 6 x {nb:.6f}, own-state term {own:.6f})")
g = np.linspace(0.005, 0.995, 199)
vals = np.array([[alpha(x, y)[0] for y in g] for x in g])
i, j = np.unravel_index(vals.argmin(), vals.shape)
best = (vals.min(), g[i], g[j])
# local refinement
x0, y0, h = g[i], g[j], 0.005
while h > 1e-7:
    cand = [(alpha(x0 + dx, y0 + dy)[0], x0 + dx, y0 + dy) for dx in (-h, 0, h) for dy in (-h, 0, h)
            if 0 < x0 + dx < 1 and 0 < y0 + dy < 1]
    m = min(cand)
    if m[0] < best[0] - 1e-15: best = m; x0, y0 = m[1], m[2]
    else: h /= 2
print(f"min over the 199 x 199 grid of (0.005..0.995)^2: {vals.min():.6f} at ({g[i]:.3f}, {g[j]:.3f}); refined: "
      f"{best[0]:.6f} at ({best[1]:.5f}, {best[2]:.5f});  alpha(1/2, 1/2) = {alpha(0.5, 0.5)[0]:.6f};  "
      f"grid points below 2.625: {(vals < 2.625 - 1e-12).sum()}")
print(f"near the edges: alpha(0.005, 0.5) = {alpha(0.005, 0.5)[0]:.3f}, alpha(0.995, 0.5) = {alpha(0.995, 0.5)[0]:.3f}, "
      f"alpha(0.5, 0.005) = {alpha(0.5, 0.005)[0]:.3f}, alpha(0.5, 0.995) = {alpha(0.5, 0.995)[0]:.3f}")
