#!/usr/bin/env python3
"""Second batch for the review of research/constant/: penalty p-values of the one-c test, the forms the analysis
did not try (1/k, 1/A, saturating slope) jointly and out of sample, the out-of-sample table (claim 6), and the
discriminating power of the three proposed measurements (claim 8).

    python3 research/audit/constant/extra.py      # -> stdout (committed copy: out_extra.txt)
"""
import math, os, sys
import numpy as np
from scipy.stats import chi2 as C2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402
import contextlib, io  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    from fits import (wls, nls, one, Ac, kc, lnA, ik, iA, sq, s_, M_, Fb, ind, rect, hull, H45, wide, joint, HC, PC)  # noqa



def pen_line(hn, hc, pn, pc, hs, tag=''):
    rh = wls([Ac] + hc, hs); rp = wls([Ac] + pc, rect); j = joint(hc, pc, hs, rect)
    pen = j.chi2 - rh.chi2 - rp.chi2
    return (f'  {tag:8s} {hn:6s} x {pn:11s} c_hull {rh.theta[0]:.4f}+-{rh.err[0]:.4f} c_per {rp.theta[0]:.4f}+-{rp.err[0]:.4f}'
            f' | joint c {j.theta[0]:.4f}, chi2 {j.chi2:6.1f}/{j.dof} p {j.p:.2g} | penalty {pen:6.1f} on 1: p {C2.sf(pen, 1):.2g}'
            f' ({math.sqrt(max(pen, 0)):.1f} sigma)')


print('=== A. the one-c test as a 1-dof penalty (the joint p dilutes it), one-term hull forms, A >= 45 and A >= 63')
HC2 = dict(HC); HC2['1/A'] = [one, iA]
for hs, tag in ((H45, 'A>=45'), (hull[2:], 'A>=63')):
    for hn in ('rim', 'log', '1/k', '1/A'):
        for pn in ('offsets', 'long side', 'both sides', 'a(s)+D/s'):
            print(pen_line(hn, HC2[hn], pn, PC[pn], hs, tag))

print('\n=== B. saturating slope on the hull: ln tau = a + cA - D lam (1 - e^{-A/lam}), jointly with one c')


def sat(t, p, o=0):
    return t[o] + t[o + 1] * p['A'] - t[o + 2] * t[o + 3] * (1 - math.exp(-p['A'] / t[o + 3]))


for pn in ('offsets', 'long side', 'both sides', 'a(s)+D/s'):
    pc = PC[pn]; npc = len(pc)

    def f(t, p):
        c = t[0]
        if p['fam'] == 'hull':
            a, D, lam = t[1:4]
            return a + c * p['A'] - D * lam * (1 - math.exp(-p['A'] / lam))
        return c * p['A'] + sum(ti * g(p) for ti, g in zip(t[4:], pc))
    best = None
    for lam0 in (8, 12, 20, 40):
        r = nls(f, [0.21, 0.0, 0.05, lam0] + [0.0] * npc, hull + rect,
                bounds=([0, -50, -5, 1] + [-np.inf] * npc, [1, 50, 5, 2000] + [np.inf] * npc))
        if best is None or r.chi2 < best.chi2:
            best = r
    hz = [z for z, p in zip(best.z, hull + rect) if p['fam'] == 'hull']
    sep = nls(lambda t, p: sat(t, p), [0, 0.215, 0.3, 12], hull, bounds=([-50, 0, -5, 1], [50, 1, 5, 2000]))
    rp = wls([Ac] + pc, rect)
    pen = best.chi2 - sep.chi2 - rp.chi2
    print(f'  six hull sizes x {pn:11s}: joint chi2 {best.chi2:.1f}/{best.dof} p {best.p:.2g}, c {best.theta[0]:.4f}, '
          f'D {best.theta[2]:+.3f} lam {best.theta[3]:.1f}; hull part {sum(z*z for z in hz):.1f}; penalty {pen:.1f} '
          f'(p {C2.sf(pen, 1):.2g}); hull alone chi2 {sep.chi2:.2f}/{sep.dof} c {sep.theta[1]:.4f}+-{sep.err[1]:.4f}')
print('  hull alone, saturating, local slopes it implies: ' + ', '.join(
    f'{A1}->{A2} {(sat(sep.theta, dict(A=A2)) - sat(sep.theta, dict(A=A1))) / (A2 - A1):.4f}'
    for A1, A2 in ((30, 45), (45, 63), (63, 84), (84, 108), (108, 135), (135, 165))))

