#!/usr/bin/env python3
"""Pool the replications of dice.sh (subset simulation on the hull dice chain).

    python3 research/blast/split-hull/dice_ana.py

Per radius: every REP line of scratch dice/sub_R<R>_s*.txt; ln tau = -ln(mean rate), error = scatter of the
replications' rates / sqrt(K) (and a jackknife); the share of the mean carried by the largest replication; the
difference to gump's anchor.
"""
import glob, math, os, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', 'scratch', 'blast', 'split-hull', 'dice')
ANCHOR = {9: (9.819, 0.002), 11: (13.633, 0.001), 13: (18.141, 0.005), 15: (23.3392, 0.0099)}
byR = {}
for f in sorted(glob.glob(os.path.join(D, 'sub_R*_s*.txt'))):
    R = int(re.search(r'sub_R(\d+)_s', f).group(1))
    for line in open(f):
        if line.startswith('REP') and ' rate ' in line:
            byR.setdefault(R, []).append(float(line.split(' rate ')[1].split()[0]))
print('  R  cells  reps   ln tau (dice chain, sampler)   rel sd of one rep   largest rep / sum   anchor      sampler - anchor')
for R in sorted(byR):
    r = np.array(byR[R]); K = len(r); m = r.mean()
    est = -math.log(m); err = r.std(ddof=1) / math.sqrt(K) / m
    jk = np.array([-math.log((r.sum() - x) / (K - 1)) for x in r]); jerr = math.sqrt((K - 1) / K * ((jk - jk.mean()) ** 2).sum())
    A = {9: 45, 11: 63, 13: 84, 15: 108, 17: 135, 19: 165, 21: 198}[R]
    s = f'  {R:2d}  {A:4d}  {K:4d}   {est:.3f} +- {err:.3f} (jackknife {jerr:.3f})   {r.std(ddof=1) / m:.2f}   {r.max() / r.sum():.2f}'
    if R in ANCHOR:
        a, ae = ANCHOR[R]; e = math.hypot(err, ae)
        s += f'   {a}   {est - a:+.3f} +- {e:.3f} ({(est - a) / e:+.1f} sigma)'
    s += f'   zero-rate reps {int((r == 0).sum())}'
    print(s)
