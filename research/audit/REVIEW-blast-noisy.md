# Audit of `research/blast/noisy/` (pull request 39): the noisy hull chain and its sampler

2026-11-18. Subject: pull request 39 at a879e34 (`research/blast/noisy/`, and the entries of 14:57 and 16:40 UTC in
`research/blast/REPORT.md`). From its later head b80248c only the committed rows (`noisy/data/runs/`: 63, 84 and
108 cells) and the diff of `nz.c` were used; the author's forecasts for this rebuild were read after sections 0 to 7
were written (section 9). Everything built here is in `research/audit/blastnoisy/` (code, `run.sh` with every
command and its run time, small tables in `data/`); bulk output is in `research/scratch/audit_noisy/`.
Marks: **[measured here]** = this audit's own code and runs; **[read]** = judged from the pull request's files;
**[rows]** = computed here from the pull request's committed rows. ln τ is the natural logarithm of a face's
lifetime in generations; "gump" is the lead's anchor for the closed hull (13.633 ± 0.001, 18.141 ± 0.005,
23.3392 ± 0.0099 at 63, 84, 108 cells a face).

## Verdict in brief

| | claim of the pull request | verdict |
|---|---|---|
| 1 | The chain: gump on the hull, M darts a generation on the region N (depth ≥ 6 under the watched face, ≥ 3 under the others), ε = M/B, ε = 0 is gump | **confirmed** by a rebuild from the README (§0): same N (9, 57, 168, 366 cells), same board, the dart law to its second moment; with the noise off the rebuilt stepper is the oracle state for state and the lead's recorder `fd.c` count for count |
| 2 | Brute force: the watched face lives as long as gump's within ± 0.01 at 45 and 63 cells for ε from 1/64 to 0.3; the other seven live longer, about 0.3 per unit ε | **confirmed and extended** (§1): at 45 and 63 cells no offset to ± 0.002 and ± 0.005 on average, up to ε = 1 (every cell of N a coin with probability 0.63 a generation); at 84 cells and ε = 1/4, new here, +0.027 ± 0.038. The other seven: confirmed in size, but they are three classes, and the gain bends with ε and grows with the face |
| 3 | The sampler is exact for the chain at any ε > 0 and agrees with brute force at 63 cells | **confirmed with two riders** (§2, §3): the moves are reversible and the estimator unbiased [read]; against this audit's brute force it reads −0.000 ± 0.009 and −0.006 ± 0.008 at 45 cells, −0.003 ± 0.010 and +0.013 ± 0.012 at 63 cells (ε = 1/16 and 1/4), −0.057 ± 0.063 at 84 cells and ε = 1/4, and it does not move with DELTA or NSWEEP. Riders: "exact" is a statement about the mean of the rate over replications, and the law of one replication's rate has a heavy tail at 108 cells because initial states are never moved; and the sampler measures hulls 1,000 to 6,000 generations old (shown equal to the life average at 63 cells and +0.018 ± 0.019 from it at 84 cells) |
| 4 | 108 cells: 23.422 ± 0.025, 23.228 ± 0.119, 23.368 ± 0.065; weighted mean +0.069 ± 0.025 above gump; intercept −0.025 ± 0.083; "an offset that grows with the face, real for this chain or for its sampler" | **numbers reproduced; the reading corrected** (§4, §5): the weighted mean is the ε = 1/16 value under another name and is not a fair summary; the mean of all 1,100 rates is +0.009 ± 0.044 from gump. The offset at ε = 1/16 is most likely neither the chain's nor a bias of the sampler but its tail: one replication in 283 at 108 cells has a rate above ten times the median, those carry 7.7% of the summed rate, and the 440 replications at ε = 1/16 met none (a one-in-five chance). "The method as tuned does not decide the 135-cell face" stands, for a sharper reason |

What the review found beyond the pull request is in §6; what it did not check in §8.

## 0. The rebuild and what anchors it [measured here]