print('\n=== C. hull hold-outs for the forms not tried (fit without the largest 1 / 2 of A >= 45, forecast)')
HF = {'H1 rim k': [one, Ac, kc], 'HL lnA': [one, Ac, lnA], 'H 1/k': [one, Ac, ik], 'H 1/A': [one, Ac, iA]}
for nm, cols in HF.items():
    out = []
    for nh in (1, 2):
        r = wls(cols, H45[:-nh]); infl = max(1, r.chi2 / r.dof) if r.dof > 0 else 1
        zz = []
        for q in H45[-nh:]:
            yf, ef = r.pred(q); d = q['y'] - yf; zz.append((d, d / math.sqrt(q['se'] ** 2 + ef ** 2 * infl)))
        out.append(f'-{nh}: sum z^2 {sum(z*z for _, z in zz):.1f}/{nh}, residuals ' + ', '.join(f'{d:+.3f}' for d, _ in zz))
    r = wls(cols, H45)
    y9, e9 = r.pred(dict(A=165, k=10))
    print(f'  {nm:9s} ' + '; '.join(out) + f';  all A>=45 -> ln tau(165) = {y9:.2f} +- {e9:.2f}')

print('\n=== D. out-of-sample table (claim 6), periodic rectangular s >= 4')
by = {s: [p for p in rect if p['rect'][0] == s] for s in (4, 5, 6)}
L1 = [by[s][-1] for s in (4, 5, 6)]; L2 = by[4][-2:] + by[5][-2:] + by[6][-2:]
PF = {'PA': [one, Ac], 'PO': [ind(4), ind(5), ind(6), Ac], 'PM': [one, Ac, M_], 'PS': [one, Ac, s_],
      'PSM': [one, Ac, s_, M_], 'Pcw': [one, Ac, Fb]}
for nm, cols in PF.items():
    cells = []
    for nh, ho in ((1, L1), (2, L2)):
        if nm == 'PO' and nh == 2:
            cells.append('-'); continue
        tr = [p for p in rect if p not in ho]
        r = wls(cols, tr); infl = max(1, r.chi2 / r.dof) if r.dof > 0 else 1
        z2 = 0; mx = 0
        for q in ho:
            yf, ef = r.pred(q); d = q['y'] - yf; z2 += d * d / (q['se'] ** 2 + ef ** 2 * infl); mx = max(mx, abs(d))
        cells.append(f'{z2:.1f}/{len(ho)}, {mx:.2f}')
    print(f'  {nm:4s} -1: {cells[0]:14s} -2: {cells[1]}')
for s in (4, 5):
    ps = by[s]
    cells = []
    for nh in (1, 2):
        r = wls([one, Ac], ps[:-nh]); infl = max(1, r.chi2 / r.dof) if r.dof > 0 else 1
        z2 = 0; mx = 0
        for q in ps[-nh:]:
            yf, ef = r.pred(q); d = q['y'] - yf; z2 += d * d / (q['se'] ** 2 + ef ** 2 * infl); mx = max(mx, abs(d))
        cells.append(f'{z2:.1f}/{nh}, {mx:.2f}')
    print(f'  s={s} PA -1: {cells[0]:14s} -2: {cells[1]}')
big = [p for p in wide if p['A'] >= 105]; tr = [p for p in wide if p['A'] < 105]
for nm, cols in (('PA', [one, Ac]), ('Pcw', [one, Ac, Fb])):
    r = wls(cols, tr); infl = max(1, r.chi2 / r.dof)
    z2 = 0; mx = 0
    for q in big:
        yf, ef = r.pred(q); d = q['y'] - yf; z2 += d * d / (q['se'] ** 2 + ef ** 2 * infl); mx = max(mx, abs(d))
    print(f'  wide {nm}: held-out A >= 105 ({len(big)}): {z2:.1f}/{len(big)}, max |res| {mx:.2f}')
print('  hull A>=45: see fits.py section 1 (H0 -1 2.1/1 0.38, -2 9.7/2 0.39; H1 0.1/1 0.10, 1.4/2 0.11; HL 0.2/1 0.12, 1.9/2 0.14)')

