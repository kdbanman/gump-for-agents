#!/usr/bin/env python3
"""nine.py: the nine equilateral face tori of claude/gpu-local-1080 (16271f3) recomputed from the rows, checked
against the committed age tables, and fitted by the forms of REVIEW-gpu-local-tori.md section 3 plus forms whose slope
rises with size; what each surviving form says for the price per cell at large A.

    python3 nine.py <checkout of claude/gpu-local-1080>     # -> nine_out.txt (beside this file)

Values: ln tau_face = ln(2E/F) +- 1/sqrt(F), E and F summed over a torus's rows. Fits: weighted least squares; the one
nonlinear parameter of a form is profiled on a grid and then refined by curve_fit; errors of derived quantities
from the covariance (absolute sigma), scaled by sqrt(chi2/dof) when that exceeds 1. "c_inf" is lim d ln tau / dA.
"""
import csv, glob, json, math, os, sys
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2 as CHI2

WT = sys.argv[1]
D = os.path.join(WT, 'research', 'data', 'gpu_local_eqtorus')
out = []
pr = lambda s='': out.append(s)

# ---- 1. values, seeds, cross-check with hist_*.json --------------------------------------------------------------
V, NOCUT, LAYERS = {}, {}, {}
tot_seed_chi2, tot_seed_dof = 0.0, 0
pr('A    lattice    runs  face deaths  ln tau_face          seeds chi2 (dof, p)   hist == rows   kind5  per-seed ln tau')
for path in sorted(glob.glob(os.path.join(D, 'eqtorus_*.csv'))):
    rows = list(csv.DictReader(open(path)))
    A = int(rows[0]['A']); lat = rows[0]['torus']
    E = sum(int(r['exposure']) for r in rows); F = sum(int(r['face']) for r in rows)
    v, e = math.log(2 * E / F), 1 / math.sqrt(F)
    c2 = sum((int(r['face']) - F * int(r['exposure']) / E) ** 2 / (F * int(r['exposure']) / E) for r in rows)
    dof = len(rows) - 1
    if dof:
        tot_seed_chi2 += c2; tot_seed_dof += dof
    h = json.load(open(os.path.join(D, 'hist_' + lat.replace(',', '_') + '.json')))['runs']
    ok = all(sum(h[r['seed']]['hist']['exposure']) == int(r['exposure']) and sum(h[r['seed']]['hist']['ends']['1']) == int(r['face'])
             for r in rows)
    k5 = sum(int(r['guard']) for r in rows)
    ps = ', '.join(f'{math.log(2 * int(r["exposure"]) / int(r["face"])):.4f}' for r in rows)
    pr(f'{A:3d}  ({lat:8s})  {len(rows)}   {F:10d}   {v:.4f} +- {e:.4f}   '
       + (f'{c2:5.2f} ({dof}, {CHI2.sf(c2, dof):.3f})' if dof else '      -         ') + f'      {ok}         {k5}    {ps}')
    V[A] = (v, e, F, rows, h)
pr(f'seed-to-seed chi2 over all tori: {tot_seed_chi2:.2f} on {tot_seed_dof} (p = {CHI2.sf(tot_seed_chi2, tot_seed_dof):.2f})')

# ---- 2. hazard by age, per torus, from the committed tables -------------------------------------------------------
pr('\nhazard of a face death by age / pooled mean hazard (bins merged to >= 300 deaths; ages in mean lives m = E/F per lane)')
for A in sorted(V):
    v, e, F, rows, h = V[A]
    ed = np.array(h[rows[0]['seed']]['hist']['edges'], float)
    ex = np.sum([h[r['seed']]['hist']['exposure'] for r in rows], 0).astype(float)
    dd = np.sum([h[r['seed']]['hist']['ends']['1'] for r in rows], 0).astype(float)
    m = ex.sum() / dd.sum(); rate = 1 / m
    cells, i = [], 0
    while i < len(ex):
        j, x, f = i, 0.0, 0.0
        while j < len(ex) and (f < 300 or x == 0):
            x += ex[j]; f += dd[j]; j += 1
        if x > 0 and (f >= 300 or not cells):
            cells.append((ed[i], ed[j], f, x))
        elif x > 0:
            lo, _, f0, x0 = cells.pop(); cells.append((lo, ed[j], f0 + f, x0 + x))
        i = j
    z = [(f - x * rate) / math.sqrt(x * rate) for lo, hi, f, x in cells]
    pr(f'{A:3d} (m = {m:.3g}, run {int(rows[0]["gens"]) / m:.2f} m): ' + '; '.join(
        f'[{lo / m:.2g},{hi / m:.2g}) {f / x / rate:.3f}+-{math.sqrt(f) / x / rate:.3f}' for lo, hi, f, x in cells)
       + f'   chi2 {sum(t * t for t in z):.1f} on {len(z) - 1}')

