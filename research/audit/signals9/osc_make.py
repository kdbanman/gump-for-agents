#!/usr/bin/env python3
"""osc_make (review of signals push 9): writes objects/osc-call-P3.15f.json, the clocked call on the store's own wire
with the period-3 oscillator P3.15f at the wall.  Every run is played with st9.c and every check asserted before the
file is written; verify_osc9.py then judges the file with reference/oracle.py alone.

    python3 osc_make.py

Placement: PERMS[14] (the signed permutation (x, y, z) -> (y, -x, z)... see `G`), translation (0, 2, 10), slid along the
wire so that the largest x of the oscillator's union is in unit WALL; the stretch's first unit is WALL.
Timing rule for a right-going pulse born by removing the stator (0,1,2) of unit u at an even generation g, the
oscillator being at its phase 0 at generation 0:   (g + u) = (WALL + 2) mod 3.
"""
import sys, json
sys.argv = sys.argv[:1]
from a9 import *
import osc9
from osc9 import orbit_of, placements, Case

GI, TT = 14, (0, 2, 10)
N, FIRST, WALL = 64, 0, 30
G = PERMS[GI]


def W(stores=(), pulses=()):
    w = list('7' * N)
    for u, k in stores:
        for j in range(k):
            w[u + j - FIRST] = 'd'
        w[u + k - FIRST] = 'f'
    for u in pulses:
        w[u - FIRST] = 'b'
    return ''.join(w)


def ok_time(g, u):
    return g % 2 == 0 and (g + u) % 3 == (WALL + 2) % 3


OSC = []          # the oscillator's part of the standing pair (plain wire + oscillator) at generations 0, 2, 4 (mod 6)


