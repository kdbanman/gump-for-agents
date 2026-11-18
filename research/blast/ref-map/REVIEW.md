# REVIEW (ref-map): are the two prices two minimum actions of one measured two-layer map?

Referee `ref-map`, 2026-11-18, 04:45–05:25 UTC. Labels: **[measured]** (gump, my stepper), **[computed]** (from my
measured maps, nothing fitted). Nothing is proved. Only `ref-anatomy/THEORY.md` was read; none of its code was read or
run. Stepper, tallies and dynamic programming are mine (`gs.c`, `build_vessel.py`, `dp.py`).

## Verdict

**"The rimmed price is the Gaussian fade action of the measured two-layer map" is REFUTED as a statement about a price
per cell. The agreement 0.2313 ≈ 0.231 is an accident of one size.** 0.2313 is S/A at 63 cells; gump's 0.231 is a
slope. With each size's own map, S/A is 0.209, 0.226, 0.232 at 30, 45, 63 cells and 0.224–0.236 at 84 (by rule): it
passes through 0.231 near 63 cells. The action's increments per cell are 0.2605, 0.2477 and then 0.20–0.25, against
gump's 0.2010, 0.2119, 0.2147: 30% and 17% too high, and falling where gump's rise, so gump's negative term in k is
not reproduced (sign wrong on the three sizes where the action is pinned). The owner should not be told that the
rimmed price is the hull's Gaussian fade action.

What may be said: (1) the number S(63) = 14.6 and the 13-generation fade reproduce; (2) the torus's 0.161 per cell,
its jump-and-crash route and the +0.8 nat non-Gaussian tail of the jump at 63 cells reproduce; (3) the chain gets the
order hull > torus and the hull's ln τ to within 10% at every size (30–84: −8%, +4%, +7%, +4 to +9%), no better; (4) gump's hull
faces of 30–84 cells do die by fades and its torus faces mostly by a jump and a crash [measured, section (f)], but the
chain says so only for one choice of the layer beneath, and at 84 cells its two routes tie where gump's faces still fade.

