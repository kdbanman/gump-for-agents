#!/usr/bin/env python3
"""The law of one replication's rate in the sampler's committed rows: is the error bar honest?

    python3 research/blast/noisy/tails.py [DIR]        (default: research/blast/noisy/data/runs)

Per (R, M): replications K; the scatter of one replication (sd over mean); the median, 90% and 99% points and the
largest rate, all over the mean; the share of the summed rate carried by the top 1% and 5% of the replications; the
sd of ln(rate) and the scatter a lognormal with that sd would have; the error of ln tau from the scatter of
replications and from the scatter of the means of whole runs (ten replications sharing 512 lanes): if the second
were larger, replications of one run would not be independent.
"""
import glob, math, os, re, sys, statistics as st
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'data', 'runs')
runs = defaultdict(list)
for f in sorted(glob.glob(os.path.join(D, '*.txt'))):
    key = None; r = []
    for line in open(f):
        if line.startswith('# sub'):
            m = re.search(r'R (\d+) .* M (\d+) eps ([0-9.]+)', line); key = (int(m.group(1)), int(m.group(2)), float(m.group(3)))
        elif line.startswith('REP') and ' rate ' in line:
            r.append(float(line.split(' rate ')[1].split()[0]))
    if key and r: runs[key].append(r)
for key in sorted(runs):
    rr = runs[key]; allr = [x for r in rr for x in r]; K = len(allr); m = sum(allr) / K
    x = sorted(v / m for v in allr); q = lambda p: x[min(K - 1, int(p * K))]; sd = st.pstdev(x)
    top1 = sum(x[-max(1, K // 100):]) / K; top5 = sum(x[-max(1, K // 20):]) / K
    sl = st.pstdev([math.log(v) for v in x if v > 0])
    rm = [sum(r) / len(r) / m for r in rr if len(r) == 10]
    e_run = st.pstdev(rm) / math.sqrt(len(rm)) if len(rm) > 2 else float('nan')
    print(f'R {key[0]} eps {key[2]:.4f} K {K:3d}: scatter {sd:.2f}; median {q(.5):.2f}, 90% {q(.9):.2f}, 99% {q(.99):.2f}, '
          f'largest {x[-1]:.1f} of the mean; top 1% carry {top1:.3f}, top 5% {top5:.3f}; sd of ln {sl:.2f} (a lognormal '
          f'with it scatters {math.sqrt(math.exp(sl * sl) - 1):.2f}); error by replications {sd / math.sqrt(K):.3f}, by runs {e_run:.3f}')
