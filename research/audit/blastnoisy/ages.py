#!/usr/bin/env python3
"""Hazard by the age of the hull, from the AGE lines of nb (the block after the last RES line of each file).

    python3 research/audit/blastnoisy/ages.py FILE ...       files of one size and one M are pooled
Columns: ln tau_face from all eight faces (8 exposure / deaths) and from the watched face alone (exposure / d0).
"""
import math, sys
ag = {}
for f in sys.argv[1:]:
    L = open(f).read().strip().split('\n')
    i = max(k for k, l in enumerate(L) if l.startswith('RES'))
    for l in L[i + 1:]:
        if l.startswith('AGE'):
            t = [int(x) for x in l.split()[1:]]
            a = ag.setdefault(t[0], [0, 0, 0]); a[0] += t[1]; a[1] += t[2]; a[2] += t[3]
E = sum(v[0] for v in ag.values()); D0 = sum(v[1] for v in ag.values()); D = sum(v[2] for v in ag.values())
print(f'all ages: exposure {E:.3e}; eight faces {math.log(8 * E / D):.4f} +- {1 / math.sqrt(D):.4f} ({D} deaths); watched face {math.log(E / D0):.4f} +- {1 / math.sqrt(D0):.4f} ({D0})')
for lo in sorted(ag):
    e, d0, d = ag[lo]
    if d and d0:
        print(f'  age from {lo:9d}: exposure {e:.3e}  eight faces {math.log(8 * e / d):8.4f} +- {1 / math.sqrt(d):.4f} ({d:6d})   watched {math.log(e / d0):8.4f} +- {1 / math.sqrt(d0):.4f} ({d0})')
