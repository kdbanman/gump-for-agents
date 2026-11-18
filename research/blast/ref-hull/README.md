# research/blast/ref-hull: referee for the hull-face lifetime at R = 17 (independent code)

Agent `ref-hull`, blast of 2026-11-18. Standing account; every number has its command. All code here was written
from `reference/oracle.py` and `docs/AUTOMATON.md`; split-hull's code was never opened. Its README was opened at
04:32 UTC on the PI's instruction, after my sampler's R = 9 and 11 numbers and my forecasts were committed.
Files: `rh.c` (stepper; `val`, `run` = sampler, `nu` = plain running), `validate.py`, `ana.py` (pools sampler
replications), `nu.py` (dip-rate analysis), `chain.sh`, `nuchain.sh`, `nuchain2.sh`, `out/` (curated rows),
`PREDICTIONS.md`, `REVIEW.md` (the verdict).

## Short answer (04:55 UTC)

1. **My own splitting sampler has split-hull's weakness; no R = 17 measurement comes from it [measured].** Strong
   separations bias it toward early death (R = 9: 29 toggles per clone give 9.787 ± 0.010, donor swap 9.791 ± 0.011,
   anchor 9.819; 4 or 6 toggles give 9.815 ± 0.011 and 9.827 ± 0.008); weak ones starve it (R = 11, 6 toggles:
   scatter 0.19 per replication). Stopped at R = 11 on the PI's instruction.
2. **split-hull's dip rates are confirmed [measured]:** ln ν(0.6 P̄) from my stepper differs from its table by
   −0.002, −0.001, +0.002, −0.005, +0.006, −0.004, +0.018 ± 0.018 at R = 9 … 21; nothing beyond 2.3 combined errors
   at p ≤ 0.6. Its P̄ (a short pilot) is off by up to 0.036 cells, which moves the high levels by up to 0.007 (12 of
   its Poisson errors at R = 19, p = 0.8) and is harmless for the forecast.
3. **Its line and forecast are reproduced:** −ln q(0.6) = 5.609, 8.667, 12.244, 16.330; slope 0.17016 ± 0.00014,
   χ² 0.5 on 2; **R = 17 by this route: 29.219 ± 0.010** (its 29.227 ± 0.014), R = 19: 35.780 ± 0.014, R = 21:
   43.011 ± 0.019. The other deep levels agree at R = 17 (29.219 at p = 0.5, 29.206 ± 0.023 at p = 0.4, 29.20–29.22 at
   fixed densities 0.30–0.20) but spread at R = 19 (35.71–35.78) and R = 21 (42.97–43.08).
4. **Is the error honest?** With a rim term allowed (a + cA + rk, the quadratic in k) the same four values give
   29.232 ± 0.023, which is exactly the lifetime's own quadratic (29.232 ± 0.023 from the four anchors alone).
   The route narrows the error only by assuming r = 0, and the fit knows r only to ± 0.043.
5. **I tried to break "no rim term" with a test that needs no lifetime, and it survived [measured].**
   ln q(p₁) − ln q(p₂) = ln ν(p₂) − ln ν(p₁) exactly, so the claim says ln ν(0.6 P̄) − ln ν(p P̄) is a straight line in
   the area at every size, R = 17–21 included. Fitted on R = 9–15 and compared at R = 17: line misses by +0.009 ±
   0.003 (p = 0.5), −0.006 ± 0.020 (0.4), +0.004 ± 0.006 (densities 0.30 against 0.24), while the quadratic in k
   misses by −0.024 ± 0.003 and −0.041 ± 0.006. In-sample the line is not exact (χ² 459 on 2 for 0.6 against 0.5:
   the 45-cell face sits 0.005–0.01 off), so the law holds to about 0.01, not to its statistical error.
6. **Verdict on "29.227 ± 0.014": fair value, error should read ± 0.02, and it favours 29.230 over 29.163 half on
   evidence and half by construction.** At R = 17, 14.65 of the 29.2 (the dip to 0.4 P̄, which carries the whole rim
   term) is measured and sits on its smooth continuation; the other half (−ln q) is a straight line through four
   points, and "the wrapped price takes over" is the statement that this line bends by about 2% (0.0025 per cell out of 0.12–0.17) beyond 108 cells,
   which no dip rate can test.
