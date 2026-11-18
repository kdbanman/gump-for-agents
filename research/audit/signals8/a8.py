#!/usr/bin/env python3
"""a8: tools of REVIEW-signals-8.  No code from research/signals/ is imported; from the push only initial cells
are read (objects/cell8.json: capL, capR, stators, sites; objects/caps.json: push 7's right cap).

Coordinates: doubled (x, y, z), exactly one odd.  unit(c) = x >> 1; tr(c, k) = (x + 2k, y, z - 2k) moves a cell k
units along v = (1,0,-1).  Family unit h (hex digit): the two stators and the sites i with bit i of h set.
7 = wire B, d = wire B', b = wire C (in wire B: a left-going pulse), f = all four sites.

Two steppers:
  Orc(ulo, uhi)   reference/oracle.py's `step`, unchanged, on a rectangular array that holds units ulo..uhi-1 with y in
                  [ylo, yhi) and w = x + z in [wlo, whi) and NO modular identification in use: `Orc.margin_dead`
                  asserts that the 4 outermost index planes on every side are dead, so np.roll never carries a live
                  cell round.  Masks by oracle.masks' formula with the array's origin.
  Box(ulo, uhi)   st8.c on the same region in sheared coordinates (x, y, x + z), dead outside; `touch` is set if a live
                  cell ever lies in the outermost layer.  Trusted only where check_st8.py compares it with Orc.
"""
import os, sys, json, ctypes, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

PUSH = os.path.join(ROOT, 'research', 'signals', 'push8')
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals8')
os.makedirs(SCR, exist_ok=True)

_D = json.load(open(os.path.join(PUSH, 'objects', 'cell8.json')))
CAPL = frozenset(map(tuple, _D['capL']))            # units 0..3; wire from unit 4
CAPR = frozenset(map(tuple, _D['capR']))            # the cell's right cap, first unit 0
ST = [tuple(c) for c in _D['stators']]              # (0,1,2), (0,1,4)
SITES = [tuple(c) for c in _D['sites']]             # (1,0,0), (1,0,2), (1,0,4), (0,2,3)
CAPR7 = frozenset(map(tuple, json.load(open(os.path.join(PUSH, 'objects', 'caps.json')))['capR']))   # push 7's right cap
RUNS = _D['runs']
SR, SL = (0, 1, 2), (0, 1, 4)                        # stator removed at an even generation: pulse towards +v / -v


def is_cell(c):
    return (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1


def unit(c):
    return c[0] >> 1


def tr(c, k):
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def fam(h):
    return ST + [SITES[i] for i in range(4) if h >> i & 1]


def word_cells(word, u0):
    out = set()
    for i, ch in enumerate(word):
        if ch != '_':
            out |= {tr(c, u0 + i) for c in fam(int(ch, 16))}
    return out


def cell_state(word, rcap=None):
    """capL + the family units of `word` from unit 4 + the right cap at unit 4 + len(word)"""
    rcap = CAPR if rcap is None else rcap
    return frozenset(CAPL | word_cells(word, 4) | {tr(c, 4 + len(word)) for c in rcap})


def wire_state(word, u0=0):
    """a bare word, no caps (for runs whose ends are never compared)"""
    return frozenset(word_cells(word, u0))


def letters_of(cells, u0, u1):
    """hex letters of units u0..u1-1 of a set of cells ('?' = not stators + sites, '_' = empty)"""
    by = {}
    for c in cells:
        by.setdefault(unit(c), set()).add(tr(c, -unit(c)))
    out = []
    for u in range(u0, u1):
        s = by.get(u, set())
        if not s:
            out.append('_'); continue
        rest = s - set(ST)
        if len(s) - len(rest) != 2 or not rest <= set(SITES):
            out.append('?'); continue
        out.append('%x' % sum(1 << i for i in range(4) if SITES[i] in rest))
    return ''.join(out)


def rle(s):
    out = []; i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out.append(s[i] + ('^%d' % (j - i) if j - i > 3 else s[i] * (j - i - 1))); i = j
    return ''.join(out)


# ---- the rule's geometry, from docs/AUTOMATON.md section 2 (doubled offsets), asserted equal to the oracle's ----
def nb_offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


for _a in range(3):
    assert sorted(nb_offsets(_a)) == sorted(oracle.offsets(_a)) and len(set(nb_offsets(_a))) == 12


class Orc:
    """the oracle on a rectangular array, nothing wrapping (see the module docstring)"""

    def __init__(self, ulo, uhi, ylo=-8, yhi=10, wlo=-8, whi=16, pad=4):
        self.ulo, self.uhi = ulo, uhi
        self.o = (2 * ulo - pad, ylo - pad, wlo - 2 * uhi - pad)            # origin (all even)
        self.shape = (2 * (uhi - ulo) + 2 * pad, yhi - ylo + 2 * pad, (whi - wlo) + 2 * (uhi - ulo) + 2 * pad)
        assert all(v % 2 == 0 for v in self.o)
        idx = np.indices(self.shape)
        par = np.stack([(idx[a] + self.o[a]) % 2 for a in range(3)])
        self.m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]
        self.valid = self.m[0] | self.m[1] | self.m[2]

    def idx(self, c):
        i = (c[0] - self.o[0], c[1] - self.o[1], c[2] - self.o[2])
        assert all(4 <= i[a] < self.shape[a] - 4 for a in range(3)), ('outside', c)
        assert self.valid[i], c
        return i

    def arr(self, cells=()):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            h[self.idx(tuple(c))] = 1
        return h

    def flip(self, h, cells):
        for c in cells:
            h[self.idx(tuple(c))] ^= 1

    def kill(self, h, c):
        i = self.idx(tuple(c)); assert h[i] == 1, ('not live', c); h[i] = 0

    def margin_dead(self, h):
        return not (h[:4].any() or h[-4:].any() or h[:, :4].any() or h[:, -4:].any() or h[:, :, :4].any() or h[:, :, -4:].any())

    def run(self, h, n=1):
        for _ in range(n):
            h = oracle.step(h, self.m)
            assert self.margin_dead(h), 'a live cell reached the margin: the array is too small for this run'
        return h

    def cells(self, h):
        i, j, k = np.nonzero(h)
        return frozenset(zip((i + self.o[0]).tolist(), (j + self.o[1]).tolist(), (k + self.o[2]).tolist()))


