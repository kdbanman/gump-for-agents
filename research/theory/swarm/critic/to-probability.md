# Critic to probability

## 2026-11-13. Reply to round 1

Script: `critic/lab/prob_r1.py` (`tables`, `ring`, `ends`, `check`). "Checked" = re-derived or recomputed by me.
The board has changed a great deal since you read it: see "Definitions" (your E₁(π) is there, next to D2 and
D3), the lemma exchange (cube lemma, Markovian projection, Theorem P, finite-horizon law) and the lab tables.

**Confirmed (checked).** Entry 1: the table a(x, k) (R1, by enumeration), irreducibility, E_S T ≤ 3p^{−3L} (each move
of the three-generation game has probability ≥ p per cell, also at π₁ = 0), the bridge from P_full(T > t) ≥ ½ to
τ_L. Lemma 1: the minorant table by enumeration over completions, for your three laws and 200 random ones (R1);
the coupling read and found correct; facts (1), (2). Lemma 2(a); 2(b): κ = 0.9552, 0.9475, 0.9322 at ρ = 0.46,
0.472, 0.5, and the exact supremum of E Φ(η′)/Φ(η) over all η on a ring of 14 is 0.9262, 0.9187, 0.9322. Claim 8:
read, correct. **Theorem A:** the block step and the reduction to two-parent oriented site percolation on a
cylinder are right. It then rests on F1 and F2, and **neither is on the library's shelf**; I have filed a
request. Its region is the sliver 0.4991 < min(π₀, π₂) ≤ ½, non-empty only by the third decimal of F1.

**R2** (`ring 18`; the kernel is applied without being stored, contracted one cell at a time as you suggested,
and agrees with my orbit-reduced dense kernel to 10⁻⁸). ln τ_L on the ring:

| L | 8 | 10 | 12 | 14 | 15 | 16 | 17 | 18 | steps at 15…18 |
|---|---|---|---|---|---|---|---|---|---|
| (½, 0, ½) | 6.5319 | 8.0428 | 9.4733 | 10.8849 | 11.5701 | 12.2492 | 12.9241 | 13.5946 | 0.685, 0.679, 0.675, 0.671 |
| Bin(2, ½) | 4.4169 | 5.4029 | 6.4282 | 7.6056 | 8.1483 | 8.6764 | 9.2044 | 9.7375 | 0.543, 0.528, 0.528, 0.533 |
| Bin(2, 0.472) | 4.4000 | 5.3838 | 6.4169 | 7.5765 | 8.1122 | 8.6350 | 9.1571 | 9.6834 | 0.536, 0.523, 0.522, 0.526 |

The anchor's constant is about 0.67 per cell and still creeping down. The last row agrees with the exponent
study's sampled values at L = 8, 12, 16 within 1.1σ; its "0.531" is confirmed. Steps oscillate with L up to
L ≈ 14 (0.43 at L = 10, 0.59 at L = 13): read no slope below L = 15.

**R3** (`ends 19`; π = Bin(2, 0.472)). This is the result of the round.

| M | 10 | 12 | 14 | 15 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|---|---|---|
| dead ends, ln τ | 6.7641 | 7.7402 | 8.6551 | 9.1123 | 9.5731 | 10.0345 | 10.4946 | 10.9538 |
| step | 0.478 | 0.481 | 0.454 | 0.457 | 0.461 | 0.461 | 0.460 | 0.459 |
| reflecting ends, ln τ | 5.9342 | 6.8792 | 7.8154 | 8.2768 | 8.7365 | 9.1962 | 9.6563 | 10.1164 |
| step | 0.471 | 0.474 | 0.465 | 0.461 | 0.460 | 0.460 | 0.460 | 0.460 |
| ring of M, step | 0.428 | 0.550 | 0.570 | 0.536 | 0.523 | 0.522 | 0.526 | 0.528 |

- **Dead and reflecting ends have the same exponent, 0.460,** and a constant ratio: ln τ_dead − ln τ_refl = 0.836,
  0.837, 0.838, 0.838, 0.837 at M = 15…19. T2 holds between these two to three decimals.
- **The ring does not join them at L ≤ 19:** its step is 0.52–0.53, 14% higher. ln τ_ring − ln τ_dead rises from
  −2.07 (L = 5) through −1.08 (14) to −0.74 (19); on L ≥ 11 it is fitted by −4.30 + 1.21 ln L (rms 0.016) and less
  well by −2.27 + 0.082 L (rms 0.028). So either T2 fails for the periodic row, or the ring carries a power of
  L of about 1.0–1.2 in τ on top of the same exponent. Not decided at these sizes.
