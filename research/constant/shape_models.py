#!/usr/bin/env python3
"""Wrap-around models for periodic slab faces: how the lifetime depends on the way the face closes on itself.

Models (stated in README.md, section "Wrap-around models"):
  area   ln tau = a + c A                                                  2 parameters
  cw     ln tau = a + c A + kappa F(tau)       massless (capillary wave)   3 parameters
         F = -1/2 ln Im tau - 2 ln|eta(tau)|, the log of the free-boson partition function of the face torus
  mexp   ln tau = a + A [c - g S(xi)],  S = sum over nonzero period vectors v of exp(-|v|/xi)     4 parameters
  mk0    the same with the modified Bessel function K0(|v|/xi)                                    4 parameters
  m1     the same, exp, shortest loop only (the vectors of length sqrt(Q1))                       4 parameters

    python3 research/constant/shape_models.py tests      # the in-sample and out-of-sample tests
    python3 research/constant/shape_models.py pairs      # forecasts for the equal-area, equal-loop pairs of shape3
"""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lat, load, wls  # noqa: E402
from scipy.special import k0 as bessel_k0  # noqa: E402

_cache = {}
XI_MAX = 3.0   # in units of |u1| (one cube step in the face plane = sqrt(2) cube sides); a 'massive' correction with a
               # longer range than the faces are wide is degenerate with a + c A and is not the model stated



def radii(l):
    """sqrt(Q) of every nonzero period vector with |v| <= 100 (cached per lattice). With xi <= 3 (the bound used
    in the fits) the neglected terms are below exp(-33)."""
    if l not in _cache:
        _cache[l] = np.sqrt(np.array(lat.vectors(*l, 10000.0), float))
    return _cache[l]


def S(l, xi, kind):
    r = radii(l)
    if kind == 'exp':
        return float(np.exp(-r / xi).sum())
    if kind == 'k0':
        return float(bessel_k0(r / xi).sum())
    if kind == 'one':
        return float(np.exp(-r[r < r[0] + 1e-9] / xi).sum())
    raise ValueError(kind)


def f_area(t, p):
    return t[0] + t[1] * p['A']


def f_cw(t, p):
    return t[0] + t[1] * p['A'] + t[2] * p['Fb']


def mk_massive(kind):
    def f(t, p):
        a, c, lng, xi = t
        return a + p['A'] * (c - math.exp(lng) * S(p['lat'], xi, kind))
    return f


def f_mexp2(t, p):
    a, c, lng, xi, h = t
    s_ = S(p['lat'], xi, 'exp')
    return a + h * s_ + p['A'] * (c - math.exp(lng) * s_)


MODELS = {
    'area': (f_area, [0.0, 0.21], ['a', 'c'], None),
    'cw': (f_cw, [0.0, 0.21, -1.0], ['a', 'c', 'kappa'], None),
    'mexp': (mk_massive('exp'), [0.0, 0.21, 0.0, 0.8], ['a', 'c', 'ln g', 'xi'],
             ([-np.inf, 0, -20, 0.05], [np.inf, 1, 20, XI_MAX])),
    'mk0': (mk_massive('k0'), [0.0, 0.21, 0.0, 0.8], ['a', 'c', 'ln g', 'xi'],
            ([-np.inf, 0, -20, 0.05], [np.inf, 1, 20, XI_MAX])),
    'mexp2': (f_mexp2, [0.0, 0.21, 0.0, 0.8, 0.0], ['a', 'c', 'ln g', 'xi', 'h'],
              ([-np.inf, 0, -20, 0.05, -np.inf], [np.inf, 1, 20, XI_MAX, np.inf])),
    'm1': (mk_massive('one'), [0.0, 0.21, 0.0, 0.8], ['a', 'c', 'ln g', 'xi'],
           ([-np.inf, 0, -20, 0.05], [np.inf, 1, 20, XI_MAX])),
}


def do_fit(name, pts, starts=None):
    f, t0, names, bounds = MODELS[name]
    best = None
    tries = [t0] if name in ('area', 'cw') else [[0.0, 0.21, lg, xi] + ([0.0] if name == 'mexp2' else [])
                                                 for lg in (-3.0, -1.0, 1.0) for xi in (0.4, 0.8, 1.5, 2.5)]
    for t in tries:
        try:
            r = wls.fit(name, f, t, pts, names, bounds)
        except Exception as e:  # noqa
            continue
        if best is None or r.chi2 < best.chi2:
            best = r
    return best


def label(p):
    rect = f' {p["rect"][0]}x{p["rect"][1]}' if p.get('rect') else ''
    return f'A={p["A"]:3d} {str(p["gram"]):>13}{rect}'


