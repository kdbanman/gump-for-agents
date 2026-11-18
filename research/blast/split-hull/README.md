# research/blast/split-hull: a rare-event sampler for the faces of gump's octahedral hull

Agent `split-hull`, blast of 2026-11-18. Aim: ln τ_face of the 135-cell rimmed face (R = 17), which brute force
cannot reach (one death per 6 × 10¹¹ hull-generations). Files: `sh.c` (stepper and sampler), `validate.py` (stepper
against `reference/oracle.py`), `chain.sh` (replications), `ana.py` (pooling), `PREDICTIONS.md` (forecasts),
`paths/` (dying paths). Bulk output: `research/scratch/blast/split-hull/runs/`.

## State (03:55 UTC; calibration running, no result at R >= 13 yet)

- **Stepper validated [measured].** `python3 research/blast/split-hull/validate.py 1200`: `sh.c`'s bit-sliced hull
  stepper equals `reference/oracle.py` cell for cell at R = 11 and R = 15 (3 soups x 1,200 generations each), together
  with the face population counter, the emptiness bits of the seven other faces, the age counters, the ring of
  lagged states (the state two generations ago), frozen lanes and the packed-configuration round trip. Negative
  control (one neighbour swapped): fails at generation 5 (R = 11) and 3 (R = 15). Last line: `VALIDATION PASSED`.
- **Parameters frozen at 03:52 UTC on R = 9 and 11 only:** M = 300,000 trials a stage, LAG = 2 (flips at depth 5,
  two generations before the crossing), one flip per 6 sites of S, levels 3 cells apart, H = 0.5, stores of 100,000.
  The tuning runs were seeds 1 to 26 at R = 9 and 11 (not in the tables); the frozen runs use seeds R x 1000 + k.
- Calibration table: being filled by `chain.sh` (R = 9, 11, 13, 15), then R = 17.


## The sampler, exactly (for the referee who rewrites it from the oracle)

**Vessel.** Cells: p ∈ Z³ (doubled coordinates) with exactly one odd coordinate and |x| + |y| + |z| ≤ R, R odd.
Neighbours: the oracle's twelve; a neighbour outside the vessel is dead (T2 makes this the infinite lattice's own
dynamics). Face f (eight sign patterns d): the cells with d·p = R; counts 45, 63, 84, 108, 135, 165, 198 for
R = 9 … 21, hull sizes 510, 876, 1,386, 2,064, 2,934, 4,020, 5,346. The **watched face** is d = (+,+,+); P is the
number of its live cells. A face is *empty* when none of its cells is alive; adjacent faces share their rim row.

**Why forward-flux sampling.** The death rate is exactly (rate of first crossings of a level, coming from above
P̄) × (chance that such a crossing continues to an empty face before returning above P̄): the ν·q bookkeeping of
`research/dying`. Forward-flux sampling (Allen, Frenkel, ten Wolde) estimates the second factor as a product of
conditional probabilities between levels with a fixed number of trials per stage; the product of the stage
fractions is an unbiased estimate of the rate (not of its logarithm), trials are plain runs of the true rule that
fit the lanes of a bit-sliced stepper, and there are no weights to carry. Level function: P itself.

**Base run** (gives the flux and the first store). 2,048 independent hulls. A hull starts as a soup (each cell
alive with probability 0.35), age 0; every generation its age grows by 1. After each generation: if any of the
eight faces is empty the hull is replaced by a fresh soup (age 0); it is a *first death* if the generation is
counted. A hull-generation is *counted* (exposure += 1) when the hull's age after the step exceeds 200 and the
counting phase is on. Phases, in global generations: 200 of burn-in; 300 of pilot, in which P̄ and σ_P are the mean
and standard deviation of P over hulls older than 200; then λ_A = ⌈P̄⌉ and λ₀ = ⌊0.9 P̄⌋ are fixed; 100 generations
to let the flags settle; then the counting phase, until 100,000 configurations are stored.
Each hull carries a flag (0 at a soup and at the end of the pilot). From age 100 on: if P ≥ λ_A the flag becomes 1;
else if P ≤ λ₀ and the flag is 1, the flag becomes 0 and this is a **crossing** (it counts if the generation is
counted; a generation at which another face is empty and P > 0 ends the hull and is no crossing; an empty watched
face with the flag at 1 is a crossing). Φ₀ = crossings / exposure. Each counted crossing is stored with
probability H = 0.5. **What is stored is the hull's state LAG = 2 generations before the crossing** (plus, as
passengers, each face cell's age since it was last alive and the last 16 values of P as of the crossing).

