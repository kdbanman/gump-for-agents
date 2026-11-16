#!/usr/bin/env python3
"""Edge profile of a hull face: for face-layer cells away from the corners (second-nearest other face >= 5 layers),
mean density, births, dead cells' live-neighbour count and Var-free statistics by r (layers to the nearest other
face), against the wrapped face; and the edge excess per unit of edge length (sum over r of cells-per-unit-length x
(rho - rho_w)); cells per unit edge length at each r from the growth of the orbit counts.
  python3 research/hulllocal/edgeprof.py RHO_W hull21_s10
"""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hl, profile  # noqa: E402

rho_w = float(sys.argv[1])
for tag in sys.argv[2:]:
    z = np.load(os.path.join(hl.SCR, tag + '.npz'))
    v = hl.vessel(str(z['name']))
    ex = z['expo'].sum(1)[:, 0][:, None]
    live, birth = z['live'].sum(1), z['birth'].sum(1)
    dsum, dcnt, dins = z['dsum'].sum(1), z['dcnt'].sum(1), z['dinsum'].sum(1)
    by = {}
    for k, c in profile.orbits(v).items():
        r = min(k[0][0], k[1][0])
        if min(k[0][1], k[1][0]) >= 5 or r >= 3:
            by.setdefault(r, []).append(c)
    print(f'== {tag}: R = {v.R}; cells away from corners, by r')
    for r in sorted(by):
        c = np.concatenate(by[r])
        rho = live[:, c].sum(1) / (len(c) * ex[:, 0]); b = birth[:, c].sum(1) / (len(c) * ex[:, 0])
        dn = dsum[:, c].sum(1) / dcnt[:, c].sum(1); di = dins[:, c].sum(1) / dcnt[:, c].sum(1)
        e = lambda a: f'{a.mean():.6f} ± {a.std(ddof=1) / np.sqrt(len(a)):.6f}'
        print(f'  r = {r:2d} ({len(c) // 8:3d} cells/face): rho {e(rho)} (rho - rho_w {rho.mean() - rho_w:+.6f}); '
              f'births {e(b)}; dead n {e(dn)}; dead n in-layer {e(di)}')
