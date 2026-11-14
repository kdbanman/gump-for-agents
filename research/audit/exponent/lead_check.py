#!/usr/bin/env python3
"""Lead's own check of one claim in research/theory/exponent.md (section 3): the 2D toy's edge lifetime is
reproduced by a few rows of the rule over coin flips.

Model D2(L, rho; w): rows 0..w-1 follow B34/S234 on the range-2 cross (neighbours: same row +-1, +-2, periodic in
L; same column, rows +-1, +-2); nothing above row 0; rows w and w+1 are fresh Bernoulli(rho) cells every generation.
A replica dies when row 0 is empty. Soup p = 0.4 on the w rows; states younger than T0 = 300 are not measured.
ln tau = ln(exposure / deaths), error 1/sqrt(deaths).

Shares no code with research/theory/exponent/ (drv.c, xp.py) or research/toy2d/. Plain numpy.

  lead_check.py W L GENS [RHO] [R] [SEED]

References (exponent.md, section 3, rho = 0.472): w = 8: 5.645, 7.432, 9.165, 10.828 at L = 12, 16, 20, 24;
deterministic 16 x L strips: 5.644, 7.407, 9.142, 10.788.  w = 1 is the swarm lab's exact chain: 6.4169 (L = 12),
8.6350 (L = 16).

Results, 2026-11-14 (4096 replicas; about four minutes of one core in all):
  lead_check.py 1 12 3000 0.472 4096 1     6.4160 +- 0.0095  (11,093 deaths)   exact 6.4169
  lead_check.py 8 12 2500 0.472 4096 13    5.6541 +- 0.0104  ( 9,217; 6,537 cut)   study 5.645, strips 5.644
  lead_check.py 8 16 5000 0.472 4096 11    7.4246 +- 0.0103  ( 9,479;   887 cut)   study 7.432, strips 7.407
  lead_check.py 8 20 14000 0.472 4096 12   9.1362 +- 0.0131  ( 5,847;   132 cut)   study 9.165, strips 9.142
  lead_check.py 8 24 40000 0.472 4096 14  10.8554 +- 0.0179  ( 3,120;    31 cut)   study 10.828, strips 10.788
The hazard is flat in age at every size. Reading: the study's eight-row numbers are reproduced by independent code
(largest difference 0.029, 1.5 combined sigma). Against the deterministic strips the model is within 0.02 at
L = 12-20 and 0.067 +- 0.027 above at L = 24 (the study's own point there is 0.040 above), so "within 0.05" holds
at the three smaller sizes and is at its edge at L = 24. Not run here: L = 28, other densities, the deterministic
strips themselves (two independent sources exist for 16 x 16: research/toy2d 7.426 +- 0.016, the swarm exam's
copy of the study's driver 7.390 +- 0.016).
"""
import math, sys
import numpy as np


def run(w, L, gens, rho=0.472, R=4096, seed=1, T0=300, p=0.4):
    rng = np.random.default_rng(seed)
    H = w + 2
    s = np.zeros((R, H, L), np.uint8)

    def soup(k):
        t = np.zeros((k, H, L), np.uint8)
        t[:, :w] = rng.random((k, w, L)) < p
        return t

    s[:] = soup(R)
    age = np.zeros(R, np.int64)
    exposure = deaths = cut = 0
    edges = np.array([T0, 2 * T0, 4 * T0, 8 * T0, 16 * T0, 1 << 62])
    bexp = np.zeros(len(edges) - 1, np.int64); bdead = np.zeros_like(bexp)
    for g in range(gens):
        s[:, w:] = rng.random((R, 2, L)) < rho                 # fresh coins beneath
        n = (np.roll(s, 1, 2) + np.roll(s, -1, 2) + np.roll(s, 2, 2) + np.roll(s, -2, 2)).astype(np.uint8)
        n[:, 1:] += s[:, :-1]; n[:, 2:] += s[:, :-2]          # rows above (none above row 0)
        n[:, :-1] += s[:, 1:]; n[:, :-2] += s[:, 2:]          # rows beneath
        new = ((n == 3) | (n == 4) | ((s == 1) & (n == 2))).astype(np.uint8)
        counted = age >= T0                                    # exposed states: the step is taken from them
        s[:, :w] = new[:, :w]
        age += 1
        rows = s[:, :w].any(axis=2)                            # (R, w): row alive?
        dead = ~rows[:, 0]
        exposure += int(counted.sum())
        deaths += int((dead & counted).sum())
        b = np.searchsorted(edges, age[counted] - 1, side="right") - 1
        bexp += np.bincount(b, minlength=len(bexp))
        bdead += np.bincount(np.searchsorted(edges, age[dead & counted] - 1, side="right") - 1, minlength=len(bexp))
        if w >= 4:                                             # three adjacent dead rows cut the edge from the coins
            d = ~rows
            fw = (d[:, :-2] & d[:, 1:-1] & d[:, 2:]).any(axis=1) & ~dead
        else:
            fw = np.zeros(R, bool)
        cut += int(fw.sum())
        redo = dead | fw
        k = int(redo.sum())
        if k:
            s[redo] = soup(k)
            age[redo] = 0
    lt = math.log(exposure / deaths)
    print(f"D2(L={L}, rho={rho}; w={w}): {R} replicas x {gens} generations, seed {seed}: deaths {deaths}, "
          f"cut (censored) {cut}, exposure {exposure}, ln tau = {lt:.4f} +- {1 / math.sqrt(deaths):.4f}")
    print("  tau by age:", "  ".join(
        f"[{edges[i]},{edges[i + 1] if i + 2 < len(edges) else 'inf'}): {bexp[i] / bdead[i]:.0f} ({bdead[i]})"
        for i in range(len(bexp)) if bdead[i] >= 30), flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    w, L, gens = int(a[0]), int(a[1]), int(a[2])
    kw = {}
    if len(a) > 3: kw["rho"] = float(a[3])
    if len(a) > 4: kw["R"] = int(a[4])
    if len(a) > 5: kw["seed"] = int(a[5])
    run(w, L, gens, **kw)