In fairness to the claim: as a ratio the number is not confined to one size (S/A = 0.2324 at 63 cells and 0.224–0.236 at
84), and with the rule that carries most of the 84-cell map from 63 cells the last increment is 0.248 and c = 0.247. What
fails is the identification with gump's 0.231, which is a slope with a negative term in k beside it: no pair or triple of
sizes at which the action is pinned gives that pair of numbers. And [conjectured] the ratio will not stay: at 84 cells the
jump-and-crash route already ties with the fade, and on a face whose rim is a vanishing share the chain's map is the
torus's, whose jump costs 0.16 per cell. A chain with one map cannot keep two prices at large sizes unless the fade
stays cheaper for ever, and at 84 cells, in the chain, it has stopped being cheaper (gump's 84-cell faces still fade).

## Per claim

| # | claim | verdict | my numbers |
|---|---|---|---|
| 1a | torus route (33,25) → (46,42) → (16,7) → starvation, found by the chain | **CONFIRMED** (63 cells) | (33,25) → (45,43) → (16,6) → (11,6) → (6,6) → …; costs 6.01 (jump), 2.01 (crash) |
| 1b | gump's dying faces go (33.3,25.2) → (48.8,39.9) → (11.2,9.9) | **CONFIRMED** (63 cells) | aligned on the last generation with P ≥ 46 before the death: (33.3, 25.2) → (48.6, 39.7) → (12.1, 9.9), then a median of 5 generations (3–9) to the empty face. 65.4 ± 1.2% of 1,670 deaths have such a generation in their last 20 (a living face: at most 4.8%); 85.1 ± 0.9% have one with P ≥ 43 in their last 12 (living: at most 20%) |
| 1c | hull face, 63 cells: a fade of about 13 generations, no over-full generation | **CORRECTED** | true for B = the whole layer beneath at 30, 45, 63 cells (12, 12, 13 steps). With B = the part under the face the cheapest route is a jump and a crash at every size ((34,20) → (40,29) → (22,6) at 63). At 84 cells, whole layer, the jump-and-crash (46,38) → (52,49) → (27,12) ties with the fade: 18.77 against 18.78 (rule carry:50), 19.07 against 19.17 (carry:200). **Gump itself [measured]:** hull faces of 30, 45, 63 cells die by fades, a median of 9 and 10 generations (4–16, 5–17) from the last time at the living mode to the empty face at 45 and 63 cells, with no excess of over-full generations before the death at 45 cells and a small one at 63 (P ≥ 45 in the last 12: 5.9 ± 0.5% against at most 3.7% alive). So the whole-layer chain is right in kind and the under-face chain finds a route gump does not take. But in gump's fades the layer beneath stays at 19–20 of 63 while the face goes from 16 to 2; the chain's route takes it down to 12–13. At 84 cells (77 deaths) gump's faces still fade, layer beneath at 27–29 of 84 |
| 2a | minimum action 0.1608 per cell on wrapped faces | **CONFIRMED at 63 cells**; 48–108 NOT TESTED | S = 10.116 (0.1606); 10.248 (0.1627) with nearest-cell filling |
| 2b | minimum action 0.2313 per cell on the hull face (gump's rimmed price 0.231) | number **CONFIRMED** (S(63) = 14.640 ± 0.047, S/A = 0.2324); reading as a price **REFUTED** | see "the deciding test" |
| 3 | the jump's tail: measured chance below the Gaussian's by 0.76 nats at 63 cells | **CONFIRMED at 63 cells** | +0.802 ± 0.027 on the point (46,42); 3×3 +0.716; 5×5 +0.599; quadrant +1.124 ± 0.013 |
| 3' | 0.42 and 1.19 at 48 and 84 cells; +0.022–0.027 per cell; the ledger summing to 0.200–0.207 | NOT TESTED | one torus size only |

## (a) The tallies [measured]

`sh run.sh` (seeds in the file; about 10 minutes of one core). 64 bit-sliced replicas, 50% noise, 300 generations of
burn-in, a replica restarted when any face empties (or when its state repeats after 120 or 2,520 generations).
τ_face = faces × exposure / deaths.

| vessel | face cells | exposure (replica-generations) | deaths | ln τ here | anchor | var P′, var B′, cov per cell at the living mode |
|---|---:|---:|---:|---|---|---|
| hull radius 7 | 30 | 1.80·10⁷ | 163,513 | 6.780 ± 0.002 | 6.804 | 0.228, 0.304, 0.106 |
| hull radius 9 | 45 | 3.93·10⁸ | 171,299 | 9.818 ± 0.002 | 9.819 | 0.272, 0.322, 0.119 |
| hull radius 11 | 63 | 1.02·10⁹ | 9,550 | 13.659 ± 0.010 | 13.633 | 0.301, 0.328, 0.125 |
| hull radius 13 (two runs summed) | 84 | 1.15·10⁹ | 120 | 18.157 ± 0.091 | 18.141 | 0.314, 0.330, 0.125 |
| torus (1,4),(0,21) | 63 | 7.67·10⁸ | 2,922 | 13.171 ± 0.018 | 13.1622 | 0.328, 0.293, 0.097 |

(30 cells: 0.024 below the anchor; a hull of radius 7 lives 110 generations, less than my burn-in, so the protocol
shows. 63 cells: 0.026 above, as `ref-anatomy` found, 13.658.) The hull's variance of P′ per cell is not constant:
0.228, 0.272, 0.301, 0.314.

**The layer beneath on a hull.** The layer s = R − 2 inside the hull has exactly as many cells as the face
(3k(k−1)/2 under the face plus 3k beyond its three edges: 45 + 18 = 63 at radius 11) [counted: `build_vessel.py hull 11`].
d = 0: B = that whole layer (the living mode (32,28) at 63 cells is `ref-anatomy`'s starting state, so this is its
choice). d = 1: B = only the part under the face (18, 30, 45, 63 cells). **The choice matters, in kind**: see 1c. With
d = 1 the actions are 6.128, 9.709, 13.843 and about 17.3–17.4 (S/A 0.204, 0.216, 0.220, 0.207).

## (b) The chain [computed]

`python3 dp.py <tally> <d> <rule> <nmin> [source tally]`. Integer grid (P, B), P ≥ 1. From each cell a Gaussian step
with that cell's measured mean and covariance (variances floored at 0.05); the cost of a step to a grid point is
½ dᵀΣ⁻¹d; death is P′ < 0.5, cost ½(mean − 0.5)²/var; start: the mode of the living histogram; value iteration to
convergence. Exact ln τ: the Gaussian density at integer points, renormalised over the states and death, quasi-stationary
death rate by power iteration. Rules for cells the tally visits fewer than nmin times:

- `visited`: they are not states (`ref-anatomy`'s rule). Void at 84 cells: the route is cut off.
- `nearest`: copy drift and covariance of the nearest measured cell.
- `carry`: the next smaller hull's map at equal fillings (bilinear), then nearest. `carryall`: every cell carried.
- `carryabs`: the smaller hull's map at equal absolute P and equal filling of B.
- `poly2`: a quadratic fit in the fillings. Void: it invents cheap paths (S(84) = 14.9) and a chain with no lifetime.

At 30, 45 and 63 cells **S does not depend on the rule at all** (6.275, 10.182, 14.640 under visited:50, visited:200,
nearest, poly2: the route lies in cells with n ≥ 2,000 except the 63-cell end-game). Statistical error by redrawing every
cell's mean and covariance (`staterr.py`, 12 draws): ± 0.011, 0.009, 0.047; the redraws average 0.00, 0.01, 0.04 below
the point values (the minimum exploits noise), so the bias is no larger than the error.

At 84 cells S depends on the rule, because 120 deaths leave the last third of any route in cells with n < 300:

| rule at 84 cells | S | S/A | route |
|---|---|---|---|
| carry:50 | 18.766 (redraws 18.20 ± 0.32: biased low by about 0.5) | 0.2234 | jump and crash; fade only: 18.783 |
| nearest:50 / nearest:200 / visited:20 / carryabs:50 | 18.813 / 18.787 / 18.876 / 18.900 | 0.224–0.225 | jump and crash |
| carry:200 | 19.068 (redraws 18.92 ± 0.17) | 0.2270 | jump and crash; fade only: 19.174 |
| carry:1000 | 19.561 | 0.2329 | fade |
| carry:5000, fade only | 19.839 | 0.2362 | fade |
| carryall from 63 cells (`ref-anatomy`'s row: 19.441) | 19.583 | 0.2331 | fade |

So S(84) = 18.8–19.8, and I would not quote it more closely than 19.4 ± 0.4. With a third tally merged (the dump run of section
(f), 77 more deaths, 197 in all; `out/h13_three_tallies.txt`): 18.909, 19.231, 19.680 for carry:50, carry:200,
carry:1000 (fade only: 18.950, 19.321, 19.680). The thin-cell values rise by 0.12–0.16 with more data, as the redraws
said they would; the range and the tie between the two routes stay.

Carrying a map between sizes at equal fillings gives S ∝ A by construction and is wrong by as much as the effects under
discussion: the 45-cell map carried to 30 and 63 cells gives 6.825 and 14.202 (own maps: 6.275, 14.640); the 63-cell
map carried to 45 gives 10.502 (`ref-anatomy`: 10.505; own: 10.182).

## (c) The deciding test [computed]: the hull's price from differences

`python3 hullsum.py 7,9,11 …` → `out/hullsum_7_9_11.txt`; `hullsum.py 9,11,13 …` → `out/hullsum_9_11_13.txt`;
`staterr.py 200 0 h7 h9 h11` → `out/staterr_7_9_11.txt`. Fit v = a + c·A + b·k through three consecutive sides.

| | 30 | 45 | 63 | 84 | increments per cell | c, b from (30,45,63) | c, b from (45,63,84) |
|---|---|---|---|---|---|---|---|
| gump ln τ (anchors) | 6.804 | 9.819 | 13.633 | 18.141 | 0.2010, 0.2119, 0.2147 | 0.2663, −0.980 | 0.2313, −0.350 |
| minimum action S, own maps | 6.275 | 10.182 | 14.640 | 18.8–19.8 | 0.2605 ± 0.0009, 0.2477 ± 0.003, 0.197–0.248 | **0.184 ± 0.019, +1.15 ± 0.29** | −0.11 … +0.25, +6.5 … 0.0 |
| S / A | 0.2092 | 0.2263 | 0.2324 | 0.224–0.236 | | | |
| S − gump ln τ | −0.53 | +0.36 | +1.01 | +0.6 … +1.7 | | | |
| chain's exact ln τ (visited:50; carry at 84) | 6.804 | 10.190 | 14.383 | 19.10–19.29 | 0.2257, 0.2329, 0.228–0.236 | 0.269, −0.65 | 0.21–0.26, +0.33 … −0.58 |
| chain ln τ − gump | 0.00 | +0.37 | +0.75 | +0.96 … +1.14 | | | |

- **Does the action give 0.23 per cell? No.** On the three sizes where S is pinned to ± 0.05 the second difference
  gives c = 0.184 ± 0.019 where gump's own numbers on the same sizes give 0.266 (4σ, statistics only), and the linear
  term is +1.15 ± 0.29 where gump's is −0.98 (7σ). On (45, 63, 84) every value of c from −0.11 to +0.25 is available by
  choosing the rule; even the rule kindest to the claim (carry:5000: c = 0.247) gives b = +0.02, not −0.35.
- **Does it reproduce the negative linear term? No**, in the plainest form: gump's increments per cell rise with size
  (0.2010, 0.2119, 0.2147), the action's first two fall (0.2605, 0.2477), and both exceed gump's.
- **Absolute values.** The chain's exact ln τ is 0.00, +0.37, +0.75, about +1.0 above gump's at 30, 45, 63, 84 cells:
  the Gaussian is too stingy on the hull by about 0.35 per unit of side (0.02 per cell), as large as gump's rim term and
  of the opposite sign. (`ref-anatomy` has +1.14 at 63 cells, I have +0.59 to +0.83 by rule: the chain's lifetime depends
  on how the Gaussian is put on the grid, by 0.3.) Its second differences do resemble gump's (0.269 against 0.266), but
  that is nearly forced: the kernel was measured on the very faces that died, and only its Gaussian shape is a model.
  So "a many-step fade for which a Gaussian suffices" is **not supported**: the non-Gaussian part of the fade's
  one-step laws grows with size as fast as the rim term does.

## (d) The torus [computed, measured]

`python3 dp.py …/t63.tal 0 visited 50` → S = 10.116, S/A = **0.1606**; route (33,28) → (35,30) → (33,25) → (45,43) →
(16,6) → (11,6) → (6,6) → (4,7) → (3,8) → (2,10) → (1,13), costs 0.07, 0.14, 6.01, 2.01, 0.61, 0.70, 0.13, 0.09, 0.12,
0.19, 0.04. The same with visited:20; 10.248 with nearest:200; 10.626 with visited:200, where my smaller tally cuts
the end-game off (`out/torus.txt`). `ref-anatomy`: 10.052, the same route. The chain's exact ln τ is 12.34, 12.52,
12.90, 14.36 under those four rules (gump 13.17): at its own size it is not "nearly forced" to better than a nat or two.
`python3 box.py …/t63.tal`: 1.34·10⁸ steps from the box |P − 33| ≤ 1, |B − 25| ≤ 2; mean (34.17, 28.94), variances 20.83,
19.27, covariance 6.47; landing on (46,42): 1,371 times, −ln 11.491 against the Gaussian's 10.689.

## (f) How gump's faces die [measured]

`sh run.sh` (its last block: `GS_DUMP` writes the last 24 generations of (P, B) of every dying face), then
`python3 dying.py <dump> <tally> <A> <mode> <threshold>` → `out/dying.txt`.

| vessel | deaths | mean P at t−8 … t−1 | mean B (whole layer) at t−8 … t−1 | deaths with P ≥ threshold in the last 12 generations (a living face: at most) |
|---|---:|---|---|---|
| torus 63 | 1,670 | 29.2, 27.8, 25.0, 23.0, 18.1, 11.0, 4.4, 1.7 | 25.8, 25.3, 23.6, 23.4, 20.8, 17.5, 15.7, 16.5 | P ≥ 46: 62.8 ± 1.2% (2.9%) |
| hull 45 | 14,815 | 16.3, 15.0, 13.4, 11.5, 9.4, 6.5, 3.7, 1.6 | 16.2, 15.6, 14.9, 14.3, 13.7, 12.7, 12.2, 12.3 | P ≥ 32: 8.8 ± 0.2% (10.9%) |
| hull 63 | 2,479 | 21.4, 19.2, 16.1, 13.0, 9.9, 6.5, 3.6, 1.6 | 22.5, 21.8, 20.5, 19.8, 19.4, 18.9, 19.3, 19.9 | P ≥ 45: 5.9 ± 0.5% (3.7%) |
| hull 84 | 77 | 23.9, 21.4, 16.9, 13.8, 10.4, 6.4, 3.6, 1.8 | 28.6, 29.4, 26.6, 27.4, 28.5, 28.7, 29.8, 31.1 | P ≥ 57: 10.4 ± 3.5% (7.3%); P ≥ 52: 28.6 ± 5.1% (70%) |

At 84 cells gump's hull faces still fade (77 deaths: a median of 11 generations, 6–17, from the living mode to the empty
face; no significant excess of over-full generations before the death), with the layer beneath at 27–29 of 84 (alive: 37)
where the chain's fade takes it to 16–19. The chain's tie between the fade and the jump-and-crash at 84 cells is not
seen in gump.

A third of the torus's deaths at 63 cells have no generation with P ≥ 46 in their last 20 (a tenth none with P ≥ 43):
the wrapped face has a fading minority too.

## Forecasts (`PREDICTIONS.md`, commit 5d9d07c, before any analysis): 3 hits, 1 half, 1 mostly

1. S(63, hull) within 10% of 14.57: 14.640. Hit.
2. The price from differences is not 0.231 ± 0.01 and moves by > 0.02 with the rule: yes (0.2477, then 0.197–0.248);
   "the first differences disagree by > 0.02" holds for all rules but the two that carry most of the map. Mostly hit.
3. Chain ln τ above gump's at every size and growing: yes in sign and growth; my sizes (+0.5, +1.5) were too large
   (+0.37, about +1.0). Half.
4. The linear term of S does not come out near −0.34: +1.15 on (30,45,63). Hit.
5. Torus: S/A in 0.15–0.17, one over-full generation then a crash: 0.1606, (45,43) → (16,6). Hit.

## Not checked

- Dying trajectories conditioned more finely than by the last over-full generation; any trajectory of the chain itself
  (only its cheapest route) to set beside them.
- Torus sizes other than 63 cells; the tail's growth per cell; the ledger; tubes.
- A second seed of the 30-, 45-, 63-cell tallies (their dump runs were not analysed as maps). The 84-cell action rests on
  120–197 deaths and is given as a range, not a number.
- The death threshold (0.5), the variance floor (0.05) and the start (mode) were not varied.
- My two jobs overlapped at times (a tally and a short analysis), each under `nice`; the load on the machine was 6–8.
- `dp.py` has had no second reader. `poly2` and `visited` at 84 cells are reported as void, not as results.
