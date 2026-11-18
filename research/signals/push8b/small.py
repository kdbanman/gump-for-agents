#!/usr/bin/env python3
"""push 8b: the smallest cell found: a short store written by push 8's one-cell operations, and a short reader.

    python3 small.py search     the shortest reader and store for which the read works (st.c stepper)
    python3 small.py make       write objects/cell-small.json (judged by verify_read.py with the oracle alone)

Store: a capped wire B on units -m1..m2-1 (wires.capped_B: the cell of push 8).  Stored 1: three live cells removed,
the stators (0,1,2) of unit -3 and (0,1,4) of unit 2 at generation 0 (push 8's `set`: the two pulses stop each other
and leave the stretch `d f` on units -1, 0) and the stator (0,1,4) of unit 2 again at generation WAIT (push 8's `add
one`: the stretch is `d d f` on units -1, 0, 1).  Stored 0: nothing removed.
Reader: a capped wire B on its own units -a..b-1, placed by cell.READERS['b13'] with the crossing at store unit 0 (the
second unit of wire B'), put beside the store when the store stands (generation TAKE of the store).
Probe: two pulses B in the reader's units ur-d and ur-d-1 (ur = -1 is the reader's unit at the crossing)."""
import json, os, sys
import lab, wires, cell, junc, line
from lab import tr, unit

WAIT, TAKE = 40, 120
G13 = lab.SYMS[13]
T0 = (-2, 0, 0)
UR = -1


def stator(u, which=2):
    return (2 * u, 1, which - 2 * u)


WRITE = [[0, [stator(-3, 2), stator(2, 4)]], [WAIT, [stator(2, 4)]]]


def store(m1, m2, one):
    S = lab.pk(wires.capped_B(-m1, m2))
    if not one:
        return S
    X = S
    for t in range(TAKE):
        for g, cells in WRITE:
            if g == t:
                if not all(c in set(lab.up(X)) for c in cells):
                    return None
                X = lab.xor(X, lab.pk(cells))
        X = lab.run(X, 1)
    return X


def place(cells):
    return lab.pk([lab.app(G13, c, T0) for c in cells])


def back(c):
    gi = cell.inv(G13)
    return lab.app(gi, (c[0] - T0[0], c[1] - T0[1], c[2] - T0[2]))


def reader(a, b):
    return place(wires.capped_B(-a, b))


def probe(d):
    return place(wires.pulse(lab.PULSE_B, UR - d) + wires.pulse(lab.PULSE_B, UR - d - 1))


def trial(m1, m2, a, b, d, T=160):
    """returns None if the cell does not work, else (cells of store 0 + reader, generation of the echo, unit)."""
    echo = None
    for one in (0, 1):
        S = store(m1, m2, one)
        if S is None or not lab.same(lab.run(S, 2), S):
            return None
        if one and line.letters(S, -3, 3)[1] != 'bbpp#b':
            return None
        R = reader(a, b)
        U = lab.union(S, R)
        if len(U) != len(S) + len(R) or not lab.same(lab.run(U, 2), U):
            return None
        X = lab.xor(U, probe(d)); Y = U
        for t in range(1, T + 1):
            X = lab.run(X, 1); Y = lab.run(Y, 1)
            D = lab.up(lab.xor(X, Y))
            if any(cell.in_tube(c) for c in D):
                return None                               # the store was touched
            if t == 2 * d + 8:
                # the echo: exactly one left-going pulse B, two to six units back from the crossing
                wants = [sorted(lab.up(place(wires.pulse(junc.LEFT['B'], UR - j)))) for j in range(2, 7)]
                if one == 0 and sorted(D) not in wants:
                    return None
                if one == 1 and D:
                    return None
        if not lab.same(X, Y):
            return None
    return len(store(m1, m2, 0)) + len(reader(a, b))


def search():
    best = None
    # the reader first, beside a long store
    for a in range(2, 13):
        for b in range(0, 8):
            for d in range(1, a):
                if UR - d - 1 < -a:
                    continue
                n = trial(8, 8, a, b, d)
                if n is not None and (best is None or (a + b, d) < best[:2]):
                    best = (a + b, d, a, b)
                    print(f'reader units -{a}..{b - 1}, launch {d} units before the crossing: works ({len(reader(a, b))} cells)', flush=True)
    _, d, a, b = best
    bs = None
    for m1 in range(4, 9):
        for m2 in range(3, 9):
            n = trial(m1, m2, a, b, d)
            if n is not None and (bs is None or n < bs[0]):
                bs = (n, m1, m2)
                print(f'store units -{m1}..{m2 - 1} with that reader: works, {n} cells in all', flush=True)
    print('smallest:', dict(m1=bs[1], m2=bs[2], a=a, b=b, d=d, cells=bs[0]))
    return bs[1], bs[2], a, b, d


def make(m1, m2, a, b, d):
    import make_read
    S0 = lab.pk(wires.capped_B(-m1, m2))
    R = reader(a, b)
    pr = probe(d)
    pg, og, rg, until = 20, 20 + 2 * d + 8, 20 + 2 * d + 8 + 2 * (a + 8), 20 + 2 * d + 8 + 2 * (a + 8) + 40
    ob = dict(name='cell-small', reader='b13',
              note=("the smallest cell found: a capped wire B (push 8's cell) and a short second wire B across it. Stored 1: three live cells "
                    "removed (push 8's set and add one) leave the stretch d d f, and the reader is put beside its second unit; stored 0: nothing "
                    "removed. Probe: two adjacent pulses B on the reader. 0: one pulse comes back; 1: nothing comes back; store and reader are "
                    "afterwards exactly as before"),
              store0=make_read.L(S0), cases=[])
    seen = set()
    for one, label, text in ((0, '0: nothing written', 'one left-going pulse B on its way back to the sender'),
                             (1, '1: set and add one (three cells removed): d d f', 'nothing: both pulses were swallowed at the crossing')):
        S = store(m1, m2, one)
        U = lab.union(S, R)
        Y = lab.run(U, pg); X = lab.xor(Y, pr)
        out = None
        for t in range(pg, until + 1):
            seen.update(lab.up(X)); seen.update(lab.up(Y))
            if t == og:
                out = lab.xor(X, Y)
            if t >= rg:
                assert lab.same(X, Y)
            X = lab.run(X, 1); Y = lab.run(Y, 1)
        x = S0
        for t in range(TAKE):
            seen.update(lab.up(x)); x = lab.run(x, 1)
        sb, so = make_read.box_for(lab.up(S0), 10)
        ob['cases'].append(dict(label=label, value=one, store=dict(start='store0', flips=(WRITE if one else []), gens=TAKE, box=sb, offset=so),
                                reader=make_read.L(R), missing=[], probe=make_read.L(pr), probe_gen=pg, out=make_read.L(out), out_gen=og,
                                out_text=text, restored=rg, until=until))
    ob['box'], ob['offset'] = make_read.box_for(seen, 10)
    fn = os.path.join(lab.HERE, 'objects', 'cell-small.json')
    json.dump(ob, open(fn, 'w'))
    print(f"{fn}: store {len(S0)} cells, reader {len(R)} cells, box {ob['box']}; out {[len(c['out']) for c in ob['cases']]}")


if __name__ == '__main__':
    if sys.argv[1] == 'search':
        search()
    else:
        args = [int(x) for x in sys.argv[2:7]] if len(sys.argv) > 2 else None
        make(*(args or search()))
