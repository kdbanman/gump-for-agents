"""Reachability certificates for Lemma 0 on a face of the dice surrogate (chain agent, link).

  python3 research/blast/lean/link_reach.py DiceHull3 ...   (prints u, the number of living states, max distance)

From the dice agent's tables G, C in GumpMath/<Dice face>Data.lean: M(x) = cells alive-able from x (some coin
outcome puts k + heads in B45/S345's window); u = a state with M(u) = all cells; nxt, dist by backward BFS on
x -> y iff y nonempty and y subset of M(x).  Writes nothing; imported by link_gen_faces.py."""
import re, sys, ast
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
D = os.environ.get('LINK_OUT', os.path.join(HERE, 'mathlib', 'GumpMath')) + '/'
SRC = os.path.join(HERE, 'mathlib', 'GumpMath') + '/'
def tables(name):
    s = open(SRC + name + 'Data.lean').read()
    G = ast.literal_eval(re.search(r'def G : List \(List ℕ\) := (\[.*?\])\n', s).group(1))
    C = ast.literal_eval(re.search(r'def C : List \(ℕ × ℕ\) := (\[.*?\])\n', s).group(1).replace('(', '[').replace(')', ']'))
    return G, C
def rule(s, n): return (3 <= n <= 5) if s else (n in (4, 5))
def alive(G, C, x, i):
    k = sum(1 for j in G[i] if (x >> j) & 1)
    s = (x >> i) & 1 == 1
    return any(rule(s, k + j + l) for j in range(C[i][0] + 1) for l in range(C[i][1] + 1))
def cert(name):
    G, C = tables(name); A = len(G); N = 1 << A
    M = [sum(1 << i for i in range(A) if alive(G, C, x, i)) for x in range(N)]
    us = [u for u in range(1, N) if M[u] == N - 1]
    if not us: return name, None
    u = us[0]
    # backward BFS: x -> y possible iff y nonzero, y subset of M[x]
    dist = {u: 0}; nxt = {}; frontier = [u]; d = 0
    surv = [x for x in range(1, N) if M[x] != 0]
    while frontier:
        d += 1; new = []
        for x in surv:
            if x in dist: continue
            for y in frontier:
                if y & ~M[x] == 0:
                    dist[x] = d; nxt[x] = y; new.append(x); break
        frontier = new
    missing = [x for x in surv if x not in dist]
    return name, dict(A=A, u=u, maxdist=d - 1, nsurv=len(surv), missing=len(missing), dies=[x for x in range(1, N) if M[x] == 0],
                      nxt=[nxt.get(x, 0) for x in range(N)], dist=[dist.get(x, 0) for x in range(N)], G=G, C=C)
if __name__ == '__main__':
    for nm in sys.argv[1:]:
        n, r = cert(nm)
        if r is None: print(n, 'no u'); continue
        print(n, 'A', r['A'], 'u', r['u'], bin(r['u']), 'maxdist', r['maxdist'], 'surviving', r['nsurv'], 'missing', r['missing'], 'die surely', r['dies'][:5])
