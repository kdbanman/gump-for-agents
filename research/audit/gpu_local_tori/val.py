#!/usr/bin/env python3
"""val.py: tor.c against reference/oracle.py, generation by generation, on the cubic torus that tiles the slab.

    python3 val.py A K B N GENS LANES [GEO_MUTANT]   # e.g. 1 7 19 19 3000 3
Runs `tor trace` (64 first-life soups), lifts lanes 0..LANES-1 into the oracle's H = 2N array-index torus (N Z^2
inside the lattice, N - 8 >= 3 dead layers between slab copies), steps the oracle and requires, every generation,
that the oracle state is lattice-periodic and reduces to exactly tor's node set. Negative controls (each must FAIL):
  shift   tor's generation g against the oracle's g + 1;
  mutant  tor built with -DMUTANT=1 (survival also at n = 6);
  geo     a graph file with two neighbour entries of one cell swapped for other cells' (one wrong edge).
Exit 0 iff the real comparison passes and all three controls fail.
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference')); sys.path.insert(0, HERE)
import oracle, geo  # noqa: E402
SCR = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_tori'); os.makedirs(SCR, exist_ok=True)


def build(mut=False):
    exe = os.path.join(SCR, 'tor_mut' if mut else 'tor')
    subprocess.run(['gcc', '-O3', '-march=native', '-o', exe, os.path.join(HERE, 'tor.c')] + (['-DMUTANT=1'] if mut else []), check=True)
    return exe


def trace(exe, gpath, n, gens, seed=12345):
    out = os.path.join(SCR, f'trace_{os.getpid()}.bin')
    subprocess.run([exe, 'trace', gpath, str(seed), str(gens), out], check=True)
    x = np.fromfile(out, '<u8').reshape(gens + 1, n); os.remove(out)
    return x


def compare(g, a, k, b, N, X, lanes, shift=0):
    H = 2 * N; m = oracle.masks(H)
    reps = {((x * a) % N, (x * k + y * b) % N) for x in range(N // a) for y in range(N // b)}   # cosets of N Z^2 in L
    assert len(reps) == N * N // (a * b)
    pts = g['pts']; ncop = len(reps); bad = 0
    for lane in range(lanes):
        bits = ((X >> np.uint64(lane)) & np.uint64(1)).astype(bool)          # [gens+1, n]
        h = np.zeros((H, H, H), np.int8)
        for c in np.nonzero(bits[0])[0]:
            for (u, v) in reps:
                q = (pts[c] + 2 * np.array([u, v, -u - v])) % H
                h[tuple(q)] = 1
        assert h.sum() == ncop * bits[0].sum()
        for _ in range(shift):
            h = oracle.step(h, m)
        for gg in range(len(bits) - shift):
            if gg:
                h = oracle.step(h, m)
            live = np.argwhere(h)
            cnt = np.zeros(g['n'], int)
            for q in live:
                ax = int(np.nonzero(q % 2)[0][0])
                c = (q - np.eye(3, dtype=int)[ax]) // 2
                ti = int(c.sum()); t = ti % N
                if t >= g['m']:
                    cnt[:] = -99; break
                c[2] -= ti - t
                p = 2 * c; p[ax] += 1
                cnt[g['canon'](list(map(int, p)))] += 1
            want = bits[gg] * ncop
            if not np.array_equal(cnt, want):
                bad += 1
    return bad


if __name__ == '__main__':
    a, k, b, N, gens, lanes = map(int, sys.argv[1:7])
    g = geo.build(a, k, b)
    ok, _ = geo.checks(g)
    gp = os.path.join(SCR, f'val_{a}_{k}_{b}.bin'); geo.write(g, gp)
    exe, mut = build(), build(True)
    X = trace(exe, gp, g['n'], gens)
    bad = compare(g, a, k, b, N, X, lanes)
    print(f'({a},{k}),(0,{b}) N = {N}: tor vs oracle, {lanes} lanes x {gens + 1} generations: {bad} mismatching generations')
    gs = min(gens, 300)
    b1 = compare(g, a, k, b, N, X[:gs + 1], 1, shift=1)
    print(f'  control shift (tor g vs oracle g+1, {gs} gens): {b1} mismatching')
    b2 = compare(g, a, k, b, N, trace(mut, gp, g['n'], gs), 1)
    print(f'  control mutant rule: {b2} mismatching of {gs + 1}')
    g2 = dict(g); nb = g['nb'].copy()
    c0 = int(np.nonzero(g['t'] == 3)[0][0]); y = nb[c0, 0]; z = int(np.nonzero(g['t'] == 3)[0][-1])
    nb[c0, 0] = z                                                            # one directed edge rewired
    g2['nb'] = nb; gp2 = gp + '.mut'; geo.write(g2, gp2)
    b3 = compare(g, a, k, b, N, trace(exe, gp2, g['n'], gs), 1)
    print(f'  control wrong edge (cell {c0}: {y} -> {z}): {b3} mismatching of {gs + 1}')
    allok = ok and bad == 0 and b1 > 0 and b2 > 0 and b3 > 0
    print('ALL OK' if allok else 'FAILURES')
    sys.exit(0 if allok else 1)
