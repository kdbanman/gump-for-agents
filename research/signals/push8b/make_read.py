#!/usr/bin/env python3
"""push 8b: write the read objects (objects/*.json) that verify_read.py judges with the oracle alone.

    python3 make_read.py

Every expected cell list in the files is computed here with st.c; verify_read.py recomputes all of it with
reference/oracle.py and compares.
  read-echo-B-line     push 7's line with E and 1 hole (plain wire B) or 2, 3, 4 holes (a stretch of wire B' from
                       unit 41); reader: capped wire B crossing at unit 42 (cell.READERS['b13']); probe: two pulses B
                       in adjacent units.
  read-echo-B-small    the same reader and probe beside a short capped wire B / wire B' (no line, small boxes).
  read-pair-C-line     reader: capped wire C at the same place (cell.READERS['r246']); probe: two pulses p> three
                       units apart.
  read-pair-C-small    the same beside the short capped wires."""
import json, os
import lab, wires, line, cell
from lab import tr, unit

OUT = os.path.join(lab.HERE, 'objects')


def box_for(cells, margin=10):
    lo = [min(c[i] for c in cells) for i in range(3)]; hi = [max(c[i] for c in cells) for i in range(3)]
    off = [margin - lo[i] + ((margin - lo[i]) % 2) for i in range(3)]
    shape = [hi[i] + off[i] + margin + ((hi[i] + off[i] + margin) % 2) for i in range(3)]
    return shape, off


def L(k):
    return [list(c) for c in lab.up(k)]


def case(label, store_k, rd, spacing, probe_gen, out_gen, restored, until, text):
    """store_k: the store at generation 0 of the read (st keys).  Returns (case dict without the store entry, every
    cell ever live: for the box)."""
    R = rd.cells(rd.phi)
    assert rd.phi == 0
    U = lab.union(store_k, R)
    assert len(U) == len(store_k) + len(R)
    seen = set(lab.up(U))
    Y = U
    for t in range(16):
        Y = lab.run(Y, 1); seen.update(lab.up(Y))
    alone = lab.union(lab.run(store_k, 16), lab.run(R, 16))
    missing = lab.xor(Y, alone)
    assert all(c in set(lab.up(alone)) for c in lab.up(missing)), 'the standing state has cells the two alone do not have'
    Y = lab.run(Y, probe_gen - 16)
    probe = lab.union(rd.pulse(rd.ur - 9), rd.pulse(rd.ur - 9 - spacing))
    X = lab.xor(Y, probe)
    out = None
    for t in range(probe_gen, until + 1):
        seen.update(lab.up(X)); seen.update(lab.up(Y))
        if t == out_gen:
            out = lab.xor(X, Y)
        if t >= restored:
            assert lab.same(X, Y), (label, t)
        X = lab.run(X, 1); Y = lab.run(Y, 1)
    d = dict(label=label, reader=L(R), missing=L(missing), probe=L(probe), probe_gen=probe_gen, out=L(out), out_gen=out_gen,
             out_text=text, restored=restored, until=until)
    return d, seen


def build(name, rname, spacing, kind, timing, texts, note):
    """kind 'line': push 7's line, n = 1 and n = 3; 'small': capped wire B and capped wire B'."""
    probe_gen, out_gen, restored, until = timing
    ob = dict(name=name, note=note, reader=rname, cases=[])
    seen = set()
    if kind == 'line':
        rd = cell.Reader(rname, 42)
        l0 = cell.line0()
        ob['line0'] = L(l0)
        sb, so = box_for(lab.up(l0), 8)
        for n in (1, 2, 3, 4):
            lab_ = 'E and 1 hole: plain wire B' if n == 1 else f"E and {n} holes: wire B' on units 41..{40 + n}"
            S = cell.standing(n)
            d, s = case(lab_, S, rd, spacing, probe_gen, out_gen, restored, until, texts[0 if n == 1 else 1])
            d['value'] = 0 if n == 1 else 1
            d['store'] = dict(start='line0', flips=[[1, [list(c) for c in cell.write_flips(n)]]], gens=900, box=sb, offset=so)
            ob['cases'].append(d); seen |= s
    else:
        rd = cell.Reader(rname, 0)
        sB = lab.pk(wires.capped_B(-10, 10))
        sBp = lab.run(lab.pk([wires.SIGB(c) for c in wires.capped_B(-10, 10)]), 1)
        for lab_, S, i in (('wire B', sB, 0), ("wire B'", sBp, 1)):
            d, s = case(lab_, S, rd, spacing, probe_gen, out_gen, restored, until, texts[i])
            d['value'] = i
            d['store'] = dict(cells=L(S))
            ob['cases'].append(d); seen |= s
    ob['box'], ob['offset'] = box_for(seen, 10)
    fn = os.path.join(OUT, name + '.json')
    json.dump(ob, open(fn, 'w'))
    print(f"{fn}: box {ob['box']}, " + '; '.join(f"[{c['label']}] reader {len(c['reader'])} cells, missing {len(c['missing'])}, out {len(c['out'])} cells" for c in ob['cases']))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    tB = (20, 50, 72, 100)
    textB = ('one left-going pulse B on its way back to the sender', 'nothing: both pulses were swallowed at the crossing')
    noteB = ("a second wire B crosses the store; two pulses B in adjacent units are sent along it towards the crossing. Beside a unit of "
             "wire B one pulse comes back; beside a unit of wire B' nothing does; in both cases store and reader are afterwards exactly as before")
    build('read-echo-B-line', 'b13', 1, 'line', tB, textB, noteB + ' (store: push 7\'s standing line; reader at unit 42)')
    build('read-echo-B-small', 'b13', 1, 'small', tB, textB, noteB + ' (store: a capped wire B or wire B\' of 20 units)')
    tC = (20, 60, 90, 120)
    textC = ('a changed train going on and one left-going pulse p< going back', 'the two pulses as they were sent, 20 units on')
    noteC = ("a wire C crosses the store; two pulses p> three units apart are sent along it. Beside wire B' they pass; beside wire B a "
             "different train goes on and one pulse comes back; in both cases store and reader are afterwards exactly as before")
    build('read-pair-C-line', 'r246', 3, 'line', tC, textC, noteC + ' (store: push 7\'s standing line; reader at unit 42)')
    build('read-pair-C-small', 'r246', 3, 'small', tC, textC, noteC + ' (store: a capped wire B or wire B\' of 20 units)')
