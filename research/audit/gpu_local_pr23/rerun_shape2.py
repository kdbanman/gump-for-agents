#!/usr/bin/env python3
"""research/shape2's own pipeline (research/shape/tslab.run: rep.c, W = 64, cap 16,384, K = 16) on the 4x4 torus,
re-run here into research/scratch/audit_gpu_local_pr23/shape2_rerun/ (their code, only read; output redirected):
one job with an original seed (must reproduce research/scratch/shape2/ch_4_0_4_s<seed>.npz exactly) and fresh seeds.
    python3 research/audit/gpu_local_pr23/rerun_shape2.py SEED [SEED ...]
    python3 research/audit/gpu_local_pr23/rerun_shape2.py --stats       # ln tau_face over the files in the directory
  RERUN_DIR=orig ... $(seq 1008000 1008075)  reproduces every original job; RERUN_DIR=fresh ... $(seq 5008000 5008303)
"""
import glob, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'shape'))
import tslab  # noqa: E402
tslab.OUT = os.path.join(ROOT, 'research', 'scratch', 'audit_gpu_local_pr23', os.environ.get('RERUN_DIR', 'shape2_rerun'))
os.makedirs(tslab.OUT, exist_ok=True)

if __name__ == '__main__':
    if sys.argv[1] == '--stats':
        s = tslab.stats(4, 0, 4)
        print(f"{s['runs']} jobs, {s['lives']} lives: F {s['F']}, W {s['Wn']}, settled {s['settled']}, "
              f"ln tau_face {s['lnF']:.4f} +- {s['eF']:.4f}; thirds {[round(x[0], 4) for x in s['thirds']]}")
        orig = sorted(glob.glob(os.path.join(ROOT, 'research', 'scratch', 'shape2', 'ch_4_0_4_s*.npz')))
        for f in glob.glob(os.path.join(tslab.OUT, 'ch_4_0_4_s*.npz')):
            o = os.path.join(ROOT, 'research', 'scratch', 'shape2', os.path.basename(f))
            if os.path.exists(o):
                a, b = np.load(f), np.load(o)
                same = all(np.array_equal(a[k], b[k]) for k in ('face', 'fw', 'settle', 'gen_end'))
                print(f'{os.path.basename(f)}: identical to the original file: {same}')
    else:
        for sd in sys.argv[1:]:
            tslab.run(4, 0, 4, 16384, int(sd), 64)
