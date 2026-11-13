#!/usr/bin/env python3
"""Goles-type energy for gump (node S5, research/theory/threshold.md): exact bookkeeping along real orbits.

Conventions (all on a finite vessel: a torus, or an open vessel whose outside is dead forever by T2):
  x(t) in {0,1}^N, n_i(t) = live neighbours, h_i(t) = n_i(t) + x_i(t)   (W = A + I, symmetric)
  E(t)  = -x(t).W.x(t-1) + 3.5 (|x(t)| + |x(t-1)|)                       defined for t >= 1
  overcrowded at t:  n_i(t) >= 6   (gump: dead at t+1; uncapped rule "h >= 4": live)
  drive        D(t) = sum over overcrowded i with x_i(t-1) = 1 of (h_i(t) - 3.5)
  dissipation  Q(t) = sum over NON-overcrowded i with x_i(t+1) != x_i(t-1) of |h_i(t) - 3.5|
  identity     E(t+1) - E(t) = D(t) - Q(t)        (checked exactly, every step, in integer units 2E)
Everything is kept doubled (2E, 2D, 2Q) so the arithmetic is exact.

  python3 research/theory/energy.py selftest          identity + inequality (c) on assorted orbits
Library use: Vessel arrays from build_torus3 / research/atlas/vessel.py (slab, octa).
"""
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'atlas'))


def offsets(a):
    b, c = [i for i in range(3) if i != a]; o = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; o.append(tuple(v))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[t] = st; o.append(tuple(v))
    return o


OFF = [offsets(a) for a in range(3)]


def build_torus3(L):
    """All cells of the (2L)^3 doubled-coordinate torus (L^3 cubes, 3L^3 cells); L >= 3."""
    cells = [(x, y, z) for x in range(2 * L) for y in range(2 * L) for z in range(2 * L) if (x & 1) + (y & 1) + (z & 1) == 1]
    idx = {c: i for i, c in enumerate(cells)}
    M = 2 * L
    nb = np.array([[idx[((c[0] + o[0]) % M, (c[1] + o[1]) % M, (c[2] + o[2]) % M)]
                    for o in OFF[[k for k in range(3) if c[k] & 1][0]]] for c in cells], np.int64)
    return cells, nb


class Stepper:
    """Gump (cap=True) or the uncapped threshold rule (cap=False) on a vessel given by neighbour indices
    (-1 = outside, dead forever)."""

    def __init__(self, nb):
        nb = np.asarray(nb, np.int64)
        self.N = len(nb)
        self.nb = np.where(nb < 0, self.N, nb)     # sentinel index N is always 0

    def counts(self, x):
        xp = np.append(x, 0).astype(np.int8)
        return xp[self.nb].sum(1)

    def step(self, x, cap=True):
        n = self.counts(x)
        h = n + x
        nxt = (h >= 4) & ((n <= 5) if cap else True)
        return nxt.astype(np.int8), n


def energy2(st, x, xm1):
    """2E(t) for x = x(t), xm1 = x(t-1), integers."""
    hm1 = st.counts(xm1) + xm1
    return int(-2 * np.dot(x.astype(np.int64), hm1) + 7 * (int(x.sum()) + int(xm1.sum())))


def terms(st, xm1, x, xp1, n, cap=True):
    """(2D, 2Q, over, O1, M, Mn) for the step x(t) -> x(t+1) with n = n(t).
    over = #overcrowded, O1 = #overcrowded with x(t-1)=1, M = #{x(t+1) != x(t-1)}, Mn = same among non-overcrowded."""
    h2 = 2 * (n.astype(np.int64) + x) - 7          # 2(h - 3.5), odd, never 0
    ov = (n >= 6) if cap else np.zeros(len(n), bool)   # uncapped rule: no exceptional cells
    o1 = ov & (xm1 == 1)
    mis = xp1 != xm1
    D2 = int(h2[o1].sum())
    Q2 = int(np.abs(h2[mis & ~ov]).sum())
    return D2, Q2, int(ov.sum()), int(o1.sum()), int(mis.sum()), int((mis & ~ov).sum())


def orbit_check(st, x0, gens, cap=True):
    """Run, verify 2E(t+1)-2E(t) == 2D-2Q exactly and inequality (c) at every step; return per-step records."""
    xm1 = x0.astype(np.int8); x, n = st.step(xm1, cap)
    E2 = energy2(st, x, xm1); recs = []
    for t in range(1, gens):
        xp1, n = st.step(x, cap)
        D2, Q2, ov, o1, M, Mn = terms(st, xm1, x, xp1, n, cap)
        E2n = energy2(st, xp1, x)
        assert E2n - E2 == D2 - Q2, ('identity fails', t, E2n - E2, D2, Q2)
        assert E2n - E2 <= -Mn + D2, ('inequality (c) fails', t)      # doubled form of (c)
        recs.append((t, E2, D2, Q2, ov, o1, M, Mn, int(x.sum())))
        xm1, x, E2 = x, xp1, E2n
    return recs


def selftest():
    import random
    from vessel import slab, octa
    rng = np.random.default_rng(1)
    tot = 0
    cells, nb = build_torus3(8)
    st = Stepper(nb)
    for rho in (0.1, 0.3, 0.5, 0.8):
        for cap in (True, False):
            r = orbit_check(st, (rng.random(st.N) < rho).astype(np.int8), 300, cap); tot += len(r)
            if not cap:
                assert all(rec[2] == 0 for rec in r)
                assert all(r[i + 1][1] <= r[i][1] for i in range(len(r) - 1))
    for m in (1, 2, 3):
        v = slab(10, m); st = Stepper(v.nb)
        for rho in (0.3, 0.6):
            r = orbit_check(st, (rng.random(st.N) < rho).astype(np.int8), 300); tot += len(r)
    v = octa('cube', 13); st = Stepper(v.nb)
    from lattice import step as lstep          # sparse stepper used (and oracle-checked) by the atlas
    x = (rng.random(st.N) < 0.4).astype(np.int8); S = frozenset(v.cells[i] for i in np.flatnonzero(x))
    for _ in range(60):
        x, _n = st.step(x); S = lstep(S)
        assert S == frozenset(v.cells[i] for i in np.flatnonzero(x)), 'stepper disagrees with lattice.step'
    for rho in (0.2, 0.4, 0.7):
        r = orbit_check(st, (rng.random(st.N) < rho).astype(np.int8), 500); tot += len(r)
    print(f'selftest ok: identity 2E(t+1)-2E(t) = 2D-2Q and inequality (c) exact on {tot} steps; '
          f'uncapped rule never increases E')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'selftest':
        selftest()
    else:
        print(__doc__)
