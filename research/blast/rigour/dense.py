#!/usr/bin/env python3
"""Independent dense check of qsd.c for small faces (A <= 12): builds the full 2^A x 2^A kernel of the one-layer
dice surrogate by enumerating every cell's coins, then gets the killed chain's dominant eigenvalue
(A <= 10: all eigenvalues by numpy.linalg.eigvals, which also gives the second one; A = 11, 12: power iteration).

    python3 dense.py graphfile rho1 rho2
"""
import sys, itertools
import numpy as np


def read(fn):
    tok = open(fn).read().split()
    A = int(tok[0]); p = 1; nb = []; m = []
    for i in range(A):
        m1, m2, d = int(tok[p]), int(tok[p + 1]), int(tok[p + 2]); p += 3
        nb.append([int(t) for t in tok[p:p + d]]); p += d; m.append((m1, m2))
    return A, nb, m


def kernel(A, nb, m, r1, r2):
    N = 1 << A
    P = np.ones((N, N))
    xs = np.arange(N)
    bit = [(xs >> i) & 1 for i in range(A)]
    for i in range(A):
        k = sum(bit[j] for j in nb[i])                # with multiplicity
        a = np.zeros(N)
        for coins in itertools.product((0, 1), repeat=m[i][0] + m[i][1]):
            w = 1.0
            for t, c in enumerate(coins):
                r = r1 if t < m[i][0] else r2
                w *= r if c else 1 - r
            n = k + sum(coins)
            alive = np.where(bit[i] == 1, (n >= 3) & (n <= 5), (n == 4) | (n == 5))
            a += w * alive
        P *= np.where(bit[i][None, :] == 1, a[:, None], 1 - a[:, None])
    return P


if __name__ == '__main__':
    A, nb, m = read(sys.argv[1])
    r1, r2 = float(sys.argv[2]), float(sys.argv[3])
    P = kernel(A, nb, m, r1, r2)
    assert np.allclose(P.sum(1), 1)
    Q = P[1:, 1:]
    if A <= 10:
        ev = np.linalg.eigvals(Q)
        ev = ev[np.argsort(-abs(ev))]
        lam = ev[0].real
        print('A %d  h = 1 - lambda = %.13e  lntau %.12f  |lambda2/lambda1| %.6f' % (A, 1 - lam, -np.log(1 - lam), abs(ev[1]) / lam))
    else:
        v = np.ones(Q.shape[0]) / Q.shape[0]
        for it in range(3000):
            w = v @ Q; z = w.sum(); v = w / z
        print('A %d  h = 1 - lambda = %.13e  lntau %.12f' % (A, 1 - z, -np.log(1 - z)))
