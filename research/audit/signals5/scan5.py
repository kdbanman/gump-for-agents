"""B(iii) and B(iv) of REVIEW-signals-5: every one of the 741 ends of the rake train, sent (a) the eight words of the
census (README section 27) and (b) every one-unit change of one arriving rake, classified on the WHOLE state.

    python3 scan5.py [--part i/n] [--U0 -60] [--tmax 400] [--out F.json]     (st5.Tube; ~1 core-hour in all)

Geometry: the end (its cells of units >= KS = 6, from census5's list of 741) at the end of the plain train; the
cells of the 3 x 3 tube inside the planes C <= 39 with unit >= U0 - 1 are stepped (st5.Tube, checked against the
oracle by check_st5.py); unit U0 - 1 is refilled with the plain train each generation, which is exact for as long as
units U0, U0 + 1 hold the plain train (checked at every generation).  Row 0 is the undisturbed run.
Events:
  words   the census words [0] [1] [2] [3] [0,1] [0,1,2] [0,2] [0,2,4,6,8]: the rake cell (1,0,4) removed at
          generation 0 from the i-th rake below KS (units 4, 2, 0, ...), as census_ends.py;
  rm      at generation g = 0, 1, 2, 3, every non-empty subset of the live cells of ONE unit of the train period
          (units u0, u0 + 1 with u0 = -10 + g // 2: the same rake, followed) removed;
  add     at generation g, every dead cell of the tube in those two units made live (one cell);
  wire    at generation g, both units replaced by bare wire C of that phase (the rake missing).
Outcome of a row:
  healed      equal to row 0 on every cell of the region (hence on the whole lattice) at some t <= tmax;
  upstream    the difference reached unit U0 + 1 before healing (something went up the stream: a burn, or an echo);
              recorded with whether the end's units >= KS - 8 were equal to row 0's at that moment;
  persistent  neither by tmax: then the row's final state is classified by st5 (period, does it equal row 0
              translated / at another phase).
"""
import argparse, json, os, sys, time
from collections import Counter
from itertools import combinations
import numpy as np
from st5 import Tube, step, train, unit, tr, in_tube, is_cell, WIRE, ROOT

ap = argparse.ArgumentParser(); ap.add_argument('--part', default='0/1'); ap.add_argument('--U0', type=int, default=-60)
ap.add_argument('--tmax', type=int, default=400); ap.add_argument('--out'); ap.add_argument('--only', type=int)
a = ap.parse_args()
pi, pn = map(int, a.part.split('/'))
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals5')
ends = json.load(open(os.path.join(OUT, 'ends.json')))['ends']
assert len(ends) == 741
KS = 6
TB = Tube(a.U0, 39)
WORDS = [[0], [1], [2], [3], [0, 1], [0, 1, 2], [0, 2], [0, 2, 4, 6, 8]]
rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in train(0, KS - 40, KS)), reverse=True)


def events():
    ev = []
    for w in WORDS:
        ev.append(('word ' + ','.join(map(str, w)), 0, frozenset(tr((1, 0, 4), rakes[i]) for i in w), frozenset()))
    for g in range(4):
        u0 = -10 + g // 2
        tg = train(g, u0, u0 + 2)
        for u in (u0, u0 + 1):
            live = sorted(c for c in tg if unit(c) == u)
            for r in range(1, len(live) + 1):
                for sub in combinations(live, r):
                    ev.append((f'rm g{g} unit{u - u0} {len(sub)}/{len(live)}', g, frozenset(sub), frozenset()))
            dead = sorted(c for c in TB.cells if unit(c) == u and c not in tg)
            for c in dead:
                ev.append((f'add g{g} unit{u - u0}', g, frozenset(), frozenset([c])))
        wire = frozenset(tr(c, u) for u in (u0, u0 + 1) for c in WIRE[g % 2])
        ev.append((f'wire g{g}', g, tg - wire, wire - tg))
    return ev


EV = events()


def cls(name):
    return name.split(' ')[0] + ('' if name.startswith('word') else ' g' + name.split(' ')[1][1])


def bare_classes(G=100):
    """Each event on the plain train with no end in reach (planes far away, train to unit 120): 'vanishes' (the
    state equals the plain train again), 'rides' (at G the difference is confined to 16 units around the place
    the train has carried the event to), or 'breaks' (it reached the boundary, or is spread wider)."""
    tb = Tube(a.U0, 600)
    x0 = tb.vec(train(0, a.U0 - 1, 121))
    E = len(EV); S = np.repeat(x0[None, :], E + 1, axis=0); idx = {c: i for i, c in enumerate(tb.cells)}
    res = [None] * E
    for t in range(G + 1):
        for j, (nm, g, rem, add) in enumerate(EV):
            if g == t:
                for c in rem: S[j + 1, idx[c]] = 0
                for c in add: S[j + 1, idx[c]] = 1
        if t > 3:
            for j in np.nonzero((S[1:] == S[0]).all(axis=1))[0]:
                res[j] = res[j] or 'vanishes'
        for j in np.nonzero(~tb.boundary_plain(S, t)[1:])[0]:
            res[j] = res[j] or 'breaks'
        if t < G:
            S = tb.step(S, t)
    for j in range(E):
        if res[j] is None:
            d = tb.units[np.nonzero(S[j + 1, :tb.n] != S[0, :tb.n])[0]]
            us = [unit(c) for c in EV[j][2] | EV[j][3]]
            res[j] = 'rides' if d.min() >= min(us) + (G - EV[j][1]) // 2 - 8 and d.max() <= max(us) + (G - EV[j][1]) // 2 + 8 else 'breaks'
    return res


