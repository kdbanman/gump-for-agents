#!/usr/bin/env python3
"""Constraint search for a reflector at the END of a wire: a cap that sends an arriving pulse back.

    python3 sat_reflect.py T C [--lo 1 --hi 5] [--KS 6] [--timeout 600] [--out FILE] [--obj pulse-B] [--absorb]

Geometry (scat.Region): the wire of objects/OBJ.json runs along (1,0,-1) and is bare (a constant) on units < 2.
Variable cells: units >= 2 of the tube lo <= x+y+z, x-y+z <= hi, cut off by the two planes x+y-z <= C, x-y-z <= C
(T2: nothing is ever born beyond them, so the solution is a semi-infinite wire in EMPTY SPACE, exactly).
Unknowns: Z (generations 0, 1; the cap alone) and X (generations 0..T; the cap with a pulse).  Constraints:
  cap     Z has period 2 (the wire's period) and is the bare wire on units < KS at both generations;
  in      X[0] = Z[0] with the right-moving pulse added, its cells at units 3 and 4;
  out     X[T] = Z[T mod 2] with the LEFT-moving pulse added, its cells at unit 3
          (--absorb: X[T] = Z[T mod 2] instead: an eater at the end of the wire);
  guard   X[t] is the bare wire on unit 2 at every generation (so the constants to the left are exact).
A model is re-stepped on the infinite lattice with sg.step_set from a pulse launched 12 units away
(check_reflector), and only then reported.  UNSAT: no such cap within the planes for this T (the delay) and KS.
"""
import argparse, json, sys, time
import sg, plab, scat


def build(wire, T, C, lo, hi, KS, absorb=False, ua=2, kin=-3, kout=-3):
    ub = (C + hi) // 4 + 3
    R = scat.Region(wire, ua, ub, lo, hi, C, C)
    pb = scat.Problem(); f = pb.f; P = wire.P
    Z = pb.traj(R, P, 0, wrap=True)
    X = pb.traj(R, T, 0)
    for i in range(R.n):
        p = R.cells[i]
        if R.units[i] < KS:
            for ph in range(P):
                pb.fix(Z[ph][i], wire.live(p, ph))
        if R.units[i] == ua:
            for t in range(T + 1):
                pb.fix(X[t][i], wire.live(p, t))
    pin = wire.pulse_cells('R', 0, kin)
    pout = frozenset() if absorb else wire.pulse_cells('L', T % 2, kout)
    assert all(c in R.index for c in pin | pout)
    for i in range(R.n):
        p = R.cells[i]
        (pb.neq if p in pin else pb.eq)(X[0][i], Z[0][i])
        (pb.neq if p in pout else pb.eq)(X[T][i], Z[T % P][i])
    return R, pb, Z, X


def check_reflector(wire, cap, KS, far=-220, launch=-8, maxgen=400, verbose=False):
    """cap: live cells of units >= KS at an even generation.  Semi-infinite wire (units far .. KS-1) + cap; a
    right-moving pulse is launched with its cells at units launch, launch+1.  Returns (verdict, info)."""
    base = scat.semi_wire(wire, 0, far, KS) | frozenset(cap)
    # the cap alone: period 2 near the end
    near = lambda s: frozenset(c for c in s if scat.unit(c) >= launch - 30)
    z = base
    for _ in range(2):
        z = sg.step_set(z)
    if near(z) != near(base):
        return 'cap not stationary', None
    k = launch - 6
    x = base ^ wire.pulse_cells('R', 0, k)
    z = base
    for t in range(1, maxgen + 1):
        x = sg.step_set(x); z = sg.step_set(z)
        if t % 2 == 0:
            d = near(x) ^ near(z)
            if not d:
                return 'absorbed', t
            us = sorted(set(scat.unit(c) for c in d))
            if us[-1] < launch - 4:
                # everything that differs is left of the launch point: is it exactly one left-moving pulse?
                for kk in range(us[0] - 8, us[0] + 2):
                    if d == wire.pulse_cells('L', 0, kk):
                        return 'reflected', dict(t=t, k=kk)
                return 'returned something else', dict(t=t, cells=sorted(d))
            if us[0] < launch - 12 and us[-1] > launch:
                return 'spread', t
    return 'undecided', None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('T', type=int); ap.add_argument('C', type=int)
    ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--KS', type=int, default=6); ap.add_argument('--timeout', type=float, default=600)
    ap.add_argument('--obj', default='pulse-B'); ap.add_argument('--out'); ap.add_argument('--absorb', action='store_true')
    ap.add_argument('--solver', default='cadical153')
    a = ap.parse_args()
    ob = plab.load(a.obj); obl = plab.load(a.obj + '-left')
    wire = scat.Wire(ob, obl)
    t0 = time.time()
    R, pb, Z, X = build(wire, a.T, a.C, a.lo, a.hi, a.KS, a.absorb)
    free = len(R.of_units(a.KS, 10 ** 6))
    tag = f'{a.obj} T={a.T} planes C={a.C} tube [{a.lo},{a.hi}] KS={a.KS}: {R.n} cells, {free} free, vars={pb.f.n} clauses={len(pb.f.cl)}'
    st, m = pb.solve(a.solver, a.timeout)
    dt = time.time() - t0
    if st != 'SAT':
        print(f'{st:7s} {tag} {dt:.0f}s', flush=True); sys.exit(0 if st == 'UNSAT' else 2)
    cap = sorted(c for c in scat.cells_of(R, Z[0], m) if scat.unit(c) >= a.KS)
    verdict, info = check_reflector(wire, cap, a.KS)
    print(f'SAT     {tag} {dt:.0f}s; cap of {len(cap)} cells; on the infinite lattice: {verdict} {info}', flush=True)
    print('   cap:', cap)
    if a.out:
        json.dump(dict(obj=a.obj, T=a.T, C=a.C, lo=a.lo, hi=a.hi, KS=a.KS, cap=[list(c) for c in cap], verdict=verdict, info=info), open(a.out, 'w'))


if __name__ == '__main__':
    main()
