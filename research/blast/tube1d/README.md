# blast/tube1d: tubes as a one-dimensional problem (agent `tube1d`, 2026-11-18)

Standing account; results, not a diary. Everything here is about wrapped faces with one short way round (loop² 12
unless said otherwise), on **deterministic gump** except §6 (the honest-dice surrogate). Labels: [proved],
[measured], [conjectured]. Times are the machine clock (UTC).

Build and files (run from this directory; `S=../../scratch/blast/tube1d`, ignored by git):

    mkdir -p $S && gcc -O3 -march=native -o $S/tube1d tube1d.c -lm

`tube1d.c` (own stepper, bit-sliced, 64 lanes; commands `trace brute ffs clone bandp band geom`, usage in its
header), `validate.py` + `validate_all.sh` (oracle check), `bandfit.py`, `margfit.py`, `tubefit.py`, `paths.py`,
`pops.py`, `imagefit.py` (analysis), `data/` (curated outputs; formats in §8), `PREDICTIONS.md` (blocks A–C).

## 0. What stands

1. **A tube dies as a whole, in a flash; no band dies first and no front sweeps** [measured, §4]. In 323 deaths of
   the 84-cell tube the typical cell is last alive 6 generations before the end and the earliest tenth 7.7; no
   band right round the girth is finally empty 4 generations before the median cell in more than 2% of deaths;
   death times of 0.5-unit bands differ by 1.2 generations r.m.s. however far apart they are along the tube. What
   lingers is a last clump of about 6 cells for 5–6 generations (which is why a "band empty ≥ 4 generations before
   the last cell" criterion reads 60–72% for a flash).
2. **The same holds for a band of a long living tube** [measured, §3]: when a band of width w ≤ 6 units of a
   144-cell tube is momentarily empty, every 0.5-unit bin of it has been empty for 2.4–3.2 generations, edge and
   middle alike, and complete emptiness lasts 1.7 generations whatever the width (it refills from its edges at once).
3. **The price of emptying one more unit of tube falls with the length already emptied, for bands of a living
   tube as for whole tubes** [measured, §3, §5]. Marginal price per cell of an empty band (five independent
   runs, 2.1·10¹¹ band-position-generations, errors from the runs): 0.2359 at 2–2.5 units, 0.2286, 0.2223, 0.2190 ±
   0.0005, 0.2165 ± 0.0011, 0.2141 ± 0.0024, 0.2102 ± 0.0031, 0.2059 ± 0.0035 at 2.5–3, 3–3.5, … 5.5–6 units (then
   0.2135 ± 0.008, 0.208 ± 0.019 to 7 units): still falling at 6 units, where it has come down to the whole tube's
   own price at that length (anchors: 0.2049, 0.2035, 0.2019, 0.2013 from 5→6 … 8→9 units). −ln P(band of width w
   empty) − ln τ_face(tube of length w) = 3.855 ± 0.022, 3.893 ± 0.053, 3.98 ± 0.20 at w = 5, 6, 7: a constant
   within errors. **Where it levels**: a straight line through the tubes fails (χ² = 26 for 3); tubes alone with an
   exponential approach give c∞ = 0.199 (0.195 … 0.202); bands and tubes with one c∞ and one ξ (item 6) give c∞ =
   0.2004, ξ = 1.95 units; a power-law prefactor τ ∝ L^p·e^(12cL) fits the tubes as well (p = 0.75 ± 0.15, c = 0.194)
   and bands and tubes together poorly (χ² = 23 for 11). So: **it does not return to the wide price 0.2087, it does
   not fall as a parabola, and it levels at 0.199–0.202 unless the correction is a power law, which the tubes alone
   cannot exclude.** The 120-cell tube hardly decides (24.53–24.61 across all variants); 192 cells would (39.0–39.2
   exponential, 38.9 power law). I could not push the band beyond 7 units (§9).
4. **Boom and bust hardly changes with tube length up to 7 units, but loses ground to thinning in bands**
   [measured, §4]: the share of deaths with a one-generation fall of at least half the face is 59.3 ± 2.0%, 56.7 ±
   1.1%, 56.3 ± 1.7%, 51.3 ± 4.7% at 48 (4×4), 60, 72 and 84 cells (tubes of length 5, 6, 7). My forecast that it
   falls to 27% by 84 cells (block C) was wrong. In bands of a living tube the same criterion gives 77% at 2
   units, 60.7% at 4, 52.6 ± 0.7% at 5, 43 ± 3% at 6, 22 ± 6% at 7: a second route (thinning over 3–4 generations,
   no over-filling) takes over with width.
5. **Forward-flux sampling on the face population does not work on the honest-dice surrogate, and I can say why**
   [measured, §6]: the dice need 3 generations to reach the face, a death takes 5–8 from one standard deviation
   below the mean, and half of the variance of the outcome is already decided by the state when the population
   first crosses half (clone test). Replications of the whole estimator scatter by 0.07 at 48 cells, 0.3 at 63,
   0.75–1.2 at 84 (7×10⁵ trials per level). **No lifetime of a tube longer than 9 units was
   measured here.** The curves beyond are extrapolations of item 3.

6. **The trace reading passes with multiplicity 2** [measured, §5]: bands and tubes fitted with one c∞ and one ξ
   and ln τ(L) = a + 12c∞L − ln(1 + K·e^(−L/ξ)) for the closed tube: K = 2: χ² = 3.35 for 9, c∞ = 0.2004, ξ = 1.95;
   K = 1: 11.1 for 9; K = 3: 3.2 for 9; K free = 2.5. Forecasts K = 2: 24.571, 29.388, 39.010, 48.628 at 10, 12,
   16, 20 units (K = 1: 24.608, 29.463, 39.168, 48.871).
7. **Girth 4 is a different problem** [measured, §7]: a tube of loop² 16 gets cut by transverse firewalls that
   neither heal nor spread (a through-cut of 3 units stays 2.4 units wide for 600 generations in 256 lanes; at
   loop² 12 the same cut heals in 24), and a 168-cell tube's face then lives only ln τ = 17.42 ± 0.17: the
   lifetime saturates with length.

Forecast frozen for the blind 120-cell tube (block B, commit 9a1ccc4, 03:46): **24.563 ± 0.030** (an extrapolation,
not independent of the PI's block 0). Fits made afterwards: 24.571 (trace reading, K = 2), 24.608 (K = 1), 24.557
(power law p = 0.75).

## 1. Stepper and validation [measured]

`sh validate_all.sh` (2 minutes; output `validate_log.txt`): the deterministic slab of `tube1d.c` against
`reference/oracle.py`, state for state over 1,500 generations on (4,0),(0,4), (1,4),(0,21), (1,12),(0,28),
(1,17),(0,32) (8 layers) and (1,3),(0,25) (7 layers): all identical, 1,501 distinct states each; with one wrong
neighbour (`bad`) the comparison fails at generation 8 and at generation 5. The slab is unfolded into the oracle's
cubic array torus of m cubes a side with m·e1, m·e2 in the period lattice (`validate.py`).

Lifetime convention check (`tube1d brute h k d 8 0 seed 500 gens`; restart at the first face death, 500
generations of burn-in not counted, τ_face = 2·exposure/deaths, lives whose state repeats with a period dividing 840
or whose state has period ≤ 2 are censored):

| vessel | mine | on file |
|---|---|---|
| (4,0),(0,4), 48 cells | 9.9229 ± 0.0053 (35,856 deaths; `brute 4 0 4 8 0 21 500 6000000`) | 9.9251 ± 0.0004 |
| (1,8),(0,20), 60 cells | 12.4124 ± 0.0220 (2,074 deaths; seed 31, 4·10⁶ generations) | 12.4166 ± 0.0031 |
| (4,4),(0,6), 72 cells | 14.8773 ± 0.0336 (885 deaths; seed 32, 2·10⁷ generations) | 14.8753 ± 0.0140 |

Without the period-840 test the 48-cell number is 9.9646 ± 0.0030 (+0.04): lives that settle into debris of period
3 or more with both faces occupied never die and pile up exposure. The burn-in is not the reason (no burn-in:
9.9611 ± 0.0053 with the same defect).

## 2. Geometry

Cell (l, a, x, y): layer l (s = 2l + 1), orientation a, cube (i, j, k) = (x, −x−y, y+l); hexagonal basis
e1 = (1,−1,0), e2 = (0,−1,1) in cube steps, |x e1 + y e2|² = 2(x² + xy + y²); period lattice (h,k),(0,d). The
girth is the shortest lattice vector; ξ-coordinate ("xi" in the code) is the position along the tube axis, in
lattice units (|e1| = 1), length = area/girth; loop² 12 has 12 cells per unit length. Tubes used: (1,8),(0,20),
(4,4),(0,6), (1,12),(0,28) (lengths 5, 6, 7, untwisted), (1,22),(0,48) (length 12), (1,38),(0,80) (length 20).

## 3. An empty band right round the girth of a living tube [measured]

`$S/tube1d bandp 1 22 48 8 0 SEED GENS 500 16` (deterministic gump, 144-cell tube, both faces, 64 lanes): five
independent runs, seed 5 with 2·10⁷ generations (`data/bandp_g12_L12.txt`) and seeds 15, 16, 17, 18 with 1.2·10⁷
(`data/bandp5_g12_L12*.txt`, which also carry the `AGE` and `PRE` histories), 2.1·10¹¹ band-position-generations
in all. Pooled by `python3 bandcombine.py data/bandp_g12_L12.txt data/bandp5_g12_L12*.txt
--out=data/band_g12_pooled.slopes` (table in `data/band_g12_pooled.txt`). A window of m bins of 0.5 units (6 cells
each) is "empty" when none of its cells is alive. **Errors are the standard error over the five runs**; the naive
1/√appearances is 2 to 2.5 times too small from 4.5 units on (appearances come in clusters: an emptied band
flickers at its edges while it heals).

| width (units) | cells | −ln P(empty), pooled | s.e. over runs | price per cell from the previous width | mean duration (gens) |
|---:|---:|---:|---:|---:|---:|
| 0.5 | 6 | 3.6263 | 0.0000 | | 1.35 |
| 1.0 | 12 | 5.4854 | 0.0001 | 0.3098 | 1.81 |
| 1.5 | 18 | 6.8326 | 0.0002 | 0.2245 | 1.79 |
| 2.0 | 24 | 8.2536 | 0.0004 | 0.2368 | 1.74 |
| 2.5 | 30 | 9.6689 | 0.0007 | 0.2359 ± 0.0001 | 1.71 |
| 3.0 | 36 | 11.0402 | 0.0009 | 0.2286 ± 0.0001 | 1.70 |
| 3.5 | 42 | 12.3740 | 0.0020 | 0.2223 ± 0.0002 | 1.69 |
| 4.0 | 48 | 13.6878 | 0.0041 | 0.2190 ± 0.0005 | 1.68 |
| 4.5 | 54 | 14.9866 | 0.0101 | 0.2165 ± 0.0011 | 1.68 |
| 5.0 | 60 | 16.2714 | 0.0217 | 0.2141 ± 0.0024 | 1.69 |
| 5.5 | 66 | 17.5324 | 0.0396 | 0.2102 ± 0.0031 | 1.66 |
| 6.0 | 72 | 18.7679 | 0.0507 | 0.2059 ± 0.0035 | 1.6 |
| 6.5 | 78 | 20.049 | 0.087 | 0.2135 ± 0.0081 | 1.5 |
| 7.0 | 84 | 21.29 | 0.20 | 0.208 ± 0.019 | 1.6 |

(The first run alone read 0.2103 ± 0.0033 at 4.5–5 units and 0.2044 at 5–6; the forecasts of block B quote those.
The durations are from the first run.)

- **The price is not constant**: a plateau at 0.236 (2–2.5 units), then a steady fall, (18.7679 − 13.6878)/24 =
  0.2117 ± 0.0021 from 4 to 6 units (forecast A1: 0.205 ± 0.015, hit) and 0.2059 ± 0.0035 at 5.5–6.
- **The band and the tube are the same object to within a constant** [measured]: −ln P(band w) − ln τ_face(tube of
  length w) = 16.2714 − 12.4166 = 3.855 ± 0.022 (5 units), 18.7679 − 14.8753 = 3.893 ± 0.053 (6), 21.29 − 17.3175 =
  3.98 ± 0.20 (7). [conjectured] The constant is two edges plus a duration: with 1.7 generations of emptiness and
  0.5-unit positions, 2σg ≈ 3.8 gives σ ≈ 0.55 per lattice unit of edge, near the 0.66 the PI quotes for patches.
- **A flash, not a hole that grew** (`AGE` lines, `data/bandp5_g12_L12.txt`, seed 15): number of generations
  each 0.5-bin had been empty when the window first was, from the edge bin to the middle: 4 units (24,993
  events) 2.38 2.87 2.86 2.78; 5 units (1,834) 2.62 3.12 3.14 3.03 2.99; 6 units (150) 2.92 3.46 3.39 3.29 3.31 3.28.
  A hole growing at u units per generation would show (w/2)/u more in the middle than at the edge; the middle is
  not older than the bins next to the edge.
- **How long an emptied band lasts**: completely empty for 1.7 generations at every width (table). The edges are
  retaken at once; the interior cannot be reborn before they arrive (T2's count: a dead face cell with dead
  in-layer neighbours has at most 3 live neighbours).
- **Boom and bust inside bands** (`PRE` lines): see §4.
- **A band emptied by hand always heals, at 0.25 units per generation from each edge** (`$S/tube1d band 1 22 48 8 0
  77 W 40 8`, W = 1, 2, 3, 4, 6: the top face's cells with axis coordinate below W are killed in 512 living lanes;
  `data/band_g12_w*.txt`). Longest run of empty 0.5-bins, W = 6: 6.02, 5.29, 4.69, 4.12, 3.65, 3.17, 2.63, 2.15,
  1.65, 1.23, 0.85 at t = 0 … 10 (0.51 units per generation, both fronts together; the living state's own
  baseline is 0.25); W = 4: 4.03, 3.28, 2.67, 2.18, 1.68, 1.26, 0.83. Half of the lanes have no empty bin left
  after 3, 5, 6, 8, 12 generations for W = 1, 2, 3, 4, 6, all of them by 2W + 16; the band's density is back at
  0.51 by then. No lane's face died and no gap grew, at any width. So the front between living and empty face
  moves into the empty side at 0.25 units per generation and a sweep would have to be pushed against it: the
  sign asked for in the brief's (b) is "heals". (Only the face layer was killed; the layers beneath were left alive.)

Other girths and a longer tube (finite-length check): §7.

## 4. How a tube dies: reactive paths [measured]

`$S/tube1d brute 1 12 28 8 0 7 500 60000000 paths_1_12_28.txt` (stopped at 210 face deaths) and
`python3 paths.py $S/tube1d 1 12 28 8 data/paths_1_12_28.txt`; lag = generations before the death at which a cell
was last alive (format in §8). Numbers below at the first 106 deaths; with the second run
(`data/paths_1_12_28_b.txt`, seed 33, 113 deaths) the 323 deaths give the same: median lag 6.0, 90th percentile
8.0, band-first against the median cell 0.9% (0.5-unit bands) and 0.3% (1-unit), last cells within 2 units in 55%:

- median over deaths of the median lag: 6.0; of the 90th-percentile lag: 7.7. The face empties within about 2
  generations everywhere; 5.8 cells are alive in the last 2 living generations, spanning under 2 units of the
  7-unit tube in 53% of deaths (forecast A3 said > 70% of deaths: miss; the last cells are often two clumps).
- band-first share, PI's criterion (some band finally empty ≥ 4 generations before the LAST cell): 72% for 0.5-unit
  bands, 60% for 1-unit bands — met by a flash because of the lingering clump (forecast A2: 85%, PI: 20%). Against
  the MEDIAN cell's last live generation: 1.9% and 0.9%; ≥ 8 generations: 0. At 60 cells (2,074 deaths): 0.4%, 0.0%.
- mean lag against distance along the tube from the last clump: 5.4 (0–0.5 units), 6.1, 6.4, 6.6, 6.7, 6.6, 6.6
  (3–3.5 units): flat beyond 1.5 units. No tilt.
- structure function of the death time of 0.5-unit bands (median lag of the band's cells) against their
  separation: 1.19, 1.78, 2.31, 2.56, 2.79, 2.79, 2.85 generations² at 0.5 … 3.5 units: it saturates by 2.5 units
  at (1.2 generations)²·2. The death time does not wander along the tube.

Boom and bust (`brute ... PATHFILE` also writes `PATHFILE.pop`, the dying face's population in its last 24
generations; `python3 pops.py A FILE.pop`). Share of deaths with a one-generation fall of at least half the face:

| vessel | cells | deaths | share | population before the fall → after (boom-and-bust deaths) |
|---|---:|---:|---:|---|
| (4,0),(0,4) torus | 48 | 597 | 59.3 ± 2.0% | 37.3 → 8.3 (stationary 24.6) |
| (1,8),(0,20) tube, length 5 | 60 | 2,074 | 56.7 ± 1.1% | 46.5 → 10.7 (30.7) |
| (4,4),(0,6) tube, length 6 | 72 | 885 | 56.3 ± 1.7% | 55.6 → 12.9 (36.9) |
| (1,12),(0,28) tube, length 7 | 84 | 113 | 51.3 ± 4.7% | 64.6 → 15.2 (43.0) |

Block C forecast (48, 37, 27% at 60, 72, 84 cells): **wrong at all three**; the "no trend" alternative, to which
I gave 20%, is the nearest (a drift of a few points per unit is not excluded: log-odds fall by 0.05 ± 0.07 per
unit from 5 to 7 units). The 84-cell run also gives ln τ_face = 17.159 ± 0.094 (on file 17.3175).

**Bands are different** (`python3 bandboom.py data/bandp5_g12_L12*.txt`: `PRE` lines of four runs, 4.8·10⁷
generations): the share of band-emptying events with a one-generation fall of at least half the band's cells in
the band's last 9 generations falls steadily with width: 81.9% (1 unit), 77.1% (2), 68.8% (3), 60.7 ± 0.2% (4;
99,919 events), 56.7 ± 0.5% (4.5), 52.6 ± 0.7% (5; 7,490), 47.6 ± 1.1% (5.5), 43.3 ± 2.8% (6; 617), 37.1 ± 2.9%
(6.5), 22 ± 6% (7; 51 events) (s.e. over the runs). (A pilot of 10⁵ generations had suggested it levels at 63%; it
does not.) The other events are a thinning over 3–4 generations with no over-filling. Mean density of a 5-unit
band 1, 2, … 7 generations before it first is empty: 0.039, 0.117, 0.302, 0.429, 0.478, 0.495, 0.508 (stationary
0.5155). In log-odds the share falls by 0.36, 0.33, 0.37 per unit from 3 to 6 units (and by 1.0 from 6 to 7, in a
tube with only 5 units left alive): in a band the boom-and-bust route costs about 0.03 per cell more than thinning.

So the falling price of a **whole tube** up to 7 units is not a change of route (not band-first, not a sweep; a
shift between routes of 0.05 ± 0.07 in log-odds per unit bends ln τ by 0.25 × 0.05² ≈ 0.0006 per unit², against
the 0.017 per unit² seen), while in a **band** of a living tube thinning gains on boom and bust with width: there
the shift bends −ln P by 0.25 × 0.36² = 0.032 per unit², i.e. it lowers the band's price by 0.0027 per cell per
unit of width, about half of the band's fall at 4–5 units (0.005 per unit); the other half is the size of the whole
tube's own fall (0.0015 per unit at 6–7 units). [measured; the bookkeeping is mine]

## 5. The one-dimensional form [measured fits; the reading is conjecture]

Anchors for loop² 12 (lengths 5…9): 12.4166 ± 0.0031, 14.8753 ± 0.0140, 17.3175 ± 0.0031, 19.7405 ± 0.0059,
22.1557 ± 0.0121. `python3 tubefit.py`:

- a straight line fails: χ² = 26.0 for 3.
- τ ∝ L^p·e^(sL) fits too: p = 0.75 ± 0.15, s/12 = 0.1937, χ² = 0.08 for 2 (p = 1/2: χ² = 2.9 for 3; p = 1: 3.0 for 3;
  see §7 for why a power is natural). Forecasts L = 10, 12, 16, 20, 30: 24.557, 29.343, 38.856, 48.321, 71.869.
- ln τ(L) = a + s·L − ln(1 + K·e^(−L/ξ)) fits: χ² = 0.07 for 2 at K = 2, ξ = 2.4, s/12 = 0.1992; χ² = 0.31 at K = 2,
  ξ = 2.0 (s/12 = 0.2003); K = 4, ξ = 1.4: 0.15 (0.2009); K free: 2.2, ξ = 2.05 (0.1998). The anchors alone do not
  separate K from ξ. Forecasts along the valley: L = 10: 24.56–24.57; 12: 29.36–29.39; 16: 38.93–39.04; 20:
  48.50–48.68; 30: 72.4–72.8.
- `python3 margfit.py data/band_g12_pooled.slopes`: band slopes (2.5–7 units, pooled over five runs, errors from
  the runs, floored at 0.0005) and tube slopes (5–9) together, price(ℓ) = c∞ + B·e^(−ℓ/ξ): χ² = 15.95 for 10 (the
  tube's 5→6 at −2.6 σ, the band's 3.5–5 at +1.1 … +1.6 σ); c∞ = 0.1966 (0.1952 … 0.1976 over χ² + 1), ξ = 2.65 (2.45
  … 2.95), B = 0.090. Bands alone: χ² = 4.3 for 6, c∞ = 0.207 (0.2005 … 0.2105), ξ = 1.65 (1.25 … 2.45). Tubes alone:
  χ² = 0.10 for 1, c∞ = 0.199 (0.195 … 0.202), ξ unconstrained. Joint curve at 10, 12, 16, 20 units: 0.1987, 0.1976,
  0.1968, 0.1967; 120-cell tube: 24.545. (With the first band run alone the same fit gave c∞ = 0.1989, ξ = 2.05,
  χ² = 4.5 for 9: the pooled data are less kind to "one curve".)
- The same script, power law instead: price = c + p·ln(ℓ2/ℓ1)/(12(ℓ2 − ℓ1)), i.e. τ ∝ ℓ^p·e^(12cℓ): bands + tubes
  χ² = 22.97 for 11 (p = 0.02; strained), c = 0.1869 ± 0.0007, p = 1.39 ± 0.03; bands alone χ² = 3.7 for 7,
  p = 1.17 ± 0.07, c = 0.193 ± 0.002; tubes alone χ² = 0.11 for 2, p = 0.72 ± 0.27, c = 0.194 ± 0.003. Its forecasts:
  L = 10: 24.545 (tubes alone 24.560); 12: 29.28 (29.35); 16: 38.65 (38.87); 20: 47.93 (48.34); 30: 70.92 (71.91).
  **The forms agree to 0.02 at 120 cells and part by 0.1–0.4 at 192 cells and 0.2–0.8 at 240**: the PI's
  "prefactors can fake prices" applies to my c∞ in full. Bands and tubes want different p (1.17 ± 0.07 against
  0.72 ± 0.27) and different c∞ (0.207 against 0.199 exponential): the band has two healing edges and a shifting
  route (§4), so "one curve" is an approximation, good to about 0.003 per cell where both are measured.

**The trace reading (PI's request after agent `image`'s identity), tested** — `python3 jointfit.py
data/band_g12_pooled.slopes 3.0`: tubes ln τ(L) = a_t + sL − ln(1 + K_t·e^(−L/ξ)) on the five anchors, bands
S(w) = a_b + sw − ln(1 + K_b·e^(−w/ξ)) on the eight pooled slopes from 3 to 7 units (errors from the five runs), one
s = 12c∞ and one ξ for both, K_b free:

| K_tube | χ² / dof | c∞ | ξ (χ² + 1) | K_band | tube at 10 | 12 | 16 | 20 units |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 (fixed) | 11.10 / 9 | 0.20216 | 1.85 (1.75 … 1.95) | 4.5 | 24.608 | 29.463 | 39.168 | 48.871 |
| **2 (fixed)** | **3.35 / 9** | **0.20037** | **1.95 (1.85 … 2.00)** | 5.5 | **24.571** | **29.388** | **39.010** | **48.628** |
| 3 (fixed) | 3.17 / 9 | 0.19938 | 1.85 (1.65 … 1.90) | 6.0 | 24.549 | 29.343 | 38.917 | 48.487 |
| free: 2.46 | 1.76 / 8 | 0.20030 | 1.80 (1.70 … 1.85) | 5.5 | 24.567 | 29.381 | 38.998 | 48.613 |

With the band slopes from 4 units only (6 slopes): K_t = 1: 8.46 / 7 (c∞ 0.2012, ξ 2.45); K_t = 2: 2.41 / 7 (0.2003,
ξ 2.00); K_t = 3: 1.52 / 7 (0.2003, ξ 1.65); free 3.3. Separately: tubes alone want ξ = 2.40 (1.80 … 3.65), c∞ =
0.1992 (0.1977 … 0.2009) at K_t = 2 (χ² 0.07 for 2) and reach only χ² = 4.7 for 2 at K_t = 1; bands alone want
ξ = 1.80 (1.45 … 1.95), c∞ = 0.199 (0.188 … 0.207). **Verdict [measured]: band and tube accept one c∞ and one ξ
(c∞ = 0.2004, ξ = 1.95 units at K_t = 2); K_t = 1 is 7.7 worse in χ² than K_t = 2 but not excluded on its own (p =
0.27); K_t = 2 and 3 are equally good; free K_t is 2.5–3.3. So the trace reading passes with a multiplicity of 2
(or 3), not 1.** The band–tube constant it implies is not quite constant: (a_b − a_t) − ln[(1 + K_b e^(−w/ξ))/(1 +
K_t e^(−w/ξ))] rises by 0.07 from 5 to 6 units and 0.05 from 6 to 7 towards 4.07; measured 3.855 ± 0.022, 3.893 ±
0.053, 3.98 ± 0.20: compatible. The 192-cell tube separates the multiplicities (39.17, 39.01, 38.92), and the
blind 120-cell tube separates K_t = 1 (24.608) from 2 (24.571) and 3 (24.549) if it is good to ± 0.015. The
power-law rival (p = 0.75 ± 0.15 for tubes) says 24.557 and 38.86.

**Form** [measured as a description; the power law above is the rival]:

    ln τ_face(L) = a + 12·c∞·L − ln(1 + K·e^(−L/ξ)),   i.e.  1/τ = r·e^(−12 c∞ L)·(1 + K e^(−L/ξ)),
    c∞ = 0.2004 (0.199 … 0.202 across K = 1, 2, 3), K = 2, ξ = 1.95 lattice units  (tubes alone do not separate K
    from ξ; the bands fix ξ).

Answers to the brief's (c): **a flash**, ln τ = a(g) + c(g)·12L with a correction that dies off with length
(e^(−L/ξ) or p·ln L), not nucleate-and-sweep (§3, §4). c(12) = 0.199 (0.195 … 0.202) if the correction is
exponential; 0.187–0.194 if it is a power law. The discount of the long tube against the wide line is then at
least 0.2087 − 0.202 = 0.007 per cell and more likely 0.010 = 4.2 × f(12) (f(12) = 0.002317): the "1.85" (54–84
cells) and the "3.0" (84–108) are two points on the way to 3–4 or more, so the discount is **not** the density
deficit times one constant at every length. [measured, given the anchors] The wide-face line itself is straight
from 63 to 108 cells (0.2084 and 0.2084 on the two halves), although both loops of those tori are only 4.6–6 units,
the range in which a tube's price is still falling by 0.0015 per cell per unit: whatever lowers the price along a
tube does not act the same way when both loops grow together. I have no explanation. [open]

What ξ ≈ 2 units is [conjectured]: not the living state's correlation length (0.43 units); not a mixture of two
routes with different prices per cell in which boom and bust is the dearer one (that reading of K·e^(−L/ξ)
predicts a boom share of 14%, 9%, 6% at 60, 72, 84 cells; measured 57%, 56%); not an image sum over the period
lattice that would also apply to wide tori (`python3 imagefit.py`: adding −ln(1 + Σ_v e^(−|v|/ξ)) to the wrapping
law on 25 faces lowers χ² only from 357 to 302 at ξ = 1.2 and still leaves the 108-cell tube at −0.038 and the 6×6
torus at +0.043). A death lasts 4–6 generations from boom to the last cell and influence travels at most one cube
(1.41 units) per generation, so a correlation over about 2 units of the conditioned event is unsurprising; I
have no derivation.

Not done: c(g) for other girths (loop² 16 turned out to be a different problem, §7); nothing here bears on
rimmed faces.

## 6. The honest-dice surrogate and why forward flux failed on it [measured]

Surrogate: nl − 2 rule layers (the top one the face) over two layers of Bernoulli(53/128 = 0.414) cells redrawn
every generation (`ndice = 2`; the swarm used 0.4155). Offsets by brute force (`brute h k d nl 2 seed 500 gens`,
one face; lives whose face is frozen with period ≤ 2 for 256 generations or repeats after 840 are censored).
48 cells, w = 5 (`brute 4 0 4 7 2 41 500 8000000`): **9.9349 ± 0.0064** (24,213 deaths, 10 censored), i.e. **+0.010
± 0.006 against gump's 9.9251**, in line with the swarm's "within 0.015". (Without the period-840 test: 9.9574 ±
0.0041, +0.032: frozen faces of period > 2 inflate it, as in §1.) Other anchors: §7.

Forward flux (`ffs h k d nl 2 seed M delta N0`): basin = face population ≥ its mean, first level one standard
deviation below, levels every 2 cells down to 0, M trials per level from the pool of states that crossed the
level before; τ = 1/(flux × Π p). It is unbiased as the number of trials grows, and it reproduces brute force at
48 cells (mean of six replications 9.951 ± 0.028 against 9.9349 ± 0.0064). But replications of the whole estimator
(3·10⁵ trials per level at 48 cells, 7·10⁵ at 63 and 84; `data/ffs_replications.txt`):

| vessel | replications (ln τ_face) | gump |
|---|---|---|
| 48, (4,0),(0,4) | 9.952, 9.852, 10.034, 9.890, 9.967, 10.011 | 9.9251 |
| 63, (1,4),(0,21) | 13.216, 13.561, 13.071, 13.755 | 13.1622 |
| 84 tube, (1,12),(0,28) | 16.805, 18.278, 18.097, 18.520 | 17.3175 |
| 84 torus, (1,4),(0,28) | 15.703, 18.344, 17.583, 16.226 | 17.5387 |

Why: (i) dice drawn at generation t first touch the face at t + 3 (light cone through 5 rule layers), so clones
of one state have identical faces for 2 generations — I store the state of 2 generations before the crossing,
which halved the scatter at 48 cells (0.14 → 0.07) but no more; (ii) from one standard deviation below the mean to
the empty face takes 5–8 generations (`tdip` in the output); (iii) clone test, `tube1d clone 4 0 4 7 2 3 25 12
20000`: 20,000 states at their first crossing of population 12 (half), 64 clones each with fresh dice: mean
chance of death 0.0142, and var(q)/(q(1 − q)) = 0.48 — half of the outcome's variance is fixed by the state at the
crossing (0.56 at population 6); 17,905 of the 20,000 states gave no death in 64 clones. (iv) [from the PI's
anatomy] 57% of deaths are a boom followed by a one-generation bust that jumps every downward level at once, so the
levels have no leverage on the rare step. A repair would have to make the boom itself a stage (rate about e^(−6) at
63 cells, so e^(−0.1·A): reachable by brute force at 120 cells, not at 240) and would still meet (iii) in the
starving stage. Not attempted.

## 7. The living tube's population tails, the surrogate's offsets, other girths [measured]

**Tails of the stationary population against length** (`$S/tube1d pophist h k d 8 0 seed 3000000 500` for the
tubes of length 5, 7, 9, 12 (seeds 51–54) and 16 (seed 55, 2.5·10⁶ generations); `python3 tails.py data/ph_L5.txt
data/ph_L7.txt data/ph_L9.txt data/ph_L12.txt data/ph_L16.txt`; thresholds are exact fractions of A at every
length; local price = Δ(−ln P)/ΔA between consecutive lengths; errors naive, from counts):

| event | 5→7 | 7→9 | 9→12 | 12→16 |
|---|---:|---:|---:|---:|
| pop ≥ 7A/12 | 0.0102 | 0.0094 | 0.0087 | 0.0082 |
| pop ≥ 2A/3 | 0.0383 | 0.0371 | 0.0361 | 0.0353 |
| pop ≥ 3A/4 (the boom) | 0.0906 ± 0.0002 | 0.0884 ± 0.0006 | 0.0890 ± 0.0018 | 0.083 ± 0.010 |
| pop ≤ 5A/12 | 0.0154 | 0.0144 | 0.0137 | 0.0131 |
| pop ≤ A/3 | 0.0397 | 0.0378 | 0.0370 | 0.0361 |
| pop ≤ A/4 | 0.0750 ± 0.0001 | 0.0693 ± 0.0002 | 0.0692 ± 0.0005 | 0.0631 ± 0.0020 |
| pop ≤ A/6 | 0.1213 ± 0.0005 | 0.1086 ± 0.0018 | 0.115 ± 0.009 | |
| for comparison ln(A2/A1)/(2ΔA) | 0.0070 | 0.0052 | 0.0040 | 0.0030 |

Mean density 0.5154 and variance per cell 0.402 at every length from 7 units on (0.5153, 0.404 at 5).
Every tail's local price falls with length. For the over-full side and for mild depletion the fall is that of the
prefactor A^(−1/2) of the tail of a sum of nearly independent pieces (last row: falls of 0.0018, 0.0012, 0.0010
between successive columns; seen 0.0012, 0.0010, 0.0008 at 2A/3 and 0.0019, 0.0008, 0.0009 at A/3). Deep depletion
falls more (A/4: 0.0057 then 0.006 over the last two steps; A/6: 0.013). Block D: D1 (upper tail, more than 0.002
between 5→7 and 7→12): 0.0018 at both 2A/3 and 3A/4, **miss by a hair**; D2 (lower tail at A/3): 0.0024, **hit**.

What this suggests for §5 [conjectured]: a falling local price is what any tail probability with a power-law
prefactor shows, and `python3 tubefit.py` on the tube anchors gives τ ∝ L^p·e^(12cL) with **p = 0.75 ± 0.15**
(χ² = 0.08 for 2; c = 0.1937); p = 1/2 fixed: χ² = 2.9 for 3, c = 0.1970, 120-cell tube 24.584; p = 1 fixed: χ² =
3.0 for 3, c = 0.1904, 24.530. The wide-face line has no such prefactor (its two halves have the same slope to
0.0002, where p = 1/2 would make them differ by 0.0016). The 120-cell tube, to ± 0.012, separates p = 1/2 (24.584)
from p = 1 (24.530); the exponential forms sit between (24.545–24.571).

**Surrogate against gump** (`brute h k d 7 2 seed 500 gens`, w = 5, dice density 53/128):

| vessel | surrogate | gump | offset |
|---|---|---|---|
| (4,0),(0,4), 48 cells | 9.9349 ± 0.0064 (24,213 deaths) | 9.9251 ± 0.0004 | +0.010 ± 0.006 |
| (1,8),(0,20), 60-cell tube | 12.4268 ± 0.0198 (2,561 deaths) | 12.4166 ± 0.0031 | +0.010 ± 0.020 |

w = 6 at 48 cells (`brute 4 0 4 8 2 42 500 8000000`): 9.9264 ± 0.0064 (24,414 deaths), offset +0.001 ± 0.006: it
vanishes from w = 5 to w = 6 within errors. No sign that the offset moves with area or girth, on two vessels;
nothing at 63–96 cells (forward flux failed, brute force not run there); w = 8 not measured.

**Other girths: loop² 16 is another problem, because it can be cut** (`$S/tube1d bandp 4 0 14 8 0 5 10000000 500
16`, the 168-cell tube (4,0),(0,14), length 12.1; `data/bandp5_g16_L12.txt`). Empty bands there are not flashes:
−ln P(band empty) = 4.53, 5.11, 5.43, 5.79, 6.22, 6.77, 7.48, 8.47 at 1, 2, 3, 4, 5, 6, 7, 8 units (a price of
0.02–0.08 per cell), they last 21, 56, 111, 100, 82, 61, 43, 27 generations at 1.5, 2, 3, 4, 5, 6, 7, 8 units, every
bin of them has been empty for 32–63+ generations (the counter stops at 63) and no boom precedes them. These are
transverse firewalls (T3) and the dead stretches between two of them. 35 faces died in 6.4·10⁸ slab-generations
with nothing censored: **ln τ_face = 17.42 ± 0.17 for a 168-cell tube**, where the uncut price would give about 34
and the face-death-only numbers on file are 17.46 at 84 cells and 22.37 at 108 (firewalled lives censored). So for
this girth ln τ saturates with length: death by a local event. The brief's (a) for girths 4 and 3 is answered by
that, not by a price.
Through-cuts by hand (`$S/tube1d band h k d 8 0 78 3 600 4 8`: all 8 layers killed in a band of 3 units, 256
lanes; `data/cut_g*_w3.txt`): at loop² 12 the cut **heals** (gap 3.0, 2.3, 1.3 units at t = 0, 6, 12; all lanes
whole by t = 48); at loop² 16 it shrinks to 2.43 units by t = 24 and **stays at 2.43–2.47 for the 600 generations
watched, in every lane**: a firewall neither heals nor spreads; its edges stand still. [conjectured, from the
geometry] A transverse {111} layer meets the face along a kagome line, and it closes round the tube only if the
girth vector lies along such a line (loop² 9, 16, 25: the girths with firewalls on file); at loop² 12 and 13 it
winds along the whole tube, so there is nothing local to cut.
**Finite-length check** (`$S/tube1d bandp 1 38 80 8 0 6 8000000 500 14`: the 240-cell tube of length 20, one run,
4.1·10¹⁰ band-position-generations; `data/bandp5_g12_L20.txt`). −ln P(band empty) in the length-20 tube minus the
pooled length-12 value: +0.007, +0.014, +0.023, +0.031, +0.026 at 3, 3.5, 4, 4.5, 5 units (the pooled errors there
are 0.001, 0.002, 0.004, 0.010, 0.022), then −0.01, −0.11, −0.32, −0.69 at 5.5, 6, 6.5, 7 units (one run; with the
factor 2 on naive errors: ± 0.08, 0.15, 0.26, 0.4). So up to 5 units a band of the shorter tube is 1–3% likelier
and the length-20 prices are higher by 0.0007, 0.0012, 0.0015, 0.0012 per cell at 2.5–3 … 4–4.5 units (0.2293,
0.2235, 0.2205, 0.2177, then 0.2134 ± 0.004): a real but small finite-length effect, one tenth of the fall being
measured. Beyond 5.5 units one run cannot tell. The boom share falls the same way in the longer tube: 68.8, 60.5,
51.5, 44.1, 33.7 ± 3.5, 22.9 ± 5.4% at 3, 4, 5, 5.5, 6, 6.5 units (length 12: 68.8, 60.7, 52.6, 47.6, 43.3, 37.1), so
the take-over by thinning is not an artefact of the short tube.

**Loop² 13 behaves like loop² 12** (`$S/tube1d bandp 1 3 50 8 0 61 12000000 500 16`: the 150-cell tube
(1,3),(0,50), length 12.01, one run, 3.7·10¹⁰ band-position-generations; `data/bandp_g13_L12.txt`; 24 bins of
0.5004 units; errors naive, to be doubled from 4.5 units on as at loop² 12). Price per cell of an empty band:
0.2386 (2–2.5 units), 0.2286, 0.2201 ± 0.0008, 0.2195 ± 0.0016, 0.2217 ± 0.0031, 0.2104 ± 0.0060, 0.210 ± 0.012 at
2.5–3 … 5–5.5 units, against loop² 12's 0.2359, 0.2286, 0.2223, 0.2190, 0.2165, 0.2141, 0.2102: the same curve
within errors from 2.5 units on. A flash again (ages when a 5-unit band first is empty: 2.53 3.00 3.03 2.95 2.88;
complete emptiness lasts 1.7 generations); boom share 68.2, 60.5, 56.0 ± 1.7, 52 ± 3% at 3, 4, 5, 5.5 units (loop² 12:
68.8, 60.7, 52.6, 47.6). Band–tube constant against the tubes on file (band widths interpolated to the tubes'
lengths 4.80 and 5.77; 6.005 is exact): −ln P(band) − ln τ_face = 16.507 − 12.4465 = 4.06 ± 0.05, 19.05 − 14.9213 =
4.12 ± 0.15, 19.686 − 15.5250 = 4.16 ± 0.26: constant again, and 0.2 above loop² 12's 3.86, about what two edges
longer by the ratio of the girths would add if the constant is 2σg (3.86 × 3.606/3.464 = 4.02). c∞(13) and ξ(13)
were not fitted (one band run, three tube anchors up to 6 units). Block E: all four forecasts hit.

Note on bins: before 04:27 `bandp` used bins of exactly 0.5 units, which leaves a sliver bin when the length is not
a multiple of 0.5; a first loop²-13 run (discarded) was biased by it, and the loop²-16 run above has a short last
bin of 0.12 units (its conclusions do not hang on that). Bins now tile the tube exactly; the loop²-12 runs
(lengths 12 and 20) are unaffected.

So c∞(g) and ξ(g) of §5 exist only for loop² 12 here; loop² 13 shares its band curve where measured; at loop² 16
the band statistic measures firewalls (it would need lanes with a firewall censored, which `bandp` does not do);
loop² 9 was not run.

## 8. Data formats (for other agents)

- `data/paths_*.txt` (reactive paths, deterministic gump, brute force): one line per face death:
  `age face lag[0] … lag[A−1]`. `age` = generations since the lane was restarted; `face` 0 = top layer, 1 = bottom;
  `lag[c]` = number of generations before the first empty generation at which face cell c was last alive
  (1 = alive in the last living generation; −1 = not alive in the last 255). Cell c of the face is
  (a, x, y) with c = (a·h + x)·d + y; positions from `tube1d geom h k d nl` (columns: c a x y, then ξ and η —
  along the axis and round the girth, lattice units — for the top face, then for the bottom face).
- `data/paths_*.txt.pop`: same lines, `age face pop[0] … pop[23]`, the dying face's population 0, 1, … 23
  generations before the first empty generation (pop[0] = 0).
- `data/bandp*.txt`: `width cells count P −lnP err appearances mean_duration`, then `AGE` and `PRE` lines
  described in their own header lines.

## 9. Not checked

- No lifetime beyond 9 units was measured; every number for L ≥ 10 is an extrapolation of §5.
- Bands were measured in a tube of length 12 only, up to 7 units (5 units of living tube left at the widest); the
  length-20 check was not run. Windows are aligned to 0.5-unit bins of the axis coordinate. Brute force gains
  half a unit of width per factor 3.5 of computing: 8 units needs about 10¹² band-position-generations (five
  times what I ran), 10 units 10¹⁴; no estimator here goes further.
- The joint fits treat the band slopes as independent with errors from five runs (floored at 0.0005) and ignore
  everything below 3 units, where more than one sub-leading term must matter.
- The paths are from one or two seeds per vessel; the 84-cell statistics rest on 323 deaths (113 with population series).
- The settled test catches periods dividing 840 and period ≤ 2 only.
- The 96-cell anchor (1,17),(0,32) is a tube with half a twist; twisted tubes on file live 0.003–0.014 longer at
  48–72 cells. Not corrected in the fits of §5.
- The surrogate's offset was measured at 48 cells (and 60, §7) only; nothing about its dependence on area or girth
  beyond that; the dice density is 0.414, not the swarm's 0.4155.
- `imagefit.py` uses the density deficits f as given in the brief and floors errors at 0.003.