def show_fit(r, resid=True):
    print('  ' + r.summary())
    if resid:
        for p, d, z in r.resid():
            print(f'      {label(p):28s} y {p["y"]:8.4f} +- {p["se"]:.4f}  resid {d:+.4f} ({z:+.1f} sigma)')


def show_score(r, pts, title):
    rows, z2, rms, mean = wls.score(r, pts)
    print(f'  forecast of {title}: sum z^2 = {z2:.1f} on {len(rows)} points; rms residual {rms:.3f}, mean {mean:+.3f}')
    for p, yf, ef, d, z in rows:
        print(f'      {label(p):28s} y {p["y"]:8.4f} +- {p["se"]:.4f}  forecast {yf:8.4f} +- {ef:.4f}  '
              f'resid {d:+.4f} ({z:+.1f} sigma)')
    return z2, len(rows), rms, mean


def tests(minq=3, drop4=False, verbose=True):
    per = [p for p in load.periodic() if p['Q1'] >= minq]
    if drop4:
        per = [p for p in per if p['Q1'] != 4]
    census = [p for p in per if p['A'] in (48, 60)]
    a72 = [p for p in per if p['A'] == 72]
    wide = [p for p in per if p['Q1'] >= 12]
    thin = [p for p in per if p['Q1'] < 12]
    out = {}
    for name in MODELS:
        print(f'\n=== model {name} ' + '=' * 60)
        out[name] = {}
        print(f'[1] fitted on the census classes at A = 48 and 60 ({len(census)} points)')
        r = do_fit(name, census); show_fit(r, verbose)
        out[name]['census'] = r
        out[name]['fc72'] = show_score(r, a72, 'the A = 72 classes')
        print(f'[2] fitted on wide faces, Q1 >= 12, every area ({len(wide)} points)')
        r = do_fit(name, wide); show_fit(r, verbose)
        out[name]['wide'] = r
        out[name]['fc_thin'] = show_score(r, thin, 'the thin faces (Q1 < 12)')
        print(f'[3] fitted on thin faces, Q1 < 12 ({len(thin)} points)')
        r = do_fit(name, thin); show_fit(r, verbose)
        out[name]['thin'] = r
        out[name]['fc_wide'] = show_score(r, wide, 'the wide faces (Q1 >= 12)')
        print(f'[4] fitted on every periodic face ({len(per)} points)')
        r = do_fit(name, per); show_fit(r, verbose)
        out[name]['all'] = r
    print('\n=== summary ' + '=' * 60)
    print(f'{"model":6s} {"par":>3s} | {"census chi2/dof":>16s} {"-> A=72 sum z2/n":>18s} {"rms":>6s} | '
          f'{"wide chi2/dof":>14s} {"c(wide)":>9s} {"-> thin rms":>11s} | {"thin chi2/dof":>14s} {"-> wide rms":>11s} | '
          f'{"all chi2/dof":>13s} {"c(all)":>8s}')
    for name, o in out.items():
        c, w, t, a = o['census'], o['wide'], o['thin'], o['all']
        print(f'{name:6s} {len(c.theta):3d} | {c.chi2:9.1f}/{c.dof:<5d} {o["fc72"][0]:11.1f}/{o["fc72"][1]:<5d} '
              f'{o["fc72"][2]:6.3f} | {w.chi2:8.1f}/{w.dof:<4d} {w.theta[1]:9.4f} {o["fc_thin"][2]:11.3f} | '
              f'{t.chi2:8.1f}/{t.dof:<4d} {o["fc_wide"][2]:11.3f} | {a.chi2:8.1f}/{a.dof:<3d} {a.theta[1]:8.4f}')
    return out


# the pairs of research/shape3/PREDICTIONS.md (label, A, X, Y): d = ln tau(Y) - ln tau(X)
PAIRS = [('P1', 48, (2, 2, 8), (1, 6, 16)), ('P2', 60, (1, 5, 20), (1, 4, 20)), ('P3', 60, (1, 8, 20), (2, 2, 10)),
         ('T01', 72, (1, 6, 24), (2, 4, 12)), ('T12', 72, (2, 4, 12), (1, 5, 24)), ('N72', 72, (2, 2, 12), (1, 10, 24)),
         ('Q36', 36, (1, 4, 12), (1, 3, 12)), ('Q45', 45, (1, 5, 15), (1, 4, 15)), ('Q54', 54, (3, 0, 6), (1, 5, 18)),
         ('Q63', 63, (1, 6, 21), (1, 7, 21))]


