# research/blast/noisy: ε-noisy gump on the whole hull, and a sampler whose offset can be taken to zero

Second phase of the blast (2026-11-18, from 11:16 UTC), same agent as `research/blast/split-hull`. Aim: the
lifetime of the 135-cell hull face (R = 17) from a surrogate whose difference from gump is controlled by one
number ε that can be extrapolated to zero **at the target size**, instead of an offset extrapolated in size (the
dice chain of `split-hull`: +0.00, +0.02, +0.06 above gump at 45, 63, 84 cells, growing; `research/blast/REPORT.md`,
"The 135-cell face: not decided").

Files: `nz.c` (stepper, brute force, sampler), `validate.py` (against `reference/oracle.py`), `brute.sh`,
`ana.py` (pooling of replications), `PREDICTIONS.md`, production scripts `run_*.sh` (see "Production").
Bulk output: `research/scratch/blast/noisy/`.

## State (13:20 UTC 2026-11-18): built, validated, cheap calibrations done; production is four scripts

**1. Built and validated [measured].** `python3 research/blast/noisy/validate.py 1200`: at M = 0 the stepper is gump
bit for bit on the hull at R = 11 and R = 15 (3 soups × 1,200 generations, every cell; the watched face's counter and
the empty-face bookkeeping against the oracle's states; the noise region and board against their definition; the
dart semantics), negative control fails at generation 2 and 1; `VALIDATION PASSED`. Brute force at M = 0 gives gump:
9.8223 ± 0.0016 at 45 cells (8E/D, 407,275 deaths; anchor 9.819), and the watched face alone 9.816 ± 0.004 (0.4% of
its deaths are ties). The sampler's fast evaluation (hit lists, in-place proposals) prints the same replications,
count for count, as the plain version on three cases.

**2. The offset against ε by brute force [measured]** (`sh brute.sh R M GENS SEED`, `python3 fit.py`, part 1;
watched face; about 10,000 lives ended by it per row at 63 cells, 51,000 at 45):

```
PART 1: brute force of the noisy chain (watched face; lives it ends alone or tied)
   R  cells   eps       M   watched deaths   ln tau_watched    minus gump        8E/D (all faces)   settled
   9    45  0.00000     0      51224       9.8161 +- 0.0044           -                          9.8223 +- 0.0016   0
   9    45  0.01562     1      50919       9.8224 +- 0.0044   +0.0064 +- 0.0063 (M = 0 here)     9.8274 +- 0.0016   0
   9    45  0.03125     2      51002       9.8206 +- 0.0044   +0.0045 +- 0.0063 (M = 0 here)     9.8235 +- 0.0016   0
   9    45  0.09375     6      51068       9.8198 +- 0.0044   +0.0037 +- 0.0063 (M = 0 here)     9.8300 +- 0.0016   0
   9    45  0.29688    19      51037       9.8214 +- 0.0044   +0.0053 +- 0.0063 (M = 0 here)     9.8408 +- 0.0016   0
   9    45  1.00000    64      50870       9.8268 +- 0.0044   +0.0107 +- 0.0063 (M = 0 here)     9.8678 +- 0.0016   0
  11    63  0.01172     3       9721       13.6425 +- 0.0101   +0.0095 +- 0.0102 (anchor)         13.6396 +- 0.0036   0
  11    63  0.01562     4       9704       13.6442 +- 0.0102   +0.0112 +- 0.0102 (anchor)         13.6454 +- 0.0036   0
  11    63  0.03125     8       9801       13.6343 +- 0.0101   +0.0013 +- 0.0102 (anchor)         13.6425 +- 0.0036   0
  11    63  0.06250    16       9808       13.6336 +- 0.0101   +0.0006 +- 0.0101 (anchor)         13.6544 +- 0.0036   0
  11    63  0.10156    26      19527       13.6382 +- 0.0072   +0.0052 +- 0.0072 (anchor)         13.6643 +- 0.0026   0
  11    63  0.25000    64       7336       13.6364 +- 0.0117   +0.0034 +- 0.0117 (anchor)         13.6918 +- 0.0042   0
  11    63  0.30078    77       9901       13.6242 +- 0.0100   -0.0088 +- 0.0101 (anchor)         13.6937 +- 0.0037   0
```

