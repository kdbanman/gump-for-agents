#!/usr/bin/env python3
"""ref-chain (third review): LinkWrappedAll's `torusNb_all` against the oracle, and the price classes of
`wrapped_full_all` / `wrapped_area` against my own prices.

  OMP_NUM_THREADS=1 python3 research/blast/ref-chain/wrapped_check.py      (about 1 min)

1. For many (H, K, D), thin and skewed, K >= D included: cell i = 3(aD + b) + o of DiceDef's `gridCells H D`, its
   in-layer neighbours from oracle.offsets reduced mod the lattice (H*E1 + K*E2, D*E2) by my own canonical form,
   as a multiset of dice indices, against kIdx (LinkWrapped.lean: the kagome list `offs` reduced by the dice
   agent's Tr(a, b) = (a mod H, (b - (a div H) K) mod D)).  Negative control: one offs entry with the wrong orientation.
2. Prices (the dominant QSD, ln tau, c_i) on tori of 6-12 cells, rotation-invariant or not: the classes of
   equal c_i against "c_i = c_j when i = j mod 3", "all equal under (K,-H-K), (D,-D) in the lattice", and
   ln tau = H D (c_0 + c_1 + c_2) (`wrapped_area`, cells 0, 1, 2 = the three orientations at the origin).
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from link_numbers import face, tables, analyse
from kagome_check import canon_ab, rotation_invariant

OFFS = {0: [(0, -1, 1), (0, 1, -1), (1, 0, 0), (1, 1, 0), (2, 0, 0), (2, 0, 1)],
        1: [(1, 0, 1), (1, 0, -1), (0, 0, 0), (0, -1, 0), (2, 0, 0), (2, -1, 1)],
        2: [(2, 1, 0), (2, -1, 0), (0, 0, 0), (0, 0, -1), (1, 0, 0), (1, 1, -1)]}

def kidx(H, K, D, i, broken=False):
    o = i % 3; a = i // 3 // D; b = i // 3 % D
    L = list(OFFS[o])
    if broken and o == 0: L[3] = (2, 1, 0)                 # one entry given the wrong orientation
    out = []
    for oo, da, db in L:
        aa, bb = a + da, b + db
        ta, tb = aa % H, (bb - (aa // H) * K) % D          # the dice agent's Tr (Int ediv/emod, H, D > 0)
        out.append((ta * D + tb) * 3 + oo)
    return sorted(out)

ok_all = True; n = 0
cases = [(H, K, D) for H in range(1, 6) for D in range(1, 6) for K in range(0, 2 * D + 2)] + \
        [(1, 7, 19), (1, 4, 21), (1, 12, 28), (1, 17, 32), (6, 0, 6), (4, 9, 3), (2, 5, 1), (1, 30, 4)]
for H, K, D in cases:
    cells, red, coin = face('torus', H, K, D)
    nb, m1, m2 = tables(cells, red, coin)
    A = 3 * H * D
    good = len(cells) == A and all(sorted(nb[i]) == kidx(H, K, D, i) for i in range(A))
    neg = all(sorted(nb[i]) == kidx(H, K, D, i, broken=True) for i in range(A))
    n += 1
    if not good or neg:
        ok_all = False
        print(f"  ({H},{K}),(0,{D}): match {good}, negative control still matches {neg}")
print(f"torusNb vs oracle on {n} tori (H, D = 1..5, K = 0..2D+1, and 8 larger or skewed): all match and every "
      f"negative control fails: {ok_all}")

from link_numbers import alive_prob
from chain_numbers import qsd

def prices(H, K, D):
    cells, red, coin = face('torus', H, K, D)
    nb, m1, m2 = tables(cells, red, coin)
    A = len(cells); n = 1 << A
    X = ((np.arange(n)[:, None] >> np.arange(A)[None, :]) & 1)
    a = np.zeros((n, A))
    for i in range(A):
        k = X[:, nb[i]].sum(1)
        tab = np.array([[alive_prob(m1[i], m2[i], kk, s) for kk in range(7)] for s in (0, 1)])
        a[:, i] = tab[X[:, i], k]
    P = np.ones((n, 1))
    for i in reversed(range(A)):
        P = (P[:, :, None] * np.stack([1 - a[:, i], a[:, i]], axis=1)[:, None, :]).reshape(n, -1)
    Q = P[1:, 1:]; d = P[1:, 0]
    mu, lam, it = qsd(Q)
    lntau = -np.log(mu @ d)
    eps = -np.log(1 - a[1:]); E = eps.sum(1)
    xg, wg = np.polynomial.legendre.leggauss(64); sg = (xg + 1) / 2; wg = wg / 2
    def mean(s, f):
        w = mu * np.exp(-s * (E - E.min())); return (w * f).sum() / w.sum()
    c = np.array([sum(w * mean(s, eps[:, i]) for s, w in zip(sg, wg)) for i in range(A)])
    return c, lntau

def classes(c):
    g = []
    for i in range(len(c)):
        for gg in g:
            if abs(c[gg[0]] - c[i]) < 1e-11: gg.append(i); break
        else: g.append([i])
    return g

print("\nprice classes (wrapped_full_all, wrapped_area); claimed: i = j mod 3, all equal if rotation-invariant:")
for t in ((1, 0, 2), (2, 0, 1), (1, 1, 2), (2, 1, 1), (1, 0, 3), (1, 1, 3), (1, 2, 3), (1, 4, 3), (3, 0, 1),
          (1, 0, 4), (1, 1, 4), (1, 2, 4), (1, 3, 4), (1, 5, 4), (2, 0, 2), (2, 1, 2), (4, 0, 1), (4, 1, 1), (4, 2, 1)):
    H, K, D = t
    c, lntau = prices(H, K, D)
    A = len(c)
    rot = rotation_invariant(H, K, D)
    viol = [(i, j) for i in range(A) for j in range(A) if i % 3 == j % 3 and abs(c[i] - c[j]) > 1e-11]
    viol_rot = rot and (c.max() - c.min() > 1e-11)
    area = H * D * (c[0] + c[1] + c[2]) - lntau
    g = classes(c)
    kind = "orientation" if sorted(map(sorted, g)) == sorted([[i for i in range(A) if i % 3 == o] for o in range(3)]) \
        else ("one" if len(g) == 1 else f"{len(g)} classes")
    print(f"  ({H},{K}),(0,{D}) A={A:2d} rot-inv={str(rot):5s} c_0,c_1,c_2 = {c[0]:.8f} {c[1]:.8f} {c[2]:.8f} "
          f"true classes: {kind:12s} mod-3 violated: {bool(viol)}  rotation clause violated: {viol_rot}  "
          f"HD(c0+c1+c2) - ln tau = {area:.1e}")
