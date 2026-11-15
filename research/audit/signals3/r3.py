"""Third-push signals review: shared pieces.  Imports no study code (research/signals/*); reads only the study's
object files (cell lists).  Stepping: gs.Dom from the second review (oracle-checked, `python3 ../signals2/gs.py`)
on the diagonal hull of the starting pattern (exact on the infinite lattice by T2), or reference/oracle.py itself
on a box torus with every generation checked to have no live cell outside that hull (then the box is never felt).

Units: unit u = cells with x in {2u, 2u+1}; tr(c, k) moves by k units along v = (1,0,-1).  Unit types are hex
digits of a subset of the four sites 0 (1,0,0), 1 (1,0,2), 2 (1,0,4), 3 (0,2,3) on top of the stators (0,1,2),
(0,1,4): C = b, B = 7, rake f, wire 8 = 8; the mirror rake is '5f' ('5' at unit u, 'f' at u+1).
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'signals2'))
import gs  # noqa: E402
oracle = gs.oracle
tr, unit = gs.tr, gs.unit
OBJ = os.path.join(gs.ROOT, 'research', 'signals', 'objects')
STAT = [(0, 1, 2), (0, 1, 4)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
HEX = {'B': 0x7, 'C': 0xb}
MIRROR = lambda c: (c[2] - 4, c[1], c[0] + 4)
_ck = json.load(open(os.path.join(OBJ, 'clock-C.json')))
capL = frozenset(map(tuple, _ck['capL'])); capR0 = frozenset(map(tuple, _ck['capR']))   # capR0: first unit 0


def uc(m, u):
    if isinstance(m, str):
        m = HEX[m]
    return {tr(c, u) for c in STAT} | {tr(SITES[i], u) for i in range(4) if m >> i & 1}


def word_cells(w, u0=0):
    s = set()
    for i, ch in enumerate(w):
        s |= uc(int(ch, 16) if ch not in 'BC' else HEX[ch], u0 + i)
    return s


def dec(S, a, b):
    by = {}
    for c in S:
        by.setdefault(unit(c), set()).add(tr(c, -unit(c)))
    o = ''
    for u in range(a, b):
        s = by.get(u, set())
        if not s:
            o += '.'
        elif set(STAT) <= s and s <= set(STAT) | set(SITES):
            o += '%x' % sum(1 << i for i in range(4) if SITES[i] in s)
        else:
            o += '?'
    return o


DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]


def hull_bounds(cells):
    return [(d, min(sum(a * b for a, b in zip(d, c)) for c in cells), max(sum(a * b for a, b in zip(d, c)) for c in cells)) for d in DIAG]


def in_hull(b):
    return lambda p: all(lo <= d[0] * p[0] + d[1] * p[1] + d[2] * p[2] <= hi for d, lo, hi in b)


class Run:
    """Exact stepping of a finite pattern on the infinite lattice (gs.Dom on the pattern's diagonal hull)."""
    def __init__(self, cells, extra=()):
        allc = set(cells) | set(extra)
        b = hull_bounds(allc)
        self.D = gs.Dom(gs.closure(allc, in_hull(b)))
        self.x = self.D.state(cells); self.t = 0

    def step(self, g=1):
        for _ in range(g):
            self.x = self.D.step(self.x); self.t += 1
        return self

    def cells(self):
        return self.D.cells_of(self.x)


def oracle_run(cells, T, every=1, pad=14):
    """reference/oracle.py on a box torus, hull-checked; yields (t, cells) every `every` generations."""
    b = hull_bounds(cells)
    lo = [min(c[i] for c in cells) - pad for i in range(3)]; hi = [max(c[i] for c in cells) + pad for i in range(3)]
    shape = tuple(((hi[i] - lo[i] + 1) + 1) // 2 * 2 for i in range(3)); off = tuple(-lo[i] + (0 if lo[i] % 2 == 0 else 1) for i in range(3))
    off = tuple(-lo[i] if lo[i] % 2 == 0 else -lo[i] + 1 for i in range(3))
    shape = tuple(hi[i] - lo[i] + 4 + ((hi[i] - lo[i]) % 2) for i in range(3))
    m = gs.box_masks(shape); idx = np.indices(shape); hull = np.ones(shape, bool)
    for d, l, h in b:
        s = sum(d[i] * (idx[i] - off[i]) for i in range(3)); hull &= (s >= l) & (s <= h)
    h = gs.to_arr(cells, shape, off)
    assert int(h.sum()) == len(set(cells))
    yield 0, frozenset(cells)
    for t in range(1, T + 1):
        h = oracle.step(h, m)
        assert not (h.astype(bool) & ~hull).any(), 'left the hull'
        if t % every == 0:
            yield t, gs.from_arr(h, off)
