#!/usr/bin/env python3
"""push 8b: does a signal on the second wire put a signal on the store (a write from outside)?

    python3 inject.py READER [--out FILE]        READER: B or C

For every non-parallel placement of survey.py in which the reader stands beside the plain capped wire B (transparent or
a local junction; junc.Junction), a probe is sent along the reader from its left end: one pulse, or two pulses 1, 2 or
3 units apart.  40 generations after the launch the cells of the store's tube that differ from the probe-free run and
lie more than 4 units from the crossing are compared with the two pulses of wire B:
  R      exactly one right-going pulse of the store (two cells), L exactly one left-going pulse
  other  some other difference there (count given)
and 240 generations after the launch the whole object is compared with the state before the probe ('restored': the
store's cap has swallowed the pulse and the reader is as it was; else the number of differing cells).
One JSON line per placement and probe with any difference in the store's tube away from the crossing; summary printed."""
import argparse, json, os, time
from collections import Counter
import lab, wires, survey, junc
from lab import tr, unit
from survey2 import in_tube

U0 = 9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('reader'); ap.add_argument('--out')
    a = ap.parse_args()
    out = a.out or os.path.join(lab.SCR, f'inject_{a.reader}.jsonl')
    L = survey.Lab(a.reader)
    t0 = time.time(); n = nok = 0; cnt = Counter()
    with open(out, 'w') as f:
        for gi_, phi, t in survey.placements(a.reader):
            n += 1
            J = junc.Junction(L, gi_, phi, t, 'B')
            if not J.ok:
                continue
            nok += 1
            Y = lab.run(J.base, J.phi)
            for s in (0, 1, 2, 3):
                pc = wires.pulse(L.pulse, J.ur - U0) + (wires.pulse(L.pulse, J.ur - U0 - s) if s else [])
                X = lab.xor(Y, J.place(pc))
                Xc = lab.run(X, 40); Yc = lab.run(Y, 40)
                D = [c for c in lab.up(lab.xor(Xc, Yc)) if in_tube(c) and abs(unit(c) - J.us) > 4]
                if not D:
                    cnt['nothing on the store'] += 1; continue
                rel = sorted(D)
                kind = f'other({len(D)})'
                for name, p in (('R', lab.PULSE_B), ('L', junc.LEFT['B'])):
                    for u in range(J.us - 30, J.us + 31):
                        if rel == sorted(wires.pulse(p, u)):
                            kind = name
                Xf = lab.run(Xc, junc.TS - 40 - J.phi)
                fin = 'restored' if lab.same(Xf, J.base) else int(len(lab.xor(Xf, J.base)))
                cnt[(kind if kind in 'RL' else 'other') + (' restored' if fin == 'restored' else ' changed')] += 1
                f.write(json.dumps(dict(reader=a.reader, g=gi_, phi=phi, t=list(t), s=s, kind=kind, final=fin, jsize=J.jsize)) + '\n')
    print(f'{n} placements, {nok} standing beside wire B, 4 probes each; ' + ', '.join(f'{k}: {v}' for k, v in cnt.most_common()) + f'; {time.time() - t0:.0f} s -> {out}')


if __name__ == '__main__':
    main()
