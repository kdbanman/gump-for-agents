# ref-boom: referee's review of `research/blast/boom` (2026-11-18, 04:45–05:20 UTC)

Referee: agent `ref-boom`. Boom's README was read for its definitions; its code was neither read nor run.
Labels: **[proved]**, **[measured]**, **[conjectured]**. Every number below is mine unless it says "boom".
All numbers: `sh run.sh; sh run2.sh; sh run3.sh; python3 pool.py p63 r63 r63b; python3 pool.py p75 r75 r75b;
python3 an.py r48 r57 p63 p75` → `out_all.txt`; islands `python3 ani.py i48 i63` → `out_islands.txt`.

## Verdicts

| claim | verdict | my number |
|---|---|---|
| 1. one hump of launches at 0.738·A | **CONFIRMED** | mean launch 0.7380 ± 0.0002 (48 cells), 0.7386 ± 0.0005 (57), 0.7375 ± 0.0004 (63), 0.7381 ± 0.0017 (75); one local maximum at 48, 57, 63; 97.8%, 97.8%, 98.5%, 98.1% above 0.60·A |
| 1b. "s.d. about 0.06·A, the same at 48…84" | **CORRECTED** | 3.07, 3.39, 3.58, 4.07 ± 0.09 cells = 0.0639, 0.0595, 0.0569, 0.0543 of A. The width grows like A^(0.58 ± 0.03), close to √A (0.443, 0.449, 0.451, 0.470 of √A), not like A |
| 2a. the sum rule 1/τ = Σ ν·d | **an identity** [proved], not a finding | Σ_p (launches at p)/(exposure) = deaths/exposure, for any definition of "launch" |
| 2b. I_up(0.74) = 0.078, J(0.74) = 0.132 ± 0.003 | **CONFIRMED** as numbers | I_up = 0.079–0.080, J = 0.136–0.137 ± 0.001 (48, 57, 63 cells); with 75 cells added 0.078–0.079 and 0.137 |
| 2c. min_θ [I_up + J] = 0.2099, "against the measured price 0.2087" | **REFUTED as evidence** (bookkeeping plus noise) | by the identity the minimum is the lifetime's own slope over the sizes used. Mine at θ = 0.74: 0.2154 ± 0.0011 (48, 63) where my lifetimes have slope 0.2156 ± 0.0005; 0.2146 ± 0.0011 (48, 63, 75) where they have 0.2136 |
| 3. the launch is a breath of the top four layers, in one step from a normal face, with layers 2–4 under-full one generation before | **CONFIRMED** (63 cells, 19,236 deaths) | launch 0.738 / 0.637 / 0.562 / 0.504; one before 0.524 / 0.400 / 0.354 / 0.376 (living 0.517 / 0.435 / 0.406 / 0.416); one after 0.222 / 0.152 / 0.190 / 0.301. A fifth to a third of the under-fill is generic to any over-full generation; the rest is specific to deaths |
| 4. the kill is a fragmentation; fail(size) = 0.90, 0.64, 0.28, 0.08; 7 or more cells regrow 99.4% | **CONFIRMED** (the island table only) | 63 cells: 0.900 ± 0.001, 0.634 ± 0.004, 0.276 ± 0.005, 0.078 ± 0.003 (sizes 1, 2, 3, 4–6); 0.0051 ± 0.0007 (7–12); 0 of 33,214 (> 12). 48 cells: 0.899, 0.631, 0.282, 0.085, 0.0052, 1 of 29,167 |

## 1. Stepper, validation, lifetimes

`rb.c`: my own stepper for the 8-layer slab with period lattice (H,K),(0,D) (hexagonal basis e1 = (2,−2,0),
e2 = (2,0,−2) in doubled coordinates), written from `docs/AUTOMATON.md` and `reference/oracle.py`; 64 replicas,
bit-sliced. `val.py`: the trajectory S_0…S_g of one replica is checked one generation at a time: S_t is tiled into
an oracle array of side 44 (dead outside the slab), the ORACLE steps once, every cell with all coordinates in
[2, 41] is compared with S_{t+1}; every class of cell is compared at every step (asserted), the class map is constant
on the period lattice and has 3HD values per layer (asserted), the shortest loops² are printed.
[measured] `python3 val.py 4 0 4 1000` (loops² 16,16,16), `python3 val.py 1 4 21 1200` (21,21,21),
`python3 val.py 1 7 19 1000` (19,19,19), `python3 val.py 1 9 25 1000`: 0 mismatching generations each; with `neg`
appended (one neighbour of one cell swapped) each fails (152 mismatching generations of 1,000 at 48 cells).

