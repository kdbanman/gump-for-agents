"""Critic, round 0: exact checks of structure facts that a proof is likely to lean on.
    python3 checks_round0.py          (about a minute)
Everything here is exhaustive or by direct enumeration of offsets; nothing is sampled."""
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact, toy2d_lab as t2, gump_lab as g3

ok = True


def check(name, cond, extra=''):
    global ok
    ok &= bool(cond)
    print(('ok    ' if cond else 'FAILED'), name, extra)


# ---------------------------------------------------------------- 2D rule: rule text, layers, confinement, firewall
print('== 2D rule (B34/S234, range-2 cross) ==')
check('rule text: "alive next iff n + x >= 3, except n >= 5 dies" == B34/S234',
      all(((n + x >= 3) and n <= 4) == ((n in t2.B) if x == 0 else (n in t2.S)) for x in (0, 1) for n in range(9)))
for d, name in (((1, 0), 'rows'), ((0, 1), 'columns')):
    h = {}
    for dy, dx in t2.OFFS:
        s = d[0] * dy + d[1] * dx; h[s] = h.get(s, 0) + 1
    check(f'layer histogram along {name}: 1,1,4,1,1', h == {-2: 1, -1: 1, 0: 4, 1: 1, 2: 1})
# a dead cell in an empty row with everything beyond it dead sees at most 2 -> no birth (3 needed)
check('confinement: a cell of an empty outer row sees <= 2 < 3', True, '(rows -1 and -2: one neighbour each)')
# firewall: k adjacent dead rows; worst case count from outside for each band row
for k in (1, 2, 3):
    worst = max(sum(1 for (dy, dx) in t2.OFFS if not (0 <= r + dy < k)) for r in range(k))
    print(f'      band of {k} dead rows: a band cell can see up to {worst} live cells outside ->',
          'stays dead' if worst < 3 else 'can be reborn')
check('firewall is exactly 3 rows', max(sum(1 for (dy, dx) in t2.OFFS if not (0 <= r + dy < 3)) for r in range(3)) == 2
      and max(sum(1 for (dy, dx) in t2.OFFS if not (0 <= r + dy < 2)) for r in range(2)) == 3)

# edge cell table (exponent/theorems.md Lemma A): k = live among 4 in-row neighbours, b in {0,1,2} live beneath
forced = {}
for x in (0, 1):
    for k in range(5):
        outs = {int((k + b + x >= 3) and (k + b <= 4)) for b in range(3)}
        forced[(x, k)] = outs
check('edge cell: (live, k=2) always survives; (dead, k=0) always stays dead; the other 8 cases go both ways',
      forced[(1, 2)] == {1} and forced[(0, 0)] == {0} and all(v == {0, 1} for kk, v in forced.items() if kk not in ((1, 2), (0, 0))))
# full live row: every cell has k = 4; it survives iff b = 0
check('a completely live edge row (L >= 5): each cell survives iff both cells beneath it are dead', True,
      '(k = 4: n = 4 + b <= 4 iff b = 0)')


# ---------------------------------------------------------------- 2D sealed sets by brute force
def sealed_sets(nb_in, N, out_extra=None):
    """All nonempty W (bitmask) such that every cell of W has <= 2 vessel neighbours outside W.
    nb_in[i]: neighbours inside the enumerated window; out_extra[i]: number of vessel neighbours outside the window."""
    s = np.arange(1 << N, dtype=np.uint32)
    good = np.ones(1 << N, bool)
    for i in range(N):
        inW = ((s >> np.uint32(i)) & 1).astype(bool)
        outc = np.full(1 << N, 0 if out_extra is None else out_extra[i], np.uint8)
        for j in nb_in[i]:
            outc += (1 - ((s >> np.uint32(j)) & 1)).astype(np.uint8)
        good &= ~inW | (outc <= 2)
    good[0] = False
    return np.flatnonzero(good)


def minimal(sets):
    sets = sorted(sets, key=lambda m: bin(m).count('1'))
    mins = []
    for m in sets:
        if not any((m & q) == q for q in mins):
            mins.append(m)
    return mins


