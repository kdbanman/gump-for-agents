#!/usr/bin/env python3
"""Independent fits for the review of research/constant/ (claims 2 to 6). Own weighted least squares (numpy), own
points (data.py). Nothing from research/constant/*.py is imported.

    python3 research/audit/constant/fits.py            # -> stdout (committed copy: out_fits.txt)
"""
import math, os, sys
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as C2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data  # noqa: E402

np.set_printoptions(linewidth=150)


# ------------------------------------------------------------------------------------------ fitting
class R:
    pass


def wls(cols, pts, floor=0.0, se_key='se'):
    """linear model y = sum theta_j * cols[j](p). Returns object with theta, cov, chi2, dof, p, resid."""
    X = np.array([[f(p) for f in cols] for p in pts], float)
    y = np.array([p['y'] for p in pts]); s = np.sqrt(np.array([p[se_key] for p in pts]) ** 2 + floor ** 2)
    Xw, yw = X / s[:, None], y / s
    th, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
    cov = np.linalg.pinv(Xw.T @ Xw)
    r = R(); r.theta, r.cov = th, cov
    r.res = y - X @ th; r.z = r.res / s
    r.chi2 = float((r.z ** 2).sum()); r.dof = len(pts) - len(cols)
    r.p = float(C2.sf(r.chi2, r.dof)) if r.dof > 0 else float('nan')
    r.err = np.sqrt(np.diag(cov))
    r.pred = lambda q: (float(np.array([f(q) for f in cols]) @ th),
                        math.sqrt(float(np.array([f(q) for f in cols]) @ cov @ np.array([f(q) for f in cols]))))
    r.cols = cols
    return r


def nls(f, t0, pts, floor=0.0, poisson=False, bounds=None):
    """nonlinear; Gaussian in ln tau (se = 1/sqrt(F)) or exact Poisson deviance 2F(e^d - 1 - d), d = y - f."""
    y = np.array([p['y'] for p in pts]); s = np.sqrt(np.array([p['se'] for p in pts]) ** 2 + floor ** 2)
    Fd = np.array([p.get('F', 1 / p['se'] ** 2) for p in pts], float)

    def res(t):
        d = y - np.array([f(t, p) for p in pts])
        if poisson:
            return np.sign(d) * np.sqrt(np.maximum(2 * Fd * (np.exp(d) - 1 - d), 0))
        return d / s
    kw = dict(xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=50000, x_scale='jac')
    if bounds:
        kw['bounds'] = bounds
    o = least_squares(res, np.array(t0, float), **kw)
    r = R(); r.theta = o.x; r.chi2 = float((o.fun ** 2).sum()); r.dof = len(pts) - len(t0)
    r.p = float(C2.sf(r.chi2, r.dof)) if r.dof > 0 else float('nan')
    J = o.jac
    r.cov = np.linalg.pinv(J.T @ J); r.err = np.sqrt(np.abs(np.diag(r.cov))); r.z = o.fun
    return r


def pv(chi2, dof):
    return float(C2.sf(chi2, dof)) if dof > 0 else float('nan')


one = lambda p: 1.0              # noqa
Ac = lambda p: float(p['A'])     # noqa
kc = lambda p: float(p['k'])     # noqa
lnA = lambda p: math.log(p['A'])  # noqa
ik = lambda p: 1.0 / p['k']      # noqa
ik2 = lambda p: 1.0 / p['k'] ** 2  # noqa
lnk = lambda p: math.log(p['k'])  # noqa
sq = lambda p: math.sqrt(p['A'])  # noqa
iA = lambda p: 1.0 / p['A']       # noqa
s_ = lambda p: float(p['rect'][0])  # noqa
M_ = lambda p: float(p['rect'][1])  # noqa
Fb = lambda p: p['F_b']             # noqa


def ind(s):
    return lambda p: 1.0 if p['rect'][0] == s else 0.0


def line(t, r, names):
    return f'{t:46s} chi2 {r.chi2:8.1f}/{r.dof:<2d} p {r.p:7.2g}  ' + '  '.join(
        f'{n} {v:+.4f}+-{e:.4f}' for n, v, e in zip(names, r.theta, r.err))


