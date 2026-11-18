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

1. **A tube dies as a whole, in a flash; no band dies first and no front sweeps** [measured, §4]. In 203 deaths of
   the 84-cell tube the typical cell is last alive 6 generations before the end and the earliest tenth 7.7; no
   band right round the girth is finally empty 4 generations before the median cell in more than 2% of deaths;
   death times of 0.5-unit bands differ by 1.2 generations r.m.s. however far apart they are along the tube. What
   lingers is a last clump of about 6 cells for 5–6 generations (which is why a "band empty ≥ 4 generations before
   the last cell" criterion reads 60–72% for a flash).
2. **The same holds for a band of a long living tube** [measured, §3]: when a band of width w ≤ 6 units of a
   144-cell tube is momentarily empty, every 0.5-unit bin of it has been empty for 2.4–3.2 generations, edge and
   middle alike, and complete emptiness lasts 1.7 generations whatever the width (it refills from its edges at once).
3. **The price of emptying one more unit of tube falls with the length already emptied, and bands and whole tubes
   lie on one curve** [measured, §3, §5]. Marginal price per cell of an empty band: 0.2365 at 2–2.5 units, 0.2285,
   0.2223, 0.2181 ± 0.0009, 0.2137 ± 0.0018, 0.2103 ± 0.0033, 0.204 ± 0.006 at 3, 3.5, 4, 4.5, 5, 5.5 units; whole
   tubes (anchors): 0.2049, 0.2035, 0.2019, 0.2013 from 5→6 … 8→9 units. And −ln P(band of width w empty) −
   ln τ_face(tube of length w) = 3.809 ± 0.018, 3.80 ± 0.06, 3.86 ± 0.20 at w = 5, 6, 7: a constant. One curve
   price(ℓ) = c∞ + B·e^(−ℓ/ξ) fits all twelve slopes (χ² = 4.5 for 9): **c∞ = 0.1989 (0.1978 … 0.1997), ξ = 2.05
   (1.85 … 2.30) lattice units, B = 0.114**. **But a power-law prefactor fits them too** (χ² = 8.1 for 10):
   τ ∝ ℓ^p·e^(12cℓ) with p = 1.39 ± 0.04, c = 0.1863 ± 0.0008. So the price of a loop²-12 tube does not return to
   the wide price 0.2087 and does not fall as a parabola; whether it levels at 0.199 or creeps down to 0.186 the
   data cannot say. The 120-cell tube will not say either (24.556 against 24.538); 192 cells would (39.0 against
   38.6).
4. **Boom and bust does not change with tube length up to 6 units, but loses ground to thinning in bands**
   [measured, §4]: the share of deaths with a one-generation fall of at least half the face is 59.3 ± 2.0%, 56.7 ±
   1.1%, 56.3 ± 1.7% at 48 (4×4), 60 and 72 cells (tubes of length 5 and 6; 84 cells in §7). My forecast that it
   falls with length (block C) was wrong there. In bands of a living tube the same criterion gives 77% at 2
   units, 60.5% at 4, 52 ± 1% at 5, 47 ± 4% at 6: a second route (thinning over 3–4 generations, no over-filling)
   takes over with width.
5. **Forward-flux sampling on the face population does not work on the honest-dice surrogate, and I can say why**
   [measured, §6]: the dice need 3 generations to reach the face, a death takes 5–8 from one standard deviation
   below the mean, and half of the variance of the outcome is already decided by the state when the population
   first crosses half (clone test). Replications of the whole estimator scatter by 0.07 at 48 cells, 0.3 at 63,
   0.75–1.2 at 84 (7×10⁵ trials per level), biased upward. **No lifetime of a tube longer than 9 units was
   measured here.** The curves beyond are extrapolations of item 3.

Forecast frozen for the blind 120-cell tube (block B, commit 9a1ccc4, 03:46): **24.563 ± 0.030** (an extrapolation,
not independent of the PI's block 0). The one-curve fit made afterwards gives 24.556, the two-route form 24.56–24.57.

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

`$S/tube1d bandp 1 22 48 8 0 5 20000000 500 16` (deterministic gump, 144-cell tube, both faces, 2·10⁷
generations × 64 lanes, 6.1·10¹⁰ band-position-generations; `data/bandp_g12_L12.txt`; slopes by
`python3 bandfit.py data/bandp_g12_L12.txt`). A window of m bins of 0.5 units (6 cells each) is "empty" when none of
its cells is alive. err = 1/√(number of separate appearances).

| width (units) | cells | −ln P(empty) | err | price per cell from the previous width | appearances | mean duration (gens) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 6 | 3.6264 | 0.0000 | | 1.2·10⁹ | 1.35 |
| 1.0 | 12 | 5.4855 | 0.0001 | 0.3099 | 1.4·10⁸ | 1.81 |
| 1.5 | 18 | 6.8325 | 0.0002 | 0.2245 | 3.7·10⁷ | 1.79 |
| 2.0 | 24 | 8.2534 | 0.0003 | 0.2368 | 9.2·10⁶ | 1.74 |
| 2.5 | 30 | 9.6687 | 0.0007 | 0.2359 | 2.3·10⁶ | 1.71 |
| 3.0 | 36 | 11.0394 | 0.0013 | 0.2285 ± 0.0002 | 581,384 | 1.70 |
| 3.5 | 42 | 12.3732 | 0.0025 | 0.2223 ± 0.0005 | 154,147 | 1.69 |
| 4.0 | 48 | 13.6819 | 0.0049 | 0.2181 ± 0.0009 | 41,798 | 1.68 |
| 4.5 | 54 | 14.9638 | 0.0093 | 0.2137 ± 0.0018 | 11,573 | 1.68 |
| 5.0 | 60 | 16.2254 | 0.0175 | 0.2103 ± 0.0033 | 3,268 | 1.69 |
| 5.5 | 66 | 17.4505 | 0.0320 | 0.2042 ± 0.0061 | 974 | 1.66 |
| 6.0 | 72 | 18.6780 | 0.0579 | 0.2046 ± 0.0110 | 298 | 1.59 |
| 6.5 | 78 | 19.9661 | 0.1072 | 0.215 ± 0.020 | 87 | 1.51 |
| 7.0 | 84 | 21.178 | 0.204 | 0.202 ± 0.038 | 24 | 1.6 |
| 7.5 | 90 | 22.44 | 0.38 | | 7 | |

- **The price is not constant**: a plateau at 0.2365 (2–2.5 units), then a steady fall, 0.2082 ± 0.0024 from 4 to 6
  units (forecast A1: 0.205 ± 0.015, hit).
- **The band and the tube are the same object** [measured]: −ln P(band w) − ln τ_face(tube of length w) = 16.2254 −
  12.4166 = 3.809 ± 0.018 (5 units), 18.678 − 14.8753 = 3.803 ± 0.060 (6), 21.178 − 17.3175 = 3.86 ± 0.20 (7).
  [conjectured] The constant is two edges plus a duration: with 1.7 generations of emptiness and 0.5-unit positions,
  2σg ≈ 3.8 gives σ ≈ 0.55 per lattice unit of edge, near the 0.66 the PI quotes for patches.
- **A flash, not a hole that grew** (`AGE` lines of the output, `data/bandp5_g12_L12.txt`): number of generations
  each 0.5-bin had been empty when the window first was, from the edge bin to the middle: 4 units 2.42 2.88 2.82
  2.77; 5 units 2.95 3.19 3.01 2.85 2.78 (pilot of 3·10⁵ generations; the long run is in the data file). A hole
  growing at u units per generation would show (w/2)/u more in the middle than at the edge.
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

Other girths, a longer tube (finite-length check) and the long run with histories: §7 (filled as the jobs end).

## 4. How a tube dies: reactive paths [measured]

`$S/tube1d brute 1 12 28 8 0 7 500 60000000 paths_1_12_28.txt` (stopped at 203 face deaths) and
`python3 paths.py $S/tube1d 1 12 28 8 data/paths_1_12_28.txt`; lag = generations before the death at which a cell
was last alive (format in §8). Numbers below at 106 deaths, unchanged within errors at 203:

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
| (1,12),(0,28) tube, length 7 | 84 | §7 | §7 | |

Block C forecast (48, 37, 27% at 60, 72, 84 cells): **wrong at 60 and 72**; the "no trend" alternative, to which
I gave 20%, is what whole tubes show up to 6 units.

**Bands are different** (`PRE` lines of `data/bandp5_g12_L12.txt`, 1.2·10⁷ generations): the share of
band-emptying events with a one-generation fall of at least half the band's cells in the band's last 9
generations falls steadily with width: 82.0% (1 unit), 77.1% (2), 73.0% (2.5), 68.7% (3), 64.4% (3.5), 60.5% (4;
24,993 events), 56.2% (4.5), 52.1 ± 1.2% (5; 1,834), 48.1 ± 2.3% (5.5), 46.7 ± 4.1% (6; 150), 40 ± 7% (6.5), 31 ±
13% (7). (A pilot of 10⁵ generations had suggested it levels at 63%; it does not.) The other events are a
thinning over 3–4 generations with no over-filling. Mean density of a 5-unit band 1, 2, … 7 generations before it
first is empty: 0.039, 0.117, 0.302, 0.429, 0.478, 0.495, 0.508 (stationary 0.5155). In log-odds the share falls by
0.43, 0.36, 0.34, 0.21 per unit from 2 to 6 units: in a band the boom-and-bust route costs about 0.03 per cell more
than thinning. That shift accounts for part of the band's falling price, not all (the thinning route's own price,
price − share × 0.031, still falls: 0.2065, 0.2017, 0.1956, 0.1936 at 2.75, 3.25, 4.25, 4.75 units).

So the falling price of a **whole tube** up to 6 units is not a change of route (not band-first, not a sweep, no
shift between boom-and-bust and thinning), while in a **band** of a living tube thinning gains on boom and bust
with width. Whether whole tubes follow at 7 units and beyond: §7. [measured]

## 5. The one-dimensional form [measured fits; the reading is conjecture]

Anchors for loop² 12 (lengths 5…9): 12.4166 ± 0.0031, 14.8753 ± 0.0140, 17.3175 ± 0.0031, 19.7405 ± 0.0059,
22.1557 ± 0.0121. `python3 tubefit.py`:

- a straight line fails: χ² = 26.0 for 3.
- ln τ(L) = a + s·L − ln(1 + K·e^(−L/ξ)) fits: χ² = 0.07 for 2 at K = 2, ξ = 2.4, s/12 = 0.1992; χ² = 0.31 at K = 2,
  ξ = 2.0 (s/12 = 0.2003); K = 4, ξ = 1.4: 0.15 (0.2009); K free: 2.2, ξ = 2.05 (0.1998). The anchors alone do not
  separate K from ξ. Forecasts along the valley: L = 10: 24.56–24.57; 12: 29.36–29.39; 16: 38.93–39.04; 20:
  48.50–48.68; 30: 72.4–72.8.
- `python3 margfit.py data/bandp_g12_L12.txt`: band slopes (2.5–6.5 units) and tube slopes (5–9) together,
  price(ℓ) = c∞ + B·e^(−ℓ/ξ): χ² = 4.50 for 9; c∞ = 0.1989 (0.1978 … 0.1997 over χ² + 1), ξ = 2.05 (1.85 … 2.30),
  B = 0.114; the worst point is the tube's 5→6 (−1.6 σ). Tube alone: c∞ = 0.199 (0.195 … 0.202), ξ unconstrained.
  Curve at 10, 12, 16, 20 units: 0.1998, 0.1992, 0.1989, 0.1989; 120-cell tube: 22.1557 + 12 × 0.2001 = 24.556.

- The same script, power law instead: price = c + p·ln(ℓ2/ℓ1)/(12(ℓ2 − ℓ1)), i.e. τ ∝ ℓ^p·e^(12cℓ): bands + tubes
  χ² = 8.05 for 10, c = 0.1863 ± 0.0008, p = 1.39 ± 0.04 (worst point again the tube's 5→6, −2.2 σ); bands alone
  p = 1.34 ± 0.11, c = 0.188 ± 0.003; tubes alone p = 0.72 ± 0.27, c = 0.194 ± 0.003. Its forecasts: L = 10: 24.538
  (tubes alone 24.560); 12: 29.26 (29.35); 16: 38.61 (38.87); 20: 47.86 (48.34); 30: 70.78 (71.91). **The two forms
  agree to 0.02 at 120 cells and part by 0.1–0.4 at 192 cells and 0.2–0.8 at 240**: the PI's "prefactors can fake
  prices" applies to my c∞ in full.

**Form** [measured as a description, three numbers; ξ comes from the bands, so one number c∞ and one intercept are
fitted to the tubes; the power law above is the rival with one number fewer]:

    ln τ_face(L) = a + 12·c∞·L − 12·B·ξ·e^(−L/ξ),   c∞ = 0.199, ξ = 2.05, B = 0.114 (bands), or equivalently
    1/τ = r·e^(−12 c∞ L)·(1 + K e^(−L/ξ)) with K ≈ 2.

Answers to the brief's (c): **a flash**, ln τ = a(g) + c(g)·12L with a correction that dies off with length
(e^(−L/ξ) or p·ln L), not nucleate-and-sweep (§3, §4). c(12) = 0.199 ± 0.001 if the correction is exponential and
bands and tubes share the curve (they do where both are measured, 5–7 units); 0.186–0.194 if it is a power law.
The discount of the long tube against the wide line is then at least 0.2087 − 0.199 = 0.0097 per cell = 4.2 × f(12)
(f(12) = 0.002317): the "1.85" (54–84 cells) and the "3.0" (84–108) are two points on the way to 4 or more, so the
discount is **not** the density deficit times a constant at any one length. [measured, given the anchors]

What ξ ≈ 2 units is [conjectured]: not the living state's correlation length (0.43 units); not a mixture of two
routes with different prices per cell in which boom and bust is the dearer one (that reading of K·e^(−L/ξ)
predicts a boom share of 14%, 9%, 6% at 60, 72, 84 cells; measured 57%, 56%); not an image sum over the period
lattice that would also apply to wide tori (`python3 imagefit.py`: adding −ln(1 + Σ_v e^(−|v|/ξ)) to the wrapping
law on 25 faces lowers χ² only from 357 to 302 at ξ = 1.2 and still leaves the 108-cell tube at −0.038 and the 6×6
torus at +0.043). A death lasts 4–6 generations from boom to the last cell and influence travels at most one cube
(1.41 units) per generation, so a correlation over about 2 units of the conditioned event is unsurprising; I
have no derivation.

Not done: c(g) for other girths (bands at loop² 16, 13, 9 are in §7 if the jobs ended); nothing here bears on
rimmed faces.

## 6. The honest-dice surrogate and why forward flux failed on it [measured]

Surrogate: nl − 2 rule layers (the top one the face) over two layers of Bernoulli(53/128 = 0.414) cells redrawn
every generation (`ndice = 2`; the swarm used 0.4155). Offsets by brute force (`brute h k d nl 2 seed 500 gens`,
one face, lives with a frozen face censored): see §7 for the final table. First run, 48 cells, w = 5: 9.9574 ±
0.0041 (59,217 deaths), i.e. **+0.032 ± 0.004 above gump's 9.9251** (the swarm quoted "within 0.015").

Forward flux (`ffs h k d nl 2 seed M delta N0`): basin = face population ≥ its mean, first level one standard
deviation below, levels every 2 cells down to 0, M trials per level from the pool of states that crossed the
level before; τ = 1/(flux × Π p). It is unbiased as the number of trials grows, and it reproduces brute force at
48 cells (mean of six replications 9.951 ± 0.028 against 9.9574 ± 0.0041). But replications of the whole estimator
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

## 7. Late results

(filled below as jobs end; see the git log)

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
- Bands were measured in a tube of length 12 only up to 7.5 units (4 units of living tube left at the widest); the
  length-20 check is in §7 if it ended. Windows are aligned to 0.5-unit bins of the axis coordinate.
- The paths are from one seed per vessel; the 84-cell statistics rest on 203 deaths.
- The settled test catches periods dividing 840 and period ≤ 2 only.
- The surrogate's offset was measured at 48 cells (and 60, §7) only; nothing about its dependence on area or girth
  beyond that; the dice density is 0.414, not the swarm's 0.4155.
- `imagefit.py` uses the density deficits f as given in the brief and floors errors at 0.003.
