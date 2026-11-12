"""Vessel builders for vessel.c and ash classification.

Vessels (all exact for the infinite-lattice dynamics of patterns started inside them):
  octa(centre, r)   cells with |p - c|_1 <= r (T2: nothing outside can ever be born)
  slab(N, m)        m consecutive {111} layers (t = i+j+k in [0, m)) on an N x N in-plane torus,
                    identification (i,j,k) ~ (i+N, j, k-N) ~ (i, j+N, k-N) in cube indices (T4: closed).
                    m = 1 is the kagome automaton on a 3N^2-cell torus.
"""
import os, subprocess, struct, sys
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice import nbrs, step, canon, components, axis  # noqa: E402

BIN = os.path.join(HERE, '..', 'scratch', 'atlas', 'vessel')
CENTRES = {'cube': (0, 0, 0), 'vertex': (1, 1, 1), 'face': (1, 0, 0), 'edge': (1, 1, 0)}


def build_bin():
    os.makedirs(os.path.dirname(BIN), exist_ok=True)
    src = os.path.join(HERE, 'vessel.c')
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O2', '-o', BIN, src])


class Vessel:
    def __init__(self, cells, nbr_index, flags=None, coords=None, torus=None):
        self.cells = cells                  # list of doubled coords (representatives)
        self.nb = np.asarray(nbr_index, np.int32)
        self.flags = np.ones(len(cells), np.int32) if flags is None else np.asarray(flags, np.int32)
        self.torus = torus

    def write(self, path):
        with open(path, 'wb') as f:
            f.write(struct.pack('i', len(self.cells)))
            f.write(self.nb.astype('<i4').tobytes())
            f.write(self.flags.astype('<i4').tobytes())

    def run(self, path, nsoups, rho, seed, maxgen, cells=True, stride=0):
        build_bin()
        self.write(path)
        cmd = [BIN, path, str(nsoups), str(rho), str(seed), str(maxgen)] + (['-c'] if cells else []) + \
              (['-p', str(stride)] if stride else [])
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
        res, trace = [], []
        for line in out.splitlines():
            if line.startswith('T '):
                _, i, g, p = line.split(); trace.append((int(i), int(g), int(p))); continue
            head, _, tail = line.partition(':')
            i, mu, per, pop = map(int, head.split())
            live = [int(v) for v in tail.split()] if cells else None
            res.append(dict(id=i, mu=mu, period=per, pop=pop, live=live))
        return (res, trace) if stride else res


def octa(centre, r):
    c = CENTRES[centre] if isinstance(centre, str) else centre
    cells = []
    for x in range(c[0] - r - 1, c[0] + r + 2):
        for y in range(c[1] - r - 1, c[1] + r + 2):
            for z in range(c[2] - r - 1, c[2] + r + 2):
                if (x & 1) + (y & 1) + (z & 1) == 1 and abs(x - c[0]) + abs(y - c[1]) + abs(z - c[2]) <= r:
                    cells.append((x, y, z))
    idx = {p: i for i, p in enumerate(cells)}
    nb = [[idx.get(q, -1) for q in nbrs(p)] for p in cells]
    return Vessel(cells, nb)


