#!/usr/bin/env python3
"""a9 (review of signals push 9): the objects, the oracle on a torus in which nothing wraps, and this review's stepper.

Nothing of research/signals/ is imported.  From the push's JSON only initial cells are taken: the two caps, the
stators and sites of the family (objects/call9.json: capL, capR, stators, sites), the 162 cells of the call line
(runs[0].extra), the two cells of the CALL (runs[0].ops[3][2]) and, in trig9.py, the six cells of the still life.

Orc    reference/oracle.py's step, unchanged, on a rectangular array torus whose masks are oracle.masks' formula for
       the array's shape and an even origin.  After every generation the four outermost index planes on every side
       are asserted dead.  A cell's neighbours are at most 2 sites from it, so no neighbour count ever contains a
       wrapped live cell: the run is the run of the infinite lattice, and the nearest image of a live cell is always
       at least 8 sites away.  Orc.image_distance() computes the exact max-norm distance from the live cells to their
       nearest torus image.
St     st9.c, this review's sparse stepper (neighbour offsets from docs/AUTOMATON.md section 2, asserted equal to
       oracle.offsets below).  Trusted only where check_st9.py compares it with Orc.
"""
import os, sys, json, ctypes, subprocess, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

P9 = os.path.join(ROOT, 'research', 'signals', 'push9', 'objects')
_D = json.load(open(os.path.join(P9, 'call9.json')))
CAPL = frozenset(map(tuple, _D['capL']))
CAPR = frozenset(map(tuple, _D['capR']))
STATORS = [tuple(c) for c in _D['stators']]          # (0,1,2), (0,1,4)
SITES = [tuple(c) for c in _D['sites']]              # (1,0,0), (1,0,2), (1,0,4), (0,2,3)
LINE = frozenset(map(tuple, _D['runs'][0]['extra']))  # the call line at rest, even generation: 162 cells
CALL = [tuple(c) for c in _D['runs'][0]['ops'][3][2]]  # the two cells made live
CROSS = 4 + _D['runs'][0]['crossings'][0]            # the store unit the push calls the crossing: unit 35
assert len(LINE) == 162 and len(CALL) == 2 and STATORS == [(0, 1, 2), (0, 1, 4)]

add = lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2])
sub = lambda a, b: (a[0] - b[0], a[1] - b[1], a[2] - b[2])
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)   # k units along the store wire
mv = lambda cells, t: frozenset(add(c, t) for c in cells)
RST = lambda u: tr(STATORS[0], u)    # removing it at an even generation: a right-going pulse is born (R@u)
LST = lambda u: tr(STATORS[1], u)    # a left-going pulse (L@u)


def unit_cells(h, u):
    return {tr(c, u) for c in STATORS} | {tr(SITES[j], u) for j in range(4) if h >> j & 1}


def wire(word, first=4, caps=True, off=(0, 0, 0)):
    """capL + one unit per hex letter from unit `first` on + the right cap; the push's cell when first = 4"""
    cells = set()
    for i, ch in enumerate(word):
        cells |= unit_cells(int(ch, 16), first + i)
    if caps:
        cells |= {tr(c, first - 4) for c in CAPL} | {tr(c, first + len(word)) for c in CAPR}
    return frozenset(add(c, off) for c in cells)


def letters(cells, n, first=4, off=(0, 0, 0)):
    """the word of n units read from the cells in the wire's 5 x 5 tube; '?' where a unit is not a family unit"""
    cells = {sub(c, off) for c in cells}
    by = {}
    for c in cells:
        if -3 <= c[0] + c[1] + c[2] <= 9 and -3 <= c[0] - c[1] + c[2] <= 9:
            by.setdefault(c[0] >> 1, set()).add(c)
    out = []
    for i in range(n):
        u = first + i
        loc = {tr(c, -u) for c in by.get(u, ())}
        if not set(STATORS) <= loc or not loc - set(STATORS) <= set(SITES):
            out.append('?'); continue
        out.append('%x' % sum(1 << j for j in range(4) if SITES[j] in loc))
    return ''.join(out)