7. **New [measured]: the curvature of the dip rate is not constant, and beyond 135 cells the levels stop agreeing.**
   The second difference in k of ln ν(0.6 P̄) is −0.176, −0.181, −0.176, −0.168 ± 0.002, −0.160 ± 0.004 centred on
   R = 11 … 19 (fixed density 0.30: −0.199, −0.202, −0.192, −0.184 ± 0.002, −0.175 ± 0.006). So with −ln q(0.6) on its
   line the route itself puts ln τ BELOW "second difference repeats" at the next sizes: 35.780 ± 0.014 against 35.812,
   43.011 ± 0.019 against 43.085 (second difference of ln τ: 0.686, 0.678, 0.671 centred on R = 15, 17, 19, not 0.691).
   But at R = 21 the step from 0.6 P̄ to 0.5 P̄ is 0.087 ± 0.032 rarer than its line, and level 0.5 says 43.080 ± 0.039:
   the route's real error is its dependence on the level, about ± 0.01 at R = 17, ± 0.03 at R = 19, ± 0.05 at R = 21.
   Reading [conjectured]: the rim-carrying half of the exponent drifts slowly toward a lower price per cell; neither
   "repeats" nor "takes over" is exact; at R = 21 the route says 42.97–43.08 against 43.085 and 42.689.

## 1. Validation of the stepper [measured]

`rh.c`: bit-sliced, 256 hulls per step; cells = doubled coordinates with exactly one odd, |x|+|y|+|z| ≤ R; twelve
neighbours from the oracle's offsets; outside the hull dead. Cell counts 510, 876, 1,386, 2,064, 2,934 for
R = 9 … 17 (`./rh val R 1 0 | head -1`).

    gcc -O3 -march=native -o rh rh.c -lm
    python3 validate.py 11 1 1200      # PASSED: 3 lanes x 1,200 generations identical to the oracle, state for state
    python3 validate.py 15 2 1200      # PASSED
    python3 validate.py 11 1 1200 1    # negative control (one neighbour of one cell swapped): FAILS at generation 1-5
    python3 validate.py 15 2 1200 1    # negative control: FAILS at generation 1-2

The oracle runs the same soup in a padded box of side 2R+10; the check asserts no live cell outside the hull.
Output: `out/validation.txt`. Not checked against the oracle: R = 9, 13, 17, 19, 21 (same code, only R differs).
Brute force under the anchors' convention (soups 0.35, ageing-in 200, hull retired at its first empty face,
ln(8·exposure/first deaths)), from the `nu` runs: **R = 9: 9.8240 ± 0.0017** (365,634 first deaths; anchor 9.819;
0.25% of those generations empty two faces at once, `./rh nu 9 77 150000 22 >/dev/null`), **R = 11: 13.630 ± 0.011**
(8,852; anchor 13.633), R = 13: 18.16 ± 0.10 (96).

## 2. The splitting sampler (`rh run`) and why it was stopped [measured]

Forward flux on the watched face's population P: λ_A = round(P̄), first level round(P̄ − 1.5σ_P), levels STEP cells
apart down to 5, then 0; base store of every crossing; clones restart from the parent's state LAG = 2 generations
before its crossing with a separation that cannot reach the face layer in 2 generations (replay checked: `replaybad 0`
in every run); errors from independent replications (`ana.py`: −ln of the mean rate, sd of rates/√K).
Separations tried: PMODE 0 = donor swap (everything five layers and more beneath the watched face taken from another
stored configuration of the same level); PMODE 1/2 = toggling m distinct cells of the fifth layer (all 58 / 81 cells
of it at R = 9 / 11). `./rh run R SEED M NS LAG STEP PMODE DIV DL NS0`; rows in `out/ffs/`, pooled in `out/ffs/POOLED.txt`.

| R | separation | levels | K | pooled ln τ | − anchor | scatter of one replication |
|---|---|---|---:|---|---|---:|
| 9 | donor swap | 5 apart | 8 | 9.791 ± 0.011 | −0.028 ± 0.011 | 0.030 |
| 9 | 29 toggles (half the layer) | 2 apart | 16 | 9.787 ± 0.010 | −0.032 ± 0.010 | 0.038 |
| 9 | 4 toggles | 2 apart | 16 | 9.815 ± 0.011 | −0.004 ± 0.011 | 0.044 |
| 9 | 6 toggles | 4 apart | 16 | 9.827 ± 0.008 | +0.008 ± 0.008 | 0.030 |
| 11 | donor swap | 5 apart | 4 | 13.551 ± 0.042 | −0.082 ± 0.042 | 0.087 |
| 11 | 41 toggles (half the layer) | 2 apart | 12 | 13.609 ± 0.023 | −0.024 ± 0.023 | 0.080 |
| 11 | 6 toggles | 2 apart | 12 | 13.592 ± 0.055 | −0.041 ± 0.055 | 0.19 |

