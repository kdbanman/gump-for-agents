# research/blast/split-hull: a rare-event sampler for the faces of gump's octahedral hull

Agent `split-hull`, blast of 2026-11-18. Aim: ln τ_face of the 135-cell rimmed face (R = 17), which brute force
cannot reach (one death per 6 × 10¹¹ hull-generations). Files: `sh.c` (stepper and sampler), `validate.py` (stepper
against `reference/oracle.py`), `chain.sh` (replications), `ana.py` (pooling), `PREDICTIONS.md` (forecasts),
`paths/` (dying paths). Bulk output: `research/scratch/blast/split-hull/runs/`.

## Short answer (04:15 UTC; numbers marked * are being sharpened by runs still going)

1. **The sampler does not reach the 135-cell face, and I can say why [measured].** Forward-flux sampling on the
   face's population, clones separated by deep flips. Unbiased, weak separations (one flip three layers down) leave
   it starved: it beats plain running by a factor of about 7 only, because a dip from 0.9 P̄ to an empty face lasts
   about 10 generations and a deep flip needs several to change the face. Strong separations (a sixth of the fifth
   layer flipped, two generations back, which is the setting I froze) bias it: **estimate − anchor = −0.027 ± 0.018
   at R = 9, −0.173 ± 0.044 at R = 11**, and at R = 13 it is starved as well (scatter 0.57 per replication). The bias
   grows as the face thins: +0.1% per stage at 0.8 P̄, +20% when four cells are left (table below). No number for
   R = 17 comes from it.
2. **What does come out is a decomposition that forecasts R = 17 [measured tables, conjectured law].** By plain
   running (no cloning) I measured the dip rates ν(p) (first passages of P ≤ p·P̄ per hull-generation, coming from
   above P̄) at R = 9 … 21. With the anchors' lifetimes, −ln q(p) = ln τ + ln ν(p) is, for p ≤ 0.6, **a straight line
   in the area with no rim term**: at p = 0.6 it is 5.611, 8.668, 12.242, 16.330 at 45, 63, 84, 108 cells, slope
   0.1701 per cell, residuals +0.003, −0.003, −0.002, +0.002 (χ² 0.4 on 2; at p = 0.5 and 0.4 likewise, χ² 1.7 and
   0.1; at p = 0.7, 0.8, 0.85 it is not a line, χ² 9, 32, 44). So the hull face's rim term (the −0.34 k of
   ln τ = 1.144 + 0.2308 A − 0.342 k) sits in **how often the face dips to 0.6 P̄**, not in what happens below.
   ν(0.6 P̄) can be measured at any size by plain running. If the line continues:
   **ln τ_face(R = 17) = 29.223 ± 0.016\***, **R = 19: 35.79 ± 0.03\***, **R = 21: 42.97 ± 0.07\***. That is the value of
   "the second difference repeats" (29.230) and 3.7 errors above "the wrapped price takes over" (29.163). It is a
   forecast resting on a four-point straight line, not a measurement of τ.
3. **Brute force agrees with the anchors [measured]:** R = 9: ln(8E/D) = 9.8201 ± 0.0055 (32,644 first deaths);
   R = 11: 13.627 ± 0.036 (790). The dip rates agree with `research/dying`'s independent code at 63 cells
   (ln ν = −2.311, −4.164, −6.513, −9.359, −12.48 at P ≤ 28, 21, 15, 9, 3 against its −2.31, −4.16, −6.51, −9.37, −12.43).

## Deliverable 1: the stepper [measured]

`python3 research/blast/split-hull/validate.py 1200`: `sh.c`'s bit-sliced hull stepper equals `reference/oracle.py`
cell for cell at R = 11 and R = 15 (3 soups × 1,200 generations each, lanes 0, 37, 2047), together with the face
population counter, the emptiness bits of the seven other faces, the age counters, the ring of lagged states (the
state two generations ago), frozen lanes and the packed-configuration round trip. Negative control (one neighbour
swapped): fails at generation 5 (R = 11) and 3 (R = 15). Last line: `VALIDATION PASSED`. Geometry: 2,064 cells and
108 per face at R = 15, as on file.

## Deliverable 2: calibration of the sampler [measured]

Parameters were frozen at 03:52 UTC after only four tuning seeds at R = 11 (which gave 13.604 ± 0.06 and looked
fine): M = 300,000 trials a stage, LAG = 2, one flip per 6 sites of S, levels 3 cells apart, H = 0.5, stores of
100,000. Twelve fresh replications then showed the bias. `sh chain.sh R R001 N`, `python3 ana.py`:

