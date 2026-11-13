"""Critic's lab (an 'unassigned idea', see critic/journal.md): the one-generation emptying cost of the 2D edge
under a product measure. Edge cells i.i.d. Bernoulli(pe); the two cells beneath each edge cell i.i.d. Bernoulli(rho),
independent of everything. P(edge row of L cells, periodic, is empty one generation later) = trace(T^L), T a
transfer matrix on windows of four consecutive cells; cost per cell = -ln(largest eigenvalue).
Exact for the product measure; says nothing by itself about the automaton's own stationary state.
    python3 iid_flash.py [pe] [rho]"""
import sys, itertools
import numpy as np


def cost(pe, rho, L=None):
    pb = [(1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2]                 # P(b = 0, 1, 2)
    def dies(s, k):                                                      # probability that the cell is dead next
        if s:
            return sum(pb[b] for b in range(3) if not (2 <= k + b <= 4))
        return sum(pb[b] for b in range(3) if not (3 <= k + b <= 4))
    # window (a, b, c, d) = cells x-2, x-1, x, x+1 ; next window (b, c, d, e): weight of cell c given a, b, d, e
    idx = {w: i for i, w in enumerate(itertools.product((0, 1), repeat=4))}
    T = np.zeros((16, 16))
    for (a, b, c, d), i in idx.items():
        for e in (0, 1):
            k = a + b + d + e
            T[i, idx[(b, c, d, e)]] = (pe if c else 1 - pe) * dies(c, k)
    ev = np.linalg.eigvals(T)
    lam = max(ev.real)
    out = -np.log(lam)
    if L:
        return out, -np.log(np.trace(np.linalg.matrix_power(T, L)).real) / L
    return out


if __name__ == '__main__':
    pe = float(sys.argv[1]) if len(sys.argv) > 1 else 0.58
    rho = float(sys.argv[2]) if len(sys.argv) > 2 else 0.472
    print(f"pe={pe}, rho={rho}: cost per cell of emptying in one generation = {cost(pe, rho):.4f}")
    for p in (0.3, 0.4, 0.472, 0.5, 0.58, 0.7):
        print(f"  pe={p}: " + '  '.join(f"rho={r}: {cost(p, r):.4f}" for r in (0.3, 0.472, 0.6)))
    # brute-force check of the transfer matrix at L = 8
    L = 8; pe, rho = 0.58, 0.472
    pb = [(1 - rho) ** 2, 2 * rho * (1 - rho), rho ** 2]
    tot = 0.0
    for S in itertools.product((0, 1), repeat=L):
        w = 1.0
        for x in range(L):
            k = S[(x - 2) % L] + S[(x - 1) % L] + S[(x + 1) % L] + S[(x + 2) % L]
            if S[x]:
                w *= pe * sum(pb[b] for b in range(3) if not (2 <= k + b <= 4))
            else:
                w *= (1 - pe) * sum(pb[b] for b in range(3) if not (3 <= k + b <= 4))
        tot += w
    print("check L=8: brute force", -np.log(tot) / L, "transfer matrix", cost(pe, rho, L)[1])
