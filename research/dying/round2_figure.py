"""round2_figure.py: research/figures/dying_excursions.png (called by round2.py)."""
import os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from load import GROUPS, ROOT
SER = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']
INK, MUTED, GRID = '#1f1f1d', '#6b6a63', '#e1e0d9'
LAB = {'c1': 'c1 (0 tied)', 'csz': 'csz (1)', 'c2v': 'c2v (2)', 'd2h': 'D2h (3)'}
OUT = os.path.join(ROOT, 'research', 'figures', 'dying_excursions.png')


def style(ax, title):
    ax.set_title(title, fontsize=11, color=INK, loc='left')
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#c3c2b7')
    ax.tick_params(colors=MUTED, labelsize=9)


def make(EX, B, C, D):
    from round2 import PBAR, SIG
    fig, axs = plt.subplots(2, 2, figsize=(12, 9.4), dpi=100)
    ax = axs[0, 0]
    for k, g in enumerate(GROUPS):
        r = EX[g]['rows']; p = np.array([x['p'] for x in r]); y = np.array([x['lnnu'] for x in r])
        ax.plot(p, y, color=SER[k], lw=2, marker='o', ms=4, label=LAB[g])
        ax.axhline(np.log(EX[g]['rate']), color=SER[k], lw=1, ls=(0, (1, 2)))
    r = {x['p']: x for x in EX['c1']['rows']}; pb, sg = PBAR['c1'], SIG['c1']
    G = lambda p: -((pb - p * pb) ** 2) / (2 * sg ** 2)
    pp = np.linspace(0.05, 0.95, 50); ax.plot(pp, r[0.9]['lnnu'] - G(0.9) + G(pp), color=SER[0], lw=1.2, ls=(0, (5, 3)), label='c1 Gaussian, fixed at p = 0.9')
    ax.set_xlabel('level p (fraction of the stationary mean)'); ax.set_ylabel('ln ν  (per face per generation)')
    ax.set_ylim(-25, 0); ax.invert_xaxis(); ax.legend(fontsize=8.5, frameon=False, loc='lower left')
    style(ax, 'A. rate of excursions from above the mean that reach p\n(dotted: death rate)')
    ax = axs[0, 1]
    for k, g in enumerate(GROUPS):
        r = EX[g]['rows']; p = np.array([x['p'] for x in r]); q = np.array([x['q'] for x in r])
        ax.plot(p, q, color=SER[k], lw=2, marker='o', ms=4, label=LAB[g])
    ax.set_yscale('log'); ax.axhline(0.5, color=MUTED, lw=0.8)
    ax.set_xlabel('level p'); ax.set_ylabel('q: fraction ending in death'); ax.invert_xaxis(); ax.legend(fontsize=8.5, frameon=False, loc='upper left')
    style(ax, 'B. of the excursions that reach p, the fraction that die')
    ax = axs[1, 0]
    bins = np.linspace(0, 6, 31)
    for k, g in ((0, 'c1'), (3, 'd2h')):
        ax.hist(B[g]['Sd_all'], bins=bins, histtype='step', density=True, color=SER[k], lw=2, label=f'{LAB[g]}: deaths at t_h')
        ax.hist(B[g]['Sn_all'], bins=bins, histtype='step', density=True, color=SER[k], lw=1.2, ls=(0, (2, 2)), label=f'{LAB[g]}: stationary face thinned to the same count')
    ax.set_xlabel('S: live-cell centroid offset (doubled units)'); ax.set_ylabel('density'); ax.legend(fontsize=8.5, frameon=False)
    style(ax, 'C. survivors at the start of the plunge: offset of their centroid')
    ax = axs[1, 1]
    for k, g in enumerate(GROUPS):
        cu = np.array(C[g]['curve'])
        ax.plot(cu[:, 0], cu[:, 1], color=SER[k], lw=2, label=f'{LAB[g]} births per empty cell')
        ax.plot(cu[:, 0], cu[:, 2], color=SER[k], lw=1.2, ls=(0, (2, 2)), label=f'{LAB[g]} survival per live cell')
    ax.axhline(1, color=MUTED, lw=0.8)
    ax.set_xlabel('lag (generations before death)'); ax.set_ylabel('over stationary'); ax.invert_xaxis(); ax.legend(fontsize=7.5, frameon=False, ncol=2, loc='lower left')
    style(ax, 'D. on the dying face, step lag → lag − 1')
    fig.tight_layout(); fig.savefig(OUT, facecolor='white'); print(OUT)