# ------------------------------------------------------------------------------------------ data
per = data.periodic()
rect = sorted([p for p in per if p['rect'] and p['rect'][0] >= 4 and p['A'] >= 60], key=lambda p: (p['rect'], p['A']))
wide = [p for p in per if p['Q1'] >= 12]
hull = data.hull()                      # includes the CPU A = 108 single death (differs from theirs by +0.0003)
H45 = hull[1:]
print(f'{len(rect)} rectangular classes s >= 4, A >= 60: ' + ', '.join(f'{p["rect"][0]}x{p["rect"][1]}' for p in rect))
print(f'{len(wide)} wide classes; {len(hull)} hull sizes')

# ------------------------------------------------------------------------------------------ 1. hull
print('\n=== 1. hull, one family')
print('local slopes: ' + ', '.join(f'{u["A"]}->{v["A"]} {(v["y"]-u["y"])/(v["A"]-u["A"]):.4f}+-'
                                   f'{math.hypot(u["se"], v["se"])/(v["A"]-u["A"]):.4f}' for u, v in zip(hull, hull[1:])))
HF = {'H0': ([one, Ac], ['a', 'c']), 'H1 rim k': ([one, Ac, kc], ['a', 'c', 'r']),
      'HL lnA': ([one, Ac, lnA], ['a', 'c', 'p']), 'H 1/k': ([one, Ac, ik], ['a', 'c', 'q']),
      'H 1/A': ([one, Ac, iA], ['a', 'c', 'q']), 'H sqrtA': ([one, Ac, sq], ['a', 'c', 'r']),
      'H2 k + 1/k': ([one, Ac, kc, ik], ['a', 'c', 'r', 'q']), 'H k + lnk': ([one, Ac, kc, lnk], ['a', 'c', 'r', 'q']),
      'H k + 1/k^2': ([one, Ac, kc, ik2], ['a', 'c', 'r', 'q']), 'H lnA + 1/k': ([one, Ac, lnA, ik], ['a', 'c', 'p', 'q'])}
for sel, t in ((hull, 'six sizes'), (H45, 'A >= 45'), (hull[2:], 'A >= 63')):
    print(f'-- {t}')
    for nm, (cols, names) in HF.items():
        if len(sel) >= len(cols):
            print('  ' + line(nm, wls(cols, sel), names))

# hold-outs (claim 6, hull part)
print('-- hold-outs, hull A >= 45: fit without the largest 1 (2), forecast; z = res/sqrt(se^2 + ferr^2*max(1,chi2/dof))')
for nm in ('H0', 'H1 rim k', 'HL lnA'):
    cols, names = HF[nm]
    for nh in (1, 2):
        tr, ho = H45[:-nh], H45[-nh:]
        r = wls(cols, tr)
        infl = max(1, r.chi2 / r.dof) if r.dof > 0 else 1
        zs = []; ds = []
        for q in ho:
            yf, ef = r.pred(q); d = q['y'] - yf; ds.append(d); zs.append(d / math.sqrt(q['se'] ** 2 + ef ** 2 * infl))
        print(f'   {nm:10s} -{nh}: sum z^2 {sum(z*z for z in zs):5.1f}/{nh}, max |res| {max(map(abs, ds)):.3f}; c {r.theta[1]:.4f}')

# ------------------------------------------------------------------------------------------ 2. periodic
print('\n=== 2. periodic rectangular, s = 4, 5, 6, A >= 60')
for s in (4, 5, 6):
    ps = [p for p in rect if p['rect'][0] == s]
    print(f'  s = {s}: ' + ', '.join(f'{p["A"]}:{p["y"]:.4f}' for p in ps) + ';  slopes ' + ', '.join(
        f'{(v["y"]-u["y"])/(v["A"]-u["A"]):.4f}+-{math.hypot(u["se"], v["se"])/(v["A"]-u["A"]):.4f}' for u, v in zip(ps, ps[1:])))
    if len(ps) >= 3:
        print('     ' + line('a + cA', wls([one, Ac], ps), ['a', 'c']))
