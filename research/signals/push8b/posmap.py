#!/usr/bin/env python3
"""push 8b: where along push 7's line each pair read works, and where the reader kills the store.

    python3 posmap.py [--ns 1,2,3,5] [--ua 34] [--ub 52]

For each of the 24 placements of junc2.py that read a uniform store with a pair of pulses (8 with a wire C as the
reader, 16 with a wire B; research/scratch/signals/p8b/junc2_{C,B}_0of1.jsonl), the reader is put beside the standing
line (n holes, generation 900) with its crossing at line unit u, for every u, run 160 generations, and then given
its probe (the first read of the junc2 record: side, spacing).
One character per unit u:
  X      the reader does not stand there: 160 generations later the state is not of period 4, or differs from the union
         in the store's tube, or more than 6 reader units from the crossing
  !      it stands, but 240 generations after the probe the object is not what it was
  0..9, a..z   it stands, the probe leaves everything exactly as it was; the character is the number of cells in which
         the run with the probe differs from the run without, 44 generations after the launch, outside 3 reader units
         of the crossing (the signal that is travelling)
The line is printed above in letters (line.letters: b wire B, p wire B', # the edge unit f)."""
import argparse, json, os
import lab, wires, survey, line, cell, junc
from lab import tr, unit
from survey import inv

NR = survey.NR          # 18, as in junc2.py


LABS = {}


class R:
    def __init__(self, wire, gi_, phi, t0, u):
        if wire not in LABS:
            LABS[wire] = survey.Lab(wire)
        L = LABS[wire]
        self.g = lab.SYMS[gi_]; self.gi = inv(self.g); self.phi = phi
        HRg = [lab.app(self.g, c) for c in L.FRh]
        us, self.ur = survey.crossing(self.g, tuple(t0), HRg, L.HS)
        self.t = (t0[0] + 2 * (u - us), t0[1], t0[2] - 2 * (u - us))
        self.own = lab.pk(wires.capped_B(-NR, NR) if wire == 'B' else wires.capped_C(-NR, NR))
        self.right = lab.PULSE_B if wire == 'B' else lab.PULSE_C
        self.left = junc.LEFT[wire]

    def place(self, cells):
        return lab.pk([lab.app(self.g, c, self.t) for c in cells])

    def back(self, c):
        return lab.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2]))

    def runit(self, c):
        return unit(self.back(c))


def one(S, rd, side, s):
    R0 = rd.place(lab.up(lab.run(rd.own, rd.phi)))
    U = lab.union(S, R0)
    if len(U) != len(S) + len(R0):
        return 'X'
    J = lab.run(U, 160)
    if not lab.same(lab.run(J, 4), J):
        return 'X'
    D = lab.up(lab.xor(J, U))
    if any(cell.in_tube(c) for c in D) or any(abs(rd.runit(c) - rd.ur) > 6 for c in D):
        return 'X'
    Y = lab.run(J, rd.phi)
    if side == 'L':
        pc = wires.pulse(rd.right, rd.ur - 9) + wires.pulse(rd.right, rd.ur - 9 - s)
    else:
        pc = wires.pulse(rd.left, rd.ur + 9) + wires.pulse(rd.left, rd.ur + 9 + s)
    X = lab.xor(Y, rd.place(pc))
    Xc = lab.run(X, 44); Yc = lab.run(Y, 44)
    n = sum(1 for c in lab.up(lab.xor(Xc, Yc)) if abs(rd.runit(c) - rd.ur) > 3)
    Xf = lab.run(Xc, 240 - 44 - rd.phi)
    if not lab.same(Xf, J):
        return '!'
    return '0123456789abcdefghijklmnopqrstuvwxyz'[min(n, 35)]


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--ns', default='1,2,3,5'); ap.add_argument('--ua', type=int, default=34); ap.add_argument('--ub', type=int, default=52)
    a = ap.parse_args()
    ns = [int(x) for x in a.ns.split(',')]
    lines = {n: cell.standing(n) for n in ns}
    print(f'units {a.ua}..{a.ub}')
    for n in ns:
        print(f'  n={n}  line {line.letters(lines[n], a.ua, a.ub + 1)[1]}')
    for w in 'BC':
        for l in open(os.path.join(lab.SCR, f'junc2_{w}_0of1.jsonl')):
            r = json.loads(l)
            rd0 = r['reads'][0]
            print(f"reader {w} g={r['g']} phi={r['phi']} t={tuple(r['t'])} probe {rd0['side']} s={rd0['s']}  (uniform stores: B {rd0['nB']}, B' {rd0['nBp']})")
            for n in ns:
                row = ''.join(one(lines[n], R(w, r['g'], r['phi'], r['t'], u), rd0['side'], rd0['s']) for u in range(a.ua, a.ub + 1))
                print(f'  n={n}       {row}', flush=True)