def play(cs, start_word, ops, T, want):
    """ops {generation: [cells]}; want {generation: letters}.  Asserts each `want`, returns the checks as a list."""
    s = wire(start_word, first=FIRST) | cs.obj0
    assert len(s) == len(wire(start_word, first=FIRST)) + len(cs.obj0)
    for t in range(T + 1):
        if t in want:
            assert t % 2 == 0
            ob = OSC[(t // 2) % 3]
            assert s == wire(want[t], first=FIRST) | ob, (t, rle(letters(s - ob, N, FIRST)), rle(want[t]))
        if t in ops:
            assert set(ops[t]) <= s
            s = s - set(ops[t])
        s = run(s, 1)
    return [[t, want[t]] for t in sorted(want)]


def main():
    orb, P = orbit_of('P3.15f')
    pl = {(gi, t): (pc, un) for gi, t, pc, un in placements(orb)}
    pc, un = pl[(GI, TT)]
    osc9.U0 = WALL
    cs = Case(pc, un, P)
    assert max(q[0] for q in cs.orb_un) >> 1 == WALL
    pw = wire('7' * N, first=FIRST); st = pw | cs.obj0
    for i in range(3):
        assert pw <= st
        OSC.append(st - pw); st = run(st, 2)
    assert st == pw | cs.obj0
    print('the oscillator beside the wire at generations 0, 2, 4:', [len(x) for x in OSC], '; free:', [len(cs.orb[i]) for i in (0, 2, 1)],
          '; missing from the free orbit at generation 2:', sorted(cs.orb[2] - OSC[1]), 'extra:', sorted(OSC[1] - cs.orb[2]))
    runs = []

    def add(name, text, start, ops, T, want):
        for g, cells in ops.items():
            for q in cells:
                u = q[0] >> 1
                if q == RST(u):
                    assert ok_time(g, u), (name, g, u)
        runs.append({'name': name, 'text': text, 'start': start, 'ops': [[g, [list(q) for q in cells]] for g, cells in sorted(ops.items())],
                     'checks': play(cs, start, ops, T, want), 'T': T})

    e = W()
    # 1 pass: the empty wire lets pulses through, right-going at the allowed timing, left-going at all three
    add('pass', 'the empty wire with the oscillator: a right-going pulse born at an allowed (place, generation) passes the oscillator; '
        'left-going pulses pass it at all three timings; each time everything is afterwards as it would have been',
        e, {0: [RST(17)], 180: [LST(44)], 360: [LST(45)], 540: [LST(46)]}, 720,
        {0: e, 60: e[:46] + '6f' + e[48:], 174: e, 354: e, 534: e, 714: e, 720: e})
    # 2 cycle: set, add, add, call (3 out), set, add, call (2 out), a pulse through the empty wire
    lead = lambda t, s: WALL + 2 - (t - s - 28) // 2          # the leading released pulse, call born at s 13 units before the wall
    def train(t, s, k):
        return W(pulses=[lead(t, s) + 2 * j for j in range(k)])
    add('cycle', 'set (two pulses stop each other at the wall, the right-going one having passed the oscillator), add, add, CALL by ONE '
        'right-going pulse born 13 units before the wall at an allowed generation: exactly three pulses leave, the wire is plain, '
        'the oscillator is as it would have been; set again, add, CALL from another allowed place: two pulses leave',
        e, {0: [RST(17), LST(44)], 120: [LST(44)], 180: [LST(44)], 300: [RST(17)], 480: [RST(20), LST(41)], 600: [LST(43)],
            720: [RST(14)]}, 960,
        {0: e, 114: W([(WALL, 1)]), 174: W([(WALL, 2)]), 294: W([(WALL, 3)]), 342: train(342, 300, 3), 348: train(348, 300, 3),
         474: e, 594: W([(WALL, 1)]), 714: W([(WALL, 2)]), 768: train(768, 726, 2), 774: train(774, 726, 2), 954: e, 960: e})
    # 3 law: k = 1..10
    for k in range(1, 11):
        add(f'law-{k}', f'a store holding {k} with the oscillator at its wall and ONE right-going pulse: exactly {k} pulses leave',
            W([(WALL, k)]), {0: [RST(17)]}, 300,
            {0: W([(WALL, k)]), 2 * k + 34: train(2 * k + 34, 0, k), 2 * k + 36: train(2 * k + 36, 0, k), 294: e, 300: e})
    # 4 move: a second store on the left catches the count exactly
    add('move', 'stores holding 2 (plain, on the left) and 3 (with the oscillator at its wall); ONE cell removed between them at an '
        'allowed place and generation: the left store then holds exactly 2 + 3',
        W([(5, 2), (WALL, 3)]), {0: [RST(17)]}, 300, {0: W([(5, 2), (WALL, 3)]), 294: W([(5, 5)]), 300: W([(5, 5)])})
    # 5 branch: the same pulse sent from the left of a place where a second store may stand
    add('branch-empty', 'no store at units 12..14: ONE right-going pulse born at unit 2 passes that place, reaches the oscillator '
        'at the allowed timing and releases the store at the wall: exactly three pulses leave, the wire is empty',
        W([(WALL, 3)]), {0: [RST(2)]}, 330,
        {0: W([(WALL, 3)]), 70: train(70, 30, 3), 72: train(72, 30, 3), 324: e, 330: e})
    add('branch-full', 'a store holding 2 at units 12..14: the same pulse is absorbed by it (it then holds 3, its wall one unit '
        'to the left) and the store at the oscillator is not released',
        W([(12, 2), (WALL, 3)]), {0: [RST(2)]}, 300,
        {0: W([(12, 2), (WALL, 3)]), 120: W([(11, 3), (WALL, 3)]), 300: W([(11, 3), (WALL, 3)])})
    d = {'note': 'A call on the store\'s own wire by ONE pulse, with the period-3 oscillator P3.15f of research/atlas/catalogue.jsonl '
         'beside the wire at the wall (review of signals push 9).  Doubled coordinates; unit u = cells with x in {2u, 2u+1}; '
         'tr(c, k) = (x + 2k, y, z - 2k).  A state `letters` at generation t = capL moved to unit first - 4 + for each letter i '
         '(hex digit h) the stators and the sites of h moved to unit first + i + capR moved to unit first + N + osc_even[(t/2) mod 3], t even '
         '(the oscillator\'s part of the standing pair plain wire + oscillator at generations 0, 2, 4: the pair is a junction, one cell of '
         'the free oscillator is absent at generations = 2 mod 3; osc_free = the free orbit, phases 0, 1, 2).  '
         'runs[].ops = [generation, cells removed (each must be live)]; runs[].checks = [generation, letters]: the whole state '
         'equals the state of those letters.  Allowed for a right-going pulse (stator (0,1,2) of unit u removed at even generation g): '
         '(g + u) mod 3 = (wall + 2) mod 3.',
         'capL': sorted(map(list, CAPL)), 'capR': sorted(map(list, CAPR)), 'stators': [list(q) for q in STATORS],
         'sites': [list(q) for q in SITES], 'N': N, 'first': FIRST, 'wall': WALL,
         'placement': {'catalogue_id': 'P3.15f', 'perm': list(G[0]), 'signs': list(G[1]), 'translation': list(TT)},
         'osc_even': [sorted(map(list, x)) for x in OSC], 'osc_free': [sorted(map(list, cs.orb[i])) for i in range(3)], 'runs': runs}
    os.makedirs(os.path.join(HERE, 'objects'), exist_ok=True)
    json.dump(d, open(os.path.join(HERE, 'objects', 'osc-call-P3.15f.json'), 'w'))
    print(f'written: {len(runs)} runs')


if __name__ == '__main__':
    main()
