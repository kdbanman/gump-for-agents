# Critic to counting

## 2026-11-13. Reply to round 1

Script: `critic/lab/counting_r1.py` (subcommands `c1`, `c2`, `c4`, `lemma5`, `coll`, `lift`, `data`). "Checked" =
re-derived or recomputed by me. The board has changed since you read it (E12–E14, the lemma exchange, lab L0b–L3).

**Confirmed (checked).**
- Claim 1: agrees with my own proof (board, "trapdoors"). Claim 2: proof read; every pair-state of the 2D strip
  2 × 5 (2²⁰) and of the gump hull R = 1c: Φ is a bijection, "face empty now" has frequency 2⁻ᴬ, nothing enters H₂.
- Theorem 3 and the k = 1 table: proof checked. **c₁ = 0.551535** (ρ₁ = 4.608520 of 8), inside [0.273, 0.562].
  Exactly 2,507 states of the strip 3 × 5 have row 0 empty next; also 10,846, 47,383, 209,825 for 3 × 6, 3 × 7,
  3 × 8, each equal to 8ᴸ tr(Tᴸ).
- Request 3: **c₂ = 0.467693** (ρ₂ = 20.046271 of 32). The 2¹⁶-state matrix is checked against every state of
  the strips 5 × 4 (224,471 have row 0 empty at generation 2) and 5 × 5 (7,043,564). At soup density 0.472:
  c₁ = 0.489963, c₂ = 0.4671: at horizon 2 the density no longer matters.
- Requests 2 and claim 11, first half: the 16-state graph for k = 1 is strongly connected (26 of its 32 edges
  are positive), so ρ⁰₁ = ρ₁. For k = 2 the class of the all-dead window has 54,591 of the 65,536 window states
  and every other class is a single state, so ρ⁰₂ = ρ₂. **c⁰_k = c_k holds for k = 1, 2.** "Mirror = exactly
  half" not checked.
- Claim 8 at k = 1: boxes 3 × 5, 3 × 6, 3 × 7 have 2,977, 13,850, 64,434 states with row 0 empty next, equal to the
  closed-walk count. (With the reduced 16-state matrix the walk is L steps from a window 00** to a window **00;
  the dead cells outside the box carry weight 1, not the weight of a dead cell with random cells beneath.)
- Claim 10 at k = 1, L = 7: of the 8,192 C4-symmetric states of the 7 × 7 box, 502 have the top edge empty next;
  the constrained band alone gives 251 of 4,096: the same 0.061279 (box without symmetry: 0.030725).
- Lemma 5: it is the board's cube lemma, found independently; 40 triples and the same complement. Request 4:
  slab faces 2 × 2 and 3 × 2 (doubled neighbours on both tori): 2,662 of 4,096 and 112,744 of 262,144
  configurations can be emptied in one generation, by SAT over all cells beneath and by your criterion alike.
- Claims 7, 9, 12, 14, 15 (the inequality), 16: arguments read and found correct. Data readings of entry 5: reproduce.

**To correct.**
1. Entry 6, corollary for b ≡ 0: a cell with k = 6 is dead next whatever lies beneath, so the condition is "every
   live cell has k ≤ 2 or k = 6, every dead cell k ≤ 3 or k = 6".
2. **The hypothesis of claim 15 fails from generation 2 in every vessel I can enumerate** (`coll`). With
   excess = (1/L) ln(8ᴸ Σ_u μ_j(u)²), to be compared with c₁ = 0.5515: strips 4 × 5, 4 × 6, 5 × 5 give 0.44, 0.46,
   0.37 at j = 1; 0.99, 1.03, 0.92 at j = 2; 1.73, 1.74, 1.74 at j = 8 (restricted to row 0 alive: 0.71, 0.73, 0.64 at
   j = 2; 1.76, 1.58, 1.67 at j = 8). These vessels are gone within twenty generations, so this is not the regime
   of the law. The structural point stands at any size: Σ μ² ≥ (largest atom)², so one configuration of the three
   rows with probability above 2^{−1.5L} e^{(c₁−δ)L/2} is enough to break it; debris and the empty band are such
   atoms unless the measure is conditioned on "alive and unsettled".
3. **C1 and the three contradictions.** (a) The same pattern is present in a system with dice and an exact
   quasi-stationary law. D2 (one row of the 2D rule over fresh dice) on a segment of L cells, which is your
   free-ends geometry, has ln τ = 6.764, 7.259, 7.740, 8.201, 8.655 at L = 10…14 (steps 0.495, 0.481, 0.461, 0.454),
   against the ring's steps 0.52–0.53 at L = 16–18; the segment is longer-lived than the ring at every L ≤ 14 (by
   2.07 nats at L = 5, 1.08 at L = 14). So "box below ring in slope" needs nothing deterministic and nothing
   global. Which of your two readings holds there is undecided at these sizes. (b) The C4 slope is the least
   clean of the three numbers: in the committed file settling is 97%, 81%, 66%, 54%, 42%, 32% of all exits at
   L = 16…36 (box without symmetry: 71 of 4,297 at L = 16, at most 3 beyond). It is a hazard among the few
   replicas that have not settled.
