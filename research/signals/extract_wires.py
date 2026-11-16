#!/usr/bin/env python3
"""Write the 21 wires and 2 sheets of the notebook entry of 2026-11-15 (research/clockwork/zombies.py's identification
of research/audit/shape3/zombie_states.txt) as small files this directory can use without the clockwork code.

    python3 extract_wires.py          # ~2 min; writes wires/Wnn.json (nn = state number in zombie_states.txt)

Each file: period, the wire's period vector v (cube units), one repeat of phase 0 as doubled coordinates (the wire is
these cells plus every multiple of 2v), and the layers s = x+y+z it occupies.  Sheets: the cells on their own torus
and the torus periods.  Every file is then re-checked here with this directory's own stepper (sg.Geom): the wire, laid
6 repeats long on a ring with 30 empty cubes beside it, must return to itself after `period` generations and not before.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'clockwork'))
import zombies as Z, geom  # noqa: E402
import sg  # noqa: E402

def connected_lift(reps, Lc):
    """reps: cells (here the union of all phases) that are canonical representatives modulo the strip lattice Lc
    (periods v and 48 u2).  Returns {rep: preimage}, the preimages chosen by breadth-first search over 'within two
    neighbour steps', so that the set, repeated along v alone, is the wire (and not the wire cut along the far period)."""
    left = set(reps); start = min(left); left.discard(start); out = {start: start}; dq = [start]
    while dq:
        p = dq.pop()
        for q in sg.nbrs(p):
            for r in [q] + sg.nbrs(q):
                c = geom.canon(r, Lc)
                if c in left:
                    left.discard(c); out[c] = r; dq.append(r)
    assert not left, 'wire part is not connected within two neighbour steps'
    return out


lines = [l for l in open(Z.ZF) if not l.startswith('#')]
rows = json.load(open(os.path.join(Z.SCR, 'zombies.json')))['rows']
for n, line in enumerate(lines):
    row = rows[n]
    kinds = [p['kind'] for p in row['parts']]
    if 'wire' not in kinds and 'sheet' not in kinds:
        continue
    w = line.split(); src = w[0]; live = list(map(int, w[5:]))
    L = tuple(map(int, src.split('_')[1:4])); cells, nb, _ = Z.G(L)
    ph = Z.slab_orbit(live, nb); k0 = ph.index(frozenset(live)); ph = ph[k0:] + ph[:k0]
    comps = Z.parts_of(frozenset().union(*ph), nb)
    assert len(comps) == len(row['parts'])
    for comp, part in zip(comps, row['parts']):
        q = [x & comp for x in ph]; P = Z.own_period(q); q = q[:P]
        assert P == part['period']
        if part['kind'] == 'wire':
            v = part['v']; Lc = (v[0], v[1] % 48, 48)
            cyc = Z.torus_test(q, L, Lc); assert cyc
            c2 = Z.G(Lc, Z.M2)[0]
            pos = connected_lift([c2[j] for j in frozenset().union(*cyc)], Lc)
            unit = sorted((p[0], p[1], p[2] - Z.SH) for p in (pos[c2[j]] for j in cyc[0]))
            rec = dict(id='W%02d' % n, kind='wire', state=n, source=src, period=P, v=v, cells=unit,
                       pops=[len(x) for x in cyc], s_range=[min(map(sum, unit)), max(map(sum, unit))])
        elif part['kind'] == 'sheet':
            a, k, b = L
            unit = sorted(cells[i] for i in q[0])
            rec = dict(id='W%02d' % n, kind='sheet', state=n, source=src, period=P,
                       periods=[[a, k, -a - k], [0, b, -b]], cells=unit, pops=[len(x) for x in q])
        else:
            continue
        # check with this directory's stepper
        if rec['kind'] == 'wire':
            v = rec['v']; N = 6
            other = [0, 30, -30] if v[0] != 0 else [30, 0, -30]
            g = sg.Geom([[N * t for t in v], other], [((1, 1, 1), -15, 31)], unitvec=v, seeds=unit)
            st = g.state(sg.lift_periodic(unit, [v], [range(N)]))
        else:
            g = sg.Geom(rec['periods'], [((1, 1, 1), 1, 15)], seeds=unit)
            st = g.state(unit)
        orb = g.orbit(st, P)
        good = (orb[P] == orb[0]).all() and all((orb[t] != orb[0]).any() for t in range(1, P))
        rec['checked'] = 'period %d on sg.Geom: %s' % (P, 'ok' if good else 'FAIL')
        json.dump(rec, open(os.path.join(HERE, 'wires', rec['id'] + '.json'), 'w'))
        print(rec['id'], rec['kind'], 'P', P, 'v', rec.get('v'), 'cells', len(unit), 'pops', min(rec['pops']), max(rec['pops']), rec['checked'], flush=True)
