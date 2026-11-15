#!/usr/bin/env python3
"""report.py: every table and fit of README.md, from data/runs.csv (this study) and the earlier O_h values
(oh_data.py). Asymmetric hull values not run here are the GPU's (CLAIMS GP1): 18.141 +- 0.005 (A = 84),
23.376 +- 0.031 (108), 29.34 +- 0.25 (135), cube-centred.

    python3 research/theory/symmetric/report.py
"""
import csv, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import oh_data

ROWS = {}
with open(os.path.join(HERE, 'data', 'runs.csv')) as fh:
    for r in csv.DictReader(fh):
        ROWS[r['spec']] = r
GPU_C1 = {84: (18.141, 0.005), 108: (23.376, 0.031), 135: (29.34, 0.25)}


def v(spec):
    """(ln tau_face, statistical error, lower value if settled lives are counted to the rung before the snapshot)"""
    r = ROWS.get(spec)
    if r is None or r['lntau'] == 'nan':
        return None
    return float(r['lntau']), float(r['se']), float(r['lntau_Slow'])


def fmt(x, nd=3):
    return 'n/a' if x is None else f'{x[0]:.{nd}f} +- {x[1]:.{nd}f}'


def diff(a, b):
    if a is None or b is None:
        return None
    return a[0] - b[0], math.hypot(a[1], b[1])


def area(R, cen):
    return 3 * (R + 1) * (R + 3) // 8 if cen == 'c' else 3 * R * (R + 2) // 8


def wls(X, y, s):
    W = 1 / s ** 2
    cov = np.linalg.inv(X.T @ (X * W[:, None])); b = cov @ (X.T @ (W * y))
    return b, np.sqrt(np.diag(cov)), float((((X @ b) - y) ** 2 * W).sum())


print('=' * 100)
print('A. slab faces, mirror imposed (rect_P_Q_cs) against the asymmetric partner of equal quotient area (rect_(P/2)_Q_c1)')
print('   P Q  quotient cells  mirror cells   ln tau (cs)        partner            cs - partner     fw share')
for P, Q in [(6, 2), (8, 2), (10, 2), (12, 2), (4, 3), (6, 3), (8, 3), (4, 4), (6, 4)]:
    a = v(f'rect_{P}_{Q}_cs'); b = v(f'rect_{P // 2}_{Q}_c1') if P % 2 == 0 else None
    fw = ROWS.get(f'rect_{P}_{Q}_cs', {}).get('fw_share', '')
    print(f'  {P:2d} {Q}  {3 * P * Q:8d} {2 * Q:12d}       {fmt(a):18s} {fmt(b):18s} {fmt(diff(a, b)):18s} {fw}')
print('   slopes per quotient cell: ', end='')
for Q, Ps in ((2, (6, 8, 10, 12)), (3, (4, 6, 8))):
    for p0, p1 in zip(Ps, Ps[1:]):
        d = diff(v(f'rect_{p1}_{Q}_cs'), v(f'rect_{p0}_{Q}_cs'))
        print(f'Q={Q} P {p0}->{p1}: {d[0] / (3 * Q * (p1 - p0)):.4f} +- {d[1] / (3 * Q * (p1 - p0)):.4f}; ', end='')
print('\n   partners, Q = 2:        ', end='')
for p0, p1 in ((3, 4), (4, 5), (5, 6)):
    d = diff(v(f'rect_{p1}_2_c1'), v(f'rect_{p0}_2_c1'))
    print(f'P/2 {p0}->{p1}: {d[0] / 12:.4f} +- {d[1] / 12:.4f}; ', end='')
print()

print('=' * 100)
print('B. slab faces, threefold axis imposed (hex_A_B_c3): quotient of n = A^2+AB+B^2 cells, three cone points, no boundary')
pts = []
for spec, n in [('hex_6_0_c3', 36), ('hex_6_0_c3_o2', 36), ('hex_6_0_c3_o4', 36), ('hex_5_2_c3', 39), ('hex_6_1_c3', 43), ('hex_4_4_c3', 48),
                ('hex_7_0_c3', 49), ('hex_6_2_c3', 52), ('hex_7_1_c3', 57), ('hex_5_4_c3', 61), ('hex_8_0_c3', 64)]:
    a = v(spec); ref = v('rect_4_2_c1')[0] + 0.2086 * (n - 48)
    if a:
        print(f'  {spec:16s} n = {n}:  {fmt(a, 4)}   forecast P3 {ref:6.2f}   minus the asymmetric line {a[0] - ref:+.3f}')
        if not spec.endswith(('o2', 'o4')):
            pts.append((n, a[0], a[1]))
