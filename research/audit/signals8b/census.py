#!/usr/bin/env python3
"""census.py (audit of push 8b, q.c): looking for a write with the reader in place.

    python3 census.py cells  READER [--k 0,1,2,3] [--part i/m]   every one-cell flip near the crossing, both phases
    python3 census.py movers READER                              every mover of wire B sent along the store at a stretch
                                                                 end next to the reader, and along plain wire under it
    python3 census.py both   READER                              a store pulse and a reader probe arriving together
    python3 census.py words  READER                              words of up to 4 reader pulses from either end and from
                                                                 both ends at once: is the store changed?
READER = B13 | B8.

The object: a capped wire B of 28 units (the store; a stretch d^k f with its wall at unit w where given), the reader a
capped wire B of 14 units with its crossing at store unit 0.  An event is a set of cell flips at given generations.
Outcome of an event, 400 generations on (st = the standing object before the event):
  healed        the state is st again
  burn          no period <= 4, or more than 60 cells gained or lost
  changed       a standing state (period <= 4) other than st.  Then: is the reader (everything outside the store's
                tube) as it was; the store in letters before -> after; and what the reading pair does now.
A WRITE would be: changed, reader as it was, and the reading pair answers differently from before (and restores).
Every `changed` outcome is written to out/census_*.jsonl; the summary counts them by kind.
"""
import argparse, json, os, sys, time
from collections import Counter
import qa, rd
from qa import pk, up, run, xor, union, same, tr, unit

SA, SB = -14, 14
READERS = {'B13': (rd.B13, -1), 'B8': (rd.B8, 0)}
RA, RB = -8, 6


def word(w, k):
    s = ['7'] * (SB - SA)
    if k:
        for u in range(w, w + k):
            s[u - SA] = 'd'
        s[w + k - SA] = 'f'
    return ''.join(s)


