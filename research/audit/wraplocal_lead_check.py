"""Lead's own check of the tube study's key number (research/wraplocal, 2026-11-15): the density of the two face
layers of a living wrapped face is lower on a tube with a short loop, by an amount set by the loop's length.

Claim (research/wraplocal/README.md, data/dens_rho_face.txt), tori of 84 cells:
    (1,12,28)  one loop of 12        0.515429 +- 0.000012
    (1,7,28)   one loop of 16        0.516947 +- 0.000028
    (1,4,28)   loops of 21 and 28    0.517541 +- 0.000013

Here: the slab graph of each torus (the vessel file research/wrap/validate.py checks against reference/oracle.py;
run `python3 research/wrap/validate.py H K D 1500` for that), and a stepper written here: plain numpy, one byte
per cell, R replicas from independent 0.4 soups, B45/S345 on the 12 listed neighbours.  Not the study's bit-sliced
live.py and none of its reduction.  Burn-in 500 generations, then GENS measured; a replica leaves the average from
the generation one of its face layers is empty.  Error: scatter of 8 blocks of replicas.

    python3 research/audit/wraplocal_lead_check.py [R] [GENS]        (default 512 4000; about 3 min on one core)
    python3 research/audit/wraplocal_lead_check.py 1024 4000 long    (two tori that differ only in long loops; 5 min)
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'wrap'))
import validate as V                                   # only ts.vessel (the graph file) and read_bin (its loader)

R = int(sys.argv[1]) if len(sys.argv) > 1 else 512
GENS = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
CLAIM = {(1, 12, 28): (0.515429, 0.000012), (1, 7, 28): (0.516947, 0.000028), (1, 4, 28): (0.517541, 0.000013)}
LONG = len(sys.argv) > 3 and sys.argv[3] == 'long'     # the claim that the effect goes on past loop^2 19
if LONG:                                               # (1,4,34): 102 cells, one loop of 21; (6,0,6): 108 cells, three of 36
    CLAIM = {(1, 4, 34): (0.517563, 0.000009), (6, 0, 6): (0.517717, 0.000008)}


def density(L, seed):
    cells, path = V.ts.vessel(L)
    n, nb, f0, f1, _ = V.read_bin(path)
    nb = np.array(nb, dtype=np.int64)
    assert nb.shape == (n, 12) and nb.max() <= n
    nb[(nb < 0) | (nb >= n)] = n                       # a neighbour outside the slab: the extra, always dead, cell
    rng = np.random.default_rng(seed)
    x = np.zeros((R, n + 1), dtype=np.uint8)
    x[:, :n] = rng.random((R, n)) < 0.4
    f0, f1 = np.array(f0), np.array(f1)
    alive = np.ones(R, dtype=bool)
    tot = np.zeros(R); cnt = np.zeros(R)
    for g in range(500 + GENS):
        c = x[:, nb].sum(axis=2, dtype=np.uint8)
        live = x[:, :n] == 1
        x[:, :n] = (~live & ((c == 4) | (c == 5))) | (live & (c >= 3) & (c <= 5))
        a, b = x[:, f0].sum(axis=1), x[:, f1].sum(axis=1)
        alive &= (a > 0) & (b > 0)
        if g >= 500:
            tot += np.where(alive, (a + b) / (len(f0) + len(f1)), 0.0); cnt += alive
    blocks = [tot[i::8].sum() / cnt[i::8].sum() for i in range(8)]
    return float(np.mean(blocks)), float(np.std(blocks, ddof=1) / np.sqrt(8)), int((~alive).sum()), n


res = {}
for i, L in enumerate(CLAIM):
    m, e, dropped, n = density(L, 20261115 + i)
    res[L] = (m, e)
    c, ce = CLAIM[L]
    print(f'{L}: {n} cells in the slab; face density {m:.6f} +- {e:.6f} ({dropped} of {R} replicas dropped); '
          f'study {c:.6f} +- {ce:.6f}; difference {(m - c) / np.hypot(e, ce):+.1f} sigma', flush=True)
ok = all(abs(res[L][0] - CLAIM[L][0]) < 3.5 * np.hypot(res[L][1], CLAIM[L][1]) for L in CLAIM)
if LONG:
    d = res[(6, 0, 6)][0] - res[(1, 4, 34)][0]; e = np.hypot(res[(6, 0, 6)][1], res[(1, 4, 34)][1])
    print(f'deficit of the torus with one loop of 21 against the torus with loops of 36 only: {d:.6f} +- {e:.6f} '
          f'({d / e:.1f} sigma from zero; study 0.000154)')
    ok &= d > 4 * e
else:
    d12 = res[(1, 4, 28)][0] - res[(1, 12, 28)][0]; e12 = np.hypot(res[(1, 4, 28)][1], res[(1, 12, 28)][1])
    d16 = res[(1, 4, 28)][0] - res[(1, 7, 28)][0]; e16 = np.hypot(res[(1, 4, 28)][1], res[(1, 7, 28)][1])
    print(f'deficit of the loop-12 tube against the long-loop torus: {d12:.6f} +- {e12:.6f} (study 0.002112)')
    print(f'deficit of the loop-16 tube against the long-loop torus: {d16:.6f} +- {e16:.6f} (study 0.000594)')
    ok &= d12 > 10 * e12 and d16 > 4 * e16 and d12 > d16
print('PASS' if ok else 'FAIL')
