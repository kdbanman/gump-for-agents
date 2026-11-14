#!/usr/bin/env python3
"""The main table of research/constant/: every model of ln tau_face(A, geometry), fitted family by family and
jointly, with chi-square, every residual, and out-of-sample forecasts of the largest sizes.

    python3 research/constant/fit.py            # everything (-> stdout; the committed copy is out/main_table.txt)
    python3 research/constant/fit.py -q         # without the per-point residuals

Models are stated in README.md.  Points come from load.py (recomputed from tracked data).  A fit "FAILS" when its
chi-square has p < 0.01 at the statistical errors of the points.
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import load, wls, shape_models as sm  # noqa: E402

Q = '-q' in sys.argv


# ------------------------------------------------------------------------------------------------ model library
def lin(terms):
    return lambda t, p: sum(ti * g(p) for ti, g in zip(t, terms))


one = lambda p: 1.0                                   # noqa: E731
A = lambda p: float(p['A'])                           # noqa: E731
kk = lambda p: float(p['k'])                          # noqa: E731
lnA = lambda p: math.log(p['A'])                      # noqa: E731
invk = lambda p: 1.0 / p['k']                         # noqa: E731
short = lambda p: float(p['rect'][0])                 # noqa: E731
long_ = lambda p: float(p['rect'][1])                 # noqa: E731
Fb = lambda p: p['Fb']                                # noqa: E731


def ind(s):
    return lambda p: 1.0 if p['rect'][0] == s else 0.0


def indA(s):
    return lambda p: float(p['A']) if p['rect'][0] == s else 0.0


invA = lambda p: 1.0 / p['A']                         # noqa: E731
invk2 = lambda p: 1.0 / p['k'] ** 2                   # noqa: E731
sqrtA = lambda p: math.sqrt(p['A'])                   # noqa: E731
XI_W = 0.72     # cube steps: the decay length of the loop-deficit fits (shape_models.py slopes), for PDe


def AoverS(n):
    return lambda p: -p['A'] / p['rect'][0] ** n      # the deficit D enters with a minus sign


def Aexp(xi):
    return lambda p: -p['A'] * math.exp(-p['rect'][0] / xi)


HULL = {  # name: (terms, parameter names)
    'H0  a + cA': ([one, A], ['a', 'c']),
    'H1  a + cA + r k': ([one, A, kk], ['a', 'c', 'r']),
    'HL  a + cA + p lnA': ([one, A, lnA], ['a', 'c', 'p']),
    'Hk  a + cA + q/k': ([one, A, invk], ['a', 'c', 'q']),
    'HA  a + cA + q/A': ([one, A, invA], ['a', 'c', 'q']),
    'Hr  a + cA + rho sqrt(A)': ([one, A, sqrtA], ['a', 'c', 'rho']),
    'H2  a + cA + r k + q/k': ([one, A, kk, invk], ['a', 'c', 'r', 'q']),
    'H2b a + cA + r k + q/k^2': ([one, A, kk, invk2], ['a', 'c', 'r', 'q']),
    'HLk a + cA + p lnA + q/k': ([one, A, lnA, invk], ['a', 'c', 'p', 'q']),
}


def f_sat(t, p):
    """saturating slope: d ln tau / dA = c - D exp(-A/lam)  (a deficit that dies out over lam cells)."""
    a, c, D, lam = t
    return a + c * p['A'] - D * lam * (1 - math.exp(-p['A'] / lam))


def f_side(t, p):
    """a deficit of the cost per cell that decays with the side: a + A (c - D exp(-k/xi))."""
    a, c, D, xi = t
    return a + p['A'] * (c - D * math.exp(-p['k'] / xi))


HULL_NL = {  # name: (f, starts, names, bounds)
    'Hsat a + cA - D lam (1 - e^(-A/lam))': (f_sat, [[0.0, 0.215, 0.3, 12.0], [0.0, 0.22, 1.0, 6.0],
                                                     [0.0, 0.21, 0.1, 30.0]],
                                             ['a', 'c', 'D', 'lam'], ([-50, 0, 0, 1], [50, 1, 5, 300])),
    'Hside a + A (c - D e^(-k/xi))': (f_side, [[0.0, 0.2, 0.5, 2.4], [0.0, 0.21, 0.2, 1.5], [0.0, 0.22, 0.1, 4.0]],
                                      ['a', 'c', 'D', 'xi'], ([-50, 0, 0, 0.2], [50, 1, 50, 20])),
}
RECT = {
    'PA  a + cA': ([one, A], ['a', 'c']),
    'PO  a(s) + cA': ([ind(4), A, ind(5), ind(6)], ['a4', 'c', 'a5', 'a6']),
    'PM  a + cA - beta M': ([one, A, long_], ['a', 'c', 'minus_beta']),
    'PS  a + cA + alpha s': ([one, A, short], ['a', 'c', 'alpha']),
    'PSM a + cA + alpha s + beta M': ([one, A, short, long_], ['a', 'c', 'alpha', 'beta']),
    'PD  a(s) + A (c - D/s)': ([ind(4), A, ind(5), ind(6), AoverS(1)], ['a4', 'c', 'a5', 'a6', 'D']),
    'PD2 a(s) + A (c - D/s^2)': ([ind(4), A, ind(5), ind(6), AoverS(2)], ['a4', 'c', 'a5', 'a6', 'D']),
    'PDe a(s) + A (c - D e^(-s/0.72))': ([ind(4), A, ind(5), ind(6), Aexp(XI_W)], ['a4', 'c', 'a5', 'a6', 'D']),
    'PD1 a(s) + A (c - D e^(-s/1))': ([ind(4), A, ind(5), ind(6), Aexp(1.0)], ['a4', 'c', 'a5', 'a6', 'D']),
    'Pcw a + cA + kappa F': ([one, A, Fb], ['a', 'c', 'kappa']),
}
PER_OFFSETS = ('PO', 'PD ', 'PD2', 'PDe', 'PD1')      # forms with one offset per width


def fitlin(name, lib, pts):
    terms, names = lib[name]
    return wls.fit(name, lin(terms), [0.0] * len(names), pts, names)


def fitnl(name, pts):
    f, starts, names, bounds = HULL_NL[name]
    best = None
    for t0 in starts:
        try:
            r = wls.fit(name, f, t0, pts, names, bounds)
        except Exception:  # noqa
            continue
        if best is None or r.chi2 < best.chi2:
            best = r
    return best


def lab(p):
    if p['fam'] == 'per':
        return sm.label(p)
    return f'{p["fam"]:5s} A={p["A"]:3d} k={p["k"]:2d}'


def show(r, title=None):
    c, e, ei = r.par('c')
    print(f'  {title or r.name:34s} chi2 {r.chi2:9.1f} / {r.dof:<2d} p {r.p:8.2g}  '
          f'{"fits " if r.dof > 0 and r.p >= 0.01 else ("FAILS" if r.dof > 0 else "exact")}  c = {c:.4f} +- {e:.4f} '
          f'(x sqrt(chi2/dof): {ei:.4f})  ' + ' '.join(f'{n} = {v:+.3f}' for n, v in zip(r.names, r.theta) if n != 'c'))
    if not Q:
        for p, d, z in r.resid():
            print(f'        {lab(p):30s} {p["y"]:8.4f} +- {p["se"]:.4f}  resid {d:+.4f} ({z:+.1f} s)')


def holdout(name, fitter, pts, held, tag):
    """fit without `held`, forecast them.  Returns (sum z^2, n, max |resid|, text)."""
    train = [p for p in pts if p not in held]
    try:
        r = fitter(train)
    except Exception as e:  # noqa
        return None
    if r.dof < 0:
        return None
    rows, z2, rms, mean = wls.score(r, held)
    txt = '; '.join(f'{lab(p).strip()}: {d:+.3f} ({z:+.1f} s)' for p, yf, ef, d, z in rows)
    return z2, len(rows), max(abs(d) for *_, d, _ in rows), r, txt


# ------------------------------------------------------------------------------------------------ data
per = load.periodic()
rect = [p for p in per if p['rect'] and p['rect'][0] >= 4 and p['A'] >= 60]          # 4x5 ... 6x7 (11 classes)
wide = [p for p in per if p['Q1'] >= 12]
hull = load.hull()
symc, symv = load.sym('c'), load.sym('v')
SCORES = []     # (family, model, parameters, in-sample chi2/dof, c, holdout results)


def section(t):
    print('\n' + '=' * 110 + '\n' + t + '\n' + '=' * 110)


# ------------------------------------------------------------------------------------------------ 1. hull
section('1. HULL faces (asymmetric octahedra), A = 30 ... 135.  k = side of the face, rim cells = 6k - 3')
print('local slopes: ' + ', '.join(
    f'{u["A"]}->{v["A"]}: {(v["y"]-u["y"])/(v["A"]-u["A"]):.4f} +- {math.hypot(u["se"], v["se"])/(v["A"]-u["A"]):.4f}'
    for u, v in zip(hull, hull[1:])))
for sel, lab_sel in [(hull, 'all six sizes'), (hull[1:], 'A >= 45')]:
    print(f'-- {lab_sel}')
    for name in HULL:
        if len(sel) < len(HULL[name][1]):
            continue
        r = fitlin(name, HULL, sel); show(r)
        hs = []
        for nh in (1, 2):
            h = holdout(name, lambda tr, name=name: fitlin(name, HULL, tr), sel, sel[-nh:], nh)
            if h:
                hs.append((nh, h))
                print(f'      without the largest {nh}: c = {h[3].theta[1]:.4f}; forecast residuals {h[4]}')
        SCORES.append(('hull, ' + lab_sel, name, len(r.theta), r, hs))

print('-- four-parameter forms that are not linear in their parameters, all six sizes')
for name in HULL_NL:
    r = fitnl(name, hull); show(r)
    hs = []
    for nh in (1, 2):
        h = holdout(name, lambda tr, name=name: fitnl(name, tr), hull, hull[-nh:], nh)
        if h:
            hs.append((nh, h))
            print(f'      without the largest {nh}: c = {h[3].theta[1]:.4f}; forecast residuals {h[4]}')
    SCORES.append(('hull, all six sizes', name, 4, r, hs))
print('-- local slopes implied by each form that fits (84->108 measured '
      f'{(hull[4]["y"]-hull[3]["y"])/24:.4f} +- {math.hypot(hull[4]["se"], hull[3]["se"])/24:.4f}):')
for sel, lab_sel, names in [(hull[1:], 'A >= 45', ['H1  a + cA + r k', 'HL  a + cA + p lnA', 'Hk  a + cA + q/k',
                                                    'HA  a + cA + q/A']),
                            (hull, 'six sizes', ['H2  a + cA + r k + q/k', 'H2b a + cA + r k + q/k^2',
                                                 'HLk a + cA + p lnA + q/k'] + list(HULL_NL))]:
    for name in names:
        r = fitnl(name, sel) if name in HULL_NL else fitlin(name, HULL, sel)
        ys = {k_: r.predict(dict(A=3 * k_ * (k_ + 1) // 2, k=k_))[0] for k_ in (7, 8, 9, 10)}
        y10, e10 = r.predict(dict(A=165, k=10))
        print(f'      {name:38s} ({lab_sel}) c = {r.theta[1]:.4f}: 84->108 {(ys[8]-ys[7])/24:.4f}, 108->135 '
              f'{(ys[9]-ys[8])/27:.4f}, 135->165 {(ys[10]-ys[9])/30:.4f}; ln tau(165) = {y10:.2f} +- {e10:.2f}')
print('-- the A = 30 face against the forms fitted to A >= 45:')
for name in ('H1  a + cA + r k', 'HL  a + cA + p lnA', 'Hk  a + cA + q/k', 'HA  a + cA + q/A'):
    r = fitlin(name, HULL, hull[1:]); yf, ef = r.predict(hull[0])
    print(f'      {name}: forecast {yf:.3f} +- {ef:.3f}, measured {hull[0]["y"]:.3f} +- {hull[0]["se"]:.3f}, '
          f'residual {hull[0]["y"] - yf:+.3f}')
print('   rim cells as a share of the face: ' + ', '.join(f'A={p["A"]}: {100*p["rim"]/p["A"]:.0f}%' for p in hull))

# ------------------------------------------------------------------------------------------------ 2. symmetric
section('2. O_h-SYMMETRIC hull faces (cost per cell of the symmetric face, c6; 6 c6 would equal c under "lockstep")')
for S, t in [(symc, 'cube-centred'), (symv, 'vertex-centred')]:
    print(f'-- {t}, A = {S[0]["A"]} ... {S[-1]["A"]}')
    for name in ('H0  a + cA', 'H1  a + cA + r k', 'HL  a + cA + p lnA'):
        r = fitlin(name, HULL, S); show(r)
        print(f'      6 c6 = {6*r.theta[1]:.4f} +- {6*r.err(1):.4f} (inflated {6*r.err(1, True):.4f})')
        hs = []
        for nh in (1, 2):
            h = holdout(name, lambda tr, name=name: fitlin(name, HULL, tr), S, S[-nh:], nh)
            if h:
                hs.append((nh, h))
                print(f'      without the largest {nh}: 6 c6 = {6*h[3].theta[1]:.4f}; forecast residuals {h[4]}')
        SCORES.append(('sym ' + t, name, len(r.theta), r, hs))

# ------------------------------------------------------------------------------------------------ 3. periodic
section('3. PERIODIC faces, rectangular s x M with s >= 4 (11 classes, A = 60 ... 126)')
by = {s: sorted([p for p in rect if p['rect'][0] == s], key=lambda p: p['A']) for s in (4, 5, 6)}
for s, ps in by.items():
    print(f's = {s}: local slopes ' + ', '.join(
        f'{u["A"]}->{v["A"]}: {(v["y"]-u["y"])/(v["A"]-u["A"]):.4f} +- {math.hypot(u["se"], v["se"])/(v["A"]-u["A"]):.4f}'
        for u, v in zip(ps, ps[1:])))
    if len(ps) >= 3:
        r = fitlin('PA  a + cA', RECT, ps); show(r, f'one width, s = {s}: a + cA')
        SCORES.append((f'periodic s = {s}', 'PA  a + cA', 2, r,
                       [(nh, h) for nh in (1, 2) for h in [holdout('', lambda tr: fitlin('PA  a + cA', RECT, tr),
                                                                   ps, ps[-nh:], nh)] if h]))
        for nh, h in SCORES[-1][4]:
            print(f'      without the largest {nh}: c = {h[3].theta[1]:.4f}; forecast residuals {h[4]}')
largest1 = [by[4][-1], by[5][-1], by[6][-1]]
largest2 = by[4][-2:] + by[5][-2:] + by[6][-2:]
print('-- all three widths together')
for name in RECT:
    r = fitlin(name, RECT, rect); show(r)
    hs = []
    for nh, held in ((1, largest1), (2, largest2)):
        if name[:3] in PER_OFFSETS and nh == 2:
            continue                                   # the s = 6 offset cannot be forecast with no s = 6 point
        h = holdout(name, lambda tr, name=name: fitlin(name, RECT, tr), rect, held, nh)
        if h:
            hs.append((nh, h))
            print(f'      without the largest {nh} of each width: c = {h[3].theta[1]:.4f}; residuals {h[4]}')
    SCORES.append(('periodic rect s >= 4', name, len(r.theta), r, hs))
    if name[:3] in ('PD ', 'PD2', 'PDe', 'PD1'):
        c_, D_ = r.theta[1], r.theta[4]
        dfc = {'PD ': lambda s_: D_ / s_, 'PD2': lambda s_: D_ / s_ ** 2, 'PDe': lambda s_: D_ * math.exp(-s_ / XI_W),
               'PD1': lambda s_: D_ * math.exp(-s_)}[name[:3]]
        print(f'      D = {D_:.4f} +- {r.err(4):.4f}; cost per cell of a strip: ' + ', '.join(
            f's = {s_}: {c_ - dfc(s_):.4f}' for s_ in (4, 5, 6, 8, 12)))
for name in ('mexp', 'mk0'):
    r = sm.do_fit(name, rect); show(r, f'{name}  a + A[c - g S(xi)]')
    print(f'      xi = {r.theta[3]:.3f} +- {r.err(3):.3f} cube steps (bound {sm.XI_MAX})')
    hs = []
    for nh, held in ((1, largest1), (2, largest2)):
        h = holdout(name, lambda tr, name=name: sm.do_fit(name, tr), rect, held, nh)
        if h:
            hs.append((nh, h))
            print(f'      without the largest {nh} of each width: c = {h[3].theta[1]:.4f}; residuals {h[4]}')
    SCORES.append(('periodic rect s >= 4', f'{name} a + A[c - g S]', 4, r, hs))

section('3b. PERIODIC faces, every wide class (shortest loop^2 >= 12; 26 classes, A = 48 ... 126)')
big = [p for p in wide if p['A'] >= 105]
for name in ('area', 'cw', 'mexp', 'mk0'):
    r = sm.do_fit(name, wide); show(r, {'area': 'PA  a + cA', 'cw': 'Pcw a + cA + kappa F',
                                         'mexp': 'mexp a + A[c - g S], f = exp', 'mk0': 'mk0  f = K0'}[name])
    if name in ('mexp', 'mk0'):
        print(f'      xi = {r.theta[3]:.3f} +- {r.err(3):.3f} cube steps = {r.theta[3]*math.sqrt(2):.2f} cube sides')
    h = holdout(name, lambda tr, name=name: sm.do_fit(name, tr), wide, big, 1)
    print(f'      without A >= 105 (5 classes): c = {h[3].theta[1]:.4f}; residuals {h[4]}')
    SCORES.append(('periodic wide', {'area': 'PA  a + cA', 'cw': 'Pcw a + cA + kappa F',
                                     'mexp': 'mexp a + A[c - g S]', 'mk0': 'mk0  a + A[c - g S]'}[name],
                   len(r.theta), r, [(1, h)]))
print('-- the same with 0.015 added in quadrature to every error (the size of the unexplained equal-loop pair')
print('   differences, CLAIMS SH2): how well each form describes the data at the level where shape is understood')
FLOOR = 0.015
widef = [dict(p, se=math.hypot(p['se'], FLOOR)) for p in wide]
for name in ('area', 'cw', 'mexp', 'mk0'):
    r = sm.do_fit(name, widef)
    c, e, ei = r.par('c')
    print(f'  {name:5s} chi2 {r.chi2:7.1f} / {r.dof}  p {r.p:.2g}  c = {c:.4f} +- {e:.4f}'
          + (f'  xi = {r.theta[3]:.2f} +- {r.err(3):.2f}' if name in ('mexp', 'mk0') else '')
          + (f'  kappa = {r.theta[2]:.2f} +- {r.err(2):.2f}' if name == 'cw' else ''))

section('3c. Equilateral tori (constant shape: 4x4, 5x5, 6x6)')
eq = sorted([p for p in per if p['gram'][0] == p['gram'][1] == p['gram'][2]], key=lambda p: p['A'])
for u, v in zip(eq, eq[1:]):
    print(f'  {u["A"]} -> {v["A"]}: local slope {(v["y"]-u["y"])/(v["A"]-u["A"]):.4f} +- '
          f'{math.hypot(u["se"], v["se"])/(v["A"]-u["A"]):.4f}')
d = (eq[2]['y'] - eq[1]['y']) / 33 - (eq[1]['y'] - eq[0]['y']) / 27
ed = math.hypot(math.hypot(eq[2]['se'], eq[1]['se']) / 33, math.hypot(eq[1]['se'], eq[0]['se']) / 27)
print(f'  change of slope: {d:+.4f} +- {ed:.4f} ({d/ed:+.1f} sigma)')

# ------------------------------------------------------------------------------------------------ 4. joint
section('4. JOINT fits: one c for hull faces and periodic faces (rectangular, s >= 4).  For each pair of forms:\n'
        '   the two families fitted separately (c_hull, c_per), then with one c.  The test of "one c" is the PENALTY\n'
        '   chi2(joint) - chi2(hull) - chi2(periodic), one degree of freedom; the joint chi2 dilutes it.')
from scipy.stats import chi2 as _chi2, norm as _norm   # noqa: E402


def lin_g(terms):
    return lambda t, p: sum(ti * g(p) for ti, g in zip(t, terms))


# corrections to c A: name -> (g(theta, point), starts, parameter names, bounds, points used)
HC3 = {  # one correction term (3 parameters with a and c): fitted at A >= 45 and at A >= 63
    'rim (r k)': (lin_g([one, kk]), [[0.0, 0.0]], ['a', 'r'], None),
    'log (p lnA)': (lin_g([one, lnA]), [[0.0, 0.0]], ['a', 'p'], None),
    '1/k': (lin_g([one, invk]), [[0.0, 0.0]], ['a', 'q'], None),
    '1/A': (lin_g([one, invA]), [[0.0, 0.0]], ['a', 'q'], None),
}
HC4 = {  # two correction terms or a nonlinear one (4 parameters): fitted to all six sizes
    'k + 1/k': (lin_g([one, kk, invk]), [[0.0, 0.0, 0.0]], ['a', 'r', 'q'], None),
    'k + 1/k^2': (lin_g([one, kk, invk2]), [[0.0, 0.0, 0.0]], ['a', 'r', 'q'], None),
    'lnA + 1/k': (lin_g([one, lnA, invk]), [[0.0, 0.0, 0.0]], ['a', 'p', 'q'], None),
    'saturating': (lambda t, p: t[0] - t[1] * t[2] * (1 - math.exp(-p['A'] / t[2])),
                   [[0.0, 0.3, 12.0], [0.0, 1.0, 6.0], [0.0, 0.1, 30.0], [0.0, 3.0, 5.0]], ['a', 'D', 'lam'],
                   ([-50, 0, 1], [50, 5, 300])),
    'side A D e^(-k/xi)': (lambda t, p: t[0] - p['A'] * t[1] * math.exp(-p['k'] / t[2]),
                           [[0.0, 0.5, 2.4], [0.0, 0.2, 1.5], [0.0, 0.1, 4.0]], ['a', 'D', 'xi'],
                           ([-50, 0, 0.2], [50, 50, 20])),
}
PC = {
    'offsets a(s)': ([ind(4), ind(5), ind(6)], ['a4', 'a5', 'a6']),
    'long side': ([one, long_], ['a', 'minus_beta']),
    'both sides': ([one, short, long_], ['a', 'alpha', 'beta']),
    'a(s), D/s': ([ind(4), ind(5), ind(6), AoverS(1)], ['a4', 'a5', 'a6', 'D']),
    'a(s), D/s^2': ([ind(4), ind(5), ind(6), AoverS(2)], ['a4', 'a5', 'a6', 'D']),
    'a(s), D e^(-s/0.72)': ([ind(4), ind(5), ind(6), Aexp(XI_W)], ['a4', 'a5', 'a6', 'D']),
    'capillary wave': ([one, Fb], ['a', 'kappa']),
}


def fam_fit(g, starts, names, bounds, pts, c0=0.21):
    """c A + g(theta) on one family; several starts for the nonlinear forms."""
    best = None
    for t0 in starts:
        b = None if bounds is None else ([-np.inf] + list(bounds[0]), [np.inf] + list(bounds[1]))
        try:
            r = wls.fit('', lambda t, p: t[0] * p['A'] + g(t[1:], p), [c0] + list(t0), pts, ['c'] + names, b)
        except Exception:  # noqa
            continue
        if best is None or r.chi2 < best.chi2:
            best = r
    return best


def joint(hname, hc, pname, hpts, ppts=None, floor=0.0, quiet=False):
    """Returns a dict: separate fits, the joint fit, the penalty for one c (1 dof) and its p-value."""
    ppts = rect if ppts is None else ppts
    if floor:
        hpts = [dict(p, se=math.hypot(p['se'], floor)) for p in hpts]
        ppts = [dict(p, se=math.hypot(p['se'], floor)) for p in ppts]
    g, hstarts, hnames, hb = hc
    pterms, pnames = PC[pname]
    gp = lin_g(pterms)
    rh = fam_fit(g, hstarts, hnames, hb, hpts)
    rp = fam_fit(gp, [[0.0] * len(pnames)], pnames, None, ppts)
    nh = len(hnames)

    def f(t, p):
        if p['fam'] == 'hull':
            return t[0] * p['A'] + g(t[1:1 + nh], p)
        return t[0] * p['A'] + gp(t[1 + nh:], p)
    names = ['c'] + ['h:' + n for n in hnames] + ['p:' + n for n in pnames]
    b = None
    if hb is not None:
        b = ([-np.inf] + list(hb[0]) + [-np.inf] * len(pnames), [np.inf] + list(hb[1]) + [np.inf] * len(pnames))
    best = None
    starts = [[c0] + list(rh.theta[1:]) + list(rp.theta[1:]) for c0 in (rh.theta[0], rp.theta[0])]
    starts += [[rp.theta[0]] + list(t0) + list(rp.theta[1:]) for t0 in hstarts]
    for t0 in starts:
        try:
            r = wls.fit(f'{hname} x {pname}', f, t0, hpts + ppts, names, b)
        except Exception:  # noqa
            continue
        if best is None or r.chi2 < best.chi2:
            best = r
    r = best
    ch = sum(z * z for p, d_, z in r.resid() if p['fam'] == 'hull')
    pen = max(r.chi2 - rh.chi2 - rp.chi2, 0.0)
    ppen = float(_chi2.sf(pen, 1))
    dc = rh.theta[0] - rp.theta[0]; edc = math.hypot(rh.err(0), rp.err(0))
    out = dict(h=hname, p=pname, rh=rh, rp=rp, r=r, hull_part=ch, pen=pen, ppen=ppen, dc=dc, edc=edc, nh=len(hpts))
    if not quiet:
        ok = lambda x: 'fits' if x.dof > 0 and x.p >= 0.01 else ('FAILS' if x.dof > 0 else 'exact')   # noqa: E731
        print(f'  {hname:20s} x {pname:20s} c_hull {rh.theta[0]:.4f}+-{rh.err(0):.4f} ({rh.chi2:5.1f}/{rh.dof} '
              f'{ok(rh):5s}) c_per {rp.theta[0]:.4f}+-{rp.err(0):.4f} ({rp.chi2:5.1f}/{rp.dof} {ok(rp):5s}) '
              f'diff {dc:+.4f}+-{edc:.4f} | one c {r.theta[0]:.4f}+-{r.err(0):.4f} chi2 {r.chi2:6.1f}/{r.dof:<2d} '
              f'p {r.p:7.2g} hull part {ch:6.1f}/{len(hpts)} | penalty {pen:6.1f} p {ppen:7.2g} '
              f'({math.sqrt(pen):4.1f} s)')
    return out


def passes(o, level=0.01):
    return (o['rh'].dof > 0 and o['rh'].p >= level and o['rp'].p >= level and o['r'].p >= level
            and o['ppen'] >= level)


ALLJ = []
for cut, hp in ((45, hull[1:]), (63, hull[2:])):
    print(f'-- one-term hull corrections, hull faces with A >= {cut} ({len(hp)} sizes)')
    for hname, hc in HC3.items():
        for pname in PC:
            o = joint(hname, hc, pname, hp); o['cut'] = f'A >= {cut}'; ALLJ.append(o)
print('-- four-parameter hull forms, all six hull sizes')
for hname, hc in HC4.items():
    for pname in PC:
        o = joint(hname, hc, pname, hull); o['cut'] = 'six sizes'; ALLJ.append(o)
print('-- two-term hull corrections, hull faces with A >= 45 (5 sizes; the hull form has 1 dof of its own)')
for hname in ('k + 1/k', 'k + 1/k^2', 'lnA + 1/k'):
    for pname in PC:
        o = joint(hname, HC4[hname], pname, hull[1:]); o['cut'] = 'A >= 45 (two terms)'; ALLJ.append(o)

print('\n-- SINGLE-c READINGS THAT PASS: each family\'s form fits its own data (p >= 0.01), the joint fit has\n'
      '   p >= 0.01, and the penalty for one c has p >= 0.01.  (*: all of these at p >= 0.05.)')
print(f'   {"hull points":20s} {"hull form":20s} {"periodic form":20s} {"one c":>16s} {"joint chi2/dof":>15s} '
      f'{"p":>6s} {"penalty":>8s} {"p":>6s}   largest |z|')
PASS = [o for o in ALLJ if passes(o)]
for o in sorted(PASS, key=lambda o: o['r'].theta[0]):
    r = o['r']
    worst = max(r.resid(), key=lambda t: abs(t[2]))
    print(f'   {o["cut"]:20s} {o["h"]:20s} {o["p"]:20s} {r.theta[0]:.4f} +- {r.err(0):.4f} {r.chi2:9.1f}/{r.dof:<3d} '
          f'{r.p:8.2g} {o["pen"]:8.1f} {o["ppen"]:6.2g} {"*" if passes(o, 0.05) else " "} '
          f'{lab(worst[0]).strip()} {worst[2]:+.1f} s')
for title, sel in [('hull A >= 45 or six sizes, p >= 0.01', [o for o in PASS if '63' not in o['cut']]),
                   ('hull A >= 45 or six sizes, p >= 0.05',
                    [o for o in PASS if '63' not in o['cut'] and passes(o, 0.05)]),
                   ('every cut, p >= 0.01', PASS)]:
    cs = [o['r'].theta[0] for o in sel]
    if cs:
        print(f'   range of the single c ({title}): {min(cs):.4f} to {max(cs):.4f} ({len(cs)} pairings)')
print('   pairings in which both forms fit their own family (p >= 0.01), by the significance of the difference:')
both = [o for o in ALLJ if o['rh'].dof > 0 and o['rh'].p >= 0.01 and o['rp'].p >= 0.01 and '63' not in o['cut']
        and 'two terms' not in o['cut']]
for o in sorted(both, key=lambda o: o['pen']):
    print(f'      {o["cut"]:10s} {o["h"]:20s} x {o["p"]:20s} c_hull - c_per = {o["dc"]:+.4f} +- {o["edc"]:.4f}; '
          f'penalty {o["pen"]:6.1f} ({math.sqrt(o["pen"]):4.1f} s)')

if not Q:
    print('\n-- residuals of every point in the single-c readings that pass (hull A >= 45 or six sizes)')
    for o in sorted(PASS, key=lambda o: o['r'].theta[0]):
        if '63' in o['cut']:
            continue
        r = o['r']
        print(f'   {o["cut"]}: {o["h"]} x {o["p"]}: c = {r.theta[0]:.4f}; ' + ', '.join(
            f'{n} = {v:+.4g}' for n, v in zip(r.names[1:], r.theta[1:])))
        for p, d_, z in r.resid():
            print(f'        {lab(p):30s} {p["y"]:8.4f} +- {p["se"]:.4f}  resid {d_:+.4f} ({z:+.1f} s)')
    print('\n-- hull residuals in the six pairings of the first write-up (one hull term, A >= 45)')
    for o in ALLJ:
        if o['cut'] == 'A >= 45' and o['h'] in ('rim (r k)', 'log (p lnA)') and \
                o['p'] in ('offsets a(s)', 'long side', 'capillary wave'):
            print(f'   {o["h"]} x {o["p"]}: c = {o["r"].theta[0]:.4f}')
            for p, d_, z in o['r'].resid():
                if p['fam'] == 'hull':
                    print(f'        {lab(p):30s} {p["y"]:8.4f} +- {p["se"]:.4f}  resid {d_:+.4f} ({z:+.1f} s)')

print('\n-- what each passing single-c reading implies beyond the data (hull A >= 45 or six sizes)')
for o in sorted(PASS, key=lambda o: o['r'].theta[0]):
    if '63' in o['cut']:
        continue
    r = o['r']; nh_ = len(r.names) - 1 - len(PC[o['p']][1])
    g = (HC3.get(o['h']) or HC4[o['h']])[0]
    th = r.theta[1:1 + nh_]; c = r.theta[0]
    y = {k_: c * 1.5 * k_ * (k_ + 1) + g(th, dict(A=1.5 * k_ * (k_ + 1), k=k_)) for k_ in (7, 8, 9, 10, 11, 12)}
    txt = (f'hull slopes 84->108 {(y[8]-y[7])/24:.4f}, 108->135 {(y[9]-y[8])/27:.4f}, 198->234 '
           f'{(y[12]-y[11])/36:.4f}; ln tau(135) {y[9]:.2f}, (165) {y[10]:.2f}')
    if o['p'].startswith('a(s), D'):
        D_ = r.theta[-1]
        dfc = {'a(s), D/s': lambda s_: D_ / s_, 'a(s), D/s^2': lambda s_: D_ / s_ ** 2,
               'a(s), D e^(-s/0.72)': lambda s_: D_ * math.exp(-s_ / XI_W)}[o['p']]
        txt += '; strip cost per cell ' + ', '.join(f's={s_}: {c - dfc(s_):.4f}' for s_ in (4, 5, 6, 8, 12))
        txt += '; offsets a(s) ' + ', '.join(f'{v:+.3f}' for v in r.theta[1 + nh_:1 + nh_ + 3])
    elif o['p'] == 'long side':
        beta = -r.theta[-1]
        txt += '; strip cost per cell ' + ', '.join(f's={s_}: {c - beta / (3 * s_):.4f}' for s_ in (4, 5, 6, 8, 12))
    print(f'   {o["cut"]:20s} {o["h"]:14s} x {o["p"]:20s} c = {c:.4f}: {txt}')

print('\n-- the same test with an error floor added in quadrature to every point (soup transients are bounded at\n'
      '   0.005 in ln tau by the sources; 0.01 is twice that)')
for floor in (0.005, 0.01):
    for hname, pname in (('rim (r k)', 'long side'), ('log (p lnA)', 'long side'), ('log (p lnA)', 'both sides'),
                         ('log (p lnA)', 'a(s), D/s'), ('1/A', 'a(s), D/s'), ('1/A', 'a(s), D/s^2'),
                         ('1/A', 'a(s), D e^(-s/0.72)'), ('1/A', 'offsets a(s)')):
        print(f'   floor {floor}:', end='')
        joint(hname, HC3[hname], pname, hull[1:], floor=floor)

# ------------------------------------------------------------------------------------------------ 5. summary
section('5. SUMMARY: in-sample fit and out-of-sample forecasts (z = residual / sqrt(se^2 + forecast error^2))')
print(f'{"family":24s} {"model":30s} {"par":>3s} {"chi2/dof":>12s} {"p":>8s} {"c":>8s}   '
      f'{"-1: sum z2/n, max|res|":>24s}   {"-2: sum z2/n, max|res|":>24s}')
for fam, name, npar, r, hs in SCORES:
    cval = r.theta[r.names.index('c')] * (6 if fam.startswith('sym') else 1)
    cells = []
    for nh in (1, 2):
        m = [h for n_, h in hs if n_ == nh]
        cells.append(f'{m[0][0]:8.1f}/{m[0][1]}  {m[0][2]:6.3f}' if m else '        -        ')
    print(f'{fam:24s} {name:30s} {npar:3d} {r.chi2:8.1f}/{r.dof:<3d} {r.p:8.2g} {cval:8.4f}   {cells[0]:>24s}   '
          f'{cells[1]:>24s}')
print('(c for the symmetric families is 6 c6.)')
