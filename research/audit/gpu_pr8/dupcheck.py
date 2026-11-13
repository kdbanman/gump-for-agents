#!/usr/bin/env python3
"""Audit of PR 8: are repeated death ages more common than chance? (duplicate soups would give identical ages)

  python3 research/audit/gpu_pr8/dupcheck.py PR8_WORKTREE

Chance expectation of exact coincidences estimated from near-coincidences: pairs with 1 <= |a - b| <= W, divided by 2W
(local density is smooth on that scale). Also lists the repeated ages and, where raw lives are stored, their births.
"""
import base64, glob, json, os, sys, zlib
from collections import Counter
import numpy as np
root = sys.argv[1]
W = 200
for p in sorted(glob.glob(os.path.join(root, 'research/data/gpu_facelaw/*.json'))):
    r = json.load(open(p)); da = r.get('death_ages')
    if not da: continue
    a = np.sort(np.array(da, np.int64)); a = a[a > 10 ** 4]
    exact = sum(n * (n - 1) // 2 for n in Counter(a.tolist()).values() if n > 1)
    near = 0
    for k in range(1, len(a)):
        j = np.searchsorted(a, a[k] - W)
        near += int(((a[k] - a[j:k]) >= 1).sum())
    print(f"{os.path.basename(p):28s} n={len(a):6d} exact pairs={exact:4d}  chance~{near / (2 * W):.1f}")
    rep = [x for x, n in Counter(a.tolist()).items() if n > 1]
    if rep and 'raw' in r:
        raw = np.frombuffer(zlib.decompress(base64.b64decode(r['raw']['b64'])), np.int64).reshape(r['raw']['shape'])
        for x in rep[:10]:
            m = (raw[0] == x) & (raw[1] == 1)
            print('    age', x, 'births', raw[2][m].tolist())
    elif rep:
        print('    repeated ages (first 10):', rep[:10])
# gaps between consecutive launch boundaries make ages a difference of two boundaries plus tt; check the low bits of ages
