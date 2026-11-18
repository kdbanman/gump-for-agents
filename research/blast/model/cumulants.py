#!/usr/bin/env python3
"""cumulants.py (blast/model): the first four cumulants per cell of the stationary face population, wrapped faces
(short ex3 runs: hist_s_*.txt in data/ or scratch), sorted by shortest loop. Errors on k3/A: naive x sqrt(20)
(samples are correlated over about ten generations).

    python3 research/blast/model/cumulants.py
"""
import glob, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import frontgas as FG, qsd
rows = []
seen = set()
for f in sorted(glob.glob(os.path.join(qsd.DAT, 'hist_s_gen_*_c1.txt')) + glob.glob(os.path.join(qsd.SCR, 'hist_s_gen_*_c1.txt'))):
    spec = os.path.basename(f)[7:-4]
    if spec in seen:
        continue
    seen.add(spec)
    t = spec.split('_'); h, k, d = int(t[1]), int(t[2]), int(t[3]); A = 3 * h * d
    for ln in open(f):
        u = ln.split()
        if u and u[0] == 'phist':
            ph = [int(x) for x in u[1:]]
    tot = sum(ph[1:]); m = sum(n * c for n, c in enumerate(ph) if n) / tot
    mu = lambda j: sum((n - m) ** j * c for n, c in enumerate(ph) if n) / tot
    k2, k3, m4, m6 = mu(2), mu(3), mu(4), mu(6)
    rows.append((FG.prim_loops(h, k, d)[0], A, spec, m / A, k2 / A, k3 / A, math.sqrt(m6 / tot * 20) / A, (m4 - 3 * k2 * k2) / A, tot))
print('shortest loop^2, A, face, rho, k2/A, k3/A (se), k4/A, samples')
for r in sorted(rows):
    print('%2d %3d %-16s rho %.5f  k2/A %.4f  k3/A %+.4f (%.4f)  k4/A %+.3f  %.2e' % r)
