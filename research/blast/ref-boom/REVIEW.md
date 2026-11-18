# ref-boom: referee's review of `research/blast/boom` (2026-11-18, 04:45–05:15 UTC)

Referee: agent `ref-boom`. Boom's README was read for its definitions; its code was neither read nor run.
Labels: **[proved]**, **[measured]**, **[conjectured]**. Every number below is mine unless it says "boom".

## Verdicts

| claim | verdict | my number |
|---|---|---|
| 1. one hump of launches at 0.738·A | **CONFIRMED** | mean launch 0.7380 ± 0.0002 (48), 0.7386 ± 0.0005 (57), 0.7382 ± 0.0006 (63), R75MEAN (75); one local maximum at every size; 97.8%, 97.8%, 98.6% above 0.60·A |
| 1b. "s.d. about 0.06·A, the same at 48…84" | **CORRECTED** | the s.d. is 3.07, 3.39, 3.58 cells = 0.0639, 0.0595, 0.0568 of A: it grows like A^0.57±0.03, close to √A (0.443, 0.449, 0.451 of √A), not like A. 75 cells: R75SD |
| 2a. the sum rule 1/τ = Σ ν·d | **an identity** [proved], not a finding | Σ_p (launches at p)/(exposure) = deaths/exposure for any definition of "launch" |
| 2b. I_up(0.74) = 0.078, J(0.74) = 0.132 ± 0.003 | **CONFIRMED** as numbers | I_up = 0.079–0.080, J = 0.135–0.136 ± 0.0014 (48, 57, 63 cells; linear or quadratic interpolation) |
| 2c. min_θ [I_up + J] = 0.2099 "against the price 0.2087" | **REFUTED as evidence** (bookkeeping + noise) | by the identity the minimum is the lifetime's own slope over the sizes used. Mine: 0.2145 ± 0.0012 (linear), 0.2168 (quadratic) against my lifetime slope 0.2147 ± 0.0007 over 48–63. With 75 cells: R75MIN |
| 3. launch = breath of the top four layers, in one step from a normal face, layers 2–4 under-full one generation before | **CONFIRMED** (63 cells, 9,785 deaths) | launch 0.738 / 0.637 / 0.562 / 0.504; one before 0.524 / 0.400 / 0.354 / 0.375 (living 0.517 / 0.435 / 0.406 / 0.416); one after 0.221 / 0.151 / 0.190 / 0.302. A third of the under-fill is generic to any over-full generation; the rest is specific to deaths |
| 4. the kill is a fragmentation; fail(size) = 0.90, 0.64, 0.28, 0.08; ≥ 7 cells regrow 99.4% | **CONFIRMED** (the island table) | 63 cells: 0.900 ± 0.001, 0.634 ± 0.004, 0.276 ± 0.005, 0.078 ± 0.003 (sizes 1, 2, 3, 4–6); 0.0051 ± 0.0007 (7–12); 0 of 33,214 (> 12). 48 cells: 0.899, 0.631, 0.282, 0.085, 0.0052, 0 |

## 1. Stepper, validation, lifetimes

`rb.c`: my own stepper for the 8-layer slab with period lattice (H,K),(0,D) (hexagonal basis e1 = (2,−2,0),
e2 = (2,0,−2) in doubled coordinates), written from `docs/AUTOMATON.md` and `reference/oracle.py`; 64 replicas,
bit-sliced. `val.py`: the trajectory S_0…S_g of one replica is checked one generation at a time: S_t is tiled into
an oracle array of side 44 (dead outside the slab), the ORACLE steps once, every cell with all coordinates in
[2, 41] is compared with S_{t+1}; every class of cell is compared at every step (asserted), the class map is constant
on the period lattice and has 3HD values per layer (asserted), the shortest loops² are printed.
[measured] `python3 val.py 4 0 4 1000` (loops² 16,16,16), `python3 val.py 1 4 21 1200` (21,21,21),
`python3 val.py 1 7 19 1000` (19,19,19), `python3 val.py 1 9 25 1000`: 0 mismatching generations each; with `neg`
appended (one neighbour of one cell swapped) each fails (e.g. 152 mismatching generations of 1,000 at 48 cells).

Protocol: a replica starts from a 40% soup and is counted after 300 generations; a face dies when its layer is
empty; the replica is then restarted. Exposure = face-generations with the face alive; ln τ = ln(exposure/deaths).
A replica whose state repeats after 840 generations is restarted (91, 3, 0 times at 48, 57, 63 cells).
Fresh seeds (`run.sh`, `run2.sh`; `python3 an.py r48 r57 r63 r75` → `out_all.txt`):

