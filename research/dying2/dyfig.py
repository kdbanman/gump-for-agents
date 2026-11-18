#!/usr/bin/env python3
"""research/dying2 figure from the data/*.csv tables:  P -u research/dying2/dyfig.py  -> research/dying2/dying2.png
A: mean P/Pbar against lag before death (c1 hull face of 63 cells, round 1, as grey points).
B: q(k), the share of dips reaching k live cells that end in death.  C: ln nu(<=k) against k/Pbar.
D: the empty band across the axis (cube edges) against lag, deaths (solid) and random thinning to the same count (dashed)."""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'data')
FACES = [('1_4_21', 'W63 wide', '#2a78d6'), ('2_4_14', 'E84 wide', '#eb6834'), ('1_12_28', 'T84 tube', '#1baf7a'),
         ('1_17_32', 'T96 tube', '#eda100')]


def load(tag, what):
    p = os.path.join(D, f'{tag}_{what}.csv')
    return np.genfromtxt(p, delimiter=',', names=True) if os.path.exists(p) else None


fig, ax = plt.subplots(2, 2, figsize=(11, 8))
for tag, name, col in FACES:
    L = load(tag, 'lags'); E = load(tag, 'excursions'); B = load(tag, 'band')
    if L is not None:
        s = L['lag'] <= 32
        ax[0, 0].plot(L['lag'][s], L['mean_P_over_Pbar'][s], '-o', color=col, lw=2, ms=4, label=name)
    if E is not None:
        k = E['k']; s = (k >= 1) & (k <= 14)
        ax[0, 1].semilogy(k[s], E['q'][s], '-o', color=col, lw=2, ms=4, label=name)
        pb = k[1] / E['k_over_Pbar'][1]; s2 = (k <= 0.95 * pb) & (E['nu_per_face_gen'] > 0)
        ax[1, 0].plot(k[s2] / pb, np.log(E['nu_per_face_gen'][s2]), '-', color=col, lw=2, label=name)
    if B is not None:
        ax[1, 1].plot(B['lag'], B['band_width_cube_edges'], '-o', color=col, lw=2, ms=4, label=name)
        ax[1, 1].plot(B['lag'], B['band_width_null'], '--', color=col, lw=1.2)
ax[0, 0].plot([16, 8, 4], [0.95, 0.67, 0.31], 's', color='#8a8984', ms=7, label='c1 hull 63 (round 1)')
ax[0, 0].set(xlabel='generations before the face is empty', ylabel='mean P / P̄', title='A. the final dip')
ax[0, 1].axhline(0.5, color='#b5b4ae', lw=1)
ax[0, 1].set(xlabel='k (live cells)', ylabel='q(k)', title='B. share of dips reaching k that die')
ax[1, 0].set(xlabel='k / P̄', ylabel='ln ν(≤k) per face-generation', title='C. dip rate')
ax[1, 1].set(xlabel='generations before death', ylabel='empty band across the axis (cube edges)',
             title='D. the band: deaths (solid), random thinning (dashed)')
for a in ax.flat:
    a.grid(color='#e6e5e0', lw=0.6); a.legend(fontsize=8, frameon=False)
    for sp in ('top', 'right'):
        a.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, 'dying2.png'), dpi=110)
print(os.path.join(HERE, 'dying2.png'))
