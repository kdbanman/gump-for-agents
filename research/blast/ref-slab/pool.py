#!/usr/bin/env python3
"""Referee's pooling of subset-sampler replications (split-slab's files and/or fresh ones).

    python3 pool.py LABEL FILE [FILE ...]

Per replication r_i = rate (REP lines).  Prints: n; ln tau from the mean rate with the delta-method error (what
split-slab quotes); bootstrap 16-84% and 2.5-97.5% interval of -ln(mean rate); median ln tau; sd of ln r; the share
of the summed rate carried by the largest replication; a lognormal reading (-(mean ln r) - s^2/2); DIAG: mean
number of distinct ancestors (initial states) among the dying chains, if present.
"""
import sys, math
import numpy as np
label = sys.argv[1]; r = []; anc = []
for fn in sys.argv[2:]:
    for line in open(fn):
        t = line.split()
        if line.startswith('REP') and 'rate' in t:
            r.append(float(t[t.index('rate') + 1]))
        if line.startswith('DIAG'):
            anc.append(int(t[5]))
r = np.array(r); n = len(r); m = r.mean(); se = r.std(ddof=1) / math.sqrt(n) / m
rs = np.random.RandomState(1)
bs = -np.log(r[rs.randint(0, n, (20000, n))].mean(1))
lr = np.log(r); s = lr.std(ddof=1)
q = np.percentile(bs, [2.5, 16, 84, 97.5])
print(f'{label}: n = {n}; ln tau (mean rate) = {-math.log(m):.3f} +- {se:.3f}; bootstrap 68% [{q[1]:.3f}, {q[2]:.3f}] 95% [{q[0]:.3f}, {q[3]:.3f}]; '
      f'median ln tau {-np.median(lr):.3f}; sd of ln rate {s:.3f} (rel sd of a replication {r.std(ddof=1) / m:.2f}); largest replication carries {r.max() / r.sum():.2f} of the sum; '
      f'lognormal reading {-(lr.mean() + s * s / 2):.3f} +- {math.sqrt(s * s / n + s ** 4 / (2 * (n - 1))):.3f}'
      + (f'; distinct ancestors of the dying chains: mean {np.mean(anc):.1f}, min {min(anc)}, max {max(anc)}' if anc else ''))
