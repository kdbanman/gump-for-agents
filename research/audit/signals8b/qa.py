"""Audit of signals push 8b: the audit's own lab.

Two steppers, neither of them the push's:
  * reference/oracle.py on an array torus (class Box): the judge.  Every live cell is kept more than 4 sites from the
    seam (asserted each generation), so a run is exact for empty space.
  * q.c, a sparse stepper on the infinite lattice (run, orbit), checked against the oracle by check_q.py.
States for q.c are sorted numpy int64 arrays of packed keys (pk / up).  Cells are doubled-coordinate tuples.
Nothing here imports the push's code.  Objects are read from JSON only.
"""
import ctypes, itertools, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SIG = os.path.join(ROOT, 'research', 'signals')
P8B = os.path.join(SIG, 'push8b')
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit8b')
os.makedirs(SCR, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

BIAS = 1 << 19
M20 = (1 << 20) - 1
_lib = None


def lib():
    global _lib
    if _lib is None:
        so, src = os.path.join(HERE, 'q.so'), os.path.join(HERE, 'q.c')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O2', '-shared', '-fPIC', '-o', so, src])
        _lib = ctypes.CDLL(so)
        _lib.q_run.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        _lib.q_run.restype = ctypes.c_int
    return _lib


def is_cell(c):
    return (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1


def pk(cells):
    cells = list(cells)
    if not cells:
        return np.zeros(0, np.int64)
    a = np.array(cells, dtype=np.int64).reshape(-1, 3)
    assert ((a & 1).sum(1) == 1).all(), 'not a cell'
    return np.unique(((a[:, 0] + BIAS) << 40) | ((a[:, 1] + BIAS) << 20) | (a[:, 2] + BIAS))


def up(k):
    k = np.asarray(k, dtype=np.int64)
    return [tuple(int(v) for v in r) for r in np.stack([((k >> 40) & M20) - BIAS, ((k >> 20) & M20) - BIAS, (k & M20) - BIAS], 1)]


def upa(k):
    k = np.asarray(k, dtype=np.int64)
    return np.stack([((k >> 40) & M20) - BIAS, ((k >> 20) & M20) - BIAS, (k & M20) - BIAS], 1)


def run(k, gens):
    if gens == 0:
        return k
    n = len(k)
    cap = max(2048, 16 * n)
    while True:
        a = np.zeros(cap, np.int64); a[:n] = k
        b = np.zeros(cap, np.int64)
        m = lib().q_run(a.ctypes.data, n, b.ctypes.data, cap, gens)
        if m >= 0:
            return a[:m].copy()
        cap *= 4


def xor(a, b):
    return np.setxor1d(a, b, assume_unique=True)


def union(*a):
    return np.unique(np.concatenate(a))


def minus(a, b):
    return np.setdiff1d(a, b, assume_unique=True)


def same(a, b):
    return len(a) == len(b) and bool((a == b).all())


# ---------------------------------------------------------------- lattice
def offsets(axis):
    b, c = [i for i in range(3) if i != axis]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[axis] = sa; o[t] = st; out.append(tuple(o))
    return out


OFFS = [offsets(a) for a in range(3)]


def axis(c):
    return 0 if c[0] & 1 else (1 if c[1] & 1 else 2)


def nbrs(c):
    return [(c[0] + o[0], c[1] + o[1], c[2] + o[2]) for o in OFFS[axis(c)]]


def step_py(live):
    """a third stepper: pure python on a set."""
    cnt = {}
    for c in live:
        for q in nbrs(c):
            cnt[q] = cnt.get(q, 0) + 1
    return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))


def tr(c, k):
    """k units along v = (1, 0, -1)."""
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def unit(c):
    return c[0] >> 1


def in_tube(c):
    """the 3 x 3 tube of the wires along (1,0,-1) through the origin."""
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5


