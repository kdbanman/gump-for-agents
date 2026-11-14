#!/usr/bin/env python3
"""Does the shorter cap of research/shape2 move ln tau_face, and the A = 60 pair difference?

    python3 research/audit/shape2/capcheck.py

(a) research/shape's A = 60 raw per-life files (research/scratch/shape/ch_*.npz, cap 5e5) recensored at 16,384,
    65,536 and 131,072: each life's exposure is cut at the cap and a face death counts only if it is first and
    at or before the cap. Presentations pooled by shape: 4x5 = (4,0,5)+(5,0,4); (16,4,19) = (5,1,4)+(2,3,10).
(b) the same on this review's own renewal runs (research/scratch/audit_shape2/ev_*_c500000_*.txt): a life's
    age is its exposure; truncation at the cap as above.
"""
import glob, math, os
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def shape_raw(tori, cap):
    E = F = 0.0
    for L in tori:
        for f in glob.glob(os.path.join(ROOT, 'research/scratch/shape', f'ch_{L}_s*.npz')):
            z = np.load(f)
            face, fw, st, ge = z['face'], z['fw'].min(1), z['settle'], float(z['gen_end'])
            stop = np.minimum(np.where(st >= 0, st, ge).astype(float), cap)
            end = np.minimum(np.minimum(face, fw), stop)
            E += end.sum(); F += ((face < fw) & (face <= stop)).sum()
    return math.log(2 * E / F), 1 / math.sqrt(F), int(F)


def own(L, cap):
    E = 0.0; F = 0
    for f in glob.glob(os.path.join(ROOT, 'research/scratch/audit_shape2', f'ev_{L}_c500000_s*.txt')):
        t = np.loadtxt(f, dtype=str)
        a = t[:, 1].astype(float); ty = t[:, 0]
        E += np.minimum(a, cap).sum(); F += int(((ty == 'F') & (a <= cap)).sum())
    return math.log(2 * E / F), 1 / math.sqrt(F), F


def report(fn, A, B, labA, labB, caps):
    for cap in caps:
        a, b = fn(A, cap), fn(B, cap)
        print(f'  cap {cap:>9}: {labA} {a[0]:.4f} +- {a[1]:.4f} ({a[2]}), {labB} {b[0]:.4f} +- {b[1]:.4f} ({b[2]}); '
              f'difference {a[0] - b[0]:+.4f} +- {math.hypot(a[1], b[1]):.4f}')


if __name__ == '__main__':
    caps = [16384, 65536, 131072, 500000]
    print('(a) research/shape A = 60 raw data, recensored:')
    report(shape_raw, ['4_0_5', '5_0_4'], ['5_1_4', '2_3_10'], '4x5 (16;21)', '(16;19)', caps)
    if glob.glob(os.path.join(ROOT, 'research/scratch/audit_shape2', 'ev_1_4_20_c500000_s*.txt')):
        print('(b) this review, A = 60 pair, renewal runs truncated:')
        report(own, ['1_4_20'][0], '1_5_20', '(1,4,20) (16;21)', '(1,5,20) (16;19)', caps)
