#!/usr/bin/env python3
"""push 8b: the reader beside push 7's line: the experiments behind the objects (st.c stepper; the objects themselves
are judged by verify_read.py with the oracle alone).

    python3 cell.py table            the reader at unit 42 beside the standing line with n = 1..6 holes, three pulses
    python3 cell.py positions        the same reader at every unit 30..56 of the lines n = 1..6: where it stands
    python3 cell.py write            the reader standing beside the line BEFORE the write (the train running)

Line: push 7's line (gun 4, end 70, N = 80; objects7.json record line-N80-gun4-end70-*), E at unit 32 and n holes at
units 49, 55, .. flipped at generation 1; standing by generation 900.
Reader: a capped wire C (clock caps), 14 + 14 units, placed as x -> g(x) + t.  READERS gives the placements used."""
import sys, json
import lab, wires, line
from lab import tr, unit
from survey import inv

NR = 14
E_CELLS = [(65, 2, -62), (66, 0, -63), (66, 0, -61)]
H0 = (99, 2, -96)

# name: (index of g in lab.SYMS, t at crossing unit 0, reader unit of the crossing)
READERS = {
    'r246': (13, (-2, 0, 0), -1),      # g = 13: beside B the crossing becomes an eater after one pulse, beside B' the pulse passes
    'r132': (8, (0, 2, 6), 0),
    'r663': (29, (0, 0, -2), -1),      # phi = 1: beside B the pulse passes, beside B' eater after one pulse
    'r549': (24, (0, 2, 6), 0),
    # wire B as the reader, the same four places
    'b13': (13, (-2, 0, 0), -1), 'b8': (8, (0, 2, 6), 0), 'b29': (29, (-2, 0, 0), -1), 'b24': (24, (0, 2, 6), 0),
    'b19': (19, (0, 4, 10), 1), 'b22': (22, (-4, 2, -2), 0),
}
PHI = {'r246': 0, 'r132': 0, 'r663': 1, 'r549': 1, 'b13': 0, 'b8': 0, 'b29': 1, 'b24': 1, 'b19': 0, 'b22': 0}


def in_tube(c):
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5


def line0():
    r = line.records()['line-N80-gun4-end70-n1']
    return lab.pk([tuple(c) for c in r['y0']])


def write_flips(n):
    return E_CELLS + [tr(H0, 6 * j) for j in range(n)]


def standing(n, gen=900):
    k = lab.run(line0(), 1)
    k = lab.xor(k, lab.pk(write_flips(n)))
    return lab.run(k, gen - 1)


class Reader:
    def __init__(self, name, u, nr=NR):
        gi_, t0, ur = READERS[name]
        self.name = name; self.g = lab.SYMS[gi_]; self.gi = inv(self.g); self.phi = PHI[name]; self.ur = ur; self.u = u
        self.t = (t0[0] + 2 * u, t0[1], t0[2] - 2 * u)
        self.nr = nr
        self.wire = 'B' if name.startswith('b') else 'C'
        self.own = lab.pk(wires.capped_B(-nr, nr) if self.wire == 'B' else wires.capped_C(-nr, nr))
        self.p = lab.PULSE_B if self.wire == 'B' else lab.PULSE_C

    def cells(self, own_gen=0):
        """the placed reader at its own generation own_gen."""
        return lab.pk([lab.app(self.g, c, self.t) for c in lab.up(lab.run(self.own, own_gen))])

    def pulse(self, at):
        """the two cells of p> at the reader's own unit `at` (own even generation), placed."""
        return lab.pk([lab.app(self.g, c, self.t) for c in wires.pulse(self.p, at)])

    def runit(self, c):
        return unit(lab.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2])))

    def back(self, c):
        return lab.app(self.gi, (c[0] - self.t[0], c[1] - self.t[1], c[2] - self.t[2]))


def install(S, rd, settle=160):
    """store S at a generation divisible by 4 + the reader at its own generation phi.  Returns (verdict, state after
    `settle` generations)."""
    R = rd.cells(rd.phi)
    U = lab.union(S, R)
    if len(U) != len(S) + len(R):
        return 'overlap', None
    J = lab.run(U, settle)
    if not lab.same(lab.run(J, 4), J):
        return 'burn', None
    D = lab.up(lab.xor(J, U))
    if any(in_tube(c) for c in D):
        return 'store changed', None
    if any(abs(rd.runit(c) - rd.ur) > 6 for c in D):
        return 'reader changed', None
    return ('transparent' if not D else f'junction({len(D)})'), J


