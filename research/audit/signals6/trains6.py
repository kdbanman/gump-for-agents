"""The plain rake train in the two frames used here, and the signal reader.

Push frame (objects/line-C.json; echo-train.json): train(t) unit u holds BASE[t%4][u%2] moved u units; the train
moves towards -v (decreasing unit) one unit per 2 generations.  BASE is initial data read from
research/signals/objects/echo-train.json and checked here (with st6.step) to be an orbit of the infinite train.

Review-5 frame (research/audit/signals5/st5.py, the ends of the census): train5(t) unit u holds PAT[t%2][(u-t//2)%2];
moves towards +v.  PAT is initial data copied from st5.py and checked here the same way.
"""
import json, os
import numpy as np
import st6
from st6 import tr, trs, units, unit_of, ROOT

J = json.load(open(os.path.join(ROOT, 'research', 'signals', 'objects', 'echo-train.json')))
BASE = [[frozenset(tuple(c) for c in J['base'][t][p]) for p in (0, 1)] for t in range(4)]


def train(t, ua, ub):
    return frozenset(tr(c, u) for u in range(ua, ub) for c in BASE[t % 4][u % 2])


PAT = [[frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2), (1, 0, 4)]),
        frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)])],
       [frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4)]),
        frozenset([(0, 0, 1), (0, 0, 3), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)])]]


def train5(t, ua, ub):
    return frozenset(tr(c, u) for u in range(ua, ub) for c in PAT[t % 2][(u - t // 2) % 2])


def check():
    for t in range(4):
        assert units(st6.step(train(t, -30, 30)), -28, 28) == train(t + 1, -28, 28), t
        assert units(train(t + 2, -30, 30), -20, 20) == units(trs(train(t, -30, 30), -1), -20, 20)
        assert units(st6.step(train5(t, -30, 30)), -28, 28) == train5(t + 1, -28, 28), t
        assert units(train5(t + 2, -30, 30), -20, 20) == units(trs(train5(t, -30, 30), 1), -20, 20)
    assert all(st6.in_tube(c) for c in train(0, 0, 2) | train(1, 0, 2) | train5(0, 0, 2) | train5(1, 0, 2))
    return True


SIG = {k: (v['parity'], frozenset(tuple(c) for c in v['cells']), v['dir']) for k, v in J['sig'].items()}


def sig(kind, u):
    par, cells, _ = SIG[kind]
    assert u % 2 == par
    return trs(cells, u)


def components(d, gap=3):
    """Split a difference into clusters of units separated by at least `gap` empty units."""
    if not d:
        return []
    us = sorted(set(unit_of(c) for c in d))
    groups = [[us[0]]]
    for u in us[1:]:
        if u - groups[-1][-1] > gap:
            groups.append([u])
        else:
            groups[-1].append(u)
    return [frozenset(c for c in d if g[0] <= unit_of(c) <= g[-1]) for g in groups]


def shape(d):
    u0 = min(unit_of(c) for c in d)
    return (u0 % 2, tuple(sorted(tr(c, -u0) for c in d)))
