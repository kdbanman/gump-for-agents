# research/blast/split-slab: rare-event samplers for wrapped faces (agent split-slab, 2026-11-18)

Brief: build a multilevel-splitting sampler for gump's wrapped faces (8-layer slab tori), calibrate it on the
anchors, reach 120 cells and beyond. What came out, in order of how far I trust it:

1. **[measured] A stepper that is bit-exact against the oracle on nine tori** (section 1), and brute-force
   lifetimes from it that agree with the anchors at 48, 63, 78 and 84 cells.
2. **[measured] Splitting on the face population cannot beat brute force on gump** (section 3): cloned
   trajectories either copy their parent (flips deep in the chaos) or are biased towards longer life (flips that
   act in time: +0.04 per level-flip at depth 3-4, +0.2 at depth 2). The reason is section 4.
3. **[measured] A wrapped face dies by boom and bust** (section 4; found independently of agent `anatomy`, same
   numbers): from an ordinary population it over-fills in ONE generation (median 47 of 63 cells, mean + 2.8 sd),
   overcrowding empties it in the next (to 14), and the scattered remnant starves in about 4 more. Nothing
   beneath the face announces it; the face leads and the layers under it follow.
4. **[measured + conjectured continuation] The 120-cell tube (1,18),(0,40): ln tau_face = 24.59 ± 0.05**, the
   forecast of record (section 5, `PREDICTIONS.md` block 3, commit 2398569), from exact bookkeeping
   1/tau = nu(p) q(p): nu measured at 120 cells, q continued from the anchors at 84, 96, 108. The same procedure
   run blind on the 108-cell tube gave 22.171 ± 0.057 against 22.1599.
5. **[measured] A sampler that does work, on a surrogate** (section 6): subset simulation over the coin flips of
   the *dice chain* (6 layers of gump over 2 layers of fair coins; brute force puts it within 0.02 of gump at 48 and
   63 cells). Exact for that chain; results and its calibration against the gump anchors are in section 6.

Marks: **[proved]**, **[measured]**, **[conjectured]**. Runs used one core (the machine gave it 40-50%).
`G/` = `research/scratch/blast/split-slab/`; build and geometry:

    gcc -O3 -march=native -o G/ss research/blast/split-slab/ss.c -lm      # the same binary is called ss_lag, ss_sub below
    python3 geom.py H K D G/g_H_K_D.bin                                    # torus (H,K),(0,D): A = 3 H D cells per layer

## 1. Stepper and validation [measured]

`geom.py` builds the slab graph from `docs/AUTOMATON.md` alone: cube index (i, j, k), layer l = i + j + k in 0..7,
in-plane period lattice (H, K), (0, D) acting by cube translations (x, y, -x - y); cell id
((l H D + i' D + j') 3 + a); it asserts T1's layer histogram and the symmetry of the neighbour relation.
`ss.c` steps 512 lanes bit-sliced (carry-save count of the 12 neighbours, B45/S345).

    python3 validate.py H K D 1200 [N]        # log of all runs: data/validate.log

A 0.4 soup on the slab torus, tiled into `reference/oracle.py`'s cubic torus of N^3 cubes (N = H D; 12 for
(4,0),(0,4) and (6,0),(0,6)), must equal the oracle's array **as a set of cells at every generation 0..1200**, for
two lanes of `ss` (lanes 0 and 311, different soups) and for a numpy stepper on the same graph. Negative control:
one neighbour entry replaced; must fail. **MATCH on all nine tori**: (4,0),(0,4); (1,4),(0,21); (1,6),(0,26);
(1,12),(0,28); (1,4),(0,28); (1,17),(0,32); (1,16),(0,36); (6,0),(0,6); (1,18),(0,40). The swapped graph is
detected on every one (first mismatch at generation 7 to 19).
Not validated against the oracle: the tori (1,22),(0,48), (1,30),(0,64), (1,38),(0,80), (8,0),(0,8) of section 6
(same builder, its internal asserts only), and the event bookkeeping, which is checked by these lifetimes:

