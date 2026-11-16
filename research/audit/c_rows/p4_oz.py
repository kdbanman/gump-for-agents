#!/usr/bin/env python3
"""P4 (CLAIMS.md): Ornstein-Zernike fit S(k) = B + C / (1 + xi^2 k^2) to research/phase/sk.py's spherical average,
and the cone-vs-sphere agreement (isotropy), from sk.py's JSON.
    G=engine/target/release/gump; S=research/scratch/audit_c/phase
    for R in $(seq 1 12); do $G run --soup 0.3 --torus 64 --rng $R --gens 5000 --no-halt --snapshot-out $S/ss64_$R.gump; done
    python3 research/phase/sk.py $S/sk64.json $S/ss64_*.gump
    python3 research/audit/c_rows/p4_oz.py $S/sk64.json
k is per cube (2 pi q / n); all bins with k > 0 and data are fitted, weighted by sk.py's errors."""
import json, sys
import numpy as np
from scipy.optimize import curve_fit
r = json.load(open(sys.argv[1]))
b = np.array(r['kbins']); kc = 0.5 * (b[1:] + b[:-1])
m, e, c = (np.array(x) for x in r['all'])
ok = (c > 0) & (e > 0)
f = lambda k, B, C, xi: B + C / (1 + xi ** 2 * k ** 2)
p, cov = curve_fit(f, kc[ok], m[ok], sigma=e[ok], p0=(0.4, 2.8, 0.7), absolute_sigma=True)
chi2 = float((((m[ok] - f(kc[ok], *p)) / e[ok]) ** 2).sum()); dof = int(ok.sum()) - 3
s = np.sqrt(np.diag(cov)) * max(1.0, np.sqrt(chi2 / dof))
print(f'OZ fit, {ok.sum()} bins: B = {p[0]:.3f} +- {s[0]:.3f}, C = {p[1]:.3f} +- {s[1]:.3f}, xi = {p[2]:.3f} +- {s[2]:.3f} cube; '
      f'S(0) = B + C = {p[0] + p[1]:.2f}; chi2 {chi2:.1f}/{dof} (errors scaled by sqrt(chi2/dof) if > 1)')
for name in ('100', '110', '111'):
    mm, ee, cc = (np.array(x) for x in r[name]); g = ok & (cc > 0) & (ee > 0)
    z = (mm[g] - m[g]) / np.sqrt(ee[g] ** 2 + e[g] ** 2)
    print(f'cone <{name}> vs sphere: {g.sum()} bins, chi2 {float((z ** 2).sum()):.1f}, max |z| {np.abs(z).max():.1f}')
