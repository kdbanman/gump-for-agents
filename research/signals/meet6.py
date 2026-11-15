#!/usr/bin/env python3
"""Meetings of signals on the plain rake train (sixth push, README section 31).

    python3 meet6.py            (about 1 min)

Signals (echo6.SIG1, proved to ride the train by prove_echo.py): up the stream E (the echo), U; down H (the hole),
K0.  At train phase 1 each kind sits at units of one parity, so two signals moving in opposite directions have one
meeting up to translation and time shift (README section 31): the script runs each pair at four offsets and checks
that the four runs are one orbit (each is the previous one two generations later, moved), then classifies the
outcome at generation T = 120:
  pass     the difference is the two signals at the places they would have reached without meeting;
  delayed  the two signals, at other places (the shift is printed);
  cancel   the difference is empty: the plain train, exactly;
  front    two edges with a uniform medium between, growing: the medium is described (its unit cells at the two
           parities, its spatial period) and each edge is checked to be rigid (S(t+4) = S(t) moved two units, up or
           down, on a window round the edge, t = 80..116);
  other    printed.
Then words: E against two holes s rakes apart (s = 1..10), E against a hole and a K0, U against two holes.
Stepping: sg.step_set on a finite piece of train (exact on units -A+t+1..A-t-1; echo6.evolve raises if the
difference leaves that window).
"""
import sys
import echo6 as E, sg

T = 120


def run(sigs, T=T):
    A = max(abs(u) for _, u in sigs) + 2 * T + 8
    S = E.train(1, -A, A)
    for K, u in sigs:
        S ^= E.sig(K, u)
    P = E.train(1, -A, A)
    Ss, Ps = [S], [P]
    for t in range(T):
        S = sg.step_set(S); P = sg.step_set(P)
        Ss.append(S); Ps.append(P)
    D = [a ^ b for a, b in zip(Ss, Ps)]
    if not E.exact_ok(D, A):
        raise E.Inexact(sigs)
    return Ss, D, A


def medium(S, lo, hi, t):
    """Cells of units lo..hi-1 of S, as per-unit base sets; returns (spatial period 1 or 2 or None, base sets)."""
    b = [frozenset(E.tr(c, -u) for c in E.units(S, u, u + 1)) for u in range(lo, hi)]
    for p in (1, 2, 4):
        if all(b[i] == b[i + p] for i in range(len(b) - p)):
            return p, b[:p]
    return None, b[:4]


def classify(sigs):
    Ss, D, A = run(sigs)
    fin = D[T]
    if fin == E.free(sigs, T):
        return 'pass', None
    if not fin:
        # when did it vanish
        tv = max(t for t in range(T + 1) if D[t]) + 1
        return 'cancel', f'the difference is empty from generation {tv}'
    r = E.read(fin, T)
    if r is not None and len(fin) < 20:
        return 'signals', str(r)
    us = sorted({E.unit_of(c) for c in fin})
    lo, hi = us[0], us[-1]
    # edges and their speeds (units per 4 generations), from generation 80 to 120
    us80 = sorted({E.unit_of(c) for c in D[80]})
    vlo = (lo - us80[0]) / 10; vhi = (hi - us80[-1]) / 10
    mid = (lo + hi) // 2
    p, base = medium(Ss[T], mid - 8, mid + 8, T)
    p1, base1 = medium(Ss[T - 1], mid - 8, mid + 8, T - 1)
    # rigidity of each edge: S(t+4) = S(t) moved by 4*v units, on a window of 12 units round the edge
    rig = True
    for t in range(80, T - 3):
        ul = min(E.unit_of(c) for c in D[t]); uh = max(E.unit_of(c) for c in D[t])
        for (ue, v) in ((ul, round(4 * vlo)), (uh, round(4 * vhi))):
            a = E.units(Ss[t + 4], ue + v - 6, ue + v + 6)
            b = E.units(E.trs(Ss[t], v), ue + v - 6, ue + v + 6)
            rig &= (a == b)
    desc = (f'edges at units {lo}..{hi}; lower edge moves {vlo:+.2f}, upper {vhi:+.2f} units per 4 generations; '
            f'both edges rigid t=80..116: {rig}; medium between: spatial period {p} '
            f'(even generation: {[sorted(x) for x in base]}; odd: {[sorted(x) for x in base1]})')
    return 'front', desc


def same_orbit(s1, s2):
    """s2 is s1 with the down signal 2 units further: is run(s2) at t+2 equal to run(s1) at t, moved?"""
    _, D1, _ = run(s1, 60); _, D2, _ = run(s2, 62)
    # s2 two generations on is s1 moved by +1 unit (train(3) = train(1) moved -1, train(1) has period 2 units)
    return all(D2[t + 2] == E.trs(D1[t], +1) for t in range(0, 61))


if __name__ == '__main__':
    E.check_train()
    allok = True
    print('== one meeting per pair (opposite directions) ==')
    for up in ('E', 'U'):
        for dn in ('H', 'K0'):
            uu = E.SIG1[up][0]; base = 20 + E.SIG1[dn][0]
            s1 = [(up, uu), (dn, base)]; s2 = [(up, uu), (dn, base + 2)]
            orb = same_orbit(s1, s2)
            k, desc = classify(s1)
            allok &= orb
            print(f'{up} meets {dn}: start {s1}: one orbit over offsets (checked for two): {orb}: {k.upper()}  {desc or ""}', flush=True)
    print('== same direction: rigid pairs (each kind behind each kind at spacing 2..8) ==')
    for a in ('E', 'U'):
        for b in ('E', 'U'):
            res = []
            for sp in range(1, 9):
                ua = E.SIG1[a][0]; ub = ua + sp
                if ub % 2 != E.SIG1[b][0]:
                    continue
                s = [(a, ua), (b, ub)]
                try:
                    k, _ = classify(s)
                except Exception as e:
                    k = 'overlap'
                res.append((sp, k))
            print(f'  {a} then {b} (spacing in units): {res}')
    for a in ('H', 'K0'):
        for b in ('H', 'K0'):
            res = []
            for sp in range(1, 9):
                ua = E.SIG1[a][0]; ub = ua + sp
                if ub % 2 != E.SIG1[b][0]:
                    continue
                s = [(a, ua), (b, ub)]
                try:
                    k, _ = classify(s)
                except Exception:
                    k = 'overlap'
                res.append((sp, k))
            print(f'  {a} then {b} (spacing in units): {res}')
    print('== E against words ==')
    for s in range(1, 11):
        sigs = [('E', 0), ('H', 21), ('H', 21 + 2 * s)]
        k, desc = classify(sigs)
        print(f'E, two holes {s} rakes apart: {k} {desc or ""}', flush=True)
    for w in ([('E', 0), ('K0', 20), ('H', 23)], [('E', 0), ('H', 21), ('K0', 24)], [('U', 1), ('H', 21), ('H', 23)],
              [('U', 1), ('K0', 20), ('K0', 22)], [('E', 0), ('K0', 20), ('K0', 22)]):
        k, desc = classify(w)
        print(f'{w}: {k} {desc or ""}', flush=True)
    print('ALL ORBIT CHECKS PASS' if allok else 'ORBIT CHECK FAILED')
