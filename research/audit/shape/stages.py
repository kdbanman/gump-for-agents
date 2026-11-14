#!/usr/bin/env python3
"""The A = 60 systole-16 difference split by stage (seeds < 400000: before the top-up; >= 400000: the top-up),
recomputed from research/shape's raw per-life files (research/scratch/shape/ch_*.npz, git-ignored) with an own
first-event estimator: end = min(face, firewall, settle-or-run-end); face death counts if strictly first.

    python3 research/audit/shape/stages.py
"""
import glob, math, os
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = os.path.join(ROOT, 'research', 'scratch', 'shape')


def est(files):
    E = F = 0.0; capped = lives = 0
    for f in files:
        z = np.load(f)
        face, fw, st, ge = z['face'], z['fw'].min(1), z['settle'], int(z['gen_end'])
        stop = np.where(st >= 0, st, ge).astype(float)
        end = np.minimum(np.minimum(face, fw), stop)
        E += end.sum(); F += ((face == end) & (face < fw)).sum(); lives += len(face)
        capped += ((end == ge) & (st < 0)).sum()
    return E, F, lives, capped


res = {}
for L in ['4_0_5', '5_0_4', '5_1_4', '2_3_10']:
    fs = glob.glob(os.path.join(D, f'ch_{L}_s*.npz'))
    seed = lambda f: int(f.rsplit('_s', 1)[1][:-4])
    for lab, sel in [('before top-up', lambda s: s < 400000), ('top-up', lambda s: s >= 400000), ('all', lambda s: True)]:
        E, F, n, c = est([f for f in fs if sel(seed(f))])
        res[(L, lab)] = (E, F)
        print(f'{L:7s} {lab:14s} lives {n:6d} capped {c:5d}  F {int(F):6d}  ln tau_face {math.log(2 * E / F):.4f} +- {1 / math.sqrt(F):.4f}')
for lab in ['before top-up', 'top-up', 'all']:
    def pooled(ts):
        E = sum(res[(t, lab)][0] for t in ts); F = sum(res[(t, lab)][1] for t in ts)
        return math.log(2 * E / F), 1 / math.sqrt(F)
    a, ea = pooled(['4_0_5', '5_0_4']); b, eb = pooled(['5_1_4', '2_3_10'])
    print(f'{lab:14s} (16,12,21) {a:.4f} +- {ea:.4f}   (16,4,19) {b:.4f} +- {eb:.4f}   difference {a - b:+.4f} +- {math.hypot(ea, eb):.4f} '
          f'({(a - b) / math.hypot(ea, eb):.1f} sigma)')
