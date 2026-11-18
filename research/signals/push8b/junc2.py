#!/usr/bin/env python3
"""push 8b: pairs of pulses as the probe.  For every non-parallel placement of survey.py in which the reader stands
beside wire B and beside wire B', send two pulses s units apart (s = 1..8) from the left end (L, the right-going pulse)
or from the right end (R, the left-going pulse), at launch delay 0 and, where the crossing has period 4, 2.

    python3 junc2.py READER [--part i/m] [--out FILE]

A probe is a *clean read* if for store B and for store B' the whole object is, 240 generations later, exactly what
it was before the probe, and what is travelling 44 generations after the launch (the difference from the probe-free
run outside 3 units of the crossing, in the reader's frame) differs between the two stores.
One JSON line per placement that has a clean read."""
import argparse, json, os, time
import lab, wires, survey, junc
from lab import tr, unit

U0 = 9


def probe(J, side, s, delay):
    """J: junc.Junction.  Returns (output, verdict)."""
    Y = lab.run(J.base, J.phi + delay)
    if side == 'L':
        pc = wires.pulse(J.L.pulse, J.ur - U0) + wires.pulse(J.L.pulse, J.ur - U0 - s)
    else:
        pc = wires.pulse(junc.LEFT[J.L.name], J.ur + U0) + wires.pulse(junc.LEFT[J.L.name], J.ur + U0 + s)
    X = lab.xor(Y, J.place(pc))
    Xc = lab.run(X, 44); Yc = lab.run(Y, 44)
    D = lab.up(lab.xor(Xc, Yc))
    out = tuple(sorted(tr(lab.app(J.gi, (c[0] - J.t[0], c[1] - J.t[1], c[2] - J.t[2])), -J.ur) for c in D if abs(J.runit(c) - J.ur) > 3))
    Xf = lab.run(Xc, junc.TS - 44 - J.phi - delay)
    return out, lab.same(Xf, J.base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--part', default='0/1'); ap.add_argument('--out'); ap.add_argument('--smax', type=int, default=8)
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    out = a.out or os.path.join(lab.SCR, f'junc2_{a.reader}_{pi}of{pm}.jsonl')
    L = survey.Lab(a.reader)
    t0 = time.time(); n = nok = nread = 0
    with open(out, 'w') as f:
        for j, (gi_, phi, t) in enumerate(survey.placements(a.reader)):
            if j % pm != pi:
                continue
            n += 1
            js = {k: junc.Junction(L, gi_, phi, t, k) for k in ('B', 'Bp')}
            if not all(x.ok for x in js.values()):
                continue
            nok += 1
            per4 = any(not lab.same(lab.run(x.base, 2), x.base) for x in js.values())
            reads = []
            for side in 'LR':
                for s in range(1, a.smax + 1):
                    for delay in ((0, 2) if per4 else (0,)):
                        r = {k: probe(js[k], side, s, delay) for k in js}
                        if r['B'][1] and r['Bp'][1] and r['B'][0] != r['Bp'][0]:
                            reads.append(dict(side=side, s=s, delay=delay, nB=len(r['B'][0]), nBp=len(r['Bp'][0])))
            if reads:
                nread += 1
                f.write(json.dumps(dict(reader=a.reader, g=gi_, phi=phi, t=list(t), per4=per4, jsize={k: js[k].jsize for k in js}, reads=reads)) + '\n'); f.flush()
                print('READ', a.reader, gi_, phi, t, [(r['side'], r['s'], r['delay'], r['nB'], r['nBp']) for r in reads], flush=True)
    print(f'{n} placements, {nok} standing beside both B and B\', {nread} with a clean read by a pair of pulses; {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
