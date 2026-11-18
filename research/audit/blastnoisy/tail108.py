#!/usr/bin/env python3
"""The large replications of the 108-cell sampler runs: how much of the rate they carry.

    python3 research/audit/blastnoisy/tail108.py PR_RUNS_DIR [MY_RUNS_DIR]

A replication is "large" when its rate exceeds K times the median rate of its eps (K = 5, 10).  Per eps and for all
eps together: number of replications, number of large ones, their share of the summed rate, ln tau of the rest
("bulk") and of all, against gump (23.3392 +- 0.0099).  With MY_RUNS_DIR (this audit's data/runs) the replications
of c15_* are added (they carry ancestry: the share of the score-0 chains that descend from one initial state).
"""
import glob, math, os, sys
import numpy as np
G = 23.3392
groups = {}
for d in sys.argv[1:]:
    for f in sorted(glob.glob(os.path.join(d, '*R15_*.txt')) + glob.glob(os.path.join(d, 'c15_*.txt'))):
        M = None
        for line in open(f):
            if line.startswith('# sub'):
                t = line.split(); M = int(dict(zip(t[2::2], t[3::2]))['M'])
            elif line.startswith('REP') and ' rate ' in line:
                top = float(line.split(' top_hit ')[1].split()[0]) if ' top_hit ' in line else float('nan')
                groups.setdefault(M, []).append((float(line.split(' rate ')[1].split()[0]), top))
allr = []
print('  eps    replications   median ln tau_k   large (> 5x / > 10x median)   share of the rate (> 5x / > 10x)   ln tau all       bulk (<= 10x median)   bulk - gump')
for M in sorted(groups, reverse=True):
    r = np.array([x[0] for x in groups[M]]); med = np.median(r); x = r / med
    allr += list(x)
    b = r[x <= 10]
    print(f'  1/{2048 // M:<4d} {len(r):6d}         {-math.log(med):8.3f}          {int((x > 5).sum()):3d} / {int((x > 10).sum()):3d}'
          f'                     {r[x > 5].sum() / r.sum():.3f} / {r[x > 10].sum() / r.sum():.3f}                    '
          f'{-math.log(r.mean()):7.3f}          {-math.log(b.mean()):7.3f}            {-math.log(b.mean()) - G:+.3f}')
    tops = [(xx, t) for (rr, t), xx in zip(groups[M], x) if t == t and (xx > 5 or t > 0.5)]
    if tops:
        print('          with ancestry: (rate / median, share of the commonest initial state among the score-0 chains): '
              + ', '.join(f'({a:.1f}, {t:.2f})' for a, t in sorted(tops, reverse=True)))
x = np.array(allr)
n5, n10 = int((x > 5).sum()), int((x > 10).sum())
print(f'  all eps together (each rate over the median of its eps): {len(x)} replications; {n5} above 5x, {n10} above 10x; '
      f'they carry {x[x > 5].sum() / x.sum():.3f} and {x[x > 10].sum() / x.sum():.3f} of the summed rate; '
      f'mean of the ones above 10x: {x[x > 10].mean() if n10 else 0:.1f}x; one in {len(x) / max(n10, 1):.0f} replications')
p = n10 / len(x)
for M in sorted(groups, reverse=True):
    n = len(groups[M])
    print(f'    at that frequency, eps 1/{2048 // M}: {n} replications meet none with probability {math.exp(-n * p):.2f}')
