#!/usr/bin/env python3
"""Scattering by SAT: unknown standing objects at the end of a wire, constrained by what they do to an arriving pulse.

Library (used by sat_reflect.py and others).  Everything is on the infinite lattice; no torus.

Region(ob, ua, ub, lo, hi, C3, C4): the variable cells are the cells p (doubled coordinates) with
    lo <= x+y+z <= hi,  lo <= x-y+z <= hi          (a diamond tube along v = (1,0,-1); closed by T2)
    ua <= unit(p) < ub,  unit(p) = p.x >> 1         (translation by one repeat 2v adds 1 to the unit)
    x+y-z <= C3,  x-y-z <= C4  (if given)           (the two diagonal planes that bound a +v end; closed by T2)
Outside: a cell with unit < ua and inside the tube is the bare wire of `ob` at the generation in question (a
constant: the trajectory must then keep unit ua equal to the bare wire, which the callers impose and which makes
the constants exact); every other cell is dead.  With C3, C4 given nothing can be born beyond the planes (T2).  If
C3 is None the region is instead cut at unit ub, and the callers must force a dead margin (units ub-1) themselves.

Traj(f, R, T, t0): variables for generations 0..T (the wire's phase at generation t is (t0 + t) mod P), with the rule
B45/S345 between consecutive generations.
"""
import os, sys
import numpy as np
import sg, plab
from sat_pulse import CNF

V = (1, 0, -1)


def unit(p):
    return p[0] >> 1


def tr(p, k):
    return (p[0] + 2 * k, p[1], p[2] - 2 * k)


class Wire:
    """A wire of repeat one cube along (1,0,-1) and its (2,1) pulses, as sets of base cells per phase."""

    def __init__(self, ob, obl=None):
        self.P = ob['bg_period']
        base = [tuple(c) for c in ob['bg']]
        w = frozenset(tr(c, k) for c in base for k in range(-30, 31))
        self.bg = []
        for ph in range(self.P):
            self.bg.append(frozenset(tr(c, -unit(c)) for c in w if -3 <= unit(c) <= 3))
            w = sg.step_set(w)
        # pulses: cells that differ from the bare wire, by phase, as the pulse is at generation `ph` after an
        # even generation at which it is ob['defect'] (right) or obl['defect'] (left)
        self.pulse = {}
        for name, o in (('R', ob), ('L', obl)):
            if o is None:
                continue
            w = frozenset(tr(c, k) for c in base for k in range(-40, 41))
            x = w ^ frozenset(tuple(c) for c in o['defect'])
            lst = []
            for ph in range(2 * self.P):
                lst.append(frozenset(c for c in x ^ w if abs(unit(c)) < 25))
                w = sg.step_set(w); x = sg.step_set(x)
            self.pulse[name] = lst

    def live(self, p, ph):
        return tr(p, -unit(p)) in self.bg[ph % self.P]

    def pulse_cells(self, name, t, k=0):
        """Cells differing from the bare wire, t generations after the pulse was the file's defect moved k units."""
        s = 1 if name == 'R' else -1
        j, r = divmod(t, 2 * self.P)
        # after 2P generations the pulse has moved P units (speed one unit per 2 generations)
        return frozenset(tr(c, k + s * j * self.P) for c in self.pulse[name][r])


