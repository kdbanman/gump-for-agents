#!/usr/bin/env python3
"""ref-chain (fourth review): `Lemma0F` (LinkHull.lean) by its definition, on my oracle-built faces.

  OMP_NUM_THREADS=1 python3 research/blast/ref-chain/lemma0f_check.py      (about 1 min)

aliveF x i: some coin outcome puts k + heads in B45/S345's window; stepF x y: every live cell of y is aliveF from x;
Lemma0F: some living u with every cell aliveF from u, reached through stepF transitions between living states from
every living x with some aliveF cell.
1. Brute force over all states (hull 1, hull 3; also torus (1,0),(0,3), strip 1x3, patch 1x3): Lemma0F holds, and
   the QSD with lambda > 0 is unique (one class).
2. A face where the QSD is not unique: two cells of one layer too far apart to be neighbours, three coins each.
   Lemma0F fails, and there are two QSDs with lambda > 0 (point masses on {0} and {1}).
3. The certificates of LinkHullCert.lean (R = 3..13), re-checked with my own aliveF/stepF on my oracle-built tables.
4. hull R for even R has no cells; the cell counts for odd R.
5. Prices on hull 3 along LinkHullCert's rotation and reflection (c_{pi i} = c_i), and the six-element group's orbits.
"""
import os, sys, re, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from link_numbers import face, tables, alive_prob
from oracle import BIRTH, SURVIVE

def rule(s, n): return (n in SURVIVE) if s else (n in BIRTH)

class F:
    def __init__(self, nb, m1, m2): self.nb, self.m1, self.m2, self.A = nb, m1, m2, len(nb)
    def k(self, x, i): return sum((x >> j) & 1 for j in self.nb[i])
    def alive(self, x, i):
        return any(rule((x >> i) & 1, self.k(x, i) + j + l) for j in range(self.m1[i] + 1) for l in range(self.m2[i] + 1))
    def M(self, x): return sum(1 << i for i in range(self.A) if self.alive(x, i))
    def step(self, x, y): return y & ~self.M(x) == 0

def lemma0f_brute(Fc):
    N = 1 << Fc.A
    M = [Fc.M(x) for x in range(N)]
    us = [u for u in range(1, N) if M[u] == N - 1]
    # backward reachability to u over living states: x -> y iff y != 0, y subset of M(x)
    for u in us:
        reach = {u}; changed = True
        while changed:
            changed = False
            for x in range(1, N):
                if x not in reach and any((y & ~M[x]) == 0 for y in reach):
                    reach.add(x); changed = True
        if all(x in reach for x in range(1, N) if M[x] != 0):
            return True, u
    return False, (us[0] if us else None)

def qsd_count(nb, m1, m2, r1=11/25, r2=21/50):
    A = len(nb); n = 1 << A
    X = ((np.arange(n)[:, None] >> np.arange(A)[None, :]) & 1)
    a = np.zeros((n, A))
    for i in range(A):
        k = X[:, nb[i]].sum(1) if nb[i] else np.zeros(n, int)
        tab = np.array([[alive_prob(m1[i], m2[i], kk, s) for kk in range(7)] for s in (0, 1)])
        a[:, i] = tab[X[:, i], k]
    P = np.ones((n, 1))
    for i in reversed(range(A)):
        P = (P[:, :, None] * np.stack([1 - a[:, i], a[:, i]], axis=1)[:, None, :]).reshape(n, -1)
    Q = P[1:, 1:]
    w, V = np.linalg.eig(Q.T)
    top = np.abs(w).max()
    mult = int(np.sum(np.abs(w - top) < 1e-9))
    return top, mult, Q

print("1. brute force")
for name, kind, args in (('hull 1', 'hull', (1,)), ('hull 3', 'hull', (3,)), ('torus 1 0 3', 'torus', (1, 0, 3)),
                         ('strip 1 3', 'strip', (1, 3)), ('patch 1 3', 'patch', (1, 3))):
    cells, red, coin = face(kind, *args)
    nb, m1, m2 = tables(cells, red, coin)
    ok, u = lemma0f_brute(F(nb, m1, m2))
    top, mult, _ = qsd_count(nb, m1, m2)
    print(f"   {name}: Lemma0F {ok} (u = {u});  top eigenvalue {top:.12f} with multiplicity {mult}")

