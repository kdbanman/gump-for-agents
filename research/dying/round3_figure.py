"""round3_figure.py: research/figures/dying_ratefunction.png (called by round3.py)."""
import os
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from load import ROOT
SER = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4']
INK, MUTED, GRID = '#1f1f1d', '#6b6a63', '#e1e0d9'
SEQ = LinearSegmentedColormap.from_list('blue', ['#f3f7fd', '#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b'])
OUT = os.path.join(ROOT, 'research', 'figures', 'dying_ratefunction.png')


def style(ax, title):
    ax.set_title(title, fontsize=11, color=INK, loc='left')
    ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    for s in ('left', 'bottom'):
        ax.spines[s].set_color('#c3c2b7')
    ax.tick_params(colors=MUTED, labelsize=9)


def make(EX, rad, rad0, edges, Hm, H0m, Hr, bins):
    fig, axs = plt.subplots(2, 2, figsize=(12, 10), dpi=100)
    ax = axs[0, 0]; k = 0
    for spec, e in EX.items():
        p = np.array([x['p'] for x in e['rows']]); y = np.array([-x['lnnu'] / e['A'] for x in e['rows']])
        ok = np.array([x['n'] >= 20 for x in e['rows']])
        slab = spec.startswith('hex')
        ax.plot(p[ok], y[ok], color=MUTED if slab else SER[k], lw=1.5 if slab else 2, ls=(0, (2, 2)) if slab else '-', marker='o', ms=3.5,
                label=('slab torus, A = 63 (no rim)' if slab else f'hull face, A = {e["A"]}'))
        if e['fdeaths'] > 0:
            ax.plot([0], [np.log(e['E'] / e['fdeaths']) / e['A']], marker='*', ms=11, color=MUTED if slab else SER[k], ls='none')
        if not slab:
            k += 1
    ax.set_xlabel('level p (fraction of the stationary mean)'); ax.set_ylabel('−ln ν(p) / A'); ax.invert_xaxis()
    ax.legend(fontsize=8.5, frameon=False, loc='upper left'); ax.set_xlim(1.0, -0.03)
    style(ax, 'A. rate of dips that reach p, per cell of face (c1)\n(star at p = 0: ln τ_face / A)')
    ax = axs[0, 1]; k = 0
    for spec, e in EX.items():
        r = {x['p']: x for x in e['rows']}
        p = np.array([x['p'] for x in e['rows'] if x['n'] >= 20]); y = np.array([(r[0.9]['lnnu'] - r[pp]['lnnu']) / e['A'] for pp in p])
        slab = spec.startswith('hex')
        ax.plot(p, y, color=MUTED if slab else SER[k], lw=1.5 if slab else 2, ls=(0, (2, 2)) if slab else '-', marker='o', ms=3.5,
                label=('slab torus, A = 63' if slab else f'hull face, A = {e["A"]}'))
        if not slab:
            k += 1
    ax.set_xlabel('level p'); ax.set_ylabel('[ln ν(0.9) − ln ν(p)] / A'); ax.invert_xaxis(); ax.set_xlim(1.0, -0.03)
    ax.legend(fontsize=8.5, frameon=False, loc='upper left')
    style(ax, 'B. the same with the size-independent rate of\nshallow dips removed (added after the forecasts)')
    ext = [bins[0], bins[-1], bins[0], bins[-1]]
    ax = axs[1, 0]
    im = ax.imshow(np.where(Hr > 50, Hm, np.nan), origin='lower', extent=ext, cmap=SEQ, vmin=0, vmax=1.2)
    ax.plot(0, 0, marker='+', color='#eb6834', ms=12, mew=2)
    ax.set_xlabel('doubled units'); ax.set_ylabel('doubled units (face centre lies below the +)')
    cb = fig.colorbar(im, ax=ax, fraction=0.046); cb.set_label('occupancy / stationary', color=INK); cb.outline.set_visible(False)
    style(ax, 'C. c1 faces caught at P ≤ 0.3 P̄ (mean 8.3 cells),\naligned on the survivors\' centroid (+)')
    ax = axs[1, 1]
    c = (edges[:-1] + edges[1:]) / 2
    ax.plot(c, rad, color=SER[0], lw=2, marker='o', ms=4, label='caught faces (P ≤ 0.3 P̄)')
    ax.plot(c, rad0, color=SER[0], lw=1.2, ls=(0, (2, 2)), marker='o', ms=3, label='stationary face thinned to the same count')
    ax.set_xlabel('distance from the survivors\' centroid (doubled units)'); ax.set_ylabel('occupancy / stationary')
    ax.legend(fontsize=8.5, frameon=False); style(ax, 'D. radial profile around the clump')
    fig.tight_layout(); fig.savefig(OUT, facecolor='white'); print(OUT)
