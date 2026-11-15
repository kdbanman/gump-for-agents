#!/usr/bin/env python3
"""P5 (CLAIMS.md): damage-front speeds from research/phase/damage.py's NPZ.
    python3 research/phase/damage.py OUT.npz 30 40 ss64_1.gump ... ss64_4.gump    (snapshots as in p4_oz.py)
    python3 research/audit/c_rows/p5_speeds.py OUT.npz [OTHER.npz ...]
Extent along u = support function / 2 (cubes, Euclidean), averaged over the directions of each class (axes, face
diagonals, body diagonals) as research/phase/fig_bulk.py does, then over trials; speed = least-squares slope over
generations T0..T (default 10..30; the fit window is not recorded with the claim); error = s.d. of per-trial slopes / sqrt(trials).
Also: trials whose damage died out (Hamming distance 0 at the end)."""
import sys
import numpy as np
T0 = 10
for fn in sys.argv[1:]:
    d = np.load(fn); sup, U, ham = d['sup'], d['U'], d['ham']
    T = sup.shape[1] - 1; t = np.arange(T0, T + 1)
    out = []
    for nm, msk in (('axes', np.abs(U).sum(1) == 1), ('face diag', np.abs(U).sum(1) == 2), ('body diag', np.abs(U).sum(1) == 3)):
        h = np.nanmean(sup[:, :, msk], axis=2) / 2
        sl = np.array([np.polyfit(t, h[i, T0:], 1)[0] for i in range(h.shape[0])])
        out.append(f'{nm} {sl.mean():.3f} +- {sl.std(ddof=1) / np.sqrt(len(sl)):.3f}')
    print(f"{fn}: {ham.shape[0]} trials, healed {(ham[:, -1] == 0).sum()}; speeds (cube/gen, t = {T0}-{T}): " + ', '.join(out))
