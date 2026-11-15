import glob, os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w
from w import tslab
d = sys.argv[1]; lam = float(sys.argv[2])     # reference F/E for rule A
fs = sorted(glob.glob(os.path.join(d, 'ch_4_0_4_s*.npz')))
z = []
for f in fs:
    o = np.load(f); st = o['settle']; ge = int(o['gen_end'])
    stop = np.where(st >= 0, st, ge).astype(float); fwm = o['fw'].min(1); face = o['face']
    end = np.minimum.reduce([face, fwm, stop]); kF = (face == end) & (face < fwm) & (face <= stop)
    z.append((end.sum(), kF.sum()))
E = np.array([x[0] for x in z]); F = np.array([x[1] for x in z])
r = (F - lam * E) / np.sqrt(lam * E)
print(len(fs), 'jobs; standardised residuals of F_j against the reference rate', lam)
print(' '.join(f'{x:+.1f}' for x in r))
print(f'sum F - lam E = {F.sum() - lam * E.sum():.0f} ({(F.sum() - lam * E.sum()) / math.sqrt(lam * E.sum()):+.2f} sigma); chi2 {np.sum(r ** 2):.1f} on {len(r)}; '
      f'mean r {r.mean():+.3f}; jobs with r < 0: {(r < 0).sum()}; lag-1 autocorrelation {np.corrcoef(r[:-1], r[1:])[0, 1]:+.3f}')
for k in range(0, len(r), 19):
    print(f'  jobs {k}-{k + 18}: ln(2E/F) = {math.log(2 * E[k:k + 19].sum() / F[k:k + 19].sum()):.4f} +- {1 / math.sqrt(F[k:k + 19].sum()):.4f}')