Protocol: a replica starts from a 40% soup and is counted after 300 generations; a face dies when its layer is
empty; the replica is then restarted. Exposure = face-generations with the face alive; ln τ = ln(exposure/deaths),
error 1/√deaths. A replica whose state repeats after 840 generations is restarted (91, 3, 1, 0 times).

| vessel | cells | face-generations | deaths | ln τ | anchor | |
|---|---:|---:|---:|---|---|---|
| (4,0),(0,4) | 48 | 2.5e9 | 122,130 | 9.9267 ± 0.0029 | 9.9251 ± 0.0004 | +0.6 s.e. |
| (1,7),(0,19) | 57 | 2.0e9 | 13,842 | 11.8810 ± 0.0085 | 11.8751 ± 0.0004 | +0.7 |
| (1,4),(0,21) | 63 | 1.0e10 (two seeds) | 19,237 | 13.1613 ± 0.0072 | 13.1622 ± 0.0007 | −0.1 |
| (1,9),(0,25) | 75 | 7.0e9 (two seeds) | 1,071 | 15.693 ± 0.031 | 15.6442 ± 0.0030 | +1.6 |

[measured] The anchors are reproduced. One oddity, not resolved: the two seeds of one vessel disagree more than
Poisson counting allows, both times: 63 cells 13.1441 ± 0.0101 and 13.1787 ± 0.0103 (9,785 and 9,452 deaths in equal
exposure: 2.4 s.d.), 75 cells 15.761 ± 0.045 and 15.629 ± 0.042 (500 and 571: 2.2 s.d.); together p ≈ 0.005.
It is not a failure of memorylessness at 48 cells [measured, `./rbt run 4 0 4 121 1500 …/t48.txt; python3 life.py t48`]:
the 73,162 slab lives of a third 48-cell run (ln τ = 9.9281 ± 0.0037) have CV² = 0.988 ± 0.011 and follow the
exponential law in every octave from 1 to 65,536 generations (no excess of early deaths after the 300-generation
start). LIFE63

## 2. (a) The launch distribution [measured]

Launch = last generation with P ≥ ceil(A/2) before the face is empty.

| cells | deaths | mean θ | s.d. (cells) | s.d./A | s.d./√A | skew | above 0.60·A | launch → empty, median (10–90%) |
|---|---:|---|---|---|---|---|---|---|
| 48 | 122,130 | 0.7380 ± 0.0002 | 3.068 ± 0.006 | 0.0639 | 0.443 | −0.43 | 0.978 | 5 (3–10) |
| 57 | 13,842 | 0.7386 ± 0.0005 | 3.391 ± 0.020 | 0.0595 | 0.449 | −0.43 | 0.978 | 5 (3–10) |
| 63 | 19,237 | 0.7375 ± 0.0004 | 3.582 ± 0.018 | 0.0569 | 0.451 | −0.46 | 0.985 | 5 (3–10) |
| 75 | 1,071 | 0.7381 ± 0.0017 | 4.071 ± 0.088 | 0.0543 | 0.470 | −0.52 | 0.981 | 6 (4–11) |

One hump: the histogram has a single local maximum at 48, 57 and 63 cells (48 cells, p = 24…46: 307, 284, 411, 618,
1042, 1848, 2880, 4682, 7397, 10222, 13546, 15909, 16873, 15407, 12546, 8649, 5160, 2686, 1118, 411, 115, 18, 1; the
307 at p = 24 is the pile-up at the cut A/2; at 75 cells 1,071 deaths do not resolve the shape). Its place is
0.738·A at every size. Its width is NOT a fixed fraction of A: s.d. ∝ A^γ with γ = 0.58 ± 0.03 (weighted fit of the
four sizes; 0.57 ± 0.03 from 48 → 63, 0.73 ± 0.13 from 63 → 75; boom's own 0.064 at 48 and 0.056 at 63 say the same,
and its 75 and 84 have 242 and 43 deaths). My first 75-cell run alone (500 deaths) gave 0.0568·A, the second
0.0519·A: at that size a run of a few hundred deaths cannot tell A from √A.
"Over-full" needs a scale: the living face has s.d. 0.093·A (48 cells) and 0.078·A (63), so the launch is at +2.4 and
+2.8 s.d., and the 2% of launches below 0.60·A are within about one s.d. of an ordinary generation.

