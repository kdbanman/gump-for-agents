#!/usr/bin/env python3
"""The census of push 7 re-run on the oracle (helix ring; orc7), for a sample of ends or guns.

    python3 census7a.py FRAME LIST.json OUT.json [--sample K --seed S] [--ids i,j,..] [--part i/n] [--events ...]

FRAME fb (receiving ends) or 5f (guns).  LIST.json: output of enum7.py (own enumeration), deduplicated here with an own
key (`canon`: the orbit over one period, translated so that the first unit that ever differs from the plain train is
unit 0, with the time shift that the translation needs).  Ends are numbered in the order of first appearance.

Events (the push's, rebuilt from its description; cells of the kinds from signals7.json / signals7_5f.json):
  fb: the eight words of holes (cell (1,0,4) removed at generation 0 from the i-th rake counted from the end, words
      [0] [1] [2] [3] [0,1] [0,1,2] [0,2] [0,2,4,6,8]); each down-running kind at unit KS - 24 at generation 1; the lower
      edge of wire B (E at unit KS - 26, H at KS - 40, generation 1).
  5f: each up-running kind (U, N1, E, EE) at unit KS - 24 at generation 1; the upper edge of wire B (E at KS - 40, H at
      KS - 26).
Each run: the end on a FINITE train (units ulo..KS-1) on a ring of L units, disturbed run x and undisturbed run y in
lockstep, both stepped by oracle.step.  The cut tail of the train can influence unit u at generation t only if
u <= ulo + t + 2 (speed limit), so every comparison below is made on units that are exact for the semi-infinite train:
  healed    x == y on the whole ring at some generation (then for ever);
  dead      the difference has reached units KS-100..KS-81 and units >= KS-30 are not equal to the undisturbed run
            (the push's criterion);
  sent      it has reached there and units >= KS-30 ARE equal (the end restored, something sent up: a candidate);
  alive     neither by generation gmax (a candidate).
For 'dead' rows the run is continued for `--after` generations and the units >= KS-30 are described: empty, or of
period dividing 8 (then: is there a uniform wire of period 2 on units KS-30..KS-17 in front?), or neither.
  wire-B edge: as the push: at generations 200..216, units >= KS-30 of period dividing 8?  units KS-30..KS-17
            non-empty and of period 2?  equal to wire B (template from an E-H meeting on a ring)?  -> cap / wall /
            periodic-no-wire / dead.
"""
import sys, os, json, argparse, random, time
from collections import Counter
import numpy as np
import orc7 as O

KS = 6
WORDS = [[0], [1], [2], [3], [0, 1], [0, 1, 2], [0, 2], [0, 2, 4, 6, 8]]
NAMES = {'fb': ['K0', 'H', 'N4', 'D3', 'D4=K0K0', 'D5=HH', 'D6', 'D7', 'N1', 'U', 'E', 'EE'],
         '5f': ['K0', 'H', 'D2', 'D3', 'N4', 'D5', 'U', 'N1', 'E', 'EE']}
SIGFILE = {'fb': 'signals7.json', '5f': 'signals7_5f.json'}


def kinds(frame):
    k = json.load(open(os.path.join(O.PUSH, SIGFILE[frame])))['kinds']
    assert len(k) == len(NAMES[frame])
    return {n: dict(dir=x['dir'], cells=[tuple(c) for c in x['cells']]) for n, x in zip(NAMES[frame], k)}


_P = {}


def patterns(frame):
    if frame not in _P:
        import enum7
        _P[frame] = enum7.train_patterns(frame)
    return _P[frame]


def train_arr(frame, t, ua, ub):
    P = patterns(frame)
    a = np.zeros((ub - ua, O.NC), np.uint8)
    for u in range(ua, ub):
        for c in P[t % 4][u % 2]:
            a[u - ua, O.INDEX[c]] = 1
    return a


_CT = None


def canon(frame, cap):
    """Own dedup key (see the docstring).  Oracle: 4 steps of the end on a finite train."""
    global _CT
    if _CT is None:
        _CT = O.Tor.helix(96, -70)
    T = _CT; ua = -70
    h = T.arr(O.train0(frame, -50, KS) | frozenset(tuple(c) for c in cap))
    S = []
    for t in range(4):
        S.append(T.units(h)[ua * -1 - 30:])                 # units -30.. : exact for 4 generations (tail at -50)
        h = T.step(h)
    lo = -30; n = S[0].shape[0]
    diff = [(S[t] != train_arr(frame, t, lo, lo + n)) for t in range(4)]
    # the train beyond the end is absent: units where the state differs from the train, lowest over the period
    u0 = min(int(np.nonzero(d.any(1))[0][0]) for d in diff) + lo
    key = []
    for t in range(4):
        st = S[(t + 2 * u0) % 4]
        key.append(frozenset(O.tr(O.BASE[i], int(k) + lo - u0) for k, i in zip(*np.nonzero(st)) if k + lo >= u0))
    return tuple(key)