def mkpt(A, l):
    return dict(A=A, lat=l, Fb=lat.F_boson(*l), gram=lat.gram(*l), y=0.0, se=1.0)


def pair_forecast(r, A, X, Y):
    """d = f(Y) - f(X) with the parameter error propagated through the difference (inflated by chi2/dof)."""
    px, py = mkpt(A, X), mkpt(A, Y)
    d0 = r.f(r.theta, py) - r.f(r.theta, px)
    g = np.zeros(len(r.theta))
    for i in range(len(r.theta)):
        h = 1e-6 * max(1.0, abs(r.theta[i]))
        t = np.array(r.theta, float); t[i] += h
        g[i] = ((r.f(t, py) - r.f(t, px)) - d0) / h
    var = float(g @ r.cov @ g) * (max(1.0, r.chi2 / r.dof) if r.dof > 0 else 1.0)
    return d0, math.sqrt(max(var, 0.0))


def pairs():
    per = [p for p in load.periodic() if p['Q1'] >= 3]
    sets = {
        'W: wide faces (Q1 >= 12), every area [primary]': [p for p in per if p['Q1'] >= 12],
        'C: census classes at A = 48 and 60 with Q1 >= 7': [p for p in per if p['A'] in (48, 60) and p['Q1'] >= 7],
        'C3: census classes at A = 48 and 60, every class (Q1 >= 3)': [p for p in per if p['A'] in (48, 60)],
        'P7: every periodic face with Q1 >= 7': [p for p in per if p['Q1'] >= 7],
    }
    print('pair          gram X -> gram Y           ' + '  '.join(f'{m:>16s}' for m in ('cw', 'mexp', 'mk0')))
    for title, pts in sets.items():
        print(f'\nfitted on: {title} ({len(pts)} points)')
        fits = {m: do_fit(m, pts) for m in ('cw', 'mexp', 'mk0')}
        for m, r in fits.items():
            print('  ' + r.summary())
        for lab, A, X, Y in PAIRS:
            row = []
            for m in ('cw', 'mexp', 'mk0'):
                d, e = pair_forecast(fits[m], A, X, Y)
                row.append(f'{d:+.4f} +- {e:.4f}')
            print(f'  {lab:4s} A={A:2d} {str(lat.gram(*X)):>13} -> {str(lat.gram(*Y)):<13}  ' + '  '.join(row))


def slopes():
    """Cost per cell between areas by shortest loop (classes of equal Q1 pooled by inverse variance in each area),
    and two forms for its deficit: c - D exp(-s/xi) (massive) and c - D/s^2 (massless, long cylinder)."""
    per = [p for p in load.periodic() if p['Q1'] >= 3 and p['A'] in (48, 60, 72)]
    def pooled(A, q):
        ps = [p for p in per if p['A'] == A and p['Q1'] == q]
        if not ps:
            return None
        w = [1 / p['se'] ** 2 for p in ps]
        return sum(wi * p['y'] for wi, p in zip(w, ps)) / sum(w), 1 / math.sqrt(sum(w))
    for A1, A2 in ((48, 60), (60, 72)):
        pts = []
        for q in (3, 4, 7, 12, 13, 16):
            u, v = pooled(A1, q), pooled(A2, q)
            if u and v:
                pts.append(dict(s=math.sqrt(q), q=q, y=(v[0] - u[0]) / (A2 - A1), se=math.hypot(u[1], v[1]) / (A2 - A1)))
        print(f'cost per cell between A = {A1} and {A2}: ' + ', '.join(f'loop^2 {p["q"]}: {p["y"]:.4f} +- {p["se"]:.4f}'
                                                                        for p in pts))
        for nm, f, t0, names in [
                ('c - D exp(-s/xi)', lambda t, p: t[0] - math.exp(t[1]) * math.exp(-p['s'] / t[2]), [0.21, 0.0, 0.7],
                 ['c', 'ln D', 'xi']),
                ('c - D / s^2', lambda t, p: t[0] - t[1] / p['q'], [0.21, 0.3], ['c', 'D']),
                ('c - D / s^n', lambda t, p: t[0] - math.exp(t[1]) * p['s'] ** (-t[2]), [0.21, 0.0, 2.0],
                 ['c', 'ln D', 'n'])]:
            r = wls.fit(nm, f, t0, pts, names)
            print('   ' + r.summary())
            print('      residuals: ' + ', '.join(f'{d:+.4f}' for _, d, _ in r.resid()))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'tests'
    if cmd == 'slopes':
        slopes()
    if cmd == 'tests':
        tests(verbose='-q' not in sys.argv, drop4='--drop4' in sys.argv)
    elif cmd == 'pairs':
        pairs()
