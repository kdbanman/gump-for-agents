#!/usr/bin/env python3
"""research/dying2/hull/hull_dying.png from data/R{11,13}_*.csv (analyze.py's tables).

  python research/dying2/hull/figure.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, 'data')
Rs = [R for R in (11, 13) if os.path.exists(os.path.join(D, f'R{R}_death_timecourse.csv'))]
col = {11: '#1f77b4', 13: '#d62728'}
A = {11: 63, 13: 84}


def load(name):
    return np.genfromtxt(os.path.join(D, name), delimiter=',', names=True, dtype=None, encoding=None)


fig, ax = plt.subplots(2, 3, figsize=(15, 9))
a = ax[0, 0]
for R in Rs:
    t = load(f'R{R}_death_timecourse.csv'); m = t['lag'] <= 40
    pb = t['mean'][m][-1] / t['mean_over_Pbar'][m][-1]
    a.plot(t['lag'][m], t['mean'][m] / pb, '-o', ms=3, c=col[R], label=f'A = {A[R]}: mean')
    a.fill_between(t['lag'][m], t['q25'][m] / pb, t['q75'][m] / pb, color=col[R], alpha=0.2, label='quartiles')
    a.plot(t['lag'][m], t['q05'][m] / pb, ':', c=col[R]); a.plot(t['lag'][m], t['q95'][m] / pb, ':', c=col[R])
    a.plot(t['lag'][m], t['edge_nb_over_Pbar'][m], '--', c=col[R], lw=1, label='edge neighbours (mean)')
a.set_xlabel('generations before the face is empty'); a.set_ylabel('P / P bar'); a.set_title('A. the dying face (dotted: 5%, 95%)')
a.invert_xaxis(); a.legend(fontsize=8)
a = ax[0, 1]
for R in Rs:
    t = load(f'R{R}_excursions.csv'); m = (t['k'] >= 1) & (t['k'] <= 16)
    a.semilogy(t['k'][m], t['q'][m], '-o', ms=3, c=col[R], label=f'A = {A[R]}')
a.axhline(0.5, c='k', lw=0.5)
a.set_xlabel('k (live cells)'); a.set_ylabel('q(k) = P(death | dip reaches <= k)'); a.set_title('B. point of no return'); a.legend()
a = ax[0, 2]
for R in Rs:
    t = load(f'R{R}_excursions.csv'); m = (t['k'] >= 0) & (t['k'] < t['k_over_Pbar'].size)
    m = t['k_over_Pbar'] <= 1.0
    a.plot(t['k_over_Pbar'][m], np.log(t['nu_per_face_gen'][m]), '-', c=col[R], label=f'A = {A[R]}')
a.set_xlabel('k / P bar'); a.set_ylabel('ln nu (dips reaching <= k, per face-generation)'); a.set_title('C. dip rate'); a.legend()
a = ax[1, 0]
offs = [-128, -64, -32, -16, -8, -4, -2, 0, 2, 4, 8, 16, 32]
for R in Rs:
    t = np.genfromtxt(os.path.join(D, f'R{R}_equal_depth.csv'), delimiter=',', skip_header=1)
    for k, ls in ((3, '-'), (6, '--')):
        for dies in (1, 0):
            r = t[(t[:, 0] == k) & (t[:, 1] == dies)]
            if len(r):
                a.plot(offs, r[0, 3:3 + len(offs)], ls, marker='o' if dies else 's', ms=3, c=col[R], alpha=1 if dies else 0.45,
                       label=f'A = {A[R]}, k = {k}, {"dies" if dies else "recovers"}')
a.set_xlim(-34, 34); a.set_xlabel('generations from the first P <= k'); a.set_ylabel('P (mean)')
a.set_title('D. equal depth: dying (dark) and recovering (pale)'); a.legend(fontsize=7)
e1 = np.array([1, -1, 0]) / np.sqrt(2); e2 = np.array([1, 1, -2]) / np.sqrt(6)
for i, R in enumerate(Rs):
    a = ax[1, 1 + i]
    c = np.genfromtxt(os.path.join(D, f'R{R}_cells.csv'), delimiter=',', skip_header=1)
    xyz = c[:, 3:6]; st = c[:, 6]; l1 = c[:, 7]
    rel = (l1 / l1.sum()) / (st / st.sum())
    sc = a.scatter(xyz @ e1, xyz @ e2, c=rel, cmap='RdBu_r', vmin=0, vmax=2, s=90, edgecolors='k', linewidths=0.3)
    plt.colorbar(sc, ax=a, label='share of last live cells / share of stationary live cells')
    a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([])
    a.set_title(f'{"EF"[i]}. A = {A[R]}: where the last cells sit (lag 1)')
fig.tight_layout()
out = os.path.join(HERE, 'hull_dying.png')
fig.savefig(out, dpi=110)
print(out)
