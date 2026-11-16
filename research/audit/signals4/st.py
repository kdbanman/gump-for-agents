"""Independent sparse stepper for gump (B45/S345 on the faces of the cubic honeycomb), written for REVIEW-signals-4
from docs/AUTOMATON.md section 2 only (no code shared with research/signals/sg.py).  Infinite lattice, no torus.
Checked cell for cell against reference/oracle.py by oracle_check.py."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
OBJ = os.path.join(ROOT, 'research', 'signals', 'objects')


def _offs(a):
    b, c = [i for i in range(3) if i != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for t in (b, c):
            for st in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[t] = st; out.append(tuple(o))
    return out


OFFS = [_offs(a) for a in range(3)]


def axis(c):
    odd = [i for i in range(3) if c[i] & 1]
    assert len(odd) == 1, c
    return odd[0]


def step(live):
    cnt = {}
    for c in live:
        for o in OFFS[axis(c)]:
            n = (c[0] + o[0], c[1] + o[1], c[2] + o[2])
            cnt[n] = cnt.get(n, 0) + 1
    return frozenset(c for c, k in cnt.items() if (k in (4, 5)) or (k == 3 and c in live))


def run(cells, gens):
    out = [frozenset(cells)]
    for _ in range(gens):
        out.append(step(out[-1]))
    return out


def tr(c, k):
    return (c[0] + 2 * k, c[1], c[2] - 2 * k)


def trs(cs, k):
    return frozenset(tr(c, k) for c in cs)


def U(c):
    return c[0] >> 1


def load(name):
    d = json.load(open(os.path.join(OBJ, name)))
    return {k: ([tuple(c) for c in v] if isinstance(v, list) and v and isinstance(v[0], list) else v) for k, v in d.items()}


def cells_file(path):
    return frozenset(tuple(int(x) for x in l.split()) for l in open(path) if l.strip() and not l.startswith('#'))


DIAG = [(1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)]


def hull(cells):
    return [(d, min(sum(d[i] * c[i] for i in range(3)) for c in cells), max(sum(d[i] * c[i] for i in range(3)) for c in cells)) for d in DIAG]


def inside(cells, h):
    return all(lo <= sum(d[i] * c[i] for i in range(3)) <= hi for c in cells for d, lo, hi in h)


# ---- the objects, built from the JSON files as the README describes them ----
L = load('line-C.json'); B = load('beam-5f.json'); D = load('divider-C8.json')


def line(N):
    return frozenset(L['capA']) | frozenset(tr(c, k) for c in L['unit'] for k in range(N)) | trs(L['gun'], N)


def beam(N):
    s = set(B['left']) | trs(B['R_odd'] if N % 2 else B['R_even'], N)
    for k in range(N):
        s |= trs(B['b1'] if k % 2 else B['b0'], k)
    return frozenset(s)


def divider(N, osc_shift=None, osc=None):
    osc = D['osc'] if osc is None else osc
    return frozenset(D['capA']) | frozenset(tr(c, k) for c in D['unit'] for k in range(N)) | trs(D['gun'], N) | trs(osc, N if osc_shift is None else osc_shift)


def period_from(xs, t0, p, upto):
    """xs[t+p] == xs[t] for t0 <= t <= upto - p, and xs[t + p/2] != xs[t] there (period exactly p if p in 4, 8)."""
    return all(xs[t + p] == xs[t] for t in range(t0, upto - p + 1)) and all(xs[t + p // 2] != xs[t] for t in range(t0, upto - p + 1))


def onset(xs, p):
    """least t0 with xs[t+p] == xs[t] for all t >= t0 in the run."""
    n = len(xs)
    t0 = n - p
    while t0 > 0 and xs[t0 - 1 + p] == xs[t0 - 1]:
        t0 -= 1
    return t0