PF = {'PA': ([one, Ac], ['a', 'c']), 'PO a(s)': ([ind(4), ind(5), ind(6), Ac], ['a4', 'a5', 'a6', 'c']),
      'PM -beta M': ([one, Ac, M_], ['a', 'c', 'b']), 'PS alpha s': ([one, Ac, s_], ['a', 'c', 'al']),
      'PSM': ([one, Ac, s_, M_], ['a', 'c', 'al', 'b']), 'Pcw': ([one, Ac, Fb], ['a', 'c', 'kap']),
      # per-width offsets and a width-dependent cost per cell, c - D g(s), extrapolated to s -> infinity
      'a(s) + A(c - D/s)': ([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] / p['rect'][0]], ['a4', 'a5', 'a6', 'c', 'D']),
      'a(s) + A(c - D/s^2)': ([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] / p['rect'][0] ** 2], ['a4', 'a5', 'a6', 'c', 'D']),
      'a(s) + A(c - D e^-s/0.72)': ([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] * math.exp(-p['rect'][0] / 0.72)],
                                    ['a4', 'a5', 'a6', 'c', 'D']),
      'a(s) + A(c - D e^-s/1.0)': ([ind(4), ind(5), ind(6), Ac, lambda p: -p['A'] * math.exp(-p['rect'][0] / 1.0)],
                                   ['a4', 'a5', 'a6', 'c', 'D']),
      'a + A(c - D/s)  (one offset)': ([one, Ac, lambda p: -p['A'] / p['rect'][0]], ['a', 'c', 'D']),
      'a + A(c - D/s^2) (one offset)': ([one, Ac, lambda p: -p['A'] / p['rect'][0] ** 2], ['a', 'c', 'D']),
      }
PR = {}
for nm, (cols, names) in PF.items():
    r = wls(cols, rect); PR[nm] = r
    print('  ' + line(nm, r, names))

# ------------------------------------------------------------------------------------------ 3. the tension
print('\n=== 3. tension: c_hull - c_per for every pair of one-term forms (separate fits), and the joint one-c fit')


def joint(hcols, pcols, hp, pp, floor=0.0, poisson=False, extra=None):
    """one c; hull columns (without A) and periodic columns (without A); returns chi2, dof, c, and the parts."""
    nh, npc = len(hcols), len(pcols)

    def f(t, p):
        c = t[0]
        if p['fam'] == 'hull':
            v = c * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:1 + nh], hcols))
            if extra == 'gpu-offset' and any('A10G' in s for s in p['srcs']):
                v += t[-1]
            return v
        return c * p['A'] + sum(ti * g(p) for ti, g in zip(t[1 + nh:1 + nh + npc], pcols))
    t0 = [0.21] + [0.0] * (nh + npc) + ([0.0] if extra else [])
    return nls(f, t0, hp + pp, floor=floor, poisson=poisson)


HC = {'rim': [one, kc], 'log': [one, lnA], '1/k': [one, ik], 'sqrtA': [one, sq]}
PC = {'offsets': [ind(4), ind(5), ind(6)], 'long side': [one, M_], 'cap. wave': [one, Fb], 'short side': [one, s_],
      'both sides': [one, s_, M_], 'a(s)+D/s': [ind(4), ind(5), ind(6), lambda p: -p['A'] / p['rect'][0]],
      'a(s)+D/s^2': [ind(4), ind(5), ind(6), lambda p: -p['A'] / p['rect'][0] ** 2]}
print(f'{"hull":6s} x {"periodic":11s} {"c_hull":>16s} {"c_per":>16s} {"diff":>18s} | joint chi2/dof   p      penalty')
rows = []
for hn, hc in HC.items():
    rh = wls([Ac] + hc, H45)
    for pn, pc in PC.items():
        rp = wls([Ac] + pc, rect)
        d = rh.theta[0] - rp.theta[0]; e = math.hypot(rh.err[0], rp.err[0])
        j = joint(hc, pc, H45, rect)
        pen = j.chi2 - rh.chi2 - rp.chi2
        rows.append((hn, pn, d, e, j, pen))
        print(f'{hn:6s} x {pn:11s} {rh.theta[0]:.4f}+-{rh.err[0]:.4f}  {rp.theta[0]:.4f}+-{rp.err[0]:.4f}  '
              f'{d:+.4f}+-{e:.4f} ({d/e:4.1f}s) | {j.chi2:7.1f}/{j.dof:<2d} {j.p:7.2g}  {pen:7.1f}   '
              f'(hull chi2 alone {rh.chi2:.1f}/{rh.dof}, per {rp.chi2:.1f}/{rp.dof})')

