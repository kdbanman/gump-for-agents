#!/usr/bin/env python3
"""push 8b: every non-parallel placement of a signal-carrying wire beside wire B and beside wire B'.

    python3 survey.py READER [--out FILE] [--only g,phi]      READER = B (pulse B) or C (pulse p>) or Cw (the wide pulse)

Store: a capped wire B on units -14..13 along v = (1,0,-1) (wires.capped_B), and the capped wire B' that stands in
the same tube at the same generation (SIGB of it, one generation on: the phase in which B' stands beside B in a
line).  Reader: a capped wire (B or C) on its own units -18..17 carrying its right-going pulse; placed as
x -> g(x) + t after phi generations of its own, g one of the 48 symmetries with g(v) != +-v (40 of them), phi = 0, 1,
t an even vector.  Because the reader's left-going pulse is the image of the right-going one under a symmetry of the
wire (half-turn for B, the mirror one generation on for C), all directions and both pulses are covered.
Placements are taken modulo sliding either wire along itself (t mod <2v, 2g(v)>); all classes are listed in which
some cell has, at some time, neighbours in both footprints (footprint: every cell ever live in the wire, with the
pulse passing, for B and B' stores alike).  Beyond that list the two are exactly independent.

Per placement and store (B, B'):
  static   'transparent': S(t) u R(t) is an orbit (checked for 2 generations; both have period 2)
           'junction':    not transparent, but at generation 200 the state has period <= 8 and differs from S u R only
                          near the crossing (store units and reader units within 7 of it)
           'burn':        anything else (with what is left of each wire)
  pulse    (transparent and junction only) the right-going pulse put on the reader 9 units before the crossing; the
           difference X(t) xor Y(t) from the same state without pulse, when the pulse should be 7 units beyond the
           crossing: 'pass' (exactly the free pulse, on time), 'gone' (no difference), or a description; and at the
           end (pulse swallowed by the far cap): 'restored' (no difference) or a description.
Output: one JSON line per placement.
"""
import argparse, json, os, sys, time
import numpy as np
import lab, wires, line
from lab import tr, unit

NS, NR = 14, 18
U0, U1 = 9, 7          # launch U0 reader units before the crossing; checkpoint U1 units beyond


def inv(g):
    perm, sg = g
    ip = [0, 0, 0]; isg = [0, 0, 0]
    for i in range(3):
        ip[perm[i]] = i; isg[perm[i]] = sg[i]
    return (tuple(ip), tuple(isg))


def reader_spec(name):
    if name == 'B':
        cells = wires.capped_B(-NR, NR); pulse = lab.PULSE_B; wire0 = lab.B0
    elif name == 'C':
        cells = wires.capped_C(-NR, NR); pulse = lab.PULSE_C; wire0 = lab.C0
    elif name == 'Cw':
        cells = wires.capped_C(-NR, NR); pulse = [tuple(c) for c in lab.load('pulse-C-wide')['defect']]; wire0 = lab.C0
    else:
        raise ValueError(name)
    return cells, pulse, wire0


def footprint(cells, pulse, ua, ub):
    """every cell ever live in units ua..ub-1 while a pulse crosses the capped wire `cells` (own frame)."""
    k = lab.pk(cells)
    x = lab.xor(k, lab.pk(wires.pulse(pulse, ua - 4)))
    seen = set()
    for t in range(2 * (ub - ua) + 16):
        seen.update(c for c in lab.up(x) if ua <= unit(c) < ub)
        x = lab.run(x, 1)
    return seen


def store_cells(kind):
    sb = wires.capped_B(-NS, NS)
    if kind == 'B':
        return lab.pk(sb)
    return lab.run(lab.pk([wires.SIGB(c) for c in sb]), 1)


def canon(tc, r):
    """representative of the cube vector tc modulo <v, r> of least norm (ties: lexicographic)."""
    best = None
    for i in range(-14, 15):
        for j in range(-14, 15):
            c = (tc[0] + i + j * r[0], tc[1] + j * r[1], tc[2] - i + j * r[2])
            key = (c[0] * c[0] + c[1] * c[1] + c[2] * c[2], c)
            if best is None or key < best:
                best = key
    return best[1]