## 3. (b) ν, d, the sum rule and the two-term price

**Numbers** [measured]. ν(p) = (face-generations at p)/exposure, d(p) = (launches at p)/(face-generations at p).
63 cells, d(p)·10⁴ at p = 44…53: 0.34, 0.77, 1.63, 3.77, 7.71, 15.2, 30.3, 60.9, 110, 208 (boom at 47…53: 4.0, 7.7,
16, 30.2, 56, 124, 170: agreed). "Each extra cell is half as frequent and twice as deadly": ν(p+1)/ν(p) = 0.49 and
d(p+1)/d(p) = 2.2–2.3 at the hump, at all four sizes. CONFIRMED.

**The sum rule is an identity** [proved]. Write n(p) for the face-generations at p, ℓ(p) for the launches at p, E for
the exposure, M for the deaths. Then ν·d = ℓ/E, and Σ_p ℓ(p) = M because each death has exactly one launch. This
holds for any definition of "launch" and any dynamics. (Boom's check "by cloning" is a fair test of the cloning
estimator of d; it is not a test of the rule.)

**What the identity does to the two-term price** [proved]. With w_A(p) = ℓ(p)/M the launch histogram,
ν(p)·d(p) = w_A(p)/τ exactly, so at p = θA, for any sizes and any common way of taking the slope in A,

    I_up(θ) + J(θ)  =  [slope of ln τ over the sizes used]  −  d/dA ln( √A · w_A(θA) ).            (*)

I_up + J contains nothing that is not in the lifetimes and in the launch histogram. For a hump of s.d. σ_A ∝ A^γ
cells the second term at the hump's top is (γ − ½)·d ln A/dA, so

    min_θ [I_up + J]  =  c_τ(sizes used) + (γ − ½)/A ,    and I_up + J − min is how fast the hump narrows in θ.

The minimum sits where the launches are by construction, and its value is the lifetime's own slope for the sizes
used, to within (γ − ½)/A ≈ 0.001. Checked numerically: the two sides of (*) agree to four decimals at every θ for
every pair of sizes (`out_all.txt`, "identity check"; with three sizes they agree only if ln ν and ln d are fitted
with the same weights).

**My values** [measured] (errors: Poisson resampling of the launch counts, 200 times):