n_, y, s = (np.array(x, float) for x in zip(*pts))
b, eb, chi2 = wls(np.stack([np.ones_like(n_), n_ - 48], 1), y, s)
print(f'  line through the nine tori: ln tau = {b[0]:.3f} + ({b[1]:.4f} +- {eb[1]:.4f})(n - 48), chi2 {chi2:.1f}/{len(y) - 2}')
pa = [(36, v('rect_3_2_c1')), (48, v('rect_4_2_c1')), (60, v('rect_5_2_c1')), (72, v('rect_6_2_c1'))]
print('  asymmetric partners rect_k_2_c1: ' + '; '.join(f'n = {n}: {fmt(x)}' for n, x in pa))
print('  asymmetric tori of 72 cells here against CLAIMS SH1 (shortest loop^2 9, 12, 16: 14.613, 14.877, 14.973): '
      + ', '.join(fmt(v(s_)) for s_ in ('rect_3_4_c1', 'rect_6_2_c1', 'rect_4_3_c1')))

print('=' * 100)
print('C. slab faces, C3v imposed (hex_N_0_c3v): a triangle of N^2/2 cells bounded by three mirror lines; no hull rim')
for N in (8, 9, 10, 11, 12):
    a = v(f'hex_{N}_0_c3v'); n = N * N / 2
    if a:
        ref = v('rect_4_2_c1')[0] + 0.2086 * (n - 48); td = 8.018 + 0.196 * (n - 39)
        print(f'  N = {N:2d}  quotient cells {n:5.1f}  {fmt(a)}   asymmetric line {ref:6.2f} ({a[0] - ref:+.2f})   T_d wedge of equal quotient area {td:6.2f} ({a[0] - td:+.2f})')
a = v('hex_6_6_c3v')
if a:
    print(f'  hex_6_6_c3v (54 quotient cells; one mirror boundary, one free cone point): {fmt(a)}')

print('=' * 100)
print('D. vessels, A = 63: one, two, three edges of every face on a coordinate mirror; other groups of order two')
for cen, R in (('c', 11), ('v', 12)):
    c1 = v(f'oct_{R}_{cen}_c1'); print(f'  R = {R} {cen}:  c1 {fmt(c1)}')
    prev = c1
    for g in ('csz', 'c2v', 'd2h'):
        x = v(f'oct_{R}_{cen}_{g}')
        if x:
            print(f'     {g:4s} {fmt(x)}  (settled lives counted low: {x[2]:.3f})   step {fmt(diff(x, prev))}   from c1 {fmt(diff(x, c1))}')
            prev = x
for g in ('ci', 'c2e'):
    x = v(f'oct_11_c_{g}')
    if x:
        print(f'  R = 11 c  {g:4s} {fmt(x)}   from c1 {fmt(diff(x, v("oct_11_c_c1")))}')
print('  A = 84, R = 13 c: c1 (GPU) 18.141 +- 0.005')
prev = GPU_C1[84]
for g in ('csz', 'c2v', 'd2h'):
    x = v(f'oct_13_c_{g}')
    if x:
        print(f'     {g:4s} {fmt(x)}  (low: {x[2]:.3f})   step {fmt(diff(x, prev))}')
        prev = x

