"""Helper for the explainer: verify fauna with reference/oracle.py, compute twists, decompose legacy ash.
Read-only on the repo. Writes fauna_out.json next to this script."""
import sys, os, json, itertools, glob, collections
import numpy as np
REPO = '/home/user/gump-for-agents'
sys.path.insert(0, os.path.join(REPO, 'reference'))
import oracle  # noqa: E402
HERE = os.path.dirname(os.path.abspath(__file__))

def valid(c):
    return sum(v % 2 for v in c) == 1

def nbr_offsets(a):
    b, c = [k for k in range(3) if k != a]
    out = []
    for sb in (2, -2):
        for sc in (2, -2):
            o = [0, 0, 0]; o[b] = sb; o[c] = sc; out.append(tuple(o))
    for sa in (1, -1):
        for k in (b, c):
            for sk in (1, -1):
                o = [0, 0, 0]; o[a] = sa; o[k] = sk; out.append(tuple(o))
    return out
OFF = [nbr_offsets(a) for a in range(3)]
def axis(c):
    return [k for k in range(3) if c[k] % 2][0]
def nbrs(c):
    return [tuple(c[k] + o[k] for k in range(3)) for o in OFF[axis(c)]]

# --- oracle orbit on a padded even array torus (open space is exact while the hull fits, T2)
def oracle_orbit(cells, gens):
    cells = [tuple(c) for c in cells]
    mn = [min(c[k] for c in cells) for k in range(3)]
    mx = [max(c[k] for c in cells) for k in range(3)]
    span = max(mx[k] - mn[k] for k in range(3))
    pad = 2 * span + 12
    H = span + 2 * pad; H += H % 2
    sh = [pad - 2 * (mn[k] // 2) for k in range(3)]
    m = oracle.masks(H)
    h = np.zeros((H, H, H), np.int8)
    for c in cells:
        h[c[0] + sh[0], c[1] + sh[1], c[2] + sh[2]] = 1
    out = [frozenset(cells)]
    for _ in range(gens):
        h = oracle.step(h, m)
        pts = np.argwhere(h)
        if len(pts):
            assert pts.min() > 0 and pts.max() < H - 1, 'touched edge'
        out.append(frozenset(tuple(int(v) - sh[k] for k, v in enumerate(p)) for p in pts))
    return out

def exact_period(orb):
    s0 = orb[0]
    for t in range(1, len(orb)):
        if orb[t] == s0:
            return t
    return None

GROUP = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
def apply(g, cells):
    p, s = g
    return [tuple(s[k] * c[p[k]] for k in range(3)) for c in cells]
def norm(cells):
    mn = [min(c[k] for c in cells) for k in range(3)]
    t = [-2 * (v // 2) for v in mn]
    return tuple(sorted(tuple(c[k] + t[k] for k in range(3)) for c in cells))
def canon(cells):
    return min(norm(apply(g, cells)) for g in GROUP)

def gmat(g):
    p, s = g
    M = np.zeros((3, 3), int)
    for k in range(3):
        M[k, p[k]] = s[k]
    return M

def find_maps(a, b):
    """(g, t) with g(a) + t == b, t even."""
    out = []; b = frozenset(b); a = list(a)
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

def kind(g, t):
    M = gmat(g); t = np.array(t); I = np.eye(3, dtype=int)
    if (M == I).all():
        return 'translation' if t.any() else 'identity'
    det = round(np.linalg.det(M)); order = next(k for k in range(1, 7) if (np.linalg.matrix_power(M, k) == I).all())
    if det == 1:
        S = sum(np.linalg.matrix_power(M, i) for i in range(order)) @ t
        return ('screw-rotation' if S.any() else 'rotation') + '-%d' % order
    if (M == -I).all():
        return 'inversion'
    if order == 2:
        par = (M @ t + t)
        return 'glide-mirror' if par.any() else 'mirror'
    return 'rotoreflection-S%d' % order

def twist(orb, P):
    """smallest L > 0 with phase L a symmetric image of phase 0 (L divides P); returns L, m, kinds."""
    for L in range(1, P + 1):
        if P % L:
            continue
        maps = find_maps(orb[0], orb[L]) if len(orb[L]) == len(orb[0]) else []
        if L == P:
            return P, 1, ['identity']
        if maps:
            return L, P // L, sorted(set(kind(g, t) for g, t in maps))

def centre(cells):
    mean = [sum(c[k] for c in cells) / len(cells) for k in range(3)]
    t = [-2 * round(v / 2) for v in mean]
    return sorted(tuple(c[k] + t[k] for k in range(3)) for c in cells), t

def read_cells(fn):
    out = []
    for l in open(fn):
        l = l.split('#')[0].split()
        if len(l) == 3:
            out.append(tuple(map(int, l)))
    return out

CAT = {o['id']: o for o in map(json.loads, open(os.path.join(REPO, 'research/atlas/catalogue.jsonl')))}

def per_cell_periods(orb, P):
    cells = set().union(*orb[:P])
    cnt = collections.Counter()
    for c in cells:
        seq = [c in orb[t] for t in range(P)]
        q = next(q for q in range(1, P + 1) if P % q == 0 and all(seq[t] == seq[(t + q) % P] for t in range(P)))
        cnt[q] += 1
    return dict(sorted(cnt.items()))

res = {}
want = {'S6a': ('cat', 'S6a'), 'S12a': ('cat', 'S12a'), 'P2.6a': ('cat', 'P2.6a'), 'S8b': ('cat', 'S8b'),
        'P66.27a': ('cat', 'P66.27a'),
        'C48.24a': ('file', 'research/clockwork/objects/C48.24a.cells'),
        'C36.33a': ('file', 'research/clockwork/objects/C36.33a.cells')}
for oid, (k, src) in want.items():
    cells = [tuple(c) for c in CAT[src]['cells']] if k == 'cat' else read_cells(os.path.join(REPO, src))
    assert all(valid(c) for c in cells)
    P = CAT[oid]['period'] if oid in CAT else int(oid[1:].split('.')[0])
    orb = oracle_orbit(cells, 2 * P)
    p_found = exact_period(orb)
    ok = p_found == P and orb[2 * P] == orb[0]
    L, m, kinds = twist(orb, P)
    c0, t = centre(cells)
    r = dict(period=P, verified=ok, period_found=p_found, pop0=len(cells), pops_minmax=[min(map(len, orb[:P])), max(map(len, orb[:P]))],
             union=len(set().union(*orb[:P])), loop_L=L, twist_m=m, closing_symmetry=kinds,
             per_cell_periods=per_cell_periods(orb, P), translation_applied=t, phase0=[list(c) for c in c0])
    if oid == 'P2.6a':
        r['phase1'] = [list(c) for c in sorted(tuple(c[k] + t[k] for k in range(3)) for c in orb[1])]
    res[oid] = r
    print(oid, ok, p_found, L, m, kinds, r['per_cell_periods'])

# P66.27a: the README's mirror (x,y,z) -> (6-y, 6-x, z) in catalogue coordinates, phase 33
c = [tuple(x) for x in CAT['P66.27a']['cells']]
orb = oracle_orbit(c, 66)
mir = frozenset((6 - y, 6 - x, z) for x, y, z in orb[0])
res['P66_mirror_check'] = (mir == orb[33])
print('P66 mirror (6-y,6-x,z) of phase0 == phase33:', mir == orb[33])

# all long-period objects on record: clockwork objects (period >= 17) and catalogue period >= 17
rows = []
meta = {}
for fn in glob.glob(os.path.join(REPO, 'research/clockwork/objects/*.jsonl')):
    for l in open(fn):
        x = json.loads(l); meta[x['id']] = x
for fn in sorted(glob.glob(os.path.join(REPO, 'research/clockwork/objects/*.cells'))):
    oid = os.path.basename(fn)[:-6]; P = int(oid[1:].split('.')[0])
    if P < 17:
        continue
    cells = read_cells(fn)
    orb = oracle_orbit(cells, P)
    pf = exact_period(orb)
    L, m, kinds = twist(orb, P)
    pc = per_cell_periods(orb, P)
    mt = meta.get(oid, {})
    rows.append([oid, P, pf == P, L, m, '/'.join(kinds), P in pc, len(set().union(*orb[:P])), mt.get('hull'),
                 mt.get('twist'), mt.get('quotient_length')])
for oid, o in CAT.items():
    if o['period'] >= 17:
        cells = [tuple(c) for c in o['cells']]; P = o['period']
        orb = oracle_orbit(cells, P)
        pf = exact_period(orb); L, m, kinds = twist(orb, P); pc = per_cell_periods(orb, P)
        rows.append([oid, P, pf == P, L, m, '/'.join(kinds), P in pc, o['union'], None, None, None])
for r in rows:
    print(r)
res['long_rows'] = rows

# legacy ash: neighbour components identified against catalogue still lifes / p2
canon_cat = {}
for oid, o in CAT.items():
    if o['period'] <= 2:
        cs = [tuple(c) for c in o['cells']]
        canon_cat[canon(cs)] = oid
        if o['period'] == 2:
            canon_cat[canon(list(oracle_orbit(cs, 1)[1]))] = oid
def components(cells):
    S = set(cells); seen = set(); comps = []
    for c in cells:
        if c in seen:
            continue
        st = [c]; seen.add(c); comp = []
        while st:
            x = st.pop(); comp.append(x)
            for y in nbrs(x):
                if y in S and y not in seen:
                    seen.add(y); st.append(y)
        comps.append(comp)
    return comps
ash = {}
for n in [8, 9, 10, 11, 12, 13, 14, 16]:
    fn = os.path.join(HERE, 'ash', 'cube%d.cells' % n) if n != 16 else os.path.join(HERE, 'cube16_final.cells')
    cells = read_cells(fn)
    comps = components(cells)
    ids = collections.Counter(canon_cat.get(canon(cp), 'uncatalogued-%d' % len(cp)) for cp in comps)
    ash[n] = dict(pop=len(cells), components=dict(ids))
    print('side', n, len(cells), dict(ids))
res['legacy_ash'] = ash
json.dump(res, open(os.path.join(HERE, 'fauna_out.json'), 'w'))
