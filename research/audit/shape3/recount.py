#!/usr/bin/env python3
"""Recount research/shape3/data/runs.csv from shape3's raw event files (research/scratch/shape3/ev_*.txt) and summary
lines, with own code; also the oldest open life per torus.   python3 research/audit/shape3/recount.py"""
import collections, csv, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
S3 = os.path.join(ROOT, 'research', 'scratch', 'shape3')
bad = 0; oldest = collections.defaultdict(int)
for r in csv.DictReader(open(os.path.join(ROOT, 'research', 'shape3', 'data', 'runs.csv'))):
    f = os.path.join(S3, f"ev_{r['a']}_{r['k']}_{r['b']}_c1000000000000000_s{r['seed']}.txt")
    c = collections.Counter(); E = 0
    for line in open(f):
        t, a = line.split()[:2]; a = int(a); c[t] += 1; E += a
        if t == 'E':
            oldest[(r['a'], r['k'], r['b'])] = max(oldest[(r['a'], r['k'], r['b'])], a)
    mine = dict(exposure=E, F=c['F'], X=c['X'], W=c['W'], S=c['S'], C=c['C'], open=c['E'])
    diff = {k: (v, r[k]) for k, v in mine.items() if float(r[k]) != v}
    bad += bool(diff)
    print(r['tag'], r['a'], r['k'], r['b'], r['seed'], 'identical' if not diff else diff)
print('rows differing:', bad)
for L, a in oldest.items():
    print('oldest open life', L, a)
