#!/usr/bin/env python3
"""A finite line that keeps a count: gun + train + receiving end, both ends of the kinds that cap wire B (push 7).

    python line7.py GUNCENSUS.json ENDCENSUS.json [--N 40] [--n 0,1,2,3,4] [--s 3] [--gun i] [--end j] [--json OUT]

Frame: the line frame (the gun frame of census7 --guns, = objects/echo-train.json's frame): the train (5f)^inf
moves towards -v, the gun at the +v end.  The receiving end is an absorber of the absorber frame (census7, train
(fb)^inf moving +v) mapped by the mirror M(x,y,z) = (z - 4, y, x + 4) (the reflection exchanging the two ends of wire
C, README section 9; an involution), then translated and stepped so that its train is the gun's train at generation 0
(the alignment is searched for and asserted).  The line: the mirrored end at units 0.., the train, the gun moved so
that its first free unit is N; all of it a finite object, stepped with step7 in 'dead' mode (nothing outside).
Checks: (1) the line alone is periodic (period 4, the whole object) for 200 generations; (2) for each n: E put at
unit N/2 - 8 and n holes H at units N/2 + 8 + 2 s j (even units, the parity of both kinds; N a multiple of 4) (j < n), all at generation 1 (train phase 1; signals7_5f.json);
the run to generation G = 6N + 400; then the whole object has period dividing 8 (generations G..G+16), and the
object differs between different n.  Printed: per unit, '.' wire B, 'B' wire B' (wire B with (1,0,2) off and (0,2,3)
on, read from the run itself as the units that are not wire B and not empty between the two caps), '#' other.
"""
import sys, os, json, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shim  # noqa: F401
import sat_gun as G
from scat import unit, tr
from step7 import Window, INDEX

HERE = os.path.dirname(os.path.abspath(__file__))
KS = 6
P5, _ = G.train([0x5, 0xf], True, -1)
PF, _ = G.train([0xf, 0xb], True, 1)
SK5 = json.load(open(os.path.join(HERE, 'signals7_5f.json')))['kinds']
N5 = ['K0', 'H', 'D2', 'D3', 'N4', 'D5', 'U', 'N1', 'E', 'EE']


def M(c):
    return (c[2] - 4, c[1], c[0] + 4)


def tr5(t, a, b):
    return frozenset(G.train_cells(P5, t, a, b, -1))


def mirrored_end(cap):
    """The absorber `cap` (absorber frame, train (fb) on units < 6 at generation 0) mirrored into the line frame and
    re-expressed so that it sits at the -v end of the (5f) train at generation 0, its lowest free unit at 0.
    Returns the cells of the end (units >= its first unit that is not the train) and that first unit."""
    W = Window('fb', -60, 30)
    a = W.array(G.train_cells(PF, 0, -60, KS, 1) | frozenset(cap))
    x = W.cells(a)
    m = frozenset(M(c) for c in x)
    hi_u = max(unit(c) for c in m) - 8            # a band of plain (mirrored) train well inside
    for t in range(4):
        for k in range(-80, 80):
            mm = frozenset(tr(c, k) for c in m)
            band = frozenset(c for c in mm if hi_u + k - 6 <= unit(c) < hi_u + k)
            if band == tr5(t, hi_u + k - 6, hi_u + k):
                # mm is the end at the -v end of the (5f) train at generation t; step to generation 0 mod 4
                Wd = Window('5f', -150, 150)
                b = Wd.array(mm)
                tt = t
                while tt % 4:
                    Wd.run(b, tt, 1, 'dead'); tt += 1
                y = Wd.cells(b)
                # first unit (from below) that differs from the train at generation 0... from above: lowest unit
                # above which everything up to the band is the train
                lo = min(unit(c) for c in y)
                u = hi_u + k - 30
                while frozenset(c for c in y if unit(c) == u) == tr5(0, u, u + 1):
                    u -= 1
                end = frozenset(c for c in y if unit(c) <= u + 2)
                # the train above u+2 up to the band is plain; move so that the end's lowest unit is 0... keep parity
                sh = -(lo - (lo % 2))
                return frozenset(tr(c, sh) for c in end), u + 2 + sh, (t, k)
    raise AssertionError('no alignment of the mirrored train with the (5f) train')


def build_line(gcap, ecap, N):
    end, utop, al = mirrored_end(ecap)
    # gun: list state at generation 0 has the (5f) train on units < KS and free cells on units >= KS; move by an even
    # number of units so that its first free unit is N (N even keeps the train's phase)
    assert N % 2 == 0
    gun = frozenset(tr(tuple(c), N - KS) for c in gcap)
    train = tr5(0, utop + 1, N)
    return end | train | gun, al


def window_for(N):
    return Window('5f', -20, N + 30)


def letters(W, a, t):
    """'.' if a unit equals wire B (template from a run of E meeting H on a ring of the line frame), '_' empty, else
    '#'."""
    return ''.join('_' if not a[u].any() else ('.' if np.array_equal(a[u], WBT[t % 4, (W.ua + u) % 2]) else '#') for u in range(a.shape[0]))


