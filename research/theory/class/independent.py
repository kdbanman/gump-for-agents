"""independent.py -- the two headline new gumps re-checked with array code that shares nothing with
lattices.py / vessel.py / gstep.c (plain numpy rolls).

  vn B2/S12   : boxes with a dead border; median lifetime of 64 soups at sides 9 and 13 (gstep: 110, 293; here the cycle start is
                only bracketed by snapshots at powers of two, so it is an upper bound within a factor 2),
                bounding-box confinement, torus density (gstep: 0.468)
  fcc B45/S345: even-parity sites of a cubic array, 12 neighbours = permutations of (+-1, +-1, 0);
                torus density after 600 generations (gstep: 0.394)
"""
import numpy as np

rng = np.random.default_rng(5)


def vn_step(x):
    n = np.zeros_like(x)
    n[1:, :] += x[:-1, :]; n[:-1, :] += x[1:, :]; n[:, 1:] += x[:, :-1]; n[:, :-1] += x[:, 1:]
    return (((n + x) >= 2) & (n <= 2)).astype(np.int8)


def vn_life(side, T=200000):
    """generation at which the final cycle is entered, to within the snapshot spacing (Brent-style snapshots)"""
    x = (rng.random((side, side)) < 0.47).astype(np.int8)
    snap, tsnap, nxt = x.copy(), 0, 1
    for t in range(1, T):
        x = vn_step(x)
        if np.array_equal(x, snap):
            return tsnap
        if t == nxt:
            snap, tsnap, nxt = x.copy(), t, 2 * t
    return T


for side, want in ((9, 110), (13, 293)):
    ls = sorted(vn_life(side) for _ in range(64))
    print(f"vn B2/S12 box side {side}: median lifetime {ls[32]} (gstep: {want}); quartiles {ls[16]}, {ls[48]}")

# confinement: a soup in a 12x12 box inside a 40x40 dead-bordered array never leaves the box
x = np.zeros((40, 40), np.int8); x[14:26, 14:26] = rng.random((12, 12)) < 0.5
out = 0
for t in range(400):
    x = vn_step(x); out += int(x.sum() - x[14:26, 14:26].sum())
print("vn B2/S12: live cells outside the seed's bounding box in 400 generations:", out)

# torus density
x = (rng.random((96, 96)) < 0.47).astype(np.int8); acc = []
for t in range(1200):
    n = sum(np.roll(x, s, a) for s in (1, -1) for a in (0, 1))
    x = (((n + x) >= 2) & (n <= 2)).astype(np.int8)
    if t >= 600: acc.append(x.mean())
print(f"vn B2/S12 torus 96x96: density {np.mean(acc):.3f} (gstep: 0.468)")

# FCC
N = 24
ii, jj, kk = np.indices((N, N, N))
site = ((ii + jj + kk) % 2 == 0)
offs = [(a, b, 0) for a in (1, -1) for b in (1, -1)] + [(a, 0, b) for a in (1, -1) for b in (1, -1)] + [(0, a, b) for a in (1, -1) for b in (1, -1)]
x = ((rng.random((N, N, N)) < 0.44) & site).astype(np.int8); acc = []
for t in range(600):
    n = sum(np.roll(x, o, (0, 1, 2)) for o in offs)
    x = (((n + x) >= 4) & (n <= 5) & site).astype(np.int8)
    if t >= 300: acc.append(x.sum() / site.sum())
print(f"fcc B45/S345 torus {N}^3/2 sites: density {np.mean(acc):.3f} (gstep: 0.394)")
