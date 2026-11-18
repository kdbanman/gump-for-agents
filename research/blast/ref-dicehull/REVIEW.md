# REVIEW (referee `ref-dicehull`): the hull dice chain and the 135-cell face

2026-11-18, 05:23 to 05:48 UTC, one core, cut short by the usage window. Subject: `research/blast/split-hull/README.md`, "Dice under the hull".
Files here: `geom.py` + `rd.c` (my own graph and 256-lane stepper, written from `docs/AUTOMATON.md`), `validate.py`,
`ana.py` (tables of the brute-force runs), `pool.py` (sampler replications), `paths.py` (fatal dips), `hd_anc.c`
(split-hull's `hd.c` plus ancestry bookkeeping and nothing else). Bulk output: `research/scratch/blast/ref-dicehull/`.
All numbers [measured] unless marked.

## Verdict in five lines

| item | verdict |
|---|---|
| (a) the chain, its R = 9 and 11 values, its living state | **CONFIRMED** |
| (b) truncation depth and coin density fake a high R = 17 | **NOT FOUND where testable** (shifts of 0.01 to 0.03, not growing in the living state up to R = 17); deep levels at R >= 13 NOT TESTED |
| (c) sampler value at R = 17 reproduces with fresh seeds | **CONFIRMED** (29.394 +- 0.066, 32 replications; pooled 156: 29.420 +- 0.042) |
| (c) "+- 0.042 / 0.060 is an honest error", "blind calibrations pass" | **CORRECTED**: the replications are heavy-tailed; like with like, sampler minus gump GROWS with size |
| (d) "R = 17 is above both 29.163 and 29.230" | **REFUTED as a claim; not excluded as a fact.** Gump at 135 cells from this method: **29.30 +- 0.09** |

## (a) The chain by my own code: CONFIRMED

- `python3 research/blast/ref-dicehull/validate.py 1200`: `rd.c` equals `reference/oracle.py` state for state over 1,200
  generations x 4 soups on the full hull (R = 9, 11; nothing born outside the hull) and, one oracle step at a time
  from every dumped state, on the dice chain (R = 9, 11; 6 and 8 rule layers; coins 32/64 and 27/64; measured coin
  densities 0.4998, 0.5009, 0.4210, 0.4995, 0.4204). Negative control (one neighbour swapped) fails at generation 1 or
  2 in every case. `VALIDATION PASSED`. Sizes equal split-hull's: (A, rule cells, dice cells) = 45, 312, 108; 63, 438, 162;
  135, 924, 360.
- Brute force of the chain, one watched face, tau = counted generations with the face alive / counted deaths. Reseeds:
  a soup of density 1/2 on every cell; the first 200 generations of a lane count neither exposure nor deaths
  (split-hull's `sh.c`: T0 = 200, the same). `rd G run SEED GENS 200 32`:

  | R | my chain value | split-hull's chain value | gump anchor | chain - gump |
  |---|---|---|---|---|
  | 9 | **9.8220 +- 0.0049** (41,206 deaths) | 9.837 +- 0.018 | 9.819 | +0.003 +- 0.005 |
  | 11 | **13.6550 +- 0.0129** (6,010 deaths) | 13.70 +- 0.06 | 13.633 | +0.022 +- 0.013 |

  Gump itself in my code under the anchors' protocol (whole hull, a lane retired at the first death of any of the 8
  faces, tau = 8 x exposure / deaths, `rd G run8 ...`): **9.8245 +- 0.0018** (R = 9; 304,731 deaths) and **13.6312 +- 0.0143**
  (R = 11; 4,915 deaths; P-bar 31.252, sigma 5.241), i.e. the anchors. Chain minus my gump: -0.003 +- 0.005, +0.024 +- 0.019.
  Ageing 1,000 instead of 200 generations (R = 9 chain): 9.8129 +- 0.0050, no effect (-0.009 +- 0.007).
  Note, settled lanes: in the R = 9 chain run 0.26% of the exposure is a lane sitting at exactly 3 live face cells
  (547,132 samples at P = 3 where the neighbouring bins predict about 51,000; presumably one cube's still life left on
  an otherwise dead face). Such a face never "dies"; it inflates ln tau by 0.003 here and is not seen at R = 11.
- Living state, R = 11 chain: P-bar 31.267, sigma 5.238 (gump on file: 31.25, 5.24); edge row minus interior +0.054
  (my classes: edge row = smallest coordinate 0 and middle coordinate >= 4; interior = smallest coordinate >= 2).
  R = 17, gump's whole hull and the chain both in my code (`tail_R17_*.txt`): P-bar 69.494 / 69.513, sigma 7.431 / 7.428,
  edge row minus interior +0.0577 / +0.0579, second row -0.0244 / -0.0244, corner cells 0.3027 / 0.3027.

## (b) What the truncation and the fair coins do

Brute force, `python3 research/blast/ref-dicehull/ana.py`:

| R | variant of the chain | ln tau | shift from the chain as defined |
|---|---|---|---|
| 9 | as defined (6 rule layers, fair coins) | 9.8220 +- 0.0049 | |
| 9 | coins of density 27/64 = 0.42 | 9.7919 +- 0.0049 | **-0.030 +- 0.007** |
| 9 | 8 rule layers (coins two layers deeper) | 9.7946 +- 0.0049 | **-0.027 +- 0.007** |
| 11 | as defined | 13.6550 +- 0.0129 | |
| 11 | coins of density 0.42 | 13.6254 +- 0.0147 | **-0.030 +- 0.020** (lower tail of P thicker by 0.012 to 0.015) |
| 11 | 8 rule layers | 13.6482 +- 0.0148 | **-0.007 +- 0.020** (lower tail thicker by 0.007 to 0.011) |

So each "defect" of the chain lengthens the life by about 0.03, the same at R = 9 and R = 11 within errors of 0.007 and
0.02: no growth seen. (At R = 9 the agreement of the chain with gump's anchor is partly luck: the corrected variants
sit 0.03 BELOW gump there, the one-face protocol against the eight-face one.)

Living state at the sizes where deaths cannot be brute-forced (gump's whole hull against the chain, my code, lower
tail of the watched face's population, ln P(P <= L), chain minus gump; errors rough):

| R | level L | chain (6 layers) - gump | chain with 8 layers - gump |
|---|---|---|---|
| 11 | P-bar - 2.5 sigma = 18; 0.5 P-bar = 15 | -0.010 +- 0.002; -0.014 +- 0.003 | |
| 15 | 38; 0.6 P-bar = 33; 0.5 P-bar = 27 | -0.010 +- 0.002; -0.012 +- 0.006; -0.007 +- 0.023 | |
| 17 | 51; 48; 0.6 P-bar = 41; 0.5 P-bar = 34 | -0.011 +- 0.002; -0.013 +- 0.004; -0.027 +- 0.014; -0.11 +- 0.07 | -0.004 +- 0.003; -0.004 +- 0.004; -0.015 +- 0.016; -0.07 +- 0.07 |

P-bar, gump / chain: 31.252 / 31.267 (R = 11), 55.193 / 55.212 (R = 15), 69.494 / 69.513 (R = 17; 8 layers: 69.496).

Reading: fair coins instead of 0.42 make the face fuller by 0.02 to 0.03 cells and thin its lower tail by about 0.014
(R = 11) and 0.011 to 0.027 (R = 17): the same size at both radii, so no growth with R in the part I can see (dips
down to 0.6 P-bar). Two more rule layers change nothing measurable at R = 11. **Not tested: what the truncation does
to the last part of a death (below 0.5 P-bar) at R >= 13**; the R = 17 tail difference at 0.5 P-bar, -0.11 +- 0.07, is
compatible both with -0.02 and with an effect that grows with depth.

## (c) The sampler with fresh seeds: value CONFIRMED, error CORRECTED

`python3 research/blast/ref-dicehull/pool.py` (my runs: `hd` / `hd_anc` with split-hull's frozen arguments, seeds
770017, 880017, 990017, 880013):

| R | whose seeds | replications | ln tau | one replication's relative sd | largest / median |
|---|---|---:|---|---:|---:|
| 13 | mine | 24 | 18.130 +- 0.066 | 0.32 | 2.0 |
| 13 | all | 252 | 18.188 +- 0.024 (gump 18.141: +0.047 +- 0.024) | 0.38 | 3.7 |
| 15 | split-hull's (still growing) | 182 | 23.389 +- 0.080 with the giant; 23.465 +- 0.034 without (gump 23.339) | 1.08 | 17.4 |
| 17 | mine | 32 | **29.394 +- 0.066** | 0.37 | 2.2 |
| 17 | split-hull's | 124 | 29.427 +- 0.050 (was 29.453 +- 0.042 at 120) | 0.55 | 5.4 |
| 17 | all | 156 | **29.420 +- 0.042** | 0.52 | 5.4 |

1. **The R = 17 number reproduces**: fresh seeds 29.394 +- 0.066 against 29.453 +- 0.042. The pool has drifted down as it grew: 29.453 (120), 29.447 (146), 29.420 (156).
2. **Few ancestors.** At R = 17 the roughly 1,000 dying chains of a replication descend from 25 to 44 of its 4,096
   initial chains, effective number (sum n)^2 / sum n^2 = 5 to 13, largest ancestor 15 to 41% (`hd_anc.c`, lines
   `ANC`). The moves change about 34 of 20,160 coins per level, so a replication's rate is the weight of a handful of
   inherited dips. The estimator stays unbiased in the RATE (fixed levels, moves that keep the conditional law), which
   means its rare large replications are part of the answer.
3. **They exist.** Split-hull's own continued run (`split-hull/dice/sub_R15_s2.txt`, REP 4) has a replication of rate
   9.9e-10, 17.4 x the median, 8% of the summed rate of 182. With it R = 15 reads 23.389 +- 0.080; without it
   23.465 +- 0.034, which is +0.126 +- 0.034 above gump. (Split-hull has since written this into its table; its
   R = 17 line and its "errors above" table are unchanged.)
4. **Like with like, the offset grows.** The pooled value of runs that have not met a giant replication, minus gump:
   +0.001 +- 0.019, -0.044 +- 0.039, +0.047 +- 0.024, +0.126 +- 0.034 at 45, 63, 84, 108 cells. A constant (+0.027) is rejected
   (chi2 14.2 on 3); a line in the area gives **+0.147 +- 0.040 at 135 cells** (chi2 3.9 on 2). The R = 17 pool (156
   replications, largest 5.4 x the median) is such a run. Whether the growth is the unsampled tail of the estimator or a
   real chain-minus-gump offset I cannot say: at R = 9 and 11, where I have the chain's truth, chain - gump is +0.003
   and +0.022 and sampler - chain is -0.002 +- 0.020 and -0.066 +- 0.041. Section (b) argues against the truncation (0.03, flat).
5. So +- 0.042 (or 0.060) is the scatter of the replications seen, not the error of the rate: **not honest on the low
   side**. No single replication carries a large share at R = 17 (largest 3.0% of 156), which is the problem, not the
   reassurance: at R = 15 the first 48 replications looked the same.

6. An idea of mine, killed (`python3 research/blast/ref-dicehull/paths.py`): that the giants are slow deaths the 56-generation
   chain cannot hold. Not so. By brute force at R = 11 a fatal dip lasts 8.2 generations from its last passage above
   P-bar - 2.5 sigma (median 7, 99% within 20, longest 25 of 1,501 deaths); the sampler's dying chains at R = 17 take a median
   of 9 to 10 (90% within 16, longest 28) and die around generation 47 of 56: nothing is pressed against the window.
   The tail is the lottery of ancestors: at R = 13 a replication's rate correlates -0.75 with its effective number of ancestors.

## (d) What the owner may be told about the 135-cell face

- **Chain, as sampled:** ln tau = 29.420 +- 0.042 (156 replications, two agents' seeds). This is an upper estimate:
  the estimator's missing large replications can only lower it.
- **Offset to gump at that size:** +0.15 +- 0.04 (statistical, line through four sizes) with a model error I put at
  0.07 (a constant would say +0.03 and gump 29.39; a curve +0.2 or more): **+0.12 +- 0.08**. It is extrapolated, not measured at 135 cells.
- **Gump's 135-cell face by this method: ln tau = 29.30 +- 0.09.** On file from direct counting: 29.34 +- 0.25.
  (Line alone: 29.273 +- 0.057. Constant alone, rejected by its chi2: 29.393 +- 0.043.)
- **Which reading:** 29.230 is 0.8 errors below, 29.163 is 1.5 errors below, split-hull's forecast 29.223 the same as
  29.230. **Nothing is decided.** "Above both" is not supported; the data lean, at about one and a half errors, against
  the wrapped price (29.163) and do not distinguish 29.230 from values up to 29.45. The sentence in split-hull's
  README, "taken as it stands it is above them by 5 and 7 errors", should not be repeated.
- What would decide it: the same sampler with initial states that are also moved (or many more initial chains per
  replication) so that a replication stops hanging on about ten ancestors, calibrated at R = 15 until the giant
  replications are either common enough to average or shown to be absent; or a brute-force value of the CHAIN at R = 13
  (about 8e7 generations per death; my `rd.c` does 2.3e7 lane-generations a second: 100 deaths in 6 minutes on one
  core, 0.03 in an hour on four), which would separate "the chain is not gump" from "the sampler's tail".

## Not checked

- The sampler's code was read, not rewritten (ref-slab did that for the slab version). I checked the acceptance rule
  for the focused moves by reading only.
- The cause of the giant replication at R = 15 (which ancestor, what kind of dip) was not examined.
- The truncation's effect on deaths at R >= 13; coin density and depth together; R = 9 anchors are protocol-dependent
  at the 0.01 level (a gump hull of that size is retired every 2,300 generations).
- Errors of the tail comparisons are rough (samples four generations apart, sqrt(4/count)).

## Brute force of the chain at R = 13 (added 06:40 UTC; the test named above as decisive)

`rd G_13_6 run SEED 157030581 200 32`, seeds 1301 to 1304, four cores, 20 minutes (files `bf13_s130*.txt` in scratch;
1.608e11 counted lane-generations). [measured]

| what | ln tau (84 cells) | deaths |
|---|---|---:|
| hull dice chain, brute force, my stepper | **18.2005 +- 0.0223** (four jobs: 18.245, 18.169, 18.185, 18.205; their scatter 0.033, expected 0.045) | 2,004 |
| chain - gump (18.141 +- 0.005) | **+0.060 +- 0.023** (2.6 errors) | |
| chain - sampler on the chain (18.192 +- 0.025, 234 replications) | **+0.009 +- 0.034** | |
| chain - my fresh sampler runs (18.130 +- 0.066) | +0.071 +- 0.070 | |

No settled lanes (the histogram of P falls smoothly to P = 1; 5e-7 of the samples at P <= 6). P-bar 42.464, sigma 5.958.

**Reading.** The chain sits on the sampler and not on gump. At 84 cells the sampler is exact to 0.03 and the +0.05 is
the chain's own offset: the surrogate value "chain less a measured offset" stands, and what I wrote in (c) 4, that the
growth of sampler-minus-gump is probably the estimator's unsampled tail, is **withdrawn for this size** (the giant
replication at R = 15 and the downward drift of the R = 17 pool remain facts about the error bar). What does not
stand is "the offset is constant": by brute force, chain minus gump is -0.003 +- 0.005, +0.024 +- 0.019, +0.060 +- 0.023 at
45, 63, 84 cells, so (b)'s "0.03 and flat" was wrong beyond R = 11. Constant over R = 11 and 13: +0.039 +- 0.015, which
gives 29.397 - 0.039 = 29.36 at 135 cells; a line in the area through the three brute-force offsets: +0.14 +- 0.05 at
135 cells [extrapolated], which gives 29.26 +- 0.06. So 29.34 is the upper of two defensible readings, the growth from
R = 11 to R = 13 is itself only 0.036 +- 0.030, and 29.30 +- 0.09 still covers both: nothing new is decided between
29.230 and 29.163, and "above both" is still not shown. Not checked: why the chain's offset grows (coins, depth or the
one-face protocol), and its value at 108 cells, which brute force cannot reach in this time.
