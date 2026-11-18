#!/usr/bin/env python3
"""place.py (audit of push 8b, q.c): every non-parallel placement of a second wire beside the store, recounted
with the audit's own enumeration, and what one pulse and a pair of pulses do there.

    python3 place.py count                  placements per reader (the push: 1056 for wire B and for wire C)
    python3 place.py survey B|C [--part i/m]  -> out/place_{B,C}_{i}of{m}.jsonl: one line per placement

Enumeration.  Store: wire B (or B') along v = (1,0,-1) in its own frame.  Reader: the reader's own wire mapped by
c -> g(c) + t, g one of the 48 signed permutations with g(v) != +-v, t an even vector, at relative phase 0 or 1 (the
reader at its own generation `phase` when the store is at an even generation).  Two t are the same placement when
they differ by 2a v + 2b g(v) (a slide along either wire).  A placement is kept when some lattice cell has a neighbour
in the store's footprint (the cells of wire B or wire B' at either phase) and a neighbour in the reader's footprint
(the cells ever live on the reader with or without one of its pulses passing: the push's definition).  Placements whose cells collide are found at install ('overlap').  Each kept placement is slid along both wires so that the interaction is centred at store unit 0 and at the
reader's own unit 0 (`ur` = 0).

Survey of one placement, beside two stores (plain capped wire B, 56 units; the same with a stretch of 40 units of
wire B' over the crossing):
  stand     the joint state is of period <= 4 after 80 generations, the store's tube as alone, and the reader changed
            only within 6 own units of the crossing ('union' if the joint state is the union at every generation)
  one pulse from the left end (right-going) and from the right end (left-going), launched 9 units from the crossing:
            what is travelling 44 generations later (own frame, outside 3 units of the crossing) and whether the whole
            object is restored 240 generations later
  pairs     the same for two pulses s = 1..8 units apart from either end
"""
import argparse, json, os, sys, time
import numpy as np
import qa, rd
from qa import pk, up, run, xor, union, same, tr, unit

V = (1, 0, -1)
CLK = qa.jload(os.path.join(qa.SIG, 'objects', 'clock-C.json'))
C_CAPL = [tuple(c) for c in CLK['capL']]; C_CAPR = [tuple(c) for c in CLK['capR']]


def capped_C(ua, ub):
    cells = [tr(c, ua) for c in C_CAPL] + [tr(c, ub) for c in C_CAPR]
    for u in range(ua, ub):
        cells += qa.unit_cells(rd.C, u)
    return sorted(set(cells))


def cR(u):
    """p> of wire C at unit u: 9f."""
    return [tr((1, 0, 2), u), tr((1, 0, 4), u + 1)]


def cL(u):
    """p< of wire C at unit u: the unit becomes 7."""
    return [tr((0, 2, 3), u), tr((1, 0, 4), u)]


NR = 18
READER = {'B': dict(own=rd.capped(-NR, NR), R=rd.pR, L=rd.pL, digit=rd.B),
          'C': dict(own=capped_C(-NR, NR), R=cR, L=cL, digit=rd.C)}


def footprint(digit, ua, ub):
    k = pk([c for u in range(ua, ub) for c in qa.unit_cells(digit, u)])
    k1 = run(k, 1)
    # keep the middle: the ends of a bare wire burn inwards at one unit per generation at most
    return {c for c in up(k) + up(k1) if ua + 3 <= unit(c) < ub - 3}


def halo(F, incl=False):
    h = set(F) if incl else set()
    for c in F:
        h.update(qa.nbrs(c))
    return h


FS = footprint(rd.B, -30, 30) | footprint(rd.BP, -30, 30)
HS = halo(FS)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def in_lattice(d, v, w):
    """is d = a v + b w with integers a, b?"""
    A = np.array([v, w], dtype=float).T
    sol, res, rk, sv = np.linalg.lstsq(A, np.array(d, dtype=float), rcond=None)
    a, b = round(sol[0]), round(sol[1])
    return all(a * v[i] + b * w[i] == d[i] for i in range(3))


def reader_footprint(kind):
    """cells ever live on the reader's units -27..26 at either phase, with either of its pulses passing or without."""
    L = READER[kind]
    k = pk(rd.capped(-40, 40) if kind == 'B' else capped_C(-40, 40))
    seen = set()
    for cells in ([], L['R'](-34), L['L'](34)):
        x = xor(k, pk(cells))
        for t in range(140):
            seen.update(c for c in up(x) if -27 <= unit(c) < 27)
            x = run(x, 1)
    return seen