- **At 45 and 63 cells there is no offset to see: within ± 0.01 of gump for every ε from 1/64 to 0.3** (63 cells:
  weighted mean of the seven rows +0.003 ± 0.004). So "linear in ε" cannot be tested there; the slope is below about 0.05 per unit ε
  at 63 cells. One row (63 cells, ε = 0.10) first read +0.032 ± 0.010; a second seed brought the pooled value to
  +0.005 ± 0.007.
- **The other seven faces do feel the noise** (it is only 3 layers under them): the eight-face value 8E/D rises
  linearly, +0.007, +0.010, +0.021, +0.031 at ε = 0.012, 0.031, 0.0625, 0.10 at 63 cells (0.3 per unit ε), bending to
  +0.059 at 0.25 and +0.061 at 0.30; at 45 cells +0.046 at ε = 1. Noise three layers under a face lengthens its life; six layers
  under, at these sizes, it does nothing measurable. This is the depth dependence the construction relies on.
- 84 cells by brute force is stage A1 below (4.4 core-hours per ε for ± 0.022).

**3. The sampler [measured].** Tuned at 63 cells (48 replications per setting; `ana.py` on scratch `tune/`): the
scatter of one replication falls with the number of sweeps faster than the cost rises (0.47, 0.22, 0.13 of the mean
at 10, 20, 40 sweeps, ε = 0.10), 15 flips per proposal are steadier than 5 at small ε and 30 or more are worse.
Frozen (`PREDICTIONS.md` block 2 and its amendment): KFLIP 15, NSWEEP = round(0.6 A), the rest as on the dice
chain. With the frozen parameters (`sh run_sub.sh R M SEED0 NRUNS`, `python3 fit.py` part 2):

```
PART 2: the sampler (frozen parameters), and the extrapolation to eps = 0
   R   eps        M   NSWEEP    K    ln tau            scatter   largest share   carry half   running value (every 100)
  11  0.01562     4     38    100   13.620 +- 0.021    0.21      0.020           43       13.620
  11  0.06250    16     38    100   13.653 +- 0.015    0.15      0.014           44       13.653
  11  0.25000    64     38    100   13.639 +- 0.013    0.13      0.014           45       13.639
  13  0.06250    64     50    100   18.173 +- 0.029    0.29      0.025           41       18.173
  R = 11: weighted mean 13.641 +- 0.009 (chi2 1.7 on 2);  line: intercept 13.641 +- 0.015, slope +0.00 +- 0.09 per unit eps (chi2 1.7 on 1);  gump 13.633 +- 0.001: mean - gump +0.008 +- 0.009, intercept - gump +0.008 +- 0.015
  R = 13: weighted mean 18.173 +- 0.029 (chi2 0.0 on 0);  gump 18.141 +- 0.005: mean - gump +0.032 +- 0.029
```

- **Against brute force at 63 cells:** ε = 1/16: sampler 13.653 ± 0.015, brute force 13.634 ± 0.010 (+0.019 ± 0.018);
  ε = 1/4: 13.639 ± 0.013 against 13.636 ± 0.012 (+0.003 ± 0.018); ε = 1/64: 13.620 ± 0.021 against 13.644 ± 0.010
  (−0.024 ± 0.023). 100 replications each; **exact within 1.1 errors at all three**. The line in ε through the
  three sampler values has intercept 13.641 ± 0.015 and slope 0.00 ± 0.09: **intercept − gump = +0.008 ± 0.015**
  (weighted mean − gump +0.008 ± 0.009). At 63 cells the method returns gump.
- **84 cells, ε = 1/16, 100 replications: 18.173 ± 0.029**, gump 18.141: +0.032 ± 0.029. No brute force of the chain
  there yet (stage A1).
