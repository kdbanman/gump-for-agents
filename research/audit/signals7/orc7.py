#!/usr/bin/env python3
"""Oracle harness for REVIEW-signals-7.  The only stepper is reference/oracle.py's `step` (unchanged, called on a
rectangular array with masks built as oracle.masks builds them).  No code from research/signals/.

Coordinates: doubled; unit(p) = p.x >> 1; one unit along v = (1,0,-1) is the translation (2,0,-2).  The 5 x 5 tube is
-1 <= x+y+z <= 7, -1 <= x-y+z <= 7 (38 cells per unit), the 3 x 3 tube 1 <= .. <= 5 (14 cells per unit).

Two kinds of torus:

  Tor.box(ua, ub)       an array large enough to hold units ua..ub-1 of the tube with a margin of 8 on every side and
                        no modular identification used: nothing wraps round.  `check_margin` asserts that the 4
                        outermost index planes on every side are dead, so the wrap of np.roll never carries a live cell.
  Tor.helix(L, ulo)     the array (16a, 16, 16b), gcd(a, b) = 1, L = 8ab: the tube closes on itself after L units (a ring
                        of L units, units ulo..ulo+L-1), winding a + b times round the array.  Exact for the ring of the
                        5 x 5 tube: every lattice shift of the array changes x+y+z and x-y+z by multiples of 16, the tube
                        holds the layers -1..7 of both, so the layers 9, 11, 13 (mod 16) of both are dead and by T3 stay
                        dead for ever and isolate the windings.  `outside` counts live cells off the mapped tube sites
                        (asserted 0 by callers).  Checked equal to the box, cell for cell, by `check_helix.py`.

A state is read back as a uint8 array [units, 38] (`units`), indexable by unit - ua.
"""
import os, sys, json
from math import gcd
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

PUSH = os.path.join(ROOT, 'research', 'signals', 'push7')
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals7')
os.makedirs(SCR, exist_ok=True)


def is_cell(p):
    return (p[0] & 1) + (p[1] & 1) + (p[2] & 1) == 1


def unit(p):
    return p[0] >> 1


def tr(p, u):
    return (p[0] + 2 * u, p[1], p[2] - 2 * u)


def in_tube(p, lo=-1, hi=7):
    return lo <= p[0] + p[1] + p[2] <= hi and lo <= p[0] - p[1] + p[2] <= hi


def tube_base(lo=-1, hi=7):
    out = []
    for x in (0, 1):
        for y in range(-8, 9):
            for z in range(-20, 21):
                p = (x, y, z)
                if is_cell(p) and in_tube(p, lo, hi):
                    out.append(p)
    return sorted(out)


BASE = tube_base()
NC = len(BASE)
INDEX = {c: i for i, c in enumerate(BASE)}
IN3 = np.array([in_tube(c, 1, 5) for c in BASE])
assert NC == 38 and int(IN3.sum()) == 14


def masks(shape, origin):
    """As oracle.masks, for a rectangular array whose index (i, j, k) is the cell origin + (i, j, k)."""
    idx = np.indices(shape)
    par = np.stack([(idx[a] + origin[a]) % 2 for a in range(3)])
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


HELIX = {}
for _a in range(1, 40):
    for _b in range(_a + 1, 40):
        if gcd(_a, _b) == 1:
            _L = 8 * _a * _b
            if _L not in HELIX or (_b - _a) < (HELIX[_L][1] - HELIX[_L][0]):
                HELIX[_L] = (_a, _b)


def helix_len(Lmin):
    """Smallest available ring length >= Lmin (even, so the train closes)."""
    return min(L for L in HELIX if L >= Lmin)