# ---- 3. fits -----------------------------------------------------------------------------------------------------
Aall = np.array(sorted(V), float)
yall = np.array([V[a][0] for a in Aall]); eall = np.array([V[a][1] for a in Aall])
L = lambda A: np.sqrt(A / 3.0)
NC = lambda A: np.isin(np.round(A), [57, 63, 93, 111]).astype(float)     # tori with 2 transverse layers (no firewall)


def fit(f, p0, A, y, e):
    p, C = curve_fit(f, A, y, p0=p0, sigma=e, absolute_sigma=True, maxfev=400000)
    c2 = float((((f(A, *p) - y) / e) ** 2).sum()); dof = len(A) - len(p)
    return p, C, c2, dof


def deriv(fun, p, C, s):
    g = np.zeros(len(p)); v0 = fun(p)
    for i in range(len(p)):
        h = 1e-6 * max(1, abs(p[i])); dp = np.array(p, float); dp[i] += h
        g[i] = (fun(dp) - v0) / h
    return v0, s * math.sqrt(max(0.0, g @ C @ g))


FORMS = [  # name, f(A, linear params..., theta), theta grid or None, c_inf(p) or None (diverges)
    ('L  line', lambda A, a, c: a + c * (A - 63), None, lambda p: p[1]),
    ('B  broken line (kink A0)', lambda A, a, c, g, A0: a + c * (A - 63) - g * np.maximum(0, A0 - A), np.linspace(48.5, 92, 872), lambda p: p[1]),
    ('E  a + cA - g exp(-(l-4)/lam)', lambda A, a, c, g, lam: a + c * (A - 63) - g * np.exp(-(L(A) - 4) / lam), np.geomspace(0.02, 50, 500), lambda p: p[1]),
    ('P  a + cA - g (48/A)^q', lambda A, a, c, g, q: a + c * (A - 63) - g * (48.0 / A) ** q, np.geomspace(0.05, 300, 500), lambda p: p[1]),
    ('M  a + A[c - g exp(-l/xi)]', lambda A, a, c, g, xi: a + A * (c - g * np.exp(-L(A) / xi)), np.geomspace(0.02, 50, 500), lambda p: p[1]),
    ('Q  a + cA + g1/A + g2/A^2', lambda A, a, c, g1, g2: a + c * (A - 63) + g1 / A + g2 / A ** 2, None, lambda p: p[1]),
    ('S  a + cA - g exp(-(A/A0)^6)', lambda A, a, c, g, A0: a + c * (A - 63) - g * np.exp(-(A / A0) ** 6), np.linspace(20, 140, 1201), lambda p: p[1]),
    ('H  a + cA - g (A0-A)+^2', lambda A, a, c, g, A0: a + c * (A - 63) - g * np.maximum(0, A0 - A) ** 2, np.linspace(49, 120, 711), lambda p: p[1]),
    ('Kq quadratic a + c(A-63) + k(A-63)^2', lambda A, a, c, k: a + c * (A - 63) + k * (A - 63) ** 2, None, None),
    ('R  a + cA + g/A (slope rises to c)', lambda A, a, c, g: a + c * (A - 63) + g / A, None, lambda p: p[1]),
    ('X  a + cA + g exp(-A/xi) (slope rises to c if g > 0)', lambda A, a, c, g, xi: a + c * (A - 63) + g * np.exp(-A / xi), np.geomspace(3, 3000, 500), lambda p: p[1]),
    ('N  line + d [2 transverse layers]', lambda A, a, c, d: a + c * (A - 63) + d * NC(A), None, lambda p: p[1]),
    ('BK broken line + k(A-63)^2 above', lambda A, a, c, k, g, A0: a + c * (A - 63) + k * np.maximum(0, A - 63) ** 2 - g * np.maximum(0, A0 - A), np.linspace(48.5, 62.9, 145), None),
]


