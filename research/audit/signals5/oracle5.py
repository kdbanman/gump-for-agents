"""The finding of B(iv) on the oracle alone: ends of the rake train that tell two kinds of one-unit gap apart (one
heals, the other kills), in both directions.

    python3 oracle5.py         (about 3 min)   writes ../../scratch/audit/signals5/oracle5_cases.json and
                                               research/audit/signals5/two_kinds.json (the initial cells)

For each chosen end and each event (the hole of the census word [0]; the riding events of kinds K-hole and K-other
from kinds5.py), two runs on reference/oracle.py on an even box torus (st5.oracle_run): the end at the end of a
finite train of units -100..5, with and without the event.  'healed': the two WHOLE torus states are equal at some
generation <= 140.  'dies': never equal, and at generation 100 they differ on some cell of units <= -20 while the
plain run still holds the plain train on units -40..-20 (the difference has run 26 units up the stream from the end;
the far tail of the finite train has not reached unit -40 by then: it moves half a unit per generation from -100);
printed with the lowest unit of the difference at generation 100.
"""
import json, os
from st5 import oracle_run, train, unit, tr, ROOT, HERE

OUT = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals5')
ends = json.load(open(os.path.join(OUT, 'ends.json')))['ends']
d = json.load(open(os.path.join(OUT, 'scan5.json')))
pe = {p['end']: p['outcomes'] for p in d['per_end']}
rows = d['upstream_from_riding']
up = {}
for r in rows:
    up.setdefault(r['end'], set()).add((r['g'], tuple(map(tuple, r['rem'])), tuple(map(tuple, r['add']))))
hole = (0, (tr((1, 0, 4), 4),), ())    # census word [0]: the rake at unit 4 at generation 0
other = (0, ((-20, 1, 24),), ())       # rm g0: wire cell (0,1,4) of the rake unit -10 at generation 0
other2 = (1, (), ((-20, -1, 22),))     # add g1: cell (0,-1,2) of unit -10 at generation 1
heal_hole = [e for e in pe if pe[e].get('word rides|healed', 0) == 8]
die_hole = [e for e in pe if pe[e].get('word rides|healed', 0) == 0]
A = [e for e in heal_hole if (other[0], other[1], other[2]) in up.get(e, set())][:3]        # heal the hole, die on other
B = [e for e in die_hole if (other[0], other[1], other[2]) not in up.get(e, set())][:3]     # die on the hole, heal other
C_ = [e for e in heal_hole if (other[0], other[1], other[2]) not in up.get(e, set())][:1]   # heal both
cases = []; G = 140


def run(cells_end, ev):
    g, rem, add = ev
    x0 = train(0, -100, 6) | cells_end
    res = None
    gens = []
    p = list(oracle_run(x0, G + g, pad=10))
    s0 = p[g][1]
    assert set(rem) <= s0 and not (set(add) & s0)
    q = list(oracle_run((s0 - set(rem)) | set(add), G, pad=10 + 0))
    # the two runs live on boxes of the same origin only if the bounding boxes agree; compare as cell sets
    for t in range(G + 1):
        if p[g + t][1] == q[t][1]:
            return 'healed', g + t
    D = p[100][1] ^ q[100 - g][1]
    plain_ok = frozenset(c for c in p[100][1] if -40 <= unit(c) < -20) == train(100, -40, -20)
    return ('dies' if plain_ok and any(unit(c) <= -20 for c in D) else 'other'), min(unit(c) for c in D)


out = []
for grp, es in (('heal hole, die on other', A), ('die on hole, heal other', B), ('heal both', C_)):
    for e in es:
        cap = frozenset(tuple(c) for c in ends[e]['cap'])
        r = {}
        for nm, ev in (('hole', hole), ('other (rm (0,1,4) at g0)', other), ('other (add (0,-1,2) at g1)', other2)):
            r[nm] = run(cap, ev)
        print(f'end #{e} ({len(cap)} cells), expected "{grp}":', r, flush=True)
        out.append(dict(end=e, group=grp, cap=sorted(cap), oracle=r))
json.dump(dict(cases=out, events=dict(hole=hole, other=other, other2=other2),
               note='initial state: st5.train(0, -100, 6) | cap at generation 0; an event (g, removed, added) is '
                    'applied to the state at generation g'), open(os.path.join(HERE, 'two_kinds.json'), 'w'))
