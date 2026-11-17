#!/usr/bin/env python3
"""The census of push 7: ends of the rake train, deduplicated up to translation and time shift, each sent every
signal of the train that runs into an end and the words of holes of the fifth push, with the outcome classified.

    python census7.py OUT.json LIST.json [LIST.json ...] [--part i/n] [--gmax 1500] [--guns]

--guns: the lists hold guns (cnf7.py with TRAIN 5f: the train (5f)^inf leaving towards -v; the line frame of
echo-train.json); the events are the kinds of signals7_5f.json that run up the stream into the gun (U, N1, E and the
pair EE) and the upper edge of wire B (E below H, meeting in front of the gun); an 'echo' is then a signal sent back
down the stream.

LISTs: cnf7.py decode output (or sat_gun --all output): absorbers of (fb)^inf at a +v end, KS = 6.
Dedup key as census_ends.py: the set over one period of the orbit's difference from the plain train, moved so that
its lowest unit is 0 (a translation by k units with a time shift of 2k is a symmetry of the train).

Events (each applied to the end in its cycle, the signal set upstream and riding in):
  hole words [0], [1], [2], [3], [0,1], [0,1,2], [0,2], [0,2,4,6,8]: rake cell (1,0,4) removed at generation 0 from
     the i-th rake counted from the end (exactly census_ends.py's words);
  every down-moving kind of signals7.json (H, K0, K3, N2, N3, N4, ... as found there): the train at generation
     g = 1 + 4j xor the kind's cells at phase 1 moved to an even unit u0 = KS - 24 (and, for ends of period 8, also
     at generation g + 4: the other arrival phase);
  the lower edge of wire B (E meeting H): E at unit KS - 26 and H at unit KS - 40 (parities of signals7.json) at
     generation 1; they meet upstream and the lower edge of the wire B runs down into the end.
Stepping: step7 (checked against the oracle by check7.py), a window of units KS - 100 .. KS + 14, the plain train
below it, dead above.  Outcome after the event, the disturbed run x against the undisturbed run y in lockstep:
  'healed'   x == y on the whole window, at some generation (whole state: nothing left anywhere);
  'echo:K'   at the generation the difference first reaches units KS - 100 .. KS - 80 (far upstream), x == y on units
             >= KS - 30 (the end and 24 units in front restored) and the difference is one rigid up-moving signal of
             kind K (checked over two more generations); 'up:other' if it is not a single known signal;
  'dead'     the difference reaches far upstream and the end (units >= KS - 30) is not restored;
  'alive'    by generation gmax the difference has not reached far upstream and x != y: candidate (a listener if
             the near region is periodic and the train in front plain); saved with its final state.
"""
import sys, os, json, argparse
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sg, sat_gun as G
from scat import unit, tr
from step7 import Window, NC

HERE = os.path.dirname(os.path.abspath(__file__))
TRAIN = '5f' if '--guns' in sys.argv else 'fb'        # --guns: ends that emit the train (5f)^inf towards -v
TD = 1 if TRAIN == 'fb' else -1
pat, _ = G.train([int(ch, 16) for ch in TRAIN], True, TD)
IN = 'down' if TRAIN == 'fb' else 'up'                   # the direction of the signals that run INTO the end
OUT = 'up' if TRAIN == 'fb' else 'down'
WORDS = [[0], [1], [2], [3], [0, 1], [0, 1, 2], [0, 2], [0, 2, 4, 6, 8]]
SK = json.load(open(os.path.join(HERE, 'signals7.json' if TRAIN == 'fb' else 'signals7_5f.json')))['kinds']
KS = 6; WL = 100; WR = 14
# names of the kinds of signals7.json (by index; checked in signals7's output: H is the hole of census_ends.py)
NAMES = ['K0', 'H', 'N4', 'D3', 'D4=K0K0', 'D5=HH', 'D6', 'D7', 'N1', 'U', 'E', 'EE'] if TRAIN == 'fb' else     ['K0', 'H', 'D2', 'D3', 'N4', 'D5', 'U', 'N1', 'E', 'EE']     # signals7_5f.json (the line frame of echo-train.json)
assert len(NAMES) == len(SK)


def key_of(states, t0):
    ks = []
    for j, s in enumerate(states):
        lo = min(unit(c) for c in s); hi = max(unit(c) for c in s) + 2
        d = s ^ G.train_cells(pat, t0 + j, lo, hi + 1, TD)
        if not d:
            return None
        m = min(unit(c) for c in d)
        ks.append(tuple(sorted(tr(c, -m) for c in d)) + (('par', (t0 + j) % 2),))
    return frozenset(ks)


def window(s, w=40):
    return frozenset(c for c in s if unit(c) >= KS - w)