print('\n-- the same, with error floors added in quadrature to every point (systematics of 0.003 / 0.005 / 0.01)')
for floor in (0.003, 0.005, 0.01):
    for hn in ('rim', 'log'):
        for pn in ('offsets', 'long side', 'both sides'):
            hc, pc = HC[hn], PC[pn]
            rh = nls(lambda t, p: t[0] * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:], hc)), [0.21, 0, 0], H45, floor)
            rp = nls(lambda t, p: t[0] * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:], pc)), [0.21] + [0] * len(pc),
                     rect, floor)
            j = joint(hc, pc, H45, rect, floor=floor)
            d = rh.theta[0] - rp.theta[0]; e = math.hypot(rh.err[0], rp.err[0])
            print(f'  floor {floor}: {hn:4s} x {pn:10s}  diff {d:+.4f}+-{e:.4f} ({d/e:4.1f}s)  joint {j.chi2:6.1f}/{j.dof} '
                  f'p {j.p:.2g}  penalty {j.chi2 - rh.chi2 - rp.chi2:6.1f}')

print('\n-- exact Poisson likelihood (deviance), instead of Gaussian 1/sqrt(F), log x long side and rim x offsets:')
for hn, pn in (('log', 'long side'), ('rim', 'offsets'), ('log', 'both sides')):
    j = joint(HC[hn], PC[pn], H45, rect, poisson=True)
    print(f'  {hn} x {pn}: joint deviance {j.chi2:.1f}/{j.dof}, c {j.theta[0]:.4f}')

print('\n-- hull subsets (log x long side; rim x offsets): drop A = 135; drop A = 108 and 135; GPU-only hull points;'
      ' A >= 63; a free CPU/GPU offset on the hull')
hsets = {'A>=45 all': H45, 'A>=45 no 135': H45[:-1], 'A 45..84': H45[:-2], 'A>=63': hull[2:],
         'GPU only (63..135)': data.hull(('gpu',)), 'CPU only (45..84)': [p for p in data.hull(('cpu',)) if 45 <= p['A'] <= 84]}
for hs_n, hs in hsets.items():
    for hn, pn in (('log', 'long side'), ('rim', 'offsets'), ('log', 'both sides')):
        hc = HC[hn]
        if len(hs) < 3:
            continue
        rh = wls([Ac] + hc, hs)
        rp = wls([Ac] + PC[pn], rect)
        j = joint(hc, PC[pn], hs, rect)
        d = rh.theta[0] - rp.theta[0]; e = math.hypot(rh.err[0], rp.err[0])
        print(f'  {hs_n:20s} {hn:4s} x {pn:10s} c_hull {rh.theta[0]:.4f}+-{rh.err[0]:.4f} (chi2 {rh.chi2:.1f}/{rh.dof})'
              f'  diff {d:+.4f}+-{e:.4f} ({d/e:4.1f}s)  joint {j.chi2:.1f}/{j.dof} p {j.p:.2g}')
for hn, pn in (('log', 'long side'), ('rim', 'offsets')):
    j = joint(HC[hn], PC[pn], H45, rect, extra='gpu-offset')
    print(f'  free GPU offset on hull points, {hn} x {pn}: joint {j.chi2:.1f}/{j.dof} p {j.p:.2g}, c {j.theta[0]:.4f}, '
          f'offset {j.theta[-1]:+.4f}+-{j.err[-1]:.4f}')

print('\n-- single-c descriptions with two-term hull corrections (all six hull sizes, and A >= 45)')
H2C = {'k + 1/k': [one, kc, ik], 'k + ln k': [one, kc, lnk], 'k + 1/k^2': [one, kc, ik2], 'lnA + 1/k': [one, lnA, ik],
       'k + lnA': [one, kc, lnA], 'sqrtA + 1/A': [one, sq, iA]}
for hs_n, hs in (('six sizes', hull), ('A >= 45', H45)):
    for hn, hc in H2C.items():
        for pn in ('offsets', 'long side', 'cap. wave', 'both sides', 'a(s)+D/s'):
            j = joint(hc, PC[pn], hs, rect)
            rh = wls([Ac] + hc, hs); rp = wls([Ac] + PC[pn], rect)
            hp = [z for z, p in zip(j.z, hs + rect) if p['fam'] == 'hull']
            print(f'  {hs_n:9s} {hn:11s} x {pn:10s} joint {j.chi2:6.1f}/{j.dof:<2d} p {j.p:7.2g}  c {j.theta[0]:.4f}  '
                  f'hull pars ' + ' '.join(f'{v:+.3f}' for v in j.theta[1:1 + len(hc)]) +
                  f'  hull chi2 {sum(z*z for z in hp):.1f}  sep c_hull {rh.theta[0]:.4f}+-{rh.err[0]:.4f}')