def placements(kind, radius=9, pulses=True):
    """list of (g index in qa.SYMS, t, phase, ur)."""
    FRown = reader_footprint(kind) if pulses else footprint(READER[kind]['digit'], -30, 30)
    out = []
    for gi, g in enumerate(qa.SYMS):
        w = qa.app(g, V)
        if w == V or w == (-1, 0, 1):
            continue
        n = cross(V, w)
        classes = {}
        rng = range(-radius, radius + 1)
        for a in rng:
            for b in rng:
                for c in rng:
                    h = (a, b, c)
                    key = n[0] * a + n[1] * b + n[2] * c
                    lst = classes.setdefault(key, [])
                    if not any(in_lattice((a - x[0], b - x[1], c - x[2]), V, w) for x in lst):
                        lst.append(h)
        FRg = [qa.app(g, c) for c in FRown]
        for key in sorted(classes):
            for h in classes[key]:
                t = (2 * h[0], 2 * h[1], 2 * h[2])
                FR = {(c[0] + t[0], c[1] + t[1], c[2] + t[2]) for c in FRg}
                HR = halo(FR)
                both = HR & HS
                if not both:
                    continue
                # centre: mean store unit and mean reader unit of the cells that see both wires
                P = rd.Placement(g, t)
                us = round(sum(unit(c) for c in both) / len(both))
                P = P.moved(-us)
                ur = round(sum(unit(P.back((c[0] - 2 * us, c[1], c[2] + 2 * us))) for c in both) / len(both))
                # slide the reader along itself so that its own crossing unit is 0
                P = rd.Placement(g, (P.t[0] + 2 * ur * w[0], P.t[1] + 2 * ur * w[1], P.t[2] + 2 * ur * w[2]))
                ur = 0
                for phase in (0, 1):
                    out.append((gi, P.t, phase, ur))
    return out


def stores():
    SB = pk(rd.capped(-28, 28))
    SBP = pk(rd.capped(-28, 28, '7' * 8 + 'd' * 40 + 'f' + '7' * 7))
    return {'B': SB, 'Bp': SBP}


def stand(S, P, own, ur):
    v, J, R = rd.install(S, P, own, settle=80)
    if J is None or v == 'store':
        return v, None
    if v == 'junction':
        d = xor(J, union(run(S, 80), run(R, 80)))
        if any(abs(unit(P.back(c)) - ur) > 6 for c in up(d)):
            return 'reader', None
    return v, J


def probe(J, P, ur, cells, delay=0):
    Y = run(J, delay + P.phase)
    X = xor(Y, pk(P(cells)))
    X44, Y44 = run(X, 44), run(Y, 44)
    out = sorted(tr(P.back(c), -ur) for c in up(xor(X44, Y44)) if abs(unit(P.back(c)) - ur) > 3)
    Xf = run(X44, 240 - 44 - delay - P.phase)
    return out, same(Xf, J)


def survey(kind, pi, pm, out):
    L = READER[kind]; S = stores(); t0 = time.time()
    pl = placements(kind)
    with open(out, 'w') as f:
        for j, (gi, t, phase, ur) in enumerate(pl):
            if j % pm != pi:
                continue
            P = rd.Placement(gi, t, phase)
            rec = dict(reader=kind, g=gi, t=list(t), phase=phase, ur=ur, stand={}, one={}, pairs={})
            Js = {}
            for k in S:
                v, J = stand(S[k], P, L['own'], ur)
                rec['stand'][k] = v; Js[k] = J
            if all(J is not None for J in Js.values()):
                for side in 'LR':
                    mk = (lambda j: L['R'](ur - 9 - j)) if side == 'L' else (lambda j: L['L'](ur + 9 + j))
                    for s in range(0, 9):
                        cells = mk(0) + (mk(s) if s else [])
                        r = {k: probe(Js[k], P, ur, cells) for k in Js}
                        val = {k: [r[k][0], r[k][1]] for k in r}
                        if s == 0:
                            rec['one'][side] = val
                        else:
                            rec['pairs'][f'{side}{s}'] = dict(read=bool(r['B'][1] and r['Bp'][1] and r['B'][0] != r['Bp'][0]),
                                                              n=[len(r['B'][0]), len(r['Bp'][0])], ok=[r['B'][1], r['Bp'][1]])
            f.write(json.dumps(rec) + '\n'); f.flush()
    print(f'{kind} part {pi}/{pm}: {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('kind', nargs='?', default='B'); ap.add_argument('--part', default='0/1')
    a = ap.parse_args()
    if a.cmd == 'count':
        for kind in 'BC':
            t0 = time.time()
            pl = placements(kind)
            pl0 = placements(kind, pulses=False)
            print(f'reader {kind}: without the pulses in the footprint {len(pl0)} placements')
            from collections import Counter
            print(f'reader {kind}: {len(pl)} placements ({len(set(p[0] for p in pl))} symmetries, both phases); per symmetry: {sorted(Counter(Counter(p[0] for p in pl).values()).items())}  ({time.time() - t0:.0f} s)')
    else:
        pi, pm = map(int, a.part.split('/'))
        survey(a.kind, pi, pm, os.path.join(qa.SCR, f'place_{a.kind}_{pi}of{pm}.jsonl'))
