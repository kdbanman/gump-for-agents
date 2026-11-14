"""fu.py -- lattices, vessels and ctypes wrappers for the class follow-up (research/theory/class/followup/).

Stepper and drivers: fu.c (built on first use into research/scratch/class_followup/libfu.so).  Validated by
`python3 fu.py validate` against an independent numpy gather stepper on every lattice used here, and against
research/audit/class/aud.c (aud_step).  Vessels are cell graphs: nbr[N, K] int32, entry N = outside, dead forever.

Lattices (integer coordinates):
    kagome4, kagome8   kagome = edge midpoints of the triangular lattice in doubled coordinates (not both even);
                       metric x^2 + xy + y^2.  kagome4: the 4 nearest (|o|^2 = 1); kagome8: + the 4 at |o|^2 = 3.
    hex9               honeycomb = triangular points with (p0 + 2 p1) mod 3 != 0; 3 nearest (|o|^2 = 1) + the 6
                       second neighbours (|o|^2 = 3, same sublattice).
    face12e, bond10    faces of the cubic honeycomb, doubled coordinates (exactly one odd coordinate); face12e = 8
                       perpendicular + 4 coplanar edge-sharing (+-2e_b, +-2e_c); bond10 = 8 perpendicular + the 2
                       parallel faces across the adjoining cubes (+-2e_a).  face12e is not gump.
Offsets are derived here from geometry and compared with research/theory/class/lattices.py and
research/audit/class/seal.py (`fu.py validate`).
"""
import ctypes, itertools, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
SCR = os.path.join(ROOT, "research", "scratch", "class_followup")
LIBF = os.path.join(SCR, "libfu.so")


# ------------------------------------------------------------------------------------------------ lattices
class Lat:
    def __init__(self, name, dim, typ, offsets, period):
        self.name, self.dim, self.typ, self.offsets, self.period = name, dim, typ, offsets, period
        self.K = max(len(o) for o in offsets)
        self.ntypes = len(offsets)


def _kag_typ(p):
    a, b = p[0] % 2, p[1] % 2
    return None if (a == 0 and b == 0) else {(1, 0): 0, (0, 1): 1, (1, 1): 2}[(a, b)]


def _hex_typ(p):
    f = (p[0] + 2 * p[1]) % 3
    return None if f == 0 else f - 1


def _tri2(o):
    return o[0] * o[0] + o[0] * o[1] + o[1] * o[1]


def _geo_offsets(typ, reps, shells):
    out = []
    for rep in reps:
        offs = [o for o in itertools.product(range(-4, 5), repeat=2)
                if any(o) and _tri2(o) in shells and typ((rep[0] + o[0], rep[1] + o[1])) is not None]
        out.append(sorted(offs))
    return out


def _face_typ(p):
    odd = [i for i in range(3) if p[i] % 2]
    return odd[0] if len(odd) == 1 else None


def _face_offsets(kind):
    out = []
    for a in range(3):
        b, c = [i for i in range(3) if i != a]
        offs = []
        for sa in (1, -1):
            for t in (b, c):
                for st in (1, -1):
                    o = [0, 0, 0]; o[a] = sa; o[t] = st; offs.append(tuple(o))
        extra = [(t, s) for t in (b, c) for s in (2, -2)] if kind == "face12e" else [(a, 2), (a, -2)]
        for t, s in extra:
            o = [0, 0, 0]; o[t] = s; offs.append(tuple(o))
        out.append(offs)
    return out


def lattice(name):
    if name == "kagome4":
        return Lat(name, 2, _kag_typ, _geo_offsets(_kag_typ, [(1, 0), (0, 1), (1, 1)], {1}), (2, 2))
    if name == "kagome8":
        return Lat(name, 2, _kag_typ, _geo_offsets(_kag_typ, [(1, 0), (0, 1), (1, 1)], {1, 3}), (2, 2))
    if name == "hex9":
        return Lat(name, 2, _hex_typ, _geo_offsets(_hex_typ, [(1, 0), (2, 0)], {1, 3}), (3, 3))
    if name in ("face12e", "bond10"):
        return Lat(name, 3, _face_typ, _face_offsets(name), (2, 2, 2))
    raise ValueError(name)


# ------------------------------------------------------------------------------------------------ vessels
class Vessel:
    def __init__(self, L, cells, canon):
        self.L, self.cells = L, list(cells)
        self.index = {p: i for i, p in enumerate(self.cells)}
        N, K = len(self.cells), L.K
        nbr = np.full((N, K), N, dtype=np.int32)
        for i, p in enumerate(self.cells):
            for j, o in enumerate(L.offsets[L.typ(p)]):
                q = canon(tuple(a + b for a, b in zip(p, o)))
                if q is not None:
                    nbr[i, j] = self.index[q]
        self.N, self.K, self.nbr = N, K, nbr
        for i in range(N):                         # symmetric graph
            for q in nbr[i]:
                if q < N:
                    assert i in nbr[q], "graph not symmetric"
        self.P = np.array(self.cells)

    def degrees(self):
        return (self.nbr < self.N).sum(1)


