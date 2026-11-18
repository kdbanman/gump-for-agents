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
   63 cells). Exact for that chain. Against the gump anchors: +0.03 ± 0.03 (63 cells), +0.02 ± 0.05 (84),
   +0.09 ± 0.07 (96, blind), +0.07 ± 0.05 (108 tube, blind), +0.07 ± 0.07 (108 equilateral, blind). It gives
   24.64 ± 0.07 for the 120-cell tube and 38.7 ± 0.2 (± 0.3 for drift) for the 192-cell tube. Beyond 120 cells
   its lifetimes (tubes and wide tori, 14-26 replications each) are too noisy to decide between the readings of
   the tube's discount: section 6 says by how much.
6. **[measured, surrogate] Wide faces keep dying by a face-wide boom and bust up to 192 cells; long tubes stop
   doing so** (section 6, last table): the share of deaths with a one-generation fall of half the face is 0.54,
   0.59, 0.68, 0.55 on wide tori of 63, 108, 144, 192 cells, and 0.50, 0.50, 0.38, 0.26, 0.17 on loop^2 12 tubes
   of 84, 108, 120, 144, 192 cells. This comparison is within the dying ensemble and does not suffer from the
   noise of the lifetimes.
7. **[measured] A long tube does not stop busting, it stops busting all at once** (section 9, the PI's follow-up):
   every 2-unit stretch of a dying tube still over-fills to 0.7 of its cells and crashes to 0.22, at every
   length; the stretches crash together up to 144 cells and in two or three separate crashes at 192 (halves in
   different generations: 0.17, 0.21, 0.26, 0.29, 0.65 at 84..192 cells; wide tori 0.03). Gump's own deaths at
   63 and 84 cells give the same numbers as the surrogate's.

Marks: **[proved]**, **[measured]**, **[conjectured]**. Runs used one core (the machine gave it 40-50%).
`G/` = `research/scratch/blast/split-slab/`; build and geometry:

    for b in ss ss_lag ss_sub; do gcc -O3 -march=native -o G/$b research/blast/split-slab/ss.c -lm; done   # one program, three names
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

The dice chain (`WD=6`): layers 0..5 follow gump's rule, layers 6 and 7 are replaced after every generation by
fair coin flips (independent per cell and generation); one face (layer 0). It is a Markov chain whose only
randomness is i.i.d. bits, so the rare event can be sampled in the space of those bits without touching the
question that sank section 3 (what perturbation is neutral in gump's measure).

    WD=6 ss_sub G/g.bin sub SEED NREP LAM1 DELTA NBATCH NSWEEP KFLIP TPRE TWIN PATHFILE|- WBACK
    python3 run_sub.py H K D NREP SEED [paths]      # the frozen parameters; output data/sub_H_K_D_sSEED.txt
    python3 table_sub.py                             # the table below

**Exact statement.** Parameters (frozen in `PREDICTIONS.md` block 2, version 2 in block 2b): LAM1 =
round(0.515 A - 2.5 sqrt(0.415 A)), DELTA = 3, NBATCH = 8 (4,096 chains), NSWEEP = round(A / 6), KFLIP = 4,
TPRE = 32, TWIN = 24, WBACK = 12.
- A chain x = (initial state, dice). Initial states are snapshots, 64 generations apart, of 512 stationary lanes
  of the dice chain (0.4 soup, 1,000 generations of burn-in; a lane whose face is dead is reseeded and not used
  for 1,000 generations). Dice: T = TPRE + TWIN = 56 generations of fair bits for the 2 A cells of layers 6, 7.
- Score S(x) = the minimum face population over generations TPRE+1..T of the trajectory from the initial state
  under those dice; the chain does not count at all if its face is already dead at generation TPRE.
  {S = 0} = {the face dies at a generation in (TPRE, T]}, so P(S = 0) = TWIN / tau_face (to (TPRE + TWIN)/tau).
- Levels lam_1 = LAM1, lam_{i+1} = lam_i - 3 while positive, then 0. P_1 = share of the valid fresh chains
  with S <= lam_1.
- For each level i: the chains with S <= lam_i are copied round-robin from a uniform random offset into a full
  ensemble of 4,096, then moved by NSWEEP Metropolis sweeps. A proposal flips KFLIP dice bits: on even sweeps
  uniform over all T x 2A bits; on odd sweeps uniform over the 2A cells and the WBACK generations of dice before
  g_min, the first generation at which the chain attains its minimum. It is accepted iff S' <= lam_i and, on odd
  sweeps, every flipped bit lies in the WBACK generations before the new g_min' (so that the reverse move is
  proposable). P_{i+1} = share of the ensemble with S <= lam_{i+1} after the sweeps.
- Estimate: 1/tau_face = (prod P_i) / TWIN. Error: independent replications (fresh chains from later windows of
  the same stationary ensemble), mean of their rates, standard error from their scatter.
- Why it is exact for the chain **[proved, standard]**: the bits are i.i.d. fair, so a flip is a symmetric move
  that preserves their law; accepting on the indicator of {S <= lam_i} (with the Hastings condition on odd sweeps)
  leaves the law conditioned on that set invariant; the seeds are exact draws from it by induction. The initial
  states are never moved, which validity does not need.
- Version 1 (`data/v1/`) had only the uniform sweeps: correct, but its level counts scattered by 20-30% between
  replications on the last four levels (the fade after the crash), 7-10% in version 2.

<!-- SUB-RESULTS-BEGIN -->
**Results** (`python3 table_sub.py`; every replication of version 2, pooled over seeds):

| cells | torus | replications | ln tau, dice chain | gump anchor | dice chain (sampler) - gump |
|---:|---|---:|---|---|---|
| 63 | (1,4),(0,21) | 48 | 13.188 ± 0.031 | 13.1622 ± 0.0007 | +0.026 ± 0.031 |
| 84 | (1,12),(0,28) | 48 | 17.336 ± 0.046 | 17.3175 ± 0.0031 | +0.019 ± 0.046 |
| 96 | (1,17),(0,32) | 48 | 19.832 ± 0.067 | 19.7446 ± 0.0042 | +0.087 ± 0.067 |
| 108 | (1,16),(0,36) | 64 | 22.232 ± 0.051 | 22.1599 ± 0.0086 | +0.072 ± 0.052 |
| 108 | (6,0),(0,6) | 40 | 22.609 ± 0.071 | 22.5405 ± 0.0074 | +0.068 ± 0.072 |
| 120 | (1,18),(0,40) | 64 | 24.696 ± 0.065 | — | — |
| 144 | (1,22),(0,48) | 18 | 29.288 ± 0.190 | — | — |
| 144 | (4,4),(0,12) | 14 | 29.738 ± 0.239 | — | — |
| 192 | (1,30),(0,64) | 26 | 38.764 ± 0.181 | — | — |
| 192 | (8,0),(0,8) | 18 | 40.588 ± 0.193 | — | — |

offset d = dice chain - gump, weighted mean over the tubes of 84, 96, 108 cells: +0.052 ± 0.031 (chi2 0.9 on 2)
  (1,18),(0,40), 120 cells: dice chain 24.696 ± 0.065; minus d: 24.644 ± 0.071
  (1,22),(0,48), 144 cells: dice chain 29.288 ± 0.190; minus d: 29.235 ± 0.193
  (1,30),(0,64), 192 cells: dice chain 38.764 ± 0.181; minus d: 38.712 ± 0.184
  (4,4),(0,12), 144 cells: dice chain 29.738 ± 0.239; minus d: 29.686 ± 0.241
  (8,0),(0,8), 192 cells: dice chain 40.588 ± 0.193; minus d: 40.536 ± 0.195
<!-- SUB-RESULTS-END -->

<!-- COMMENTARY-BEGIN -->
- **Exactness [measured].** The dice chain by brute force: 9.9407 ± 0.0085 at 48 cells (13,992 deaths;
  `WD=6 ss G/g_4_0_4.bin plain 77 600000 20 11`) and 13.182 ± 0.027 at 63 cells (1,417 deaths;
  `WD=6 ss G/g_1_4_21.bin plain 77 1500000 27 17`). The sampler on the same chain: 9.920 ± 0.021 (48 cells, version
  1, 32 replications, `data/v1/`) and the 63-cell row above. Gump itself: 9.9251 and 13.1622, so the dice chain
  sits +0.016 ± 0.009 and +0.020 ± 0.027 above gump there.
- **Calibration [measured].** 48 and 63 cells were tuning tori, 84 cells became one (block 2b); **96 cells and the
  two 108-cell tori (tube and the equilateral (6,0),(0,6)) are blind**. Sampler minus gump anchor (table):
  +0.026 ± 0.031 (63), +0.019 ± 0.046 (84), +0.087 ± 0.067 (96), +0.072 ± 0.052 (108 tube), +0.068 ± 0.072 (108
  wide): each within 1.4 of its error, all five positive, weighted mean **+0.04 ± 0.02**, which is the size of the
  dice chain's own offset by brute force. The 108-cell discount of the tube against the wide torus comes out
  0.38 ± 0.09 (gump: 0.381). **Bias I can exclude: more than about 0.08 on average over 63 to 108 cells, more than
  about 0.2 at any one of them; a drift of the offset with size is bounded only to +0.002 ± 0.003 per cell** (84
  to 108 cells), which is +0.2 ± 0.25 at 192 cells. So beyond 120 cells the absolute numbers carry about ± 0.3
  on top of their statistical errors.
- **120 cells [measured, surrogate].** Dice chain 24.696 ± 0.065 (64 replications); minus the offset d of the tube
  anchors (+0.052 ± 0.031): **24.64 ± 0.07** for gump. Independent of section 5's 24.59 ± 0.05 (other randomness,
  other assumptions) and 0.6 sd from it; weighted together 24.61 ± 0.04.
