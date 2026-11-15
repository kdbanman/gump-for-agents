#!/usr/bin/env python3
"""Survey of pulse-carrying wires: enumerate backgrounds (repeat 1 cube) that carry a (P, S) pulse in a small tube,
then test each background for robustness and its pulses for what they do when they meet.

    python3 survey.py M1 M2 N P S [--max 40] [--timeout 300]

1. SAT as in sat_pulse.py (tube(M1, M2), ring of N cubes, uniform stretch of K = max(3, S+1) cubes); after each
   solution the background found (all its phases) is forbidden and the solver is asked again, until UNSAT (then the
   list of backgrounds with a pulse of width <= N - K - 1 - S is complete for this tube) or --max / --timeout.
2. For each background, in the wide tube [-7,13]^2 (exact in free space), ring of 64 cubes:
   flips    every one-cell flip of one cube (cells live in some phase and their neighbours, every phase):
            how many heal / stay local / start a front ('fire') / other
   alone    the pulse found, alone, moves S cubes per P generations for a full lap
   meet     if the wire has a symmetry that reverses it, the pulse and its mirror image are sent at each other
            (two parities): 'fire', 'annihilate' (nothing left), 'pass' (both continue), or a description
Appends one JSON line per background to research/scratch/signals/survey.jsonl.
"""
import argparse, itertools, json, os, time
from collections import Counter
from math import gcd
import numpy as np
from pysat.solvers import Solver
import sg, plab
from sat_pulse import build

GROUP = [(p, s) for p in itertools.permutations(range(3)) for s in itertools.product((1, -1), repeat=3)]
N2 = 64


def reversing_symmetry(bgcells, P):
    """(g, t, phase) with x -> g(x) + t mapping the wire (phase 0) onto the wire (some phase), reversing (1,0,-1)."""
    wire = lambda cells, K: frozenset(c for k in range(-K, K + 1) for c in plab.tr(cells, k))
    W = [wire(bgcells, 14)]
    for _ in range(P - 1):
        W.append(sg.step_set(W[-1]))
    app = lambda g, c: tuple(g[1][k] * c[g[0][k]] for k in range(3))
    for g in GROUP:
        if app(g, plab.V) != (-1, 0, 1):
            continue
        img = [app(g, c) for c in bgcells]
        for ph in range(P):
            for tgt in [c for c in W[ph] if -2 <= c[0] <= 2]:
                t = tuple(tgt[k] - img[0][k] for k in range(3))
                if any(x % 2 for x in t):
                    continue
                if all(tuple(c[k] + t[k] for k in range(3)) in W[ph] for c in img):
                    return g, t, ph
    return None