def rle(w):
    out = []
    for ch, g in itertools.groupby(w):
        n = len(list(g)); out.append(ch if n == 1 else f'{ch}^{n}' if n > 3 else ch * n)
    return ' '.join(out)


# ---------------------------------------------------------------- the oracle
class Orc:
    PAD = 12

    def __init__(self, cells, reach=(), pad=None):
        pad = self.PAD if pad is None else pad
        pts = np.array(list(cells) + list(reach), dtype=np.int64)
        lo = pts.min(0) - pad; hi = pts.max(0) + pad
        lo -= lo % 2                                    # even origin: parities are kept
        shape = hi - lo + 1; shape += shape % 2         # even sides: a proper torus
        self.org = tuple(int(v) for v in lo); self.shape = tuple(int(v) for v in shape)
        par = np.indices(self.shape) % 2
        self.m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]   # oracle.masks' formula
        self.valid = self.m[0] | self.m[1] | self.m[2]
        self.h = np.zeros(self.shape, np.int8)
        self.t = 0
        for c in cells:
            self._set(c, 1, must=0)
        self._guard()

    def _ix(self, c):
        i = (c[0] - self.org[0], c[1] - self.org[1], c[2] - self.org[2])
        assert all(4 <= i[a] < self.shape[a] - 4 for a in range(3)), ('outside the guarded box', c)
        assert self.valid[i], ('not a face', c)
        return i

    def _set(self, c, v, must=None):
        i = self._ix(c)
        if must is not None:
            assert self.h[i] == must, ('cell is not %s' % ('live' if must else 'dead'), c, self.t)
        self.h[i] = v

    def remove(self, c): self._set(tuple(c), 0, must=1)
    def make(self, c): self._set(tuple(c), 1, must=0)

    def flip(self, c):
        i = self._ix(tuple(c)); self.h[i] ^= 1

    def alive(self, c): return bool(self.h[self._ix(tuple(c))])

    def _guard(self):
        h = self.h
        assert not (h[:4].any() or h[-4:].any() or h[:, :4].any() or h[:, -4:].any() or h[:, :, :4].any() or h[:, :, -4:].any()), \
            ('a live cell within 4 sites of the seam', self.t)

    def step(self, n=1):
        for _ in range(n):
            self.h = oracle.step(self.h, self.m); self.t += 1
            self._guard()
        return self

    def cells(self):
        o = self.org
        return frozenset((int(a) + o[0], int(b) + o[1], int(c) + o[2]) for a, b, c in zip(*np.nonzero(self.h)))

    def count(self): return int(self.h.sum())

    def image_distance(self):
        """exact max-norm distance from the live cells to their nearest image under a nonzero torus translation"""
        p = np.argwhere(self.h).astype(np.int64)
        best = None
        for T in itertools.product((-1, 0, 1), repeat=3):
            if T == (0, 0, 0) or T < (0, 0, 0):
                continue
            q = p + np.array(T) * np.array(self.shape)
            # bounding boxes first: the distance of two sets is at least the distance of their boxes
            gap = np.maximum(q.min(0) - p.max(0), p.min(0) - q.max(0)).max()
            if best is not None and gap >= best:
                continue
            d = np.abs(p[:, None, :] - q[None, :, :]).max(2).min() if len(p) * len(p) <= 4_000_000 else gap
            best = int(d) if best is None else min(best, int(d))
        return best


def cubic_check(cells, gens):
    """the same run on oracle.masks(H) with a cubic H (the oracle exactly as its own main uses it) and on Orc"""
    pts = np.array(list(cells)); lo = pts.min(0) - 12; lo -= lo % 2
    H = int((pts.max(0) - lo + 13).max()); H += H % 2
    m = oracle.masks(H); h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] - lo[0], c[1] - lo[1], c[2] - lo[2]] = 1
    o = Orc(cells)
    for g in range(gens):
        h = oracle.step(h, m); o.step()
        cub = frozenset((int(a) + int(lo[0]), int(b) + int(lo[1]), int(c) + int(lo[2])) for a, b, c in zip(*np.nonzero(h)))
        if cub != o.cells():
            return False
    return True


