# REVIEW by ref-hull: split-hull's value for the 135-cell hull face

Written 04:55 UTC, 2026-11-18. Numbers and commands: this directory's README.md; full tables `out/NU-ANALYSIS.txt`
(`python3 nu.py out/nu`).

## What was refereed

split-hull's sampler gave no number for R = 17 (it failed its calibration; mine fails the same way, README §2). What
it offers is a forecast, **ln τ_face(135) = 29.227 ± 0.014**, from ln τ = −ln q(p) − ln ν(p): ν(0.6 P̄) measured by
plain running at R = 17, −ln q(0.6) extrapolated from 45–108 cells by a straight line in the area.

## Verdict

**Dip rates: CONFIRMED.** Independent stepper (validated against the oracle, R = 11 and 15, negative control fails),
independent seeds, all eight faces, 0.5–1.4 × 10⁹ hull-generations per radius. ln ν(0.6 P̄), mine − split-hull's:
−0.0022, −0.0010, +0.0015, −0.0047, +0.0064, −0.0053, +0.023 at R = 9, 11, 13, 15, 17, 19, 21; the largest is 2.3
combined errors. One finding: its P̄ comes from a short pilot and is off by −0.005 … +0.036 cells (mine are known to
0.0004); through the "threshold-free" interpolation this shifts ln ν(p P̄) by up to 0.007 (12 of its quoted errors at
p = 0.8, R = 19) and by 0.003–0.008 at p = 0.6: its errors on ln ν omit this. Harmless for the forecast.

**Line and forecast: REPRODUCED.** −ln q(0.6) = 5.609, 8.667, 12.244, 16.330; slope 0.17016 ± 0.00014; χ² 0.5 on 2.
By the same route my number is **29.219 ± 0.010** (statistical, with errors of 0.005 assumed for the R = 9 and 11
anchors), 0.008 below split-hull's, inside its error. R = 19: 35.781 ± 0.014 (its 35.778); R = 21: 43.006 ± 0.019
(its 43.03).

**The error ± 0.014 is the error of a model with no rim term, and the model is not known that well.**
- Allowing a rim term (a quadratic in k through the same four values): r = −0.027 ± 0.043 and 29.232 ± 0.023, which
  is to the digit what the four anchors give with no dip rate at all (29.232 ± 0.023). The route's gain in precision
  is the assumption r = 0.
- Attempt to break r = 0 without any lifetime (level differences are ratios of dip rates, measurable at every size):
  in-sample the straight line is rejected (χ² 459 on 2 for 0.6 against 0.5; the 45-cell face is 0.005–0.01 off), but
  out of sample, at R = 17, the line misses by +0.009 ± 0.003, −0.006 ± 0.020, +0.004 ± 0.006 where the quadratic
  misses by −0.024 and −0.041. **So "no rim term below 0.6 P̄" survives, to about 0.01, for everything between 0.6 P̄
  and 0.4 P̄ at 135 cells**; I could not break it. Below 0.4 P̄ nothing is tested at 135 cells.
- Level dependence: at R = 17 all deep levels and both conventions agree (29.20–29.22); at R = 19 they spread over
  35.73–35.78 and at R = 21 over 42.96–43.04. The choice of level is harmless at 135 cells and worth ± 0.03–0.04 beyond.
- My reading of the honest figure: **29.22 ± 0.02 if −ln q stays on its line; nothing if it does not.**

**Evidence or construction?** Both, in halves. Of 29.22, the part −ln ν(0.4 P̄) = 14.65 ± 0.02 is measured at 135
cells; it carries the entire rim term of the lifetime, and it sits where its smooth continuation puts it (ln ν(0.6 P̄)
at R = 17 is +0.0005 ± 0.0010 from its own quadratic in k). The other half, −ln q, is a four-point straight line,
which in the edge k is "the second difference repeats" under another name. "The wrapped price takes over" (29.163)
is, in these terms, a bend of about 2% in that line between 108 and 135 cells; three intervals of data show the
slope steady to 0.5%, so a bend would be a 5-error break of pattern, but no dip rate can exclude it. The forecast
excludes 29.163 by 0.056 = 2.8 of my honest errors conditionally, and is silent unconditionally.

**What the measured half does say, and split-hull did not [measured]:** the second difference in k of ln ν(0.6 P̄)
is not constant. −0.176, −0.181, −0.176, then −0.169 ± 0.002 and −0.153 ± 0.006 centred on R = 17 and 19 (fixed
density 0.30: −0.199, −0.202, −0.193, −0.186, −0.162 ± 0.009). The rim-carrying half of the exponent is bending
toward a lower price per cell from about 135 cells on. With −ln q on its line, the second difference of ln τ falls
0.691 → 0.686 → 0.679 → 0.663 and the forecasts are 29.22, 35.76 ± 0.03, 43.00 ± 0.04: at R = 21 already 0.085 ±
0.04 below "repeats" (43.085), still 0.31 above "takes over" (42.689). Neither named alternative is right if this
holds: the price drifts down slowly.

## Verdict line

split-hull's sampler value for R = 17: **NOT REACHED** (by either code). split-hull's dip-rate forecast 29.227 ±
0.014: **CONFIRMED as arithmetic and as measurement (mine: 29.219 ± 0.010); its error is conditional on a straight
line that is tested only above 0.4 P̄; honest figure 29.22 ± 0.02 conditional.** It is not a measurement of τ.

## Which code I believe where they differ

P̄ and the dip rates at p ≥ 0.7: mine (16 independent seeds, P̄ to 0.0004). Sampler bias at R = 11 (mine −0.024 ±
0.023 for half a layer toggled, its −0.173 ± 0.044 for a sixth): both are measurements of different designs; the
difference (4 errors) probably sits in its levels below five cells, which mine does not have [not investigated].

## Next step

Measure ν(0.6 P̄) and ν(0.4 P̄) on wrapped faces (tori of 63–126 cells) by plain running: cheap, and it tells whether
the 0.022 per cell between rimmed and wrapped faces lives in ν (then the bend seen above is the take-over starting,
and its end point is known) or in q (then the hull's q-line has a different slope from the torus's and must bend).
