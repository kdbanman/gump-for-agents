#!/usr/bin/env python3
"""Compare the audit enumerator's output (research/scratch/audit_ss/NAME.out, .champ) with the study's row in
research/statespace/data/vessels.jsonl, statistic by statistic.   compare.py NAME [NAME...]"""
import json, sys
ROOT = '/home/user/gump-for-agents'
import os
S = ROOT + '/research/scratch/audit_ss/'
if not os.path.exists(S + 'slab_3_1_1_3.out'):
    S = ROOT + '/research/audit/statespace/out/'      # the committed copies
rows = {json.loads(l)['name']: json.loads(l) for l in open(ROOT + '/research/statespace/data/vessels.jsonl')}


def parse(name):
    d = {}
    for l in open(S + name + '.out'):
        k, *v = l.split()
        d[k] = v
    o = {}
    o['N'] = int(d['N'][0])
    o['goe'] = int(d['no_pred'][0])
    o['image_t'] = [int(x) for x in d['image']]
    o['cyclic_states'] = int(d['on_cycles'][0])
    o['cycles'] = int(d['cycles'][0])
    o['by_period'] = [[int(a) for a in x.split(':')] for x in d['periods(p:cycles:states)']]
    o['largest_basin'] = int(d['largest_basin'][0]); o['empty_basin'] = int(d['empty_basin'][0])
    t = d['transient']; o['mean_transient'] = float(t[1]); o['median_transient'] = int(t[3]); o['max_transient'] = int(t[5])
    t = d['visited']; o['mean_visited'] = float(t[1]); o['median_visited'] = int(t[3]); o['max_visited'] = int(t[5])
    o['transient_hist'] = [int(x) for x in d['transient_hist']]
    o['n_champions'] = int(d['champions'][0])
    ch = [l.split() for l in open(S + name + '.champ')]
    o['champions'] = sorted(int(a, 16) for a, _ in ch)
    o['champion_periods'] = sorted(set(int(p) for _, p in ch))
    return o


def perm_to_study(name):
    """audit cell index -> study cell index, via doubled coordinates (study's vessels.py used only for its cell order)"""
    sys.path.insert(0, ROOT + '/research/statespace'); sys.path.insert(0, ROOT + '/research/audit/statespace')
    import vessels, geom
    kind, *args = name.split('_')
    mine = geom.V(kind, args); theirs = vessels.make(kind, args)
    return [theirs.canon(geom.doubled(c)) for c in mine.cells]


def compare(name, study):
    o = parse(name); r = rows[study]
    P = perm_to_study(name)
    assert sorted(P) == list(range(len(P)))
    o['champions'] = sorted(sum(1 << P[i] for i in range(len(P)) if (s >> i) & 1) for s in o['champions'])
    out = []
    def chk(k, a, b):
        out.append((k, a == b if not isinstance(a, float) else abs(a - b) < 1e-6, a, b))
    for k in ('N', 'goe', 'cyclic_states', 'cycles', 'largest_basin', 'empty_basin', 'mean_transient',
              'median_transient', 'max_transient', 'mean_visited', 'median_visited', 'max_visited', 'n_champions'):
        chk(k, o[k], r[k])
    chk('image_t', o['image_t'], r['image_t'][:len(o['image_t'])])
    chk('by_period', o['by_period'], [x[:3] for x in r['by_period']])
    chk('transient_hist', o['transient_hist'], r['transient_hist'])
    theirs = sorted(int(x, 16) for x in r['champions'])
    chk(f'champions (first {len(theirs)} listed)', o['champions'][:len(theirs)], theirs)
    chk('champion_cycle_period', o['champion_periods'] if len(o['champion_periods']) > 1 else o['champion_periods'][0],
        r['champion_cycle_period'])
    allok = all(x[1] for x in out)
    print(f'{study}: {"ALL AGREE" if allok else "DISAGREEMENT"} ({len(out)} statistics)')
    for k, ok, a, b in out:
        if not ok or k in ('goe', 'mean_transient', 'max_transient', 'n_champions'):
            sa, sb = str(a)[:80], str(b)[:80]
            print(f'   {k:24s} {"ok " if ok else "BAD"} audit {sa}   study {sb}')
    return allok


if __name__ == '__main__':
    for nm in sys.argv[1:]:
        study = nm.split('=')[1] if '=' in nm else nm
        compare(nm.split('=')[0], study)