print('\n-- saturating slope on the hull, ln tau = a + cA - D*lam*(1 - exp(-A/lam))  (slope c - D e^{-A/lam}), A >= 30')
for hs_n, hs in (('six', hull), ('A>=45', H45)):
    best = None
    for lam0 in (10, 30, 60, 120):
        try:
            r = nls(lambda t, p: t[0] + t[1] * p['A'] - t[2] * t[3] * (1 - math.exp(-p['A'] / t[3])), [0, 0.22, 0.05, lam0], hs,
                    bounds=([-50, 0, -5, 1], [50, 1, 5, 2000]))
        except Exception:
            continue
        if best is None or r.chi2 < best.chi2:
            best = r
    print(f'  {hs_n}: chi2 {best.chi2:.2f}/{best.dof}, c {best.theta[1]:.4f}+-{best.err[1]:.4f}, D {best.theta[2]:+.3f}, '
          f'lambda {best.theta[3]:.1f}')

# ------------------------------------------------------------------------------------------ 4. kappa
print('\n=== 4. the capillary-wave coefficient kappa: ln tau = a + cA + kappa F  (or a_A + kappa F at one area)')


def kfit(pts, floor=0.0, per_area=False):
    if per_area:
        As = sorted({p['A'] for p in pts})
        cols = [(lambda A_: (lambda p: 1.0 if p['A'] == A_ else 0.0))(A_) for A_ in As] + [Fb]
        r = wls(cols, pts, floor)
        return r, r.theta[-1], r.err[-1]
    r = wls([one, Ac, Fb], pts, floor)
    return r, r.theta[2], r.err[2]


cen = [p for p in per if p['A'] in (48, 60)]
sels = {
    'census A48,60 Q1>=7': [p for p in cen if p['Q1'] >= 7],
    'census A48,60 Q1>=12': [p for p in cen if p['Q1'] >= 12],
    'census A48,60 Q1>=3': cen,
    'census A48,60,72 Q1>=7': [p for p in per if p['A'] in (48, 60, 72) and p['Q1'] >= 7],
    'wide Q1>=12 all areas': wide,
    'wide Q1>=13': [p for p in per if p['Q1'] >= 13],
    'Q1>=7 all areas': [p for p in per if p['Q1'] >= 7],
    'A=48 alone Q1>=7': [p for p in per if p['A'] == 48 and p['Q1'] >= 7],
    'A=60 alone Q1>=7': [p for p in per if p['A'] == 60 and p['Q1'] >= 7],
    'A=72 alone Q1>=7': [p for p in per if p['A'] == 72 and p['Q1'] >= 7],
    'A=48 alone Q1>=12': [p for p in per if p['A'] == 48 and p['Q1'] >= 12],
    'A=60 alone Q1>=12': [p for p in per if p['A'] == 60 and p['Q1'] >= 12],
    'A=72 alone Q1>=12': [p for p in per if p['A'] == 72 and p['Q1'] >= 12],
}
print(f'{"selection":26s} {"n":>3s} | {"a+cA+kF: kappa":>16s} chi2/dof  infl.err | {"a_A + kF (one offset per area)":>30s}'
      f' | floor 0.015: kappa')
for nm, ps in sels.items():
    if len(ps) < 4:
        continue
    r, k, e = kfit(ps)
    infl = e * math.sqrt(max(1, r.chi2 / r.dof))
    r2, k2, e2 = kfit(ps, per_area=True)
    infl2 = e2 * math.sqrt(max(1, r2.chi2 / r2.dof)) if r2.dof > 0 else float('nan')
    r3, k3, e3 = kfit(ps, floor=0.015)
    print(f'{nm:26s} {len(ps):3d} | {k:+.3f}+-{e:.3f} {r.chi2:7.1f}/{r.dof:<2d} +-{infl:.3f} | '
          f'{k2:+.3f}+-{e2:.3f} {r2.chi2:7.1f}/{r2.dof:<2d} +-{infl2:.3f} | {k3:+.3f}+-{e3:.3f} (chi2 {r3.chi2:.1f}/{r3.dof})')

