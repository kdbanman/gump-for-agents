#!/usr/bin/env python3
"""Ids for the oracle sample: K ends at random (seed 7) plus up to M ends of every outcome vector of the fast census.

    python3 sample_ids.py K M FAST.json [FAST.json ...]      -> prints the ids, comma separated
"""
import sys, json, random
from collections import defaultdict
K, M = int(sys.argv[1]), int(sys.argv[2])
rows = {}
for fn in sys.argv[3:]:
    for r in json.load(open(fn))['rows']:
        rows[r['i']] = r
ids = set(random.Random(7).sample(sorted(rows), min(K, len(rows))))
vec = defaultdict(list)
for i in sorted(rows):
    vec[tuple(o['out'] for o in rows[i]['outcomes'])].append(i)
rnd = random.Random(8)
for v, lst in vec.items():
    ids |= set(rnd.sample(lst, min(M, len(lst))))
print(','.join(map(str, sorted(ids))))
