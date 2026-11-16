"""Segment lab: finite objects in empty space made of stretches of wire B and wire B' (= B with one cell per unit
moved; survey wire 21) between two caps, and pulses on them.  Everything lives in the closed 3 x 3 tube
1 <= x+y+z, x-y+z <= 5 (T2), so a vessel that is just that tube, long enough, is exact for empty space.

Unit u = the cells with x in {2u, 2u+1}.  All states are given at an even generation (wire B in phase 0).
H: (x,y,z) -> (-x-2, y, 8-z) is a half-turn that maps B and B' onto themselves reversed, and units >= 0 onto units <= -1.
"""
import numpy as np
import sg, plab, scat

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
H = lambda c: (-c[0] - 2, c[1], 8 - c[2])
tr = scat.tr
B = frozenset([(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)])
Bp = frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 4)])
UNITS = {'B': B, 'Bp': Bp}
# caps, as cells relative to the first unit after the wire (found by caps.py):
CAPS = {
    # on wire B: swallows every pulse B and stays as it is
    'eater': [(0, -1, 2), (0, 0, 1), (0, 1, 4), (1, -2, 2), (1, 0, 0), (1, 0, 4), (2, -2, 1), (2, -1, 0)],
    # on wire B': the end of the creeping caps
    'E': [(0, -2, 3), (0, -1, 2), (0, 2, 3), (1, -2, 2), (1, 0, 2), (2, -1, 2), (2, 0, 3)],
}
# pulses at an even generation, right-moving, as cells that differ from the wire, with the pulse "at unit 0"
PULSE = {
    'B': frozenset([(1, 0, 0), (2, 2, 1)]),
}


def _bp_pulse():
    """The 2-cell pulse of B' (survey wire 21, given there at the odd phase), one generation later."""
    g = plab.geom(24, 1, 5)
    odd = g.state(sg.lift_periodic([(0, 0, 1), (0, 0, 3), (0, 0, 5), (0, 1, 2), (0, 1, 4)], [(1, 0, -1)], [range(24)]))
    x = odd.copy()
    for c in [(9, 2, -6), (10, 0, -5)]:
        x[g.index[g.canon(c)]] ^= 1
    x = g.run(x, 1); z = g.run(odd, 1)
    assert g.cells_of(z) == frozenset(g.canon(c) for c in sg.lift_periodic(Bp, [(1, 0, -1)], [range(24)]))
    d = sorted(g.cells[i] for i in np.nonzero((x != z)[:g.n])[0])
    u = min(scat.unit(c) for c in d)
    return frozenset(tr(c, -u) for c in d)


PULSE['Bp'] = _bp_pulse()


def half(segs, cap):
    """Right half: segs = [(kind, n), ...] laid from unit 0 upward, then the cap.  Returns (cells, end unit)."""
    cells = set(); u = 0
    for kind, n in segs:
        for k in range(n):
            cells |= {tr(c, u + k) for c in UNITS[kind]}
        u += n
    if cap:
        cells |= {tr(c, u) for c in CAPS[cap]}
    return frozenset(cells), u


class Obj:
    """left: (segs, cap) read outward from the middle towards -v (it is laid as a right half and turned by H);
    right: (segs, cap) from the middle towards +v."""

    def __init__(self, left, right, lo=1, hi=5):
        r, self.ur = half(*right)
        # H maps x >= -2 onto x <= 0: lay the left half from unit -1 (one extra unit of its first kind), turn it;
        # its cells at x = 0 coincide with the right half's when the two halves start with the same kind
        segs = list(left[0]); segs[0] = (segs[0][0], segs[0][1] + 1)
        l, ul = half(segs, left[1])
        assert segs[0][0] == right[0][0][0]
        self.ul = -ul
        self.cells = r | frozenset(H(tr(c, -1)) for c in l)
        m = 4 * (max(self.ur, ul) + 6)
        self.g = sg.Geom([], [(S1, lo, hi), (S2, lo, hi), (S3, -m - 10, m), (S4, -m - 10, m)], seeds=list(self.cells))
        self.x0 = self.g.state(self.cells)

    def stationary(self, x=None):
        x = self.x0 if x is None else x
        return bool((self.g.run(x, 2, sparse=True) == x).all())

    def with_pulse(self, x, kind, u, direction=1):
        """Add a pulse of wire `kind` at unit u (right-moving: its cells at units u, u+1), or its H-image
        (left-moving, the image of the right-mover at unit -u-1... placed so that its cells are near unit u)."""
        x = x.copy()
        if direction > 0:
            cells = [tr(c, u) for c in PULSE[kind]]
        else:
            cells = [H(tr(c, -u - 2)) for c in PULSE[kind]]
        for c in cells:
            x[self.g.index[c]] ^= 1
        return x

    def diffline(self, x, z, ua, ub):
        d = np.nonzero((x != z)[:self.g.n])[0]
        cnt = {}
        for i in d:
            u = scat.unit(self.g.cells[i]); cnt[u] = cnt.get(u, 0) + 1
        return ''.join('.' if u not in cnt else (str(cnt[u]) if cnt[u] < 10 else '#') for u in range(ua, ub))

    def kinds(self, x, ua, ub):
        """One letter per unit: B, P (= B'), . (empty), ? (anything else), at an even generation."""
        live = self.g.cells_of(x); by = {}
        for c in live:
            by.setdefault(scat.unit(c), set()).add(tr(c, -scat.unit(c)))
        out = ''
        for u in range(ua, ub):
            s = frozenset(by.get(u, ()))
            out += 'B' if s == B else ('P' if s == Bp else ('.' if not s else '?'))
        return out

    def show(self, x, gens, every=2, ua=None, ub=None):
        ua = self.ul - 4 if ua is None else ua; ub = self.ur + 5 if ub is None else ub
        z = self.x0.copy()
        for t in range(0, gens + 1):
            if t % every == 0:
                print('%4d %s   %s' % (t, self.diffline(x, z, ua, ub), self.kinds(x, ua, ub) if t % 2 == 0 else ''))
            x = self.g.run(x, 1, sparse=True); z = self.g.run(z, 1, sparse=True)
        return x
