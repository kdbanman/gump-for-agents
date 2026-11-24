#!/usr/bin/env python3
"""ref-chain (second review): the Link theorems' face-specific claims, from my own code.

  OMP_NUM_THREADS=1 python3 research/blast/ref-chain/link_numbers.py      (about 30 s)

Faces are built from their definitions in GumpMath/DiceDef.lean (cell lists in that file's order: `hullCells`
x then y; `gridCells` a, then b, then o; the `red` and `coin` of `hull`, `torus`, `strip`, `patch`), with the
in-layer neighbours and the coins beneath taken from reference/oracle.py's offsets (d = (1,1,1): zero sum in the
layer, -2 one layer beneath (density rho1), -4 two beneath (rho2)), not from the dice agent's tables.
Kernel: cell i alive next iff rule(x_i, k_i + b_i), rule = oracle BIRTH/SURVIVE; rho = (11/25, 21/50).
Printed: lambda, ln tau, the per-cell prices c_i, the classes the Lean theorems assert equal (`cls` of
Link<Face>Sym.lean and torus202_full) against the classes of numerically equal prices, the certificate's u, the
count of states that can survive, and which states die surely.
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
from oracle import offsets, BIRTH, SURVIVE
from chain_numbers import qsd

R1, R2 = 11 / 25, 21 / 50
E1 = np.array((2, -2, 0)); E2 = np.array((2, 0, -2))


def is_cell(p):
    return sum(c % 2 for c in p) == 1


def ab_cell(o, a, b):
    base = [(1, 0, 0), (0, 1, 0), (0, 0, 1)][o]
    return tuple(int(v) for v in np.array(base) + a * E1 + b * E2)


def cell_ab(p):
    o = [i for i in range(3) if p[i] % 2][0]
    base = [(1, 0, 0), (0, 1, 0), (0, 0, 1)][o]
    q = np.array(p) - np.array(base)
    return o, int(-q[1] // 2), int(-q[2] // 2)


def face(kind, *args):
    """cells (list of points, in DiceDef order), red, coin."""
    if kind == 'hull':
        R, = args
        cells = [(x, y, R - x - y) for x in range(R + 1) for y in range(R + 1 - x)]
        cells = [p for p in cells if is_cell(p)]
        return cells, (lambda p: p), (lambda q: sum(abs(c) for c in q) <= R)
    W, D = args[-2], args[-1]
    if kind == 'torus':
        H, K, D = args
        cells = [ab_cell(o, a, b) for a in range(H) for b in range(D) for o in range(3)]
        def red(p):
            o, a, b = cell_ab(p)
            return ab_cell(o, a % H, (b - (a // H) * K) % D)
        return cells, red, (lambda q: True)
    cells = [ab_cell(o, a, b) for a in range(W) for b in range(D) for o in range(3)]
    if kind == 'strip':
        def red(p):
            o, a, b = cell_ab(p)
            return ab_cell(o, a, b % D)
        return cells, red, (lambda q: True)
    if kind == 'patch':
        return cells, (lambda p: p), (lambda q: True)


def tables(cells, red, coin):
    index = {p: i for i, p in enumerate(cells)}
    nb, m1, m2 = [], [], []
    for p in cells:
        o = [i for i in range(3) if p[i] % 2][0]
        s = sum(p)
        lst = []; c1 = c2 = 0
        for off in offsets(o):
            q = tuple(a + b for a, b in zip(p, off))
            ds = sum(q) - s
            if ds == 0:
                r = red(q)
                if r in index: lst.append(index[r])
            elif ds == -2 and coin(q): c1 += 1
            elif ds == -4 and coin(q): c2 += 1
        nb.append(lst); m1.append(c1); m2.append(c2)
    return nb, m1, m2


def alive_prob(m1, m2, k, s):
    from math import comb
    tot = 0.0
    for j in range(m1 + 1):
        for l in range(m2 + 1):
            if (k + j + l) in (SURVIVE if s else BIRTH):
                tot += comb(m1, j) * R1**j * (1 - R1)**(m1 - j) * comb(m2, l) * R2**l * (1 - R2)**(m2 - l)
    return tot


def analyse(name, kind, args, cls_claim, u_claim, exact=None):
    cells, red, coin = face(kind, *args)
    nb, m1, m2 = tables(cells, red, coin)
    A = len(cells); n = 1 << A
    X = ((np.arange(n)[:, None] >> np.arange(A)[None, :]) & 1)
    a = np.zeros((n, A))
    for i in range(A):
        k = X[:, nb[i]].sum(1) if nb[i] else np.zeros(n, int)
        tab = {(s, kk): alive_prob(m1[i], m2[i], kk, s) for s in (0, 1) for kk in range(7)}
        a[:, i] = [tab[(int(X[x, i]), int(k[x]))] for x in range(n)]
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
    print(f"\n== {name}: A = {A}, coins (m1,m2) = {list(zip(m1, m2))}, neighbour counts = {[len(l) for l in nb]}")
    print(f"   lambda = {lam:.16f}   ln tau = {lntau:.12f}" + (f"  (exact.csv {exact})" if exact else "")
          + f"   sum c_i - ln tau = {c.sum() - lntau:.1e}")
    print("   c_i = " + ", ".join(f"{v:.10f}" for v in c))
    # classes of numerically equal prices
    groups = []
    for i in range(A):
        for g in groups:
            if abs(c[g[0]] - c[i]) < 1e-11: g.append(i); break
        else: groups.append([i])
    claimed = {}
    for i, v in enumerate(cls_claim): claimed.setdefault(v, []).append(i)
    claimed = list(claimed.values())
    viol = [(i, j, abs(c[i] - c[j])) for g in claimed for i in g for j in g if i < j and abs(c[i] - c[j]) > 1e-11]
    print(f"   classes asserted equal by Lean: {claimed}")
    print(f"   classes of equal prices (|diff| < 1e-11): {groups}")
    print(f"   asserted equalities violated: {viol if viol else 'none'};  Lean's classes as coarse as the numerics: "
          f"{sorted(map(sorted, claimed)) == sorted(map(sorted, groups))}")
    # support structure
    S = Q > 0
    canlive = S.any(1)
    dies = [int(x) + 1 for x in np.nonzero(~canlive)[0]]
    ui = u_claim - 1
    Mu = all(a[u_claim, i] > 0 for i in range(A))
    print(f"   states that can survive: {canlive.sum()} of {n - 1}; surely dying: {dies};  u = {u_claim}: every cell "
          f"alive-able {Mu}, Q u y > 0 for all living y: {bool(S[ui].all())}")
    # every surviving state reaches u: BFS backwards
    seen = np.zeros(n - 1, bool); seen[ui] = True; front = seen.copy(); depth = 0
    while front.any():
        nxt = S[:, front].any(1) & ~seen
        if not nxt.any(): break
        seen |= nxt; front = nxt; depth += 1
    print(f"   every state that can survive reaches u: {bool((seen | ~canlive)[canlive].all() and seen[canlive].all())}; "
          f"largest distance to u: {depth}")
    return c, lam, lntau


if __name__ == '__main__':
    analyse('hull 3', 'hull', (3,), [0, 1, 1, 0, 1, 1, 1, 1, 0], 207, '2.483715746334')
    analyse('torus 1 0 3', 'torus', (1, 0, 3), [0, 0, 1, 0, 0, 1, 0, 0, 1], 10, '3.393524719052')
    analyse('torus 1 1 3', 'torus', (1, 1, 3), [0] * 9, 3, '2.694626605944')
    analyse('strip 1 3', 'strip', (1, 3), [0, 1, 0, 0, 1, 0, 0, 1, 0], 14, '2.798878056925')
    analyse('patch 1 3', 'patch', (1, 3), [0, 1, 2, 3, 4, 3, 2, 1, 0], 73, '1.880418934121')
    analyse('torus 2 0 2', 'torus', (2, 0, 2), [0] * 12, 7, '3.981836588280')
