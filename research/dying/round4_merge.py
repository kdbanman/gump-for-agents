#!/usr/bin/env python3
"""round4_merge.py: concatenate the one-size outputs of `R4ONLY=v11c|v13c|v15c round4.py` (research/scratch/dying/r4)
into research/dying/data/r4_*.csv (identical to a run of round4.py over all sizes: each size uses its own fixed seed)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); SCR = os.path.join(HERE, '..', 'scratch', 'dying', 'r4')
for t in ('company', 'tangent', 'stationary', 'percell', 'by_k'):
    lines = []
    for v in ('v11c', 'v13c', 'v15c'):
        L = open(os.path.join(SCR, f'r4_{t}_{v}.csv')).read().splitlines()
        lines += L if not lines else L[1:]
    open(os.path.join(HERE, 'data', f'r4_{t}.csv'), 'w').write('\n'.join(lines) + '\n')
    print(t, len(lines) - 1, 'rows')
