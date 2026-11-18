#!/usr/bin/env python3
"""laws8 (REVIEW-signals-8): the push's lab8-only numbers of section 5 and 6, recomputed with st8 (and samples on the
oracle).

    python3 laws8.py census [--k 3] [--orc 12]   the 760 one-cell events at d^k f; my own classes; --orc: that many
                                                 events of each class re-run on the oracle, whole state at the end
    python3 laws8.py law [--K 40] [--orc 5,17]   the eight release laws for k = 1..K; the listed k on the oracle
    python3 laws8.py catch [--K 12]              a second store catches the count read (k = 1..K); k = 3, 7, 12 on the oracle
    python3 laws8.py smallest                    which N allow set / add / a count read, every placement of every operation
    python3 laws8.py inside [--K 6]              a stator removed inside the stretch ("take one off"): which units give k - 1

Background for census and law: capL + 7^nl d^k f 7^nr + push 7's right cap (as the push); nothing reaches a cap.
Census classes (state at generation 100, flips at generation g0 = 0 or 1), decided on the whole state:
  healed      equal to the untouched run
  count +1/-1 exactly the cell with a stretch one unit longer / shorter and nothing else, period 2 away from the cap
  pulse away  the stretch as it was and a train of letters moving away
  released    no d and no f left between the trains' side and the far side: plain wire, and a train of family
              letters on one side that is the same train one unit further 2 generations later (rigid), '<-' or '->'
  standing    not healed, the same 4 generations later, not a count
  other       anything else
"""
import sys, re, time, json, random
from collections import Counter, defaultdict
import numpy as np
import a8
from a8 import tr, SR, SL

T0 = time.time()
E5 = [(x, y, z) for x in (0, 1) for y in range(-4, 5) for z in range(-6, 9)
      if a8.is_cell((x, y, z)) and -1 <= x + y + z <= 7 and -1 <= x - y + z <= 7]
E3 = [c for c in E5 if 1 <= c[0] + c[1] + c[2] <= 5 and 1 <= c[0] - c[1] + c[2] <= 5]
assert len(E5) == 38 and len(E3) == 14


class Line:
    """one experiment on capL + word + right cap with st8 (sim='box') or the oracle (sim='orc')"""

    def __init__(self, word, rcap=None, sim='box'):
        self.word = word; self.N = len(word); self.rcap = rcap
        self.S = (a8.Orc if sim == 'orc' else a8.Box)(-6, self.N + 16)
        self.h = self.S.arr(a8.cell_state(word, rcap))

    def run(self, n):
        self.h = self.S.run(self.h, n); return self

    def flip(self, *cells):
        self.S.flip(self.h, cells); return self

    def kill(self, *cells):
        for c in cells:
            self.S.kill(self.h, c)
        return self

    def cells(self):
        return self.S.cells(self.h)

    def letters(self):
        return a8.letters_of(self.cells(), 4, 4 + self.N)

    def exact(self):
        """is the whole state exactly the cell of its own letters?"""
        w = self.letters()
        return '?' not in w and '_' not in w and self.cells() == a8.cell_state(w, self.rcap)

    def copy_state(self):
        return self.h.copy()


_REF = {}


def classify(nl, k, nr, flips, g0, sim='box', G=100):
    word = '7' * nl + 'd' * k + 'f' + '7' * nr
    if (word, sim, G) not in _REF:
        _REF[(word, sim, G)] = Line(word, a8.CAPR7, sim).run(G)
    ref = _REF[(word, sim, G)]
    x = Line(word, a8.CAPR7, sim).run(g0).flip(*flips).run(G - g0)
    c100 = x.cells()
    if c100 == ref.cells():
        return 'healed', c100
    w = x.letters(); ex = x.exact()
    x.run(2); w2 = x.letters(); x.run(2); still = x.cells() == c100
    if still:
        m = re.fullmatch(r'(7*)(d+)f(7*)', w)
        if m and ex:
            return 'count %+d' % (len(m.group(2)) - k), c100
        return 'standing', c100
    if not ex:
        return 'other', c100
    left, mid, right = w[:nl - 3].strip('7'), w[nl - 3:nl + k + 4].strip('7'), w[nl + k + 4:].strip('7')
    if bool(left) == bool(right):
        return 'other', c100
    rigid = (w2[:-1] == w[1:]) if left else (w2[1:] == w[:-1])
    if not rigid:
        return 'other', c100
    side, prod = ('<-', left) if left else ('->', right)
    if mid == '':
        return f'released {side} {a8.rle(prod)}', c100
    m = re.fullmatch(r'(d+)f', mid)
    if m and len(m.group(1)) == k:
        return f'pulse away {side} {a8.rle(prod)}', c100
    return 'other', c100


