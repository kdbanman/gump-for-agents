#!/usr/bin/env python3
"""What follows an over-full generation in a living face, wrapped against rimmed (research/blast/anatomy).

    python3 overfull.py        # uses the records of t63 and h63, lags 40..127 before a death (a living face)

For every recorded generation with P >= level: the population one generation later, and (hull) the share of live
cells that survive that generation, by position.
"""
import json, os, sys
import numpy as np
import deaths as D
for vessel, run in (('slab_1_4_21', 't63'), ('hull_11', 'h63')):
    meta = json.load(open(os.path.join(D.SCR, vessel + '.json')))
    na = len(meta['faces'][0]); hd, S, U = D.load_rec(run, na, len(meta['under'][0]))
    P = S.sum(2).astype(int)
    print(f'== {run}')
    for level in (40, 42, 44, 46, 48):
        d, j = np.where(P[:, 41:128] >= level); j = j + 41
        nxt = P[d, j - 1]
        print(f'   P >= {level}: {len(d):6d} generations; one generation later: mean P {nxt.mean():5.1f}, 10-90% {np.percentile(nxt, 10):.0f}-{np.percentile(nxt, 90):.0f}; '
              f'share with P <= 15: {(nxt <= 15).mean():.4f} +- {np.sqrt((nxt <= 15).mean() * (1 - (nxt <= 15).mean()) / len(d)):.4f}; share with P <= {na // 2 - 16}: {(nxt <= na // 2 - 16).mean():.4f}')
    if meta['kind'] == 'hull':
        d, j = np.where(P[:, 41:128] >= 44); j = j + 41
        surv = {}; 
        for f in range(len(meta['faces'])):
            k = hd[d, 1] == f
            if not k.any(): continue
            now = S[d[k], j[k]].astype(bool); nx = S[d[k], j[k] - 1].astype(bool)
            for i, mp in enumerate(meta['mapped'][f]):
                key = 'corner' if sorted(mp)[1] == 0 else ('next to corner' if tuple(sorted(mp)) == (0, 1, 10) else ('rim line' if min(mp) == 0 else f'depth {min(mp)}'))
                a = surv.setdefault(key, [0, 0, 0, 0]); a[0] += now[:, i].sum(); a[1] += (now[:, i] & nx[:, i]).sum(); a[2] += len(now); a[3] += nx[:, i].sum()
        for key, a in surv.items():
            print(f'   after P >= 44 on the hull face, {key:15s}: occupied {a[0] / a[2]:.3f} of the time at that generation; of those alive, {a[1] / max(a[0], 1):.3f} survive it; occupancy one generation later {a[3] / a[2]:.3f}')