print("2. a face with two QSDs: cells (1,0,0) and (21,-10,-10) of the layer x+y+z = 1, no neighbours, coins (2,1)")
nb, m1, m2 = [[], []], [2, 2], [1, 1]
ok, u = lemma0f_brute(F(nb, m1, m2))
top, mult, Q = qsd_count(nb, m1, m2)
print(f"   Lemma0F {ok} (candidate u = {u});  Q = {Q.round(6).tolist()};  top eigenvalue {top:.6f} = rho1^2 rho2 "
      f"= {(11/25)**2 * 21/50:.6f}, multiplicity {mult}: delta_(0) and delta_(1) are both QSDs with lambda > 0")

print("3. LinkHullCert certificates on my tables")
src = open(os.path.join(HERE, '..', 'lean', 'mathlib', 'GumpMath', 'LinkHullCert.lean')).read()
for m in re.finditer(r"theorem hull(\d+)_lemma0 : Lemma0F \(Gump\.Dice\.hull \d+\) :=\n  lemma0_of_cert _ (\d+) (\d+) (\[[^\]]*\])\n    (\[.*?\]) \(by decide \+kernel\)", src, re.S):
    R, u, c0 = int(m.group(1)), int(m.group(2)), int(m.group(3))
    common = eval(m.group(4)); walks = eval(m.group(5))
    cells, red, coin = face('hull', R)
    Fc = F(*tables(cells, red, coin))
    def path(a, l, b):
        for c in l:
            if not (0 < c < (1 << Fc.A) and Fc.step(a, c)): return False
            a = c
        return a == b
    ok = (0 < u < (1 << Fc.A) and all(Fc.alive(u, i) for i in range(Fc.A)) and path(1 << c0, common, u)
          and all(path(1 << i, walks[i] if i < len(walks) else [], 1 << c0) for i in range(Fc.A)))
    # negative control: drop the first step of the growth path
    neg = path(1 << c0, common[1:], u) if len(common) > 1 else None
    print(f"   hull {R} ({Fc.A} cells): certificate passes on my tables: {ok};  with the growth path's first step "
          f"removed: {neg}")
for m in re.finditer(r"theorem hull(\d+)_(rot|refl) : autOK \(Gump\.Dice\.hull \d+\) (\[[^\]]*\]) = true", src):
    R, kind, pi = int(m.group(1)), m.group(2), eval(m.group(3))
    cells, red, coin = face('hull', R)
    nb, m1, m2 = tables(cells, red, coin)
    ok = sorted(pi) == list(range(len(cells))) and all(
        sorted(pi[j] for j in nb[i]) == sorted(nb[pi[i]]) and m1[pi[i]] == m1[i] and m2[pi[i]] == m2[i] for i in range(len(cells)))
    # is it the geometric map? rotation (x,y,z) -> (y,z,x); reflection (x,y,z) -> (y,x,z)
    g = (lambda p: (p[1], p[2], p[0])) if kind == 'rot' else (lambda p: (p[1], p[0], p[2]))
    geo = all(cells[pi[i]] == g(cells[i]) for i in range(len(cells)))
    if R in (3, 13): print(f"   hull {R} {kind}: autOK on my tables {ok};  equals the map {('(y,z,x)' if kind == 'rot' else '(y,x,z)')}: {geo}")
    elif not (ok and geo): print(f"   hull {R} {kind}: autOK {ok}, geometric {geo}  <-- check")

print("4. cell counts:", {R: len(face('hull', R)[0]) for R in range(0, 16)})

print("5. prices on hull 3 along the rotation and reflection")
from link_numbers import analyse
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    c, lam, lt = analyse('hull 3', 'hull', (3,), [0] * 9, 207)
rot = [3, 5, 7, 8, 2, 6, 1, 4, 0]; refl = [0, 4, 6, 8, 1, 7, 2, 5, 3]
print(f"   max |c_(rot i) - c_i| = {max(abs(c[rot[i]] - c[i]) for i in range(9)):.1e}, "
      f"max |c_(refl i) - c_i| = {max(abs(c[refl[i]] - c[i]) for i in range(9)):.1e}")
G = {tuple(range(9))}
frontier = [tuple(range(9))]
while frontier:
    g = frontier.pop()
    for h in (rot, refl):
        gh = tuple(h[g[i]] for i in range(9))
        if gh not in G: G.add(gh); frontier.append(gh)
orbits = sorted({tuple(sorted({g[i] for g in G})) for i in range(9)})
print(f"   group generated: {len(G)} elements; orbits {orbits};  prices per orbit: "
      f"{[round(float(c[o[0]]), 10) for o in orbits]}")