def torus(L, H):
    assert all(H % q == 0 for q in L.period)
    cells = [p for p in itertools.product(range(H), repeat=L.dim) if L.typ(p) is not None]
    return Vessel(L, cells, lambda p: tuple(a % H for a in p))


def region(L, pred, bound):
    cells = [p for p in itertools.product(range(-bound, bound + 1), repeat=L.dim) if L.typ(p) is not None and pred(p)]
    return Vessel(L, cells, lambda p: p if (max(abs(a) for a in p) <= bound and pred(p)) else None)


def strip2d(L, u, lo, hi, g, n):
    """2D: cells with lo <= u.p <= hi, periodic under n*g (u.g = 0, g a translation of the lattice).
    Canonical representative: p - k n g with 0 <= w.p - k n (w.g) < n (w.g), w = g."""
    assert u[0] * g[0] + u[1] * g[1] == 0
    wg = g[0] * g[0] + g[1] * g[1]
    per = n * wg

    def canon(p):
        h = u[0] * p[0] + u[1] * p[1]
        if h < lo or h > hi:
            return None
        k = (g[0] * p[0] + g[1] * p[1]) // per
        return (p[0] - k * n * g[0], p[1] - k * n * g[1])

    R = 4 * (abs(lo) + abs(hi) + n * (abs(g[0]) + abs(g[1])) + 4)
    cells = set()
    for p in itertools.product(range(-R, R + 1), repeat=2):
        if L.typ(p) is None:
            continue
        q = canon(p)
        if q is not None:
            cells.add(q)
    cells = sorted(cells)
    V = Vessel(L, cells, canon)
    V.h = V.P @ np.array(u)
    return V


# ------------------------------------------------------------------------------------------------ structure
def outside_count(L, inside, cand):
    """max over candidate cells p NOT inside of #{neighbours of p inside}: the sealing number c of the vessel's
    outside (exact if cand covers every outside cell within reach)."""
    worst = 0
    for p in cand:
        if L.typ(p) is None or inside(p):
            continue
        k = sum(1 for o in L.offsets[L.typ(p)] if inside(tuple(a + b for a, b in zip(p, o))))
        worst = max(worst, k)
    return worst


def armoured_core(V, b, c):
    """Theorem E: (b-1)-core of the cells of vessel-degree <= c - 1."""
    deg = V.degrees()
    W = set(int(i) for i in np.nonzero(deg <= c - 1)[0])
    ch = True
    while ch:
        ch = False
        for i in list(W):
            if sum(1 for q in V.nbr[i] if int(q) in W) < b - 1:
                W.discard(i); ch = True
    return W


def sealed_subset(V, W, b):
    """largest subset of W whose cells have <= b - 1 neighbours in the vessel outside it (plain peeling)."""
    W = set(int(i) for i in W)
    ch = True
    while ch:
        ch = False
        for i in list(W):
            if sum(1 for q in V.nbr[i] if q < V.N and int(q) not in W) > b - 1:
                W.discard(i); ch = True
    return W


# ------------------------------------------------------------------------------------------------ rules
def mask(s):
    m = 0
    for k in s:
        m |= 1 << k
    return m


def capped(b, c, K):
    return list(range(b, min(c, K + 1))), list(range(b - 1, min(c, K + 1)))


# ------------------------------------------------------------------------------------------------ C library
_lib = []


def lib():
    if not _lib:
        os.makedirs(SCR, exist_ok=True)
        src = os.path.join(HERE, "fu.c")
        if not os.path.exists(LIBF) or os.path.getmtime(LIBF) < os.path.getmtime(src):
            subprocess.run(["cc", "-O3", "-march=native", "-shared", "-fPIC", "-o", LIBF, src], check=True)
        _lib.append(ctypes.CDLL(LIBF))
    return _lib[0]


_i32p = np.ctypeslib.ndpointer(np.int32, flags="C")
_u64p = np.ctypeslib.ndpointer(np.uint64, flags="C")
_f64p = np.ctypeslib.ndpointer(np.float64, flags="C")
_i64p = np.ctypeslib.ndpointer(np.int64, flags="C")


def pack(states):
    R, N = states.shape
    x = np.zeros(N + 1, np.uint64)
    for r in range(R):
        x[:N] |= states[r].astype(np.uint64) << np.uint64(r)
    return x


