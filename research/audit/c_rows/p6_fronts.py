#!/usr/bin/env python3
"""P6 (CLAIMS.md): planar front speeds from research/phase/front_planar.py's NPZ.
    python3 research/phase/front_planar.py OUT.npz 72 110 4
    python3 research/audit/c_rows/p6_fronts.py OUT.npz [OTHER.npz ...]
Advance in cubes = adv / |d| / 2 as in research/phase/fig_bulk.py; speed = least-squares slope of the trial mean
over several windows (the window is not recorded with the claim), error = s.d. of per-trial slopes / sqrt(trials)."""
import sys
import numpy as np
for fn in sys.argv[1:]:
    d = np.load(fn)
    for nm, nrm in (('100', 1), ('110', np.sqrt(2)), ('111', np.sqrt(3))):
        A = d[nm] / nrm / 2; T = A.shape[1] - 1; parts = []
        for a, b in ((0, T), (20, T), (40, T), (60, T)):
            t = np.arange(a, b + 1); sl = np.array([np.polyfit(t, A[i, a:b + 1], 1)[0] for i in range(A.shape[0])])
            parts.append(f'{a}-{b}: {sl.mean():.4f} +- {sl.std(ddof=1) / np.sqrt(len(sl)):.4f}')
        print(f'{fn} {{{nm}}} final advance {A[:, -1].mean():.2f} cubes; slopes ' + '; '.join(parts))
