#!/usr/bin/env python3
"""Claim 7 of the review: do the forecast numbers of research/constant/PREDICTIONS.md follow from the stated models,
and what did the repository already hold when they were committed (5dd18b9)?

    python3 research/audit/constant/forecasts.py
"""
import csv, io, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402
import numpy as np  # noqa: E402

ROOT = data.ROOT

# --- (A) empty patches: -ln P = c cells + (sigma/4) cut bonds, cells = 3ab, cut bonds = 8(a+b) - 4
print('(A) empty patches, recomputed from the stated form (c = 0.212, sigma = 0.34; range sigma 0.15 .. 0.6)')
for a in range(1, 7):
    cells, cut = 3 * a * a, 8 * (2 * a) - 4
    f = lambda c, s: c * cells + s / 4 * cut  # noqa
    print(f'  {a}x{a}: {f(0.212, 0.34):5.2f} ({f(0.212, 0.15):5.2f} .. {f(0.212, 0.6):5.2f});  per cell {f(0.212, 0.34)/cells:.3f}')
print(f'  single cell: -ln(1 - 0.52) = {-math.log(0.48):.3f}; sigma_b = (0.73 - 0.212)/6 = {(0.73-0.212)/6:.4f}; '
      f'sigma = 4 sigma_b = {4*(0.73-0.212)/6:.3f}; strip step 3c + 2 sigma = {3*0.212 + 2*0.34:.2f}')

# --- (B) the capillary-wave forecast on fitting set W (wide classes), own fit
per = data.periodic()
W = [p for p in per if p['Q1'] >= 12]
X = np.array([[1, p['A'], p['F_b']] for p in W]); y = np.array([p['y'] for p in W]); s = np.array([p['se'] for p in W])
th, *_ = np.linalg.lstsq(X / s[:, None], y / s, rcond=None)
kap = th[2]
print(f'\n(B) capillary wave fitted on W ({len(W)} classes): kappa {kap:+.4f}')
PAIRS = [('P1', 48, (2, 2, 8), (1, 6, 16)), ('P2', 60, (1, 5, 20), (1, 4, 20)), ('P3', 60, (1, 8, 20), (2, 2, 10)),
         ('T01', 72, (1, 6, 24), (2, 4, 12)), ('T12', 72, (2, 4, 12), (1, 5, 24)), ('N72', 72, (2, 2, 12), (1, 10, 24)),
         ('Q36', 36, (1, 4, 12), (1, 3, 12)), ('Q45', 45, (1, 5, 15), (1, 4, 15)), ('Q54', 54, (3, 0, 6), (1, 5, 18)),
         ('Q63', 63, (1, 6, 21), (1, 7, 21))]
fore = {}
for lab, A, Xl, Yl in PAIRS:
    ix, iy = data.invariant(*Xl), data.invariant(*Yl)
    d = kap * (data.Fb(iy['tau']) - data.Fb(ix['tau']))
    fore[lab] = d
    print(f'  {lab:4s} A={A} ({ix["Q1"]},{ix["B2"]},{ix["Q2"]}) -> ({iy["Q1"]},{iy["B2"]},{iy["Q2"]}): d = {d:+.4f}')

# --- what research/shape3/data/runs.csv held at 5dd18b9, and the pair differences it gives
txt = subprocess.run(['git', '-C', ROOT, 'show', '5dd18b9:research/shape3/data/runs.csv'], capture_output=True,
                     text=True).stdout
rows = list(csv.DictReader(io.StringIO(txt)))
print(f'\nresearch/shape3/data/runs.csv at the forecast commit 5dd18b9: {len(rows)} rows, tags '
      f'{sorted({r["tag"] for r in rows})}')
by = {}
for r in rows:
    k = (int(r['a']), int(r['k']), int(r['b']))
    E, F = by.get(k, (0.0, 0))
    by[k] = (E + float(r['exposure']), F + int(r['F']))
for lab, A, Xl, Yl in PAIRS:
    if Xl in by and Yl in by:
        (ex, fx), (ey, fy) = by[Xl], by[Yl]
        d = math.log(2 * ey / fy) - math.log(2 * ex / fx); e = math.hypot(fx ** -0.5, fy ** -0.5)
        print(f'  {lab:4s}: in the tree at forecast time: d = {d:+.4f} +- {e:.4f}; forecast {fore[lab]:+.4f}; '
              f'z = {(d - fore[lab]) / e:+.1f}')
    else:
        print(f'  {lab:4s}: not in the tree at forecast time')
cur = subprocess.run(['git', '-C', ROOT, 'diff', '--stat', '5dd18b9', 'HEAD', '--', 'research/shape3'], capture_output=True,
                     text=True).stdout.strip()
print(f'changes to research/shape3 since 5dd18b9: {cur or "none"}')
print('patch data in the tree now: ' + (subprocess.run(['git', '-C', ROOT, 'ls-files'], capture_output=True, text=True)
                                       .stdout.count('patch') and 'see ls-files' or 'none'))
