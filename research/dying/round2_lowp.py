#!/usr/bin/env python3
"""round2_lowp.py: added after round-2 B (not forecast). Is the clumping of a dying face's survivors specific to
dying? The same statistic S (round 2, B) for stationary null faces whose population is naturally low (P <= 0.7 P̄ and
<= 0.6 P̄), each against 20 stationary faces thinned to the same count.

    python3 research/dying/round2_lowp.py
"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import round2
rng = np.random.default_rng(3)
for g in ['c1', 'd2h']:
    z = np.load(f'{round2.R2}/canon_{g}.npz'); NUL = z['NUL']; canon = z['canon']
    xy = round2.proj(canon); rho = NUL.mean(0); c0 = (rho[:, None] * xy).sum(0) / rho.sum()
    S = lambda live: np.hypot(*(xy[live].mean(0) - c0))
    pop = NUL.sum(1); pb = pop.mean()
    for cut in (0.7, 0.6):
        sel = np.nonzero(pop <= cut * pb)[0]; sd = []; sn = []
        for i in sel:
            f = NUL[i]; k = f.sum(); sd.append(S(f)); cand = np.nonzero(pop >= k)[0]; s1 = []
            for _ in range(20):
                h = NUL[rng.choice(cand)]; live = np.nonzero(h)[0]; th = np.zeros(63, bool); th[rng.choice(live, k, replace=False)] = True; s1.append(S(th))
            sn.append(np.mean(s1))
        sd = np.array(sd); sn = np.array(sn)
        bs = [sd[j].mean() / sn[j].mean() for j in [rng.integers(0, len(sd), len(sd)) for _ in range(500)]]
        print(g, f'stationary faces with P <= {cut} Pbar: n {len(sel)}, mean k {pop[sel].mean():.1f}, S {sd.mean():.3f} vs thinned {sn.mean():.3f}, ratio {sd.mean() / sn.mean():.3f} ± {np.std(bs):.3f}')