def dedup(frame, caps):
    seen = {}; out = []
    for cap in caps:
        k = canon(frame, cap)
        if k not in seen:
            seen[k] = len(out); out.append([tuple(c) for c in cap])
    return out


def wireB_template(frame):
    """WB[t % 4] = the cells of one unit of the wire B that the meeting of E and H leaves (uniform: checked)."""
    K = kinds(frame)
    T = O.Tor.helix(240, 0)
    h = T.arr(O.train0(frame, 0, 240)); h = T.step(h)
    uE, uH = (120, 106) if frame == 'fb' else (106, 120)
    T.flip(h, [O.tr(c, uE) for c in K['E']['cells']] + [O.tr(c, uH) for c in K['H']['cells']])
    h = T.step(h, 79)
    WB = {}
    for t in range(80, 84):
        U = T.units(h)
        assert all(np.array_equal(U[u], U[113]) for u in range(100, 126)), 'wire B not uniform'
        WB[t % 4] = U[113].copy()
        h = T.step(h)
    return WB


class Census:
    def __init__(self, frame, L=448, gmax=330, after=0):
        self.frame = frame; self.K = kinds(frame)
        self.set_ring(L)
        self.gmax = gmax; self.after = after
        self.WB = wireB_template(frame)
        tr0 = O.train0('fb', KS - 40, KS)
        self.rakes = sorted((u for u in range(KS - 40, KS) if O.tr((1, 0, 4), u) in tr0), reverse=True)
        self.inn = 'down' if frame == 'fb' else 'up'

    def set_ring(self, L):
        self.L = L; self.ulo = KS + 24 - L + 10            # ring units ulo-10 .. KS+23 ; train on ulo .. KS-1
        self.T = O.Tor.helix(L, self.ulo - 10)
        self.ua = self.ulo - 10

    def events(self):
        ev = [('word', tuple(w)) for w in WORDS] if self.frame == 'fb' else []
        ev += [('sig', n) for n in NAMES[self.frame] if self.K[n]['dir'] == self.inn]
        ev.append(('wireB', None))
        return ev

    def flips(self, ev):
        typ, arg = ev
        if typ == 'word':
            return 0, [O.tr((1, 0, 4), self.rakes[i]) for i in arg]
        if typ == 'sig':
            return 1, [O.tr(c, KS - 24) for c in self.K[arg]['cells']]
        uE, uH = (KS - 26, KS - 40) if self.frame == 'fb' else (KS - 40, KS - 26)
        return 1, [O.tr(c, uE) for c in self.K['E']['cells']] + [O.tr(c, uH) for c in self.K['H']['cells']]

    def exact_from(self, t):
        """Lowest unit that is exact for the semi-infinite train at generation t."""
        return self.ulo + t + 3

    def undisturbed(self, cap, G):
        T = self.T
        h = T.arr(O.train0(self.frame, self.ulo, KS) | frozenset(cap))
        ys = [h]
        for t in range(G):
            h = T.step(h); ys.append(h)
        assert T.outside(h) == 0
        return ys

    def classify(self, cap, ev, ys):
        T = self.T; t0, fl = self.flips(ev)
        x = ys[t0].copy(); T.flip(x, fl)
        far_a, far_b = KS - 100 - self.ua, KS - 80 - self.ua
        near = KS - 30 - self.ua
        for t in range(t0, self.gmax + 1):
            y = ys[t]
            if t > t0 and np.array_equal(x, y):
                return dict(out='healed', t=t)
            if self.exact_from(t) > KS - 100:
                return dict(out='horizon', t=t)
            ux, uy = T.units(x), T.units(y)
            if t > t0 and not np.array_equal(ux[far_a:far_b], uy[far_a:far_b]):
                assert T.outside(x) == 0
                if np.array_equal(ux[near:], uy[near:]):
                    return dict(out='sent', t=t)
                r = dict(out='dead', t=t)
                if self.after:
                    r['then'] = self.describe(x, t)
                return r
            x = T.step(x)
        return dict(out='alive', t=self.gmax)

    def describe(self, x, t):
        """State of units >= KS-30 `after` generations on (if still exact there)."""
        T = self.T; near = KS - 30 - self.ua
        G = t + self.after
        if self.exact_from(G + 16) > KS - 30:
            return 'not followed (horizon)'
        x = T.step(x, self.after)
        seq = []
        for j in range(17):
            seq.append(T.units(x)[near:]); x = T.step(x)
        if not any(s.any() for s in seq):
            return 'empty'
        per = all(np.array_equal(seq[j], seq[j + 8]) for j in range(9))
        endalive = any(s[30:].any() for s in seq)
        wire = seq[0][:14].any() and all(np.array_equal(seq[j][:14], seq[j + 2][:14]) for j in range(15))
        uni = wire and all(np.array_equal(seq[0][k], seq[0][0]) for k in range(14))
        return ('periodic' if per else 'not periodic') + (', cells on units >= KS' if endalive else ', nothing on units >= KS') + \
               (', uniform wire in front' if uni else (', period-2 wire in front' if wire else ''))

    def wireB(self, cap):
        T = self.T; t0, fl = self.flips(('wireB', None))
        assert self.exact_from(216) <= KS - 30
        x = T.arr(O.train0(self.frame, self.ulo, KS) | frozenset(cap))
        x = T.step(x, t0); T.flip(x, fl)
        x = T.step(x, 200 - t0)
        near = KS - 30 - self.ua; seq = []
        for j in range(17):
            seq.append(T.units(x)[near:]); x = T.step(x)
        assert T.outside(x) == 0
        per = all(np.array_equal(seq[j], seq[j + 8]) for j in range(9))
        wire = bool(seq[0][:14].any()) and all(np.array_equal(seq[j][:14], seq[j + 2][:14]) for j in range(15))
        isB = all(np.array_equal(seq[j][k], self.WB[(200 + j) % 4]) for j in range(17) for k in range(14))
        out = 'wireB:cap' if per and wire and isB else ('wireB:wall' if per and wire else ('wireB:periodic-no-wire' if per else 'wireB:dead'))
        return dict(out=out, t=217)

    def row(self, cap):
        cap = [tuple(c) for c in cap]
        ys = self.undisturbed(cap, self.gmax)
        # the end is an orbit of period dividing 4 on the exact units (units >= KS - 12 over 24 generations)
        a = KS - 12 - self.ua
        orbit = all(np.array_equal(self.T.units(ys[t])[a:], self.T.units(ys[t + 4])[a:]) for t in range(0, 24))
        outs = []
        for ev in self.events():
            r = self.wireB(cap) if ev[0] == 'wireB' else self.classify(cap, ev, ys)
            r['ev'] = [ev[0], list(ev[1]) if isinstance(ev[1], tuple) else ev[1]]
            outs.append(r)
        return dict(orbit=orbit, outcomes=outs)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('frame'); ap.add_argument('list'); ap.add_argument('out')
    ap.add_argument('--sample', type=int); ap.add_argument('--seed', type=int, default=7); ap.add_argument('--ids')
    ap.add_argument('--part', default='0/1'); ap.add_argument('--after', type=int, default=0); ap.add_argument('--L', type=int, default=448)
    ap.add_argument('--gmax', type=int, default=330)
    a = ap.parse_args()
    d = json.load(open(a.list)); assert d['complete'], 'list not complete'
    ends = dedup(a.frame, d['list'])
    print(f'{len(d["list"])} list entries, {len(ends)} distinct ends', flush=True)
    ids = list(range(len(ends)))
    if a.ids:
        ids = [int(x) for x in a.ids.split(',')]
    elif a.sample:
        ids = sorted(random.Random(a.seed).sample(ids, min(a.sample, len(ids))))
    pi, pn = map(int, a.part.split('/'))
    ids = ids[pi::pn]
    C = Census(a.frame, a.L, a.gmax, a.after)
    rows = {}
    if os.path.exists(a.out):
        rows = {r['i']: r for r in json.load(open(a.out))['rows']}
    t0 = time.time(); res = Counter()
    for n, i in enumerate(ids):
        if i not in rows:
            r = C.row(ends[i]); r['i'] = i; r['cells'] = len(ends[i]); r['cap'] = [list(c) for c in ends[i]]
            rows[i] = r
            if n % 10 == 9:
                json.dump(dict(frame=a.frame, list=a.list, nends=len(ends), rows=[rows[k] for k in sorted(rows)]), open(a.out, 'w'))
                print(f'  {n + 1}/{len(ids)} ends, {time.time() - t0:.0f} s', flush=True)
    json.dump(dict(frame=a.frame, list=a.list, nends=len(ends), rows=[rows[k] for k in sorted(rows)]), open(a.out, 'w'))
    rs = [rows[i] for i in ids]
    print(f'{len(rs)} ends on the oracle; every one an orbit of period dividing 4: {all(r["orbit"] for r in rs)}')
    evs = [tuple(map(str, o['ev'])) for o in rs[0]['outcomes']]
    for k, ev in enumerate(evs):
        ct = Counter(r['outcomes'][k]['out'] for r in rs)
        print(f'  {ev[0]:6s} {ev[1]:22s} ' + ', '.join(f'{o} {v}' for o, v in sorted(ct.items())))
    vec = Counter(tuple(o['out'] for o in r['outcomes']) for r in rs)
    print(f'{len(vec)} outcome vectors:')
    for v, n in vec.most_common():
        print(f'  {n:5d} ' + ' '.join(x.replace('healed', 'h').replace('dead', 'd').replace('wireB:', 'B:') for x in v))


if __name__ == '__main__':
    main()