def unpack(x, R=64):
    N = len(x) - 1
    return np.array([(x[:N] >> np.uint64(r)) & np.uint64(1) for r in range(R)], dtype=np.uint8)


def step(V, x, B, S):
    f = lib().fu_step
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, _u64p, _u64p, ctypes.c_uint32, ctypes.c_uint32]
    out = np.zeros_like(x)
    f(V.N, V.K, np.ascontiguousarray(V.nbr), x, out, mask(B), mask(S))
    return out


def peel(V, W, b):
    f = lib().fu_peel
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, _u64p, ctypes.c_int]
    W = W.copy()
    f(V.N, V.K, np.ascontiguousarray(V.nbr), W, b)
    return W


def _groups(groups):
    gidx = np.concatenate([np.asarray(g, np.int32) for g in groups]).astype(np.int32) if groups else np.zeros(1, np.int32)
    gstart = np.cumsum([0] + [len(g) for g in groups]).astype(np.int32)
    return gidx, gstart


def slab_run(V, B, S, b, groups, lab, p, gens, T0=200, P=8, seed=1, nbins=40, maxw=400000):
    f = lib().fu_slab
    f.restype = ctypes.c_long
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int, _i32p, _i32p,
                  _i32p, ctypes.c_double, ctypes.c_int, ctypes.c_long, ctypes.c_int, ctypes.c_uint64, _f64p, _f64p,
                  _f64p, ctypes.c_int, _i32p, ctypes.c_int]
    gidx, gstart = _groups(groups)
    res = np.zeros(20); be = np.zeros(nbins); bw = np.zeros(nbins); waits = np.zeros(maxw, np.int32)
    nw = f(V.N, V.K, np.ascontiguousarray(V.nbr), mask(B), mask(S), b, gidx, gstart,
           np.ascontiguousarray(lab, dtype=np.int32), p, T0, gens, P, seed, res, be, bw, nbins, waits, maxw)
    return dict(exposure=res[0], walls=int(res[1]), cuts=int(res[2]), pits=int(res[3]), periodic=int(res[4]),
                early=[int(v) for v in res[5:9]], max_age_end=int(res[9]), alive_old_end=int(res[10]),
                max_age=int(res[19]),
                dens=[res[11 + l] / res[15 + l] if res[15 + l] else float("nan") for l in range(4)],
                binexp=be, binwall=bw, waits=waits[:nw].copy())


def life_run(V, B, S, b, groups, p, cap, P=16, seed=1, x0=None):
    f = lib().fu_life
    f.argtypes = [ctypes.c_int, ctypes.c_int, _i32p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int, ctypes.c_int,
                  _i32p, _i32p, ctypes.c_double, ctypes.c_long, ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p,
                  _i64p, _i32p, _i32p, _i64p, _i64p, _i32p, _i32p]
    gidx, gstart = _groups(groups)
    life = np.zeros(64, np.int64); kind = np.zeros(64, np.int32); pop = np.zeros(64, np.int32)
    tD = np.zeros(64, np.int64); tG = np.zeros(64, np.int64); gf = np.zeros(64, np.int32); dz = np.zeros(64, np.int32)
    xp = None if x0 is None else x0.ctypes.data_as(ctypes.c_void_p)
    f(V.N, V.K, np.ascontiguousarray(V.nbr), mask(B), mask(S), b, len(groups), gidx, gstart, p, cap, P, seed, xp,
      life, kind, pop, tD, tG, gf, dz)
    return dict(life=life, kind=kind, pop=pop, tD=tD, tG=tG, gfirst=gf, dsize=dz)


def bulk_run(V, B, S, p, chk, seed=1):
    """the review's validated torus statistic (research/audit/class/aud.c, aud_bulk)."""
    sys.path.insert(0, os.path.join(ROOT, "research", "audit", "class"))
    import aud
    return aud.bulk_run(V, B, S, p, chk, seed=seed)


def tau_line(r, nwalls=2):
    d = r["walls"]
    if d == 0:
        return None
    tau = nwalls * r["exposure"] / d
    w = r["waits"].astype(float)
    return dict(lntau=float(np.log(tau)), err=float(1 / np.sqrt(d)), cv=float(w.std() / w.mean()) if len(w) > 1 else None)


def hazard(r, nwalls=2, groups=((0, 6), (6, 9), (9, 11), (11, 13), (13, 40))):
    """tau per wall in age bins [2^k0, 2^k1) of age - T0."""
    out = []
    for k0, k1 in groups:
        e = r["binexp"][k0:k1].sum(); d = r["binwall"][k0:k1].sum()
        if e > 0:
            out.append([2 ** k0, 2 ** k1, int(d), round(float(nwalls * e / d), 1) if d else None])
    return out


