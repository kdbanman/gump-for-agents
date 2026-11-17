#!/usr/bin/env python3
"""The rigid signals of the rake train in the absorber frame of push 7 (train (fb)^inf moving +v into the end, as in
`sat_gun.py fb C --dir 1`), found from scratch: every one-cell flip of the plain train inside the 5 x 5 tube on units
0, 1 at each of the four phases, and every two-cell flip inside the 3 x 3 tube on units 0, 1 (both cells at one
generation), each run with sg.step_set on a finite piece of train (units -150..149, exact on the units compared for
the generations used) and classified:
  'vanish'  no difference after 40 generations;
  'ride'    the difference D(t) = state xor train is non-empty, of at most 12 cells, and for t = 40..80 step 2,
            D(t + 2) = D(t) moved by +1 unit (down: with the train, towards the end) or -1 unit (up): a rigid signal;
            its canonical form (D at the first t >= 40 with t = 1 mod 4, moved so that its lowest unit is 0 or 1
            keeping the unit parity) names it;
  'other'   anything else (breaks the stream, or two signals, or a front).
Each riding kind is then proved to ride for ever by the two-generation identity of `prove_echo.py`: the train xor D
at phase 1 on units -30..29, stepped twice on the infinite lattice, equals on units -27..26 the train at phase 3 xor
D moved one unit in its direction.

    python signals7.py [--two] [--train5f]     (one-cell flips: 15 s; --two adds the two-cell flips: 1.5 min)
--train5f: the same in the gun frame (train (5f)^inf moving -v), written to signals7_5f.json.
Writes research/signals/push7/signals7.json: the kinds with direction, size, cells at phase 1, and the events that
make them.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sg, sat_gun as G
from scat import unit, tr
from geom7 import tube_cells
from step7 import Window, INDEX

TRAIN = '5f' if '--train5f' in sys.argv else 'fb'      # 5f: the gun frame (the train (5f)^inf moving -v)
TDIR = 1 if TRAIN == 'fb' else -1
pat, _ = G.train([int(ch, 16) for ch in TRAIN], True, TDIR)
train = lambda t, a, b: G.train_cells(pat, t, a, b, TDIR)
A, B = -150, 150


def shift(s, k):
    return frozenset(tr(c, k) for c in s)


def canon(D):
    m = min(unit(c) for c in D); m -= m % 2         # keep the parity of the lowest unit
    return tuple(sorted(tr(c, -m) for c in D))


RW = None


def classify(g, flips):
    """Ring mode of step7 (checked against the oracle by check7.py): a ring of 160 units, the flips at units 80, 81."""
    global RW
    if RW is None:
        RW = Window(TRAIN, 0, 160)
    x = RW.train(g)
    for c in flips:
        c = tr(c, 80); u = unit(c); x[u, INDEX[tr(c, -u)]] ^= 1
    t = g; seq = {}
    while t < 84:
        RW.run(x, t, 1, 'ring'); t += 1
        if t >= 40:
            seq[t] = frozenset(tr(c, -80) for c in RW.cells(x ^ RW.train(t)))
    if not seq[40] and not seq[83]:
        return 'vanish', None
    for d in (1, -1):
        if all(seq[t] and len(seq[t]) <= 12 and shift(seq[t], d) == seq[t + 2] for t in range(40, 81, 2)):
            t1 = next(t for t in range(40, 50) if t % 4 == 1)
            return ('down' if d == TDIR else 'up'), canon(seq[t1])
    return 'other', None


def prove(cells, d):
    D = frozenset(tuple(c) for c in cells)
    x = train(1, -30, 30) ^ D
    for _ in range(2):
        x = sg.step_set(x)
    lhs = frozenset(c for c in x if -27 <= unit(c) < 27)
    rhs = frozenset(c for c in (train(3, -40, 40) ^ shift(D, d)) if -27 <= unit(c) < 27)
    return lhs == rhs


def main():
    two = '--two' in sys.argv
    E5, O5 = tube_cells(-1, 7); E3, O3 = tube_cells(1, 5)
    in3 = set(E3 + O3)
    kinds = {}; tally = {}
    def note(ev, res):
        cls, key = res
        tally[(ev['n'], cls)] = tally.get((ev['n'], cls), 0) + 1
        if key is not None:
            k = kinds.setdefault(key, dict(dir=cls, cells=[list(c) for c in key], events=[]))
            if len(k['events']) < 6:
                k['events'].append(ev)
    base = [tr(c, u) for u in (0, 1) for c in E5 + O5]
    t3 = {}
    for g in range(4):
        for c in base:
            r = classify(g, [c]); i3 = tr(c, -unit(c)) in in3
            note(dict(n=1, gen=g, cells=[list(c)], in3=i3), r)
            t3[(i3, r[0])] = t3.get((i3, r[0]), 0) + 1
    print('one-cell flips (inside the 3 x 3 tube?, class):', t3, flush=True)
    if two:
        b3 = [c for c in base if tr(c, -unit(c)) in in3]
        for g in range(4):
            for c1, c2 in itertools.combinations(b3, 2):
                note(dict(n=2, gen=g, cells=[list(c1), list(c2)]), classify(g, [c1, c2]))
        print('with two-cell flips:', {k: v for k, v in tally.items()}, flush=True)
    out = []
    for key, k in kinds.items():
        k['size'] = len(key); k['proved'] = prove(key, TDIR if k['dir'] == 'down' else -TDIR)
        k['parity'] = min(unit(tuple(c)) for c in key) % 2
        out.append(k)
    out.sort(key=lambda k: (k['dir'], k['size'], k['cells']))
    for i, k in enumerate(out):
        print(f"kind {i}: {k['dir']:4s} {k['size']} cells, lowest unit parity {k['parity']}, proved {k['proved']}: "
              f"{k['cells']}  made by e.g. {k['events'][0]}")
    json.dump(dict(frame=f'train ({TRAIN})^inf moving {TDIR:+d} unit per 2 generations, sat_gun.train(.., True, {TDIR}); '
                         'down = with the train, up = against it; D at train phase 1 (t = 1 mod 4) as cells relative '
                         'to an even unit',
                   tally={f'{a}-cell {b}': v for (a, b), v in tally.items()}, kinds=out),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signals7.json' if TRAIN == 'fb' else 'signals7_5f.json'), 'w'), indent=0)


def tr_in3(c, in3):
    return {c} if tr(c, -unit(c)) in in3 else set()


if __name__ == '__main__':
    main()
