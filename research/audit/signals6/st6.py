"""Steppers for REVIEW-signals-6, written from the cube-index table of docs/AUTOMATON.md section 2 (no code from
research/signals/ or research/audit/signals5/).  Doubled coordinates; frame of the push (objects/line-C.json):
unit u = cells moved by u*(2,0,-2); unit_of(c) = c[0] >> 1.

  nbrs(c)             the 12 neighbours, derived from the cube-index table (X[i,j,k] = doubled 2(i,j,k)+e_x, ...)
  step(live)          sparse step on the infinite lattice
  Batch(cells)        numpy batch stepper on a fixed finite cell set (cells outside are dead for ever: callers pick
                      sets closed by T2, e.g. the 3x3 tube 1 <= x+y+z, x-y+z <= 5, and a long enough unit range)
  oracle_torus(...)   reference/oracle.py's step on an even torus (the judge)
"""
import os, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

# cube-index table, X -> Y -> Z cyclic.  For axis a with (b, c) the next two cyclically:
#   A[i,j,k]: A[i, j±1, k±1] (in b, c indices), B at (0,0,0),(0,-1,0)... written in the a-frame as in the doc
def _offsets_cube(a):
    # (da, db, dc) cube offsets for the doc's X-row; then rotate to axis a.
    same = [(0, 1, 1), (0, 1, -1), (0, -1, 1), (0, -1, -1)]
    nb_b = [(0, 0, 0), (0, -1, 0), (1, 0, 0), (1, -1, 0)]      # Y[i,j,k] Y[i,j-1,k] Y[i+1,j,k] Y[i+1,j-1,k]
    nb_c = [(0, 0, 0), (0, 0, -1), (1, 0, 0), (1, 0, -1)]      # Z[i,j,k] Z[i,j,k-1] Z[i+1,j,k] Z[i+1,j,k-1]
    # the doc's X row lists Y with j-shifts and Z with k-shifts; and the Y row / Z row are its cyclic rotations,
    # which is consistent only if X's Y-neighbours are indexed (i, j, k) with the shift on j (Y's own normal) etc.
    out = []
    b, c = (a + 1) % 3, (a + 2) % 3
    def rot(o):  # o in the (a, b, c) frame -> (x, y, z)
        r = [0, 0, 0]; r[a] = o[0]; r[b] = o[1]; r[c] = o[2]; return tuple(r)
    for o in same:
        out.append((a, rot(o)))
    for o in nb_b:
        out.append((b, rot(o)))
    for o in nb_c:
        out.append((c, rot(o)))
    return out


def _doubled(axis, ijk):
    p = [2 * v for v in ijk]; p[axis] += 1; return tuple(p)


def _offsets_doubled(a):
    base = _doubled(a, (0, 0, 0))
    return [tuple(q - p for q, p in zip(_doubled(ax, o), base)) for ax, o in _offsets_cube(a)]


OFF = [_offsets_doubled(a) for a in range(3)]
assert all(len(set(o)) == 12 for o in OFF)
# cross-check with the doubled-offset description of the doc (4 corner-coplanar, 8 edge-perpendicular)
for a in range(3):
    b, c = [i for i in range(3) if i != a]
    want = set()
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; want.add(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for s in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = s; want.add(tuple(o))
    assert set(OFF[a]) == want, a


def axis_of(c):
    return 0 if c[0] & 1 else (1 if c[1] & 1 else 2)


def is_cell(c):
    return (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1


def nbrs(c):
    return [(c[0] + o[0], c[1] + o[1], c[2] + o[2]) for o in OFF[axis_of(c)]]


def step(live):
    n = Counter()
    for c in live:
        for q in nbrs(c):
            n[q] += 1
    return frozenset(q for q, k in n.items() if k in (4, 5) or (k == 3 and q in live))


def run(s, g):
    for _ in range(g):
        s = step(s)
    return s


def unit_of(c):
    return c[0] >> 1


def tr(c, k):
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def trs(s, k):
    return frozenset(tr(c, k) for c in s)


def units(s, ua, ub):
    return frozenset(c for c in s if ua <= unit_of(c) < ub)


def in_tube(c):
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5


def tube_unit(u):
    out = []
    for x in (0, 1):
        for y in range(-8, 9):
            for z in range(-10, 11):
                c = (x, y, z)
                if is_cell(c) and in_tube(c):
                    out.append(tr(c, u))
    return sorted(out)


class Batch:
    """Batch stepper on a fixed cell list; cells outside the list are dead for ever (index n)."""
    def __init__(self, cells):
        self.cells = sorted(set(cells)); n = self.n = len(self.cells)
        self.idx = {c: i for i, c in enumerate(self.cells)}
        self.nbr = np.array([[self.idx.get(q, n) for q in nbrs(c)] for c in self.cells], np.int64)
        self.unit = np.array([unit_of(c) for c in self.cells])

    def vec(self, s):
        v = np.zeros(self.n + 1, np.uint8)
        for c in s:
            v[self.idx[c]] = 1
        return v

    def set_of(self, v):
        return frozenset(self.cells[i] for i in np.nonzero(v[:self.n])[0])

    def step(self, S):
        k = S[:, self.nbr].sum(axis=2, dtype=np.uint8)
        x = S[:, :self.n]
        out = np.zeros_like(S)
        out[:, :self.n] = (k == 4) | (k == 5) | ((k == 3) & (x == 1))
        return out


def box_masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def oracle_torus(cells, gens, shape, origin=(0, 0, 0)):
    """Yield (t, cells) for t = 0..gens, stepping with oracle.step on an even box torus of `shape` whose index
    (0,0,0) is doubled coordinate `origin` (cells are wrapped into the box)."""
    assert all(s % 2 == 0 for s in shape) and all(o % 2 == 0 for o in origin)
    m = box_masks(shape)
    h = np.zeros(shape, np.int8)
    for c in cells:
        h[(c[0] - origin[0]) % shape[0], (c[1] - origin[1]) % shape[1], (c[2] - origin[2]) % shape[2]] = 1
    for t in range(gens + 1):
        yield t, frozenset((int(a) + origin[0], int(b) + origin[1], int(c) + origin[2]) for a, b, c in np.argwhere(h))
        if t < gens:
            h = oracle.step(h, m)
