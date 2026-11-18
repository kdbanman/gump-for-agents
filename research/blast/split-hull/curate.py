#!/usr/bin/env python3
"""Collect a small sample of dying paths per radius from the scratch files into research/blast/split-hull/paths/.

    python3 research/blast/split-hull/curate.py [PER_RUN=40]

From every replication's paths file: at most PER_RUN paths, one per ancestor (paths that share an ancestor share
the start of their history, so one per ancestor is the nearest thing to independent deaths a replication holds).
Output paths/R<R>.txt: the header lines and the line "C" of cell coordinates as written by sh.c, then lines
    seed ancestor T k age[0..A-1] P pop[-15..0]
"""
import glob, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'runs')
PER = int(sys.argv[1]) if len(sys.argv) > 1 else 40
os.makedirs(os.path.join(HERE, 'paths'), exist_ok=True)
byR = {}
for f in sorted(glob.glob(os.path.join(RUNS, 'paths_R*_s*.txt'))):
    R, seed = map(int, re.search(r'paths_R(\d+)_s(\d+)\.txt', f).groups())
    byR.setdefault(R, []).append((seed, f))
for R, fs in sorted(byR.items()):
    out, hdr, n = [], None, 0
    for seed, f in fs:
        lines = open(f).read().split('\n')
        if hdr is None:
            hdr = [l for l in lines if l.startswith('#') or l.startswith('C')]
        seen = set(); k = 0
        for l in lines:
            if not l or l[0] in '#C':
                continue
            a = l.split(' ', 1)[0]
            if a in seen:
                continue
            seen.add(a); out.append(f'{seed} {l}'); k += 1
            if k >= PER:
                break
        n += 1
    with open(os.path.join(HERE, 'paths', f'R{R}.txt'), 'w') as fp:
        fp.write('# sample of dying paths, one per ancestor, at most %d per replication; first column added here: the seed\n' % PER)
        fp.write('\n'.join(hdr) + '\n' + '\n'.join(out) + '\n')
    print(f'R = {R}: {len(out)} paths from {n} replications')
