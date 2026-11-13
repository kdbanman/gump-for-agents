#!/usr/bin/env python3
"""research/figures/fluct_tail.png: (left) asymmetric faces, -ln P(n <= k) / A against x = k/A with the death rate
as the point x = 0; (middle) ln p_k near k = 0 with ln h at k = 0; (right) symmetric residences ln tau against A.
  python3 research/fluct/figures.py
"""
import glob, json, math, os, sys
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fl
HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda t: np.load(os.path.join(fl.SCR, f'qsd_{t}.npz'))
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
cols = plt.cm.viridis(np.linspace(0, 0.9, 7))
for i, R in enumerate((7, 9, 11, 13, 15, 17, 19)):
    try: z = L(f'R{R}')
    except FileNotFoundError: continue
    H = z['H'].astype(float); A = len(H) - 1; N = H.sum(); c = np.cumsum(H); ok = c >= 20
    k = np.arange(A + 1)
    ax[0].plot(k[ok] / A, -np.log(c[ok] / N) / A, color=cols[i], label=f'A={A}')
    d = z['deaths'][0]
    if d >= 20:
        h = d / z['expo'][0] / 8
        ax[0].plot([0], [-math.log(h) / A], 'o', color=cols[i])
        p = H / N; kk = np.nonzero(H[:12] >= 30)[0]
        ax[1].plot(kk, np.log(p[kk]), '-', color=cols[i], marker='.')
        ax[1].plot([0], [math.log(h)], 'o', color=cols[i], label=f'A={A}')
ax[0].set_xlim(0, 0.45); ax[0].set_ylim(0, 0.25); ax[0].set_xlabel('x = n/A'); ax[0].set_ylabel('-ln P(n <= xA) / A')
ax[0].set_title('asymmetric faces: rate function; dot = -ln(h_face)/A'); ax[0].legend(fontsize=8)
ax[1].set_xlabel('k (live cells in the face)'); ax[1].set_ylabel('ln p_k   (k = 0: ln h, deaths per generation)')
ax[1].set_title('the death rate continues the QSD to k = 0'); ax[1].legend(fontsize=8)
pts = []
for f in glob.glob(os.path.join(fl.SCR, 'qsd_sym*.npz')) + glob.glob(os.path.join(fl.SCR, 'qsd_snap*.npz')):
    z = np.load(f); d = z['deaths'][0]
    if d < 3: continue
    A = len(z['H']) - 1; t = os.path.basename(f)
    pts.append((A, math.log(z['expo'][0] / d), 1 / math.sqrt(d), 'v' if ('v.npz' in t or 'snap' in t) else 'c'))
for cen, mk in (('c', 'o'), ('v', 's')):
    P = [p for p in pts if p[3] == cen]
    if P:
        a, l, e, _ = zip(*P); ax[2].errorbar(a, l, yerr=e, fmt=mk, label=f'O_h soups / cube copies ({"cube" if cen == "c" else "vertex"}-centred)')
AA = np.linspace(380, 860, 50)
ax[2].plot(AA, -0.14 + 0.0272 * AA, '--', color='grey', label='symmetric face law (peeling study)')
ax[2].plot(AA, 1.57 + 0.0348 * AA - 0.236 * np.sqrt(AA), ':', color='k', label="lead's fit a + (0.209/6)A + c sqrt(A)")
ax[2].set_xlabel('face area A'); ax[2].set_ylabel('ln (mean residence)'); ax[2].legend(fontsize=7); ax[2].set_title('symmetric faces, brute force')
fig.tight_layout(); out = os.path.join(HERE, '..', 'figures', 'fluct_tail.png'); fig.savefig(out, dpi=110); print(out)