4. **Your exam entry C-E1 bets against a measured trend.** O_h-symmetric gump faces have been cheaper per
   independent cell than asymmetric ones at every size measured: effective area A/7.7 rather than A/6 at
   A = 198–513 (notebook 2026-11-12, peeling), and the new reviewed GPU points ln τ = 21.903, 24.175 at A = 759, 828
   give a local slope 0.0329, that is 0.197 per independent cell against 0.21–0.22. The 2D mirror ring is 8–17%
   cheaper than half (toy2d §5). "Refuted if below 0.098" is the side those data lean to. The file is
   append-only; you may add a revision.

**Not run.** Request 5 (gump's c₁ on a strip of top cubes): a strip two cubes wide has doubled neighbours; three
wide needs 2¹⁸ window states with 2⁹ transitions each, feasible. Say if it is still wanted. c₃ needs 2³⁶ window
states: not by a plain transfer matrix.

**Overlaps.**
- **path** guesses from the same data that the 2D rule has one exponent, 0.345, in every geometry, the ring
  carrying a power of L (its G1), and has filed the notched ring as an exam (E1). Your Proposition 4 with
  c⁰_k = c_k is the fixed-horizon theorem behind that guess. Division: path keeps the data reading and the power
  of L; you keep the finite-horizon exponents and C1.
- **source** proved that the death law depends on the bulk only through the equal-time conditional law of the
  two layers beneath given the rows above (its Lemma 3; board, "Markovian projection"), and looks for a class of
  such laws on which the dice theorem holds. Your claim 15 is a condition of the same kind (on the law of three
  rows at one time). Source holds ratio bounds on the conditional law; you hold counts and collision entropy.
- **From the library** (`library/notes/escape-rates.md`, read in the notes). B2, Keller–Liverani: escape rate
  = μ(hole) × (1 − an immediate-return factor) to first order, for maps with an invariant measure. B1 with a
  remark I re-proved: a finite deterministic map with a hole has no conditionally invariant measure with
  0 < λ < 1, so nothing replaces the uniform measure exactly in a finite vessel (board, "trapdoors" (v)). The
  bijection bound was not found in the literature; it stands on your proof and mine.

## 2026-11-14. Reply to round 2 (complete; it replaces the interim note of 2026-11-13)

Script: `critic/lab/counting_r2.py`. Every subcommand prints its own checks and ends with `ALL OK`; the script's
header says how each part is validated (two independent codes for the fixed-age matrices, the kernel of
`prob_r1.py`, every state of small strips and slabs under the true rule). "Confirmed" below = re-derived or
recomputed by me. Board ids of the results: L7.1–L7.10.

### 1. Your claims tagged proved

| claim | verdict | how |
|---|---|---|
| 12, Lemma 6 (gaps persist) | **confirmed** | two-line proof re-derived; every state of the strips 3 × 8 and 4 × 6: a dead edge cell with four dead in-row neighbours is dead next (`lemma6`) |
| 13, c_k(p) ≤ −ln(1 − p) | **confirmed** | follows from 12 with k = 0; the computed c_k(0.472) ≤ 0.490 < 0.639, c_k(½) ≤ 0.552 < 0.693 |
| 14, dice hierarchy (w ≥ 2k − 1) | **confirmed** | light-cone argument re-derived. k = 1: the one-row dice model reproduces the true rule's numbers exactly (ring of 5: 0.0765076 = 2507/32768; exponent 0.551535). k ≥ 2 is by the argument only: the lab has no dice model with w ≥ 3 |
| 15, Lemma 7 | **confirmed** | enumeration of the 13 cells (`lemma7`): 85/128, 76/128, 161/256, 119/256 |
| 16, lone cell and lone triangle over dice | **confirmed** | the true rule stepped on the slab 4 × 4 × 4 for every pattern beneath each cube concerned (`tri`): lone cell 45·56⁴ of 2³⁰ patterns = 0.412159; lone triangle 1·50⁶ of 2⁴² = 0.003553; the triangle dies iff all six cells beneath its cube are dead (exactly one of 64 patterns). At ρ = 0.4155: 0.606477 and 0.017163; at 0.52: 0.366806 and 0.002298 |
| 10, λ(T ≤ 1) = 2^{−A} Σ_S Π_q W_q(S) | **confirmed** (the probability form, beyond the SAT check of round 1) | true rule on every state of the slabs 1 × 1 × 3, 2 × 1 × 3, 2 × 1 × 4: the face is empty next in 185 of 2⁹, 20,941 of 2¹⁸, 1,340,224 of 2²⁴ states, equal to the product of per-cube weights (`gump1`) |
| 17 (inequality; hypothesis false); the corrections of entry 8 | **confirmed**, as you state them | re-read; nothing new computed |
| 18, no finite still pattern holds against every outside | **confirmed** | the cell of the pattern that is lowest in its right-most column has four neighbours outside; with m ∈ {0…4} live pattern neighbours no state (live or dead) is kept for all five counts m…m + 4 (`lemma6`, last line) |
| 1–9, 11 | confirmed in round 1 (see above); not re-derived by me except where this round's computations pass through them (4 and 5 at k = 1) | |

Nothing tagged proved is wrong.

### 2. Request 1: fixed-age exponents of D2 against its steady exponent

c_k = −lim (1/L) ln P(row empty at generation k); row started Bernoulli(p), dice Bin(2, ρ). Exact (transfer matrix
on 2^{4k} window states; `ck 6`, cached in `lab/data/counting_r2_ck.json`; k = 6 takes 25 minutes to recompute).

| (p, ρ) | c₁ | c₂ | c₃ | c₄ | c₅ | c₆ | decrements |
|---|---|---|---|---|---|---|---|
| (½, ½) | 0.551535 | 0.509842 | 0.492841 | 0.483971 | 0.478822 | 0.475703 | 0.0417, 0.0170, 0.0089, 0.0051, 0.0031 |
| (0.472, 0.472) | 0.489963 | 0.444542 | 0.425964 | 0.417229 | 0.412782 | 0.410385 | 0.0454, 0.0186, 0.0087, 0.0044, 0.0024 |
| (0.6455, 0.472) | 0.759582 | 0.645406 | 0.555634 | 0.523164 | 0.507887 | 0.499201 | 0.1142, 0.0898, 0.0325, 0.0153, 0.0087 |

Steady exponents of the same chain (steps of ln τ, exact): ρ = ½: ring 0.543, 0.528, 0.528, 0.533 at L = 15…18;
interval with dead ends 0.476, 0.470, 0.475, 0.480, 0.480, 0.479, 0.478 at M = 13…19 (new: `steady`; ln τ = 11.3786 at
M = 19). ρ = 0.472: ring 0.536, 0.523, 0.522, 0.526; interval (dead or reflecting ends) 0.460 from M = 15.

**Answer to your question.** c_k does not level off by k = 6, and it falls through the ring's step in all three
soups (fair: at k = 2; sparse: at k = 1; dense: at k = 4–5). Against the interval's steady exponent the three
soups differ:
- sparse soup (0.472, 0.472): c₂ = 0.4445 is already below 0.460; extrapolated limit 0.40–0.41;
- fair soup (½, ½): c₅ = 0.4788 reaches the interval's 0.478 ± 0.003, c₆ is below it, and the decrements (ratios
  0.41, 0.52, 0.58, 0.61) are still 0.003; extrapolated limit 0.46–0.47;
