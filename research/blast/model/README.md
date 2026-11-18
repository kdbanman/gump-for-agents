# blast/model: models of the face-death rate against every number on file (2026-11-18)

Agent `model` of the blast. Brief: `../BRIEF-COMMON.md`. Forecasts: `PREDICTIONS.md` (blocks M1–M3, each committed
before the data it concerns was opened). Labels: **[measured]**, **[fitted]**, **[conjectured]**, **[post hoc]**.
Nothing here is proved. The session was cut to about 70 minutes; "Not checked" at the end is long.

## Short answer

1. **[fitted] The front gas with one σ fails on the data on file; with a free weight per loop length it fails less,
   and the data prefer growth exponential in the area to a power of the length.** 54 pooled wrapped faces of 48–126
   cells (everything `research/wrap/faces.py` loads, long tubes and the 96-cell faces included):

   | form | parameters | χ² (A ≥ 48, 54 faces) | χ² (A ≥ 36, 58 faces) |
   |---|---:|---:|---:|
   | FG: K·e^(−2σ\|v\|)·L_v^m, every loop direction | 5 (a, c, σ, K, m) | 3160 on 49 | 4473 on 53 |
   | FG2: the same with m = 2 | 4 | 7446 on 50 | 7536 on 54 |
   | SW: K·e^(−2σ\|v\|)·L_v·e^(gA) | 5 | 3350 on 49 | 4453 on 53 |
   | FGq: K_q·L_v^m, K free for loop² 12, 13, 16, 19, 21 | 8 | 358 on 46 (m = 1.70 ± 0.05) | 455 on 50 |
   | SWq: K_q·L_v·e^(g(A−63)) | 8 | 251 on 46 (g = 0.0143) | 322 on 50 |
   | GEN: K_q·L_v^m·e^(g(A−63)) | 9 | 222 on 45 (m = 0.23 ± 0.14, g = 0.025 ± 0.002) | 230 on 49 (m = 0.10 ± 0.10) |
   | HAZ (research/wrap): r_q·e^(g_q(A−63)), rates add | 10 | **87 on 44** | **107 on 48** |
   | EXPA: as HAZ, log-discounts add | 10 | 136 on 44 | 141 on 48 |

   Where FG fails exactly: (a) **the loop-length law is not e^(−2σ|v|).** The share of the death rate per loop
   direction at 63 cells is 0.130, 0.102, 0.055, 0.015, 0.001 ± 0.001 for loop² 12, 13, 16, 19, 21 (HAZ r_q; GEN
   K_21). From 12 to 13 to 16 it falls as e^(−1.3…1.7 per unit of girth); from 16 to 19 as e^(−3.7); from 19 to 21 by
   a factor above 5 for 5% more girth. One σ puts far too much discount on the "wide" faces (loop² 21–36):
   residuals −19σ to −32σ at the 57- and 63-cell equilateral faces, +6σ to +15σ at 75–108 cells. (b) **Growth with
   size:** with K_q free, a common power of L leaves the long loop² 12 tubes +6.4σ, +6.8σ (96, 108 cells) and the
   loop² 16 faces −5σ (72, 84, 96 cells); GEN drives m to 0.1–0.2. But no common growth law fits either: g_12 =
   0.0298 ± 0.0005, g_13 = 0.0290 ± 0.0009, g_16 = 0.0226 ± 0.0008 in HAZ. (c) **Small sizes:** refitted with the
   long tubes, HAZ takes the 36- and 39-cell equilateral faces at +2.5σ and +2.1σ (the frozen law of 2026-11-15
   missed them by 16σ and 9σ); FGq and SWq miss them by +4σ to +5σ; FG by −20σ, −10σ. (d) **Rates add better than
   log-discounts** (87 against 136 at equal parameters); the worst multi-loop face is (12, 0, 16) at 48 cells,
   −3.7σ (0.004 in ln τ). What survives of the front gas: D/L² ≈ constant on the loop² 12 tubes is real
   (PI's arithmetic), and the PI's 120-cell number agrees with every form that fits (24.52–24.59).
   `python3 research/blast/model/frontgas.py 48` (and `36`); outputs `data/frontgas_48.txt`, `data/frontgas_36.txt`.

2. **[measured] σ from the empty-patch counts, all shapes: 0.50 to 0.73 per lattice unit, depending on the shape
   family and on the bulk price assumed; no two-term form fits all shapes.** Rhombi from 2×2: σ = 0.55 (c free:
   0.243), 0.71–0.73 (c = 0.2086 forced). Strips 1×b (the shapes nearest to a band): σ = 0.50 (c free: 0.220), 0.52
   (c forced). Every shape of ≥ 12 cells in one fit: σ = 0.42–0.50 with residuals above 1 nat. The strip that wraps
   the 12×12 face (1×12) is 0.45 nats cheaper than the open-strip trend (it has no ends). So "σ ≈ 0.66" is inside
   what the patches allow and is not fixed by them. **[post hoc]** The full cost per unit length of a one-unit-wide
   empty strip, 1.65 (= 3 × 0.55), predicts the ratios of the tube shares between girths as e^(−1.65 Δg): 0.79 and
   0.52 for loop² 12→13 and 13→16, against 0.78 and 0.54 measured (HAZ r_q); it fails beyond (16→19: 0.55 against
   0.27; 19→21: 0.69 against < 0.2). `python3 research/blast/model/patches.py`.

3. **[fitted] The hull faces do not need a second price.** With the wide wrapped price held at c = 0.2086,
   ln τ = c·A + b·k + d + e/k (k the side in unit cells; three free numbers) fits the five hull faces of 30–108 cells
   with χ² 16.8 on 2 (worst 3.1σ = 0.008 in ln τ, at 45 cells); "two prices" (a free price per cell, b·k + d) has
   χ² 152.8 on 2 on the same five (it cannot take the 30-cell face: 10σ) and 0.0 on 1 on 45–108 cells, where
   every three-number form fits (m·ln A: m = −1.45, χ² 0.9; e/k: 2.1). Forecasts: 135 cells 29.17–29.21 (expansion
   forms) against 29.23 (two prices); 165 cells 35.66–35.72 against 35.81. No version of the front gas touches the
   hull's excess: fronts only add ways to die, and a hull face already has the *lower* density and the *larger*
   variance (ρ 0.497, s² 0.436 at 63 cells against 0.517, 0.388 wrapped) yet lives 0.47 longer; its excess is in the
   tail (price per live cell lost 0.50 against 0.42–0.44). `python3 research/blast/model/hull.py`.

4. **[measured] New: the living state of a tube is not the living state of a wide face, and it does not depend on
   the tube's length.** Stationary cumulants per cell of the face population P (1.5 × 10⁸ samples per face):

   | face | ρ | κ₂/A = s² | κ₃/A | κ₄/A |
   |---|---|---|---|---|
   | tube loop² 12, 78 / 84 / 96 / 108 / 120 cells | 0.51542–0.51544 | 0.4024, 0.4021, 0.4022, 0.4023, 0.4023 | −0.491, −0.488, −0.488, −0.489, −0.489 | +2.12, +2.07, +2.04, +2.04, +2.03 |
   | tube loop² 13, 75 / 96 cells | 0.51612, 0.51614 | 0.3972, 0.3967 | −0.465, −0.455 | +2.08, +1.87 |
   | one loop² 16, 96 cells | 0.51699 | 0.3886 | −0.388 | +1.47 |
   | wide (no loop² < 25): 75 / 93 / 108 / 111 cells | 0.51752–0.51773 | 0.3819, 0.3792, 0.3784, 0.3781 | −0.362, −0.319, −0.304, −0.301 | +1.54, +0.98, +0.77, +0.71 |

   (errors: ρ ± 0.00003, s² ± 0.0002, κ₃/A ± 0.004.) A loop² 12 raises the variance per cell by 6% and makes the
   third and fourth cumulants extensive (wide faces' κ₃/A and κ₄/A are still shrinking with area: their non-Gaussian
   part is the tail itself, not extensive). "The differences are not in the living state" (the brief) holds for the
   density to 0.4% and fails for the fluctuations. `python3 research/blast/model/cumulants.py`.

5. **[measured, zero fitted numbers] The tilt estimate from the first two stationary moments gives the size and
   order of the wrapping discounts, not their growth with length.** D_var = A·(λ·δρ + ½λ²·δs²) with δρ, δs² against
   the wide faces at equal area (s²_wide = 0.3703 + 0.858/A) and λ = 0.41 (tail slope of ln π(n), item 6):

   | face | D_var | D measured | ratio |
   |---|---|---|---|
   | loop² 12 tubes, 54 / 60 / 66 / 78 / 84 / 96 / 108 cells | 0.153, 0.158, 0.171, 0.210, 0.229, 0.273, 0.318 | 0.091, 0.117, 0.142, 0.198, 0.224, 0.302, 0.390 | 1.68, 1.35, 1.20, 1.06, 1.02, 0.90, 0.81 |
   | loop² 13, 75 / 96 cells | 0.145, 0.201 | 0.140, 0.236 | 1.04, 0.85 |
   | loop² 16: 4×4 (48 cells), (4,0),(0,8) (96 cells) | 0.154, 0.102 | 0.108, 0.109 | 1.43, 0.94 |
   | loop² 19 ×3 (57 cells); 12 ×3 (36 cells) | 0.057; 0.340 | 0.036; 0.166 | 1.59; 2.05 |

   As a law it fails (Σ z² = 4594 on 20 faces): the tube's moments are constant in its length while its discount
   per cell rises from 0.0017 to 0.0036. **[conjectured]** The rest is in the higher cumulants: the tilt series
   λf + λ²δκ₂/2 − λ³δκ₃/6 + λ⁴δκ₄/24 for the loop² 12 tube reads 0.0009 + 0.0027 + (0.002–0.004) + (0.0015–0.0024)
   per cell and has not converged at fourth order: its sum, 0.007–0.011, is the discount per cell of a long tube
   (measured local value from 96 to 108 cells: 0.0074), i.e. a tube price of 0.198–0.201 per cell. This is the
   PI's front gas seen from the stationary side: a one-dimensional object with its own fluctuation law per unit
   length. `python3 research/blast/model/moments.py 0.41` (output `data/moments_041.txt`).

6. **[measured] The quasi-stationary population distribution π(n) of wrapped faces, down to n = 1** (48, 57, 60,
   63, 66 cells; `data/hist_gen_*.txt`): ln π(n) is Gaussian down to about 0.75 P̄, then bends into a tail whose
   local slope is not constant: it peaks at 0.40 (48 cells), 0.43 (63 cells), 0.44 (66-cell tube) per live cell
   near n ≈ P̄/2 and falls to 0.33–0.39 at 4–8 cells, with an odd–even ripple below 6. The death rate is 0.73–0.78 ×
   π(1). The chance that a dip to n continues to death falls by e^(−0.42…0.45) per cell (63 cells; 0.50 on hull
   faces, `research/dying`). **The tangent construction is not a predictor:** with the slope taken over
   0.15–0.45 P̄, ln τ − [A(λρ − λ²s²/2) + ½ln(2πσ²)] = +0.01, +0.10, −0.25, −0.22, −0.62 at 48, 57, 60, 63, 66
   cells; the window slope rises with area (0.354, 0.367, 0.387, 0.390, 0.411) and ln τ moves by A·x_t ≈ 23 per unit
   of λ. `python3 research/blast/model/qsd.py --summary gen_4_0_4_c1 gen_1_7_19_c1 gen_1_8_20_c1 gen_1_4_21_c1 gen_1_5_22_c1`.

## Ranked models

| # | model, in three lines | fitted numbers | against the anchors | kills it |
|---|---|---:|---|---|
| 1 | **Two ways to die, rates add (HAZ refitted).** 1/τ = e^(−a−cA)(1 + Σ_v r_q e^(g_q(A−63))): a short loop opens a second channel at price c − g_q. A description; the only form within reach of the errors. | 10 | χ² 87 on 44 (A ≥ 48), 107 on 48 (A ≥ 36); hull: not addressed | the 120-cell tube above 24.55 (HAZ says 24.51; it is already −2.6σ at 108 cells): then the channel's price is not constant |
| 2 | **A tube has its own price (stationary cumulants).** Tubes are one-dimensional: ρ, κ₂, κ₃, κ₄ per cell independent of length; long-tube price c − Δ, Δ = tilt series of the cumulant differences, 0.007–0.011 for loop² 12. Short tubes cross over. | 0 (λ measured) | second order alone: discounts within 20% at 66–96 cells, ×1.7 at 54, ×0.8 at 108 (Σ z² 4594 on 20) | local slope of the loop² 12 tube from 120 to 240 cells outside 0.196–0.202 |
| 3 | **Rim as an expansion in the side at the wrapped price.** Hull: ln τ = 0.2086·A + b·k + d + e/k. | 3 | χ² 16.8 on 2 (30–108 cells); two prices 152.8 on 2 | the 135-cell hull face at 29.23 or above (expansion: 29.17–29.21) |
| 4 | **Front gas, weight per loop length free (FGq / SWq / GEN).** | 8–9 | χ² 358 / 251 / 222 on 46–45 | already: long tubes +6σ, loop² 16 faces −5σ |
| 5 | **Front gas, one σ (FG).** | 5 | χ² 3160 on 49 | dead on file (the cutoff between loop² 19 and 21) |
| 6 | **Tangent construction c = λρ − λ²s²/2 with measured λ.** | 1 (additive constant) | spread 0.63 in ln τ over five faces of 48–66 cells | dead as a predictor; survives as bookkeeping |
| 7 | **Logistic mean field, c = −ln(1 − ρ) − ρ = 0.2116.** No fitted number, 1.4% high. | 0 | wrong tail (slope ln β = 0.73 at n → 0 against 0.35–0.45), wrong s² (0.48 against 0.38), dc/dρ = 1.07 | dead: a coincidence of the integral |

## Forecasts and scores (`PREDICTIONS.md`)

- M1 (commit e0f4d78, before the 96-cell rows were opened): loop² 13 at 96 cells 19.810 ± 0.012, **measured
  19.8109 ± 0.0062 (inside)**; loop² 16 at 96 cells 19.920 ± 0.012, **measured 19.9373 ± 0.0060 (outside, +0.017)
  and 19.9284 ± 0.0063 (inside)**; "the two equal within 0.008": 0.0089 ± 0.0087 (missed narrowly).
  Open: 120-cell tube 24.560 ± 0.020; 240-cell tube 48.0 ± 0.35 (revised in M3 to 48.40 ± 0.25); wide face near 200
  cells: wide line − 0.02 ± 0.06; hull 135 cells 29.200 ± 0.035; hull 165 cells 35.72 ± 0.09.
- M2 (commit 8190fb7, before any 66- or 84-cell histogram was looked at): variance excess of the tube over the wide
  face 0.013 ± 0.005 at 66 cells, **measured 0.0164 (inside)**; 0.021 ± 0.005 at 84 cells, **measured 0.0203
  (inside)**. The reasoning was half wrong (see M3): the excess grows because the wide faces' variance falls.
- Tangent construction "works to 0.3 with one constant": I gave 35%; it fails (spread 0.63).
- The times in the block headers run two to five minutes ahead of the machine clock; the commits carry the true order.

## What was run, and on what it rests

- Stepper: `research/dying/ex3.c` (512 bit-sliced replicas on a cell graph from `research/theory/symmetric/geom.py`;
  renewal lives from 0.4 soups; P histogram over exposure at age > 512; excursion table by minimum P).
- **Validation (mine):** `python3 research/blast/model/validate.py 1500` → `data/validate_out.txt`, ALL OK: for each
  of 8 wrapped slabs (48–84 cells) and 3 hulls (45–84 cells), `sy trace` on the graph file equals a naive stepper
  written from `reference/oracle.py`'s offsets and rule constants (populations at every generation 0–1500, cell sets
  at generations 1, 2, 3, 10, 100, 1500); one redirected neighbour slot fails; ex3's lives file is byte-identical to
  sy's. Not validated this way: the faces used only for stationary moments beyond that list (96–120 cells and
  others: same code path, graphs from the same generator), and ex3's histogram bookkeeping (cross-checks: my ln τ
  from the same files agree with the anchors: 9.931 ± 0.005 / 9.9251, 11.874 ± 0.007 / 11.8751, 12.422 ± 0.008 /
  12.423, 13.152 ± 0.009 / 13.1622, 13.668 ± 0.012 / 13.646).
