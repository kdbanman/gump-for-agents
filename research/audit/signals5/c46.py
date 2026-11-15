"""C of REVIEW-signals-5: every gap run of the fifth push in which the gap kills the gun while the oscillator beside
the line survives (28 records of gapstream.jsonl, 18 of gapstream_end.jsonl): what travels from the oscillator to
the gun?  st5.step (sparse), checked here against the oracle on the first record of each file.

    python3 c46.py          (about 2 min)

For each record: the line N = 12 in its cycle (generation 2N + 8, as gapstream.py) + the oscillator's cells S,
stepped tg generations; the gapped run has the cell `hole` removed.  Both runs are stepped 300 generations.  D(t) =
cells where they differ, outside the support of the oscillator's free orbit.  Reported:
  t_gun    generations from the gap until D first contains a cell of unit >= 12 (the gun's units);
  front    the highest unit of D on the wire side of the oscillator, sampled, to see the speed;
  behind   at t_gun + 10: of the wire units from the oscillator's highest unit + 1 to 11, how many hold in the
           gapped run fewer than half the live cells they hold in the plain run (burnt), and how many are equal to
           the plain run (healed behind the front); a signal would leave units equal behind it, a fire leaves them
           burnt;
  osc      the oscillator equal to its free orbit (in the gapped run) at t_gun + 10.
"""
import json, os
import numpy as np
from st5 import step, unit, tr, oracle_run, ROOT

P5 = os.path.join(ROOT, 'research', 'scratch', 'signals', 'p5')
ln = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'line-C.json')))
N = 12
x = frozenset(tuple(c) for c in ln['capA']) | frozenset(tr(tuple(c), k) for c in ln['unit'] for k in range(N)) | \
    frozenset(tr(tuple(c), N) for c in ln['gun'])
for _ in range(2 * N + 8):
    x = step(x)
line_cells = x


def in_line_tube(c):
    return 1 <= c[0] + c[1] + c[2] <= 7 and 1 <= c[0] - c[1] + c[2] <= 7


recs = []
for fn, want in (('gapstream.jsonl', 'LISTENER?'), ('gapstream_end.jsonl', 'gap kills the gun, oscillator kept')):
    for l in open(os.path.join(P5, fn)):
        r = json.loads(l)
        if r['verdict'] == want and not r['gap_gun']:
            r['file'] = fn; recs.append(r)
print(len(recs), 'records')
rows = []; checked = set()
for r in recs:
    S = frozenset(tuple(c) for c in r['cells'])
    orb = [S]
    for _ in range(r['P'] - 1):
        orb.append(step(orb[-1]))
    sup = frozenset().union(*orb)
    y = S | line_cells
    for _ in range(r['tg']):
        y = step(y)
    hole = tuple(r['hole']); assert hole in y
    g = y - {hole}
    if r['file'] not in checked:              # the sparse stepper against the oracle on this run, 150 generations
        checked.add(r['file'])
        z = g
        for t, s in oracle_run(g, 150, pad=40):
            assert s == z, ('oracle mismatch', t); z = step(z)
    ohi = max(unit(c) for c in S if in_line_tube(c)) if any(in_line_tube(c) for c in S) else max(unit(c) for c in S)
    ohi = min(ohi, 11)
    p_, g_ = y, g; t_gun = None; fronts = []; hist = []
    for t in range(1, 301):
        p_, g_ = step(p_), step(g_)
        D = [c for c in (p_ ^ g_) if c not in sup]
        wd = [unit(c) for c in D if in_line_tube(c)]
        fronts.append(max(wd) if wd else None)
        hist.append((p_, g_))
        if t_gun is None and any(unit(c) >= N and in_line_tube(c) for c in D):
            t_gun = t
        if t_gun is not None and t >= t_gun + 10:
            break
    if t_gun is None:
        rows.append((r['file'], r['osc'], r['gap_k'], None)); continue
    p10, g10 = hist[t_gun + 9]
    burnt = eqn = 0; units = list(range(ohi + 1, N))
    for u in units:
        pu = frozenset(c for c in p10 if unit(c) == u and in_line_tube(c) and c not in sup)
        gu = frozenset(c for c in g10 if unit(c) == u and in_line_tube(c) and c not in sup)
        burnt += len(gu) < len(pu) / 2
        eqn += pu == gu
    ph = next((i for i in range(r['P']) if (g10 & sup) == orb[i]), None)
    rows.append((r['file'], r['osc'], r['gap_k'], t_gun, [fronts[i] for i in range(0, t_gun + 10, 4)], len(units), burnt, eqn, ph is not None))
print(f'{"file":22s} {"osc":10s} k  t_gun  units(osc..11) burnt equal  osc_ok  front (every 4 gens)')
for rw in rows:
    if rw[3] is None:
        print(rw[0], rw[1], rw[2], 'gun never reached in 300 generations'); continue
    f, o, k, tg, fr, nu, b, e, ok = rw
    print(f'{f:22s} {o:10s} {k}  {tg:4d}   {nu:3d}          {b:3d}   {e:3d}    {ok}    {fr}')
n_fire = sum(1 for rw in rows if rw[3] is not None and rw[6] == rw[5])
print(f'{len(rows)} runs; in {n_fire} every wire unit between the oscillator and the gun is burnt 10 generations after '
      f'the difference reaches the gun; runs with any wire unit equal to the plain run behind the front: '
      f'{sum(1 for rw in rows if rw[3] is not None and rw[7] > 0)}')