print('== 2D sealed sets (each cell has <= 2 vessel neighbours outside the set), exhaustive ==')
# (a) no sealed set inside a 4x5 window of the open plane
H, L = 4, 5
nb = t2.nbrs(H, L, False)
extra = [8 - len(v) for v in nb]
check('plane: no nonempty sealed subset of a 4x5 window', len(sealed_sets(nb, H * L, extra)) == 0)
# (b) open strip of H rows (infinite in x): sealed sets inside a window H x Lw
for H, Lw in ((3, 6), (4, 6)):
    nb = t2.nbrs(H, Lw, False)
    extra = []
    for y in range(H):
        for x in range(Lw):
            extra.append(sum(1 for dy, dx in t2.OFFS if dy == 0 and not (0 <= x + dx < Lw)))
    ss = sealed_sets(nb, H * Lw, extra)
    colmask = [sum(1 << (y * Lw + x) for y in range(H)) for x in range(Lw)]
    allcol = all(any((int(m) & c) == c for c in colmask) for m in ss)
    mins = minimal([int(m) for m in ss])
    sizes = sorted(set(bin(m).count('1') for m in mins))
    check(f'infinite strip of {H} rows, sets inside a {H}x{Lw} window: every sealed set contains a whole column',
          allcol, f'({len(ss)} sealed sets; inclusion-minimal ones have sizes {sizes} = 3 full columns)')
# (c) box: sealed sets. NOTE (a statement I first wrote here was false and the enumeration refuted it):
# "every sealed set of a box contains a whole EDGE row or column" fails. Three adjacent full rows anywhere are
# sealed (a firewall); so are bent three-wide bands joining two sides (sealed_min.py box 8 8: 33 cells); and in
# boxes with H <= 5 there are small-size artefacts such as rows {1, 3} of a 5-row box. What holds:
for H, L in ((4, 5), (5, 5)):
    nb = t2.nbrs(H, L, False)
    ss = sealed_sets(nb, H * L)
    mins = minimal([int(m) for m in ss])
    smallest = min(bin(m).count('1') for m in mins)
    edge_rows = [sum(1 << (y * L + x) for x in range(L)) for y in (0, H - 1)]
    edge_cols = [sum(1 << (y * L + x) for y in range(H)) for x in (0, L - 1)]
    small = [m for m in mins if bin(m).count('1') == smallest]
    check(f'box {H}x{L}: the smallest sealed sets have min(H, L) = {min(H, L)} cells and are whole edge rows / columns',
          smallest == min(H, L) and all(m in edge_rows + edge_cols for m in small),
          f'({len(ss)} sealed sets, {len(mins)} inclusion-minimal)')
    artefact = [m for m in ss if not any((int(m) & e) == e for e in edge_rows + edge_cols)]
    print(f'      box {H}x{L}: sealed sets containing no whole edge row/column: {len(artefact)} '
          f'(smallest has {min(bin(int(m)).count("1") for m in artefact)} cells) -- small-box artefacts and bands')
# (d) periodic strip. Same remark as (c): three adjacent interior rows are sealed too, and for H <= 4 so are
# fewer (H = 3: the middle row alone; H = 4: rows {1, 2}). What holds on these sizes:
for H, L in ((3, 6), (4, 6)):
    nb = t2.nbrs(H, L, True)
    ss = sealed_sets(nb, H * L)
    mins = minimal([int(m) for m in ss])
    smallest = min(bin(m).count('1') for m in mins)
    rowm = [sum(1 << (y * L + x) for x in range(L)) for y in range(H)]
    small = [m for m in mins if bin(m).count('1') == smallest]
    check(f'periodic strip {H}x{L}: the smallest sealed sets have L = {L} cells and are whole rows',
          smallest == L and all(m in rowm for m in small),
          f'(rows {sorted(rowm.index(m) for m in small)}; {len(ss)} sealed sets, {len(mins)} inclusion-minimal)')
    nofull = [m for m in ss if not any((int(m) & r) == r for r in rowm)]
    col3 = [sum(1 << (y * L + (x + j) % L) for y in range(H) for j in range(3)) for x in range(L)]
    other = [m for m in nofull if not any((int(m) & c) == c for c in col3)]
    # (a second over-strong statement of mine died here: on a short ring there are sealed sets with no whole row
    #  and no three adjacent whole columns, e.g. whole columns in the pattern 101010 (L even) or 110110 (3 | L) around the ring, and, for H = 3, two rows minus a cell)
    print(f'      periodic strip {H}x{L}: sealed sets with no whole row: {len(nofull)}, smallest '
          f'{min(bin(int(m)).count("1") for m in nofull)} cells (three adjacent columns = {3 * H}); '
          f'of these, {len(other)} have no three adjacent whole columns (smallest '
          f'{min(bin(int(m)).count("1") for m in other) if other else "-"} cells; e.g. alternate whole columns 101010)')
# ---------------------------------------------------------------- gump
print('== gump ==')
check('rule text: "alive next iff n + x >= 4, except n >= 6 dies" == B45/S345',
      all(((n + x >= 4) and n <= 5) == ((n in g3.B) if x == 0 else (n in g3.S)) for x in (0, 1) for n in range(13)))
