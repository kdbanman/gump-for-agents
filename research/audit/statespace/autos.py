#!/usr/bin/env python3
"""Full automorphism group of a vessel's neighbour (multi)graph, and the symmetry of ALL its champions.

  autos.py KIND ARGS...      reads research/scratch/audit_ss/NAME.champ (from run_one.sh)

An automorphism is a permutation s of the cells with A[s(i)][s(j)] = A[i][j] for the multiplicity matrix A; every
such permutation commutes with the dynamics (the rule is outer-totalistic), whether or not it comes from a lattice
symmetry. Search: colour refinement, then backtracking with adjacency checks against the cells already mapped.
"""
import sys
import numpy as np
sys.path.insert(0, '/home/user/gump-for-agents/research/audit/statespace')
import geom


def automorphisms(A):
    n = len(A)
    col = [0] * n
    while True:
        sig = [(col[i], tuple(sorted((col[j], A[i][j]) for j in range(n) if A[i][j])), A[i][i]) for i in range(n)]
        keys = sorted(set(sig)); new = [keys.index(s) for s in sig]
        if len(set(new)) == len(set(col)):
            col = new; break
        col = new
    order = sorted(range(n), key=lambda i: (sum(1 for j in range(n) if col[j] == col[i]), i))
    out = []
    mp = [-1] * n; used = [False] * n

    def rec(k):
        if k == n:
            out.append(tuple(mp)); return
        i = order[k]
        for c in range(n):
            if used[c] or col[c] != col[i] or A[c][c] != A[i][i]:
                continue
            if all(A[i][order[q]] == A[c][mp[order[q]]] and A[order[q]][i] == A[mp[order[q]]][c] for q in range(k)):
                mp[i] = c; used[c] = True
                rec(k + 1)
                mp[i] = -1; used[c] = False
    rec(0)
    return out


def main():
    kind, args = sys.argv[1], sys.argv[2:]
    v = geom.V(kind, args)
    n = v.n
    A = [[0] * n for _ in range(n)]
    for i, r in enumerate(v.nb):
        for j in r:
            if j >= 0:
                A[i][j] += 1
    G = automorphisms(A)
    name = kind + '_' + '_'.join(args)
    ch = [int(l.split()[0], 16) for l in open(f'/home/user/gump-for-agents/research/scratch/audit_ss/{name}.champ')]
    perm = lambda s, g: sum(1 << g[i] for i in range(n) if (s >> i) & 1)
    chs = set(ch)
    stab = [sum(1 for g in G if perm(s, g) == s) for s in ch]
    closed = all(perm(s, g) in chs for s in ch for g in G)
    orbits = len(set(min(perm(s, g) for g in G) for s in ch))
    print(f'{name}: |Aut(graph)| = {len(G)}; champions {len(ch)}; with nontrivial stabiliser '
          f'{sum(1 for x in stab if x > 1)}; orbits {orbits}; set closed under Aut: {closed}')


if __name__ == '__main__':
    main()
