# ref-hull: forecasts frozen before the data

## 2026-11-18 04:36 UTC — R = 17 (135-cell hull face), before any R = 17 run of mine exists and before opening
## split-hull's results, calibration table or PREDICTIONS

Known to me: hull anchors 9.819, 13.633, 18.141 ± 0.005, 23.3392 ± 0.0099 (per-cell increments 0.2119, 0.2147, 0.2166
over the three intervals); the two candidates 29.230 (second difference repeats; increment 0.2181) and 29.163
(wrapped price takes over; increment 0.2157); the prefactor model's 29.205.

1. True ln τ(135): point forecast **29.215**, 68% interval 29.18–29.25. P(truth nearer 29.230 than 29.163, i.e.
   above 29.1965) = **0.70**. Reason: the increments have risen smoothly (+0.0028, +0.0019); the take-over scenario
   needs that trend to reverse within one step.
2. My own measurement will NOT reach ± 0.03 (P = 0.85): at R = 11 one replication of my sampler scatters by 0.19 in
   ln τ (clones of one parent share their fate for several levels), and the CPU left is about 15 minutes of one
   shared core. Forecast for my error at R = 17: ± 0.08 to ± 0.15.
3. My R = 17 value will lie within 2 combined errors of split-hull's (P = 0.75).
4. Sign of any disagreement: perturbation makes faces die sooner in my code (measured at R = 9: 29 flips per clone
   give 9.787 ± 0.010, 4 flips give 9.815 ± 0.011, anchor 9.819; about −1.8e-4 per flip per stage). If that slope
   holds at R = 17, a sampler with ~17 flips × ~19 stages reads about 0.06 LOW. So: P(split-hull's R = 17 value is
   below the truth by more than 0.03) = 0.5 [conjectured]. I cannot see their calibration, which would show it at R = 15
   (expected offset there about −0.04).
5. Share of sampled deaths whose largest one-generation fall is at least half the face (A/2 cells): about 1.8% at
   R = 9 (measured), will be below 2% at R = 13, 15, 17 and not growing (P = 0.7).

## 2026-11-18 04:55 UTC — scoring of the block above, and one new forecast

- 1 (truth 29.215; P(nearer 29.230) = 0.70): NOT SCORED. No measurement of τ(135) exists; the dip-rate route gives
  29.219 ± 0.010 by construction in its unmeasured half (REVIEW.md).
- 2 (my sampler will not reach ± 0.03): RIGHT, trivially: it was stopped at R = 11 (scatter 0.19, as forecast) when
  the PI redirected me to the dip rates.
- 3: void (split-hull's sampler produced no R = 17 value). 4: the sign was right at the sizes where split-hull
  measured its bias (−0.027 at R = 9, −0.173 at R = 11); the size at R = 11 was far above my slope's −0.02.
- 5 (share of deaths with a one-generation fall ≥ A/2 below 2% and not growing): RIGHT at R = 11 (0.4% ± 0.2%,
  against 1.5–1.9% at R = 9); not measured at R ≥ 13.
- New, for the wrapped faces nobody has decomposed yet: the second difference in k of ln ν(0.6 P̄) on hull faces will
  keep shrinking (centred on R = 21: between −0.15 and −0.11, P = 0.6), and on wide tori −ln ν(0.6 P̄) will be a
  straight line in the area with slope 0.035–0.045 per cell (P = 0.5), i.e. the hull's bend is heading for the
  wrapped price in ν while q has the same slope 0.170 for both (P = 0.4).
