"""Mirror-plane depletion: symmetric soups on a torus, site classes, orbit mean field.

Point groups act on doubled coordinates about the origin, mod 2N (so each mirror has two
parallel copies on the torus, at 0 and N cubes). Subgroups of O_h used here:
  oh (48), th (24: coordinate mirrors x->-x etc. + 3-fold, no diagonal mirrors),
  td (24: diagonal mirrors x<->y etc., no coordinate mirrors), d2h (8: the 3 coordinate mirrors), c1.
A site's class = (number of coordinate mirrors, number of diagonal mirrors) in its stabiliser.

usage: python3 sym.py soup  GROUP N P RNG OUT.gump      symmetric soup snapshot (feed to the engine)
       python3 sym.py classes GROUP N SNAP [SNAP ...]   time-averaged density per site class (+ distance profile)
       python3 sym.py mf GROUP N                         orbit mean field per site class
"""
import sys, os, itertools, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import gl
from scipy.stats import betabinom

def ops(group):
    out = []
    for perm in itertools.permutations(range(3)):
        P = np.zeros((3, 3), int)
        for r, c in enumerate(perm):
            P[r, c] = 1
        even = np.linalg.det(P) > 0
        for sg in itertools.product((1, -1), repeat=3):
            M = np.diag(sg) @ P
            prod = sg[0] * sg[1] * sg[2]
            ok = {'oh': True, 'th': even, 'td': prod == 1, 'd2h': perm == (0, 1, 2), 'c1': perm == (0, 1, 2) and prod == 1 and sg == (1, 1, 1)}[group]
            if ok:
                out.append(M)
    return out

def is_coord_mirror(M):
    return np.array_equal(M, np.diag(np.diag(M))) and sorted(np.diag(M)) == [-1, 1, 1]

def is_diag_mirror(M):
    # reflection (det -1, M^2 = I, trace 1) that is not diagonal: x<->y or x<->-y type
    return round(np.linalg.det(M)) == -1 and np.trace(M) == 1 and not is_coord_mirror(M) and np.array_equal(M @ M, np.eye(3, dtype=int))

def cell_coords(N):
    a, i, j, k = np.meshgrid(np.arange(3), np.arange(N), np.arange(N), np.arange(N), indexing='ij')
    P = 2 * np.stack([i, j, k], -1) + np.eye(3, dtype=int)[a]
    return P  # shape (3,N,N,N,3) doubled coords

def index_of(P, N):
    """doubled coords (mod 2N) -> flat index into V (3,N,N,N)."""
    P = P % (2 * N)
    a = np.argmax(P % 2, axis=-1)
    c = P // 2
    return ((a * N + c[..., 0]) * N + c[..., 1]) * N + c[..., 2]

def orbit_ids(group, N):
    P = cell_coords(N).reshape(-1, 3)
    imgs = np.stack([index_of(P @ M.T, N) for M in ops(group)])
    return imgs.min(0), imgs

def site_class(group, N):
    P = cell_coords(N).reshape(-1, 3)
    own = index_of(P, N)
    nc = np.zeros(len(P), int); nd = np.zeros(len(P), int)
    for M in ops(group):
        fixed = index_of(P @ M.T, N) == own
        if is_coord_mirror(M):
            nc += fixed
        elif is_diag_mirror(M):
            nd += fixed
    return nc, nd

def mirror_distance(group, N):
    """distance (doubled units, min image) from each cell to the nearest mirror plane of the group."""
    P = cell_coords(N).reshape(-1, 3).astype(float)
    d = np.full(len(P), np.inf)
    for M in ops(group):
        if is_coord_mirror(M) or is_diag_mirror(M):
            n = (np.eye(3) - M)[np.argmax(np.abs(np.eye(3) - M).sum(1))]
            n = n / np.linalg.norm(n)
            # planes n.x = 0 mod the lattice of mirror copies; brute force over a few translates
            best = np.full(len(P), np.inf)
            for t in itertools.product((-1, 0, 1), repeat=3):
                x = P + 2 * N * np.array(t)
                best = np.minimum(best, np.abs(x @ n))
            d = np.minimum(d, best)
    return d

