# research/gpu-local: forecasts committed before the results

Append-only: corrections go in new dated blocks. Header times from `date -u`.

## 1. The guard on the queued runs, and the hull face at A = 108 (2026-11-15T04:18Z, HEAD 8d465b2)

Written before any measurement run on this card (only checks, guard tests and a throughput benchmark have run). The
forecasts for the equilateral tori are the lead's, in `research/constant/PREDICTIONS.md` part C and its addendum; I add
none of my own for ln τ there, only for what the guard will see.

**Kind-5 lives (cycles the kernel does not recognise, period > 128).**
- Equilateral tori, A = 81 to 111, 8 layers: detected settling of any kind was 0 in every slab run of A ≥ 90 on file
  and falls steeply with size below that (`research/gpu/README.md` "Zombie lives"). Forecast: **no kind-5 life** in
  the A = 93 run (3 × 10⁴ face deaths), probability 80%; if any appear, fewer than 5, carrying < 10⁻⁴ of the
  exposure. Same for A = 108 and 111. At A = 81 and 84 (10⁵ deaths each): 0 to 3 kind-5 lives, 70% on zero.
- Hull octahedron R = 15 (A = 108), 10⁴ deaths: no kind-5 life, probability 85%. The alternative I cannot exclude
  from the data on file: the earlier run (1,059 deaths, under one mean life long) has no age bound on zombies at all.

**ln τ_face of the asymmetric hull face at A = 108** (R = 15, soup 0.35, T0 = 200, τ_face = 8 × exposure / deaths,
guard on with thresholds 16 · 2^j). On file: 23.376 ± 0.031 (1,059 deaths, one run). A smoothness reading of the
local slopes (0.2119, 0.2146 for 45→63→84, then 0.2181 ± 0.0013) puts the slope 84→108 at 0.2173 to 0.2181, that is
ln τ at 23.36 to 23.38.
- Forecast: **23.37 ± 0.03** for the new run on its own (planned statistical error ± 0.010). I expect the new value
  inside 23.31 to 23.44 with 95%.
- If it lands below 23.31: the old run was a high draw or carried unrecognised cycles (then kind-5 lives should be
  seen here, see above). Above 23.44: a high draw now, or the hazard is not flat at ages the old run did not reach
  (it reached ≤ 6 × 10⁸; this run will pass 10¹⁰): check the hazard by age before believing either.
- Probability that the new value is lower than the old by more than 0.031: 20%.

## 2. Three more equilateral tori on this card: A = 57, 63 and the 5 × 5 anchor (2026-11-15T05:46Z, HEAD 39f165f)

Written after the A = 93 result (19.4141 ± 0.0053, in the data directory at this commit) and the 4 × 4 calibration
(9.9251 ± 0.0004), before any run of these three. They are my additions to the queue: with them the whole family of
`research/constant/PREDICTIONS.md` part C comes from one driver and one counting rule. The lead's forecasts for
A = 57 and 63 are there (flat 11.842 and 13.115, massive 11.855 and 13.128, rising 11.828 to 11.835 and 13.100 to
13.107, all anchored on a 4 × 4 value that I now measure 0.007 lower).

- **5 × 5 (A = 75):** on file 15.6614 ± 0.0026 (143,857 deaths, several sources). Mean life 3 × 10⁶, so the
  16-generation rule bias of `rep.c` is below 10⁻⁵ there. Forecast: within 2σ of the file, 15.656 to 15.667.
- **A = 57 and 63:** A = 93 came out below every reading and nearest the massive one (a slope that falls with
  size). Taking that sign and the lower 4 × 4 anchor: **11.848 ± 0.008** and **13.124 ± 0.008**; both above the
  chord between my 4 × 4 and the 5 × 5 value (chord: 11.837 and 13.112 with 15.661 at A = 75). If both come out on or
  below the chord, the falling slope seen at 75 → 93 does not start below A = 75.
- Launch caps 2,048, 8,192 and 65,536 generations (3% or less of the mean life in each case).

## 3. A = 81, 84, 108, 111: one slope from A = 63 up (2026-11-15T06:13Z, HEAD dcb61c8)

Written with A = 48, 57, 63, 75, 93 measured on this card (9.9251, 11.8756 ± 0.0006, 13.1622 ± 0.0007,
15.6630 ± 0.0023, 19.4141 ± 0.0053) and before any row exists for A = 81, 84, 108 or 111 (the first A = 81 run
started a minute ago; `research/data/gpu_local_eqtorus/` holds no file for these four at this commit).

Outcome of block 2 first: 5 × 5 as forecast (file 15.6614). **A = 57 and 63 came out 0.028 and 0.038 above my
forecasts** (11.848, 13.124), 3 to 5 of my stated errors, and 0.021 and 0.034 above the highest of the lead's
readings (massive: 11.855, 13.128). I was wrong by the same mechanism as those readings: all of them hang on the
4 × 4 anchor.

What the five points show: local slopes 0.2167 (48 → 57), 0.2144 (57 → 63), **0.2084 (63 → 75), 0.2084 (75 → 93)**.
ln τ − 0.2088·A = −0.097, −0.026, +0.008, +0.003, −0.004. So the small tori are low (4 × 4 by 0.1) and from A = 63
the family is straight within ± 0.006.

**Forecast (conjecture): ln τ_face = 13.1622 + 0.2084·(A − 63) from A = 63 up**, slope uncertain by ± 0.0003:

