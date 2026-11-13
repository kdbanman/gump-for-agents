#!/usr/bin/env python3
"""Do perturbed clones become independent within a trial? From configurations at the first interface lam0
(asymmetric octahedron, radius R), run pairs of clones with independent perturbations at depth >= D, each to
m <= lam1 (success) or m >= lamA (failure); report the phi coefficient of the paired outcomes
(0 = clones independent, 1 = clones identical, as with no perturbation).

  python3 research/fluct/clone_corr.py R lam1 [npairs]
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl, ffs

R, lam1 = int(sys.argv[1]), int(sys.argv[2]); NP = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
v = fl.Vessel(fl.octa_hull(R), 'c', False)
rng = np.random.default_rng(7)
f = ffs.FFS(v, ffs.Basin(v, 'soup'), 1, 3, rng, 200)
m = f.pilot(2000); lamA = int(round(m.mean())); lam0 = int(round(m.mean() - m.std()))
configs, phi, st = f.stage0(lam0, lamA, NP)
print(f'R={R} lamA={lamA} lam0={lam0} -> lam1={lam1}')
for D in (-1, 0, 1, 2, 3, 5):
    if D > v.node_depth().max(): continue
    f.D = D; f.pert_nodes = np.nonzero(v.node_depth() >= D)[0] if D >= 0 else None
    res = []
    for half in range(2):                      # each pair: same config twice in one batch of 64 slots (32 pairs)
        pass
    out = np.zeros((NP, 2), bool); lens = np.zeros((NP, 2))
    for b0 in range(0, NP, 32):
        idx = list(range(b0, min(NP, b0 + 32)))
        for q, j in enumerate(idx):
            for c in range(2):
                r = 2 * q + c
                f.sim.set(r, np.unpackbits(configs[j][0], count=v.n).astype(bool)); f.perturb(r)
        for r in range(2 * len(idx), 64): f.sim.set(r, np.zeros(v.n, bool))
        lo = np.full(64, lam1); hi = np.full(64, lamA); hi[2 * len(idx):] = 0
        sg, sm, mm = f.sim.run_until(100000, lo, hi)
        for q, j in enumerate(idx):
            out[j] = (sm[2 * q] <= lam1) & (sm[2 * q] >= 0), (sm[2 * q + 1] <= lam1) & (sm[2 * q + 1] >= 0)
            lens[j] = sg[2 * q], sg[2 * q + 1]
    a, b = out[:, 0].astype(float), out[:, 1].astype(float)
    p = (a.mean() + b.mean()) / 2
    phi_c = ((a * b).mean() - a.mean() * b.mean()) / max(1e-12, np.sqrt(a.var() * b.var()))
    print(f'  D={D:2d}: P(success)={p:.3f}, outcome correlation of clone pairs {phi_c:.3f}, mean trial length {lens.mean():.1f} gens')