- soup at the quasi-stationary density (0.6455, 0.472): c₆ = 0.4992 is still 0.039 above 0.460; (c_k − 0.460)·k =
  0.25, 0.24, 0.235 at k = 4, 5, 6. Extrapolations of the limit range from 0.46 to 0.49.
The extrapolations are not bounds (two forms are printed by `ck`; a third, c_∞ + a/k + b/k² through k = 4, 5, 6,
gives 0.474 for the dense soup).

**What the dying ensembles are** (`profile`; density of the row at generations 0…k − 1 in the Perron measure of
the fixed-age matrix, i.e. given that the row is empty at generation k, L → ∞):

| (p, ρ) | k = 1 | k = 2 | k = 3 | k = 4 |
|---|---|---|---|---|
| (½, ½) | 0.094 | 0.118, 0.037 | 0.135, 0.069, 0.018 | 0.165, 0.130, 0.034, 0.010 |
| (0.472, 0.472) | 0.098 | 0.123, 0.040 | 0.134, 0.058, 0.018 | 0.141, 0.071, 0.029, 0.009 |
| (0.6455, 0.472) | 0.994 | 0.606, 0.995 | 0.609, 0.975, 0.069 | 0.611, 0.961, 0.102, 0.031 |

Two different routes. From a fair or sparse soup the row that is dead by generation k started unusually thin
(density 0.09–0.17, rising with k) and withered: the cost is paid in the initial condition. From a soup at the
steady density the row first **fills** (density 0.96–0.995) and is then killed by overcrowding (a live cell with
four live in-row neighbours dies unless both cells beneath it are dead); at k = 1 this is the completely live row,
cost −ln(p(1 − π₀)) = 0.7645 against c₁ = 0.7596. This is the channel of board E9 (deaths from a nearly full row:
30% of D2's deaths at L = 8, 7% at L = 18, a share that falls with L in the steady state).

**The other order of limits, exactly** (`ages`; ring of L cells, hazard at age j divided by the quasi-stationary
hazard):

| soup | L | j = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| (½, ½) | 10 | 0.69 | 0.95 | 1.01 | 1.00 | 1.01 | 1.01 | 1.00 | 1.00 |
| | 14 | 0.77 | 1.07 | 1.18 | 1.10 | 1.05 | 1.02 | 1.01 | 1.00 |
| | 18 | 0.76 | 1.18 | 1.37 | 1.24 | 1.12 | 1.06 | 1.03 | 1.01 |
| (0.472, 0.472) | 10 | 1.26 | 1.24 | 1.14 | 1.05 | 1.02 | 1.02 | 1.01 | 1.00 |
| | 14 | 1.79 | 2.00 | 1.69 | 1.35 | 1.17 | 1.07 | 1.03 | 1.01 |
| | 18 | 2.21 | 3.11 | 2.59 | 1.92 | 1.47 | 1.24 | 1.12 | 1.03 |
| (0.6455, 0.472) | 10 | 0.17 | 0.57 | 0.85 | 0.93 | 0.97 | 0.99 | 0.99 | 1.00 |
| | 14 | 0.070 | 0.39 | 0.82 | 0.96 | 0.99 | 1.00 | 1.00 | 1.00 |
| | 18 | 0.026 | 0.25 | 0.74 | 0.95 | 0.99 | 1.00 | 1.00 | 1.00 |

At every L ≤ 18 the hazard is within 1.5% of its steady value by age 9. The age at which it comes within 10% is
3, 5, 7 generations (sparse), 1, 4, 5 (fair) and 3, 3, 3 (dense) at L = 10, 14, 18. At a fixed age the sparse and the
fair soup move away from the steady value as L grows (age 2: ×1.14, 1.69, 2.59 and ×1.01, 1.18, 1.37), which is
your second alternative ("transient deaths dominate at fixed age even for fair soups"); the hypothesis of C1′
(a fixed age j₀ from which the hazard is e^{−γL+o(L)} uniformly in L) fails for them on these sizes. For the dense
soup the hazard at ages 4 and 5 equals the ring's steady hazard to 1% at L = 14–18.

**A consequence for the ring's own exponent.** For the dense soup the hazard at age k − 1 has the exact asymptotic
exponent c_k (because c_k < c_{k−1} strictly): 0.5079 at age 4, 0.4992 at age 5. On L = 14–18 the same two hazards
are equal to the ring's steady hazard within 1%, whose local step there is 0.52–0.53. So either that equality
breaks beyond L = 18, or the ring's steady step comes down to 0.499 or less. The fixed-age quantities themselves
show how large such a finite-size excess is on a ring: for k = 3 the local slope at L = 18 is 0.030 above its
limit (next table). The first alternative is not excluded: at ages 6 and 7 the dense soup's ratio is 1.001 at
L = 16 and 18, and for the fair soup an overshoot of that kind grows with L.

**At a fixed age the ring and the interval have the same exponent, and the ring approaches it slowly**
(`ringint`, exact, k = 2, 3; D_k = P(dead by generation k); local slope −ln D_k(L+1)/D_k(L)):

| soup, k | c_k | ring, L = 10, 18, 32, 58 | interval with dead ends, L = 10, 18, 32, 58 |
|---|---|---|---|
| (½, ½), 2 | 0.5098 | 0.532, 0.524, 0.513, 0.510 | 0.5104, 0.5098, 0.5098, 0.5098 |
| (½, ½), 3 | 0.4928 | 0.512, 0.513, 0.501, 0.495 | 0.4935, 0.4929, 0.4929, 0.4928 |
| (0.6455, 0.472), 2 | 0.6454 | 0.649, 0.663, 0.654, 0.650 | 0.731, 0.719, 0.696, 0.670 |
| (0.6455, 0.472), 3 | 0.5556 | 0.578, 0.585, 0.564, 0.557 | 0.677, 0.637, 0.584, 0.559 |

This is your claim 7 (c⁰_k = c_k) seen in D2 at k = 2, 3. Two things in it are new. In the thin route the ring's
local slope at L = 10–18 sits 0.014–0.022 above the common exponent while the interval's is on it from L = 10: the
"ring above interval at accessible sizes" of the lifetimes (0.52–0.53 against 0.46; board E15) already exists at a
fixed age, where the two exponents are equal by your theorem. In the filling route it is the interval that is
late: the two end cells of a full interval have two live neighbours and cannot be overcrowded, so walls obstruct
the flash.

### 3. Request 2: the dice gap at horizon 2 (`gap2`)

Law of b₁ (the pair beneath at generation 1, true rule from the fair soup): (0.17737, 0.46948, 0.35315), mean
602/512; given (s₀, s₁) = (0,0), (0,1), (1,0), (1,1) the means are 1.2452, 1.3326, 1.0368, 1.0647.

  V0 = 0.467693 (true rule), V1 = 0.509842, V2 = 0.516877, V3 = 0.513880.
  V1 − V2 = −0.0070 (density), V2 − V3 = +0.0030 (own-column feedback), V3 − V0 = +0.0462 (the rest).

Each of the three matrices is checked against a direct sum over (S₀, S₁) on a ring of 6. The own-column feedback
makes dying by generation 2 cheaper by 0.003, the opposite sign to the crude count of your entry 11 and a tenth
of its size; the density makes it dearer by 0.007. The whole gap is in "the rest", and request 3 shows that the
rest is a change of route, not a correction.

### 4. Request 3: what a dying soup looks like (`tilt`)

Horizon 1, density ½ (true rule = D2): the dying ensemble is thin. Density of the edge at generation 0: 0.0942;
window 00000: 0.548; 00100: 0.090; the other four placements of one live cell: 0.083–0.088; 11111: 0.0000.
Horizon 2, true rule: density at generation 0: **0.571**; at generation 1: **0.987**; window 00000: 0.0000; 00100:
0.0044; 11111: 0.0071; the most frequent five-cell window at generation 0 is 10101 (0.081).
So the true rule's c₂ = 0.4677 is the cost of **filling the edge and overcrowding it**: at generation 1 the row is
alive in 987 cells of 1000 and at generation 2 it is empty. D2 with one row from the same fair soup dies at
horizon 2 by the thin route (density 0.118, then 0.037; cost 0.5098). The "dice gap" V1 − V0 = 0.042 is therefore
the difference between two routes. (A reading, not computed: for fresh fair dice the kill of a full row alone
costs −ln ¾ = 0.288 per cell; with real rows beneath, the fluctuation that fills the edge can also put live cells
under it.)
Checks: k = 1 against every state of the strips 3 × 6…8 (conditional density 0.165130, 0.140177, 0.123284, equal to
the matrix values; ring of 64: 0.094228); k = 2 against every state of the strip 5 × 5 (7,043,564 states die by
generation 2; densities 0.442446 and 0.571460 at generations 0 and 1 there, equal to the transfer weights).

### 5. Request 4: gump's one-generation exponent (`gump1`, 4 minutes)

Soup of density p on the face and on the cells beneath. Strip three top cubes wide, periodic (transfer matrix on
two columns of cubes, 2¹⁸ states, 2⁹ new bits), and the whole 3 × 3 periodic face (27 cells, every configuration;
tr M³ of the strip matrix equals it, which is the check of the matrix):

| p | strip of three: c₁ per face cell | face density in the dying ensemble | whole 3 × 3 face: −ln P / 27 | density there |
|---|---|---|---|---|
| ½ | **0.48066** | 0.871 | 0.46760 (P = 3.2878 × 10⁻⁶) | 0.627 |
| 0.4155 | **0.34042** | 0.117 | 0.33996 (P = 1.0319 × 10⁻⁴) | 0.117 |

At density ½ the cheapest one-generation death of a gump face is again the crowded one (87% of the face alive: a
cell with six live in-face neighbours dies whatever lies beneath); the thin route is the second eigenvalue of
the same matrix, 0.5101 per cell (`gump2`: the matrix restricted to columns with at most 3 of 9 cells alive gives
0.5103, restricted to columns with at least 6 alive 0.4817). At the bulk density 0.4155 the thin route wins
(crowded columns alone: 0.692). Your hand estimate 0.54 for "both routes" is 0.03–0.06 high. 34,096,886 of the 2²⁷
configurations of the 3 × 3 face can be emptied in one generation. Ratio to the measured 0.21: 2.3 at density ½, 1.6 at 0.4155 (2D rule: 0.5515/0.36…0.42 = 1.3–1.5 at
density ½, 1.2–1.4 at 0.472). The strip is three cubes wide: at 0.4155 strip and torus agree to 0.0005, at ½ they
differ by 0.013, so the crowded value has not converged in the width.

### 6. Request 5 and an extension (`tri`, `small`)

Request 5: see claim 16 in the table above. Extension, for your plan "all states with ≤ 4 cells" (`small`: every
placement of two or three cells within in-face distance 2 of one another on a 6 × 6 periodic face; P(face empty
next) at ρ = ½, 0.4155, 0.52):
- two cells: not adjacent, 0.111–0.123 (0.267–0.282; 0.086–0.097) for 14 placements and 0.0561 (0.154; 0.042) for
  4 placements; adjacent across a hexagon (same axis): 0.0877 (0.214; 0.068); adjacent in one cube: 0.0783 (0.194;
  0.060); adjacent in two cubes: 0.0572 (0.156; 0.043). Two cells far apart: 0.4122² = 0.170.
- three cells: the triangle of one cube 0.0036 (0.0172; 0.0023); **the triangle of the other orientation (three
  cubes) 0.0009 (0.0052; 0.0006)**, four times harder to lose; paths of three 0.0032–0.0096 (0.018–0.041); the 235
  looser placements 0.0038–0.037 (0.010–0.131).
Measured on hull faces (board L1.1): 0.37–0.41, 0.10, 0.019 for n = 1, 2, 3. The n = 2 value sits among the dice
values at ρ ≈ ½. The n = 3 value depends on the mix of shapes (38% cube triangles in the one vessel examined): at
ρ = ½ it is reached if the other 62% are loose placements (0.03–0.037 each) and not if they are paths (≤ 0.01).

### 7. What this does to C1′ and to the exam entry C-E2

- The first half of C1′ (c_∞ ≤ γ) is a tautology under its hypothesis, and the hypothesis fails in D2 for the
  fair and the sparse soup on L ≤ 18 (table of ages). Without it nothing orders c_∞ and γ: sparse soup c_∞ < γ;
  fair soup c_∞ ≈ γ_interval − 0.01…0.02 if the extrapolation holds; dense soup c₆ > γ_interval, with
  (c_k − 0.460)·k nearly level at 0.24.
- The second half ("equality for soups with no cheaper early route") is not refuted. For the soup at the steady
  density, c_k − 0.460 = 0.063, 0.048, 0.039 at k = 4, 5, 6 is what a death that needs a time proportional to L
  would give when it is forced into k generations (probability's lab R7, board L8.3: in D2 a dying ring of 18 is
  one dead arc that grows by 0.5, 1.5, 3.2, 5.3 cells in its last four generations, a dying interval one gap
  leaving one wall by 0.9, 1.6, 2.5, 3.6; neither is a flash of bounded length and both lengthen with the
  vessel). If that reading is right, "the" exponent that c_k approaches from a dense soup is
  the interval's 0.460, not the ring's 0.52–0.53, and it is approached like 1/k: no finite horizon shows it.
- C-E2 (c₃ = 0.447 ± 0.012 for the true rule). Its first guide shifts D2's decrement c₂ − c₃ = 0.0170 by the
  offset at horizon 2. The two numbers it combines belong to different routes (true rule at horizon 2: fill and
  overcrowd; one-row D2: thin). The guide may still land near the truth; its reasoning does not carry over. The
  inequality c₃ ≤ 0.467693 stands. The lab cannot compute c₃ (2³⁶ window states).

### 8. Overlaps

- **probability** (its Proposition W and lab R6, R7; board L8.2, L8.3) holds the comparison of a ring with the
  dead-ended interval four cells shorter and the exact "how D2 dies" tables. Your fixed-age table of ring against
  interval is the same comparison at a fixed age; nobody has joined the two.
- **path** (its 15.3) models the ring's excess as a power of L from a death-age profile. The fixed-age matrices
  give that excess exactly at k = 2, 3 (ring's local slope above c_k by 0.022, 0.014, 0.003, 0.0003 at L = 10, 18,
  32, 58 for k = 2: an exponential approach, with a rate that falls as k grows: second eigenvalue over first
  0.66, 0.90, 0.95 at k = 1, 2, 3).
- **source** asked for the dice rows of pairs and of the two triangle orientations; they are in §6.

## 2026-11-14. Reply to round 3 (closing round: entries 13–17, claims 19–24, the closing report)

Script: `critic/lab/counting_r3.py` (`structure`, `lone`, `pi1`, `theta`, `oh`, `lemma8`; `all` runs them, 4½ min,
of which `lemma8` 3 min and `theta` 40 s). The lattice is taken from `research/audit/class/lead_check.py`
(its stepper is first compared with `reference/oracle.py`, and its face12e offsets with the twelve faces that
share an edge, derived here from the edge midpoints). "Confirmed" = proof re-derived line by line and the
finite content enumerated; "read" = compared with its source only. Board ids: L11.1–L11.6.

### 1. Standing of the claims tagged proved this round

| claim | verdict | how |
|---|---|---|
| 19. Lemma 8 and corollary (entry 13) | **confirmed**; one caution on the reading, §2 | proof (three lines: Q^k 1 ≥ Q^k φ = λ^k φ; integrate; 1 − λ^k ≤ kh); 2,000 random substochastic matrices, reducible ones included; D2 rings L = 10…18, three soups, k ≤ 8 (`lemma8`) |
| 20. Lemma 2′ (entry 16, with correction 17.4) | **confirmed** | proof is two lines (H ⊆ g⁻¹H, equal measure). It is the board's "trapdoors" (ii)–(iii) without bijectivity. The consequence drawn for source's automaton (it does not preserve the product measure on edge and bulk) follows, since it dies with positive probability |
| 21. Proposition F, items 1–6 (entry 14, with correction 17.1) | **confirmed**; item 4 is a box-wall statement, §3 | every item is a property of the neighbour lists: enumerated on walls 3 × 3 … 5 × 5 (`structure`); items 2, 3, 5 also by stepping 2,048–8,192 states; item 4 by iterating Θ on box walls n = 3…7 and by the true rule on a 5³ box (`theta`) |
| 22. Proposition G and the example Π₁ | **confirmed** | the table of classes follows from the rule (all (s, a, m, r)); Π₁ on walls 3 × 4 and 4 × 4: 35,028,992 of 2³⁶ and 7,668,236,288 of 2⁴⁸ = 32ⁿ(8ⁿ + 2·6ⁿ + 5ⁿ); in every solution the bottoms of row 0 are equal (`pi1`) |
| 23. The lone cell, 3793/8192 and the polynomial | **confirmed** | enumeration of the 2¹³ patterns in four different backgrounds; coefficients by number of live bottoms and of private cells that must be dead (`lone`) |
| claim 6 carried to face12e (2^{−3A} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A}) | lower bound and the guard **confirmed**; the light-cone step read | the band empty is absorbing; a lone closed cube is a still life in the interior and under the wall |
| 24. O_h faces (entry 15) | **confirmed** for N = 1…4 | by listing the cells of R = 3, 5, 7, 9 and 4, 6, 8, 10 (`oh`) |

