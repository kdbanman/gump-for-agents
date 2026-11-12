#!/usr/bin/env python3
"""Vessels (finite cell graphs) for rep.c, and a runner that returns per-replica layer last-alive times.

Geometries (doubled coordinates; a cell has exactly one odd coordinate):
  slab(N, m, N2) m {111} layers (normal d0=(1,1,1)) on a skewed N x N2 in-plane torus (periods (N,0,-N), (0,N2,-N2)
                in cubes): two flat faces, no edges, no corners; 3*N*N2 cells per layer, independent of m.
  torus(N, m)   cubic N^3 torus (gump's --torus N); m = None: whole torus, else an m-layer slab soup in it.
  octa(R, sym)  open-space octahedron |p|_1 <= R (= its own diagonal hull, exact by T2); sym=True: O_h-symmetric soup
                about the origin (a cube centre).
Layers: list of (diag, s) with the cell indices of that {111} layer (s taken mod the period on tori).
"""
import itertools, os, struct, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REP = os.path.join(HERE, '..', 'scratch', 'peeling', 'rep')
DIAGS = [(1, 1, 1), (-1, 1, 1), (1, -1, 1), (1, 1, -1)]


def build_rep():
    src = os.path.join(HERE, 'rep.c')
    if not os.path.exists(REP) or os.path.getmtime(REP) < os.path.getmtime(src):
        os.makedirs(os.path.dirname(REP), exist_ok=True)
        subprocess.check_call(['gcc', '-O3', '-march=native', '-o', REP + '.new', src])
        os.replace(REP + '.new', REP)   # atomic: running copies keep the old binary


def nbr_offsets(p):
    a = next(i for i in range(3) if p[i] % 2)
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            v = [0, 0, 0]; v[b] = sb; v[c] = sc; out.append(v)
    for o in (b, c):
        for sa in (1, -1):
            for so in (1, -1):
                v = [0, 0, 0]; v[a] = sa; v[o] = so; out.append(v)
    return out


class Vessel:
    def __init__(self, cells, canon, orbit, layers, name):
        """cells: list of doubled coords; canon(q) -> index or None (dead forever); orbit: list (-1 = never live)."""
        self.cells, self.orbit, self.layers, self.name = cells, orbit, layers, name
        self.nb = np.full((len(cells), 12), -1, np.int32)
        for i, p in enumerate(cells):
            for k, v in enumerate(nbr_offsets(p)):
                j = canon((p[0] + v[0], p[1] + v[1], p[2] + v[2]))
                self.nb[i, k] = -1 if j is None else j

    def write(self, path):
        with open(path, 'wb') as f:
            f.write(struct.pack('<i', len(self.cells)))
            f.write(self.nb.astype('<i4').tobytes())
            f.write(np.asarray(self.orbit, '<i4').tobytes())
            f.write(struct.pack('<i', len(self.layers)))
            for _, idx in self.layers:
                f.write(struct.pack('<i', len(idx)))
                f.write(np.asarray(idx, '<i4').tobytes())

    def run(self, W, p, seed, cap, K, extra=()):
        """Returns (settle[R], pop[R], la[R, nL]) as numpy arrays; also sets self.lc2 and self.gen_end."""
        build_rep()
        path = os.path.join(HERE, '..', 'scratch', 'peeling', f'v_{self.name}_{os.getpid()}.bin')
        self.write(path)
        pr = subprocess.run([REP, path, str(W), str(p), str(seed), str(cap), str(K), *extra],
                            capture_output=True, text=True, check=True)
        out = pr.stdout
        self.gen_end = int(pr.stderr.split()[-1])
        os.remove(path)
        rows = [list(map(int, l.split())) for l in out.splitlines() if not l.startswith('T')]
        arr = np.array(rows, dtype=np.int64)
        self.lc2 = arr[:, 3]
        st = arr[:, 1]
        # refine: a replica that is periodic with period 1 or 2 settled at its last change w.r.t. t-2 (to K)
        st = np.where(st >= 0, np.minimum(st, self.lc2), -1)
        return st, arr[:, 2], arr[:, 4:]


def _layers(cells, mod=None):
    lay = {}
    for i, p in enumerate(cells):
        for d, v in enumerate(DIAGS):
            s = v[0] * p[0] + v[1] * p[1] + v[2] * p[2]
            if mod:
                s %= mod
            lay.setdefault((d, s), []).append(i)
    return [(k, lay[k]) for k in sorted(lay)]


def slab(N, m, N2=None):
    N2 = N2 or N
    cells, idx = [], {}
    for t in range(m):
        for i in range(N):
            for j in range(N2):
                k = t - i - j
                for a in range(3):
                    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
                    idx[(i, j, t, a)] = len(cells); cells.append(tuple(p))

    def canon(q):
        a = next(x for x in range(3) if q[x] % 2)
        c = [(q[x] - (1 if x == a else 0)) // 2 for x in range(3)]
        t = sum(c)
        if not 0 <= t < m:
            return None
        return idx[(c[0] % N, c[1] % N2, t, a)]
    # d0 layers exact; transverse diagonals periodic mod 4N
    lay = {}
    for i, p in enumerate(cells):
        for d, v in enumerate(DIAGS):
            s = v[0] * p[0] + v[1] * p[1] + v[2] * p[2]
            if d:
                s %= [0, 4 * N, 4 * N2, 4 * int(np.gcd(N, N2))][d]
            lay.setdefault((d, s), []).append(i)
    layers = [(k, lay[k]) for k in sorted(lay)]
    return Vessel(cells, canon, list(range(len(cells))), layers, f'slab{N}x{N2}_{m}')


def torus(N, m=None):
    cells, idx = [], {}
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for a in range(3):
                    p = [2 * i, 2 * j, 2 * k]; p[a] += 1
                    idx[tuple(p)] = len(cells); cells.append(tuple(p))

    def canon(q):
        return idx[tuple(x % (2 * N) for x in q)]
    orbit = list(range(len(cells)))
    if m is not None:  # slab soup: layers t = 0..m-1 along d0, t = (i+j+k) mod N
        for n_, p in enumerate(cells):
            t = ((p[0] + p[1] + p[2] - 1) // 2) % N
            if t >= m:
                orbit[n_] = -1
    return Vessel(cells, canon, orbit, _layers(cells, 2 * N), f'torus{N}_{m}')


OH = [(perm, sg) for perm in itertools.permutations(range(3)) for sg in itertools.product((1, -1), repeat=3)]


def octa(R, sym=False):
    cells, idx = [], {}
    rng = range(-R, R + 1)
    for x in rng:
        for y in rng:
            for z in rng:
                if abs(x) + abs(y) + abs(z) <= R and (x % 2) + (y % 2) + (z % 2) == 1:
                    idx[(x, y, z)] = len(cells); cells.append((x, y, z))

    def canon(q):
        return idx.get(tuple(q))
    if sym:
        orbit, oid = [], {}
        for p in cells:
            key = min(tuple(sg[k] * p[perm[k]] for k in range(3)) for perm, sg in OH)
            orbit.append(oid.setdefault(key, len(oid)))
    else:
        orbit = list(range(len(cells)))
    return Vessel(cells, canon, orbit, _layers(cells), f'octa{R}_{int(sym)}')


if __name__ == '__main__':
    v = slab(4, 6)
    print(len(v.cells), len(v.layers), [(k, len(i)) for k, i in v.layers[:8]])