class Tor:
    def __init__(self, shape, origin, ua, ub, ring):
        self.shape, self.origin, self.ua, self.ub, self.ring = tuple(shape), tuple(origin), ua, ub, ring
        assert all(s % 2 == 0 for s in shape) and all(o % 2 == 0 for o in origin)
        self.m = masks(self.shape, (0, 0, 0))          # origin even: parities are those of the index
        nu = ub - ua
        ix = np.zeros((nu, NC), np.int64); iy = ix.copy(); iz = ix.copy()
        for k in range(nu):
            for i, c in enumerate(BASE):
                p = tr(c, ua + k)
                ix[k, i], iy[k, i], iz[k, i] = self.site(p, strict=not ring)
        flat = (ix * shape[1] + iy) * shape[2] + iz
        assert len(np.unique(flat)) == flat.size, 'tube sites collide'
        self.ix, self.iy, self.iz = ix, iy, iz

    @classmethod
    def box(cls, ua, ub, pad=8):
        # x in [2ua, 2ub), y in [-4, 4], z in [-2ub - 1, -2ua + 9)
        ox = 2 * ua - pad; oy = -4 - pad; oz = -2 * ub - 2 - pad
        ox -= ox % 2; oy -= oy % 2; oz -= oz % 2
        sx = 2 * (ub - ua) + 2 * pad + 2; sy = 8 + 2 * pad + 2; sz = 2 * (ub - ua) + 12 + 2 * pad
        sx += sx % 2; sy += sy % 2; sz += sz % 2
        return cls((sx, sy, sz), (ox, oy, oz), ua, ub, False)

    @classmethod
    def helix(cls, L, ulo):
        a, b = HELIX[L]
        return cls((16 * a, 16, 16 * b), (0, 0, 0), ulo, ulo + L, True)

    def site(self, p, strict=False):
        s = tuple(p[a] - self.origin[a] for a in range(3))
        if strict:
            assert all(0 <= s[a] < self.shape[a] for a in range(3)), (p, s)
        return tuple(s[a] % self.shape[a] for a in range(3))

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            c = tuple(c); assert is_cell(c), c
            if self.ring:
                assert in_tube(c), c
            h[self.site(c, strict=not self.ring)] = 1
        return h

    def flip(self, h, cells):
        for c in cells:
            c = tuple(c); assert is_cell(c) and in_tube(c), c
            h[self.site(c, strict=not self.ring)] ^= 1

    def step(self, h, n=1):
        for _ in range(n):
            h = oracle.step(h, self.m)
        return h

    def units(self, h):
        return h[self.ix, self.iy, self.iz].astype(np.uint8)

    def outside(self, h):
        return int(h.sum()) - int(h[self.ix, self.iy, self.iz].sum())

    def check_margin(self, h, w=4):
        assert not self.ring
        for a in range(3):
            lo = [slice(None)] * 3; hi = [slice(None)] * 3
            lo[a] = slice(0, w); hi[a] = slice(self.shape[a] - w, None)
            assert not h[tuple(lo)].any() and not h[tuple(hi)].any(), 'live cell in the margin'

    def cells(self, h):
        """Live cells as true coordinates (tube sites only; callers assert outside == 0)."""
        U = self.units(h)
        return frozenset(tr(BASE[i], int(k) + self.ua) for k, i in zip(*np.nonzero(U)))


def ucells(U, ua):
    """[units, NC] array -> frozenset of cells, unit index 0 = unit ua."""
    return frozenset(tr(BASE[i], int(k) + ua) for k, i in zip(*np.nonzero(U)))


def uarr(cells, ua, ub):
    a = np.zeros((ub - ua, NC), np.uint8)
    for c in cells:
        u = unit(c)
        a[u - ua, INDEX[tr(tuple(c), -u)]] = 1
    return a


# ---- initial data taken from the push's files (cells only) ------------------------------------------------------
_obj = None


def objects():
    global _obj
    if _obj is None:
        _obj = json.load(open(os.path.join(PUSH, 'objects7.json')))
    return _obj


def bases():
    """Train base cells at generation 0: bases[frame][parity] relative to the unit (frame 'fb': the train moving +v
    into a receiving end; '5f': moving -v away from a gun)."""
    return {k: [[tuple(c) for c in par] for par in v] for k, v in objects()['bases'].items()}


def train0(frame, ua, ub):
    B = bases()[frame]
    return frozenset(tr(c, u) for u in range(ua, ub) for c in B[u % 2])


def record(name):
    return next(r for r in objects()['records'] if r['name'] == name)