def read(J, rd, launch=-9, check=8, spacing=None):
    """one pulse (or two, `spacing` units apart) on the standing state J (generation divisible by 4).  Returns
    (what arrives, state 240 generations later, verdict)."""
    Y = lab.run(J, rd.phi)
    X = lab.xor(Y, rd.pulse(rd.ur + launch))
    if spacing:
        X = lab.xor(X, rd.pulse(rd.ur + launch - spacing))
    n1 = 2 * (check - launch)
    Xc = lab.run(X, n1); Yc = lab.run(Y, n1)
    D = lab.up(lab.xor(Xc, Yc))
    far = sorted(tr(rd.back(c), -(rd.ur + check)) for c in D if rd.runit(c) - rd.ur > 3)
    backw = sorted(tr(rd.back(c), -(rd.ur + check)) for c in D if rd.runit(c) - rd.ur < -3)
    free = sorted(wires.pulse(rd.p, 0))
    two = sorted(wires.pulse(rd.p, 0) + wires.pulse(rd.p, -spacing)) if spacing else None
    arr = 'pulse' if far == free else 'both pulses' if far == two else ('nothing' if not far else f'{len(far)} cells')
    if backw:
        arr += f' (+{len(backw)} back)'
    Xf = lab.run(Xc, 240 - n1 - rd.phi)
    if lab.same(Xf, J):
        return arr, Xf, 'restored'
    if not lab.same(lab.run(Xf, 4), Xf):
        return arr, None, 'not periodic'
    D = lab.up(lab.xor(Xf, J))
    if any(in_tube(c) for c in D):
        return arr, None, f'STORE changed ({len(D)})'
    if any(abs(rd.runit(c) - rd.ur) > 6 for c in D):
        return arr, None, f'reader changed ({len(D)})'
    return arr, Xf, f'mark({len(D)})'


def table(names=('r246', 'r132', 'r663', 'r549'), u=42, spacing=None):
    for name in names:
        print(f'reader {name} at unit {u}:' + (f' probe: two pulses {spacing} apart' if spacing else ''))
        for n in range(1, 7):
            S = standing(n)
            _, s = line.letters(S, 36, 52)
            rd = Reader(name, u)
            v, J = install(S, rd)
            row = f'  n={n}  units 36..51 {s}  install: {v}'
            if J is not None:
                for i in range(3):
                    arr, J2, verdict = read(J, rd, spacing=spacing)
                    row += f' | probe {i + 1}: {arr}, {verdict}'
                    if J2 is None:
                        break
                    J = J2
                st = lab.pk([c for c in lab.up(J) if in_tube(c)])
                _, s2 = line.letters(st, 36, 52)
                row += ' | store ' + ('unchanged' if s2 == s else 'CHANGED ' + s2)
            print(row)


def positions(names=('r246', 'r132', 'r663', 'r549')):
    for name in names:
        print(f'reader {name}: verdict of the first two pulses at each unit 34..52 (t transparent, j junction, X burn; P pulse arrives and all restored, e eaten and all restored, m a mark is left, s scattered and restored, ! other)')
        for n in range(1, 7):
            S = standing(n)
            _, s = line.letters(S, 34, 53)
            a = b = c = ''
            for u in range(34, 53):
                rd = Reader(name, u)
                v, J = install(S, rd)
                if J is None:
                    a += 'X'; b += ' '; c += ' '; continue
                a += v[0]
                for i, acc in enumerate(('b', 'c')):
                    arr, J2, verdict = read(J, rd)
                    ch = ('P' if arr == 'pulse' and verdict == 'restored' else 'e' if arr == 'nothing' and verdict == 'restored'
                          else 's' if verdict == 'restored' else 'm' if verdict.startswith('mark') else '!')
                    if i == 0:
                        b += ch
                    else:
                        c += ch
                    if J2 is None:
                        if i == 0:
                            c += ' '
                        break
                    J = J2
            print(f'  n={n}  line {s}\n       inst {a}\n       1st  {b}\n       2nd  {c}')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'table'
    if cmd == 'table':
        table()
    elif cmd == 'positions':
        positions()


def kymo(name, u, n, launches, T=80, every=2, settle=160):
    """launches: list of (generation, own unit relative to the crossing, cells) -- cells None: p>."""
    rd = Reader(name, u)
    S = standing(n)
    v, J = install(S, rd, settle)
    print(f'reader {name} at unit {u}, n = {n}: {v}')
    Y = lab.run(J, rd.phi); X = Y
    for t in range(T + 1):
        for (tl, at, cells) in launches:
            if tl == t:
                X = lab.xor(X, rd.pulse(rd.ur + at) if cells is None else lab.pk([lab.app(rd.g, c, rd.t) for c in wires.pulse(cells, rd.ur + at)]))
        if t % every == 0:
            cs = lab.up(X)
            st = lab.pk([c for c in cs if in_tube(c)])
            rr = lab.pk([c for c in (rd.back(c) for c in cs) if in_tube(c)])
            _, s1 = line.letters(st, 36, 50)
            _, s2 = line.letters(rr, -rd.nr - 4, rd.nr + 4)
            print(f'{t:4d}  {s1}  {s2}  diff {len(lab.xor(X, Y))}')
        X = lab.run(X, 1); Y = lab.run(Y, 1)
