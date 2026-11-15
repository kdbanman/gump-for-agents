#!/usr/bin/env python3
"""Attack 2 of the fifth push: a census of the ends of the rake train (absorbers), deduplicated up to translation and
time shift, and its transition graph under words of gaps.  sg.step_set only.

    python3 census_ends.py LIST.json [LIST.json ...] [--out F.json]

Each LIST is written by `sat_gun.py fb C --dir 1 [--mult m] [--lo L --hi H] --all --out LIST` (absorbers of the
train (fb)^inf moving into the +v end).  Dedup: for an end A of period dividing T, d(t) = cells of the orbit at t that
differ from the plain train at t (a finite set), moved so that its lowest unit is 0; key(A) = the set of d(t) over
one period.  Translating an end by k units and shifting time by 2k (the train moves one unit per 2 generations)
leaves the key unchanged; odd time shifts are not symmetries of the train.  Two list entries with one key are one end.
Words (rakes removed, counted from the end, the rake cell (1,0,4) at generation 0): [0], [1], [2], [3], [0,1],
[0,1,2], [0,2], [0,2,4,6,8].  Outcome after the word: 'healed' (equal to the undisturbed run, cell for cell, near the
end, within 300 generations), else the run is followed to 1500 generations and classed: 'dead' (the train 100
units from the end, or 40 to 60 units at the end of the run, is not the plain train: the end burnt back or something
runs up the stream), 'not periodic', or an end of
period p alive, with its key: 'SAME KEY, NOT HEALED' (the end moved or shifted its phase: a mover) or 'NEW END'
(a listener).  Edges between two live ends are printed."""
import json, sys, argparse
from collections import Counter, defaultdict
import sg, scat, sat_gun as G
from scat import unit, tr

ap = argparse.ArgumentParser(); ap.add_argument('lists', nargs='+'); ap.add_argument('--out'); ap.add_argument('--part', default='0/1')
a = ap.parse_args()
pat, _ = G.train([0xf, 0xb], True, 1)
WORDS = [[0], [1], [2], [3], [0, 1], [0, 1, 2], [0, 2], [0, 2, 4, 6, 8]]


def key_of(states, t0):
    ks = []
    for j, s in enumerate(states):
        hi = max(unit(c) for c in s) + 2
        lo = min(unit(c) for c in s)          # s is a window: complete on units >= lo
        d = s ^ G.train_cells(pat, t0 + j, lo, hi + 1, 1)
        if not d:
            return None
        m = min(unit(c) for c in d)
        ks.append(tuple(sorted(tr(c, -m) for c in d)) + (('par', (t0 + j) % 2),))
    return frozenset(ks)


def window(s, KS, w=40):
    return frozenset(c for c in s if unit(c) >= KS - w)


ends = {}; entries = 0
for fn in a.lists:
    d = json.load(open(fn)); KS = d['KS']; T = d['T']
    for e in d['list']:
        entries += 1
        cap = frozenset(tuple(c) for c in e['cap'])
        x = G.train_cells(pat, 0, -60, KS, 1) | cap
        st = []
        for t in range(T):
            st.append(window(x, KS, 20)); x = sg.step_set(x)
        assert window(x, KS, 20) == st[0], 'not periodic'
        k = key_of(st, 0)
        if k not in ends:
            ends[k] = dict(src=fn.split('/')[-1], KS=KS, T=T, cap=sorted(cap), cells=len(cap))
print(f'{entries} list entries, {len(ends)} distinct ends up to translation and time shift', flush=True)
names = {k: i for i, k in enumerate(ends)}
res = Counter(); edges = []
pi, pn = map(int, a.part.split('/'))
W = 100


def wstep(x, t, KS):
    """One generation on the window of units >= KS - W, the plain train refilled below it (exact while the two units
    KS - W .. KS - W + 1 still hold the plain train, which the caller checks)."""
    y = sg.step_set(x)
    return frozenset(c for c in y if unit(c) >= KS - W) | G.train_cells(pat, t + 1, KS - W - 3, KS - W, 1)


def plain_at(x, t, KS, a_, b_):
    return frozenset(c for c in x if a_ <= unit(c) < b_) == G.train_cells(pat, t, a_, b_, 1)


done = 0; vectors = []
for k, e in list(ends.items())[pi::pn]:
    vec = []
    KS = e['KS']; cap = frozenset(tuple(c) for c in e['cap'])
    rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in G.train_cells(pat, 0, KS - 40, KS, 1)), reverse=True)
    for wd in WORDS:
        y = G.train_cells(pat, 0, KS - W - 3, KS, 1) | cap
        x = y - {tr((1, 0, 4), rakes[i]) for i in wd}
        out = None
        for t in range(1500):
            x = wstep(x, t, KS); y = wstep(y, t, KS)
            if t < 300 and window(x, KS) == window(y, KS):
                out = 'healed'; break
            if not plain_at(x, t + 1, KS, KS - W, KS - W + 20):
                out = 'dead'; break
        if out is None:
            tt = 1500; seq = []
            for j in range(48):
                seq.append(window(x, KS, 60)); x = wstep(x, tt + j, KS)
            p = next((q for q in range(1, 25) if all(seq[i + q] == seq[i] for i in range(24))), None)
            plainnear = all(plain_at(seq[j], tt + j, KS, KS - 60, KS - 40) for j in range(8))
            if not plainnear:
                out = 'dead'
            elif p is None:
                out = 'not periodic'
            else:
                k2 = key_of([frozenset(c for c in seq[j] if unit(c) >= KS - 50) for j in range(p if p % 2 == 0 else 2 * p)], tt)
                if k2 == k:
                    out = 'SAME KEY, NOT HEALED'
                else:
                    out = 'NEW END'
                    if k2 not in names:
                        names[k2] = len(names)
                edges.append((names[k], wd, out, names.get(k2), p))
                print(f'  end #{names[k]} ({e["src"]}, {e["cells"]} cells) word {wd}: {out}, period {p}, -> #{names.get(k2)}', flush=True)
        res[out] += 1; vec.append(out)
    vectors.append(dict(end=names[k], src=e['src'], cells=e['cells'], outcomes=vec))
    done += 1
    if done % 50 == 0:
        print(f'  {done} ends done: {dict(res)}', flush=True)
print(f'part {a.part}: outcomes over', len(list(ends)[pi::pn]), 'ends x', len(WORDS), 'words:', dict(res))
if a.out:
    json.dump(dict(ends=list(ends.values()), outcomes=dict(res), edges=edges, vectors=vectors, words=WORDS), open(a.out, 'w'))
vc = Counter(tuple(v['outcomes']) for v in vectors)
print('outcome vectors over the words', WORDS, ':')
for v, n in vc.most_common():
    print('  ', n, v)
