#!/usr/bin/env python3
"""Harvest wires along (1,0,-1) from random soups in closed diamond tubes, and test each for fronts and pulses.

    python3 harvest.py M1 M2 L NSOUP [--rho 0.4] [--seed 1] [--R 40]

Tube(M1, M2): the cells with s1 = x+y+z in [1, 2 M1 - 1] and s2 = x-y+z in [1, 2 M2 - 1].  Both diagonals are
perpendicular to (1,0,-1), so by T2 the tube is a closed vessel: whatever starts in it stays in it, and everything
found here exists unchanged in empty space.  Soups fill a ring of L cubes; a settled state is kept if it is not empty,
has least period L along the ring, and is a wire (the union of its phases is connected round the ring, tested on the
double cover).  Kept wires are deduplicated by (period, per-phase population and neighbour-count histogram, up to rotation and
reversal): a coarse key, so the count of distinct wires is a lower bound.

Each wire is then laid R repeats long and (a) cut: one repeat removed, in every phase (at most 24 phases);
(b) hit: one repeat replaced by soup, 24 times.  Fates as in flips.py: heals / stays / runs (with the sides) / pulse.
Appends one JSON line per wire to research/scratch/signals/harvest.jsonl.
"""
import argparse, json, os, random
from collections import Counter, deque
import numpy as np
import sg
from fronts import regular

S1, S2 = (1, 1, 1), (1, -1, 1)
G = (1, 0, -1)


def tube(m1, m2, cubes, unit=1):
    return sg.Geom([(cubes, 0, -cubes)], [(S1, 1, 2 * m1 - 1), (S2, 1, 2 * m2 - 1)], unitvec=(unit, 0, -unit))


def is_wire(g2, st2, P):
    """g2: ring of 2L cubes carrying two copies of the state.  True iff the union over one period is connected round
    the ring: some cell is linked (share-a-neighbour) to its own translate by L cubes."""
    U = np.zeros(g2.n + 1, bool); x = st2
    for _ in range(P):
        U |= x.astype(bool); x = g2.run(x, 1)
    U[g2.n] = False
    L = g2.N // 2
    comp = -np.ones(g2.n + 1, int); c = 0
    for i in np.nonzero(U)[0]:
        if comp[i] >= 0:
            continue
        comp[i] = c; dq = deque([i])
        while dq:
            u = dq.popleft()
            near = set(g2.nb[u].tolist()); near |= set(g2.nb[[q for q in near if q < g2.n]].ravel().tolist())
            for q in near:
                if q < g2.n and U[q] and comp[q] < 0:
                    comp[q] = c; dq.append(q)
        c += 1
    M = comp[g2.grid]                       # (2L, nloc)
    return bool(((M[:L] >= 0) & (M[:L] == M[L:])).any())


def fate(g, bg, x, u0, maxgen=4000):
    r = g.track(bg, x, u0, span=g.N - 1, maxgen=maxgen)
    lo, hi = r['lo'], r['hi']
    away = bool(((lo >= 3) | (hi <= -3))[r['cnt'] > 0].any())
    if away:
        return 'pulse', r
    return {0: 'heals', 1: 'stays', 2: 'runs', 3: 'open'}[r['ret']], r