BARE = bare_classes()
print('events on the bare train:', dict(Counter((cls(EV[j][0]), BARE[j]) for j in range(len(EV)))), flush=True)


def run_end(e):
    cap = frozenset(tuple(c) for c in e['cap'])
    x0 = TB.vec((train(0, a.U0 - 1, KS) | cap))
    E = len(EV)
    S = np.repeat(x0[None, :], E + 1, axis=0)
    idx = {c: i for i, c in enumerate(TB.cells)}
    alive = np.ones(E + 1, bool)
    out = [None] * E; echo = []
    near = np.nonzero(TB.units >= KS - 8)[0]
    for t in range(a.tmax + 1):
        for j, (nm, g, rem, add) in enumerate(EV):
            if g == t:
                for c in rem:
                    assert S[j + 1, idx[c]] == 1
                    S[j + 1, idx[c]] = 0
                for c in add:
                    assert S[j + 1, idx[c]] == 0
                    S[j + 1, idx[c]] = 1
        if t > 3:
            eq = (S[1:] == S[0]).all(axis=1) & alive[1:]
            for j in np.nonzero(eq)[0]:
                out[j] = ('healed', t); alive[j + 1] = False
        bp = TB.boundary_plain(S, t)
        assert bp[0], 'plain run disturbed at the boundary'
        for j in np.nonzero(~bp[1:] & alive[1:])[0]:
            endeq = bool((S[j + 1, near] == S[0, near]).all())
            out[j] = ('upstream, end ' + ('unchanged' if endeq else 'changed'), t); alive[j + 1] = False
            if BARE[j] != 'breaks' and len(echo) < 200:
                echo.append(dict(event=EV[j][0], bare=BARE[j], g=EV[j][1], rem=sorted(EV[j][2]), add=sorted(EV[j][3]), t=t, end_unchanged=endeq))
        if not alive[1:].any():
            break
        keep = np.nonzero(alive)[0]
        S2 = TB.step(S[keep], t)
        S[keep] = S2
    persist = []
    for j in np.nonzero(alive[1:])[0]:
        persist.append(dict(event=EV[j][0], bare=BARE[j], g=EV[j][1], rem=sorted(EV[j][2]), add=sorted(EV[j][3]),
                            final=sorted(TB.cells_of(S[j + 1])), plain=sorted(TB.cells_of(S[0])), t=a.tmax))
        out[j] = ('persistent', a.tmax)
    return out, persist, echo


t0 = time.time()
mine = list(range(len(ends)))[pi::pn] if a.only is None else [a.only]
table = Counter(); per_end = []; persist_all = []; tails = Counter(); echo_all = []
for n, i in enumerate(mine):
    out, persist, echo = run_end(ends[i])
    for q in echo:
        q['end'] = i; echo_all.append(q)
    vec = Counter((cls(EV[j][0]) + ' ' + BARE[j], o[0]) for j, o in enumerate(out))
    table.update(vec)
    for j, o in enumerate(out):
        if o[0] == 'healed':
            tails[cls(EV[j][0])] = max(tails[cls(EV[j][0])], o[1])
    per_end.append(dict(end=i, cells=len(ends[i]['cap']), outcomes={f'{k[0]}|{k[1]}': v for k, v in vec.items()}))
    for p in persist:
        p['end'] = i; persist_all.append(p)
    if n % 25 == 0:
        print(f'{n + 1}/{len(mine)} ends, {time.time() - t0:.0f}s, persistent so far {len(persist_all)}', flush=True)
print(f'part {a.part}: {len(mine)} ends x {len(EV)} events, {time.time() - t0:.0f}s')
for k in sorted(table):
    print(f'  {k[0]:20s} {k[1]:28s} {table[k]}')
print('  longest heal by class:', dict(tails))
print('  persistent rows:', len(persist_all), '; rows of riding/vanishing events that went upstream:', len(echo_all))
if a.out:
    json.dump(dict(events=[(e[0], e[1]) for e in EV], table={f'{k[0]}|{k[1]}': v for k, v in table.items()},
                   per_end=per_end, persistent=persist_all, upstream_from_riding=echo_all, tails={f'{k[0]}': v for k, v in tails.items()}),
              open(a.out, 'w'))
