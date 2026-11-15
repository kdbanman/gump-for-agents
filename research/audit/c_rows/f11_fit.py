#!/usr/bin/env python3
"""F11 (CLAIMS.md): refit ln tau_fw = a + b*N*m + c*N on research/peeling/slab_fw.csv, and print the first-event
counts quoted in the notebook (firewall first at N = 4, m = 4..6 and N = 5, m = 5..6).
    python3 research/audit/c_rows/f11_fit.py
Selection as research/peeling/figures.py's firewall panel (square N x N, 3 <= m <= 6, N >= 4, >= 20 firewall-first
events); tau_fw = the table's mean_fw (= exposure / fw_first); fits unweighted and weighted by the firewall-first count."""
import csv, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(here, '..', '..', 'peeling', 'slab_fw.csv'))))
sel = [r for r in rows if r['N1'] == r['N2'] and 3 <= int(r['m']) <= 6 and int(r['N1']) >= 4 and int(r['fw_first']) >= 20]
N = np.array([int(r['N1']) for r in sel], float); m = np.array([int(r['m']) for r in sel], float)
X = np.vstack([np.ones_like(N), N * m, N]).T
y = np.log([float(r['mean_fw']) for r in sel]); w = np.array([int(r['fw_first']) for r in sel], float)
for name, ww in (('unweighted', np.ones_like(w)), ('weighted by fw_first', w)):
    c = np.linalg.lstsq(X * np.sqrt(ww)[:, None], y * np.sqrt(ww), rcond=None)[0]; rms = np.sqrt(np.mean((y - X @ c) ** 2))
    print(f'{name:21s} {len(sel)} batches, N = {int(N.min())}-{int(N.max())}: ln tau_fw = {c[0]:+.2f} + {c[1]:.3f} N m + {c[2]:.3f} N; rms {rms:.2f}')
cut = np.array([int(r['cut']) for r in sel], float)
b, a0 = np.polyfit(cut, y, 1)
print(f'ln tau_fw against the band size (column cut = 3 x smallest transverse layer), as in figures.py: slope {b:.3f} per cell')
for r in rows:
    if r['N1'] == r['N2'] and (r['N1'], r['m']) in {('4', '4'), ('4', '5'), ('4', '6'), ('5', '5'), ('5', '6')}:
        print(f"N={r['N1']} m={r['m']}: firewall first {r['fw_first']}/{r['replicas']}, peel first {r['peel_first']}")
