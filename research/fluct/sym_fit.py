#!/usr/bin/env python3
"""Symmetric (O_h) face residences from qsd_sym*/qsd_snap* runs: table, fits of ln tau(A) for cube-centred states,
the vertex/cube factor at equal area, and the extrapolation to the side-17 first plateau (cube-centred, A = 828).
Writes research/fluct/data/sym_residence.csv.     python3 research/fluct/sym_fit.py
"""
import glob, math, os, sys
import numpy as np
from scipy import stats
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(fl.SCR, 'qsd_sym*.npz')) + glob.glob(os.path.join(fl.SCR, 'qsd_snap*.npz'))):
    z = np.load(f); t = os.path.basename(f)[4:-4]; A = len(z['H']) - 1
    d, e = int(z['deaths'][0]), float(z['expo'][0])
    cen = 'v' if (t.endswith('v') or t.startswith('snap')) else 'c'
    H = z['H'].astype(float); k = np.arange(A + 1); N = H.sum(); mu = (k * H).sum() / N; var = ((k - mu) ** 2 * H).sum() / N
    rows.append(dict(tag=t, A=A, cen=cen, deaths=d, expo=e, mean=mu / A, var=var / A))
os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
with open(os.path.join(HERE, 'data', 'sym_residence.csv'), 'w') as fh:
    fh.write('tag,A,centre,deaths,exposure,tau,ln_tau,se_ln,lo90,hi90,mean_per_site,var_per_site\n')
    print(f'{"run":28s} {"A":>4s} c {"deaths":>6s} {"tau":>10s} {"ln tau":>7s} {"+-":>5s}  90% CI of tau           n/A    var/A')
    for r in sorted(rows, key=lambda r: (r['A'], r['cen'])):
        d, e = r['deaths'], r['expo']
        if d:
            lo, hi = stats.chi2.ppf([0.05, 0.95], 2 * d) / 2
            tau = e / d; r.update(tau=tau, ln=math.log(tau), se=1 / math.sqrt(d), lo=e / hi, hi=e / lo)
        else:
            lo = stats.chi2.ppf(0.90, 2) / 2; r.update(tau=None, ln=None, se=None, lo=e / lo, hi=None)   # 90% lower bound: E / 2.30
        s = (f'{r["tag"]:28s} {r["A"]:4d} {r["cen"]} {d:6d} {r["tau"] or 0:10.4g} {r["ln"] or 0:7.2f} {r["se"] or 0:5.2f}  '
             f'{r["lo"]:.3g} .. {r["hi"] if r["hi"] else float("inf"):.3g}   {r["mean"]:.3f}  {r["var"]:.2f}')
        print(s if d else s + '   (no death: tau > lo at 90%)')
        fh.write(f'{r["tag"]},{r["A"]},{r["cen"]},{d},{e:.6g},{r["tau"] or ""},{r["ln"] or ""},{r["se"] or ""},{r["lo"]:.4g},{r["hi"] or ""},{r["mean"]:.4f},{r["var"]:.3f}\n')

# pool by (A, centre)
pool = {}
for r in rows:
    p = pool.setdefault((r['A'], r['cen']), [0, 0.0]); p[0] += r['deaths']; p[1] += r['expo']
C = sorted((A, math.log(e / d), 1 / math.sqrt(d)) for (A, c), (d, e) in pool.items() if c == 'c' and d >= 10)
V = sorted((A, math.log(e / d), 1 / math.sqrt(d), d, e) for (A, c), (d, e) in pool.items() if c == 'v' and d >= 3)
A_, y, s = map(np.array, zip(*C))
print(f'\ncube-centred points used (deaths >= 10): {[int(a) for a in A_]}')
forms = {
    'a + bA': lambda A: np.stack([np.ones_like(A), A], 1),
    'a + bA + c sqrt(A)': lambda A: np.stack([np.ones_like(A), A, np.sqrt(A)], 1),
    'a + bA + cA^2': lambda A: np.stack([np.ones_like(A), A, A ** 2], 1),
    'a + (0.209/6)A + c sqrt(A)': None,
}
preds = {}
for name, X in forms.items():
    if X is None:
        yy = y - 0.209 / 6 * A_; Xm = np.stack([np.ones_like(A_), np.sqrt(A_)], 1)
        f = lambda Aq, b: b[0] + 0.209 / 6 * Aq + b[1] * np.sqrt(Aq); Xq = lambda Aq: np.stack([np.ones_like(Aq), np.sqrt(Aq)], 1)
    else:
        yy = y; Xm = X(A_); f = lambda Aq, b, X=X: X(np.atleast_1d(Aq).astype(float)) @ b; Xq = X
    W = 1 / s ** 2
    cov = np.linalg.inv(Xm.T @ (Xm * W[:, None])); b = cov @ (Xm.T @ (W * yy))
    chi2 = float(((Xm @ b - yy) ** 2 * W).sum()); dof = len(A_) - len(b)
    out = []
    for Aq in (693, 759, 828, 1053):   # 1053 = the legacy side-19 cube, properly confined: an extrapolation far outside the data
        xq = Xq(np.array([float(Aq)]))[0]; m = float(xq @ b) + (0.209 / 6 * Aq if X is None else 0)
        se = math.sqrt(float(xq @ cov @ xq)) * max(1.0, math.sqrt(chi2 / max(dof, 1)))
        out.append((Aq, m, se))
    preds[name] = out
    print(f'  {name:28s} coef {np.round(b, 6)}  chi2 {chi2:.1f}/{dof}  -> ' + '; '.join(f'A={a}: ln tau {m:.2f} +- {e:.2f}' for a, m, e in out))
print('\nvertex-centred points:', [(a, round(l, 2), d) for a, l, _, d, _ in V])
for a, l, se, d, e in V:
    cc = [(m, e2) for (Aq, m, e2) in preds['a + bA + c sqrt(A)'] if Aq == a]
    direct = [(lc, sc) for (Ac, lc, sc) in C if Ac == a]
    ref = direct[0] if direct else (cc[0] if cc else None)
    if ref:
        if a == 693:   # fresh soups only (no copies of the cube16 snapshots); this is the value the notebook / STATUS quote
            sv = [r for r in rows if r['A'] == 693 and r['cen'] == 'v' and not r['tag'].startswith('snap')]
            dv, ev = sum(r['deaths'] for r in sv), sum(r['expo'] for r in sv)
            sc = [r for r in rows if r['A'] == 693 and r['cen'] == 'c']
            dc, ec = sum(r['deaths'] for r in sc), sum(r['expo'] for r in sc)
            print(f'  A=693, fresh soups only ({dv} vertex deaths, {dc} cube deaths): ln(tau_v / tau_c) = {math.log((ev / dv) / (ec / dc)):+.2f} +- {math.hypot(1 / math.sqrt(dv), 1 / math.sqrt(dc)):.2f}  (factor {(ev / dv) / (ec / dc):.2f}; the line below pools the cube16 copies into the vertex value)')
        print(f'  A={a}: ln(tau_v / tau_c) = {l - ref[0]:+.2f} +- {math.hypot(se, ref[1]):.2f}  (factor {math.exp(l - ref[0]):.2f}; reference {"measured" if direct else "fit"})')
