"""signals: shared helpers.  Cells are doubled-coordinate tuples (exactly one odd coordinate), as in docs/AUTOMATON.md.

Three steppers, each checked against reference/oracle.py by check_stepper.py:
  step_set(live)              sparse, on the infinite lattice (python sets)
  Geom(...).run / .cycle ...  C kernels (sgc.c) on a quotient of the lattice by a period lattice, optionally cut down
                              to a region bounded by diagonal layers (exact by T2/T4 for patterns that start inside)
  oracle_run(cells, shape, g) reference/oracle.py's own step() on an even box torus (the judge)
"""
import ctypes, os, subprocess, sys
from collections import Counter, deque
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'signals')
os.makedirs(SCR, exist_ok=True)
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

OFFS = [oracle.offsets(a) for a in range(3)]
DIAGS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def axis(p):
    return 0 if p[0] & 1 else (1 if p[1] & 1 else 2)


def is_cell(p):
    return (p[0] & 1) + (p[1] & 1) + (p[2] & 1) == 1


def nbrs(p):
    x, y, z = p
    return [(x + o[0], y + o[1], z + o[2]) for o in OFFS[axis(p)]]


def step_set(live):
    """One generation on the infinite lattice."""
    cnt = Counter()
    for c in live:
        for q in nbrs(c):
            cnt[q] += 1
    return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))


def dot(d, p):
    return d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def read_cells(fn):
    out = []
    for line in open(fn):
        w = line.split('#')[0].split()
        if len(w) == 3:
            out.append(tuple(map(int, w)))
    return frozenset(out)


def write_cells(fn, cells, header=''):
    with open(fn, 'w') as f:
        for h in header.splitlines():
            f.write('# ' + h + '\n')
        for c in sorted(cells):
            f.write('%d %d %d\n' % tuple(c))


# ------------------------------------------------------------------ the oracle as judge
def box_masks(shape):
    """oracle.masks for a box that need not be cubic (same definition: coordinate a odd, the others even)."""
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def oracle_run(cells, shape, gens, every=1):
    """Step `cells` (doubled coords, taken mod shape) with reference/oracle.py's step() on the even box torus `shape`.
    Yields (t, frozenset of cells with coordinates in [0, shape)) for t = 0, every, 2*every, ... <= gens."""
    assert all(s % 2 == 0 for s in shape)
    m = box_masks(shape) if len(set(shape)) > 1 else oracle.masks(shape[0])
    h = np.zeros(shape, np.int8)
    for c in cells:
        assert is_cell(c)
        h[c[0] % shape[0], c[1] % shape[1], c[2] % shape[2]] = 1
    for t in range(gens + 1):
        if t % every == 0:
            yield t, frozenset(map(tuple, np.argwhere(h).tolist()))
        if t < gens:
            h = oracle.step(h, m)