def load_ends(lists):
    """Distinct ends of the lists (key_of over one period T, computed with step7 on units >= KS - 20)."""
    ends = {}; entries = 0
    Wk = Window(TRAIN, KS - 40, KS + WR)
    for fn in lists:
        d = json.load(open(fn)); T = d['T']; assert d['KS'] == KS
        for e in d['list']:
            entries += 1
            cap = frozenset(tuple(c) for c in e['cap'])
            a = Wk.array(G.train_cells(pat, 0, KS - 40, KS, TD) | cap); a0 = a.copy()
            st = []
            for t in range(T):
                st.append(frozenset(c for c in Wk.cells(a) if unit(c) >= KS - 20)); Wk.run(a, t, 1)
            assert np.array_equal(a[10:], a0[10:]), 'not periodic'
            k = key_of(st, 0)
            if k not in ends:
                ends[k] = dict(src=os.path.basename(fn), C=d['C'], lo=d['lo'], hi=d['hi'], T=T, cap=sorted(cap), cells=len(cap))
    return ends, entries


def period_of(W, cap):
    a = W.array(G.train_cells(pat, 0, W.ua, KS, TD) | cap); a0 = a.copy()
    for t in range(8):
        W.run(a, t, 1)
        if t + 1 in (4, 8) and np.array_equal(a[WL - 30:], a0[WL - 30:]):
            return t + 1
    return None


def kind_of(D):
    """D: frozenset of difference cells; the up-moving kind of signals7 it equals (any position of right parity)."""
    m = min(unit(c) for c in D); m0 = m - m % 2
    can = sorted(tr(c, -m0) for c in D)
    for i, k in enumerate(SK):
        if [tuple(c) for c in k['cells']] == can:
            return i
    return None


def classify(W, x, y, t, gmax):
    """x, y arrays at generation t; lockstep."""
    far = slice(0, 20); near = slice(WL - 30, None)
    while t < gmax:
        W.run(x, t, 2); W.run(y, t, 2); t += 2
        if np.array_equal(x, y):
            return 'healed', t, None
        if not np.array_equal(x[far], y[far]):
            if np.array_equal(x[near], y[near]):
                D = W.cells(x ^ y)
                # rigid and up-moving over the next 2 generations?  (only units > far region compared)
                x2, y2 = x.copy(), y.copy(); W.run(x2, t, 2); W.run(y2, t, 2)
                D2 = W.cells(x2 ^ y2)
                lo = W.ua + 22
                Da = frozenset(c for c in D if unit(c) >= lo); Db = frozenset(tr(c, 1) for c in D2 if unit(c) >= lo - 1)
                if (t - 1) % 4 == 0 or (t - 1) % 4 == 2:
                    pass
                if Da == frozenset(c for c in Db if unit(c) >= lo) and len(D) <= 16:
                    # name it at phase 1: step to the next t = 1 mod 4 if needed
                    x3, y3 = x.copy(), y.copy(); tt = t
                    while tt % 4 != 1:
                        W.run(x3, tt, 1); W.run(y3, tt, 1); tt += 1
                    k = kind_of(W.cells(x3 ^ y3))
                    return (f'echo:{NAMES[k]}' if k is not None and SK[k]['dir'] == OUT else 'up:other'), t, sorted(D)
                return 'up:other', t, sorted(D)
            return 'dead', t, None
    return 'alive', t, None


def events_for(T):
    ev = [('word', w, 0) for w in WORDS] if TRAIN == 'fb' else []
    for i, k in enumerate(SK):
        if k['dir'] == IN:
            ev.append(('sig', i, 0))
            if T == 8:
                ev.append(('sig', i, 4))
    ev.append(('wireB', None, 0))
    return ev


def find_kind(name_cells):
    for i, k in enumerate(SK):
        if sorted(tuple(c) for c in k['cells']) == sorted(name_cells):
            return i
    return None


def start_states(W, cap, ev):
    """(x, y, t): the disturbed and undisturbed arrays at generation t."""
    y = W.array(G.train_cells(pat, 0, W.ua, KS, TD) | cap)
    typ, arg, dt = ev
    if typ == 'word':
        rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in G.train_cells(pat, 0, KS - 40, KS, 1)), reverse=True)
        x = W.array((G.train_cells(pat, 0, W.ua, KS, TD) | cap) - {tr((1, 0, 4), rakes[i]) for i in arg})
        return x, y, 0
    t = 1 + dt
    W.run(y, 0, t); x = y.copy()
    if typ == 'sig':
        D = [tr(tuple(c), KS - 24) for c in SK[arg]['cells']]
    else:
        iE = NAMES.index('E'); iH = NAMES.index('H')
        uE, uH = (KS - 26, KS - 40) if TRAIN == 'fb' else (KS - 40, KS - 26)
        D = [tr(tuple(c), uE) for c in SK[iE]['cells']] + [tr(tuple(c), uH) for c in SK[iH]['cells']]
    for c in D:
        u = unit(c); x[u - W.ua, __import__('step7').INDEX[tr(c, -u)]] ^= 1
    return x, y, t


WB = None
WBT = None