- **Efficiency against ε** (the trade the PI expected): at 84 cells one replication scatters by 0.20, 0.22 to 0.29,
  0.53, 2.0 of the mean at ε = 1/4, 1/16, 1/64, 1/256 (24 replications each in tuning, 100 at 1/16); at 1/256 two
  replications of 24 carry half the rate. At 63 cells the scatter is 0.13, 0.14, 0.26 at ε = 0.10, 0.031, 0.012 (40
  sweeps). Small ε means few darts (ε|N| per generation: 2.6 at 84 cells and ε = 1/64), too few to steer the face, and
  the estimate falls back on rare initial states. The cost of a replication grows the other way, with ε|N|
  (84 cells: 9, 13, 30 s at ε = 1/64, 1/16, 1/4). Hence ε = 1/16, 1/32, 1/64 at 108 and 135 cells (10 to 42 darts on N
  per generation at 135 cells).

**4. Production: four scripts, each one command, output usable at any time** (replications are whole lines).

| script | cores | hours (estimated) | what it decides |
|---|---:|---:|---|
| `sh research/blast/noisy/prod_A_brute84.sh` | 4 | 2.5 | The chain's own offset at 84 cells at ε = 1/16 and 1/64 (± 0.022 each) against gump's 18.141: is it zero, as at 45 and 63 cells, or does it appear with size as the dice chain's did (+0.06)? Also whether the sampler is exact at 84 cells (it reads 18.173 ± 0.029 at ε = 1/16). |
| `sh research/blast/noisy/prod_A_sub84.sh` | 3 | 1.5 | The sampler at 84 cells at ε = 1/64, 1/32, 1/4: the line in ε where gump is known; how many replications ε = 1/64 needs. |
| `sh research/blast/noisy/prod_B_108.sh` | 4 | 2.5 | 108 cells, blind (forecast in block 2): ε = 1/16, 1/32, 1/64, 440/300/360 replications; intercept at ε = 0 against gump's 23.3392. |
| `sh research/blast/noisy/prod_C_135.sh [ROUND]` | 4 | 8 per round | 135 cells: ε = 1/16, 1/32, 1/64, 500/360/450 replications per round; the line in ε and its intercept; rounds add up (fresh seeds). |

Order: A1 and A2 can run together only on 7 cores; on 4, A1 first (it is the test of the construction), then A2,
B, C. After each: `python3 research/blast/noisy/fit.py` (brute-force table; per-ε values with scatter, largest
share, "replications that carry half the rate" and running values; the line in ε per size). Times for 108 and 135
cells are scaled from 84 cells (cost per trajectory = a part proportional to the hull plus 0.13 ms per dart on N per
generation), not measured: nothing has been run above 84 cells with the frozen parameters.

