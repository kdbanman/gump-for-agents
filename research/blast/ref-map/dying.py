#!/usr/bin/env python3
"""How gump's faces die, from the dumps of gs (GS_DUMP): the last 24 generations (P, B whole, B under) of every dying face.
  dying.py <dump> <tally of the same run> <A> <mode P> <over-full threshold P>"""
import sys, numpy as np
d = np.loadtxt(sys.argv[1], dtype=int); d = d.reshape(len(d), 24, 3); A, mode, thr = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
ph = np.zeros(128)
for line in open(sys.argv[2]):
    w = line.split()
    if w[0] == 'P': ph[int(w[1])] = float(w[2])
p_thr = ph[thr:].sum() / ph.sum()
P = d[:, :, 0]; n = len(d)
print(f"{sys.argv[1].split('/')[-1]}: {n} deaths; A={A}; living mode P={mode}; over-full means P >= {thr} (stationary frequency per generation {p_thr:.2e})")
print("  mean (P, B, B under) at t-12 .. t-1: " + ' '.join(f"({d[:, j, 0].mean():.1f},{d[:, j, 1].mean():.1f},{d[:, j, 2].mean():.1f})" for j in range(12, 24)))
for W in (6, 12, 20):
    f = (P[:, 24 - W:].max(1) >= thr).mean()
    print(f"  deaths with an over-full generation in the last {W}: {f:.3f} +- {np.sqrt(f*(1-f)/n):.3f}   (a living face: at most {min(1, W * p_thr):.3f})")
over = P >= thr; has = over[:, 12:].any(1); last = 23 - np.argmax(over[:, ::-1], 1)        # index of the last over-full generation
sel = has & (last >= 1) & (last <= 22) & (last >= 12)
if sel.sum() > 10:
    i = np.where(sel)[0]; j = last[sel]
    for off, name in ((-1, 'before'), (0, 'over-full'), (1, 'after')):
        print(f"    {name:9s}: mean (P,B,B under) = ({d[i, j+off, 0].mean():.1f}, {d[i, j+off, 1].mean():.1f}, {d[i, j+off, 2].mean():.1f})")
    m = 24 - j; print(f"    generations from the last over-full generation to the empty face: median {np.median(m):.0f} (10%-90%: {np.percentile(m,10):.0f}-{np.percentile(m,90):.0f})")
ab = P >= mode; hasm = ab.any(1); lastm = 23 - np.argmax(ab[:, ::-1], 1); L = 24 - lastm[hasm]
print(f"  generations from the last time at or above the living mode to the empty face: median {np.median(L):.0f} (10%-90%: {np.percentile(L,10):.0f}-{np.percentile(L,90):.0f}); never in 24: {1-hasm.mean():.3f}")
nf = ~(P[:, 4:].max(1) >= thr)
print(f"  deaths with no over-full generation in the last 20: {nf.mean():.3f}; their mean P at t-12..t-1: " + ' '.join(f"{P[nf, j].mean():.1f}" for j in range(12, 24)))