def wireB_template():
    R = Window('5f', 0, 200); x = R.train(1)
    for name, u0 in (('E', 86), ('H', 100)):
        for c in SK5[N5.index(name)]['cells']:
            c = tr(tuple(c), u0); u = unit(c); x[u, INDEX[tr(c, -u)]] ^= 1
    R.run(x, 1, 59, 'ring'); T = np.zeros((4, 2, x.shape[1]), np.uint8)
    for t in range(60, 64):
        for p in (0, 1):
            T[t % 4, p] = x[90 + p]
            assert all(np.array_equal(x[u], x[90 + p]) for u in range(80 + p, 108, 2)), 'wire B not uniform'
        R.run(x, t, 1, 'ring')
    return T


WBT = None


def main():
    global WBT
    ap = argparse.ArgumentParser(); ap.add_argument('guns'); ap.add_argument('ends')
    ap.add_argument('--N', type=int, default=40); ap.add_argument('--n', default='0,1,2,3,4'); ap.add_argument('--s', type=int, default=3)
    ap.add_argument('--gun', type=int, default=0); ap.add_argument('--end', type=int, default=0); ap.add_argument('--json')
    a = ap.parse_args()
    WBT = wireB_template()
    grows = sorted([r for r in json.load(open(a.guns))['rows'] if r['outcomes'][-1]['out'] == 'wireB:cap'], key=lambda r: (r['cells'], r['i']))
    erows = sorted([r for r in json.load(open(a.ends))['rows'] if r['outcomes'][-1]['out'] == 'wireB:cap'], key=lambda r: (r['cells'], r['i']))
    g, e = grows[a.gun], erows[a.end]
    print(f"gun {g['i']} ({g['cells']} cells, of {len(grows)} guns that cap wire B); end {e['i']} ({e['cells']} cells, of {len(erows)} ends)")
    N = a.N
    line, al = build_line([tuple(c) for c in g['cap']], [tuple(c) for c in e['cap']], N)
    W = window_for(N)
    x0 = W.array(line)
    assert W.cells(x0) == line
    x = x0.copy(); per = True
    for t in range(0, 200, 4):
        W.run(x, t, 4, 'dead')
        if not np.array_equal(x, x0):
            per = False; print(f'  the line alone is not periodic: first differs at generation {t + 4}'); break
    print(f"  line N={N}: {len(line)} cells, mirror alignment (t, k) = {al}; the line alone has period 4 for 200 generations: {per}")
    if not per:
        return
    finals = {}; recs = []
    Gn = 6 * N + 400
    for n in map(int, a.n.split(',')):
        y = x0.copy(); W.run(y, 0, 1, 'dead'); xx = y.copy()
        D = [tr(tuple(c), N // 2 - 8) for c in SK5[N5.index('E')]['cells']]
        for j in range(n):
            D += [tr(tuple(c), N // 2 + 8 + 2 * a.s * j) for c in SK5[N5.index('H')]['cells']]
        for c in D:
            u = unit(c); xx[u - W.ua, INDEX[tr(c, -u)]] ^= 1
        W.run(xx, 1, Gn - 1, 'dead')
        seq = []
        for j in range(17):
            seq.append(xx.copy()); W.run(xx, Gn + j, 1, 'dead')
        p8 = all(np.array_equal(seq[j], seq[j + 8]) for j in range(9))
        p = next((q for q in (1, 2, 4, 8) if all(np.array_equal(seq[j], seq[j + q]) for j in range(17 - q))), None)
        finals[n] = seq[0]
        print(f"  n={n}: whole object at generation {Gn}: {int(seq[0].sum())} cells, period {p} (dividing 8: {p8})")
        print(f"      units {W.ua}..{W.ub - 1}: {letters(W, seq[0], Gn)}")
        recs.append(dict(name=f"line-N{N}-gun{g['i']}-end{e['i']}-n{n}", L=N + 60, ulo=W.ua - 5, y0=[list(c) for c in sorted(line)],
                         flips=[[1, [list(c) for c in D]]], claim=dict(type='orbit', gen=Gn, until=Gn + 16, period=8, ua=W.ua - 5, ub=W.ua + N + 55),
                         text=f"finite line N={N} (gun {g['i']}, mirrored end {e['i']}) with E and {n} holes: the whole object has period dividing 8 at generations {Gn}..{Gn + 16}"))
    ns = sorted(finals)
    for i in range(len(recs) - 1):
        recs.append(dict(name=recs[i]['name'] + '-vs-next', L=recs[i]['L'], ulo=recs[i]['ulo'], y0=recs[i]['y0'], flips=recs[i]['flips'],
                         claim=dict(type='distinct', flips2=recs[i + 1]['flips'], until=Gn),
                         text=f"the line's final objects after {ns[i]} and {ns[i + 1]} holes differ at generation {Gn}"))
    print('  final objects pairwise different:', all(not np.array_equal(finals[i], finals[j]) for i in ns for j in ns if i < j))
    if a.json:
        recs.append(dict(name=f"line-N{N}-gun{g['i']}-end{e['i']}-alone", L=N + 60, ulo=W.ua - 5, y0=[list(c) for c in sorted(line)],
                         claim=dict(type='orbit', gen=0, until=40, period=4, ua=W.ua - 5, ub=W.ua + N + 55),
                         text=f"finite line N={N}: gun {g['i']} + train + mirrored end {e['i']} is an oscillator of period 4"))
        json.dump(dict(records=recs), open(a.json, 'w'))
        print(f'  wrote {len(recs)} records to {a.json}')


if __name__ == '__main__':
    main()
