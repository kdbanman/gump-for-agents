#!/usr/bin/env python3
"""Spot-check of the wires on file: one-cell flips, front speed, ash.  Own sparse stepper on the lattice modulo the
ring translation only (no transverse images; equal to oracle.step by lat.selftest), plus one cell-for-cell comparison
with oracle.step on the cubic torus for a W00 front.

    nice -n 10 python3 fronts_check.py W00 [W05 W18 ...] [--oracle]

Per wire (cells from research/signals/wires/Wnn.json at bcd5844), ring of N repeats:
 bare     the ring has exactly the stated period;
 flips    every candidate cell of one repeat (live in some phase, or a neighbour of such a cell), flipped at phase 0,
          run 250 generations on a ring of 40 repeats: heal (no difference left) / local (difference within 4
          repeats of the flip) / front (difference spans >= 8 repeats) / other;
 front    the first front-starting flip, on a ring of 160 repeats, 760 generations: leading edge (repeat index of the
          farthest differing cell) on each side over time; exact space-time period (p, s) at the edge: the state in a
          window of 14 repeats around the edge at t+p is the state at t moved s repeats, for every t in the last 300
          generations, tried for p <= 60; the ash 20+ repeats behind the edge: its exact period, and whether it is the
          wire in some phase.
"""
import json, subprocess, sys
from collections import Counter
from lat import nbrs, sstep, Torus, ROOT

args = [x for x in sys.argv[1:] if not x.startswith('--')]
ORACLE = '--oracle' in sys.argv


def load(wid):
    r = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'bcd5844:research/signals/wires/{wid}.json']))
    cells = r['cells'] if isinstance(r['cells'], list) else json.loads(r['cells'])
    return dict(P=r['period'], v=tuple(r['v']), cells=[tuple(c) for c in cells])