| torus | cells | brute force here (face deaths) | anchor | command |
|---|---:|---|---|---|
| (4,0),(0,4) | 48 | 9.9197 ± 0.0067 (22,234) | 9.9251 ± 0.0004 | `ss G/g_4_0_4.bin ffs 21 128 20 11 3 8192 8192 1 5 6 0`, line FLUXSTAGE |
| (1,4),(0,21) | 63 | 13.1852 ± 0.0293 (1,161) | 13.1622 ± 0.0007 | `ss G/g_1_4_21.bin ffs 21 128 27 17 3 8192 8192 1 5 6 0`, line FLUXSTAGE |
| (1,6),(0,26) | 78 | 16.069 ± 0.044 (527) | 16.0932 ± 0.0093 | `ss G/g_1_6_26.bin plain 101 5000000 34 23` |
| (1,12),(0,28) | 84 | 17.33 ± 0.12 (75) | 17.3175 ± 0.0031 | `ss G/g_1_12_28.bin plain 101 2500000 37 26` |

Conventions: lives start from a 0.4 soup with 1,000 generations of burn-in (the brute-force rows of the anchors
have none), end at the first face death, are cut at age 50,000 (a guard against settled lanes); tau_face =
face-generations / face deaths. Transverse firewalls are not detected (none is expected in runs this short: the
card saw 0 on these tubes and 298 against 18,394 deaths at 6 x 6); a settled lane is not detected either.

## 2. The splitting sampler: exact statement

    ss G/g.bin ffs SEED NREP PA LAM0 DELTA M N0TGT NFLIP FDEP0 FDEP1 NPATH [PATHFILE]

- Level function: the population p of one face layer (layer 0 or layer 7). Basin {p >= PA}. Levels
  lam_0 = LAM0 > lam_1 = LAM0 - DELTA > ... (while positive), last level 0 (the face is dead).
- Stage 0 (exact, no perturbation): 512 lanes of plain gump. For each lane and face, a *crossing* is the first
  generation with p <= lam_0 since the face was last >= PA. Phi = crossings / face-generations. The slab state at
  each crossing is stored (the first M of a window). The same pass books every excursion's minimum (until the face
  is back at >= PA, or dead): nu(p) = excursions with minimum <= p per face-generation, and E / deaths. One
  persistent ensemble; replication r uses its r-th window (at least N0TGT crossings, checked every 64 generations).
- Stage i = 1..n: M trials. Trial j takes parent (r0 + j) mod S_{i-1} of the S_{i-1} states stored at level
  i-1 (r0 uniform), flips NFLIP cells, each uniform over the layers at depth FDEP0..FDEP1 beneath the active face
  (depth d = layer d for face 0, layer 7 - d for face 1), and runs plain gump until the active face has
  p <= lam_i (success; state stored) or p >= PA (failure; also failure after 1,000 generations).
  P_i = successes / M. A parent already at p <= lam_i is an immediate success (flips applied).
- Estimate: 1/tau_face = Phi * prod P_i. Error: NREP independent replications of the whole estimator, the mean
  of their rates and the standard error from their scatter; never a binomial formula.
- `WD=w ss ...` runs everything on the *dice chain*: layers 0..w-1 on the rule, layers w and w+1 replaced after
  every generation by fair coin flips, one face (layer 0). A true Markov chain; NFLIP = 0 there.

## 3. Why splitting on the face population fails [measured]

**(a) Flips deep in the chaos are unbiased and useless.** One flip at depth 5-6 (the far side of the slab):

| torus | split estimate | brute force in the same windows | anchor | sd of one replication | natural deaths per replication |
|---|---|---|---|---:|---:|
| 48 cells | 9.9228 ± 0.0063 | 9.9197 ± 0.0067 | 9.9251 | 0.07 | 174 |
| 63 cells | 13.181 ± 0.028 | 13.185 ± 0.029 | 13.1622 | 0.32 | 9.1 (1/sqrt = 0.33) |

