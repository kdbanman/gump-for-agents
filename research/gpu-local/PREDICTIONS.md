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

## 5. Block 4 scored (the hull face at A = 108); forecasts for the tube and wrapped faces, three thicker slabs and a longer 6 × 6 (2026-11-16T02:09Z, HEAD 16271f3)

Written after the two hull rows at R = 15 (in the data directory with this commit) and before any row of the faces
forecast below (no csv or json of them exists).

**Block 4, scored** (`python research/gpu-local/hullface.py summary 15`): **ln τ_face = 23.3392 ± 0.0099** at A = 108
(10,187 deaths, two seeds, χ² 0.09 on 1; no life settled, no kind-5 life, so the kind-5 forecast "none, 85%" held).

| reading of block 4 | its value at A = 108 | measured − reading | in combined errors |
|---|---:|---:|---:|
| (c) one price 0.2087 per cell plus a term linear in the rim | 23.273 ± 0.010 | +0.066 | 4.7 |
| (d) the second difference of 45, 63, 84 repeats | 23.338 ± 0.012 | +0.001 | 0.1 |
| (b) the local slope keeps rising by the same step | 23.356 ± 0.015 | −0.017 | 0.9 |
| the old run (1,059 deaths) | 23.376 ± 0.031 | −0.037 | 1.1 |
| **my forecast** | 23.35 ± 0.02 | −0.011 | 0.5 |

