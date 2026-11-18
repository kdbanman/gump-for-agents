#!/usr/bin/env python3
"""Reactive paths of dying faces: statistics of the per-cell last-alive lags written by `tube1d brute ... PATHFILE`.

    python3 paths.py EXE h k d nl PATHFILE

Line of PATHFILE: age face lag[0..A-1]   (lag = generations before the death at which the cell was last alive;
1 = alive in the last living generation; -1 = not alive in the last 255).  Geometry from `EXE geom h k d nl`.
"""
import sys, subprocess
import numpy as np
exe, h, k, d, nl, pf = sys.argv[1:7]
g = subprocess.run([exe, 'geom', h, k, d, nl], capture_output=True, text=True).stdout.split('\n')
hdr = g[0].split(); girth = float(hdr[hdr.index('girth') + 1 + 2]) if False else None
L = float(g[0].split('length')[1]); G = float(g[0].split('girth')[2].split()[0])
rows = np.array([[float(v) for v in l.split()] for l in g[2:] if l.strip()])
order = np.argsort(rows[:, 0].astype(int)); rows = rows[order]
xi = [rows[:, 4], rows[:, 6]]
A = len(rows)
P = [l.split() for l in open(pf) if l.strip()]
P = [(int(p[0]), int(p[1]), np.array(p[2:], int)) for p in P if len(p) == A + 2]
n = len(P)
print(f"# {pf}: {n} face deaths, A={A}, girth {G:.3f}, length {L:.3f}")
def circ_span(x, L):
    x = np.sort(x % L)
    if len(x) <= 1: return 0.0
    gaps = np.diff(np.concatenate([x, [x[0] + L]]))
    return L - gaps.max()
for BW in (0.5, 1.0):
    nb = int(round(L / BW)); share = {4: 0, 8: 0}; shmed = {4: 0, 8: 0}
    for age, f, lag in P:
        lag = np.where(lag < 0, 256, lag); b = np.minimum((xi[f] / BW).astype(int), nb - 1)
        m = np.array([lag[b == i].min() if (b == i).any() else 999 for i in range(nb)])   # generation (before the end) at which the band was last occupied
        last = lag.min()
        for q in share: share[q] += (m.max() >= last + q); shmed[q] += (m.max() >= np.median(lag) + q)
    print(f"band-first share, band width {BW}: empty >=4 gens before the last cell: {share[4]/n:.3f}; >=8 gens: {share[8]/n:.3f}; "
          f">=4 gens before the MEDIAN cell's last live generation: {shmed[4]/n:.3f}; >=8: {shmed[8]/n:.3f}")
med = []; p90 = []; span2 = []; span1 = []; nlast = []
prof = {}; 
for age, f, lag in P:
    lag = np.where(lag < 0, 256, lag)
    med.append(np.median(lag)); p90.append(np.percentile(lag, 90))
    lastc = lag <= 2; span2.append(circ_span(xi[f][lastc], L)); nlast.append(lastc.sum())
    span1.append(circ_span(xi[f][lag <= 1], L))
    # death-time profile against distance along the tube from the centre of the last clump
    x0 = xi[f][lag <= 1]; ang = np.angle(np.exp(2j * np.pi * x0 / L).mean()) * L / (2 * np.pi)
    dist = np.abs((xi[f] - ang + L / 2) % L - L / 2)
    for dd, lg in zip((dist / 0.5).astype(int), lag): prof.setdefault(dd, []).append(min(lg, 60))
med = np.array(med); span2 = np.array(span2)
print(f"median over deaths of the median lag {np.median(med):.1f}; of the 90th-percentile lag {np.median(p90):.1f}  (how many generations before the end a typical cell / the earliest tenth was last alive)")
print(f"cells alive in the last 2 living generations: mean number {np.mean(nlast):.2f}; span along the tube < 2 units in {np.mean(span2 < 2):.3f} of deaths (median span {np.median(span2):.2f}; tube length {L:.2f})")
print("distance from the last clump (units) | mean lag | median lag | cells")
for dd in sorted(prof): print(f"  {dd*0.5:.1f}-{dd*0.5+0.5:.1f}  {np.mean(prof[dd]):.2f}  {np.median(prof[dd]):.1f}  {len(prof[dd])}")
