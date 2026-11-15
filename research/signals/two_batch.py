#!/usr/bin/env python3
"""Batch driver for sat_two.py (two-sided standing objects that turn a lone rake): one line per instance.

    python3 two_batch.py MODE --T 6 10 14 --w 2 3 4 --dT 2 4 6 8 --V b 7 d e 8 [--lo 1 --hi 5] [--timeout 120] [--out F.jsonl]

MODE = emit   : the object is restored at Tr = T + dT and the right wire is not bare then (sat_two.build(emit=Tr))
MODE = restore: the object is restored at Tr = T + dT (no condition on the right wire)
MODE = steady : units KS-2..KS+w the same at T+dT+4 as at T+dT (swallowing the p> train in steady state)
MODE = steadyleak: the same and the right wire not bare at T+dT+4
MODE = turn   : the turn only (dT ignored)
Every model is re-stepped (sat_two.lone_test, sg.step_set) and written to the jsonl file with its test."""
import argparse, json, time
import sat_two as S
from scat import unit
ap = argparse.ArgumentParser()
ap.add_argument('mode'); ap.add_argument('--T', type=int, nargs='+'); ap.add_argument('--w', type=int, nargs='+')
ap.add_argument('--dT', type=int, nargs='+', default=[0]); ap.add_argument('--V', nargs='+', default=['b'])
ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=120); ap.add_argument('--out')
a = ap.parse_args()
for w in a.w:
    for T in a.T:
        for V in a.V:
            for dT in (a.dT if a.mode != 'turn' else [0]):
                t0 = time.time(); Tr = T + dT if a.mode != 'turn' else 0
                st_ = a.mode.startswith('steady')
                R, pb, Z, X, U = S.build(T, a.KS, a.lo, a.hi, w, int(V, 16), 2, None, 0 if st_ else Tr, a.mode in ('emit', 'steadyleak'), dT if st_ else 0)
                st, m = pb.solve('cadical153', a.timeout)
                line = f'{st:7s} {a.mode} T={T} (k={S.turn_class(T, a.KS)}) Tr={Tr} w={w} V={V} tube [{a.lo},{a.hi}] {time.time() - t0:.0f}s'
                if st == 'SAT':
                    obj = sorted(R.cells[i] for i in range(R.n) if a.KS <= R.units[i] < a.KS + w and Z[0][i] in m)
                    r = S.lone_test(obj, a.KS, w, int(V, 16))
                    line += f' | {len(obj)} cells {r}'
                    if a.out:
                        with open(a.out, 'a') as f:
                            f.write(json.dumps(dict(mode=a.mode, T=T, Tr=Tr, w=w, V=V, lo=a.lo, hi=a.hi, KS=a.KS, obj=[list(c) for c in obj],
                                                    test={k: (list(v) if isinstance(v, tuple) else v) for k, v in r.items()})) + '\n')
                print(line, flush=True)
