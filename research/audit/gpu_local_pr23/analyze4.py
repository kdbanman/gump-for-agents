#!/usr/bin/env python3
"""ln tau_face of the 4x4 8-layer torus from t4.c's records (age, kind, snap_age, life), with the conventions of the
two pipelines emulated on the same lives:
  exact      every life to its end, events exact to the generation, settled (kind 5) censored at recognition;
  snapcut    the same with settled lives censored at their snapshot age (the cycle was entered by then);
  cap16384   lives censored at age 16,384 (research/shape2's cap);
  grid16     death and firewall times moved to the end of their 16-generation window plus one, as rep.c's
             la + 1 with la rounded up to a multiple of K = 16 (research/shape/tslab.run with K = 16);
  shape2     cap16384 and grid16 together;
  T0         exposure and deaths only after age T0 (burn-in);
plus the hazard of a face death by age.
    python3 research/audit/gpu_local_pr23/analyze4.py research/scratch/audit_gpu_local_pr23/prod_s*.bin
"""
import math, sys
import numpy as np

recs = [np.fromfile(p, np.int64).reshape(-1, 4) for p in sys.argv[1:]]
for p, r in zip(sys.argv[1:], recs):
    k = r[:, 1]
    E, F = r[:, 0].sum(), (k == 1).sum()
    print(f'{p}: {len(r)} lives, E {E:.6g}, F {F}, fw {(k == 4).sum()}, settled {(k == 5).sum()}, open {(k == 0).sum()}: '
          f'ln(2E/F) {math.log(2 * E / F):.4f} +- {1 / math.sqrt(F):.4f}')
r = np.concatenate(recs)
age, kind, sage = r[:, 0].astype(np.int64), r[:, 1], r[:, 2]
F = int((kind == 1).sum()); W = int((kind == 4).sum()); S = int((kind == 5).sum())


def est(a, dead, name):
    E = a.sum(); n = int(dead.sum())
    v = math.log(2 * E / n)
    print(f'  {name:34s} E {E:.6g}  F {n}  ln tau_face {v:.4f} +- {1 / math.sqrt(n):.4f}')
    return v


print(f'pooled: {len(r)} lives, face {F}, firewall {W}, settled {S}; '
      f'ln tau_fw = ln(E/W) {math.log(age.sum() / W):.3f} +- {1 / math.sqrt(W):.3f}; settled exposure share '
      f'{age[kind == 5].sum() / age.sum():.2e}')
face = kind == 1
v0 = est(age, face, 'exact')
a_snap = np.where(kind == 5, sage, age)
est(a_snap, face, 'snapcut')
cap = 16384
est(np.minimum(age, cap), face & (age <= cap), 'cap16384')
g = np.where((kind == 1) | (kind == 4), 16 * np.ceil((age - 1) / 16).astype(np.int64) + 1, age)
est(g, face, 'grid16')
est(np.minimum(g, cap), face & (g <= cap), 'shape2 (cap16384 + grid16)')
for T0 in (60, 200, 1000):
    keep = age > T0
    est(age[keep] - T0, face & keep, f'T0 = {T0}')
print('hazard of a face death by age (x1e5 per generation), deaths, ln(2/h):')
edges = [0, 16, 32, 48, 60, 64, 96, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 1 << 40]
for lo, hi in zip(edges[:-1], edges[1:]):
    ex = (np.clip(age, lo, hi) - lo).sum()
    d = int((face & (age > lo) & (age <= hi)).sum())
    if ex:
        print(f'  ({lo},{hi}]: {d:8d}  {1e5 * d / ex:7.3f} +- {1e5 * math.sqrt(max(d, 1)) / ex:.3f}  '
              f'{math.log(2 * ex / d) if d else float("nan"):.4f}')
ex60 = (np.clip(age, 0, 60)).sum(); d60 = int((face & (age <= 60)).sum())
exl = (np.clip(age, 60, None) - 60).sum(); dl = int((face & (age > 60)).sum())
print(f'0-60: {1e5 * d60 / ex60:.2f} +- {1e5 * math.sqrt(d60) / ex60:.2f}; after 60: {1e5 * dl / exl:.3f} +- {1e5 * math.sqrt(dl) / exl:.3f}')