Reading: the same two failures split-hull reports, same sign (a separation makes the face die sooner; at R = 9 about
−0.03 for half a layer, 3 errors), and starvation once the separation is weak (0.19 per replication at R = 11 for
5 CPU-seconds; ± 0.03 at R = 17 would have needed of order an hour of one core, with an uncalibrated bias growing
like flips × stages). My strong setting is less biased at R = 11 than split-hull's (−0.024 ± 0.023 against its
−0.173 ± 0.044); the designs differ in that mine has no levels below 5 cells, where split-hull located its bias,
and toggles the whole layer [difference not investigated]. No R = 13, 15, 17 runs.
**Largest one-generation fall of P among sampled deaths:** mean 11.9 cells at R = 9 (P̄ = 21.6) and 16.4 at R = 11
(P̄ = 31.3): a typical death contains one generation that removes about half the mean population. Share of deaths
with a fall of at least half the face (A/2 cells): 1.5–1.9% (± 0.2%) at R = 9, 0.4% ± 0.2% at R = 11: falling, not
growing. Not measured at R ≥ 13.

## 3. Dip rates by plain running (`rh nu`) [measured]

256 hulls, soups 0.35, a hull replaced when any face is empty; all eight faces watched (rates per face and per
hull-generation of age > 200). Face flag set when P ≥ λ_A = ⌈P̄⌉ (from age 100); within an excursion below λ_A every
new minimum books a first passage of each level it newly reaches; a generation at which the hull dies counts for a
face only if that face is empty. 16 independent seeds per radius (24 at R = 19), errors from the scatter between
seeds. `sh nuchain.sh DIR; sh nuchain2.sh DIR; python3 nu.py DIR`, plus seeds 21–28 at R = 21 (250,000 generations) and
R = 19 (300,000) by hand (rows kept in `out/nu/`, so
`python3 nu.py out/nu` reproduces `out/NU-ANALYSIS.txt`; about 10 CPU-minutes in all).

| R | cells | hull-generations | P̄ (mine) | P̄ (split-hull) | ln ν(0.6 P̄) mine | split-hull | ln ν(0.5 P̄) mine | ln ν(0.4 P̄) mine |
|---|---:|---:|---|---|---|---|---|---|
| 9 | 45 | 8.4e8 | 21.6027 ± 0.0003 | 21.597 | −4.2102 ± 0.0002 | −4.208 ± 0.001 | −5.0610 | −5.9916 |
| 11 | 63 | 9.2e8 | 31.2531 ± 0.0003 | 31.255 | −4.9660 ± 0.0001 | −4.965 ± 0.002 | −6.2405 | −7.6604 |
| 13 | 84 | 9.2e8 | 42.4484 ± 0.0002 | 42.445 | −5.8975 ± 0.0002 | −5.899 ± 0.002 | −7.6784 ± 0.0006 | −9.6638 ± 0.0015 |
| 15 | 108 | 1.4e9 | 55.1942 ± 0.0002 | 55.203 | −7.0097 ± 0.0003 | −7.005 ± 0.002 | −9.3672 ± 0.0010 | −11.997 ± 0.005 |
| 17 | 135 | 1.4e9 | 69.4929 ± 0.0002 | 69.480 | −8.2976 ± 0.0006 | −8.304 ± 0.003 | −11.297 ± 0.003 | −14.646 ± 0.021 |
| 19 | 165 | 1.4e9 | 85.3452 ± 0.0003 | 85.381 | −9.7532 ± 0.0015 | −9.749 ± 0.007 | −13.445 ± 0.010 | −17.59 ± 0.07 |
| 21 | 198 | 1.0e9 | 102.7507 ± 0.0004 | 102.78 | −11.3692 ± 0.0033 | −11.387 ± 0.018 | −15.944 ± 0.034 | |

(R = 9, 11 entries of the 0.5 and 0.4 columns have errors below 0.0011; all levels and both conventions are in
`out/NU-ANALYSIS.txt`, PART A.) Levels p·P̄ are not integers: ln ν is interpolated linearly in the level, as
split-hull does, so a P̄ wrong by δ moves ln ν(p P̄) by about 0.4·p·δ at p = 0.6.

**The line (PART B).** −ln q(p) = ln τ(anchor) + ln ν(p P̄), anchors 9.819, 13.633, 18.141 ± 0.005, 23.3392 ± 0.0099
(errors of the first two are my assumption, 0.005 each):

