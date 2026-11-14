"""aud.py -- the audit's own lattices, vessels and ctypes wrappers around aud.c.

Shares no code with research/theory/class/.  Lattices are given by (is_cell, offsets_of) in integer coordinates:

    gump     faces of the cubic honeycomb, doubled coords (exactly one odd), 8 perpendicular + 4 coplanar CORNER
    face12e  same cells, 8 perpendicular + 4 coplanar EDGE-sharing (+-2e_b, +-2e_c)        [not gump]
    fcc      Z^3 with even coordinate sum, 12 nearest
    cross2   Z^2, range-2 von Neumann cross (8 neighbours)

Vessels are built as cell graphs: a list of canonical cell coordinates and an int32 array nbr[N, K] whose entry N
means "outside the vessel, dead forever".
"""
import ctypes, itertools, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.normpath(os.path.join(HERE, "..", "..", "scratch", "audit-class"))
LIB = os.path.join(SCR, "libaud.so")


# ----------------------------------------------------------------------------------------------- lattices
def face_type(p):
    odd = [i for i in range(3) if p[i] % 2]
    return odd[0] if len(odd) == 1 else None


def face_offsets(kind):
    """offsets[type] for the face lattice; kind = 'gump' (corner four) or 'face12e' (edge four)."""
    out = []
    for a in range(3):
        b, c = [i for i in range(3) if i != a]
        offs = []
        for sa in (1, -1):
            for t in (b, c):
                for st in (1, -1):
                    o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
        if kind == "gump":
            for sb in (2, -2):
                for sc in (2, -2):
                    o = [0, 0, 0]; o[b] = sb; o[c] = sc; offs.append(tuple(o))
        elif kind == "face12e":
            for t in (b, c):
                for st in (2, -2):
                    o = [0, 0, 0]; o[t] = st; offs.append(tuple(o))
        elif kind == "bond10":                     # 8 perpendicular + the 2 parallel faces across the adjoining cubes
            for st in (2, -2):
                o = [0, 0, 0]; o[a] = st; offs.append(tuple(o))
        elif kind == "face8":                      # the 8 perpendicular only
            pass
        else:
            raise ValueError(kind)
        out.append(offs)
    return out


class Lat:
    def __init__(self, name, dim, typ, offsets):
        self.name, self.dim, self.typ, self.offsets = name, dim, typ, offsets
        self.K = max(len(o) for o in offsets)


def lattice(name):
    if name in ("gump", "face12e", "bond10", "face8"):
        return Lat(name, 3, face_type, face_offsets(name))
    if name == "fcc":
        offs = [o for o in itertools.product((-1, 0, 1), repeat=3) if sum(abs(a) for a in o) == 2]
        return Lat(name, 3, lambda p: 0 if sum(p) % 2 == 0 else None, [offs])
    if name == "cross2":
        offs = [(k, 0) for k in (-2, -1, 1, 2)] + [(0, k) for k in (-2, -1, 1, 2)]
        return Lat(name, 2, lambda p: 0, [offs])
    if name == "vn":
        return Lat(name, 2, lambda p: 0, [[(1, 0), (-1, 0), (0, 1), (0, -1)]])
    raise ValueError(name)


# ----------------------------------------------------------------------------------------------- vessels
class Vessel:
    def __init__(self, L, cells, canon):
        """cells: list of canonical coordinate tuples.  canon(p) -> canonical tuple, or None if outside."""
        self.L, self.cells = L, cells
        self.index = {p: i for i, p in enumerate(cells)}
        N, K = len(cells), L.K
        nbr = np.full((N, K), N, dtype=np.int32)
        for i, p in enumerate(cells):
            for j, o in enumerate(L.offsets[L.typ(p)]):
                q = canon(tuple(a + b for a, b in zip(p, o)))
                if q is not None:
                    nbr[i, j] = self.index[q]
        self.N, self.K, self.nbr = N, K, nbr
        # symmetry of the graph (every edge in both directions)
        for i in range(N):
            for q in nbr[i]:
                if q < N:
                    assert i in nbr[q], "graph not symmetric"

    def degrees(self):
        return (self.nbr < self.N).sum(1)


def torus(L, H):
    """All cells with coordinates in [0, H)^d, wrapped mod H (H even for the face lattice and fcc)."""
    cells = [p for p in itertools.product(range(H), repeat=L.dim) if L.typ(p) is not None]
    return Vessel(L, cells, lambda p: tuple(a % H for a in p))