- (c) is refuted as stated; I gave it 3%. "Above 23.40" (5%) did not happen.
- **A sign error in block 4, corrected here.** It said (c) could be saved if "the 45-cell face carries a small-size
  deficit of 0.065". The sign is the other way: the measured second differences (0.691, and now 0.692 ± 0.014) are
  *larger* than 3 × 0.2087 = 0.626, and a deficit at the small end lowers a second difference. To keep the tori's
  price the small hull faces would have to live *longer* than the form, by at least 0.197 at 45 cells and 0.066 at
  63 with nothing at 84 and 108. Four values cannot exclude that; the 135-cell face would (29.230 if the second
  difference repeats, 29.163 if the tori's price holds from 84 on; on file 29.34 ± 0.25), and it is out of this
  card's reach (about 40 deaths a day).
- Owed from `research/audit/REVIEW-gpu-local-tori2.md` (its item 5), on block 3: at 81 cells the measured 16.9222 ±
  0.0031 is 2.5 combined errors above the forecast of the line through the first five faces and 0.2 from the smooth
  forms' forecast, whose own error there was ± 0.023. So 81 cells was never a sharp test between them.

**Forecasts for the next chain** (`research/scratch/gpu-local/chain2.sh`; each face: `eqtorus.py check` first, guard
on). The lead's forecasts by form are frozen in `research/wrap/PREDICTIONS.md` (W11 to W13); these are mine. Loops²
are my own enumeration (`python research/gpu-local/loops.py H K D`: primitive lattice vectors, x² + xy + y²) and
agree with the lead's lists.

| torus (H, K), (0, D) | cells | loops² | my forecast | basis |
|---|---:|---|---:|---|
| (1, 12), (0, 28) | 84 | 12, 49, 61, 61 | 17.325 ± 0.008 | it repeats the CPU value 17.3248 ± 0.0058 (independent code) |
| (1, 4), (0, 28) | 84 | 21, 28, 49, 49 | 17.544 ± 0.004 | see below |
| (1, 16), (0, 36) | 108 | 12, 81, 93, 93 | 22.229 ± 0.012 | a tube of fixed girth is straight in its length: the CPU value plus 24 × 0.20437 |
| (1, 17), (0, 32) | 96 | 12, 67, 67 | 19.777 ± 0.008 | the same line; the twist of the tube does not matter |
| (1, 3), (0, 25) | 75 | 13, 37, 43 | 15.535 ± 0.008 | the tester's 15.5363 ± 0.0104 repeats |
| (1, 9), (0, 25) | 75 | 19, 25, 39 | 15.651 ± 0.006 | my 5 × 5 (15.6630) less 0.012 for one loop of 19 |
| (1, 4), (0, 26) | 78 | 21, 28, 31 | 16.291 ± 0.004 | my line 13.1621 + 0.20867 (A − 63); the tester's 16.277 ± 0.012 does not repeat |

- **(1, 4), (0, 28), the lead's W13** (17.534 if a loop of 21 still discounts by the relation of the living state's
  density, 17.547 if the effect ends before 21). My reason for 17.544: my equilateral 63-cell face has three loops
  of 21 and lies within 0.007 of the line through the faces of 75 cells and more, whose loops² are 25 to 37. A
  discount of 0.013 per loop of 21 at 84 cells would put that face about 0.026 low unless loops of 25 to 37
  discount nearly as much; and if they do, my equilateral 84 (three loops of 28) is discounted about as much as
  this face (one of 21, one of 28). Either way the two 84-cell faces differ by little. Below 17.5405 (the midpoint
  of the lead's two): 20%.
- (1, 16), (0, 36): above 22.214 (the midpoint of the straight line and the power form): 70%.
- **Thicker slabs** (not asked; `eqtorus.py ... m=N`, rows in `research/data/gpu_local_thick/`). Why: the hull face
  pays 0.231 per cell where the 8-layer tori pay 0.2087, and no term linear in the rim joins them (above). One
  candidate is depth: a hull face has the whole octahedron behind it, a torus face has 8 layers and a second face.
  `research/constant/README.md` notes that 8 layers were never tested against more at large faces; the only
  thickness data are first peels at A = 48 (notebook, "independent of thickness once m ≥ 7", to a few per cent).
  Runs: (1, 4), (0, 21) at 12 and 16 layers; (2, 4), (0, 14) at 16 layers. Forecast: no change. The 63-cell face
  within 0.005 of its 8-layer value 13.1622 at both thicknesses: 85%; if it moves, upward: 80%. The 84-cell face
  at 16 layers: 17.547 ± 0.006, so a slope 63 → 84 of 0.2087 ± 0.0004 (the hull's slope there is 0.2146).
- **The equilateral 6 × 6 again** (the lead's optional job; six runs of 150 minutes, about 18,000 more deaths):
  pooled with the 2,032 on file, 22.552 ± 0.008 (my line; the lead's relation says 22.535, on file 22.5600 ±
  0.0222). Firewalls about 400, ln τ_fw 25.7 ± 0.1.
- Kind-5 lives in the whole chain: none, 85%.

## 6. Block 5 scored so far: seven wrapped faces and three thicker slabs (2026-11-16T10:14Z, HEAD aea5a72)

Written when parts A and B of `chain2.sh` had ended; the 6 × 6 runs of block 5 are still going and are scored later.
(`python research/gpu-local/eqtorus.py summary H K D [m=N]`, `eq_analyze.py H K D`.)

| torus (H, K), (0, D) | cells | my forecast | measured | measured − forecast | in combined errors |
|---|---:|---:|---:|---:|---:|
| (1, 12), (0, 28) | 84 | 17.325 ± 0.008 | 17.3175 ± 0.0031 | −0.008 | 0.9 |
| (1, 4), (0, 28) | 84 | 17.544 ± 0.004 | 17.5387 ± 0.0031 | −0.005 | 1.0 |
| (1, 16), (0, 36) | 108 | 22.229 ± 0.012 | 22.1557 ± 0.0121 | −0.073 | **4.3** |
| (1, 17), (0, 32) | 96 | 19.777 ± 0.008 | 19.7405 ± 0.0059 | −0.037 | **3.7** |
| (1, 3), (0, 25) | 75 | 15.535 ± 0.008 | 15.5250 ± 0.0028 | −0.010 | 1.2 |
| (1, 9), (0, 25) | 75 | 15.651 ± 0.006 | 15.6442 ± 0.0030 | −0.007 | 1.0 |
| (1, 4), (0, 26) | 78 | 16.291 ± 0.004 | 16.2884 ± 0.0033 | −0.003 | 0.5 |

- **All seven are below my forecast, and the two long tubes are misses.** My reason for them ("a tube of fixed
  girth is straight in its length") was half right: the three tubes of girth² 12 at 84, 96 and 108 cells are
  straight among themselves (second difference −0.008 ± 0.017), but with a slope of 0.2017 ± 0.0004 per cell, not
  the 0.2044 fitted to shorter tubes that I extrapolated with. I took a slope from a range where it was still
  falling. The seeds scatter more than they should on those two faces (χ² 5.5 and 6.3 on 3); with errors scaled
  by that the misses are 3.0 and 2.9.
- (1, 4), (0, 28): I gave "below 17.5405" 20%, and it is below (17.5387). It lies between the lead's two W13
  values, 0.9 errors from "a loop of 21 still discounts" (17.534) and 1.9 from "the effect ends before 21" (17.547).
- "The tester's 16.277 at (1, 4), (0, 26) does not repeat": held (16.2884, 0.9 of its errors above it).
- **Thicker slabs.** 63 cells: 13.1596 ± 0.0012 at 12 layers, 13.1589 ± 0.0013 at 16, against 13.1622 ± 0.0007 at
  8. Both within 0.005, as forecast (85%). "If it moves, upward" (80%) was wrong: the two together are 0.0029 ±
  0.0011 *below* the 8-layer value (2.6σ). 84 cells at 16 layers: 17.5401 ± 0.0044 (forecast 17.547 ± 0.006), slope
  63 → 84 at 16 layers 0.20863 ± 0.00022 (forecast 0.2087 ± 0.0004). Depth is not what makes a hull cell dearer.
- Kind-5 lives so far in the chain: none.

## 7. The 6 × 6 scored; forecasts for chain 3 (more tube seeds, loops of 16 and 13 at 96 cells, a 120-cell tube) (2026-11-17T01:15Z, HEAD 0345df0)

Written after the six new 6 × 6 rows and before any row of chain 3 (`research/scratch/gpu-local/chain3.sh`).

**The 6 × 6 of block 5, scored** (`python research/gpu-local/eq_analyze.py 6 0 6`): ten seeds, 18,394 deaths,
**22.5405 ± 0.0074** (seeds' χ² 6.0 on 9; no kind-5 life). My forecast 22.552 ± 0.008: off by −0.012, 1.1 combined
errors. The lead's two values: 22.535 (the density relation; +0.006, 0.7 errors) and 22.551 (the straight line;
−0.011, 1.4 errors). It leans to the relation and does not decide. Firewalls: I said about 400 and ln τ_fw 25.7 ±
0.1; there are 298 and ln τ_fw = 25.970 ± 0.058, a miss of 2.3 combined errors. The six long runs (ages to 3.3 ×
10⁹) give 26.01 ± 0.06 where the four short ones (ages to 4 × 10⁸) gave 25.70 ± 0.15; I extrapolated a rate from
young lives. Whether firewalls come less often to old lives was not tested.

**Chain 3** (the lead's note of 10:20Z, 2026-11-16, in its order; guard on; `eqtorus.py check` first on each face;
loops² from `loops.py`):

| torus (H, K), (0, D) | cells | loops² | runs | my forecast | basis |
|---|---:|---|---|---:|---|
| (1, 17), (0, 32) | 96 | 12, 67, 67 | 4 more of 20 min | pooled 19.741 ± 0.006 | the value on file repeats |
| (1, 16), (0, 36) | 108 | 12, 81, 93, 93 | 4 more of 60 min | pooled 22.156 ± 0.012 | the value on file repeats |
| (4, 0), (0, 8) | 96 | 16, 48, 64 | 4 of 22 min | 19.937 ± 0.012 | the 16-tube line (19.946 to 19.951 from the 4 × 7) less a bend of 0.012 |
| (1, 8), (0, 32) | 96 | 16, 49, 57, 73 | 4 of 22 min | 19.937 ± 0.012 | the same loop with a twist: the same value |
| (1, 3), (0, 32) | 96 | 13, 61, 64 | 4 of 20 min | 19.82 ± 0.015 | my 75-cell value plus 21 × 0.20602 (19.851), less a bend of 0.03 |
| (1, 18), (0, 40) | 120 | 12, 103, 103 | 8 of 180 min | 24.576 ± 0.020 | the 108-cell tube plus 12 × 0.2017 |

- The 12-tube slope from 84 to 108 cells with the new seeds: inside 0.2005 to 0.2029, 80%.
- The bend: the 12-tubes came out 0.039 below their short-tube line at 96 cells. I expect a loop of 16 to bend
  about a third as much and a loop of 13 about three quarters as much (in proportion to their discounts). Below
  19.940 at (4, 0), (0, 8): 60%. Below 19.840 at (1, 3), (0, 32): 75%.
- The two 16-loop faces within 0.012 of each other: 80% (the three 12-tubes of different twist lie on one line).
- The 120-cell tube within 0.04 of 24.576: 75%. If the tube's slope keeps falling it is lower.
- Kind-5 lives: none, 85%.
- The chain script commits and pushes its data rows itself (after the 96-cell faces and at the end), with
  `chain3_summary.txt`, so that the lead can read them without a turn of this session; nothing is analysed or
  scored until this session's next turn.

## 8. Block 7 scored so far: more tube seeds, loops of 16 and 13 at 96 cells (2026-11-17T11:43Z, HEAD 3fb4ec0)

Written when the first five faces of `chain3.sh` had ended (rows pushed by the script at 3fb4ec0); the 120-cell tube
is running and is scored later. (`python research/gpu-local/eq_analyze.py H K D`.)

| torus (H, K), (0, D) | cells | my forecast | measured | measured − forecast | in combined errors |
|---|---:|---:|---:|---:|---:|
| (1, 17), (0, 32), eight seeds | 96 | 19.741 ± 0.006 | 19.7446 ± 0.0042 | +0.004 | 0.5 |
| (1, 16), (0, 36), eight seeds | 108 | 22.156 ± 0.012 | 22.1599 ± 0.0086 | +0.004 | 0.3 |
| (4, 0), (0, 8) | 96 | 19.937 ± 0.012 | 19.9366 ± 0.0064 | −0.000 | 0.0 |
| (1, 8), (0, 32) | 96 | 19.937 ± 0.012 | 19.9284 ± 0.0063 | −0.009 | 0.6 |
| (1, 3), (0, 32) | 96 | 19.82 ± 0.015 | 19.8109 ± 0.0062 | −0.009 | 0.6 |

- The 12-tube slope from 84 to 108 cells is 0.2020 ± 0.0003 with the new seeds: inside 0.2005 to 0.2029 (I gave 80%).
  The seeds' scatter that worried block 6 has gone: χ² 10.0 on 7 and 6.8 on 7.
- "Below 19.940 at (4, 0), (0, 8)" (60%): yes. "Below 19.840 at (1, 3), (0, 32)" (75%): yes. "The two 16-loop faces
  within 0.012 of each other" (80%): yes, 0.008 ± 0.009.
- The bends against the short-tube lines are 0.040 ± 0.007 for the loop of 13 (I said about 0.03) and 0.014 to 0.019 for
  the loop of 16 (I said 0.012). So the loop of 13 bends as much as the loop of 12 did (0.039), not three quarters of it.
- Kind-5 lives so far in the chain: none.

## 9. The 120-cell tube scored; forecasts for chain 4 (the 126- and 132-cell tubes of the same family) (2026-11-18T12:04Z, HEAD d4f0c41)

Written after the eight rows of (1, 18), (0, 40) and before any row of chain 4
(`research/scratch/gpu-local/chain4.sh`).

**The 120-cell tube of block 7, scored** (`python research/gpu-local/eq_analyze.py 1 18 40`): eight runs, 3,494
deaths, **24.5086 ± 0.0169** (seeds' χ² 4.4 on 7). My forecast 24.576 ± 0.020: off by −0.067, 2.6 combined errors.
"Within 0.04 of 24.576" (75%): no. "If the tube's slope keeps falling it is lower": it is. "Kind-5 lives: none"
(85%): none in the whole chain. The forecasts frozen by the theory session (`research/blast/REPORT.md` on
`claude/exciting-hamilton-0h2tr1`) were 24.56 ± 0.03 to 24.60 ± 0.07, all above it too.

I used the chord from 96 to 108 cells for the last 12 cells. The measured chord from 108 to 120 is 0.1957 ± 0.0016.
I gave the falling slope a quarter of the probability and it deserved more: the chords had already gone 0.2044
(54 to 84, the lead's line), 0.2023, 0.2013.

**Chain 4** (my own choice of run; the card would otherwise be idle until the lead's next note). Same family as
the 84-, 108- and 120-cell tubes: a = 1, loop vector (2, −4), 12 cells per unit of length. Guard on;
`eqtorus.py check` first on each face.

| torus (H, K), (0, D) | cells | loops² | runs | my forecast | the line through 84, 96, 108 | the theory session's K = 2 form |
|---|---:|---|---|---:|---:|---:|
| (1, 19), (0, 42) | 126 | 12, 111, 117 | 8 of 180 min | 25.685 ± 0.035 | 25.801 ± 0.012 | about 25.776 |
| (1, 20), (0, 44) | 132 | 12, 121, 133, 133 | 8 of 180 min | 26.855 ± 0.060 | 27.013 ± 0.013 | about 26.979 |

- Basis: the 120-cell value plus 0.196 per cell, with ± 0.004 on that slope. The K = 2 column is my own
  continuation of that form from its 24.571 at 120 cells (slope 0.2008 there, limit 0.2004), not a number its
  authors wrote.
- Expected deaths: about 1,100 at 126 cells (± 0.030) and about 340 at 132 cells (± 0.055).
- The 126-cell tube below 25.74: 80%. Below 25.70: 60%. If it is above 25.76 then the 120-cell value was a low
  fluctuation (I give that 10%).
- The chord from 120 to 132 cells below 0.2004 (the limit of the fitted form): 75%. Below 0.190: 20%.
- Kind-5 lives: none, 85%. Firewalls: none, 90% (no 12-tube has had one since 84 cells).
- What would change my mind about the cause: I have no mechanism for a slope below the fitted limit. The theory
  session reports that long tubes stop busting all at once (the two halves crash in different generations); if
  that makes death cheaper per cell, the slope should go on falling at 132 cells.

## 10. A second code on the 120-cell tube: forecast (2026-11-18T19:21Z, HEAD 30d881c)

Written before any row of `fr.py run 1 18 40` (the CPU second code, 12 threads, 48 hours, seeds from 30000; rows
append every 15 minutes to `research/data/gpu_local_cpu/fr_1_18_40_m8.csv`). The card's value is 24.5086 ± 0.0169,
which is 0.081 ± 0.020 below the line through the 84-, 96- and 108-cell tubes (24.589 ± 0.010).

- Expected: about 760 deaths, ± 0.036 (from the 96-cell tube's 311 deaths per thread-hour and the lifetime ratio).
- The CPU value within two combined errors of the card's (within about 0.08 of 24.509): 90%.
- The CPU value below 24.589: 90%. Below 24.55: 80%.
- If it comes out at 24.59 or above, the card's value was a low fluctuation or the two codes differ at this size;
  I give that 7%.
- First look at chain 4, not a result: after two of the eight runs the 126-cell tube has 223 deaths and 25.848 ±
  0.067, above my 25.685 ± 0.035 and beside the straight line's 25.801.

## 11. Chain 4 scored; forecasts for chain 5 (the 120-cell tube again, more of the 126) (2026-11-20T12:35Z, HEAD 0f1a4e0)

Written after the sixteen rows of chain 4 and before any row of chain 5 (`research/scratch/gpu-local/chain5.sh`).

**Block 9, scored** (`python research/gpu-local/eq_analyze.py 1 19 42`, `… 1 20 44`):

| torus (H, K), (0, D) | cells | my forecast | measured | measured − forecast | in combined errors |
|---|---:|---:|---:|---:|---:|
| (1, 19), (0, 42) | 126 | 25.685 ± 0.035 | 25.7572 ± 0.0320 | +0.072 | 1.5 |
| (1, 20), (0, 44) | 132 | 26.855 ± 0.060 | 26.9057 ± 0.0584 | +0.051 | 0.6 |

- "The 126-cell tube below 25.74" (80%): no. "Below 25.70" (60%): no. "Above 25.76, so the 120-cell value was a
  low fluctuation" (10%): 25.757, under the mark by 0.003.
- "The chord from 120 to 132 cells below 0.2004" (75%): 0.1998 ± 0.0051 with the card's 120-cell value, which is yes
  by the letter and decides nothing. "Below 0.190" (20%): no.
- Kind-5 lives none (85%): none. Firewalls none (90%): none.
- Deaths: I expected about 1,100 and 340; there are 977 and 293.
- I was wrong to build on one face. I put 10% on the 120-cell value being a low draw; the second code (block 10,
  interim 24.594 ± 0.040 at 613 deaths) and the 126-cell face both say it probably is, in part.

**Block 10** (the second code at 120 cells) is scored when its run ends, about 19:30Z on 2026-11-20.

**Chain 5** (my own choice again: the lead's queue has no new note). Guard on; checks first.

| torus (H, K), (0, D) | cells | runs | my forecast for the new seeds alone |
|---|---:|---|---:|
| (1, 18), (0, 40) | 120 | 8 more of 180 min, seeds 12018011 to 12018018 | 24.545 ± 0.030 |
| (1, 19), (0, 42) | 126 | 8 more of 180 min, seeds 12619011 to 12619018 | 25.765 ± 0.040 |

- The new 120-cell seeds above the first eight's 24.5086: 80%. Above 24.589 (the line through 84 to 108 cells): 8%.
- The new 126-cell seeds' χ² below 14.1 on 7 (the 95% point): 90%. If it is above again, the deaths of long tubes are
  over-dispersed between runs and every error at these sizes is too small.
- Kind-5 lives none: 85%. Firewalls none: 90%.

## 12. Block 10 scored (the second code at 120 cells); forecasts for the CPU's next runs (2026-11-20T19:30Z, HEAD e9f188b)

**Block 10, scored** (`python research/gpu-local/cpu/fr.py summary 1 18 40`): twelve seeds, 576 thread-hours, 716
deaths, **24.5969 ± 0.0374** (seeds' χ² 17.6 on 11). I expected about 760 deaths and ± 0.036.

- "Within two combined errors of the card's 24.5086 ± 0.0169" (90%): no, by a little: +0.088 ± 0.041, 2.2 errors.
- "Below 24.589" (90%): no. "Below 24.55" (80%): no.
- "At 24.59 or above: the card's value was a low fluctuation or the two codes differ at this size" (7%): this is
  the case that happened. Which of the two it is, is not known. The first two new seeds of chain 5 on the card
  (not a result: 848 deaths) give 24.549 ± 0.034 by themselves.

**The CPU's next runs** (`research/scratch/gpu-local/chain_cpu2.sh`, 12 threads, written before any row):

| torus (H, K), (0, D) | cells | run | the card | my forecast for the second code |
|---|---:|---|---:|---:|
| (1, 16), (0, 36) | 108 | 24 hours, seeds from 31000 | 22.1599 ± 0.0086 | 22.165 ± 0.014 (about 8,000 deaths, ± 0.011) |
| (1, 18), (0, 40) | 120 | 48 more hours, seeds from 32000 | 24.5165 ± 0.0152 so far | the new seeds alone 24.565 ± 0.040 |

- Why 108 cells first: the two codes agree to 0.007 at 96 cells and are 0.088 ± 0.041 apart at 120. If they differ
  by something that grows with the face, 108 cells shows it at a quarter of the cost.
- The second code within two combined errors of the card at 108 cells: 90%. More than 0.03 above the card: 6%.
- The new CPU seeds at 120 cells below the first twelve's 24.597: 70%.
- Seeds' χ² at 108 cells below 19.7 on 11 (the 95% point): 92%.
