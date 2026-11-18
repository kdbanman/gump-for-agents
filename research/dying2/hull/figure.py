#!/usr/bin/env python3
"""research/dying2/hull/hull_dying.svg from data/R{11,13}_*.csv (no matplotlib on this machine: plain SVG).

  python research/dying2/hull/figure.py

A: the dying face, mean P / P bar and quartiles against lag. B: q(k) (log). C: q at the first passage to exactly k,
by the number of survivors in the rim row (k = 4, 6). D, E: where the last cells sit (lag 1), per canonical cell,
share of last live cells over share of stationary live cells (blue < 1 < red).
"""
import math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'data')
Rs = [R for R in (11, 13) if os.path.exists(os.path.join(D, f'R{R}_death_timecourse.csv'))]
COL = {11: '#1f77b4', 13: '#d62728'}
AREA = {11: 63, 13: 84}
S = []


def T(x, y, s, size=12, anchor='start', col='#222'):
    S.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{col}" font-family="sans-serif">{s}</text>')


def axes(x0, y0, w, h, xr, yr, title, xl, yl, logy=False):
    S.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#888"/>')
    T(x0, y0 - 8, title, 13)
    T(x0 + w / 2, y0 + h + 32, xl, 11, 'middle')
    S.append(f'<text x="{x0 - 38}" y="{y0 + h / 2}" font-size="11" text-anchor="middle" font-family="sans-serif" '
             f'transform="rotate(-90 {x0 - 38} {y0 + h / 2})">{yl}</text>')
    fy = (lambda v: math.log10(v)) if logy else (lambda v: v)
    X = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda v: y0 + h - (fy(v) - fy(yr[0])) / (fy(yr[1]) - fy(yr[0])) * h
    return X, Y


def line(X, Y, xs, ys, col, dash='', width=1.6):
    pts = ' '.join(f'{X(a):.1f},{Y(b):.1f}' for a, b in zip(xs, ys) if np.isfinite(b) and b > 0)
    S.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{width}" stroke-dasharray="{dash}"/>')


def ld(name):
    return np.genfromtxt(os.path.join(D, name), delimiter=',', names=True, dtype=None, encoding=None)


# A
X, Y = axes(70, 40, 380, 260, (40, 0), (0, 1.15), 'A. the dying face (band: quartiles)', 'generations before the face is empty', 'P / P bar')
for v in (0, 8, 16, 24, 32, 40):
    T(X(v), 318, str(v), 10, 'middle')
for v in (0, 0.5, 1.0):
    T(64, Y(v) + 4, f'{v}', 10, 'end')
for i, R in enumerate(Rs):
    t = ld(f'R{R}_death_timecourse.csv'); m = t['lag'] <= 40
    pb = t['mean'][m][-1] / t['mean_over_Pbar'][m][-1]
    up = [f'{X(a):.1f},{Y(b / pb):.1f}' for a, b in zip(t['lag'][m], t['q75'][m])]
    dn = [f'{X(a):.1f},{Y(b / pb):.1f}' for a, b in zip(t['lag'][m][::-1], t['q25'][m][::-1])]
    S.append(f'<polygon points="{" ".join(up + dn)}" fill="{COL[R]}" fill-opacity="0.15" stroke="none"/>')
    line(X, Y, t['lag'][m], t['mean_over_Pbar'][m], COL[R])
    line(X, Y, t['lag'][m], t['edge_nb_over_Pbar'][m], COL[R], '4,3', 1)
    T(300, 230 + 16 * i, f'A = {AREA[R]} (dashed: edge neighbours)', 11, 'start', COL[R])
# B
X, Y = axes(540, 40, 380, 260, (0, 16), (1e-4, 1), 'B. q(k): death after a dip to k or fewer cells', 'k (live cells)', 'q', True)
for v in (0, 4, 8, 12, 16):
    T(X(v), 318, str(v), 10, 'middle')
for v in (1e-4, 1e-3, 1e-2, 1e-1, 1):
    T(534, Y(v) + 4, f'{v:g}', 10, 'end')