# ------------------------------------------------------------------ quotient geometries
def hnf_cols(G):
    """G: r x 3 integer rows (generators).  Returns (U, H): U unimodular 3x3, H = G.U lower echelon, H[i][i] > 0."""
    G = [list(map(int, r)) for r in G]
    U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    def add(i, j, k):          # col_i += k col_j
        for M in (G, U):
            for row in M:
                row[i] += k * row[j]
    def swap(i, j):
        for M in (G, U):
            for row in M:
                row[i], row[j] = row[j], row[i]
    for i in range(len(G)):
        while True:
            nz = [j for j in range(i, 3) if G[i][j] != 0]
            if not nz:
                raise ValueError('generators are dependent')
            if len(nz) == 1:
                break
            jm = min(nz, key=lambda j: abs(G[i][j]))
            for j in nz:
                if j != jm:
                    add(j, jm, -(G[i][j] // G[i][jm]))
        if nz[0] != i:
            swap(i, nz[0])
        if G[i][i] < 0:
            for M in (G, U):
                for row in M:
                    row[i] = -row[i]
    return U, G


_lib = None


def lib():
    global _lib
    if _lib is None:
        so, src = os.path.join(HERE, 'sgc.so'), os.path.join(HERE, 'sgc.c')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O2', '-shared', '-fPIC', '-o', so, src])
        _lib = ctypes.CDLL(so)
        P = ctypes.c_void_p
        _lib.dstep.argtypes = [ctypes.c_int, P, P, P]; _lib.dstep.restype = ctypes.c_int
        _lib.drun.argtypes = [ctypes.c_int, P, P, ctypes.c_long]
        _lib.srun.argtypes = [ctypes.c_int, P, P, ctypes.c_long]
        _lib.dcycle.argtypes = [ctypes.c_int, P, P, ctypes.c_long, P]; _lib.dcycle.restype = ctypes.c_long
        _lib.track.argtypes = [ctypes.c_int, P, P, P, P, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_long,
                               P, P, P, P, P]
        _lib.track.restype = ctypes.c_int
        _lib.soups.argtypes = [ctypes.c_int, P, P, ctypes.c_int, ctypes.c_double, ctypes.c_uint64, ctypes.c_long,
                               P, P, P]
    return _lib


def ptr(a):
    return a.ctypes.data_as(ctypes.c_void_p)


class Geom:
    """The lattice modulo the period lattice generated by `periods` (cube vectors; translation by 2g in doubled
    coordinates), restricted to cells p with lo <= d.p <= hi for each (d, lo, hi) in `bounds` (cells outside are dead
    forever; exact by T2 when every d is a body diagonal with d.g = 0 for every period g and the pattern starts
    inside).  The first period is taken to be N times `unitvec` when `unitvec` is given; cell i then has
    unit[i] in [0, N), its position along the ring."""

    def __init__(self, periods, bounds=(), unitvec=None, seeds=None, box=None):
        self.periods = [tuple(map(int, g)) for g in periods]
        self.bounds = [(tuple(d), lo, hi) for d, lo, hi in bounds]
        for d, lo, hi in self.bounds:
            assert all(dot(d, g) == 0 for g in self.periods), 'bound not invariant under the periods'
        self.U, self.H = hnf_cols(self.periods) if self.periods else ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [])
        Um = np.array(self.U)
        self.Ui = np.rint(np.linalg.inv(Um)).astype(int)
        assert (Um @ self.Ui == np.eye(3, dtype=int)).all()
        self.U = [tuple(r) for r in self.U]; self.Ui = [tuple(int(v) for v in r) for r in self.Ui]
        self._cache = {}
        if seeds is None:
            B = box or 6
            seeds = [(x, y, z) for x in range(-B, B + 1) for y in range(-B, B + 1) for z in range(-B, B + 1)
                     if is_cell((x, y, z))]
        seeds = [self.canon(p) for p in seeds if self.inside(p)]
        cells = dict.fromkeys(seeds); dq = deque(cells)
        while dq:
            p = dq.popleft()
            for q in nbrs(p):
                if self.inside(q):
                    q = self.canon(q)
                    if q not in cells:
                        cells[q] = None; dq.append(q)
        self.cells = sorted(cells)
        self.index = {p: i for i, p in enumerate(self.cells)}
        self.n = n = len(self.cells)
        nb = np.full((n, 12), n, np.int32)
        for i, p in enumerate(self.cells):
            for k, q in enumerate(nbrs(p)):
                if self.inside(q):
                    nb[i, k] = self.index[self.canon(q)]
        self.nb = np.ascontiguousarray(nb)
        self.unit = None
        if unitvec is not None:
            m = self._q(tuple(2 * v for v in unitvec))
            assert m[1] == 0 and m[2] == 0 and m[0] > 0 and self.H[0][0] % m[0] == 0, (m, self.H)
            self.m = m[0]; self.N = self.H[0][0] // m[0]
            self.unit = np.array([self._q(p)[0] // self.m for p in self.cells], np.int32)
            # grid[u, l] = index of the cell that is local cell l of repeat u (local cell = cell modulo unitvec)
            base = [i for i in range(n) if self.unit[i] == 0]
            self.nloc = len(base); assert self.nloc * self.N == n
            self.grid = np.zeros((self.N, self.nloc), np.int64)
            for l, i in enumerate(base):
                p = self.cells[i]
                for u in range(self.N):
                    j = self.index[self.canon((p[0] + 2 * u * unitvec[0], p[1] + 2 * u * unitvec[1], p[2] + 2 * u * unitvec[2]))]
                    assert self.unit[j] == u
                    self.grid[u, l] = j

    def _q(self, p):
        """Cube index of the cell p (or half of an even vector), in the HNF-adapted coordinates."""
        c = (p[0] >> 1, p[1] >> 1, p[2] >> 1)
        U = self.U
        return [c[0] * U[0][j] + c[1] * U[1][j] + c[2] * U[2][j] for j in range(3)]

    def inside(self, p):
        for d, lo, hi in self.bounds:
            s = dot(d, p)
            if s < lo or s > hi:
                return False
        return True

    def canon(self, p):
        r = self._cache.get(p)
        if r is not None:
            return r
        a = axis(p)
        q = self._q(p)
        H = self.H
        for i in range(len(H) - 1, -1, -1):
            k = q[i] // H[i][i]
            if k:
                q = [q[j] - k * H[i][j] for j in range(3)]
        Ui = self.Ui
        c = [q[0] * Ui[0][j] + q[1] * Ui[1][j] + q[2] * Ui[2][j] for j in range(3)]
        r = [2 * c[0], 2 * c[1], 2 * c[2]]; r[a] += 1
        r = tuple(r)
        if len(self._cache) < 2000000:
            self._cache[p] = r
        return r

    # ---- states
    def state(self, cells):
        st = np.zeros(self.n + 1, np.uint8)
        for p in cells:
            assert self.inside(p), p
            st[self.index[self.canon(p)]] = 1
        return st

    def cells_of(self, st):
        return frozenset(self.cells[i] for i in np.nonzero(st[:self.n])[0])

    def run(self, st, g, sparse=False):
        st = st.copy()
        (lib().srun if sparse else lib().drun)(self.n, ptr(self.nb), ptr(st), g)
        return st

    def cycle(self, st, maxgen=1000000):
        """Run to a cycle.  Returns (period or 0, generation of detection, a state on the cycle)."""
        st = st.copy(); gen = ctypes.c_long()
        per = lib().dcycle(self.n, ptr(self.nb), ptr(st), maxgen, ctypes.byref(gen))
        return per, gen.value, st

    def orbit(self, st, g):
        out = [st]
        for _ in range(g):
            out.append(self.run(out[-1], 1, sparse=True))
        return out

    def track(self, bg, x, u0, span=None, maxgen=2000):
        """Run bg and x together; see sgc.c track().  Returns dict(ret, gens, per, lo, hi, cnt, bg, x)."""
        bg = bg.copy(); x = x.copy()
        lo = np.zeros(maxgen + 1, np.int32); hi = np.zeros(maxgen + 1, np.int32); cnt = np.zeros(maxgen + 1, np.int32)
        gens = ctypes.c_long(); per = ctypes.c_long()
        ret = lib().track(self.n, ptr(self.nb), ptr(bg), ptr(x), ptr(self.unit), self.N, int(u0),
                          int(span or self.N - 2), maxgen, ptr(lo), ptr(hi), ptr(cnt), ctypes.byref(gens), ctypes.byref(per))
        g = gens.value
        return dict(ret=ret, gens=g, per=per.value, lo=lo[:g + 1], hi=hi[:g + 1], cnt=cnt[:g + 1], bg=bg, x=x)

    def soups(self, nsoup, rho, seed, maxgen, mask=None, keep=True):
        mask = np.ones(self.n + 1, np.uint8) if mask is None else mask
        period = np.zeros(nsoup, np.int64); gen = np.zeros(nsoup, np.int64)
        states = np.zeros((nsoup, self.n + 1), np.uint8) if keep else None
        lib().soups(self.n, ptr(self.nb), ptr(mask), nsoup, float(rho), int(seed), int(maxgen), ptr(period), ptr(gen),
                    ptr(states) if keep else None)
        return period, gen, states

    def as_grid(self, st):
        """State as an N x nloc 0/1 array: row u is repeat u; np.roll(.., k, axis=0) is translation by k repeats."""
        return st[self.grid]

    def from_grid(self, M):
        st = np.zeros(self.n + 1, np.uint8); st[self.grid] = M
        return st

    def translate(self, st, g):
        """State translated by the cube vector g (must preserve the bounds)."""
        return self.state([(p[0] + 2 * g[0], p[1] + 2 * g[1], p[2] + 2 * g[2]) for p in self.cells_of(st)])


def lift_periodic(cells, periods, reps):
    """Copies of `cells` under k1 g1 + k2 g2 + ... for k_i in reps[i] (ranges): a finite piece of a periodic pattern."""
    out = set(cells)
    for g, rg in zip(periods, reps):
        out = {(p[0] + 2 * k * g[0], p[1] + 2 * k * g[1], p[2] + 2 * k * g[2]) for p in out for k in rg}
    return frozenset(out)
