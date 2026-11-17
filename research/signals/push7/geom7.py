#!/usr/bin/env python3
"""Geometry and train for the transfer-matrix enumerator `ends7.cpp` (push 7), and the decoding of its output.

    python geom7.py TRAIN LO HI T OUT.geo        TRAIN = fb (the rake train moving +v into an end: absorbers)
                                                 or 5f (the train moving -v away from the end: guns)

Frame: that of `sat_gun.py --dir +1` (fb) or `--dir -1` (5f): tube lo <= x+y+z <= hi, lo <= x-y+z <= hi along
v = (1,0,-1); unit(p) = p.x >> 1; translating by one unit adds (2,0,-2).  Cells of unit 0: the E slab (x = 0) and
the O slab (x = 1).  An even-x cell has neighbours in units -1, 0, +1, an odd-x cell in units 0, +1 only.

Gauge.  The train moves one unit per 2 generations in direction dir, so column_{u+dir}(t) = column_u(t - 2).  Write
s = 2 dir and tau = t - s u (mod T): the gauged column of unit u, colg_u(tau) = column_u(tau + s u), is the same for
every unit of the train, and the rule becomes: cell c of unit u at gauge time tau + 1 is the rule applied to c at
tau and to its neighbours in unit u + delta at gauge time tau - s delta.  This relation does not depend on u, so a
translation by one unit (with the time shift 2 dir that the train needs) is a symmetry, the train is one state,
and ends up to translation and time shift are paths of states.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sg, sat_gun as G
from scat import unit, tr


def tube_cells(lo, hi):
    E, O = [], []
    for x in (0, 1):
        for y in range(-12, 13):
            for z in range(-30, 30):
                p = (x, y, z)
                if sg.is_cell(p) and lo <= x + y + z <= hi and lo <= x - y + z <= hi:
                    (E if x == 0 else O).append(p)
    return sorted(E), sorted(O)


def in_tube(p, lo, hi):
    return lo <= p[0] + p[1] + p[2] <= hi and lo <= p[0] - p[1] + p[2] <= hi


class Geo:
    def __init__(self, train, lo, hi, T):
        self.train, self.lo, self.hi, self.T = train, lo, hi, T
        self.dir = 1 if train == 'fb' else -1
        self.s = 2 * self.dir
        masks = [int(ch, 16) for ch in train]
        self.pat, _ = G.train(masks, True, self.dir)
        self.E, self.O = tube_cells(lo, hi)
        self.idx = {}
        for i, c in enumerate(self.E):
            self.idx[c] = ('E', i)
        for i, c in enumerate(self.O):
            self.idx[c] = ('O', i)

    def locate(self, p):
        """(unit, type, index) of a tube cell."""
        u = unit(p); b = tr(p, -u)
        t, i = self.idx[b]
        return u, t, i

    def nbrs(self, c):
        out = []
        for q in sg.nbrs(c):
            if in_tube(q, self.lo, self.hi):
                out.append(self.locate(q))
        return out

    def train_at(self, t, ua, ub):
        return G.train_cells(self.pat, t, ua, ub, self.dir)

    def column(self, cells_at, u):
        """Gauged column of unit u from a function t -> set of cells: (E bits, O bits) as lists [cell][tau]."""
        T = self.T
        Eb = [[0] * T for _ in self.E]; Ob = [[0] * T for _ in self.O]
        for tau in range(T):
            t = (tau + self.s * u) % T
            st = cells_at(t)
            for i, c in enumerate(self.E):
                Eb[i][tau] = int(tr(c, u) in st)
            for i, c in enumerate(self.O):
                Ob[i][tau] = int(tr(c, u) in st)
        return Eb, Ob

    def train_state(self):
        tc = {t: self.train_at(t, -4, 4) for t in range(self.T)}
        Em, Om = self.column(lambda t: tc[t], -1)
        E0, _ = self.column(lambda t: tc[t], 0)
        bits = ''
        for slab in (Em, Om, E0):
            for row in slab:
                bits += ''.join(map(str, row))
        return bits

    def write(self, fn):
        with open(fn, 'w') as f:
            f.write(f'{self.T} {self.s} {len(self.E)} {len(self.O)}\n')
            for typ, cells in (('E', self.E), ('O', self.O)):
                for c in cells:
                    nb = self.nbrs(c)
                    f.write(f'{len(nb)} ' + ' '.join(f'{u} {0 if t == "E" else 1} {i}' for u, t, i in nb) + '\n')
            f.write(self.train_state() + '\n')

    # ---- decoding of a path of states -------------------------------------------------------------------------
    def slabs(self, bits):
        """A state's bit string -> (E_{-1}, O_{-1}, E_0) as lists [cell][tau]."""
        T = self.T; nE, nO = len(self.E), len(self.O); k = 0; out = []
        for n in (nE, nO, nE):
            sl = []
            for i in range(n):
                sl.append([int(b) for b in bits[k:k + T]]); k += T
            out.append(sl)
        return out

    def orbit(self, states, u1=6, far=-60, extra=4):
        """Orbit of the end given by the path (S_1..S_k) of state bit strings (train before, dead after), placed so
        that S_1's E_0 is unit u1 (so S_1's O_{-1} is unit u1 - 1).  Returns {t: frozenset(cells)} for t < T on units
        >= far."""
        T = self.T; k = len(states)
        E = {}; O = {}
        for j, b in enumerate(states):
            Em, Om, E0 = self.slabs(b)
            w = u1 + j            # E_0 of S_{j+1} is unit u1 + j
            E[w - 1] = Em; O[w - 1] = Om; E[w] = E0
        lo_u = u1 - 1             # units below lo_u: the train (S_1's E_{-1} is unit u1 - 1 and is in E already)
        out = {}
        for t in range(T):
            cells = set(c for c in self.train_at(t, far, lo_u) if True)
            for w in range(lo_u, u1 + k + extra):
                tau = (t - self.s * w) % T
                if w in E:
                    for i, c in enumerate(self.E):
                        if E[w][i][tau]:
                            cells.add(tr(c, w))
                if w in O:
                    for i, c in enumerate(self.O):
                        if O[w][i][tau]:
                            cells.add(tr(c, w))
            out[t] = frozenset(cells)
        return out


if __name__ == '__main__':
    train, lo, hi, T, fn = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    g = Geo(train, lo, hi, T)
    g.write(fn)
    print(f'{fn}: train {train} tube [{lo},{hi}] T={T}: {len(g.E)} E + {len(g.O)} O cells per unit')
