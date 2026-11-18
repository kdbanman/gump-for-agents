#!/usr/bin/env python3
"""Running pooled value of the dice chain's ln tau as replications accumulate (has the heavy tail been met?).

    python3 research/blast/split-hull/dice_run.py [R ...]        (default 15 17 19)

Order: the first runs (seeds 1, 2, 3, 91), then the later seeds interleaved as they ran in parallel (1001, 2001,
1002, 2002, ...).  Every 50 replications: -ln(mean rate), its error, the largest replication's share of the summed
rate, the lognormal estimate (mean of logs - variance/2).  Then per seed file: its own pooled value.
"""
import glob, math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'dice')
for R in ([int(a) for a in sys.argv[1:]] or [15, 17, 19]):
    files = []
    for f in glob.glob(os.path.join(D, f'sub_R{R}_s*.txt')) + glob.glob(os.path.join(D, f'pathrun_R{R}_s*.txt')):
        seed = int(re.search(r'_s(\d+)\.txt', f).group(1))
        files.append(((0, seed, 0) if seed < 1000 else (1, seed % 1000, seed // 1000), seed, f))
    files.sort()
    r, per = [], []
    for _, seed, f in files:
        rr = [float(l.split(' rate ')[1].split()[0]) for l in open(f) if l.startswith('REP') and ' rate ' in l]
        if rr:
            per.append((seed, rr)); r += rr
    r = np.array(r)
    if len(r) < 2:
        continue
    print(f'R = {R}: {len(r)} replications in {len(per)} runs (each run has its own stationary lanes)')
    print('    n    -ln<rate>   +-      largest share   lognormal estimate')
    for n in list(range(50, len(r), 50)) + [len(r)]:
        x = r[:n]; l = -np.log(x[x > 0]); s = l.std(ddof=1)
        print(f'  {n:4d}   {-math.log(x.mean()):.3f}   {x.std(ddof=1) / math.sqrt(n) / x.mean():.3f}     {x.max() / x.sum():.3f}          {l.mean() - s * s / 2:.3f}')
    l = -np.log(r[r > 0]); s = l.std(ddof=1)
    srt = np.sort(r)[::-1]
    print(f'  all: scatter of one replication {r.std(ddof=1) / r.mean():.2f} of the mean; sd of ln tau_k {s:.3f}, skewness {((l - l.mean()) ** 3).mean() / s ** 3:+.2f}; '
          f'the 3 largest replications carry {srt[:3].sum() / r.sum():.3f} of the sum; smallest and median ln tau_k {l.min():.2f}, {np.median(l):.2f}')
    runs = [(-math.log(np.mean(rr)), len(rr)) for _, rr in per if len(rr) >= 5]
    v = np.array([a for a, _ in runs])
    print(f'  per run (>= 5 replications): {len(v)} runs, their -ln<rate> from {v.min():.2f} to {v.max():.2f}, sd {v.std(ddof=1):.3f}')
