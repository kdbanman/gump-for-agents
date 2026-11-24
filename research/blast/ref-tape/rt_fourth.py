#!/usr/bin/env python3
"""ref-tape, fourth review (2026-11-24): superposition and the meetings of section 31, on reference/oracle.py.

    python3 rt_fourth.py super        tightness of run_or_far's "more than 4n" (max norm, doubled coordinates)
    python3 rt_fourth.py meet         the four meetings on rings: the outcome and the front recurrence of meet_*
    python3 rt_fourth.py edges        U-H against E-H: the upper and lower edges, as unit pictures

Objects: the train (line-C.json rake5/rakef) and the signals (sig6.py) from rt_objects.py; nothing from the Lean side
except the transcribed definitions named below (front m C: units <= m moved two units down, units > m two up;
wire B's two phases BEc = tape letter B, BOc = section 15's odd phase of B).
"""
import random, sys, time
from rt_lib import orc_run, orc_ring, ringwrap, trs, tr, unit_of, is_cell
import rt_objects as O
import rt_dyn
from rt_dyn import report

BEc = frozenset([(0, 1, 2), (0, 1, 4), (1, 0, 0), (1, 0, 2), (1, 0, 4)])
BOc = frozenset([(0, 0, 1), (0, 0, 5), (0, 1, 2), (0, 1, 4), (1, 2, 2)])
assert BEc == O.UNIT_B


def check_super():
    """run_or_far: cells more than 4n apart (max norm) run independently for n generations. Is 4n tight? Look for
    two patterns whose closest cells are exactly 4n apart and which DO interact within n generations."""
    rnd = random.Random(4)
    for n in (1, 2, 3):
        found = None
        t0 = time.time()
        for trial in range(4000):
            if time.time() - t0 > 60:
                break
            R = 2 + n
            A = frozenset(c for c in ((x, y, z) for x in range(-R, 1) for y in range(-R, R + 1) for z in range(-R, R + 1))
                          if is_cell(c) and rnd.random() < 0.45)
            D = 4 * n
            B0 = frozenset(c for c in ((x, y, z) for x in range(0, R + 1) for y in range(-R, R + 1) for z in range(-R, R + 1))
                           if is_cell(c) and rnd.random() < 0.45)
            if not A or not B0:
                continue
            for dist in (D, D + 1):
                # move B along x by an even amount so that the closest pair is exactly `dist` apart (max norm)
                for s in range(0, 4 * D + 8, 2):
                    B = frozenset((c[0] + s, c[1], c[2]) for c in B0)
                    dmin = min(max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2])) for p in A for q in B)
                    if dmin >= dist:
                        break
                if dmin != dist:
                    continue
                oa, ob, oab = orc_run(A, n), orc_run(B, n), orc_run(A | B, n)
                inter = any(oab[t] != oa[t] | ob[t] for t in range(n + 1))
                if dist == D + 1 and inter:
                    report(False, f'n={n}: patterns {dist} apart interact (contradicts run_or_far)')
                    return
                if dist == D and inter and found is None:
                    found = (trial, len(A), len(B))
            if found:
                break
        report(found is not None or n == 3, f'n={n}: two patterns exactly 4n = {4 * n} apart (max norm) that interact within '
               f'{n} generations: {"found, trial %d (%d and %d cells)" % found if found else "none found in the time"}; '
               f'at 4n + 1 apart no interaction in any trial')


