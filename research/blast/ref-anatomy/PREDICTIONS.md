# Forecasts of ref-anatomy

Honest note: the torus and tube runs were measured and read before any forecast was written (the referee had 50
minutes); nothing is claimed for them. The block below was written at 04:05 UTC on 2026-11-18, while the hull run
was still going and before any of its output was opened.

## Block 1 (hull face of 63 cells, radius 11), 2026-11-18 04:05 UTC

1. ln tau_face within 0.03 of 13.633 (85%).
2. Lag-1 autocorrelation of the face population positive, between +0.10 and +0.25 (70%); lag 2 within 0.05 of zero (70%).
3. Share of deaths with a one-generation fall of >= 32 cells in the last 12 generations between 0.01 and 0.03 (75%).
4. Mean P one generation after P >= 46 between 30 and 33 (75%); share of those generations followed by P <= 15
   below 0.001 (80%).
5. q(4) between 0.17 and 0.20 (70%); nu(4) within a factor e^(+-0.06) of the torus (60%).
6. Share of fatal excursions whose first generation at <= 16 cells came within 4 generations of P >= 44: under 0.15 (65%).
7. Plane fit to last-alive times (my 16-generation window, censored) beats 95% of shuffles in 0.60-0.85 of deaths (60%).
8. The largest-fall distribution of hull deaths is one hump with median 12-14 cells (70%).