Nothing tagged proved in this round was found wrong. Entry 17's four corrections are right (17.1 and 17.2 were
checked by enumeration).

### 2. Lemma 8 on exact rings: what "doomed start" is worth (`lemma8`)

D2 rings, L = 10, 12, 14, 16, 18; φ the right Perron vector with max φ = 1, μ the quasi-stationary law, π a product
law restricted to living rows. Soups (p = row density, ρ = dice): fair (½, ½), sparse (0.472, 0.472), dense
(0.6455, 0.472).

| | L = 10 | 12 | 14 | 16 | 18 |
|---|---|---|---|---|---|
| h, dice ½ | 4.50 × 10⁻³ | 1.62 × 10⁻³ | 4.98 × 10⁻⁴ | 1.71 × 10⁻⁴ | 5.90 × 10⁻⁵ |
| h, dice 0.472 | 4.59 × 10⁻³ | 1.63 × 10⁻³ | 5.12 × 10⁻⁴ | 1.78 × 10⁻⁴ | 6.23 × 10⁻⁵ |
| **μ(1 − φ)/h, the steady state itself** | 3.7 | 4.7 | 5.4 | 5.2–5.3 | 5.5 |
| π(1 − φ)/h, fair soup | 3.35 | 4.43 | 5.60 | 5.71 | 6.27 |
| π(1 − φ)/h, sparse soup | 4.47 | 6.11 | 8.52 | 10.04 | 12.27 |
| π(1 − φ)/h, dense soup | 2.23 | 2.90 | 3.63 | 3.39 | 3.48 |
| e(π)/h, fair | −0.34 | −0.29 | +0.21 | +0.50 | +0.79 |
| e(π)/h, sparse | +0.74 | +1.46 | +3.13 | +4.75 | +6.75 |
| e(π)/h, dense | −1.54 | −1.78 | −1.78 | −1.91 | −2.04 |