# ------------------------------------------------------------------------------------------------ validation
def np_step(nbr, s, B, S):
    """independent numpy gather stepper: s (R, N + 1) uint8, last column dead."""
    cnt = s[:, nbr].sum(axis=2)
    x = s[:, :-1]
    Bt = np.zeros(32, bool); Bt[B] = True
    St = np.zeros(32, bool); St[S] = True
    new = np.where(x == 1, St[cnt], Bt[cnt]).astype(np.uint8)
    out = np.zeros_like(s); out[:, :-1] = new
    return out


def validate():
    sys.path.insert(0, os.path.join(ROOT, "research", "theory", "class"))
    sys.path.insert(0, os.path.join(ROOT, "research", "audit", "class"))
    import lattices as AL, aud, seal
    ok = True
    # offsets against the author's lattices.py and the review's seal.py
    S = seal.lattices()
    for name, al in (("kagome4", "kagome4"), ("kagome8", "kagome8"), ("hex9", "hex9")):
        L = lattice(name); A = AL.get(al)
        same = all(sorted(L.offsets[t]) == sorted(A.offsets[t]) for t in range(L.ntypes))
        same &= all(L.typ(p) == A.typ(p) for p in itertools.product(range(6), repeat=2))
        ok &= same
        print(f"offsets {name}: equal to research/theory/class/lattices.py: {same}; K = {L.K}, per type "
              f"{[len(o) for o in L.offsets]}")
    for name in ("face12e", "bond10"):
        L = lattice(name)
        same = all(sorted(L.offsets[t]) == sorted(S[name][3][t]) for t in range(3))
        ok &= same
        print(f"offsets {name}: equal to research/audit/class/seal.py: {same}")
    # stepper: fu_step vs numpy gather vs aud_step, cell for cell
    rng = np.random.default_rng(7)
    tests = [("kagome4", 2, 3, torus(lattice("kagome4"), 16)), ("kagome8", 4, 6, torus(lattice("kagome8"), 16)),
             ("kagome8", 4, 7, strip2d(lattice("kagome8"), (2, 1), 0, 12, (2, -4), 3)),
             ("hex9", 4, 6, torus(lattice("hex9"), 18)), ("hex9", 4, 8, strip2d(lattice("hex9"), (2, 1), 1, 14, (1, -2), 5)),
             ("kagome4", 2, 3, strip2d(lattice("kagome4"), (1, 0), 0, 12, (0, 2), 5)),
             ("face12e", 4, 6, torus(lattice("face12e"), 8)), ("bond10", 3, 5, torus(lattice("bond10"), 8)),
             ("bond10", 3, 6, region(lattice("bond10"), lambda q: all(1 <= a <= 9 for a in q), 10))]
    for name, b, c, V in tests:
        B, Sv = capped(b, c, V.K)
        st = (rng.random((64, V.N)) < 0.45).astype(np.uint8)
        s = np.zeros((64, V.N + 1), np.uint8); s[:, :-1] = st
        x = pack(st); xa = x.copy()
        good = True
        for t in range(100):
            s = np_step(V.nbr, s, B, Sv)
            x = step(V, x, B, Sv)
            xa = aud.step(V, xa, B, Sv)
            good &= bool((unpack(x) == s[:, :-1]).all()) and bool((x == xa).all())
        alive = int(s[:, :-1].sum())
        ok &= good and alive > 0
        print(f"stepper {name} (b={b}, c={c}) on {V.N} cells x 64 replicas x 100 generations: fu_step == numpy gather "
              f"== aud_step every generation: {good} (live cells at the end {alive})")
    # peeling: bit-sliced against plain set peeling
    V = strip2d(lattice("kagome4"), (1, 0), 0, 12, (0, 2), 6)
    B, Sv = capped(2, 3, 4)
    x = pack((rng.random((64, V.N)) < 0.45).astype(np.uint8))
    good = True
    for t in range(60):
        x = step(V, x, B, Sv)
        Wb = unpack(peel(V, ~x & np.uint64(2 ** 64 - 1), 2))
        u = unpack(x)
        for r in range(0, 64, 8):
            ref = sealed_subset(V, np.nonzero(u[r] == 0)[0], 2)
            good &= set(np.nonzero(Wb[r])[0].tolist()) == ref
    ok &= good
    print(f"bit-sliced peeling == plain peeling on a kagome4 strip, 60 generations x 8 replicas: {good}")
    print("ALL OK" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        sys.exit(0 if validate() else 1)
