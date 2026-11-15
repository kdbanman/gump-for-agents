"""Second, independent fit of ledger row P4 (Ornstein-Zernike correlation length of the chaotic phase).
Reads the two sk64.json files written by the pre-fix research/phase/sk.py (errors uncorrected) and
  (a) rebuilds the 64^3 lattice of modes and the bins/cones exactly as sk.py did (checks the mode counts),
  (b) derives the corrected error per bin from the lattice (independent modes = pairs + self-conjugate),
  (c) fits S = a + b/(1 + xi^2 k^2) by weighted least squares on windows k <= kmax,
  (d) tests the corrected errors empirically from the difference of the two sets (4 shared snapshots),
  (e) measures how much the variation of S across a bin inflates the scatter that sk.py used,
  (f) compares the cones <100>, <110>, <111> with the sphere average for k <= 1.5.
usage: python3 research/audit/p4_second_fit.py [SET1.json SET2.json]"""
import sys, json
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
from scipy.optimize import curve_fit
from scipy.stats import chi2 as chi2d

files = sys.argv[1:3] or ['research/scratch/phase/sk64.json', 'research/scratch/audit_c/phase/sk64.json']
D = [json.load(open(f)) for f in files]
n = D[0]['n']; cnt = D[0]['snaps']; bins = np.array(D[0]['kbins'])
assert all(d['n'] == n and d['snaps'] == cnt for d in D)
kc = 0.5 * (bins[1:] + bins[:-1])

