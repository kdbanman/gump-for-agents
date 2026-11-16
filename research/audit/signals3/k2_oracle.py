"""The k = 2 caps of the 5 x 5 tube on reference/oracle.py (README section 18).

    python3 k2_oracle.py [FILE]     (default: research/scratch/signals/k2caps_16_47.json, as k2caps.py writes it;
                                     also accepts objects/turn-k2-cap-5x5.json)

For each cap (frame: first cap unit 10; placed at first unit K = 20): (1) stationary (period 2) on the oracle;
(2) a lone rake started 5 units away, wire C back to capL of clock-C at unit 0: oracle box torus, hull-checked,
compared cell for cell with gs every generation for 60 generations; the mirror rake '5f' located (class k from
b - a); (3) whether the cap survives: live cells of units >= K - 1 at generation 60, against 0; the kymograph
row at 60.  (4) the clock capL + 9 units + cap lit at unit 4, on the oracle for 80 generations: rake / mirror
rake passings and the live population at the end.  Also clock-C's capR as the positive control (k = 0).
"""
import json, os, sys
import r3
from r3 import tr, unit, uc
import turn_check as T
SCR = os.path.join(r3.gs.ROOT, 'research', 'scratch', 'signals')
F = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SCR, 'k2caps_16_47.json')
d = json.load(open(F))
caps = [[tuple(c) for c in d['cap']]] if isinstance(d, dict) else [[tuple(c) for c in e['cap']] for e in d]
caps = [('clock-C capR', [tr(c, 10) for c in r3.capR0])] + [(f'k2 #{i}', c) for i, c in enumerate(caps)]
K = 20
for name, cap0 in caps:
    cap = {tr(c, K - 10) for c in cap0}
    base = set(r3.capL) | T.wireC(0, K) | cap
    for t, s in r3.oracle_run(base, 2):
        pass
    stat = s == frozenset(base)
    r = K - 5; st = set(base) ^ uc('C', r) ^ uc(0xf, r)
    G = r3.Run(st, extra=base); agree = True; mir = None; a = -2 * r
    for t, s in r3.oracle_run(st, 60):
        if t:
            G.step(1); agree &= G.cells() == s
        if t % 2 == 0 and mir is None:
            ms = T.find_mirror(s, 0, K - 3)
            if ms:
                mir = (t, max(ms))
    b = mir[0] + 2 * mir[1] if mir else None
    capcells = sum(1 for c in s if unit(c) >= K - 1)
    print(f'{name}: {len(cap0)} cells; stationary on the oracle {stat}; oracle = gs for 60 generations {agree}; '
          f'mirror rake first at t={mir and mir[0]} unit {mir and mir[1]}; k = {(b - a) % 4 if b is not None else None}; '
          f'live cells on the cap units at t=60: {capcells} (bare cap: {len(cap)}); row at 60: {r3.dec(s, 0, K + 6)}', flush=True)
    N = 9; ob = set(r3.capL) | T.wireC(0, N) | {tr(c, N - 10) for c in cap0}
    ev = []
    for t, s in r3.oracle_run(ob | {tr((1, 0, 4), 4)}, 80):
        if t % 2 == 0 and t:
            ev += [('R', t - 2 * u) for u in T.find_rake(s, 1, N - 1)] + [('M', t + 2 * u) for u in T.find_mirror(s, 1, N - 2)]
    seq = []
    for e in ev:
        if e not in seq:
            seq.append(e)
    print(f'    clock N=9 on the oracle: passings {seq}; live cells at t=80: {len(s)}; row: {r3.dec(s, -4, N + 6)}', flush=True)