| A | lattice | forecast | the lead's flat / massive |
|---:|---|---:|---|
| 81 | (3,3),(0,9) | 16.913 ± 0.006 | 16.933 / 16.923 |
| 84 | (2,4),(0,14) | 17.539 ± 0.007 | 17.570 / 17.552 |
| 108 | (6,0),(0,6) | 22.540 ± 0.014 | 22.661 / 22.568 (the file's 592 deaths) |
| 111 | (1,10),(0,37) | 23.165 ± 0.015 | 23.298 / 23.194 |

- Refuted if any of the four misses by more than 3 of its combined errors, or if the slope 93 → 111 differs from
  0.2084 by more than 0.002.
- What could break it without the slope being wrong: these tori are equilateral in the metric but their loops run in
  different lattice directions (4 × 4, 5 × 5, 6 × 6 are aligned with the cube axes; 19, 21, 27, 28, 31, 37 are
  rotated), and they differ in whether a firewall can form (none at 57, 63, 93, 111). If direction or the firewall
  channel matters at the 0.01 level, the four will scatter about the line by that much, not follow it.

## 4. Block 3 scored; corrections to block 1; the hull face at A = 108 again (2026-11-15T11:45Z, HEAD fe6f5ff)

Written after the rows for A = 81, 84, 108, 111 (in the data directory with this commit) and before any hull run at
R = 15 on this card (a 5-minute calibration at R = 11 is running; no R = 15 row or json exists).

**Block 3, scored** (`python research/gpu-local/eq_analyze.py A K B`):

| A | forecast | measured | measured − forecast | in combined errors |
|---:|---:|---:|---:|---:|
| 81 | 16.913 ± 0.006 | 16.9222 ± 0.0031 | +0.009 | 1.4 |
| 84 | 17.539 ± 0.007 | 17.5467 ± 0.0031 | +0.008 | 1.0 |
| 108 | 22.540 ± 0.014 | 22.5600 ± 0.0222 | +0.020 | 0.8 |
| 111 | 23.165 ± 0.015 | 23.2032 ± 0.0231 | +0.038 | 1.4 |

- First criterion (no miss beyond 3 combined errors): met. Second (slope 93 → 111 within 0.002 of 0.2084): the
  slope is 0.2105 ± 0.0013, off by 0.0021. **By its letter the block fails its second criterion**, by 0.0001. The
  criterion was badly set: its margin is 1.5 times the statistical error that slope was always going to have, so
  it could fail by chance one time in eight with the line exactly right. I should have stated it in errors.
- What the four say beyond the letter: all four are above the line, by 0.8 to 1.4 of my errors each. Against the
  line with the errors of its own fit (the review's ± 0.002 and ± 0.003 at 81 and 84,
  `research/audit/REVIEW-gpu-local-tori.md` section 3), A = 81 is 2.5 and A = 84 is 1.8 errors high. The slope I
  forecast with was low by about 0.0003: one line through all seven tori from A = 63 has slope 0.20867 ± 0.00009
  and χ² 7.8 on 5 (`research/gpu-local/eq_fit.py`).
- The same review committed forecasts by form (720ee7e, before these rows): the line 16.913, every smooth
  correction 16.927 at A = 81. Measured 16.9222 ± 0.0031 lies between them, 3.0 statistical errors above the first
  and 1.5 below the second.

**Corrections to block 1** (from `research/audit/REVIEW-gpu-local-pr23.md` section 6; block 1 stays as written):
- Its premise "detected settling was 0 in every slab run of A ≥ 90 on file" is false: fwslab 3 × 10 × 8 (A = 90)
  has 21 settled lives and 4 × 9 × 8 (A = 108) has 3. Outcome of that forecast so far: no kind-5 life in any torus
  run here (A = 48 to 111, 13.0 million face deaths), and 2 lives settled by the kernel at A = 81 and 1 at A = 84.
- The hull forecast 23.37 ± 0.03 is centred on the value it re-measures: its slope 0.2181 is computed from the old
  A = 108 run itself. It is a test of whether the old run repeats, not an out-of-sample forecast.

**Out-of-sample readings for the hull face at A = 108**, from the hull values at A ≤ 84 on file (9.820, 13.635 ±
0.001, 18.141 ± 0.005 at A = 45, 63, 84; faces of edge k = 5, 6, 7 with A = 3k(k+1)/2, so the next is k = 8) and the
torus line. They are written as second differences in k, because a term proportional to the rim (to k) drops out
of those, and the area's second difference is 3 cells:

| reading | second difference 63, 84, 108 | ln τ_face at A = 108 |
|---|---:|---:|
| (c) one price per cell, the tori's 0.2087, plus any term linear in the rim | 3 × 0.2087 = 0.626 | **23.273 ± 0.010** |
| (d) the second difference of 45, 63, 84 repeats (0.691; a price of 0.230 per cell with a rim term) | 0.691 | **23.338 ± 0.012** |
| (b) the local slope keeps rising by the same step (0.2119, 0.2146, then 0.2173) | 0.709 | 23.356 ± 0.015 |
| the old run (1,059 deaths) | 0.729 ± 0.033 | 23.376 ± 0.031 |

- (c) already fails on file at the step before (0.691 against 0.626, errors about 0.006) unless the 45-cell face
  carries a small-size deficit of 0.065, which the tori make plausible (their deficit is 0.11 at 48 cells and gone
  by 63). So (c) is "one price, rim linear, no deficit left at 63 cells". The old run is 3.1 of its errors above it.
- Planned error of the new run ± 0.010, so it separates (c) from the rest by 6 or more errors and (d) from the old
  value by 3. **My forecast: 23.35 ± 0.02** (between (d) and the old value); (c) 3%; above 23.40, 5%.
- The run: `hullface.py run 15 420 SEED`, seeds 15001 and 15002, 1,280 replicas at 2.7 × 10⁵ generations per second
  each, so every lane reaches age 6.8 × 10⁹ (3.9 first-death means; the old run stopped at 6 × 10⁸). Guard on.
  Kind-5 forecast unchanged (none, 85%). If any appear, both exposure conventions are reported.
