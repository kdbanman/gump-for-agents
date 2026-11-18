#!/usr/bin/env python3
"""Statistical error of the minimum action: each cell's mean is redrawn from N(mean, cov/n) and its variances are
rescaled by 1 + N(0, 2/n)^(1/2) (parametric bootstrap, 12 draws), rule visited:nmin.  staterr.py [nmin] [d] [vessels...]"""
import sys, os, copy, numpy as np
from dp import Map, build, chain
SCR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-map')
nmin = int(sys.argv[1]) if len(sys.argv) > 1 else 200; d = int(sys.argv[2]) if len(sys.argv) > 2 else 0
ves = sys.argv[3:] or ['h9', 'h11', 'h13']
rng = np.random.default_rng(7); res = {}; AA = []
for v in ves:
    m = Map('+'.join(os.path.join(SCR, f + '.tal') for f in v.split('+')), d); out = []; AA.append(m.A)
    for k in range(12):
        q = copy.copy(m); n = np.maximum(m.n, 1)
        z1 = rng.standard_normal(m.n.shape); z2 = rng.standard_normal(m.n.shape)
        sP = np.sqrt(np.maximum(m.vPP, 1e-9) / n); rho = np.clip(m.vPB / np.sqrt(np.maximum(m.vPP * m.vBB, 1e-9)), -0.99, 0.99)
        sB = np.sqrt(np.maximum(m.vBB, 1e-9) / n)
        q.mP = m.mP + sP * z1; q.mB = m.mB + sB * (rho * z1 + np.sqrt(1 - rho ** 2) * z2)
        f = 1 + np.sqrt(2 / n) * rng.standard_normal(m.n.shape); f = np.clip(f, 0.3, 3)
        q.vPP = m.vPP * f; q.vBB = m.vBB * f; q.vPB = m.vPB * f
        out.append(chain(q, *build(q, 'visited', nmin), tau=False)['S'])
    res[v] = np.array(out)
    print(f"{v} d={d} visited:{nmin}: S of 12 redraws mean {res[v].mean():.3f} sd {res[v].std(ddof=1):.3f} (min {res[v].min():.3f} max {res[v].max():.3f})", flush=True)
if len(ves) == 3:
    a, b, c = (res[v] for v in ves); cc = (c - 2 * b + a) / 3; D1 = AA[1] - AA[0]; D2 = AA[2] - AA[1]; bb = (b - a) - D1 * cc
    print(f"c from second difference: {cc.mean():.4f} sd {cc.std(ddof=1):.4f}; b: {bb.mean():+.3f} sd {bb.std(ddof=1):.3f}; "
          f"first differences per cell {((b-a)/D1).mean():.4f} sd {((b-a)/D1).std(ddof=1):.4f}, {((c-b)/D2).mean():.4f} sd {((c-b)/D2).std(ddof=1):.4f}")