| sizes | lifetime slope, my runs (anchors) | I_up + J at θ = 0.74, linear interpolation in p | quadratics in p | nearest integer p |
|---|---|---|---|---|
| 48, 63 | 0.2156 ± 0.0005 (0.2158) | 0.2154 ± 0.0011 (I_up 0.079, J 0.136); grid minimum 0.2139 at 0.745 | 0.2168 ± 0.0006 | 0.2143; grid minimum 0.2084 at θ = 0.675 |
| 48, 57, 63 | 0.2158 (0.2159) | 0.2154 ± 0.0011; grid minimum 0.2146 at 0.745 | 0.2171 ± 0.0006 (I_up 0.080, J 0.137) | 0.2202; grid minimum 0.2049 at θ = 0.695 |
| 48, 63, 75 (boom's sizes for d) | 0.2136 (0.2120) | 0.2146 ± 0.0011 (I_up 0.078, J 0.137); grid minimum 0.2133 at 0.745 | 0.2158 ± 0.0006 | 0.2181; grid minimum 0.1969 at θ = 0.695 |
| 63, 75 | 0.2110 ± 0.0026 (0.2068) | 0.2225 ± 0.0062; grid minimum 0.2033 at 0.775 | 0.2156 ± 0.0035 | 0.2250; grid minimum 0.1951 at θ = 0.690 |

By pairs of neighbouring sizes at θ = 0.74 (linear): I_up = 0.0792, 0.0797, 0.0760 and J = 0.136 ± 0.002,
0.136 ± 0.004, 0.147 ± 0.006 for 48→57, 57→63, 63→75 (lifetime slopes 0.2171, 0.2134, 0.2110 ± 0.0026).

- **Interpolation.** θA is 35.52 and 46.62 at θ = 0.74. Linear interpolation of ln ν and ln d between the two
  integers, and quadratics in p fitted over 0.62–0.88·A, agree to 0.001 on I_up and on J and to 0.001–0.002 on the
  sum. Rounding p to the nearest integer does not work at these sizes: ln ν changes by 0.7 and ln d by 0.8 per cell,
  a rounding of up to half a cell at each size is divided by ΔA = 15, and I_up at θ = 0.72 comes out 0.031 instead
  of 0.065, J 0.195 instead of 0.153; the sum then wanders between 0.197 and 0.259 and its "minimum over θ" is the
  luckiest rounding (0.2084, 0.2049, 0.1969 above). Boom's I_up row is smooth, so boom did not round ν; I cannot tell
  from the README what was done to d.
- **The honest error of "0.2099".** (i) Boom's own ± 0.003–0.004 on J at each θ (242 deaths at 75 cells). (ii) It is
  the smallest of seven noisy values (its neighbours are 0.217 and 0.212): a parabola through boom's seven sums
  bottoms at 0.2111 at θ = 0.744 with residuals of 0.0016. Taking the minimum of a noisy curve is biased low: with
  1,071 deaths at 75 cells my 63 → 75 curve has its grid minimum at 0.2033 while its value at 0.74 is 0.2225 ± 0.0062
  and its lifetime slope is 0.2110. (iii) Interpolation ± 0.002. (iv) By (*) the true value for boom's sizes is their
  lifetime slope: 0.2120 (anchors, line through 48, 63, 75) to 0.2158 (48 → 63). Boom's own lifetimes (9.9182,
  13.148, 15.663, 17.39 ± 0.15) have an unweighted slope of 0.2129 over 48–75 and 0.2083 over 48–84, the latter low
  because its 84-cell run (43 deaths) came out 0.15 low. **"0.2099" is 0.212 ± 0.004, and it is boom's own lifetime
  slope read back through the launch histogram.** Its agreement with 0.2087 to 0.001 is an accident of that error.
- **Was the agreement forced?** Agreement with the lifetime slope OF THE SAME RUNS is forced [proved], and is what I
  find (0.2154 against 0.2156; 0.2146 against 0.2136). Agreement with 0.2087, the slope of larger faces, is not
  forced, and done cleanly it is not there: the computation on 48–63 cells gives 0.2154 ± 0.0011, because the
  lifetime curve is steeper there than the wide-face line (the 48-cell torus has loops² of 16).
- **Laplace, or a term that grows with A?** [measured] If ν and d each had a large-deviation law at fixed θ, the
  hump would be √A cells wide (γ = ½), boom's √A in front of ν would be the right normalisation, the minimum over θ
  would be the right asymptotic statement, and the sum over θ would add a constant to ln τ. If the hump kept its
  shape in θ (γ = 1, what claim 1 says in words), I_up + J would be flat in θ, there would be no minimum, and the
  sum over θ would add −½·ln A to ln τ. Measured: γ = 0.58 ± 0.03. So Laplace is nearly right at 48–75 cells: the
  sum over θ contributes about 0.08·ln A, a change of slope of 0.001 per cell, nothing that matters. The curvature
  agrees roughly: I_up + J rises by 0.010 at θ = 0.68 and 0.012 at 0.80 above its minimum (boom: 0.019, 0.016),
  which gives a Laplace width of 0.05·A at 63 cells against the measured 0.057·A. Not excluded: γ creeping up with
  size (0.73 ± 0.13 from 63 to 75).
- **What is prediction and what is bookkeeping.** Bookkeeping: the sum rule; that the minimum of I_up + J is at the
  launch hump; that its value is the price of the sizes used. Measurement with content: the launch is at
  θ* = 0.738 at every size (a number a theory must produce); the cost at θ* splits into I_up = 0.079 (how rare an
  over-full face is: a property of the living state, measurable without a single death, the same to 0.001 from
  48 → 57 and 57 → 63 cells and 0.076 from 63 → 75) and J = 0.136 (how rarely such a face is the last full one);
  across the hump (θ* ± one s.d.) the split runs from 0.04 + 0.19 to 0.13 + 0.09. Prediction: none. Nothing here
  gives the price of a size that has not been run to its deaths, because J is measured from the deaths.