print('\n=== E. would the proposed measurements discriminate?')
# 1. equilateral tori: slope under the massless reading is exactly c (F constant); under the massive reading
# (deficit fitted on census Q1>=7 classes, between 60 and 72) the local slope is c - g d(A S)/dA with S the lattice sum.
eqA = [(48, 16), (57, 19), (63, 21), (75, 25), (81, 27), (84, 28), (93, 31), (108, 36), (111, 37)]
print('  1. equilateral tori: shortest loop^2 = n = A/3; massive deficit of the slope D e^{-s/xi} with the two loop-fits:')
for D, xi, c in ((1.0556, 0.742, 0.2122), (1.1722, 0.7148, 0.2171)):
    row = ', '.join(f'A={A}: {c - D * math.exp(-math.sqrt(n) / xi):.4f}' for A, n in eqA)
    print(f'     D {D}, xi {xi}, c {c}: {row}')
print('     -> the deficit is < 0.0012 for n >= 19: from A = 57 on, the massive and massless readings differ by less '
      'than the +-0.001 the plan buys. What the plan does decide: whether the constant-shape slope is ~0.209-0.212 or ~0.218+.')
# 2. hull faces of equal area, different rim: rim term per rim cell -0.06 (H1) vs +0.05..0.07 (two-term)
print('  2. equal-area hulls: 10^4 deaths -> +-0.010 in ln tau; six rim cells x (0.06 + 0.06) = 0.7 between readings: '
      '70 sigma, if a constant per corner and the corner angle are not changed at the same time (they are, for a '
      'truncated face: 3 -> up to 6 corners).')
# 3. width 6: slope 108 -> 126 with 6x6 at 2000 and 6x7 at 800 deaths
for F66, F67 in ((592, 92), (2000, 400), (2000, 800)):
    e = math.hypot(1 / math.sqrt(F66), 1 / math.sqrt(F67)) / 18
    print(f'  3. width 6: 6x6 {F66} deaths, 6x7 {F67}: slope error {e:.4f}; 0.208 vs 0.215 separated by {0.007/e:.1f} sigma;'
          f' vs 0.2127 (c of a(s)+A(c-D/s)): {(0.2127-0.2082)/e:.1f} sigma')
r = wls([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] / p['rect'][0]], rect)
print(f'     now: a(s) + A(c - D/s) gives c = {r.theta[3]:.4f} +- {r.err[3]:.4f}; its 6-wide slope c - D/6 = '
      f'{r.theta[3] - r.theta[4] / 6:.4f}')
# what precision on the 6-wide slope would pin c in the a(s)+A(c-D/s) model: simulate the error with a hypothetical
# 6x7 of F deaths at the model value
for F67 in (400, 800, 3000):
    pts = [dict(p) for p in rect]
    for p in pts:
        if p['rect'] == (6, 7):
            p['se'] = 1 / math.sqrt(F67)
        if p['rect'] == (6, 6):
            p['se'] = 1 / math.sqrt(2000)
    rr = wls([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] / p['rect'][0]], pts)
    print(f'     with 6x6 at 2000 and 6x7 at {F67} deaths: c(a(s)+A(c-D/s)) error {rr.err[3]:.4f} (now {r.err[3]:.4f})')
# a 7-wide torus instead: 7x7 (A = 147)? cost
print('     alternative: the s=5 family to 5x9 / 5x10 (A = 135, 150) is cheaper per unit of lever on D than s=6.')
for extra_pts in ((('5x9', 135, 5, 9, 300),), (('5x9', 135, 5, 9, 300), ('6x7', 126, 6, 7, 400))):
    pts = [dict(p) for p in rect]
    for nm, A_, s, M, F in extra_pts:
        found = [p for p in pts if p['rect'] == (s, M)]
        if found:
            found[0]['se'] = 1 / math.sqrt(F)
        else:
            pts.append(dict(fam='per', A=A_, rect=(s, M), y=0.0, se=1 / math.sqrt(F)))
    X = np.array([[f(p) for f in [ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] / p['rect'][0]]] for p in pts])
    w = np.array([1 / p['se'] for p in pts])
    cov = np.linalg.pinv((X * w[:, None]).T @ (X * w[:, None]))
    print(f'     adding {[e[0] + " (" + str(e[4]) + " deaths)" for e in extra_pts]}: error on c {math.sqrt(cov[3, 3]):.4f}, '
          f'on D {math.sqrt(cov[4, 4]):.4f}')

print('\n=== F. a better discriminator: the hull local slope 84 -> 108 (and 108 -> 135) under each description that')
print('    passes, single c or not; A = 108 runs at ~2,100 hull-face deaths per GPU-hour (R15_s1), A = 84 at ~5e5')
from fits import lnk, ik2  # noqa: E402


