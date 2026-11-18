#!/usr/bin/env python3
"""State-for-state check of gs.c against reference/oracle.py's step(), plus a negative control.
  validate.py hull R G        validate.py slab K D G
The hull sits in the oracle's array (an even torus wider than the hull: confinement T2 makes it free space).
The slab torus (1,K),(0,D) is lifted periodically into the oracle's cubic torus of H = 2D (needs (D,0) in the lattice),
8 live layers and D-8 dead ones (T3 keeps them dead)."""
import sys, os, subprocess, random
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'reference'))
import oracle
import build_vessel as bv
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-map')
GS = os.path.join(SCR, 'gs')
kind = sys.argv[1]
if kind == 'hull':
    R = int(sys.argv[2]); G = int(sys.argv[3]); cells, idx, nb, faces = bv.hull(R); N = len(cells)
    c = R + 5 + ((R + 5) % 2); H = 2 * c
    sites = [[(p[0] + c, p[1] + c, p[2] + c)] for p in cells]
    tag = f'h{R}'
else:
    K, D, G = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); S = bv.Slab(K, D); nb, faces = S.graph(); N = S.N
    assert (21 * 1) % 1 == 0 and (D * K) % D == 0      # (D,0) = D*(1,K) - K*(0,D) is in the lattice
    H = 2 * D; sites = [[] for _ in range(N)]
    for x in range(H):
        for y in range(H):
            for z in range(H):
                if (x % 2) + (y % 2) + (z % 2) != 1: continue
                s = (x + y + z) % H
                if 1 <= s <= 2 * S.L - 1:
                    sites[S.index((x - (x + y + z - s), y, z))].append((x, y, z))
    assert all(len(l) == len(sites[0]) for l in sites), 'uneven lift'
    tag = f't{3*D}'
m = oracle.masks(H)
flat = [np.array([s[0] * H * H + s[1] * H + s[2] for s in l]) for l in sites]
allsites = np.concatenate(flat); nlift = len(flat[0])
def run(graphfile, label):
    random.seed(12345)
    inits = [[i for i in range(N) if random.random() < 0.5] for _ in range(2)]
    initf = os.path.join(SCR, f'val_{tag}.init'); dumpf = os.path.join(SCR, f'val_{tag}.dump')
    open(initf, 'w').write('\n'.join(' '.join(map(str, l)) for l in inits) + '\n')
    subprocess.check_call([GS, graphfile, '1', str(G), 'validate', initf, dumpf])
    lines = open(dumpf).read().split('\n')
    hs = []
    for k in range(2):
        h = np.zeros(H * H * H, np.int8)
        for i in inits[k]: h[flat[i]] = 1
        hs.append(h.reshape(H, H, H))
    for t in range(G + 1):
        for k in range(2):
            live = np.array(lines[2 * t + k].split(), dtype=int)
            mine = np.zeros(H * H * H, np.int8)
            for i in live: mine[flat[i]] = 1
            if not np.array_equal(mine, hs[k].reshape(-1)):
                print(f'{label}: MISMATCH replica {k} at generation {t} (oracle pop {int(hs[k].sum())//nlift}, gs pop {len(live)})'); return False
            if t < G: hs[k] = oracle.step(hs[k], m)
    print(f'{label}: identical to the oracle for {G} generations, both replicas; final populations {[int(h.sum())//nlift for h in hs]}'); return True
gf = os.path.join(SCR, f'val_{tag}.graph'); bv.write(gf, nb, faces)
ok = run(gf, f'{tag} N={N} H={H} lift x{nlift}')
nb2 = [list(r) for r in nb]; i = N // 2; nb2[i][3] = nb[(i + 7) % N][3] if nb[(i + 7) % N][3] != nb[i][3] else (i + 11) % N
gf2 = os.path.join(SCR, f'val_{tag}_bad.graph'); bv.write(gf2, nb2, faces)
bad = run(gf2, f'{tag} NEGATIVE CONTROL (one neighbour of cell {i} swapped)')
print('VALIDATION', 'PASSED' if ok and not bad else 'FAILED')
