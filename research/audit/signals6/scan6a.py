"""A of REVIEW-signals-6: the events of REVIEW-signals-5's scan (scan5.py, 426 per end) that become an up-moving
signal (E or U) on the bare train, and what each of the 741 ends does when they are sent.  Own code (st6, trains6,
frame6); review-5 frame (the train moves towards +v, the end at units >= KS = 6, events at units -10 + g//2, +1).

    python3 scan6a.py bare                  classify the 426 events on the bare train            (~30 s)
    python3 scan6a.py ends [--tmax 160]     run every event that makes E or U against every end   (see output)

Events, built here from scan5.py's description (same order): the eight words (rake cell (1,0,4) removed at
generation 0 from rakes 4, 2, 0, ... below KS); for g = 0..3 and u0 = -10 + g//2, units u0 and u0+1: every
non-empty subset of the live cells of one unit removed, every dead tube cell added, the pair replaced by bare wire.

Bare classification: the event on the plain train of units -A..A, read at G (train5 phase 2) and G+4, G+8 as in
kinds6.read: vanish, a tuple of rigid signals (E, U, H, K0 named by the push's shapes mapped with frame6), or break.

End classification for an event whose bare outcome contains E or U ('up-maker'): the end with the event, and the
undisturbed end, stepped together (Batch on the 3x3 tube inside the planes C <= 39, units -A..15); R(t) = the
difference minus the bare run's up-moving components (as on the bare train, which the script checks on the units
upstream of the end).  'equal' = R(t) empty at some t with every up-moving component at least 6 units upstream of
any cell where the undisturbed run differs from the plain train (then equal for ever, by locality and
prove_echo's argument; see the review); 'dead' = R reaches 20 units upstream of KS; else 'other' (printed).
"""
import sys, json, os, time, argparse
from collections import Counter, defaultdict
from itertools import combinations
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import frame6
import kinds6

T.check()
KS = 6
P5 = (1 + frame6.DELTA) % 4
NAMES5 = {frame6.sig5(k)[1]: k for k in ('E', 'U', 'H', 'K0')}
assert all(frame6.sig5(k)[0] == P5 for k in NAMES5.values())
UP = {'E', 'U'}
SCR = os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals6')


def events():
    ev = []
    pl = T.train5(0, KS - 40, KS)
    rakes = sorted((u for u in range(KS - 40, KS) if tr((1, 0, 4), u) in pl), reverse=True)
    for w in [[0], [1], [2], [3], [0, 1], [0, 1, 2], [0, 2], [0, 2, 4, 6, 8]]:
        ev.append(('word ' + ','.join(map(str, w)), 0, frozenset(tr((1, 0, 4), rakes[i]) for i in w)))
    for g in range(4):
        u0 = -10 + g // 2
        tg = T.train5(g, u0, u0 + 2)
        for u in (u0, u0 + 1):
            live = sorted(c for c in tg if unit_of(c) == u)
            for r in range(1, len(live) + 1):
                for sub in combinations(live, r):
                    ev.append((f'rm g{g} unit{u - u0} {len(sub)}/{len(live)}', g, frozenset(sub)))
            for c in kinds6.tube3(u):
                if c not in tg:
                    ev.append((f'add g{g} unit{u - u0}', g, frozenset([c])))
        wire = frozenset(tr(c, u) for u in (u0, u0 + 1) for c in T.PAT[g % 2][0] if False)  # placeholder
        ev.append((f'wire g{g}', g, None))
    return ev


# bare wire C of scan5 (st5.WIRE), initial data: the two parities
WIRE = [frozenset([(0, 1, 2), (0, 1, 4), (0, 2, 3), (1, 0, 0), (1, 0, 2)]),
        frozenset([(0, 0, 1), (0, 0, 3), (0, 1, 2), (0, 1, 4), (1, 2, 2)])]


def flips_of(e):
    nm, g, fl = e
    if fl is None:
        u0 = -10 + g // 2
        tg = T.train5(g, u0, u0 + 2)
        wire = frozenset(tr(c, u) for u in (u0, u0 + 1) for c in WIRE[g % 2])
        return tg ^ wire
    return fl


def read5(D, G):
    if not D[G]:
        return ('vanish',) if not D[G + 4] and not D[G + 8] else ('break',)
    comps = T.components(D[G]); res = []
    for c in comps:
        ok = None
        for d in (-2, 2):
            if trs(c, d) <= D[G + 4] and trs(c, 2 * d) <= D[G + 8]:
                ok = d
        if ok is None:
            return ('break',)
        res.append((NAMES5.get(T.shape(c), 'new:' + repr(T.shape(c))), ok, c))
    if frozenset().union(*[trs(c, d) for _, d, c in res]) != D[G + 4]:
        return ('break',)
    return tuple(sorted(r[0] for r in res)), res


def run_rows(B, rows_init, gstart, gens, snap_at):
    """rows_init: list of (row index, generation, flip set) applied as xor at that generation to a copy of row 0."""
    pass


