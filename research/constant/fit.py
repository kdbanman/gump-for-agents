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


HULL = {  # name: (terms, parameter names, what the extra terms mean)
    'H0  a + cA': ([one, A], ['a', 'c']),
    'H1  a + cA + r k': ([one, A, kk], ['a', 'c', 'r']),
    'HL  a + cA + p lnA': ([one, A, lnA], ['a', 'c', 'p']),
    'H2  a + cA + r k + q/k': ([one, A, kk, invk], ['a', 'c', 'r', 'q']),
}
RECT = {
    'PA  a + cA': ([one, A], ['a', 'c']),
    'PO  a(s) + cA': ([ind(4), A, ind(5), ind(6)], ['a4', 'c', 'a5', 'a6']),
    'PM  a + cA - beta M': ([one, A, long_], ['a', 'c', 'minus_beta']),
    'PS  a + cA + alpha s': ([one, A, short], ['a', 'c', 'alpha']),
    'PSM a + cA + alpha s + beta M': ([one, A, short, long_], ['a', 'c', 'alpha', 'beta']),
    'Pcw a + cA + kappa F': ([one, A, Fb], ['a', 'c', 'kappa']),
}


def fitlin(name, lib, pts):
    terms, names = lib[name]
    return wls.fit(name, lin(terms), [0.0] * len(names), pts, names)


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

print('-- the A = 30 face against the forms fitted to A >= 45:')
for name in ('H1  a + cA + r k', 'HL  a + cA + p lnA'):
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
        if name.startswith('PO') and nh == 2:
            continue                                   # the s = 6 offset cannot be forecast with no s = 6 point
        h = holdout(name, lambda tr, name=name: fitlin(name, RECT, tr), rect, held, nh)
        if h:
            hs.append((nh, h))
            print(f'      without the largest {nh} of each width: c = {h[3].theta[1]:.4f}; residuals {h[4]}')
    SCORES.append(('periodic rect s >= 4', name, len(r.theta), r, hs))
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
section('4. JOINT fits: one c for hull faces (A >= 45) and periodic faces (rectangular, s >= 4)')
H = hull[1:]


def joint(hterms, hnames, pterms, pnames, title, hpts=H, ppts=rect):
    """parameters: c, then the hull's, then the periodic family's."""
    def f(t, p):
        c = t[0]
        if p['fam'] == 'hull':
            return c * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:1 + len(hterms)], hterms))
        return c * p['A'] + sum(ti * g(p) for ti, g in zip(t[1 + len(hterms):], pterms))
    names = ['c'] + ['h:' + n for n in hnames] + ['p:' + n for n in pnames]
    r = wls.fit(title, f, [0.21] + [0.0] * (len(names) - 1), hpts + ppts, names)
    ch = sum(z * z for p, d, z in r.resid() if p['fam'] == 'hull')
    cp = r.chi2 - ch
    # separate fits with the same forms
    rh = wls.fit('h', lambda t, p: t[0] * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:], hterms)),
                 [0.21] + [0.0] * len(hterms), hpts, ['c'] + hnames)
    rp = wls.fit('p', lambda t, p: t[0] * p['A'] + sum(ti * g(p) for ti, g in zip(t[1:], pterms)),
                 [0.21] + [0.0] * len(pterms), ppts, ['c'] + pnames)
    dc = rh.theta[0] - rp.theta[0]; edc = math.hypot(rh.err(0), rp.err(0))
    print(f'  {title}')
    print(f'      separately: c_hull = {rh.theta[0]:.4f} +- {rh.err(0):.4f} (chi2 {rh.chi2:.1f}/{rh.dof}), '
          f'c_per = {rp.theta[0]:.4f} +- {rp.err(0):.4f} (chi2 {rp.chi2:.1f}/{rp.dof}); '
          f'difference {dc:+.4f} +- {edc:.4f} ({dc/edc:+.1f} sigma)')
    print(f'      jointly:    c = {r.theta[0]:.4f} +- {r.err(0):.4f}; chi2 {r.chi2:.1f}/{r.dof} (p {r.p:.2g}): '
          f'hull part {ch:.1f} on {len(hpts)} points, periodic part {cp:.1f} on {len(ppts)}; '
          f'penalty for one c: {r.chi2 - rh.chi2 - rp.chi2:.1f} (1 dof)')
    if not Q:
        for p, d_, z in r.resid():
            if p['fam'] == 'hull':
                print(f'        {lab(p):30s} {p["y"]:8.4f} +- {p["se"]:.4f}  resid {d_:+.4f} ({z:+.1f} s)')
    return r, rh, rp