- **Long tubes and wide tori beyond the anchors [measured, surrogate; few replications; NOT decisive].**
  (`python3 derived.py` prints the numbers of this paragraph.) At 144 and 192 cells ln(rate) scatters between
  replications with sd 0.65 (tubes), 0.8 and 1.0 (wide tori), there are 14 to 26 of them, the mean is carried by
  the largest, and the quoted errors are too small: for a lognormal scatter of that width they would be 0.14 to
  0.33 instead of 0.18 to 0.24, and against the wide line 13.1622 + 0.20866 (A - 63) the two wide tori read
  **-0.33 ± 0.24 at 144 cells** ((4,4),(0,12): 29.74 against 30.06) and **+0.51 ± 0.19 (lognormal: ± 0.32) at
  192 cells** ((8,0),(0,8): 40.59 against 40.08). Together they neither confirm nor refute that 0.2087 holds
  to 192 cells. With that warning:
  - the tube's slope from 108 to 192 cells is (38.764 - 22.232) / 84 = **0.197 ± 0.002 per cell** (120 to 144:
    0.191 ± 0.008; 144 to 192: 0.197 ± 0.006). The quadratic discount 0.0046 (A/12)^2 and the straight line near
    0.198 both predict 0.198 to 0.199 here and cannot be separated below 240 cells; the return to the wide price
    (0.2086) is disfavoured (5 sd on the statistical error, about 2 sd once a drift of ± 0.3 at 192 cells is
    allowed);
  - the 192-cell tube itself: 38.76 ± 0.18 on the dice chain, 38.71 ± 0.18 after the offset (and ± 0.3 for
    drift). The PI's forms give 39.17 / 39.01 / 38.92 / 38.86 (trace form K = 1 / 2 / 3, power law): K = 1 is
    2.5 sd away on the statistical error, the others 0.8 to 1.7;
  - tube against wide torus of the same chain and area: 0.38 ± 0.09 at 108 cells, 0.45 ± 0.31 at 144, 1.82 ± 0.26
    (lognormal ± 0.35) at 192 (the three readings: 0.66 / 0.77 / 0.47 at 144 and 1.18 / 1.29 / 0.47 at 192);
  - what it would take: about 100 replications per torus (15 core-minutes each at 192 cells), or more chains per
    replication; and a convergence test (doubling NSWEEP), which was not done at these sizes. The scatter between
    replications is larger on the wide torus (1.0) than on the tube (0.65) at 192 cells: the wide face's single
    face-wide event is the harder one for the Metropolis moves.
  - The 240-cell tube was not run.
