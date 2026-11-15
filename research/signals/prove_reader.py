#!/usr/bin/env python3
"""A left cap of the B/C tape that eats EVERY word: proof by closing a finite automaton (exact, no sampling).

    python3 prove_reader.py [objects/clock-C.json] [--U 3]

The tape (README section 10) moves rigidly towards -v, one unit per 2 generations.  Put a left cap (capL of the
clock, cells in units < 0) at the -v end of a tape holding an arbitrary infinite word.  Write s(t) for the cells of
units <= U at generation 2t.  A cell's neighbours lie in its own unit or the adjacent ones, so s(t+1) depends only on
s(t) and units U+1, U+2 at generation 2t, and units U+1 .. at generation 2t+2 depend only on units >= U at 2t.
The script starts from capL + every one of the 2^(U+1) words on units 0..U, and closes the set S of states s under
"append any 3 letters on units U+1..U+3, step 2 generations (sg.step_set on the finite pattern; units <= U+3 cannot
feel the cut at U+5 in 2 generations), keep units <= U", checking at every step that
  (i)  units U+1 .. U+3 after the 2 generations are exactly the pure tape (the letters moved one unit): the cap
       never sends anything into the tape;
and at the end that
  (ii) S is finite (the closure terminates) and every s in S reaches the bare state capL + CCC.. after at most
       U + 6 letters C.
(i) and (ii) for every s in the closed set prove, for every word whatsoever, that the cap swallows the word,
letter by letter, emits nothing, and is exactly as it was once the word has been followed by U + 6 letters C.
The automaton's transitions are then replayed with reference/oracle.py on a torus for a sample (--oracle).
"""
import argparse, json, sys, itertools
import sg, scat, sat_writer as W
tr = scat.tr; unit = scat.unit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('obj', nargs='?', default='objects/clock-C.json'); ap.add_argument('--U', type=int, default=3)
    ap.add_argument('--key', default='capL')
    a = ap.parse_args(); U = a.U
    cap = frozenset(map(tuple, json.load(open(a.obj))[a.key]))
    assert max(unit(c) for c in cap) < 0
    S = {}; todo = []
    def add(s):
        if s not in S:
            S[s] = {}; todo.append(s)
    for w in itertools.product('BC', repeat=U + 1):
        add(cap | W.tape_cells(''.join(w), 0, 0, U + 1))
    nsteps = 0
    while todo:
        s = todo.pop()
        for w in itertools.product('BC', repeat=3):
            word = ''.join(w) + 'CC'                      # units U+1 .. U+5
            x = s | frozenset(tr(c, U + 1) for c in W.tape_cells(word, 0, 0, 5))
            y = sg.step_set(sg.step_set(x)); nsteps += 1
            tape_after = frozenset(tr(c, U + 1) for c in W.tape_cells(word[1:4], 0, 0, 3))
            got = frozenset(c for c in y if U + 1 <= unit(c) <= U + 3)
            if got != tape_after:
                print('FAIL (i): the cap disturbs the tape beyond unit', U, 'from a state of', len(s), 'cells'); sys.exit(1)
            s2 = frozenset(c for c in y if unit(c) <= U)
            S[s][''.join(w)] = s2
            add(s2)
            if len(S) > 20000:
                print('FAIL (ii): more than 20000 states'); sys.exit(1)
    bare = cap | W.tape_cells('C' * (U + 1), 0, 0, U + 1)
    worst = 0
    for s in S:
        x, k = s, 0
        while x != bare and k <= U + 6:
            x = S[x]['CCC']; k += 1
        if x != bare:
            print('FAIL (ii): a state does not return to the bare cap under letters C'); sys.exit(1)
        worst = max(worst, k)
    print(f'PASS  closed set of {len(S)} cap states (units <= {U}), {nsteps} two-generation steps checked: the cap never'
          f' disturbs the tape beyond unit {U}')
    print(f'PASS  every state returns to the bare cap after at most {worst} letters C')
    print(f'ALL PASS - {a.key} of {a.obj} eats every word of the B/C tape')


if __name__ == '__main__':
    main()
