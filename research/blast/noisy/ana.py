#!/usr/bin/env python3
"""Pool the replications of the subset sampler on the noisy chain.

    python3 research/blast/noisy/ana.py [DIR_OR_FILES ...]      (default: the committed rows, data/runs/)

Groups the REP lines of all given files by the header line (R, M, sampler parameters).  Per group: the number of
replications K; ln tau = -ln(mean rate) with the error from the scatter of the replications' rates (and a
jackknife); the scatter of one replication's rate as a fraction of the mean; the largest replication's share of
the summed rate; how many replications carry half of the summed rate (the fewer, the less the error can be
trusted: "has the tail been met?"); the running pooled value every 50 replications in file order.
"""
import glob, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:] or [os.path.join(HERE, 'data', 'runs')]
files = []
for a in args:
    files += sorted(glob.glob(os.path.join(a, '*.txt'))) if os.path.isdir(a) else [a]
groups = {}
for f in files:
    key = None
    for line in open(f):
        if line.startswith('# sub'):
            t = line.split(); d = dict(zip(t[2::2], t[3::2]))
            key = tuple((k, d[k]) for k in ('R', 'A', 'DW', 'DO', 'M', 'eps', 'LAM1', 'DELTA', 'chains', 'NSWEEP', 'KFLIP', 'TPRE', 'TWIN', 'WBACK'))
        elif line.startswith('REP') and ' rate ' in line and key:
            groups.setdefault(key, []).append(float(line.split(' rate ')[1].split()[0]))
for key in sorted(groups, key=lambda k: (int(dict(k)['R']), float(dict(k)['eps']), int(dict(k)['KFLIP']), int(dict(k)['NSWEEP']))):
    d = dict(key); r = np.array(groups[key]); K = len(r)
    if K < 2:
        continue
    m = r.mean(); est = -math.log(m); err = r.std(ddof=1) / math.sqrt(K) / m
    jk = np.array([-math.log((r.sum() - x) / (K - 1)) for x in r]); jerr = math.sqrt((K - 1) / K * ((jk - jk.mean()) ** 2).sum())
    srt = np.sort(r)[::-1]; half = int(np.searchsorted(np.cumsum(srt), 0.5 * r.sum()) + 1)
    l = -np.log(r[r > 0]); s = l.std(ddof=1)
    print(f"R {d['R']} ({d['A']} cells) eps {float(d['eps']):.4f} (M {d['M']}, N {d['DW']},{d['DO']}) KFLIP {d['KFLIP']} NSWEEP {d['NSWEEP']} LAM1 {d['LAM1']} "
          f"T {d['TPRE']}+{d['TWIN']} WBACK {d['WBACK']}: K = {K}")
    print(f"    ln tau = {est:.3f} +- {err:.3f} (jackknife {jerr:.3f});  one replication scatters by {r.std(ddof=1) / m:.2f} of the mean;  largest share {srt[0] / r.sum():.3f};  "
          f"{half} replications carry half the rate;  median ln tau_k {np.median(l):.2f}, sd {s:.2f};  zero-rate {int((r == 0).sum())}")
    if K >= 100:
        print('    running value: ' + '  '.join(f'{n}: {-math.log(r[:n].mean()):.3f}' for n in list(range(50, K, 50)) + [K]))
