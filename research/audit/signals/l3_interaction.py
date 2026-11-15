#!/usr/bin/env python3
"""L3 audit: two pulses of wire B, built from pulse-B.json and pulse-B-left.json (at 896f44b), stepped by oracle.step.

    nice -n 10 python3 l3_interaction.py

Separation d = (first cube of the left pulse's cells) - (first cube of the right pulse's cells) at generation 0.
 head-on  right pulse at cube 0, left pulse at cube d, d = 1 .. 44, on rings N = 64 and 65 (box torus (2N, 20, 2N)).
          On a ring they meet twice: after the first meeting (t1 = d + 16) and after the second (t2 = N + d + 16:
          the second meeting is the first one with the separation increased by N, so its parity flips on an odd ring).  Each time the state is classed:
            pass   = exactly bare XOR both pulses where they would be had they never met
            mark k = stationary (same 2 and 40 generations later) and k cells differ from bare
            fire   = more than 60 cells differ;   other = anything else (described)
 follow   two right pulses d = 1 .. 12 cubes apart (and two left pulses): after 2N generations, is the state exactly
          the pair moved (a rigid train)?
 mark     the 3-cell mark (d = 22, 24), hit by a later pulse from each side: what is left (count, stationary?).
"""
import json, subprocess
from lat import ring_torus, wire, shift, ROOT


def load(name):
    return json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'896f44b:research/signals/objects/{name}.json']))


R0 = load('pulse-B'); L0 = load('pulse-B-left')
bg = [tuple(c) for c in R0['bg']]
assert bg == [tuple(c) for c in L0['bg']]
cube = lambda c: c[0] // 2
norm = lambda cells: shift(cells, -min(cube(c) for c in cells))
R = norm(frozenset(tuple(c) for c in R0['defect'])); L = norm(frozenset(tuple(c) for c in L0['defect']))


class Run:
    def __init__(self, N, defects):
        self.T = ring_torus(N); self.N = N
        b0 = wire(bg, 0, N)
        x0 = set(b0)
        for D in defects:
            for c in D:
                x0 ^= {c}
        self.x = self.T.arr(x0); self.b = self.T.arr(b0); self.t = 0

    def to(self, t):
        while self.t < t:
            self.x = self.T.step(self.x); self.b = self.T.step(self.b); self.t += 1
        return self.T.cells(self.x), self.T.cells(self.b)


def classify(run, t, expect):
    x, b = run.to(t)
    d = x ^ b
    if expect is not None and d == frozenset(run.T.mod(c) for c in expect):
        return 'pass'
    if len(d) > 60:
        return 'fire'
    x2, _ = run.to(t + 2)
    x40, _ = run.to(t + 40)
    if x2 == x and x40 == x:
        cubes = sorted(set((c[0] // 2) % run.N for c in d))
        return f'mark{len(d)}@{cubes[0]}..{cubes[-1]}' if d else 'clean'
    return f'other({len(d)})'


def main():
    out = {}
    print('head-on: d -> (after first meeting, after second meeting)')
    for N in (64, 65):
        row = []
        for d in range(1, 45):
            Ld = shift(L, d)
            if any(c in R for c in Ld):
                row.append((d, 'overlap')); continue
            run = Run(N, [R, Ld])
            t1 = d + 16
            t1 += t1 % 2
            e1 = shift(R, t1 // 2) ^ shift(Ld, -(t1 // 2))
            c1 = classify(run, t1, e1)
            t2 = N + d + 16; t2 += t2 % 2
            e2 = shift(R, t2 // 2) ^ shift(Ld, -(t2 // 2)) if c1 == 'pass' else None
            c2 = classify(run, t2, e2) if c1 in ('pass',) else '-'
            row.append((d, c1, c2))
        out[N] = row
        print(f'  ring N={N}:')
        for r in row:
            print('    ', r, flush=True)
    print('follow: two pulses moving the same way, d cubes apart; rigid train after 2N gens?')
    N = 64
    for name, P, s in (('right', R, 1), ('left', L, -1)):
        res = []
        for d in range(1, 13):
            Pd = shift(P, d)
            if any(c in P for c in Pd):
                res.append((d, 'overlap')); continue
            run = Run(N, [P, Pd])
            x, b = run.to(2 * N)
            exp = frozenset(run.T.mod(c) for c in shift(P, s * N) ^ shift(Pd, s * N))
            res.append((d, 'train' if (x ^ b) == exp else f'no({len(x ^ b)})'))
        print(f'  {name}:', res, flush=True)
    # the mark (left by an even d), then a third pulse from either side; ring of 96 so nothing laps
    print('mark hit by a later pulse (ring 96): state 100 and 140 generations after the third pulse was due to arrive')
    N = 96
    for d in (22, 24):
        for side in ('from the left (a right-mover)', 'from the right (a left-mover)'):
            extra = shift(R, -20) if 'left (' in side else shift(L, d + 20)
            run = Run(N, [R, shift(L, d), extra])
            x, b = run.to(160); x2, _ = run.to(162); x3, _ = run.to(200)
            dd = x ^ b
            cubes = sorted(set((c[0] // 2) % N for c in dd))
            print(f'  d={d}, third pulse {side}: {len(dd)} cells differ from bare at t=160, cubes {cubes}; '
                  f'stationary (t=160,162,200): {x == x2 == x3}', flush=True)
    json.dump({str(k): v for k, v in out.items()}, open(__import__('lat').SCR + '/l3_headon.json', 'w'))


if __name__ == '__main__':
    main()
