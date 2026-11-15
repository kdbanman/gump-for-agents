#!/usr/bin/env python3
"""L1 audit: the four pulses, from reference/oracle.py and the stored cells only.

    nice -n 10 python3 l1_pulses.py [name ...]        (names: pulse-A pulse-B pulse-B-left pulse-S; default all)

For each pulse (cells read from research/signals/objects/<name>.json at commit bcd5844 / 896f44b):
 R  rings of many lengths N on the box torus (2N, Hy, 2N) (oracle.step; Hy = 20, and Hy = 40 for N = 40; and the
    cubic oracle.masks torus H = 2N for N = 24): the bare ring has exactly the stated period; at every generation
    t = j*p the state equals generation 0 moved j*s cubes AND equals the bare ring of the same generation XOR the
    defect moved j*s cubes (nothing else differs anywhere on the torus); at every generation every live cell lies in
    the transverse footprint (x+z, y) of the bare wire's diamond tube; run for >= 3 laps and >= 100 periods.
 M  the smallest ring on which the pulse runs (scan N = 3 .. 14 for 3 laps).
 I  infinite lattice, no torus at all: a finite segment of L cubes of the wire (own sparse stepper, checked against
    the oracle by lat.selftest), the pulse put a third of the way in; at every generation, inside the light cone
    window [t+1, L-2-t] (cubes untouched by the cut ends), the state is exactly the bare infinite wire, and at
    even t exactly bare XOR the moved defect; at odd t the difference from bare lies within 4 cubes of the pulse.
"""
import json, subprocess, sys, time
from lat import Torus, ring_torus, shift, wire, sstep, sstep_ring, canon_ring, selftest, ROOT, V

NAMES = sys.argv[1:] or ['pulse-B', 'pulse-B-left', 'pulse-A', 'pulse-S']


def load(name, rev='bcd5844'):
    rev = '896f44b' if name == 'pulse-B-left' else rev
    txt = subprocess.check_output(['git', '-C', ROOT, 'show', f'{rev}:research/signals/objects/{name}.json'])
    return json.loads(txt)


def cube(c):
    return c[0] // 2


def tf(c, N):
    """transverse coordinates (x+z, y), invariant along the wire; x+z taken mod 2N into a centred range"""
    u = (c[0] + c[2]) % (2 * N)
    return u - 2 * N if u > N else u


