"""Lead's own check of the sixth signals push (2026-11-15): four signals ride the rake train, and what each pair
of opposite-moving signals does when it meets.

Claims (research/signals/README.md sections 30, 31): the plain rake train carries four rigid signals, E and U
moving up the stream and H (the hole) and K0 moving down, each one unit per two generations; U meets K0: both
vanish exactly; E meets H and U meets H: the stream between two spreading edges becomes a uniform wire (wire B);
E meets K0: behind an edge moving up, every rake is left with one cell missing.

Here: reference/oracle.py only, on a ring of 48 units (a 96-torus), from the cell tables of
research/signals/objects/echo-train.json (the train's unit cells at each phase, each signal's cells).  None of the
push's code.  Checked, with D(t) = run XOR plain train, over the whole torus:
  0  the table is the rule's own: one oracle step of train(t) is train(t + 1), for a whole period;
  1  each signal alone: D keeps its cell count at every second generation and D(t + 2) is D(t) moved by the
     stated one unit, for 80 generations;
  2  U and K0 on a collision course: D is empty from some generation on;
  3  E or U against H: D never empties, its span along the ring grows by two units every two generations, and well
     inside the span the state is the same in every unit (a uniform wire, not the train, whose repeat is two units),
     but for at most one unit left where the two met (the push reports one such unit for E, none for U);
  4  E against K0: D never empties, and well inside its span D is exactly one cell per rake, the same cell in each.

    python3 research/audit/signals_meet_lead_check.py        (about 80 s)
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'reference'))
import oracle

H, R = 96, 48
OFF = (0, 48, 48)
ob = json.load(open(os.path.join(HERE, '..', 'signals', 'objects', 'echo-train.json')))
m = oracle.masks(H); valid = m[0] | m[1] | m[2]
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)


def arr(cs):
    h = np.zeros((H, H, H), dtype=bool)
    for c in cs:
        x = tuple((c[i] + OFF[i]) % H for i in range(3))
        assert valid[x], c
        h[x] = True
    return h


def train(t):
    return arr({tr(tuple(c), u) for u in range(R) for c in ob['base'][t % 4][u % 2]})


def sig(k, u):
    assert u % 2 == ob['sig'][k]['parity']
    return arr({tr(tuple(c), u) for c in ob['sig'][k]['cells']})


def shift(a, k):
    return np.roll(np.roll(a, 2 * k, axis=0), -2 * k, axis=2)


def units(a):                                     # ring units (x // 2) that hold a cell of a
    return sorted({int(x) // 2 for x in np.argwhere(a)[:, 0]})


def arc(us):                                      # (first unit, length) of the shortest arc of the ring holding the units
    if len(us) < 2:
        return (us[0] if us else 0), len(us)
    gaps = [(us[(i + 1) % len(us)] - us[i]) % R for i in range(len(us))]
    i = int(np.argmax(gaps))
    return us[(i + 1) % len(us)], R - gaps[i] + 1


span = lambda us: arc(us)[1]


def run(x, T):
    out = []
    for t in range(T + 1):
        out.append(x ^ train(1 + t)); x = oracle.step(x, m)
    return out, x


ok = True
t0 = all(np.array_equal(oracle.step(train(t), m), train(t + 1)) for t in range(4))
ok &= t0
print(f'0  one oracle step of the table\'s train is its next phase, a whole period: {t0}')
for k in ('E', 'U', 'H', 'K0'):
    D, _ = run(train(1) ^ sig(k, 10 + ob['sig'][k]['parity']), 80)
    n = len(ob['sig'][k]['cells']); d = ob['sig'][k]['dir']
    good = all(int(D[t].sum()) == n for t in range(0, 81, 2)) and all(np.array_equal(D[t + 2], shift(D[t], d)) for t in range(0, 79, 2))
    ok &= good
    print(f'1  {k}: {n} cell(s), moving {d:+d} unit per two generations (the train moves -1), rigid for 80 generations: {good}')
for a, ua, b, ub in (('U', 1, 'K0', 20), ('E', 0, 'H', 21), ('U', 1, 'H', 21), ('E', 0, 'K0', 20)):
    D, x = run(train(1) ^ sig(a, ua) ^ sig(b, ub), 60)
    n = [int(d.sum()) for d in D]
    if (a, b) == ('U', 'K0'):
        first = next((t for t in range(61) if n[t] == 0), None)
        good = first is not None and all(v == 0 for v in n[first:])
        print(f'2  U meets K0: the whole torus is the plain train from generation {first} on: {good}')
    else:
        us = units(D[60]); sp = [span(units(D[t])) for t in (40, 50, 60)]
        grow = min(n[20:]) > 0 and sp[1] - sp[0] in (9, 10, 11) and sp[2] - sp[1] in (9, 10, 11)
        lo = arc(us)[0]
        inner = [(lo + j) % R for j in range(8, sp[2] - 8)]
        def unit_cells(a_, u):                    # cells of ring unit u, moved to unit 0
            s = np.argwhere(a_)
            return frozenset((int(c[0]) - 2 * u, int(c[1]), (int(c[2]) + 2 * u - OFF[2]) % H) for c in s if int(c[0]) // 2 == u)
        if b == 'H':
            from collections import Counter
            kc = Counter(unit_cells(x, u) for u in inner)
            main, nmain = kc.most_common(1)[0]
            plain = {unit_cells(train(61), u) for u in inner}
            odd_units = [u for u in inner if unit_cells(x, u) != main]
            good = grow and len(odd_units) <= 1 and main not in plain
            print(f'3  {a} meets H: the difference never empties, its span is {sp} units at generations 40, 50, 60; '
                  f'inside, {nmain} of {len(inner)} units hold the same {len(main)} cells (not the train\'s); '
                  f'units that hold something else: {odd_units}: {good}')
        else:
            dk = [unit_cells(D[60], u) for u in inner]
            even, odd = {d for u, d in zip(inner, dk) if u % 2 == 0}, {d for u, d in zip(inner, dk) if u % 2 == 1}
            good = grow and len(even) == 1 and len(odd) == 1 and sorted(len(next(iter(s))) for s in (even, odd)) == [0, 1]
            print(f'4  E meets K0: the difference never empties, span {sp}; inside, {len(inner)} units: one cell missing '
                  f'or added in every second unit, the same cell each time, none in the others: {good}')
    ok &= good
print('PASS' if ok else 'FAIL')
