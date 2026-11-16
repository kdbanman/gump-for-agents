#!/usr/bin/env python3
"""Caps of every pulse-carrying wire of the survey: does any end of any wire send anything back?

    python3 caps_any.py C [--wires 0-29] [--max 4000] [--survey ../scratch/signals/survey.jsonl] [--lo 1 --hi 5]

For each wire of the survey (one JSON line each: `bg`, `bg_period`, `defect` = its right-moving (2,1) pulse; the
file is written by `python3 survey.py 3 3 9 2 1 --max 30`), all caps inside the planes x+y-z <= C, x-y-z <= C are
enumerated by SAT as in caps.py (period = the wire's), up to --max, and each is hit once by the wire's pulse:
a wire 260 units long whose far end is simply cut (it burns, at most one unit per generation, and is too far to
matter in the 150 generations of the test), pulse launched 20 units from the cap, state compared with the
pulse-free run 60 and 80 generations after the pulse reaches the cap:
    eats      nothing differs
    changed   a difference at the cap only, the same at both times
    clock     a difference at the cap only, not the same at both times
    fire      the difference spreads (more than 12 units) and is contiguous
    back      a cluster of differing cells, separated from everything else by 4 clean units, that has moved 10 units
              towards -v between the two times: something travels back along the wire  <- what is looked for
"""
import argparse, json, sys, time
from collections import Counter
import numpy as np
import sg, plab, scat, caps

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)


class RawLab:
    def __init__(self, wire, lo, hi, C, L=260, KS=6):
        self.wire, self.L, self.KS = wire, L, KS
        self.body = [frozenset(scat.tr(c, k) for c in wire.bg[ph] for k in range(-L, KS)) for ph in range(wire.P)]
        self.g = sg.Geom([], [(S1, lo, hi), (S2, lo, hi), (S3, -4 * L - 40, C), (S4, -4 * L - 40, C)], seeds=list(self.body[0]))

    def diff(self, x, z, umin):
        return [c for c in (self.g.cells[i] for i in np.nonzero((x != z)[:self.g.n])[0]) if scat.unit(c) >= umin]

    def shoot(self, cap, k_launch=-20):
        g = self.g; wire = self.wire; KS = self.KS
        z = g.state(self.body[0] | frozenset(cap))
        x = z.copy()
        for c in wire.pulse_cells('R', 0, k_launch):
            x[g.index[c]] ^= 1
        t1 = 2 * (KS - k_launch) + 60
        x = g.run(x, t1, sparse=True); z = g.run(z, t1, sparse=True)
        umin = -self.L + t1 + 40
        d = self.diff(x, z, umin)
        if not d:
            return 'eats', None
        us = sorted(set(scat.unit(c) for c in d))
        if us[-1] - us[0] > 20 and len(us) > 12:
            return 'fire', None
        x2 = g.run(x, 20, sparse=True); z2 = g.run(z, 20, sparse=True)
        d2 = frozenset(self.diff(x2, z2, umin))
        cl = [[us[0], us[0]]]
        for u in us[1:]:
            if u - cl[-1][1] >= 5:
                cl.append([u, u])
            else:
                cl[-1][1] = u
        if cl[0][1] < KS - 8:
            away = frozenset(c for c in d if scat.unit(c) <= cl[0][1])
            moved = frozenset(scat.tr(c, -10) for c in away)
            if moved <= d2 and not any(cl[0][0] - 14 <= scat.unit(c) <= cl[0][1] - 6 for c in d2 - moved):
                return 'back', dict(cells=sorted(away), rest=len(d) - len(away))
            return 'fire', None
        return ('changed' if frozenset(d) == d2 else 'clock'), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('C', type=int); ap.add_argument('--wires', default='0-29'); ap.add_argument('--max', type=int, default=4000)
    ap.add_argument('--survey', default='../scratch/signals/survey.jsonl'); ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--out', default='../scratch/signals/caps_any.jsonl')
    a = ap.parse_args()
    S = [json.loads(l) for l in open(a.survey)]
    lo_, hi_ = map(int, a.wires.split('-')) if '-' in a.wires else (int(a.wires), int(a.wires))
    for w in range(lo_, hi_ + 1):
        ob = S[w]
        wire = scat.Wire(ob, None)
        t0 = time.time()
        cs, status, nfree = caps.enumerate_caps(wire, a.C, a.lo, a.hi, 6, wire.P, a.max, 1200, verbose=False)
        lab = RawLab(wire, a.lo, a.hi, a.C)
        res = Counter(); backs = []
        for cap in cs:
            v, info = lab.shoot(cap)
            res[v] += 1
            if v == 'back':
                backs.append(dict(cap=[list(c) for c in cap], cells=[list(c) for c in info['cells']], rest=info['rest']))
        print(f'wire {w} ({len(ob["bg"])} cells per unit, pulse of {len(ob["defect"])}): {len(cs)} caps ({status}, {nfree} free cells, C={a.C}): {dict(res)}  {time.time() - t0:.0f}s', flush=True)
        for b in backs[:3]:
            print('    BACK: cap', b['cap'], 'returns', b['cells'], 'rest', b['rest'], flush=True)
        with open(a.out, 'a') as f:
            f.write(json.dumps(dict(wire=w, C=a.C, lo=a.lo, hi=a.hi, status=status, ncaps=len(cs), res=dict(res), backs=backs)) + '\n')


if __name__ == '__main__':
    main()