def tube_mask(k):
    a = upa(k)
    s1 = a[:, 0] + a[:, 1] + a[:, 2]; s2 = a[:, 0] - a[:, 1] + a[:, 2]
    return (s1 >= 1) & (s1 <= 5) & (s2 >= 1) & (s2 <= 5)


# the family of README section 9: two stators and four sites per unit
ST = [(0, 1, 2), (0, 1, 4)]
SITE = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]


def unit_cells(digit, u=0):
    return [tr(c, u) for c in ST] + [tr(SITE[i], u) for i in range(4) if digit >> i & 1]


def letters(k, ua, ub):
    """hex digit per unit of the family at an even generation (phase 0); '.' empty, '#' not a family unit.
    Only cells inside the 3 x 3 tube are read."""
    by = {}
    for c in up(k):
        if in_tube(c):
            by.setdefault(unit(c), set()).add(tr(c, -unit(c)))
    s = ''
    for u in range(ua, ub):
        x = by.get(u, set())
        if not x:
            s += '.'; continue
        if not set(ST) <= x or not x <= set(ST) | set(SITE):
            s += '#'; continue
        s += '0123456789abcdef'[sum(1 << i for i in range(4) if SITE[i] in x)]
    return s


# ---------------------------------------------------------------- symmetries
def syms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            out.append((perm, sg))
    return out


SYMS = syms()


def app(g, p, t=(0, 0, 0)):
    perm, sg = g
    return (sg[0] * p[perm[0]] + t[0], sg[1] * p[perm[1]] + t[1], sg[2] * p[perm[2]] + t[2])


def inv(g):
    perm, sg = g
    ip = [0, 0, 0]; isg = [0, 0, 0]
    for i in range(3):
        ip[perm[i]] = i; isg[perm[i]] = sg[i]
    return (tuple(ip), tuple(isg))


# ---------------------------------------------------------------- the oracle on a box torus
class Box:
    """An array torus of the given even shape; cell c sits at index c + off.  step() is oracle.step and asserts
    that nothing lives within 4 sites of the seam."""

    def __init__(self, shape, off):
        assert all(s % 2 == 0 for s in shape) and all(o % 2 == 0 for o in off)
        self.shape = tuple(shape); self.off = tuple(off)
        par = np.indices(self.shape) % 2
        self.m = [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]
        self.valid = self.m[0] | self.m[1] | self.m[2]

    @classmethod
    def around(cls, cells, margin):
        a = np.array(list(cells))
        lo = a.min(0) - margin; lo -= lo % 2
        hi = a.max(0) + margin; hi += hi % 2
        return cls(tuple(int(v) for v in hi - lo + 2), tuple(int(-v) for v in lo))

    def arr(self, cells):
        h = np.zeros(self.shape, np.int8)
        for c in cells:
            i = (c[0] + self.off[0], c[1] + self.off[1], c[2] + self.off[2])
            assert all(4 < i[q] < self.shape[q] - 5 for q in range(3)), ('outside the box', c)
            assert self.valid[i], ('not a cell', c)
            h[i] = 1
        return h

    def flip(self, h, cells):
        for c in cells:
            i = (c[0] + self.off[0], c[1] + self.off[1], c[2] + self.off[2])
            assert self.valid[i]
            h[i] ^= 1

    def step(self, h):
        n = oracle.step(h, self.m)
        assert not (n[:5].any() or n[-5:].any() or n[:, :5].any() or n[:, -5:].any() or n[:, :, :5].any() or n[:, :, -5:].any()), \
            'the pattern came within 4 sites of the seam'
        return n

    def cells(self, h):
        return sorted((int(p[0]) - self.off[0], int(p[1]) - self.off[1], int(p[2]) - self.off[2]) for p in np.argwhere(h))

    def keys(self, h):
        return pk(self.cells(h))


def jload(path):
    return json.load(open(path))


def obj(name):
    """an object of push 8b, by file name without .json."""
    return jload(os.path.join(P8B, 'objects', name + '.json'))
