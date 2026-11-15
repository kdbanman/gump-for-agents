"""B of REVIEW-signals-6: what small changes of the plain rake train become (own stepper st6.Batch, push frame).

    python3 kinds6.py one            the 112 one-cell flips of the 3x3 tube, units 0,1, phases 0..3   (~20 s)
    python3 kinds6.py two            every two-cell flip inside units 0,1 of the tube (1,512 events)    (~2 min)
    python3 kinds6.py two3           every two-cell flip with the cells in units {0,1} x {2,3}... (pairs one or
                                     two units apart: units 0..3, one cell in 0,1)                       (~4 min)
    python3 kinds6.py wide           one-cell flips of the cells of the wider tube -3 <= x+y+z, x-y+z <= 9 that
                                     are outside the 3x3 tube, units 0,1, phases 0..3                    (~2 min)

Each event: the state train(f) with the cells flipped, at generation f, stepped to generation G (G = 1 mod 4) and
G+4, G+8 on a finite piece of units -A..A (exact on units -A+t+1 .. A-t-1, asserted for the difference).  Outcome:
'vanish' (no difference at G), a list of rigid components (each cluster of the difference, separated by >= 4 empty
units, equal at G+4 and G+8 to itself moved by d units per 4 generations, d in {-2, +2}; named E/U/H/K0 when its
shape at phase 1 equals that signal, else 'new:<shape>'), or 'break' (anything else).
"""
import sys, json, os, time
from collections import Counter, defaultdict
from itertools import combinations
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T

T.check()
NAMES = {(T.SIG[k][0], tuple(sorted(T.SIG[k][1]))): k for k in T.SIG}
# the review-5 signal K3 (two cells), in the push frame (frame6 maps it): (0,0,3) of an even unit u, (0,0,5) of u+2
ATOMS = {k: (T.SIG[k][0], frozenset(T.SIG[k][1]), 2 * T.SIG[k][2] if k in ('E', 'U') else -2) for k in T.SIG}
ATOMS['K3'] = (0, frozenset([(0, 0, 3), (4, 0, 1)]), -2)
NAMES[(0, ((0, 0, 3), (4, 0, 1)))] = 'K3'


def cover(c, d):
    """Exact cover of a rigid component c (moving d units per 4 generations, read at phase 1) by atoms of that
    direction; returns the list of names or None."""
    c = set(c)
    if not c:
        return []
    q = min(c)
    for k, (par, cells, dd) in ATOMS.items():
        if dd != d:
            continue
        for a in cells:
            # place atom so that its cell a lands on q
            du = (q[0] - a[0]) // 2
            if (q[0] - a[0]) % 2 or du % 2 != par:
                continue
            pl = trs(cells, du)
            if q in pl and pl <= c:
                r = cover(c - pl, d)
                if r is not None:
                    return [k] + r
    return None


def classify_runs(events, G=101, A=170, lo=-3, hi=9):
    cells = [c for u in range(-A, A) for c in _tube_unit(u, lo, hi)]
    B = st6.Batch(cells)
    S = np.zeros((len(events) + 1, B.n + 1), np.uint8)
    t0 = 0
    S[0] = B.vec(T.train(0, -A, A))
    snaps = {}
    pend = defaultdict(list)
    for j, (f, flip) in enumerate(events):
        pend[f].append((j, flip))
    for t in range(G + 9):
        for j, flip in pend.get(t, []):
            assert B.set_of(S[0]) >= units(T.train(t, -A, A), -A + t + 2, A - t - 2)
            S[j + 1] = S[0] ^ B.vec(frozenset(flip))
        if t in (G, G + 4, G + 8):
            snaps[t] = S.copy()
        S = B.step(S)
        # rows not yet started are reset at their start generation; keep them equal to the plain row meanwhile
        for f in pend:
            if f > t + 1:
                for j, _ in pend[f]:
                    S[j + 1] = S[0]
    assert G % 4 == 1
    out = []
    for j in range(len(events)):
        D = {}
        for t in (G, G + 4, G + 8):
            d = B.set_of(snaps[t][j + 1] ^ snaps[t][0])
            D[t] = d
        if not all(-A + t + 1 <= unit_of(c) < A - t - 1 for t in D for c in D[t]):
            out.append(('break', 'wide'))     # the difference spans more than ~2A - 2G units: grown, not a signal
            continue
        out.append(read(D, G))
    return out


