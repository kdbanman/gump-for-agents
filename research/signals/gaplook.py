#!/usr/bin/env python3
"""Look at the gap runs that gapstream.py flagged (sg.step_set).

    python3 gaplook.py final F.jsonl      the 'LISTENER?' records with the gun alive: both final states, period and
                                          population, the wire decoded (one letter per unit, '?' = not a family unit)
    python3 gaplook.py fire F.jsonl [n]   the first n records where the gap kills the gun: plain and gapped runs side
                                          by side, every second generation, and the size of their difference"""
import json, sys
import sg, scat, turnclass as tc
from clocks import period
tr = scat.tr; unit = scat.unit
mode, fn = sys.argv[1], sys.argv[2]
ln = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'line-C.json'))); N = 12
x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | frozenset(tr(tuple(c), N) for c in ln['gun'])
for _ in range(2 * N + 8):
    x = sg.step_set(x)
recs = [json.loads(l) for l in open(fn)]
if mode == 'final':
    recs = [r for r in recs if r['verdict'] == 'LISTENER?' and r['gap_gun']]
else:
    recs = [r for r in recs if r['verdict'] in ('LISTENER?', 'gap kills the gun, oscillator kept') and not r['gap_gun']][:int(sys.argv[3]) if len(sys.argv) > 3 else 1]
for r in recs:
    S = frozenset(tuple(c) for c in r['cells']); y = S | x
    for _ in range(r['tg']):
        y = sg.step_set(y)
    g = y - {tuple(r['hole'])}
    print(r['osc'], 'gap', r['gap_k'], 'at generation', r['tg'], '; oscillator units', min(unit(c) for c in S), '..', max(unit(c) for c in S))
    if mode == 'final':
        for name, z in (('plain', y), ('gap', g)):
            p, t0 = period(set(z), 4000)
            w = z
            for _ in range(t0 + (t0 % 2)):
                w = sg.step_set(w)
            print('  ', name, 'final period', p, 'from', t0 + r['tg'], 'population', len(w))
            for i in range(0, 8, 2):
                print('      ', tc.dec(w - S, -6, 16)); w = sg.step_set(sg.step_set(w))
    else:
        for t in range(0, 70, 2):
            print('  %3d' % (r['tg'] + t), tc.dec(y - S, -2, 15), tc.dec(g - S, -2, 15), len(y ^ g))
            y = sg.step_set(sg.step_set(y)); g = sg.step_set(sg.step_set(g))
