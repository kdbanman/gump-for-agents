#!/usr/bin/env python3
"""Copy the small results of the review from research/scratch/audit_noisy into this directory's data/:
data/brute and data/young: the last RES line of every nb run and its AGE lines; data/runs/<tag>.txt: the header and
REP lines of every sampler run of that tag, in seed order.

    python3 research/audit/blastnoisy/collect.py
"""
import glob, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, '..', '..', 'scratch', 'audit_noisy')
for sub in ('brute', 'young'):
    os.makedirs(os.path.join(HERE, 'data', sub), exist_ok=True)
    for f in sorted(glob.glob(os.path.join(S, sub, '*.txt'))):
        L = open(f).read().strip().split('\n')
        idx = [k for k, l in enumerate(L) if l.startswith('RES')]
        if idx:
            open(os.path.join(HERE, 'data', sub, os.path.basename(f)), 'w').write('\n'.join(L[idx[-1]:]) + '\n')
os.makedirs(os.path.join(HERE, 'data', 'runs'), exist_ok=True)
tags = {}
for f in sorted(glob.glob(os.path.join(S, 'runs', '*_s*.txt'))):
    m = re.match(r'(.*)_s(\d+)\.txt$', os.path.basename(f))
    tags.setdefault(m.group(1), []).append((int(m.group(2)), f))
for tag, fs in tags.items():
    with open(os.path.join(HERE, 'data', 'runs', tag + '.txt'), 'w') as o:
        for _, f in sorted(fs):
            for line in open(f):
                if line.startswith('# sub') or line.startswith('REP'):
                    o.write(line)
print('copied', sum(len(v) for v in tags.values()), 'runs in', len(tags), 'tags')
