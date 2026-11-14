#!/usr/bin/env python3
"""Recompute research/shape/data/A72.csv and A60.csv from their counts, the grouping chi^2, and test the robustness of
the size claims ("ratio 1.8 +- 0.3", "systole 3 sits 0.21 below the trend") to which points enter.

    python3 research/audit/shape/recompute.py
"""
import csv, itertools, math, os, sys
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import geom_check as gc  # noqa: E402
DATA = os.path.join(HERE, '..', '..', 'shape', 'data')
G = gc.point_group()


def load(A):
    rows = []
    for r in csv.DictReader(open(os.path.join(DATA, f'A{A}.csv'))):
        L = (int(r['a']), int(r['k']), int(r['b']))
        E, F = float(r['exposure']), int(r['face_deaths'])
        y, e = math.log(2 * E / F), 1 / math.sqrt(F)
        cls = min(gc.image(L, g, A // 3) for g in G)
        assert abs(y - float(r['ln_tau_face'])) < 1e-3 and gc.systole2(L) == int(r['systole2']), r
        rows.append(dict(L=L, y=y, e=e, s2=gc.systole2(L), cls=cls, W=int(r['firewalls']), F=F))
    return rows


def pool(v):
    w = np.array([1 / e ** 2 for _, e in v]); y = np.array([x for x, _ in v])
    m = (w * y).sum() / w.sum()
    return m, 1 / math.sqrt(w.sum()), float((w * (y - m) ** 2).sum()), len(v) - 1


def groups(items, key):
    g = {}
    for it in items:
        g.setdefault(key(it), []).append((it['y'], it['e']))
    chi = sum(pool(v)[2] for v in g.values()); dof = sum(pool(v)[3] for v in g.values())
    return {k: pool(v)[:2] for k, v in g.items()}, chi, dof


def wline(x, y, e):
    w = 1 / np.asarray(e) ** 2; A = np.vstack([np.ones(len(x)), x]).T
    cov = np.linalg.inv(A.T @ (A * w[:, None])); beta = cov @ (A.T @ (w * np.asarray(y)))
    chi = float((w * (np.asarray(y) - A @ beta) ** 2).sum())
    return beta, cov, chi


if __name__ == '__main__':
    shapes = {}
    for A in (72, 60):
        rows = load(A)
        print(f'A = {A}: every row reproduced from its counts (ln(2E/F), 1/sqrt F, systole^2)')
        _, chi, dof = groups(rows, lambda r: r['cls'])
        print(f'  presentations of one torus (point-group class): chi2 {chi:.2f} / {dof}')
        m, chi, dof = groups(rows, lambda r: r['s2'])
        print(f'  by systole^2, all presentations: chi2 {chi:.2f} / {dof}  p = {stats.chi2.sf(chi, dof):.3g}')
        sh, _, _ = groups(rows, lambda r: r['cls'])
        s2 = {r['cls']: r['s2'] for r in rows}
        items = [dict(y=v[0], e=v[1], s2=s2[c], cls=c) for c, v in sh.items()]
        m2, chi2_, dof2 = groups(items, lambda r: r['s2'])
        print(f'  by systole^2, distinct shapes only (presentations pooled first): chi2 {chi2_:.2f} / {dof2}  '
              f'p = {stats.chi2.sf(chi2_, dof2) if dof2 else float("nan"):.3g}')
        for k in sorted(m2):
            print(f'    systole^2 {k:2d}: {m2[k][0]:.4f} +- {m2[k][1]:.4f}   shapes: ' +
                  ', '.join(f'{c} {sh[c][0]:.4f}+-{sh[c][1]:.4f}' for c in sh if s2[c] == k))
        shapes[A] = (sh, s2, m2)
    # ---- ratio of the systole effect between areas, for every reasonable choice of points
    print('\nSize of the systole effect, A = 72 against A = 60 (differences of pooled values):')
    (_, _, g72), (sh60, s260, g60) = shapes[72], shapes[60]
    c16 = [c for c in sh60 if s260[c] == 16]
    choices = [('12 -> 16 (README)', g72[16], g72[12], g60[16], g60[12]),
               ('13 -> 16', g72[16], g72[13], g60[16], g60[13])]
    for c in c16:
        choices.append((f'12 -> 16, A=60 shape {c} only', g72[16], g72[12], sh60[c], g60[12]))
    for lab, a1, a0, b1, b0 in choices:
        d72 = a1[0] - a0[0]; e72 = math.hypot(a1[1], a0[1]); d60 = b1[0] - b0[0]; e60 = math.hypot(b1[1], b0[1])
        r = d72 / d60; er = r * math.hypot(e72 / d72, e60 / d60)
        print(f'  {lab:40s} A72 {d72:.3f} +- {e72:.3f}  A60 {d60:.3f} +- {e60:.3f}  ratio {r:.2f} +- {er:.2f}')
    # slopes per unit systole over 12..16 (the only range both areas have)
    sl = {}
    for A in (72, 60):
        sh, s2, _ = shapes[A]
        ks = [c for c in sh if 12 <= s2[c] <= 16]
        b, cov, chi = wline([math.sqrt(s2[c]) for c in ks], [sh[c][0] for c in ks], [sh[c][1] for c in ks])
        sl[A] = (b[1], math.sqrt(cov[1, 1]))
        print(f'  line in sigma over systole^2 12..16, A = {A}: slope {b[1]:.4f} +- {math.sqrt(cov[1, 1]):.4f}, chi2 {chi:.1f} / {len(ks) - 2}')
    r = sl[72][0] / sl[60][0]
    print(f'  ratio of slopes {r:.2f} +- {r * math.hypot(sl[72][1] / sl[72][0], sl[60][1] / sl[60][0]):.2f}')
    # ---- "systole 3 sits 0.21 below the trend": extrapolation from different subsets of the A = 72 shapes
    print('\nA = 72: gap of systole^2 9 below a line in sigma fitted to subsets of the other shapes '
          '(extrapolated to sigma = 3, with the line\'s own error):')
    sh, s2, g = shapes[72]
    y9 = g[9]
    others = sorted({s2[c] for c in sh if s2[c] > 9})
    for sub in [tuple(others)] + [tuple(x) for n in (3, 4, 5) for x in itertools.combinations(others, n) if x != tuple(others)]:
        ks = [c for c in sh if s2[c] in sub]
        for var, f in [('sigma', math.sqrt), ('sigma^2', float)]:
            b, cov, chi = wline([f(s2[c]) for c in ks], [sh[c][0] for c in ks], [sh[c][1] for c in ks])
            x0 = np.array([1, f(9)]); pred = x0 @ b; ep = math.sqrt(x0 @ cov @ x0)
            gap = pred - y9[0]
            if var == 'sigma' or len(sub) == len(others):
                print(f'  systole^2 {str(sub):18s} line in {var:7s}: chi2 {chi:5.1f}/{len(ks) - 2}  predicted {pred:.3f} +- {ep:.3f}  '
                      f'gap {gap:.3f} +- {math.hypot(ep, y9[1]):.3f}')
