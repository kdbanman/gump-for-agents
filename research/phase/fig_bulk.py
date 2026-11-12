"""Figures for part A (bulk chaotic phase). Reads research/scratch/phase/* produced by the
commands in research/phase/README.md; writes research/figures/phase_bulk.png, phase_spread.png."""
import os, json, glob, csv
import numpy as np
from math import comb
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import betabinom, binom

H = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(H, '../scratch/phase'); F = os.path.join(H, '../figures')
C1, C2, C3, C4 = '#2a78d6', '#eb6834', '#1baf7a', '#6250d6'
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.spines.top': False, 'axes.spines.right': False, 'lines.linewidth': 1.6})
k = np.arange(13)
def fmap(p, icc=0.0):
    P = binom.pmf(k, 12, p) if icc == 0 else betabinom.pmf(k, 12, p * (1 - icc) / icc, (1 - p) * (1 - icc) / icc)
    return (1 - p) * P[4:6].sum() + p * P[3:6].sum()

fig, ax = plt.subplots(2, 2, figsize=(9, 7.2))
# (a) return map
a = ax[0, 0]
ps = np.linspace(0, 1, 401)
a.plot(ps, ps, color=INK2, lw=0.8, ls=':')
a.plot(ps, [fmap(p) for p in ps], color=C2, label='mean field (binomial)')
a.plot(ps, [fmap(p, 0.035) for p in ps], color=C4, ls='--', label='overdispersed, ICC 0.035')
N = 3 * 64 ** 3
for f in sorted(glob.glob(os.path.join(S, 'ts64/ts_p*_r0.csv'))):
    r = np.array([int(x['pop']) for x in csv.DictReader(open(f))][:60]) / N
    a.plot(r[:-1], r[1:], '-', color=C1, lw=0.5, alpha=0.5)
    a.plot(r[:1], r[1:2], 'o', color=C1, ms=3)
a.plot([0.41552], [0.41552], 'o', color=INK, ms=6, zorder=5)
a.annotate('lattice steady state 0.4155', (0.4155, 0.4155), (0.55, 0.30), fontsize=8, color=INK,
           arrowprops=dict(arrowstyle='-', color=INK2, lw=0.6))
a.set_xlabel(r'density $\rho_t$'); a.set_ylabel(r'$\rho_{t+1}$'); a.set_xlim(0, 1); a.set_ylim(0, 0.55)
a.legend(fontsize=7.5, loc='upper right', frameon=False)
a.set_title('(a) density return map; dots = first step of 25 soups (64³ torus)', fontsize=9, loc='left')
# (b) autocorrelations
a = ax[0, 1]
d = np.genfromtxt(os.path.join(S, 'long64.csv'), delimiter=',', names=True)
x = d['pop'][1000:] / N; x = x - x.mean()
lags = np.arange(0, 16)
glob_acf = [1] + [np.mean(x[:-l] * x[l:]) / x.var() for l in lags[1:]]
B = json.load(open(os.path.join(S, 'bulk64.json')))
cell = np.mean([b['acf'] for b in B], 0)[:16]
a.axhline(0, color=INK2, lw=0.6)
a.plot(lags, glob_acf, 'o-', color=C2, ms=4, label='global density (k = 0 mode)')
a.plot(lags, cell, 's-', color=C1, ms=4, label='single cell')
a.set_xlabel('lag (generations)'); a.set_ylabel('autocorrelation')
a.legend(frameon=False, fontsize=7.5)
a.set_title('(b) temporal autocorrelation: global density rings with period ≈ 3', fontsize=9, loc='left')
# (c) structure factor
a = ax[1, 0]
sk = json.load(open(os.path.join(S, 'sk64.json')))
kb = np.array(sk['kbins']); kc = 0.5 * (kb[1:] + kb[:-1])
for name, c, mk in [('100', C1, 'o'), ('110', C2, 's'), ('111', C3, '^')]:
    m, e, cn = sk[name]; m = np.array(m); e = np.array(e); ok = np.array(cn) > 0
    a.errorbar(kc[ok], m[ok], e[ok], fmt=mk, color=c, ms=3.5, lw=0.8, label=f'k ∥ <{name}>')
