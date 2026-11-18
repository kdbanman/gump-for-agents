#!/usr/bin/env python3
"""xlab9 (push 9): the call line: a capped wire C laid across the store wire, one unit before the wall of a stretch.

Uses push 8b's sparse stepper lab.py / st.c and its capped wire C (wires.capped_C), unchanged; both are judged here
only through objects that the oracle then steps (verify_call9.py).

Placement (found by cross9.py among push 8b's survey classes): the reader's own frame is a capped wire C on its units
-NR..NR-1 along (1,0,-1); a cell q of it goes to g(q) + T0 + (2m, 0, -2m) with g = SYMS[11] = (x,y,z) -> (x, -z, -y)
... see CALL below; its axis is (1,1,0).  With m = (unit before the wall) - US the crossing is at the unit before the wall.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'push8'))
import exp8 as X, wire8 as W8           # noqa: E402
sys.path.insert(0, os.path.join(HERE, '..', 'push8b'))
import lab, wires, survey               # noqa: E402
from lab import tr, unit                # noqa: E402
import cross9 as Cx                     # noqa: E402
from cross9 import letters              # noqa: E402

CALL = dict(G=11, PHI=0, T0=(-4, 2, -4), US=1, UR=3)       # the call line (release to the left as k pulses)


class Line:
    def __init__(self, spec=CALL, nr=18, reader='C'):
        self.G, self.PHI, self.T0, self.US, self.UR = spec['G'], spec['PHI'], spec['T0'], spec['US'], spec['UR']
        self.g = lab.SYMS[self.G]; self.gi = survey.inv(self.g)
        self.pulse = lab.PULSE_C if reader == 'C' else lab.PULSE_B
        ua, ub = (-nr, nr) if isinstance(nr, int) else nr
        self.rc = (wires.capped_C if reader == 'C' else wires.capped_B)(ua, ub)
        self.own = lab.run(lab.pk(self.rc), self.PHI)

    def tt(self, u):
        """translation that puts the crossing at store unit u"""
        m = u - self.US
        return (self.T0[0] + 2 * m, self.T0[1], self.T0[2] - 2 * m)

    def cells(self, u):
        tt = self.tt(u)
        return lab.pk([lab.app(self.g, q, tt) for q in lab.up(self.own)])

    def probe(self, u, ats=(9, 10)):
        """the cells of right-going pulses of the reader launched `ats` reader units before the crossing"""
        tt = self.tt(u)
        return lab.pk([lab.app(self.g, q, tt) for at in ats for q in wires.pulse(self.pulse, self.UR - at)])

    def rletters(self, Xs, u, a=-14, b=14):
        tt = self.tt(u)
        back = lab.pk([c for c in (lab.app(self.gi, (c[0] - tt[0], c[1] - tt[1], c[2] - tt[2])) for c in lab.up(Xs)) if Cx.in_tube(c)])
        return letters(back, self.UR + a, self.UR + b)


def store(word):
    """push 8's cell with the wire letters `word` (units 4..): keys, N"""
    N = len(word)
    cells = X.CAPL | X.hexword(word, 4) | frozenset(tr(c, 4 + N) for c in X.CAPR2)
    return lab.pk(cells), N