print('=' * 100)
print('E. D2h faces (three edges in lockstep with the neighbouring faces) against asymmetric faces of the same hull')
print('    A   R   c1 (c)             d2h (c)            c1 - d2h     per rim  per rim period ((R-1)/2 an edge)   d2h (v)            v - c (d2h)')
for R in (9, 11, 13, 15, 17):
    A = area(R, 'c'); c1 = v(f'oct_{R}_c_c1') or (GPU_C1.get(A) + (None,) if A in GPU_C1 else None)
    d = v(f'oct_{R}_c_d2h'); dv = v(f'oct_{R + 1}_v_d2h')
    if d is None:
        continue
    dd = diff(c1, d)
    print(f'  {A:4d} {R:3d}   {fmt(c1):18s} {fmt(d):18s} {dd[0]:7.3f}  {dd[0] / 3:7.3f}  {dd[0] / 3 / ((R - 1) / 2):7.3f}                     {fmt(dv):18s} {fmt(diff(dv, d))}')
print('  slopes per cell of d2h (c): ' + ', '.join(f'{area(a, "c")}->{area(b_, "c")}: {diff(v(f"oct_{b_}_c_d2h"), v(f"oct_{a}_c_d2h"))[0] / (area(b_, "c") - area(a, "c")):.4f}'
                                                  for a, b_ in ((11, 13), (13, 15), (15, 17)) if v(f'oct_{b_}_c_d2h')))
print('  asymmetric v - c: ' + '; '.join(f'A = {area(R, "c")}: {fmt(diff(v(f"oct_{R + 1}_v_c1"), v(f"oct_{R}_c_c1") or (GPU_C1[area(R, "c")] if area(R, "c") in GPU_C1 else None)))}'
                                        for R in (7, 9, 11, 13) if v(f'oct_{R + 1}_v_c1')))

print('=' * 100)
print('F. faces with a threefold axis: T (free rims), T_h (rims in lockstep), T_d (C3v, free rims), O_h (C3v, rims in lockstep)')
print('   group   R   A    ln tau_face (c)     (c/k)A, c = 0.209   |  R   ln tau_face (v)      v - c')
for g, k, Rs in (('t', 3, (15, 17, 19, 21)), ('th', 3, (19, 21, 23)), ('td', 6, (19, 21, 23, 25, 27, 29, 31, 33)), ('oh', 6, (23, 25, 27, 29, 31, 33))):
    for R in Rs:
        a = v(f'oct_{R}_c_{g}'); b_ = v(f'oct_{R + 1}_v_{g}'); A = area(R, 'c')
        print(f'   {g:3s}  {R:3d} {A:4d}   {fmt(a):18s}  {0.209 / k * A:7.3f} ({(a[0] - 0.209 / k * A) if a else float("nan"):+.2f})    | {R + 1:3d}  {fmt(b_):18s}  {fmt(diff(b_, a))}')
print('   local slopes x |stabiliser| (per quotient cell), cube-centred:')
for g, k, Rs in (('t', 3, (15, 17, 19, 21)), ('td', 6, (19, 21, 23, 25, 27, 29, 31, 33)), ('oh', 6, (23, 25, 27, 29, 31, 33))):
    out = []
    for r0, r1 in zip(Rs, Rs[1:]):
        d = diff(v(f'oct_{r1}_c_{g}'), v(f'oct_{r0}_c_{g}'))
        if d:
            out.append(f'{area(r0, "c")}->{area(r1, "c")}: {k * d[0] / (area(r1, "c") - area(r0, "c")):.3f}')
    print(f'     {g:3s} ' + ', '.join(out))

print('=' * 100)
print('G. the rim term of a wedge: T_d minus O_h at equal hull; T_h minus T')
pts = {'c': [], 'v': []}
for R in (23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33):
    cen = 'c' if R % 2 else 'v'; d = diff(v(f'oct_{R}_{cen}_td'), v(f'oct_{R}_{cen}_oh'))
    if d:
        per = (R - 1) / 4 if cen == 'c' else R / 4
        print(f'   R = {R} {cen}  A = {area(R, cen)}  rim periods in the wedge {per:5.2f}   T_d - O_h = {fmt(d)}   per period {d[0] / per:.3f}')
        pts[cen].append((per, d[0], d[1]))
