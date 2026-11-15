#!/usr/bin/env python3
"""Re-read research/shape2's raw 4x4 files (research/scratch/shape2/ch_4_0_4_s*.npz) with own code: the file's
ln tau_face, hazard by age, per-job dispersion, and the death-time grid (rep.c resolution K = 16).
    python3 research/audit/gpu_local_pr23/shape2_raw.py"""
import glob, math, os, sys
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
fs = sorted(glob.glob(os.path.join(ROOT, 'research/scratch/shape2/ch_4_0_4_s*.npz')))
E = F = W = S = L = 0
per = []
allend, allkF = [], []
for f in fs:
    z = np.load(f)
    face, fw, st, ge = z['face'], z['fw'], z['settle'], int(z['gen_end'])
    stop = np.where(st >= 0, st, ge).astype(float)
    fwm = fw.min(1)
    end = np.minimum.reduce([face, fwm, stop])
    kF = (face == end) & (face < fwm) & (face <= stop)
    kW = (fwm == end) & (fwm <= face) & (fwm <= stop)
    e, nF = end.sum(), int(kF.sum())
    E += e; F += nF; W += int(kW.sum()); L += len(end); S += int(((st >= 0) & (stop == end) & ~kF & ~kW).sum())
    per.append((int(z['seed']), e, nF)); allend.append(end); allkF.append(kF)
end = np.concatenate(allend); kF = np.concatenate(allkF)
print(f'{len(fs)} files, {L} lives, E {E:.6g}, F {F}, W {W}, settled {S}: ln(2E/F) = {math.log(2*E/F):.4f} +- {1/math.sqrt(F):.4f}')
# per-job dispersion: chi2 of per-job F against Poisson with rate F/E * e_j
lam = F / E
chi = sum((nf - lam * e) ** 2 / (lam * e) for _, e, nf in per)
print(f'per-job dispersion: chi2 {chi:.1f} on {len(per)-1} dof')
# hazard by age bins
edges = [0, 16, 32, 48, 64, 96, 128, 256, 512, 1024, 2048, 4096, 8192, 12288, 16385]
print('age bin: deaths, exposure, hazard x1e5, ln(2/h)')
for lo, hi in zip(edges[:-1], edges[1:]):
    ex = (np.clip(end, lo, hi) - lo).sum()
    d = int((kF & (end > lo) & (end <= hi)).sum())
    print(f'  ({lo},{hi}]: {d} {ex:.4g} {1e5*d/ex:.3f} {math.log(2*ex/d) if d else float("nan"):.4f}')
fd = end[kF].astype(np.int64)
print('face death time mod 16 (D = la + 1, la on the 16-grid):', np.bincount(fd % 16, minlength=16).tolist())
