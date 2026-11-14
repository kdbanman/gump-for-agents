#!/usr/bin/env python3
"""Slab first-peel statistic for one cohort of fresh soups, two independent steppers on the same geom.slab graph:
fl.c (the stepper the GPU kernel was checked against) and research/peeling's rep.c (the stepper behind the CPU line).

  taskset -c 3 python3 research/audit/gpu_pr12/cohort_check.py N1 N2 M P CAP [SEED]

fl.c: 256 numpy soups of density P, run_until the first extinct face layer (or a period-1/2 settle), no reseeding.
Prints the single-cohort mean first peel, ln(2 x mean), the CV, and the hazard in age bins.
"""
import math, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'fluct'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'scratch', 'pr12', 'research', 'gpu'))
import fl  # noqa: E402
from vessels import SlabVessel  # noqa: E402
N1, N2, M = map(int, sys.argv[1:4]); P = float(sys.argv[4]); CAP = int(sys.argv[5]); SEED = int(sys.argv[6]) if len(sys.argv) > 6 else 1
v = SlabVessel(N1, N2, M)
S = fl.Sim(v, W=4)
rng = np.random.default_rng([SEED, N1, N2, M, 77])
S.set_all(rng.random((S.R, v.n)) < P)
L = fl.lib(); R = S.R
sg = np.zeros(R, np.int32); sm = np.zeros(R, np.int32); mm = np.zeros(R, np.int32)
t = L.fl_run_until(CAP, np.zeros(R, np.int32), np.full(R, 1 << 30, np.int32), sg, sm, mm)
died = (sg >= 0) & (sm == 0); settled = (sg >= 0) & (sm == -2)
x = np.where(sg >= 0, sg, t).astype(float)
k = int(died.sum()); mean = x.sum() / k
print(f'fl.c cohort {N1}x{N2}x{M} p={P}: {R} soups, {k} first peels, {int(settled.sum())} settled, {int((sg < 0).sum())} open at {t}: '
      f'mean first peel {mean:.4g}, ln(2 x mean) = {math.log(2 * mean):.3f} +- {1 / math.sqrt(k):.3f}; CV {x[died].std() / x[died].mean():.3f}')
for lo, hi in ((0, 60), (60, 500), (500, 2000), (2000, 5000), (5000, 1e9)):
    e = np.clip(np.minimum(x, hi) - lo, 0, None).sum(); d = int((died & (x >= lo) & (x < hi)).sum())
    print(f'  age {lo:g}-{hi:g}: deaths {d}, hazard x mean = {d / e * mean if e else float("nan"):.2f}')
