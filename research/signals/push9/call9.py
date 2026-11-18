#!/usr/bin/env python3
"""call9 (push 9): the call line and its protocol, written to objects/call9.json for verify_call9.py.

    python3 call9.py            plays every run on push 8b's stepper (asserting each check), prints the letters at the
                                checked generations and writes objects/call9.json
    python3 call9.py --law      the call for k = 1..40 (push 8b's stepper)

The object: push 8's cell (capL + N units of wire B + capL turned round) and, across it, a capped wire C of 24 units
(the clock's caps, as in push 8b's wires.capped_C) along (1,1,0): the CALL LINE.  The line is placed so that it
crosses the store wire at one unit c ("the crossing"); the pair stands exactly as the two alone (transparent).
  - a stretch d^k f whose first unit is c + 1 stands beside it;
  - pulses of the store wire pass under the line in both directions, and two pulses that stop each other there leave
    their mark d f as on plain wire;
  - TWO right-going pulses of the line in adjacent units (the CALL) pass the crossing and go on unchanged; if the
    stretch's first unit is c + 1 the stretch leaves as exactly k left-going pulses two units apart and the wire is
    left plain; with no stretch there, or with the stretch anywhere else, nothing happens.
States are written as push 8's letters (one hex digit per unit of the store wire) + the line at rest.  Operations:
R@u, L@u = ONE live stator of unit u of the store wire removed ((0,1,2): a right-going pulse; (0,1,4): a left-going
one); CALL = TWO cells of the line's tube made live at one generation, 11 units of the line before the crossing (they
become the pair of pulses).  A check [generation, letters] says that the whole state is capL + those units + the
right cap + the line at rest, cell for cell.
"""
import os, sys, json
import xlab9 as XL
from xlab9 import lab, wires, letters, X, tr, unit, W8

HERE = os.path.dirname(os.path.abspath(__file__))
NR = 12                                    # the line: wire C on its own units -12..11
LINE = XL.Line(nr=NR)
SEED = [(0, 0, 1), (2, -2, 1)]             # made live at an even generation in a unit of wire C: the pair of pulses (own frame, unit 0)
LAUNCH = 11                                # the seed is put LAUNCH line units before the crossing

R_ = lambda i: list(tr(X.RIGHT, 4 + i))    # i = position of the unit among the wire's letters
L_ = lambda i: list(tr(X.LEFT, 4 + i))


def line_cells(c):
    """the line at rest (even generation), crossing at wire position c"""
    return [list(q) for q in lab.up(LINE.cells(4 + c))]


def call_cells(c):
    tt = LINE.tt(4 + c)
    return [list(lab.app(LINE.g, tr(q, LINE.UR - LAUNCH), tt)) for q in SEED]


def state(word, extra):
    N = len(word)
    cells = X.CAPL | X.hexword(word, 4) | frozenset(tr(q, 4 + N) for q in X.CAPR2)
    n = len(cells)
    cells = cells | frozenset(tuple(q) for q in extra)
    assert len(cells) == n + len(extra)
    return cells


def mk(name, text, start, c, ops, checks):
    N = len(start)
    return dict(name=name, text=text, N=N, H=2 * (N + 16 + N % 2), start=start, crossing=c, extra=line_cells(c) if c is not None else [],
                ops=ops, checks=checks)


