#!/usr/bin/env python3
"""Exact quasi-stationary death rate of M(1) (one layer of the rule over coins of density 102/256) on the thin torus,
for the review of research/theory/thin/. Own code: graph from tt.vessel (geom_check.my_slab), coin-sharing components
found here by union-find, kernel = product over components, power iteration by two matrix products.

    python3 research/audit/thin/exact.py b wall        # ring: wall 0; segment of n = b - 3 sites: wall 3
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tt  # noqa: E402

Q = 102 / 256


def setup(b, wall):
    cells, idx, nb, face, wallc, coin, inter = tt.vessel('model', b, 1, wall)
    F = face[0]; cs = set(coin); fs = set(F)
    par = {}

    def find(x):
        while par.setdefault(x, x) != x:
            x = par[x]
        return x
    for i in F:
        for x in nb[i]:
            if x in cs:
                par[find(('c', x))] = find(('f', i))
    comps = {}
    for i in F:
        comps.setdefault(find(('f', i)), []).append(i)
    comps = list(comps.values())
    order = [i for c in comps for i in c]          # bit j of a state = face cell order[j]
    pos = {i: j for j, i in enumerate(order)}
    N = len(order)
    xs = np.arange(1 << N, dtype=np.int64)
    bit = lambda j: (xs >> j) & 1
    kface = {i: sum(bit(pos[x]) for x in nb[i] if x in fs) for i in F}   # live face neighbours, per x
    P = []; off = 0; offs = []
    for c in comps:
        K = sorted({x for i in c for x in nb[i] if x in cs})
        kp = {x: j for j, x in enumerate(K)}
        Pc = np.zeros((1 << N, 1 << len(c)))
        for conf in range(1 << len(K)):
            ones = bin(conf).count('1'); wgt = Q ** ones * (1 - Q) ** (len(K) - ones)
            out = np.zeros(1 << N, dtype=np.int64)
            for t, i in enumerate(c):
                ncoin = sum((conf >> kp[x]) & 1 for x in nb[i] if x in cs)
                n = kface[i] + ncoin; s = bit(pos[i])
                nxt = ((n == 4) | (n == 5) | ((s == 1) & (n == 3))).astype(np.int64)
                out |= nxt << t
            Pc[xs, out] += wgt   # xs distinct: no repeated index
        assert np.allclose(Pc.sum(1), 1)
        P.append(Pc); offs.append(off); off += len(c)
    return comps, P, offs, N


def qsd(b, wall, tol=1e-13, maxit=5000):
    comps, P, offs, N = setup(b, wall)
    # split components into two groups for the two matrix products
    half = len(comps) // 2
    gA, gB = list(range(half)), list(range(half, len(comps)))

    def outer(idx, v=None):
        T = np.ones((1 << N, 1)) if v is None else v[:, None].copy()
        bits = []
        for c in idx:
            T = (T[:, :, None] * P[c][:, None, :]).reshape(1 << N, -1)   # new component is the fastest index
            bits.append(c)
        return T, bits

    def comp_index(bits):
        # composite index (first listed component slowest) -> state bits
        sizes = [len(comps[c]) for c in bits]
        tot = sum(sizes); m = np.arange(1 << tot); res = np.zeros_like(m); sh = 0
        for c, s in zip(reversed(bits), reversed(sizes)):
            res |= ((m >> sh) & ((1 << s) - 1)) << offs[c]; sh += s
        return res
    TB, bB = outer(gB)
    iA = None; iB = comp_index(bB)
    v = np.ones(1 << N); v[0] = 0; v /= v.sum()
    lam_old = 0
    for it in range(maxit):
        TA, bA = outer(gA, v)
        if iA is None:
            iA = comp_index(bA)
        M = TA.T @ TB                                   # [a, b] composite
        w = np.zeros(1 << N)
        w[(iA[:, None] | iB[None, :]).ravel()] = M.ravel()
        w[0] = 0
        lam = w.sum() / v.sum(); v = w / w.sum()
        if abs(lam - lam_old) < tol and it > 20:
            break
        lam_old = lam
    return lam, it, [len(c) for c in comps]


if __name__ == '__main__':
    b, wall = int(sys.argv[1]), int(sys.argv[2])
    lam, it, cs = qsd(b, wall)
    print(f'M(1) b={b} wall={wall} (n = {b - wall} sites): components {cs}; lambda = {lam:.12f} after {it} iterations; '
          f'ln tau = -ln(1 - lambda) = {-math.log(1 - lam):.6f}')
