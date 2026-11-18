#!/usr/bin/env python3
"""Part C: the 108-cell rows of the pull request (research/blast/noisy/data/runs/sub_R15_*), combined in several ways.

    python3 research/audit/blastnoisy/c108.py DIR        (DIR = .../research/blast/noisy/data/runs)

 - per eps: ln tau, error, the value without the largest replication, a tail index from the largest 5% (Hill);
 - the weighted mean as in the pull request, and its bootstrap: the weights are estimated from the same replications
   as the values, and a sample that met a large replication has both a lower ln tau and a larger error, so the
   weighted mean leans towards the samples that met none;
 - the pooled mean of all rates (one tau for the three eps, every replication the same weight);
 - the line in eps (weighted least squares) with a bootstrap interval of its intercept.
"""
import glob, math, os, sys
import numpy as np
D = sys.argv[1]; G = (23.3392, 0.0099)
rng = np.random.default_rng(7)
data = {}
for M, eps in ((128, 1 / 16), (64, 1 / 32), (32, 1 / 64)):
    r = []
    for f in sorted(glob.glob(os.path.join(D, f'sub_R15_M{M}_s*.txt'))):
        r += [float(l.split(' rate ')[1].split()[0]) for l in open(f) if l.startswith('REP')]
    data[eps] = np.array(r)


def est(r):
    m = r.mean(); return -math.log(m), r.std(ddof=1) / m / math.sqrt(len(r))


def wmean(vals):
    w = np.array([1 / e ** 2 for _, e in vals]); v = np.array([x for x, _ in vals])
    return (w * v).sum() / w.sum(), 1 / math.sqrt(w.sum())


def line(eps, vals):
    w = np.array([1 / e ** 2 for _, e in vals]); v = np.array([x for x, _ in vals]); x = np.array(eps)
    S, Sx, Sy, Sxx, Sxy = w.sum(), (w * x).sum(), (w * v).sum(), (w * x * x).sum(), (w * x * v).sum()
    d = S * Sxx - Sx * Sx
    return (Sxx * Sy - Sx * Sxy) / d, math.sqrt(Sxx / d), (S * Sxy - Sx * Sy) / d, math.sqrt(S / d)


eps = sorted(data, reverse=True)
vals = [est(data[e]) for e in eps]
for e, (v, s) in zip(eps, vals):
    r = data[e]; x = np.sort(r / r.mean())[::-1]; k = max(10, len(r) // 20)
    hill = 1 / np.mean(np.log(x[:k] / x[k]))
    r1 = np.sort(r)[:-1]
    print(f'eps 1/{round(1 / e)}: {len(r)} replications, ln tau {v:.4f} +- {s:.4f} (minus gump {v - G[0]:+.4f} +- {math.hypot(s, G[1]):.4f}); '
          f'without the largest replication {-math.log(r1.mean()):.4f}; median of ln tau_k {np.median(-np.log(r)):.3f}; '
          f'tail index of rate / mean from the largest {k}: {hill:.2f}')
wm = wmean(vals); ln = line(eps, vals)
print(f'weighted mean (as the pull request): {wm[0]:.4f} +- {wm[1]:.4f}, minus gump {wm[0] - G[0]:+.4f} +- {math.hypot(wm[1], G[1]):.4f}')
print(f'line in eps: intercept {ln[0]:.4f} +- {ln[1]:.4f} (minus gump {ln[0] - G[0]:+.4f}), slope {ln[2]:+.2f} +- {ln[3]:.2f}')
allr = np.concatenate([data[e] for e in eps]); pv = est(allr)
print(f'pooled mean of all {len(allr)} rates: {pv[0]:.4f} +- {pv[1]:.4f}, minus gump {pv[0] - G[0]:+.4f} +- {math.hypot(pv[1], G[1]):.4f}')
# bootstrap: weights re-estimated in every resample (as the estimator does) against weights held at the sample's errors
bw, bf, bi, bp = [], [], [], []
for _ in range(20000):
    bv = [est(rng.choice(data[e], len(data[e]))) for e in eps]
    bw.append(wmean(bv)[0]); bf.append(wmean([(v, s0) for (v, _), (_, s0) in zip(bv, vals)])[0]); bi.append(line(eps, bv)[0])
    bp.append(-math.log(np.concatenate([rng.choice(data[e], len(data[e])) for e in eps]).mean()))
bw, bf, bi, bp = map(np.sort, map(np.array, (bw, bf, bi, bp)))
q = lambda a: f'[{a[500]:.3f}, {a[19499]:.3f}]'
print(f'bootstrap (20,000 resamples of the replications within each eps):')
print(f'  weighted mean, weights re-estimated: mean {bw.mean():.4f}, 95% {q(bw)}; weights held fixed: mean {bf.mean():.4f}, 95% {q(bf)}')
print(f'  -> re-estimating the weights moves the weighted mean by {bw.mean() - bf.mean():+.4f} on average (upwards = towards the samples without a large replication)')
print(f'  intercept of the line: mean {bi.mean():.4f}, 95% {q(bi)} (minus gump [{bi[500] - G[0]:+.3f}, {bi[19499] - G[0]:+.3f}])')
print(f'  pooled mean of all rates: 95% {q(bp)} (minus gump [{bp[500] - G[0]:+.3f}, {bp[19499] - G[0]:+.3f}])')
e16 = data[1 / 16]; b16 = np.sort([-math.log(rng.choice(e16, len(e16)).mean()) for _ in range(20000)])
print(f'  eps 1/16 alone: 95% {q(b16)} (minus gump [{b16[500] - G[0]:+.3f}, {b16[19499] - G[0]:+.3f}]); share of resamples at or below gump: {(b16 <= G[0]).mean():.4f}')
