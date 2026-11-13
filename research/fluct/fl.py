"""fl: driver for fl.c (bit-sliced replicas of gump on a finite cell graph) + vessels + gump I/O.

A vessel is the exact diagonal hull {p : lo_d <= d.p <= hi_d, d = 4 diagonals} (exact forever by T2), as a
cell graph; with sym=True it is reduced to O_h orbits about a centre c (one graph node per orbit), which is exact
for O_h-symmetric states (gump preserves symmetry) and 48x cheaper.

Groups: for every one of the 8 faces (d, +/-) its outer layer and the layer below ("sub"); with sym only the
d0+ face (all 8 are images). Weighted counts are in cells, so they are directly face populations n.
"""
import ctypes, itertools, json, os, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
GUMP = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
SCR = os.path.join(ROOT, 'research', 'scratch', 'fluct')
os.makedirs(SCR, exist_ok=True)
DIAGS = np.array([(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)])
OH = [(perm, sg) for perm in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)]


def nbr_offsets(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for o in (b, c):
        for sa in (1, -1):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(v)
    return np.array(out)


OFFS = [nbr_offsets(a) for a in range(3)]


def octa_hull(R, centre='c'):
    """hull (4 x [lo, hi]) of the soup region |p - c|_1 <= R, c = 0 ('c') or (1,1,1) ('v')."""
    c = np.zeros(3, int) if centre == 'c' else np.ones(3, int)
    cells = all_cells_box(R + 2, c)
    cells = cells[np.abs(cells - c).sum(1) <= R]
    s = cells @ DIAGS.T
    return [[int(s[:, d].min()), int(s[:, d].max())] for d in range(4)]


def all_cells_box(h, c):
    r = np.arange(-h, h + 1)
    g = np.stack(np.meshgrid(r, r, r, indexing='ij'), -1).reshape(-1, 3) + c
    return g[(g % 2).sum(1) == 1]


def area(R, centre='c'):
    h = octa_hull(R, centre)
    v = Vessel(h, centre, sym=False, build=False)
    return v.A


class Vessel:
    def __init__(self, hull, centre='c', sym=False, build=True):
        self.hull, self.centre, self.sym = hull, centre, sym
        c = np.zeros(3, int) if centre == 'c' else np.ones(3, int)
        self.c = c
        h = max(max(abs(a), abs(b)) for a, b in hull) + 2
        cells = all_cells_box(h, c)
        s = cells @ DIAGS.T
        ok = np.all([(s[:, d] >= hull[d][0]) & (s[:, d] <= hull[d][1]) for d in range(4)], axis=0)
        cells = cells[ok]; s = s[ok]
        self.cells = cells
        top = s[:, 0] == hull[0][1]
        self.A = int(top.sum())
        if not build:
            return
        index = {tuple(p): i for i, p in enumerate(cells)}
        N = len(cells)
        if sym:
            q = cells - c
            keys = []
            for perm, sg in OH:
                keys.append(q[:, perm] * np.array(sg))
            K = np.stack(keys, 0)                      # 48 x N x 3
            # canonical = lexicographic min over images
            flat = (K[..., 0] + 512) * 1048576 + (K[..., 1] + 512) * 1024 + (K[..., 2] + 512)
            canon = flat.min(0)
            uniq, orb = np.unique(canon, return_inverse=True)
            self.orbit_of = orb                        # cell -> orbit
            no = len(uniq)
            rep = np.zeros(no, int); rep[orb[::-1]] = np.arange(N)[::-1]   # first cell of each orbit
            self.rep = rep
            self.osize = np.bincount(orb, minlength=no)
            nodes = cells[rep]
            node_of_cell = orb
        else:
            nodes = cells; node_of_cell = np.arange(N); self.orbit_of = node_of_cell
            self.osize = np.ones(N, int)
        self.n = len(nodes)
        nb = np.full((self.n, 12), -1, np.int32)
        for i, p in enumerate(nodes):
            a = int(np.argmax(p % 2))
            for k, v in enumerate(OFFS[a]):
                j = index.get(tuple(p + v))
                if j is not None:
                    nb[i, k] = node_of_cell[j]
        self.nb = nb
        # groups
        groups, names = [], []
        faces = [(d, sgn) for d in range(4) for sgn in (1, -1)] if not sym else [(0, 1)]
        for d, sgn in faces:
            for depth in (0, 1):
                sv = hull[d][1] - 2 * depth if sgn > 0 else hull[d][0] + 2 * depth
                sel = np.nonzero(s[:, d] == sv)[0]
                w = np.bincount(node_of_cell[sel], minlength=self.n)
                idx = np.nonzero(w)[0]
                groups.append((idx.astype(np.int32), w[idx].astype(np.int32)))
                names.append((d, sgn, depth))
        self.groups, self.gnames = groups, names
        self.face_groups = [i for i, (d, sg, dep) in enumerate(names) if dep == 0]
        self.sub_groups = [i for i, (d, sg, dep) in enumerate(names) if dep == 1]
        self.depth = None

    def node_depth(self):
        """min over the 8 faces of the layer distance (in layers) of each node from that face."""
        if self.depth is None:
            q = self.cells[self.rep] if self.sym else self.cells
            s = q @ DIAGS.T
            dd = np.min([np.minimum(self.hull[d][1] - s[:, d], s[:, d] - self.hull[d][0]) for d in range(4)], axis=0) // 2
            self.depth = dd
        return self.depth


_lib = None


def lib():
    global _lib
    if _lib is None:
        so = os.path.join(SCR, 'fl.so'); src = os.path.join(HERE, 'fl.c')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-o', so + '.new', src])
            os.replace(so + '.new', so)
        L = ctypes.CDLL(so)
        P = np.ctypeslib.ndpointer
        L.fl_init.restype = ctypes.c_int
        L.fl_init.argtypes = [ctypes.c_int, ctypes.c_int, P(np.int32), ctypes.c_int, P(np.int32), P(np.int32), P(np.int32),
                              ctypes.c_int, P(np.int32), P(np.int32)]
        L.fl_state.restype = ctypes.POINTER(ctypes.c_uint64)
        L.fl_age.restype = ctypes.POINTER(ctypes.c_uint32)
        L.fl_seed.argtypes = [ctypes.c_uint64]
        L.fl_counts.argtypes = [P(np.uint16)]
        L.fl_run.restype = ctypes.c_long
        L.fl_run.argtypes = [ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double]
        L.fl_run_until.restype = ctypes.c_long
        L.fl_run_until.argtypes = [ctypes.c_long, P(np.int32), P(np.int32), P(np.int32), P(np.int32), P(np.int32)]
        _lib = L
    return _lib


class Sim:
    def __init__(self, v, W=1, seed=1, seedable=None):
        self.v, self.W, self.R = v, W, 64 * W
        L = lib()
        gsz = np.array([len(g[0]) for g in v.groups], np.int32)
        gc = np.concatenate([g[0] for g in v.groups]).astype(np.int32)
        gw = np.concatenate([g[1] for g in v.groups]).astype(np.int32)
        fg = np.array(v.face_groups, np.int32)
        sd = np.ones(v.n, np.int32) if seedable is None else seedable.astype(np.int32)
        self.B = L.fl_init(v.n, W, np.ascontiguousarray(v.nb, np.int32), len(gsz), gsz, gc, gw, len(fg), fg, sd)
        assert self.B > 0
        L.fl_seed(seed)
        self.state = np.ctypeslib.as_array(L.fl_state(), shape=((v.n + 1), W))
        self.age = np.ctypeslib.as_array(L.fl_age(), shape=(self.R,))
        self.G = len(gsz)

    def counts(self):
        out = np.zeros((self.G, self.R), np.uint16); lib().fl_counts(out); return out

    def m(self):
        return self.counts()[self.v.face_groups].min(0)

    def run(self, gens, record=True, reseed_p=0.0, ages=False):
        c = np.zeros((gens, self.G, self.R), np.uint16) if record else None
        a = np.zeros((gens, self.R), np.uint32) if ages else None
        nres = lib().fl_run(gens, c.ctypes.data if record else None, a.ctypes.data if ages else None, reseed_p)
        return c, a, nres

    def run_until(self, maxgens, lo, hi):
        sg = np.zeros(self.R, np.int32); sm = np.zeros(self.R, np.int32); mm = np.zeros(self.R, np.int32)
        lib().fl_run_until(maxgens, np.ascontiguousarray(lo, np.int32), np.ascontiguousarray(hi, np.int32), sg, sm, mm)
        return sg, sm, mm

    # replica access: a replica's state is a bool vector over nodes
    def get(self, r):
        return ((self.state[:self.v.n, r // 64] >> np.uint64(r % 64)) & np.uint64(1)).astype(bool)

    def set(self, r, bits):
        w, b = r // 64, np.uint64(r % 64)
        col = self.state[:self.v.n, w]
        col &= ~(np.uint64(1) << b)
        col |= bits.astype(np.uint64) << b

    def get_all(self):
        """(R, n) bool"""
        n = self.v.n
        by = self.state[:n].view(np.uint8).reshape(n, self.W * 8)
        return np.unpackbits(by, axis=1, bitorder='little').T.astype(bool)

    def set_all(self, bits):
        n = self.v.n
        assert bits.shape == (self.R, n)
        by = np.packbits(bits.T, axis=1, bitorder='little')       # n x 8W
        self.state[:n] = by.view(np.uint64).reshape(n, self.W)
        self.state[n] = 0

    def flip(self, r, node):
        self.state[node, r // 64] ^= np.uint64(1) << np.uint64(r % 64)


# ---------- gump I/O ----------

def gump_cells(args, gens, tag):
    """run gump with args for gens generations, return (cells as int array, summary dict)."""
    f = os.path.join(SCR, f'cells_{tag}_{os.getpid()}.txt')
    out = subprocess.run([GUMP, 'run', *args, '--gens', str(gens), '--no-halt', '--cells-out', f], capture_output=True, text=True, check=True).stdout
    summ = json.loads(out.strip().splitlines()[-1])
    cells = np.loadtxt(f, dtype=int, comments='#', ndmin=2)
    os.remove(f)
    return cells, summ


def bits_from_cells(v, cells):
    """bool vector over v's nodes; for sym vessels checks that the cell set is a union of orbits."""
    index = {tuple(p): i for i, p in enumerate(v.cells)}
    live = np.zeros(len(v.cells), bool)
    for p in cells:
        live[index[tuple(p)]] = True        # KeyError = a live cell outside the vessel
    if not v.sym:
        return live
    o = v.orbit_of
    cnt = np.bincount(o, weights=live, minlength=v.n)
    assert np.all((cnt == 0) | (cnt == v.osize)), 'state is not O_h-symmetric about the centre'
    return cnt > 0


def cells_from_bits(v, bits):
    live = bits[v.orbit_of] if v.sym else bits
    return v.cells[live]