def hull_pred(cols_h, theta_h, c, A):
    k = data.kside(A) if A in (30, 45, 63, 84, 108, 135, 165) else None
    p = dict(A=A, k=k)
    return c * A + sum(t * g(p) for t, g in zip(theta_h, cols_h))


cands = []
for hn, hc in (('log', [one, lnA]), ('1/k', [one, ik]), ('1/A', [one, iA]), ('rim', [one, kc])):
    r = wls([Ac] + hc, H45)
    cands.append((f'hull alone, {hn} (A>=45)', hc, r.theta[1:], r.theta[0]))
for hn, hc, hs in (('k + 1/k (six), one c with long side', [one, kc, ik], hull),
                   ('k + 1/k^2 (six), one c with long side', [one, kc, ik2], hull),
                   ('1/A (A>=45), one c with a(s)+D/s', [one, iA], H45),
                   ('1/k (A>=45), one c with a(s)+D/s', [one, ik], H45)):
    pn = 'long side' if 'long' in hn else 'a(s)+D/s'
    j = joint(hc, PC[pn], hs, rect)
    cands.append((hn, hc, j.theta[1:1 + len(hc)], j.theta[0]))
for nm, hc, th, c in cands:
    y = {A: hull_pred(hc, th, c, A) for A in (84, 108, 135, 165)}
    print(f'  {nm:42s} c {c:.4f}: slope 84->108 {(y[108]-y[84])/24:.4f}, 108->135 {(y[135]-y[108])/27:.4f}, '
          f'135->165 {(y[165]-y[135])/30:.4f}')
print('  saturating, one c with a(s)+D/s: c 0.2155, slopes 84->108 0.2155, 108->135 0.2156 (section B)')
for F108, F84 in ((1060, 34368), (10000, 34368), (10000, 300000), (20000, 300000)):
    e = math.hypot(F108 ** -0.5, F84 ** -0.5) / 24
    print(f'  A=108 at {F108} deaths, A=84 at {F84}: slope 84->108 error {e:.4f}; GPU-hours for A=108 '
          f'{max(0, F108 - 1060) / 2118:.1f}, A=84 {max(0, F84 - 34368) / 5.1e5:.1f}')

print('\n=== G. a massive-type hull correction in the side: ln tau = a + A (c - D e^{-k/xi}), alone and with one c')
fm = lambda t, p: t[0] + p['A'] * (t[1] - t[2] * math.exp(-p['k'] / t[3]))  # noqa: E731
best = None
for x0 in (0.5, 1, 2, 4):
    r = nls(fm, [0, 0.215, 0.1, x0], hull, bounds=([-50, 0, 0, 0.05], [50, 1, 100, 50]))
    best = r if best is None or r.chi2 < best.chi2 else best
print(f'  hull alone, six sizes: chi2 {best.chi2:.2f}/{best.dof} p {best.p:.2g}; c {best.theta[1]:.4f}+-{best.err[1]:.4f}, '
      f'D {best.theta[2]:.3f}, xi {best.theta[3]:.3f} (units of the side k)')
for pn in ('offsets', 'long side', 'both sides', 'a(s)+D/s'):
    pc = PC[pn]; npc = len(pc)

    def f(t, p):
        if p['fam'] == 'hull':
            return t[1] + p['A'] * (t[0] - t[2] * math.exp(-p['k'] / t[3]))
        return t[0] * p['A'] + sum(ti * g(p) for ti, g in zip(t[4:], pc))
    bj = None
    for x0 in (0.5, 1, 2, 4):
        r = nls(f, [0.21, 0, 0.1, x0] + [0.0] * npc, hull + rect, bounds=([0, -50, 0, 0.05] + [-np.inf] * npc,
                                                                            [1, 50, 100, 50] + [np.inf] * npc))
        bj = r if bj is None or r.chi2 < bj.chi2 else bj
    rp = wls([Ac] + pc, rect)
    pen = bj.chi2 - best.chi2 - rp.chi2
    print(f'  one c with {pn:10s}: joint chi2 {bj.chi2:.1f}/{bj.dof} p {bj.p:.2g}; c {bj.theta[0]:.4f}; xi {bj.theta[3]:.2f}; '
          f'penalty {pen:.1f} (p {C2.sf(max(pen, 0), 1):.2g})')
