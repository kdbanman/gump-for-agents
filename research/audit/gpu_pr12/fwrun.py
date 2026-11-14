#!/usr/bin/env python3
"""Claim a: an independent CPU slab ensemble with firewall tracking (research/peeling's rep.c stepper, not PR 12's code).

  taskset -c 3 python3 research/audit/gpu_pr12/fwrun.py N1 N2 m CAP SEED [W]

32*W replicas of a p = 0.4 soup on geom.slab(N1, m, N2), run to CAP. Per replica: the two face-layer death times,
the first transverse T3 firewall (min over the 3 transverse diagonals, as research/peeling/slabs.py).
Prints (i) PR 12's statistic, ln(2 x exposure / face deaths) from generation 0 with settled replicas censored at
settling (what the GPU run reports: it sees face deaths only), (ii) the competing-risk face rate with firewall-first
replicas censored at their firewall (the quantity the face law means), (iii) what happens after a firewall.
Appends one JSON line to research/scratch/audit_gpu_pr12/fwrun.jsonl.
"""
import json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'peeling'))
import geom                                           # noqa: E402
from analyze import death_times, ring_firewall, INF   # noqa: E402

N1, N2, m, cap, seed = map(int, sys.argv[1:6]); W = int(sys.argv[6]) if len(sys.argv) > 6 else 8
v = geom.slab(N1, m, N2)
st, pop, la = v.run(W, 0.4, seed, cap, 16)
ge = v.gen_end
D = death_times(la, ge)
keys = [k for k, _ in v.layers]
f0 = D[:, keys.index((0, 1))]; f1 = D[:, keys.index((0, 2 * m - 1))]
first = np.minimum(f0, f1)
fw = np.full(len(st), INF)
for d in (1, 2, 3):
    cols = [i for i, k in enumerate(keys) if k[0] == d]
    fw = np.minimum(fw, ring_firewall(D[:, cols], ring=True))
stop = np.where(st >= 0, st, ge).astype(float)
R = len(st); A = 3 * N1 * N2
line = -0.091 + 0.2088 * A
# (i) the PR's statistic: face deaths only
died = first <= stop
expo = np.minimum(first, stop).sum()
k1 = int(died.sum())
s1 = math.log(2 * expo / k1)
# (ii) competing risks: censor at a firewall that precedes the first peel
fwf = (fw < first) & (fw <= stop)
pf = died & ~fwf
expo2 = np.minimum.reduce([first, stop, fw]).sum()
k2 = int(pf.sum())
s2 = math.log(2 * expo2 / k2) if k2 else float('inf')
lag = (first - fw)[fwf & died]
print(f'slab {N1}x{N2}x{m} A={A} replicas {R} cap {ge}: face deaths {k1}, firewall before the first peel {int(fwf.sum())} '
      f'(of which peeled by the cap {int((fwf & died).sum())}), settled first {int(((st >= 0) & ~died).sum())}')
print(f'  PR statistic ln(2 x mean first peel) = {s1:.3f} +- {1 / math.sqrt(k1):.3f}   line {line:.3f}   diff {s1 - line:+.3f}')
print(f'  peel-first only (firewall censored)  = {s2:.3f} +- {1 / math.sqrt(max(k2, 1)):.3f}   diff {s2 - line:+.3f}')
if fwf.sum():
    print(f'  firewall rate: ln(exposure / firewall-first) = {math.log(expo2 / fwf.sum()):.3f}')
if len(lag):
    print(f'  generations from firewall to first peel: median {np.median(lag):.3g}, 90% {np.quantile(lag, .9):.3g} '
          f'(mean first peel {expo / k1:.3g})')
os.makedirs(os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr12'), exist_ok=True)
with open(os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_pr12', 'fwrun.jsonl'), 'a') as f:
    f.write(json.dumps(dict(N1=N1, N2=N2, m=m, A=A, cap=ge, seed=seed, R=R, face_deaths=k1, pr_stat=s1, fw_first=int(fwf.sum()),
                            peel_first=k2, peel_first_stat=s2, line=line, lag_median=float(np.median(lag)) if len(lag) else None)) + '\n')
