#!/usr/bin/env python3
"""Census of the left ends of the B/C tape: what every left cap of wire C does with an arbitrary word.

    python3 readers.py TABLE.json [--U 3] [--max M]

Left caps are made from the right caps of a scatter table (scatter_table.py, wire C; its `states`) by the mirror
of the clock: (x,y,z) -> (z-4, y, x+4) maps wire C at one generation onto wire C at the next, reversed, so the image
of (wire + right cap) one generation on is (left cap + wire) at an even generation (this is how capL of the clock
was made).  Each left cap is then classified exactly, by the automaton of prove_reader.py (all words at once):
  sink      the cap state never leaves capL + pure tape: at every even generation the state is the cap and the
            tape moved on; the cap eats every word and remembers nothing (capL of the clock is one)
  memory    the closed set of cap states is larger: the cap is changed by what it eats, but it never disturbs the
            tape and the set is finite (a reader with a finite memory; how many states, and whether all return
            to the bare cap under letters C, is printed)
  emits     for some word the cap disturbs the tape beyond unit U (it sends something back, or burns)
  big       more than --limit states
Stepping: sg.step_set on finite patterns, light-cone exact as argued in prove_reader.py.
"""
import argparse, itertools, json
from collections import Counter
import sg, scat, sat_writer as W
tr = scat.tr; unit = scat.unit
M = lambda c: (c[2] - 4, c[1], c[0] + 4)


def left_cap_from_right(R, K=10):
    """R: cells of a right cap with its first unit at K (at an even generation, on wire C units < K)."""
    x = W.tape_cells('C' * (K + 30), 0, -30, K) | R
    if sg.step_set(sg.step_set(x)) & frozenset(c for c in x if unit(c) >= K - 4) != frozenset(c for c in x if unit(c) >= K - 4):
        pass
    y = frozenset(M(c) for c in sg.step_set(x))
    # find the shift that makes the image's wire part equal to wire C (even phase) far from the cap
    for s in range(-80, 80):
        z = frozenset(tr(c, s) for c in y)
        ref = W.tape_cells('C' * 12, 0, 6, 18)
        if frozenset(c for c in z if 6 <= unit(c) < 18) == ref:
            break
    else:
        return None
    # boundary: the smallest b such that units >= b (up to 18) are pure wire C
    b = 18
    while b > -40 and frozenset(c for c in z if b - 1 <= unit(c) < 18) == W.tape_cells('C' * 40, 0, b - 1, 18):
        b -= 1
    return frozenset(tr(c, -b) for c in z if unit(c) < b)


def classify(cap, U=3, limit=3000):
    S = {}; todo = []
    def add(s):
        if s not in S:
            S[s] = {}; todo.append(s)
    for w in itertools.product('BC', repeat=U + 1):
        add(cap | W.tape_cells(''.join(w), 0, 0, U + 1))
    init = set(S)
    # the cap alone must be stationary
    bare = cap | W.tape_cells('C' * (U + 6), 0, 0, U + 6)
    if frozenset(c for c in sg.step_set(sg.step_set(bare)) if unit(c) <= U) != frozenset(c for c in bare if unit(c) <= U):
        return 'not stationary', 0
    while todo:
        s = todo.pop()
        for w in itertools.product('BC', repeat=3):
            word = ''.join(w) + 'CC'
            x = s | frozenset(tr(c, U + 1) for c in W.tape_cells(word, 0, 0, 5))
            y = sg.step_set(sg.step_set(x))
            if frozenset(c for c in y if U + 1 <= unit(c) <= U + 3) != frozenset(tr(c, U + 1) for c in W.tape_cells(word[1:4], 0, 0, 3)):
                return 'emits', len(S)
            s2 = frozenset(c for c in y if unit(c) <= U)
            S[s][''.join(w)] = s2; add(s2)
            if len(S) > limit:
                return 'big', len(S)
    if set(S) == init:
        return 'sink', len(S)
    b0 = frozenset(c for c in bare if unit(c) <= U)
    back = 0
    for s in S:
        x = s
        for _ in range(4 * U + 20):
            if x == b0:
                break
            x = S[x]['CCC']
        back += x == b0
    return f'memory ({len(S)} states, {back} return to the bare cap under C letters)', len(S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('table'); ap.add_argument('--U', type=int, default=3); ap.add_argument('--max', type=int, default=10 ** 9)
    ap.add_argument('--clocks', help='clocks.py output: classify only these right caps (those that turn the rake)')
    a = ap.parse_args()
    D = json.load(open(a.table))
    items = list(D['states'].items())[:a.max]
    if a.clocks:
        keep = {str(r['state']) for r in json.load(open(a.clocks))}
        items = [kv for kv in items if kv[0] in keep]
    tally = Counter(); ex = {}
    for sid, st in items:
        R = frozenset(map(tuple, st))
        if not R:
            continue
        u0 = min(unit(c) for c in R)
        L = left_cap_from_right(frozenset(tr(c, 10 - u0) for c in R))
        if L is None:
            tally['no image'] += 1; continue
        v, n = classify(L, a.U)
        k = v.split(' (')[0]
        tally[k] += 1
        if k == 'memory':
            print(sid, v, len(L), 'cells', flush=True)
        ex.setdefault(k, sid)
    print(a.table, dict(tally), 'examples:', ex)


if __name__ == '__main__':
    main()
