#!/usr/bin/env python3
"""Dying paths of the dice chain kept by the subset sampler (data/subpaths_*.txt): is it still boom and bust?

    python3 subpaths.py FILE [FILE ...] A        # files of one torus are pooled

Line format:  S rep chain gd | pop(gd-1) pop(gd-2) ... (up to 24 generations back; gd = death generation in the
56-generation window).  Chains of one replication descend from few ancestors and are strongly correlated, so every
statistic is computed per replication first; quoted: mean over replications and their standard error.
"""
import math, sys
import numpy as np
A = int(sys.argv[-1]); mu, sd = 0.515 * A, math.sqrt(0.415 * A)      # python3 subpaths.py FILE [FILE ...] A   (files of one torus are pooled)
reps = {}
for fi, fn in enumerate(sys.argv[1:-1]):
    for line in open(fn):
        if line[0] != 'S':
            continue
        a, b = line.split('|'); t = a.split(); p = list(map(int, b.split()))
        if len(p) >= 16:
            reps.setdefault((fi, int(t[1])), []).append(p[:16])
st = {k: [] for k in ('half', 'p4', 'fall', 'top', 'after', 'lag', 'maxpop', 'gens_below_third', 'second', 'gap', 'two', 'sumtwo')}
for r, rows in sorted(reps.items()):
    P = np.array(rows); d = P[:, 1:] - P[:, :-1]; big = d.max(1); bl = d.argmax(1) + 1
    top = P[np.arange(len(P)), bl]; aft = P[np.arange(len(P)), bl - 1]
    st['half'].append((big >= A / 2).mean()); st['p4'].append((big >= 0.4 * A).mean()); st['fall'].append(big.mean())
    st['top'].append(top.mean()); st['after'].append(aft.mean()); st['lag'].append(bl.mean()); st['maxpop'].append(P.max(1).mean())
    st['gens_below_third'].append((P < mu / 3).sum(1).mean())
    ds = np.sort(d, axis=1); second = ds[:, -2]; order = np.argsort(d, axis=1); gap = np.abs(order[:, -1] - order[:, -2])
    st['second'].append(second.mean()); st['gap'].append(gap.mean()); st['two'].append(((second >= 0.15 * A) & (gap >= 2)).mean()); st['sumtwo'].append((big + second).mean())
n = len(reps)
f = lambda k: f'{np.mean(st[k]):.2f} ± {np.std(st[k], ddof=1) / math.sqrt(n) if n > 1 else float("nan"):.2f}'
print(f'{" + ".join(sys.argv[1:-1])}: A = {A}, {sum(len(v) for v in reps.values())} dying chains in {n} replications; stationary population {mu:.1f} ± {sd:.1f}')
print(f'  share of deaths with a one-generation fall >= A/2: {f("half")};  >= 0.4 A: {f("p4")}')
print(f'  largest one-generation fall: {f("fall")} cells = {np.mean(st["fall"]) / A:.2f} A, from {f("top")} (= mean + {(np.mean(st["top"]) - mu) / sd:.1f} sd) to {f("after")}, ending {f("lag")} generations before the death')
print(f'  highest population in the last 16 generations: {f("maxpop")} = {np.mean(st["maxpop"]) / A:.2f} A;  generations spent below a third of the mean before the death: {f("gens_below_third")}')
print(f'  second largest one-generation fall: {f("second")} cells = {np.mean(st["second"]) / A:.2f} A, {f("gap")} generations away from the largest; deaths with two falls >= 0.15 A at least 2 generations apart: {f("two")}')
allp = np.array([p for rows in reps.values() for p in rows])
print('  mean population by generations before the death (1..12): ' + ' '.join(f'{x:.1f}' for x in allp.mean(0)[:12]))
print('ROW | ' + ' | '.join([str(A), str(n), f("half"), f("p4"), f'{np.mean(st["fall"]) / A:.2f} A', f'mean + {(np.mean(st["top"]) - mu) / sd:.1f} sd = {np.mean(st["top"]) / A:.2f} A', f'{np.mean(st["after"]) / A:.2f} A', f("lag")]) + ' |')
