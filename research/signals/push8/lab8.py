#!/usr/bin/env python3
"""lab8 (push 8): a small stepper for gump on a box in sheared coordinates, and helpers for wires along (1,0,-1).

    L = Lab(ua, ub, ylo=-6, yhi=10, wlo=-6, whi=14, ring=False)   units ua..ub-1 (x in [2ua, 2ub)), y in [ylo, yhi),
                                                                  w = x + z in [wlo, whi); all bounds even
    a = L.arr(cells); L.run(a, n); L.cells(a)                     cells are doubled coordinates (x, y, z)
    L.touch                                                       True if a live cell ever reached the box's outer layer

Cells outside the box are dead.  With ring=True the box is a ring of ub - ua units (the move by (2,0,-2) per unit).
Checked bit for bit against reference/oracle.py by check8.py (the push-7 line, whole state, every generation).
The stepper is lab8.c, compiled on first use into research/scratch/signals/p8/lab8.so.
"""
import os, sys, ctypes, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.normpath(os.path.join(HERE, '..', '..', 'scratch', 'signals', 'p8'))
_lib = None


def lib():
    global _lib
    if _lib is None:
        os.makedirs(SCR, exist_ok=True)
        src = os.path.join(HERE, 'lab8.c'); so = os.path.join(SCR, 'lab8.so')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-o', so, src])
        _lib = ctypes.CDLL(so)
        _lib.run.argtypes = [ctypes.c_void_p, ctypes.c_void_p] + [ctypes.c_int] * 5 + [ctypes.c_void_p]
        _lib.run.restype = ctypes.c_int
    return _lib


def unit(c):
    return c[0] >> 1


def tr(c, k):
    """the cell moved k units towards +v = (1,0,-1)"""
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def is_cell(c):
    return (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1


class Lab:
    def __init__(self, ua, ub, ylo=-6, yhi=10, wlo=-6, whi=14, ring=False):
        assert ylo % 2 == 0 and yhi % 2 == 0 and wlo % 2 == 0 and whi % 2 == 0
        self.ua, self.ub, self.ylo, self.yhi, self.wlo, self.whi, self.ring = ua, ub, ylo, yhi, wlo, whi, ring
        self.NX, self.NY, self.NW = 2 * (ub - ua), yhi - ylo, whi - wlo
        self.shape = (self.NX + 4, self.NY + 4, self.NW + 4)
        self.scratch = np.zeros(self.shape, np.uint8)
        self.touch = False
        lib()

    def idx(self, c):
        x, y, z = c
        i, j, k = x - 2 * self.ua, y - self.ylo, x + z - self.wlo
        if self.ring:
            i %= self.NX
        if not (0 <= i < self.NX and 0 <= j < self.NY and 0 <= k < self.NW):
            raise ValueError(f'cell {c} outside the box')
        return (i + 2, j + 2, k + 2)

    def arr(self, cells=()):
        a = np.zeros(self.shape, np.uint8)
        for c in cells:
            assert is_cell(c), c
            a[self.idx(c)] = 1
        return a

    def flip(self, a, cells):
        for c in cells:
            assert is_cell(c), c
            a[self.idx(c)] ^= 1

    def cells(self, a):
        i, j, k = np.nonzero(a[2:-2, 2:-2, 2:-2])
        x = i + 2 * self.ua; y = j + self.ylo; w = k + self.wlo
        return frozenset(zip(x.tolist(), y.tolist(), (w - x).tolist()))

    def run(self, a, n=1):
        assert a.dtype == np.uint8 and a.flags['C_CONTIGUOUS'] and a.shape == self.shape
        t = ctypes.c_int(0)
        lib().run(a.ctypes.data, self.scratch.ctypes.data, self.NX, self.NY, self.NW, n, 1 if self.ring else 0, ctypes.byref(t))
        if t.value:
            self.touch = True
        return a

    def units(self, a, u0, u1):
        """view of the interior on units u0..u1-1 (no ring wrap)"""
        return a[2 + 2 * (u0 - self.ua): 2 + 2 * (u1 - self.ua), 2:-2, 2:-2]

    def unit_cells(self, a, u):
        """cells of unit u, moved to unit 0"""
        b = self.units(a, u, u + 1)
        i, j, k = np.nonzero(b)
        return frozenset((int(i_), int(j_) + self.ylo, int(k_) + self.wlo - int(i_)) for i_, j_, k_ in zip(i, j, k))


def step_set(cells, n=1):
    """n generations of a finite set of cells on the infinite lattice (pure Python; slow; for cross-checks)."""
    import itertools
    OFF = {}
    for a in range(3):
        b, c = [i for i in range(3) if i != a]
        o = []
        for sb, sc in itertools.product((2, -2), repeat=2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; o.append(tuple(v))
        for sa in (1, -1):
            for t in (b, c):
                for st in (1, -1):
                    v = [0, 0, 0]; v[a] = sa; v[t] = st; o.append(tuple(v))
        OFF[a] = o
    cells = set(cells)
    for _ in range(n):
        cnt = {}
        for c in cells:
            a = 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
            for o in OFF[a]:
                q = (c[0] + o[0], c[1] + o[1], c[2] + o[2])
                cnt[q] = cnt.get(q, 0) + 1
        cells = {q for q, k in cnt.items() if k in (4, 5) or (k == 3 and q in cells)}
    return frozenset(cells)