| R | cells | replications | pooled ln τ | anchor | estimate − anchor | scatter of one replication | effective ancestors |
|---|---:|---:|---|---|---|---:|---:|
| 9 | 45 | 12 | 9.792 ± 0.018 | 9.819 | −0.027 ± 0.018 | 0.064 | 320 |
| 11 | 63 | 12 | 13.461 ± 0.044 | 13.633 | **−0.173 ± 0.044** | 0.153 | 33 |
| 13 | 84 | 4 | 17.79 ± 0.26 | 18.141 | −0.35 ± 0.26 | 0.57 | 6 |
| 15 | 108 | 0 | not run: at 0.57 scatter and a bias already shown, it would have cost ten minutes for nothing | 23.339 | | | |

"Effective ancestors": (Σn)²/Σn² over the first-level crossings the stored deaths descend from, median over
replications. It falls by about 10 for every 4 in ln τ: at R = 17 a replication would hang on one crossing.

**Where the bias enters** (`python3 levels.py`, part 1: the sampler's ν(L) against plain running, same definition):

| R = 11, level L (P ≤ L) | 28 | 25 | 22 | 19 | 16 | 13 | 10 | 7 | 4 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|
| sampler − brute force, ln ν | −0.000 | +0.001 | +0.004 | +0.009 | +0.014 | +0.036 | +0.064 | +0.101 | +0.178 | +0.36 |
| in combined errors | −0.5 | +1.5 | +2.8 | +2.5 | +1.8 | +2.8 | +3.0 | +3.0 | +3.2 | +3.4 |

(R = 13, four replications: +0.009 at P ≤ 29, +0.025 at 23, +0.043 at 20 (6 errors), +0.17 at 11.) Flipping a sixth of
the fifth layer beneath a face makes every further loss of three cells more likely, slightly while the face is
full and by a fifth when it is nearly empty. **What bias I can exclude:** none below 0.17 at 63 cells for the
frozen setting; the sampler is not calibrated. For the weak setting (one flip at depth three, no lag; six
replications before the freeze: 13.69 ± 0.16) a bias above 0.4 is excluded and nothing finer.

A second separation, **donor swap** (everything five layers and more beneath the watched face replaced, two
generations back, by the same cells of an independent hull from the base run; `sh variant.sh 11 11201 6 2 0 swap2 1`):
13.534 ± 0.117 at R = 11 (6 replications, scatter 0.24): −0.10 ± 0.12, neither cleared nor convicted.

## Deliverable 3: R = 17. Not measured; forecast instead

See point 2 above and `PREDICTIONS.md` block 3 (frozen 04:11 UTC, commit 3946e01, before the longer runs).
`python3 research/blast/split-hull/levels.py`, parts 2 to 4. Brute-force dip rates (threshold-free: ln ν
interpolated linearly in L at L = p·P̄; Poisson errors 0.001 to 0.06, printed by the script):

<!-- DIPTABLE -->
```
PART 2: brute-force dip rates at fixed fractions of P-bar (threshold-free), per hull-generation and per face
   R    A   P-bar   sigma_P  ln nu(0.85)  ln nu(0.8)  ln nu(0.7)  ln nu(0.6)  ln nu(0.5)  ln nu(0.4)  ln nu(0.3)
   9   45   21.597   4.564      -2.503     -2.797     -3.455     -4.208     -5.058     -5.988     -6.978
      (Poisson errors)            0.000      0.000      0.001      0.001      0.002      0.003      0.004     exposure 7.51e+07
  11   63   31.255   5.224      -2.620     -2.994     -3.881     -4.965     -6.239     -7.659     -9.172
      (Poisson errors)            0.000      0.000      0.001      0.002      0.003      0.006      0.012     exposure 8.18e+07
  13   84   42.445   5.964      -2.730     -3.212     -4.400     -5.899     -7.687     -9.669    -11.770
      (Poisson errors)            0.000      0.001      0.001      0.002      0.004      0.014      0.039     exposure 1.23e+08
  15  108   55.176   6.702      -2.895     -3.497     -5.031     -7.010     -9.355    -11.993        nan
      (Poisson errors)            0.001      0.001      0.002      0.004      0.014      0.045        nan     exposure 8.19e+07
  17  135   69.478   7.436      -3.063     -3.812     -5.767     -8.304    -11.323        nan        nan
      (Poisson errors)            0.001      0.001      0.002      0.008      0.038        nan        nan     exposure 8.19e+07
  19  165   85.381   8.155      -3.264     -4.172     -6.595     -9.749    -13.450        nan        nan
      (Poisson errors)            0.000      0.000      0.002      0.007      0.049        nan        nan     exposure 3.89e+08
  21  198  102.752   8.938      -3.495     -4.595     -7.548    -11.337        nan        nan        nan
      (Poisson errors)            0.001      0.002      0.009      0.059        nan        nan        nan     exposure 3.07e+07

  ln tau (anchor) + ln nu(p) = -ln q(p): what is left of the lifetime once the attempt rate at p is taken out
   R    A   -ln q(0.85)  -ln q(0.8)  -ln q(0.7)  -ln q(0.6)  -ln q(0.5)  -ln q(0.4)  -ln q(0.3)
   9   45      7.316      7.022      6.364      5.611      4.761      3.831      2.841
  11   63     11.013     10.639      9.752      8.668      7.394      5.974      4.461
  13   84     15.411     14.929     13.741     12.242     10.454      8.472      6.371
  15  108     20.444     19.843     18.308     16.330     13.984     11.347        nan
  second differences in the edge k (9,11,13 and 11,13,15); ln tau itself gives 0.694, 0.690:
    p = 0.85: 0.700  0.635     slopes per cell 45-63, 63-84, 84-108: 0.2054 0.2094 0.2097
    p = 0.8: 0.672  0.624     slopes per cell 45-63, 63-84, 84-108: 0.2010 0.2043 0.2047
    p = 0.7: 0.601  0.578     slopes per cell 45-63, 63-84, 84-108: 0.1882 0.1899 0.1903
    p = 0.6: 0.517  0.513     slopes per cell 45-63, 63-84, 84-108: 0.1698 0.1702 0.1703
    p = 0.5: 0.427  0.471     slopes per cell 45-63, 63-84, 84-108: 0.1463 0.1457 0.1471
    p = 0.4: 0.355  0.376     slopes per cell 45-63, 63-84, 84-108: 0.1191 0.1190 0.1198
    p = 0.3: 0.290  nan     slopes per cell 45-63, 63-84, 84-108: 0.0900 0.0910 nan

PART 4: weighted straight-line fit of -ln q(p) and the forecasts with errors
  p = 0.85: -ln q = -2.096 + 0.20842 A  (slope error 0.00019; chi2 43.8 on 2)   R = 17: 29.105 +- 0.014;  R = 19: 35.559 +- 0.019;  R = 21: 42.667 +- 0.025
  p = 0.8: -ln q = -2.164 + 0.20351 A  (slope error 0.00019; chi2 32.4 on 2)   R = 17: 29.122 +- 0.014;  R = 19: 35.588 +- 0.019;  R = 21: 42.726 +- 0.025
  p = 0.7: -ln q = -2.182 + 0.18958 A  (slope error 0.00019; chi2 9.2 on 2)   R = 17: 29.178 +- 0.014;  R = 19: 35.693 +- 0.019;  R = 21: 42.902 +- 0.027
  p = 0.6: -ln q = -2.048 + 0.17012 A  (slope error 0.00019; chi2 0.4 on 2)   R = 17: 29.223 +- 0.016;  R = 19: 35.772 +- 0.021;  R = 21: 42.974 +- 0.065
  p = 0.5: -ln q = -1.816 + 0.14616 A  (slope error 0.00023; chi2 1.7 on 2)   R = 17: 29.238 +- 0.042;  R = 19: 35.750 +- 0.055
  p = 0.4: -ln q = -1.528 + 0.11909 A  (slope error 0.00038; chi2 0.1 on 2)   
  second differences in k of ln nu(0.6 P-bar): -0.177+-0.013  -0.177+-0.013  -0.183+-0.017  -0.151+-0.022  -0.142+-0.063   (centred on R = 11 ... 19)

PART 5: levels at fixed density x (L = x A): weighted straight-line fit of ln tau + ln nu and forecasts
  x = 0.42: slope 0.20116, chi2 313.4 on 2, residuals +0.083 -0.005 +0.018 +0.074   R = 17: 29.033 +- 0.010;  R = 19: 35.455 +- 0.015;  R = 21: 42.520 +- 0.019
  x = 0.38: slope 0.19159, chi2 161.6 on 2, residuals +0.059 -0.004 +0.013 +0.053   R = 17: 29.099 +- 0.010;  R = 19: 35.578 +- 0.015;  R = 21: 42.726 +- 0.020
  x = 0.34: slope 0.17861, chi2 42.3 on 2, residuals +0.030 -0.003 +0.007 +0.027   R = 17: 29.171 +- 0.011;  R = 19: 35.690 +- 0.015;  R = 21: 42.868 +- 0.027
  x = 0.31: slope 0.16680, chi2 9.7 on 2, residuals +0.014 -0.002 +0.004 +0.012   R = 17: 29.206 +- 0.013;  R = 19: 35.752 +- 0.017;  R = 21: 42.918 +- 0.063
  x = 0.28: slope 0.15344, chi2 0.6 on 2, residuals +0.002 -0.000 -0.002 +0.007   R = 17: 29.229 +- 0.022;  R = 19: 35.781 +- 0.026
  x = 0.25: slope 0.13888, chi2 3.4 on 2, residuals -0.001 +0.001 -0.008 +0.021   R = 17: 29.245 +- 0.050;  R = 19: 35.791 +- 0.068
  x = 0.22: slope 0.12335, chi2 0.5 on 2, residuals -0.000 +0.001 -0.004 +0.020   R = 17: 29.363 +- 0.141
```
<!-- /DIPTABLE -->

What the forecast rests on, and what would break it: (a) the anchors (the 108-cell one, ± 0.0099, gives most of the
forecast's error); (b) P̄ from each run's 300-generation pilot (± 0.015 cells, ± 0.005 in ln ν(0.6), included);
(c) the conjecture that the line continues. If the 135-cell face is 29.163, −ln q(0.6) must fall 0.06 below a line
that four sizes follow to 0.003. A check inside the 135-cell data that needs no lifetime: ln ν(0.6) − ln ν(0.5)
should itself be linear in the area if both lines hold; it is 0.850, 1.274, 1.788, 2.345, 3.02 ± 0.04\*, 3.7 ± 0.2\*
at 45 … 165 cells, steps per cell 0.0236, 0.0245, 0.0232, 0.0250\*, 0.024\*.

## Deliverable 4: the prefactor [measured tables; the reading is conjecture]

- **ln τ + ln ν(p) is linear in A only for p ≤ 0.6, and its slope is not the wrapped price.** Slopes per cell of
  −ln q(p): 0.2084 (p = 0.85), 0.2035 (0.8), 0.1896 (0.7), 0.1701 (0.6), 0.1462 (0.5), 0.1191 (0.4). The slope passes
  through the wrapped faces' 0.2087 at p ≈ 0.85, where −ln q is *not* a line (χ² 44 on 2), so that coincidence
  means nothing. There is no level at which "attempt rate removed" leaves the wrapped slope and a straight line.
- **How ν scales.** At fixed p, ln ν(p) is a quadratic in the edge k: for p = 0.6, second differences −0.177,
  −0.177, −0.183 ± 0.017, −0.166 ± 0.030\*, −0.11 ± 0.08\* centred on R = 11 … 19, i.e. −0.059 per cell with a term
  +0.305 k. The lifetime's rim term is −0.342 k: nine tenths of it is the attempt rate's. Shallower, the rim term
  of ν is smaller (the fits of −ln q with a term in k give −0.29 k at p = 0.85, −0.26 at 0.8, −0.14 at 0.7, −0.03 at
  0.6, −0.07 at 0.5, −0.05 at 0.4), so the rim acts on the passage from about 0.85 P̄ down to 0.6 P̄.
- **Reading [conjectured].** A rimmed face is "dearer per cell" than a wrapped one because its dips to 0.6 P̄ get
  rarer with size faster, not because the collapse below 0.6 P̄ costs more. Note that p·P̄ is not a fixed density:
  P̄/A = 0.480, 0.496, 0.505, 0.511, 0.515, 0.517, 0.519 at R = 9 … 21 (the rim's emptier corners), so 0.6 P̄ is a
  deeper dip, per interior cell, on a small face than on a large one. Not tested: levels at fixed density.

## Deliverable 5: reactive paths

`paths/R9.txt`, `R11.txt`, `R13.txt` (300, 300, 100 paths; `python3 curate.py 25` from the frozen sampler's runs, one
path per ancestor per replication). **Caveat: these come from the flip sampler, biased by −0.03, −0.17 and more;**
its dying paths carry flips five layers down. Format: header lines; a line `C` with the doubled coordinates of
the face's cells in order; then per path `seed ancestor T k age[0..A−1] P pop[−15..0]`: T generations from the
crossing of ⌊0.9 P̄⌋ to the empty face, k faces empty at the death, age = generations before the death at which
that cell was last alive (255 = 255 or more), then the face population at the last 16 generations.
- Duration T: 8.95 ± 0.09 (R = 9), 9.93 ± 0.21 (R = 11), 12.5 ± 1.0 (R = 13) generations.
- Deaths containing a one-generation fall of half the face (the PI's "bust"): 2.1% at R = 9 (anatomy's brute force:
  1.6 to 2.2%), 0.9% at R = 11 (dominated by a few ancestors; median replication 0.01%), none in 4 replications at
  R = 13. **The sampler cannot tell whether the bust share grows with size:** a bust is a crossing that is already
  deep, such crossings are rare among the 100,000 stored, and the downward levels never look for them. The
  forecast of point 2 does not have this weakness (ν and the anchors count every route).

## What failed, a line each

- One flip three layers down at the crossing (no lag): unbiased within 0.16 at R = 11 but scatter 0.4 to 0.5 per
  replication at 3 × 10⁵ trials a stage; coarser levels (6, 9 cells) no better.
- One flip one layer down: 12.96 ± 0.10 at R = 11 (8 replications at 3 × 10⁴ trials): biased by −0.67.
- Lag 2, a sixth of the fifth layer (frozen): biased −0.17 at R = 11. Lag 2, one flip: scatter 0.4 (3 seeds).
- Donor swap: −0.10 ± 0.12 at R = 11, scatter 0.24: no better.
- Freezing after four seeds: the four gave 13.604 ± 0.06; twelve gave 13.461 ± 0.044.

## Not checked

- Whether the −ln q(0.6) line continues beyond 108 cells: that is the forecast itself.
- Levels at fixed density instead of fixed fractions of P̄; the same decomposition on wrapped faces (the test that
  would say whether the two prices differ only in the attempt rate).
- The sampler at R = 15 and R = 17; lag 3 or 4 with a single flip; whether the donor swap is unbiased.
- P̄ beyond the 300-generation pilots (agreement with `research/dying`'s exposure means: 21.60, 55.19 there; 21.60,
  55.18 here). Settled lives: none seen (no hull reached age 100,000, no trial timed out).
- The bust channel at large sizes (see deliverable 5).

## The sampler, exactly (for the referee who rewrites it from the oracle)

**Vessel.** Cells: p ∈ Z³ (doubled coordinates) with exactly one odd coordinate and |x| + |y| + |z| ≤ R, R odd.
Neighbours: the oracle's twelve; a neighbour outside the vessel is dead (T2 makes this the infinite lattice's own
dynamics). Face f (eight sign patterns d): the cells with d·p = R; counts 45, 63, 84, 108, 135, 165, 198 for
R = 9 … 21, hull sizes 510, 876, 1,386, 2,064, 2,934, 4,020, 5,346. The **watched face** is d = (+,+,+); P is the
number of its live cells. A face is *empty* when none of its cells is alive; adjacent faces share their rim row.

**Why forward-flux sampling.** The death rate is exactly (rate of first crossings of a level, coming from above
P̄) × (chance that such a crossing continues to an empty face before returning above P̄): the ν·q bookkeeping of
`research/dying`. Forward-flux sampling (Allen, Frenkel, ten Wolde) estimates the second factor as a product of
conditional probabilities between levels with a fixed number of trials per stage; the product of the stage
fractions is an unbiased estimate of the rate (not of its logarithm), trials are plain runs of the true rule that
fit the lanes of a bit-sliced stepper, and there are no weights to carry. Level function: P itself.

**Base run** (gives the flux and the first store). 2,048 independent hulls. A hull starts as a soup (each cell
alive with probability 0.35), age 0; every generation its age grows by 1. After each generation: if any of the
eight faces is empty the hull is replaced by a fresh soup (age 0); it is a *first death* if the generation is
counted. A hull-generation is *counted* (exposure += 1) when the hull's age after the step exceeds 200 and the
counting phase is on. Phases, in global generations: 200 of burn-in; 300 of pilot, in which P̄ and σ_P are the mean
and standard deviation of P over hulls older than 200; then λ_A = ⌈P̄⌉ and λ₀ = ⌊0.9 P̄⌋ are fixed; 100 generations
to let the flags settle; then the counting phase, until 100,000 configurations are stored.
Each hull carries a flag (0 at a soup and at the end of the pilot). From age 100 on: if P ≥ λ_A the flag becomes 1;
else if P ≤ λ₀ and the flag is 1, the flag becomes 0 and this is a **crossing** (it counts if the generation is
counted; a generation at which another face is empty and P > 0 ends the hull and is no crossing; an empty watched
face with the flag at 1 is a crossing). Φ₀ = crossings / exposure. Each counted crossing is stored with
probability H = 0.5. **What is stored is the hull's state LAG = 2 generations before the crossing** (plus, as
passengers, each face cell's age since it was last alive and the last 16 values of P as of the crossing).

**Levels.** λ₀, λ₀ − 3, λ₀ − 6, …; the first value ≤ 0 is replaced by 0, the last level (the empty face).

**Stage i** (from λ_i to λ_{i+1}). M = 300,000 trials. Trial j starts from stored configuration π(j mod N_i), π a
uniform random permutation of the N_i configurations of level i, drawn afresh for the stage. The start state is
the stored (two-generations-old) state with ⌈|S|/6⌉ **perturbations**, applied one after another: with probability
½ "kill" (one live cell of S, chosen uniformly, dies), otherwise "revive" (one dead cell of S, chosen uniformly,
comes alive); if the kind drawn has no candidate the other kind is done. **S**: the cells with x + y + z = R − 10
(the fifth layer beneath the watched face's layer) and d·p ≤ R − 4 for the seven other sign patterns (|S| = 21, 36,
54, 75, 99, 126, 156 for R = 9 … 21). Then the true rule runs. The first two generations are a **replay**: nothing
at depth five can change the face layer within two generations (a cell's neighbours are at most two layers up,
T1), so after two generations the watched face is exactly the parent's face at its crossing or success, with its
whole history, while the layers beneath it already differ between clones. (Checked in every trial by comparing P
with the parent's: `replaybad 0` in every RESULT line.) From that generation on (trial age 2, 3, …), in this order:
(1) P = 0: success (in the last stage with weight 1/k, k the number of faces empty at that generation);
(2) another face empty: failure; (3) P ≤ λ_{i+1}: success; (4) P ≥ λ_A: failure; (5) age above 20,000: failure,
booked as a timeout (none occurred). On success the state stored for level i + 1 is the trial's state **two
generations before** the success. If a stage has more than 100,000 successes a uniform subset of 100,000 is kept
(reservoir sampling). p̂_i = (sum of success weights) / M.

**Estimator.** 1/τ̂ = Φ₀ · ∏ p̂_i; ν̂(λ_i) = Φ₀ · ∏_{j<i} p̂_j; q̂ = 1/(τ̂ ν̂). By the symmetry of the eight faces the rate
at which the watched face is among the first to empty (ties shared) is 1/τ_face = deaths / (8 · exposure), the
anchors' definition (fresh soups of 0.35, ageing-in 200, a hull retired at its first death).

**Error procedure.** K independent replications of everything (base run, pilot, stores, stages; seeds R·1000 + k).
Pooled value ln τ = −ln(mean of the K rates 1/τ̂_k); error = standard deviation of the rates / (√K · mean), with
a jackknife beside it (`ana.py`). The mean of the K logarithms is printed too; it is biased upward by about half
the variance of one replication's logarithm.

**Why the lag.** Gump is deterministic, so clones must be separated, and a separation deep enough to be harmless
takes generations to reach the face, while the whole dip from 0.9 P̄ to an empty face lasts about ten generations.
Flipping one cell three layers down at the moment of the crossing left the estimator starved (scatter 0.4 to 0.5 of
one replication at R = 11 with 3 × 10⁵ trials a stage, half the replications 0.5 too high), and flipping one layer
down biased it (12.96 ± 0.10 against 13.633: `./sh` with the earlier depth argument; rows in "What failed").
Starting each clone two generations in the past moves the flips to depth five, lets the true rule launder them for
two generations, and still has the clones differ directly beneath the face at the moment of the crossing.

**Passengers.** Per face cell an 8-bit age (generations since last alive, saturating at 255), stepped with the
state and stored with it; and the last 16 values of P. Neither enters the dynamics or the selection.

## Reproduce

```sh
python3 research/blast/split-hull/validate.py 1200            # stepper against the oracle, R = 11 and 15 (~1 min)
sh research/blast/split-hull/chain.sh 13 13001 10             # 10 replications at R = 13 (frozen parameters)
python3 research/blast/split-hull/ana.py                      # pooled values, nu and q by level, path statistics
# one replication by hand:  shf R SEED M LAG NFLIP STEP H PATHFILE CAP
research/scratch/blast/split-hull/shf 11 11001 300000 2 -6 3 0.5 - 100000
```