def run_form(name, f, grid, cinf, A, y, e):
    npar = f.__code__.co_argcount - 1
    if len(A) <= npar:
        return None
    if grid is not None:
        best = None
        for th in grid:
            z = np.zeros(npar - 1)
            y0 = f(A, *z, th)
            X = np.stack([f(A, *np.eye(npar - 1)[i], th) - y0 for i in range(npar - 1)], 1)
            beta, *_ = np.linalg.lstsq(X / e[:, None], (y - y0) / e, rcond=None)
            c2 = float(((((X @ beta + y0) - y) / e) ** 2).sum())
            if best is None or c2 < best[0]:
                best = (c2, list(beta) + [th])
        p0 = best[1]
    else:
        p0 = [13, 0.21] + [0] * (npar - 2)
    try:
        p, C, c2, dof = fit(f, p0, A, y, e)
    except Exception as ex:  # noqa: BLE001
        return dict(name=name, fail=str(ex))
    if grid is not None and best[0] < c2 - 1e-6:      # refinement must not lose the grid minimum
        c2 = best[0]
    s = math.sqrt(max(1.0, c2 / dof)) if dof > 0 else 1.0
    r = dict(name=name, p=p, C=C, chi2=c2, dof=dof, pval=CHI2.sf(c2, dof) if dof > 0 else float('nan'), s=s)
    r['res'] = (y - f(A, *p)) / e
    r['pred81'] = deriv(lambda q: f(np.array([81.0]), *q)[0], p, C, s)
    r['slope_hi'] = deriv(lambda q: (f(np.array([111.0]), *q)[0] - f(np.array([93.0]), *q)[0]) / 18, p, C, s)
    r['val150'] = deriv(lambda q: f(np.array([150.0]), *q)[0], p, C, s)
    r['slope150'] = deriv(lambda q: (f(np.array([151.0]), *q)[0] - f(np.array([149.0]), *q)[0]) / 2, p, C, s)
    r['cinf'] = deriv(cinf, p, C, s) if cinf else None
    return r


e57 = eall.copy(); e57[Aall == 57] *= math.sqrt(9.25 / 3)
for label, mask, ee in (('all nine (48-111)', Aall >= 0, eall), ('all nine, the error at 57 scaled by sqrt(9.25/3)', Aall >= 0, e57),
                        ('eight, 57-111', Aall >= 57, eall), ('seven, 63-111', Aall >= 63, eall), ('six, 75-111', Aall >= 75, eall)):
    A, y, e = Aall[mask], yall[mask], ee[mask]
    pr(f'\n=== fits to {label}: A = {", ".join(str(int(a)) for a in A)} ===')
    pr('form                                            chi2/dof   p        c_inf               slope 93-111 (model)   at 81            residuals / sigma')
    for name, f, grid, cinf in FORMS:
        r = run_form(name, f, grid, cinf, A, y, e)
        if r is None:
            continue
        if 'fail' in r:
            pr(f'{name:46s}  fit failed: {r["fail"]}'); continue
        ci = f'{r["cinf"][0]:.5f} +- {r["cinf"][1]:.5f}' if r['cinf'] else 'diverges        '
        pr(f'{name:46s}  {r["chi2"]:6.1f}/{r["dof"]}  {r["pval"]:.2g}  {ci:20s}  {r["slope_hi"][0]:.5f} +- {r["slope_hi"][1]:.5f}   '
           f'{r["pred81"][0]:.4f}+-{r["pred81"][1]:.4f}   ' + ' '.join(f'{x:+.1f}' for x in r['res']))
        if True:
            pr(f'      params {np.array2string(r["p"], precision=5)}; local slope at 150 {r["slope150"][0]:.5f} +- {r["slope150"][1]:.5f}')

# ---- 4. data slopes ----------------------------------------------------------------------------------------------
pr('\nlocal slopes from the data:')
for (a, b) in ((63, 93), (93, 111), (63, 84), (84, 111), (75, 111), (63, 111)):
    s = (V[b][0] - V[a][0]) / (b - a); es = math.hypot(V[a][1], V[b][1]) / (b - a)
    pr(f'  {a} -> {b}: {s:.5f} +- {es:.5f}')
