# Forecasts (thin line), committed before the runs that test them

Append-only. Each block says what was known when it was written. Scores are added below each forecast after the
run, misses included. Sizes: b = sites round the ring of the torus (1,1),(0,b); face area A = 3b cells.
ln tau is per face (hazard among living lives older than T0 = 256).

## Block 1 (2026-11-14, before any lifetime run of this line)

Known: the census values ln tau = 8.6426(20), 10.0201(29), 11.3481(40) at b = 16, 20, 24 (research/shape2);
`ring.c` validated cell by cell against the reference stepper and the oracle (`run.py validate`), a timing run,
and one 3,000-generation dump at b = 24 used only for the density by layer (0.444 face, 0.397 layers 2-5).
No lifetime or model number of this line has been looked at.

**F1 (reproduction).** `ring.c` (deterministic, m = 8) gives ln tau within 3 sigma (errors combined) of the
census at b = 16, 20, 24.

**F2 (the slope keeps falling).** The two census increments are 1.3775 (b 16 -> 20) and 1.3280 (20 -> 24). Two
forms fitted exactly through the three points: ln tau = a + g b + c ln b gives g = 0.2767 per site, c = 1.213;
ln tau = a + g b + c / b gives g = 0.3073, c = -11.9. Forecast: the deterministic values lie between the two
forms, widened by 0.02:

| b | A | log form | 1/b form | forecast interval | "slope stays 0.333 per site" (alternative, forecast to fail from b = 32) |
|---|---|---|---|---|---|
| 28 | 84 | 12.642 | 12.648 | 12.62 - 12.67 | 12.680 |
| 32 | 96 | 13.911 | 13.930 | 13.89 - 13.95 | 14.012 |
| 36 | 108 | 15.160 | 15.200 | 15.14 - 15.22 | 15.344 |
| 40 | 120 | 16.395 | 16.462 | 16.37 - 16.48 | 16.676 |
| 48 | 144 | 18.83 | 18.97 | 18.81 - 18.99 | 19.34 |

Cost per cell between b = 40 and 48: 0.1015 - 0.1045 (it was 0.1148 at 16 -> 20 and 0.1107 at 20 -> 24).
Asymptotic cost per cell (a guess, not a fit): 0.097 +- 0.008.

**F3 (is noise enough on the thin torus).** Model = the rule on the top w layers over two layers of coins of
density 102/256, one face. Forecast for (model - deterministic) in ln tau, at b = 16 and b = 24, by analogy
with the wide faces (exponent.md section 5):

| w | forecast |
|---|---|
| 1 | between -1.5 and -0.3 (too weak) |
| 2 | between +0.3 and +1.2 (too tough) |
| 3 | between +0.05 and +0.30 |
| 4 | within +-0.08 |
| 5, 6 | within +-0.03 |

**F4 (the coin density hardly matters at depth).** w = 5, b = 20: coin densities 0.30 and 0.55 give ln tau
within 0.05 of the value at 0.398.

**F5 (static formulation).** E(l) = probability that l given consecutive sites of the face are empty
(site s = {Z_s, Y_s, X_{s+1}}, three cells contiguous along the axis), measured on a living deterministic ring
of b = 64; k(l) = -ln[E(l+1)/E(l)].
(a) k(l) decreases with l, and its mean over l = 30..40 is within 0.02 of the lifetime slope per site between
b = 32 and b = 48.
(b) ln tau(b) + ln E(b - s) is constant within +-0.10 over b = 16..48 for one shift s between 0 and 6 sites.

## Block 2 (2026-11-14, before any run with a wall, and before the b = 64 window run)

Known now (not yet scored above): deterministic rings 8.647, 10.020, 11.345, 12.648, 13.927 at b = 16…32
(local slopes per site 0.343, 0.331, 0.326, 0.320: still falling); models at b = 16: w = 1…6 give +1.29, +1.38,
+0.49, +0.049, +0.006, +0.012 against the deterministic ring; one-layer model at b = 24: 13.21 (slope 0.410 per
site against 0.337). Looking back from a death the face population falls by 2.2–2.5 cells per generation for more
than twelve generations: the thin face dies by an island shrinking from both ends, not in a flash. Windows on the
b = 24 ring: k(l) falls to 0.416 at l = 10 and then rises (the ring is too short).

Reading (conjecture): ln tau = g·b + (power of b); the power comes from where and how the gap starts. A face with
a wall across it (cells of 3 sites held dead: a segment of n = b − 3 sites with free ends) needs no nucleation: both
gaps are there from the start.