**Levels.** λ₀, λ₀ − 3, λ₀ − 6, …; the first value ≤ 0 is replaced by 0, the last level (the empty face).

**Stage i** (from λ_i to λ_{i+1}). M = 300,000 trials. Trial j starts from stored configuration π(j mod N_i), π a
uniform random permutation of the N_i configurations of level i, drawn afresh for the stage. The start state is
the stored (two-generations-old) state with ⌈|S|/6⌉ **perturbations**, applied one after another: with probability
½ "kill" (one live cell of S, chosen uniformly, dies), otherwise "revive" (one dead cell of S, chosen uniformly,
comes alive); if the kind drawn has no candidate the other kind is done. **S**: the cells with x + y + z = R − 10
(the fifth layer beneath the watched face's layer) and d·p ≤ R − 4 for the seven other sign patterns (|S| = 21, 36,
54, 75, 99, 126, 156 for R = 9 … 21). Then the true rule runs. The first two generations are a **replay**: nothing
at depth five can change the face layer within two generations (a cell's neighbours are at most two layers up,
T1), so after two generations the watched face is exactly the parent's face at its crossing or success, with its
whole history, while the layers beneath it already differ between clones. (Checked in every trial by comparing P
with the parent's: `replaybad 0` in every RESULT line.) From that generation on (trial age 2, 3, …), in this order:
(1) P = 0: success (in the last stage with weight 1/k, k the number of faces empty at that generation);
(2) another face empty: failure; (3) P ≤ λ_{i+1}: success; (4) P ≥ λ_A: failure; (5) age above 20,000: failure,
booked as a timeout (none occurred). On success the state stored for level i + 1 is the trial's state **two
generations before** the success. If a stage has more than 100,000 successes a uniform subset of 100,000 is kept
(reservoir sampling). p̂_i = (sum of success weights) / M.

**Estimator.** 1/τ̂ = Φ₀ · ∏ p̂_i; ν̂(λ_i) = Φ₀ · ∏_{j<i} p̂_j; q̂ = 1/(τ̂ ν̂). By the symmetry of the eight faces the rate
at which the watched face is among the first to empty (ties shared) is 1/τ_face = deaths / (8 · exposure), the
anchors' definition (fresh soups of 0.35, ageing-in 200, a hull retired at its first death).

**Error procedure.** K independent replications of everything (base run, pilot, stores, stages; seeds R·1000 + k).
Pooled value ln τ = −ln(mean of the K rates 1/τ̂_k); error = standard deviation of the rates / (√K · mean), with
a jackknife beside it (`ana.py`). The mean of the K logarithms is printed too; it is biased upward by about half
the variance of one replication's logarithm.

**Why the lag.** Gump is deterministic, so clones must be separated, and a separation deep enough to be harmless
takes generations to reach the face, while the whole dip from 0.9 P̄ to an empty face lasts about ten generations.
Flipping one cell three layers down at the moment of the crossing left the estimator starved (scatter 0.4 to 0.5 of
one replication at R = 11 with 3 × 10⁵ trials a stage, half the replications 0.5 too high), and flipping one layer
down biased it (12.96 ± 0.10 against 13.633: `./sh` with the earlier depth argument; rows in "What failed").
Starting each clone two generations in the past moves the flips to depth five, lets the true rule launder them for
two generations, and still has the clones differ directly beneath the face at the moment of the crossing.

**Passengers.** Per face cell an 8-bit age (generations since last alive, saturating at 255), stepped with the
state and stored with it; and the last 16 values of P. Neither enters the dynamics or the selection.

## Reproduce

```sh
python3 research/blast/split-hull/validate.py 1200            # stepper against the oracle, R = 11 and 15 (~1 min)
sh research/blast/split-hull/chain.sh 13 13001 10             # 10 replications at R = 13 (frozen parameters)
python3 research/blast/split-hull/ana.py                      # pooled values, nu and q by level, path statistics
# one replication by hand:  shf R SEED M LAG NFLIP STEP H PATHFILE CAP
research/scratch/blast/split-hull/shf 11 11001 300000 2 -6 3 0.5 - 100000
```
