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

---

# Third task (05:46–06:05 UTC): does the remaining 0.057 vanish when the state includes its own next generations?

The one-step-ahead population of the face is the face population one generation later, so the "look-ahead state"
is the run of face populations (P(t), P(t+1), P(t+2), P(t+3)). Mode `ahead` of `rb.c` (binary `rba`, validated:
`RB=rba python3 val.py 1 4 21 1000 [neg]`, `… 1 12 28 1000 [neg]`) counts it over every counted generation with
P(t) ≥ 0.62·A (a future cut by the death is entered as zeros) and writes the same run for every launch.
`sh run6.sh; sh run7.sh; python3 ah.py a48 a57 a63 a75 a84 a108` → `out_ahead.txt`; tube: `python3 ah.py a48 a57 a63
atube84` → `out_ahead_tube.txt`. Fresh seeds 301–307; 73,269 / 10,425 / 4,871 / 370 / 38 / 0 deaths at 48 / 57 / 63 /
75 / 84 / 108 cells. Events are anchored at t; d = chance that t is the launch of a death given the event; I, J, F
as above, fitted on 48, 57, 63 cells; I + J + F = 0.2155 for every event (identity; these runs' lifetime slope).
Layer 2's look-ahead N₂(t+1) was not measured.

## Answer

**No static event of the living face whose rarity is the price was found; and one is unlikely to exist in
fractions of the area. But something more useful came out: the kill exponent of a face event is a constant out to
108 cells, so a face's lifetime can be read from its living state without waiting for a death.**

1. **In fractions of A the chance of death always falls with area** [measured, 48–84 cells]:

| event | I (static) | J (kill) | d at 48, 57, 63, 75, 84 cells | share of launches |
|---|---|---|---|---|
| face ≥ 0.74·A | 0.088 | 0.129 | 0.005, 0.002, 0.001, … | 0.57 |
| ≥ 0.70·A now, ≤ 0.30·A next | 0.091 | 0.122 | 0.014, 0.004, 0.002, … | 0.78 |
| ≥ 0.70·A now, ≤ 0.20·A next (the PI's event) | 0.150 ± 0.001 | 0.068 ± 0.001 | 0.100, 0.054, 0.036, 0.016, 0.006 | 0.43 |
| ≥ 0.70·A now, ≤ 0.10·A next | 0.236 ± 0.008 | 0.020 ± 0.004 | 0.52, 0.44, 0.36, 0.24 (28 events) | 0.06 → 0.03 |
| ≥ 0.70·A now, ≤ 0.10·A two generations on | 0.181 ± 0.002 | 0.036 ± 0.001 | 0.37, 0.27, 0.22, 0.14, 0.09 | 0.47 |
| ≥ 0.70·A now, ≤ 0.10·A three generations on | 0.169 ± 0.001 | 0.045 ± 0.001 | 0.31, 0.21, 0.16, 0.09, 0.06 | 0.72 |

   "Over-full now and nearly empty next" is worth about what the four fillings were worth (I = 0.150, J = 0.068
   against 0.166 + 0.057); a bust to a tenth of the face still leaves J = 0.020 and costs 0.236, more than the price.
2. **In cells it does not** [measured]: given ≥ 0.70·A now and at most k cells two generations later, d = 0.81, 0.48,
   0.24, 0.11 for k = 2, 4, 6, 8, the same at 48, 57 and 63 cells to 0.005 (J = 0.000 ± 0.002; 75 cells: 0.55 ± 0.05,
   0.25, 0.11; 84 cells: 0.24, 0.11). **The death is decided when about four cells are left (even odds), not at the
   launch and not at the bust.** But the static rate of these events is 0.270, 0.250, 0.235, 0.222: above the price,
   because a larger face takes longer to come down to a handful and the share of deaths that are this quick falls
   (dead within three generations of the launch: 17%, 13%, 11%, 8%, 5% of deaths at 48…84 cells). At three
   generations and k = 4 the static rate is 0.216 ± 0.002, the lifetime slope itself, but by cancellation of
   J = +0.005 and F = −0.006: an accident of this range of sizes. Without the lag it is the dip law already in the
   notebook: a face spends T_k = 9.09, 9.15, 8.84, 9.29, 9.58 generations at 1–4 cells per death (48…84 cells;
   k = 6: 19.9, 20.2, 20.0, 21.9, 23.5; k = 8 grows: 40, 43, 44, 49, 58). That event's rarity is the price because
   it is the death itself, seen a few generations early; it is not a state of the living face.
3. **Out of sample: the kill law is a constant, and the living state carries the rest** [measured]. With ln d and
   ln f of an event fitted linearly in A on 48, 57, 63 cells, and the event's living-state frequency measured at the
   target size:

| event | 75 cells (15.6442) | 84 cells (17.5387) | 108 cells (22.5405); no death in the run |
|---|---|---|---|
| face ≥ 0.74·A | 15.676 ± 0.037 (+0.03) | 17.568 ± 0.050 (+0.03) | 22.575 ± 0.086 (+0.03) |
| face ≥ 0.70·A | 15.702 ± 0.031 (+0.06) | 17.606 ± 0.042 (+0.07) | 22.655 ± 0.072 (+0.11) |
| ≥ 0.70·A now, ≤ 0.30·A next (frozen as forecast 12) | 15.672 ± 0.032 (+0.03) | 17.554 ± 0.043 (+0.02) | 22.526 ± 0.075 (−0.01) |
| ≥ 0.70·A now, ≤ 0.25·A next | 15.642 ± 0.035 (0.00) | 17.514 ± 0.049 (−0.02) | 22.429 ± 0.096 (−0.11) |
| ≥ 0.70·A now, ≤ 0.20·A next | 15.624 ± 0.052 (−0.02) | 17.492 ± 0.085 (−0.05) | 22.40 ± 0.31 (−0.14; 105 events) |
| ≥ 0.70·A now, ≤ 0.20·A two generations on | 15.654 ± 0.034 (+0.01) | 17.528 ± 0.049 (−0.01) | 22.488 ± 0.109 (−0.05) |
| straight line through the anchors of 48, 57, 63 | 15.76 (+0.11) | 17.70 (+0.16) | 22.88 (+0.34) |
| the same events with d held constant (purely static) | 11.8–14.0 | 12.3–15.3 | 13.6–18.6 |

   In one formula, fitted on 48–63 cells only: **ln τ(A) = −ln ν_A(face ≥ 0.74·A) + 0.1273·A − 1.37**, where ν_A is
   the fraction of generations a living face of A cells is that full (2.6·10⁻⁴ at 84 cells, 3.7·10⁻⁵ at 108: tens
   of thousands of events in two minutes where there is no death at all). It gives 15.68, 17.57, 22.58 against
   15.64, 17.54, 22.54. So over wide tori of 48–108 cells the kill costs a fixed 0.127–0.129 per cell, and the whole
   bend of the price with size (0.2158 below 63 cells, 0.2087 above) is in the living state's frequency of an
   over-full face. This is a measured kill law times a static frequency, not a derivation: J is fitted.
4. **It does not carry over to a tube, and that locates the tube's discount** [measured]. The 84-cell tube
   (1,12),(0,28), loop² 12, anchor 17.3175 (my run: 17.37 ± 0.13, 57 deaths): its face is over-full as often as the
   wide torus's (532,132 generations at ≥ 0.74·A in 2·10⁹ against 522,723), so the same formula gives 17.550 ± 0.050
   (face ≥ 0.74·A) and 17.527 ± 0.043 (≥ 0.70·A now, ≤ 0.30·A next): the wide value, 0.21–0.23 above the tube. **The
   tube's discount of 0.22 is entirely in the kill**, as boom said; the living-state estimator is blind to it.

## Not checked

- N₂(t+1) and any look-ahead of the layers beneath; events mixing the four fillings with the look-ahead.
- Why J is constant (it is fitted on three sizes, tori with loops² 16, 19, 21, and tested on three more).
- The errors hold the fit's slope error and a factor 3 on the counting error of the events; no term for curvature.
  The forecasts with the tighter events run low at 108 cells (−0.11 to −0.14), the loosest run high (+0.11, +0.15).
- Tubes other than the one above; rimmed faces (a hull face has no hump of launches at all, boom §8).


---

# Wide faces of 126–192 cells (06:42–07:00 UTC)

Plain running, four cores, 17 minutes (`sh run8.sh`; binary `rbw` = final `rb.c` with room for 192 cells and a
wall-clock stop; `python3 ah.py a48 a57 a63 a75 a84 a108 a126 a144 a192` → `out_wide_frozen.txt`, and the same with
`a48L`, `a63L` in place of `a48`, `a63` → `out_wide_refit.txt`). Vessels: (6,0),(0,7), 126 cells, loops² 36, 43, 49;
(4,4),(0,12), 144 cells, loops² 48, 48, 48 (my choice: the equilateral one); (8,0),(0,8), 192 cells, loops² 64 ×3.
Validated against the oracle on all three (200 generations each in a box of side 64, 0 mismatches; the swapped
neighbour fails at 192 cells: `RB=rbw HB=64 python3 val.py 6 0 7 200`, `… 4 4 12 200`, `… 8 0 8 200 [neg]`).
Exposure 5.92e+09, 1.80e+10, 1.41e+10 face-generations; deaths 0, 0, 0; periodic restarts 0, 0, 0.

[measured] The estimator ln τ = −ln ν_A(face ≥ 0.74·A) + 0.1273·A − 1.37 (kill law frozen from 48, 57, 63 cells):

| size | generations with face ≥ 0.74·A | estimator, frozen kill law | kill law refitted (below) | wide-face line | other |
|---|---:|---|---|---|---|
| 126 | 51,301 | 26.324 ± 0.113 (fit 0.112, frequency 0.013) | 26.329 ± 0.042 | 26.305 | card's 6×7: 26.4045 ± 0.1043 |
| 144 | 37,022 | 30.055 ± 0.139 (fit 0.138, frequency 0.016) | 30.062 ± 0.051 | 30.060 | |
| 192 | 608 | 40.030 ± 0.242 (fit 0.209, frequency 0.122) | 40.043 ± 0.142 (fit 0.073, frequency 0.122) | 40.073 | dice chain: 40.49 ± 0.20 |

The frozen kill law's fit error grows to 0.21 at 192 cells, so one core spent the 17 minutes on the fit sizes:
63 cells, 59,405 deaths, and 48 cells, 1,117,473 deaths. The refit gives ln τ = −ln ν + 0.1275·A − 1.387
(J = 0.1283 ± 0.0004 against 0.1286 ± 0.0010): the same law, three times sharper; it gives 15.676, 17.569, 22.578 at 75,
84, 108 cells (anchors 15.6442, 17.5387, 22.5405: +0.03 each).

**The living state says the wide price holds at 0.2087 out to 192 cells**: the estimator is +0.02, 0.00, −0.03 from
the line at 126, 144, 192 cells (slope from 126 to 192: 0.2078 ± 0.0022); it neither bends further nor rises to the
dice chain's 40.49 (0.45 apart, 1.8 of the combined errors).

What the errors do not hold: the choice of threshold. With the same procedure the neighbouring thresholds give,
relative to the line at 126 / 144 / 192 cells (refit): face ≥ 0.66·A: +0.20, +0.23, +0.29; ≥ 0.70·A: +0.13, +0.14,
+0.15; ≥ 0.72·A: +0.07, +0.06, +0.02; ≥ 0.74·A: +0.02, 0.00, −0.03; ≥ 0.76·A: +0.01, −0.04, −0.05 (27 events at 192);
"≥ 0.70·A now, ≤ 0.30·A next": −0.06, −0.12, −0.34 ± 0.19. The kill law of an event away from the launch point
(0.738) is not exactly exponential in A, and the drift is one-signed for each event; thresholds from 0.72 to 0.76,
around the launch point, agree to 0.07. A systematic of about ± 0.1 at 192 cells is the honest addition.

Not checked: the long 48-cell run's own lifetime is 9.9408 ± 0.0009, 0.016 above the anchor and above my four
shorter 48-cell runs (9.925–9.928); [conjectured] replicas caught in cycles whose period does not divide 840 add
exposure in a long run (825 periodic restarts were caught). The estimator does not use the fit runs' exposure, only
d and f, and the refitted J agrees with the frozen one, but nobody should quote 9.9408.