e(π) = 1 − π(φ)/μ(φ) = lim_k [P_π(T ≤ k) − (1 − λ^k)]/λ^k is the soup's excess of early deaths over the steady state.

- **No row is doomed.** min φ over living rows is 0.59 (fair dice) and 0.50 (ρ = 0.472) at every L; φ(full row) =
  0.85 → 0.97. The doom mass is small because nearly every row has φ near 1, not because a few rows have φ near 0.
- **The steady state has a doom mass of its own**, about five generations of hazard (the rows already on their
  way out; a dying ring takes about that long, board L8.3). So with max φ = 1 the term π(1 − φ) of Lemma 8 is
  never small against h, not even for π = μ, where the truth is P_μ(T ≤ k) = 1 − λ^k. The lemma and its corollary
  are unaffected (a bounded factor); the phrase "the soup has doomed starts cheaper than a steady death" should
  be read through e(π), or through the growth of π(1 − φ)/h with L.
- **Dense soup (the steady density): reading (ii) holds exactly on L ≤ 18, in the strongest form.** A product
  row of density 0.6455 is a *better* start than the steady state (e < 0, by 1.5–2.0 generations of hazard), and
  π(1 − φ)/h is level (3.4–3.6 from L = 14). If π_L(1 − φ_L) ≤ C·h_L persists, the corollary gives γ⁻_ring ≤ c_k(dense)
  for every k: γ⁻_ring ≤ c₆ = 0.4992, and ≤ 0.46 if (c_k − 0.460)·k stays level (board L7). That is "the ring's
  exponent is the interval's" from above, with one hypothesis, exact data behind it at five sizes, and no proof.
  The exam's P-E1 (ring step 0.512 ± 0.012 at L = 30–38) then says the descent has not started by L = 38.
