#!/usr/bin/env python3
"""Are the replications of one run (one persistent ensemble of 512 lanes) as independent as replications of
different runs?  Per run: ln tau from its mean rate, mean of ln(rate), and (if a path file is given) the plain
share of deaths with a one-generation fall >= A/2; then chi-square of the run means about the pooled mean.

    python3 runs.py A SUBFILE[:PATHFILE] ...
"""
import sys, math
import numpy as np
A = int(sys.argv[1]); rows = []
for arg in sys.argv[2:]:
    sf, pf = (arg.split(':') + [None])[:2]
    r = [float(t[t.index('rate') + 1]) for t in (l.split() for l in open(sf)) if t and t[0] == 'REP' and 'rate' in t]
    sh = None
    if pf:
        reps = {}
        for line in open(pf):
            if line[0] == 'S':
                a, b = line.split('|'); p = list(map(int, b.split()))
                if len(p) >= 16:
                    reps.setdefault(int(a.split()[1]), []).append(p[:16])
        sh = []
        for k, v in sorted(reps.items()):
            P = np.array(v); d = P[:, 1:] - P[:, :-1]; sh.append((2 * d.max(1) >= A).mean())
        sh = np.array(sh)
    r = np.array(r); lr = np.log(r)
    rows.append((sf.split('/')[-1], len(r), -math.log(r.mean()), r.std(ddof=1) / math.sqrt(len(r)) / r.mean(), -lr.mean(), lr.std(ddof=1) / math.sqrt(len(r)), sh))
    print(f'{rows[-1][0]}: n = {len(r)}, ln tau (mean rate) {rows[-1][2]:.3f} +- {rows[-1][3]:.3f}, -mean ln rate {rows[-1][4]:.3f} +- {rows[-1][5]:.3f}'
          + (f', share fall >= A/2: {sh.mean():.3f} +- {sh.std(ddof=1) / math.sqrt(len(sh)):.3f}' if sh is not None else ''))
def chi(vals, errs):
    vals, errs = np.array(vals), np.array(errs); w = 1 / errs ** 2; m = (w * vals).sum() / w.sum()
    return ((vals - m) ** 2 * w).sum(), len(vals) - 1
c, k = chi([x[4] for x in rows], [x[5] for x in rows]); print(f'between runs, mean ln rate: chi2 = {c:.1f} on {k}')
s = [x for x in rows if x[6] is not None]
if len(s) > 1:
    c, k = chi([x[6].mean() for x in s], [x[6].std(ddof=1) / math.sqrt(len(x[6])) for x in s]); print(f'between runs, share: chi2 = {c:.1f} on {k}')
