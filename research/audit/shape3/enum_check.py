#!/usr/bin/env python3
"""Claim 2 of the review of research/shape3, by an enumeration that shares nothing with enum3.py / lattice.py.

For every index n <= 28: all sublattices of the triangular lattice Z^2 (form Q = x^2 + xy + y^2) of index n, by
Hermite normal form (a, k), (0, b); the reduced Gram matrix (Q1, 2B, Q2) from brute-force shortest vectors; the orbit
under the 12 integer matrices preserving Q (the in-plane point group of the slab, found here by search over small
integer matrices); then
  (i)   det = Q1 Q2 - B^2 = 0.75 n^2 for every lattice;
  (ii)  the partition of the HNFs into point-group orbits equals the partition by reduced Gram matrix;
  (iii) the equal-area, equal-shortest-loop groups (two or more orbits with the same Q1), listed for Q1 = 9 and Q1 >= 12;
  (iv)  for the pairs of research/shape3, Q1, Q2 and which member has the longer second loop.

    python3 research/audit/shape3/enum_check.py
"""
import itertools
from fractions import Fraction


def Q(v):
    return v[0] * v[0] + v[0] * v[1] + v[1] * v[1]


def Bf(u, v):  # bilinear form of Q: B(u, v) = (Q(u+v) - Q(u) - Q(v)) / 2
    return Fraction(Q((u[0] + v[0], u[1] + v[1])) - Q(u) - Q(v), 2)


def point_group():
    G = []
    for m in itertools.product(range(-1, 2), repeat=4):
        M = ((m[0], m[1]), (m[2], m[3]))
        if M[0][0] * M[1][1] - M[0][1] * M[1][0] not in (1, -1):
            continue
        img = lambda v: (M[0][0] * v[0] + M[0][1] * v[1], M[1][0] * v[0] + M[1][1] * v[1])
        if all(Q(img(v)) == Q(v) for v in [(1, 0), (0, 1), (1, 1), (1, -1), (2, 1)]):
            G.append(M)
    assert len(G) == 12, len(G)
    return G


def hnfs(n):
    for a in range(1, n + 1):
        if n % a == 0:
            b = n // a
            for k in range(b):
                yield (a, k, b)


def member(v, L):
    a, k, b = L
    x, y = v
    return x % a == 0 and (y - (x // a) * k) % b == 0


def short_vectors(L, R):
    out = []
    for x in range(-R, R + 1):
        for y in range(-R, R + 1):
            if (x, y) != (0, 0) and member((x, y), L):
                out.append((x, y))
    return sorted(out, key=Q)


def gram(L, n):
    R = 2 * n + 2
    vs = short_vectors(L, R)
    u = vs[0]
    v = next(w for w in vs if u[0] * w[1] - u[1] * w[0] != 0)
    # reduce so that 0 <= 2B <= Q1 (u shortest, v shortest independent of u; then |2B| <= Q1 automatically)
    B2 = abs(2 * Bf(u, v))
    assert B2 <= Q(u) and Q(u) <= Q(v)
    assert abs(u[0] * v[1] - u[1] * v[0]) == n   # u, v is a basis
    return (Q(u), int(B2), Q(v))


def canon(L, G, n):
    a, k, b = L
    gens = [(a, k), (0, b)]
    imgs = []
    for M in G:
        gg = [(M[0][0] * x + M[0][1] * y, M[1][0] * x + M[1][1] * y) for x, y in gens]
        imgs.append(next(H for H in hnfs(n) if all(member(w, H) for w in gg)))
    return min(imgs)


def main():
    G = point_group()
    allgood = True
    groups = {}
    for n in range(1, 29):
        Ls = list(hnfs(n))
        gr = {L: gram(L, n) for L in Ls}
        for L, (q1, b2, q2) in gr.items():
            if Fraction(q1 * q2) - Fraction(b2, 2) ** 2 != Fraction(3, 4) * n * n:
                print('det fails', n, L); allgood = False
        orb = {L: canon(L, G, n) for L in Ls}
        part_o = sorted(sorted(L for L in Ls if orb[L] == o) for o in set(orb.values()))
        part_g = sorted(sorted(L for L in Ls if gr[L] == g) for g in set(gr.values()))
        same = part_o == part_g
        allgood &= same
        cls = {}
        for o in set(orb.values()):
            cls.setdefault(gr[o][0], []).append((gr[o], o))
        for q1, mem in cls.items():
            if len(mem) > 1 and (q1 == 9 or q1 >= 12):
                groups.setdefault(3 * n, []).append((q1, sorted(mem)))
        print(f'n {n:2d} A {3 * n:2d}: {len(Ls):3d} HNFs, {len(set(orb.values())):2d} orbits, {len(set(gr.values())):2d} Gram classes, '
              f'partitions equal: {same}')
    print('det = 0.75 n^2 and orbit partition = Gram partition for every n <= 28:', allgood)
    print('\nequal-area, equal-shortest-loop groups with Q1 = 9 or Q1 >= 12 (A <= 84):')
    for A in sorted(groups):
        for q1, mem in sorted(groups[A]):
            print(f'  A {A:2d} Q1 {q1:2d}: ' + ', '.join(f'{o} Gram {g}' for g, o in mem))
    print('\npairs of research/shape3 (each member: (Q1, 2B, Q2)):')
    for tag, X, Y in [('Q36', (1, 4, 12), (1, 3, 12)), ('Q45', (1, 5, 15), (1, 4, 15)), ('Q54', (3, 0, 6), (1, 5, 18)),
                      ('Q63', (1, 6, 21), (1, 7, 21)), ('P1', (2, 2, 8), (1, 6, 16)), ('P3', (1, 8, 20), (2, 2, 10)),
                      ('T01', (1, 6, 24), (2, 4, 12)), ('T12', (2, 4, 12), (1, 5, 24)), ('N72', (2, 2, 12), (1, 10, 24))]:
        n = X[0] * X[2]
        gx, gy = gram(X, n), gram(Y, n)
        print(f'  {tag}: X {X} {gx}  Y {Y} {gy}  equal Q1: {gx[0] == gy[0]}  Y has the longer second loop: {gy[2] > gx[2]}')


if __name__ == '__main__':
    main()
