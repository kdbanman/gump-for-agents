#!/usr/bin/env python3
"""Identify the 37 settled states of research/audit/shape3/zombie_states.txt (periods that do not divide 840, found
by accident in the lifetime runs on 8-layer twisted-torus slabs, geometry research/audit/shape3/geom.py).

    python3 zombies.py        # ~2 min; prints per-state and per-object tables; writes research/scratch/clockwork/zombies.json

Per state:
 1. step it on its own slab (dead walls) for one period; split the spacetime union into 'share a neighbour'
    components (these never interact: exact decomposition); each part's own period.
 2. WALLS: put the whole state in the middle of a 24-layer slab on the same torus (walls 8 layers further away) and
    require the same cycle, cell for cell, for two periods.
 3. FREE: for each phase and each start cell, lift the part from the torus into free space by BFS (one preimage per
    live cell), run it to its cycle with lattice.step; accept a cycle X whose projection to the torus is one-to-one
    and equals the slab orbit, phase for phase, for two periods (an exact certificate that the part is the shadow of
    the free oscillator X).
 4. STRIP: if no free lift works, the same on a torus periodic along one lattice vector v only (lattice (v, (0,48)),
    24-layer slab): a part that passes is a wire, periodic along v.
 5. COVER: if no strip works, the same on covers (k1 v1, k2 v2), k in {1,2,3}: a part that fails every one is a sheet
    that only closes on this torus.
Free objects are put in the atlas canonical form and matched against research/atlas/catalogue.jsonl,
objects/*.cells and research/scratch/clockwork/census_{3,4}_objects.json (the box census lists, if present).
"""
import glob, json, math, os, sys
from collections import defaultdict, deque
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'audit', 'shape3'))
import geom  # noqa: E402
from cw import (catalogue, orbit, canonical_orbit, sym_order, spacetime_sym, hull_cells, hull_ranges,
                thickness, read_cells, fmt_key, step, find_map, SCR)  # noqa: E402

ZF = os.path.join(HERE, '..', 'audit', 'shape3', 'zombie_states.txt')
OFF = [geom.offsets(a) for a in range(3)]
SH = 16          # shift (doubled s) into the 24-layer slab
M2 = 24
_G = {}


def G(L, m=geom.M):
    if (L, m) not in _G:
        cells, nb, *_ = geom.build(L, m)
        _G[L, m] = (cells, nb, {c: i for i, c in enumerate(cells)})
    return _G[L, m]


def ax(p):
    return [t for t in range(3) if p[t] & 1][0]


def slab_step(live, nb):
    cnt = defaultdict(int)
    for i in live:
        for j in nb[i]:
            if j >= 0:
                cnt[j] += 1
    return frozenset(j for j, k in cnt.items() if k in (4, 5) or (k == 3 and j in live))


def slab_orbit(live, nb):
    seen = {}; ph = []; cur = frozenset(live)
    while cur not in seen:
        seen[cur] = len(ph); ph.append(cur); cur = slab_step(cur, nb)
    return ph[seen[cur]:]


def parts_of(U, nb):
    U = set(U); seen = set(); out = []
    for c in sorted(U):
        if c in seen:
            continue
        comp = {c}; st = [c]; seen.add(c)
        while st:
            u = st.pop()
            near = {v for v in nb[u] if v >= 0}
            near |= {w for v in list(near) for w in nb[v] if w >= 0}
            for v in near:
                if v in U and v not in seen:
                    seen.add(v); comp.add(v); st.append(v)
        out.append(frozenset(comp))
    return out


def own_period(q):
    n = len(q)
    return next(p for p in range(1, n + 1) if n % p == 0 and all(q[(t + p) % n] == q[t] for t in range(n)))


def lift(live, L, s0):
    """One preimage per live cell, chosen by BFS from s0 over 'share a neighbour' links (then further seeds)."""
    cells, _, idx = G(L); live = set(live); out = {}
    for seed in [s0] + sorted(live):
        if seed in out:
            continue
        out[seed] = cells[seed]; dq = deque([seed])
        while dq:
            i = dq.popleft(); p = out[i]
            for o in OFF[ax(p)]:
                q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
                for o2 in [(0, 0, 0)] + OFF[ax(q)]:
                    r = (q[0] + o2[0], q[1] + o2[1], q[2] + o2[2])
                    if 1 <= sum(r) <= 2 * geom.M - 1:
                        j = idx[geom.canon(r, L)]
                        if j in live and j not in out:
                            out[j] = r; dq.append(j)
    return [out[i] for i in sorted(live)]


def certify(X, q, L, stepf, proj):
    """X: a state of the test geometry; True iff its orbit projects one-to-one onto the slab orbit q for 2P steps."""
    P = len(q); pr = proj(X)
    if pr is None or pr not in q:
        return False
    k = q.index(pr); cur = X
    for u in range(2 * P + 1):
        pr = proj(cur)
        if pr is None or pr != q[(k + u) % P]:
            return False
        cur = stepf(cur)
    return True


