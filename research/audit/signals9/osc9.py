#!/usr/bin/env python3
"""osc9 (review of signals push 9): the period-3 oscillator P3.15f of research/atlas/catalogue.jsonl beside wire B,
by this review's own enumeration (st9.c; `orc` replays chosen cases on reference/oracle.py).

    python3 osc9.py scan [ID]      every placement of the object: stands beside plain wire?  a right-going and a
                                   left-going pulse at each of the three arrival timings; then, beside d^k f at every
                                   offset of the wall, the same pulses for k = 1..KMAX
    python3 osc9.py show GI B C    one placement in detail
    python3 osc9.py orc            the cases of out/osc_cases.json on the oracle

A placement is (gi, (0, b, c)): the cells g(orbit[0]) + (0, b, c) at an even generation of the wire, g = PERMS[gi]
(signed permutation), every (b, c) even for which the closed neighbourhoods of the two unions meet and the object's
union has no cell of the wire's union; slides along the wire are the same placement.  The object has period 3 and
the wire 2, so every relative phase occurs in one orbit.  A pulse is born by removing ONE stator at an even
generation; its arrival timing relative to the oscillator is changed by moving the birth place one unit (2
generations): three birth places = the three timings.
Reference unit of a placement: u_obj = the unit (x >> 1) of its union's largest x; the wall offset e means the first d
of the stretch is at unit u_obj + e.
"""
import sys, json, time
from a9 import *

CAT = os.path.join(ROOT, 'research', 'atlas', 'catalogue.jsonl')
N, FIRST = 64, 0
U0 = 30                                            # the object's reference unit on the test wire
KMAX = 8


def load(oid):
    for l in open(CAT):
        d = json.loads(l)
        if d['id'] == oid:
            return frozenset(map(tuple, d['cells'])), d['period']
    raise KeyError(oid)


def halo(cells):
    out = set(cells)
    for q in cells:
        out.update(nbrs(q))
    return out


def placements(orb):
    union = frozenset().union(*orb)
    W0 = frozenset(q for u in range(-9, 10) for q in unit_cells(7, u))
    W1 = frozenset(q for q in run(frozenset(q for u in range(-12, 13) for q in unit_cells(7, u)), 1) if -9 <= q[0] >> 1 < 10)
    wun = W0 | W1
    whalo = halo(frozenset(q for q in wun if -1 <= q[0] >> 1 <= 1))
    seen = set(); out = []
    for gi, g in enumerate(PERMS):
        gun = [app(g, q) for q in union]; base = [app(g, q) for q in orb[0]]
        gh = halo(gun)
        cand = set()
        for a in whalo:
            for b in gh:
                d = sub(a, b)
                if d[0] % 2 == 0 and d[1] % 2 == 0 and d[2] % 2 == 0:
                    cand.add((d[1], d[2] + d[0]))
        for b, cc in sorted(cand):
            un = frozenset((x, y + b, z + cc) for x, y, z in gun)
            if un & wun:
                continue
            cells = frozenset((x, y + b, z + cc) for x, y, z in base)
            x0 = min(q[0] for q in un) >> 1
            key = (frozenset(tr(q, -x0) for q in cells), frozenset(tr(q, -x0) for q in un))
            if key in seen:
                continue
            seen.add(key)
            out.append((gi, (0, b, cc), cells, un))
    return out


def W(k=0, wall=None):
    wd = list('7' * N)
    if k:
        for j in range(k):
            wd[wall + j - FIRST] = 'd'
        wd[wall + k - FIRST] = 'f'
    return ''.join(wd)


