#!/usr/bin/env python3
"""Z5 (CLAIMS.md): union of final-cycle periods over harvest.py outputs, and whether two sets of outputs agree.
    python3 research/audit/c_rows/z5_periods.py DIR [DIR2]
DIR holds harvest_*.json (research/atlas/harvest.py writes them to research/scratch/atlas/)."""
import glob, json, os, sys
from collections import Counter
def load(d):
    out = {}
    for f in sorted(glob.glob(os.path.join(d, 'harvest_*.json'))):
        h = json.load(open(f)); out[os.path.basename(f)] = h
    return out
def periods(h):
    c = Counter()
    for s in h['soups']:
        c[s['period'] if isinstance(s, dict) else s[1]] += 1
    return c
A = load(sys.argv[1]); tot = Counter(); n = 0
for k, h in A.items():
    tot += periods(h); n += h['n']
print(f'{len(A)} files, {n} soups; periods present: {sorted(tot)}')
if len(sys.argv) > 2:
    B = load(sys.argv[2])
    for k in A:
        same = k in B and A[k]['soups'] == B[k]['soups']
        print(f'  {k}: soups identical to {sys.argv[2]}: {same}')
