"""C of REVIEW-signals-5: two of the gap runs beside the receiving end (gapstream_end.jsonl) on the oracle alone.

    python3 orc46.py      (about 1 min)   writes research/audit/signals5/end_echo.json (initial cells)

The line N = 12 (objects/line-C.json) is run by reference/oracle.py to generation 2N + 8, the oscillator's cells S of
the record are added, the whole is run tg more generations (the record's generation 0 .. tg), and then two runs
continue: plain, and with the record's hole removed.  D(t) = cells where they differ, inside the line's tube
(1 <= x+y+z, x-y+z <= 7) and outside the support of the oscillator's free orbit.  Printed every 2 generations: the
units holding D, and the units u in which the gapped run is exactly bare wire C (the cells of objects line-C 'unit',
or of the wire's other phase, moved to unit u) while the plain run is not (empty in both runs below: kept as a check).
Checks:  C18.23a gap 0: from the reflection on, D lies in at most 3 consecutive units and moves towards the gun,
         while the end's units (<= 3) are equal in the two runs (an echo: a signal sent back up the stream);
         C13.24a gap 0: behind the moving front the gapped run is a uniform wire of repeat one unit (not wire C):
         the front is a wall between the rake train and another wire, moving up the stream.
"""
import json, os
from st5 import oracle_run, step, unit, tr, WIRE, ROOT, HERE

P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
ln = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
N = 12
x0 = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ln['gun'])
tube = lambda c: 1 <= c[0] + c[1] + c[2] <= 7 and 1 <= c[0] - c[1] + c[2] <= 7
recs = [json.loads(l) for l in open(os.path.join(P5, 'gapstream_end.jsonl'))]
save = []
for osc, k in (('C18.23a', 0), ('C13.24a', 0)):
    r = next(q for q in recs if q['osc'] == osc and q['gap_k'] == k and q['verdict'] == 'gap kills the gun, oscillator kept')
    S = frozenset(tuple(c) for c in r['cells'])
    orb = [S]
    for _ in range(r['P'] - 1):
        orb.append(step(orb[-1]))
    sup = frozenset().union(*orb)
    *_, (t_, a) = oracle_run(x0, 2 * N + 8, pad=24)
    *_, (t_, b) = oracle_run(a | S, r['tg'], pad=24)
    hole = tuple(r['hole']); assert hole in b
    G = 60
    P = [s for t, s in oracle_run(b, G, pad=24)]
    Q = [s for t, s in oracle_run(b - {hole}, G, pad=24)]
    save.append(dict(osc=osc, gap_k=k, line=sorted(a), oscillator=sorted(S), tg=r['tg'], hole=hole,
                     note='line = line-C N=12 at generation 2N+8 (oracle); state at record generation 0 = line | oscillator; '
                          'step tg generations, then remove hole'))
    print(f'{osc} gap {k}: oscillator units {min(unit(c) for c in S)}..{max(unit(c) for c in S)}, hole at unit {unit(hole)}')
    compact = []; bare_ok = []
    for t in range(0, G + 1, 2):
        D = [c for c in P[t] ^ Q[t] if tube(c) and c not in sup]
        us = sorted({unit(c) for c in D})
        ph = (2 * N + 8 + r['tg'] + t) % 2
        bare = [u for u in range(-2, 15) if frozenset(c for c in Q[t] if unit(c) == u and tube(c) and c not in sup) == frozenset(tr(c, u) for c in WIRE[ph])
                and frozenset(c for c in P[t] if unit(c) == u and tube(c) and c not in sup) != frozenset(tr(c, u) for c in WIRE[ph])]
        print(f'  t={t:2d} D on units {us}  gapped run bare wire (plain not) on units {bare}')
        compact.append((t, us)); bare_ok.append((t, us, bare))
    if osc == 'C18.23a':
        seg = [(t, us) for t, us in compact if 24 <= t <= 38]
        ok = all(us and us[-1] - us[0] <= 2 and us[0] > 3 for t, us in seg) and all(seg[i + 1][1][-1] > seg[i][1][-1] for i in range(len(seg) - 1))
        print('  echo check (t = 24..38: D within 3 consecutive units above unit 3, moving towards the gun):', ok)
        whole = [len(P[t] ^ Q[t]) for t in range(24, 39, 2)]
        rigid = all(frozenset(tr(c, 1) for c in P[t] ^ Q[t]) == P[t + 2] ^ Q[t + 2] for t in range(24, 37, 2))
        print('  whole-state difference, t = 24..38 (every cell of the torus):', whole, '; moves rigidly one unit towards the gun per 2 generations:', rigid)
    else:
        ok = True; shapes = set()
        for t in range(34, 45):
            front = max(unit(c) for c in P[t] ^ Q[t] if tube(c) and c not in sup)
            base = [frozenset(tr(c, -u) for c in Q[t] if unit(c) == u and tube(c) and c not in sup) for u in range(4, front - 1)]
            ok &= len(set(base)) == 1
            shapes.add((t % 2, tuple(sorted(base[0]))))
        print('  front check (t = 34..44: every unit from 4 to two below the front holds the same cells in the gapped run, a '
              'uniform wire of repeat one unit):', ok, '; its two phases:', sorted(shapes))
json.dump(save, open(os.path.join(HERE, 'end_echo.json'), 'w'))