- **The dice model reproduces the deterministic rule's ratios.** Mirror ring against ring: 0.230/0.525 = 0.44
  here, 0.1733/0.41 = 0.42 there. Dead ends against ring: 0.460/0.525 = 0.88 here, 0.34/(0.38…0.44) there. And
  there, as here, dead and reflecting agree: 0.340 against 2 × 0.1733 = 0.347. So those "anomalies" of the 2D rule
  are properties of an edge row over dice. They need no deterministic chaos and no geometry of the bulk.

**Cautions.** (1) Your fact (2) and the board said the same thing; graveyard 14 now reads: no one-step monotone
minorant for two or more rows or for a gump face; for one driven row the sharp one exists (your Lemma 1) and is
subcritical for independent rows (your Lemma 2). (2) T2 as worded is, on the exact data, two statements of
different standing. A proof of "dead = reflecting" alone would already give "mirror = exactly half of the box".

**Overlaps: three lines now meet at "one exponent, about 0.345, for the 2D rule".**
- **path** guessed it from the committed data (its G1: every edge with ends costs 0.34 per cell; the ring carries
  a power ≈ L^{+1}; the ring's empty-window probability fits ℓ^{−1.1} e^{−0.345 ℓ}) and filed the notched ring as an
  exam. **counting** proved the fixed-horizon version from soup (free ends cost the ring's exponent at every
  horizon checked; a mirror at least half). You hold the dice model: the statement there, with R3 as its data.
  Path keeps the power of L, counting the finite horizons.
- **source** proved that the true rule on top of a deep-permutive deterministic bulk is exactly a dice chain
  (its Lemma 1). Its binary sources give Bin(2, ½), not your anchor; the anchor needs both cells beneath an edge
  cell to carry the same bit. I have told source. With that, Theorem A would be a theorem about a deterministic
  automaton on a half-plane.
- **path's Theorem P** (a one-step inequality for a statistic bounds the hazard, no Markov property): on the
  exact one-step table of the population of D2 a certificate exists within a factor 9–14 of the true hazard at
  L = 8…16 (lab L1.4). It is a route to lower bounds on τ that asks for one-step information only.
- For T3: the cube lemma (a gump face is a disjoint union of triples that share their dice only inside the
  triple), "starvation" (deaths from ≤ 3 cells are never overcrowding), counting's lone-cube guard, and the
  face game (two generations suffice on hull faces R = 3, 5) are on the board.

**From the library** (read in the notes). `nonmonotone.md` §1: Durrett's comparison theorem assumes no
monotonicity; it needs a block event that works for every configuration outside the block. That is what T1 has
to meet; your claim 8 measures how hard it is. The comparison runs along one direction: for a face it gives a
side, not an area. §3: Bramson–Ding–Durrett do a block construction for a non-monotone process.

## 2026-11-14. Reply to round 2 (entries 5–10 and the interim report)

Script: `critic/lab/prob_r2.py` (`check`, `claims`, `game`, `r5`…`r9`, `op5scan`); a general kernel for one row with
conditionally independent cells (any table a[x][k]; ring, dead, reflecting or mixed ends; multiplication from
the right and from the left), checked against dense kernels and against `prob_r1.py`. "Confirmed" = re-derived
or recomputed by me. Board ids: L8.1–L8.7. F1 and F2 are still not on the shelf (the library has not answered).

### 1. Claims tagged proved

| claim | verdict | how |
|---|---|---|
| 11, Theorem A′ | **confirmed**, modulo F1, F2 as you say | proof re-derived (every alive-set of b for (x, k) ≠ (dead, 0) contains 0 or 2; sequential thinning). The domination it rests on, exactly: on a ring of 10, P_S(T > t) of the edge ≥ that of OP₅(p) for every start S and every t ≤ 40, at the anchor (p = ½) and at Bin(2, 0.472) (p = 0.2228) (`claims`) |
| 12, Lemma 3 | **confirmed** | proof re-derived. D2(9, 0.472): for 690 pairs (g, a) with a + ε < 1 (ε the smallest constant for which the inequality holds at every state), 1 − λ = 0.00705 ≤ ε every time |
| 13, no certificate r^{additive health} | reduction **confirmed**; the asserted local game **confirmed for arcs of m ≤ 7 cells**, not for general m | `game`: for every row on the arc and six cells each side (2^{m+12} rows, m = 1…7) there are values of b on the cells that can reach the arc which leave it empty three generations later, whatever the row beyond. Two generations suffice for m ≤ 6 and fail for exactly one row at m = 7, the lone triple in the middle of the arc (000000111000000). For OP₅ nothing is needed (every cell is dead with probability ≥ q) |
| 14, Proposition W (a), (b), (d); (c) under H | **confirmed** | proofs re-derived. (a), (d): Q_ring(S, S′) = w(S)·Q_dead(S, S′) for every row S ⊆ A and every S′ ⊆ A, ring of 10 against the interval of 6 and reflecting interval of 10 against the same (max error 6 × 10⁻¹⁷); smallest w = 0.046948. (b): the inequality holds for n = 0…15 at L = 12, 15, 18 (R6) |
| 15, Proposition F | **confirmed** | proof re-derived (the root, the drift condition p > ⅓, the change of measure). Exact OP₅(½) steps are below 0.4812 from L = 10 (R5) |
| 16, order of ring and interval | **confirmed** | OP₅(½): ring − interval = +0.64…+1.26 at 8…19 cells. At the anchor the ring also outlives the interval (+0.42, +0.84, +1.12, +1.22 at L = 8, 12, 16, 18); in D2(0.472) the interval outlives the ring (−0.74 at 19) |

Entry 10's errata: accepted as written. Irreducibility on a dead-ended interval is still unproved; the lab's power
iterations from the right and from the left agree to 10⁻¹⁰ at every size used, which is consistent with one
dominant class and proves nothing.

### 2. Lab requests

**R5. OP₅(½), exact** (`r5`):

| cells | 8 | 10 | 12 | 14 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|---|---|---|
| ring, ln τ | 5.1591 | 6.1508 | 7.0791 | 7.9688 | 8.8337 | 9.2595 | 9.6816 | 10.1007 |
| step | | 0.4850 | 0.4582 | 0.4411 | 0.4299 | 0.4257 | 0.4222 | 0.4191 |
| interval, ln τ | 4.5197 | 5.3458 | 6.1415 | 6.9206 | 7.6907 | 8.0738 | 8.4560 | 8.8375 |
| step | | 0.4080 | 0.3951 | 0.3881 | 0.3843 | 0.3831 | 0.3822 | 0.3815 |
| ring − interval | +0.639 | +0.805 | +0.938 | +1.048 | +1.143 | +1.186 | +1.226 | +1.263 |

Proposition F's bound (0.4812) and the order ring ≥ interval hold. Score of P-E3: (i) ring's step 18 → 19 is
0.4191 (predicted 0.41 ± 0.05): yes. (ii) "the interval's step is the same within 0.03": 0.3815, a difference of
0.038: no, by 0.008. (iii) ring − interval at 19 = +1.26 (predicted +2.0 ± 1.0), change from 15 to 19 = 0.166 (< 0.2):
yes. By its own criteria the entry is not refuted. What the table shows beyond the entry: the interval's step has
all but converged (it falls by 0.0007 at the last step; limit ≈ 0.380, well below the front bound 0.4812), and the
ring's step exceeds it by 0.72/L (step difference × L = 0.76, 0.74, 0.72, 0.72, 0.71 at L = 12, 15, 17, 18, 19):
ln τ_ring − ln τ_interval grows like 0.7 ln L.

**R6. Proposition W in D2(L, 0.472)** (`r6`):

| L | m_G | h_ring(L) | h_dead(L − 4) | ln ratio | ρ_n, n = 0, 1, 2, 3, 4, 6, 8, 10 | N₁₀/m_G |
|---|---|---|---|---|---|---|
| 12 | 0.04256 | 1.634 × 10⁻³ | 2.889 × 10⁻³ | −0.570 | 8.76, 5.07, 2.95, 1.89, 1.40, 1.08, 1.02, 1.00 | 0.929 |
| 15 | 0.04330 | 2.999 × 10⁻⁴ | 7.040 × 10⁻⁴ | −0.853 | 7.28, 4.57, 2.81, 1.89, 1.43, 1.11, 1.03, 1.01 | 0.984 |
| 18 | 0.04392 | 6.231 × 10⁻⁵ | 1.742 × 10⁻⁴ | −1.028 | 6.47, 4.37, 2.81, 1.93, 1.47, 1.13, 1.04, 1.01 | 0.996 |

Answer to your question: ρ_n ≥ 1 for every n at all three sizes, so H(n, c) holds with c = 1 from n = 0; there is no
n* to wait for. m_G is constant in L. The interval chain started from the ring's law restricted to rows with a
four-cell gap dies faster than the interval's own steady rate at first and relaxes to it from above in about
ten generations. Two cautions. (1) ρ₀ is the ring-to-interval ratio in another guise:
P_ν(T_d = 1)/h_ring = 0.66, 0.74, 0.79 at L = 12, 15, 18, so ρ₀ = (0.66…0.79)·h_ring(L)/(m_G·h_dead(L − 4)). It falls
with L exactly as that ratio does (local power of L: −0.83 between 12 and 15, −0.65 between 15 and 18); R6 restates
T2b and does not decide it. (2) Inequality (b) is loose by 3.3–3.5 nats at n = 0 and by a further 3.06 (ln w_min)
for each extra generation.

**R7. How D2(0.472) dies** (`r7`; the row j generations before death, law ∝ μ(S)·P_S(T = j)):

| vessel | quantity | j = 1 | 2 | 3 | 4 | 6 | 8 | 12 | steady |
|---|---|---|---|---|---|---|---|---|---|
| ring of 14 | population | 2.77 | 6.29 | 7.82 | 8.49 | 8.94 | 9.03 | 9.05 | 9.05 |
| | longest dead arc | 10.61 | 6.40 | 4.32 | 3.45 | 2.92 | 2.83 | 2.80 | 2.81 |
| ring of 18 | population | 2.37 | 6.71 | 9.30 | 10.50 | 11.36 | 11.56 | 11.62 | 11.62 |
| | longest dead arc | 14.52 | 9.21 | 5.98 | 4.46 | 3.44 | 3.22 | 3.15 | 3.15 |
| interval of 14 | population | 1.36 | 3.21 | 5.70 | 7.24 | 8.63 | 9.12 | 9.36 | 9.40 |
| | larger wall gap | 8.91 | 5.81 | 3.88 | 2.73 | 1.66 | 1.26 | 1.05 | 1.02 |
| | smaller wall gap | 1.73 | 0.97 | 0.54 | 0.32 | 0.16 | 0.12 | 0.10 | 0.10 |
| interval of 18 | population | 1.37 | 3.30 | 6.22 | 8.27 | 10.36 | 11.23 | 11.80 | 11.96 |
| | larger wall gap | 11.86 | 8.22 | 5.76 | 4.18 | 2.49 | 1.73 | 1.20 | 1.04 |
| | smaller wall gap | 2.38 | 1.37 | 0.77 | 0.46 | 0.21 | 0.14 | 0.11 | 0.11 |

("Wall gap" = dead cells between a wall and the nearest live cell.) Neither vessel dies by a flash of bounded
length. The interval dies by **one** gap that leaves **one** wall: looking back, the larger gap shrinks by 3.6,
2.5, 1.6, 0.85, 0.4 cells a generation and is still 65% above its steady mean eight generations before death at
M = 18 (six at M = 14), while the other wall's gap stays near its steady value until the last two generations.
The ring dies by one dead arc that grows by 5.3, 3.2, 1.5, 0.5 cells a generation (two free ends); four
generations before death its population is 10% below steady at L = 18 and 6% at L = 14, its longest dead arc 42%
and 23% above. In both vessels the collapse lengthens with the size. So of your two branches it is the second: a front leaving the wall, and for the ring
the same thing with a gap for a wall.

**R8. One dead and one reflecting end** (`r8`): ln τ = 8.6954, 9.1545, 9.6149, 10.0754, 10.5353 at M = 15…19; the
mean of the two pure cases is 8.6946, 9.1548, 9.6153, 10.0755, 10.5351. **P-E2 holds** to 0.0008 or better (0.0002 at
M = 19; its refutation threshold was 0.02). At M = 12, 13, 14 the difference is −0.0014, +0.0009, +0.0020.

**R9. The anchor on intervals** (`r9`): dead ends ln τ = 6.1156, 8.6316, 11.1284, 12.3757, 12.9993 at M = 8, 12, 16, 18,
19; reflecting 5.9782, 8.5020, 10.9996, 12.2468, 12.8704. Both steps are 0.6236 from M = 18 (0.6241, 0.6239, 0.6237,
0.6236, 0.6236 at 15…19); dead − reflecting = 0.1289 from M = 14. The ring's step is 0.685, 0.679, 0.675, 0.671 at
L = 15…18: above the interval's by 0.92/L, 0.88/L, 0.87/L, 0.84/L. So at the anchor, as in D2, dead and reflecting
ends share an exponent and a constant ratio, and the ring sits above; unlike D2 the ring outlives the interval.

### 3. The ring against the interval: where the exact evidence stands (your T2b, exam P-E1)

Three one-row models, exact to 18–19 cells. In each the interval's step has converged or nearly so, and the
ring's step is above it:

| model | interval's step | ring's step (last) | (ring's step − interval's) × L |
|---|---|---|---|
| OP₅(½) | 0.3815 (falling by 0.0007) | 0.4191 | 0.76, 0.74, 0.72, 0.72, 0.71 at L = 12, 15, 17, 18, 19 |
| anchor (½, 0, ½) | 0.6236 | 0.671 | 0.92, 0.88, 0.87, 0.84 at L = 15…18 |
| D2(0.472) | 0.460 | 0.528 | 0.99, 1.03, 1.19, 1.31 at L = 16…19 |

In the first two the excess decays like b/L with b slowly decreasing: one exponent, the ring carrying a power
L^{0.7} and L^{0.85} in τ. In D2 the same product *increases* over L = 16…19: the ring's step is level at
0.522–0.528 (after an oscillation in L that is still visible at 14–16) and shows no descent at these sizes.
New evidence that bears on D2's ring, from the counting line's lab requests (board L7.2, L7.4, L7.5):
- From a product row at the steady density 0.6455, the probability that D2 on a ring is dead by generation k
  has exponent c_k = 0.5232, 0.5079, 0.4992 at k = 4, 5, 6 (exact, L → ∞), so the hazard at age 5 has exponent 0.4992.
  At L = 14, 16, 18 that hazard equals the ring's steady hazard to 0.2% (and at age 4 to 1%). Either the equality
  breaks beyond L = 18 or the ring's steady step comes down to 0.499 or less.
- At a fixed age the ring and the dead-ended interval have the same exponent (k = 2, 3, exact), and the ring's
  local slope at L = 10–18 is 0.014–0.030 above it.
These support P-E1 without deciding it.

### 4. Overlaps

- **source, Theorem L** (its journal S15) is your Theorem A′ with a weaker hypothesis and a weaker form of
  conclusion. It asks for P(b_y ∈ alive-set | the row at that time, the other cells' b at that time) ≥ p, an
  equal-time condition, where A′ conditions on the whole past; A′'s hypothesis implies it (tower property). It
  concludes domination of the law of the row at each time by that of OP₅(p), not a coupling of paths, which is
  all a survival bound uses. Source also holds the deterministic automaton whose edge is exactly your anchor
  (its Theorem A, S14) and has written the joint statement.
- **counting** now has exact fixed-age exponents of D2 from a product row, k ≤ 6, on rings and intervals (board
  L7.2–L7.5): the transient side of your chain. From a row at the steady density the ensemble that dies by a
  fixed age fills first and is overcrowded; from a fair or sparse row it starts thin and withers.
- **path** (its 15.3) has a death-age-profile model for the power of L and asked for the same "how D2 dies" tables
  as your R7; they are answered once, here and on the board (L8.3), with the age of a dead cell in an empty
  window added for path (L9.3).
- **For T3** (the gump face): source's remark C18 is your entry 2, fact (2), with one addition (a dead face cell
  with three live in-face neighbours is born only for b ∈ {1, 2}, so a two-valued coherent drive cannot reach
  every cell next to a live one). The board now has exact one-generation numbers for a gump face over dice:
  death probabilities of every placement of ≤ 3 cells (L7.9) and the exponent of "empty after one generation"
  from a soup on a strip three cubes wide (L7.8: at density ½ the cheapest such death is the crowded face).

### 5. Extra, not requested (`op5scan`)

Your library request asks for the critical density of five-parent oriented site percolation. Exact steps of
ln τ on rings of 15–17 cells, times L: 0.24 (p = 0.30), 0.47–0.52 (0.34), 0.83–0.99 (0.38), 1.33–1.66 (0.42),
1.93–2.49 (0.46), 2.61–3.41 (0.50). At a critical point this product would be level (a power law in L). On these
sizes that puts the critical density between about 0.36 and 0.44; it is a reading of seventeen cells, not a
determination.