**F6 (segments of the deterministic thin face).** ln tau_seg(n), n = 13, 21, 29, 37 (b = 16, 24, 32, 40, wall 3):
the three local slopes agree within ±0.012 per site (no drift like the ring's), and their value lies in
0.28–0.32 per site (0.093–0.107 per cell). The ring's local slope keeps falling towards the same value.

**F7 (one-layer model, segments).** For the one-layer model on coins, the local slope of ln tau_seg(n) between
n = 6 and n = 8 is within 3% of the slope between n = 16 and n = 24. (If so, the exact solution of segments of
≤ 8 sites gives the model's asymptotic cost; if not, it does not.)

**F5 stands as committed** (windows on the b = 64 ring); added before that run: (c) on the b = 64 ring the
minimum of k(l) over l ≤ 40 is below 0.33 per site.

## Block 3 (2026-11-14, before any run on a wider torus)

Known: `ringk.c` steps the tori (1,k),(0,b) (validated against the reference stepper and the engine; no lifetime
run yet). Census values for (1,2),(0,b) (shortest loop squared 7): 9.8122(20), 12.1133(31), 14.3592(116) at
b = 16, 20, 24; cost per cell 0.1918 then 0.1872.

**F8 (the next torus, loop squared 7).**
(a) `ringk.c` reproduces the three census values within 3 sigma (errors combined).
(b) It dies the same way: the lag at which half the face population is gone, looking back from a death, grows
    in proportion to b: lag(b = 24) / lag(b = 16) between 1.35 and 1.65.
(c) The local cost per cell keeps falling: ln tau at b = 28 (A = 84) between 16.50 and 16.61
    (cost per cell from A = 72 between 0.1785 and 0.1875).

## Block 4 (2026-11-14 21:30, before looking at any simulated one-layer segment)

Known now: deterministic segments 6.8102(10), 9.1708(15), 11.5509(33) at n = 13, 21, 29: slopes 0.2951(2) and
0.2975(5) per site, nearly straight (F6 on track). Exact one-layer segments (`sweep.py seq`): ln tau =
2.4531, 2.7560, 3.7164, 4.1927, 4.6461, 5.1074 at n = 2…7, steps 0.303, 0.960, 0.476, 0.453, 0.461. The one-layer
*ring* has slope 0.410 per site between b = 16 and 24, and in the deterministic system the segment's slope is
0.875 of the ring's at those sizes. So the exact steps near 0.46 cannot be the asymptote.

**F9 (replaces the expectation behind F7, which I now expect to fail).** One-layer model, segments: the slope of
ln tau_seg(n) between n = 16 and n = 24 lies in 0.355–0.395 per site, and the steps at n ≤ 8 exceed it by more
than 15%: exact enumeration to 8 sites does not reach the straight part of the law.

**F10 (deterministic segments, small n).** The local slope between n = 5 and n = 9 exceeds 0.32 per site (the
straight part, 0.295–0.30, is reached only above n ≈ 10).

## Correction to "Known" in Block 4 (2026-11-14 21:55, found after F9 and F10 were written)

The value 6.8102(10) for the deterministic segment of 13 sites was wrong: one of sixteen lanes had stopped dying
(a periodic state of the whole slab whose period does not divide 840, so the snapshot test of that binary did not
see it) and sat there for 3.6 × 10⁷ generations. Without it: 6.7262(14) (README, "Subtle points"). The slopes
quoted in Block 4 become 0.3056(2) (13 → 21) and 0.2978(4) (21 → 29): the segment law is *not* straight at
these sizes, its slope still falls, about half as fast as the ring's. F9 and F10 stand as written.

## Scores, first part (2026-11-14 21:55; F5, F6, F8, F10 are scored further down when their runs are in)

Commands: `python3 analyze.py life 'det_b*'`, `… 'mod_b16_w*'`, `… 'mod_b24_w*'`, `… 'mod_b20_w*'`,
`… 'seg_m1_n*'`, `python3 sweep.py seq`.

**F1: hit.** 8.6470(16), 10.0199(36), 11.3447(63) against the census 8.6426(20), 10.0201(29), 11.3481(40):
+1.7σ, −0.0σ, −0.5σ.

**F2: hit where tested (b = 28, 32, 36); b = 40 and 48 not run.** 12.6482(83) in 12.62–12.67; 13.9233(139) in
13.89–13.95; 15.1644(204) in 15.14–15.22. The alternative "slope stays 0.333 per site" is 6σ away at b = 32 and
9σ at b = 36. The cost per cell between b = 40 and 48 was not measured (a ring of b = 48 lives e^19 generations).

**F3: miss for w = 1, 2, 3; half hit for w = 4; hit for w = 5, 6.** Model minus deterministic ring:

| w | forecast | b = 16 | b = 24 | |
|---|---|---|---|---|
| 1 | −1.5 … −0.3 | +1.286(3) | +1.868(13) | **miss, wrong sign**: one layer over coins is tougher, not weaker |
| 2 | +0.3 … +1.2 | +1.382(4) | +2.258(20) | miss (too small a forecast) |
| 3 | +0.05 … +0.30 | +0.495(3) | +0.845(13) | miss |
| 4 | ±0.08 | +0.049(3) | +0.115(12) | hit at b = 16, miss at b = 24 |
| 5 | ±0.03 | +0.006(3) | +0.003(12) | hit |
| 6 | ±0.03 | +0.012(3) | +0.027(10) | hit (at the edge at b = 24) |

What I had wrong: the analogy with the wide faces. On the thin torus the shallow models are all too tough and the
excess grows with b (it is a slope error, not an offset): the layers beneath a thin face do more to kill it than
coins do.

**F4: hit at density 0.55 (+0.030 ± 0.007), miss at 0.30 (−0.069 ± 0.008).** Five layers do not screen a
change of the coins by a quarter of their density; the measured dependence is about 0.5 in ln tau per unit of
density.

**F7: miss, as expected by the time F9 was written.** One-layer segments: slope between n = 6 and 8
0.4496(3) per site; between n = 16 and 24 0.3690(7): 22% apart, not 3%.

**F9: hit.** Slope between n = 16 and 24: 0.3690(7), inside 0.355–0.395. Exact steps at n = 4 … 8: 0.960,
0.476, 0.453, 0.461, 0.437 (the last from simulation), all more than 15% above it. (The very first step, n = 2 → 3,
is 0.303 and below it; the forecast's wording "the steps at n ≤ 8" should have said "from n = 4".)
