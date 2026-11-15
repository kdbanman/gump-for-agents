#!/usr/bin/env python3
"""t4.c against the engine, every generation, on the 4x4 8-layer slab: a random soup tiled 9 times into the engine's
cubic 12-torus (`gump run --torus 12 --trace`), every engine generation reduced to torus nodes (and required to be
lattice-periodic), compared with t4's lane 0 node set. Negative controls: the engine one generation later, and a start
state with one node flipped, must mismatch. Exits non-zero on failure.
    python3 research/audit/gpu_local_pr23/validate4.py [GENS] [SEED]"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_pr23')
sys.path.insert(0, HERE)
import geom4  # noqa: E402
ENGINE = os.path.join(ROOT, 'engine', 'target', 'release', 'gump')
T4 = os.path.join(SCR, 't4')
NT = 12


def engine_sets(start, gens):
    pts = set()
    for c in np.nonzero(start)[0]:
        p0 = np.array(geom4.CELLS[c])
        for x in range(NT // 4):
            for y in range(NT // 4):
                q = p0 + np.array([8 * x, 8 * y, -8 * x - 8 * y])
                pts.add(tuple(int(z) % (2 * NT) for z in q))
    assert len(pts) == 9 * int(start.sum())
    cf, tr = os.path.join(SCR, 'v_cells.txt'), os.path.join(SCR, 'v_trace.txt')
    open(cf, 'w').write('\n'.join(' '.join(map(str, q)) for q in sorted(pts)))
    subprocess.run([ENGINE, 'run', '--cells', cf, '--torus', str(NT), '--gens', str(gens), '--no-halt', '--trace', tr],
                   check=True, capture_output=True)
    sets = []
    for line in open(tr).read().splitlines()[:gens + 1]:
        nodes = []
        for tok in line.split()[1:]:
            q = list(map(int, tok.split(',')))
            ax = [x % 2 for x in q].index(1)
            c = [(q[x] - (x == ax)) // 2 for x in range(3)]
            t = sum(c) % NT
            assert t < 8, 'engine cell outside the slab'
            nodes.append(geom4.INDEX[(t, c[0] % 4, c[1] % 4, ax)])
        u = np.unique(nodes)
        assert len(nodes) == 9 * len(u), 'engine state not lattice-periodic'
        sets.append(u)
    return sets


def t4_sets(start, gens):
    g = os.path.join(SCR, 'g44.bin'); geom4.write(g)
    ci = os.path.join(SCR, 'v_init.txt'); open(ci, 'w').write('\n'.join(map(str, np.nonzero(start)[0])))
    out = subprocess.run([T4, g, '2', '1', str(gens), '-trace', ci], check=True, capture_output=True, text=True).stdout
    return [np.array(list(map(int, l.split()[1:])), np.int64) for l in out.splitlines()]


def compare(eng, mine, shift=0):
    bad = first = 0
    for t in range(len(mine) - shift):
        if not np.array_equal(eng[t + 1 + shift], mine[t]):
            bad += 1; first = first or t + 1
    return bad, first


if __name__ == '__main__':
    gens = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    rng = np.random.default_rng(seed)
    start = rng.random(len(geom4.CELLS)) < 0.4
    eng = engine_sets(start, gens + 1)
    assert np.array_equal(eng[0], np.nonzero(start)[0])
    mine = t4_sets(start, gens)
    pops = [len(x) for x in mine]
    b0, f0 = compare(eng, mine)
    b1, f1 = compare(eng, mine, shift=1)
    fl = start.copy(); fl[200] ^= True
    b2, f2 = compare(eng, t4_sets(fl, 300)[:300])
    print(f'4x4x8, soup seed {seed}: t4 vs engine every generation, {gens} gens: {b0} mismatches '
          f'(population {pops[0]} .. {pops[-1]}, {len(set(pops))} distinct); controls: shifted {b1} mismatches (first {f1}), '
          f'flipped node {b2} of 300 (first {f2})')
    ok = b0 == 0 and b1 > 0 and b2 > 0
    print('OK' if ok else 'FAIL'); sys.exit(0 if ok else 1)
