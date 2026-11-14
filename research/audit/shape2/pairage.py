#!/usr/bin/env python3
"""A = 60 pair (16;21) - (16;19): difference of ln tau_face in age bins, in three data sets.

    python3 research/audit/shape2/pairage.py

Is the difference the same in young and old lives? If it is, a cap only costs precision and the three runs can be
pooled; if it grows with age, a short cap biases the difference down.
  shape2  research/scratch/shape2/ch_1_{4,5}_20_*.npz   (cap 65,536)
  shape   research/scratch/shape/ch_{4_0_5,5_0_4 | 5_1_4,2_3_10}_*.npz   (cap 5e5)
  review  research/scratch/audit_shape2/ev_1_{4,5}_20_*.txt   (renewal, cap 5e5)
"""
import glob, math, os
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
EDGES = [0, 16384, 65536, 131072, 262144, 1e9]


def npz(tori, d):
    end, isF = [], []
    for L in tori:
        for f in glob.glob(os.path.join(ROOT, 'research/scratch', d, f'ch_{L}_s*.npz')):
            z = np.load(f)
            face, fw, st, ge = z['face'], z['fw'].min(1), z['settle'], float(z['gen_end'])
            stop = np.where(st >= 0, st, ge).astype(float)
            e = np.minimum(np.minimum(face, fw), stop)
            end.append(e); isF.append((face < fw) & (face <= stop))
    return np.concatenate(end), np.concatenate(isF)


def ev(L):
    end, isF = [], []
    for f in glob.glob(os.path.join(ROOT, 'research/scratch/audit_shape2', f'ev_{L}_c500000_s*.txt')):
        t = np.loadtxt(f, dtype=str); end.append(t[:, 1].astype(float)); isF.append(t[:, 0] == 'F')
    return np.concatenate(end), np.concatenate(isF)


def bins(end, isF):
    out = []
    for lo, hi in zip(EDGES[:-1], EDGES[1:]):
        ex = (np.clip(end, lo, hi) - lo).sum(); nf = int((isF & (end > lo) & (end <= hi)).sum())
        out.append((math.log(2 * ex / nf), 1 / math.sqrt(nf), nf) if nf > 20 else None)
    return out


sets = {'shape2': (npz(['1_4_20'], 'shape2'), npz(['1_5_20'], 'shape2')),
        'shape': (npz(['4_0_5', '5_0_4'], 'shape'), npz(['5_1_4', '2_3_10'], 'shape')),
        'review': (ev('1_4_20'), ev('1_5_20'))}
allb = [[] for _ in EDGES[:-1]]
for name, (A, B) in sets.items():
    ba, bb = bins(*A), bins(*B)
    row = []
    for i, (x, y) in enumerate(zip(ba, bb)):
        if x and y:
            d, e = x[0] - y[0], math.hypot(x[1], y[1]); row.append(f'{d:+.4f}+-{e:.4f}'); allb[i].append((d, e))
        else:
            row.append('-')
    print(f'{name:7s} ' + '  '.join(f'[{int(lo)},{int(hi) if hi < 1e9 else "inf"}): {r}' for lo, hi, r in zip(EDGES[:-1], EDGES[1:], row)))
print('pooled over data sets, per age bin:')
ms = []
for (lo, hi), lst in zip(zip(EDGES[:-1], EDGES[1:]), allb):
    w = sum(1 / e ** 2 for _, e in lst); m = sum(d / e ** 2 for d, e in lst) / w; ms.append((m, 1 / math.sqrt(w)))
    print(f'  [{int(lo)},{int(hi) if hi < 1e9 else "inf"}): {m:+.4f} +- {1 / math.sqrt(w):.4f}  (chi2 between data sets {sum(((d - m) / e) ** 2 for d, e in lst):.2f} / {len(lst) - 1})')
w = sum(1 / e ** 2 for _, e in ms); m = sum(d / e ** 2 for d, e in ms) / w
print(f'  constant in age: {m:+.4f} +- {1 / math.sqrt(w):.4f}, chi2 {sum(((d - mm) / e) ** 2 for (d, e), mm in zip(ms, [m] * len(ms))):.2f} / {len(ms) - 1}')
