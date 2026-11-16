#!/usr/bin/env python3
"""repro.py: bias.py's K = 16 lives against research/shape2's own per-job files (research/scratch/shape2/ch_*.npz,
the jobs behind research/shape2/data/A48.csv and A60.csv), job by job.

    python3 repro.py A K B
"""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
a, k, b = sys.argv[1:4]
same = diff = missing = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_tori', 'bias', f'b_{a}_{k}_{b}_s*.npz'))):
    s = f.rsplit('_s', 1)[1][:-4]
    g = os.path.join(ROOT, 'research', 'scratch', 'shape2', f'ch_{a}_{k}_{b}_s{s}.npz')
    if not os.path.exists(g):
        missing += 1; continue
    x, y = np.load(f), np.load(g)
    ok = all(np.array_equal(x[f'{n}16'], y[m]) for n, m in (('face', 'face'), ('fw', 'fw'), ('st', 'settle'))) \
        and int(x['ge16']) == int(y['gen_end'])
    same += ok; diff += not ok
print(f'({a},{k}),(0,{b}): jobs identical to research/scratch/shape2 {same}, different {diff}, no original file {missing}')
