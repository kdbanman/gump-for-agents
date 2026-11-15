"""README section 13 (a wire against chaos), re-run with an independent stepper, other seeds, densities, block
lengths.  Wire on a long RING (no caps needed; probes far from the wrap), inside the wide tube 1-a <= x+y+z,
x-y+z <= 5+a (a = 8: the study's 11 x 11), closed by T2.

    python3 chaos_check.py WIRE SOUP RHO W NRUN [seed0] [L=400] [T=400]

WIRE: C or B (unit cells at an even generation, period 2).  SOUP: all (every block cell random, the wire inside
included) or outside (the wire's own 3x3 tube inside the block kept as the wire).  Block: the cells of the wide tube
with -4W <= x+y-z - S0, x-y-z - S0 <= 0 (the study's shape), placed at the middle of the ring.
Probes at 40 and 80 units beyond the block's ends on both sides.  For each side: arrival time at the near and the
far probe (first difference from the bare wire); whether the far probe is ever bare again for >= 6 generations
after its first difference and before it stays non-bare ("something clean ahead"); whether the far probe is bare at
the end (T).
"""
import sys
import numpy as np
import gs

a = 8
inside = lambda p, L: 1 - a <= p[0] + p[1] + p[2] <= 5 + a and 1 - a <= p[0] - p[1] + p[2] <= 5 + a and 0 <= gs.unit(p) < L
UNITS = {'C': [(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)], 'B': [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]}


def build(L):
    cells = gs.closure([(1, 0, 2), (0, 1, 2), (0, 0, 3)], lambda p: inside(p, L))
    D = gs.Dom(cells, lambda p: gs.tr(p, -(gs.unit(p) // L) * L))
    D.u = np.array([gs.unit(c) for c in D.cells])
    C = np.array(D.cells)
    D.s1 = C @ (1, 1, 1); D.s2 = C @ (1, -1, 1); D.s3 = C @ (1, 1, -1); D.s4 = C @ (1, -1, -1)
    D.intube = (D.s1 >= 1) & (D.s1 <= 5) & (D.s2 >= 1) & (D.s2 <= 5)
    return D


def main():
    wire, soup, rho, W, nrun = sys.argv[1], sys.argv[2], float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    seed0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1000
    L = int(sys.argv[7]) if len(sys.argv) > 7 else 400; T = int(sys.argv[8]) if len(sys.argv) > 8 else 400
    D = build(L)
    base = D.state([gs.tr(c, k) for c in UNITS[wire] for k in range(L)])
    assert (D.run(base, 2) == base).all() and not (D.run(base, 1) == base).all()
    # block: s3, s4 in [S0 - 4W, S0], S0 chosen so the block sits around unit L/2 (s3 ~ 4u on the wire)
    S0 = 4 * (L // 2) + 3
    blk = (D.s3 <= S0) & (D.s3 >= S0 - 4 * W) & (D.s4 <= S0) & (D.s4 >= S0 - 4 * W)
    bu = D.u[blk & D.intube]; ulo, uhi = int(bu.min()), int(bu.max())
    probes = {'-v near': ulo - 40, '-v far': ulo - 80, '+v near': uhi + 40, '+v far': uhi + 80}
    pidx = {k: np.nonzero(D.u == u)[0] for k, u in probes.items()}
    rng = np.random.default_rng(seed0)
    R = np.zeros((nrun, D.n + 1), np.uint8)
    for r in range(nrun):
        x = base.copy(); rnd = (rng.random(D.n) < rho).astype(np.uint8)
        sel = blk & ~D.intube if soup == 'outside' else blk
        x[:D.n][sel] = rnd[sel]
        R[r] = x
    bases = [base, D.step(base)]
    hist = {k: np.zeros((nrun, T + 1), bool) for k in probes}     # True = differs from the bare wire
    X = R.copy()
    for t in range(T + 1):
        bt = bases[t % 2]
        for k, ix in pidx.items():
            hist[k][:, t] = (X[:, ix] != bt[ix]).any(1)
        X = D.step(X)
    print(f'wire {wire}, soup {soup}, rho {rho}, block W={W} ({int(blk.sum())} cells, wire units {ulo}..{uhi}), ring {L}, T={T}, seeds from {seed0}: {nrun} runs')
    from collections import Counter
    for side in ('-v', '+v'):
        sp = Counter(); clean = 0; reached = 0; bare_end = 0
        for r in range(nrun):
            hn, hf = hist[side + ' near'][r], hist[side + ' far'][r]
            if not hf.any():
                continue
            reached += 1
            tn = int(np.argmax(hn)); tf = int(np.argmax(hf))
            sp[(tf - tn) / 40] += 1
            # last time the far probe is bare
            nb = np.nonzero(~hf)[0]; last_bare = int(nb.max()) if len(nb) else -1
            bare_end += last_bare == T
            # bare again for >= 6 generations between first difference and the time it stays non-bare
            run = 0; best = 0
            for t in range(tf, (last_bare + 1) if last_bare < T else T + 1):
                run = run + 1 if not hf[t] else 0; best = max(best, run)
            clean += best >= 6 and last_bare < T
        print(f'  {side} side: front reached the far probe in {reached}/{nrun}; generations per unit near->far {dict(sp)}; '
              f'far probe bare at the end {bare_end}; something clean ahead of the front {clean}')


if __name__ == '__main__':
    main()