# ---------------------------------------------------------------- this review's stepper
_SCR = os.path.join(ROOT, 'research', 'scratch', 'audit9')
os.makedirs(_SCR, exist_ok=True)
_SO = os.path.join(_SCR, 'st9.so')
if not os.path.exists(_SO) or os.path.getmtime(_SO) < os.path.getmtime(os.path.join(HERE, 'st9.c')):
    subprocess.check_call(['gcc', '-O2', '-shared', '-fPIC', '-o', _SO, os.path.join(HERE, 'st9.c')])
_L = ctypes.CDLL(_SO)
_L.st_run.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_L.st_run.restype = ctypes.c_int


def _own_offsets(a):
    b, c = (a + 1) % 3, (a + 2) % 3
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for w in (b, c):
            for s in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[w] = s; out.append(tuple(o))
    return out


for _a in range(3):
    assert sorted(_own_offsets(_a)) == sorted(oracle.offsets(_a)) and len(set(_own_offsets(_a))) == 12
NB = {a: _own_offsets(a) for a in range(3)}
axis = lambda c: 0 if c[0] & 1 else 1 if c[1] & 1 else 2
nbrs = lambda c: [add(c, o) for o in NB[axis(c)]]


def run(cells, gens, ring=0, cap=None):
    """`gens` generations of a set of cells with st9.c; returns a frozenset (None if the state outgrew `cap` cells)"""
    cells = list(cells); n = len(cells)
    cap = cap or max(4 * n + 4096, 20000)
    buf = np.zeros((cap, 3), np.int32)
    if n:
        buf[:n] = np.array(cells, np.int32)
    m = _L.st_run(buf.ctypes.data, n, cap, gens, ring)
    if m < 0:
        return None
    return frozenset(map(tuple, buf[:m].tolist()))


def step_set(cells):
    """a pure-python set stepper (third implementation, for checks)"""
    cnt = {}
    for c in cells:
        for q in nbrs(c):
            cnt[q] = cnt.get(q, 0) + 1
    return frozenset(q for q, n in cnt.items() if (n in (4, 5) and q not in cells) or (n in (3, 4, 5) and q in cells)) | \
        frozenset()


def orbit(cells, gens, ring=0):
    out = [frozenset(cells)]
    for _ in range(gens):
        out.append(run(out[-1], 1, ring))
    return out


# ---------------------------------------------------------------- the call line in its own frame
# Standard wire C (research/signals/README.md section 10), per unit along (2,0,-2), even generation.
WIREC = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]
PERMS = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def app(g, c, t=(0, 0, 0)):
    p, s = g
    return (s[0] * c[p[0]] + t[0], s[1] * c[p[1]] + t[1], s[2] * c[p[2]] + t[2])


def find_line_frame():
    """every (g, t) with g(unit j of standard wire C) + t in the line for 8 consecutive j: the line's own frame"""
    found = []
    for g in PERMS:
        img0 = app(g, WIREC[0])
        for target in LINE:
            t = sub(target, img0)
            if all(app(g, tr(c, j), t) in LINE for j in range(8) for c in WIREC):
                found.append((g, t))
    return found


def line_letters(cells, g, t, units):
    """the line's units read in its own frame (hex letters as for the store wire)"""
    p, s = g
    inv = {}
    for c in cells:
        d = sub(c, t); q = [0, 0, 0]
        for i in range(3):
            q[p[i]] = s[i] * d[i]
        inv[tuple(q)] = c
    out = []
    for u in units:
        loc = {tr(q, -u) for q in inv if q[0] >> 1 == u and -3 <= q[0] + q[1] + q[2] <= 9 and -3 <= q[0] - q[1] + q[2] <= 9}
        if not set(STATORS) <= loc or not loc - set(STATORS) <= set(SITES):
            out.append('?'); continue
        out.append('%x' % sum(1 << j for j in range(4) if SITES[j] in loc))
    return ''.join(out)