def check_super2(n=2):
    """for n = 2: the largest distance (max norm) at which random facing patterns are seen to interact"""
    rnd = random.Random(5)
    best = {}
    t0 = time.time()
    while time.time() - t0 < 90:
        R = 4
        A = frozenset(c for c in ((x, y, z) for x in range(-R, 1) for y in range(-R, R + 1) for z in range(-R, R + 1))
                      if is_cell(c) and rnd.random() < 0.5)
        B0 = frozenset((-c[0], c[1], c[2]) for c in A) if rnd.random() < 0.5 else frozenset(
            c for c in ((x, y, z) for x in range(0, R + 1) for y in range(-R, R + 1) for z in range(-R, R + 1))
            if is_cell(c) and rnd.random() < 0.5)
        for s in range(0, 20, 2):
            B = frozenset((c[0] + s, c[1], c[2]) for c in B0)
            if A & B:
                continue
            d = min(max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2])) for p in A for q in B)
            if d > 4 * n:
                break
            if d in best:
                continue
            oa, ob, oab = orc_run(A, n), orc_run(B, n), orc_run(A | B, n)
            if any(oab[t] != oa[t] | ob[t] for t in range(n + 1)):
                best[d] = True
    print(f'n={n}: distances at which an interaction was found within {n} generations: {sorted(best)} '
          f'(the theorem allows interaction only at distance <= {4 * n})', flush=True)


