#!/usr/bin/env python3
"""push 8b: a reader wire PARALLEL to push 7's standing line, at every transverse offset, alongside the stored stretch.

    python3 survey3.py READER [--ns 1,3] [--out FILE]

Store: line.standing(n) for each n given (n = 1: plain wire B; n = 3: units 41..43 wire B', unit 44 the edge unit).
Reader: a capped wire (B or C) on its own units -14..13, placed as x -> g(x) + t after phi generations, g one of the 8
symmetries with g(v) = +-v, t = (2a, 2b, 2c) with c chosen so that the reader's unit 0 lies at store unit 42 or 43
(both: the two alignments differ when g reverses the wire or mixes the two slabs of a unit); all (a, b) for which some
cell has neighbours in both footprints.  The pulse is put on at the reader's unit -9 and looked for at unit +9:
it runs past the whole stretch.  Outcomes as survey2.py.  One JSON line per placement and n."""
import argparse, json, os, sys, time
import lab, wires, line
from lab import tr, unit
from survey import inv, footprint
import survey2
from survey2 import in_tube

NR = 14
U0, U1 = 9, 9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--ns', default='1,3'); ap.add_argument('--out')
    a = ap.parse_args()
    ns = [int(x) for x in a.ns.split(',')]
    out = a.out or os.path.join(lab.SCR, f'survey3_{a.reader}.jsonl')
    P = survey2.Probe(a.reader, 3)
    stores = {n: line.standing(n, 900) for n in ns}
    HS = lab.halo({tr(c, u) for c in P.FS0 for u in range(20, 64)})
    t0 = time.time(); cnt = 0
    f = open(out, 'w')
    for gi_, g in enumerate(lab.SYMS):
        r = lab.appv(g, lab.V)
        if r not in ((1, 0, -1), (-1, 0, 1)):
            continue
        gi = inv(g)
        HR0 = [lab.app(g, c) for c in P.FRh]
        for a_ in range(-9, 10):
            for b_ in range(-9, 10):
                for c_ in range(-9, 10):
                    # normalise the slide along v: the image of the reader's unit-0 cell (0,1,2) lies in store unit 42 or 43
                    t = (2 * a_, 2 * b_, 2 * c_)
                    p0 = lab.app(g, (0, 1, 2), t)
                    if unit(p0) != 0:
                        continue
                    if not any((p[0] + t[0] + 84, p[1] + t[1], p[2] + t[2] - 84) in HS for p in HR0):
                        continue
                    for al in (42, 43):
                        tt = (t[0] + 2 * al, t[1], t[2] - 2 * al)
                        for phi in (0, 1):
                            R0 = P.reader(g, phi, tt)
                            for n in ns:
                                rec = dict(reader=a.reader, n=n, g=gi_, phi=phi, t=list(tt), al=al)
                                S0 = stores[n]
                                U = lab.union(S0, R0)
                                rec['overlap'] = len(S0) + len(R0) - len(U)
                                ok = rec['overlap'] == 0
                                if ok:
                                    x, s, rr = U, S0, R0
                                    for _ in range(4):
                                        x = lab.run(x, 1); s = lab.run(s, 1); rr = lab.run(rr, 1)
                                        if not lab.same(x, lab.union(s, rr)):
                                            ok = False; break
                                if ok:
                                    rec['static'] = 'transparent'; Y = U
                                else:
                                    J = lab.run(U, 200)
                                    if not lab.same(lab.run(J, 4), J):
                                        rec['static'] = 'burn'; f.write(json.dumps(rec) + '\n'); cnt += 1; continue
                                    D = lab.up(lab.xor(J, U))
                                    rec['static'] = 'junction'; rec['jdiff'] = len(D)
                                    rec['jstore'] = sum(1 for c in D if in_tube(c))
                                    # a junction must leave both wires recognisable: the store's letters unchanged
                                    Y = J
                                rec['pulse'] = []
                                for delay in (0, 2):
                                    Yt = lab.run(Y, phi + delay)
                                    pc = [lab.app(g, c, tt) for c in wires.pulse(P.pulse, -U0)]
                                    X = lab.xor(Yt, lab.pk(pc))
                                    n1 = 2 * (U0 + U1)
                                    Xc = lab.run(X, n1); Yc = lab.run(Yt, n1)
                                    D = lab.up(lab.xor(Xc, Yc))
                                    o = {}
                                    sid = P.signal_id(D, g, tt, U1)
                                    if sid == P.free:
                                        o['check'] = 'pass'
                                    elif not D:
                                        o['check'] = 'gone'
                                    else:
                                        o['check'] = [list(c) for c in sid] if len(sid) <= 12 else f'{len(sid)} cells'
                                    n2 = 2 * (NR - U1) + 72
                                    Xf = lab.run(Xc, n2); Yf = lab.run(Yc, n2)
                                    D = lab.up(lab.xor(Xf, Yf))
                                    if not D:
                                        o['final'] = 'restored'
                                    else:
                                        o['final'] = dict(n=len(D), store=sum(1 for c in D if in_tube(c)))
                                    rec['pulse'].append(o)
                                f.write(json.dumps(rec) + '\n'); cnt += 1
    f.close()
    print(f'{cnt} runs in {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