def diffcubes(g, x, bg):
    return (g.as_grid(x) != g.as_grid(bg)).sum(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('m1', type=int); ap.add_argument('m2', type=int); ap.add_argument('N', type=int)
    ap.add_argument('P', type=int); ap.add_argument('S', type=int)
    ap.add_argument('--max', type=int, default=40); ap.add_argument('--timeout', type=float, default=300)
    a = ap.parse_args()
    N, P, S = a.N, a.P, a.S; K = max(3, S + 1)
    assert gcd(S, N) == 1
    g, f, X = build(a.m1, a.m2, N, P, S, 1, K, live=True)
    gw = plab.geom(N2)
    out = open(os.path.join(sg.SCR, 'survey.jsonl'), 'a')
    base = [g.cells[i] for i in g.grid[0]]
    t0 = time.time(); nbg = 0; status = 'max reached'
    with Solver(name='cadical153', bootstrap_with=f.cl) as s:
        while nbg < a.max:
            if time.time() - t0 > a.timeout:
                status = 'TIMEOUT'; break
            if not s.solve():
                status = 'complete'; break
            m = set(l for l in s.get_model() if l > 0)
            st = np.zeros(g.n + 1, np.uint8)
            for i in range(g.n):
                st[i] = X[0][i] in m
            M = g.as_grid(st); nbg += 1
            rows = [g.as_grid(g.run(st, t))[0] for t in range(P)]
            for r in rows:                                   # forbid this background in every phase
                s.add_clause([(-X[0][int(g.grid[0, l])] if r[l] else X[0][int(g.grid[0, l])]) for l in range(g.nloc)])
            bgc = [tuple(map(int, base[l])) for l in np.nonzero(M[0])[0]]
            defect = [tuple(int(base[l][j] + 2 * u * plab.V[j]) for j in range(3)) for u in range(N) for l in range(g.nloc) if M[u, l] != M[0, l]]
            ob = dict(bg=bgc, defect=defect)
            # ---- tests in the wide tube
            bg = plab.background(gw, ob)
            bper = gw.cycle(bg)[0]
            bgs = [gw.run(bg, t, sparse=True) for t in range(bper)]
            U = np.nonzero(np.array([b[:gw.n] for b in bgs]).any(0))[0]
            cand = set(U.tolist()) | set(gw.nb[U].ravel().tolist()); cand.discard(gw.n)
            c0 = sorted(i for i in cand if gw.unit[i] == N2 // 2)
            fl = Counter()
            for t in range(bper):
                for i in c0:
                    x = bgs[t].copy(); x[i] ^= 1
                    r = gw.track(bgs[t], x, N2 // 2, span=20, maxgen=300)
                    fl[{0: 'heal', 1: 'local', 2: 'fire', 3: 'other'}[r['ret']]] += 1
            x = plab.with_defect(gw, bg, defect, 0)
            lap = gw.run(x, N2 * P // S if (N2 * P) % S == 0 else N2 * P, sparse=True)
            alone = bool((lap == (x if (N2 * P) % S == 0 else x)).all())
            meet = []
            sym = reversing_symmetry(bgc, bper)
            if sym and alone:
                gsym, tsym, ph = sym
                app = lambda c: tuple(gsym[1][k] * c[gsym[0][k]] + tsym[k] for k in range(3))
                for d in (0, 1):
                    y = plab.with_defect(gw, bgs[0], defect, 0)
                    # the mirror pulse lives on phase `ph`; advance the right-mover alone by ph generations first
                    y = gw.run(y, ph, sparse=True)
                    y = plab.with_defect(gw, y, [app(c) for c in defect], 20 + d)
                    b = bgs[ph % bper]
                    T = 2 * 40 * P // S + 60
                    y1 = gw.run(y, T, sparse=True); b1 = gw.run(b, T, sparse=True)
                    d1 = diffcubes(gw, y1, b1); n1 = int((d1 > 0).sum()); c1 = int(d1.sum())
                    y2 = gw.run(y1, 2 * P * 4, sparse=True); b2 = gw.run(b1, 2 * P * 4, sparse=True)
                    d2 = diffcubes(gw, y2, b2); n2 = int((d2 > 0).sum())
                    nd = len(defect)
                    if n1 == 0:
                        meet.append('annihilate')
                    elif n2 > n1 + 2 or n1 > 30:
                        meet.append('fire')
                    elif c1 == 2 * nd and n2 == n1:
                        meet.append('pass?')
                    else:
                        meet.append('other(%d cubes, %d cells)' % (n1, c1))
            rec = dict(tube=[a.m1, a.m2], N=N, p=P, s=S, bg=[list(c) for c in bgc], bg_period=int(bper), defect=[list(c) for c in defect],
                       flips=dict(fl), alone=alone, reversible=bool(sym), meet=meet)
            out.write(json.dumps(rec) + '\n'); out.flush()
            print(f'  bg #{nbg}: {len(bgc)} cells/cube, period {bper}; pulse of {len(defect)} cells, alone {"ok" if alone else "NO"}; '
                  f'flips {dict(sorted(fl.items()))}; reversible {bool(sym)}; meet {meet}', flush=True)
    print(f'{status}: {nbg} backgrounds; tube {a.m1}x{a.m2} N={N} (p,s)=({P},{S}) width<={N - K - 1 - S}; {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
