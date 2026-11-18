#!/usr/bin/env python3
"""How a wrapped face dies, from natural deaths of plain gump (path files written by `ss GEOM lag SEED GENS PATHFILE`).

    python3 howdie.py H K D data/paths_H_K_D.txt

Path file: one line per face death,  P face age pop(-1) ... pop(-24) | last[0..A-1]
  pop(-k): population of the dying face k generations before the death generation (first generation it is empty);
  last[c]: last generation (relative to the death generation, -1..-63) at which face cell c was alive; -64 = not
  alive in the last 63 generations.  Cell c of a face = ((i' D + j') 3 + a): reduced in-plane cube index (i', j')
  (geom.py), a = normal axis; its cube is (i', j', l - i' - j') with l = 0 (face 0) or 7 (face 1).
"""
import math, sys
import numpy as np


def shortest(H, K, D, R=12):
    best = None
    for m in range(0, R + 1):
        for j in range(-R, R + 1):
            if m == 0 and j <= 0:
                continue
            x, y = m * H, m * K + j * D
            q = x * x + x * y + y * y
            if best is None or q < best[0]:
                best = (q, x, y)
    return best


def main():
    H, K, D = map(int, sys.argv[1:4])
    pops = []; last = []
    for line in open(sys.argv[4]):
        if line[0] != 'P':
            continue
        a, b = line.split('|'); t = a.split()
        pops.append(list(map(int, t[3:]))); last.append(list(map(int, b.split())))
    P = np.array(pops); L = np.array(last); N, A = L.shape; nl = P.shape[1]
    mu, sd = 0.5153 * A, math.sqrt(0.415 * A)
    print(f'torus ({H},{K}),(0,{D}), A = {A}: {N} natural deaths; stationary face population about {mu:.1f} +- {sd:.1f}')
    mx = P.max(1); lagmx = P.argmax(1) + 1
    print(f'  highest population in the last {nl} generations: median {np.median(mx):.0f} = {np.median(mx) / A:.2f} A = mean + {(np.median(mx) - mu) / sd:.1f} sd '
          f'(10%..90%: {np.percentile(mx, 10):.0f}..{np.percentile(mx, 90):.0f}); at lag (median) {np.median(lagmx):.0f}')
    d = P[:, 1:] - P[:, :-1]          # fall from lag k+1 to lag k
    big = d.max(1); bl = d.argmax(1) + 1
    before = P[np.arange(N), bl]; after = P[np.arange(N), bl - 1]
    print(f'  largest one-generation fall: median {np.median(big):.0f} cells (10%..90%: {np.percentile(big, 10):.0f}..{np.percentile(big, 90):.0f}), '
          f'from {np.median(before):.0f} (= mean + {(np.median(before) - mu) / sd:.1f} sd) to {np.median(after):.0f}; it ends {np.median(bl):.0f} generations before the death (10%..90%: {np.percentile(bl, 10):.0f}..{np.percentile(bl, 90):.0f})')
    print(f'  deaths whose largest fall starts above mean + 1.5 sd: {(before >= mu + 1.5 * sd).mean():.3f}; above mean + 2 sd: {(before >= mu + 2 * sd).mean():.3f}; above the mean: {(before >= mu).mean():.3f}')
    print(f'  deaths whose largest fall removes more than half of the mean population: {(big >= mu / 2).mean():.3f}; more than a third: {(big >= mu / 3).mean():.3f}')
    frac = []; spread = []
    for r in L:
        v, c = np.unique(r, return_counts=True); frac.append(c.max() / A); spread.append(r[r > -64].std())
    print(f'  share of the face cells last alive in one and the same generation: median {np.median(frac):.2f} (10%..90%: {np.percentile(frac, 10):.2f}..{np.percentile(frac, 90):.2f}); '
          f'sd of the cells\' last-alive generations within a death: median {np.median(spread):.2f}')
    # profile aligned on the crash: mean population at offsets around the generation before the largest fall
    prof = {}
    for i in range(N):
        for off in range(-6, 5):
            k = bl[i] - off          # lag index of generation (crash start + off)
            if 1 <= k <= nl:
                prof.setdefault(off, []).append(P[i, k - 1])
    print('  mean population at generations relative to the top of the largest fall (0 = last generation before it):')
    print('   ' + '  '.join(f'{off:+d}: {np.mean(prof[off]):.1f}' for off in sorted(prof)))
    # along the short loop's perpendicular (the tube axis): do segments die at the same time?
    q, vx, vy = shortest(H, K, D); n = H * D
    unit = (math.sqrt(3) / 2) / math.sqrt(q); length = n * unit
    nseg = max(2, int(round(length / 1.75)))
    seg = np.zeros(A, int)
    for c in range(A):
        ij = c // 3; i, j = ij // D, ij % D
        t = (vx * j - vy * i) % n
        seg[c] = min(nseg - 1, int(t * unit / length * nseg))
    rng = []; sds = []
    for r in L:
        med = [np.median(r[(seg == s)]) for s in range(nseg)]
        rng.append(max(med) - min(med)); sds.append(np.std(med))
    print(f'  shortest loop^2 {q}; face = {math.sqrt(q):.2f} x {length:.2f} lattice units; {nseg} segments along the axis perpendicular to the shortest loop:')
    print(f'   range of the segments\' median last-alive generation within a death: median {np.median(rng):.1f} generations (10%..90%: {np.percentile(rng, 10):.1f}..{np.percentile(rng, 90):.1f}); share of deaths with range <= 1: {(np.array(rng) <= 1).mean():.2f}, >= 4: {(np.array(rng) >= 4).mean():.2f}')


if __name__ == '__main__':
    main()
