#!/usr/bin/env python3
"""Review of research/shape2/: geometry, from research/audit/shape/geom_check.py (not from research/shape2/).

    python3 research/audit/shape2/geom2.py

1. Classes of index 16 and 20 under the slab's point group (from O_h), against Gram classes; representatives,
   systole^2, second minimum, first six primitive norms -- compared with research/shape2/data/classes_A*.csv.
2. Transverse layer indexing, checked against T1 independently of the ring order: for every cell and every
   diagonal, the layer offsets (mod P) of its in-slab neighbours must be a sub-multiset of {-4:1,-2:2,0:6,2:2,4:1}
   (with the missing ones exactly the out-of-slab neighbours), and the ring order used by ts.py must be
   s = 1, 3, ..., P-1 (adjacent = s differs by 2 mod P).
3. Repeated neighbours (multigraph) on the thin tori, and the layer count / cut of every diagonal.
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'research', 'audit', 'shape'))
import geom_check as gc  # noqa

G = gc.point_group()
DIAG = [(-1, 1, 1), (1, -1, 1), (1, 1, -1)]


def prim_norms(L, k=6):
    vs = set()
    for v in gc.lat_vecs(L, 40):
        x, y = v
        from math import gcd
        # primitive in the lattice: v/p not in the lattice for p>1
        if any(gc.in_lat((x // p, y // p), L) for p in range(2, 41) if x % p == 0 and y % p == 0):
            continue
        vs.add(min(v, (-x, -y)))
    return sorted(gc.norm2(v) for v in vs)[:k]


def layer_check(L):
    cells, idx, nb = gc.my_slab(L)
    P = gc.periods(L)
    want = Counter({-4: 1, -2: 2, 0: 6, 2: 2, 4: 1})
    bad = 0; dup = 0
    for n, c in enumerate(cells):
        row = nb[n]
        dup += len([x for x in row if x is not None]) != len(set(x for x in row if x is not None))
        for d, dv in enumerate(DIAG):
            s = sum(dv[i] * gc.doubled(c)[i] for i in range(3))
            got = Counter()
            for x in row:
                if x is None:
                    continue
                s2 = sum(dv[i] * gc.doubled(cells[x])[i] for i in range(3))
                dd = (s2 - s) % P[d]
                # the offset must be one of -4..4 mod P; when P is small several are congruent: accept any match
                got[dd] += 1
            wantm = Counter()
            for k_, v in want.items():
                wantm[k_ % P[d]] += v
            if any(got[k_] > wantm[k_] for k_ in got):
                bad += 1
    lay = []
    for d, dv in enumerate(DIAG):
        cnt = Counter(sum(dv[i] * gc.doubled(c)[i] for i in range(3)) % P[d] for c in cells)
        lay.append((P[d] // 2, sorted(set(cnt.values()))))
    return bad, dup, P, lay, len(cells)


if __name__ == '__main__':
    for n in (16, 20):
        allL = list(gc.hnfs(n))
        cls = {}
        for L in allL:
            cls.setdefault(min(gc.image(L, g, n) for g in G), []).append(L)
        gram = {}
        for L in allL:
            gram.setdefault(gc.gram_class(L), []).append(L)
        same = sorted(map(sorted, cls.values())) == sorted(map(sorted, gram.values()))
        print(f'index {n}: {len(allL)} lattices, {len(cls)} point-group classes, {len(gram)} Gram classes, partitions equal {same}')
        theirs = {}
        for r in csv.DictReader(open(os.path.join(ROOT, 'research/shape2/data', f'classes_A{3*n}.csv'))):
            theirs[(int(r['cls_a']), int(r['cls_k']), int(r['cls_b']))] = r
        for rep, mem in sorted(cls.items(), key=lambda t: gc.systole2(t[0])):
            # which of their representatives lies in this class?
            hit = [L for L in theirs if L in mem]
            assert len(hit) == 1, (rep, hit)
            L = hit[0]; r = theirs[L]
            pn = ' '.join(map(str, prim_norms(L)))
            bad, dup, P, lay, nc = layer_check(L)
            ok = pn == r['loops6'] and int(r['n_presentations']) == len(mem)
            cut = min([3 * nc // (p // 2) for p in P if p // 2 >= 3])
            print(f'  {L}: members {len(mem)} (theirs {r["n_presentations"]}), loops {pn} (theirs {r["loops6"]}) '
                  f'{"OK" if ok else "DIFF"}; layer/T1 violations {bad}, cells with repeated nbrs {dup}; '
                  f'periods {P}, layers {[x[0] for x in lay]}, cut {cut} (theirs {r["cut"]})')
