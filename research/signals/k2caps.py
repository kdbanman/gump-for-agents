#!/usr/bin/env python3
"""Enumerate caps of wire C (period 2, the 5 x 5 tube) that turn a lone rake with class k = 2 (sat_turn.py set-up),
and put each into a shuttle clock with capL of clock-C: a clock of period 0 mod 4 needs exactly such a cap.

    python3 k2caps.py [T=16] [C=47] [--max 20] [--minutes 20]

Every model is blocked (its cap's cells at generation 0) and the solver asked again.  Each cap is tested: the
lone-rake turn re-stepped (turnclass.right_turn), and the clock capL + N units of wire C + cap, lit by one cell,
for N = 5, 6 (period by sg.step_set; a shuttle clock of this pair should have period 4N + c with c = 0 mod 4).
Stepping: sg.step_set only; nothing here is a verdict of the oracle."""
import argparse, json, time
from pysat.solvers import Solver
import sg, scat, sat_turn, turnclass
from clocks import period
tr = scat.tr; unit = scat.unit
ap = argparse.ArgumentParser()
ap.add_argument('T', type=int, nargs='?', default=16); ap.add_argument('C', type=int, nargs='?', default=47)
ap.add_argument('--max', type=int, default=20); ap.add_argument('--minutes', type=float, default=20)
a = ap.parse_args()
R, pb, Z, X, ua, u0 = sat_turn.build(a.T, a.C, -1, 7, 10, 2)
ck = json.load(open('objects/clock-C.json'))
capL = [tuple(c) for c in ck['capL']]; un = [tuple(c) for c in ck['unit']]
free = R.of_units(10, 99); t0 = time.time(); out = []
with Solver(name='cadical153', bootstrap_with=pb.f.cl) as s:
    for n in range(a.max):
        if time.time() - t0 > 60 * a.minutes or not s.solve():
            print('stopped: ', 'UNSAT (list complete)' if time.time() - t0 <= 60 * a.minutes else 'time'); break
        m = set(l for l in s.get_model() if l > 0)
        cap = sorted(R.cells[i] for i in free if Z[0][i] in m)
        s.add_clause([(-Z[0][i] if Z[0][i] in m else Z[0][i]) for i in free])
        r = turnclass.right_turn(frozenset(tr(c, 14) for c in cap))
        res = []
        for N in (5, 6):
            cells = set(capL) | {tr(c, k) for c in un for k in range(N)} | {tr(c, N - 10) for c in cap}
            res.append(period(cells | {tr((1, 0, 4), N // 2)}, 40 * N + 600))
        print(f'#{n} {len(cap)} cells; lone turn {r}; clock N=5,6 (period, from): {res}  [{time.time() - t0:.0f}s]', flush=True)
        out.append(dict(cap=[list(c) for c in cap], turn=str(r), clock=res))
        json.dump(out, open(sg.os.path.join(sg.SCR, f'k2caps_{a.T}_{a.C}.json'), 'w'))
