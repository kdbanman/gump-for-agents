#!/usr/bin/env python3
"""Lead's own check of one number in research/theory/swarm/audit/AUDIT-theoremA.md: the lifetime of the edge of
the automaton A(L) (row 0: B34/S234 on the cross with nothing above; every other row copies the row two below;
initial fair bits beneath row 0, each written into two consecutive rows).

Shares no code with the swarm's lab, the audit's scripts or the exam. Plain numpy.

  lead_check_theoremA.py literal L GENS [R] [SEED]   the map on the whole array, tape of 2*GENS rows, run GENS steps
  lead_check_theoremA.py lazy    L GENS [R] [SEED]   rows 1, 2 drawn fresh each generation (the same law if the
                                                     audit's Theorem U.1 is right; 'literal' tests that)
A replica whose row 0 is empty has died; its row 0 is refilled with a soup of density 0.4 (the tape beneath it is
untouched). States younger than T0 = 50 since the refill are not measured. ln tau = ln(exposure / deaths).

Audit's exact values: ln tau_L = 6.5319, 9.4733 at L = 8, 12.

Results, 2026-11-14:
  literal 8 4000 512 1      6.5188 +- 0.0190  (2,772 deaths)     exact 6.5319
  lazy    8 20000 4096 2    6.5350 +- 0.0030  (110,312 deaths)   exact 6.5319
  lazy   12 60000 4096 3    9.4631 +- 0.0073  (18,997 deaths)    exact 9.4733
"""
import math, sys
import numpy as np


def run(mode, L, gens, R=512, seed=1, T0=50, p=0.4):
    rng = np.random.default_rng(seed)
    if mode == "literal":
        H = 2 * gens + 3
        bits = rng.random((R, gens + 1, L)) < 0.5
        y = np.zeros((R, H, L), np.uint8)
        y[:, 1:2 * (gens + 1):2] = bits                     # rows 1, 3, 5, ...
        y[:, 2:2 * (gens + 1) + 1:2] = bits                 # rows 2, 4, 6, ... (each bit twice)
    row0 = (rng.random((R, L)) < p).astype(np.uint8)
    age = np.zeros(R, np.int64)
    exposure = deaths = 0
    for g in range(gens):
        if mode == "literal":
            r1, r2 = y[:, 1], y[:, 2]
        else:
            r1 = (rng.random((R, L)) < 0.5).astype(np.uint8); r2 = r1
        n = (np.roll(row0, 1, 1) + np.roll(row0, -1, 1) + np.roll(row0, 2, 1) + np.roll(row0, -2, 1) + r1 + r2)
        new = ((n == 3) | (n == 4) | ((row0 == 1) & (n == 2))).astype(np.uint8)
        counted = age >= T0
        if mode == "literal":
            y[:, 1:-2] = y[:, 3:]                           # every row j >= 1 copies the row two below
        row0 = new
        age += 1
        dead = ~row0.any(axis=1)
        exposure += int(counted.sum()); deaths += int((dead & counted).sum())
        k = int(dead.sum())
        if k:
            row0[dead] = rng.random((k, L)) < p
            age[dead] = 0
    print(f"A({L}) {mode}: {R} replicas x {gens} generations, seed {seed}: deaths {deaths}, exposure {exposure}, "
          f"ln tau = {math.log(exposure / deaths):.4f} +- {1 / math.sqrt(deaths):.4f}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    run(a[0], int(a[1]), int(a[2]), *[int(v) for v in a[3:]])
