#!/usr/bin/env python3
"""The one-layer model on the thin torus, solved exactly (no sampling).

Model: the face layer (3b cells) follows B45/S345; every cell of the two layers beneath is an independent coin
of density rho, redrawn every generation. A face cell has 6 neighbours in the face, 2 in the first coin layer
and 1 in the second. The coins of the first layer are shared: the three face cells X_{c+1}, Y_{c-1}, Z_c (a
"triple", one triangle of the kagome layer) share the three coins X_c, Y_c, Z_c of the layer beneath, pairwise,
and no coin is shared between triples (derived in `triples()` from thin.TAB, not typed in). So the kernel is a
product over the b triples, each triple's 8 outcomes depending on the states and in-face counts of its cells.

    python3 exact1.py b [rho16]       # quasi-stationary death rate, ln tau = -ln h, by power iteration

State index: sum over triples c of 8^c (x_X' + 2 x_Y' + 4 x_Z'), with X'_c = X_{c+1}, Y'_c = Y_{c-1}, Z'_c = Z_c.
The matrix is never stored: p'(y) = sum_x p(x) prod_c q_c(y_c | x) is contracted with einsum, over one state per
translation orbit (the kernel commutes with the b translations, and the iteration is started symmetric).
"""
import itertools, math, sys, time
import numpy as np
import thin


def triples(b):
    """cells of triple c as (orientation, site); checks the sharing structure of the coins on TAB"""
    T = [[(0, (c + 1) % b), (1, (c - 1) % b), (2, c)] for c in range(b)]
    # coins of layer 1 seen by each face cell
    def coins(o, s, dt):
        return {(o2, (s + dc) % b) for (d, o2, dc) in thin.TAB[o] if d == dt}
    for c in range(b):
        c1 = [coins(o, s, 1) for o, s in T[c]]
        assert all(len(x) == 2 for x in c1)
        assert c1[0] | c1[1] | c1[2] == {(0, c), (1, c), (2, c)}
        assert c1[1] & c1[2] == {(0, c)} and c1[0] & c1[2] == {(1, c)} and c1[0] & c1[1] == {(2, c)}
        assert all(len(coins(o, s, 2)) == 1 for o, s in T[c])
    return T


def triple_table(rho):
    """P3[sX, kX, sY, kY, sZ, kZ, outcome]: outcome = yX + 2 yY + 4 yZ; s = state, k = live in-face neighbours"""
    P = np.zeros((2, 7, 2, 7, 2, 7, 8))
    alive = lambda s, n: (n in (4, 5)) or (s == 1 and n == 3)
    for u, v, w, a, bb, cc in itertools.product((0, 1), repeat=6):   # shared coins X1, Y1, Z1; private coins
        pr = np.prod([rho if z else 1 - rho for z in (u, v, w, a, bb, cc)])
        for sX, kX, sY, kY, sZ, kZ in itertools.product((0, 1), range(7), (0, 1), range(7), (0, 1), range(7)):
            yX = alive(sX, kX + v + w + a)       # X_{c+1} sees coins Y_c, Z_c of layer 1
            yY = alive(sY, kY + u + w + bb)      # Y_{c-1} sees X_c, Z_c
            yZ = alive(sZ, kZ + u + v + cc)      # Z_c sees X_c, Y_c
            P[sX, kX, sY, kY, sZ, kZ, yX + 2 * yY + 4 * yZ] += pr
    return P


def setup(b):
    T = triples(b)
    pos = {cell: (c, j) for c in range(b) for j, cell in enumerate(T[c])}     # cell -> (triple, slot)
    n = 8 ** b
    idx = np.arange(n, dtype=np.int64)
    bit = lambda c, j: (idx >> (3 * c + j)) & 1
    # in-face neighbour counts of every cell, for every state
    S = np.zeros((b, 3, n), np.int8); K = np.zeros((b, 3, n), np.int8)
    for c in range(b):
        for j, (o, s) in enumerate(T[c]):
            S[c, j] = bit(c, j)
            for (dt, o2, dc) in thin.TAB[o]:
                if dt == 0:
                    c2, j2 = pos[(o2, (s + dc) % b)]
                    K[c, j] += bit(c2, j2)
    # translation by one site = cyclic shift of the triples
    rot = (idx >> 3) | ((idx & 7) << (3 * (b - 1)))
    return S, K, rot


def solve(b, rho, tol=1e-12, verbose=True):
    P3 = triple_table(rho)
    S, K, rot = setup(b)
    n = 8 ** b
    # orbit representatives (smallest index in the orbit) and orbit sizes
    orb = np.arange(n, dtype=np.int64); r = np.arange(n, dtype=np.int64)
    for _ in range(b - 1):
        r = rot[r]; orb = np.minimum(orb, r)
    reps = np.nonzero(orb == np.arange(n))[0]
    reps = reps[reps != 0]
    size = np.bincount(orb, minlength=n)[reps]
    Q = [P3[S[c, 0, reps], K[c, 0, reps], S[c, 1, reps], K[c, 1, reps], S[c, 2, reps], K[c, 2, reps]] for c in range(b)]
    letters = 'abcdefghij'[:b]
    spec = 'x,' + ','.join('x' + ch for ch in letters) + '->' + letters[::-1]   # last triple = most significant digit
    p = np.full(n, 1.0 / (n - 1)); p[0] = 0
    h_old = -1; t0 = time.time()
    chunk = max(1, (1 << 24) // n * 64)
    for it in range(2000):
        out = np.zeros(n)
        w = p[reps] * size
        for a in range(0, len(reps), chunk):
            sl = slice(a, a + chunk)
            out += np.einsum(spec, w[sl], *[q[sl] for q in Q], optimize=True).reshape(n)
        # symmetrise over translations (the sum over an orbit's members is the rotated sum over its representative)
        acc = out.copy(); r = np.arange(n, dtype=np.int64)
        for _ in range(b - 1):
            r = rot[r]; acc += out[r]
        out = acc / b
        h = out[0]; out[0] = 0; p = out / out.sum()
        if verbose and it % 10 == 0:
            print(f'  it {it} h = {h:.10f} ln tau = {-math.log(h):.6f}  ({time.time() - t0:.0f} s)', flush=True)
        if abs(h - h_old) < tol * h:
            break
        h_old = h
    return h, p


if __name__ == '__main__':
    b = int(sys.argv[1]); rho16 = int(sys.argv[2]) if len(sys.argv) > 2 else 26112
    h, p = solve(b, rho16 / 65536)
    idx = np.arange(8 ** b); pop = sum(((idx >> k) & 1) for k in range(3 * b))
    hist = np.bincount(pop, weights=p)
    print(f'b = {b} rho = {rho16}/65536: h = {h:.10f}, ln tau = {-math.log(h):.6f}, mean face population {np.dot(hist, np.arange(len(hist))):.4f}')
    print('P(n) for n = 1..:', ' '.join(f'{x:.5f}' for x in hist[1:]))
