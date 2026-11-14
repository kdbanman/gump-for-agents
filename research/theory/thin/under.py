#!/usr/bin/env python3
"""What lies beneath the face, from a dump of the deterministic slab (README section 4).

    python3 under.py [b] [generations]      # default 48 5000; 8 lanes, the first 300 generations dropped

Prints (1) the density by layer; (2) the density by layer beneath a gap of the face (>= L empty sites), by position
in the gap; (3) the same at the gap's middle some generations earlier; (4) the law of the number m of live cells
among the three beneath a face cell (two one layer down, one two layers down), given the cell's state and its
number k of live face neighbours, against binomial(3, interior density).
"""
import math, os, sys
import numpy as np
import run as R, thin


def main(b=48, gens=5000, m=8, seed=77):
    R.build()
    dp = os.path.join(R.OUT, f'dump_under_{os.getpid()}.txt'); out = os.path.join(R.OUT, f'vout_under_{os.getpid()}.txt')
    R.ring('det', b, m, seed, gens, 0, out, extra=('-d', dp))
    D = R.read_dump(dp, b, m)[300:]            # [g, lane, cells]
    os.remove(dp); os.remove(out)
    G, NLn, _ = D.shape
    S = D.reshape(G, NLn, m, 3, b)             # layer t, orientation (X, Y, Z), site c
    site = S[:, :, :, 2, :] + S[:, :, :, 1, :] + np.roll(S[:, :, :, 0, :], -1, axis=-1)     # live cells of site s = {Z_s, Y_s, X_{s+1}}
    dens = site.mean((0, 1, 3)) / 3
    print(f'b = {b}, {G} generations x {NLn} lanes (lives restart from a soup after a death; the first 300 generations dropped)')
    print('(1) density by layer:', ' '.join(f'{x:.4f}' for x in dens))
    face = site[:, :, 0, :]; emp = face == 0

    def runs(L):
        r = emp.copy()
        for j in range(1, L):
            r &= np.roll(emp, -j, axis=-1)
        return r                                # r[g, l, s]: sites s .. s+L-1 of face 0 are empty
    print('(2) density by layer beneath sites s .. s+L-1 all empty on the face, at site s + offset')
    for L in (4, 8, 12):
        r = runs(L)
        print(f'    L = {L} ({int(r.sum())} cases)')
        for off in (-2, 0, L // 2, L - 1, L + 1):
            print(f'      offset {off:3d}: ' + ' '.join(f'{np.roll(site[:, :, t, :], -off, axis=-1)[r].mean() / 3:.3f}' for t in range(m)))
    r = runs(8)
    print('(3) density by layer at the middle of a gap of 8 sites, some generations before it is seen')
    for lag in (0, 2, 4, 8, 16, 32):
        print(f'      {lag:2d} earlier: ' + ' '.join(f'{np.roll(site[:G - lag, :, t, :], -4, axis=-1)[r[lag:]].mean() / 3:.3f}' for t in range(m)))
    nb = thin.graph(b, m)
    fcells = np.arange(3 * b)
    inface = np.array([[j for j, (dt, _, _) in zip(nb[i], thin.TAB[i // b]) if dt == 0] for i in fcells])
    below = np.array([[j for j, (dt, _, _) in zip(nb[i], thin.TAB[i // b]) if dt > 0] for i in fcells])
    X = D.reshape(G * NLn, -1)
    k = X[:, inface].sum(-1); mm = X[:, below].sum(-1); st = X[:, fcells]
    rho = float(dens[2:6].mean())
    print(f'(4) P(m | state, k) for the three cells beneath a face cell; binomial(3, {rho:.4f}) = ' +
          ' '.join(f'{math.comb(3, j) * rho ** j * (1 - rho) ** (3 - j):.4f}' for j in range(4)))
    for s_ in (0, 1):
        for kk in range(7):
            sel = (st == s_) & (k == kk); n = int(sel.sum())
            if n < 1000:
                continue
            h = np.bincount(mm[sel], minlength=4) / n
            print(f'      {"alive" if s_ else "dead "} k = {kk} ({n:9d} cases): ' + ' '.join(f'{x:.4f}' for x in h) + f'   mean {mm[sel].mean():.3f}')


if __name__ == '__main__':
    main(*(int(x) for x in sys.argv[1:3]))