def read(D, G):
    if not D[G]:
        return ('vanish',) if not D[G + 4] and not D[G + 8] else ('break',)
    comps = T.components(D[G])
    res = []
    for c in comps:
        ok = None
        for d in (-2, 2):
            if trs(c, d) <= D[G + 4] and trs(c, 2 * d) <= D[G + 8]:
                ok = d
        if ok is None:
            return ('break',)
        sh = T.shape(c)
        cv = cover(c, ok)
        if cv is None:
            res.append(('new:' + repr(sh) + f' d{ok:+d}', min(unit_of(q) for q in c), ok))
        else:
            res += [(k, 0, ok) for k in cv]
    # the moved components must account for the whole difference
    if frozenset().union(*[trs(c, r[2]) for c, r in zip(comps, res)]) != D[G + 4]:
        return ('break',)
    return tuple(sorted(r[0] for r in res))


_TU = {}


def _tube_unit(u, lo, hi):
    if (lo, hi) not in _TU:
        out = []
        for x in (0, 1):
            for y in range(-14, 15):
                for z in range(-16, 17):
                    c = (x, y, z)
                    if st6.is_cell(c) and lo <= c[0] + c[1] + c[2] <= hi and lo <= c[0] - c[1] + c[2] <= hi:
                        out.append(c)
        _TU[(lo, hi)] = out
    return [tr(c, u) for c in _TU[(lo, hi)]]


def tube3(u):
    return _tube_unit(u, 1, 5)


def main(mode):
    t0 = time.time()
    if mode == 'one':
        ev = [(f, [c]) for f in range(4) for u in (0, 1) for c in tube3(u)]
        kw = dict(lo=1, hi=5)
    elif mode == 'two':
        cs = tube3(0) + tube3(1)
        ev = [(f, list(p)) for f in range(4) for p in combinations(cs, 2)]
        kw = dict(lo=1, hi=5)
    elif mode == 'two3':
        a = tube3(0) + tube3(1); b = tube3(2) + tube3(3)
        ev = [(f, [p, q]) for f in range(4) for p in a for q in b]
        kw = dict(lo=1, hi=5)
    elif mode == 'wide':
        cs = [c for u in (0, 1) for c in _tube_unit(u, -3, 9) if not st6.in_tube(c)]
        ev = [(f, [c]) for f in range(4) for c in cs]
        kw = dict(lo=-3, hi=9, A=230, G=101)
    print(mode, len(ev), 'events', flush=True)
    res = []
    CH = 800
    for i in range(0, len(ev), CH):
        res += classify_runs(ev[i:i + CH], **kw)
    cnt = Counter(res)
    for k, v in sorted(cnt.items(), key=lambda x: -x[1]):
        print(f'  {v:6d}  {k}')
    news = [(e, r) for e, r in zip(ev, res) if any(str(x).startswith('new') for x in r)]
    for e, r in news[:20]:
        print('  NEW', e, r)
    # which events make each single kind (one-cell mode): per (phase, add/remove)
    if mode == 'one':
        for k in ('E', 'U', 'H', 'K0'):
            ex = [(f, c, 'remove' if c in T.train(f, -3, 4) else 'add') for (f, cl), r in zip(ev, res) for c in cl if r == (k,)]
            print(' ', k, len(ex), ex[:8])
    json.dump([[e[0], [list(c) for c in e[1]], list(map(str, r))] for e, r in zip(ev, res)],
              open(os.path.join(st6.ROOT, 'research', 'scratch', 'audit', 'signals6', f'kinds6_{mode}.json'), 'w'))
    print(f'{time.time() - t0:.0f} s')


if __name__ == '__main__':
    main(sys.argv[1])
