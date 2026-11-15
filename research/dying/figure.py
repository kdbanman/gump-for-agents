#!/usr/bin/env python3
"""figure.py: research/figures/dying_face.png from research/scratch/dying/canon_G.npz (load.py).

    python3 research/dying/figure.py
"""
import os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from load import SCR, GROUPS, TIED, regions, ROOT
OUT = os.path.join(ROOT, 'research', 'figures', 'dying_face.png')
SER = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']
INK, MUTED, GRID = '#1f1f1d', '#6b6a63', '#e1e0d9'
SEQ = LinearSegmentedColormap.from_list('blue', ['#f3f7fd', '#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#0d366b'])
LABEL = {'c1': 'c1 (no tied edge)', 'csz': 'csz (z tied)', 'c2v': 'c2v (x, y tied)', 'd2h': 'D2h (all tied)'}


def proj(c):
    x, y, z = c[:, 0], c[:, 1], c[:, 2]
    return (x - y) / np.sqrt(2), (2 * z - x - y) / np.sqrt(6)


def main():
    Z = {g: np.load(os.path.join(SCR, f'canon_{g}.npz')) for g in GROUPS}
    canon = Z['c1']['canon']; band, interior, apex = regions(canon)
    u, v = proj(canon)
    corners = np.array([[11, 0, 0], [0, 11, 0], [0, 0, 11]]); cu, cv = proj(corners)
    edge_ends = {0: (1, 2), 1: (0, 2), 2: (0, 1)}       # edge a (coordinate a = 0) joins the other two apexes
    lags = ['null', 16, 8, 4, 2, 1]
    fig = plt.figure(figsize=(13.5, 13.2), dpi=100)
    gs = fig.add_gridspec(5, 6, height_ratios=[1, 1, 1, 1, 1.45], hspace=0.28, wspace=0.05, left=0.07, right=0.93, top=0.94, bottom=0.05)
    norm = LogNorm(0.005, 0.6)
    for i, g in enumerate(GROUPS):
        X, W, NUL = Z[g]['X'], Z[g]['W'], Z[g]['NUL']
        for j, l in enumerate(lags):
            ax = fig.add_subplot(gs[i, j])
            occ = NUL.mean(0) if l == 'null' else (X[:, l] * W[:, None]).sum(0) / W.sum()
            for a in range(3):
                p, q = edge_ends[a]
                tied = a in TIED[g]
                # bar drawn just outside the edge, away from the face centre (the origin of the projection)
                mu, mv = (cu[p] + cu[q]) / 2, (cv[p] + cv[q]) / 2; nrm = np.hypot(mu, mv); du, dv = 0.75 * mu / nrm, 0.75 * mv / nrm
                ax.plot([cu[p] + du, cu[q] + du], [cv[p] + dv, cv[q] + dv], color='#eb6834' if tied else GRID, lw=4 if tied else 1.0, zorder=0, solid_capstyle='round')
            ax.scatter(u, v, c=np.clip(occ, 0.005, None), cmap=SEQ, norm=norm, s=62, edgecolors='white', linewidths=0.6, zorder=2)
            ax.set_aspect('equal'); ax.axis('off')
            ax.set_xlim(-9.2, 9.2); ax.set_ylim(-7.4, 10.0)
            if i == 0:
                ax.set_title('stationary (null)' if l == 'null' else f'lag {l}', fontsize=11, color=INK)
            if j == 0:
                ax.text(-9.4, 2.0, LABEL[g], rotation=90, ha='center', va='center', fontsize=11, color=INK)
            ax.text(0, -7.2, f'{(occ.sum()):.1f} live cells', ha='center', fontsize=8.5, color=MUTED)
    cax = fig.add_axes([0.945, 0.40, 0.012, 0.50])
    sm = plt.cm.ScalarMappable(norm=norm, cmap=SEQ); cb = fig.colorbar(sm, cax=cax)
    cb.set_label('mean occupancy of the cell (log scale)', color=INK); cb.outline.set_visible(False)
    fig.text(0.07, 0.965, 'How a face of the R = 11 cube-centred hull dies (A = 63): mean face at lags before its death; '
             'orange bar = edge shared with a face in lockstep', fontsize=12, color=INK)

    # bottom row: three line panels
    lagax = np.arange(0, 41)
    sub = gs[4, :].subgridspec(1, 3, wspace=0.22)
    axB = fig.add_subplot(sub[0]); axC = fig.add_subplot(sub[1]); axD = fig.add_subplot(sub[2])
    for k, g in enumerate(GROUPS):
        X, NUL = Z[g]['X'], Z[g]['NUL']
        axB.plot(lagax, X[:, :41].sum(2).mean(0) / NUL.sum(1).mean(), color=SER[k], lw=2, label=LABEL[g])
    N = Z['c1']['NBR']; nb_ = [Z['c1']['NUL'][:, b].mean() for b in band]
    axB.plot(lagax, np.mean([N[:, a, :41][:, :, band[a]].mean(2).mean(0) / nb_[a] for a in range(3)], 0), color=SER[0], lw=2, ls=(0, (2, 2)),
             label='c1 neighbour: its band on the shared edge')
    axB.plot(lagax, N[:, :, :41].sum(3).mean((0, 1)) / Z['c1']['NUL'].sum(1).mean(), color=SER[0], lw=1.2, ls=(0, (6, 2)), label='c1 neighbour: whole face')
    axB.set_title('A. face population / stationary mean', fontsize=11, color=INK, loc='left')
    axB.set_xlabel('lag (generations before death)'); axB.invert_xaxis(); axB.legend(fontsize=8, frameon=False, loc='lower left')
    # C: csz bands relative to their own stationary occupancy
    X, NUL = Z['csz']['X'], Z['csz']['NUL']
    def rel(sel):
        return X[:, :41][:, :, sel].mean(2).mean(0) / NUL[:, sel].mean()
    axC.plot(lagax, (rel(band[0]) + rel(band[1])) / 2, color=SER[1], lw=2, label='csz free edges x, y (rows 1-2)')
    axC.plot(lagax, rel(band[2]), color=SER[1], lw=2, ls=(0, (2, 2)), label='csz tied edge z (rows 1-2)')
    axC.plot(lagax, rel(interior), color=MUTED, lw=1.5, label='csz interior')
    Xd, Nd = Z['d2h']['X'], Z['d2h']['NUL']
    axC.plot(lagax, np.mean([Xd[:, :41][:, :, b].mean(2).mean(0) / Nd[:, b].mean() for b in band], 0), color=SER[3], lw=2, ls=(0, (2, 2)), label='D2h tied edges (rows 1-2)')
    axC.plot(lagax, Xd[:, :41][:, :, interior].mean(2).mean(0) / Nd[:, interior].mean(), color=SER[3], lw=1.2, label='D2h interior')
    axC.set_title('B. occupancy / its own stationary value', fontsize=11, color=INK, loc='left')
    axC.set_xlabel('lag (generations before death)'); axC.invert_xaxis(); axC.legend(fontsize=8, frameon=False, loc='lower left')
    # D: stationary occupancy by row from a free and a tied edge
    rows = np.arange(1, 6)
    for k, g in enumerate(GROUPS):
        NUL = Z[g]['NUL']
        prof = [[NUL[:, (canon[:, a] == r - 1) & ~apex].mean() for r in rows] for a in range(3)]
        free = [a for a in range(3) if a not in TIED[g]]; tied = list(TIED[g])
        if free:
            axD.plot(rows, np.mean([prof[a] for a in free], 0), color=SER[k], lw=2, marker='o', ms=6, label=f'{g} free edge')
        if tied:
            axD.plot(rows, np.mean([prof[a] for a in tied], 0), color=SER[k], lw=2, ls=(0, (2, 2)), marker='s', ms=6, label=f'{g} tied edge')
    axD.set_xticks(rows); axD.set_xlabel('row from the edge (1 = shared rim row)')
    axD.set_title('C. stationary occupancy by row', fontsize=11, color=INK, loc='left')
    axD.legend(fontsize=8, frameon=False, ncol=2, loc='lower right')
    for ax in (axB, axC, axD):
        ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
        for s in ('top', 'right'):
            ax.spines[s].set_visible(False)
        for s in ('left', 'bottom'):
            ax.spines[s].set_color('#c3c2b7')
        ax.tick_params(colors=MUTED, labelsize=9)
    axB.set_ylim(0, 1.05); axC.set_ylim(0, 1.15); axD.set_ylim(0.25, 0.58)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, facecolor='white'); print(OUT)


if __name__ == '__main__':
    main()
