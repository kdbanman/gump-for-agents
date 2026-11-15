"""The four-site family of wires: stators (0,1,2), (0,1,4) in every unit plus a subset of the four sites
(1,0,0), (1,0,2), (1,0,4), (0,2,3) (cells at an even generation; unit u = moved by u*(2,0,-2)).
B = sites 0,1,2;  B' = 0,2,3;  C (survey wire 28) = 0,1,3;  C' (survey wire 17) = 1,2,3.
Tools: which subsets are wires, their 2-cell pulses, and what a pulse does at a clean wall between two of them.
Everything lives in the closed 3 x 3 tube 1 <= x+y+z, x-y+z <= 5."""
import itertools, sys
import numpy as np
import sg, scat

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
STATOR = [(0, 1, 2), (0, 1, 4)]
SITES = [(1, 0, 0), (1, 0, 2), (1, 0, 4), (0, 2, 3)]
NAMES = {(0, 1, 2): 'B', (0, 2, 3): "B'", (0, 1, 3): 'C', (1, 2, 3): "C'"}
tr = scat.tr


def unit_cells(sub):
    return frozenset(STATOR + [SITES[i] for i in sub])


def ring(N=24):
    return sg.Geom([(N, 0, -N)], [(S1, 1, 5), (S2, 1, 5)], unitvec=(1, 0, -1))


def wire_state(g, sub):
    return g.state([tr(c, k) for c in unit_cells(sub) for k in range(g.N)])


def pulses(g, sub, maxcells=2):
    """All sets of <= maxcells cells within units 10..12 (cells of the tube) whose flip at an even generation is a
    (2, +-1) pulse.  Returns list of (direction, cells moved to unit 0)."""
    z = wire_state(g, sub)
    cand = [i for i in range(g.n) if 10 <= g.unit[i] <= 11]
    out = []
    for r in range(1, maxcells + 1):
        for comb in itertools.combinations(cand, r):
            if min(g.unit[i] for i in comb) != 10:
                continue
            x = z.copy()
            for i in comb:
                x[i] ^= 1
            y = g.run(x, 2)
            d = set(np.nonzero((y != z)[:g.n])[0].tolist())
            for s in (1, -1):
                if d == {int(g.grid[(g.unit[i] + s) % g.N, np.nonzero(g.grid[g.unit[i]] == i)[0][0]]) for i in comb}:
                    out.append((s, frozenset(tr(g.cells[i], -10) for i in comb)))
    return out


if __name__ == '__main__':
    g = ring()
    print('subsets of the four sites that are wires (period <= 2) in the closed tube:')
    wires = []
    for r in range(0, 5):
        for sub in itertools.combinations(range(4), r):
            z = wire_state(g, sub)
            p1 = bool((g.run(z, 1) == z).all()); p2 = bool((g.run(z, 2) == z).all())
            if p2:
                wires.append(sub)
                ps = pulses(g, sub)
                print('  sites', sub, NAMES.get(sub, ''), 'period', 1 if p1 else 2, '; 2-cell pulses:', [(s, sorted(c)) for s, c in ps])


def decode(g, st):
    """One hex digit per unit: the 4-bit mask of occupied sites if the unit is stators + sites only, else '?'."""
    live = {}
    for i in np.nonzero(st[:g.n])[0]:
        live.setdefault(int(g.unit[i]), set()).add(tr(g.cells[i], -int(g.unit[i])))
    out = ''
    for u in range(g.N):
        s = live.get(u, set())
        rest = s - set(STATOR) - set(SITES)
        if rest or not set(STATOR) <= s:
            out += '?' if s else '.'
        else:
            out += '%x' % sum(1 << i for i in range(4) if SITES[i] in s)
    return out


def config(g, masks):
    """State from a list of 4-bit masks, one per unit (None = empty unit)."""
    cells = []
    for u, m in enumerate(masks):
        if m is None:
            continue
        cells += [tr(c, u) for c in STATOR] + [tr(SITES[i], u) for i in range(4) if m >> i & 1]
    return g.state(cells)


class Piece:
    """A finite piece of the closed 3 x 3 tube, units -L .. L-1, ends simply cut (they burn inward, at most one
    unit per generation: look only at |unit| < L - T)."""

    def __init__(self, L=90):
        self.L = L
        seeds = [tr(c, k) for c in STATOR + SITES for k in range(-L, L)]
        m = 4 * L + 20
        self.g = sg.Geom([], [(S1, 1, 5), (S2, 1, 5), (S3, -m, m), (S4, -m, m)], seeds=seeds)

    def config(self, fn):
        """fn(u) -> mask for unit u."""
        cells = []
        for u in range(-self.L, self.L):
            m = fn(u)
            cells += [tr(c, u) for c in STATOR] + [tr(SITES[i], u) for i in range(4) if m >> i & 1]
        return self.g.state(cells)

    def decode(self, st, ua, ub):
        live = {}
        for c in self.g.cells_of(st):
            live.setdefault(scat.unit(c), set()).add(tr(c, -scat.unit(c)))
        out = ''
        for u in range(ua, ub):
            s = live.get(u, set())
            if s - set(STATOR) - set(SITES) or not set(STATOR) <= s:
                out += '?' if s else '.'
            else:
                out += '%x' % sum(1 << i for i in range(4) if SITES[i] in s)
        return out

    def flip(self, st, cells, k=0):
        st = st.copy()
        for c in cells:
            st[self.g.index[tr(c, k)]] ^= 1
        return st