(commands: the two `ffs` lines of section 1.) The estimate agrees with the brute-force count of *its own*
stage-0 windows ten times better than either agrees with the truth, and its scatter is the Poisson scatter of the
natural deaths: every clone repeats its parent. Started from a shallow level, where a replication contains 0.1
to 0.3 natural deaths, the relative sd of one replication is 1.8 to 2.2, for gump with one flip at depth 5-6 or
3-4 and equally for the dice chains WD = 3 and 5, where clones are separated by honest dice:
`[WD=w] ss G/g_1_4_21.bin ffs 51 48 33 27 3 8192 8192 NFLIP D0 D1 0` (NFLIP 1, depths 5 6 or 3 4; WD=3 or 5 with NFLIP 0).

**(b) Flips that act in time are biased towards longer life.** 63 cells, 64 replications on the same stage-0
windows (in-sample brute force 13.176 ± 0.041, anchor 13.1622): 8 flips at depth 5-6: 13.180 ± 0.031; 63 flips at
depth 5-6: 13.221 ± 0.031; 63 flips at depth 4-5: 13.291 ± 0.036
(`ss G/g_1_4_21.bin ffs 31 64 27 17 3 8192 8192 NFLIP D0 D1 0`). At 48 cells (anchor 9.9251; levels 17, 14, ..., 0
from PA = 24; 256 replications of M = 8192 for the first two rows, 32 of M = 16384 for the rest; run with a build
of `ss.c` before the persistent stage-0 ensemble, so reproducible statistically, not digit for digit, by
`ss G/g_4_0_4.bin ffs 11 256 24 17 3 8192 8192 NFLIP D0 D1 0`):

| flips per clone, depth | ln tau_face | minus anchor |
|---|---|---|
| 1, depth 5-6 | 9.925 ± 0.015 | 0.000 |
| 1, depth 3-4 | 9.965 ± 0.015 | +0.040 |
| 6, depth 3-4 | 10.105 ± 0.027 | +0.18 |
| 24, depth 3-4 | 10.300 ± 0.032 | +0.37 |
| 1, depth 2 | 10.119 ± 0.033 | +0.19 |
| 6, depth 1-2 | 11.73 ± 0.04 | +1.8 |

The sign is always the same: a flip rescues a dying face far more often than it dooms a living one. A flip moves
the local density towards 1/2; under a face that has just crashed the layers are depleted (z = -2.5 one layer
down), so there a flip is a source of live cells. A perturbation is harmless only where the state is stationary,
and by then (section 4) it is too late to matter. **Bias I can exclude for the deep-flip version: 0.03 at 48
cells (2 sd); but that version is brute force with extra steps.**

**(c) Why.** The whole event takes about 6 generations from a normal-looking state, the levels of a downward
ladder are all jumped in the single generation of the crash, and information from 3 or more layers down needs 2
or more generations to reach the face. There is no slow precursor to split on (section 4).

## 4. How a wrapped face dies [measured]

Natural deaths of plain gump, no flips: `ss_lag G/g.bin lag 3 GENS data/paths_H_K_D.txt > data/lag_H_K_D.txt`
(GENS = 30000 at 48 cells: 1,268 deaths; 400000 at 63 cells: 770 deaths), then
`python3 howdie.py H K D data/paths_H_K_D.txt` (outputs in `data/howdie_*.txt`).

| | 48 cells (4,0),(0,4) | 63 cells (1,4),(0,21) |
|---|---|---|
| stationary face population | 24.7 ± 4.5 | 32.6 ± 4.9 |
| largest one-generation fall in the last 24 generations (median) | 25 cells, from 36 to 11 | 33 cells, from 47 to 14 |
| population at the top of that fall | mean + 2.5 sd = 0.75 A | mean + 2.8 sd = 0.75 A |
| deaths whose fall starts above mean + 1.5 sd / + 2 sd | 92% / 78% | 95% / 88% |
| deaths with a one-generation fall of at least A/2 / at least 0.4 A | 59.5% / 82% | 55.8% / 82% |
| the fall ends this many generations before the death (median; 10%..90%) | 4; 2..10 | 4; 2..9 |
| mean population, 6 generations before the fall to 4 after | 24.5 24.7 25.9 23.8 25.1 **35.5 \| 10.7** 6.2 4.4 4.1 4.3 | 32.3 32.5 34.0 31.1 33.0 **46.3 \| 14.3** 7.8 4.8 3.8 3.9 |
| share of the face's cells last alive in one and the same generation (median) | 0.52 | 0.52 |

