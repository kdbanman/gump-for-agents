#!/usr/bin/env python3
"""Verify, with reference/oracle.py as the judge, that capL of the clock eats every word of the B/C tape and capR
writes C for ever: the tape between them is a shift register that empties into capL, exactly, at every step.

    python3 verify_reader.py [--N 40] [--words 12] [--seed 1]

Object: capL + N units of tape holding a word w (each unit a B unit or a C unit, cells as in sat_writer.EVEN) +
capR moved N units (objects/clock-C.json).  Claim: at every even generation 2t the state is exactly
capL + tape(w moved t units towards -v, padded with C on the right) + capR, cell for cell; so after 2N generations
it is the bare clock (capL + C^N + capR).  Words: all-B, alternating, and random words of densities 0.1 .. 0.9.
Stepping: oracle.masks and oracle.step on a cubic array torus with a wide margin.  (The proof for every word, by a
closed automaton, is prove_reader.py.)
"""
import argparse, json, random
import numpy as np
import sg, sat_writer as Wr
oracle = sg.oracle
tr = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)

ap = argparse.ArgumentParser()
ap.add_argument('--N', type=int, default=40); ap.add_argument('--words', type=int, default=12); ap.add_argument('--seed', type=int, default=1)
a = ap.parse_args(); N = a.N
ob = json.load(open(sg.os.path.join(sg.HERE, 'objects', 'clock-C.json')))
capL = frozenset(map(tuple, ob['capL'])); capR = frozenset(tr(tuple(c), N) for c in ob['capR'])
def obj(word):
    return capL | Wr.tape_cells(word, 0, 0, N) | capR
allc = obj('B' * N) | obj('C' * N)
lo = [min(c[i] for c in allc) for i in range(3)]; hi = [max(c[i] for c in allc) for i in range(3)]
H = max(hi[i] - lo[i] for i in range(3)) + 28; H += H % 2
off = [((H - (hi[i] - lo[i])) // 2 - lo[i]) // 2 * 2 for i in range(3)]
m = oracle.masks(H)
def arr(cs):
    h = np.zeros((H, H, H), np.int8)
    for c in cs:
        h[c[0] + off[0], c[1] + off[1], c[2] + off[2]] = 1
    return h
random.seed(a.seed)
words = ['B' * N, 'BC' * (N // 2), 'BBC' * (N // 3) + 'C' * (N % 3)]
while len(words) < a.words:
    p = random.choice([0.1, 0.3, 0.5, 0.7, 0.9]); words.append(''.join('B' if random.random() < p else 'C' for _ in range(N)))
ok_all = True
for w in words:
    h = arr(obj(w)); ok = True
    for t in range(1, N + 3):
        h = oracle.step(oracle.step(h, m), m)
        shifted = (w[t:] + 'C' * N)[:N]
        if not np.array_equal(h, arr(obj(shifted))):
            ok = False; print('   differs at generation', 2 * t); break
    print('PASS' if ok else 'FAIL', f'word {w[:24]}{"..." if N > 24 else ""} ({w.count("B")} B): exact shift into capL at every even generation for {2 * (N + 2)} generations; ends as the bare clock', flush=True)
    ok_all &= ok
print('ALL PASS' if ok_all else 'SOME CHECKS FAILED', f'- reader capL, writer capR, N = {N}, {len(words)} words, torus side {H}')