def ring_check(ob, N, Hy=20, laps=3, minper=100, cubic=False):
    bg = [tuple(c) for c in ob['bg']]; p, s, P = ob['p'], ob['s'], ob['bg_period']
    T = Torus((2 * N,) * 3) if cubic else ring_torus(N, Hy)
    Hy = T.shape[1]
    bare0 = wire(bg, 0, N)
    if len({T.mod(c) for c in bare0}) != len(bare0):
        return dict(ok=False, why='ring images overlap')
    defect = frozenset(tuple(c) for c in ob['defect'])
    K = max(minper, -(-laps * N // abs(s)))
    b = T.arr(bare0); x = T.arr(bare0 ^ defect)
    x0 = T.cells(x)
    # transverse footprint of the bare wire: bounding box in s1 = u + y, s2 = u - y
    fy = lambda c: (c[1] + Hy // 2) % Hy - Hy // 2
    s12 = lambda c: (tf(c, N) + fy(c), tf(c, N) - fy(c))
    bt = [s12(c) for c in bare0]
    bare_fp = (min(a for a, _ in bt), max(a for a, _ in bt), min(b_ for _, b_ in bt), max(b_ for _, b_ in bt))
    lo1, hi1, lo2, hi2 = 1, 5, 1, 5          # the closed 3 x 3 diamond tube of the search (all four bare wires lie in it)
    assert lo1 <= bare_fp[0] and bare_fp[1] <= hi1 and lo2 <= bare_fp[2] and bare_fp[3] <= hi2
    bare_orbit = [T.cells(b)]
    out = dict(ok=True, N=N, shape=T.shape, gens=K * p, tube=bare_fp)
    leak = 0; maxdiff_odd = 0
    for t in range(1, K * p + 1):
        b = T.step(b); x = T.step(x)
        cb, cx = T.cells(b), T.cells(x)
        if t <= P:
            bare_orbit.append(cb)
        for c in cx:
            a1, a2 = s12(c)
            if not (lo1 <= a1 <= hi1 and lo2 <= a2 <= hi2):
                leak += 1
        if t % p == 0:
            j = t // p
            mv = frozenset(T.mod(c) for c in shift(x0, j * s))
            dv = frozenset(T.mod(c) for c in shift(defect, j * s))
            if cx != mv or (cx ^ cb) != dv:
                out.update(ok=False, why=f'mismatch at t={t}'); break
        else:
            maxdiff_odd = max(maxdiff_odd, len(cx ^ cb))
    per = next((q for q in range(1, P + 1) if bare_orbit[q] == bare_orbit[0]), None)
    if per != P:
        out.update(ok=False, why=f'bare period {per} != {P}')
    if leak:
        out.update(ok=False, why=f'{leak} live cells outside the 3x3 tube 1<=s1,s2<=5')
    out['maxdiff_odd'] = maxdiff_odd
    return out


def sparse_ring_check(ob, N, laps=3):
    """ring of N cubes with no transverse images (own sparse stepper modulo N*v): runs `laps` laps exactly?"""
    bg = [tuple(c) for c in ob['bg']]; p, s = ob['p'], ob['s']
    cr = lambda cells: frozenset(canon_ring(c, N) for c in cells)
    bare = cr(wire(bg, 0, N)); defect = cr(tuple(c) for c in ob['defect'])
    if len(bare) != N * len(bg):
        return False
    x = bare ^ defect; x0 = x; b = bare
    K = -(-laps * N // abs(s))
    for t in range(1, K * p + 1):
        x = sstep_ring(x, N); b = sstep_ring(b, N)
        if t % p == 0:
            j = t // p
            if x != cr(shift(x0, j * s)) or (x ^ b) != cr(shift(defect, j * s)):
                return False
    return True


def infinite_check(ob, L=600, T=240):
    bg = [tuple(c) for c in ob['bg']]; p, s, P = ob['p'], ob['s'], ob['bg_period']
    # phases of the bare wire: one representative cube (x//2 == 0) of an infinite wire, from a long finite piece
    piece = wire(bg, -30, 30); reps = []
    for t in range(P + 1):
        reps.append(frozenset(c for c in piece if cube(c) == 0)); piece = sstep(piece)
    assert reps[P] == reps[0]
    defect = frozenset(tuple(c) for c in ob['defect'])
    k0 = L // 3 if s > 0 else 2 * L // 3
    dmin = min(cube(c) for c in defect)
    dshift = k0 - dmin
    D = shift(defect, dshift)
    x = wire(bg, 0, L) ^ D
    bad = None; maxodd = 0
    for t in range(1, T + 1):
        x = sstep(x)
        lo, hi = t + 1, L - 2 - t
        win = frozenset(c for c in x if lo <= cube(c) <= hi)
        bare = frozenset(c for c in shift(reps[t % P], 0) for _ in [0])
        bw = set()
        for k in range(lo, hi + 1):
            bw |= shift(reps[t % P], k)
        bw = frozenset(bw)
        diff = win ^ bw
        pos = k0 + (t * s) // p
        if t % p == 0:
            dv = frozenset(c for c in shift(D, (t // p) * s) if lo <= cube(c) <= hi)
            if diff != dv or len(dv) != len(D):
                bad = t; break
        else:
            if any(abs(cube(c) - pos) > 4 + max(cube(q) for q in D) - min(cube(q) for q in D) for c in diff):
                bad = t; break
            maxodd = max(maxodd, len(diff))
    return dict(ok=bad is None, bad=bad, L=L, T=T, start=k0, end=k0 + T * s // p, maxodd=maxodd, cells_end=len(x))


def main():
    assert selftest()
    for name in NAMES:
        ob = load(name); t0 = time.time()
        print(f'== {name}: bg {len(ob["bg"])} cells/cube, period {ob["bg_period"]}, defect {len(ob["defect"])} cells, (p,s)=({ob["p"]},{ob["s"]})', flush=True)
        for N, Hy, cub in [(9, 20, False), (10, 20, False), (11, 20, False), (13, 20, False), (16, 20, False), (17, 20, False),
                           (24, 0, True), (31, 20, False), (40, 40, False), (64, 20, False)]:
            r = ring_check(ob, N, Hy or 20, cubic=cub)
            print(f'  ring N={N:3d} torus {r.get("shape")}: {"PASS" if r["ok"] else "FAIL " + r["why"]}; {r.get("gens")} gens; '
                  f'bare wire spans s1 {r.get("tube", "")[:2]} s2 {r.get("tube", "")[2:]}, every live cell in 1<=s1,s2<=5; max |diff| at odd gens {r.get("maxdiff_odd")}', flush=True)
        small = [(N, sparse_ring_check(ob, N)) for N in range(3, 15)]
        print('  small rings, no transverse images (N, runs 3 laps):', small, flush=True)
        r = infinite_check(ob)
        print(f'  infinite lattice, segment of {r["L"]} cubes, {r["T"]} gens, pulse from cube {r["start"]} to {r["end"]}: '
              f'{"PASS" if r["ok"] else "FAIL at t=%s" % r["bad"]}; max |diff| at odd gens {r["maxodd"]}; {time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
