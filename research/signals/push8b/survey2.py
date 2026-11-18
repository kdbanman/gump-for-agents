#!/usr/bin/env python3
"""push 8b: a reader wire at every non-parallel placement beside push 7's standing line, at every unit near the stored
stretch.

    python3 survey2.py READER [--n 3] [--ulo 37] [--uhi 49] [--part i/m] [--out FILE]

Store: push 7's line (gun 4, end 70, N = 80) after E and n holes, at generation 900 (line.standing; wire B from unit 4
to unit 79, with the stretch p..p f at units 41..41+n: p = a unit of wire B', f = the edge unit, all four sites).
Reader and placements: as survey.py (the classes of t modulo sliding either wire), each moved along the store so that
the crossing (mean store unit of the cells in both halos) is at every unit ulo..uhi.
Per placement and position:
  static   'transparent' (store and reader together are the union of the two alone for 4 generations; the line has
           period 4), 'junction' (at generation 160 the state has period dividing 4 and differs from the union only
           within 7 units of the crossing; includes the case of no difference at that generation), else 'burn'
  pulse    for each launch delay 0, 2: the reader's right-going pulse put on 8 units before the crossing; when it
           should be 6 units beyond, the difference from the pulse-free run, in the reader's frame relative to the
           free pulse: 'pass', 'gone', or a signal id / description; at the end (100 generations later): 'restored'
           or what differs (and whether any cell of the store's tube differs).
Output: JSON lines.  `python3 reads.py` lists the placements where two neighbouring positions give different clean
outcomes (a read)."""
import argparse, json, os, sys, time
import numpy as np
import lab, wires, line
from lab import tr, unit
from survey import inv, reader_spec, footprint, canon

NR = 14
U0, U1 = 8, 6


def in_tube(c):
    return 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5


