"""Shared lattice utilities for the atlas: sparse stepping, symmetry, canonical forms, descriptors,
and verification against reference/oracle.py.  Cells are doubled-coordinate tuples (exactly one odd).
"""
import itertools, os, sys
from collections import Counter
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'reference'))
import oracle  # noqa: E402

OFFS = [oracle.offsets(a) for a in range(3)]
DIAGS = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)]
GROUP = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]


def axis(c):
    return [i for i in range(3) if c[i] & 1][0]


def nbrs(c):
    x, y, z = c
    return [(x + o[0], y + o[1], z + o[2]) for o in OFFS[axis(c)]]


def step(live):
    """One generation of the infinite-lattice automaton on a set of cells."""
    cnt = Counter()
    for c in live:
        for n in nbrs(c):
            cnt[n] += 1
    return frozenset(c for c, k in cnt.items() if (k in (4, 5)) or (k == 3 and c in live))


def apply(g, cells):
    p, s = g
    return [tuple(s[k] * c[p[k]] for k in range(3)) for c in cells]


def normal(cells):
    """Translate by an even vector so each coordinate's minimum is 0 or 1; return sorted tuple."""
    cells = list(cells)
    mn = [min(c[k] for c in cells) for k in range(3)]
    sh = [2 * (m // 2) for m in mn]
    return tuple(sorted(tuple(c[k] - sh[k] for k in range(3)) for c in cells))


def canon(cells):
    return min(normal(apply(g, cells)) for g in GROUP)


def sym_order(cells):
    """Order of the stabiliser in (even translations) x O_h."""
    n0 = normal(cells)
    return sum(1 for g in GROUP if normal(apply(g, cells)) == n0)


def thickness(cells):
    """Number of {111} layers spanned along each of the 4 body diagonals (sorted)."""
    t = []
    for d in DIAGS:
        s = [d[0] * c[0] + d[1] * c[1] + d[2] * c[2] for c in cells]
        t.append((max(s) - min(s)) // 2 + 1)
    return tuple(sorted(t))


def components(cells, dist=1):
    """Connected components under the neighbour relation (dist=1) or 'share a neighbour' (dist=2)."""
    cells = set(cells); seen = set(); comps = []
    for c in cells:
        if c in seen:
            continue
        comp = []; stack = [c]; seen.add(c)
        while stack:
            u = stack.pop(); comp.append(u)
            near = set(nbrs(u))
            if dist == 2:
                near |= {w for v in nbrs(u) for w in nbrs(v)}
            for v in near:
                if v in cells and v not in seen:
                    seen.add(v); stack.append(v)
        comps.append(frozenset(comp))
    return comps


def period(cells, maxp=10000):
    """Return (preperiod, period) of the orbit of a finite pattern, or None if not found within maxp."""
    seen = {}
    cur = frozenset(cells)
    for t in range(maxp + 1):
        if cur in seen:
            return seen[cur], t - seen[cur]
        seen[cur] = t
        cur = step(cur)
    return None


def is_strict_still(cells):
    """True if no nonempty proper union of neighbour-components is itself a still life with the rest."""
    comps = components(cells, 1)
    k = len(comps)
    if k == 1:
        return True
    for mask in range(1, 2 ** (k - 1)):
        a = frozenset().union(*[comps[i] for i in range(k) if mask >> i & 1])
        b = frozenset(cells) - a
        if step(a) == a and step(b) == b:
            return False
    return True


def oracle_orbit(cells, gens):
    """Step the pattern with reference/oracle.py on a padded even torus; return list of cell sets."""
    cells = list(cells)
    mn = [min(c[k] for c in cells) for k in range(3)]
    mx = [max(c[k] for c in cells) for k in range(3)]
    pad = 2 * (max(mx[k] - mn[k] for k in range(3)) // 2) + 12   # hull is at most ~3x the box
    H = max(mx[k] - mn[k] for k in range(3)) + 2 * pad
    H += H % 2
    sh = [pad - 2 * (mn[k] // 2) for k in range(3)]
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + sh[0], c[1] + sh[1], c[2] + sh[2]] = 1
    out = [frozenset(cells)]
    for _ in range(gens):
        h = oracle.step(h, m)
        out.append(frozenset(tuple(int(v) - sh[k] for k, v in enumerate(p)) for p in np.argwhere(h)))
    return out


def oracle_verify(cells, per):
    """Check with the oracle that the pattern returns to itself after `per` steps and not before."""
    orb = oracle_orbit(cells, per)
    s0 = frozenset(map(tuple, cells))
    return orb[per] == s0 and all(orb[t] != s0 for t in range(1, per))


def fmt(cells):
    return ' '.join('%d,%d,%d' % c for c in cells)


def parse(s):
    return tuple(tuple(int(v) for v in t.split(',')) for t in s.split())