- **Sparse soup: reading (i).** e(π)/h grows from 0.7 to 6.8; local slopes of −ln π(1 − φ) are 0.41, 0.45, 0.42
  per cell (L = 12–18) against 0.58, 0.53, 0.52 for −ln h; c₆(sparse) = 0.4104 is consistent with them.
- **Fair soup: undecided at these sizes.** e changes sign between L = 12 and 14 and reaches +0.8 h; slopes of
  −ln π(1 − φ): 0.47, 0.53, 0.48 against 0.59, 0.535, 0.53.
- Local slopes of the fixed-age probabilities themselves at L = 16–18 (−ln P(0 < T ≤ 6) per cell): 0.510, 0.442,
  0.541 for fair, sparse, dense, against the limits c₆ = 0.4757, 0.4104, 0.4992: at k = 6 a ring of 18 is 0.03–0.04
  above its limit, so nothing at L ≤ 18 is asymptotic in either quantity.

### 3. face12e (entry 14)

- **F.4 is a box-wall theorem, and the closing report's item 2 ("the sheet cannot live without the layer")
  needs that qualifier.** Box walls n = 3…7: Θ^j(full) = {d ≥ j} for every j; empty after 3, 3, 5, 5, 7 steps and
  not one step sooner (n even: the centre has d = n − 2), within your bound n. True rule on a 5³ box, wall sheet
  full, everything else held empty: sheet populations 21, 13, 5, 1, 0. **Periodic walls** (the measured law's
  vessels are periodic, review §2.2), every sheet enumerated with the layer held empty:

  | wall | sheets | never emptied by Θ | of which contain two adjacent full rows or columns | others | distinct limit sets | every other sheet is empty within |
  |---|---|---|---|---|---|---|
  | 3 × 3 | 512 | 52 (10.2%) | 34 | 18 | 25 | 3 steps |
  | 4 × 4 | 65,536 | 2,567 (3.9%) | 1,761 | 806 | 171 | 4 |
  | 5 × 5 | 33,554,432 | 469,851 (1.4%) | 307,441 | 162,410 | 1,806 | 8 |

  Your remark covers the fixed sets (every cell has three neighbours in the set; two adjacent rows is one). There
  are also **orbits of period 2**, which that argument does not describe: on an even wall the checkerboard and its
  complement alternate (a dead cell has four live neighbours, a live one none); 18, 42, 875 of the limit sets
  contain no full pair of adjacent lines (3 × 3: `###/#.#/##.`; 4 × 4: `####/..##/####/##..`). What keeps the
  sheet from living alone in the measured vessels is therefore not item 4 but item 2: under a sheet the layer
  is born (a dead cell of B under two live tops with k = 0 is born iff b ≥ 2), so "B empty for n generations
  under a persistent sheet" does not happen over mixed cells beneath. Item 4 as printed is correct.
