#!/usr/bin/env python3
"""Single-cell perturbation census of an oscillator.

  perturb.py OID [--phases K] [--dist D]
For each phase t < K (default: period / glide order) and every cell within neighbour-distance D (default 1)
of the union, flip that cell and run to the final cycle in an exact octahedral vessel.  Prints a summary and
writes research/scratch/clockwork/perturb_OID.json (one record per trial).
"""
import argparse, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cw import obj, orbit, nbrs, run_batch, vessel_for, objects, catalogue, SCR, fmt_key  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('oid'); ap.add_argument('--phases', type=int); ap.add_argument('--dist', type=int, default=1)
    a = ap.parse_args()
    cat = catalogue(); o = cat[a.oid]; P = o['period']
    keyid = {tuple(map(tuple, x['cells'])): x['id'] for x in cat.values()}
    c = obj(a.oid); orb = orbit(c, P)
    U = frozenset().union(*orb[:P])
    near = set(U)
    for _ in range(a.dist):
        near |= {y for x in near for y in nbrs(x)}
    near = sorted(near)
    K = a.phases or (P // 2 if o['spacetime_sym'] >= 2 else P)
    v = vessel_for(near, margin=8)
    trials, inits = [], []
    for t in range(K):
        for x in near:
            inits.append(orb[t] ^ {x}); trials.append((t, x, x in orb[t], x in U))
    res = run_batch(v, inits, maxgen=200000, tag=a.oid)
    recs, summ = [], Counter()
    for (t, x, wason, inU), r in zip(trials, res):
        objs = objects(v, r)
        ids = sorted('%s' % keyid.get(k, 'new:P%d/%d' % (p, len(k))) for p, k in objs)
        if r['period'] == 0:
            fate = 'unsettled'
        elif not objs:
            fate = 'dies'
        elif a.oid in ids and len(ids) == 1:
            fate = 'heals'
        elif a.oid in ids:
            fate = 'survives+debris'
        else:
            fate = 'breaks'
        summ[fate] += 1
        recs.append(dict(t=t, cell=x, was_live=wason, in_union=inU, mu=r['mu'], period=r['period'],
                         pop=r['pop'], fate=fate, objects=ids,
                         new=[fmt_key(k) for p, k in objs if k not in keyid]))
    json.dump(recs, open(os.path.join(SCR, f'perturb_{a.oid}.json'), 'w'))
    print(a.oid, 'trials', len(recs), dict(summ))
    for grp, sel in [('flip a live cell', lambda r: r['was_live']), ('add a cell in the union', lambda r: not r['was_live'] and r['in_union']),
                     ('add a cell outside the union', lambda r: not r['in_union'])]:
        rr = [r for r in recs if sel(r)]
        print(' %-30s n=%4d %s' % (grp, len(rr), dict(Counter(r['fate'] for r in rr))))
    ash = Counter(i for r in recs if r['fate'] in ('breaks', 'survives+debris') for i in r['objects'])
    print(' ash after breaking:', ash.most_common(25))
    print(' periods of final cycles (breaks):', sorted(Counter(r['period'] for r in recs if r['fate'] == 'breaks').items()))
    mus = sorted(r['mu'] for r in recs if r['fate'] != 'heals')
    if mus:
        print(' transients (non-heal): median', mus[len(mus) // 2], 'max', mus[-1])
    hm = sorted(r['mu'] for r in recs if r['fate'] == 'heals')
    if hm:
        print(' heal times: median', hm[len(hm) // 2], 'max', hm[-1])


if __name__ == '__main__':
    main()
