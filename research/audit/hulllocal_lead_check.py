"""Lead's own check of the hull-density study's key number (research/hulllocal, 2026-11-16): the face layer in the
interior of a living octahedral hull is occupied as a wrapped face is (0.5177), not 0.012 more as the tube
relation would ask if it joined the two prices.

Here: reference/oracle.py only, and geometry written here from the oracle's own array.  A 0.4 soup inside the
octahedron max over the eight sign patterns s of s.(x, y, z) <= M, with M chosen so that each outermost layer
(s.(x, y, z) = M) holds 108 cells: the hull of radius 15.  Layers of a face are the distinct values of its
s.(x, y, z), counted from the outside (rank 0 = the face layer).  For a cell of a face layer, depth = the smallest
rank it has in any other face's layers (0: an edge or corner cell).  Burn-in 1,000 generations, then GENS
measured; every face layer must stay alive throughout.  Density of the face layers by depth, eight faces pooled;
error from the scatter of the eight faces and SEEDS runs.

    python3 research/audit/hulllocal_lead_check.py [GENS] [SEED]        (default 6000 1; about 8 min)
"""
import itertools, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import oracle

GENS = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 1
H = 96
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
c = np.indices((H, H, H)) - H // 2
SIG = [np.array(s) for s in itertools.product((1, -1), repeat=3)]
S = [s[0] * c[0] + s[1] * c[1] + s[2] * c[2] for s in SIG]
smax = np.max(S, axis=0)
M = next(M for M in range(10, 44) if all(int((valid & (smax <= M) & (S[i] == M)).sum()) == 108 for i in range(8)))
inside = valid & (smax <= M)
vals = [np.unique(S[i][inside])[::-1] for i in range(8)]
step = int(vals[0][0] - vals[0][1])
rank = [(M - S[i]) // step for i in range(8)]
print(f'M = {M}: {int(inside.sum())} cells in the hull, 108 in each outermost layer, layers {step} apart', flush=True)
face = [inside & (S[i] == M) for i in range(8)]
depth = []
for i in range(8):
    d = np.full((H, H, H), 99)
    for j in range(8):
        if j != i:
            d = np.minimum(d, rank[j])
    depth.append(d)
bins = [('edge and corner cells, depth 0', 0, 0), ('depth 1', 1, 1), ('depth 2', 2, 2), ('depth 3 and 4', 3, 4),
        ('depth 3 and more', 3, 98), ('depth 5 and more', 5, 98)]
sel = {b[0]: [face[i] & (depth[i] >= b[1]) & (depth[i] <= b[2]) for i in range(8)] for b in bins}
rng = np.random.default_rng(SEED)
x = inside & (rng.random((H, H, H)) < 0.4)
tot = {b[0]: np.zeros(8) for b in bins}
for g in range(1000 + GENS):
    x = oracle.step(x, m)
    if g % 250 == 0:
        assert not (x & ~inside).any(), 'a cell outside the hull is alive'
        assert all(x[face[i]].any() for i in range(8)), f'a face layer is empty at generation {g}'
    if g >= 1000:
        for k in tot:
            for i in range(8):
                tot[k][i] += x[sel[k][i]].sum()
W = 0.517742
for name, lo, hi in bins:
    n = int(sel[name][0].sum())
    per = tot[name] / (GENS * n)
    print(f'{name:32s} {n:3d} cells per face: density {per.mean():.5f} +- {per.std(ddof=1) / np.sqrt(8):.5f}   '
          f'minus the wrapped face\'s {W}: {per.mean() - W:+.5f}', flush=True)
