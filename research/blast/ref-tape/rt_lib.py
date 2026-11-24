#!/usr/bin/env python3
"""ref-tape: the referee's own tools, written from reference/oracle.py and the catalogue's JSON files only.

Nothing from research/blast/lean/ (the tape agent's scripts) is imported or copied.

  orc_run(cells, T, shape=None)   reference/oracle.py's step, unchanged, on a rectangular array torus big enough that
                                  nothing wraps (the masks are oracle.masks' formula for the array's shape, the
                                  origin even); after every generation the four outermost planes on each side are
                                  asserted dead, so the run is the run of the infinite lattice.
  orc_ring(cells, T, L, hy)       the same step on the torus (2L, hy, 2L): a wire along (1,0,-1) of L units closes into
                                  a ring (unit u is moved by (2u, 0, -2u)); the run of a periodic infinite word.
  sstep / srun                    a sparse stepper on the infinite lattice (offsets from oracle.offsets); trusted only
                                  through rt_validate.py, which compares it with orc_run state for state.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'reference'))
import oracle  # noqa: E402

SIG = os.path.join(ROOT, 'research', 'signals')
OBJ = os.path.join(SIG, 'objects')


def load(path):
    return json.load(open(path))


tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)       # k units along v = (1,0,-1)
trs = lambda cells, k: frozenset(tr(c, k) for c in cells)
unit_of = lambda c: c[0] >> 1                                # floor(x/2)
add = lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def is_cell(c):
    return sum(v & 1 for v in c) == 1


def masks_shape(shape):
    par = np.indices(shape) % 2
    return [(par[a] == 1) & (par.sum(0) == 1) for a in range(3)]


def orc_run(cells, T, margin=12):
    """reference/oracle.step on a box = the bounding box of `cells` + `margin` on every side (the edge assertion
    below fails if that is not enough); returns T+1 frozensets."""
    cells = frozenset(cells)
    assert all(is_cell(c) for c in cells)
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]; zs = [c[2] for c in cells]
    lo = [min(v) for v in (xs, ys, zs)]; hi = [max(v) for v in (xs, ys, zs)]
    pad = margin
    org = [((l - pad) // 2) * 2 for l in lo]                 # even origin
    shape = tuple(h - o + pad + 1 + ((h - o + pad + 1) % 2) for h, o in zip(hi, org))
    M = masks_shape(shape)
    h = np.zeros(shape, np.int8)
    for c in cells:
        h[c[0] - org[0], c[1] - org[1], c[2] - org[2]] = 1
    out = [cells]
    for _ in range(T):
        h = oracle.step(h, M)
        for ax in range(3):
            sl = [slice(None)] * 3
            sl[ax] = list(range(4)) + list(range(shape[ax] - 4, shape[ax]))
            assert not h[tuple(sl)].any(), 'live cell near the box edge'
        idx = np.argwhere(h)
        out.append(frozenset((int(a) + org[0], int(b) + org[1], int(c) + org[2]) for a, b, c in idx))
    return out


def orc_ring(cells, T, L, hy=24, y0=-8):
    """reference/oracle.step on the torus (2L, hy, 2L); cells given in lattice coordinates (x, z taken mod 2L,
    y - y0 in [0, hy)). Returns T+1 frozensets of torus coordinates (x mod 2L, y, z mod 2L)."""
    shape = (2 * L, hy, 2 * L)
    M = masks_shape(shape)
    h = np.zeros(shape, np.int8)
    for c in cells:
        assert 2 <= c[1] - y0 < hy - 2
        h[c[0] % shape[0], c[1] - y0, c[2] % shape[2]] = 1
    assert not (h.astype(bool) & ~(M[0] | M[1] | M[2])).any()
    conv = lambda idx: frozenset((int(a), int(b) + y0, int(c)) for a, b, c in idx)
    out = [conv(np.argwhere(h))]
    for _ in range(T):
        h = oracle.step(h, M)
        assert not h[:, :2].any() and not h[:, -2:].any(), 'live cell near the y edge of the ring torus'
        out.append(conv(np.argwhere(h)))
    return out


def ringwrap(cells, L):
    return frozenset((c[0] % (2 * L), c[1], c[2] % (2 * L)) for c in cells)


OFFS = [oracle.offsets(a) for a in range(3)]


def axis(c):
    for a in range(3):
        if c[a] & 1:
            return a


def sstep(S, offs=OFFS):
    """one generation of B45/S345 on the infinite lattice, sparse (neighbourhood is symmetric on cells)."""
    cnt = {}
    for p in S:
        for o in offs[axis(p)]:
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            cnt[q] = cnt.get(q, 0) + 1
    out = set()
    for q, n in cnt.items():
        if q in S:
            if 3 <= n <= 5:
                out.add(q)
        elif n == 4 or n == 5:
            out.add(q)
    return frozenset(out)


def srun(S, T, offs=OFFS):
    S = frozenset(S); out = [S]
    for _ in range(T):
        S = sstep(S, offs); out.append(S)
    return out


def units(S, a, b):
    """the cells of S whose unit lies in a .. b"""
    return frozenset(c for c in S if a <= unit_of(c) <= b)