- **Dying paths [measured, surrogate]** (`python3 subpaths.py G/subpaths_full/FILE [FILE ...] A`, outputs in
  `data/subpaths_stats.txt`; per-replication means ± their standard error; "fall" = the largest one-generation
  fall of the face population in the last 16 generations). The sampler's deaths at 63 cells reproduce the natural
  route of section 4: a fall of at least A/2 in 0.54 ± 0.02 of deaths (natural gump 0.558), of at least 0.4 A in
  0.81 ± 0.02 (0.823), from 46.1 to 14.0 cells (47 to 14). **Wide tori keep the face-wide boom and bust up to
  192 cells; along the loop^2 12 tubes it fades out as the tube lengthens** (rows in order of size; (1,4),(0,21),
  (6,0),(0,6), (4,4),(0,12), (8,0),(0,8) are wide, the others tubes):

<!-- PATHTABLE-BEGIN -->
  | torus | cells | replications | fall >= A/2 | fall >= 0.4 A | largest fall | it starts from | and leaves | generations from it to the death |
  |---|---:|---:|---|---|---|---|---|---|
  | (1,4),(0,21) | 63 | 16 | 0.54 ± 0.02 | 0.81 ± 0.02 | 0.51 A | mean + 2.7 sd = 0.73 A | 0.22 A | 5.39 ± 0.12 |
  | (1,12),(0,28) | 84 | 16 | 0.50 ± 0.03 | 0.77 ± 0.02 | 0.49 A | mean + 2.8 sd = 0.71 A | 0.23 A | 5.69 ± 0.07 |
  | (6,0),(0,6) | 108 | 24 | 0.59 ± 0.03 | 0.88 ± 0.02 | 0.51 A | mean + 3.5 sd = 0.73 A | 0.22 A | 5.94 ± 0.07 |
  | (1,16),(0,36) | 108 | 16 | 0.50 ± 0.04 | 0.72 ± 0.03 | 0.48 A | mean + 2.9 sd = 0.70 A | 0.22 A | 6.36 ± 0.10 |
  | (1,18),(0,40) | 120 | 32 | 0.38 ± 0.03 | 0.65 ± 0.03 | 0.44 A | mean + 2.5 sd = 0.66 A | 0.23 A | 6.56 ± 0.09 |
  | (4,4),(0,12) | 144 | 14 | 0.68 ± 0.05 | 0.95 ± 0.01 | 0.53 A | mean + 4.2 sd = 0.74 A | 0.21 A | 6.34 ± 0.10 |
  | (1,22),(0,48) | 144 | 8 | 0.26 ± 0.05 | 0.59 ± 0.05 | 0.41 A | mean + 2.3 sd = 0.64 A | 0.23 A | 7.13 ± 0.18 |
  | (8,0),(0,8) | 192 | 12 | 0.55 ± 0.08 | 0.91 ± 0.04 | 0.51 A | mean + 4.5 sd = 0.72 A | 0.22 A | 6.91 ± 0.22 |
  | (1,30),(0,64) | 192 | 16 | 0.17 ± 0.06 | 0.33 ± 0.07 | 0.34 A | mean + 1.5 sd = 0.58 A | 0.24 A | 8.33 ± 0.26 |
<!-- PATHTABLE-END -->

  Whatever the shape, the fall leaves 0.22 to 0.24 A. On the wide tori it starts from 0.72 to 0.73 A at every size
  (mean + 2.7 sd at 63 cells, + 4.5 sd at 192: the over-full generation is a fixed *fraction* of the face) and
  removes half the face. On the 192-cell tube it starts from a face that is hardly over-full (0.58 A, mean + 1.5
  sd), removes a third, and the death comes 8 generations later instead of 5 to 6. **[conjectured]** The tube
  does not have to fill everywhere at once: a stretch of it booms and busts and the rest follows within the
  time information needs to travel along it, which would be why a long tube is cheaper per cell the longer it
  is. The route changes between 2.6 and 3 girths of length (84 and 108 cells: 2.0 and 2.6 girths, still face-wide
  half the time; 192 cells: 4.6 girths); the discount of the short tubes (0.22 at 84 cells) is already there
  before it does, so that part has another cause. The path files hold
  populations only; whether the emptying travels along the axis needs per-cell records, which this mode does not
  write.
<!-- COMMENTARY-END -->


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
- **Dice chain, sampled deaths at 63 to 192 cells:** `data/subpaths_*.txt`, the first 60 dying chains of the
  final ensemble of each replication (all of them, 25 MB, in `G/subpaths_full/`, git-ignored; regenerate with
  `python3 run_sub.py H K D NREP SEED paths`): `S rep chain gd | pop(gd-1) pop(gd-2) ...`, the face population
  up to 24 generations back from the death generation gd. Chains of one replication are close relatives;
  `subpaths.py` averages within replications first. No per-cell record in this mode.
- The splitting sampler of section 2 can also write lineages (`PATH` lines: stage-0 state in hex and the flip
  seeds of every stage, to be replayed); not used, since its deaths are the natural ones.

## 8. Not checked

- Gump beyond 84 cells was never run to a death here; everything at 96 cells and more is either the bookkeeping
  continuation (section 5) or the dice chain (section 6).
- Whether the dice chain's offset from gump, or the sampler's accuracy at fixed effort, drifts beyond 108 cells:
  the wide tori read 0.33 below and 0.64 above the wide line at 144 and 192 cells, more than their quoted errors
  allow. The tori of 144 and 192 cells were not validated against the oracle (same builder and stepper). No run at 240 cells or more, none on
  tubes of loop^2 13 or 16, none on a 300-cell torus.
- The sampler's sweeps were never checked for convergence by doubling them at a large size; version 1 (uniform
  proposals only) read 0.10 and 0.15 higher than version 2 at 63 and 84 cells, inside its own errors.
