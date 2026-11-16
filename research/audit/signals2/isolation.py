"""README section 13, "the isolation is exact": the coupling count recomputed, and the same question asked in a
second geometry (a wire running PAST a slab of soup, not ending at it).

    python3 isolation.py

(1) Cap geometry, as chaoswire.py cap: wire C ending in capL (objects/clock-C.json: capL + units 0..L-1 + capR),
    block = cells of the 11x11 tube with h3-4W <= x+y-z <= h3, h4-4W <= x-y-z <= h4, where h3, h4 lie G+1 layers
    below the least x+y-z, x-y-z of capL (G empty layers between).  For each phase of the wire:
      a = live wire cells with a neighbour in the block,
      b = cells outside the block, dead in the wire at that phase, with a block neighbour and
          (#block neighbours + #live wire neighbours) >= 4  (could be born),
      mx = the largest number of block neighbours of a cell outside the block (T2: <= 3).
    a = b = 0 at both phases is sufficient for exact isolation: by induction, the soup stays in its planes (an
    outside cell sees <= 3 block cells and, when b = 0, too few wire cells to reach 4), no block cell ever sees a
    live wire cell (a = 0), and every outside cell sees what it would see with the wire alone.
(2) Parallel geometry: a ring of wire C (repeat 1 unit), and a slab of soup on one side of it,
    x+y+z in [5 + 2(G+1), 5 + 2(G+1) + 10] (G empty layers 7, .., 5+2G between the wire's tube and the soup),
    x-y+z in [-7, 13], all units.  The same counts, then 20 soups of density 0.4 run for 600 generations: does the
    wire ever differ from the bare wire?
"""
import numpy as np
import gs, clockobj as K
S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
dot = lambda d, p: d[0] * p[0] + d[1] * p[1] + d[2] * p[2]
a = 8; W = 12


def counts(D, blk, wire_phases):
    blk1 = np.append(blk, False); out = []
    nbb = blk1[D.nb].sum(1)
    mx = int(nbb[~blk].max())
    for w in wire_phases:
        wl = w[:D.n].astype(bool); nbw = w[D.nb].sum(1)
        A = int((wl & (nbb > 0)).sum())
        Bc = int((~blk & ~wl & (nbb > 0) & (nbb + nbw >= 4)).sum())
        touch = int((~blk & (nbb > 0) & ((nbw > 0) | wl)).sum())
        out.append((A, Bc, touch))
    return mx, out


L = 60
wire = set(K.capL) | {gs.tr(c, k) for c in K.UNIT for k in range(L)} | {gs.tr(c, L) for c in K.capR}
print('(1) cap geometry (wire C ending in capL)')
for G in (0, 1, 2, 3):
    h3 = min(dot(S3, c) for c in K.capL) - 2 * (G + 1); h4 = min(dot(S4, c) for c in K.capL) - 2 * (G + 1)
    s3w = [dot(S3, c) for c in wire]; s4w = [dot(S4, c) for c in wire]
    ins = lambda p: (1 - a <= dot(S1, p) <= 5 + a and 1 - a <= dot(S2, p) <= 5 + a and h3 - 4 * W <= dot(S3, p) <= max(s3w)
                     and h4 - 4 * W <= dot(S4, p) <= max(s4w))
    D = gs.Dom(gs.closure(list(wire) + [(-2 * W, 0, 2 * W + 1)], ins))
    C = np.array(D.cells)
    blk = (C @ S3 <= h3) & (C @ S3 >= h3 - 4 * W) & (C @ S4 <= h4) & (C @ S4 >= h4 - 4 * W)
    w0 = D.state(wire); w1 = D.step(w0); assert (D.step(w1) == w0).all()
    mx, out = counts(D, blk, (w0, w1))
    print(f'   G={G}: block {int(blk.sum())} cells; max block neighbours of an outside cell {mx}; per phase '
          f'(live wire cells touching the block, outside cells that could be born, outside cells touching both) = {out}')
print('(2) parallel geometry (ring of wire C beside a slab of soup)')
Lr = 24
UC = K.UNIT
for G in (1, 2, 3):
    lo = 5 + 2 * (G + 1); hi = lo + 10
    ins = lambda p: 1 <= dot(S1, p) <= hi and 1 - a <= dot(S2, p) <= 5 + a and 0 <= gs.unit(p) < Lr
    D = gs.Dom(gs.closure([(1, 0, 2), (0, 1, 2)], ins), lambda p: gs.tr(p, -(gs.unit(p) // Lr) * Lr))
    C = np.array(D.cells)
    blk = (C @ S1 >= lo)
    w0 = D.state([gs.tr(c, k) for c in UC for k in range(Lr)]); w1 = D.step(w0); assert (D.step(w1) == w0).all()
    mx, out = counts(D, blk, (w0, w1))
    rng = np.random.default_rng(31 + G)
    X = np.repeat(w0[None], 20, 0); rnd = (rng.random((20, D.n)) < 0.4).astype(np.uint8)
    X[:, :D.n][:, blk] = rnd[:, blk]
    intube = ((C @ S1) <= 5) & ((C @ S2) >= 1) & ((C @ S2) <= 5) & ((C @ S1) >= 1)
    changed = np.zeros(20, bool); first = np.full(20, -1)
    for t in range(600):
        wt = (w0, w1)[t % 2]
        d = (X[:, :D.n][:, intube] != wt[:D.n][intube]).any(1)
        first[(first < 0) & d] = t; changed |= d
        X = D.step(X)
    print(f'   G={G}: max block neighbours of an outside cell {mx}; per phase (touching, could be born, touching both) = {out}; '
          f'wire changed in {int(changed.sum())}/20 soups (first change at {sorted(first[first >= 0].tolist())[:6]})')
