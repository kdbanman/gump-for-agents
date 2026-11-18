# research/blast/split-slab: a rare-event sampler for wrapped faces (agent split-slab, 2026-11-18)

Brief: build a multilevel-splitting sampler for gump's wrapped faces (8-layer slab tori), calibrate it against
the anchors, then reach 120 cells and beyond. **Outcome: the sampler was built and it is correct, but it does not
beat brute force, for a reason that is itself the main finding: a face does not die by a dip that deepens, it dies
by one over-full generation followed by a one-generation crash, so there is no ladder of levels to split on.**
What is delivered instead: a validated stepper, the negative result with its numbers, an independent account of
how wrapped faces die (48 to 84 cells, with the paths), and a 120-cell forecast from exact bookkeeping plus a
three-point continuation that was first tested blind on the 108-cell tube.

Marks: **[proved]**, **[measured]**, **[conjectured]**. All runs: one core (the machine gave it 40-50%).
Binary: `gcc -O3 -march=native -o research/scratch/blast/split-slab/ss research/blast/split-slab/ss.c -lm`
(below `ss`; `G/` = `research/scratch/blast/split-slab/`, geometry files from `python3 geom.py H K D G/g_H_K_D.bin`).

## 1. Stepper and validation [measured]

`geom.py` builds the slab graph from `docs/AUTOMATON.md` alone: cube index (i, j, k), layer l = i + j + k in 0..7,
in-plane period lattice (H, K), (0, D) acting by cube translations (x, y, -x - y); cell id
((l H D + i' D + j') 3 + a); it asserts T1's layer histogram and the symmetry of the neighbour relation.
`ss.c` steps 512 lanes bit-sliced (carry-save count of the 12 neighbours, B45/S345).

    python3 validate.py H K D 1200 [N]        # log: data/validate.log

A 0.4 soup on the slab torus, tiled into `reference/oracle.py`'s cubic torus of N^3 cubes (N = H D, or 12 for
(4,0),(0,4) and (6,0),(0,6)), must equal the oracle's array **as a set of cells at every generation 0..1200**, for
two lanes of `ss` (lanes 0 and 311) and for a numpy stepper on the same graph. Negative control: one neighbour
entry replaced; must fail. Result: **MATCH on all nine tori used** ((4,0),(0,4); (1,4),(0,21); (1,6),(0,26);
(1,12),(0,28); (1,4),(0,28); (1,17),(0,32); (1,16),(0,36); (6,0),(0,6); (1,18),(0,40)); the swapped graph is
detected on every one (first mismatch at generation 7 to 19).
Not validated against the oracle: the event bookkeeping (face death, excursions); it is checked only by the
lifetimes below agreeing with the anchors.

## 2. The splitting sampler: exact statement

`ss G ffs SEED NREP PA LAM0 DELTA M N0TGT NFLIP FDEP0 FDEP1 NPATH [PATHFILE]`

- Level function: the population p of one face layer (layer 0 or layer 7). Basin A = {p >= PA}. Levels
  lam_0 = LAM0 > lam_1 = LAM0 - DELTA > ... > 0 (while positive), last level 0 (the face is dead).
- Stage 0 (exact, no perturbation): 512 lanes of plain gump from a 0.4 soup (1,000 generations of burn-in after
  every reseed; a lane is reseeded when a face dies or at age 50,000). For each lane and face, a *crossing* is the
  first generation with p <= lam_0 since the face was last >= PA. Phi = crossings / face-generations. The slab
  state at each crossing is stored (the first M of a window). The same pass books every excursion's minimum
  (until the face is back at >= PA, or dead): nu(p) = excursions with minimum <= p per face-generation, and the
  brute-force lifetime E/deaths. One persistent ensemble; replication r uses the r-th window (at least N0TGT
  crossings, checked every 64 generations).
- Stage i = 1..n: M trials. Trial j takes parent (r0 + j) mod S_{i-1} among the S_{i-1} states stored at level
  i-1 (r0 uniform), copies it, flips NFLIP cells, each uniform over the layers at depth FDEP0..FDEP1 beneath the
  active face (depth d = layer d for face 0, layer 7 - d for face 1), and runs plain gump until the active face has
  p <= lam_i (success; state stored) or p >= PA (failure; also a failure after 1,000 generations).
  P_i = successes / M. A parent already at p <= lam_i gives an immediate success (flips applied).
- Estimate: 1/tau_face = Phi * prod P_i. Error: NREP independent replications of the whole estimator; the mean of
  their rates, and the standard error from their scatter. Never a binomial formula.
- `WD=w ss ...` runs the same code on the *dice chain*: layers 0..w-1 on the rule, layers w and w+1 replaced after
  every generation by fair coin flips, one face. A true Markov chain: splitting is exactly unbiased there with
  NFLIP = 0.

## 3. Why splitting fails here [measured]

PENDING-SPLIT

## 4. How a wrapped face dies (natural deaths, no flips) [measured]

PENDING-DEATH

## 5. The 120-cell tube from exact bookkeeping [measured + conjectured continuation]

PENDING-NUQ

## 6. Reactive paths (deliverable 4)

PENDING-PATHS

## 7. Not checked

PENDING-NOT

## Files

`geom.py` (graph, numpy stepper), `ss.c` (stepper; modes `dump`, `plain`, `ffs`, `lag`), `validate.py`,
`nuq.py` (bookkeeping forecast), `howdie.py` (anatomy of deaths), `chain_tube.sh`, `chain_paths.sh` (the runs),
`data/` (validation log, plain-run histograms, lag profiles, paths), `PREDICTIONS.md`.