def describe(D, g, t, us, ur):
    """D: list of cells.  store-unit and reader-unit ranges relative to the crossing."""
    if not D:
        return dict(n=0)
    gi = inv(g)
    su = [unit(c) - us for c in D]
    ru = [unit(lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2]))) - ur for c in D]
    return dict(n=len(D), su=[min(su), max(su)], ru=[min(ru), max(ru)])


def placements(name, R=7):
    """yield (g, phi, t) for all interacting classes."""
    rc, pulse, wire0 = reader_spec(name)
    FR = footprint(rc, pulse, -9, 9)
    FS = set()
    for kind in ('B', 'Bp'):
        k = store_cells(kind)
        for ph in range(2):
            FS.update(c for c in lab.up(k) if -9 <= unit(c) < 9)
            k = lab.run(k, 1)
    # the store's own pulses do not matter here: the store carries none in this survey
    HS = lab.halo(FS)
    for gi_, g in enumerate(lab.SYMS):
        r = lab.appv(g, lab.V)
        if r in ((1, 0, -1), (-1, 0, 1)):
            continue
        HR0 = [lab.app(g, c) for c in lab.halo(FR)]
        seen = set()
        for a in range(-R, R + 1):
            for b in range(-R, R + 1):
                for c in range(-R, R + 1):
                    tc = canon((a, b, c), r)
                    if tc in seen:
                        continue
                    seen.add(tc)
                    t = (2 * tc[0], 2 * tc[1], 2 * tc[2])
                    if any((p[0] + t[0], p[1] + t[1], p[2] + t[2]) in HS for p in HR0):
                        for phi in (0, 1):
                            yield gi_, phi, t