def bare(ev, G=102, A=230):
    cells = [c for u in range(-A, A) for c in kinds6.tube3(u)]
    B = st6.Batch(cells)
    S = np.zeros((len(ev) + 1, B.n + 1), np.uint8); S[0] = B.vec(T.train5(0, -A, A))
    snaps = {}
    for t in range(G + 9):
        for j, e in enumerate(ev):
            if e[1] == t:
                fl = flips_of(e)
                assert all(c in B.idx for c in fl)
                S[j + 1] = S[0] ^ B.vec(fl)
            elif e[1] > t:
                S[j + 1] = S[0]
        if t in (G, G + 4, G + 8):
            snaps[t] = S.copy()
        S = B.step(S)
    out = []
    for j in range(len(ev)):
        D = {t: B.set_of(snaps[t][j + 1] ^ snaps[t][0]) for t in snaps}
        if not all(-A + t + 1 <= unit_of(c) < A - t - 1 for t in D for c in D[t]):
            out.append((('break', 'wide'), None)); continue
        r = read5(D, G)
        out.append(r if isinstance(r[0], tuple) else (r, None))
    return out


def main_bare():
    t0 = time.time()
    ev = events()
    assert len(ev) == 426, len(ev)
    res = bare(ev)
    cnt = Counter((e[0].split(' ')[0], r[0]) for e, r in zip(ev, res))
    for k, v in sorted(cnt.items()):
        print(f'  {k[0]:5s} {str(k[1]):40s} {v}')
    ups = [(j, e[0], e[1], r[0]) for j, (e, r) in enumerate(zip(ev, res)) if any(x in UP for x in r[0])]
    print(len(ups), 'events make an up-moving signal:')
    for u in ups:
        print('   ', u)
    json.dump(dict(ev=[[e[0], e[1], sorted(map(list, flips_of(e)))] for e in ev], res=[list(r[0]) for r in res]),
              open(os.path.join(SCR, 'bare6.json'), 'w'))
    print(f'{time.time() - t0:.0f} s')


if __name__ == '__main__':
    if sys.argv[1] == 'bare':
        main_bare()


def main_ends(tcheck=42, ua=-100, C=39, chunk=40):
    t0 = time.time()
    ev = events()
    bres = bare(ev)
    upj = [j for j, r in enumerate(bres) if any(x in UP for x in r[0])]
    ends = json.load(open(os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals5', 'ends.json')))['ends']
    assert len(ends) == 741
    cells = [c for u in range(ua, 16) for c in kinds6.tube3(u) if c[0] + c[1] - c[2] <= C and c[0] - c[1] - c[2] <= C]
    B = st6.Batch(cells)
    # bare-train differences of the up-makers at tcheck, on the same piece with no end (planes far: same cells,
    # the plain train to unit 15; exact on units ua+t+1 .. 15-t-1, which holds the signal)
    Sb = np.zeros((len(upj) + 1, B.n + 1), np.uint8); Sb[0] = B.vec(T.train5(0, ua, 16) & frozenset(B.cells))
    for t in range(tcheck + 1):
        for i, j in enumerate(upj):
            if ev[j][1] == t:
                Sb[i + 1] = Sb[0] ^ B.vec(flips_of(ev[j]))
            elif ev[j][1] > t:
                Sb[i + 1] = Sb[0]
        if t < tcheck:
            Sb = B.step(Sb)
    Dbare = [B.set_of(Sb[i + 1] ^ Sb[0]) for i in range(len(upj))]
    for i, d in enumerate(Dbare):
        r = bres[upj[i]][1]
        assert len(r) == 1 and d and all(ua + tcheck + 1 <= unit_of(c) <= -20 for c in d), (i, sorted(d))
        assert T.shape(d) == T.shape(r[0][2]), 'bare signal at tcheck is not the signal read at G'
    out = Counter(); bad = []
    for e0 in range(0, len(ends), chunk):
        es = ends[e0:e0 + chunk]
        R = len(upj) + 1
        S = np.zeros((len(es) * R, B.n + 1), np.uint8)
        for k, e in enumerate(es):
            cap = frozenset(tuple(c) for c in e['cap'])
            S[k * R:(k + 1) * R] = B.vec((T.train5(0, ua, KS) | cap))
        # undisturbed rows: check the end leaves units < KS as the plain train (t = 0..3, then periodic)
        for t in range(tcheck + 1):
            for k in range(len(es)):
                for i, j in enumerate(upj):
                    if ev[j][1] == t:
                        S[k * R + i + 1] = S[k * R] ^ B.vec(flips_of(ev[j]))
                    elif ev[j][1] > t:
                        S[k * R + i + 1] = S[k * R]
            if t < 4:
                for k in range(len(es)):
                    st = B.set_of(S[k * R])
                    assert units(st, ua + t + 1, KS) == units(T.train5(t, ua, KS), ua + t + 1, KS), ('end disturbs train', e0 + k)
            if t < tcheck:
                S = B.step(S)
        for k in range(len(es)):
            # undisturbed end: its non-train cells at tcheck (units >= ?)
            st = B.set_of(S[k * R])
            far = min(unit_of(c) for c in st ^ (T.train5(tcheck, ua, 16) & frozenset(B.cells)) if unit_of(c) > ua + tcheck + 2)
            assert far >= KS - 1, far
            for i, j in enumerate(upj):
                d = B.set_of(S[k * R + i + 1] ^ S[k * R])
                if d == Dbare[i] and max(unit_of(c) for c in d) <= far - 6:
                    out['equal'] += 1
                else:
                    out['other'] += 1; bad.append((e0 + k, ev[j][0]))
        print(f'{e0 + len(es)}/741 ends, {dict(out)}, {time.time() - t0:.0f} s', flush=True)
    print('RESULT', len(upj), 'up-making events x', len(ends), 'ends:', dict(out))
    print('rows not equal:', bad[:30])


if __name__ == '__main__' and sys.argv[1] == 'ends':
    main_ends()
