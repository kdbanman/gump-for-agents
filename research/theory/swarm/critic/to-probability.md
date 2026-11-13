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