print('-- jackknife and leave-one-class-out on "census A48,60 Q1>=7"')
ps = sels['census A48,60 Q1>=7']
ks = []
for i in range(len(ps)):
    _, k, _ = kfit(ps[:i] + ps[i + 1:]); ks.append(k)
    print(f'   without A={ps[i]["A"]} {ps[i]["gram"]}: kappa {k:+.3f}')
ks = np.array(ks); n = len(ks)
print(f'   jackknife error {math.sqrt((n - 1) / n * ((ks - ks.mean()) ** 2).sum()):.3f}; range {ks.min():+.3f} .. {ks.max():+.3f}')
print('-- profile of chi2 against fixed kappa, census A48,60 Q1>=7 (a, c free), raw and scaled by chi2_min/dof')
r0, k0, _ = kfit(ps)
for kap in (-0.6, -0.8, -0.9, -1.0, -1.1, -1.2, -1.3, -1.5):
    r = wls([one, Ac], [dict(p, y=p['y'] - kap * p['F_b']) for p in ps])
    print(f'   kappa {kap:+.1f}: chi2 {r.chi2:7.1f}; delta {r.chi2 - r0.chi2:7.1f}; scaled delta '
          f'{(r.chi2 - r0.chi2) / (r0.chi2 / r0.dof):6.2f}')
print('-- what spans F in that set, and the residuals of the kappa fit')
for p, z, d in zip(ps, r0.z, r0.res):
    print(f'   A={p["A"]} {str(p["gram"]):>13} F {p["F_b"]:.4f} y {p["y"]:.4f}+-{p["se"]:.4f}  res {d:+.4f} ({z:+.1f}s)')

# ------------------------------------------------------------------------------------------ 5. loop slopes
print('\n=== 5. cost per cell between areas, by shortest loop (classes of one Q1 pooled per area), and its deficit')
for A1, A2 in ((48, 60), (60, 72)):
    pts = []
    for q in (3, 4, 7, 12, 13, 16):
        u = [p for p in per if p['A'] == A1 and p['Q1'] == q]; v = [p for p in per if p['A'] == A2 and p['Q1'] == q]
        if not (u and v):
            continue
        def pool(ps):
            w = np.array([1 / p['se'] ** 2 for p in ps]); return float((w * [p['y'] for p in ps]).sum() / w.sum()), w.sum() ** -0.5
        (yu, eu), (yv, ev) = pool(u), pool(v)
        pts.append(dict(q=q, s=math.sqrt(q), y=(yv - yu) / (A2 - A1), se=math.hypot(eu, ev) / (A2 - A1), nu=len(u), nv=len(v)))
    print(f'  {A1}->{A2}: ' + ', '.join(f'Q1 {p["q"]} {p["y"]:.4f}+-{p["se"]:.4f} ({p["nu"]}/{p["nv"]} classes)' for p in pts))
    for nm, f, t0 in (('c - D exp(-s/xi)', lambda t, p: t[0] - t[1] * math.exp(-p['s'] / t[2]), [0.21, 1.0, 0.7]),
                      ('c - D/s^2', lambda t, p: t[0] - t[1] / p['q'], [0.21, 0.3])):
        r = nls(f, t0, pts)
        print(f'     {nm:18s} chi2 {r.chi2:6.1f}/{r.dof}  ' + ' '.join(f'{v:.4f}+-{e:.4f}' for v, e in zip(r.theta, r.err)))
    for drop in (3, 4):
        sub = [p for p in pts if p['q'] != drop]
        r = nls(lambda t, p: t[0] - t[1] * math.exp(-p['s'] / t[2]), [0.21, 1.0, 0.7], sub)
        print(f'     exp form without Q1 {drop}: chi2 {r.chi2:.1f}/{r.dof} c {r.theta[0]:.4f} xi {r.theta[2]:.3f}+-{r.err[2]:.3f}')
    sub = [p for p in pts if p['q'] >= 7]
    r = nls(lambda t, p: t[0] - t[1] * math.exp(-p['s'] / t[2]), [0.21, 1.0, 0.7], sub)
    print(f'     exp form on Q1 >= 7 only: chi2 {r.chi2:.1f}/{r.dof} c {r.theta[0]:.4f} xi {r.theta[2]:.3f}+-{r.err[2]:.3f}')