| vessel | cells | face-generations | deaths | ln τ | anchor | |
|---|---:|---:|---:|---|---|---|
| (4,0),(0,4) | 48 | 2.5e9 | 122,130 | 9.9267 ± 0.0029 | 9.9251 ± 0.0004 | +0.6 s.e. |
| (1,7),(0,19) | 57 | 2.0e9 | 13,842 | 11.8810 ± 0.0085 | 11.8751 ± 0.0004 | +0.7 |
| (1,4),(0,21) | 63 | 5.0e9 | 9,785 | 13.1441 ± 0.0101 | 13.1622 ± 0.0007 | −1.8 |
| (1,9),(0,25) | 75 | R75E | R75D | R75LT | 15.6442 ± 0.0030 | R75Z |

[measured] The 63-cell torus is 1.8 s.e. low here and was 1.2 low in boom's run (13.148 ± 0.012): the two CPU
codes together give 13.146 ± 0.008, 2.1 s.e. below the GPU anchor. Not significant; worth a third look by someone.

## 2. (a) The launch distribution [measured]

Launch = last generation with P ≥ ceil(A/2) before the face is empty.

| cells | deaths | mean θ | s.d. (cells) | s.d./A | s.d./√A | skew | above 0.60·A | launch → empty, median (10–90%) |
|---|---:|---|---|---|---|---|---|---|
| 48 | 122,130 | 0.7380 ± 0.0002 | 3.068 ± 0.006 | 0.0639 | 0.443 | −0.43 | 0.978 | 5 (3–10) |
| 57 | 13,842 | 0.7386 ± 0.0005 | 3.391 ± 0.020 | 0.0595 | 0.449 | −0.43 | 0.978 | 5 (3–10) |
| 63 | 9,785 | 0.7382 ± 0.0006 | 3.578 ± 0.026 | 0.0568 | 0.451 | −0.43 | 0.986 | 5 (3–10) |
| 75 | R75D | R75MEAN | R75SDC | R75SDA | R75SDR | | | |

One hump: the histogram has a single local maximum at every size (48 cells: 307, 284, 411, 618, 1042, 1848, 2880,
4682, 7397, 10222, 13546, 15909, 16873, 15407, 12546, 8649, 5160, 2686, 1118, 411, 115, 18, 1 at p = 24…46; the 307 at
p = 24 is the pile-up at the cut A/2). Its place is 0.738·A to four parts in ten thousand. Its width is NOT a fixed
fraction of A: s.d. ∝ A^γ with γ = 0.570 ± 0.027 (48, 57, 63 cells; boom's own 0.064 at 48 and 0.056 at 63 say the
same; its 75 and 84 have 242 and 43 deaths). R75GAMMA
"Over-full" needs a scale: the living face has s.d. 0.093·A (48) and 0.078·A (63), so the launch is +2.4 and +2.8
s.d., and the 2% of launches below 0.60·A are within about one s.d. of an ordinary generation.

## 3. (b) ν, d, the sum rule and the two-term price

**Numbers** [measured]. ν(p) = (face-generations at p)/exposure, d(p) = (launches at p)/(face-generations at p).
63 cells, d(p)·10⁴ at p = 44…53: 0.343, 0.779, 1.73, 3.76, 7.9, 15.0, 31.4, 61.5, 122, 207 (boom at 47…53: 4.0, 7.7,
16, 30.2, 56, 124, 170: agreed). "Each extra cell is half as frequent and twice as deadly": ν(p+1)/ν(p) = 0.49 and
d(p+1)/d(p) = 2.2 at the hump, at 48, 57 and 63 cells. CONFIRMED.

**The sum rule is an identity** [proved]. Write n(p) for the face-generations at p, ℓ(p) for the launches at p, E for
the exposure, M for the deaths. Then ν·d = ℓ/E, and Σ_p ℓ(p) = M because each death has exactly one launch. This
holds for any definition of "launch" and any dynamics. (Boom's check "by cloning" tests the cloning estimator of d,
which is a fair test of that estimator; it is not a test of the rule.)

**What the identity does to the two-term price** [proved]. With w_A(p) = ℓ(p)/M the launch histogram,
ν(p)·d(p) = w_A(p)/τ exactly, so at p = θA, for any sizes and any common way of taking the slope in A,

    I_up(θ) + J(θ)  =  [slope of ln τ over the sizes used]  −  d/dA ln( √A · w_A(θA) ).            (*)

