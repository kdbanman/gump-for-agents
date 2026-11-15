#!/usr/bin/env python3
"""Census of the one-cell flips of wire B, and the emitter, with oracle.step only.

    nice -n 10 python3 flips_B.py

Candidates: every cell of one cube (x // 2 == 0) that is live in some phase of the bare wire or is a neighbour of
such a cell; each flipped at generation 0 and at generation 1 (the wire has period 2).  Ring of N = 64 cubes, box
torus (128, 20, 128), flip in cube 32, run 60 generations (pulses cannot meet round the ring), extended to 160 for
anything not yet settled.  Classes (by the set of cells differing from the bare wire of the same generation):
  heal      empty at the end
  standing  stationary (x(t) = x(t-2)), non-empty, within 3 cubes of the flip
  pulse+/-  the difference is exactly a moved copy of pulse B (right) / its mirror (left), alone (and nothing else)
  pulses    two pulses, one each way;  front  more than 40 cells differ and the span keeps growing;  other
"""
import json, subprocess
from collections import Counter
from lat import ring_torus, wire, shift, sstep, nbrs, ROOT

ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', 'bcd5844:research/signals/objects/pulse-B.json']))
obl = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', '896f44b:research/signals/objects/pulse-B-left.json']))
bg = [tuple(c) for c in ob['bg']]
cube = lambda c: c[0] // 2
N = 64; T = ring_torus(N); K0 = 32
# phases of the bare wire, one cube
piece = wire(bg, -10, 10); ph = []
for t in range(3):
    ph.append(frozenset(c for c in piece if cube(c) == 0)); piece = sstep(piece)
assert ph[2] == ph[0] and ph[1] != ph[0]
live = ph[0] | ph[1]
cand = set(live)
for c in wire(live, -2, 3):
    for q in nbrs(c):
        cand.add(q)
cand = sorted(set(shift([q], -cube(q))[0] if False else next(iter(shift([q], -cube(q)))) for q in cand))
print(f'wire B: {len(live)} cells live in some phase per cube; {len(cand)} candidate cells per cube; {2 * len(cand)} trials')

R = frozenset(tuple(c) for c in ob['defect']); L = frozenset(tuple(c) for c in obl['defect'])
norm = lambda cells: shift(cells, -min(cube(c) for c in cells))
Rn, Ln = norm(R), norm(L)
bare0 = wire(bg, 0, N)
B = [T.arr(bare0)]; B.append(T.step(B[0]))
Bc = [T.cells(B[0]), T.cells(B[1])]
mod = lambda cells: frozenset(T.mod(c) for c in cells)


def is_moved(d, P):
    if not d:
        return None
    for k in range(N):
        if mod(shift(P, k)) == d:
            return k
    return None


res = []
cnt = Counter()
for phase in (0, 1):
    for c in cand:
        cell = next(iter(shift([c], K0)))
        x = B[phase].copy(); x[T.mod(cell)] ^= 1
        t = phase; prev = None; hist = []
        cls = None
        while True:
            x = T.step(x); t += 1
            d = T.cells(x) ^ Bc[t % 2]
            cubes = sorted(set(((cube(q) - K0 + N // 2) % N) - N // 2 for q in d))
            hist.append((len(d), cubes[0] if cubes else None, cubes[-1] if cubes else None))
            if t >= 60 and t % 2 == 0:
                if not d:
                    cls = 'heal'
                else:
                    stat = prev is not None and d == prev
                    kR = is_moved(d, Rn); kL = is_moved(d, Ln)
                    half = lambda side: frozenset(q for q in d if (((cube(q) - K0) % N) < N // 2) == side)
                    kR2 = is_moved(half(True), Rn); kL2 = is_moved(half(False), Ln)
                    if kR is not None:
                        cls = f'pulse+ (at {(kR - K0) % N} cubes)'
                    elif kL is not None:
                        cls = f'pulse- (at {-((K0 - kL) % N)} cubes)'
                    elif kR2 is not None and kL2 is not None:
                        cls = 'pulses both ways'
                    elif stat and max(abs(cubes[0]), abs(cubes[-1])) <= 3:
                        cls = f'standing ({len(d)} cells)'
                    elif len(d) > 40 and hist[-1][2] - hist[-1][1] > hist[-21][2] - hist[-21][1]:
                        cls = 'front'
                    elif t >= 160:
                        cls = f'other ({len(d)} cells, cubes {cubes[0]}..{cubes[-1]})'
                if cls:
                    break
            if t % 2 == 0:
                prev = d
        kind = cls.split(' (')[0]
        cnt[kind] += 1
        res.append(dict(cell=c, phase=phase, live_in_phase=c in ph[phase], cls=cls, t=t))
        if kind not in ('heal',):
            print(f'  flip {c} at phase {phase} (live: {c in ph[phase]}): {cls}', flush=True)
print('census:', dict(cnt))
json.dump(res, open(__import__('lat').SCR + '/flipsB.json', 'w'))
