#!/usr/bin/env python3
"""States of reference/oracle.py for the Lean stepper to be compared with (state for state).

    python3 research/blast/lean/oracle_states.py OUT SEED GENS [HALF=5] [DENSITY=0.4] [H=96]

A soup: every valid cell with all three doubled coordinates within HALF of the centre of an H^3 array is alive
with probability DENSITY (numpy default_rng(SEED)). The pattern's diagonal hull has L1 radius at most 3*HALF about
the centre, so with 3*HALF < H/2 - 4 the oracle's array-index torus never matters (T2) and the run is the run on the
infinite lattice. Written: "G g n" then n lines "x y z" (array indices = doubled coordinates), g = 0 .. GENS.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'reference'))
import oracle

out, seed, gens = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
half = int(sys.argv[4]) if len(sys.argv) > 4 else 5
dens = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
H = int(sys.argv[6]) if len(sys.argv) > 6 else 96
assert H % 2 == 0 and 3 * half < H // 2 - 4
m = oracle.masks(H)
valid = m[0] | m[1] | m[2]
c = H // 2
box = np.zeros((H, H, H), bool); box[c - half:c + half + 1, c - half:c + half + 1, c - half:c + half + 1] = True
rng = np.random.default_rng(seed)
h = ((rng.random((H, H, H)) < dens) & valid & box).astype(np.int8)
with open(out, 'w') as f:
    for g in range(gens + 1):
        pts = np.argwhere(h == 1)
        f.write(f'G {g} {len(pts)}\n')
        for x, y, z in pts:
            f.write(f'{x} {y} {z}\n')
        if g < gens:
            h = oracle.step(h, m)