| level | −ln q at 45, 63, 84, 108 | line: slope, χ² on 2 | rim term r if allowed | R = 17, line | R = 17, line + rim | R = 19, line | R = 21, line |
|---|---|---|---|---|---|---|---|
| p = 0.85 | 7.315 11.013 15.411 20.447 | 0.20819, 65 | −0.330 ± 0.043 | 29.092 | 29.246 ± 0.023 | | |
| p = 0.7 | 6.363 9.751 13.743 18.311 | 0.18953, 14 | −0.158 ± 0.043 | 29.171 | 29.245 ± 0.023 | | |
| p = 0.6 | 5.609 8.667 12.244 16.330 | 0.17016 ± 0.00014, 0.5 | −0.027 ± 0.043 | **29.219 ± 0.010** | 29.232 ± 0.023 | 35.780 ± 0.014 | 43.011 ± 0.019 |
| p = 0.5 | 4.758 7.392 10.463 13.972 | 0.14626, 0.1 | +0.011 ± 0.044 | 29.219 ± 0.011 | 29.214 ± 0.023 | 35.755 ± 0.017 | 43.080 ± 0.039 |
| p = 0.4 | 3.827 5.973 8.477 11.342 | 0.11925, 0.1 | −0.013 ± 0.045 | 29.206 ± 0.023 | 29.212 ± 0.032 | 35.73 ± 0.07 | |
| density 0.30 | 5.804 8.724 12.139 16.042 | 0.16249, 0.6 | −0.031 ± 0.043 | 29.211 ± 0.010 | 29.225 ± 0.023 | 35.757 ± 0.014 | 42.965 ± 0.020 |
| density 0.28 | 5.471 8.233 11.456 15.141 | 0.15348, 0.0 | −0.004 ± 0.043 | 29.217 ± 0.010 | 29.219 ± 0.023 | 35.759 ± 0.015 | 42.981 ± 0.023 |
| density 0.26 | 5.122 7.715 10.736 14.191 | 0.14395, 0.0 | +0.006 ± 0.044 | 29.213 ± 0.010 | 29.210 ± 0.023 | 35.737 ± 0.017 | 43.04 ± 0.04 |
| anchors alone (no ν) | | | −0.339 ± 0.043 | | 29.232 ± 0.023 | (35.816 ± 0.043) | (43.09 ± 0.07) |

The errors in one column are almost wholly the anchors' and are common to all rows; differences between rows are
known far better (they are differences of dip rates) and are significant at R = 19 and 21.

**The tests without a lifetime (PART E, G, D).**
- Level differences, line fitted on R = 9–15, checked at R = 17: 0.6 against 0.5: measured 2.9991 ± 0.0029, line
  2.9900, quadratic in k 3.0227; 0.6 against 0.4: 6.349 ± 0.020, line 6.355, quadratic 6.376; densities 0.30
  against 0.24: 3.603 ± 0.005, line 3.599, quadratic 3.643. Control with a known rim term (0.8 against 0.6): line
  off by 0.10, quadratic by −0.013 at R = 17, −0.049 at R = 19 and −0.108 at R = 21 (errors 0.001–0.003).
  The same level differences further out: 0.6 against 0.5, measured − line = −0.011 ± 0.009 at R = 19 and
  +0.087 ± 0.032 at R = 21; densities 0.30 against 0.24: −0.025 ± 0.017 and +0.05 ± 0.06.
- ln ν(p P̄) itself against its own quadratic in k from R = 9–15: at R = 17, +0.0025, −0.0016, −0.0077, +0.0005 ±
  0.0010, +0.020 ± 0.004 for p = 0.85, 0.8, 0.7, 0.6, 0.5 (the first one is +0.0005 at 0.6); at R = 19, −0.011, −0.014,
  −0.021, +0.012 ± 0.002, +0.076 ± 0.010; at R = 21, −0.016, −0.029, −0.034, +0.041 ± 0.004. A quadratic in k extrapolates one size step to
  0.01–0.02 and three steps to 0.03–0.05, on quantities where the truth is known.
- Second differences in k of ln ν(0.6 P̄): −0.176, −0.181, −0.176, −0.168 ± 0.002, −0.160 ± 0.004 (centred on
  R = 11 … 19); of ln ν(0.5 P̄): −0.258, −0.251, −0.241, −0.219 ± 0.011, −0.351 ± 0.039 (the last one against the
  trend: 820 events at R = 21). Interpolating ln ν between integer levels with three points instead of two changes
  none of these by more than 0.002 (PART H).

## 4. What I did not check

- The anchors themselves at R ≥ 13 (taken as given); the errors of the R = 9 and 11 anchors (assumed 0.005; my own
  brute force gives 9.8240 ± 0.0017 and 13.630 ± 0.011, which would move the R = 17 line forecast by about −0.004).
- Whether the line for −ln q holds below 0.3 P̄ at any size, or beyond 108 cells at any level: nothing here can.
- R = 7 (30 cells): under this protocol my runs give ln(8E/D) = 6.867 ± 0.008 after 4 × 10⁴ generations and 6.948 after
  2 × 10⁵, and P̄ scatters between seeds (± 0.15): some hulls seem to freeze with all eight faces occupied and
  inflate the exposure [conjectured, not verified]. So I neither confirm nor refute "the 30-cell face is 0.22 above
  the line"; what the lifetime-free test shows is that the 45-cell face is already 0.005–0.01 off the line of the
  larger ones in level differences.
- λ_A = ⌈P̄⌉ was taken from split-hull's P̄ (22, 32, 43, 56, 70, 86, 103); my own P̄ gives the same integers.
- The sampler beyond R = 11; the largest-fall statistic beyond R = 11.