class Obj:
    def __init__(self, name, w=0, k=0, sa=SA, sb=SB, ra=None, rb=None):
        global SA, SB
        mk, self.ur = READERS[name]
        self.P = mk(0)
        ra = self.ur - 7 if ra is None else ra; rb = self.ur + 8 if rb is None else rb
        self.ra, self.rb = ra, rb
        s = ['7'] * (sb - sa)
        if k:
            for u in range(w, w + k):
                s[u - sa] = 'd'
            s[w + k - sa] = 'f'
        self.S = pk(rd.capped(sa, sb, ''.join(s)))
        self.sa, self.sb = sa, sb
        self.own = rd.capped(ra, rb)
        v, J, R = rd.install(self.S, self.P, self.own, settle=160)
        self.verdict = v
        self.J = J if v in ('union', 'junction') else None
        self.R = R
        if self.J is not None:
            self.read0 = self.read(self.J)

    def letters(self, X):
        return qa.letters(X, self.sa, self.sb)

    def rletters(self, X):
        return qa.letters(pk([self.P.back(c) for c in up(X)]), self.ra, self.rb)

    def reader_part(self, X):
        return X[~qa.tube_mask(X)]

    def read(self, X):
        """the reading pair, launched 5 units before the crossing: 'echo' | 'nothing' | 'other(...)', '+restored' or not."""
        r = rd.lock(X, {0: pk(self.P(rd.pR(self.ur - 5) + rd.pR(self.ur - 6)))}, 200)
        d = r['diffs'].get(20, pk([]))
        desc = rd.describe(self.P, d)
        what = 'echo' if desc.startswith('L@') and ' ' not in desc else 'nothing' if desc == '-' else f'other({desc})'
        return what + ('' if r['first'] is not None and not r['tube'] else ' NOT RESTORED')

    def event(self, flips, T=400):
        """flips: {generation: list of cells}.  Returns (code, X)."""
        J = self.J
        last = max(flips)
        X = J
        t = 0
        for g in sorted(flips):
            X = run(X, g - t); t = g
            X = xor(X, pk(flips[g]))
        t1 = (last // 4 + 1) * 4 + 60
        X = run(X, t1 - t); t = t1
        if same(X, J):
            return 'healed', X
        if abs(len(X) - len(J)) > 60:
            return 'burn', X
        X = run(X, 180); t += 180
        if abs(len(X) - len(J)) > 60:
            return 'burn', X
        if same(X, J):
            return 'healed', X
        if not same(run(X, 4), X):
            X = run(X, T - t)
            if abs(len(X) - len(J)) > 60 or not same(run(X, 4), X):
                return 'burn', X
            if same(X, J):
                return 'healed', X
        return 'changed', X

    def classify(self, X):
        intact = same(self.reader_part(X), self.reader_part(self.J))
        s0, s1 = self.letters(self.J), self.letters(X)
        rec = dict(reader_intact=intact, store0=s0, store1=s1, reader1=self.rletters(X), ncells=int(len(xor(X, self.J))))
        rec['read0'] = self.read0
        rec['read1'] = self.read(X)
        rec['write'] = bool(intact and rec['read1'] != rec['read0'] and 'NOT' not in rec['read1'])
        return rec


def region_cells(P=None, ua=-5, ub=6, wide=1):
    """all lattice cells of the tube widened by `wide` layers on each side (wide = 1: the 5 x 5 tube), units ua..ub-1,
    in the store's frame (P None) or mapped from the reader's own frame."""
    out = []
    for u in range(ua, ub):
        for x in (2 * u, 2 * u + 1):
            for y in range(-8, 9):
                for z in range(-2 * u - 10, -2 * u + 16):
                    c = (x, y, z)
                    if qa.is_cell(c) and 1 - 2 * wide <= x + y + z <= 5 + 2 * wide and 1 - 2 * wide <= x - y + z <= 5 + 2 * wide:
                        out.append(c)
    if P is not None:
        out = P(out)
    return out


def run_events(ob, events, tag, fout, cnt, keep=None):
    for label, flips in events:
        code, X = ob.event(flips)
        cnt[code] += 1
        if code == 'changed':
            rec = ob.classify(X)
            kind = ('WRITE' if rec['write'] else 'reader as it was, same answer' if rec['reader_intact'] and rec['read1'] == rec['read0']
                    else 'reader as it was, read fails' if rec['reader_intact'] else 'reader changed')
            cnt['changed: ' + kind] += 1
            rec.update(tag=tag, event=label, kind=kind)
            fout.write(json.dumps(rec) + '\n'); fout.flush()
            if rec['write'] and keep is not None:
                keep.append(rec)


def seeds(name, ks, wmax=7):
    out = [(0, 0)]
    for k in ks:
        if k == 0:
            continue
        for w in range(-wmax - k, wmax + 1):
            if -wmax <= w <= wmax or -wmax <= w + k <= wmax:
                out.append((w, k))
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd'); ap.add_argument('reader'); ap.add_argument('--k', default='0,1,2,3'); ap.add_argument('--part', default='0/1')
    a = ap.parse_args()
    pi, pm = map(int, a.part.split('/'))
    ks = [int(x) for x in a.k.split(',')]
    t0 = time.time()
    fn = os.path.join(qa.SCR, f'census_{a.cmd}_{a.reader}_{pi}of{pm}.jsonl')
    fout = open(fn, 'w'); total = Counter(); writes = []
    if a.cmd == 'cells':
        sd = [s for i, s in enumerate(seeds(a.reader, ks)) if i % pm == pi]
        for (w, k) in sd:
            ob = Obj(a.reader, w, k)
            if ob.J is None:
                total['seed does not stand'] += 1; continue
            cells = sorted(set(region_cells()) | set(region_cells(ob.P, ob.ur - 5, ob.ur + 6)))
            ev = [(f'flip {c} at generation {g}', {g: [c]}) for c in cells for g in (0, 1)]
            cnt = Counter()
            run_events(ob, ev, f'w={w} k={k}', fout, cnt, writes)
            total.update(cnt); total['seeds'] += 1
            print(f'{a.reader} w={w} k={k} ({ob.letters(ob.J)}; reads {ob.read0}): {len(ev)} events: ' + ', '.join(f'{v} {c}' for c, v in sorted(cnt.items())), flush=True)
    if a.cmd in ('movers', 'both', 'words'):
        sa, sb = -22, 22
        mk, ur = READERS[a.reader]
        ra, rb = ur - 20, ur + 20
        plain = pk(rd.capped(sa, sb)); rplain = pk(rd.capped(ra, rb))

        def place_word(wd, u0, sign=1):
            """flips that turn plain wire B on units u0.. into the word (hex digits)."""
            cells = set()
            for i, ch in enumerate(wd):
                cells ^= set(qa.unit_cells(int(ch, 16), u0 + i)) ^ set(qa.unit_cells(rd.B, u0 + i))
            return sorted(cells)

        RIGHT = ['6f', '6ef', '6eef', '6f6f', '6f76f', '6f776f', 'd6f', 'd6ef', 'cfd6f', 'd6f6f', '6fd6f']
        LEFT = ['b', 'bb', 'bbb', 'b7b', 'b77b', 'b777b', 'b5f', 'bb5f', 'b5f9f', 'b7b5f', 'b5f7b']
        # each mover rides plain wire rigidly (checked here, on the store alone): after 2j generations the difference
        # is the word moved j units
        for wd, sign in [(m, 1) for m in RIGHT] + [(m, -1) for m in LEFT]:
            d0 = pk(place_word(wd, -3 if sign > 0 else 3))
            x = xor(plain, d0)
            ok = all(same(xor(run(x, 2 * j), plain), pk(place_word(wd, (-3 if sign > 0 else 3) + sign * j))) for j in (1, 2, 5))
            if not ok:
                print(f'  (word {wd} does not ride rigidly: dropped)')
                (RIGHT if sign > 0 else LEFT).remove(wd)
        sd = [(0, 0)] + [(w, k) for k in ks if k for w in range(-9 - k, 10)]
        sd = [s_ for i, s_ in enumerate(sd) if i % pm == pi]
        for (w, k) in sd:
            ob = Obj(a.reader, w, k, sa, sb, ra, rb)
            if ob.J is None:
                total['seed does not stand'] += 1; continue
            ev = []
            if a.cmd == 'movers':
                for delay in (0, 2):
                    for wd in RIGHT:
                        if k == 0 or w > -14:
                            ev.append((f'{wd} from the left, launched at unit -18, generation {delay}', {delay: place_word(wd, -18)}))
                    for wd in LEFT:
                        ev.append((f'{wd} from the right, launched at unit {18 - len(wd) + 1}, generation {delay}', {delay: place_word(wd, 18 - len(wd) + 1)}))
                # pulses born inside the stretch (one stator removed, either stator, either phase)
                for u in range(w, w + k + 1):
                    for which in (2, 4):
                        for g in (0, 1):
                            ev.append((f'stator (0,1,{which}) of unit {u} removed at generation {g}', {g: [rd.stator(u, which)]}))
            elif a.cmd == 'both':
                rops = {'R': rd.pR(ur - 10), 'RR': rd.pR(ur - 10) + rd.pR(ur - 11), 'L': rd.pL(ur + 10), 'LL': rd.pL(ur + 10) + rd.pL(ur + 11)}
                sops = {'store R': rd.pR(-10), 'store L': rd.pL(10), 'store RR': rd.pR(-10) + rd.pR(-11), 'store LL': rd.pL(10) + rd.pL(11)}
                for rn, rc in rops.items():
                    for sn, sc in sops.items():
                        for dl in range(0, 25):
                            # the reader probe at generation 12, the store pulse at generation dl (even: as is)
                            if dl % 2:
                                continue
                            ev.append((f'{sn} at generation {dl}, reader {rn} at generation 12', {dl: sc, 12: ob.P(rc)} if dl != 12 else {12: sc + ob.P(rc)}))
                        for dl in range(1, 25, 2):
                            # odd offsets: the store pulse launched one unit nearer or further does not change parity; use
                            # the store pulse one generation old (its odd form on plain wire)
                            x = xor(plain, pk(sc)); odd = up(xor(run(x, 1), run(plain, 1)))
                            ev.append((f'{sn} (odd form) at generation {dl}, reader {rn} at generation 12', {dl: odd, 12: ob.P(rc)}))
            elif a.cmd == 'words':
                import itertools
                for side in 'LR':
                    mkp = (lambda j: rd.pR(ur - 8 - j)) if side == 'L' else (lambda j: rd.pL(ur + 8 + j))
                    for n in range(0, 4):
                        for rest in itertools.combinations(range(1, 8), n):
                            cells = set()
                            for j in (0,) + rest:
                                cells ^= set(mkp(j))
                            ev.append((f'reader pulses from the {"left" if side == "L" else "right"} end at offsets {(0,) + rest}', {0: ob.P(sorted(cells))}))
                for sl in range(0, 4):
                    for sr in range(0, 4):
                        for dl in range(-8, 9):
                            cl = set(rd.pR(ur - 9)) ^ (set(rd.pR(ur - 9 - sl)) if sl else set())
                            cr = set(rd.pL(ur + 9 + dl)) ^ (set(rd.pL(ur + 9 + dl + sr)) if sr else set())
                            ev.append((f'reader: left word (0,{sl}) and right word (0,{sr}), right launch {dl} units further', {0: ob.P(sorted(cl ^ cr))}))
            cnt = Counter()
            run_events(ob, ev, f'w={w} k={k}', fout, cnt, writes)
            total.update(cnt); total['seeds'] += 1
            print(f'{a.reader} w={w} k={k} ({ob.letters(ob.J)}; reads {ob.read0}): {len(ev)} events: ' + ', '.join(f'{v} {c}' for c, v in sorted(cnt.items())), flush=True)
    print(f'TOTAL {a.reader} {a.cmd}: ' + ', '.join(f'{v} {c}' for c, v in sorted(total.items())) + f'  ({time.time() - t0:.0f} s) -> {fn}')
    for r in writes:
        print('WRITE', json.dumps(r))
