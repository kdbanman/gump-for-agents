#!/usr/bin/env python3
"""Independent event check for the thin tori (numpy stepper, own layer indexing, events checked every generation).

    python3 research/audit/shape2/fwcheck.py a k b R GENS SEED

Graph: research/audit/shape/geom_check.my_slab (AUTOMATON.md cube-index table, multiplicity kept; ts.c uses the same
graph and both match the engine). Everything else is written here: layers s = d.p mod P with P computed from the two
generators (checked against every neighbour pair: s(nbr) - s(cell) in {0, +-2, +-4} mod P), ring adjacency = s
differs by 2 mod P, face layers t = 0 and 7. Each replica runs ONE life from a p = 0.4 soup and keeps running after
its events, so that we can check (i) a dead face stays dead, (ii) three adjacent dead transverse layers stay dead,
and record per replica the generation of the first face death, the first firewall and the extinction of the slab,
exactly (no check interval). Prints how many face/firewall pairs fall within 8 and 16 generations of each other
(the "ties" of a periodic check) and which came first.
"""
import math, os, sys
from math import gcd
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import geom_check as gc  # noqa


def setup(L):
    a, k, b = L
    cells, idx, nb = gc.my_slab(L)
    n = len(cells)
    NB = np.array([[n if x is None else x for x in row] for row in nb])
    dp = np.array([gc.doubled(c) for c in cells])
    layers = []
    for d in [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]:
        P = 0
        for (x, y) in [(a, k), (0, b)]:
            P = gcd(P, abs(2 * (d[0] * x + d[1] * y - d[2] * (x + y))))
        s = (dp @ np.array(d)) % P
        for i in range(n):
            for x in nb[i]:
                if x is not None:
                    assert (s[x] - s[i]) % P in {0, 2, 4, P - 2, P - 4}, (L, d)
        res = list(range(1, P, 2))
        assert set(s) == set(res)
        M = np.zeros((len(res), n), bool)
        for j, r in enumerate(res):
            M[j, s == r] = True
        layers.append(M)
    t = np.array([c[3] for c in cells])
    return n, NB, layers, t == 0, t == 7


def main(L, R, gens, seed):
    n, NB, layers, f0, f1 = setup(L)
    rng = np.random.default_rng(seed)
    x = np.zeros((n + 1, R), bool); x[:n] = rng.random((n, R)) < 0.4
    INF = 1 << 40
    face = np.full(R, INF); fw = np.full(R, INF); ext = np.full(R, INF)
    fwd = np.full(R, -1); fwl = np.full(R, -1)
    viol_face = viol_fw = 0
    ar = np.arange(R)
    for g in range(1, gens + 1):
        c = x[NB].sum(1)
        x[:n] = (c == 4) | (c == 5) | (x[:n] & (c == 3))
        xi = x[:n].astype(np.int32)
        fd = (f0 @ xi == 0) | (f1 @ xi == 0)
        viol_face += int((~fd & (face < INF)).sum())
        face[fd & (face == INF)] = g
        ext[(xi.sum(0) == 0) & (ext == INF)] = g
        for di, M in enumerate(layers):
            m = M.shape[0]
            if m < 3:
                continue
            dead = (M.astype(np.int32) @ xi) == 0                     # (m, R)
            three = dead & np.roll(dead, -1, 0) & np.roll(dead, -2, 0)
            new = three.any(0) & (fw == INF)
            fw[new] = g; fwd[new] = di; fwl[new] = three[:, new].argmax(0)
            chk = (fw < g) & (fwd == di)
            if chk.any():
                l0 = fwl[chk]; r = ar[chk]
                ok = dead[l0 % m, r] & dead[(l0 + 1) % m, r] & dead[(l0 + 2) % m, r]
                viol_fw += int((~ok).sum())
    first = np.minimum(face, fw)
    isF = (face < fw) & (face < INF); isW = (fw <= face) & (fw < INF)
    E = np.minimum(first, gens).sum(); F = int(isF.sum()); W = int(isW.sum())
    both = (face < INF) & (fw < INF)
    dlt = (face - fw)[both]
    def win(w):
        m = np.abs(dlt) < w
        return f'{int(m.sum())} (face first {int((dlt[m] < 0).sum())}, firewall first {int((dlt[m] > 0).sum())}, same gen {int((dlt[m] == 0).sum())})'
    fx = (face < INF) & (ext < INF) & (ext - face < 16)
    print(f'{L}: R {R} gens {gens}: first events F {F} W {W}, none {R - F - W}; exposure {E:.4g}; '
          f'ln tau_face {math.log(2 * E / F) if F else float("nan"):.3f} +- {1 / math.sqrt(F) if F else 0:.3f} '
          f'(F/(F+W) {F / max(F + W, 1):.3f}); ln tau_fw {math.log(E / W) if W else float("inf"):.3f}')
    print(f'   face/firewall within 16 gens: {win(16)}; within 8: {win(8)}')
    print(f'   face deaths followed by extinction of the whole slab within 16 gens: {int(fx.sum())} of {int((face < INF).sum())}; '
          f'first face deaths (before any firewall) so followed: {int((fx & isF).sum())} of {F}')
    print(f'   violations: dead face revived {viol_face}; firewall layers revived {viol_fw}')


if __name__ == '__main__':
    a = list(map(int, sys.argv[1:]))
    main(tuple(a[:3]), a[3], a[4], a[5])
