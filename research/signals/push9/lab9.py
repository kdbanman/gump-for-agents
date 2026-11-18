#!/usr/bin/env python3
"""lab9 (push 9): wire B with a stretch and an object standing beside it.

Uses push 8's lab8 (the stepper), wire8 and exp8 unchanged.  The stepper is checked against reference/oracle.py on
objects of the kind used here (wire B, a stretch, an object outside the tube, pulses) by check9.py.

Geometry (push 8): unit u holds the cells with x in {2u, 2u+1}; tr(c, k) moves a cell k units towards
+v = (1,0,-1).  Family unit = stators (0,1,2), (0,1,4) + sites 0 = (1,0,0), 1 = (1,0,2), 2 = (1,0,4), 3 = (0,2,3);
hex digit of the subset; 7 = wire B, d = wire B', b = wire C (the left-going pulse of wire B), 6f = the right-going
pulse.  The wire's 3 x 3 tube: 1 <= x+y+z <= 5, 1 <= x-y+z <= 5.

Box coordinates of lab8: (x, y, w = x + z); the tube is |y| + |w - 3| <= 2.
"""
import os, sys, json, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'push8'))
import lab8, wire8 as W, exp8 as X          # noqa: E402
from lab8 import Lab, tr, unit, is_cell, step_set      # noqa: E402

SCR = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p9')
os.makedirs(SCR, exist_ok=True)
CAT = os.path.join(ROOT, 'research', 'atlas', 'catalogue.jsonl')

# ---- the 48 lattice symmetries (signed permutations of the doubled coordinates)
SYMS = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1, -1), repeat=3):
        SYMS.append((perm, sg))


def app(g, c, t=(0, 0, 0)):
    perm, sg = g
    return (sg[0] * c[perm[0]] + t[0], sg[1] * c[perm[1]] + t[1], sg[2] * c[perm[2]] + t[2])


def in_tube(c, r=2):
    """inside the wire's tube: r = 2 the 3 x 3 tube, r = 4 the 5 x 5 tube"""
    return abs(c[1]) + abs(c[0] + c[2] - 3) <= r


def half(c):
    """the half-turn that maps wire B onto itself reversed"""
    return (-c[0] - 2, c[1], 8 - c[2])


def catalogue():
    return [json.loads(l) for l in open(CAT)]


def nbrs(c):
    a = 0 if c[0] & 1 else (1 if c[1] & 1 else 2)
    b, d = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sd in (2, -2):
            v = list(c); v[b] += sb; v[d] += sd; out.append(tuple(v))
    for sa in (1, -1):
        for t in (b, d):
            for st in (1, -1):
                v = list(c); v[a] += sa; v[t] += st; out.append(tuple(v))
    return out


def halo(cells):
    out = set(cells)
    for c in cells:
        out.update(nbrs(c))
    return out


def orbit(cells, P):
    out = [frozenset(cells)]
    for _ in range(P - 1):
        out.append(step_set(out[-1]))
    return out


def norm_t(t):
    """an even translation reduced by the unit vector (2,0,-2) to the form (0, b, c); returns ((0,b,c), units moved)"""
    m = t[0] // 2
    return (0, t[1], t[2] + 2 * m), m


WB = [W.fam(7), None]
WB[1] = frozenset(c for c in step_set(frozenset(tr(c, u) for u in range(-3, 4) for c in WB[0])) if unit(c) == 0)
WB_ALL = [frozenset(tr(c, u) for u in range(-8, 9) for c in WB[p]) for p in (0, 1)]
WB_HALO = [halo(frozenset(tr(c, u) for u in range(-1, 2) for c in WB[p])) for p in (0, 1)]


