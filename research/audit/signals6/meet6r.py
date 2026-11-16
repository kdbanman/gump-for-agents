"""C of REVIEW-signals-6: meetings of the signals on the plain train, own stepper (st6.Batch on the 3x3 tube,
push frame), every offset in a range, outcome compared cell for cell with the push's claim, fronts proved for ever
by glue6.prove.

    python3 meet6r.py opp      opposite directions, offsets d = b - a = 1..41 of the parity allowed (~1 min)
    python3 meet6r.py same     same direction, spacings 1..12                                    (~1 min)
    python3 meet6r.py words    E against 2 holes at spacings s = 1..14 rakes, 3..6 holes, U against holes (~3 min)

A configuration is a list of (kind, unit) at train phase 1, generation 0 (kind in E, U, H, K0, K3).
"""
import sys, time
from collections import Counter
import numpy as np
import st6
from st6 import tr, trs, unit_of, units
import trains6 as T
import kinds6
import glue6

T.check()
ATOMS = kinds6.ATOMS     # name -> (parity, cells at phase 1, velocity per 4 generations relative to the TUBE)
DIRS = {'E': +1, 'U': +1, 'H': -1, 'K0': -1, 'K3': -1}
WB = [frozenset(tuple(c) for c in w) for w in T.J['wireB']]


def sigcells(k, u):
    par, cells, _ = ATOMS[k]
    assert u % 2 == par, (k, u)
    return trs(cells, u)


def free(sigs, t):
    """Where the signals are at generation t (t even) with no interaction, as a difference from train(1+t)."""
    j = t // 2
    d = frozenset()
    for k, u in sigs:
        d = d ^ trs(sigcells(k, u + (DIRS[k] + 1) * j), -j)
    return d


class Runner:
    def __init__(self, A):
        self.A = A
        self.B = st6.Batch([c for u in range(-A, A) for c in kinds6.tube3(u)])

    def run(self, configs, T_, keep=None):
        """Returns per config the list of states (frozensets) at the generations in keep, and differences."""
        B = self.B; A = self.A
        S = np.zeros((len(configs) + 1, B.n + 1), np.uint8)
        P = T.train(1, -A, A); S[0] = B.vec(P)
        for i, sg in enumerate(configs):
            x = P
            for k, u in sg:
                x = x ^ sigcells(k, u)
            S[i + 1] = B.vec(x)
        keep = set(range(T_ + 1)) if keep is None else set(keep)
        out = {}
        for t in range(T_ + 1):
            if t in keep:
                out[t] = S.copy()
            if t < T_:
                S = B.step(S)
        return out

    def diff(self, snap, i):
        d = self.B.set_of(snap[i + 1] ^ snap[0])
        return d

    def state(self, snap, i):
        return self.B.set_of(snap[i + 1])

    def exact(self, d, t):
        return all(-self.A + t + 1 <= unit_of(c) < self.A - t - 1 for c in d)


def wireB_med(t):
    """wire B base at generation t (the train phase 1 or 3 generations use WB[1], as the push states; checked)."""
    return lambda u: WB[(t + 1) % 2] if True else None


def holed_med(t, L=60):
    S = T.train(1, -L, L)
    for u in range(-L, L):
        if u % 2 == 1:
            S = S ^ sigcells('H', u)
    for _ in range(t % 4):           # generation t of these runs is train phase t + 1
        S = st6.step(S)
    bases = [glue6.base_at(S, u) for u in (0, 1)]
    return lambda u: bases[u % 2]


def outcome(R, snaps, i, T_, sigs):
    d = R.diff(snaps[T_], i)
    assert R.exact(d, T_), 'inexact'
    if not d:
        return 'cancel'
    if d == free(sigs, T_):
        return 'pass'
    if (T_ - 8) % 4 == 0:
        D = {T_ - 8 + 1 + k: R.diff(snaps[T_ - 8 + k], i) for k in (0, 4, 8)} if all(T_ - 8 + k in snaps for k in (0, 4, 8)) else None
        if D is not None:
            r = kinds6.read(D, T_ - 7)
            if r not in (('break',), ('vanish',)) and not any(str(x).startswith('new') for x in r):
                return 'signals ' + ','.join(r)
    S0 = R.state(snaps[T_ - 4], i); S4 = R.state(snaps[T_], i)
    d0 = R.diff(snaps[T_ - 4], i)
    lo = min(unit_of(c) for c in d0) - 12; hi = max(unit_of(c) for c in d) + 12
    for name, medf in (('wireB', wireB_med), ('holed', holed_med)):
        med = medf(T_ - 4)
        ok, desc = glue6.prove(S0, S4, lo, hi, med)
        if ok:
            return f'front[{name}] {desc}'
    return 'other'


