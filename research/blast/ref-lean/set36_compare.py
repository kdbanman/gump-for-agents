#!/usr/bin/env python3
"""Referee: Lean's set36 against the set that research/theory/sealed.py's SAT search prints (thickness.md, Prop. 5).

    research/scratch/blast/ref-lean/venv/bin/python research/blast/ref-lean/set36_compare.py [FILE]

FILE (optional) holds the output of `sealed.py minsat 2 7 36`; without it, sealed.py's own encoding is solved once
at K = 36 (the iteration K = 1..35 before it is skipped, so the model can differ from the one minsat prints).
Both sets are put in a canonical form under the symmetries of the two-layer slab 1 <= s <= 3 along (1,1,1):
the six permutations of the coordinates, the inversion p -> (2,2,0) - p that swaps the layers, and the even
in-layer translations. Needs pysat (python-sat), installed in a private venv by the referee.
"""
import ast, itertools, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'research', 'theory'))
import falsify as F  # noqa: E402


def canon(S):
    best = None
    for perm in itertools.permutations(range(3)):
        for inv in (False, True):
            T = [tuple(p[i] for i in perm) for p in S]
            if inv:
                T = [(2 - x, 2 - y, -z) for x, y, z in T]
            for m in T:
                if F.dot((1, 1, 1), m) == 1 and F.axis(m) == 0:
                    t = F.sub((1, 0, 0), m)
                    U = tuple(sorted(F.add(p, t) for p in T))
                    if best is None or U < best:
                        best = U
    return best


def sealed_py_set(path=None):
    if path:
        txt = open(path).read()
        return [tuple(c) for c in ast.literal_eval(re.search(r': (\[\(.*?\)\])', txt).group(1))]
    import sealed as S
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Cadical153
    m, R, K = 2, 7, 36
    P = sorted(S.patch(m, R, 'hex')); pool = IDPool(); var = {c: pool.id(c) for c in P}
    base = []
    for c in P:
        ns = [q for q in S.nbrs(c) if 0 <= S.layer(q) < m]
        need = len(ns) - 3
        inside = [var[q] for q in ns if q in var]
        if need <= 0: continue
        if len(inside) < need: base.append([-var[c]]); continue
        enc = CardEnc.atleast(lits=inside, bound=need, vpool=pool, encoding=EncType.seqcounter)
        base += [cl + [-var[c]] for cl in enc.clauses]
    base.append([var[(1, 0, 0)]])
    enc = CardEnc.atmost(lits=[var[c] for c in P], bound=K, vpool=pool, encoding=EncType.seqcounter)
    with Cadical153(bootstrap_with=base + enc.clauses) as s:
        assert s.solve()
        mdl = set(l for l in s.get_model() if l > 0)
        return [c for c in P if var[c] in mdl]


if __name__ == '__main__':
    W = sealed_py_set(sys.argv[1] if len(sys.argv) > 1 else None)
    L = F.lean_set36()
    import sealed as S
    print(f'sealed.py set: {len(W)} cells, sealed (is_sealed m=2): {S.is_sealed(W, 2)}; Lean set36: {len(L)} cells, '
          f'sealed: {S.is_sealed(L, 2)}')
    print('the same set up to the slab\'s symmetries:', canon(W) == canon(L))
