"""Follow-up of scan5.py: the rows in which an event that rides the bare train cleanly (or vanishes on it) produced a
difference that reached the refilled boundary 66 units upstream of the end.  Is that the end burning back up the
stream (a fuse), or an echo (the end restored and something sent away up the stream)?

    python3 echo5.py [SCAN.json ...] [--U0 -400] [--G 500] [--which heal]   (st5.Tube; --U0 -250 --G 300 --which heal: 5 min)

Each row is re-run with the boundary moved to U0 (exact while units U0, U0 + 1 hold the plain train; checked) for G
generations and classed at the end:
  healed          whole state equal to the undisturbed run at some generation;
  burn            the train 20..40 units in front of the end is not the plain train (the stream is broken there);
  echo            the end's units >= KS - 8 equal the undisturbed run's, the train 20..40 units in front of the end
                  is plain, and a difference remains further up the stream;
  end changed     the end's units differ from the undisturbed run's while the train 20..40 units in front is plain
                  (a listener candidate: saved for the oracle).
"""
import argparse, json, os
from collections import Counter, defaultdict
import numpy as np
from st5 import Tube, train, unit, ROOT

ap = argparse.ArgumentParser(); ap.add_argument('scans', nargs='*'); ap.add_argument('--U0', type=int, default=-400)
ap.add_argument('--G', type=int, default=500)
ap.add_argument('--which', default='all', help='all, or heal: only ends that heal every census word')
a = ap.parse_args()
OUT = os.path.join(ROOT, 'research', 'scratch', 'audit', 'signals5')
scans = a.scans or [os.path.join(OUT, 'scan5.json')]
ends = json.load(open(os.path.join(OUT, 'ends.json')))['ends']
rows = defaultdict(list)
for fn in scans:
    d = json.load(open(fn))
    heal = {pe['end'] for pe in d['per_end'] if pe['outcomes'].get('word rides|healed', 0) == 8}
    for r in d['upstream_from_riding']:
        if a.which == 'all' or r['end'] in heal:
            rows[r['end']].append(r)
print(sum(len(v) for v in rows.values()), 'rows on', len(rows), 'ends')
KS = 6
TB = Tube(a.U0, 39)
idx = {c: i for i, c in enumerate(TB.cells)}
near = np.nonzero(TB.units >= KS - 8)[0]
front = np.nonzero((TB.units >= KS - 40) & (TB.units < KS - 20))[0]
res = Counter(); cand = []; byclass = Counter()
for e, rs in rows.items():
    cap = frozenset(tuple(c) for c in ends[e]['cap'])
    x0 = TB.vec(train(0, a.U0 - 1, KS) | cap)
    S = np.repeat(x0[None, :], len(rs) + 1, axis=0)
    out = [None] * len(rs)
    for t in range(a.G + 1):
        for j, r in enumerate(rs):
            if r['g'] == t:
                for c in r['rem']: S[j + 1, idx[tuple(c)]] = 0
                for c in r['add']: S[j + 1, idx[tuple(c)]] = 1
        if t > 3:
            for j in np.nonzero((S[1:] == S[0]).all(axis=1))[0]:
                out[j] = out[j] or 'healed'
        bp = TB.boundary_plain(S, t); assert bp[0]
        for j in np.nonzero(~bp[1:])[0]:
            out[j] = out[j] or 'reached U0'
        if t < a.G:
            S = TB.step(S, t)
    tv = TB.train_vec(a.G)
    for j, r in enumerate(rs):
        if out[j] is None:
            fr = bool((S[j + 1, front] == tv[front]).all())
            ne = bool((S[j + 1, near] == S[0, near]).all())
            out[j] = 'burn' if not fr else ('echo' if ne else 'end changed')
            if out[j] == 'end changed':
                cand.append(dict(end=e, **r))
        res[out[j]] += 1; byclass[(r['event'].split(' ')[0], out[j])] += 1
print(dict(res))
print(dict(byclass))
json.dump(dict(result=dict(res), candidates=cand), open(os.path.join(OUT, 'echo5.json'), 'w'))
print(len(cand), 'candidates saved to', os.path.join(OUT, 'echo5.json'))