def placements(orb, phases=None):
    """every placement of the orbit `orb` (list of frozensets, one per phase) beside wire B at its phase 0:
    yields (gi, ph, (0,b,c), cells) with cells = g(orb[ph]) + (0,b,c), for which the closed neighbourhoods of the
    object's union and of the wire's union meet and the object does not overlap the wire's union.  Orientations
    that give the same placed orbit are listed once."""
    P = len(orb)
    union = frozenset().union(*orb)
    if phases is None:
        phases = (0, 1) if P % 2 == 0 and P > 1 else (0,)
    wun = WB_ALL[0] | WB_ALL[1]
    whalo = np.array(sorted(WB_HALO[0] | WB_HALO[1]))
    seen = set()
    for gi, g in enumerate(SYMS):
        gun = [app(g, c) for c in union]
        gh = np.array(sorted(halo(gun)))
        d = (whalo[:, None, :] - gh[None, :, :]).reshape(-1, 3)
        d = d[((d & 1) == 0).all(1)]
        m = d[:, 0] // 2
        bc = np.unique(np.stack([d[:, 1], d[:, 2] + 2 * m], 1), axis=0)
        for ph in phases:
            base = [app(g, c) for c in orb[ph]]
            for b, c in bc.tolist():
                t = (0, b, c)
                un = frozenset((x, y + b, z + c) for x, y, z in gun)
                if un & wun:
                    continue
                cells = frozenset((x, y + b, z + c) for x, y, z in base)
                # canonical key up to a move along the wire
                x0 = min(q[0] for q in cells) // 2
                key = (frozenset(tr(q, -x0) for q in cells), frozenset(tr(q, -x0) for q in un))
                if key in seen:
                    continue
                seen.add(key)
                yield gi, ph, t, cells


def box_for(cells, R, margin=6):
    """a ring Lab of R units whose y, w box holds the tube and `cells` with a margin"""
    ys = [c[1] for c in cells] + [-2, 2]; ws = [c[0] + c[2] for c in cells] + [1, 5]
    ylo = min(ys) - margin; yhi = max(ys) + margin + 1; wlo = min(ws) - margin; whi = max(ws) + margin + 1
    ylo -= ylo % 2; yhi += yhi % 2; wlo -= wlo % 2; whi += whi % 2
    return Lab(0, R, ylo, yhi, wlo, whi, ring=True)


def hexring(L, a, u0=None, u1=None):
    """hex family letters of the units of the ring, reading only the cells inside the 3 x 3 tube
    ('?' = not stators + sites, '_' = empty)"""
    u0 = L.ua if u0 is None else u0; u1 = L.ub if u1 is None else u1
    out = []
    sts = set(W.ST); sites = W.SITES
    for u in range(u0, u1):
        uc = [c for c in L.unit_cells(a, u) if in_tube(c)]
        if not uc:
            out.append('_'); continue
        rest = set(uc) - sts
        if len(uc) - len(rest) != 2 or not rest <= set(sites):
            out.append('?'); continue
        out.append('%x' % sum(1 << i for i in range(4) if sites[i] in rest))
    return ''.join(out)


def outside(L, a):
    """the live cells outside the 3 x 3 tube"""
    return frozenset(c for c in L.cells(a) if not in_tube(c))


def rot(s, i):
    return s[i:] + s[:i]


def canon_ring(s):
    """the ring word rotated to its least rotation (for counting outcomes)"""
    return min(rot(s, i) for i in range(len(s)))


# ---- a stepper with a static bias on the neighbour counts (lab9.c): a search tool
_blib = None


def blib():
    global _blib
    if _blib is None:
        import ctypes, subprocess
        src = os.path.join(HERE, 'lab9.c'); so = os.path.join(SCR, 'lab9.so')
        if not os.path.exists(so) or os.path.getmtime(so) < os.path.getmtime(src):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-shared', '-fPIC', '-o', so, src])
        _blib = ctypes.CDLL(so)
        _blib.run_bias.argtypes = [ctypes.c_void_p] * 3 + [ctypes.c_int] * 5 + [ctypes.c_void_p]
        _blib.run_bias.restype = ctypes.c_int
    return _blib


def run_bias(L, a, bias, n=1):
    """n generations of the array a in the Lab L with the count of every site raised by bias (same shape)"""
    import ctypes
    assert bias.dtype == np.uint8 and bias.shape == L.shape and bias.flags['C_CONTIGUOUS']
    t = ctypes.c_int(0)
    blib().run_bias(a.ctypes.data, L.scratch.ctypes.data, bias.ctypes.data, L.NX, L.NY, L.NW, n, 1 if L.ring else 0, ctypes.byref(t))
    if t.value:
        L.touch = True
    return a


def bias_of(L, cells):
    """the bias array of a set of cells that are held live (each adds one to the count of its 12 neighbours;
    their own sites get 100, so they are never born in the stepped state)"""
    b = np.zeros(L.shape, np.uint8)
    for c in cells:
        for q in nbrs(c):
            try:
                b[L.idx(q)] += 1
            except ValueError:
                pass
    for c in cells:
        b[L.idx(c)] = 100          # the held cells' own sites stay out of the stepped state
    return b