- Transverse firewalls and settled lanes are not detected in any mode (guards: age cap 50,000 in plain runs,
  1,000-generation trial limit in `ffs`).
- Boom and bust on gump at 84 cells and more, and on tubes: only 48 and 63 cells (both "wide") were looked at.
- The level function was never anything but one face layer's population. A look-ahead score (minimum population
  over the next few generations, a legitimate function of the state of a deterministic system) was proposed by the
  PI at 03:50 UTC; I did not build it for gump: its clones would still need a perturbation that is neutral in the
  measure, which section 3(b) says flips are not once they act. The dice chain sidesteps that.
- The early 48-cell table of section 3(b) predates the first commit of `ss.c`; the 63-cell rows are from the
  committed code.

## 9. Does a long tube stop busting, or stop busting all at once? (the PI's follow-up, 04:45 UTC)

Asked after sections 1-8 were written. The stored paths held populations only, so the dying paths were
regenerated with every face cell recorded for the last 16 generations: the subset sampler on the dice chain
(`python3 run_sub.py H K D NREP 5 cells` -> `G/cells/cells_H_K_D_s5.txt`, the first 8 dying chains of each of the
8 batches of every replication; these replications also enter the table of section 6), natural deaths of gump
itself at 48, 63 and 84 cells (`ss_lag G/g.bin lag 5 GENS - G/cells/gump_H_K_D.txt`), and, as the null, 16-generation
windows of LIVING gump faces (`ss_lag G/g.bin lag 8 80000 - - G/cells/null_H_K_D.txt`, one window every 256
generations). All as launched: `chain_cells.sh`, `chain_null.sh`. The cell files are bulk (scratch, git-ignored).

    python3 sections.py H K D G/cells/FILE      # one torus, everything;  python3 sec_table.py: the tables below
    (full output for every torus: data/sections_full.txt)

**Definitions** (fixed in `sections.py` and committed, 18812e7, before I read the PI's forecast, block 3 of
`research/blast/PREDICTIONS.md`; table 9e was added after). A *ring* is the set of face cells at one position
along the axis perpendicular to the shortest loop (6 cells, every 0.5 lattice units on these tubes). *Sections*
are contiguous blocks of rings: about 4 rings = 2 lattice units = 24 cells (4 sections of 21 cells at 84 cells, 4
of 24-30 at 108, then 5, 6, 8 sections of 24), or the two halves; on the tori (H,0),(0,D) halves and quarters are
cut along the two periods. The *crash* of a section (or of the face) is its largest one-generation fall in the last
16 generations (ties: nearest the death); *before* and *after* are the section's population at the two ends of
that fall as fractions of its size; *half-fall*: before - after >= 0.5; *local bust*: before >= 0.68 and a
half-fall. Shares are per replication (or per natural death, or per null window) first; mean ± standard error.

<!-- SEC9-TABLES-BEGIN -->
**9a. Tubes cut into sections of 2 lattice units (24 cells; 21 and 27-30 cells at 84 and 108 cells).**

| cells | ensemble | units (deaths) | face-wide half-fall | sections with a half-fall | sections busting locally | section before -> after | busting sections per death | >= 1 section busts | spread of crash generations | distinct crash generations | r.m.s. difference, neighbours (2 units) | at 4 units | at half the tube |
|---:|---|---:|---|---|---|---|---|---|---|---|---:|---:|---:|
| 84 | dying, dice chain (sampler) | 16 (1024) | 0.45 ± 0.03 | 0.58 ± 0.02 | 0.56 ± 0.02 | 0.73 ± 0.01 -> 0.22 ± 0.00 | 2.25 ± 0.07 of 4 | 0.97 ± 0.01 | 2.76 ± 0.20 | 1.65 ± 0.04 | 3.05 | 3.15 | 3.15 |
| 84 | dying, gump (natural deaths) | 111 (111) | 0.53 ± 0.05 | 0.61 ± 0.03 | 0.59 ± 0.03 | 0.73 ± 0.01 -> 0.21 ± 0.00 | 2.37 ± 0.10 of 4 | 0.96 ± 0.02 | 2.67 ± 0.34 | 1.69 ± 0.08 | 3.01 | 3.28 | 3.28 |
| 84 | LIVING, gump (null) | 308 (308) | 0.00 ± 0.00 | 0.13 ± 0.01 | 0.12 ± 0.01 | 0.71 ± 0.00 -> 0.36 ± 0.00 | 0.50 ± 0.04 of 4 | 0.41 ± 0.03 | 8.75 ± 0.16 | 3.52 ± 0.03 | 6.02 | 5.92 | 5.92 |
| 108 | dying, dice chain (sampler) | 16 (1024) | 0.46 ± 0.03 | 0.53 ± 0.01 | 0.52 ± 0.01 | 0.72 ± 0.00 -> 0.22 ± 0.00 | 2.07 ± 0.06 of 4 | 0.95 ± 0.01 | 2.14 ± 0.21 | 1.59 ± 0.05 | 2.57 | 2.68 | 2.68 |
| 108 | LIVING, gump (null) | 308 (308) | 0.00 ± 0.00 | 0.07 ± 0.01 | 0.07 ± 0.01 | 0.69 ± 0.00 -> 0.38 ± 0.00 | 0.29 ± 0.03 of 4 | 0.27 ± 0.03 | 8.97 ± 0.18 | 3.52 ± 0.04 | 6.08 | 6.29 | 6.29 |
| 120 | dying, dice chain (sampler) | 16 (1024) | 0.37 ± 0.04 | 0.55 ± 0.01 | 0.54 ± 0.01 | 0.72 ± 0.00 -> 0.22 ± 0.00 | 2.68 ± 0.07 of 5 | 0.98 ± 0.00 | 2.97 ± 0.24 | 1.95 ± 0.08 | 2.68 | 2.74 | 2.74 |
| 120 | LIVING, gump (null) | 308 (308) | 0.00 ± 0.00 | 0.09 ± 0.01 | 0.09 ± 0.01 | 0.69 ± 0.00 -> 0.37 ± 0.00 | 0.44 ± 0.04 of 5 | 0.37 ± 0.03 | 9.51 ± 0.16 | 4.19 ± 0.04 | 5.91 | 5.97 | 5.97 |
| 144 | dying, dice chain (sampler) | 10 (640) | 0.33 ± 0.07 | 0.52 ± 0.02 | 0.51 ± 0.02 | 0.72 ± 0.01 -> 0.22 ± 0.00 | 3.08 ± 0.14 of 6 | 0.97 ± 0.01 | 3.45 ± 0.40 | 2.15 ± 0.12 | 2.65 | 2.94 | 2.98 |
| 144 | LIVING, gump (null) | 308 (308) | 0.00 ± 0.00 | 0.09 ± 0.01 | 0.09 ± 0.01 | 0.69 ± 0.00 -> 0.37 ± 0.00 | 0.53 ± 0.04 of 6 | 0.44 ± 0.03 | 10.39 ± 0.13 | 4.93 ± 0.05 | 5.95 | 6.07 | 6.07 |
| 192 | dying, dice chain (sampler) | 10 (640) | 0.07 ± 0.03 | 0.48 ± 0.02 | 0.46 ± 0.02 | 0.69 ± 0.01 -> 0.22 ± 0.00 | 3.71 ± 0.15 of 8 | 0.98 ± 0.01 | 5.55 ± 0.35 | 3.42 ± 0.15 | 2.85 | 3.31 | 3.66 |
| 192 | LIVING, gump (null) | 308 (308) | 0.00 ± 0.00 | 0.08 ± 0.01 | 0.07 ± 0.01 | 0.69 ± 0.00 -> 0.37 ± 0.00 | 0.60 ± 0.04 of 8 | 0.47 ± 0.03 | 11.30 ± 0.11 | 6.15 ± 0.06 | 5.87 | 6.09 | 6.04 |

