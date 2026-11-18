#!/usr/bin/env python3
"""How long is the fatal dip?   python3 research/blast/ref-dicehull/paths.py
1. Brute force of the chain (rd.c mode win with PBAR SIGMA; files dur_R*_WD6.txt): for every death, generations since the face
   population was last above L = round(Pbar - k sigma), k = 2.5, 3.5, 4.5: mean, quantiles, share longer than 24 / 32 / 56.
2. The sampler's dying chains at R = 17 (hd_anc.c with FULLPATH=1; paths_R17_s*.txt): the same duration for LAM1 = 51, the
   generation of death, and the share of dying chains whose face was at or below LAM1 already at generation 1..8 of 56
   (their fatal dip was under way in the initial state: the sampler can only get such deaths from rare initial states)."""
import glob, os, re
import numpy as np
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'scratch', 'blast', 'ref-dicehull')
for f in sorted(glob.glob(os.path.join(S, 'dur_R*_WD6.txt'))):
    for line in open(f):
        if line.startswith('DUR'):
            w = line.split(); lev = int(w[3]); h = np.array([float(x) for x in w[5:]]); n = h.sum()
            if n == 0:
                continue
            d = np.arange(len(h)); cs = np.cumsum(h) / n; q = [int(np.searchsorted(cs, p)) for p in (0.5, 0.9, 0.99)]
            print(f'{os.path.basename(f)}: level {lev}: {int(n)} deaths; generations since last above it: mean {(h * d).sum() / n:.2f}, median {q[0]}, 90% {q[1]}, 99% {q[2]}, '
                  f'max {int(d[h > 0].max())}; share > 24: {h[25:].sum() / n:.4f}, > 32: {h[33:].sum() / n:.4f}, > 56: {h[57:].sum() / n:.5f}')
for f in sorted(glob.glob(os.path.join(S, 'paths_R17_s*.txt'))):
    LAM = 51; byrep = {}
    for line in open(f):
        if not line.startswith('S '):
            continue
        a, b = line.split('|'); w = a.split(); rep, gd = int(w[1]), int(w[3]); p = [int(x) for x in b.split()]   # p[0] = generation gd-1, ... p[-1] = generation 1
        dur = next((i + 1 for i, x in enumerate(p) if x > LAM), None)
        byrep.setdefault(rep, []).append((gd, dur, p[-1], min(p[-8:]) if len(p) >= 8 else min(p)))
    for rep, v in sorted(byrep.items()):
        gd = np.array([x[0] for x in v]); cens = np.array([x[1] is None for x in v]); dur = np.array([x[1] if x[1] else x[0] for x in v])
        early = np.array([x[3] <= LAM for x in v]); p1 = np.array([x[2] for x in v])
        print(f'{os.path.basename(f)} rep {rep}: {len(v)} dying chains; death at generation: median {np.median(gd):.0f}; generations since last above {LAM}: '
              f'median {np.median(dur):.0f}, 90% {np.percentile(dur, 90):.0f}, max {dur.max()}; never above {LAM} in the whole chain: {cens.mean():.3f}; '
              f'at or below {LAM} somewhere in generations 1-8: {early.mean():.3f}; population at generation 1: mean {p1.mean():.1f}, min {p1.min()}')