def slab(N, m, init_layers=None):
    """m-layer slab on an N x N in-plane torus.  Cell key (i mod N, j mod N, t, a)."""
    keys, cells = [], []
    for t in range(m):
        for i in range(N):
            for j in range(N):
                k = t - i - j
                for a in range(3):
                    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
                    keys.append((i, j, t, a)); cells.append(tuple(p))
    idx = {kk: n for n, kk in enumerate(keys)}

    def key_of(q):
        a = axis(q); c = [(q[d] - (1 if d == a else 0)) // 2 for d in range(3)]
        t = c[0] + c[1] + c[2]
        if t < 0 or t >= m:
            return None
        return (c[0] % N, c[1] % N, t, a)

    nb = []
    for p in cells:
        row = []
        for q in nbrs(p):
            kq = key_of(q)
            row.append(-1 if kq is None else idx[kq])
        nb.append(row)
    flags = None
    if init_layers is not None:
        flags = [1 if kk[2] in init_layers else 0 for kk in keys]
    v = Vessel(cells, nb, flags, torus=N)
    v.keys = keys
    return v


def unwrap_component(v, comp):
    """Unwrap a set of cell indices of a torus vessel into true lattice coordinates (BFS via offsets)."""
    comp = set(comp)
    start = next(iter(comp))
    pos = {start: v.cells[start]}
    stack = [start]
    # build a map from neighbour slot to offset
    while stack:
        u = stack.pop(); pu = pos[u]
        for q, w in zip(nbrs(pu), v.nb[u]):
            if w >= 0 and w in comp and w not in pos:
                pos[w] = q; stack.append(w)
    return pos


def classify_final(v, live, period, torus=False):
    """Split a final cycle state (cell indices) into R-connected objects (distance <= 2 in the union of
    phases); return list of (period_of_object, key) where key = min over phases of canon(phase)."""
    if not live:
        return []
    if not torus:
        S = frozenset(v.cells[i] for i in live)
        phases = [S]
        for _ in range(max(period, 1) - 1):
            phases.append(step(phases[-1]))
        assert step(phases[-1]) == S, 'cycle does not close in the infinite lattice'
        U = frozenset().union(*phases)
        objs = []
        for comp in components(U, 2):
            ph = [p & comp for p in phases]
            per = next(d for d in range(1, len(ph) + 1) if len(ph) % d == 0 and all(ph[(t + d) % len(ph)] == ph[t] for t in range(len(ph))))
            objs.append((per, min(canon(p) for p in ph[:per] if p) if any(ph) else ()))
        return objs
    # torus: phases via index dynamics, then unwrap R-components of the union
    nbm = v.nb
    def tstep(s):
        cnt = Counter()
        for i in s:
            for j in nbm[i]:
                if j >= 0: cnt[j] += 1
        return frozenset(j for j, c in cnt.items() if c in (4, 5) or (c == 3 and j in s))
    S = frozenset(live); phases = [S]
    for _ in range(max(period, 1) - 1):
        phases.append(tstep(phases[-1]))
    U = frozenset().union(*phases)
    # R-components on the index graph
    seen, objs = set(), []
    for c0 in U:
        if c0 in seen: continue
        comp, st = [], [c0]; seen.add(c0)
        while st:
            u = st.pop(); comp.append(u)
            near = set(j for j in nbm[u] if j >= 0)
            near |= set(k for j in list(near) for k in nbm[j] if k >= 0)
            for w in near:
                if w in U and w not in seen: seen.add(w); st.append(w)
        # unwrap via the union's neighbour+distance-2 structure: BFS over neighbours within the union plus dead links
        pos = {comp[0]: v.cells[comp[0]]}; st = [comp[0]]; cs = set(comp)
        while st:
            u = st.pop(); pu = pos[u]
            for q, w in zip(nbrs(pu), nbm[u]):
                if w < 0: continue
                for q2, w2 in [(q, w)] + list(zip(nbrs(q), nbm[w])):
                    if w2 >= 0 and w2 in cs and w2 not in pos:
                        pos[w2] = q2; st.append(w2)
        ph = [frozenset(pos[i] for i in p if i in cs) for p in phases]
        L = len(ph)
        per = next(d for d in range(1, L + 1) if L % d == 0 and all(ph[(t + d) % L] == ph[t] for t in range(L)))
        if per > 1 or True:
            # sanity: the unwrapped object must follow the infinite-lattice rule (fails if it wraps the torus)
            ok = all(step(ph[t]) == ph[(t + 1) % L] for t in range(L))
        objs.append((per if ok else -per, min(canon(p) for p in ph[:per] if p)))
    return objs
