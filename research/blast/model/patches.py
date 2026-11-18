#!/usr/bin/env python3
"""patches.py (blast/model): what the empty-patch counts of 2026-11-14 (research/data/gpu_patches/) say about the
cost of the edge of a hole, all shapes on file, strips and hexagonal balls included.

-ln P(patch empty) = c * cells + s_p * perimeter + k0, fitted by weighted least squares (weights from the hit
counts; shapes with fewer than 20 hits dropped) on several subsets. 'perimeter' is the file's column; for an
a x b rhombus it is 8(a + b) - 4, i.e. 4 per lattice unit of edge, so sigma per lattice unit = 4 s_p.

    python3 research/blast/model/patches.py
"""
import csv, glob, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.abspath(os.path.join(HERE, '..', '..', 'data', 'gpu_patches'))
agg = {}
for f in sorted(glob.glob(os.path.join(D, 'patches_s81*_A10G.csv'))):
    for r in csv.DictReader(open(f)):
        e = agg.setdefault(r['shape'], dict(cells=int(r['cells']), per=int(r['perimeter']), S=0, H=0))
        e['S'] += int(r['samples']); e['H'] += int(r['hits'])
rows = []
print('shape            cells perim  hits         -lnP     se    -lnP/cell')
for k, e in agg.items():
    if e['H'] == 0:
        continue
    y = -math.log(e['H'] / e['S']); se = 1 / math.sqrt(e['H'])
    rows.append((k, e['cells'], e['per'], y, se, e['H']))
    print(f"{k:16s} {e['cells']:4d} {e['per']:5d} {e['H']:12d} {y:8.3f} {se:6.3f} {y / e['cells']:7.3f}")


def fit(sel, label, cfix=None):
    R = [r for r in rows if sel(r) and r[5] >= 20]
    y = np.array([r[3] for r in R]); w = 1 / np.maximum(np.array([r[4] for r in R]), 0.005)   # floor: model error dominates
    if cfix is None:
        X = np.array([[r[1], r[2], 1.0] for r in R])
        th, *_ = np.linalg.lstsq(X * w[:, None], y * w, rcond=None); c, sp, k0 = th
    else:
        X = np.array([[r[2], 1.0] for r in R]); yy = y - cfix * np.array([r[1] for r in R])
        th, *_ = np.linalg.lstsq(X * w[:, None], yy * w, rcond=None); c = cfix; sp, k0 = th
    res = y - (c * np.array([r[1] for r in R]) + sp * np.array([r[2] for r in R]) + k0)
    print(f'{label:46s} n={len(R):2d}  c={c:.4f}  s_p={sp:.4f} (sigma per lattice unit {4 * sp:.3f})  k0={k0:+.3f}  '
          f'max|res|={np.max(np.abs(res)):.3f}')


print()
isr = lambda r: r[0].startswith('rhombus')
big = lambda r: isr(r) and r[1] >= 12
fit(big, 'rhombi from 2x2')
fit(lambda r: isr(r) and r[1] >= 18, 'rhombi from 2x3')
fit(lambda r: isr(r) and r[1] >= 27, 'rhombi from 3x3')
fit(big, 'rhombi from 2x2, c = 0.2086 forced', 0.2086)
fit(lambda r: isr(r) and r[1] >= 27, 'rhombi from 3x3, c = 0.2086 forced', 0.2086)
fit(lambda r: r[0].startswith('strip'), 'strips 1 x b')
fit(lambda r: r[0].startswith('strip'), 'strips, c = 0.2086 forced', 0.2086)
fit(lambda r: not isr(r) and not r[0].startswith('strip'), 'other shapes (balls)')
fit(lambda r: r[1] >= 12, 'every shape of 12 cells or more')
fit(lambda r: r[1] >= 12, 'every shape of 12 cells or more, c = 0.2086', 0.2086)