S.append(f'<line x1="{X(0)}" x2="{X(16)}" y1="{Y(0.5)}" y2="{Y(0.5)}" stroke="#aaa"/>')
for i, R in enumerate(Rs):
    t = ld(f'R{R}_excursions.csv'); m = (t['k'] >= 1) & (t['k'] <= 16)
    line(X, Y, t['k'][m], t['q'][m], COL[R])
    T(800, 70 + 16 * i, f'A = {AREA[R]}', 11, 'start', COL[R])
# C
X, Y = axes(1010, 40, 380, 260, (0, 8), (0, 0.16), 'C. q at first passage to k, by survivors on the rim', 'survivors in the rim row', 'q')
for v in range(0, 9):
    T(X(v), 318, str(v), 10, 'middle')
for v in (0, 0.05, 0.1, 0.15):
    T(1004, Y(v) + 4, f'{v}', 10, 'end')
j = 0
for R in Rs:
    p = os.path.join(D, f'R{R}_condq.csv')
    if not os.path.exists(p):
        continue
    t = ld(f'R{R}_condq.csv')
    for k, dash in ((4, ''), (6, '4,3')):
        m = (t['k'] == k) & (t['class'] == 'rim-row survivors')
        if m.sum():
            xs = t['value'][m].astype(float); ys = t['q'][m]
            line(X, Y, xs, ys, COL[R], dash)
            for a, b, e in zip(xs, ys, t['q_se'][m]):
                S.append(f'<line x1="{X(a):.1f}" x2="{X(a):.1f}" y1="{Y(max(b - e, 0)):.1f}" y2="{Y(min(b + e, 0.16)):.1f}" stroke="{COL[R]}"/>')
            T(1230, 70 + 16 * j, f'A = {AREA[R]}, k = {k}' + (' (dashed)' if dash else ''), 11, 'start', COL[R]); j += 1
# D, E maps
e1 = np.array([1, -1, 0]) / math.sqrt(2); e2 = np.array([1, 1, -2]) / math.sqrt(6)
for i, R in enumerate(Rs):
    c = np.genfromtxt(os.path.join(D, f'R{R}_cells.csv'), delimiter=',', skip_header=1)
    xyz = c[:, 3:6]; st = c[:, 6]; l1 = c[:, 7]
    rel = (l1 / l1.sum()) / (st / st.sum())
    u, v = xyz @ e1, xyz @ e2
    x0, y0, w = 120 + 520 * i, 400, 400
    sc = w / (u.max() - u.min() + 1)
    T(x0, y0 - 14, f'{"DE"[i]}. A = {AREA[R]}: last live cells (lag 1) over stationary, per cell', 13)
    for a, b, r_, o in zip(u, v, rel, st):
        z = max(0.0, min(2.0, r_)) - 1
        col = f'rgb({int(255 * (1 if z > 0 else 1 + z))},{int(255 * (1 - abs(z)))},{int(255 * (1 if z < 0 else 1 - z))})'
        S.append(f'<circle cx="{x0 + (a - u.min() + 0.5) * sc:.1f}" cy="{y0 + (v.max() - b + 0.5) * sc:.1f}" r="{0.36 * sc:.1f}" fill="{col}" stroke="#444" stroke-width="0.4"/>')
        T(x0 + (a - u.min() + 0.5) * sc, y0 + (v.max() - b + 0.5) * sc + 3, f'{r_:.2f}', 7.5, 'middle')
T(1110, 470, 'colour: blue 0 ... white 1 ... red 2', 11)
T(1110, 490, 'number in each cell: the ratio', 11)
T(1110, 510, 'stationary occupancy: corners 0.26, rim row 0.48,', 11)
T(1110, 526, 'interior 0.52 (A = 63)', 11)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="860" viewBox="0 0 1440 860"><rect width="1440" height="860" fill="white"/>{"".join(S)}</svg>'
out = os.path.join(HERE, 'hull_dying.svg')
open(out, 'w').write(svg)
print(out)
