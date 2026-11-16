"""Reviewer's helpers for the signals audit.  Imports nothing from research/signals; the judge is reference/oracle.py.

Cells are doubled-coordinate tuples.  Three ways to step:
  torus_run(cells, shape, T)  oracle.step on an even box torus (oracle.step is shape-agnostic; masks built here with
                              the same definition as oracle.masks and checked equal to it for cubic boxes)
  sstep(live)                 own sparse stepper on the infinite lattice (python sets), checked against the oracle
                              by selftest()
"""
import os, sys
from collections import Counter
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_signals')
os.makedirs(SCR, exist_ok=True)
OFFS = [oracle.offsets(a) for a in range(3)]
V = (1, 0, -1)


def axis(p):
    return 0 if p[0] & 1 else (1 if p[1] & 1 else 2)


def nbrs(p):
    return [(p[0] + o[0], p[1] + o[1], p[2] + o[2]) for o in OFFS[axis(p)]]


def sstep(live):
    cnt = Counter()
    for c in live:
        for q in nbrs(c):
            cnt[q] += 1
    return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))


def canon_ring(c, N, v=V):
    """representative of c modulo the ring translation N*v (cube index x//2 brought into [0, N))"""
    k = (c[0] // 2) // (N * v[0]) if v[0] > 0 else 0
    if k:
        c = (c[0] - 2 * k * N * v[0], c[1] - 2 * k * N * v[1], c[2] - 2 * k * N * v[2])
    return c


def sstep_ring(live, N, v=V):
    """Own sparse stepper on the lattice modulo N*v only (a ring of N cubes with no transverse images); v[0] = 1."""
    cnt = Counter()
    for c in live:
        for q in nbrs(c):
            cnt[canon_ring(q, N, v)] += 1
    return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))


def masks(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def shift(cells, k, v=V):
    return frozenset((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2]) for c in cells)


def wire(bg, k0, k1, v=V):
    """Cells of the wire repeated over cubes k0 .. k1-1 (infinite-lattice coordinates)."""
    out = set()
    for k in range(k0, k1):
        out |= shift(bg, k, v)
    return frozenset(out)


class Torus:
    def __init__(self, shape):
        assert all(s % 2 == 0 for s in shape)
        self.shape = tuple(shape)
        self.m = masks(self.shape) if len(set(shape)) > 1 else oracle.masks(shape[0])
        self.valid = self.m[0] | self.m[1] | self.m[2]

    def mod(self, c):
        return (c[0] % self.shape[0], c[1] % self.shape[1], c[2] % self.shape[2])

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            q = self.mod(c)
            assert self.valid[q], c
            h[q] ^= 1
        return h

    def step(self, h):
        return oracle.step(h, self.m)

    @staticmethod
    def cells(h):
        return frozenset(map(tuple, np.argwhere(h).tolist()))


def ring_torus(N, Hy=20):
    """Box torus on which a wire along (1,0,-1) closes into a ring of N cubes; its transverse images are 2N apart in
    x+z and Hy apart in y."""
    return Torus((2 * N, Hy, 2 * N))


def selftest(seed=1, trials=6):
    """Own sparse stepper == oracle on random finite blobs in a big enough box (T2: a finite pattern stays in its
    diagonal hull, so the box torus never wraps)."""
    rng = np.random.default_rng(seed)
    T = Torus((48, 48, 48))
    for _ in range(trials):
        cells = set()
        for x in range(18, 30):
            for y in range(18, 30):
                for z in range(18, 30):
                    if ((x & 1) + (y & 1) + (z & 1)) == 1 and rng.random() < 0.35:
                        cells.add((x, y, z))
        h = T.arr(cells); s = frozenset(cells)
        for _ in range(12):
            h = T.step(h); s = sstep(s)
            assert T.cells(h) == s
    assert all((oracle.masks(16)[a] == masks((16, 16, 16))[a]).all() for a in range(3))
    return True


if __name__ == '__main__':
    print('selftest', selftest())
