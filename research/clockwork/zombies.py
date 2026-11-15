#!/usr/bin/env python3
"""Identify the settled states of research/audit/shape3/zombie_states.txt (periods not dividing 840, found by the
lifetime runs on 8-layer twisted-torus slabs).

For each state: step it on its own slab (geom.py, dead walls) for one period; split the spacetime union into
'share a neighbour' components (exactly non-interacting parts); unwrap each part from the torus into free space by
BFS over the doubled offsets (a part whose unwrapping closes with a non-zero lattice vector wraps the torus); step the
lifted phase in free space (lattice.step) and require that its orbit equals the lifted slab orbit for two periods.
Each localized part is then put in canonical form (atlas canonical_orbit) and matched against the atlas catalogue,
objects/*.cells and the box-census object lists in research/scratch/clockwork/census_{3,4}_objects.json.

    python3 zombies.py            # writes research/scratch/clockwork/zombies.json, prints per-state and per-object tables
"""
import glob, json, os, sys
from collections import defaultdict, deque
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'audit', 'shape3'))
import geom  # noqa: E402
from cw import (catalogue, orbit, components, canonical_orbit, sym_order, spacetime_sym, hull_cells, hull_ranges,
                thickness, read_cells, fmt_key, step, find_map, SCR)  # noqa: E402

ZF = os.path.join(HERE, '..', 'audit', 'shape3', 'zombie_states.txt')
OFF = [geom.offsets(a) for a in range(3)]


def ax(p):
    return [t for t in range(3) if p[t] & 1][0]


def slab_step(live, nb):
    cnt = defaultdict(int)
    for i in live:
        for j in nb[i]:
            if j >= 0:
                cnt[j] += 1
    return frozenset(j for j, k in cnt.items() if k in (4, 5) or (k == 3 and j in live))


def slab_orbit(live, nb, maxp=5000):
    seen = {}; ph = []; cur = frozenset(live)
    while cur not in seen:
        seen[cur] = len(ph); ph.append(cur); cur = slab_step(cur, nb)
    return ph[seen[cur]:]


def unwrap(comp, cells, L):
    """BFS-lift a set of torus cell indices to free doubled coordinates, linking cells that share a neighbour
    (two offset steps).  Returns (lift dict, wrapped flag)."""
    idx = {c: i for i, c in enumerate(cells)}
    comp = set(comp); start = min(comp)
    lift = {start: cells[start]}; dq = deque([start]); wrapped = False
    while dq:
        i = dq.popleft(); p = lift[i]
        for o in OFF[ax(p)]:
            q = (p[0] + o[0], p[1] + o[1], p[2] + o[2])
            for o2 in [(0, 0, 0)] + OFF[ax(q)]:
                r = (q[0] + o2[0], q[1] + o2[1], q[2] + o2[2])
                if not (1 <= sum(r) <= 2 * geom.M - 1):
                    continue
                j = idx[geom.canon(r, L)]
                if j not in comp:
                    continue
                if j in lift:
                    if lift[j] != r:
                        wrapped = True
                else:
                    lift[j] = r; dq.append(j)
    return lift, wrapped


def known_keys():
    k = {fmt_key(tuple(map(tuple, o['cells']))): oid for oid, o in catalogue().items()}
    for fn in glob.glob(os.path.join(HERE, 'objects', '*.cells')):
        n = os.path.basename(fn)[:-6]; P = int(n[1:].split('.')[0])
        k.setdefault(fmt_key(canonical_orbit(orbit(read_cells(fn), P - 1))[0]), n)
    census = {}
    for t in (3, 4):
        fn = os.path.join(SCR, f'census_{t}_objects.json')
        if os.path.exists(fn):
            for key, d in json.load(open(fn)).items():
                census.setdefault(key, d.get('id') or f'census{t}')
    return k, census


