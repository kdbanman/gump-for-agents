# ref-boom: forecasts frozen before any run (2026-11-18 04:50 UTC)

1. (p = 0.8) The two-size (48, 63 cells) value of min_θ [I_up + J], with ln ν and ln d interpolated linearly in p,
   will lie between 0.216 and 0.226, not at 0.210: because Σ ν·d = 1/τ is an identity, I_up(θ) + J(θ) =
   (slope of ln τ between the sizes) − Δ ln(√A·w_A(θA))/ΔA with w_A the launch histogram, so the minimum returns the
   lifetime's own slope (0.2158 for 48→63) plus at most (1/2)·Δ ln A/ΔA = 0.009.
2. (p = 0.85) Launch hump: one hump, mean 0.738 ± 0.005 of A at 48 and 63 cells. (p = 0.75) Its s.d. in cells
   grows like √A between 48 and 63 (ratio 1.10–1.19), not like A (ratio 1.31).
3. (p = 0.8) Layer profile at the launch (63 cells) within 0.01·A of boom's 0.73/0.64/0.56/0.51 and of the
   launch−1 values 0.40/0.36/0.38 for layers 2–4. (p = 0.6) The under-full layers 2–4 one generation earlier are
   also there before NON-fatal generations with the same over-full face (a property of any over-full generation,
   not a precursor specific to deaths), to within 0.015·A.
4. (p = 0.7) My ln τ at 48 and 63 cells within 2 standard errors of the anchors 9.9251, 13.1622.

## Scored (05:10 UTC; numbers in REVIEW.md)

1. MISS by 0.001 as stated: 0.2154 ± 0.0011 at θ = 0.74 (grid minimum 0.2139) with linear interpolation; the
   quadratic version (0.2168) is inside the interval. The reason given held (it is the lifetime slope, 0.2156).
2. HIT (mean 0.7380, 0.7375); HIT (s.d. ratio 1.168).
3. HIT (profile within 0.006 everywhere beneath the face); MISS (the under-fill before a fatal launch is 0.035,
   0.052, 0.040 of A, of which only 0.007, 0.017, 0.010 is generic).
4. HIT (48 cells +0.6 s.e.; 63 cells −0.1 pooled, single runs −1.8 and +1.6).

## Second task (static rarity of the four-layer state): frozen 05:28 UTC, before any static run was analysed

Procedure, fixed now. Boxes B_δ = {x_k ≥ m_k − δ for k = 1..4}, m = (0.738, 0.637, 0.562, 0.504), δ = 0 … 0.10 in
steps of 0.02; ln P_A(B) by multilinear interpolation of ln P over the integer thresholds. d₄(B) = launches in B /
generations in B; f(B) = share of all launches in B. Forecast: ln τ(A′) = −ln P_A′(B) − ln d₄(B; A′) + ln f(B; A′),
with ln d₄ and ln f extrapolated linearly in A from 48, 57, 63 cells (constant if the slope is within 2 s.e. of 0),
and P_A′(B) measured at A′ by plain running. The box used for the forecast is the loosest δ whose d₄-slope J₄ is
smallest in absolute value among boxes with at least 200 living-state events at A′.

Guesses:
5. (p = 0.6) d₄ in the box at the launch profile (δ = 0) is between 0.03 and 0.5 at 63 cells, not near 1.
6. (p = 0.65) J₄ at δ = 0 is below 0.05 per cell (against J = 0.136 for the face alone): most of the price moves
   into the static rarity of the four-layer state. (p = 0.5) J₄ < 0.02.
7. (p = 0.5) the out-of-sample forecast at 75 cells lands within 0.15 of 15.66; (p = 0.3) at 84 cells within 0.25
   of 17.54; (p = 0.2) at 108 cells within 0.5 of 22.54 (the boxes reachable at 108 will be too loose).
8. (p = 0.6) no statistic of the four fillings one generation earlier predicts a fatal launch with a lift above 10
   at the top 1% of living states.

## Second task, scored (05:43 UTC; numbers in STATIC.md)

5. HIT: d₄ in the box at the launch profile is 0.117 at 63 cells (0.273 at 48).
6. MISS: J₄ at δ = 0 is 0.057 ± 0.003, not below 0.05 (and not below 0.02): a quarter of the price stays in the kill.
7. HIT at 75 cells (forecast 15.53 ± 0.16, anchor 15.6442); HIT at 84 (17.33 ± 0.10 against 17.5387, within 0.25);
   HIT at 108 (22.13 ± 0.11 against 22.5405, within 0.5) -- but all three are low and the misses grow (0.12, 0.21,
   0.41), and the purely static version fails by 1.3, 2.8, 6.5.
8. HIT: the best statistic of the four fillings one generation earlier has a lift of 6.6-6.8 at the top 1% of living
   states (48, 63 cells; 10 ± 3 at 75 cells with 462 deaths).

## Third task (look-ahead events of the face): frozen 05:48 UTC, before any look-ahead run was analysed

Events anchored at t: L1(a, b) = {P(t) ≥ aA, P(t+1) ≤ bA}; L2(a, k) = {P(t) ≥ aA, P(t+1) < A/2, P(t+2) ≤ k};
L3(a, k) = {P(t) ≥ aA, P(t+1), P(t+2) < A/2, P(t+3) ≤ k}. d = chance that t is the launch of a death given the
event; I, J, F as before, fitted on 48, 57, 63 cells; forecasts at 75 and 84 from the living-state frequency there.
9. (p = 0.6) L1(0.70, 0.20): d between 0.02 and 0.3 at 63 cells and J between 0.02 and 0.08: not size-independent.
10. (p = 0.6) L2(0.70, 4 cells): |J| ≤ 0.015 and I within 0.012 of the lifetime slope of the fit sizes.
11. (p = 0.5) the forecast at 75 cells from L2(0.70, 4 cells) with d and f held constant is within 0.2 of 15.64;
    (p = 0.4) at 84 cells within 0.3 of 17.54.
12. (05:54 UTC, before the 108-cell look-ahead run finished) (p = 0.6) The forecast at 108 cells from L1(0.70, 0.30A)
    (living frequency at 108 cells, d and f extrapolated linearly from 48, 57, 63) is within 0.15 of 22.5405;
    (p = 0.5) the same from the face alone, {P ≥ 0.70A}, is within 0.25.
13. (05:56 UTC, before the tube run) (p = 0.6) For the 84-cell tube (1,12),(0,28) (anchor 17.3175; the wide 84-cell
    torus 17.5387) the forecast from the tube's own living-state frequency of L0(0.74) and L1(0.70, 0.30A) with the
    WIDE faces' kill law lands within 0.08 of 17.54, i.e. misses the tube by about +0.2: the tube's discount is in
    the kill (boom's finding), not in the static term.