I_up + J contains nothing that is not in the lifetimes and in the launch histogram. For a hump of s.d. σ_A ∝ A^γ
cells the second term at the hump's top is (γ − ½)·d ln A/dA:

    min_θ [I_up + J]  =  c_τ(sizes used) + (γ − ½)/A ,    and I_up + J − min is how fast the hump narrows in θ.

So the minimum sits where the launches are by construction, and its value is the lifetime's own slope for the sizes
used, to within (γ − ½)/A ≈ 0.001. Checked numerically: the two sides of (*) agree to four decimals at every θ
(`out_all.txt`, "identity check").

**My values** [measured] (`python3 an.py r48 r57 r63 r75`; bootstrap = Poisson resampling of the launch counts):

| sizes | lifetime slope, my runs (anchors) | min I_up + J, linear in p | quadratic fit of ln ν, ln d in p | nearest integer p |
|---|---|---|---|---|
| 48, 63 | 0.2145 ± 0.0007 (0.2158) | 0.2139 at θ = 0.745; at 0.74: 0.2141 ± 0.0014 | 0.2159 ± 0.0009 at 0.740 | at 0.74: 0.2147; grid minimum 0.2091 at θ = 0.675 |
| 48, 57, 63 | 0.2147 (0.2159) | 0.2145 ± 0.0012 at 0.740 (I_up 0.079, J 0.135) | 0.2168 at 0.74 (I_up 0.080, J 0.137) | at 0.74: 0.2277; grid minimum 0.1994 at θ = 0.695 |
R75ROWS

- **Interpolation.** θA is 35.52 and 46.62 at θ = 0.74. Linear interpolation of ln ν and ln d between the two
  integers, and quadratics in p fitted over 0.62–0.88·A, agree to 0.001 on I_up, 0.002 on J and 0.002 on the sum.
  Rounding p to the nearest integer does not work at these sizes: ln ν changes by 0.7 and ln d by 0.8 per cell, a
  rounding error of up to half a cell at each size is divided by ΔA = 15, and I_up at θ = 0.72 comes out 0.030
  instead of 0.065, J 0.193 instead of 0.151; the sum then wanders between 0.199 and 0.249 and its "minimum over θ"
  is whichever rounding is luckiest (0.2091, 0.1994 above). Boom's I_up row is smooth, so boom did not round ν; I
  cannot tell from the README what was done to d. The two errors cancel in the sum only if ν and d are interpolated
  the same way at the same p.
- **The honest error of "0.2099".** (i) Boom's own ± 0.003–0.004 on J at each θ (242 deaths at 75 cells). (ii) It is
  the smallest of seven noisy values (its neighbours are 0.217 and 0.212): a parabola through boom's seven sums
  bottoms at 0.2111 at θ = 0.744 with residuals of 0.0016, so the pick of the lowest point is worth −0.001 to −0.003.
  (iii) Interpolation ± 0.002. (iv) By (*) the true value for boom's sizes is their lifetime slope: 0.2120 (anchors,
  line through 48, 63, 75) to 0.2158 (48 → 63). Boom's own lifetimes (9.9182, 13.148, 15.663, 17.39 ± 0.15) have an
  unweighted slope of 0.2129 over 48–75 and 0.2083 over 48–84, the latter low because its 84-cell run (43 deaths)
  came out 0.15 low. **"0.2099" is 0.212 ± 0.004, and it is boom's own lifetime slope read back through the launch
  histogram.** Its agreement with 0.2087 to 0.001 is an accident of ± 0.004; the same computation on clean data from
  48–63 cells gives 0.2145–0.2168, the slope of those lifetimes, and not 0.2087.
- **Was the agreement forced?** The agreement with the lifetime slope OF THE SAME RUNS is forced [proved]. The
  agreement with 0.2087, the slope of other, larger faces, is not forced and, done cleanly, is not there
  (0.2145–0.2168 against 0.2087: the lifetime curve between 48 and 63 cells is steeper than the wide-face line; the
  48-cell torus has loops² of 16).
- **Laplace or a growing term?** [measured] If ν and d each had a large-deviation law at fixed θ, the hump would be
  √A cells wide (γ = ½), boom's √A in front of ν would be the right normalisation, the minimum over θ would be the
  right asymptotic statement and the sum over θ would add a constant to ln τ. If the hump kept its shape in θ (γ = 1,
  what claim 1 says in words), I_up + J would be flat in θ, there would be no minimum, and the sum over θ would add
  −½·ln A to ln τ. Measured: γ = 0.570 ± 0.027 over 48–63 cells. So Laplace is nearly right: the sum over θ
  contributes about (γ − ½)·ln A ≈ 0.07·ln A, a change of slope of 0.001 per cell at these sizes, and no term that
  grows in any way that matters. The curvature agrees roughly: I_up + J rises by 0.012 at θ = 0.68 and 0.011 at
  0.80 (boom: 0.019, 0.016), which gives a Laplace width of 0.050·A at 63 cells against the measured 0.057·A.
