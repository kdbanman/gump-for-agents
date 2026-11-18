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

### Scored (04:12 UTC; `out/h63.txt`)

1 hit (13.6234). 2 miss, badly (+0.517 and +0.340: the hull face's population is a slow variable; I expected it to
look like the torus alive). 3 hit at the edge (0.0108). 4 hit (31.18; 0.0004). 5 hit (0.1827; e^+0.038). 6 hit
(0.084). 7 hit (0.790). 8 hit (one hump, median 14). Seven of eight.

## Block 2 (the two-variable map (P, B) and its minimum action), 2026-11-18 04:24 UTC, before any joint tally exists

Known to me when writing: the review's numbers (one-variable return maps, the regression in over-full generations,
the route 33 → 48.8 → 11.2 with 25 → 39.9 → 9.9 beneath), `model`'s remark that the measured upper tail is 1.27
times the Gaussian exponent. Not known: any joint map, any action.

1. Gaussian minimum action per cell on the wide torus (map measured at 63 cells): 0.16 (60%: 0.12–0.20); below
   gump's 0.2087 (70%).
2. ln τ of the Gaussian two-variable chain at 63 cells (exact absorption time): 11.0 (60%: 9.5–12.5); below 13.16 (75%).
3. The torus's minimum-action route has a single generation at x ≥ 0.70 followed by one at x ≤ 0.25 (65%).
4. Hull face: action per cell higher than the torus's (65%); ratio between 1.05 and 1.25 (45%); its route has no
   generation at x ≥ 0.70 and takes at least 6 generations from the last normal state (55%).
5. Collapse: drift at equal (x, b) agrees between 48, 63 and 84 cells to 0.01 in filling over the populated living
   region (60%); covariance times A agrees to 10% (60%).
6. The third layer: in ordinary generations the residual of P′ about the (P, B) map depends on C by less than 0.1
   cell per cell (70%); in over-full generations by 0.15 or more (50%).
7. The loop²-12 tube's map equals the wide torus's at equal fillings to 0.005 over the living and over-full region
   (60%), so the action does not reproduce the tube's lower lifetime (60%).

### Scored (04:42 UTC; `out/theory.txt`, `out/theory2.txt`)

1 hit (0.1595). 2 miss (13.07: the chain's lifetime at the map's own size is nearly forced, which I had not seen).
3 hit in kind (x = 0.730, then 0.254). 4 two of three (higher: yes; ratio 1.45, not 1.05–1.25; a 13-generation
fade with no over-full generation: yes). 5 half (neighbouring sizes agree to 0.006–0.008 in drift and 4% in
variance; 48 against 84 differ by 0.014; the 1/A pattern was not foreseen). 6 hit (−0.04; −0.24). 7 first half hit
(0.001), second half miss (3% more noise does give the tube a lower action).