NB = {}
for a in range(3):
    b, c = (a + 1) % 3, (a + 2) % 3
    e = np.eye(3, dtype=int)
    NB[a] = [sb * 2 * e[b] + sc * 2 * e[c] for sb in (1, -1) for sc in (1, -1)] + \
            [sa * e[a] + sx * e[x] for sa in (1, -1) for x in (b, c) for sx in (1, -1)]

def mf(group, N, iters=600):
    """Orbit mean field: every orbit of the group is one independent Bernoulli variable.
    A site's live-neighbour count is sum over Stab-orbits of its neighbourhood of m * x_orbit.
"""
    oid, _ = orbit_ids(group, N)
    P = cell_coords(N).reshape(-1, 3)
    a = np.argmax(P % 2, axis=-1)
    # for each site: neighbour orbit ids with multiplicities
    nb_idx = np.zeros((len(P), 12), int)
    for ax in range(3):
        m = a == ax
        for r, off in enumerate(NB[ax]):
            nb_idx[m, r] = index_of(P[m] + off, N)
    nb_orb = oid[nb_idx]
    uniq_orbits, inv = np.unique(oid, return_inverse=True)
    rho = np.full(len(uniq_orbits), 0.4)
    tb = np.zeros(13); tb[[4, 5]] = 1; ts = np.zeros(13); ts[[3, 4, 5]] = 1
    # per site, group neighbour orbits: list of (orbit, multiplicity)
    groups = []
    for s in range(len(P)):
        u, c = np.unique(nb_orb[s], return_counts=True)
        groups.append((np.searchsorted(uniq_orbits, u), c))
    # representative site per orbit
    rep = np.zeros(len(uniq_orbits), int)
    rep[inv] = np.arange(len(P))
    hist = []
    for it in range(iters):
        new = np.empty_like(rho)
        for o in range(len(uniq_orbits)):
            g, c = groups[rep[o]]
            dist = np.zeros(13); dist[0] = 1
            for oo, m in zip(g, c):
                q = rho[oo]
                d2 = np.zeros(13)
                d2[:13 - m] += dist[:13 - m] * (1 - q)
                d2[m:] += dist[:13 - m] * q
                dist = d2
            r = rho[o]
            new[o] = (1 - r) * (dist * tb).sum() + r * (dist * ts).sum()
        rho = new
        hist.append(rho.copy())
    return np.mean(hist[iters // 2:], 0)[inv]   # time average over the (period-4) mean-field cycle

if __name__ == '__main__':
    mode, group, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
    if mode == 'soup':
        p, rng = float(sys.argv[4]), int(sys.argv[5])
        oid, _ = orbit_ids(group, N)
        r = np.random.default_rng(rng).random(3 * N ** 3)
        V = (r[oid] < p).reshape(3, N, N, N)
        gl.write_snapshot(sys.argv[6], V)
        print('pop', int(V.sum()), 'orbits', len(np.unique(oid)))
    elif mode == 'classes':
        nc, nd = site_class(group, N)
        dist = mirror_distance(group, N)
        acc = np.zeros(3 * N ** 3); k = 0
        for f in sys.argv[4:]:
            V, _ = gl.read_snapshot(f); acc += V.reshape(-1); k += 1
        rho = acc / k
        out = {'group': group, 'N': N, 'snaps': k, 'classes': {}, 'profile': {}}
        for c in sorted(set(zip(nc, nd))):
            m = (nc == c[0]) & (nd == c[1])
            out['classes'][f'{c[0]}c{c[1]}d'] = [float(rho[m].mean()), int(m.sum())]
        db = np.round(dist).astype(int)
        for d in range(0, 9):
            m = db == d
            if m.any():
                out['profile'][d] = [float(rho[m].mean()), int(m.sum())]
        print(json.dumps(out))
    elif mode == 'mf':
        rho = mf(group, N)
        nc, nd = site_class(group, N)
        res = {}
        for c in sorted(set(zip(nc, nd))):
            m = (nc == c[0]) & (nd == c[1])
            res[f'{c[0]}c{c[1]}d'] = [round(float(rho[m].mean()), 4), int(m.sum())]
        print(json.dumps({'group': group, 'N': N, 'mf': res}))
