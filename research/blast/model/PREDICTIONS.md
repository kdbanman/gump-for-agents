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
