#!/usr/bin/env python3
"""Part B: states visited by vessels too large to list (the owner's closed cubes; the face law).

  python3 research/statespace/large.py      prints both tables, writes data/large_cubes.csv, data/large_facelaw.csv

Closed cubes. A deterministic orbit never repeats a state before it enters its final cycle, so the number of
distinct states one seed visits is exactly (cycle_start) + (period): generations 0 .. cycle_start-1 are distinct
and distinct from the cycle, which has `period` states. cycle_start and period for sides 8-13 are the engine's
(`gump run --cube N --lite`, last line; equal to the legacy logs, docs/AUTOMATON.md section 4), for 14 and 15 the
same command (saved in research/scratch/ss/cubeN.json), for 16 research/data/cube16_summary.json. The vessel is the
diagonal hull of the seed (T2): the regular octahedron |p - c|_1 <= R, R = 3n - 2, about the cube's centre (a cube
centre for odd n, a vertex for even n). A = cells of one face (outermost layer of one of its 8 {111} faces).

Face law. ln tau_face = -0.091 + 0.2088 A (CLAIMS F4, flat slab faces, A = 27-90), with the GL3 line
0.033 + 0.2084 A for equilateral tori of 63-93 cells beside it: log2 of the states a seed visits while one face of
A cells lives.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
AX = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)])


def hull_counts(R, vertex):
    c = np.array([1, 1, 1]) if vertex else np.array([0, 0, 0])
    r = np.arange(-R - 2, R + 3)
    G = np.array(np.meshgrid(r, r, r, indexing='ij')).reshape(3, -1).T + c
    G = G[((G & 1).sum(1) == 1)]
    s = (G - c) @ AX.T
    inside = (np.abs(s) <= R).all(1)
    N = int(inside.sum())
    A = int((inside & (s[:, 0] == R)).sum())
    return N, A


CUBES = {8: (23, 1, 'still', 384), 9: (71, 1, 'still', 54), 10: (65, 1, 'still', 264), 11: (4218, 1, 'still', 36),
         12: (24286, 1, 'still', 288), 13: (169049, 1, 'still', 108)}


def cube_rows():
    rows = []
    for n in range(8, 17):
        if n in CUBES:
            T, P, st, pop = CUBES[n]; src = 'engine = legacy log'
        elif n in (14, 15):
            fn = os.path.join(ROOT, 'research', 'scratch', 'ss', f'cube{n}.json')
            if not os.path.exists(fn):
                continue
            d = json.loads(open(fn).read().strip().split('\n')[-1])
            T, P, st, pop = d['cycle_start'], d['period'], d['status'], d['pop']; src = 'engine (this study)'
        else:
            d = json.load(open(os.path.join(ROOT, 'research', 'data', 'cube16_summary.json')))
            T, P, st, pop = d['cycle_start'], d['period'], d['status'], d['pop']; src = 'research/data/cube16_summary.json'
        R = 3 * n - 2
        N, A = hull_counts(R, n % 2 == 0)
        vis = T + P
        b = math.log2(vis)
        rows.append(dict(side=n, seed_cells=3 * n * n * (n + 1), R=R, centre='vertex' if n % 2 == 0 else 'cube',
                         hull_cells=N, face_cells_A=A, all_face_cells=8 * A, cycle_start=T, period=P, status=st,
                         final_pop=pop, visited=vis, log2_visited=b, bits_per_hull_cell=b / N, bits_per_face_cell=b / A,
                         bits_per_A_over_7p7=b / (A / 7.7), source=src))
    return rows


def facelaw_rows():
    rows = []
    for A in (27, 36, 48, 63, 75, 84, 93, 108, 135, 459, 693):
        lt = -0.091 + 0.2088 * A
        rows.append(dict(A=A, ln_tau=lt, log2_visited=lt / math.log(2), bits_per_face_cell=lt / math.log(2) / A,
                         half_A=A / 2, measured=A <= 135))
    return rows


if __name__ == '__main__':
    cr = cube_rows()
    hdr = ['side', 'seed_cells', 'R', 'centre', 'hull_cells', 'face_cells_A', 'cycle_start', 'period', 'status',
           'visited', 'log2_visited', 'bits_per_hull_cell', 'bits_per_face_cell', 'bits_per_A_over_7p7']
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    with open(os.path.join(HERE, 'data', 'large_cubes.csv'), 'w') as f:
        f.write(','.join(hdr) + '\n')
        for r in cr:
            f.write(','.join(f'{r[h]:.5f}' if isinstance(r[h], float) else str(r[h]) for h in hdr) + '\n')
    print(' | '.join(hdr))
    for r in cr:
        print(' | '.join(f'{r[h]:.4f}' if isinstance(r[h], float) else f'{r[h]:,}' if isinstance(r[h], int) else str(r[h]) for h in hdr))
    fr = facelaw_rows()
    with open(os.path.join(HERE, 'data', 'large_facelaw.csv'), 'w') as f:
        f.write('A,ln_tau,log2_visited,bits_per_face_cell,measured\n')
        for r in fr:
            f.write(f"{r['A']},{r['ln_tau']:.4f},{r['log2_visited']:.4f},{r['bits_per_face_cell']:.5f},{r['measured']}\n")
    print()
    for r in fr:
        print(r['A'], f"{r['log2_visited']:.2f} bits, {r['bits_per_face_cell']:.4f} per face cell", '' if r['measured'] else '(extrapolated)')