def census(k, norc, seed=8):
    nl = nr = 60; w0 = 4 + nl
    rows = []
    for g0 in (0, 1):
        for u in range(w0 - 3, w0 + k + 4):
            for c in E5:
                cls, cells = classify(nl, k, nr, [tr(c, u)], g0)
                rows.append((u - w0, c, g0, cls, hash(cells)))
    cnt = Counter(r[3] for r in rows)
    grp = Counter()
    for key, v in cnt.items():
        grp[key.split(' <-')[0].split(' ->')[0] if key.startswith(('released', 'pulse away')) else key] += v
    print(f'd^{k} f in wire B: {len(rows)} one-cell events (units -3..{k + 3} from the first d, 38 cells of the 5 x 5 tube, 2 phases)  [{time.time() - T0:.0f} s]')
    for key, v in sorted(grp.items(), key=lambda kv: -kv[1]):
        print(f'  {v:4d}  {key}')
    rel = [r for r in rows if r[3].startswith('released')]
    print(f"  released: {sum(1 for r in rel if '<-' in r[3])} to the left, {sum(1 for r in rel if '->' in r[3])} to the right")
    lt = Counter(r[3] for r in rel if '<-' in r[3])
    kinds = Counter()
    for key, v in lt.items():
        t = key.split('<- ')[1]
        raw = t
        if re.fullmatch(r'b(7b)*', t):
            kinds['separate pulses (b7)^j: ' + t] += v
        elif re.fullmatch(r'b\^?\d*|bb+', t):
            kinds['a block of adjacent b: ' + t] += v
        elif t.startswith('b5f'):
            kinds['b5f(9f)^j: ' + t] += v
        else:
            kinds['other train: ' + t] += v
    for key, v in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f'      <- {v:3d}  {key}')
    json.dump([dict(u=r[0], cell=r[1], g0=r[2], cls=r[3]) for r in rows], open(a8.os.path.join(a8.HERE, 'out', f'census_k{k}.json'), 'w'))
    if norc:
        rng = random.Random(seed); by = defaultdict(list)
        for r in rows:
            by[r[3].split(' ')[0] if not r[3].startswith('count') else r[3]].append(r)
        bad = 0; n = 0
        for key, v in by.items():
            for r in rng.sample(v, min(norc, len(v))):
                cls, cells = classify(nl, k, nr, [tr(r[1], r[0] + w0)], r[2], sim='orc')
                n += 1; bad += (cls != r[3]) or (hash(cells) != r[4])
        print(f'  oracle: {n} events (up to {norc} of each class) re-run; class and whole state at generation 100 equal to st8 in {n - bad}  [{time.time() - T0:.0f} s]')
    return rows


TRIGGERS = [  # (name, unit relative to the stretch's first unit, cell, phase, kind, expected product as a function of k)
    ('stator (0,1,2) of the unit before the stretch removed, phase 0', -1, (0, 1, 2), 0, lambda k: ('b7' * k)[:-1]),
    ('site (1,0,2) of that unit removed, phase 0', -1, (1, 0, 2), 0, lambda k: ('b7' * k)[:-1]),
    ('stator (0,1,4) of that unit removed, phase 1', -1, (0, 1, 4), 1, lambda k: ('b7' * k)[:-1]),
    ('(1,4,2) of that unit made live (outside the 3 x 3 tube), phase 0', -1, (1, 4, 2), 0, lambda k: ('b7' * k)[:-1]),
    ('(0,2,3) of the first unit of the stretch removed, phase 0', 0, (0, 2, 3), 0, lambda k: ('b7' * (k - 1))[:-1]),
    ('(0,2,3) of the unit before the stretch made live, phase 0', -1, (0, 2, 3), 0, lambda k: 'b5f' + '9f' * k),
    ('stator (0,1,4) of the unit before the stretch removed, phase 0', -1, (0, 1, 4), 0, lambda k: 'b5f' + '9f' * (k + 1)),
    ('site (1,0,4) of the unit before the stretch removed, phase 0', -1, (1, 0, 4), 0, lambda k: 'b' * (2 * k + 2)),
]


def law_one(trig, k, sim='box'):
    name, du, c, g0, form = trig
    nl = 2 * k + 60; G = 4 * k + 100 + g0
    x = Line('7' * nl + 'd' * k + 'f' + '7' * 20, a8.CAPR7, sim).run(g0).flip(tr(c, 4 + nl + du)).run(G - g0)
    w = x.letters(); ex = x.exact()
    x.run(2); w2 = x.letters()
    return w.strip('7') == form(k) and ex and w2[:-1] == w[1:] and set(w[nl - 2:]) == {'7'}


def law(K, orc):
    ok_all = True
    for trig in TRIGGERS:
        okk = [law_one(trig, k) for k in range(1, K + 1)]
        oko = [law_one(trig, k, 'orc') for k in orc]
        ok_all &= all(okk) and all(oko)
        print(('PASS ' if all(okk) and all(oko) else 'FAIL ') + f"{trig[0]}: k = 1..{K} (st8): {sum(okk)} of {K} give exactly the push's train, rigid, the wire plain behind; "
              f"oracle k = {orc}: {oko}" + ('' if all(okk) else f' failing k: {[k for k in range(1, K + 1) if not okk[k - 1]]}') + f'  [{time.time() - T0:.0f} s]', flush=True)
    return ok_all