def settle(c, stepf, maxg=3000):
    seen = {}; ph = []; cur = frozenset(c)
    while cur not in seen and len(ph) < maxg:
        seen[cur] = len(ph); ph.append(cur); cur = stepf(cur)
    return ph[seen[cur]:] if cur in seen else None


def try_geometry(q, L, embed, stepf, proj, tries=None):
    """Search lifts of every phase from every start cell; return the certified cycle (list of phases) or None."""
    P = len(q)
    for t in range(P):
        for s0 in sorted(q[t]):
            cyc = settle(embed(lift(q[t], L, s0)), stepf)
            if cyc and len(cyc) == P:
                for X in cyc:
                    if certify(X, q, L, stepf, proj):
                        k = cyc.index(X)
                        return cyc[k:] + cyc[:k]
    return None


def free_test(q, L):
    cells, _, idx = G(L)

    def proj(X):
        if any(not 1 <= sum(p) <= 2 * geom.M - 1 for p in X):
            return None
        s = frozenset(idx[geom.canon(p, L)] for p in X)
        return s if len(s) == len(X) else None
    return try_geometry(q, L, frozenset, step, proj)


def torus_test(q, L, Lc):
    """Test geometry: torus Lc (a sublattice of L), 24-layer slab, state shifted SH up."""
    cells, _, idx = G(L); c2, nb2, i2 = G(Lc, M2)

    def embed(ps):
        return frozenset(i2[geom.canon((p[0], p[1], p[2] + SH), Lc)] for p in ps)

    def proj(X):
        s = frozenset(idx.get(geom.canon((c2[j][0], c2[j][1], c2[j][2] - SH), L), -1) for j in X)
        return s if len(s) == len(X) and -1 not in s else None
    return try_geometry(q, L, embed, lambda X: slab_step(X, nb2), proj)


def walls_test(ph, L):
    cells, _, idx = G(L); c2, nb2, i2 = G(L, M2)
    tgt = [frozenset(i2[geom.canon((cells[i][0], cells[i][1], cells[i][2] + SH), L)] for i in x) for x in ph]
    cur = tgt[0]
    for t in range(2 * len(ph) + 1):
        if cur != tgt[t % len(ph)]:
            return False
        cur = slab_step(cur, nb2)
    return True