**5. Not checked.** Brute force of the chain at 84 cells (stage A1). The sampler above 84 cells. Whether the offset
is linear in ε anywhere (it is zero within ± 0.01 where measured). Convergence in the number of sweeps beyond 40 at
63 cells. Other noise regions (a slab of a few layers at depth 6 would cost fewer darts for the same steering).
Whether the dart law's deviation from independent coins matters (it should not: both are honest and go to gump).
The settled-life guard has fired once (R = 9); settled lives at larger sizes were not looked for beyond it.

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
S=research/scratch/blast/noisy
# brute force rows of the table (seed = 900 + M at R = 9 with 2,000,000 generations; at R = 11: 16,000,000 generations,
# seeds 1177, 1126 and 1127, 1108, 1103, 1116, 1104, and 1164 with 12,000,000):
sh research/blast/noisy/brute.sh 11 26 16000000 1126          # one line appended to $S/brute.txt (about 6 minutes)
# sampler with the frozen parameters (63 cells: seeds 11100.., 11800.., 11400..; 84 cells: 13100..):
sh research/blast/noisy/run_sub.sh 11 16 11100 10             # 10 runs x 10 replications, eps = 1/16 at R = 11 (4 minutes)
sh research/blast/noisy/run_sub.sh 13 64 13100 10             # eps = 1/16 at R = 13 (22 minutes)
python3 research/blast/noisy/fit.py                           # both tables and the line in eps, from the committed rows in data/
python3 research/blast/noisy/fit.py $S                        # the same from scratch (runs still in progress)
python3 research/blast/noisy/ana.py $S/tune                   # the tuning runs (63 cells: t_M<M>_K<KFLIP>_S<NSWEEP>.txt; 84: t84_...)
# tuning runs were made as:  $S/nz 11 sub SEED 48 18 3 8 NSWEEP KFLIP 32 24 12 M > $S/tune/t_M<M>_K<KFLIP>_S<NSWEEP>.txt
#   (seed 21 for the first eight settings, 22 for the rest; 84 cells: nz 13 sub 31..34 24 28 3 8 50 15 32 24 12 M)
```

## Added by the PI after the review of pull request 39 (17:57 UTC, 2026-11-18)

- **The rows are in the repository.** `data/brute.txt` (the brute-force table, part 1), `data/runs/` (every sampler
  row with the frozen parameters: 63, 84 and 108 cells) and `data/tune/` (the tuning runs). `fit.py` and `ana.py`
  read `data/` unless given another directory; from `data/` and from scratch `fit.py` prints the same 28 lines.
- **Ancestry.** `nz.c` in `sub` mode prints after each `REP` line a line `ANC rep : λ:D/top ...`: for each level,
  D = the number of distinct initial chains that the chains at or below λ descend from, and top = the share of the
  largest family among them. It uses no random numbers: the `REP` lines are bit for bit those of the build before
  (checked on seed 11100 at 63 cells).
- **`diag.sh`**: the frozen sampler with new seeds and the ancestry lines (63, 84, 108 cells), then the 108-cell
  sampler at ε = 1/16 with the odd sweeps off (WBACK 0). Output in scratch `runs_diag/`; results in `REPORT.md`.

## The method's limit (PI, 20:52 UTC 2026-11-18, after the lead's rebuild; this belongs next to the method)

- **The sampler never moves the initial state.** Across initial states it is plain sampling of a long-tailed
  quantity (the chance that a given stationary state dies within the window). At 63 and 84 cells that tail is
  mild and the sampler matches brute force. At 108 cells about one replication in 280 has a rate above ten
  times the median, one initial state can hold most of the dying chains, and a replication's rate follows that
  share. So at 108 cells **the error from the scatter of replications understates**, a sample that has met no
  large replication reads high in ln τ, and an inverse-variance mean over ε favours exactly those samples.
  `fit.py` prints the equal-weight value beside the weighted one for this reason.
- **What to change, if this is taken up again:** the initial states, not ε. Either an independence move over
  stationary snapshots (accepted iff the score stays under the level) with a pool drawn afresh for each
  replication, or a pool large enough that its largest weight is small: with one shared finite pool every
  replication is exact for the pool's own law, and the pool's tail becomes a common error (the lead's point).
  Test it where the answer is known, 63 cells and then 84 cells at ε = 1/4 (brute force +0.027 ± 0.038), before
  108 cells.
- **Odd sweeps.** Read twice as reversible (here and by the rebuild), and cleared by measurement at 84 cells and
  ε = 1/16: on 18.142 ± 0.010 (1,050 replications), off 18.146 ± 0.009 (1,040), on minus off −0.001 ± 0.014, gump
  18.141 ± 0.005 (`data/runs_diag/`, `diag2.sh`, `diag3.sh`). At 108 cells on minus off was +0.092 ± 0.050, with
  both errors from a law whose tail the samples had not caught.
- **The depth series** (`data/depth.txt`, `diag2.sh`): coins at depth ≥ d under the watched face at 63 cells and
  ε = 1/4 move its ln τ by −0.005, +0.019, +0.054, +0.101, +0.304, +0.674 for d = 6 … 1 (± 0.012 to 0.016).
  Repeated by the lead's rebuild on other seeds (`research/audit/blastnoisy/depth.sh`); pooled: +0.003, +0.023,
  +0.040, +0.112, +0.315, +0.670. Not run: the same with coins at each replaced layer's own density, which
  separates "coins are denser than gump's layer" from "coins are uncorrelated with the face" (open problem 9 (r)).
  In `nz.c` only the brute path needs it (its darts are drawn on the fly, so a coin of any bias is one comparison;
  the sampler's fair bits are not touched), and the layer densities can be measured by the same binary at M = 0.
