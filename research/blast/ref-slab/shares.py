#!/usr/bin/env python3
"""Referee's recount of the 'boom and bust' shares from dying paths (own script; convention of split-slab's table:
the largest one-generation fall of the face population among the 16 generations before the death generation,
i.e. falls p(-k-1) -> p(-k), k = 1..15).

    python3 shares.py A brute PATHFILE                 # independent natural deaths (dice.c brute): binomial error
    python3 shares.py A sub PATHFILE:SUBFILE [...]     # subset-sampler paths; SUBFILE gives each replication's rate

For sampler paths: per replication the share s_i among its dying chains; quoted (1) the plain mean over
replications +- its standard error (split-slab's convention) and (2) the RATE-WEIGHTED mean sum r_i s_i / sum r_i
(the consistent estimate of the share among natural deaths: a replication stands for r_i of the death rate),
with a bootstrap error over replications.
"""
import sys, math
import numpy as np
A = int(sys.argv[1]); mode = sys.argv[2]


def falls(p):
    P = np.array(p)[:, :16]; d = P[:, 1:] - P[:, :-1]
    big = d.max(1); k = d.argmax(1)
    return big, P[np.arange(len(P)), k + 1], P[np.arange(len(P)), k], k + 1


def read(fn):
    reps = {}
    for line in open(fn):
        if line[0] != 'S':
            continue
        a, b = line.split('|'); p = list(map(int, b.split()))
        if len(p) >= 16:
            reps.setdefault(int(a.split()[1]), []).append(p[:16])
    return reps


if mode == 'brute':
    rows = read(sys.argv[3])[0]; big, top, aft, lag = falls(rows); n = len(big)
    h = (2 * big >= A).mean(); q = (big >= 0.4 * A).mean()
    print(f'{sys.argv[3]}: A = {A}, {n} natural deaths: fall >= A/2: {h:.4f} +- {math.sqrt(h * (1 - h) / n):.4f}; >= 0.4 A: {q:.4f} +- {math.sqrt(q * (1 - q) / n):.4f}; '
          f'largest fall {big.mean() / A:.3f} A, from {top.mean() / A:.3f} A to {aft.mean() / A:.3f} A, {lag.mean():.2f} generations before the death')
else:
    S = []; Q = []; Wt = []; F = []; T = []; L = []
    for arg in sys.argv[3:]:
        pf, sf = arg.split(':')
        rate = {}
        for line in open(sf):
            t = line.split()
            if line.startswith('REP') and 'rate' in t:
                rate[int(t[1])] = float(t[t.index('rate') + 1])
        for r, rows in sorted(read(pf).items()):
            big, top, aft, lag = falls(rows)
            S.append((2 * big >= A).mean()); Q.append((big >= 0.4 * A).mean()); Wt.append(rate[r]); F.append(big.mean() / A); T.append(top.mean() / A); L.append(lag.mean())
    S, Q, Wt, F, T, L = map(np.array, (S, Q, Wt, F, T, L)); n = len(S)
    rs = np.random.RandomState(2); ix = rs.randint(0, n, (20000, n))
    def wm(x):
        return (Wt * x).sum() / Wt.sum(), ((Wt[ix] * x[ix]).sum(1) / Wt[ix].sum(1)).std()
    print(f'A = {A}, {n} replications: fall >= A/2: plain {S.mean():.3f} +- {S.std(ddof=1) / math.sqrt(n):.3f}, rate-weighted {wm(S)[0]:.3f} +- {wm(S)[1]:.3f} | '
          f'>= 0.4 A: plain {Q.mean():.3f} +- {Q.std(ddof=1) / math.sqrt(n):.3f}, rate-weighted {wm(Q)[0]:.3f} +- {wm(Q)[1]:.3f} | largest fall {F.mean():.3f} A (weighted {wm(F)[0]:.3f}), from {T.mean():.3f} A (weighted {wm(T)[0]:.3f}), lag {L.mean():.2f} (weighted {wm(L)[0]:.2f}) | '
          f'per-replication shares range {S.min():.2f}..{S.max():.2f}, effective replications by rate weight {Wt.sum() ** 2 / (Wt ** 2).sum():.1f}; correlation of ln rate with the share {np.corrcoef(np.log(Wt), S)[0, 1]:+.2f} (n = {n})')
