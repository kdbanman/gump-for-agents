#!/usr/bin/env python3
"""The face law ln tau_face = a + b*A, fitted to the flat-slab table slab_area.csv (audit U4: the constants quoted
as -0.09 + 0.209*A were typed in by hand; this is the fit).

Selection (the same as figures.py): m = 8 slabs, fewer than 6% of replicas frozen before the first peel, A >= 27.
y = ln(2 * mean first-peel time) (a slab has two faces), weights = inverse variance from the 95% CI of the mean.
Prints the fit with weighted-fit errors (the quoted +-0.06, +-0.002 are about 1.3-2x these, i.e. conservative).

    python3 research/peeling/face_law_fit.py
"""
import csv, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.DictReader(open(os.path.join(HERE, 'slab_area.csv')))
        if r['m'] == '8' and int(r['fw_before_peel']) < 0.06 * int(r['replicas']) and int(r['A']) >= 27]
A = np.array([float(r['A']) for r in rows])
ci = lambda k: np.log(2 * np.array([float(r[k]) for r in rows]))
y = np.log(2 * np.array([float(r['mean_first']) for r in rows]))
w = 1 / ((ci('ci_hi') - ci('ci_lo')) / 3.92) ** 2
X = np.c_[np.ones(len(A)), A]
cov = np.linalg.inv(X.T @ (X * w[:, None])); a, b = cov @ (X.T @ (w * y))
print(f"{len(A)} slab batches, A = {int(A.min())}..{int(A.max())}")
print(f"ln tau_face = {a:.3f} (+-{np.sqrt(cov[0, 0]):.3f}) + {b:.4f} (+-{np.sqrt(cov[1, 1]):.4f}) * A;"
      f" max residual {np.abs(y - X @ [a, b]).max():.2f}")
print("quoted: -0.09 +- 0.06 + 0.209 +- 0.002 (figures.py uses -0.090 + 0.2088)")