- The generation before the boom has an ordinary population (25.1, 33.0): the boom is one step, so it is a
  property of the *arrangement*, not of the count. Agent `anatomy` reports 57-59% for the A/2 criterion; here
  59.5% and 55.8%.
- By lag before the death (63 cells, `data/lag_1_4_21.txt`): the mean population of the dying face is within
  0.3 sd of stationary until 9 generations before, then z = -0.6, -0.8, -1.3, -1.8, -2.8, -4.3, -5.7, -6.2 at lags
  8..1. The layer beneath follows *behind* (z = -0.4, -0.3, -0.8, -0.9, -1.5, -2.2, -2.7, -2.5), the second layer
  further behind (-1.1 at lags 2-3), and depths 3 to 7 never leave ± 0.5. The spread of the dying face's
  population at lags 3-5 is 14 to 17 cells against 4.9 stationary: two populations (not yet crashed, crashed),
  which is why a mean profile shows a "dip that deepens" that no single face follows.
- Both tori die as one piece: the two halves of the face along its longer period have the same median last-alive
  generation in 93% (48) and 96% (63) of deaths.
- **[conjectured]** Consequence for the theory: the rate is (rate of over-full generations) x (chance the crash
  leaves no clump able to regrow anywhere on the face). The second factor is a void probability and would be
  exponential in area by itself; shape would enter through how the remnant clumps see the short loops. I did not
  test this. Not checked on gump beyond 63 cells (section 6 has the dice chain's paths at larger sizes).

## 5. The 120-cell tube from exact bookkeeping [measured; the continuation of q is conjectured]

1/tau = nu(p) q(p) holds exactly at every level p (each death ends one excursion). nu_A(p) costs only plain
running: `ss G/g.bin plain 101 GENS PA LAM0` with PA = round(0.515 A - s), LAM0 = round(0.515 A - 3 s),
s = sqrt(0.415 A) (`chain_tube.sh`; outputs `data/plain_*.txt`, HIST lines: cum = excursions with minimum <= p).
q_A(p) = 1/(tau_A nu_A(p)) at the anchors moves slowly with size at fixed p (-0.013 to -0.025 per cell, against
0.20 per cell for ln tau), so it can be continued a short way: `nuq.py` puts a straight line in A through three
anchor sizes, `nuq_quad.py` a parabola.

| target | anchors used | level p (excursions at the target) | straight line (frozen procedure) | parabola (written after the test) | truth |
|---|---|---|---|---|---|
| 108 cells, blind test | 78, 84, 96 | 14 (430) | **22.171 ± 0.057** | 22.165 ± 0.087 | 22.1599 ± 0.0086 |
| | | 18 (3,113) | 22.213 ± 0.023 | 22.174 ± 0.044 | |
| | | 22 (22,002) | 22.216 ± 0.012 | 22.136 ± 0.034 | |
| **120 cells** | 84, 96, 108 | 18 (508) | **24.636 ± 0.052** | 24.562 ± 0.078 | GPU, about 13:00 UTC |
| | | 22 (3,837) | 24.621 ± 0.022 | 24.556 ± 0.040 | |
| | | 26 (25,646) | 24.662 ± 0.014 | 24.557 ± 0.031 | |

    python3 nuq.py data/plain_1_16_36_s101.txt data/plain_1_6_26_s101.txt:16.0932:0.0093 data/plain_1_12_28_s101.txt:17.3175:0.0031 data/plain_1_17_32_s101.txt:19.7446:0.0042
    python3 nuq.py data/plain_1_18_40_s101.txt data/plain_1_12_28_s101.txt:17.3175:0.0031 data/plain_1_17_32_s101.txt:19.7446:0.0042 data/plain_1_16_36_s101.txt:22.1599:0.0086
    (nuq_quad.py: same arguments; outputs in data/nuq_*.txt)

- The straight line was frozen before either run (`PREDICTIONS.md` block 1) and passed its test at the level of
  record (+0.011 ± 0.058). At shallower levels it overshoots by 0.04 to 0.06 (4 sd): ln q_A(p) is convex in A (the
  middle anchor lies 0.01 to 0.02 below the chord). The parabola is unbiased on the test at every level
  (22.12 to 22.18) but was chosen after seeing it.
- At 120 cells the level of record sits where the test's overshooting levels sat (ln q about -8.4), so I put
  the forecast between the two continuations: **24.59 ± 0.05** (frozen-procedure value 24.636 ± 0.052; parabola
  24.56 ± 0.04). It implies a local slope from 108 to 120 cells of 0.2025 ± 0.004 per cell: the tube's slope has
  stopped falling (0.2023 from 84 to 96, 0.2013 from 96 to 108), if this is right.
- Errors are Poisson errors of excursion counts (independent events) and the anchors' own; levels are strongly
  correlated with each other, so they are not averaged.
- No face died in the 120-cell run (5.5e9 face-generations); at 108 cells one did. This is a forecast, not a
  measurement of a lifetime. It cannot reach 144 cells or more: no anchors there, and nu at a level where q is
  known would need 1e12 face-generations.

## 6. A sampler that works: subset simulation on the dice chain [measured]

RESULTS-SUB

## 7. Reactive paths (deliverable 4)

- **Gump, natural deaths, exact (no flips):** `data/paths_4_0_4.txt` (1,268 deaths, 48 cells) and
  `data/paths_1_4_21.txt` (770 deaths, 63 cells). One line per death:
  `P face age pop(-1) ... pop(-24) | last[0] ... last[A-1]`: face = 0 or 1 (layer 0 or 7), age of the life,
  population of the dying face 1..24 generations before the death generation (the first generation it is
  empty), then for each face cell c the last generation at which it was alive, relative to the death generation
  (-1..-63; -64 = not alive in the last 63 generations). Cell c = (i' D + j') 3 + a: reduced in-plane cube index
  (i', j') as in `geom.py`, a = normal axis; its cube is (i', j', l - i' - j'), l = 0 or 7.
  More at any size brute force reaches: `ss_lag G/g.bin lag SEED GENS file` (84 cells: about 1 death per 2e7
  lane-generations; not run for lack of time).
- **Dice chain, sampled deaths at 108 cells and more:** `data/subpaths_*.txt`, one line per dying chain of the
  final ensemble of each replication: `S rep chain gd | pop(gd-1) pop(gd-2) ...` (up to 24 generations back).
  Chains of one replication are close relatives; `subpaths.py` averages within replications first.
- The splitting sampler of section 2 can also write lineages (`PATH` lines: stage-0 state in hex and the flip
  seeds of every stage, to be replayed); not used, since its deaths are the natural ones.

## 8. Not checked

- Gump beyond 84 cells was never run to a death here; everything at 96 cells and more is either the bookkeeping
  continuation (section 5) or the dice chain (section 6).
- Whether the dice chain's offset from gump drifts with size or shape beyond the anchors.
- Transverse firewalls and settled lanes are not detected in any mode (guards: age cap 50,000 in plain runs,
  1,000-generation trial limit in `ffs`).
- Boom and bust on gump at 84 cells and more, and on tubes: only 48 and 63 cells (both "wide") were looked at.
- The level function was never anything but one face layer's population. A look-ahead score (minimum population
  over the next few generations, a legitimate function of the state of a deterministic system) was proposed by the
  PI at 03:50 UTC; I did not build it for gump: its clones would still need a perturbation that is neutral in the
  measure, which section 3(b) says flips are not once they act. The dice chain sidesteps that.
- The early 48-cell table of section 3(b) predates the first commit of `ss.c`; the 63-cell rows are from the
  committed code.

## Files

`geom.py` (graph, numpy stepper), `ss.c` (stepper; modes `dump`, `plain`, `ffs`, `lag`, `sub`), `validate.py`,
`nuq.py`, `nuq_quad.py` (bookkeeping forecast), `howdie.py` (anatomy of natural deaths), `run_sub.py`,
`table_sub.py`, `subpaths.py` (subset sampler: frozen-parameter driver, table, dying paths), `chain_*.sh` (the
runs as launched), `data/` (validation log, plain-run histograms, lag profiles, paths, sampler outputs; `data/v1/`
= sampler version 1), `PREDICTIONS.md`.