def opp():
    R = Runner(320)
    Tm = 200
    for k, med in (('wireB', wireB_med(0)), ('wireB', wireB_med(1))):
        assert glue6.check_medium(med, 1, st6.step), 'wire B is not a period-4 orbit'
    for ph in (0, 1, 2, 3):
        assert glue6.check_medium(holed_med(ph), 2, st6.step)
    print('media: wire B and the holed train are orbits with Phi = id (interior of a 80-unit piece): ok')
    for up in ('E', 'U'):
        for dn in ('H', 'K0', 'K3'):
            a = ATOMS[up][0]
            ds = [d for d in range(1, 42) if (a + d) % 2 == ATOMS[dn][0]]
            confs = [[(up, a), (dn, a + d)] for d in ds]
            snaps = R.run(confs, Tm)
            # one orbit: run(d+2) at t+2 == run(d) at t moved +1 unit, every t = 0..Tm-2
            orb = []
            for i in range(1, len(ds)):
                good = all(R.diff(snaps[t + 2], i) == trs(R.diff(snaps[t], i - 1), 1) for t in range(0, Tm - 1))
                orb.append((ds[i - 1], good))
            first_ok = next((d for d, g in orb if g and all(gg for dd, gg in orb if dd >= d)), None)
            outs = Counter(outcome(R, snaps, i, Tm, confs[i]).split(' pieces')[0] for i in range(len(ds)))
            o0 = outcome(R, snaps, len(ds) - 1, Tm, confs[-1])
            print(f'{up} meets {dn}: offsets {ds[0]}..{ds[-1]}; one orbit for every pair of offsets d, d+2 with d >= '
                  f'{first_ok} (failures: {[d for d, g in orb if not g]}); outcome at generation {Tm} by offset: {dict(outs)}')
            print(f'    at offset {ds[-1]}: {o0}', flush=True)


def same():
    R = Runner(200)
    Tm = 120
    for grp in (('E', 'U'), ('H', 'K0', 'K3')):
        for x in grp:
            for y in grp:
                confs = []; sps = []
                for sp in range(1, 13):
                    ua = ATOMS[x][0]; ub = ua + sp
                    if ub % 2 != ATOMS[y][0]:
                        continue
                    sg = [(x, ua), (y, ub)]
                    if sigcells(x, ua) & sigcells(y, ub):
                        continue
                    confs.append(sg); sps.append(sp)
                snaps = R.run(confs, Tm, keep=[0, 2, Tm])
                res = []
                for i, sp in enumerate(sps):
                    d = R.diff(snaps[Tm], i)
                    assert R.exact(d, Tm)
                    passT = d == free(confs[i], Tm)
                    # proof for ever: the two-generation identity from generation 0
                    pr = R.diff(snaps[2], i) == free(confs[i], 2)
                    res.append(f'{sp}:{"P" if pr else ("p" if passT else "x")}')
                print(f'  {x} below, {y} above (spacing in units: P = rides together, proved by the 2-generation '
                      f'identity; p = unchanged at {Tm} only; x = not): {" ".join(res)}', flush=True)


def words():
    R = Runner(420)
    Tm = 240
    confs = []; names = []
    for s in range(1, 15):
        confs.append([('E', 0), ('H', 21), ('H', 21 + 2 * s)]); names.append(f'E, 2 holes {s} rakes apart')
    for n in (3, 4, 5, 6):
        for s in (3, 4):
            confs.append([('E', 0)] + [('H', 21 + 2 * s * i) for i in range(n)]); names.append(f'E, {n} holes, {s} apart')
    confs.append([('E', 0), ('H', 21), ('H', 27), ('H', 33), ('H', 41)]); names.append('E, holes at 21,27,33,41')
    confs.append([('E', 0), ('H', 21), ('H', 27), ('H', 35)]); names.append('E, holes at 21,27,35')
    confs.append([('E', 0), ('H', 21), ('H', 29), ('H', 33)]); names.append('E, holes at 21,29,33')
    snaps = R.run(confs, Tm, keep=list(range(100, Tm + 1, 20)) + [Tm - 4])
    for i, nm in enumerate(names):
        o = outcome(R, snaps, i, Tm, confs[i])
        # B' stretch: the standing pieces' units at generations 100..240
        S = R.state(snaps[Tm], i)
        d = R.diff(snaps[Tm], i)
        lo = min(unit_of(c) for c in d); hi = max(unit_of(c) for c in d)
        med = wireB_med(Tm)
        nonB = [u for u in range(lo + 4, hi - 4) if glue6.base_at(S, u) != med(u)]
        hist = []
        for t in range(100, Tm + 1, 20):
            St = R.state(snaps[t], i); dt = R.diff(snaps[t], i)
            l2 = min(unit_of(c) for c in dt); h2 = max(unit_of(c) for c in dt)
            hist.append([u for u in range(l2 + 4, h2 - 4) if glue6.base_at(St, u) != wireB_med(t)(u)])
        stand = all(h == hist[-1] for h in hist)
        print(f'{nm}: {o}\n    non-wire-B units inside at t = 100..{Tm} step 20: {"standing " + str(hist[-1]) if stand else hist}', flush=True)


if __name__ == '__main__':
    t0 = time.time()
    {'opp': opp, 'same': same, 'words': words}[sys.argv[1]]()
    print(f'{time.time() - t0:.0f} s')