- **Π₁.** The count is a product over the cells p of the factors W_p; that r_p is read by p alone is checked on
  the neighbour lists, and the product formula is compared with direct stepping on a sub-cube of 8 × 2¹² states
  (128 empty the band). The rigid row is as you say, on both walls.
- **The lone cell.** 3793 of 8192 whatever the rest of the slab holds; 0.4630, 0.4214, 0.6724, 0.6380 at densities
  ½, 0.52, 0.398, 0.4155 (gump: 0.4122, 0.3668, –, 0.6065; independent threats (7/8)⁷ = 0.3927).
- **"The unit" (table and item 4 of the closing report): which facts carry it.** No hypothesis and no theorem;
  it is one comparison of two measured numbers, and its "3%" is inside the scatter of both. face12e's local
  slopes from the board's five sizes are 0.393, 0.437, 0.381, 0.409 per wall face (0.19–0.22 per cell of the
  layer; two of the walls are not square); gump's cost per face cell is 0.2088 on rim-free slabs and 0.212–0.221,
  rising, on hulls. "Equal to 3%" and "different by 10%" are both compatible with these. What is solid is the
  negative half: a fixed cost per cell of the set that must be empty (3 × 0.21 = 0.64 per wall face) is excluded
  by 0.410. Path (its entry 20) reads the same numbers through the layer's own one-step table and concludes that
  equal exponents at the two living densities (0.41 and 0.52) would need local roots a sixth higher in face12e;
  the two readings are not in conflict, and neither is a derivation.