**9b. Two halves (tubes: along the length; wide tori: across one period).**

| cells | torus | ensemble | units | halves crash in different generations | spread 0 / 1 / 2 / >= 3 generations | r.m.s. difference | a half with a half-fall: at least one | both | half before -> after |
|---:|---|---|---:|---|---|---:|---|---|---|
| 84 | (1,12),(0,28) tube | dying, dice chain (sampler) | 16 | 0.17 ± 0.02 | 0.83 ± 0.02 / 0.01 ± 0.00 / 0.02 ± 0.01 / 0.13 ± 0.02 | 2.12 | 0.74 ± 0.02 | 0.25 ± 0.02 | 0.72 ± 0.00 -> 0.23 ± 0.00 |
| 84 | (1,12),(0,28) tube | dying, gump (natural deaths) | 111 | 0.17 ± 0.04 | 0.83 ± 0.04 / 0.03 ± 0.02 / 0.03 ± 0.02 / 0.12 ± 0.03 | 1.94 | 0.71 ± 0.04 | 0.35 ± 0.05 | 0.73 ± 0.01 -> 0.22 ± 0.01 |
| 84 | (1,12),(0,28) tube | LIVING, gump (null) | 308 | 0.94 ± 0.01 | 0.06 ± 0.01 / 0.09 ± 0.02 / 0.09 ± 0.02 / 0.76 ± 0.02 | 6.07 | 0.02 ± 0.01 | 0.00 ± 0.00 | 0.65 ± 0.00 -> 0.40 ± 0.00 |
| 108 | (1,16),(0,36) tube | dying, dice chain (sampler) | 16 | 0.21 ± 0.02 | 0.79 ± 0.02 / 0.04 ± 0.01 / 0.06 ± 0.01 / 0.12 ± 0.02 | 1.70 | 0.72 ± 0.03 | 0.28 ± 0.03 | 0.71 ± 0.00 -> 0.23 ± 0.00 |
| 108 | (1,16),(0,36) tube | LIVING, gump (null) | 308 | 0.90 ± 0.02 | 0.10 ± 0.02 / 0.09 ± 0.02 / 0.11 ± 0.02 / 0.70 ± 0.03 | 5.98 | 0.01 ± 0.00 | 0.00 ± 0.00 | 0.63 ± 0.00 -> 0.41 ± 0.00 |
| 120 | (1,18),(0,40) tube | dying, dice chain (sampler) | 16 | 0.26 ± 0.04 | 0.74 ± 0.04 / 0.04 ± 0.02 / 0.07 ± 0.03 / 0.15 ± 0.02 | 1.75 | 0.60 ± 0.03 | 0.18 ± 0.02 | 0.69 ± 0.01 -> 0.23 ± 0.00 |
| 120 | (1,18),(0,40) tube | LIVING, gump (null) | 308 | 0.92 ± 0.02 | 0.08 ± 0.02 / 0.08 ± 0.02 / 0.11 ± 0.02 / 0.73 ± 0.03 | 6.16 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.63 ± 0.00 -> 0.42 ± 0.00 |
| 144 | (1,22),(0,48) tube | dying, dice chain (sampler) | 10 | 0.29 ± 0.04 | 0.71 ± 0.04 / 0.08 ± 0.04 / 0.09 ± 0.02 / 0.13 ± 0.03 | 1.75 | 0.61 ± 0.05 | 0.17 ± 0.05 | 0.67 ± 0.01 -> 0.22 ± 0.00 |
| 144 | (1,22),(0,48) tube | LIVING, gump (null) | 308 | 0.91 ± 0.02 | 0.09 ± 0.02 / 0.07 ± 0.02 / 0.10 ± 0.02 / 0.74 ± 0.03 | 6.20 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.62 ± 0.00 -> 0.43 ± 0.00 |
| 192 | (1,30),(0,64) tube | dying, dice chain (sampler) | 10 | 0.65 ± 0.08 | 0.35 ± 0.08 / 0.16 ± 0.04 / 0.15 ± 0.04 / 0.34 ± 0.06 | 3.09 | 0.22 ± 0.06 | 0.04 ± 0.02 | 0.59 ± 0.02 -> 0.24 ± 0.01 |
| 192 | (1,30),(0,64) tube | LIVING, gump (null) | 308 | 0.92 ± 0.02 | 0.08 ± 0.02 / 0.10 ± 0.02 / 0.09 ± 0.02 / 0.73 ± 0.03 | 6.42 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.60 ± 0.00 -> 0.44 ± 0.00 |
| 63 | (1,4),(0,21) wide | dying, dice chain (sampler) | 16 | 0.11 ± 0.01 | 0.89 ± 0.01 / 0.02 ± 0.00 / 0.01 ± 0.00 / 0.08 ± 0.01 | 1.69 | 0.78 ± 0.02 | 0.34 ± 0.03 | 0.74 ± 0.00 -> 0.22 ± 0.00 |
| 63 | (1,4),(0,21) wide | dying, gump (natural deaths) | 774 | 0.11 ± 0.01 | 0.89 ± 0.01 / 0.01 ± 0.00 / 0.01 ± 0.00 / 0.09 ± 0.01 | 2.05 | 0.79 ± 0.01 | 0.32 ± 0.02 | 0.74 ± 0.00 -> 0.21 ± 0.00 |
| 63 | (1,4),(0,21) wide | LIVING, gump (null) | 308 | 0.84 ± 0.02 | 0.16 ± 0.02 / 0.06 ± 0.01 / 0.09 ± 0.02 / 0.69 ± 0.03 | 5.98 | 0.05 ± 0.01 | 0.00 ± 0.00 | 0.67 ± 0.00 -> 0.39 ± 0.00 |
| 108 | (6,0),(0,6) wide | dying, dice chain (sampler) | 16 | 0.03 ± 0.01 | 0.97 ± 0.01 / 0.01 ± 0.00 / 0.00 ± 0.00 / 0.02 ± 0.01 | 0.78 | 0.82 ± 0.03 | 0.36 ± 0.04 | 0.73 ± 0.00 -> 0.22 ± 0.00 |
| 108 | (6,0),(0,6) wide | LIVING, gump (null) | 308 | 0.91 ± 0.02 | 0.09 ± 0.02 / 0.12 ± 0.02 / 0.10 ± 0.02 / 0.69 ± 0.03 | 6.22 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.64 ± 0.00 -> 0.42 ± 0.00 |
| 192 | (8,0),(0,8) wide | dying, dice chain (sampler) | 6 | 0.03 ± 0.02 | 0.97 ± 0.02 / 0.01 ± 0.00 / 0.01 ± 0.01 / 0.01 ± 0.01 | 0.76 | 0.82 ± 0.05 | 0.27 ± 0.07 | 0.72 ± 0.01 -> 0.23 ± 0.00 |
| 192 | (8,0),(0,8) wide | LIVING, gump (null) | 308 | 0.90 ± 0.02 | 0.10 ± 0.02 / 0.10 ± 0.02 / 0.14 ± 0.02 / 0.66 ± 0.03 | 5.92 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.60 ± 0.00 -> 0.45 ± 0.00 |