- **What is prediction and what is bookkeeping.** Bookkeeping: the sum rule; that the minimum of I_up + J is at the
  launch hump; that its value is the price of the sizes used. Measurement with content: the launch is at
  θ* = 0.738 at every size (a number a theory must produce); the cost at θ* splits into I_up = 0.079 (how rare an
  over-full face is; a property of the living state, measurable without a single death) and J = 0.135 (how rarely
  such a face is the last full one); across the hump (θ* ± one s.d.) the split runs from 0.04 + 0.19 to 0.13 + 0.09.
  Prediction: none. Nothing here gives the price of a size that has not been run to its deaths, because J is
  measured from the deaths.

## 4. (c) The layer profile [measured; 63 cells, 9,785 deaths; shares of A; layers counted from the dying face]

| generation | face | layer 2 | layer 3 | layer 4 | boom |
|---|---|---|---|---|---|
| living state | 0.517 | 0.435 | 0.406 | 0.416 | 0.517 / 0.435 / 0.406 / 0.416 |
| launch − 2 | 0.493 | 0.421 | 0.400 | 0.407 | 0.496 / 0.419 / 0.399 / 0.407 |
| launch − 1 | 0.524 | **0.400** | **0.354** | **0.375** | 0.525 / 0.399 / 0.355 / 0.377 |
| launch | 0.738 | 0.637 | 0.562 | 0.504 | 0.732 / 0.637 / 0.562 / 0.507 |
| launch + 1 | 0.221 | 0.151 | 0.190 | 0.302 | 0.230 / 0.154 / 0.191 / 0.297 |
| launch + 2 | 0.118 | 0.154 | 0.241 | 0.351 | 0.127 / 0.158 / 0.242 / 0.347 |

48 cells (122,079 deaths): 0.495/0.421/0.397/0.406, 0.524/0.399/0.354/0.376, 0.738/0.637/0.561/0.504,
0.222/0.152/0.189/0.299, 0.120/0.154/0.241/0.348. CONFIRMED to 0.005 beneath the face; boom's face is 0.006–0.009
off mine at and after the launch (0.732, 0.230, 0.127 against 0.738, 0.221, 0.118; its 0.732 is also under its own
mean launch of 0.7375, so its profile runs select the deaths a little differently).

The control boom did not make: ALL generations with the same face population as a launch (weighted by the launch
histogram; a sample of 1 in 8), one generation before, at, and after:

| | face | layer 2 | layer 3 | layer 4 |
|---|---|---|---|---|
| before a death's launch | 0.525 | 0.401 | 0.355 | 0.375 |
| before any generation with that p | 0.524 | 0.428 | 0.389 | 0.406 |
| at a death's launch | 0.742 | 0.638 | 0.562 | 0.503 |
| at any generation with that p | 0.742 | 0.487 | 0.428 | 0.419 |
| after a death's launch | 0.220 | 0.151 | 0.190 | 0.302 |
| after any generation with that p | 0.362 | 0.375 | 0.374 | 0.411 |

So (i) the precursor is real: with the face normal (0.524), layers 2–4 are 0.035, 0.052, 0.041 of A under the
living state one generation before a fatal launch, of which 0.007, 0.017, 0.010 is what any over-full face has
behind it and 0.027, 0.034, 0.031 is specific to the deaths. In units of a layer's own fluctuation (about 0.08·A)
that is 0.4–0.6 s.d. per layer: a tilt of the odds, not a warning sign. (ii) What separates a fatal launch from an
ordinary over-full face is the layers beneath AT the launch: an ordinary face of 0.74·A has 0.487/0.428/0.419
beneath it (nearly normal), a fatal one 0.638/0.562/0.503. The over-full face is cheap (I_up); the deep over-fill
is where J is paid. (iii) An ordinary over-full face falls to 0.36·A the next generation, a fatal one to 0.22·A.

## 5. (d) Islands [measured] (`./rbi island 1 4 21 302 600 …/i63.txt; python3 ani.py i48 i63` → `out_islands.txt`)

My procedure, from boom's description: take the state one generation after a face of q ≥ 0.62·A cells; group the
live face cells into clusters through in-layer neighbours; run the state once per cluster with every other cell of
that face killed and everything beneath untouched; "fails" = the face is empty before it is half full again.
15,000 parents in each of three bands of q (0.62–0.70, 0.70–0.78, ≥ 0.78 of A); no run undecided after 400 generations.

