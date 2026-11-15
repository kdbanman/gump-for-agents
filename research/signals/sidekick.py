#!/usr/bin/env python3
"""Guns by a side kick: a shuttle clock (objects/clock-C.json) with a second, long wire running past one of its
caps.  When the rake turns at the cap, does the second wire receive a pulse, while the clock goes on and the
unlit pair is stationary?  The second wire may run along any of the six face diagonals (a turn in direction is a
corner for free).

    python3 sidekick.py [--wire B|C] [--N 3] [--R 7] [--dirs all|par] [--len 70]

For every orientation of the second wire (the 48 symmetries applied to one unit of wire B or wire C, one per
direction and placement up to translation along it) and every translation by an even vector (2i, 2j, 2k) with
|i|, |j|, |k| <= R that brings it within a neighbour step of the clock but shares no cell with it:
  unlit  the clock (unlit) + the second wire (a finite piece of +-len units, cut ends) is stationary (period 2) on
         every cell within 12 doubled units of the clock;
  lit    with the rake lit, after 3 periods of the clock, the cells of the second wire between 14 and 40 units
         (doubled 28..80) from the clock differ from the unlit run (something has travelled out along it), and the
         clock's own cells still repeat with the clock's period.
Stepping: sg.step_set (the infinite lattice; the cut ends of the second wire are > 100 doubled units away and
are never looked at within the time run).  Candidates are printed for inspection; nothing here is a verdict of
the oracle.
"""
import argparse, itertools, json
import sg, scat

tr = scat.tr


def syms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg_ in itertools.product((1, -1), repeat=3):
            out.append((perm, sg_))
    return out


def apply(s, p):
    perm, sgn = s
    return tuple(sgn[i] * p[perm[i]] for i in range(3))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wire', default='B'); ap.add_argument('--N', type=int, default=3); ap.add_argument('--R', type=int, default=7)
    ap.add_argument('--len', type=int, default=60); ap.add_argument('--dirs', default='all')
    a = ap.parse_args(); N = a.N
    ck = json.load(open('objects/clock-C.json'))
    clock = frozenset(map(tuple, ck['capL'])) | {tr(tuple(c), k) for c in ck['unit'] for k in range(N)} | {tr(tuple(c), N) for c in ck['capR']}
    clock = frozenset(clock)
    lit = clock | {tr(tuple(ck['ignite']), N // 2)}
    P = 4 * N + 2
    unitB = [(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)] if a.wire == 'B' else [tuple(c) for c in ck['unit']]
    def canon(p, v):
        vv = sum(x * x for x in v); k = round(sum(p[q] * v[q] for q in range(3)) / vv)
        return tuple(p[q] - k * v[q] for q in range(3))
    orients = {}
    for s in syms():
        v = apply(s, (2, 0, -2))
        if a.dirs == 'par' and v not in ((2, 0, -2), (-2, 0, 2)):
            continue
        cells = [apply(s, c) for c in unitB]
        if v < tuple(-x for x in v):
            v = tuple(-x for x in v)
        key = (v, frozenset(canon(c, v) for c in cells))
        orients[key] = (v, cells)
    print(len(orients), 'distinct orientations of the second wire')
    cx = [sum(c[i] for c in clock) / len(clock) for i in range(3)]
    dist = lambda c: max(abs(c[q] - cx[q]) for q in range(3))
    nb = frozenset(q for c in clock for q in sg.nbrs(c)) - clock
    core = lambda S: frozenset(c for c in S if dist(c) <= 2 * N + 16)
    tested = 0; cands = []; stat = 0
    for v, cells in orients.values():
        L = a.len
        w = frozenset((c[0] + k * v[0], c[1] + k * v[1], c[2] + k * v[2]) for c in cells for k in range(-L, L))
        D = set()
        for n_ in nb:
            for c in cells:
                d = canon(tuple(n_[q] - c[q] for q in range(3)), v)
                if all(x % 2 == 0 for x in d):
                    D.add(d)
        for d in sorted(D):
            W = frozenset((c[0] + d[0], c[1] + d[1], c[2] + d[2]) for c in w)
            if W & clock:
                continue
            tested += 1
            x0 = clock | W
            if core(sg.step_set(sg.step_set(x0))) != core(x0):
                continue
            stat += 1
            x = lit | W; z = x0
            for t in range(3 * P + 20):
                x = sg.step_set(x); z = sg.step_set(z)
            Wn = lambda S: frozenset(c for c in S if 2 * N + 24 <= dist(c) <= 2 * N + 70)
            dif = Wn(x) ^ Wn(z)
            if not dif:
                continue
            x2 = x
            for t in range(P):
                x2 = sg.step_set(x2)
            cands.append(dict(dir=v, shift=d, ndiff=len(dif), clock_periodic=core(x2) == core(x)))
            print('CANDIDATE', cands[-1], flush=True)
    print(f'tested {tested} placements touching the clock, {stat} of them stationary unlit; {len(cands)} send something out along the second wire')


if __name__ == '__main__':
    main()