def in_lat(x, y, L):
    a, k, b = L
    return x % a == 0 and (y - (x // a) * k) % b == 0


def hnf(v1, v2):
    """(a, k, b) form of the lattice spanned by v1, v2 (cube coordinates in the basis u1, u2)."""
    def eg(a, b):
        if b == 0:
            return (a, 1, 0)
        g, x, y = eg(b, a % b); return (g, y, x - (a // b) * y)
    (x1, y1), (x2, y2) = v1, v2; g, s, t = eg(x1, x2)
    if g < 0:
        g, s, t = -g, -s, -t
    b = abs(x1 * y2 - x2 * y1) // g
    return (g, (s * y1 + t * y2) % b, b)


def short_vectors(L):
    """Primitive lattice vectors (x > 0) with |x| <= 6, |y| <= 8, shortest cube length first."""
    out = []
    for x in range(1, 7):
        for y in range(-8, 9):
            if in_lat(x, y, L) and not any(x % d == 0 and y % d == 0 and in_lat(x // d, y // d, L) for d in range(2, 7)):
                out.append((x * x + y * y + (x + y) ** 2, (x, y)))
    return [v for _, v in sorted(out)]


def basis(L):
    vs = short_vectors(L)
    for i, v in enumerate(vs):
        for w in vs[i + 1:]:
            if abs(v[0] * w[1] - v[1] * w[0]) == L[0] * L[2]:
                return v, w


def describe(ph):
    P = len(ph); co = canonical_orbit(ph); c0 = frozenset(co[0]); ph2 = orbit(c0, P - 1)
    U = frozenset().union(*ph2); so = sym_order(c0); st = spacetime_sym(ph2); m = st // so
    tw = None
    if m > 1:
        k = next(k for k in range(1, P) if find_map(ph2[0], ph2[k]))
        tw = dict(shift=k, maps=[[list(g[0]), list(g[1]), list(t)] for g, t in find_map(ph2[0], ph2[k])])
    pc = []   # per-cell periods
    for c in sorted(U):
        s = [c in x for x in ph2]
        pc.append(own_period(s))
    cnt = defaultdict(int)
    for p in pc:
        cnt[p] += 1
    return dict(key=fmt_key(co[0]), period=P, minpop=min(map(len, ph2)), maxpop=max(map(len, ph2)), union=len(U),
                hull=len(hull_cells(hull_ranges(U))), layers=list(thickness(U)), sym=so, union_sym=sym_order(U),
                spacetime_sym=st, twist=m, quotient_length=P // m, twist_map=tw,
                cell_periods=dict(sorted(cnt.items())), cells=[list(c) for c in sorted(c0)])


def known_keys():
    k = {fmt_key(tuple(map(tuple, o['cells']))): oid for oid, o in catalogue().items()}
    for fn in glob.glob(os.path.join(HERE, 'objects', '*.cells')):
        n = os.path.basename(fn)[:-6]
        if n.startswith('Z'):
            continue
        P = int(n[1:].split('.')[0])
        k.setdefault(fmt_key(canonical_orbit(orbit(read_cells(fn), P - 1))[0]), n)
    census = {}
    for t in (3, 4):
        fn = os.path.join(SCR, f'census_{t}_objects.json')
        if os.path.exists(fn):
            for key, d in json.load(open(fn)).items():
                census.setdefault(key, d.get('id') or f'census{t}-unnamed')
    return k, census


def wire_fingerprint(cyc, Lc):
    """Up-to-symmetry fingerprint of a wire on the strip torus: period, |v|^2, pop sequence up to rotation/reversal."""
    pops = [len(x) for x in cyc]; P = len(pops)
    rots = [tuple(pops[i:] + pops[:i]) for i in range(P)]
    return (P, min(rots + [tuple(reversed(r)) for r in rots]))


def selfsuff(G, ph):
    q = [x & G for x in ph]
    return all(step(q[t]) == q[(t + 1) % len(q)] for t in range(len(q)))


def blocks(ph):
    """Finest split of a free cycle into groups of neighbour-components of its union that evolve on their own
    (exhaustive over subsets: each block and the remainder reproduce their restricted orbits); then strip from each
    block whole still chunks (neighbour-components of its period-1 cells, one or two at a time) while it still
    reproduces its orbit.  Returns a list of restricted cycles (each at its own period)."""
    import itertools
    from cw import components
    U = frozenset().union(*ph); comps = components(U, 1); rem = list(range(len(comps))); out = []
    while rem:
        for r in range(1, len(rem) + 1):
            S = next((S for S in itertools.combinations(rem, r)
                      if selfsuff(frozenset().union(*[comps[i] for i in S]), ph) and
                      (r == len(rem) or selfsuff(frozenset().union(*[comps[i] for i in rem if i not in S]), ph))), None)
            if S:
                break
        G = set().union(*[comps[i] for i in S]); rem = [i for i in rem if i not in S]
        per = {c: own_period([c in x for x in ph]) for c in G}
        changed = True
        while changed:
            changed = False
            sc = sorted(components(frozenset(c for c in G if per[c] == 1), 1), key=len, reverse=True)
            for r in (1, 2):
                for T in itertools.combinations(sc, r):
                    H = frozenset(G) - frozenset().union(*T)
                    if H and selfsuff(H, ph) and selfsuff(frozenset(G) - H, ph):
                        out.append(frozenset(G) - H); G = set(H); changed = True; break
                if changed:
                    break
        out.append(frozenset(G))
    res = []
    for G in out:
        q = [x & G for x in ph]; res.append(q[:own_period(q)])
    return res


def main():
    known, census = known_keys()
    rows = []; objs = {}; wires = defaultdict(list)
    lines = [l for l in open(ZF) if not l.startswith('#')]
    for n, line in enumerate(lines):
        w = line.split(); src = w[0]; P0 = int(w[2]); live = list(map(int, w[5:]))
        L = tuple(map(int, src.split('_')[1:4])); cells, nb, _ = G(L)
        ph = slab_orbit(live, nb); k0 = ph.index(frozenset(live)); ph = ph[k0:] + ph[:k0]
        assert len(ph) == P0, (src, len(ph), P0)
        row = dict(n=n, src=src, torus=L, period=P0, pop=len(live), walls_free=walls_test(ph, L), parts=[])
        for comp in parts_of(frozenset().union(*ph), nb):
            q = [x & comp for x in ph]; P = own_period(q); q = q[:P]
            s = [sum(cells[i]) for i in comp]
            rec = dict(period=P, union=len(comp), pops=[min(map(len, q)), max(map(len, q))],
                       touches_walls=(min(s) == 1) + (max(s) == 2 * geom.M - 1))
            if P == 1:
                c0 = frozenset(lift(q[0], L, min(q[0])))
                if step(c0) == c0:
                    key = fmt_key(canonical_orbit([c0])[0]); rec.update(kind='still', id=known.get(key) or census.get(key), key=key)
                else:
                    rec.update(kind='still-on-torus-only')
                row['parts'].append(rec); continue
            cyc = free_test(q, L)
            if cyc:
                d = describe(cyc); oid = known.get(d['key']) or census.get(d['key'])
                rec.update(kind='free', key=d['key'], id=oid, blocks=[])
                for b in blocks(cyc):
                    if len(b) == 1:
                        k = fmt_key(canonical_orbit(b)[0]); rec['blocks'].append(dict(period=1, union=len(b[0]), id=known.get(k) or census.get(k)))
                        continue
                    d = describe(b); oid = known.get(d['key']) or census.get(d['key'])
                    o = objs.setdefault(d['key'], dict(d, known_as=oid, states=[]))
                    o['states'].append(n); rec['blocks'].append(dict(period=d['period'], union=d['union'], id=oid, key=d['key']))
            else:
                v1, v2 = basis(L); rec['kind'] = 'sheet'
                for v in short_vectors(L)[:8]:
                    Lc = (v[0], v[1] % 48, 48)
                    cyc = torus_test(q, L, Lc)
                    if cyc:
                        cube = (v[0], v[1], -v[0] - v[1])
                        rec.update(kind='wire', v=cube, cells_per_repeat=[min(map(len, cyc)), max(map(len, cyc))])
                        wires[(P, tuple(sorted(map(abs, cube))))].append(n)
                        break
                if rec['kind'] == 'sheet':
                    rec['covers_failed'] = []
                    for k1, k2 in [(1, 2), (2, 1), (2, 2), (1, 3), (3, 1), (3, 3)]:
                        Lc = hnf((k1 * v1[0], k1 * v1[1]), (k2 * v2[0], k2 * v2[1]))
                        if torus_test(q, L, Lc):
                            rec['kind'] = 'cover'; rec['cover'] = Lc; break
                        rec['covers_failed'].append(Lc)
            row['parts'].append(rec)
        rows.append(row)
        print('%2d %-16s P%-3d pop %3d walls-free %s | ' % (n, src, P0, len(live), 'same' if row['walls_free'] else 'DIFF') +
              '  '.join('P%d u%d %s%s' % (p['period'], p['union'], p['kind'],
                                         (' =' + str(p.get('id')) + (' = ' + ' + '.join('P%d u%d %s' % (b['period'], b['union'], b['id']) for b in p['blocks']) if 'blocks' in p else '')) if p['kind'] in ('free', 'still') else
                                         (' v=%s' % (p['v'],) if p['kind'] == 'wire' else '')) for p in row['parts']), flush=True)
    json.dump(dict(rows=rows, objects=list(objs.values()), wires={str(k): v for k, v in wires.items()}),
              open(os.path.join(SCR, 'zombies.json'), 'w'))
    print('\nfree objects')
    for o in sorted(objs.values(), key=lambda o: (o['period'], o['minpop'])):
        print('P%-3d pops %d..%d union %d hull %d layers %s sym %d unionsym %d st %d twist %d L %d cellper %s states %s known %s' % (
            o['period'], o['minpop'], o['maxpop'], o['union'], o['hull'], o['layers'], o['sym'], o['union_sym'],
            o['spacetime_sym'], o['twist'], o['quotient_length'], o['cell_periods'], o['states'], o['known_as']))
    if '--write' in sys.argv:     # new free objects -> objects/<id>.cells + objects/zombie_objects.jsonl
        from cw import write_cells
        names = {os.path.basename(f)[:-6] for f in glob.glob(os.path.join(HERE, 'objects', '*.cells'))}
        with open(os.path.join(HERE, 'objects', 'zombie_objects.jsonl'), 'w') as f:
            for o in sorted(objs.values(), key=lambda o: (o['period'], o['minpop'])):
                if o['known_as']:
                    continue
                k = 0
                while 'C%d.%d%s' % (o['period'], o['minpop'], 'abcdefgh'[k]) in names:
                    k += 1
                name = 'C%d.%d%s' % (o['period'], o['minpop'], 'abcdefgh'[k]); names.add(name)
                rec = dict(id=name, **{x: o[x] for x in ('period', 'minpop', 'maxpop', 'union', 'hull', 'layers', 'sym',
                                                        'spacetime_sym', 'twist', 'quotient_length', 'cell_periods')},
                           source='zombie_states.txt lines (0-based, comments skipped) %s' % o['states'],
                           cells=o['cells'])
                f.write(json.dumps(rec) + '\n')
                write_cells(os.path.join(HERE, 'objects', name + '.cells'), frozenset(map(tuple, o['cells'])),
                            '%s: period %d, union %d, twist %d (quotient length %d), cell periods %s; phase 0, doubled coords;\n'
                            'found by accident in lifetime runs (research/audit/shape3/zombie_states.txt state %s); zombies.py'
                            % (name, o['period'], o['union'], o['twist'], o['quotient_length'], o['cell_periods'], o['states']))
                print('wrote', name)
    print('\nwires (period, |v| class): states')
    for k, v in sorted(wires.items()):
        print(k, v)


if __name__ == '__main__':
    main()
