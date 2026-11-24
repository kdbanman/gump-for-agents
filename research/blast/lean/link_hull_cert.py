#!/usr/bin/env python3
"""Writes mathlib/GumpMath/LinkHullCert.lean: a Lemma 0 certificate for `hull R` (`certOK`, LinkHull.lean),
checked there by the kernel (`decide +kernel`), for the R given on the command line.

    python3 research/blast/lean/link_hull_cert.py TABLES R...    (TABLES: the output of the #eval dump below)

The tables (cell coordinates, Face.nb, m1, m2 for each cell) come from `#eval` of the dice agent's definitions:
    def dump (R : ℕ) : String := let F := Gump.Dice.hull R
      toString ((List.range F.A).map fun i => ([(F.cell i).x, (F.cell i).y, (F.cell i).z], F.nb i, F.m1 i, F.m2 i))
Nothing computed here is trusted: the kernel re-checks every step against `Face.nb`, `Face.m1`, `Face.m2`.

The certificate: u = every cell whose normal is not z (every cell can be alive next from it); c0 a non-corner
x-cell; a walk of single cells from every cell to c0; and a growth path from {c0} to u (grow inside the x- and
y-cells, then light the two z-cells next to the x- and y-corners, then u).
"""
import ast, os, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'


def rule(s, n):
    return (3 <= n <= 5) if s else n in (4, 5)


def load(path):
    T = {}
    for line in open(path):
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        r, rest = line.split(' ', 1)
        T[int(r)] = ast.literal_eval(rest.replace('(', '[').replace(')', ']'))
    return T


class Face:
    def __init__(self, rows):
        self.cell = [r[0] for r in rows]
        self.nb = [r[1][0] for r in rows]
        self.m1 = [r[1][1][0] for r in rows]
        self.m2 = [r[1][1][1] for r in rows]
        self.A = len(rows)

    def k(self, x, i):
        return sum(1 for j in self.nb[i] if (x >> j) & 1)

    def alive(self, x, i):
        s = bool((x >> i) & 1)
        k = self.k(x, i)
        return any(rule(s, k + j + l) for j in range(self.m1[i] + 1) for l in range(self.m2[i] + 1))

    def step(self, x, y):
        return 0 < y < 2 ** self.A and all(self.alive(x, i) for i in range(self.A) if (y >> i) & 1)

    def M(self, x):
        return sum(1 << i for i in range(self.A) if self.alive(x, i))


def axis(p):
    return 0 if p[0] % 2 else (1 if p[1] % 2 else 2)


def cert(F):
    A = F.A
    u = sum(1 << i for i in range(A) if axis(F.cell[i]) != 2)
    assert all(F.alive(u, i) for i in range(A)), 'u'
    corner = [len(F.nb[i]) == 2 for i in range(A)]
    xy = [i for i in range(A) if axis(F.cell[i]) != 2 and not corner[i]]
    c0 = next(i for i in xy if axis(F.cell[i]) == 0)
    # walks of single cells to c0 (BFS backwards over {a} -> {b})
    succ = {a: [b for b in range(A) if F.step(1 << a, 1 << b)] for a in range(A)}
    pred = {b: [] for b in range(A)}
    for a in range(A):
        for b in succ[a]:
            pred[b].append(a)
    nxt = {c0: None}
    q = deque([c0])
    while q:
        b = q.popleft()
        for a in pred[b]:
            if a not in nxt:
                nxt[a] = b
                q.append(a)
    assert len(nxt) == A, 'walks'
    walks = []
    for i in range(A):
        w, a = [], i
        while a != c0:
            a = nxt[a]
            w.append(1 << a)
        walks.append(w)
    # growth from {c0}: inside the non-corner x- and y-cells, then the z-cells next to the corners, then u
    T = sum(1 << i for i in xy)
    s, path = 1 << c0, []
    while s != T:
        s2 = F.M(s) & T
        assert s2 != s and F.step(s, s2), 'growth'
        path.append(s2); s = s2
    zs = 0
    for i in range(A):
        if corner[i] and axis(F.cell[i]) != 2:
            zs |= sum(1 << j for j in F.nb[i] if axis(F.cell[j]) == 2)
    if not F.step(s, u):
        s2 = s | zs
        assert F.step(s, s2), 'z'
        path.append(s2); s = s2
    assert F.step(s, u), 'last'
    path.append(u)
    return u, c0, path, walks


def lean(R, F):
    u, c0, path, walks = cert(F)
    w = ', '.join('[' + ', '.join(map(str, x)) + ']' for x in walks)
    return (f"/-- The certificate for `hull {R}` ({F.A} cells): u, c0, growth path, walks. -/\n"
            f"theorem hull{R}_lemma0 : Lemma0F (Gump.Dice.hull {R}) :=\n"
            f"  lemma0_of_cert _ {u} {c0} [{', '.join(map(str, path))}]\n    [{w}] (by decide +kernel)\n")


def main():
    T = load(sys.argv[1])
    Rs = [int(r) for r in sys.argv[2:]]
    body = '\n'.join(lean(R, Face(T[R])) for R in Rs)
    s = f"""/-
`Lemma0F (hull R)` checked by the kernel from a certificate (`certOK`, `lemma0_of_cert`), hence `hull_full_all R`,
for R = {', '.join(map(str, Rs))}. Written by `link_hull_cert.py` (the certificate is data; the kernel checks every step).
-/
import GumpMath.LinkHull

namespace Gump.Link

{body}
end Gump.Link
"""
    open(OUT + 'LinkHullCert.lean', 'w').write(s)
    for R in Rs:
        F = Face(T[R]); u, c0, path, walks = cert(F)
        print(R, 'A', F.A, 'path', len(path), 'max walk', max(len(x) for x in walks))


main()
