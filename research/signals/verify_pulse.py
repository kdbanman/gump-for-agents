#!/usr/bin/env python3
"""Verify a pulse (a travelling defect with the same background on both sides) with reference/oracle.py as the judge.

    python3 verify_pulse.py objects/<name>.json [--cubes C] [--periods K]

The file gives: `bg`, the live cells of one repeat of the background wire at generation 0 (doubled coordinates); `v`,
the repeat vector in cubes (the wire is bg + every multiple of 2v); `defect`, the cells whose state is flipped at
generation 0; and the claim (p, s): after p generations the whole state is itself moved by s repeats (s*v cubes).
The wire is closed into a ring on the cubic torus of side C cubes (it must fit: C*v/|v_x| a multiple of C), H = 2C.
Checks, all with oracle.masks and oracle.step on the H^3 array torus and nothing else:
  A  the background ring alone has period exactly `bg_period`;
  B  for j = 1 .. K: the state at generation j*p equals the state at generation 0 translated by j*s*v, cell for
     cell over the whole torus (K defaults to enough for two and a half laps of the ring, at least 10);
  C  at each of those generations the state differs from the background of the same generation in exactly the
     translated defect cells, and nowhere else: the disturbance is localised and the wire behind it is as it was;
  D  the defect is not a symmetry of the background: the state at generation 0 is not a translate of the background.
"""
import argparse, json, sys
import sg

ap = argparse.ArgumentParser()
ap.add_argument('file'); ap.add_argument('--cubes', type=int); ap.add_argument('--periods', type=int)
a = ap.parse_args()
ob = json.load(open(a.file))
v = ob['v']; p, s = ob['p'], ob['s']
C = a.cubes or ob.get('cubes', 40); H = 2 * C
reps = C // abs(v[0]); assert C % abs(v[0]) == 0 and all((reps * t) % C == 0 for t in v)
mod = lambda c: (c[0] % H, c[1] % H, c[2] % H)
tr = lambda cells, k: frozenset(mod((c[0] + 2 * k * v[0], c[1] + 2 * k * v[1], c[2] + 2 * k * v[2])) for c in cells)
bg0 = frozenset().union(*[tr([tuple(c) for c in ob['bg']], k) for k in range(reps)])
assert len(bg0) == reps * len(ob['bg'])
defect = frozenset(mod(tuple(c)) for c in ob['defect'])
x0 = bg0 ^ defect
K = a.periods or max(10, -(-5 * reps // (2 * abs(s))))
T = K * p
print(f"{ob['name']}: background of {len(ob['bg'])} cells per repeat, repeat vector {tuple(v)}, ring of {reps} repeats on the cubic torus "
      f"of side {C} cubes (H = {H}); defect of {len(defect)} flipped cells; claim: every p = {p} generations the state is itself "
      f"moved by s = {s} repeat(s); {K} periods = {T} generations = {K * abs(s) / reps:.2f} laps", flush=True)
ok = True
P = ob['bg_period']
orb = [st for _, st in sg.oracle_run(bg0, (H, H, H), max(P, 1))]
good = orb[P] == orb[0] and all(orb[t] != orb[0] for t in range(1, P))
print('PASS' if good else 'FAIL', f'A  the background ring alone has period exactly {P} under the oracle'); ok &= good
good = all(x0 != tr(bg0, k) for k in range(reps)) and x0 != bg0
print('PASS' if good else 'FAIL', 'D  the starting state is not the background or a translate of it'); ok &= good
nB = nC = 0; badB = []; badC = []
for (t, st), (_, bg) in zip(sg.oracle_run(x0, (H, H, H), T), sg.oracle_run(bg0, (H, H, H), T)):
    if t == 0 or t % p:
        continue
    j = t // p
    gb = st == tr(x0, j * s); gc = (st ^ bg) == tr(defect, j * s) if (t % P == 0) else True
    nB += gb; nC += gc
    if not gb: badB.append(t)
    if not gc: badC.append(t)
print('PASS' if nB == K else 'FAIL', f'B  generation j*{p} equals generation 0 translated by j*{s} repeats, cell for cell, for j = 1 .. {K}'
      + ('' if nB == K else f' (fails at {badB[:5]})')); ok &= nB == K
print('PASS' if nC == K else 'FAIL', f'C  at those generations the state differs from the background only in the {len(defect)} translated defect cells'
      + ('' if nC == K else f' (fails at {badC[:5]})')); ok &= nC == K
print('ALL PASS' if ok else 'SOME CHECKS FAILED', '-', ob['name'])
sys.exit(0 if ok else 1)
