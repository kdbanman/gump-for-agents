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