class Region:
    def __init__(self, wire, ua, ub, lo, hi, C3=None, C4=None, lo2=None, hi2=None):
        self.wire = wire; self.ua, self.ub, self.lo, self.hi, self.C3, self.C4 = ua, ub, lo, hi, C3, C4
        self.lo2 = lo if lo2 is None else lo2; self.hi2 = hi if hi2 is None else hi2
        cells = []
        for u in range(ua, ub):
            for x in (2 * u, 2 * u + 1):
                for y in range(-(hi - lo) // 2 - 2, (hi - lo) // 2 + 3):
                    for z in range(lo - x - abs(y) - 2, hi - x + abs(y) + 3):
                        p = (x, y, z)
                        if sg.is_cell(p) and self.in_var(p):
                            cells.append(p)
        self.cells = sorted(set(cells)); self.index = {p: i for i, p in enumerate(self.cells)}
        self.n = len(self.cells)
        self.units = np.array([unit(p) for p in self.cells])
        # neighbours: variable index, or ('w', p) for a wire constant, or nothing (dead)
        self.nbv = []; self.nbw = []
        for p in self.cells:
            v = []; w = []
            for q in sg.nbrs(p):
                if q in self.index:
                    v.append(self.index[q])
                elif unit(q) < ua and self.in_tube(q):
                    w.append(q)
            self.nbv.append(v); self.nbw.append(w)

    def in_tube(self, p):
        return self.lo <= p[0] + p[1] + p[2] <= self.hi and self.lo2 <= p[0] - p[1] + p[2] <= self.hi2

    def in_var(self, p):
        if not (self.ua <= unit(p) < self.ub and self.in_tube(p)):
            return False
        if self.C3 is not None and p[0] + p[1] - p[2] > self.C3:
            return False
        if self.C4 is not None and p[0] - p[1] - p[2] > self.C4:
            return False
        return True

    def of_units(self, a, b):
        return [i for i in range(self.n) if a <= self.units[i] < b]


class Problem:
    def __init__(self):
        self.f = CNF()
        self.T = self.f.var(); self.f.add(self.T)        # the constant true

    def traj(self, R, T, t0=0, wrap=None, left=None):
        """Variables X[t][i], t = 0..T; rule between t and t+1.  wrap: if set, X[T] is not created; instead the
        successor of X[T-1] is X[0] (a state of period T).  left(q, t): the state of an outside cell q with
        unit < ua at generation t, as True/False or a literal (default: the bare wire R.wire at phase t0 + t)."""
        f = self.f; n = R.n
        nlayers = T if wrap else T + 1
        X = [[f.var() for _ in range(n)] for _ in range(nlayers)]
        for t in range(T):
            ph = t0 + t
            Y = X[(t + 1) % nlayers]
            for i in range(n):
                ins = [X[t][j] for j in R.nbv[i]]
                for q in R.nbw[i]:
                    v = R.wire.live(q, ph) if left is None else left(q, t)
                    if v is True:
                        ins.append(self.T)
                    elif v is not False:
                        ins.append(v)
                self.rule(X[t][i], Y[i], ins)
        return X

    def rule(self, x, y, ins):
        f = self.f
        ge = f.totalizer(ins, 6) if ins else []
        g3 = ge[2] if len(ge) >= 3 else None; g4 = ge[3] if len(ge) >= 4 else None; g6 = ge[5] if len(ge) >= 6 else None
        if g3 is None:
            f.add(-y); return
        f.add(-y, g3)                                   # alive next needs >= 3
        if g4 is None:
            f.add(-y, x); f.add(-x, -g3, y); return
        f.add(-y, g4, x)                                # ... and >= 4 unless it was alive
        if g6 is None:
            f.add(-g4, y); f.add(-x, -g3, y); return
        f.add(-y, -g6)                                  # ... and <= 5
        f.add(g6, -g4, y); f.add(g6, -x, -g3, y)

    def fix(self, lit, val):
        self.f.add(lit if val else -lit)

    def eq(self, a, b):
        self.f.add(-a, b); self.f.add(a, -b)

    def neq(self, a, b):
        self.f.add(a, b); self.f.add(-a, -b)

    def solve(self, solver='cadical153', timeout=600, assumptions=()):
        """Returns (status, set of true variables or None); status in 'SAT', 'UNSAT', 'TIMEOUT'."""
        from pysat.solvers import Solver
        import threading
        with Solver(name=solver, bootstrap_with=self.f.cl) as s:
            timer = threading.Timer(timeout, lambda: s.interrupt()); timer.start()
            try:
                r = s.solve_limited(assumptions=list(assumptions), expect_interrupt=True)
            finally:
                timer.cancel()
            if r is None:
                return 'TIMEOUT', None
            if not r:
                return 'UNSAT', None
            return 'SAT', set(l for l in s.get_model() if l > 0)


def cells_of(R, X, model):
    return frozenset(R.cells[i] for i in range(R.n) if X[i] in model)


def semi_wire(wire, ph, far=-60, upto=0):
    """The bare wire at phase ph on units far .. upto-1 (a finite piece: its far end burns, at most one unit per
    generation, so it is as good as infinite for (upto - far) generations near `upto`)."""
    return frozenset(tr(c, k) for c in wire.bg[ph % wire.P] for k in range(far, upto))