pr('  difference (93->111) - (63->93): '
   f'{(V[111][0] - V[93][0]) / 18 - (V[93][0] - V[63][0]) / 30:+.5f} +- '
   f'{math.sqrt((V[111][1] / 18) ** 2 + (V[93][1] * (1 / 18 + 1 / 30)) ** 2 + (V[63][1] / 30) ** 2):.5f}')

# ---- 5. scatter between lattices, and the line's slope with it -------------------------------------------------
m = Aall >= 63
A, y, e = Aall[m], yall[m], eall[m]
pr('\nline from 63 with an extra scatter t added in quadrature to every point (lattice-to-lattice):')
for t in (0.0, 0.001, 0.002, 0.003, 0.005, 0.01):
    ee = np.sqrt(e ** 2 + t ** 2); w = 1 / ee ** 2
    X = np.vstack([np.ones(len(A)), A - 63]).T
    C = np.linalg.inv(X.T @ (w[:, None] * X)); b = C @ X.T @ (w * y); c2 = float((((y - X @ b) / ee) ** 2).sum())
    pr(f'  t = {t:.3f}: slope {b[1]:.5f} +- {C[1, 1] ** .5:.5f}, at 63 {b[0]:.4f}, chi2 {c2:.2f} on {len(A) - 2} (p {CHI2.sf(c2, len(A) - 2):.2f})')

# ---- 6. hazard at large tori in absolute age ----------------------------------------------------------------------
pr('\nhazard / mean hazard in absolute age (generations), tori 81-111:')
for A in (81, 84, 93, 108, 111):
    v, e, F, rows, h = V[A]
    ed = np.array(h[rows[0]['seed']]['hist']['edges'], float)
    ex = np.sum([h[r['seed']]['hist']['exposure'] for r in rows], 0).astype(float)
    dd = np.sum([h[r['seed']]['hist']['ends']['1'] for r in rows], 0).astype(float)
    rate = dd.sum() / ex.sum(); cuts = [0, 1e7, 1e8, 3.2e8, 1e18]
    cells = []
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        k = (ed[:-1] >= lo) & (ed[:-1] < hi)
        x, f = ex[k].sum(), dd[k].sum()
        if x > 0:
            cells.append(f'[{lo:.0e},{hi:.0e}) {f / x / rate:.3f} +- {math.sqrt(max(f, 1)) / x / rate:.3f} ({int(f)})')
    pr(f'  {A}: ' + '; '.join(cells))

# ---- 7. the earlier review's forecasts by form (research/audit/gpu_local_tori/predictions.txt, 720ee7e) and the card's block 3
FC = {'L/B line from 63': {81: (16.913, .002), 84: (17.539, .003), 108: (22.540, .006), 111: (23.165, .006)},
      'C line + free curvature': {81: (16.913, .003), 84: (17.539, .003), 108: (22.540, .016), 111: (23.165, .019)},
      'S stretched': {81: (16.914, .009), 84: (17.537, .011), 108: (22.515, .029), 111: (23.137, .032)},
      'E loop': {81: (16.927, .023), 84: (17.547, .028), 108: (22.461, .154), 111: (23.070, .181)},
      'M massive-like': {81: (16.927, .023), 84: (17.547, .027), 108: (22.461, .144), 111: (23.071, .168)},
      'card block 3': {81: (16.913, .006), 84: (17.539, .007), 108: (22.540, .014), 111: (23.165, .015)}}
pr('\nforecasts committed before the rows, scored (measured - forecast, in combined errors):')
for k, d in FC.items():
    zs = [(V[a][0] - v) / math.hypot(V[a][1], e) for a, (v, e) in d.items()]
    pr(f'  {k:26s} ' + '  '.join(f'{a}: {V[a][0] - v:+.4f} ({z:+.1f})' for (a, (v, e)), z in zip(d.items(), zs))
       + f'   chi2 {sum(z * z for z in zs):.1f} on 4')

txt = '\n'.join(out)
print(txt)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'nine_out.txt'), 'w').write(txt + '\n')
