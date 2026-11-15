#!/usr/bin/env python3
"""Writes objects/echo-train.json: the plain rake train, its four riding signals, one-cell events that make them,
the meetings and the gun that absorbs U, with the outcomes measured by echo6 / meet6 (sg.step_set), for
verify_echo.py to check on the oracle.     python3 make_echo_json.py   (about 1 min)"""
import json
import echo6 as E, sg, meet6

T_MEET = 56
WB = [[(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)], [(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)]]
out = dict(name='echo-train', v=[1, 0, -1], unit=[2, 0, -2],
           note='Line frame of line-C.json: the rake train moves towards -v. train(t): unit u holds base[t % 4][u % 2] '
                'moved by u units. A signal K at train phase 1 with lowest unit u is the train xor sig[K].cells moved u '
                'units (u of parity sig[K].parity); it moves dir units every 2 generations.',
           base=[[sorted(map(list, E.BASE[t][p])) for p in (0, 1)] for t in range(4)],
           sig={K: dict(parity=E.SIG1[K][0], cells=sorted(map(list, E.SIG1[K][1])), dir=E.DIR[K]) for K in E.SIG1},
           wireB=WB)
# one-cell events: (phase f, cell) on the plain train -> kind, and the place at generation 40
ev = [(0, (1, 0, 0), 'E'), (3, (0, 0, 3), 'U'), (3, (1, 2, 2), 'H'), (1, (0, 1, 4), 'K0')]
evs = []
for f, c, K in ev:
    A = 80
    P = E.train(f, -A, A); S = P ^ {c}
    D = E.diff_run(S, f, 40, A)
    # generation 40 from phase f: phase (f + 40) % 4 = f
    g = 40 + ((1 - f) % 4)  # a generation at phase 1
    D = E.diff_run(S, f, g, A)
    r = E.decompose(D[g])
    assert r and len(r) == 1 and r[0][0] == K, (f, c, K, r)
    evs.append(dict(phase=f, cell=list(c), flip='remove' if c in P else 'add', kind=K, gen=g, unit=r[0][1]))
out['events'] = evs
# meetings and words
mt = []
for sigs, kind in [([('E', 0), ('H', 21)], 'wireB'), ([('U', 1), ('H', 21)], 'wireB'), ([('U', 1), ('K0', 20)], 'cancel'),
                   ([('E', 0), ('K0', 20)], 'holed'),
                   ([('E', 0), ('H', 21), ('H', 27)], 'wireB'), ([('E', 0), ('H', 21), ('H', 27), ('H', 33)], 'wireB'),
                   ([('E', 0), ('H', 21), ('H', 27), ('H', 33), ('H', 41)], 'wireB')]:
    Ss, D, A = meet6.run(sigs, T_MEET)
    d = D[T_MEET]; St = Ss[T_MEET]
    rec = dict(signals=[[K, u] for K, u in sigs], outcome=kind, gen=T_MEET)
    if kind == 'cancel':
        rec['empty_from'] = max(t for t in range(T_MEET + 1) if D[t]) + 1
    else:
        us = sorted({E.unit_of(c) for c in d}); lo, hi = us[0], us[-1]
        rec['lo'], rec['hi'] = lo, hi
        if kind == 'wireB':
            ph = T_MEET % 2   # wire B: WB[0] at even generations of the run (phase-1 start), checked below
            bad = [u for u in range(lo + 3, hi - 5) if frozenset(E.tr(c, -u) for c in E.units(St, u, u + 1)) != frozenset(map(tuple, WB[(T_MEET + 1) % 2]))]
            rec['not_wireB'] = bad
        else:
            # the train with every rake holed: train(1 + T) xor H at every unit of H's parity, in the middle
            ref = Ss[T_MEET]
            fH = (1 + T_MEET) % 4
            assert fH == 1
            holed = E.train(1, lo - 10, hi + 10)
            for u in range(lo - 10, hi + 10):
                if u % 2 == E.SIG1['H'][0]:
                    holed = holed ^ E.sig('H', u)
            rec['holed_equal_units'] = [lo + 3, hi - 2]
            assert E.units(St, lo + 3, hi - 2) == E.units(holed, lo + 3, hi - 2), 'holed medium'
    mt.append(rec)
    print(rec)
out['meetings'] = mt
g = json.load(open(E.os.path.join(E.SCR6, 'guns_5f_37.json')))
out['gun_absorbs_U'] = dict(cap=g['list'][4]['cap'], source='python3 sat_gun.py 5f 37 --all, solution #4 (23 cells)', KS=6)
json.dump(out, open(E.os.path.join(E.HERE, 'objects', 'echo-train.json'), 'w'), indent=0)
print('written')