PO_t, PO_n = [ind(4), ind(5), ind(6)], ['a4', 'a5', 'a6']
PM_t, PM_n = [one, long_], ['a', 'minus_beta']
Pcw_t, Pcw_n = [one, Fb], ['a', 'kappa']
J = []
J.append(('H1 x PO', joint([one, kk], ['a', 'r'], PO_t, PO_n, 'hull rim (a + r k)  x  periodic offsets a(s)')))
J.append(('HL x PO', joint([one, lnA], ['a', 'p'], PO_t, PO_n, 'hull log (a + p lnA)  x  periodic offsets a(s)')))
J.append(('H1 x PM', joint([one, kk], ['a', 'r'], PM_t, PM_n, 'hull rim  x  periodic long side (a - beta M)')))
J.append(('HL x PM', joint([one, lnA], ['a', 'p'], PM_t, PM_n, 'hull log  x  periodic long side')))
J.append(('H1 x Pcw', joint([one, kk], ['a', 'r'], Pcw_t, Pcw_n, 'hull rim  x  periodic capillary wave (a + kappa F)')))
J.append(('HL x Pcw', joint([one, lnA], ['a', 'p'], Pcw_t, Pcw_n, 'hull log  x  periodic capillary wave')))
J.append(('H2 x PO', joint([one, kk, invk], ['a', 'r', 'q'], PO_t, PO_n,
                           'hull two-term rim (a + r k + q/k), all six sizes  x  periodic offsets', hpts=hull)))
J.append(('H2 x PM', joint([one, kk, invk], ['a', 'r', 'q'], PM_t, PM_n,
                           'hull two-term rim, all six sizes  x  periodic long side', hpts=hull)))
J.append(('H2 x Pcw', joint([one, kk, invk], ['a', 'r', 'q'], Pcw_t, Pcw_n,
                            'hull two-term rim, all six sizes  x  periodic capillary wave', hpts=hull)))

print('\n  what the two-term hull fits at the periodic constant imply for larger hull faces (forecasts):')
for tag, (r, rh, rp) in J[-3:]:
    c = r.theta[0]; a, rr, q = r.theta[1:4]
    def y(k): return c * 1.5 * k * (k + 1) + a + rr * k + q / k
    print(f'      {tag}: c = {c:.4f}, r = {rr:+.3f} per unit side, q = {q:+.2f};  ln tau(A=135) = {y(9):.2f}, '
          f'(A=165) = {y(10):.2f}; local slopes 108->135 {(y(9)-y(8))/27:.4f}, 135->165 {(y(10)-y(9))/30:.4f}, '
          f'198->234 {(y(12)-y(11))/36:.4f}')
for name in ('H1  a + cA + r k', 'HL  a + cA + p lnA'):
    r = fitlin(name, HULL, H)
    y9, e9 = r.predict(dict(A=135, k=9)); y10, e10 = r.predict(dict(A=165, k=10)); y8, _ = r.predict(dict(A=108, k=8))
    print(f'      {name} (hull alone, A >= 45): ln tau(A=135) = {y9:.2f} +- {e9:.2f}, (A=165) = {y10:.2f} +- {e10:.2f}; '
          f'local slopes 108->135 {(y9-y8)/27:.4f}, 135->165 {(y10-y9)/30:.4f}')

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
