"""push 8b: shared helpers.  Cells are doubled-coordinate tuples (exactly one odd), docs/AUTOMATON.md.

Stepper: st.c (sparse, infinite lattice or a ring along (1,0,-1)), checked against reference/oracle.py by
check_st.py.  States are sorted numpy uint64 arrays of packed keys (pk / up).
"""
import ctypes, itertools, json, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SIG = os.path.join(ROOT, 'research', 'signals')
SCR = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p8b')
os.makedirs(SCR, exist_ok=True)
OFF = 1 << 20

_lib = None


def lib():
    global _lib
    if _lib is None:
        so, src = os.path.join(HERE, 'st.so'), os.path.join(HERE, 'st.c')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O2', '-shared', '-fPIC', '-o', so, src])
        _lib = ctypes.CDLL(so)
        _lib.run.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        _lib.run.restype = ctypes.c_int
    return _lib


def is_cell(p):
    return (p[0] & 1) + (p[1] & 1) + (p[2] & 1) == 1


def pk(cells):
    """cells (iterable of tuples) -> sorted uint64 array of keys."""
    cells = list(cells)
    if not cells:
        return np.zeros(0, np.uint64)
    a = np.array(cells, dtype=np.int64).reshape(-1, 3)
    assert (((a & 1).sum(1)) == 1).all(), 'not a cell'
    k = ((a[:, 0] + OFF) << 42) | ((a[:, 1] + OFF) << 21) | (a[:, 2] + OFF)
    return np.unique(k.astype(np.uint64))


def up(k):
    """keys -> list of tuples."""
    k = np.asarray(k, dtype=np.uint64).astype(np.int64)
    m = (1 << 21) - 1
    return [tuple(int(v) for v in r) for r in np.stack([(k >> 42) - OFF, ((k >> 21) & m) - OFF, (k & m) - OFF], 1)]


def run(k, gens, L=0):
    """gens generations of the sorted key array k (ring of L units along (1,0,-1) if L > 0)."""
    if gens == 0:
        return k
    n = len(k)
    cap = max(4096, 8 * n)
    while True:
        buf = np.zeros(cap, np.uint64); buf[:n] = k
        tmp = np.zeros(cap, np.uint64)
        m = lib().run(buf.ctypes.data, n, tmp.ctypes.data, cap, gens, L)
        if m >= 0:
            return buf[:m].copy()
        cap *= 4


def orbit(k, gens, L=0):
    out = [k]
    for _ in range(gens):
        k = run(k, 1, L); out.append(k)
    return out


def xor(a, b):
    return np.setxor1d(a, b, assume_unique=True)


def union(*a):
    return np.unique(np.concatenate(a))


def same(a, b):
    return len(a) == len(b) and bool((a == b).all())


# ------------------------------------------------------------------ the lattice
def offsets(axis):
    a = axis; b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


OFFS = [offsets(a) for a in range(3)]


def axis(p):
    return 0 if p[0] & 1 else (1 if p[1] & 1 else 2)


def nbrs(p):
    return [(p[0] + o[0], p[1] + o[1], p[2] + o[2]) for o in OFFS[axis(p)]]


def halo(cells):
    """cells and all their neighbours."""
    s = set(cells)
    for c in cells:
        s.update(nbrs(c))
    return s


def step_py(live):
    """One generation on the infinite lattice, pure python (a third stepper for cross-checks)."""
    cnt = {}
    for c in live:
        for q in nbrs(c):
            cnt[q] = cnt.get(q, 0) + 1
    return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))


# the 48 symmetries: signed permutation matrices (they preserve "exactly one odd coordinate")
def _syms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            out.append((perm, sg))
    return out


SYMS = _syms()


def app(g, p, t=(0, 0, 0)):
    perm, sg = g
    return (sg[0] * p[perm[0]] + t[0], sg[1] * p[perm[1]] + t[1], sg[2] * p[perm[2]] + t[2])


def appv(g, v):
    return app(g, v)


def tr(c, k):
    """move by k units along v = (1,0,-1)."""
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def unit(c):
    return c[0] >> 1


V = (1, 0, -1)

# ------------------------------------------------------------------ the wires on file (README sections 9, 10)
B0 = [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]           # wire B, even generations, unit 0
BP0 = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 4)]          # wire B'
C0 = [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]           # wire C
PULSE_B = [(13, 0, -12), (14, 2, -11)]      # objects/pulse-B.json: flip these two cells (unit 6) at an even gen
PULSE_C = [(13, 0, -10), (15, 0, -10)]      # objects/pulse-C.json (p>)
PULSE_C_LEFT = [(12, 2, -9), (13, 0, -8)]   # objects/pulse-C-left.json (p<)


def HT(c):
    """the half-turn of README section 3: maps wire B to itself reversed."""
    return (-c[0] - 2, c[1], 8 - c[2])


def MIR(c):
    """the mirror of README section 9: maps wire C at one generation onto wire C at the next, reversed."""
    return (c[2] - 4, c[1], c[0] + 4)


def load(name):
    return json.load(open(os.path.join(SIG, 'objects', name + '.json')))