def box(L, lo, hi):
    """All cells with lo[a] <= p[a] <= hi[a]; outside dead."""
    cells = [p for p in itertools.product(*[range(l, h + 1) for l, h in zip(lo, hi)]) if L.typ(p) is not None]
    inside = lambda p: p if all(l <= a <= h for a, l, h in zip(p, lo, hi)) else None
    return Vessel(L, cells, inside)


def region(L, pred, bound):
    """All cells p in [-bound, bound]^d with pred(p); outside dead."""
    cells = [p for p in itertools.product(range(-bound, bound + 1), repeat=L.dim) if L.typ(p) is not None and pred(p)]
    return Vessel(L, cells, lambda p: p if (max(abs(a) for a in p) <= bound and pred(p)) else None)


def slab111(L, m, a, b):
    """Face lattice or fcc: m consecutive layers of s = x + y + z (step 2), periodic under a*g1, b*g2 with
    g1 = (2,-2,0), g2 = (0,2,-2) for the face lattice (s = 1, 3, ..) and (1,-1,0), (0,1,-1) for fcc (s = 0, 2, ..).
    Canonical cell: (x mod Px, s - x - z, z mod Pz).  Returns (vessel, layer index of each cell)."""
    if L.name in ("gump", "face12e", "bond10", "face8"):
        Px, Pz, s0 = 2 * a, 2 * b, 1
    elif L.name == "fcc":
        Px, Pz, s0 = a, b, 0
    else:
        raise ValueError
    svals = [s0 + 2 * k for k in range(m)]

    def canon(p):
        s = p[0] + p[1] + p[2]
        if s < svals[0] or s > svals[-1]:
            return None
        x, z = p[0] % Px, p[2] % Pz
        return (x, s - x - z, z)

    cells = []
    for s in svals:
        for x in range(Px):
            for z in range(Pz):
                p = (x, s - x - z, z)
                if L.typ(p) is not None:
                    cells.append(p)
    V = Vessel(L, cells, canon)
    layer = np.array([(p[0] + p[1] + p[2] - s0) // 2 for p in cells])
    return V, layer


def slab100(L, xlo, xhi, n1, n2=None):
    """Face lattice: all cells with xlo <= x <= xhi, periodic in y and z with periods 2*n1, 2*n2 (n cubes).
    Returns (vessel, x coordinate of each cell)."""
    n2 = n1 if n2 is None else n2
    Py, Pz = 2 * n1, 2 * n2

    def canon(p):
        if p[0] < xlo or p[0] > xhi:
            return None
        return (p[0], p[1] % Py, p[2] % Pz)

    cells = [p for p in itertools.product(range(xlo, xhi + 1), range(Py), range(Pz)) if L.typ(p) is not None]
    V = Vessel(L, cells, canon)
    return V, np.array([p[0] for p in cells])


def strip2d(L, m, n):
    """2D one-type lattice on Z^2: rows y = 0..m-1, periodic in x with period n."""
    cells = [(x, y) for y in range(m) for x in range(n)]
    V = Vessel(L, cells, lambda p: (p[0] % n, p[1]) if 0 <= p[1] < m else None)
    return V, np.array([p[1] for p in cells])


# ----------------------------------------------------------------------------------------------- rule helpers
def mask(s):
    m = 0
    for k in s:
        m |= 1 << k
    return m


def capped(b, c, K):
    """B, S of the capped threshold (b, c): alive next iff n + x >= b and n <= c - 1."""
    return list(range(b, min(c, K + 1))), list(range(b - 1, min(c, K + 1)))


# ----------------------------------------------------------------------------------------------- C library
def lib():
    os.makedirs(SCR, exist_ok=True)
    src = os.path.join(HERE, "aud.c")
    if not os.path.exists(LIB) or os.path.getmtime(LIB) < os.path.getmtime(src):
        subprocess.run(["cc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIB, src], check=True)
    return ctypes.CDLL(LIB)


_i32p = np.ctypeslib.ndpointer(np.int32, flags="C")
_u64p = np.ctypeslib.ndpointer(np.uint64, flags="C")
_f64p = np.ctypeslib.ndpointer(np.float64, flags="C")
_i64p = np.ctypeslib.ndpointer(np.int64, flags="C")


def pack(states):
    """states: array [R <= 64, N] of 0/1 -> uint64[N + 1] with bit r = replica r."""
    R, N = states.shape
    x = np.zeros(N + 1, np.uint64)
    for r in range(R):
        x[:N] |= states[r].astype(np.uint64) << np.uint64(r)
    return x


def unpack(x, R=64):
    N = len(x) - 1
    return np.array([(x[:N] >> np.uint64(r)) & np.uint64(1) for r in range(R)], dtype=np.uint8)


def step(V, x, B, S, _l=[]):
    if not _l:
        _l.append(lib())
    f = _l[0].aud_step
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, _u64p, _u64p, ctypes.c_uint32, ctypes.c_uint32]
    out = np.zeros_like(x)
    f(V.N, V.K, np.ascontiguousarray(V.nbr), x, out, mask(B), mask(S))
    return out


def face_run(V, B, S, groups, lab, p, gens, T0=200, seed=1, maxw=200000, nbins=40):
    """groups: list of index arrays (watched cell sets).  Returns a dict."""
    L = lib()
    f = L.aud_face
    f.restype = ctypes.c_long
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int, _i32p, _i32p,
                  _i32p, ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.c_uint64, _f64p, _f64p, _f64p,
                  ctypes.c_int, _i32p, _i32p, ctypes.c_int]
    fidx = np.concatenate([np.asarray(g, np.int32) for g in groups]).astype(np.int32)
    fstart = np.cumsum([0] + [len(g) for g in groups]).astype(np.int32)
    res = np.zeros(22); be = np.zeros(nbins); bd = np.zeros(nbins)
    waits = np.zeros(maxw, np.int32); wg = np.zeros(maxw, np.int32)
    nw = f(V.N, V.K, np.ascontiguousarray(V.nbr), mask(B), mask(S), len(groups), fidx, fstart,
           np.ascontiguousarray(lab, dtype=np.int32), p, T0, gens, seed, res, be, bd, nbins, waits, wg, maxw)
    return dict(exposure=res[0], deaths=int(res[1]), early=int(res[2]), settle=int(res[3]), early_settle=int(res[4]),
                gens=int(res[5]), dens=[res[6 + l] / res[10 + l] if res[10 + l] else float("nan") for l in range(4)],
                by_group=[int(res[14 + g]) for g in range(min(8, len(groups)))], binexp=be, bindeath=bd,
                waits=waits[:nw].copy(), wgroup=wg[:nw].copy())


def life_run(V, B, S, p, cap, seed=1, x0=None):
    L = lib()
    f = L.aud_life
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_double, ctypes.c_long,
                  ctypes.c_uint64, ctypes.c_void_p, _i64p, _i32p, _i32p]
    life = np.zeros(64, np.int64); pop = np.zeros(64, np.int32); kind = np.zeros(64, np.int32)
    xp = None if x0 is None else x0.ctypes.data_as(ctypes.c_void_p)
    f(V.N, V.K, np.ascontiguousarray(V.nbr), mask(B), mask(S), p, cap, seed, xp, life, pop, kind)
    return life, pop, kind


def bulk_run(V, B, S, p, chk, seed=1):
    L = lib()
    f = L.aud_bulk
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_double, ctypes.c_uint64,
                  ctypes.c_int, _i64p, _f64p]
    chk = np.asarray(chk, np.int64)
    out = np.zeros(4 * len(chk))
    f(V.N, V.K, np.ascontiguousarray(V.nbr), mask(B), mask(S), p, seed, len(chk), chk, out)
    return out.reshape(-1, 4)       # rows: running, density (running), activity (running), density (all)


# ----------------------------------------------------------------------------------------------- sealed sets
def largest_sealed_subset(V, W, b):
    """Largest subset of the index set W in which every cell has at most b - 1 neighbours in V minus the subset
    (plain peeling).  Returns a set of indices."""
    W = set(int(i) for i in W)
    out = {i: sum(1 for q in V.nbr[i] if q < V.N and q not in W) for i in W}
    stack = [i for i in W if out[i] > b - 1]
    while stack:
        i = stack.pop()
        if i not in W:
            continue
        W.discard(i)
        for q in V.nbr[i]:
            q = int(q)
            if q in W:
                out[q] += 1
                if out[q] > b - 1:
                    stack.append(q)
    return W


def tau_stats(r, nfaces):
    """ln tau per face, its standard error, CV of the uncensored waits."""
    d = r["deaths"]
    if d == 0:
        return None
    tau = nfaces * r["exposure"] / d
    w = r["waits"].astype(float)
    cv = float(w.std() / w.mean()) if len(w) > 1 else float("nan")
    return dict(lntau=float(np.log(tau)), err=float(1 / np.sqrt(d)), cv=cv, deaths=d)