for cen in 'cv':
    if len(pts[cen]) >= 3:
        p, y, s = (np.array(x, float) for x in zip(*pts[cen]))
        b, eb, chi2 = wls(np.stack([np.ones_like(p), p], 1), y, s)
        print(f'   {cen}: T_d - O_h = {b[0]:.2f} + ({b[1]:.3f} +- {eb[1]:.3f}) per period, chi2 {chi2:.1f}/{len(p) - 2} (errors statistical; scatter is larger, see the centre kinds)')
        b1, eb1, chi21 = wls(p[:, None], y, s)
        print(f'      through the origin: {b1[0]:.3f} per period, chi2 {chi21:.1f}/{len(p) - 1}')
for R in (19, 20, 21):
    cen = 'c' if R % 2 else 'v'; d = diff(v(f'oct_{R}_{cen}_t'), v(f'oct_{R}_{cen}_th'))
    if d:
        per = (R - 1) / 2 if cen == 'c' else R / 2
        print(f'   R = {R} {cen}  A = {area(R, cen)}  rim periods in the sector {per:5.2f}   T - T_h = {fmt(d)}   per period {d[0] / per:.3f}')

print('=' * 100)
print('H. the centring (v - c at equal area), every group')
allp = []
for g, Rs in (('c1', (7, 9, 11, 13)), ('csz', (11,)), ('c2v', (11,)), ('d2h', (11, 13, 15)), ('t', (15, 17, 19)), ('th', (19, 21, 23)), ('td', (19, 21, 23, 25, 27, 29, 31)),
              ('oh', (23, 25, 27, 29, 31, 33))):
    out = []
    for R in Rs:
        A = area(R, 'c'); a = v(f'oct_{R}_c_{g}')
        if a is None and g == 'c1' and A in GPU_C1:
            a = GPU_C1[A]
        d = diff(v(f'oct_{R + 1}_v_{g}'), a)
        if d:
            out.append(f'A = {A}: {d[0]:+.3f} +- {d[1]:.3f}')
            if g == 'oh':
                allp.append((A, d[0], max(d[1], abs((v(f"oct_{R + 1}_v_{g}")[2] - v(f"oct_{R + 1}_v_{g}")[0]) - (a[2] - a[0])))))
    print(f'   {g:4s} ' + '; '.join(out))
pool = oh_data.load()
C = {A: (math.log(e / d), 1 / math.sqrt(d)) for (A, c), (d, e) in pool.items() if c == 'c' and d >= 10}
V = {A: (math.log(e / d), 1 / math.sqrt(d)) for (A, c), (d, e) in pool.items() if c == 'v' and d >= 10}
old = [(A, V[A][0] - C[A][0], math.hypot(V[A][1], C[A][1])) for A in sorted(V) if A in C]
print('   oh, earlier data: ' + '; '.join(f'A = {a}: {d:+.3f} +- {e:.3f}' for a, d, e in old))
both = [p for p in allp if p[0] < 400] + old
a_, d_, e_ = (np.array(x, float) for x in zip(*both))
print(f'   O_h, this study at A < 400 (error widened by the settled-life bracket) with the earlier data at A >= 408, {len(a_)} areas:')
for name, X in (('constant', np.ones((len(a_), 1))), ('k sqrt(A)', np.sqrt(a_)[:, None]), ('d0 + k sqrt(A)', np.stack([np.ones_like(a_), np.sqrt(a_)], 1))):
    b, eb, chi2 = wls(X, d_, e_)
    print(f'     {name:16s}: ' + ', '.join(f'{x:.4f} +- {ex:.4f}' for x, ex in zip(b, eb)) + f'  chi2 {chi2:.1f}/{len(a_) - X.shape[1]}')

print('=' * 100)
print('I. this study against the earlier O_h values (same vessel, other stepper, soup 0.35, T0 = 1000)')
for R, cen in ((29, 'c'), (30, 'v'), (31, 'c'), (32, 'v'), (33, 'c'), (34, 'v')):
    A = area(R, cen); o = (C if cen == 'c' else V).get(A); m = v(f'oct_{R}_{cen}_oh')
    if m and o:
        print(f'   R = {R} {cen} A = {A}: here {fmt(m)}   earlier {o[0]:.3f} +- {o[1]:.3f}   difference {m[0] - o[0]:+.3f} +- {math.hypot(m[1], o[1]):.3f}')