**9c. Wide tori cut into four quarters.**

| cells | torus | ensemble | units | quarters crash in different generations | spread 0 / 1 / 2 / >= 3 | distinct crash generations | quarters with a half-fall | all four | quarter before -> after |
|---:|---|---|---:|---|---|---|---|---|---|
| 108 | (6,0),(0,6) | dying, dice chain (sampler) | 16 | 0.28 ± 0.03 | 0.72 ± 0.03 / 0.06 ± 0.02 / 0.02 ± 0.02 / 0.19 ± 0.03 | 1.31 ± 0.04 | 0.56 ± 0.02 | 0.12 ± 0.02 | 0.74 ± 0.00 -> 0.22 ± 0.00 |
| 108 | (6,0),(0,6) | LIVING, gump (null) | 308 | 1.00 ± 0.00 | 0.00 ± 0.00 / 0.00 ± 0.00 / 0.01 ± 0.01 / 0.98 ± 0.01 | 3.49 ± 0.04 | 0.03 ± 0.01 | 0.00 ± 0.00 | 0.68 ± 0.00 -> 0.38 ± 0.00 |
| 192 | (8,0),(0,8) | dying, dice chain (sampler) | 6 | 0.15 ± 0.08 | 0.85 ± 0.08 / 0.02 ± 0.01 / 0.06 ± 0.05 / 0.07 ± 0.02 | 1.16 ± 0.08 | 0.56 ± 0.05 | 0.09 ± 0.04 | 0.73 ± 0.01 -> 0.22 ± 0.00 |
| 192 | (8,0),(0,8) | LIVING, gump (null) | 308 | 1.00 ± 0.00 | 0.00 ± 0.00 / 0.01 ± 0.01 / 0.01 ± 0.01 / 0.98 ± 0.01 | 3.51 ± 0.03 | 0.00 ± 0.00 | 0.00 ± 0.00 | 0.63 ± 0.00 -> 0.41 ± 0.00 |

**9d. Deaths with NO face-wide fall of half the face: are they staggered busts? (tubes, sections of 2 units)**