## 4. (c) The layer profile [measured; 63 cells, 19,236 deaths; shares of A; layers counted from the dying face]

| generation | face | layer 2 | layer 3 | layer 4 | boom |
|---|---|---|---|---|---|
| living state | 0.517 | 0.435 | 0.406 | 0.416 | 0.517 / 0.435 / 0.406 / 0.416 |
| launch − 2 | 0.494 | 0.421 | 0.399 | 0.408 | 0.496 / 0.419 / 0.399 / 0.407 |
| launch − 1 | 0.524 | **0.400** | **0.354** | **0.376** | 0.525 / 0.399 / 0.355 / 0.377 |
| launch | 0.738 | 0.637 | 0.562 | 0.504 | 0.732 / 0.637 / 0.562 / 0.507 |
| launch + 1 | 0.222 | 0.152 | 0.190 | 0.301 | 0.230 / 0.154 / 0.191 / 0.297 |
| launch + 2 | 0.119 | 0.154 | 0.242 | 0.350 | 0.127 / 0.158 / 0.242 / 0.347 |

48 cells (122,079 deaths): 0.495/0.421/0.397/0.406, 0.524/0.399/0.354/0.376, 0.738/0.637/0.561/0.504,
0.222/0.152/0.189/0.299, 0.120/0.154/0.241/0.348. CONFIRMED to 0.005 beneath the face; boom's face is 0.006–0.009
off mine at and after the launch (0.732, 0.230, 0.127 against 0.738, 0.222, 0.119; its 0.732 is also under its own
mean launch of 0.7375, so its profile runs select the deaths a little differently).

The control boom did not make: ALL generations with the same face population as a launch (weighted by the launch
histogram; a sample of 1 in 8), one generation before, at, and after:

| | face | layer 2 | layer 3 | layer 4 |
|---|---|---|---|---|
| before a death's launch | 0.525 | 0.400 | 0.354 | 0.376 |
| before any generation with that p | 0.524 | 0.428 | 0.389 | 0.406 |
| at a death's launch | 0.741 | 0.638 | 0.562 | 0.504 |
| at any generation with that p | 0.741 | 0.487 | 0.428 | 0.419 |
| after a death's launch | 0.220 | 0.151 | 0.190 | 0.302 |
| after any generation with that p | 0.363 | 0.375 | 0.374 | 0.411 |

(i) The precursor is real: with the face normal (0.524), layers 2–4 are 0.035, 0.052, 0.040 of A under the living
state one generation before a fatal launch; 0.007, 0.017, 0.010 of that is what any over-full face has behind it,
and 0.028, 0.035, 0.030 is specific to the deaths. In units of a layer's own fluctuation (about 0.08·A) it is
0.4–0.6 s.d. per layer: a tilt of the odds, not a warning sign. (ii) What separates a fatal launch from an ordinary
over-full face is the layers beneath AT the launch: an ordinary face of 0.74·A has 0.487/0.428/0.419 beneath it
(nearly normal), a fatal one 0.638/0.562/0.504. An over-full face alone is cheap (I_up); the deep over-fill is where
J is paid. (iii) An ordinary over-full face falls to 0.36·A in the next generation, a fatal one to 0.22·A.

## 5. (d) Islands [measured] (`./rbi island 4 0 4 301 300 …/i48.txt; ./rbi island 1 4 21 302 600 …/i63.txt`)

My procedure, from boom's description: take the state one generation after a face of q ≥ 0.62·A cells; group the
live face cells into clusters through in-layer neighbours; run the state once per cluster with every other cell of
that face killed and everything beneath untouched; "fails" = the face is empty before it is half full again.
15,000 parents in each of three bands of q (0.62–0.70, 0.70–0.78, ≥ 0.78 of A); none undecided after 400 generations.

| cluster size | 1 | 2 | 3 | 4–6 | 7–12 | > 12 |
|---|---|---|---|---|---|---|
| fails, 63 cells | 0.900 ± 0.001 | 0.634 ± 0.004 | 0.276 ± 0.005 | 0.078 ± 0.003 | 0.0051 ± 0.0007 | 0 of 33,214 |
| fails, 48 cells | 0.899 ± 0.001 | 0.631 ± 0.004 | 0.282 ± 0.006 | 0.085 ± 0.003 | 0.0052 ± 0.0007 | 1 of 29,167 |
| boom | 0.90 | 0.64 | 0.28 | 0.08 | 0.006 | 0.000 |

