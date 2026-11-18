# research/blast/noisy: ε-noisy gump on the whole hull, and a sampler whose offset can be taken to zero

Second phase of the blast (2026-11-18, from 11:16 UTC), same agent as `research/blast/split-hull`. Aim: the
lifetime of the 135-cell hull face (R = 17) from a surrogate whose difference from gump is controlled by one
number ε that can be extrapolated to zero **at the target size**, instead of an offset extrapolated in size (the
dice chain of `split-hull`: +0.00, +0.02, +0.06 above gump at 45, 63, 84 cells, growing; `research/blast/REPORT.md`,
"The 135-cell face: not decided").

Files: `nz.c` (stepper, brute force, sampler), `validate.py` (against `reference/oracle.py`), `brute.sh`,
`ana.py` (pooling of replications), `PREDICTIONS.md`, production scripts `run_*.sh` (see "Production").
Bulk output: `research/scratch/blast/noisy/`.

STATE_PLACEHOLDER

## The chain, exactly

- **Vessel and rule.** Every cell p (doubled coordinates, exactly one odd) with |x| + |y| + |z| ≤ R, R odd; the
  oracle's twelve neighbours, a neighbour outside the hull dead; gump's rule B45/S345 on every cell. All eight
  faces are real (face f: d_f·p = R). The watched face is d = (+,+,+).
- **Noise region N.** The cells at depth ≥ 6 under the watched face and ≥ 3 under each of the other seven faces
  (depth of p under face f: (R − d_f·p)/2). |N| = 9, 57, 168, 366, 675, 1,119 for R = 9 … 19 (of 510, 876, 1,386, 2,064,
  2,934, 4,020 cells). No face's own three outer layers are touched; the watched face has six clean layers.
- **Noise law: darts.** After every generation M darts are thrown, one after another, at a board of B squares,
  B the smallest power of two ≥ 4|N| (64, 256, 1,024, 2,048, 4,096, 8,192). The first |N| squares are the cells of N
  (in the order of the cell table: x, then y, then z ascending, the watched face's cells excluded as they come
  first), the others are empty. A dart on a cell sets that cell to the dart's own fair coin. **ε = M/B** is the
  expected number of darts per cell and generation; a cell is replaced with probability 1 − (1 − 1/B)^M ≈ ε for
  small ε, nearly independently of the others (the number of darts on N is Binomial(M, |N|/B)). M = 0 is gump.
  *Why darts and not an independent coin per cell:* the chain's randomness is then a string of independent fair
  bits (log₂B bits of square and one coin per dart) every one of which matters, which is what the sampler needs
  (flipping a bit is a symmetric move that preserves their law), and it is short at small ε. The price: ε is a
  multiple of 1/B, and "probability ε per cell" holds only to first order.
- **Life protocol (the anchors').** A hull starts as a soup (each cell alive with probability 0.35), age 0. A life
  ends at the first generation at which any of the eight faces is empty. Brute force (`nz R brute SEED GENS M`):
  512 hulls; 200 generations of ageing-in; a hull-generation is counted when the hull's age after the step
  exceeds 200; τ_watched = exposure / (lives ended by the watched face, alone or tied); at ε = 0 this is gump's
  τ_face = 8·exposure/deaths up to ties (0.4% of the watched face's deaths at 45 cells are tied). The noise breaks
  the symmetry between the faces, so at ε > 0 only the watched face's count is used for the watched face.
  A hull whose watched face's population has had period 2 or a period dividing 12 for 4,096 generations is a
  settled life: counted, replaced (one seen in 2 × 10⁹ hull-generations at R = 9, none elsewhere so far).

## The sampler, exactly (split-slab's subset simulation, over the darts)

`nz R sub SEED NREP LAM1 DELTA NBATCH NSWEEP KFLIP TPRE TWIN WBACK M [DW DO [PATHFILE]]`

- A chain = (initial state, T = TPRE + TWIN generations of darts, M per generation, each 16 bits: the square in
  the low log₂B bits and the coin in bit 15). Initial states: snapshots, 64 generations apart, of 512 lanes of the
  noisy chain run under the life protocol (1,000 generations of burn-in; a lane is used only at age ≥ 1,000).
- Score S = the minimum population of the watched face over generations TPRE+1 … T **while the life lasts**: the
  life ends at the first generation g_o at which another face is empty; generation g_o itself still counts (a tie
  is a death of the watched face), later ones do not. A chain with any face empty at generation TPRE has no score.
  P(S = 0) = TWIN / τ_watched (to first order in T/τ).
- Levels λ₁ = LAM1, then −DELTA while positive, then 0. P₁ = share of the valid fresh chains with S ≤ λ₁. At each
  level the chains with S ≤ λ_i are copied round-robin from a uniform random offset into an ensemble of
  NBATCH × 512 and moved by NSWEEP Metropolis sweeps. A proposal flips KFLIP bits of the chain's darts (a bit of a
  square, or a coin): on even sweeps anywhere in the T generations, on odd sweeps in the WBACK generations before
  g_min, the first generation at which the chain attains its minimum. It is accepted iff S′ ≤ λ_i and, on odd
  sweeps, every flipped bit lies in the WBACK generations before the new g_min′ (so that the reverse move is
  proposable). P_{i+1} = share of the ensemble with S ≤ λ_{i+1} after the sweeps.
- Estimate 1/τ = (∏P_i)/TWIN. Error: independent replications (each run has its own 512 lanes; replications of
  one run use later windows of them); pooled value −ln(mean rate), error from the scatter of the rates, and the
  number of replications that carry half of the summed rate (`ana.py`).
- Exact for the chain for any ε > 0 **[proved, standard]**: the dart bits are independent and fair, a flip
  preserves their law, acceptance on the indicator of {S ≤ λ_i} (with the reversibility condition on odd sweeps)
  leaves the conditioned law invariant, and the seeds are exact draws from it by induction.

## Reproduce

```sh
python3 research/blast/noisy/validate.py 1200                 # stepper = gump at M = 0, R = 11 and 15; negative control
sh research/blast/noisy/brute.sh 11 26 16000000 1126          # brute force, R = 11, M = 26 (eps 0.10): one line in scratch brute.txt
python3 research/blast/noisy/ana.py                           # pooled sampler values from scratch runs/
```
