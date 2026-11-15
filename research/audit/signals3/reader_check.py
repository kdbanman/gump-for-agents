"""Claim 1 (README section 15): capL of the clock eats every word of the B/C tape; census of left caps.

    python3 reader_check.py local            the 2^6 local checks on gs AND on the oracle, for capL
    python3 reader_check.py census C [--max M] [--closure]   left caps from scratch/signals/table_28_C.json

The argument re-derived (review section 1): with X(0) = capL + an infinite word w on units >= 0, it suffices that
for every w, step^2(capL + w) = capL + (w moved one unit towards -v).  Units >= 2 of step^2 depend only on units
>= 0, which are pure tape, so the tape theorem gives them.  Units <= 1 of step^2 depend only on units <= 3, i.e.
on capL and w[0..3]: 16 cases.  Here every word of 6 letters (units 0..5) is checked on units <= 3 (64 cases),
then C on units 6..13 and capR at unit 14 (felt by units <= 3 only after 5 generations).
census: each right cap R of the table (first unit 0) -> left cap = mirror of (wire C + R) one generation on,
re-anchored so wire C sits on units >= 0; capR0 must give capL exactly.  'sink' = the 16-case check passes
(that is the whole of prove_reader's 16-state automaton).  --closure: for non-sinks, close the set of states
(units <= 3 at even generations) under 2 more letters, and report 'disturbs' (units 4, 5 not the pure tape after
2 generations for some reachable state and letters) or 'memory' (closed, never disturbs, more than 16 states).
"""
import itertools, json, os, sys
import numpy as np
import r3
from r3 import tr, unit, uc
SCR = os.path.join(r3.gs.ROOT, 'research', 'scratch', 'signals')
capR14 = frozenset(tr(c, 14) for c in r3.capR0)


def tail(a, b):
    return set().union(*[uc('C', u) for u in range(a, b)]) if b > a else set()


def batch_check(cap, words, U):
    """cap (units < 0) + each word on units 0..len-1, C, capR far; step 2; return list of units<=U results."""
    n = len(words[0])
    allsites = set().union(*[uc(0xf, u) for u in range(n)])
    base = set(cap) | tail(n, 14) | capR14
    run = r3.Run(base, extra=allsites)
    X = np.stack([run.D.state(base | r3.word_cells(w)) for w in words])
    Y = run.D.step(run.D.step(X))
    return [frozenset(c for c in run.D.cells_of(y) if unit(c) <= U) for y in Y], run


def local():
    words = [''.join(p) for p in itertools.product('BC', repeat=6)]
    got, run = batch_check(r3.capL, words, 3)
    bad = 0
    for w, g in zip(words, got):
        want = frozenset(c for c in (r3.capL | r3.word_cells(w[1:5])) if unit(c) <= 3)
        bad += g != want
    print(f'gs: {len(words)} words of 6 letters, units <= 3 after 2 generations = capL + word moved: {len(words) - bad} pass')
    badO = 0
    for w in words:
        start = set(r3.capL) | r3.word_cells(w) | tail(6, 14) | capR14
        for t, s in r3.oracle_run(start, 2):
            pass
        want = frozenset(c for c in (r3.capL | r3.word_cells(w[1:5])) if unit(c) <= 3)
        badO += frozenset(c for c in s if unit(c) <= 3) != want
    print(f'oracle: the same 64: {64 - badO} pass')
    return bad == 0 and badO == 0


def left_from_right(R):
    x = set(R) | tail(-30, 0)
    y = r3.Run(x).step(1).cells()
    z = frozenset(r3.MIRROR(c) for c in y)
    ref = frozenset(uc('C', 0))
    # find shift putting a pure C unit far from the cap: the image of units -20..-10 of the wire
    for s in range(-60, 60):
        zz = frozenset(tr(c, s) for c in z)
        if all(frozenset(tr(c, -u) for c in zz if unit(c) == u) == ref for u in range(8, 16)):
            break
    else:
        return None
    b = 16
    while b > -30 and frozenset(tr(c, -(b - 1)) for c in zz if unit(c) == b - 1) == ref:
        b -= 1
    return frozenset(tr(c, -b) for c in zz if unit(c) < b)


def closure(cap, U=3, limit=3000):
    """States = cells of units <= U at even generations, starting from cap + every word on 0..U."""
    S = set(); todo = []
    for w in itertools.product('BC', repeat=U + 1):
        s = frozenset(cap | r3.word_cells(''.join(w)))
        if s not in S:
            S.add(s); todo.append(s)
    while todo:
        s = todo.pop()
        words = [''.join(p) for p in itertools.product('BC', repeat=2)]
        allsites = set().union(*[uc(0xf, u) for u in range(U + 1, U + 3)])
        base = set(s) | tail(U + 1, U + 10) | {tr(c, U + 10) for c in r3.capR0}
        base_noword = set(s) | tail(U + 3, U + 10) | {tr(c, U + 10) for c in r3.capR0}
        run = r3.Run(base, extra=allsites | {(x, y, z) for (x, y, z) in s})
        X = np.stack([run.D.state(base_noword | r3.word_cells(w, U + 1)) for w in words])
        Y = run.D.step(run.D.step(X))
        for w, y in zip(words, Y):
            c2 = run.D.cells_of(y)
            want = frozenset(r3.word_cells(w[1] + 'C', U + 1))
            if frozenset(c for c in c2 if U + 1 <= unit(c) <= U + 2) != want:
                return 'disturbs', len(S)
            s2 = frozenset(c for c in c2 if unit(c) <= U)
            if s2 not in S:
                S.add(s2); todo.append(s2)
                if len(S) > limit:
                    return 'big', len(S)
    return ('sink' if len(S) == 2 ** (U + 1) else 'memory'), len(S)


def census(C, mx, do_closure):
    D = json.load(open(os.path.join(SCR, f'table_28_{C}.json')))
    sinks = nons = fail = 0; cl = {}
    found_capR = False
    for sid, st in list(D['states'].items())[:mx]:
        R = frozenset(map(tuple, st))
        if not R:
            continue
        found_capR |= R == r3.capR0
        L = left_from_right(R)
        if L is None:
            fail += 1; continue
        if R == r3.capR0:
            print('capR0 -> mirror left cap equals clock capL:', L == r3.capL)
        words = [''.join(p) for p in itertools.product('BC', repeat=6)]
        got, _ = batch_check(L, words, 3)
        ok = all(g == frozenset(c for c in (L | r3.word_cells(w[1:5])) if unit(c) <= 3) for w, g in zip(words, got))
        if ok:
            sinks += 1
        else:
            nons += 1
            if do_closure:
                r, n = closure(L)
                cl[r] = cl.get(r, 0) + 1
                if r != 'disturbs':
                    print('  non-sink', sid, r, n)
    print(f'C = {C}: sinks {sinks}, not sinks {nons}, could not anchor {fail}; capR0 in table: {found_capR}; closure of non-sinks: {cl}')


if __name__ == '__main__':
    if sys.argv[1] == 'local':
        print('ALL PASS' if local() else 'FAIL')
    else:
        a = sys.argv[2:]
        mx = int(a[a.index('--max') + 1]) if '--max' in a else 10 ** 9
        census(int(a[0]), mx, '--closure' in a)