# (a) lattice of modes, same conventions as sk.py
q = np.fft.fftfreq(n, 1.0 / n)
Q = np.stack(np.meshgrid(q, q, q, indexing='ij'))
qn = np.sqrt((Q ** 2).sum(0)); k = 2 * np.pi * qn / n
u = Q / np.maximum(qn, 1e-9); au = np.abs(u); srt = np.sort(au, axis=0)[::-1]
selfconj = np.all((Q == -n // 2) | (Q == 0), axis=0)          # -q == q mod n
masks = {'all': k > 0}
for name, d in [('100', [1, 0, 0]), ('110', [1, 1, 0]), ('111', [1, 1, 1])]:
    d = np.sort(np.array(d) / np.linalg.norm(d))[::-1]
    masks[name] = (k > 0) & ((srt * d[:, None, None, None]).sum(0) > np.cos(np.radians(20)))
lat = {}
for name, m in masks.items():
    idx = np.digitize(k[m], bins)
    c = np.bincount(idx, minlength=len(bins) + 1)[1:-1]
    ks = np.bincount(idx, weights=k[m], minlength=len(bins) + 1)[1:-1]
    sc = np.bincount(idx, weights=selfconj[m], minlength=len(bins) + 1)[1:-1]
    lat[name] = dict(c=c, kmean=ks / np.maximum(c, 1), nind=(c + sc) / 2, idx=idx, k=k[m])
    for d in D:
        assert np.array_equal(np.array(d[name][2]), c), name
print(f'(a) lattice mode counts reproduce the files for all four masks; n={n}, snapshots={cnt}')

# (b) corrected errors.  old e^2 = Var_modes(Sbar)/(c*cnt).  Error of the bin mean with c modes of
# which nind are independent: sqrt(Var_modes(Sbar)/nind) = e*sqrt(c*cnt/nind)
def get(d, name):
    m, e, c = (np.array(x, float) for x in d[name])
    var_modes = e ** 2 * c * cnt
    enew = np.sqrt(var_modes / np.maximum(lat[name]['nind'], 1))
    return m, e, c, var_modes, enew
fac = np.sqrt(lat['all']['c'] * cnt / np.maximum(lat['all']['nind'], 1))
print(f'(b) correction factor e_new/e_old per bin (sphere), k<=3: min {fac[kc<=3].min():.4f} max '
      f'{fac[kc<=3].max():.4f}; sqrt(2*cnt) = {np.sqrt(2*cnt):.4f}; self-conjugate modes with k<=3: '
      f'{int(selfconj[(k>0)&(k<=3)].sum())}')

oz = lambda kk, a, b, xi: a + b / (1 + xi ** 2 * kk ** 2)
def fit(m, e, kk, sel):
    p, C = curve_fit(oz, kk[sel], m[sel], p0=[0.5, 2.5, 0.7], sigma=e[sel], absolute_sigma=True, maxfev=20000)
    r = (m[sel] - oz(kk[sel], *p)) / e[sel]; dof = sel.sum() - 3
    return p, np.sqrt(np.diag(C)), (r ** 2).sum(), dof

# (c) fits
print('(c) OZ fits, corrected errors. xi +- err (unscaled covariance), chi2/dof, p; [xi with bin-mean k]')
P = {}
for s, d in enumerate(D):
    m, e, c, vm, en = get(d, 'all')
    for kmax in [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0]:
        sel = (kc <= kmax) & (c > 0)
        p, pe, x2, dof = fit(m, en, kc, sel)
        p2, pe2, x22, _ = fit(m, en, lat['all']['kmean'], sel)
        P[(s, kmax)] = p
        print(f'   set{s+1} k<={kmax:<4} xi={p[2]:.3f}+-{pe[2]:.3f}  a={p[0]:.3f} b={p[1]:.3f} S(0)={p[0]+p[1]:.3f}'
              f'  chi2={x2:6.1f}/{dof}  p={chi2d.sf(x2, dof):.2g}   [kmean: xi={p2[2]:.3f} chi2={x22:.1f}]')
    p, pe, x2, dof = fit(m, e, kc, (kc <= 3) & (c > 0))
    print(f'   set{s+1} k<=3 with the OLD errors: xi={p[2]:.3f}+-{pe[2]:.4f} chi2={x2:.0f}/{dof}')

# (d) empirical test: Sbar1 - Sbar2 = (sum of 8 own - sum of 8 own')/12, so with per-snapshot variance
# sigma_i^2 = cnt*e_i^2 (e_i the corrected error of the 12-mean): Var = (8/cnt^2)(sigma_1^2 + sigma_2^2)
nsh = 4; nown = cnt - nsh
print(f'(d) set1 - set2 against the corrected errors (assuming {nsh} shared snapshots):')
for name in ['all', '100', '110', '111']:
    g = [get(d, name) for d in D]
    for kmax in [3.0, kc[-1] + 1]:
        sel = (kc <= kmax) & (g[0][2] > 0)
        sd_new = np.sqrt(nown / cnt ** 2 * cnt * (g[0][4] ** 2 + g[1][4] ** 2))
        sd_old = np.sqrt(nown / cnt ** 2 * cnt * (g[0][1] ** 2 + g[1][1] ** 2))
        z = ((g[0][0] - g[1][0]) / sd_new)[sel]; zo = ((g[0][0] - g[1][0]) / sd_old)[sel]
        print(f'   {name:4} {"k<=3 " if kmax == 3 else "all k"} bins={sel.sum():2}  chi2/bins: corrected '
              f'{(z**2).mean():5.2f}  old {(zo**2).mean():6.1f}   rms z corrected {np.sqrt((z**2).mean()):.2f}')

# (e) inflation of the mode scatter by the variation of S(k) across a bin (anisotropy not included):
# Var_modes(Sbar) = noise + Var_bin(model).  Also the noise expected for a Gaussian field: S^2/cnt.
print('(e) within-bin model variance / scatter used by sk.py, and scatter*cnt/S^2 (1 = Gaussian):')
for s, d in enumerate(D):
    m, e, c, vm, en = get(d, 'all'); p = P[(s, 2.5)]; L = lat['all']
    mod = oz(L['k'], *p); i = L['idx']
    mv = (np.bincount(i, weights=mod ** 2, minlength=len(bins) + 1)[1:-1] / np.maximum(c, 1)
          - (np.bincount(i, weights=mod, minlength=len(bins) + 1)[1:-1] / np.maximum(c, 1)) ** 2)
    r = mv / np.maximum(vm, 1e-30); g = vm * cnt / np.maximum(m, 1e-9) ** 2
    sel = (kc <= 3) & (c > 0)
    print(f'   set{s+1} k<=3: model-variance fraction max {r[sel].max():.3f} (bin {kc[sel][r[sel].argmax()]:.2f}),'
          f' median {np.median(r[sel]):.4f};  scatter*cnt/S^2 median {np.median(g[sel]):.2f} '
          f'range {g[sel].min():.2f}-{g[sel].max():.2f}')
    first = np.where(sel)[0][:4]
    print('      first bins: c=' + ' '.join(f'{int(c[j])}' for j in first) + '  frac=' +
          ' '.join(f'{r[j]:.3f}' for j in first) + '  scatter*cnt/S^2=' + ' '.join(f'{g[j]:.2f}' for j in first))

# (f) cones vs sphere, k <= 1.5.  Cone modes are a subset of the sphere's, so the difference has
# variance sigma^2 (1/nind_cone - 1/nind_all), sigma^2 = the sphere's mode scatter (nested);
# e_cone^2 + e_all^2 (as if independent, which understates chi2) is also shown.
print('(f) cone - sphere for k<=1.5, corrected errors: chi2 nested / chi2 independent / bins')
for s, d in enumerate(D):
    ma, _, ca, vma, ea = get(d, 'all')
    out = []
    for name in ['100', '110', '111']:
        mc, _, cc, _, ec = get(d, name); sel = (kc <= 1.5) & (cc > 0)
        dd = (mc - ma)[sel]
        vn = vma * (1 / np.maximum(lat[name]['nind'], 1) - 1 / np.maximum(lat['all']['nind'], 1))
        x_n = (dd ** 2 / vn[sel]).sum()
        x_i = (dd ** 2 / (ec ** 2 + ea ** 2)[sel]).sum()
        out.append(f'{name}: {x_n:5.1f} / {x_i:5.1f} / {sel.sum()} (p={chi2d.sf(x_n, sel.sum()):.2g})')
    print(f'   set{s+1}  ' + '   '.join(out))