class Case:
    def __init__(self, cells, un, P):
        uo = max(q[0] for q in un) >> 1
        self.obj0 = frozenset(tr(q, U0 - uo) for q in cells)
        self.P = P
        self.orb = [self.obj0]
        for _ in range(2 * P - 1):
            self.orb.append(run(self.orb[-1], 1))
        self.orb_un = frozenset().union(*self.orb)

    def obj(self, t):
        return self.orb[t % self.P]

    def stands(self, word):
        S = wire(word, first=FIRST) | self.obj0
        if len(S) != len(wire(word, first=FIRST)) + len(self.obj0):
            return False
        per = 2 * self.P if self.P % 2 else self.P
        return run(S, per) == S and run(S, 6 * per) == S

    def shoot(self, word, rem, T=None, see=None):
        """remove the stators `rem` at generation 0; returns (final class, what was seen leaving on the left); with
        `see` (a test on the letters of an exact state) the class 'plain' becomes 'eaten' unless the test held once.
        The state is looked at every 6 generations (a multiple of both periods) and the run stops when it repeats."""
        per = 6 if self.P == 3 else (2 * self.P if self.P % 2 else self.P)
        T = T or 40 * per
        saw = see is None
        base = wire(word, first=FIRST)
        s = (base | self.obj0) - set(rem)
        seen = None; prev = None; t = 0
        while t < T:
            s = run(s, per, cap=60000); t += per
            if s is None or len(s) > 2500:
                return 'burn', seen
            if (seen is None or not saw) and t >= 18 and self.obj(t) <= s:
                lw = letters(s - self.obj(t), N, FIRST)
                if '?' not in lw and s == wire(lw, first=FIRST) | self.obj(t):
                    if seen is None and 'd' not in lw and 'f' not in lw and 'b' in lw:
                        seen = rle(lw.strip('7'))
                    if not saw and see(lw):
                        saw = True
            if s == prev and t >= 60:
                break
            prev = s
        if s != run(s, per):
            return 'changing', seen
        if self.obj(t) <= s:
            lw = letters(s - self.obj(t), N, FIRST)
            if '?' not in lw and s == wire(lw, first=FIRST) | self.obj(t):
                return (('plain' if saw else 'eaten') if set(lw) == {'7'} else 'store:' + rle(lw.strip('7'))), seen
            return 'wire changed, object as it would be', seen
        return 'object changed', seen


def plain_tests(cs):
    """the six pulse tests on plain wire: 'pass' if everything is restored and the pulse was seen beyond the object"""
    res = []
    for dirn in 'RL':
        for j in range(3):
            if dirn == 'R':
                rem = [RST(U0 - 12 - j)]; see = lambda lw: '6f' in lw[U0 + 6 - FIRST:]
            else:
                rem = [LST(U0 + 12 + j)]; see = lambda lw: 'b' in lw[:U0 - 8 - FIRST]
            cls, seen = cs.shoot(W(), rem, see=see)
            res.append(cls)
    return res


def orbit_of(oid):
    cells, P = load(oid)
    orb = [cells]
    for _ in range(P - 1):
        orb.append(step_set(orb[-1]))
    assert step_set(orb[-1]) == cells
    return orb, P


def scan(oid):
    orb, P = orbit_of(oid)
    pl = placements(orb)
    print(f'# {oid}: period {P}, {len(orb[0])} cells, union {len(frozenset().union(*orb))}; {len(pl)} placements')
    good = []; nstand = 0; tally = {}
    for gi, t, pc, un in pl:
        cs = Case(pc, un, P)
        if not cs.stands(W()):
            continue
        nstand += 1
        res = plain_tests(cs)
        key = ''.join('p' if r == 'plain' else 'e' if r == 'eaten' else 'x' for r in res)
        tally[key] = tally.get(key, 0) + 1
        good.append({'gi': gi, 't': list(t), 'plain': key})
    print(f'# {nstand} stand beside plain wire; pulse outcomes, R at three timings then L at three timings (p = the pulse '
          f'passed and everything is as it would have been, e = the pulse vanished and everything is as it would have been, '
          f'x = anything else): {dict(sorted(tally.items()))}')
    json.dump({'id': oid, 'placements': len(pl), 'standing': good}, open(os.path.join(HERE, 'out', f'osc_plain_{oid}.json'), 'w'))


