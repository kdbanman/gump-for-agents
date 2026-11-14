#!/usr/bin/env python3
"""This review's independent runs (ts.c, research/scratch/audit_shape2/) against research/shape2's tables.

    python3 research/audit/shape2/compare.py
"""
import csv, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
import drv  # noqa  (redirects ts.OUT)
from drv import ts  # noqa
import glob

THEIRS = {}
for fn in ('A48.csv', 'A60.csv', 'A72x.csv'):
    for r in csv.DictReader(open(os.path.join(ROOT, 'research/shape2/data', fn))):
        THEIRS[tuple(map(int, r['cls'].split()))] = r

TORI = [(1, 0, 16), (1, 1, 16), (2, 0, 8), (1, 7, 16), (1, 2, 16), (2, 2, 8), (1, 6, 16), (1, 3, 16), (4, 0, 4),
        (1, 0, 20), (1, 1, 20), (1, 9, 20), (2, 0, 10), (1, 2, 20), (1, 8, 20), (2, 2, 10), (1, 5, 20), (1, 4, 20)]


def ages(L):
    out = []
    for f in glob.glob(os.path.join(ts.OUT, f'ev_{L[0]}_{L[1]}_{L[2]}_c500000_s*.txt')):
        t = np.loadtxt(f, dtype=str); out.append(t)
    t = np.concatenate(out)
    return t[:, 0], t[:, 1].astype(float)


def hz(ty, a, edges):
    s = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        ex = (np.clip(a, lo, hi) - lo).sum(); nf = int(((ty == 'F') & (a > lo) & (a <= hi)).sum())
        if nf:
            s.append(f'[{int(lo)},{int(hi) if hi < 1e9 else "inf"}):{math.log(2 * ex / nf):.3f}({nf})')
    return ' '.join(s)


res = {}
for L in TORI:
    if not glob.glob(os.path.join(ts.OUT, f'ev_{L[0]}_{L[1]}_{L[2]}_c500000_s*.txt')):
        continue
    r = ts.stats(L, quiet=True)
    ty, a = ages(L)
    cnt = r['cnt']; lives = sum(cnt.values())
    th = THEIRS.get(L)
    tl = f"{th['ln_tau_face']} +- {th['err']}" if th else '-'
    d = (r['lnF'] - float(th['ln_tau_face'])) / math.hypot(r['eF'], float(th['err'])) if th else float('nan')
    # estimator excluding the first 256 generations of every life (stationary hazard)
    ex = (np.clip(a, 256, None) - 256).sum(); nf = int(((ty == 'F') & (a > 256)).sum())
    st = math.log(2 * ex / nf) if nf else float('nan')
    res[L] = (r['lnF'], r['eF'], r['lnFX'], st)
    print(f'{str(L):12s} lives {lives:8d} F {cnt.get("F", 0):7d} X {cnt.get("X", 0):6d} W {cnt.get("W", 0):8d} '
          f'S {cnt.get("S", 0):5d} C {cnt.get("C", 0):5d}  ln tau_face {r["lnF"]:.4f} +- {r["eF"]:.4f} '
          f'(X as face {r["lnFX"]:.4f}; ages > 256 only {st:.4f}); theirs {tl}; diff {d:+.1f} sd; ln tau_fw {r["lnW"]:.3f}; '
          f'near2 {r["near2"]}')
    print(f'{"":12s} hazard thirds ' + ', '.join(f'{x:.3f}' for x, _, _ in r['thirds']) + '; by age ' +
          hz(ty, a, [0, 64, 256, 1024, 4096, 16384, 65536, 1e9]))


def pr(A, B, lab):
    if A in res and B in res:
        x, y = res[A], res[B]
        print(f'  {lab}: {y[0] - x[0]:+.4f} +- {math.hypot(x[1], y[1]):.4f}  (ages > 256 only: {y[3] - x[3]:+.4f})')


print('\nDifferences (second minus first):')
pr((2, 2, 8), (1, 6, 16), 'A=48 (12;16) -> (12;19,19)')
pr((2, 2, 8), (4, 0, 4), 'A=48 (12;16) -> 4x4 (16)')
pr((1, 6, 16), (4, 0, 4), 'A=48 (12;19) -> 4x4 (16)')
pr((1, 3, 16), (4, 0, 4), 'A=48 (13) -> 4x4 (16)')
pr((1, 5, 20), (1, 4, 20), 'A=60 (16;19) -> (16;21)')
pr((1, 8, 20), (2, 2, 10), 'A=60 (12;25) -> (12;28)')
pr((2, 0, 8), (1, 7, 16), 'A=48 loop^2 4 pair')
four = [res[L] for L in [(2, 2, 8), (1, 6, 16), (1, 3, 16), (4, 0, 4)] if L in res]
if len(four) == 4:
    print(f'  A=48 four classes: spread {max(v[0] for v in four) - min(v[0] for v in four):.4f}; '
          f'(12 pooled) -> 16: {res[(4, 0, 4)][0] - (res[(2, 2, 8)][0] + res[(1, 6, 16)][0]) / 2:+.4f}')
print('\nCost per cell between A = 48 and 60, this review alone (classes of equal systole^2 averaged):')
for lab, a48, a60 in [('3', [(1, 1, 16)], [(1, 1, 20)]), ('4', [(2, 0, 8), (1, 7, 16)], [(1, 9, 20), (2, 0, 10)]),
                      ('7', [(1, 2, 16)], [(1, 2, 20)]), ('12', [(2, 2, 8), (1, 6, 16)], [(1, 8, 20), (2, 2, 10)]),
                      ('16', [(4, 0, 4)], [(1, 5, 20), (1, 4, 20)])]:
    if all(L in res for L in a48 + a60):
        for j, nm in ((0, 'X as firewall'), (2, 'X as face')):
            m = lambda Ls: sum(res[L][j] for L in Ls) / len(Ls)
            print(f'  systole^2 {lab:>2s} ({nm}): b = {(m(a60) - m(a48)) / 12:.4f}')