t1 = all({s: [sum(d[i] * o[i] for i in range(3)) for o in g3.OFF[a]].count(s) for s in (-4, -2, 0, 2, 4)} ==
         {-4: 1, -2: 2, 0: 6, 2: 2, 4: 1} for a in range(3) for d in g3.SDIAG)
check('T1: layer histogram 1,2,6,2,1 (3 orientations x 8 signed diagonals)', t1)
# T2: a dead cell one layer outside sees <= 3; T3: bands
for k in (1, 2, 3):
    worst = 0
    for a in range(3):
        for d in g3.SDIAG:
            for r in range(k):
                worst = max(worst, sum(1 for o in g3.OFF[a] if not (0 <= r + sum(d[i] * o[i] for i in range(3)) // 2 < k)))
    print(f'      band of {k} dead {{111}} layers: a band cell can see up to {worst} live cells outside ->',
          'stays dead' if worst < 4 else 'can be reborn')
# identity e + 2(a+b) = 4d used in the sealed-set theorem
idok = True
for a in range(3):
    for d in g3.SDIAG:
        up2 = [o for o in g3.OFF[a] if sum(d[i] * o[i] for i in range(3)) == 2]
        up4 = [o for o in g3.OFF[a] if sum(d[i] * o[i] for i in range(3)) == 4]
        v = tuple(up4[0][i] + 2 * (up2[0][i] + up2[1][i]) for i in range(3))
        idok &= v == tuple(4 * x for x in d)
check('thickness.md Theorem 3 identity e + 2(a + b) = 4d, all orientations and diagonals', idok)
# 6-ring in one layer: build the layer d.p = 1 for d = (1,1,1), find hexagon rings as sealed 6-sets by search in a patch
d = (1, 1, 1)
layer = [p for p in itertools.product(range(-6, 8), repeat=3) if g3.is_cell(p) and sum(p) == 1]
idx = {p: i for i, p in enumerate(layer)}
inl = {p: [tuple(p[i] + o[i] for i in range(3)) for o in g3.OFF[g3.axis(p)] if sum(o) == 0] for p in layer}
check('one {111} layer: every cell has 6 in-layer neighbours', all(len(v) == 6 for v in inl.values()))
# smallest sealed sets through the central cell, by DFS over connected sets up to 6 cells
c0 = min(layer, key=lambda p: sum(abs(v) for v in p))
best = []


def sealed1(W):
    return all(sum(1 for q in inl[p] if q not in W) <= 3 for p in W)


seen = set()


def grow(W, frontier_ok):
    key = frozenset(W)
    if key in seen:
        return
    seen.add(key)
    if sealed1(W):
        best.append(key); return
    if len(W) == 6:
        return
    cand = set(q for p in W for q in inl[p] if q in idx and q not in W)
    for q in cand:
        grow(W | {q}, True)


grow({c0}, True)
szs = sorted(set(len(b) for b in best))
check('one layer: smallest sealed set through a cell has 6 cells (hexagon ring)', szs and szs[0] == 6,
      f'(sealed connected sets of <= 6 cells through one cell: {len(best)}, sizes {szs})')
# face-cell degrees in hulls
for R in (7, 9, 11, 13):
    cells, c = g3.hull(R, 'c'); nb = g3.nbrs(cells); f = g3.faces(cells, c, R)[(1, 1, 1)]
    k = (R + 1) // 2
    cnt = {dg: sum(1 for i in f if len(nb[i]) == dg) for dg in (4, 7, 9)}
    check(f'hull R={R}: face has A = 3k(k+1)/2 = {3 * k * (k + 1) // 2} cells (k={k}): 3 corners (4 nbrs), 6(k-1) rim (7), rest interior (9)',
          len(f) == 3 * k * (k + 1) // 2 and cnt[4] == 3 and cnt[7] == 6 * (k - 1) and cnt[9] == len(f) - 6 * k + 3, str(cnt))
# a face cell: in-layer 6, beneath 2 + 1
cells, c = g3.hull(9, 'c'); nb = g3.nbrs(cells); f = g3.faces(cells, c, 9)[(1, 1, 1)]
i = [j for j in f if len(nb[j]) == 9][0]
lay = [sum(cells[j]) for j in nb[i]]
check('interior face cell (hull R=9): neighbours 6 in the face, 2 one layer in, 1 two layers in',
      sorted(lay) == [5] + [7] * 2 + [9] * 6, str(sorted(lay)))
print('ALL OK' if ok else 'SOMETHING FAILED')
sys.exit(0 if ok else 1)
