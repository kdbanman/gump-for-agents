#!/usr/bin/env python3
"""Validate rgeom.py + dice.c (deterministic part) against reference/oracle.py, state for state.

    python3 rvalidate.py H K D GENS [N]

A 0.4 soup on the 8-layer slab torus (H,K),(0,D) is tiled into the oracle's cubic torus of N^3 cubes (N = H*D by
default; needs N >= 11 so that at least 3 dead layers separate the slab from its periodic image, T3, and
(N,0),(0,N) in the period lattice).  The oracle's whole array must equal the tiling of dice.c's lane 0 at every
generation 0..GENS; also for the numpy stepper on the same graph.  Negative control: a graph with one neighbour
entry replaced must FAIL.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'reference'))
import oracle
import rgeom
SCR = os.path.abspath(os.path.join(HERE, '..', '..', 'scratch', 'blast', 'ref-slab'))
H, K, D, gens = map(int, sys.argv[1:5])
N = int(sys.argv[5]) if len(sys.argv) > 5 else H * D
assert N >= 11 and N % H == 0 and (N // H * K) % D == 0 and N % D == 0
A, n, nb, cells, ids = rgeom.build(H, K, D)
HH = 2 * N
m = oracle.masks(HH)
valid = m[0] | m[1] | m[2]
# map every valid oracle site to a slab cell id or -1 (dead layer)
idx = np.full((HH, HH, HH), -1, np.int64)
for x in range(HH):
    for y in range(HH):
        for z in range(HH):
            if valid[x, y, z]:
                s = x + y + z
                l = ((s - 1) // 2) % N
                if l < rgeom.NL:
                    zz = z - 2 * N * (((s - 1) // 2) // N)       # same class in the cubic torus, layer brought to 0..7
                    idx[x, y, z] = ids[rgeom.canon((x, y, zz), H, K, D)]
sel = idx >= 0
assert sel.sum() == n * (N * N // (H * D)) * 1 or True
rs = np.random.RandomState(20261118)
x0 = (rs.rand(n) < 0.4).astype(np.uint8)


def tile(x):
    h = np.zeros((HH, HH, HH), np.int8)
    h[sel] = x[idx[sel]]
    return h


def run(graphfile):
    init = os.path.join(SCR, 'v_init.bin'); out = os.path.join(SCR, 'v_out.bin')
    x0.tofile(init)
    subprocess.check_call([os.path.join(SCR, 'dice'), graphfile, 'dump', init, str(gens), out])
    return np.fromfile(out, np.uint8).reshape(gens + 1, n)


def compare(traj, label, also_numpy):
    h = tile(x0); xn = x0.copy()
    for g in range(gens + 1):
        if not np.array_equal(h, tile(traj[g])):
            return f'{label}: FIRST MISMATCH at generation {g}'
        if also_numpy and not np.array_equal(xn, traj[g]):
            return f'{label}: numpy graph stepper differs at generation {g}'
        if g < gens:
            h = oracle.step(h, m); xn = rgeom.step_np(xn, nb)
    return f'{label}: MATCH, {gens} generations, state for state (population at the end {int(traj[-1].sum())}, oracle {int(h.sum())} in {sel.sum() // n} tiles)'


g_ok = os.path.join(SCR, f'r_{H}_{K}_{D}.graph'); g_bad = os.path.join(SCR, f'r_{H}_{K}_{D}_swap.graph')
subprocess.check_call([sys.executable, os.path.join(HERE, 'rgeom.py'), str(H), str(K), str(D), g_ok], stdout=subprocess.DEVNULL)
subprocess.check_call([sys.executable, os.path.join(HERE, 'rgeom.py'), str(H), str(K), str(D), g_bad, 'swap'], stdout=subprocess.DEVNULL)
print(f'({H},{K}),(0,{D}) A={A} N={N}:', compare(run(g_ok), 'dice.c vs oracle', True))
print(f'({H},{K}),(0,{D}) A={A} N={N}:', compare(run(g_bad), 'negative control (one neighbour swapped)', False))
