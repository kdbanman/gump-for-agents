# ref-boom, second task: is the wrapped price the static rarity of the four-layer over-full state?

Agent `ref-boom`, 2026-11-18, 05:20–05:45 UTC. Labels: **[measured]**, **[proved]**, **[conjectured]**.
Stepper: `rb.c`, mode `static` (binary `rbs`; validated against the oracle on the 84- and 108-cell tori too:
`RB=rbs python3 val.py 1 4 28 1000 [neg]`, `RB=rbs python3 val.py 6 0 6 1000 [neg]`; its counts in `run` mode are
byte for byte those of the first build). Runs: `sh run5.sh` (one core, plain running, fresh seeds 201–206).
Analysis: `python3 st.py s48 s57 s63 s75 s84 s108` → `out_static.txt`.

## Answer

**No, not as it stands: at the launch state three quarters of the price is static and one quarter is still in the
kill.** [measured; fits on 48, 57, 63 cells] Take the box B₀ = {face ≥ 0.738, layer 2 ≥ 0.637, layer 3 ≥ 0.562, layer 4 ≥ 0.504}
(the mean launch profile). Its living-state frequency falls with area at **I₄ = 0.166 ± 0.003 per cell**; the chance
that a generation in it is the launch of a death is d₄ = 0.273 (48 cells), 0.162 (57), 0.117 (63), 0.061 (75), so
**J₄ = 0.057 ± 0.003 per cell**, against J = 0.136 for the face alone. I₄ + J₄ + F = 0.2174, the lifetime slope of these
runs (F = −0.005 is the change of the share of launches inside the box; the sum is an identity). d₄ is not
size-independent in any box that plain running can populate at 75 cells or more.

d₄ does rise towards 1 as the box tightens, and its size-dependence fades, but the static cost then exceeds the price:

| box: every layer ≥ launch profile − δ | δ = +0.10 | +0.08 | +0.06 | +0.04 | +0.02 | 0 | −0.02 | −0.04 | −0.06 |
|---|---|---|---|---|---|---|---|---|---|
| d₄, 48 cells | 0.0038 | 0.0088 | 0.0215 | 0.054 | 0.130 | 0.273 | 0.468 | 0.68 | 0.85 (31 events) |
| d₄, 63 cells | 0.0003 | 0.0009 | 0.0031 | 0.011 | 0.038 | 0.117 | 0.280 | 0.45 (25 events) | – |
| share of launches in the box, 63 cells | 0.84 | 0.73 | 0.57 | 0.37 | 0.19 | 0.063 | 0.014 | 0.0015 | – |
| d₄, 57 cells | 0.0008 | 0.0023 | 0.0068 | 0.021 | 0.062 | 0.162 | 0.340 | 0.64 (30 events) | – |
| d₄, 75 cells | 0.00004 | 0.0002 | 0.0007 | 0.0031 | 0.015 | 0.061 | 0.23 (25 events) | – | – |
| I₄ (static rate; 48, 57, 63) | 0.044 | 0.061 | 0.081 | 0.105 | 0.133 | 0.166 ± 0.003 | 0.199 ± 0.010 | 0.24 ± 0.04 | – |
| J₄ (kill; 48, 57, 63) | 0.168 | 0.150 | 0.128 | 0.106 | 0.081 | 0.057 ± 0.003 | 0.035 ± 0.006 | 0.02 ± 0.02 | – |

(ln P by multilinear interpolation over the integer thresholds; errors of I₄ assume the events are correlated over
3 generations, not measured.) J₄ falls by 0.012 for every 0.01 the box is tightened and would reach zero near
δ = −0.05, the profile (0.79, 0.69, 0.61, 0.55), where I₄ ≈ 0.25. **So the state from which death is nearly certain
costs about 0.23–0.25 per cell, more than the price (0.218 for 48–63 cells). The face does not go there: it launches
from a shallower state that costs 0.166 and takes a chance e^(−0.057·A) on the kill.** [measured for δ ≥ −0.04;
the 0.25 is an extrapolation] The launch profile is the minimum of I₄ + J₄, as it must be; what is new is that at
that minimum the split is 0.166 + 0.057 instead of 0.079 + 0.136: the four fillings move 0.08 per cell from "the
kill" into "the rarity of the state", and 0.057 per cell is still not in them (the arrangement within the layers,
or layers 5 and below).

