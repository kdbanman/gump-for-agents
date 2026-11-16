#!/usr/bin/env python3
"""Steady-state scattering by SAT: a cap at the end of wire B that, fed a periodic train of pulses, sends a periodic
train back (or eats the train, or emits one unfed).

    python3 sat_steady.py MODE N C [--off K] [--lo 1 --hi 5] [--timeout 600] [--out FILE] [--max 1]

MODE reflect: the wire carries right-moving pulses N units apart (one arrives every p = 2N generations) AND
              left-moving pulses N units apart; --off K places the left-movers (see ring_states);
     eat:     right-movers only (a check of the method: eaters exist);
     gun:     left-movers only (a cap that emits a pulse every 2N generations, unfed).
The state of the wire far from the cap is then known exactly and is periodic in time (p = 2N) and along the wire
(N units): it is computed on a ring of N units of the closed 3 x 3 tube and must return to itself after p
generations (for `reflect` this needs N even and the right parity of K: the pulses must pass through each other).
SAT problem (scat.Region as in sat_reflect.py: tube [lo,hi]^2, planes x+y-z <= C, x-y-z <= C at the +v end):
  X[0..p-1] with X[p] = X[0]; units < 2 are constants (the ring state, lifted); X is fixed to the ring state on
  units 2, 3 at every generation (which makes the constants exact); units >= 4 are free.
A model is an exact periodic solution on the semi-infinite wire with an infinite train.  It is then tested on a
finite object (caps.Lab-like vessel) with a finite train and with a single pulse.
"""
import argparse, json, sys, time
import numpy as np
import sg, plab, scat

S1, S2, S3, S4 = (1, 1, 1), (1, -1, 1), (1, 1, -1), (1, -1, -1)
KS = 4


def ring_states(wire, N, mode, off, lo=1, hi=5):
    """States of a ring of N units of wire B with the pulses of `mode`, generations 0 .. 2N-1, or None if the ring
    does not return to itself after 2N generations.  Right pulse: the file's defect moved to units 0, 1.  Left
    pulse: the left file's defect moved to unit `off`."""
    g = sg.Geom([(N, 0, -N)], [(S1, lo, hi), (S2, lo, hi)], unitvec=(1, 0, -1))
    x = g.state([scat.tr(c, k) for c in wire.bg[0] for k in range(N)])
    def flip(cells):
        for c in cells:
            x[g.index[g.canon(c)]] ^= 1
    if mode in ('reflect', 'eat'):
        flip(wire.pulse_cells('R', 0, -6))
    if mode in ('reflect', 'gun'):
        flip(wire.pulse_cells('L', 0, off - 6))
    orb = [x]
    for t in range(2 * N):
        orb.append(g.run(orb[-1], 1))
    if not (orb[-1] == orb[0]).all():
        return None, g
    # the pulses must still be there (not have stopped each other into a standing mark): not period 2
    if (orb[2] == orb[0]).all():
        return None, g
    return orb[:-1], g


def build(wire, orb, g, N, C, lo, hi):
    p = 2 * N
    ub = (C + hi) // 4 + 3
    R = scat.Region(wire, 2, ub, lo, hi, C, C)
    pb = scat.Problem()
    live = lambda q, t: bool(orb[t % p][g.index[g.canon(q)]])
    X = pb.traj(R, p, 0, wrap=True, left=live)
    for i in range(R.n):
        if R.units[i] < KS:
            for t in range(p):
                pb.fix(X[t][i], live(R.cells[i], t))
    return R, pb, X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['reflect', 'eat', 'gun']); ap.add_argument('N', type=int); ap.add_argument('C', type=int)
    ap.add_argument('--off', type=int, default=0); ap.add_argument('--lo', type=int, default=1); ap.add_argument('--hi', type=int, default=5)
    ap.add_argument('--timeout', type=float, default=600); ap.add_argument('--out'); ap.add_argument('--solver', default='cadical153')
    a = ap.parse_args()
    wire = scat.Wire(plab.load('pulse-B'), plab.load('pulse-B-left'))
    orb, g = ring_states(wire, a.N, a.mode, a.off, a.lo, a.hi)
    tag = f'{a.mode} N={a.N} (p={2 * a.N}) off={a.off} planes C={a.C} tube [{a.lo},{a.hi}]'
    if orb is None:
        print(f'NORING  {tag}: the ring of {a.N} units with these pulses does not return to itself', flush=True); return
    t0 = time.time()
    R, pb, X = build(wire, orb, g, a.N, a.C, a.lo, a.hi)
    free = len(R.of_units(KS, 10 ** 6))
    tag += f': {R.n} cells, {free} free, vars={pb.f.n} clauses={len(pb.f.cl)}'
    st, m = pb.solve(a.solver, a.timeout)
    dt = time.time() - t0
    if st != 'SAT':
        print(f'{st:7s} {tag} {dt:.0f}s', flush=True); sys.exit(0 if st == 'UNSAT' else 2)
    states = [sorted(scat.cells_of(R, X[t], m)) for t in range(2 * a.N)]
    cap = [c for c in states[0] if scat.unit(c) >= KS]
    print(f'SAT     {tag} {dt:.0f}s; cap of {len(cap)} cells at generation 0', flush=True)
    print('   cap:', cap)
    if a.out:
        json.dump(dict(mode=a.mode, N=a.N, off=a.off, C=a.C, lo=a.lo, hi=a.hi, KS=KS, states=[[list(c) for c in s] for s in states]), open(a.out, 'w'))


if __name__ == '__main__':
    main()
