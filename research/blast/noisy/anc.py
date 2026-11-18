#!/usr/bin/env python3
"""Ancestry of the sampler's final chains (the ANC lines that nz.c prints in sub mode).

    python3 research/blast/noisy/anc.py [DIR]        (default: research/scratch/blast/noisy/runs_diag)

Per (R, M, WBACK): the number of replications; at the last level (lambda = 0) the number D of distinct initial
chains that the dying chains descend from (median, smallest, largest) and the share of the largest family (median,
largest); the same at the first level and at mid-height; then the replications ordered by rate: rate over the mean,
D and largest share at lambda = 0, for the five largest and the median one.
"""
import glob, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'scratch', 'blast', 'noisy', 'runs_diag')
G = {}
for f in sorted(glob.glob(os.path.join(D, '*.txt'))):
    key = None; rate = {}
    for line in open(f):
        if line.startswith('# sub'):
            m = re.search(r'R (\d+) A (\d+) .* M (\d+) eps ([0-9.]+) .* WBACK (\d+)', line)
            key = (int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4)), int(m.group(5)))
        elif line.startswith('REP') and ' rate ' in line and key:
            rate[int(line.split()[1])] = float(line.split(' rate ')[1].split()[0])
        elif line.startswith('ANC') and key:
            rep = int(line.split()[1])
            lv = [(int(a), int(b), float(c)) for a, b, c in re.findall(r'(\d+):(\d+)/([0-9.]+)', line.split(':', 1)[1])]
            if rep in rate and lv and lv[-1][0] == 0:
                G.setdefault(key, []).append((rate[rep], lv))
med = lambda v: sorted(v)[len(v) // 2]
for key in sorted(G):
    R, A, M, eps, wb = key; rows = G[key]; K = len(rows); mean = sum(r for r, _ in rows) / K
    print(f'R {R} ({A} cells) eps {eps:.4f} (M {M}) WBACK {wb}: {K} replications, ln tau {-math.log(mean):.3f}')
    for name, pick in (('first level', lambda lv: lv[0]), ('mid level', lambda lv: lv[len(lv) // 2]), ('lambda = 0', lambda lv: lv[-1])):
        d = [pick(lv)[1] for _, lv in rows]; t = [pick(lv)[2] for _, lv in rows]
        print(f'    {name:11s}: distinct initial chains median {med(d)}, range {min(d)} to {max(d)};  largest family median {med(t):.3f}, largest {max(t):.3f}')
    srt = sorted(rows, key=lambda x: -x[0])
    show = srt[:5] + [srt[K // 2]]
    print('    by rate (rate/mean: D, largest share at lambda = 0): ' + ';  '.join(f'{r / mean:.2f}: {lv[-1][1]}, {lv[-1][2]:.2f}' for r, lv in show) + '  (last = median replication)')
