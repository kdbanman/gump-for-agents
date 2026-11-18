# Forecasts of agent `model` (blast, 2026-11-18), frozen before the data

## Block M1: 03:40 UTC (machine clock)

**What I had seen when writing this.** The anchors of `BRIEF-COMMON.md`; `research/wrap/README.md` (HAZ etc.);
`research/wrap/data/runs.csv`; the card's CSVs under `research/data/gpu_local_eqtorus/` EXCEPT
`eqtorus_1_3_32.csv`, `eqtorus_1_8_32.csv`, `eqtorus_4_0_8.csv`, their `hist_*.json` and `chain3_summary.txt`
(not opened); not the "Chain 3" section of `research/gpu-local/README.md`; no other blast agent's directory;
the PI's blocks 0 and 1 in `research/blast/PREDICTIONS.md` (so these are not independent of the PI's numbers).
My own runs so far: population histograms of the 48- and 57-cell tori only.

**How the numbers were made (by hand, from the tube discounts on file).** D = (wide line 13.1623 +
0.20861 (A − 63)) − ln τ. For one loop² of 12: D = 0.091, 0.114, 0.164, 0.226, 0.302, 0.390 at 54 … 108 cells. As
a share of the death rate x = e^D − 1, ln(x/A) rises by 0.0171, 0.0167, 0.0164, 0.0153 per cell from 60 to 108
cells (72 from shape3 via the PI's 0.164), i.e. **x ≈ K·A·e^{0.016 A}**: "one more way to die, starting at any of
∝ A places, at a price 0.016 per cell below the bulk price" (a band that nucleates and sweeps: price 0.193). Loop²
13 gives the same 0.016 from 57 to 75 cells (ln(x/A) = −6.499, −6.387, −6.392, −6.345, −6.208). The PI's front gas
(x ∝ L^m, m ≈ 2–2.6) and HAZ (x ∝ e^{gA}) bracket it; I give the sweep form as centre and the others as the spread.

| face | cells | forecast ln τ_face | P(inside) | how |
|---|---:|---|---:|---|
| (1,3),(0,32), one loop² 13 | 96 | **19.810 ± 0.012** | 50% | x(75) = 0.151 scaled by (96/75)·e^{0.016·21}: D = 0.239 (front gas L²: 0.230) |
| (4,0),(0,8) and (1,8),(0,32), one loop² 16 | 96 | **19.920 ± 0.012**, the two equal within 0.008 | 50% | x(63) = 0.055 (HAZ r₁₆) scaled: D = 0.117–0.135 |
| (1,18),(0,40), one loop² 12 | 120 | **24.560 ± 0.020** | 60% | sweep 24.558, power law (m = 2.56) 24.568, HAZ-like (g = 0.025) 24.555 |
| tube of loop² 12, 240 cells | 240 | **48.0 ± 0.35** (local slope near 240 cells: 0.196 ± 0.005) | 55% | sweep 47.87, D = 0.0048 L²: 48.17, pure power law m = 2.56: 48.5, HAZ-like 47.4 |
| wide torus (no loop² < 60), A cells near 200 | ~200 | **13.1623 + 0.20861 (A − 63) − 0.02 ± 0.06** (A = 192: 40.05; 201: 41.93) | 60% | the wide line, shaded down for a bulk price slightly below 0.2086 |
| hull face, radius 17 | 135 | **29.200 ± 0.035** | 55% | between "second difference repeats" 29.230 and "wrapped price takes over" 29.163 |
| hull face, radius 19 | 165 | **35.72 ± 0.09** | 50% | repeats: 35.81; A^(−1.5) prefactor: 35.73; rim zone of range 2.3 units: 35.68; wrapped price from 135 on: 35.61 |

Qualitative, same time:
- P(the 135-cell hull face is nearer 29.230 than 29.163, once known to ± 0.03) = 55%.
- P(the hull's third second difference (84, 108, 135) is below 0.680) = 55%: I expect the excess over 3 × 0.2086 to
  start shrinking here, because the range over which a wrapped face notices its own image (loop² 19 yes, 21 no:
  2w ≈ 4.4–4.6 lattice units) puts the first hull cells that are out of reach of every rim at k ≈ 8–9.
- P(on tubes of loop² 12 the share of band-first deaths grows with length) = 80%; P(the local slope of the 12-tube
  at 240 cells is below 0.199) = 65%; below 0.190: 20%.
- P(a tangent construction from the measured population histogram (mean, variance, tail slope of ln π(n))
  reproduces ln τ of the wrapped faces of 48–84 cells to within 0.3 with one common additive constant) = 35%.
  I expect it to fail: the first two histograms give a tail slope of only 0.35–0.37 per live cell.

## Block M2: 03:41 UTC, the variance forecast (before I look at any histogram of a 66- or 84-cell face)

Seen so far in my own histograms (48, 57, 63 wide, 60 tube): a loop raises the variance per cell of the face's
population, s² = var(P)/A: 0.3877 (63, loops 21), 0.3937 (57, loops 19), 0.4045 (60, one loop 12), 0.4146 (48,
three loops 16), while ρ moves by 0.002 at most. In the tangent estimate the discount of a wrapped face would then
be D = A·(λ·f + ½λ²·δs²) with λ ≈ 0.39–0.41 the tail slope of ln π(n): it gives 0.12 (60 tube; measured 0.113),
0.12 (4 × 4; 0.108), 0.03 (57; 0.036) with nothing fitted. **If that is the mechanism, the growth of the discount
with tube length must be a growth of the variance excess.** Forecast:

- s²(66-cell tube (1,5),(0,22)) − s²(66-cell wide (1,4),(0,22)) = **0.013 ± 0.005**. P = 55%.
- s²(84-cell tube (1,12),(0,28)) − s²(84-cell wide (1,4),(0,28)) = **0.021 ± 0.005**. P = 50%.
- Dead if the excess at 84 cells is below 0.012 (the variance excess does not grow with length; the growing
  discount is then in the tail, not in the stationary fluctuations). P(dead) = 35%.

Scores of block M1 known at this time (the 96-cell faces, opened only after commit e0f4d78): loop² 13 measured
19.8109 ± 0.0062 against my 19.810 ± 0.012 (inside); loop² 16: 19.9373 ± 0.0060 for (4,0),(0,8) (outside: +0.017)
and 19.9284 ± 0.0063 for (1,8),(0,32) (inside); "equal within 0.008": difference 0.0089 ± 0.0087 (narrowly missed).
The header of block M1 says 03:40; the machine clock at its commit was 03:35.

## Block M3: 03:47 UTC, a revision of the 240-cell tube after my own stationary measurements (still before any tube beyond 108 cells is known to me)

Scores of M2 (my runs, `moments.py`): s² excess of the 66-cell tube over the 66-cell wide face 0.0164 (forecast
0.013 ± 0.005: inside); of the 84-cell tube over the 84-cell wide face 0.0203 (forecast 0.021 ± 0.005: inside; the
"dead" clause not met). **But the reasoning was half wrong:** the tube's own variance per cell does not grow with
its length (0.4024, 0.4021, 0.4022, 0.4023, 0.4023 at 78, 84, 96, 108, 120 cells); the excess grows because the
wide faces' variance per cell still falls with area (0.3877, 0.3819, 0.3784 at 63, 75, 108 cells).

New for the 240-cell tube: on tubes of loop² 12 all four cumulants per cell of the stationary population are
independent of length from 78 cells on (ρ 0.51543, κ₂ 0.4023, κ₃ −0.489, κ₄ +2.03 per cell; wide faces at 108
cells: 0.51772, 0.378, −0.30, +0.77 and still shrinking). A tube is a one-dimensional object with its own
fluctuation law per unit length, so I now expect a price per cell of its own, c − Δ with Δ = 0.007–0.011 (the
tilt series λf + λ²δκ₂/2 − λ³δκ₃/6 + λ⁴δκ₄/24 at λ = 0.41 gives 0.0009 + 0.0027 + 0.002–0.004 + 0.0015–0.0024 and
has not converged; the measured local discount is already 0.0074 per cell from 96 to 108 cells).

- Tube of loop² 12, 240 cells: **48.40 ± 0.25** (replaces 48.0 ± 0.35 of M1 as my best number; both are scored).
  Local slope from 120 to 240 cells: **0.1985 ± 0.002**. P = 55%.
- The 120-cell forecast is unchanged (24.560 ± 0.020).

## Block M4: 03:57 UTC (machine clock), after agent `anatomy`'s boom and bust and my own upper-tail measurements

What I had seen: `research/blast/anatomy/README.md` (its four sentences and the table of §2 only); my `upper.py`,
`boom.py` on the 48-cell torus and the 45- and 63-cell hull faces. Not yet: any ex5 run of a 63- or 66-cell wrapped
face; any lifetime beyond the anchors.

Reasoning. (i) The over-full tail is the same on tubes and wide faces of equal area to 0.001 per cell, so the
tube's discount is not in the boom and nothing in the boom changes my tube numbers. (ii) On wrapped faces the share
of deaths with a fall of half the face rises slowly with area (anatomy: 0.572, 0.590, 0.601 at 48, 63, 75 cells):
the route without a bust costs about 0.004–0.005 per cell more than the route with one, so the wide line should
bend down by about 0.0015 per cell as the bust route takes over (bust price ≈ 0.2069). (iii) A hull face cannot
bust (its fall map stops at 0.40–0.44 A where the torus's reaches 0.19 A), so I move a little towards "the second
difference repeats" at 135 and 165 cells.

| face | cells | forecast | P(inside) | change from M1/M3 |
|---|---:|---|---:|---|
| tube loop² 12, (1,18),(0,40) | 120 | 24.560 ± 0.020 | 60% | none |
| tube loop² 12 | 240 | 48.40 ± 0.25 | 55% | none (M3) |
| wide torus | 200 | 41.716 ± 0.05 (wide line 41.742; at A cells: 13.1623 + 0.2069 (A − 63) − ln[(1 + 0.695 e^(−0.0045 (A − 63)))/1.695]) | 55% | sharpened |
| hull face | 135 | 29.215 ± 0.030 | 55% | was 29.200 ± 0.035 |
| hull face | 165 | 35.76 ± 0.08 | 50% | was 35.72 ± 0.09 |

- The size at which the inside of a hull face busts on its own often enough to matter (half of the deaths go
  through an interior fall of half the interior): **side k = 12 ± 2 unit cells, 234 cells (range 165–340)**
  [conjectured; rests on a rim zone 1.4–1.5 lattice units wide and a coordination cost of 1–3 nats, neither
  measured]. P(the hull's local second difference is still above 0.67 at (108, 135, 165)) = 60%.
- P(the share of deaths with a half-face fall on a wide torus of 84 cells is above 0.60) = 65%; at 108 cells above
  0.62: 55%.
- P(at equal area the 66-cell tube and the 66-cell wide torus have the same over-full share of deaths five
  generations or so before death, within 0.03) = 50%. If the tube's is lower by more than 0.03 its extra deaths are
  starvation deaths; if equal, its discount sits in the kill after the bust.

## Block M5: 04:11 UTC (machine clock): the two-route formula's number for the 120-cell tube

Scores of M4's last clause (my 66-cell pair, `pair66.py`): over-full share of dying faces, tube 0.169 ± 0.007 (lag 4;
0.171 at lag 5) against wide 0.192 ± 0.008: "the same within 0.03" holds as written (−0.023 ± 0.011), but the
reading is the other branch: the numbers of over-full deaths are equal (506 and 513) and the tube's extra deaths
are deaths without a bust.

Formula (README item h): D = ln(b + (1 − b)·e^Δ), Δ = ln π_tube − ln π_wide at equal area, read at the fraction f of
the mean population, b = 1/(1 + e^(−0.364 − 0.0045 (A − 63))). The level f is one fitted number: on the four measured
pairs (66, 84, 96, 108 cells) Σ z² = 86.6, 11.4, 3.8, 24.9, 262 at f = 0.45, 0.50, 0.525, 0.55, 0.60. At 120 cells
(tube (1,18),(0,40) against wide (1,11),(0,40); 5.6 × 10⁸ and 4.1 × 10⁸ stationary samples; no death seen):
Δ(0.525) = 0.974 → D = 0.455 → **ln τ = 24.598**; Δ(0.50) = 1.032 → D = 0.490 → 24.563.

- The formula's forecast for the 120-cell tube: **24.585 ± 0.030** (P = 60%).
- My number for it moves from 24.560 ± 0.020 to **24.575 ± 0.025** (both are scored; the first was frozen in M1).
- The formula at 240 cells cannot be evaluated (my stepper counts faces of at most 127 cells); M3's 48.40 ± 0.25 stands.