def crossing(g, t, FRh, HS):
    """mean store unit and reader unit of the cells in both halos."""
    gi = inv(g)
    both = [(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in FRh]
    both = [p for p in both if p in HS]
    us = round(sum(unit(p) for p in both) / len(both))
    ur = round(sum(unit(lab.app(gi, (p[0] - t[0], p[1] - t[1], p[2] - t[2]))) for p in both) / len(both))
    return us, ur


class Lab:
    def __init__(self, name):
        self.name = name
        self.rc, self.pulse, self.wire0 = reader_spec(name)
        self.rk = lab.pk(self.rc)
        self.stores = {kind: store_cells(kind) for kind in ('B', 'Bp')}
        self.stores1 = {kind: lab.run(self.stores[kind], 1) for kind in self.stores}
        FR = footprint(self.rc, self.pulse, -9, 9)
        self.FRh = lab.halo(FR)
        FS = set()
        for kind in ('B', 'Bp'):
            k = self.stores[kind]
            for ph in range(2):
                FS.update(c for c in lab.up(k) if -9 <= unit(c) < 9)
                k = lab.run(k, 1)
        self.HS = lab.halo(FS)

    def place(self, cells_k, g, t):
        return lab.pk([lab.app(g, c, t) for c in lab.up(cells_k)])

    def reader(self, g, phi, t, pulse_at=None):
        """the placed reader at global generation 0 (its own generation phi); with the pulse at own unit pulse_at
        (own generation 0) if given."""
        k = self.rk
        if pulse_at is not None:
            k = lab.xor(k, lab.pk(wires.pulse(self.pulse, pulse_at)))
        k = lab.run(k, phi)
        return self.place(k, g, t)

    def run_one(self, gi_, phi, t, T1=200):
        g = lab.SYMS[gi_]
        HRg = [lab.app(g, c) for c in self.FRh]
        us, ur = crossing(g, t, HRg, self.HS)
        rec = dict(reader=self.name, g=gi_, phi=phi, t=list(t), axis=list(lab.appv(g, lab.V)), us=us, ur=ur, res={})
        R0 = self.reader(g, phi, t); R1 = lab.run(R0, 1)
        gi = inv(g)
        for kind in ('B', 'Bp'):
            S0, S1 = self.stores[kind], self.stores1[kind]
            out = {}
            U = lab.union(S0, R0); U1_ = lab.union(S1, R1)
            out['overlap'] = len(S0) + len(R0) - len(U)
            if out['overlap'] == 0 and lab.same(lab.run(U, 1), U1_) and lab.same(lab.run(U1_, 1), U):
                out['static'] = 'transparent'; Y = U; base = 0
            else:
                J = lab.run(U, T1)
                per = next((p for p in (1, 2, 4, 8) if lab.same(lab.run(J, p), J)), None)
                D = lab.up(lab.xor(J, U))
                d = describe(D, g, t, us, ur)
                out['settle'] = dict(period=per, **d)
                if per is not None and d['n'] and max(abs(d['su'][0]), abs(d['su'][1]), abs(d['ru'][0]), abs(d['ru'][1])) <= 7:
                    out['static'] = 'junction'; out['junction_cells'] = len(J) - len(U); Y = J; base = T1
                    out['period'] = per
                elif per is not None and d['n'] == 0:
                    out['static'] = 'transient'; Y = J; base = T1      # disturbed, then exactly the union again
                else:
                    out['static'] = 'burn'
                    # what is left: is the store's far part / the reader's far part as it was
                    Jc = set(lab.up(J));
                    sfar = [c for c in lab.up(S0) if abs(unit(c) - us) > 9]
                    rfar = [c for c in lab.up(R0) if abs(unit(lab.app(gi, (c[0] - t[0], c[1] - t[1], c[2] - t[2]))) - ur) > 12]
                    out['store_far_intact'] = all(c in Jc for c in sfar)
                    out['reader_far_intact'] = all(c in Jc for c in rfar)
                    rec['res'][kind] = out
                    continue
            # the pulse: put on at reader-own generation 0, i.e. global generation tau with tau + phi even
            tau = base + phi
            Yt = lab.run(Y, phi)
            pc = [lab.app(g, c, t) for c in wires.pulse(self.pulse, ur - U0)]
            X = lab.xor(Yt, lab.pk(pc))
            n1 = 2 * (U0 + U1)
            Xc = lab.run(X, n1); Yc = lab.run(Yt, n1)
            D = lab.xor(Xc, Yc)
            free = lab.pk([lab.app(g, c, t) for c in wires.pulse(self.pulse, ur + U1)])
            if lab.same(D, free):
                out['check'] = 'pass'
            elif len(D) == 0:
                out['check'] = 'gone'
            else:
                out['check'] = describe(lab.up(D), g, t, us, ur)
            n2 = 2 * (NR + 4) + 120
            Xf = lab.run(Xc, n2); Yf = lab.run(Yc, n2)
            D = lab.xor(Xf, Yf)
            if len(D) == 0:
                out['final'] = 'restored'
            else:
                per = next((p for p in (1, 2, 4, 8) if lab.same(lab.run(Xf, p), Xf)), None)
                out['final'] = dict(period=per, **describe(lab.up(D), g, t, us, ur))
            rec['res'][kind] = out
        return rec


def sig(o):
    if o['static'] == 'burn':
        return 'burn'
    c = o['check'] if isinstance(o['check'], str) else 'other'
    f = o['final'] if isinstance(o['final'], str) else 'changed'
    return f"{o['static']}:{c}:{f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--out'); ap.add_argument('--R', type=int, default=7)
    a = ap.parse_args()
    out = a.out or os.path.join(lab.SCR, f'survey_{a.reader}.jsonl')
    L = Lab(a.reader)
    t0 = time.time(); n = 0
    from collections import Counter
    cnt = Counter()
    with open(out, 'w') as f:
        for gi_, phi, t in placements(a.reader, a.R):
            rec = L.run_one(gi_, phi, t)
            f.write(json.dumps(rec) + '\n'); n += 1
            cnt[(sig(rec['res']['B']), sig(rec['res']['Bp']))] += 1
    print(f'{n} placements in {time.time() - t0:.0f} s -> {out}')
    for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]):
        print(f'  {v:6d}  B: {k[0]:40s} B\': {k[1]}')


if __name__ == '__main__':
    main()
