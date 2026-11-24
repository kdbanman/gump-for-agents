#!/usr/bin/env python3
"""Compare the watched face's births and deaths, and the support under it, between chains (layer-diagnostic rows).

    python3 research/blast/density/drift.py FILE [FILE ...]     (outputs of nzd with NZD_LAYERS=1: DRIFT, BYPOP lines)

For each population p of the watched face (the generation before) and each file: births per generation split by the
number of the newborn's three neighbours below (2 in layer 1, 1 in layer 2) alive the generation before, deaths per
generation, the mean drift (births - deaths), the supply (dead face cells with 2 and with 3 live cells below), the
conversion (births with 3 below / dead cells with 3 below), and the density of the replaced cells of layer 1 and 2
(core1, core2) at that population.
"""
import sys

def load(f):
    D = {}; BY = {}
    for l in open(f):
        t = l.split()
        if l.startswith('DRIFT') and t[1].isdigit():
            p = int(t[1]); v = [float(x) for x in t[3:]]
            D[p] = dict(n=v[0], b=v[1:5], d=v[5], s2=v[6], s3=v[7])
        if l.startswith('BYPOP'):
            BY[t[1]] = {int(x.split(':')[0]): float(x.split(':')[1]) for x in t[3:]}
    return D, BY

runs = [(f.split('/')[-1].replace('.txt', ''), *load(f)) for f in sys.argv[1:]]
ps = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 31]
print('p    chain                 count    b0     b1     b2     b3   deaths  drift   dead2  dead3  b3/dead3  core1  core2  full1')
for p in ps:
    for name, D, BY in runs:
        if p not in D:
            continue
        r = D[p]; b = r['b']
        print(f'{p:3d}  {name:20s} {r["n"]:8.0f} {b[0]:6.3f} {b[1]:6.3f} {b[2]:6.3f} {b[3]:6.3f} {r["d"]:6.3f} {sum(b) - r["d"]:+7.3f} '
              f'{r["s2"]:6.2f} {r["s3"]:6.2f} {b[3] / r["s3"] if r["s3"] else 0:8.4f}  {BY.get("core1", {}).get(p, -1):.3f}  {BY.get("core2", {}).get(p, -1):.3f}  {BY.get("full1", {}).get(p, -1):.3f}')
    print()
