#!/usr/bin/env python3
"""The share of face deaths that contain a one-generation fall of at least half the face (the test asked by the PI).
   python3 research/blast/rim/bust.py RINGFILE GRAPH [...]      (pairs; files written by rim.c -r)
For each death (life age > 400) of a single face f: its population P at lags 0..13 before the death generation;
falls F_l = P(l+1) - P(l), l = 0..11 (the twelve one-generation steps that end at the death). Reported: the share
with max F >= A/2, >= 0.4 A, the median of max F, the mean of the largest P in the window, and the stationary mean
P (from the 'Q' lines: replica 0 every 4096 generations)."""
import sys, numpy as np


def faces_of(graph):
    g = np.fromfile(graph, np.int32); n = g[0]; q = 1 + 12 * n; nf = g[q]; q += 1; sz = []
    for _ in range(nf): sz.append(int(g[q])); q += 1 + sz[-1]
    return sz


def analyse(ring, graph):
    sz = faces_of(graph); off = np.concatenate([[0], np.cumsum(sz)]); nf = len(sz)
    mx, big, st = [], [], []
    for line in open(ring):
        p = line.split()
        if p[0] == 'Q':
            b = np.frombuffer(p[1].encode() if len(p) > 1 else line[1:].strip().encode(), np.uint8) - 48
            st.append([b[off[f]:off[f + 1]].sum() for f in range(nf)]); continue
        mask = int(p[1]); fs = [f for f in range(nf) if (mask >> f) & 1]
        if len(fs) != 1 or len(p) < 3 + 13: continue
        f = fs[0]
        P = np.array([(np.frombuffer(x.encode(), np.uint8)[off[f]:off[f + 1]] - 48).sum() for x in p[3:]])
        F = P[1:13] - P[:12]; mx.append(F.max()); big.append(P.max())
    A = sz[0]; mx = np.array(mx); big = np.array(big); st = np.array(st, float)
    n = len(mx); h = (mx >= A / 2).mean(); h4 = (mx >= 0.4 * A).mean()
    return dict(A=A, deaths=n, half=h, err=np.sqrt(h * (1 - h) / n), s40=h4, med=float(np.median(mx)), peak=float(big.mean()),
                stat=float(st.mean()) if len(st) else float('nan'), sizes=sz)


if __name__ == '__main__':
    a = sys.argv[1:]
    print('ring file                              A  deaths  share(fall >= A/2)  share(>= 0.4A)  median fall  mean peak P  stationary P')
    for ring, graph in zip(a[::2], a[1::2]):
        r = analyse(ring, graph)
        print(f"{ring.split('/')[-1]:36s} {r['A']:3d} {r['deaths']:7d}  {r['half']:.4f} +- {r['err']:.4f}   {r['s40']:.4f}        {r['med']:5.1f}        {r['peak']:5.1f}       {r['stat']:5.1f}")