class Ring:
    def __init__(self, w, N):
        self.v = w['v']; self.N = N; self.X = 2 * N * self.v[0]     # x-period of the ring (v[0] > 0)
        assert self.v[0] > 0

    def canon(self, c):
        k = c[0] // self.X
        if k:
            c = (c[0] - 2 * k * self.N * self.v[0], c[1] - 2 * k * self.N * self.v[1], c[2] - 2 * k * self.N * self.v[2])
        return c

    def step(self, live):
        cnt = Counter()
        for c in live:
            for q in nbrs(c):
                cnt[self.canon(q)] += 1
        return frozenset(c for c, k in cnt.items() if k in (4, 5) or (k == 3 and c in live))

    def tr(self, cells, k):
        v = self.v
        return frozenset(self.canon((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)

    def rep(self, c):                # repeat index of a cell (by x)
        return (c[0] // (2 * self.v[0])) % self.N

    def wire(self, cells):
        out = set()
        for k in range(self.N):
            out |= self.tr(cells, k)
        return frozenset(out)


def orbit(R, x, n):
    out = [x]
    for _ in range(n):
        x = R.step(x); out.append(x)
    return out


def rel(R, r, r0):
    d = (r - r0) % R.N
    return d - R.N if d > R.N // 2 else d


def candidates(R, w, ph):
    live = frozenset().union(*ph)
    near = set(live)
    for c in live:
        near |= {R.canon(q) for q in nbrs(c)}
    return sorted(c for c in near if R.rep(c) == R.N // 2)


def census(w):
    R = Ring(w, 40); P = w['P']
    bare = R.wire(w['cells']); ph = orbit(R, bare, P)
    assert ph[P] == ph[0] and all(ph[t] != ph[0] for t in range(1, P)), 'bare period'
    cand = candidates(R, w, ph[:P])
    fates = Counter(); first_front = None
    for c in cand:
        x = ph[0] ^ {c}
        fate = None
        for t in range(1, 251):
            x = R.step(x)
            d = x ^ ph[t % P]
            if not d:
                fate = 'heal'; break
            rs = [rel(R, R.rep(q), R.N // 2) for q in d]
            if max(rs) - min(rs) >= 8:
                fate = 'front'; break
        if fate is None:
            rs = [rel(R, R.rep(q), R.N // 2) for q in d]
            fate = 'local' if max(map(abs, rs)) <= 4 else 'other'
        fates[fate] += 1
        if fate == 'front' and first_front is None:
            first_front = c
    return len(cand), fates, first_front


def front(w, cell, N=160, T=760):
    R = Ring(w, N); P = w['P']
    bare = R.wire(w['cells']); ph = orbit(R, bare, P)
    # move the flip cell from repeat 20 (census ring) to repeat N//2 of this ring
    src = cell
    d0 = (N // 2) - (src[0] // (2 * w['v'][0]))
    c = next(iter(R.tr([src], d0)))
    x = ph[0] ^ {c}
    hist = []; states = {}
    for t in range(1, T + 1):
        x = R.step(x)
        d = x ^ ph[t % P]
        rs = [rel(R, R.rep(q), N // 2) for q in d]
        hist.append((t, max(rs), min(rs), len(d)))
        if t > T - 420:
            states[t] = x
    out = {}
    for side, idx in (('+v', 1), ('-v', 2)):
        e1, e2 = hist[T - 401][idx], hist[T - 1][idx]
        out[side] = dict(speed=(e2 - e1) / 400.0)
        # exact (p, s) at the edge
        best = None
        for p in range(1, 61):
            s = round(out[side]['speed'] * p)
            if s == 0:
                continue
            ok = True
            for t in range(T - 300, T - p + 1, 7):
                e = hist[t - 1][idx]
                lo, hi = (e - 8, e + 6) if side == '+v' else (e - 6, e + 8)
                win = lambda st, a, b: frozenset(q for q in st if a <= rel(R, R.rep(q), N // 2) <= b)
                A = win(states[t], lo, hi)
                B = win(states[t + p], lo + s, hi + s)
                if R.tr(A, s) != B:
                    ok = False; break
            if ok:
                best = (p, abs(s)); break
        out[side]['ps'] = best
        # ash: repeats between 20 and 10+ behind the edge, at the end
        e = hist[T - 1][idx]
        a, b = (N // 2 + 4, N // 2 + e - 20) if side == '+v' else (N // 2 + e + 20, N // 2 - 4)
        if b - a >= 6:
            region = lambda st: frozenset(q for q in st if a <= (N // 2 + rel(R, R.rep(q), N // 2)) <= b)
            q = next((q for q in range(1, 400) if region(states[T]) == region(states[T - q])), None)
            asw = any(region(states[T]) == region(ph[t]) for t in range(P))
            out[side]['ash'] = dict(period=q, repeats=b - a + 1, cells=len(region(states[T])), is_wire_phase=asw)
    return out, hist


def oracle_cross(w, cell, C=60, T=300):
    """W00 only (v[0] = 1): the same flip on the cubic torus of side C cubes (H = 2C) with oracle.step, compared cell
    for cell with the sparse ring of C repeats (the torus ring has C repeats) for T generations."""
    R = Ring(w, C); P = w['P']
    H = 2 * C; Tt = Torus((H, H, H))
    bare = R.wire(w['cells'])
    d0 = (C // 2) - (cell[0] // (2 * w['v'][0]))
    c = next(iter(R.tr([cell], d0)))
    x = bare ^ {c}
    h = Tt.arr(x)
    assert len({Tt.mod(q) for q in bare}) == len(bare), 'torus ring overlaps'
    for t in range(1, T + 1):
        x = R.step(x); h = Tt.step(h)
        if t % 25 == 0 or t == T:
            if frozenset(Tt.mod(q) for q in x) != Tt.cells(h):
                return f'MISMATCH at t={t}'
    return f'identical for {T} generations ({len(x)} live cells at the end)'


if __name__ == '__main__':
    res = {}
    for wid in args:
        w = load(wid)
        n, fates, ff = census(w)
        print(f'{wid} (period {w["P"]}, v {w["v"]}): {n} candidate cells, flips at phase 0: {dict(fates)}; first front from {ff}', flush=True)
        if ff:
            out, hist = front(w, ff)
            for side, o in out.items():
                print(f'   front {side}: speed {o["speed"]:.4f} repeats/gen; exact (p, s) at the edge: {o["ps"]}; ash: {o.get("ash")}', flush=True)
            if ORACLE and wid == 'W00':
                print('   oracle cross-check:', oracle_cross(w, ff), flush=True)
        res[wid] = dict(cands=n, fates=dict(fates), first_front=ff)
    json.dump(res, open(__import__('lat').SCR + '/fronts_check.json', 'w'))
