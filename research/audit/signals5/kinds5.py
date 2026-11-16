"""B(iv) of REVIEW-signals-5, continued: the events of scan5.py that ride the bare train, sorted into kinds of signal,
and the ends' response per kind.  st5.step / st5.Tube.

    python3 kinds5.py        (about 1 min)

Kind of a riding event: its difference from the plain train after 60 generations on a long bare train (units
-200..200, the event at units -10, -9 at generation g), moved so that its lowest unit is 0, together with the
parity of the generation (the train's symmetry is one unit with two generations).  Two events of one kind are the
same signal from then on.  Per end, scan5.json gives which events heal and which go upstream; the table counts the
ends by their response to each kind.
"""
import json, os
from collections import Counter, defaultdict
from st5 import step, train, unit, tr, ROOT

OUT = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals5')
d = json.load(open(os.path.join(OUT, 'scan5.json')))
rows = d['upstream_from_riding']
key = lambda r: (r['event'], r['g'], tuple(map(tuple, r['rem'])), tuple(map(tuple, r['add'])))
pe = {p['end']: p['outcomes'] for p in d['per_end']}
by = defaultdict(set)
for r in rows:
    by[r['end']].add(key(r))
alldead = [e for e in pe if pe[e].get('word rides|healed', 0) == 0 and not any(' rides|healed' in k for k in pe[e])]
riding = sorted(set().union(*[by[e] for e in alldead]))
print(len(riding), 'riding events (from the ends that die on all of them)')
G = 60
kinds = {}
for ev in riding:
    nm, g, rem, add = ev
    x = train(g, -200, 200); y = (x - frozenset(rem)) | frozenset(add)
    for t in range(g, G):
        x = step(x); y = step(y)
    D = frozenset(c for c in x ^ y if -150 < unit(c) < 150)
    if not D:
        kinds[ev] = 'vanished'; continue
    m = min(unit(c) for c in D)
    kinds[ev] = (tuple(sorted(tr(c, -m) for c in D)), G % 2, len(D))
names = {}
for ev in riding:
    k = kinds[ev]
    if k not in names:
        names[k] = 'K%d' % len(names)
print('kinds:')
for k, n in names.items():
    evs = [ev for ev in riding if kinds[ev] == k]
    print(f'  {n}: {len(evs)} events, {k[2] if k != "vanished" else 0} cells of difference at generation {G}; e.g. '
          + '; '.join(f'{e[0]} rem {list(e[2])} add {list(e[3])}' for e in evs[:3]))
resp = Counter()
for e in pe:
    r = []
    for k, n in names.items():
        evs = [ev for ev in riding if kinds[ev] == k]
        up = sum(ev in by[e] for ev in evs)
        r.append(f'{n}:' + ('heal' if up == 0 else ('dies' if up == len(evs) else f'mixed {up}/{len(evs)}')))
    resp[tuple(r)] += 1
print('ends by response to each kind:')
for r, n in resp.most_common():
    print(f'  {n:4d}  {"  ".join(r)}')
json.dump(dict(kinds={n: [list(map(list, ev[2])) + [ev[1]] for ev in riding if kinds[ev] == k] for k, n in names.items()},
               ends={str(e): [ev[0] for ev in by[e]] for e in pe}), open(os.path.join(OUT, 'kinds5.json'), 'w'))
