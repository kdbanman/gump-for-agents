#!/usr/bin/env python3
"""Pulse search in a closed tube by a transfer graph (de Bruijn graph of space-time columns).  Shares nothing with
research/signals (no SAT, no sg.Geom): own tube geometry from oracle.offsets, own local rule, checked against
oracle.step on a box torus.

    nice -n 10 python3 transfer.py M1 M2 P S [--limit NODES] [--pmax SUCC] [--still]

Tube M1 x M2 along v = (1,0,-1): cells with 1 <= x+y+z <= 2*M1-1 and 1 <= x-y+z <= 2*M2-1 (closed by T2, so exact
for patterns of empty space that start inside).  Cube index of a cell: (x - z) // 4 (translation by v adds 4 to
x - z); every neighbour of a cell lies in its own cube or an adjacent one, so x_{t+1}[k] = f(x_t[k-1], x_t[k], x_t[k+1]).
A *column* C_k is the state of cube k at generations 0 .. P-1.  A bi-infinite sequence of columns is an orbit with
x(P) = x(0) moved S cubes iff at every position k
    (non-wrap) f(C_{k-1,t}, C_{k,t}, C_{k+1,t}) = C_{k,t+1}  (t = 0 .. P-2)    (wrap) f(C_{k-1,P-1}, C_{k,P-1}, C_{k+1,P-1}) = C_{k-S,0}.
Graph: nodes are windows of S+1 consecutive columns.  Forward, a new right column is constrained generation by
generation (all constraints at the old right end are checked); backward, a new left column A gets A_0 from the wrap
constraint whose target it is, A_t (t <= P-2) from the non-wrap constraint at the old left end, and A_{P-1} free
until later constraints (S >= 2; for S = 1 the two are coupled and solved together).
A pulse on a uniform background b (one cube repeated, period dividing P; its column beta) is a path that leaves the
all-beta window and comes back to it: the state differs from b on a finite set D with D(P) = D(0) + S, so for S != 0
it moves.  Conversely every such pulse, of ANY width, is such a cycle.  For each non-empty uniform background the
program closes the set of windows from which the all-beta window is reached (backward search), then if that hits a
limit, the set reachable from it (forward); a closure that is finite and misses the all-beta window proves there is
no pulse of any width on that background.  (The empty background carries no pulse: no finite pattern moves, T2.)
Limits: --limit windows, --pmax successors of one window; beyond them the background is UNDECIDED.  A pulse found is
re-stepped with oracle.step on a box torus.
"""
import argparse, itertools, sys, time
from collections import deque
import numpy as np
from lat import nbrs, Torus

ap = argparse.ArgumentParser()
ap.add_argument('m1', type=int); ap.add_argument('m2', type=int); ap.add_argument('P', type=int); ap.add_argument('S', type=int)
ap.add_argument('--limit', type=int, default=300_000); ap.add_argument('--pmax', type=int, default=200_000)
ap.add_argument('--only', type=int, default=None, help='only this background index')
ap.add_argument('--still', action='store_true', help='only backgrounds that do not change in time')
ap.add_argument('--wire', default=None, help='only the background of this research/signals object (git show bcd5844), phase 0')
a = ap.parse_args()
M1, M2, P, S = a.m1, a.m2, a.P, a.S
inside = lambda c: 1 <= c[0] + c[1] + c[2] <= 2 * M1 - 1 and 1 <= c[0] - c[1] + c[2] <= 2 * M2 - 1
cubeof = lambda c: (c[0] - c[2]) // 4
R = 2 * (M1 + M2) + 8
cells0 = sorted(c for c in itertools.product(range(-R, R + 1), repeat=3)
                if (c[0] & 1) + (c[1] & 1) + (c[2] & 1) == 1 and inside(c) and cubeof(c) == 0)
nc = len(cells0)
mv = lambda c, k: (c[0] + 2 * k, c[1], c[2] - 2 * k)
loc = {c: l for l, c in enumerate(cells0)}
W = nc
blockof = cubeof


def locate(c):
    k = blockof(c)
    return k, loc[mv(c, -k)]