def describe(ph):
    P = len(ph); co = canonical_orbit(ph); c0 = frozenset(co[0]); ph2 = orbit(c0, P - 1)
    U = frozenset().union(*ph2); so = sym_order(c0); st = spacetime_sym(ph2); m = st // so
    gsym = None
    if m > 1:   # the twisting element: first k with g(phase 0) = phase k
        k = next(k for k in range(1, P) if find_map(ph2[0], ph2[k]))
        gsym = (k, [g for g, _ in find_map(ph2[0], ph2[k])])
    return dict(key=fmt_key(co[0]), period=P, minpop=min(map(len, ph2)), maxpop=max(map(len, ph2)), union=len(U),
                hull=len(hull_cells(hull_ranges(U))), layers=list(thickness(U)), sym=so, union_sym=sym_order(U),
                spacetime_sym=st, twist=m, quotient_length=P // m, twist_map=gsym, cells=[list(c) for c in sorted(c0)])


def main():
    known, census = known_keys()
    geoms = {}
    rows = []; objs = {}
    for n, line in enumerate(l for l in open(ZF) if not l.startswith('#')):
        w = line.split(); src = w[0]; P0 = int(w[2]); live = list(map(int, w[5:]))
        L = tuple(map(int, src.split('_')[1:4]))
        if L not in geoms:
            geoms[L] = geom.build(L)
        cells, nb, f0, f1, _ = geoms[L]
        ph = slab_orbit(live, nb)
        assert frozenset(live) in ph
        k0 = ph.index(frozenset(live)); ph = ph[k0:] + ph[:k0]
        assert len(ph) == P0, (src, len(ph), P0)
        U = frozenset().union(*ph)
        parts = []
        for comp in components_idx(U, nb):
            q = [x & comp for x in ph]; Lq = len(q)
            Pp = next(p for p in range(1, Lq + 1) if Lq % p == 0 and all(q[(t + p) % Lq] == q[t] for t in range(Lq)))
            lift, wrapped = unwrap(comp, cells, L)
            s = [sum(cells[i]) for i in comp]
            walls = (min(s) == 1) + (max(s) == 2 * geom.M - 1)
            rec = dict(slab_period=Pp, union=len(comp), wrapped=wrapped, walls_touched=walls, layers_s=(max(s) - min(s)) // 2 + 1)
            if not wrapped:
                lp = [frozenset(lift[i] for i in x) for x in q[:Pp]]
                fo = orbit(lp[0], 2 * Pp)
                rec['free_same'] = all(fo[t] == lp[t % Pp] for t in range(2 * Pp + 1))
                if not rec['free_same']:
                    rec['free_fate'] = next(((a, b) for a, b in [periodish(lp[0])] ), None)
                if Pp > 1 and rec['free_same']:
                    d = describe(lp)
                    oid = known.get(d['key']) or census.get(d['key'])
                    rec['key'] = d['key']; rec['known_as'] = oid
                    o = objs.setdefault(d['key'], dict(d, known_as=oid, seen=0, sources=[]))
                    o['seen'] += 1; o['sources'].append(n)
                elif Pp == 1 and rec['free_same']:
                    d = canonical_orbit([lp[0]])[0]; rec['key'] = fmt_key(d); rec['known_as'] = known.get(rec['key'])
            parts.append(rec)
        rows.append(dict(n=n, src=src, period=P0, pop=len(live), parts=parts))
        osc = [p for p in parts if p['slab_period'] > 1]
        print('%2d %-16s P%-3d pop %3d parts %d | ' % (n, src, P0, len(live), len(parts)) +
              '  '.join('P%d u%d%s%s%s' % (p['slab_period'], p['union'], ' WRAP' if p['wrapped'] else '',
                                          ' walls%d' % p['walls_touched'] if p['walls_touched'] else '',
                                          '' if p.get('free_same', True) else ' FREE-DIFFERS') +
                        (' =' + str(p.get('known_as')) if p['slab_period'] > 1 else '') for p in osc) +
              '  +%d still' % (len(parts) - len(osc)))
    json.dump(dict(rows=rows, objects=list(objs.values())), open(os.path.join(SCR, 'zombies.json'), 'w'))
    print()
    for o in sorted(objs.values(), key=lambda o: (o['period'], o['minpop'])):
        print('P%-3d pops %d..%d union %d hull %d layers %s sym %d st %d twist %d L %d  seen %d  known %s  map %s' % (
            o['period'], o['minpop'], o['maxpop'], o['union'], o['hull'], o['layers'], o['sym'], o['spacetime_sym'],
            o['twist'], o['quotient_length'], o['seen'], o['known_as'], o['twist_map']))


def periodish(c):
    from cw import period
    return period(c, 3000) or (None, None)


def components_idx(U, nb):
    U = set(U); seen = set(); out = []
    for c in U:
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


if __name__ == '__main__':
    main()