_lib = None


def lib():
    global _lib
    if _lib is None:
        src = os.path.join(HERE, 'st8.c'); so = os.path.join(SCR, 'st8.so')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-o', so, src])
        _lib = ctypes.CDLL(so)
        _lib.st8_run.argtypes = [ctypes.c_void_p, ctypes.c_void_p] + [ctypes.c_int] * 4 + [ctypes.c_void_p, ctypes.c_void_p]
        _lib.st8_run.restype = ctypes.c_int
    return _lib


_OFF = np.array([[(o[0], o[1], o[0] + o[2]) for o in nb_offsets(a)] for a in range(3)], dtype=np.int32)   # (dx, dy, dw)


class Box:
    """st8.c on units ulo..uhi-1, y in [ylo, yhi), w = x + z in [wlo, whi); dead outside"""

    def __init__(self, ulo, uhi, ylo=-8, yhi=10, wlo=-8, whi=16):
        assert ylo % 2 == 0 and yhi % 2 == 0 and wlo % 2 == 0 and whi % 2 == 0
        self.ulo, self.uhi, self.ylo, self.yhi, self.wlo, self.whi = ulo, uhi, ylo, yhi, wlo, whi
        self.NX, self.NY, self.NW = 2 * (uhi - ulo), yhi - ylo, whi - wlo
        self.shape = (self.NX + 4, self.NY + 4, self.NW + 4)
        self.tmp = np.zeros(self.shape, np.uint8)
        self.touch = False
        lib()

    def idx(self, c):
        i, j, k = c[0] - 2 * self.ulo, c[1] - self.ylo, c[0] + c[2] - self.wlo
        if not (0 <= i < self.NX and 0 <= j < self.NY and 0 <= k < self.NW):
            raise ValueError(f'cell {c} outside the box')
        return (i + 2, j + 2, k + 2)

    def arr(self, cells=()):
        a = np.zeros(self.shape, np.uint8)
        for c in cells:
            assert is_cell(c), c
            a[self.idx(tuple(c))] = 1
        return a

    def flip(self, a, cells):
        for c in cells:
            assert is_cell(c), c
            a[self.idx(tuple(c))] ^= 1

    def kill(self, a, c):
        i = self.idx(tuple(c)); assert a[i] == 1, ('not live', c); a[i] = 0

    def live(self, a, c):
        return bool(a[self.idx(tuple(c))])

    def run(self, a, n=1):
        assert a.dtype == np.uint8 and a.flags['C_CONTIGUOUS'] and a.shape == self.shape
        t = ctypes.c_int(0)
        lib().st8_run(a.ctypes.data, self.tmp.ctypes.data, self.NX, self.NY, self.NW, n, _OFF.ctypes.data, ctypes.byref(t))
        if t.value:
            self.touch = True
        return a

    def cells(self, a):
        i, j, k = np.nonzero(a[2:-2, 2:-2, 2:-2])
        x = i + 2 * self.ulo; y = j + self.ylo; w = k + self.wlo
        return frozenset(zip(x.tolist(), y.tolist(), (w - x).tolist()))

    def units(self, a, u0, u1):
        return a[2 + 2 * (u0 - self.ulo): 2 + 2 * (u1 - self.ulo)]

    def letters(self, a, u0, u1):
        return letters_of(self._cells_units(a, u0, u1), u0, u1)

    def _cells_units(self, a, u0, u1):
        sub = a[2 + 2 * (u0 - self.ulo): 2 + 2 * (u1 - self.ulo), 2:-2, 2:-2]
        i, j, k = np.nonzero(sub)
        x = i + 2 * u0; y = j + self.ylo; w = k + self.wlo
        return frozenset(zip(x.tolist(), y.tolist(), (w - x).tolist()))


def step_set(cells, n=1):
    """n generations of a finite set on the infinite lattice (pure Python; a third stepper for cross-checks)"""
    OFF = [nb_offsets(a) for a in range(3)]
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
