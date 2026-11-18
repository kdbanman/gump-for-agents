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
