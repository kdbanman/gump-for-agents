"""Lead's own look at ledger row P4 (correlation length of the chaotic phase), 2026-11-15.

Fits the Ornstein-Zernike form S(k) = a + b / (1 + xi^2 k^2) to the producer's spherically averaged structure
factor (research/scratch/phase/sk64.json, written by research/phase/sk.py; not in git: regenerate with sk.py)
over several k ranges, weighted by the file's errors and unweighted. Written without reading the auditor's
p4_oz.py. Run: python3 research/audit/p4_lead_check.py [path-to-sk-json]
"""
import json, sys
import numpy as np
from scipy.optimize import curve_fit

path = sys.argv[1] if len(sys.argv) > 1 else 'research/scratch/phase/sk64.json'
d = json.load(open(path))
edges = np.array(d['kbins'], float)
k = 0.5 * (edges[:-1] + edges[1:])  # bin centres
S, E = np.array(d['all'][0], float), np.array(d['all'][1], float)
cnt = np.array(d['all'][2], float) if len(d['all']) > 2 else np.ones_like(S)
ok = (cnt > 0) & (S > 0) & (k > 0)
k, S, E = k[ok], S[ok], E[ok]
# Files written by sk.py before its error formula was fixed (no 'err' key) carry errors too small by
# sqrt(2 x snapshots): the snapshots were counted twice, and so were both members of each +-k pair.
FIX = 1.0 if 'err' in d else float(np.sqrt(2 * d['snaps']))
f = lambda k, a, b, xi: a + b / (1 + xi * xi * k * k)
print(f'{path}: n = {d["n"]}, {d["snaps"]} snapshots, {len(k)} bins, k from {k[0]:.3f} to {k[-1]:.3f}')
print('range        weights     a      b      xi      chi2/dof')
for kmax in (1.0, 1.5, 2.0, 3.0, 99.0):
    m = k <= kmax
    if m.sum() < 5:
        continue
    for name, sig in (('errors', E[m]), ('none', None)):
        try:
            p, _ = curve_fit(f, k[m], S[m], p0=(0.4, 2.8, 0.7), sigma=sig, absolute_sigma=sig is not None, maxfev=20000)
        except Exception as ex:
            print(f'k <= {kmax:<5} {name:8} fit failed: {ex}')
            continue
        chi = float((((S[m] - f(k[m], *p)) / E[m]) ** 2).sum())
        print(f'k <= {kmax:<5} {name:8} {p[0]:6.3f} {p[1]:6.3f} {abs(p[2]):6.3f}   {chi:9.1f}/{m.sum() - 3}')
# the form quoted in the notebook, S = 0.40 + 2.77 / (1 + xi^2 k^2) with xi = 0.68
chi = float((((S - f(k, 0.40, 2.77, 0.68)) / E) ** 2).sum())
print(f'notebook form (0.40, 2.77, 0.68) on all bins: chi2 {chi:.0f}/{len(k)}; largest |residual| {np.abs(S - f(k, 0.40, 2.77, 0.68)).max():.3f}')
for cone in ('100', '110', '111'):
    Sc, Ec = np.array(d[cone][0], float)[ok], np.array(d[cone][1], float)[ok]
    nc, na = np.array(d[cone][2], float)[ok], cnt[ok]
    m = (k <= 1.5) & (Sc > 0) & (Ec > 0)
    z2 = ((Sc[m] - S[m]) ** 2 / (Ec[m] ** 2 + E[m] ** 2)).sum()
    # A cone's modes are a subset of the sphere's (REVIEW-p4.md, point 4): the variance of the difference is the
    # per-mode scatter times (1/n_cone - 1/n_all), not the sum of the two squared errors.
    nested = ((Sc[m] - S[m]) ** 2 / ((E[m] * FIX) ** 2 * (na[m] / nc[m] - 1))).sum()
    print(f'cone <{cone}> against the sphere average, k <= 1.5, nested variance: chi2 {nested:.1f} on {m.sum()} bins')
    print(f'cone <{cone}> against the sphere average, k <= 1.5: chi2 {z2:.1f} on {m.sum()} bins (file errors as written); {z2 / FIX ** 2:.1f} with corrected errors')
print(f'with corrected errors (file errors x {FIX:.2f}), weighted fits:')
for kmax in (1.0, 1.5, 2.0, 2.5, 3.0):
    m = k <= kmax
    Ef = E[m] * FIX
    p, cov = curve_fit(f, k[m], S[m], p0=(0.4, 2.8, 0.7), sigma=Ef, absolute_sigma=True, maxfev=20000)
    chi = float((((S[m] - f(k[m], *p)) / Ef) ** 2).sum())
    print(f'k <= {kmax:<4} xi = {abs(p[2]):.3f} +- {np.sqrt(cov[2, 2]):.3f}   S(0) = a + b = {p[0] + p[1]:.3f}   chi2 {chi:6.1f}/{m.sum() - 3}')
