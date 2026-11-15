"""Wires on rings: geometry, loading, per-cell periods, and the cut / flip / kink experiments' shared parts."""
import glob, json, os
import numpy as np
import sg

HERE = os.path.dirname(os.path.abspath(__file__))
S = (1, 1, 1)


def load(wid):
    return json.load(open(os.path.join(HERE, 'wires', wid + '.json')))


def all_wires(kind='wire'):
    out = []
    for fn in sorted(glob.glob(os.path.join(HERE, 'wires', 'W*.json'))):
        r = json.load(open(fn))
        if r['kind'] == kind:
            out.append(r)
    return out


def transverse(v, width):
    """An in-plane (sum 0) cube vector independent of v, `width` cubes long along a cube face diagonal."""
    return [0, width, -width] if v[0] != 0 else [width, 0, -width]


def ring(rec, N, width=40, slab=(-15, 31)):
    """Ring of N repeats of the wire, images of the ring `width` cubes apart, slab of {111} layers s in `slab`
    (exact for anything that starts in those layers, T4; exact sideways only while nothing comes within reach of the
    images, which callers check with `spread`)."""
    v = rec['v']
    g = sg.Geom([[N * t for t in v], transverse(v, width)], [(S, slab[0], slab[1])], unitvec=v, seeds=[tuple(c) for c in rec['cells']])
    return g


def wire_state(g, rec, units=None):
    v = rec['v']
    return g.state(sg.lift_periodic([tuple(c) for c in rec['cells']], [v], [range(g.N) if units is None else units]))


def cell_periods(rec):
    """Per-cell period over one repeat of the wire (on a ring of 4): {cell (repeat 0..): period}."""
    g = ring(rec, 4)
    orb = g.orbit(wire_state(g, rec), rec['period'])[:-1]
    A = np.array([o[:g.n] for o in orb])
    out = {}
    for i in np.nonzero(A.any(0))[0]:
        if g.unit[i] != 1:
            continue
        s = A[:, i]; P = len(s)
        out[g.cells[i]] = next(p for p in range(1, P + 1) if P % p == 0 and (np.roll(s, -p) == s).all())
    return out
