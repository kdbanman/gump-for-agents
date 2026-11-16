#!/usr/bin/env python3
"""The echo meeting a word of holes on the line itself (README section 34): what is left at the end.

    python3 record6.py [N]        (about 1 min; sg.step_set)

The line of N units (default 40) in its cycle, at a generation where units 2..30 are at train phase 1: E at unit 4
and n = 0..4 holes at units 21, 27, 33, 41 (n of them) xored in.  After G = 6N + 200 generations the state is
printed unit by unit as: '-' empty, 'B' wire B (either parity), 'b' wire B' (B with (1,0,2) off and (0,2,3) on at
wire B's generation 0; either parity), 'C' bare wire C, 'T' the rake train, '?' anything else; with the period of
the whole state (up to 40) and whether the final states for different n differ.
"""
import sys
import echo6 as E, sg

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
WB = [frozenset([(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)]), frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)])]
WBp0 = (WB[0] - {(1, 0, 2)}) | {(0, 2, 3)}
WBp = [WBp0, None]
WC = [frozenset(E.UNIT), None]


def letters(S):
    s = ''
    for u in range(-4, N + 3):
        b = frozenset(E.tr(c, -u) for c in E.units(S, u, u + 1))
        if not b:
            s += '-'
        elif b in WB:
            s += 'B'
        elif b == WBp0 or b == WBp[1]:
            s += 'b'
        elif b in WC[:1] or b == WC[1]:
            s += 'C'
        elif any(b == E.BASE[f][p] for f in range(4) for p in (0, 1)):
            s += 'T'
        else:
            s += '?'
    return s


WBp[1] = frozenset(E.tr(c, -0) for c in E.units(sg.step_set(frozenset(E.tr(c, k) for k in range(-6, 7) for c in WBp0)), 0, 1))
WC[1] = frozenset(E.tr(c, -0) for c in E.units(sg.step_set(frozenset(E.tr(c, k) for k in range(-6, 7) for c in E.UNIT)), 0, 1))
X0 = E.run(E.line_object(N), 2 * N + 8)
while E.phase_at(X0, 2, 30) != 1:
    X0 = sg.step_set(X0)
finals = []
holes = [21, 27, 33, 41]
for n in range(0, 5):
    S = X0 ^ E.sig('E', 4)
    for u in holes[:n]:
        S = S ^ E.sig('H', u)
    G = 6 * N + 200
    S = E.run(S, 80)
    print(f'E and {n} holes: generation 80: {letters(S)}', flush=True)
    S = E.run(S, G - 80)
    hist = [S]
    for _ in range(40):
        hist.append(sg.step_set(hist[-1]))
    per = next((p for p in range(1, 41) if hist[p] == hist[0]), None)
    finals.append(hist[0])
    print(f'E and {n} holes: after {G} generations {len(S)} cells, period {per}: {letters(S)}', flush=True)
print('final states pairwise different:', len(set(finals)) == len(finals))
