# Forecasts of agent `boom` (blast of 2026-11-18), frozen before the data

## Block A: 03:57 UTC by the machine clock, before any run of mine

Known to me: BRIEF-COMMON.md, anatomy's README (boom 48.5 of 63, survivors 11.6, one bust in about 130 fatal,
ln P(P ≥ 46) = −6.04 on both the wide torus and the loop²-9 tube at 63 cells, mean 32.6, s.d. 4.94; E[P(t+1) | P ≥ 46]
= 22.9), PREDICTIONS.md blocks 0–2. Nothing of mine has run.

Definitions I will use. A death is booked on the generation of the **largest population in the 30 generations before
the first empty one** (latest if tied): its "peak" p. ν(p) = stationary probability of population p per
face-generation; d(p) = chance that a generation with population p is the peak of a death. Then 1/τ = Σ_p ν(p)·d(p)
exactly, and θ* = (mean peak of deaths)/A.

1. **Saddle.** θ* (mean peak of the deaths whose peak is ≥ 0.68·A) = 0.77 ± 0.02 at 48, 63, 75 and 84 cells, and it
   moves by less than 0.02 between 48 and 84 cells. P = 60%.
2. **Shares.** At fixed θ = 0.77, −d ln ν(θA)/dA (48 → 84 cells) = I_up = 0.090 ± 0.015 (43% of 0.2087) and
   −d ln d(θA)/dA = J = 0.119 ± 0.02 (57%). P(I_up share between 33% and 53%) = 60%. P(I_up + J at the saddle within
   0.015 of 0.2087) = 65%.
3. **Sum rule by cloning.** Σ_p ν(p)·d_clone(p) reproduces 1/τ of the same run within 25% at 48 and 63 cells
   (the clones of one parent are strongly correlated; I expect the effective number of independent clones per parent
   to be under 3 of 64). P = 60%.
4. **Bias test.** The clones' population 4 generations after the flip has the same mean as the natural
   continuation given the same starting population, within 0.3 cells. P = 85%.
5. **Tube discount: which factor.** At equal area the tube's ν at the saddle is within 10% of the torus's (the
   lower mean and the larger variance cancel; anatomy's −6.04 against −6.04), and the discount is in d: P(more than
   half of the discount in ln τ between the 84-cell tube (1,12),(0,28) and the wide 84-cell torus, 0.221, is in
   d rather than ν) = 70%. Variance per cell of the face population is larger on tubes by 2–6% and grows with
   length at fixed girth: P = 55%.
6. **Return map.** E[P(t+1) | P(t) = p] is unimodal with slope between −0.5 and −0.9 at the fixed point (over-fill
   answered by under-fill one generation later; a damped period-2 oscillation). P = 80%. A one-variable Gaussian
   map with the measured mean and variance gives a minimum action within 20% of 0.2087: P = 35% (I expect the
   Gaussian tail to be wrong for the survivors' starvation, where the numbers are a dozen cells).
7. **One-variable Markov closure.** The chain on {0..A} built from the measured one-step transition counts has a
   lifetime within 0.3 in ln τ of the true one at 48 and 63 cells: P = 45%.
8. **Hull.** The share of hull-face deaths with a half-face fall at 84 cells is below the 1.6% at 63 (so no trend
   towards a switch by 700 cells): P = 55%.

## Block B: 04:05 UTC, after a 100,000-generation test on the 48-cell torus (4,812 deaths), before any production run has been read

Seen so far (test48 only): launches are one hump at 0.74·A (s.d. 0.06·A) whatever the level L; clones of one parent
count as 2.3 independent ones of 64; the one-variable map with the run's own one-step statistics gives a minimum
action of 0.2104 per cell (empirical tails) and 0.188 (Gaussian) against ln τ/A = 0.2068.

9. **The 120-cell tube (1,18),(0,40)**: ln τ_face = 24.56 ± 0.04 (the discount against the wide line keeps its
   second difference: 0.226, 0.302, 0.392 → 0.496). P = 55%. This is extrapolation of the anchors, written before my
   own plain runs at 108 and 120 cells; any number my decomposition gives later is entered below it.
10. **Where the tube's discount sits at 108 cells** (plain runs give ν(p) there; discount 0.38–0.39 in ln τ): the
    tube's ln ν at θ = 0.74 exceeds the 6×6 torus's by less than half of the discount (under 0.19): P = 65%. Point
    forecast +0.10. Variance per cell of the face population, tube over torus: 1.03 ± 0.02.
11. **Minimum action of the one-variable map with empirical one-step tails, at 63 cells (run t63)**: 0.210 ± 0.004
    per cell; P = 60%. Gaussian version 0.185–0.195: P = 60%.
12. **Launch hump** at 63, 75, 84 cells and on the tubes: mean launch 0.74 ± 0.015 of A everywhere (no drift with
    A, none between tube and torus beyond 0.01): P = 60%.