| cells | ensemble | share of deaths without a face-wide half-fall | their sections: half-fall | busting locally | section before | >= 1 section busts | >= half of the sections bust | spread of crash generations |
|---:|---|---|---|---|---|---|---|---|
| 84 | dying, dice chain (sampler) | 0.55 ± 0.03 | 0.43 ± 0.02 | 0.42 ± 0.02 | 0.71 ± 0.01 | 0.94 ± 0.01 | 0.58 ± 0.04 | 3.81 ± 0.29 |
| 84 | dying, gump (natural deaths) | 0.47 ± 0.05 | 0.42 ± 0.03 | 0.39 ± 0.03 | 0.68 ± 0.01 | 0.92 ± 0.04 | 0.48 ± 0.07 | 4.17 ± 0.52 |
| 84 | LIVING, gump (null) | 1.00 ± 0.00 | 0.13 ± 0.01 | 0.12 ± 0.01 | 0.71 ± 0.00 | 0.41 ± 0.03 | 0.08 ± 0.02 | 8.75 ± 0.16 |
| 108 | dying, dice chain (sampler) | 0.54 ± 0.03 | 0.38 ± 0.01 | 0.36 ± 0.01 | 0.69 ± 0.00 | 0.91 ± 0.02 | 0.43 ± 0.03 | 3.22 ± 0.29 |
| 108 | LIVING, gump (null) | 1.00 ± 0.00 | 0.07 ± 0.01 | 0.07 ± 0.01 | 0.69 ± 0.00 | 0.27 ± 0.03 | 0.02 ± 0.01 | 8.97 ± 0.18 |
| 120 | dying, dice chain (sampler) | 0.63 ± 0.04 | 0.44 ± 0.01 | 0.42 ± 0.01 | 0.70 ± 0.00 | 0.96 ± 0.01 | 0.35 ± 0.04 | 4.00 ± 0.25 |
| 120 | LIVING, gump (null) | 1.00 ± 0.00 | 0.09 ± 0.01 | 0.09 ± 0.01 | 0.69 ± 0.00 | 0.37 ± 0.03 | 0.00 ± 0.00 | 9.51 ± 0.16 |
| 144 | dying, dice chain (sampler) | 0.67 ± 0.07 | 0.45 ± 0.02 | 0.45 ± 0.02 | 0.70 ± 0.01 | 0.95 ± 0.01 | 0.55 ± 0.04 | 4.43 ± 0.42 |
| 144 | LIVING, gump (null) | 1.00 ± 0.00 | 0.09 ± 0.01 | 0.09 ± 0.01 | 0.69 ± 0.00 | 0.44 ± 0.03 | 0.01 ± 0.01 | 10.39 ± 0.13 |
| 192 | dying, dice chain (sampler) | 0.93 ± 0.03 | 0.46 ± 0.02 | 0.44 ± 0.02 | 0.69 ± 0.01 | 0.98 ± 0.01 | 0.51 ± 0.05 | 5.81 ± 0.30 |
| 192 | LIVING, gump (null) | 1.00 ± 0.00 | 0.08 ± 0.01 | 0.07 ± 0.01 | 0.69 ± 0.00 | 0.47 ± 0.03 | 0.00 ± 0.00 | 11.30 ± 0.11 |

**9e. Timing of the sections that do bust (pairs of sections that both have a half-fall): r.m.s. difference of crash generations by separation.**

| cells | ensemble | 2 units | 4 units | 6 units | 8 units |
|---:|---|---:|---:|---:|---:|
| 84 | dying, dice chain (sampler) (sections of 1.75 units) | 2.51 | 2.74 |  |  |
| 84 | dying, gump (natural deaths) (sections of 1.75 units) | 2.20 | 2.56 |  |  |
| 84 | LIVING, gump (null) (sections of 1.75 units) | 5.54 | 7.62 |  |  |
| 108 | dying, dice chain (sampler) (sections of 2.25 units) | 1.56 | 1.84 |  |  |
| 108 | LIVING, gump (null) (sections of 2.25 units) | 6.58 | 3.61 |  |  |
| 120 | dying, dice chain (sampler) (sections of 2.00 units) | 1.47 | 1.78 |  |  |
| 120 | LIVING, gump (null) (sections of 2.00 units) | 6.73 | 4.55 |  |  |
| 144 | dying, dice chain (sampler) (sections of 2.00 units) | 1.93 | 2.44 | 2.47 |  |
| 144 | LIVING, gump (null) (sections of 2.00 units) | 5.85 | 5.76 | 7.26 |  |
| 192 | dying, dice chain (sampler) (sections of 2.00 units) | 1.54 | 2.76 | 3.36 | 3.44 |
| 192 | LIVING, gump (null) (sections of 2.00 units) | 7.68 | 6.57 | 4.66 | 6.46 |

**9f. Share of pairs of busting sections (both with a half-fall) that crash in the SAME generation, by separation.**

| cells | ensemble | 2 units | 4 units | 6 units | 8 units |
|---:|---|---|---|---|---|
| 84 | dying, dice chain (sampler) (sections of 1.75 units) | 0.84 ± 0.02 | 0.79 ± 0.04 |  |  |
| 84 | dying, gump (natural deaths) (sections of 1.75 units) | 0.86 ± 0.03 | 0.82 ± 0.05 |  |  |
| 84 | LIVING, gump (null) (sections of 1.75 units) | 0.26 ± 0.10 | 0.00 ± 0.00 |  |  |
| 108 | dying, dice chain (sampler) (sections of 2.25 units) | 0.90 ± 0.01 | 0.83 ± 0.03 |  |  |
| 108 | LIVING, gump (null) (sections of 2.25 units) | 0.25 ± 0.25 | 0.00 ± 0.00 |  |  |
| 120 | dying, dice chain (sampler) (sections of 2.00 units) | 0.88 ± 0.02 | 0.75 ± 0.04 |  |  |
| 120 | LIVING, gump (null) (sections of 2.00 units) | 0.23 ± 0.12 | 0.00 ± 0.00 |  |  |
| 144 | dying, dice chain (sampler) (sections of 2.00 units) | 0.85 ± 0.03 | 0.68 ± 0.05 | 0.62 ± 0.07 |  |
| 144 | LIVING, gump (null) (sections of 2.00 units) | 0.09 ± 0.09 | 0.00 ± 0.00 | 0.17 ± 0.17 |  |
| 192 | dying, dice chain (sampler) (sections of 2.00 units) | 0.77 ± 0.03 | 0.38 ± 0.06 | 0.27 ± 0.08 | 0.25 ± 0.08 |
| 192 | LIVING, gump (null) (sections of 2.00 units) | 0.17 ± 0.09 | 0.09 ± 0.09 | 0.25 ± 0.13 | 0.00 ± 0.00 |
<!-- SEC9-TABLES-END -->

**Answers [measured: dice chain, sampled deaths; gump itself at 63 and 84 cells and for the null].**