def front_ring(m, S, L):
    """Lean's front m C = glue m (shiftC (-2) C) (shiftC 2 C), on the ring: the OUTPUT units <= m hold C moved two
    units down, the output units > m hold C moved two units up (units counted relative to m in (-L/2, L/2])"""
    rel = lambda u: ((u - m + L // 2 - 1) % L) - (L // 2 - 1)
    out = set()
    for c in S:
        lo, hi = ringwrap([tr(c, -2)], L), ringwrap([tr(c, 2)], L)
        lo, hi = next(iter(lo)), next(iter(hi))
        if rel(unit_of(lo)) <= 0:
            out.add(lo)
        if rel(unit_of(hi)) > 0:
            out.add(hi)
    return frozenset(out)


MEET = {  # Lean: pair A B a b(n); seam m(n); from generation 2n + g; medium on units m-2..m+3 (None: not checked)
    'UH': ('U', 'H', 1, lambda n: 5 + 2 * n, lambda n: 4 + n, 12, 'wireB'),
    'EH': ('E', 'H', 0, lambda n: 5 + 2 * n, lambda n: 1 + n, 22, 'wireB'),
    'EK': ('E', 'K0', 0, lambda n: 4 + 2 * n, lambda n: 1 + n, 12, None),
}


def pair_ring(A, B, a, b, L, ring1):
    return ring1 ^ ringwrap(trs(O.SIGS[A][1], a) | trs(O.SIGS[B][1], b), L)


def check_meet(T=120, L=160):
    ring = orc_ring(O.train0_cells(0, L - 1), 5, L)
    # U meets K0: vanish, from 2n + 4, for distances 3 + 2n
    for n in (0, 3, 8):
        a, b = 1 + 20, 1 + 20 + 3 + 2 * n
        orb = orc_ring(pair_ring('U', 'K0', a, b, L, ring[1]), 2 * n + 40, L)
        tr_orb = orc_ring(O.train0_cells(0, L - 1), 2 * n + 42, L)
        good = all(orb[t] == tr_orb[1 + t] for t in range(2 * n + 4, 2 * n + 41))
        early = orb[2 * n + 3] != tr_orb[1 + 2 * n + 3]
        report(good and early, f'U-K0 distance {3 + 2 * n}: the plain train from generation {2 * n + 4} to {2 * n + 40}; '
               f'not yet at {2 * n + 3}: {early}')
    for name, (A, B, a0, bf, mf, g, med) in MEET.items():
        for n in (0, 5):
            t0 = time.time()
            a, b, m = a0 + 20, bf(n) + 20, mf(n) + 20      # everything moved 20 units (even) up the ring
            orb = orc_ring(pair_ring(A, B, a, b, L, ring[1]), T, L)
            start = 2 * n + g
            rec = [t for t in range(start, T - 3) if orb[t + 4] != front_ring(m, orb[t], L)]
            early = [t for t in range(max(0, start - 6), start) if orb[t + 4] != front_ring(m, orb[t], L)]
            wrong = orb[start + 4] == front_ring(m + 3, orb[start], L)
            report(not wrong, f'{name} distance {bf(n) - a0}: negative control, the seam 3 units off fails')
            medok = True
            if med == 'wireB':
                for t in range(start, T + 1):
                    loc = frozenset(c for c in orb[t] if unit_of(c) in {(m + i) % L for i in range(-2, 4)})
                    want = ringwrap(frozenset().union(*[trs(BOc if (t - 2 * n) % 2 == 0 else BEc, m + i)
                                                        for i in range(-2, 4)]), L)
                    medok &= loc == want
            span = len({unit_of(c) for c in orb[T] ^ orc_ring(O.train0_cells(0, L - 1), 0, L)[0]})
            report(not rec and medok, f'{name} distance {bf(n) - a0}: X(t+4) = front({mf(n)}) X(t) for every t = {start}..{T - 4} '
                   f'(fails at {rec[:5]}); medium on the seam units {"= wire B" if med else "(not checked)"}: {medok}; '
                   f'the recurrence fails at the earlier generations {early} ({time.time() - t0:.0f} s)')


def picture(S, bg, wb, L, lo, hi):
    """one letter per unit: '.' = the plain train, 'o' = wire B (either phase), '#' = anything else"""
    out = []
    for u in range(lo, hi + 1):
        uu = u % L
        here = lambda c: (c[0] - 2 * uu, c[1], ((c[2] + 2 * uu + L) % (2 * L)) - L)   # unit uu of the torus, at unit 0
        loc = frozenset(here(c) for c in S if unit_of(c) == uu)
        if loc == frozenset(here(c) for c in bg if unit_of(c) == uu):
            out.append('.')
        elif loc in (BEc, BOc):
            out.append('o')
        else:
            out.append('#')
    return ''.join(out)


def check_edges(L=128, T=100):
    tr_orb = orc_ring(O.train0_cells(0, L - 1), T + 2, L)
    res = {}
    for name in ('UH', 'EH'):
        A, B, a0, bf, mf, g, med = MEET[name]
        for n in (0, 4, 9):
            a, b, m = a0 + 10, bf(n) + 10, mf(n) + 10
            orb = orc_ring(pair_ring(A, B, a, b, L, tr_orb[1]), T, L)
            for t in (T - 3, T - 2, T - 1, T):
                pic = picture(orb[t], tr_orb[1 + t], None, L, m - 64, m + 63)
                print(f'{name} n={n} gen {t}: {pic}', flush=True)
            # the upper edge: the topmost non-train unit and the 12 units below it, at the last 4 generations
            tops = []
            for t in (T - 3, T - 2, T - 1, T):
                pic = picture(orb[t], tr_orb[1 + t], None, L, m - 64, m + 63)
                top = max(i for i, ch in enumerate(pic) if ch != '.')
                bot = min(i for i, ch in enumerate(pic) if ch != '.')
                tops.append((pic[top - 13: top + 1], pic[bot: bot + 14]))
            res[(name, n)] = tops
    for side, k in (('upper', 0), ('lower', 1)):
        for i in range(4):
            u = {res[('UH', n)][i][k] for n in (0, 4, 9)}
            e = {res[('EH', n)][i][k] for n in (0, 4, 9)}
            print(f'{side} edge, generation T-{3 - i}: U-H {sorted(u)}  E-H {sorted(e)}  same: {u == e}', flush=True)
    upper_same = all({res[('UH', n)][i][0] for n in (0, 4, 9)} == {res[('EH', n)][i][0] for n in (0, 4, 9)} for i in range(4))
    lower_same = all({res[('UH', n)][i][1] for n in (0, 4, 9)} == {res[('EH', n)][i][1] for n in (0, 4, 9)} for i in range(4))
    print(f'VERDICT edges: lower edges of U-H and E-H the same: {lower_same}; upper edges the same: {upper_same}', flush=True)


if __name__ == '__main__':
    {'super': check_super, 'super2': check_super2, 'meet': check_meet, 'edges': check_edges}[sys.argv[1]]()
    print('ALL PASS' if rt_dyn.ok else 'SOME CHECKS FAILED')