`nb.c` is a brute force of the chain written from the README's section "The chain, exactly" before `nz.c` was
opened. It takes the hull as a graph from `research/audit/blast/geom.py` (the oracle's offsets) and uses the
bit-sliced rule of `research/audit/blast/fd.c`; the noise region is built from the face layers of the graph file;
the darts have two forms, L (M darts of 16 bits on a board of B squares, as the README words it) and F (the number
of darts on N by inversion of the binomial, uniform cells by multiply-and-reject, then a fresh coin for every hit
cell; the same law, 3 to 10 times faster).

- `python3 research/audit/blastnoisy/validate.py` (1 to 3 minutes): **VALIDATION PASSED**. Noise off: nb = oracle on
  every cell of 4 hulls for 1,200 generations at R = 11 and 13; a swapped neighbour entry fails at generation 4.
  Noise on: nb's states equal those of a slow reference that steps with `oracle.step` and applies the same darts
  (read from the same generator) to a region built in the script from the doubled coordinates, for L and F, at
  R = 9, 11, 13, 15 (M = 4 to 256, 60 to 300 generations, 650 to 17,000 darts on N applied to the four tracked hulls per case); the reference with
  two cells of N swapped, or with the darts thrown before the step, fails at generation 1. The law of one
  generation's darts: mean and variance of the number of distinct cells hit, the coin, the per-cell frequency and
  "nothing outside N" agree with M darts on B squares for L and F (the variance is 7 to 21% below that of
  independent coins, as the law says: 2.556 measured, 2.557 by the law, 3.250 for independent coins at 63 cells,
  ε = 1/16).
- |N| = 9, 57, 168, 366 and B = 64, 256, 1,024, 2,048 for R = 9 to 15, by nb from the graph and by the script from
  coordinates; the README's numbers.
- **nb equals the lead's recorder count for count.** With fd's soup (0.4) and ageing-in (1,000 generations) and
  fd's seed, `nb hull_11 run 21 22000000 0 F 999 2000000 0 0.4` gives exposure 11,156,152,152, 106,948 deaths and
  1,033 young deaths: the numbers of `research/scratch/audit_blast/hull63_s21.sum` (fd.c, 22,000,000 generations
  of 512 hulls). nb is three to five times faster than fd for plain lifetimes (13 µs a generation of 512 hulls
  at 84 cells): 2,500 deaths of an 84-cell hull face cost 10 minutes of one core.
- nb with the README's protocol (soup 0.35, 200 generations of ageing-in) and the noise off returns gump:
  13.6336 ± 0.0032 at 63 cells (98,077 deaths; anchor 13.633), 18.122 ± 0.014 at 84 cells (4,968 deaths in two
  seeds; anchor 18.141 ± 0.005), 9.8202 ± 0.0014 at 45 cells. L and F give the same lifetimes at 45 cells
  (9.8223 ± 0.0040 and 9.8175 ± 0.0040 at ε = 1/16; 9.8213 ± 0.0051 and 9.8207 ± 0.0040 at ε = 1).

## 1. The chain by brute force (claims 1 and 2) [measured here]

`python3 research/audit/blastnoisy/summary.py`, table 1 (from `data/brute/`; runs: `sh run.sh brute`). "Watched" =
ln(exposure / lives ended by the watched face, alone or tied); "others" = the same for the seven other faces
together; both minus gump.

```
cells   eps     M  runs  watched deaths   ln tau watched      minus gump           other seven faces    minus gump
   45  0.0000    0    1      64042        9.8158 +- 0.0040   -0.0044 +- 0.0042     9.8208 +- 0.0015   +0.0006 +- 0.0020
   45  0.0625    4    2     127640        9.8199 +- 0.0028   -0.0003 +- 0.0031     9.8283 +- 0.0011   +0.0081 +- 0.0018
   45  0.2500   16    1      63407        9.8272 +- 0.0040   +0.0070 +- 0.0042     9.8379 +- 0.0015   +0.0176 +- 0.0021
   45  1.0000   64    2     102323        9.8209 +- 0.0031   +0.0007 +- 0.0034     9.8708 +- 0.0012   +0.0506 +- 0.0019
   63  0.0000    0    1      12420       13.6206 +- 0.0090   -0.0124 +- 0.0090    13.6354 +- 0.0034   +0.0024 +- 0.0036
   63  0.0625   16    2      24169       13.6480 +- 0.0064   +0.0150 +- 0.0065    13.6587 +- 0.0024   +0.0257 +- 0.0026
   63  0.2500   64    1      12399       13.6224 +- 0.0090   -0.0106 +- 0.0090    13.7002 +- 0.0035   +0.0672 +- 0.0037
   63  1.0000  256    1       6157       13.6293 +- 0.0127   -0.0037 +- 0.0128    13.7639 +- 0.0052   +0.1309 +- 0.0052
   84  0.0000    0    2        694       18.0111 +- 0.0380   -0.1299 +- 0.0383    18.1392 +- 0.0153   -0.0018 +- 0.0161
   84  0.2500  256    1        725       18.1681 +- 0.0371   +0.0271 +- 0.0375    18.2681 +- 0.0148   +0.1271 +- 0.0156
45 cells, watched face, weighted over eps > 0: +0.0016 +- 0.0018 (chi2 2.4 on 2)
63 cells, watched face, weighted over eps > 0: +0.0049 +- 0.0048 (chi2 5.9 on 2)
```

(At M = 0 the eight faces are equivalent and gump is the eight-face value; "watched" is then face 0 alone, see §6
for its count at 84 cells. Errors of the weighted lines do not include the anchor's.)

- **45 and 63 cells: no offset of the watched face at any noise.** Weighted over ε > 0: +0.002 ± 0.002 at 45 cells,
  +0.005 ± 0.005 at 63 cells. The largest single reading is +0.015 ± 0.007 at 63 cells and ε = 1/16 (two seeds:
  +0.023 ± 0.009 and +0.007 ± 0.009; the pull request's own row there is +0.001 ± 0.010); at four and sixteen times the noise the same
  face reads −0.011 ± 0.009 and −0.004 ± 0.013, so it is not an effect of ε. Claim 2's "within ± 0.01" holds.
- **84 cells, ε = 1/4** (a size the pull request did not run by brute force): 18.168 ± 0.037, **+0.027 ± 0.038 from
  gump** (725 deaths of the watched face in 5.6 × 10¹⁰ hull-generations, one seed, 106 minutes). The reading
  wandered on the way: +0.19 ± 0.07 after 225 deaths, +0.08 ± 0.04 after 538. With the sampler's value at the same
  point (§3) the chain is at +0.007 ± 0.030 from gump at four times the ε of the 108-cell claim. If an offset is proportional to ε, as the other
  faces' is up to ε = 1/4, that bounds the chain's offset at 84 cells and ε = 1/16 by about +0.03 (two errors).
- **The other seven faces** gain +0.026 ± 0.003, +0.067 ± 0.004, +0.131 ± 0.005 at 63 cells for ε = 1/16, 1/4, 1
  (0.41, 0.27, 0.13 per unit ε: "about 0.3" holds between, and the gain bends), +0.008, +0.018, +0.051 at 45 cells,
  +0.127 ± 0.016 at 84 cells and ε = 1/4. They are not one class: the three faces that share an edge with the watched
  face gain least, the three that share only a corner more, the opposite face most (63 cells, ε = 1/4: +0.034,
  +0.086, +0.112, each ± 0.005 to 0.010; ε = 1: +0.090, +0.151, +0.201), because the watched face's six clean
  layers take noise away from under its neighbours. So at 63 cells full noise three layers under a face lengthens
  its life by a fifth (the opposite face), and six layers under it does nothing measurable (−0.4 ± 1.3%).

## 2. The sampler, read (claim 3) [read]

`nz.c` at a879e34; at b80248c it differs by 14 lines that only record and print ancestry (arrays `anc`, `anc2`,
`fam`, the `ANC` line); they use no random number and change no branch of the sampler.

- **Even sweeps.** KFLIP bits are flipped at positions drawn independently of the state; accepted iff the new score
  is ≤ λ. A flip preserves the law of the darts (each dart is log₂B + 1 independent fair bits). Reversible.
- **Odd sweeps.** Positions are drawn in the WBACK generations before g_min; the move is refused unless every drawn
  position lies in the WBACK generations before the new g_min. Both windows have WBACK·M·(log₂B + 1) positions, so
  the same list of positions has the same probability from either end, and the kernel is symmetric on
  {S ≤ λ}: reversible. (The generation offset and the bit number of a flip are cut from overlapping bits of one
  random word, `(z >> 40) % WBACK` and `(z >> 24) % cbits`, so they are independent only to about 2 × 10⁻⁴; this
  matters only for odd-sweep moves that change g_min, and is far below every error here.)
- **Estimator.** The product of the level fractions with round-robin copies from a uniform offset (each survivor
  has the same expected number of copies) and kernels that leave each level's law invariant: unbiased for
  P(S = 0 | alive at TPRE) by the standard argument for fixed-level splitting, whatever the number of sweeps. It
  is the mean rate that is unbiased, and the pull request pools rates before taking the logarithm.
- **Chains without a score** (a face empty at generation TPRE) are left out of the first level's denominator and
  can never be accepted as a proposal (their score is 2²⁰): the target is conditioned on being alive at TPRE,
  which is the brute force's "per hull-generation with all eight alive" to first order in 56/τ. No bias.
- **Initial states are never moved.** That is allowed (a kernel that fixes the initial state and is invariant for
  the darts given it is invariant for the pair), so it costs no bias; it costs variance, §4.
- **Two things "exact" does not cover.** (i) The initial states are lanes 1,000 to about 6,000 generations old;
  brute force averages over lives of 10⁵ (63 cells) to 10⁹ (108 cells) generations. If a hull's hazard depended on
  its age the sampler would measure another number. At 63 cells it does not [measured here, §6]. (ii) Replications
  of one run share lanes; from the rows the variance between run means is 0.9 to 1.1 of what independent
  replications give at 108 cells [rows], so the pull request's errors are not understated on that account.

## 3. The sampler, tested (claim 3) [measured here]

The pull request's binary (`nz_author`, unmodified) for the frozen 63-cell sets; elsewhere `nz_anc`, the same
source with ancestry columns added by `patch_anc.py` (it prints the same REP numbers for the same seed).
`python3 research/audit/blastnoisy/summary.py`, tables 2 and 3.

```
cells   eps    who            replications  ln tau sampler      scatter   brute force (nb)     sampler - brute      sampler - gump
   45  0.0625  this review      200         9.8195 +- 0.0088   0.12       9.8199 +- 0.0028   -0.0004 +- 0.0092   -0.0008 +- 0.0089
   45  0.2500  this review      200         9.8216 +- 0.0074   0.11       9.8272 +- 0.0040   -0.0056 +- 0.0084   +0.0014 +- 0.0076
   63  0.0156  pull request     100        13.6198 +- 0.0213   0.21                                               -0.0132 +- 0.0213
   63  0.0625  this review      270        13.6423 +- 0.0085   0.14      13.6480 +- 0.0064   -0.0057 +- 0.0107   +0.0093 +- 0.0086
   63  0.0625  pull request     100        13.6533 +- 0.0148   0.15      13.6480 +- 0.0064   +0.0053 +- 0.0161   +0.0203 +- 0.0148
   63  0.0625  both             370        13.6452 +- 0.0074   0.14      13.6480 +- 0.0064   -0.0028 +- 0.0098   +0.0122 +- 0.0075
   63  0.2500  this review      250        13.6345 +- 0.0087   0.14      13.6224 +- 0.0090   +0.0122 +- 0.0125   +0.0015 +- 0.0088
   63  0.2500  pull request     100        13.6389 +- 0.0131   0.13      13.6224 +- 0.0090   +0.0165 +- 0.0159   +0.0059 +- 0.0131
   63  0.2500  both             350        13.6358 +- 0.0072   0.14      13.6224 +- 0.0090   +0.0134 +- 0.0115   +0.0028 +- 0.0073
   84  0.0625  this review       10        18.2038 +- 0.0635   0.20                                               +0.0628 +- 0.0637
   84  0.0625  pull request     100        18.1731 +- 0.0287   0.29                                               +0.0321 +- 0.0291
   84  0.0625  both             110        18.1759 +- 0.0267   0.28                                               +0.0349 +- 0.0272
   84  0.2500  this review       40        18.1108 +- 0.0508   0.32      18.1681 +- 0.0371   -0.0573 +- 0.0629   -0.0302 +- 0.0511
  108  0.0156  this review        6        23.7865 +- 0.0838   0.21                                               +0.4473 +- 0.0844
  108  0.0625  this review        6        23.2063 +- 0.2118   0.52                                               -0.1329 +- 0.2121
  108  0.2500  this review       20        22.6414 +- 0.5018   2.24                                               -0.6978 +- 0.5019
```

- **Against brute force where both are precise: equal.** Five comparisons, none beyond 1.2 of its errors.
- **DELTA and NSWEEP** (63 cells, ε = 1/16; frozen: DELTA 3, NSWEEP 38):

  ```
  DELTA NSWEEP  replications  ln tau              scatter   minus the frozen setting
      1     38    100          13.6305 +- 0.0091   0.09      -0.0147 +- 0.0117
      3     19    150          13.6539 +- 0.0197   0.24      +0.0087 +- 0.0210
      3     38    370          13.6452 +- 0.0074   0.14      
      3     76     50          13.6201 +- 0.0158   0.11      -0.0252 +- 0.0174
      6     38    150          13.6096 +- 0.0212   0.26      -0.0356 +- 0.0224
  weighted mean of the 5 settings 13.6366 +- 0.0050; chi2 5.3 on 4
  ```

  The five settings scatter around their weighted mean with χ² = 5.3 on 4. An exact sampler does not move, and
  this one does not within ± 0.01 to 0.02. Their weighted mean is −0.011 ± 0.008 from this audit's brute force.
- **84 cells, ε = 1/4:** 18.111 ± 0.051 (40 replications; scatter 0.32), −0.030 ± 0.051 from gump and −0.057 ± 0.063
  from the brute force of §1. The two together put the chain at +0.007 ± 0.030 from gump there.
- **108 cells, ε = 1/4** (20 replications, 127 s each): 22.64 ± 0.50; one replication carries 52% of the summed
  rate (§4, §5); the other nineteen give 23.335 ± 0.079, −0.004 from gump.

## 4. Ancestry: what the final level descends from [measured here]

`summary.py`, table 4 (`nz_anc`). Each replication starts 4,096 fresh chains (512 lanes at 8 moments).

```
cells   eps    DELTA NSWEEP  reps   fresh chains the score-0 chains descend from   share of the commonest one   its share against the rate (correlation)
   45  0.0625     3     27   200     163 / 170 / 176                              0.04 / 0.05 / 0.07 (max 0.15)   +0.24
   45  0.2500     3     27   200     187 / 193 / 199                              0.03 / 0.04 / 0.04 (max 0.09)   +0.13
   63  0.0625     1     38   100     232 / 241 / 248                              0.03 / 0.03 / 0.03 (max 0.08)   -0.02
   63  0.0625     3     19   150      77 / 81 / 85                              0.09 / 0.11 / 0.15 (max 0.37)   +0.34
   63  0.0625     3     38    20     129 / 132 / 137                              0.06 / 0.07 / 0.08 (max 0.11)   -0.08
   63  0.0625     3     76    50     169 / 175 / 179                              0.03 / 0.04 / 0.04 (max 0.10)   +0.04
   63  0.0625     6     38   150      46 / 49 / 53                              0.11 / 0.14 / 0.17 (max 0.34)   +0.10
   84  0.0625     3     50    10      81 / 84 / 90                              0.08 / 0.11 / 0.15 (max 0.37)   +0.53
   84  0.2500     3     50    40      89 / 92 / 94                              0.08 / 0.12 / 0.14 (max 0.62)   +0.76
  108  0.0156     3     65     6      46 / 48 / 50                              0.14 / 0.14 / 0.17 (max 0.20)   +0.24
  108  0.0625     3     65     6      50 / 55 / 58                              0.21 / 0.23 / 0.44 (max 0.63)   +0.95
  108  0.2500     3     65    20      57 / 59 / 61                              0.11 / 0.15 / 0.22 (max 0.92)   +0.90
```

- The final level never descends from one or two initial states: from about 170 to 190 at 45 cells, 130 at 63 (frozen
  setting), 85 to 90 at 84, 50 to 60 at 108.
- But the families are unequal and the inequality grows with the face. At 108 cells and ε = 1/16 the commonest
  initial state holds 8 to 63% of the dying chains in six replications, and the replication's rate follows that
  share (correlation +0.95): **a replication's rate at 108 cells is set by its luckiest initial state.** At ε = 1/4
  one replication in 20 had 92% of its dying chains from one initial state and a rate 22 times the median
  (1.54 × 10⁻⁹): from that lane's state the watched face dies within the window with probability about 1.5 × 10⁻⁴,
  10⁵ times the average.
- What that means for the variance: the sampler steers the darts, not the initial state, so across initial
  states it is plain sampling, 4,096 draws a replication, of a quantity (the chance of death given the initial
  state) whose law has a long tail. One replication's relative scatter is 0.14 (63 cells), 0.28 (84), 0.52 (108,
  ε = 1/16), and the error of a pooled value is honest only once the tail has been met. For small ε it is worse
  by construction: as ε → 0 the death is decided by the initial state alone and the sampler becomes brute force
  with 4,096 hulls a replication.

## 5. The 108-cell rows (claim 4) [rows]

`python3 research/audit/blastnoisy/c108.py DIR`, `tail108.py DIR`, `rows.py DIR` with DIR the pull request's
`noisy/data/runs` (seconds). The pull request's table is reproduced to the digit (23.4223 ± 0.0250,
23.2281 ± 0.1188, 23.3685 ± 0.0649; weighted mean 23.4084 ± 0.0229; intercept 23.3143 ± 0.0820, slope +1.70 ± 1.42).

| ε | replications | rate / mean: median, 95%, 99%, largest | skewness | tail index (largest 5%) | ln τ without the largest replication | bootstrap 95% of ln τ |
|---|---|---|---|---|---|---|
| 1/16 | 440 | 0.89, 1.86, 3.20, 6.76 | 4.8 | 3.1 | 23.436 | [23.372, 23.470] |
| 1/32 | 300 | 0.73, 1.66, 4.85, 34.5 | 14.6 | 1.2 | 23.347 | [22.974, 23.411] |
| 1/64 | 360 | 0.80, 1.74, 3.38, 20.2 | 12.1 | 1.9 | 23.424 | [23.233, 23.477] |

- **ε = 1/16 is stable across the seed files**: 23.4223 ± 0.039 (seeds 151xx, 220 replications) and 23.4223 ± 0.031
  (152xx, 220); the agreement to four digits is chance, the rows differ. Its error is fair *for the sample it is*:
  tail index about 3, bootstrap interval [+0.033, +0.130] from gump, 0.08% of resamples at or below gump.
- **The errors at ε = 1/32 and 1/64 are not errors in the usual sense** (tail index below 2: the variance is not
  defined by the sample); the pull request says as much for 1/32.
- **The weighted mean (+0.069 ± 0.025) is not a fair summary.** Its weights are 1 : 0.04 : 0.15, so it is the
  ε = 1/16 value; the samples that met a large replication get both a lower ln τ and a larger error, hence less
  weight; and a mean over ε assumes there is no dependence on ε, which is the opposite of reading the result as an
  offset of the chain. With every replication given the same weight, the mean of all 1,100 rates is
  **23.349 ± 0.043, +0.009 ± 0.044 from gump** (bootstrap [−0.083, +0.083]). The line's intercept has a bootstrap
  interval [−0.20, +0.15] from gump, wider than its quoted ± 0.083.
- **The large replications** (`tail108.py`; rates over the median of their ε; this audit's 108-cell replications
  included):

```
  eps    replications   median ln tau_k   large (> 5x / > 10x median)   share of the rate (> 5x / > 10x)   ln tau all       bulk (<= 10x median)   bulk - gump
  1/4        20           23.388            1 /   1                     0.525 / 0.525                     22.641           23.335            -0.004
          with ancestry: (rate / median, share of the commonest initial state among the score-0 chains): (22.2, 0.92), (2.2, 0.51)
  1/16      446           23.534            1 /   0                     0.015 / 0.000                     23.419           23.419            +0.080
          with ancestry: (rate / median, share of the commonest initial state among the score-0 chains): (2.5, 0.63), (2.0, 0.50)
  1/32      300           23.542            6 /   1                     0.198 / 0.115                     23.228           23.347            +0.008
  1/64      366           23.600            2 /   2                     0.085 / 0.085                     23.374           23.458            +0.119
```

  Across all ε (1,132 replications), one in 283 is above ten times the median (27 times on average) and those
  four carry 7.7% of the summed rate; above five times: ten replications, 10.6%. The ε = 1/16 sample has none
  above ten and one above five. At the pooled frequency 446 replications meet none with probability 0.21. Without
  the replications above ten times the median, ε = 1/16, 1/32, 1/64 read +0.080, +0.008, +0.119 from gump: the
  "bulk" is above gump by about what the large ones carry, and it is highest at the smallest ε, where a response
  of the chain to ε would be smallest.

## 6. Beyond the pull request [measured here]

- **A hull's hazard does not depend on its age at 63 cells.** In gump (noise off), hulls replaced at age 6,000
  (`nb ... 6000`): 13.6338 ± 0.0055 for ages 1,000 to 3,000 and 13.6395 ± 0.0046 for 3,000 to 6,000 (94,476 deaths in
  all, eight faces), against 13.633; in the long run every half-decade of age from 3,000 to 10⁶ generations is
  within 0.011 of the mean (`ages.py`). So the sampler's young lanes are a fair sample at 63 cells. At 84 cells:
  18.159 ± 0.019 for ages 1,000 to 6,000 (2,838 deaths, eight faces; 18.177 ± 0.030 and 18.147 ± 0.024 in the two
  halves) against 18.141 ± 0.005: +0.018 ± 0.019, no effect to that precision. Not measured at 108 cells, where a life
  is 10⁹ generations.
- **One unexplained count.** In gump at 84 cells (two seeds, 4,968 deaths) face 0 took 694 deaths against 611 a face
  for the other seven; within seed 1304 the eight counts differ with χ² = 25 on 7 (p = 0.0008). The vessel, the rule
  and the soup are symmetric, the five noise-free runs at 45 and 63 cells give p = 0.21 to 0.79 for the same test, and
  nb reproduces fd's counts exactly, so I read it as chance (about thirty such tables were looked at); it is the
  reason the 84-cell offsets above are taken against the anchor and not against face 0's own noise-free count.
- **The other seven faces are three classes** (§1), which the pull request's "8E/D" hides.

## 7. Chain or sampler? (D)

**Most likely the sampler, through its tail and not through a bias; I put about 65% on that, 20% on the chain,
15% on a plain 3-error fluctuation with no cause.** The evidence, in order of weight:

1. The chain shows no offset of the watched face by brute force at 45 and 63 cells at any ε up to 1 (± 0.002,
   ± 0.005), and +0.027 ± 0.038 at 84 cells at ε = 1/4. An offset of +0.083 at 108 cells and ε = 1/16 is a response
   of 1.3 per unit ε; the 84-cell brute force reads 0.11 ± 0.15 per unit ε (0.03 ± 0.12 with the sampler's value
   added), and the other faces' response, where it can be measured, grows 1.9 times from 63 to 84 cells.
2. The sampler has no bias where it can be tested (45 and 63 cells to ± 0.01; 84 cells and ε = 1/4 to ± 0.06),
   does not move with its levels or sweeps, and its moves are right by reading. So the offset is not a wrong
   sampler.
3. The law of one replication's rate at 108 cells has a tail: replications above ten times the median are met once
   in 283 and carry 7.7% of the summed rate (seen at ε = 1/4, 1/32 and 1/64; each traced, where ancestry was
   printed, to one initial state). The ε = 1/16 sample met none and reads 8% low in rate. Pooled over ε the
   108-cell rows give gump (+0.009 ± 0.044), and the samples' bulks are not ordered by ε as a response of the
   chain would be (+0.080, +0.008, +0.119 at 1/16, 1/32, 1/64; −0.004 at 1/4 in nineteen replications).
4. Against: the chance that 446 replications meet none is one in five, not small; the frequency of large
   replications may itself depend on ε; and the 84-cell sampler value at ε = 1/16, where no large replication has
   been seen in 150 (largest 2.5 times the mean), is also above gump (+0.035 ± 0.027).

**The measurement that decides it.** On this machine: 1,500 more replications of the frozen sampler at 108 cells
and ε = 1/16 (15 core-hours at the 35 s a replication costs here). If replications above ten times the median come at the pooled frequency
(five expected) the value falls to gump; if none comes in 1,940 (probability 0.1% at that frequency) the offset is
the chain's. The same budget on a GPU buys the direct answer: a brute force of the noisy chain at 108 cells and
ε = 1/16 needs the exposure of the gump anchor itself (1.5 × 10¹³ hull-generations for 1,100 deaths of one face,
± 0.03). The cheaper cure for the method is to stop sampling initial states plainly: a longer TPRE, so that the
vulnerable state is made by the darts and not drawn, or a first stage that splits on the initial state.

## 8. Not checked

- The chain by brute force at 84 cells at ε = 1/16 and at ε = 1; anything by brute force at 108 cells.
- Whether the frequency of large replications depends on ε (the account of §7 assumes it does not; 1/32 has six
  above five times the median where 1/16 has one, 2 errors apart).
- What a vulnerable initial state looks like (a hole in the face, a long dip, an eroded rim); the ancestry
  columns name the chain, and the state was not looked at.
- A hull's hazard by age at 108 cells, and at 84 cells beyond what §6 gives.
- The sampler's fast evaluation (hit lists, in-place proposals) against a plain evaluation; it is covered only
  through the agreement with brute force. KFLIP, TPRE, TWIN, WBACK and LAM1 were not varied.
- `validate.py`, `fit.py`, `ana.py` and the production scripts of the pull request were not run or read line by
  line; `fit.py`'s numbers were recomputed by `c108.py`.
- A second seed of the 84-cell brute force at ε = 1/4. The count-for-count check of nb against fd at 84 cells (it
  was done at 63).
- Settled lives under noise (nb's guard works only with the noise off; none was seen in 9 × 10¹⁰ noise-free
  hull-generations).

## 9. The author's forecasts for this rebuild (`noisy/PREDICTIONS.md` block 3 at b80248c, frozen 17:58 UTC)

Read after sections 0 to 8 were committed (d35b1eb). Its conjecture, "the +0.083 ± 0.027 at 108 cells and ε = 1/16
is the sampler's, not the chain's: an unbiased estimate whose law has a rare heavy tail", is this review's §7,
reached separately.

| | forecast | here |
|---|---|---|
| 1 | Brute force at 84 cells, ε = 1/16, within 0.015 of gump given an error ≤ 0.01 (80%); above by more than 0.03 (7%) | not measured here (§8) |
| 2 | Brute force at 84 cells at a large ε: above gump by 0.01 to 0.06 (60%); by more than 0.06 (15%) | +0.027 ± 0.038 at ε = 1/4: in the 60% band by its value; its error reaches both neighbours |
| 3 | The sampler at 108 cells with the odd sweeps off within two errors of 23.422 (75%); its scatter above 0.52 (70%) | not run here |
| 4 | Ancestry at 108 cells: median number of distinct initial chains at the last level between 35 and 70 at every ε (75%); the replication with the largest rate has a largest-family share above the median's (65%) | yes and yes in this audit's three small sets: medians 59, 55, 48 at ε = 1/4, 1/16, 1/64 (20, 6, 6 replications); the largest-rate replication's share is 0.92, 0.63, 0.18 against medians 0.15, 0.23, 0.14 |
| 5 | 2,000 replications at ε = 1/16, or a sampler that moves the initial states, bring the 108-cell value within 0.03 of gump (65%) | not run; it is the deciding measurement of §7 |

## E. The three qualifications carried from `REVIEW-blast.md` (the 16:40 entry) [read]

All three match that review. (1) "88% at 63 cells, 92% at 84" and "32.5% against 11.9%": the review's verdict and
§2; the tables have 0.881 (`data/slab63.txt`) and 0.916 (`data/wide84.txt`). (2) "1 in 128 at 63 cells, 1 in 1,100
at 84": the review's rows 1e and its summary item 3 (matched to the review's text; I did not find the two ratios
as one line of a table). (3) "0.311 against 0.260": `data/slab63.txt` has q(4) = 0.3114 and 0.2605. The entry's
list of what the audit confirmed and what it calls not a result agrees with the review's verdict section.

## Reproduce

```sh
sh research/audit/blastnoisy/run.sh check      # 1 to 3 minutes
sh research/audit/blastnoisy/run.sh brute      # about 3.3 core-hours as listed (one run after another; times in the file)
sh research/audit/blastnoisy/run.sh sampler    # about 2.5 core-hours
python3 research/audit/blastnoisy/collect.py   # scratch -> data/
python3 research/audit/blastnoisy/summary.py   # the tables of sections 1, 3, 4 (seconds; reads data/ and the pull request's rows)
sh research/audit/blastnoisy/run.sh tables     # the same, by run, with bootstrap intervals; sections 5 and 6
```