The same in the three bands of q to 0.03. Clusters of 7 or more regrow 99.89% of the time as they occur (99.5% for
7–12 cells; the largest that failed had 11 cells at 63 and 14 at 48). CONFIRMED. Not tested: the rest of claim 4
(the products of failure chances and their cancelling errors, the survivors of the fatal busts).

## 6. (e) Other things in boom's README

- Sentence 1, "every death … is launched from an over-full generation": true by definition for P ≥ A/2; the content
  is the hump (§2). "The same at 48, 63, 75, 84" is right for the mean and wrong for the width.
- Sentence 2 presents the sum rule as measured and the minimum as agreeing with the anchors: see §3. Boom's §3
  already prints the fair comparison (the anchors' 0.2115 for 48–84 cells) beside 0.2087.
- "J(θ) ≈ 0.5·(1 − θ)": mine is 0.136, 0.121, 0.107, 0.092, 0.077 at θ = 0.74…0.82 against 0.130, 0.120, 0.110,
  0.100, 0.090: fair from 0.74 to 0.78, 17% high at 0.82.
- §5 (maps), §6 (tubes), §7, §8 (hulls): NOT TESTED.

## 7. What the owner may be told about "a formula for the price"

There is no formula yet, and boom's 0.2099 is not one. What boom found, and my own code confirms, is the route: a
wrapped face dies when, in one generation and from an ordinary state, its top four layers fill together (the face to
0.738 of its area, at every size from 48 to 75 cells), crash together in the next generation, and leave only
fragments of fewer than seven cells, which cannot regrow the face. The death rate can be written exactly as (how
often the face is that full) × (how often such a face is the last full one), and at the launch point the first
factor costs 0.079 per cell and the second 0.136. But that product is arithmetic: both numbers were measured from
the same runs whose lifetimes they are meant to explain, and their sum must return those runs' own price (0.2154
for 48–63 cells in my runs, where the lifetimes have slope 0.2156), whatever the mechanism. Boom's 0.2099 landing on
the wide faces' 0.2087 is noise of ± 0.004 around 0.212. A formula would have to produce three numbers from the
rule: the launch point 0.738; the cost 0.079 of an over-full face (a property of the living chaos alone, so the
easier one, and already steady from 48 to 63 cells); and the cost 0.136 of the layers beneath filling with the face
and the crash leaving only fragments. The split is the useful result: nearly two thirds of the price is paid below
the face and in the kill, not in the face's own fluctuation.

## 8. Not checked

- 84 cells and above; tubes; hulls; boom's §5–§8; the cloning estimate of d (I used natural deaths only).
- Why two seeds of one vessel differ by 2.2–2.4 Poisson s.d. twice (see §1).
- Periods that do not divide 840 are not caught by the restart check.
- Builds: r48, r63, r57, r75, r63b, r75b were run with the first build `rb`; the island mode and the lifetime
  accumulators were added to `rb.c` afterwards and built as `rbi`, `rbt`; `rbi run` and `rbt run` reproduce
  `rb run` byte for byte on a 2e7 test (`cmp`), and the final source was validated again (`val.py`, four vessels).
- No second reader for `an.py`, `ani.py`, `pool.py`.

## 9. Forecasts (PREDICTIONS.md, commit 782d9f5, before any run)

1. min I_up + J from 48, 63 cells, linear interpolation, in 0.216–0.226: **miss by 0.001** (0.2154 ± 0.0011 at 0.74,
   grid minimum 0.2139; the quadratic version, 0.2168, is inside). The reason given held: it returns the lifetime
   slope of the sizes used (0.2156), not 0.210.
2. One hump at 0.738 ± 0.005: **hit**. s.d. ratio 63/48 in 1.10–1.19: **hit** (1.168).
3. Profile within 0.01: **hit**. Under-fill before the launch generic to any over-full generation, within 0.015:
   **miss** (two thirds or more of it is specific to deaths).
4. Lifetimes within 2 s.e. of the anchors: **hit** (+0.6, −0.1; single runs at 63 cells −1.8 and +1.6).