def wireB_template():
    """Wire B as the meeting of E and H leaves it (ring mode, 200 units, E at unit 100 and H at unit 86 at generation
    1, as start_states places them at KS - 26 and KS - 40): WBT[t % 4][u % 2] = the cells of a unit u in the middle of
    the wire B (units 90, 91) at generations 60..63; checked uniform on units 80..107 at each of those generations."""
    global WBT
    if WBT is None:
        R = Window(TRAIN, 0, 200); x = R.train(1)
        from step7 import INDEX
        for i, u0 in ((NAMES.index('E'), 100 if TRAIN == 'fb' else 86), (NAMES.index('H'), 86 if TRAIN == 'fb' else 100)):
            for c in SK[i]['cells']:
                c = tr(tuple(c), u0); u = unit(c); x[u, INDEX[tr(c, -u)]] ^= 1
        R.run(x, 1, 59, 'ring'); WBT = np.zeros((4, 2, NC), np.uint8)
        for t in range(60, 64):
            for p in (0, 1):
                WBT[t % 4, p] = x[90 + p]
                assert all(np.array_equal(x[u], x[90 + p]) for u in range(80 + p, 108, 2)), "wire B not uniform"
            R.run(x, t, 1, 'ring')
    return WBT


def classify_wireB(cap):
    """The lower edge of wire B arriving: a window of 220 units below the end (exact for some 400 generations: the
    upper edge needs that long to reach the window's lower boundary from KS - 30).  At t = 200..216: is the region of
    units >= KS - 30 periodic (period dividing 8), with units KS - 30 .. KS - 16 non-empty and of period 2?
    'wireB:cap' if moreover those units are wire B (wireB_template): an end of wire B (candidate); 'wireB:wall' if
    they are another wire (the end stands and has sent a front up the wire B that converts it); 'wireB:periodic-no-
    wire' if periodic without a wire in front (debris); 'wireB:dead' otherwise."""
    global WB
    if WB is None:
        WB = Window(TRAIN, KS - 220, KS + WR)
    x, y, t = start_states(WB, cap, ('wireB', None, 0))
    WB.run(x, t, 200 - t); t = 200
    seq = []
    for j in range(17):
        seq.append(x[220 - 30:].copy()); WB.run(x, t, 1); t += 1
    per = all(np.array_equal(seq[j], seq[j + 8]) for j in range(9))
    wire = seq[0][:14].any() and all(np.array_equal(seq[j][:14], seq[j + 2][:14]) for j in range(15))
    T = wireB_template(); u0 = KS - 30
    isB = all(np.array_equal(seq[j][k], T[(200 + j) % 4, (u0 + k) % 2]) for j in range(17) for k in range(14))
    if per and wire and isB:
        return 'wireB:cap', t, None
    if per and wire:
        return 'wireB:wall', t, None
    if per:
        return 'wireB:periodic-no-wire', t, None
    return 'wireB:dead', t, None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('lists', nargs='+')
    ap.add_argument('--part', default='0/1'); ap.add_argument('--guns', action='store_true'); ap.add_argument('--gmax', type=int, default=1500)
    a = ap.parse_args()
    ends, entries = load_ends(a.lists)
    print(f'{entries} list entries, {len(ends)} distinct ends', flush=True)
    pi, pn = map(int, a.part.split('/'))
    W = Window(TRAIN, KS - WL, KS + WR)
    rows = []; res = Counter(); vec = Counter()
    done = {}
    if os.path.exists(a.out):
        for r in json.load(open(a.out))['rows']:
            done[r['i']] = r
    items = list(ends.values())
    for i in range(pi, len(items), pn):
        e = items[i]
        if i in done:
            rows.append(done[i]); continue
        cap = frozenset(tuple(c) for c in e['cap'])
        per = period_of(W, cap)
        out = []
        for ev in events_for(e['T'] if per is None else per):
            if ev[0] == 'wireB':
                o, tt, info = classify_wireB(cap)
            else:
                x, y, t = start_states(W, cap, ev)
                o, tt, info = classify(W, x, y, t, a.gmax)
            out.append(dict(ev=[ev[0], ev[1], ev[2]], out=o, t=tt))
            res[o] += 1
            if o not in ('healed', 'dead', 'wireB:dead', 'wireB:wall', 'wireB:periodic-no-wire'):
                print(f'  end {i} ({e["cells"]} cells, C={e["C"]}) event {ev}: {o} at {tt}', flush=True)
        rows.append(dict(i=i, src=e['src'], C=e['C'], lo=e['lo'], hi=e['hi'], cells=e['cells'], period=per,
                         cap=[list(c) for c in e['cap']], outcomes=out))
        if len(rows) % 20 == 0:
            json.dump(dict(rows=rows), open(a.out, 'w'))
            print(f'  {len(rows)} ends done: {dict(res)}', flush=True)
    json.dump(dict(rows=rows, nends=len(items), entries=entries), open(a.out, 'w'))
    vc = Counter(tuple(o['out'] for o in r['outcomes']) for r in rows)
    print(f'part {a.part}: {len(rows)} ends; outcomes {dict(res)}')
    for v, n in vc.most_common():
        print('  ', n, v)


if __name__ == '__main__':
    main()