| cluster size | 1 | 2 | 3 | 4–6 | 7–12 | > 12 |
|---|---|---|---|---|---|---|
| fails, 63 cells | 0.900 ± 0.001 | 0.634 ± 0.004 | 0.276 ± 0.005 | 0.078 ± 0.003 | 0.0051 ± 0.0007 | 0 of 33,214 |
| fails, 48 cells | 0.899 ± 0.001 | 0.631 ± 0.004 | 0.282 ± 0.006 | 0.085 ± 0.003 | 0.0052 ± 0.0007 | 1 of 29,167 |
| boom | 0.90 | 0.64 | 0.28 | 0.08 | 0.006 | 0.000 |

The same in the three bands of q to 0.03. Clusters of 7 or more regrow 99.89% of the time as they occur (99.5% for
7–12 cells; the largest that failed had 11 cells at 63 and 14 at 48). CONFIRMED. Not tested: the second half of
claim 4 (the products of failure chances, the cancelling errors), the survivors' statistics of the fatal busts.

## 6. (e) Other things in boom's README

- Sentence 1, "every death … is launched from an over-full generation": true by definition for P ≥ A/2; the content
  is the hump (§2). "The same at 48, 63, 75, 84" is right for the mean and wrong for the width.
- Sentence 2 presents the sum rule as measured and the minimum as agreeing with the anchors: see §3. The table's
  header "anchors: 0.2087 (63–111 cells), 0.2115 (48–84)" already holds the fair comparison (0.2115).
- "J(θ) ≈ 0.5·(1 − θ)": mine is 0.135, 0.120, 0.108, 0.091, 0.073 at θ = 0.74…0.82 against 0.130, 0.120, 0.110,
  0.100, 0.090: fair to 0.74–0.78, 20% high at 0.82.
- §5's maps and §6's tube comparisons: NOT TESTED.

## 7. What the owner may be told about "a formula for the price"

There is no formula yet, and boom's 0.2099 is not one. What boom found, and I confirm with my own code, is the route:
a wrapped face dies when, in one generation and from an ordinary state, its top four layers fill together (the face
to 0.738 of its area, at every size from 48 to 63 cells to four parts in ten thousand), crash together in the next
generation, and leave only fragments of fewer than seven cells, which cannot regrow. The death rate can be written
exactly as (how often the face is that full) × (how often such a face is the last full one), and at the launch point
the first factor costs 0.079 per cell and the second 0.135. But that product is arithmetic: the two numbers were
measured from the same runs whose lifetimes they are supposed to explain, and their sum must return those runs' own
price (0.2145 for 48–63 cells in my runs, where the faces' lifetimes have slope 0.2147), whatever the mechanism.
Boom's 0.2099 matching the wide faces' 0.2087 is noise of ± 0.004 around 0.212. A formula would have to produce
three numbers from the rule: the launch point 0.738, the cost 0.079 of an over-full face (a property of the living
chaos alone, so the easier one), and the cost 0.135 of the layers beneath filling with it and the crash leaving
only fragments. The split is the useful thing: it says 63% of the price is paid below the face and in the kill.

## 8. Not checked

- 84 cells and above; tubes; hulls; boom's §5 (maps), §6 (tubes), §7, §8.
- The cloning estimate of d (I used natural deaths only).
- Why my 63-cell lifetime is 1.8 s.e. under the anchor (protocol differences with the GPU code were not examined).
- Periods that do not divide 840 are not caught by the restart check.
- The production runs r48, r63 were made with the first build of `rb.c`; the island mode was added afterwards and
  built as `rbi`; `rbi run` reproduces `rb run` byte for byte on a 2e7 test (`cmp test48.txt test48b.txt`), and
  r57, r75 were run with `rb` (first build). No second reader for `an.py`.

## 9. Forecasts (PREDICTIONS.md, commit 782d9f5, before any run)

1. min I_up + J from 48, 63 in 0.216–0.226: **miss** as stated (0.2139–0.2159); the reason given (it returns the
   lifetime slope, not 0.210) held, and I had taken the anchors' slope 0.2158 as the floor where my runs have 0.2145.
2. One hump at 0.738 ± 0.005: **hit**. s.d. ratio 63/48 in 1.10–1.19: **hit** (1.166).
3. Profile within 0.01: **hit**. Under-fill generic to any over-full generation within 0.015: **miss** (two thirds
   of it is specific to deaths).
4. Lifetimes within 2 s.e. of the anchors: **hit** (+0.6, +0.7, −1.8).
