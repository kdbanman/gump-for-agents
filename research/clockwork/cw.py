"""Shared helpers for the clockwork study (P66.27a and kin).  Cells: doubled-coordinate tuples."""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, os.path.join(ROOT, 'research', 'atlas'))
from lattice import (step, nbrs, axis, apply, normal, canon, GROUP, DIAGS, components,  # noqa: E402,F401
                     oracle_orbit, period, canonical_orbit, spacetime_sym, thickness)

CAT = os.path.join(ROOT, 'research', 'atlas', 'catalogue.jsonl')
SCR = os.path.join(ROOT, 'research', 'scratch', 'clockwork')
os.makedirs(SCR, exist_ok=True)


def catalogue():
    return {o['id']: o for o in map(json.loads, open(CAT))}


def obj(oid):
    return frozenset(map(tuple, catalogue()[oid]['cells']))


def orbit(cells, n):
    out = [frozenset(cells)]
    for _ in range(n):
        out.append(step(out[-1]))
    return out


def read_cells(fn):
    out = []
    for line in open(fn):
        line = line.split('#')[0].split()
        if len(line) == 3:
            out.append(tuple(map(int, line)))
    return frozenset(out)


def write_cells(fn, cells, header=''):
    with open(fn, 'w') as f:
        for h in header.splitlines():
            f.write('# ' + h + '\n')
        for c in sorted(cells):
            f.write('%d %d %d\n' % c)


def find_map(a, b):
    """All (g, t) with g in O_h, t an even translation, g(a)+t == b."""
    out = []
    a = list(a); b = frozenset(b)
    mb = [min(c[k] for c in b) for k in range(3)]
    for g in GROUP:
        img = apply(g, a)
        mi = [min(c[k] for c in img) for k in range(3)]
        t = tuple(mb[k] - mi[k] for k in range(3))
        if any(v % 2 for v in t):
            continue
        if frozenset(tuple(c[k] + t[k] for k in range(3)) for c in img) == b:
            out.append((g, t))
    return out


def gmat(g):
    p, s = g
    M = [[0] * 3 for _ in range(3)]
    for k in range(3):
        M[k][p[k]] = s[k]
    return M


def exact_period(cells, maxp=5000):
    r = period(cells, maxp)
    return r


# ---------------------------------------------------------------- batch runner (runinit.c)
import subprocess  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, 'research', 'atlas'))
from vessel import octa, classify_final  # noqa: E402
RUNINIT = os.path.join(SCR, 'runinit')


def build_runinit():
    src = os.path.join(HERE, 'runinit.c')
    if not os.path.exists(RUNINIT) or os.path.getmtime(RUNINIT) < os.path.getmtime(src):
        subprocess.check_call(['gcc', '-O2', '-o', RUNINIT, src])


def vessel_for(cells, margin=4):
    """Octahedral (L1-ball) vessel holding the pattern with `margin` doubled units to spare: exact by T2."""
    cells = list(cells)
    c = tuple(int(round(sum(p[k] for p in cells) / len(cells))) for k in range(3))
    r = max(sum(abs(p[k] - c[k]) for k in range(3)) for p in cells) + margin
    v = octa(c, r)
    v.index = {p: i for i, p in enumerate(v.cells)}
    return v


def run_batch(v, inits, maxgen=100000, tag='batch'):
    """Run each initial cell set to its final cycle in vessel v.  Returns list of dicts (mu, period, final cells)."""
    build_runinit()
    vf = os.path.join(SCR, f'v_{tag}_{os.getpid()}.bin'); v.write(vf)
    inp = '\n'.join(' '.join(str(v.index[p]) for p in s) for s in inits) + '\n'
    out = subprocess.run([RUNINIT, vf, str(maxgen)], input=inp, capture_output=True, text=True, check=True).stdout
    os.remove(vf)
    res = []
    for line in out.splitlines():
        head, _, tail = line.partition(':')
        mu, per, pop = map(int, head.split())
        res.append(dict(mu=mu, period=per, pop=pop, live=frozenset(v.cells[int(i)] for i in tail.split())))
    return res


def objects(v, r):
    """R-connected objects of a final cycle: list of (period, canonical key)."""
    if not r['period'] or not r['live']:
        return []
    return classify_final(v, [v.index[p] for p in r['live']], r['period'])


def fmt_key(k):
    return ' '.join('%d,%d,%d' % c for c in k)


# ---------------------------------------------------------------- diagonal hulls as vessels
from vessel import Vessel  # noqa: E402
DIAG4 = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]


def dot(d, p):
    return d[0] * p[0] + d[1] * p[1] + d[2] * p[2]


def hull_ranges(cells):
    return [(min(dot(d, p) for p in cells), max(dot(d, p) for p in cells)) for d in DIAG4]


def hull_cells(ranges):
    """All cells p with lo_d <= d.p <= hi_d for the 4 diagonals: an exact vessel by T2.
    Uses s1 = s2 + s3 + s4 and p = ((s2+s3)/2, (s2+s4)/2, (s3+s4)/2)."""
    (l1, h1), (l2, h2), (l3, h3), (l4, h4) = ranges
    out = []
    odd = lambda lo, hi: range(lo | 1, hi + 1, 2)
    for s2 in odd(l2, h2):
        for s3 in odd(l3, h3):
            for s4 in odd(l4, h4):
                if not (l1 <= s2 + s3 + s4 <= h1):
                    continue
                p = ((s2 + s3) // 2, (s2 + s4) // 2, (s3 + s4) // 2)
                if (p[0] & 1) + (p[1] & 1) + (p[2] & 1) == 1:
                    out.append(p)
    return sorted(out)


def cell_vessel(cells):
    cells = sorted(cells)
    idx = {p: i for i, p in enumerate(cells)}
    v = Vessel(cells, [[idx.get(q, -1) for q in nbrs(p)] for p in cells])
    v.index = idx
    return v
