"""Steppers for REVIEW-signals-5, written from docs/AUTOMATON.md section 2 (no code from research/signals/sg.py or
scat.py).  Doubled coordinates; a cell has exactly one odd coordinate.

  step(live)            sparse, infinite lattice (python sets)
  Tube(...)             numpy batch stepper on the cells of the 3 x 3 tube 1 <= x+y+z, x-y+z <= 5 inside the planes
                        x+y-z, x-y-z <= C, units >= U0 - 1; unit U0 - 1 is overwritten every generation by the plain
                        rake train (exact while units U0, U0+1 still hold the plain train, which callers check).
  oracle_run(...)       reference/oracle.py's own step() on an even box torus (the judge)
Checked against the oracle by check_st5.py.
"""
import os, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402


def _offs(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for s in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = s; out.append(tuple(o))
    return out


OFFS = [_offs(a) for a in range(3)]


def axis(c):
    return 0 if c[0] & 1 else (1 if c[1] & 1 else 2)


def is_cell(c):
    return (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1


def nb(c):
    return [(c[0] + o[0], c[1] + o[1], c[2] + o[2]) for o in OFFS[axis(c)]]


def step(live):
    cnt = Counter(q for c in live for q in nb(c))
    return frozenset(q for q, k in cnt.items() if k == 4 or k == 5 or (k == 3 and q in live))


def unit(c):
    return c[0] >> 1


def tr(c, k):
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def mirror(c):
    """(x,y,z) -> (z-4, y, x+4): the reflection exchanging the two ends of wire C (README section 9)."""
    return (c[2] - 4, c[1], c[0] + 4)


# ---------------------------------------------------------------- the rake train (fb)^inf moving towards +v
# Base cells (relative to the unit) of the two units of one train period at the two parities, taken once from
# sat_gun.train([f, b], dir=+1) and checked here to be a rigid orbit (check_st5.py, on the oracle).
PAT = [[frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2), (1, 0, 4)]),
        frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)])],
       [frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4)]),
        frozenset([(0, 0, 1), (0, 0, 3), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)])]]
WIRE = [frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]),
        frozenset([(0, 0, 1), (0, 0, 3), (0, 1, 2), (0, 1, 4), (1, 2, 2)])]


def train(t, ua, ub):
    """The plain train at generation t on units ua..ub-1: unit u holds PAT[t%2][(u - t//2) % 2]."""
    return frozenset(tr(c, u) for u in range(ua, ub) for c in PAT[t % 2][(u - t // 2) % 2])


def in_tube(c, C=10 ** 9):
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5 and c[0] + c[1] - c[2] <= C and c[0] - c[1] - c[2] <= C


class Tube:
    def __init__(self, U0, C=39):
        self.U0 = U0
        ub = (C + 5) // 4 + 3
        cells = []
        for x in range(2 * (U0 - 1), 2 * ub):
            for y in range(-4, 5):
                for z in range(-x - 12, -x + 12):
                    c = (x, y, z)
                    if is_cell(c) and in_tube(c, C):
                        cells.append(c)
        self.cells = sorted(cells); self.n = n = len(cells)
        self.idx = {c: i for i, c in enumerate(self.cells)}
        self.units = np.array([unit(c) for c in self.cells])
        assert self.units.max() < ub - 1
        nbr = np.full((n, 12), n, np.int64)
        for i, c in enumerate(self.cells):
            for k, q in enumerate(nb(c)):
                if q in self.idx:
                    nbr[i, k] = self.idx[q]
                else:
                    assert not in_tube(q, C) or unit(q) < U0 - 1, q
        self.nbr = nbr
        self.bnd = np.nonzero(self.units == U0 - 1)[0]
        self.chk = np.nonzero((self.units == U0) | (self.units == U0 + 1))[0]
        self._tr = {}

    def vec(self, cells):
        v = np.zeros(self.n + 1, np.uint8)
        for c in cells:
            if unit(c) >= self.U0 - 1:
                v[self.idx[c]] = 1
        return v

    def cells_of(self, v):
        return frozenset(self.cells[i] for i in np.nonzero(v[:self.n])[0])

    def train_vec(self, t):
        k = t % 4
        if k not in self._tr:
            self._tr[k] = self.vec(train(k, self.U0 - 1, max(self.units) + 1) & frozenset(self.cells))
        return self._tr[k]

    def step(self, S, t):
        """S: (E, n+1) uint8 at generation t -> generation t+1 (boundary unit refilled with the plain train)."""
        cnt = S[:, self.nbr].sum(axis=2, dtype=np.int8)
        x = S[:, :self.n]
        y = ((cnt == 4) | (cnt == 5) | ((cnt == 3) & (x == 1))).astype(np.uint8)
        out = np.zeros_like(S); out[:, :self.n] = y
        tv = self.train_vec(t + 1)
        out[:, self.bnd] = tv[self.bnd]
        return out

    def boundary_plain(self, S, t):
        tv = self.train_vec(t)
        return (S[:, self.chk] == tv[self.chk]).all(axis=1)


def box_masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def oracle_run(cells, gens, pad=8):
    """Step `cells` with oracle.step on an even box torus large enough (pad on every side); yields (t, cells)."""
    cs = list(cells)
    lo = [min(c[i] for c in cs) - pad for i in range(3)]
    lo = [v - (v % 2) for v in lo]
    hi = [max(c[i] for c in cs) + pad for i in range(3)]
    shape = tuple(((hi[i] - lo[i]) // 2 + 1) * 2 for i in range(3))
    m = box_masks(shape)
    h = np.zeros(shape, np.int8)
    for c in cs:
        h[c[0] - lo[0], c[1] - lo[1], c[2] - lo[2]] = 1
    for t in range(gens + 1):
        yield t, frozenset((int(a) + lo[0], int(b) + lo[1], int(c) + lo[2]) for a, b, c in np.argwhere(h))
        if t < gens:
            h = oracle.step(h, m)
