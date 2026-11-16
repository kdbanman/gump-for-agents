#!/usr/bin/env python3
"""l6check.py: L6 (registered deficit centroid) on the second csz job (plan part 3) and on both csz jobs pooled.
    python3 research/audit/dying/l6check.py"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ana
Gm = ana.Geo('v11c', 'csz')
s = ana.samples('v11c', 'csz', Gm); GENS = json.load(open(os.path.join(ana.SCR, 'r_v11c_csz.json')))['gens']
m = ana.nullmask(s, 'study', GENS); rho = s['F'][m].mean((0, 1)); Pbar = rho.sum()
res = {}
for tag, base in (('job 1 (seed 9202)', 'r_v11c_csz'), ('job 2 (seed 9205)', 'r_v11c_csz_s2')):
    NUB = (Gm.NU + 7) // 8
    raw = np.fromfile(os.path.join(ana.SCR, base + '.dmp'), dtype=np.uint8).reshape(-1, 24 + ana.H * NUB)
    hd = raw[:, :24].copy().view(np.int32); near = []; ages = []
    for d in range(len(hd)):
        st = ana.unpack(raw[d, 24:24 + 128 * NUB].reshape(128, NUB), Gm.NU)
        k = [kk for kk in range(8) if hd[d, 4] >> kk & 1][0]
        X = st[:, Gm.fpos[k]]; P = X.sum(1)
        lh = np.cumprod(P < Pbar / 2).sum() - 1
        w = rho - X[lh]; c = (w[:, None] * Gm.canon).sum(0) / w.sum(); near.append(np.argmin(c)); ages.append(hd[d, 2])
    near = np.array(near); res[tag] = near
    print(f'{tag}: deaths {len(near)}, nearest z (tied) {np.mean(near == 2):.3f} ± {np.sqrt(np.mean(near == 2) * (1 - np.mean(near == 2)) / len(near)):.3f}; median age {np.median(ages):.0f}')
allv = np.concatenate(list(res.values()))
print(f'pooled: {len(allv)} deaths, nearest z {np.mean(allv == 2):.3f} ± {np.sqrt(np.mean(allv == 2) * (1 - np.mean(allv == 2)) / len(allv)):.3f} (study 0.211 ± 0.007 over 3001)')