a.axhline(1, color=INK2, lw=0.6, ls=':')
a.set_xlabel('|k| (radians per cube)'); a.set_ylabel('S(k)  (1 = uncorrelated)')
a.legend(frameon=False, fontsize=7.5); a.set_xlim(0, 3.2)
a.set_title('(c) structure factor, 12 snapshots of 64³: isotropic', fontsize=9, loc='left')
# (d) neighbour counts
a = ax[1, 1]
hl = np.sum([b['hist_live'] for b in B], 0); hd = np.sum([b['hist_dead'] for b in B], 0)
w = 0.38
a.bar(k - w / 2, hl / hl.sum(), w, color=C1, label='live cells')
a.bar(k + w / 2, hd / hd.sum(), w, color=C2, label='dead cells')
a.plot(k, binom.pmf(k, 12, 0.4155), 'o-', color=INK, ms=3, lw=0.8, label='binomial(12, 0.4155)')
a.axvspan(3.5, 5.5, color=GRID, alpha=0.5, lw=0, zorder=0); a.axvspan(2.5, 3.5, color=GRID, alpha=0.25, lw=0, zorder=0)
a.set_xlabel('live neighbours n'); a.set_ylabel('fraction'); a.set_xticks(k)
a.legend(frameon=False, fontsize=7.5)
a.set_title('(d) neighbour counts (shaded: S, B windows)', fontsize=9, loc='left')
fig.tight_layout(); fig.savefig(os.path.join(F, 'phase_bulk.png'), dpi=110)

# ---------------- spreading figure
fig, ax = plt.subplots(1, 3, figsize=(11, 3.6))
dm = np.load(os.path.join(S, 'damage64.npz')); sup = dm['sup']; U = dm['U']
a = ax[0]
t = np.arange(sup.shape[1])
for nm, m, c in [('axes <100>', np.abs(U).sum(1) == 1, C1), ('face diag <110>', np.abs(U).sum(1) == 2, C2),
                 ('body diag <111>', np.abs(U).sum(1) == 3, C3)]:
    h = np.nanmean(sup[:, :, m], axis=2) / 2  # cubes
    a.plot(t, np.nanmean(h, 0), color=c, label=nm)
a.plot(t, t, color=INK2, ls=':', lw=0.8); a.text(13, 15.5, 'speed limit along axis (1 cube/gen)', fontsize=7, color=INK2, rotation=33)
a.plot(t, np.sqrt(3) * t, color=INK2, ls='--', lw=0.6); a.text(4, 12.5, 'limit along <111>', fontsize=7, color=INK2, rotation=50)
a.set_ylim(0, 30); a.set_xlabel('generation'); a.set_ylabel('damage extent along u (cubes, Euclidean)')
a.legend(frameon=False, fontsize=7.5, loc='lower right')
a.set_title('(a) damage from one flipped cell (40/40 spread)', fontsize=9, loc='left')
a = ax[1]
mp = dm['dmap30'].sum(axis=2) if 'dmap30' in dm else None
n = mp.shape[0]
im = a.imshow(mp.T / dm['ham'].shape[0], origin='lower', cmap='Blues', extent=[-n / 2, n / 2, -n / 2, n / 2])
a.set_xlabel('x (cubes)'); a.set_ylabel('y (cubes)'); a.grid(False)
a.set_title('(b) damage at t = 30, projected on z', fontsize=9, loc='left')
fp = np.load(os.path.join(S, 'fplanar72.npz'))
a = ax[2]
for nm, nrm, c in [('100', 1, C1), ('110', np.sqrt(2), C2), ('111', np.sqrt(3), C3)]:
    A = fp[nm] / nrm / 2
    a.plot(np.arange(A.shape[1]), A.mean(0), color=c, label=f'{{{nm}}} front')
a.plot(np.arange(110), np.arange(110), color=INK2, ls=':', lw=0.8)
a.set_ylim(0, 25); a.set_xlabel('generation'); a.set_ylabel('front advance into vacuum (cubes)')
a.legend(frameon=False, fontsize=7.5)
a.set_title('(c) planar chaos/vacuum fronts (72³ torus)', fontsize=9, loc='left')
fig.tight_layout(); fig.savefig(os.path.join(F, 'phase_spread.png'), dpi=110)
print('ok')