def catch(K):
    ok = True; res = []
    for k in range(1, K + 1):
        word = '7' * 10 + 'df' + '7' * 20 + 'd' * k + 'f' + '7' * 10
        for sim in (['box', 'orc'] if k in (3, 7, 12) else ['box']):
            x = Line(word, None, sim).kill(tr(SR, 4 + 31)).run(200 + 4 * k)
            good = x.cells() == a8.cell_state('7' * 10 + 'd' * (k + 1) + 'f' + '7' * (len(word) - 12 - k))
            ok &= good; res.append((k, sim, good))
    print(('PASS ' if ok else 'FAIL ') + f'catch: a receiver df 20 units to the left holds k + 1 after the count read of a store holding k, the store gone, k = 1..{K} '
          f'(oracle for k = 3, 7, 12): {all(g for _, _, g in res)}  [{time.time() - T0:.0f} s]')
    return ok


def smallest():
    """every N: (a) pairs R@u, L@v that set; (b) from each set state, every single stator op that gives count 2;
    (c) from each count-2 state, every single stator op after which the cell is empty again, with or without two
    separate b on the wire at some even generation"""
    for N in range(3, 10):
        e0 = a8.cell_state('7' * N)
        ok0 = Line('7' * N).run(2).cells() == e0
        sets = {}
        for u in range(4, 4 + N):
            for v in range(4, 4 + N):
                if u == v:
                    continue
                x = Line('7' * N).kill(tr(SR, u), tr(SL, v)).run(160)
                w = x.letters()
                if x.exact() and w.replace('7', '') == 'df':
                    sets[(u, v)] = w
        adds = {}
        for w in sorted(set(sets.values())):
            for nm, st in (('R', SR), ('L', SL)):
                for u in range(4, 4 + N):
                    x = Line(w)
                    if not x.S.live(x.h, tr(st, u)):
                        continue
                    x.kill(tr(st, u)).run(160)
                    w2 = x.letters()
                    if x.exact() and w2.replace('7', '') == 'ddf':
                        adds[(w, nm, u)] = w2
        reads = []; reads2 = []
        for w2 in sorted(set(adds.values())):
            for nm, st in (('R', SR), ('L', SL)):
                for u in range(4, 4 + N):
                    x = Line(w2)
                    if not x.S.live(x.h, tr(st, u)):
                        continue
                    x.kill(tr(st, u)); two = False
                    for g in range(0, 80, 2):
                        ww = x.letters()
                        if ww.replace('7', '') in ('bb', '6f6f') and 'bb' not in ww and x.exact():
                            two = True
                        x.run(2)
                    x.run(120)
                    if x.cells() == e0:
                        reads.append((w2, nm, u))
                        if two:
                            reads2.append((w2, nm, u))
        print(f'  N = {N} ({38 + 5 * N} cells; stands: {ok0}): set by {len(sets)} pairs -> {sorted(set(sets.values()))}; add one: {len(adds)} operations -> {sorted(set(adds.values()))}; '
              f'one operation that empties a count-2 cell: {len(reads)}, of which with two separate pulses seen on the wire: {len(reads2)}' + (f', e.g. {reads2[0]}' if reads2 else ''))


def inside(K):
    for k in range(1, K + 1):
        word = '7' * 20 + 'd' * k + 'f' + '7' * 20; rowR = []; rowL = []
        for nm, st, row in (('R', SR, rowR), ('L', SL, rowL)):
            for j in range(0, k + 1):
                x = Line(word).kill(tr(st, 4 + 20 + j)).run(4 * k + 200)
                w = x.letters()
                m = re.fullmatch(r'(7*)(d+)f(7*)', w)
                row.append('E' if set(w) == {'7'} and x.exact() else ('%d@%+d' % (len(m.group(2)), len(m.group(1)) - 20) if m and x.exact() else a8.rle(w.strip('7'))))
        print(f'  k = {k}: stator (0,1,2) of unit 1..k and of the edge unit: {rowR};  stator (0,1,4): {rowL}')


if __name__ == '__main__':
    what = sys.argv[1]
    arg = lambda n, d: (sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d)
    if what == 'census':
        census(int(arg('--k', 3)), int(arg('--orc', 0)))
    elif what == 'law':
        ok = law(int(arg('--K', 40)), [int(v) for v in arg('--orc', '5,17').split(',') if v])
        print('ALL PASS' if ok else 'SOME FAIL')
    elif what == 'catch':
        catch(int(arg('--K', 12)))
    elif what == 'smallest':
        smallest()
    elif what == 'inside':
        inside(int(arg('--K', 6)))
