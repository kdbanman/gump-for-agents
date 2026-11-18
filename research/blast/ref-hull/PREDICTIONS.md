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