# neighbour lists: for each local cell i of block 0, its in-tube neighbours as (block offset, local index)
NB = []
for i in range(W):
    c = [q for q, v in loc.items() if v == i][0]
    lst = []
    for q in nbrs(c):
        if inside(q):
            k, li = locate(q)
            assert k in (-1, 0, 1)
            lst.append((k, li))
    NB.append(lst)
masks = {d: np.zeros(W, np.int64) for d in (-1, 0, 1)}
for i in range(W):
    for k, li in NB[i]:
        masks[k][i] |= 1 << li
MAXV = 1 << W
print(f'tube {M1}x{M2}: {nc} cells per cube, {MAXV} cube states; (P,S)=({P},{S}); windows of {S + 1} columns', flush=True)
if MAXV > 1 << 24:
    sys.exit('block alphabet too large')
ALL = np.arange(MAXV, dtype=np.int64)
pc = lambda v: np.array([bin(int(x)).count('1') for x in v]) if np.ndim(v) else bin(int(v)).count('1')
# counts contributed by the right-hand block, for every value of it: CC[i][c] = popcount(c & masks[1][i])
POP = np.zeros(MAXV, np.int8)
for b in range(W):
    POP += ((ALL >> b) & 1).astype(np.int8)
CC = np.stack([POP[ALL & masks[1][i]] for i in range(W)])          # (W, MAXV)
CCL = np.stack([POP[ALL & masks[-1][i]] for i in range(W)])
cache = {}; cacheL = {}
CMAX = max(16, (600 << 20) // (8 * MAXV))          # cache entries: about 600 MB per cache


def fvecL(y, z):
    """f(c, y, z) for every c"""
    key = (y, z)
    r = cacheL.get(key)
    if r is not None:
        return r
    out = np.zeros(MAXV, np.int64)
    for i in range(W):
        n = CCL[i] + bin(y & int(masks[0][i])).count('1') + bin(z & int(masks[1][i])).count('1')
        alive = (y >> i) & 1
        out |= ((n == 4) | (n == 5) | ((n == 3) & (alive == 1))).astype(np.int64) << i
    if len(cacheL) < CMAX:
        cacheL[key] = out
    return out


PMAX = a.pmax


class Overflow(Exception):
    pass


def predecessors(n):
    """windows (A, n[0], .., n[S-1]) preceding window n, with lookahead: for t < P-1 some D gives
    f(D, A_t, n[0]_t) = A_{t+1}."""
    C0, C1 = n[0], n[1]
    sets = []
    for t in range(P - 1):                                         # non-wrap at the old left end
        cs = np.nonzero(fvecL(C0[t], C1[t]) == C0[t + 1])[0].tolist()
        sets.append(cs)
    vw = fvecL(C0[P - 1], C1[P - 1])                                # wrap at the old left end: f(A_{P-1}, C0, C1) = C_{m-S,0}
    if S == 1:
        # target is A_0 itself: A_0 = vw[A_{P-1}]
        if P == 1:
            return [((int(x),),) + n[:-1] for x in np.nonzero(vw == ALL)[0]]
        last = list(range(MAXV))
        cands = sets + [last]
        ok = lambda tup: int(vw[tup[-1]]) == tup[0]
    else:
        A0 = f1(n[S - 2][P - 1], n[S - 1][P - 1], n[S][P - 1])      # wrap at window position S-1 targets the new column
        if P == 1:
            return [((A0,),) + n[:-1]]
        sets[0] = [c for c in sets[0] if c == A0]
        cands = sets + [list(range(MAXV))]                          # A_{P-1}: its own wrap is checked S steps later
        ok = None
    if any(len(c) == 0 for c in cands):
        return []
    comp = lambda t, at, an: an in img_l(at, C0[t])
    return [(A,) + n[:-1] for A in chain(cands, comp, ok)]


def fvec(x, y):
    """f(x, y, c) for every c (vector over c)"""
    key = (x, y)
    r = cache.get(key)
    if r is not None:
        return r
    out = np.zeros(MAXV, np.int64)
    for i in range(W):
        n = CC[i] + bin(x & int(masks[-1][i])).count('1') + bin(y & int(masks[0][i])).count('1')
        alive = (y >> i) & 1
        nxt = ((n == 4) | (n == 5) | ((n == 3) & (alive == 1)))
        out |= nxt.astype(np.int64) << i
    if len(cache) < CMAX:
        cache[key] = out
    return out


MK = [(int(masks[-1][i]), int(masks[0][i]), int(masks[1][i])) for i in range(W)]


def f1(x, y, z):
    out = 0
    for i, (ma, mb, mc) in enumerate(MK):
        n = bin(x & ma).count('1') + bin(y & mb).count('1') + bin(z & mc).count('1')
        if n == 4 or n == 5 or (n == 3 and (y >> i) & 1):
            out |= 1 << i
    return out


imgF = {}; imgL = {}


def img_f(x, y):
    """set of f(x, y, d) over all d"""
    r = imgF.get((x, y))
    if r is None:
        r = imgF[(x, y)] = frozenset(np.unique(fvec(x, y)).tolist())
    return r


def img_l(y, z):
    """set of f(d, y, z) over all d"""
    r = imgL.get((y, z))
    if r is None:
        r = imgL[(y, z)] = frozenset(np.unique(fvecL(y, z)).tolist())
    return r


def chain(cands, comp, last_ok=None):
    """all tuples (c_0 .. c_{P-1}) with c_t in cands[t], comp(t, c_t, c_{t+1}) for t < P-1 and last_ok(tuple)"""
    out = []
    def rec(t, pre):
        if t == len(cands):
            if last_ok is None or last_ok(pre):
                out.append(tuple(pre))
                if len(out) > PMAX:
                    raise Overflow
            return
        for c in cands[t]:
            if t == 0 or comp(t - 1, pre[-1], c):
                pre.append(c); rec(t + 1, pre); pre.pop()
    rec(0, [])
    return out


def successors(n):
    """windows (n[1], .., n[S], C) following window n.  C is also required to admit a continuation one step further
    (lookahead): for t < P-1 some D gives f(B_t, C_t, D) = C_{t+1}, and some D gives f(B_{P-1}, C_{P-1}, D) = n[1][0]."""
    A, B = n[-2], n[-1]
    sets = []
    for t in range(P):
        target = B[t + 1] if t + 1 < P else n[0][0]
        cs = np.nonzero(fvec(A[t], B[t]) == target)[0]
        if t == P - 1:
            w = n[1][0] if S >= 1 else None
            cs = [c for c in cs.tolist() if w in img_f(B[t], c)]
        else:
            cs = cs.tolist()
        if len(cs) == 0:
            return []
        sets.append(cs)
    comp = lambda t, ct, cn: cn in img_f(B[t], ct)
    return [n[1:] + (C,) for C in chain(sets, comp)]


# self-check of f against the oracle: random tube states on a ring of 12 blocks
def check():
    rng = np.random.default_rng(0)
    Nb = 12; N = Nb
    T = Torus((2 * N, 24, 2 * N))
    for trial in range(5):
        st = [int(rng.integers(MAXV)) for _ in range(Nb)]
        cells = set()
        for k in range(Nb):
            for i in range(W):
                if (st[k] >> i) & 1:
                    c = [q for q, v in loc.items() if v == i][0]
                    cells.add(mv(c, k))
        h = T.step(T.arr(cells))
        got = set(T.cells(h))
        exp = set()
        for k in range(Nb):
            v = f1(st[(k - 1) % Nb], st[k], st[(k + 1) % Nb])
            for i in range(W):
                if (v >> i) & 1:
                    c = [q for q, vv in loc.items() if vv == i][0]
                    exp.add(T.mod(mv(c, k)))
        assert got == exp, 'local rule disagrees with the oracle'
    print('local rule == oracle.step on 5 random tube rings', flush=True)


check()
rep = lambda u: u
bgs = []
seen = set()
for u in range(1 << nc):
    orb = [u]
    for t in range(P):
        b = rep(orb[-1]); orb.append(f1(b, b, b) & ((1 << nc) - 1))
    if orb[P] == u and u != 0 and (not a.still or orb[1] == u):
        col = tuple(rep(x) for x in orb[:P])
        key = frozenset([col])
        bgs.append(col)
if a.wire:
    import json, subprocess
    from lat import ROOT
    ob = json.loads(subprocess.check_output(['git', '-C', ROOT, 'show', f'bcd5844:research/signals/objects/{a.wire}.json']))
    u0 = 0
    for c in ob['bg']:
        for k in range(-3, 4):
            q = mv(tuple(c), k)
            if cubeof(q) == 0:
                u0 |= 1 << loc[q]
    bgs = [b for b in bgs if b[0] == u0]
    print(f'restricted to the background of {a.wire}: {len(bgs)} column(s)')
print(f'{len(bgs)} non-empty uniform background columns (period dividing {P}, every phase counted)', flush=True)
t0 = time.time(); found = []; undecided = []
for bi, beta in enumerate(bgs):
    if a.only is not None and bi != a.only:
        continue
    Z = (beta,) * (S + 1)

    def explore(forward):
        if forward:
            nxt = successors
        else:
            nxt = predecessors
        try:
            start = [n for n in nxt(Z) if n != Z]
        except Overflow:
            return 'limit', None, None, -1
        seen = set(start); dq = deque(start); parent = {n: Z for n in start}
        while dq:
            node = dq.popleft()
            try:
                nl = nxt(node)
            except Overflow:
                return 'limit', None, None, len(seen)
            for nx in nl:
                if nx == Z:
                    return 'hit', node, parent, len(seen)
                if nx not in seen:
                    seen.add(nx); parent[nx] = node; dq.append(nx)
            if len(seen) > a.limit:
                return 'limit', None, None, len(seen)
        return 'closed', None, None, len(seen)

    rb = explore(False)
    if rb[0] == 'closed':
        continue                                   # all-beta window not on a non-trivial cycle: no pulse
    if rb[0] == 'hit':
        node, parent = rb[1], rb[2]
        path = [node]
        while path[-1] != Z:
            path.append(parent[path[-1]])
        # backward: each step added a column on the left; read the columns left to right
        found.append((bi, list(node) + [q[-1] for q in path[1:]]))
        print(f'  background #{bi} ({bin(beta[0]).count("1")} cells/cube at gen 0): PULSE (backward search, {rb[3]} windows)', flush=True)
        continue
    rf = explore(True)
    if rf[0] == 'closed':
        continue
    if rf[0] == 'hit':
        node, parent = rf[1], rf[2]
        path = [node]
        while path[-1] != Z:
            path.append(parent[path[-1]])
        found.append((bi, [nd[-1] for nd in reversed(path)] + [Z[0]] * S))
        print(f'  background #{bi} ({bin(beta[0]).count("1")} cells/cube at gen 0): PULSE (forward search, {rf[3]} windows)', flush=True)
        continue
    undecided.append(bi)
    print(f'  background #{bi}: UNDECIDED (backward {rb[0]} at {rb[3]} windows, forward {rf[0]} at {rf[3]}; '
          f'limits {a.limit} windows, {PMAX} successors of one window)', flush=True)
print(f'RESULT tube {M1}x{M2} (P,S)=({P},{S}): {len(bgs)} backgrounds, pulses on {len(found)}, undecided {len(undecided)}, '
      f'none on {len(bgs) - len(found) - len(undecided)}; {time.time() - t0:.0f}s', flush=True)
# oracle re-step of every pulse found: the columns (gen 0) between beta's on a ring with 12 beta cubes each side
for bi, cols in found:
    beta = bgs[bi]
    st = [beta[0]] * 12 + [c[0] for c in cols] + [beta[0]] * 12
    N = len(st)
    T = Torus((2 * N, 24, 2 * N))
    cells = set()
    for k in range(N):
        for i in range(W):
            if (st[k] >> i) & 1:
                cells.add(mv(cells0[i], k))
    h = T.arr(cells)
    for _ in range(P):
        h = T.step(h)
    want = {T.mod(mv(c, S)) for c in cells}
    bare = all(c == beta[0] for c in st)
    print(f'  oracle re-step, background #{bi}: ring of {N} cubes, x(P) == x(0) moved {S} cubes: {T.cells(h) == want}; '
          f'not the bare background: {not bare}', flush=True)