The launch profile itself does not move with size: mean fillings (0.738, 0.637, 0.562, 0.505) at 48 cells,
(0.739, 0.636, 0.560, 0.504) at 63, (0.739, 0.635, 0.559, 0.504) at 75; s.d. (0.064, 0.065, 0.074, 0.083),
(0.056, 0.055, 0.064, 0.071), (0.053, 0.053, 0.057, 0.068).

## Out-of-sample forecasts (procedure frozen in PREDICTIONS.md before the static runs were analysed)

ln τ(A′) = −ln P_A′(B) − ln d₄(B) + ln f(B): P measured at A′ by plain running (no death needed), d₄ and f
extrapolated linearly in A from the fit sizes.

| size | box (pre-registered rule) | living events in the box | forecast ln τ | anchor | miss |
|---|---|---:|---|---|---|
| 75 cells | δ = 0 | 492 | 15.53 ± 0.16 | 15.6442 (my run here: 15.686 ± 0.047) | −0.12 |
| 84 cells | δ = +0.02 | 2,041 | 17.33 ± 0.10 | 17.5387 (my run here, 87 deaths: 17.36 ± 0.11) | −0.21 |
| 108 cells | δ = +0.04 | 2,165 | 22.13 ± 0.11 | 22.5405 (no death in my run) | −0.41 |

(Fit sizes 48, 57, 63. Rule: among boxes with at least 200 living events at the target size, the one with the
smallest |J₄|. The δ = 0 box at 84 cells has 125 events and gives 17.37 ± 0.30; the
δ = +0.02 box at 108 cells has 100 events and gives 22.19 ± 0.33. The quoted errors hold no term for curvature.) Looser boxes forecast lower and
worse: at 75 cells 15.53, 15.46, 15.31, 15.11, 14.89, 14.68 for δ = 0, 0.02, …, 0.10 (ln d₄ of a loose box is not
linear in A: as the face grows the living states of a loose box pile up at its cheap, less lethal corner, and d₄
falls faster than the fitted exponential; at 75 cells and δ = 0.04, d₄ is 0.0031 where the fit says 0.0046).
All three forecasts are low, by 0.12, 0.21, 0.41: 0.7, 2.1 and 3.7 of their quoted errors.

**A purely static forecast (d₄ and f held at their 48–63 values) fails**: 14.33 at 75 cells against 15.64, 14.70 at
84 cells against 17.54, 16.06 at 108 cells against 22.54. The
forecast that works carries the fitted law d₄ ∝ e^(−0.057·A), i.e. it is "static rarity × a measured kill law", and
its error grows with the distance from the fit sizes. The larger the face, the looser the box that plain running
can populate, and the more of the price sits in the extrapolated kill.

## One generation earlier [measured]

The four populations at launch − 1 are shifted from the living state by +0.09, −0.47, −0.69, −0.52 living s.d.
(63 cells; Mahalanobis distance 0.72, 0.82, 0.92 at 48, 63, 75 cells). The best statistic of the four fillings (a
Gaussian likelihood ratio, quadratic) puts 49–56% of the deaths in its top 10% of living states, 6.6–10% in its top
1%, 0.7% in its top 0.1%: a lift of 5 to 7 (10 ± 3 at 75 cells with 462 deaths), "a factor of a few". As a static
cost the launch − 1 state is worth D²/2A = 0.0053, 0.0054, 0.0057 per cell: 2.5% of the price. At the launch itself
the same four numbers put 84%, 95%, 96% of the deaths in the top 0.1% of living states. **The price is paid in one
generation, between a state that is 0.005 per cell from ordinary and one that is 0.166 per cell from ordinary**; no
statistic of the four fillings one generation earlier carries it. What makes four layers fill at once from a nearly
ordinary state must be in the arrangement, not in the counts. [conjectured]

## Not checked

- Layers 5–8, the other face, any spatial statistic; whether the remaining J₄ = 0.057 is in them.
- Boxes of other shapes (a half-space along the best linear direction would have more events than a corner).
- The errors of I₄ (temporal correlation of box events assumed, not measured); fits use 2–3 sizes.
- The 0.25 for "certain death" is an extrapolation of J₄(δ) to zero.