- Runs: `queue1.sh` (long histograms; killed after the 66-cell tube to save time) and `queue2.sh` (short runs for the
  moments, 150,000 generations × 512 replicas each, then the 84-cell pair). ex3 counts faces of at most 127 cells,
  so nothing above 120 cells.

## Failed, in a line each

- Tangent construction as a formula for c or for the discounts: too sensitive to λ, and λ is not a constant.
- "The growth of the tube discount with length is a growth of its variance" (M2's reasoning): the tube's variance is flat.
- A single exponential in the girth for the loop weights (the patch strip cost): right from 12 to 16, wrong beyond.
- A Poisson gas of identical band voids as the whole of (f, δκ₂, δκ₃, δκ₄): the sizes it implies disagree
  (δκ₂/f = 15 live cells, δκ₃/δκ₂ and δκ₄/δκ₃ = 4–10).

## Not checked

- No derivation of λ from the rule (the brief's line 1): not attempted in the time.
- The 84-cell pair's tails (tube against wide at equal area): running when this was written; see the last section if present.
- Hull histograms (ρ, s², tail) were taken from `research/dying/README.md`, not rerun.
- Errors of the hull fits use the tabulated statistical errors only; the 30-cell face may carry small-size effects
  that no expansion should be asked to fit.
- The wide reference for s² rests on four faces (75–111 cells); λ = 0.41 is a round value between the measured
  0.39 and 0.44; the ratio column moves by about ±8% for ±0.02 in λ.
- Sweep or flash (the brief's line 4) was not confronted beyond what GEN says (growth exponential in A, i.e. a
  second price, is preferred to a count of places).
- Other agents' directories were not read.