class Probe:
    def __init__(self, name, n=3, gen=900):
        self.name = name
        if name == 'B':
            self.rc = wires.capped_B(-NR, NR); self.pulse = lab.PULSE_B
        elif name == 'C':
            self.rc = wires.capped_C(-NR, NR); self.pulse = lab.PULSE_C
        else:
            raise ValueError(name)
        self.rk = lab.pk(self.rc)
        self.store = line.standing(n, gen)
        self.n = n
        FR = footprint(self.rc, self.pulse, -8, 8)
        self.FRh = lab.halo(FR)
        # the store's footprint in the frame of one unit: all cells ever live in wire B, B' or the edge unit
        FS = set()
        k = self.store
        for ph in range(2):
            FS.update(tr(c, -unit(c)) for c in lab.up(k) if 20 <= unit(c) < 60)
            k = lab.run(k, 1)
        self.FS0 = FS
        self.HS = lab.halo({tr(c, u) for c in FS for u in range(-9, 9)})
        self.free = tuple(sorted(wires.pulse(self.pulse, 0)))

    def classes(self, R=7):
        """(g index, phi, t, us, ur): t canonical with the crossing near store unit 0."""
        for gi_, g in enumerate(lab.SYMS):
            r = lab.appv(g, lab.V)
            if r in ((1, 0, -1), (-1, 0, 1)):
                continue
            HR0 = [lab.app(g, c) for c in self.FRh]
            gi = inv(g)
            seen = set()
            for a in range(-R, R + 1):
                for b in range(-R, R + 1):
                    for c in range(-R, R + 1):
                        tc = canon((a, b, c), r)
                        if tc in seen:
                            continue
                        seen.add(tc)
                        t = (2 * tc[0], 2 * tc[1], 2 * tc[2])
                        both = [(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in HR0]
                        both = [p for p in both if p in self.HS]
                        if both:
                            us = round(sum(unit(p) for p in both) / len(both))
                            ur = round(sum(unit(lab.app(gi, (p[0] - t[0], p[1] - t[1], p[2] - t[2]))) for p in both) / len(both))
                            for phi in (0, 1):
                                yield gi_, phi, t, us, ur

    def reader(self, g, phi, t):
        return lab.pk([lab.app(g, c, t) for c in lab.up(lab.run(self.rk, phi))])

    def signal_id(self, D, g, t, ur_check):
        """D (cells) in the reader's frame, moved back by ur_check units."""
        gi = inv(g)
        out = sorted(tr(lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2])), -ur_check) for c in D)
        return tuple(out)

    def run_one(self, gi_, phi, t, ur, u, us0, T1=160):
        """the placement (g, phi, t) moved k = u - us0 units along the store: crossing at store unit u."""
        g = lab.SYMS[gi_]; gi = inv(g)
        k = u - us0
        tt = (t[0] + 2 * k, t[1], t[2] - 2 * k)
        rec = dict(reader=self.name, n=self.n, g=gi_, phi=phi, t=list(tt), u=u, ur=ur)
        S0 = self.store; R0 = self.reader(g, phi, tt)
        U = lab.union(S0, R0)
        rec['overlap'] = len(S0) + len(R0) - len(U)
        tr_ok = rec['overlap'] == 0
        if tr_ok:
            a, s, r = U, S0, R0
            for _ in range(4):
                a = lab.run(a, 1); s = lab.run(s, 1); r = lab.run(r, 1)
                if not lab.same(a, lab.union(s, r)):
                    tr_ok = False; break
        if tr_ok:
            rec['static'] = 'transparent'; Y = U
        else:
            J = lab.run(U, T1)
            if not lab.same(lab.run(J, 4), J):
                rec['static'] = 'burn'; return rec
            D = lab.up(lab.xor(J, U))
            su = [unit(c) - u for c in D]
            ru = [unit(lab.app(gi, (c[0] - tt[0], c[1] - tt[1], c[2] - tt[2]))) - ur for c in D]
            if D and max(max(map(abs, su)), max(map(abs, ru))) > 7:
                rec['static'] = 'burn'; return rec
            rec['static'] = 'junction'; rec['jdiff'] = len(D); rec['jper'] = 2 if lab.same(lab.run(J, 2), J) else 4
            Y = J
        rec['pulse'] = []
        for delay in (0, 2):
            Yt = lab.run(Y, phi + delay)
            pc = [lab.app(g, c, tt) for c in wires.pulse(self.pulse, ur - U0)]
            X = lab.xor(Yt, lab.pk(pc))
            n1 = 2 * (U0 + U1)
            Xc = lab.run(X, n1); Yc = lab.run(Yt, n1)
            D = lab.up(lab.xor(Xc, Yc))
            o = {}
            sid = self.signal_id(D, g, tt, ur + U1)
            if sid == self.free:
                o['check'] = 'pass'
            elif not D:
                o['check'] = 'gone'
            else:
                o['check'] = [list(c) for c in sid] if len(sid) <= 12 else f'{len(sid)} cells'
                o['check_store'] = sum(1 for c in D if in_tube(c))
            n2 = 2 * (NR - U1) + 72
            Xf = lab.run(Xc, n2); Yf = lab.run(Yc, n2)
            D = lab.up(lab.xor(Xf, Yf))
            if not D:
                o['final'] = 'restored'
            else:
                o['final'] = dict(n=len(D), store=sum(1 for c in D if in_tube(c)), per4=lab.same(lab.run(Xf, 4), Xf))
                if len(D) <= 12:
                    o['final']['cells'] = [list(c) for c in D]
            rec['pulse'].append(o)
        return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--n', type=int, default=3)
    ap.add_argument('--ulo', type=int, default=37); ap.add_argument('--uhi', type=int, default=49)
    ap.add_argument('--part', default='0/1'); ap.add_argument('--out')
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    out = a.out or os.path.join(lab.SCR, f'survey2_{a.reader}_n{a.n}_{pi}of{pm}.jsonl')
    P = Probe(a.reader, a.n)
    t0 = time.time(); cnt = 0
    with open(out, 'w') as f:
        for j, (gi_, phi, t, us, ur) in enumerate(P.classes()):
            if j % pm != pi:
                continue
            for u in range(a.ulo, a.uhi + 1):
                rec = P.run_one(gi_, phi, t, ur, u, us)
                rec['cls'] = j
                f.write(json.dumps(rec) + '\n'); cnt += 1
            f.flush()
    print(f'{cnt} runs in {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
