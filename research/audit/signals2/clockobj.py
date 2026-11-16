"""The clock of research/signals/objects/clock-C.json, rebuilt from the file's cell lists (no study code)."""
import json, os
import gs
F = os.path.join(gs.ROOT, 'research', 'signals', 'objects', 'clock-C.json')
ob = json.load(open(F))
capL = [tuple(c) for c in ob['capL']]; UNIT = [tuple(c) for c in ob['unit']]; capR = [tuple(c) for c in ob['capR']]
IGN = tuple(ob['ignite'])
DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]


def obj(N):
    s = set(capL) | {gs.tr(c, k) for c in UNIT for k in range(N)} | {gs.tr(c, N) for c in capR}
    assert len(s) == 32 + 5 * N
    return frozenset(s)


def ign(N):
    return gs.tr(IGN, N // 2)


def hull_bounds(cells):
    return [(d, min(sum(a * b for a, b in zip(d, c)) for c in cells), max(sum(a * b for a, b in zip(d, c)) for c in cells)) for d in DIAG]


def in_hull(bounds):
    return lambda p: all(lo <= d[0] * p[0] + d[1] * p[1] + d[2] * p[2] <= hi for d, lo, hi in bounds)


def hull_dom(cells):
    """All cells in the diagonal hull of `cells` (exact domain for anything started inside it, by T2)."""
    b = hull_bounds(cells); ins = in_hull(b)
    return gs.Dom(gs.closure(cells, ins)), b
