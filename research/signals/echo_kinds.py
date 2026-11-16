#!/usr/bin/env python3
"""Every one-cell change of the plain rake train, and what it becomes (README section 30).

    python3 echo_kinds.py        (about 30 s; sg.step_set on a finite piece, exact on the units compared)

Each cell of the 3 x 3 tube in units 0, 1, flipped (removed if live, added if dead) at each train phase f = 0..3
(112 events), run 41 to 44 generations to a generation at which the train is at phase 1: 'vanish' (no difference),
one of the signals E, U, H, K0 of echo6.SIG1 (the difference is exactly that signal, echo6.decompose), or 'break'
(anything else; in every such case here the difference has more than 8 cells and is still growing).
"""
from collections import Counter, defaultdict
import echo6 as E

A = 70
cnt = Counter(); ex = defaultdict(list)
for f in range(4):
    P = E.train(f, -A, A)
    for u in (0, 1):
        for c in E.tube_cells(u):
            S = (P - {c}) if c in P else (P | {c})
            g = 41 + ((1 - f - 41) % 4)          # (f + g) % 4 == 1
            D = E.diff_run(S, f, g, A)
            assert E.exact_ok(D, A)
            d = D[g]
            if not d:
                k = 'vanish'
            else:
                r = E.decompose(d)
                k = r[0][0] if r and len(r) == 1 else 'break'
                if k == 'break':
                    assert len(d) > 8 and len(d) > len(D[g - 8]), (f, c)
            cnt[k] += 1
            ex[k].append((f, u, c, 'remove' if c in P else 'add'))
print(dict(cnt), 'of', sum(cnt.values()))
for k in ('E', 'U', 'H', 'K0'):
    print(k, ex[k])