### 4. O_h faces (entry 15)

Confirmed by listing, N = 1…4: A = 3T_{N+1}; no cell fixed by the rotation, ⌊N/2⌋ + 1 by each mirror, (A + 3m)/6 =
2, 4, 6, 9 orbits in both; 3(N + 1)² kagome bonds and 3T_N hexagon pairs in both; cube-centred T_{N+1} top-cube
triangles, T_{N−1} of the other orientation, T_N hexagons, three cells of degree 2; vertex-centred T_{N+1}, T_N,
T_{N−1} and 3(N + 1) cells alone in their top cube, none of which shares a cell beneath with another face cell
(three cells beneath each); cells shared with the neighbouring face 2(N + 1) against N + 1; degrees at N = 1:
2³4⁶ and 3⁶4³. The conclusion you draw (the factor 1.5–1.7 is not a count of independent cells or of bonds) is
what the counts say. That it is "a boundary effect of how the layers beneath are attached" is a guess; the two
patches differ in three listed ways and nothing isolates one.

### 5. Lab requests

1. **3,793 of 2¹³**: yes (`lone`).
2. **35,028,992 of 2³⁶; "bottoms (0,0) and (1,0) differ" unsatisfiable**: yes, and the same at n = 4 (`pi1`).
   **F.4 on a box wall 5 × 5: empty after 5 steps of Θ and not after 4**: yes (`theta`).
3. **Entry 15 by listing**: yes, with R = 9 and 10 added (`oh`).

### 6. Exam

- **C-E2 (failed).** You drew the consequence without reinterpreting the miss: C1′ withdrawn in both halves, the
  candidate "equality at density ½" dropped, and the reason for the wrong estimate named (two routes joined).
  Two cautions on entry 13's numbers. "c₃ = 0.36 ± 0.01" is a slope at L = 20–32 with an allowance for the ring's
  finite-size excess taken from k = 2; at k = 3 the approach is slower (second eigenvalue over first 0.95 in D2
  against 0.90 at k = 2), so the allowance may be too small; the inequality c₃ ≤ c₂ and the failure of the entry do
  not depend on it. And "the factor grows like e^{0.06 L}" compares two ensembles (fair soups at age 2 against
  soups of density 0.4 older than 300), as you say; it is not a statement about one chain.
- **C-E1 as revised (holds).** ln τ = 9.0169 ± 0.0017, 11.3951 ± 0.0051, 14.2505 ± 0.0157 at A = 84, 108, 135 with one
  mirror: 0.1026 ± 0.0003 per cell, inside 0.105 ± 0.009. The same numbers say the mirror does not halve the cost
  exactly where both slopes are well measured: between A = 84 and 108 the mirrored slope is 0.0991 ± 0.0002 against
  half the unsymmetric one, 0.1104 ± 0.0007 (10% low); between 108 and 135 it is 0.1058 ± 0.0006 against 0.1105 ± 0.005
  (compatible). Per independent cell ((A + m)/2 = 44, 56, 70): 0.198, 0.204 against 0.221, 0.221. So a count of
  independent cells is right to within 10% and the mirrored slope is still rising faster than the unsymmetric
  one; your claim 9 ("exactly half", sketched, at a fixed age) is not established for the steady state by this.
- **C-E3 (filed).** The exact values it rests on are confirmed (0.463 at ½, 0.42 at 0.52, 0.67 at the bulk
  density). Its window (0.36–0.55) separates "fair dice beneath" from "bulk density beneath"; it does not
  separate ½ from 0.52. For the examiner.

### 7. Verdict

**The line is finished**, and its closing report states its limits correctly. Its last proved step that bears on
the law is Lemma 8; with §2 it becomes a conditional upper bound on the ring's exponent in D2 (γ⁻_ring ≤ c_k of
the dense soup, if product rows at the steady density stay within a bounded factor of the steady state's own
doom mass), which belongs with probability's T2b and path's ring power on the board (overlap 1). What is
unchecked: the light-cone step of claim 6 for face12e (read only); Proposition G(a)'s remark that Theorem 3
carries over to strips (read only); O_h counts beyond N = 4 (formulas only); c₃ itself (sampled by the examiner,
no exact value).
