#!/usr/bin/env python3
"""Periods of the shuttle clocks of objects/clock-C.json for a range of lengths, with the C stepper (sgc.c, checked
against the oracle by check_stepper.py) in a closed vessel (the 3 x 3 tube cut by planes beyond the caps: exact for
empty space by T2).  The oracle itself is the judge for a few N in verify_clock.py; this is the long list.

    python3 clock_family.py N1 N2 [--file objects/clock-C.json]

Prints every N whose lit object does NOT have period exactly 4N + c (c from the file, default 2), and a summary.
"""
import argparse, json
import sg, scat

ap = argparse.ArgumentParser()
ap.add_argument('N1', type=int); ap.add_argument('N2', type=int); ap.add_argument('--file', default='objects/clock-C.json')
a = ap.parse_args()
ob = json.load(open(a.file)); c0 = ob.get('c', 2)
capL = [tuple(c) for c in ob['capL']]; unit = [tuple(c) for c in ob['unit']]; capR = [tuple(c) for c in ob['capR']]
S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
bad = []; n = 0
for N in range(a.N1, a.N2 + 1):
    cells = set(capL) | {scat.tr(c, k) for c in unit for k in range(N)} | {scat.tr(c, N) for c in capR}
    s3 = [c[0] + c[1] - c[2] for c in cells]; s4 = [c[0] - c[1] - c[2] for c in cells]
    g = sg.Geom([], [(S1, 1, 5), (S2, 1, 5), (S3, min(s3), max(s3)), (S4, min(s4), max(s4))], seeds=list(cells))
    x = g.state(cells | {scat.tr(tuple(ob['ignite']), N // 2)})
    per, gen, st = g.cycle(x, 100 * N + 1000)
    n += 1
    if per != 4 * N + c0:
        bad.append((N, per))
print(f'{ob["name"]}: N = {a.N1} .. {a.N2}: {n - len(bad)} of {n} have period exactly 4N + {c0}; exceptions: {bad}')