def image_distance_set(cells, shape):
    p = np.array(list(cells), np.int64); best = None
    for T in itertools.product((-1, 0, 1), repeat=3):
        if T <= (0, 0, 0):
            continue
        q = p + np.array(T) * np.array(shape)
        d = int(np.abs(p[:, None, :] - q[None, :, :]).max(2).min())
        best = d if best is None else min(best, d)
    return best


# ---------------------------------------------------------------- the line's frame, fixed (asserted)
LG = ((0, 2, 1), (1, -1, -1))        # standard wire C (x, y, z) -> (x, -z, -y) + LT: its axis (1,0,-1) -> (1,1,0)
LT = (28, -34, -72)                  # with this translation the line's 26 units of wire C are its units 0..25
LCROSS = 21                          # the line's unit at the crossing (21 units before it, 4 after)
assert all(app(LG, tr(c, j), LT) in LINE for j in range(26) for c in WIREC)
lstep = lambda cells, n: frozenset((c[0] + 2 * n, c[1] + 2 * n, c[2]) for c in cells)   # n units along the line
lcell = lambda q, u=0: app(LG, tr(q, u), LT)       # a cell of the standard frame, unit u of the line
assert [lcell((0, 0, 1), 6), lcell((2, -2, 1), 6)] == CALL   # the CALL: (0,0,1), (2,-2,1) of line unit 6, 15 before the crossing


def lletters(cells, units=range(26)):
    return line_letters(cells, LG, LT, units)


def lword(word, first):
    """the cells of a word of family units on the line (own frame), unit `first` on; and the plain cells they replace"""
    new = frozenset(lcell(q, 0) for i, ch in enumerate(word) for q in unit_cells(int(ch, 16), first + i))
    old = frozenset(lcell(q, 0) for i in range(len(word)) for q in unit_cells(0xb, first + i))
    return new, old


def with_lword(state, word, first):
    new, old = lword(word, first)
    assert old <= state
    return (state - old) | new


def play(start, ops, gens, engine='st', every=2, reach=(), keep=None):
    """ops: {generation: (cells removed, cells made live)}; removed cells must be live and made cells dead.
    Returns {generation: frozenset} for generations divisible by `every` (or in `keep`)."""
    out = {}
    if engine == 'orc':
        rc = list(reach) + [c for r, m in ops.values() for c in list(r) + list(m)]
        o = Orc(start, reach=rc)
        for g in range(gens + 1):
            if g in ops:
                for c in ops[g][0]: o.remove(c)
                for c in ops[g][1]: o.make(c)
            if g % every == 0 or (keep and g in keep):
                out[g] = o.cells()
            if g < gens:
                o.step()
        out['image_distance'] = o.image_distance(); out['shape'] = o.shape
        return out
    s = frozenset(start)
    for g in range(gens + 1):
        if g in ops:
            r, m = frozenset(ops[g][0]), frozenset(ops[g][1])
            assert r <= s and not (m & s), ('operation does not apply', g)
            s = (s - r) | m
        if g % every == 0 or (keep and g in keep):
            out[g] = s
        if g < gens:
            s = run(s, 1)
    return out


def long_line(n, at=23):
    """the line with n more units of wire C put in before its unit `at` (the cells from unit `at` on move n units)"""
    out = set()
    for c in LINE:
        u = (c[0] - LT[0]) >> 1
        out.add((c[0] + 2 * n, c[1] + 2 * n, c[2]) if u >= at else c)
    out |= {lcell(q, at + j) for j in range(n) for q in WIREC}
    assert len(out) == 162 + 5 * n
    return frozenset(out)