def wall(oid, only=None, ks=range(1, KMAX + 1), erange=range(-5, 6)):
    orb, P = orbit_of(oid)
    pl = {(gi, t): (pc, un) for gi, t, pc, un in placements(orb)}
    plain = {(d['gi'], tuple(d['t'])): d['plain'] for d in json.load(open(os.path.join(HERE, 'out', f'osc_plain_{oid}.json')))['standing']}
    sel = [key for key in sorted(plain) if (only is None or key in only)]
    print(f'# {oid}: {len(sel)} placements; beside d^3 f with its first unit at u_obj + e, e = {erange[0]}..{erange[-1]}: a right-going pulse '
          f'at the three timings.  Listed: every (placement, e) at which the stretch stands and some timing releases it '
          f'(the wire plain and the object as it would have been at the end); then k = {ks[0]}..{ks[-1]} for those.')
    trig = []; nst = 0; kinds = {}
    for key in sel:
        pc, un = pl[key]; cs = Case(pc, un, P)
        for e in erange:
            wl = U0 + e
            if not cs.stands(W(3, wl)):
                kinds['does not stand'] = kinds.get('does not stand', 0) + 1
                continue
            nst += 1
            outs = [cs.shoot(W(3, wl), [RST(wl - 12 - j)]) for j in range(3)]
            sig = tuple(sorted({cls if cls != 'plain' else 'released' for cls, seen in outs}))
            kinds[sig] = kinds.get(sig, 0) + 1
            if any(cls == 'plain' for cls, seen in outs):
                trig.append((key, e, outs))
    print(f'# {nst} (placement, e) stand; by the set of outcomes over the three timings: {kinds}')
    cases = []
    for key, e, outs3 in trig:
        pc, un = pl[key]; cs = Case(pc, un, P); wl = U0 + e
        print(f'gi {key[0]} t {key[1]} e {e:+d}   (plain wire: {plain[key]})')
        allrel = True
        for j in range(3):
            row = []
            for k in ks:
                if not cs.stands(W(k, wl)):
                    row.append(f'k={k}: does not stand'); allrel = False; continue
                cls, seen = cs.shoot(W(k, wl), [RST(wl - 12 - j)])
                allrel &= cls == 'plain'
                row.append(f'k={k}: {"released" if cls == "plain" else cls}' + (f' [{seen}]' if seen else ''))
            print(f'     timing {j}: ' + '; '.join(row))
        cases.append({'gi': key[0], 't': list(key[1]), 'e': e, 'plain': plain[key], 'all_released': allrel, 'obj0': sorted(cs.obj0)})
    json.dump({'id': oid, 'cases': cases}, open(os.path.join(HERE, 'out', f'osc_cases_{oid}.json'), 'w'))
    print(f'# {len(cases)} (placement, e) with a release at some timing; released at every timing and every k: '
          f'{sum(c["all_released"] for c in cases)}; of those with all six plain-wire tests passed: '
          f'{sum(c["all_released"] and c["plain"] == "pppppp" for c in cases)}')


if __name__ == '__main__':
    t0 = time.time()
    oid = 'P3.15f'
    if sys.argv[1] == 'scan':
        scan(oid)
    elif sys.argv[1] == 'wall':
        only = None
        if '--push' in sys.argv:       # the eight placements the push names
            only = {(gi, t) for gi in (12, 14, 20, 22, 25, 27, 33, 35) for t in ((0, 0, 10), (0, 2, 10))}
        if '--part' in sys.argv:
            i, n = map(int, sys.argv[sys.argv.index('--part') + 1].split('/'))
            orb, P = orbit_of(oid)
            keys = sorted({(d['gi'], tuple(d['t'])) for d in json.load(open(os.path.join(HERE, 'out', f'osc_plain_{oid}.json')))['standing']})
            only = set(keys[i::n])
        wall(oid, only)
    print(f'# {time.time() - t0:.0f} s')