def sides_of(r, N):
    lo, hi = r['lo'], r['hi']
    out = {}
    for name, ext in (('+', hi), ('-', -lo)):
        other = -lo if name == '+' else hi
        tw = int(np.argmax(other >= N // 2 - 3)) if (other >= N // 2 - 3).any() else len(other)
        e = ext[:tw]
        if len(e) and e.max() >= 12:
            arr = [int(np.argmax(e >= k)) for k in range(1, int(e.max()) + 1)]
            reg = regular(np.diff(arr))
            out[name] = list(reg) if reg else 'irregular'
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('m1', type=int); ap.add_argument('m2', type=int); ap.add_argument('L', type=int); ap.add_argument('nsoup', type=int)
    ap.add_argument('--rho', type=float, default=0.4); ap.add_argument('--seed', type=int, default=1); ap.add_argument('--R', type=int, default=40)
    ap.add_argument('--maxgen', type=int, default=20000)
    a = ap.parse_args()
    L = a.L
    g1 = tube(a.m1, a.m2, L); g2 = tube(a.m1, a.m2, 2 * L)
    per, gen, states = g1.soups(a.nsoup, a.rho, a.seed, a.maxgen)
    stats = Counter(); wires = {}
    for s in range(a.nsoup):
        P = int(per[s]); st = states[s]
        if P == 0:
            stats['unsettled'] += 1; continue
        if st[:g1.n].sum() == 0:
            stats['dies'] += 1; continue
        M = g1.as_grid(st)
        if any((np.roll(M, d, axis=0) == M).all() for d in range(1, L) if L % d == 0):
            stats['shorter repeat'] += 1; continue
        st2 = g2.from_grid(np.concatenate([M, M]))
        if not is_wire(g2, st2, P):
            stats['finite objects'] += 1; continue
        pops = []; x = st
        for _ in range(P):                      # per phase: population and the histogram of live cells by live-neighbour count
            cnt = x[g1.nb].sum(1)[x[:g1.n] == 1]
            pops.append((int(x.sum()),) + tuple(np.bincount(cnt, minlength=13).tolist())); x = g1.run(x, 1)
        rots = [tuple(pops[i:] + pops[:i]) for i in range(P)]
        key = (P, min(rots + [tuple(reversed(r)) for r in rots]))
        stats['wire'] += 1
        if key not in wires:
            wires[key] = st
    print(f'tube {a.m1}x{a.m2}, ring of {L} cubes ({g1.n} cells), {a.nsoup} soups at rho {a.rho}: {dict(stats)}; distinct wires {len(wires)}', flush=True)
    # ---- tests
    R = a.R; gl = tube(a.m1, a.m2, L * R, unit=L); u0 = R // 2
    rng = random.Random(a.seed)
    out = open(os.path.join(sg.SCR, 'harvest.jsonl'), 'a')
    tot = Counter(); nfr = 0
    for (P, pops), st in sorted(wires.items(), key=lambda kv: kv[0]):
        pops = [q[0] for q in pops]
        cells = sorted(g1.cells_of(st))
        bg0 = gl.state(sg.lift_periodic(cells, [(L, 0, -L)], [range(R)]))
        orb = gl.orbit(bg0, P - 1)
        keep = np.ones(gl.n + 1, np.uint8); keep[:gl.n] = gl.unit != u0
        inu = np.nonzero(gl.unit == u0)[0]
        res = Counter(); fronts = Counter(); pulses = []
        phases = range(P) if P <= 24 else sorted(rng.sample(range(P), 24))
        for t in phases:
            f, r = fate(gl, orb[t], orb[t] & keep, u0)
            res['cut:' + f] += 1
            if f == 'runs':
                fronts[json.dumps(sides_of(r, R), sort_keys=True)] += 1
            if f == 'pulse':
                pulses.append(dict(kind='cut', t=t))
        for k in range(24):
            t = rng.randrange(P); x = orb[t].copy()
            seed = rng.getrandbits(30); r2 = random.Random(seed)
            for i in inu:
                x[i] = r2.random() < a.rho
            f, r = fate(gl, orb[t], x, u0)
            res['hit:' + f] += 1
            if f == 'runs':
                fronts[json.dumps(sides_of(r, R), sort_keys=True)] += 1
            if f == 'pulse':
                pulses.append(dict(kind='hit', t=t, seed=seed))
        rec = dict(m1=a.m1, m2=a.m2, L=L, period=P, pops=[min(pops), max(pops)], cells=[list(c) for c in cells], results=dict(res),
                   fronts=dict(fronts), pulses=pulses, rho=a.rho, seed=a.seed)
        out.write(json.dumps(rec) + '\n'); out.flush()
        tot.update(res); nfr += bool(fronts)
        if fronts or pulses or any(k.endswith('open') for k in res):
            print(f'  wire P{P} pops {min(pops)}-{max(pops)}: {dict(sorted(res.items()))} fronts {dict(fronts)} PULSES {len(pulses)}', flush=True)
    print(f'  tests over {len(wires)} wires: {dict(sorted(tot.items()))}; wires with a front: {nfr}', flush=True)


if __name__ == '__main__':
    main()