def runs():
    out = []
    c = 31
    CALL = call_cells(c)
    e = '7' * 50
    s1 = '7' * 32 + 'df' + '7' * 16; s2 = '7' * 32 + 'ddf' + '7' * 15; s3 = '7' * 32 + 'dddf' + '7' * 14
    out.append(mk('cycle', 'the empty cell with the call line across it.  set (two cells removed, 13 and 14 units from the crossing: the two pulses '
                  'stop each other and leave d f just after the crossing), two left-going pulses add one each, CALL: three pulses leave and '
                  'the left cap swallows them; the cell and the line are as at the start.  Then the same again with one pulse added: two pulses leave',
                  e, c,
                  [[0, [R_(18), L_(45)], []], [120, [L_(46)], []], [200, [L_(46)], []], [280, [], CALL],
                   [520, [R_(18), L_(45)], []], [640, [L_(46)], []], [720, [], CALL]],
                  [[0, e], [120, s1], [200, s2], [280, s3], [340, None], [346, None], [520, e], [640, s1], [720, s2], [780, None], [786, None], [960, e], [962, e]]))
    s = '7' * 5 + 'df' + '7' * 25 + 'dddf' + '7' * 14
    out.append(mk('move', 'two stores holding 1 and 3, the call line across the wire one unit before the right one.  CALL: exactly three '
                  'pulses leave the right store and the left store then holds 1 + 3',
                  s, c, [[0, [], CALL]], [[0, s], [60, None], [66, None], [260, '7' * 5 + 'ddddf' + '7' * 41], [262, '7' * 5 + 'ddddf' + '7' * 41]]))
    s = '7' * 36 + 'dddf' + '7' * 10
    out.append(mk('idle', 'the same line with the stretch four units further on, and a CALL: nothing changes (the line calls only a stretch '
                  'that begins one unit after the crossing)',
                  s, c, [[0, [], CALL]], [[0, s], [80, s], [200, s]]))
    out.append(mk('idle-empty', 'a CALL with no stretch on the wire: nothing changes', e, c, [[0, [], CALL]], [[0, e], [80, e], [200, e]]))
    return out


def play(run, show=True):
    N = run['N']; extra = run['extra']
    U = lab.pk(state(run['start'], extra))
    assert lab.same(lab.run(U, 2), U), 'start state is not standing'
    ops = {g: (off, on) for g, off, on in run['ops']}
    G = max(g for g, _ in run['checks'])
    Xs = U
    for g in range(G + 1):
        for chk in run['checks']:
            if chk[0] == g:
                got = letters(Xs, 4, 4 + N)
                if chk[1] is None:
                    chk[1] = got
                assert lab.same(Xs, lab.pk(state(chk[1], extra))), (run['name'], g, got, chk[1])
                if show:
                    print(f"  {run['name']:11s} generation {g:4d}: {X.hexrle(got)}")
        if g in ops:
            off, on = ops[g]
            live = set(lab.up(Xs))
            assert all(tuple(q) in live for q in off) and not any(tuple(q) in live for q in on), (run['name'], g)
            Xs = lab.xor(Xs, lab.pk([tuple(q) for q in off + on]))
        Xs = lab.run(Xs, 1)


def write():
    rs = runs()
    for run in rs:
        play(run)
    d = dict(note="the call line of push 9. Doubled coordinates; unit u = cells with x in {2u, 2u+1}; tr(c, k) = (x + 2k, y, z - 2k). "
                  "A state 'letters' = capL + for each letter i (hex digit h) the stators and the sites of h moved to unit 4 + i + capR moved "
                  "to unit 4 + N + the run's extra cells (the call line at rest at an even generation: a capped wire C of 24 units along "
                  "(1,1,0)). runs[].ops = [generation, cells removed (each must be live), cells made live (each must be dead)]; "
                  "runs[].checks = [generation, letters]: the whole state equals the state of those letters. H = side of the oracle's "
                  "cubic torus. crossing = position among the letters of the unit the line crosses.",
             capL=sorted(map(list, X.CAPL)), capR=sorted(map(list, X.CAPR2)), stators=W8.ST, sites=W8.SITES, runs=rs)
    json.dump(d, open(os.path.join(HERE, 'objects', 'call9.json'), 'w'))
    print('wrote objects/call9.json')


def law(kmax=40):
    ok = True
    for k in range(1, kmax + 1):
        nL = 2 * k + 34; s = '7' * nL + 'd' * k + 'f' + '7' * 8; N = len(s); c = nL - 1
        ex = line_cells(c)
        U = lab.pk(state(s, ex))
        Xs = lab.xor(U, lab.pk([tuple(q) for q in call_cells(c)]))
        Xs = lab.run(Xs, 2 * LAUNCH + 4 * k + 40)
        got = letters(Xs, 4, 4 + N)
        good = lab.same(Xs, lab.pk(state(got, ex))) and got.strip('7') == ('b7' * k)[:-1]
        Xs = lab.run(Xs, 4 * N + 100)
        good &= lab.same(Xs, lab.pk(state('7' * N, ex)))
        ok &= good
        print(f'  k = {k:2d}: exactly {k} pulses two units apart with the line at rest, then the empty cell: {good}')
    print('law holds for k = 1..%d' % kmax if ok else 'LAW FAILS')


if __name__ == '__main__':
    if '--law' in sys.argv:
        law()
    else:
        write()