1. **A long tube does not stop busting. It stops busting all at once.** At every length each stretch of 2
   lattice units goes from 0.69-0.73 of its cells to 0.22 in one generation (9a), which is exactly what a wide
   face does as a whole (0.72 -> 0.23, 9b) and not what a living face does (largest fall in 16 generations:
   0.69 -> 0.37). The threshold "half of the cells" sits at the median of that fall, which is why "half" of the
   sections pass it at every length (0.58, 0.53, 0.55, 0.52, 0.48 at 84..192 cells; living faces 0.07 to 0.13), as
   half of the wide faces do. At least one section busts locally in 95-98% of deaths at every length (living:
   27-47% per 16-generation window). What falls with length is only the *face-wide* half-fall: 0.45, 0.46, 0.37,
   0.33, 0.07.
2. **Timing (9b, 9a, 9e, 9f).** The two halves of the tube crash in different generations in 0.17 ± 0.02 (84
   cells), 0.21 ± 0.02 (108), 0.26 ± 0.04 (120), 0.29 ± 0.04 (144) and **0.65 ± 0.08 (192)** of deaths; when they
   differ it is mostly by 3 generations or more, not by one. Distinct crash generations per death among the
   2-unit sections: 1.65, 1.59, 1.95, 2.15, 3.42 (of 4, 4, 5, 6, 8 sections; living faces 3.5 to 6.2). Among
   sections that both bust, neighbours (2 units apart) crash in the same generation 77-90% of the time at every
   length; 4 units apart: 0.79, 0.83, 0.75, 0.68 up to 144 cells but 0.38 ± 0.06 at 192; 6 and 8 units apart at
   192 cells: 0.27 and 0.25, r.m.s. difference 3.4 generations. So a bust is coherent over about one girth
   (3.5 units) and the staggering sets in sharply between 12 and 16 units of length (144 and 192 cells): up to
   144 cells most deaths are still one crash that part of the tube misses by a little; at 192 cells there are
   typically two or three separate crashes a few generations apart.
3. **A wide face is rigid in time (9b, 9c).** Halves crash in the same generation in 0.97 ± 0.01 (108 cells) and
   0.97 ± 0.02 (192 cells) of deaths (0.89 at 63 cells, where a half is 31 cells and the largest fall is noisier);
   the four quarters all in one generation in 0.72 and 0.85, with 1.31 and 1.16 distinct crash generations
   (living faces: 3.5). Nothing changes from 108 to 192 cells.
4. **The "thinning" deaths of long tubes are staggered busts (9d).** In deaths with no face-wide fall of half
   (0.55 of deaths at 84 cells, 0.93 at 192), 0.36 to 0.45 of the sections still bust locally (over-full to
   0.68 and a fall of half; living: 0.07 to 0.12), at least one does in 91-98% and at least half of them do in
   35-58% (living: 0-8%).
5. **Surrogate against gump.** On the 84-cell tube (111 natural deaths of gump) and the wide 63-cell torus (774)
   every row agrees with the sampler's dice-chain deaths within errors: face-wide half-fall 0.53 ± 0.05 against
   0.45 ± 0.03, sections busting 0.59 ± 0.03 against 0.56 ± 0.02, section before -> after 0.73 -> 0.21 against
   0.73 -> 0.22, halves in different generations 0.17 ± 0.04 against 0.17 ± 0.02 (63 cells: 0.11 against 0.11).
   Gump itself was not looked at beyond 84 cells (no natural deaths there).

**The PI's forecasts (block 3 of `research/blast/PREDICTIONS.md`), scored.**
(1) halves in different generations, "30-45% at 84 cells, above 65% at 192": 0.17 ± 0.02 and 0.65 ± 0.08. The
rise is there, the level at 84 cells is half the forecast and the 192-cell value sits on the line: **half
right**. (2) "At the 192-cell tube at least one half loses half of its own cells in one generation in more than
half of deaths": 0.22 ± 0.06, **failed as worded**; the unit that busts is a stretch of 2 to 4 units, not a
half of 8 (at least one 2-unit section busts in 0.98, and the reading "it still busts, locally" stands). (3)
"Wide tori of 108 and 192 cells: halves in the same generation in more than 75% of deaths": 97% and 97%,
**held**. (4) "Sections 2 units long on a 144- or 192-cell tube: r.m.s. difference between neighbours 1.0-1.6
generations, no growth beyond 3 units": among busting pairs 1.93 (144) and 1.54 (192) for neighbours, then
2.44, 2.47 (144) and 2.76, 3.36, 3.44 (192) at 4, 6, 8 units: the neighbour value is about right, **the "no
growth" is wrong**: the difference keeps growing to about 6 units. (With all sections, not only busting ones,
the numbers are 2.6 to 3.7: the sections without a clear crash add noise.)

**What this does and does not show.** It shows the route: local over-fill and crash everywhere, synchronised
over about a girth, and beyond 12 units of length no longer synchronised along the tube. It does not show
causation between sections (no test of whether one crash triggers the next: differences of 3 generations over 6
units are within the speed limit of one unit per generation, so a travelling cause is possible but not needed),
and the timing statistics rest on 10 replications at 144 and 192 cells (640 dying chains each, relatives within
a replication). Not done: sections of other widths, the 96-cell tube (other twist), tubes of loop^2 13 and 16.


## Files

`geom.py` (graph, numpy stepper), `ss.c` (stepper; modes `dump`, `plain`, `ffs`, `lag`, `sub`), `validate.py`,
`nuq.py`, `nuq_quad.py` (bookkeeping forecast), `howdie.py` (anatomy of natural deaths), `run_sub.py`,
`table_sub.py`, `derived.py`, `subpaths.py`, `fill.py` (subset sampler: frozen-parameter driver, tables, dying
paths), `sections.py`, `sec_table.py`, `fill9.py` (section 9), `chain_*.sh` (the runs as launched; several were
cut short and replaced, as their headers say), `data/` (validation log, plain-run histograms, lag profiles,
paths, sampler outputs, `sections_full.txt`; `data/v1/` = sampler version 1), `PREDICTIONS.md`. Bulk, git-ignored,
under `research/scratch/blast/split-slab/`: `subpaths_full/` (25 MB), `cells/` (per-cell records of section 9).
