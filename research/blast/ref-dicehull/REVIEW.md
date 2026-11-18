# REVIEW (referee `ref-dicehull`): the hull dice chain and the 135-cell face

2026-11-18, 05:23 to 05:50 UTC, one core. Subject: `research/blast/split-hull/README.md`, "Dice under the hull".
Files here: `geom.py` + `rd.c` (my own graph and 256-lane stepper, written from `docs/AUTOMATON.md`), `validate.py`,
`ana.py` (tables of the brute-force runs), `pool.py` (sampler replications), `paths.py` (fatal dips), `hd_anc.c`
(split-hull's `hd.c` plus ancestry bookkeeping and nothing else). Bulk output: `research/scratch/blast/ref-dicehull/`.
All numbers [measured] unless marked.

## Verdict in five lines

| item | verdict |
|---|---|
| (a) the chain, its R = 9 and 11 values, its living state | **CONFIRMED** |
| (b) truncation depth and coin density fake a high R = 17 | **NOT FOUND where testable** (shifts of 0.01 to 0.03, not growing in the living state up to R = 17); deep levels at R >= 13 NOT TESTED |
| (c) sampler value at R = 17 reproduces with fresh seeds | **CONFIRMED** (29.420 +- 0.068, 26 replications; pooled 146: 29.447 +- 0.036) |
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

  GUMPROWS
- Living state, R = 11 chain: P-bar 31.267, sigma 5.238 (gump on file: 31.25, 5.24); edge row minus interior +0.054
  (my classes: edge row = smallest coordinate 0 and middle coordinate >= 4; interior = smallest coordinate >= 2).
  R = 17, gump's whole hull and the chain both in my code (`tail_R17_*.txt`): P-bar 69.494 / 69.513, sigma 7.431 / 7.428,
  edge row minus interior +0.0577 / +0.0579, second row -0.0244 / -0.0244, corner cells 0.3027 / 0.3027.

## (b) What the truncation and the fair coins do

Brute force, `python3 research/blast/ref-dicehull/ana.py`:

VARROWS

Living state at the sizes where deaths cannot be brute-forced (gump's whole hull against the chain, my code, lower
tail of the watched face's population, ln P(P <= L), chain minus gump; errors rough):

TAILROWS

Reading: fair coins instead of 0.42 make the face fuller by 0.02 to 0.03 cells and thin its lower tail by about 0.014
(R = 11) and 0.011 to 0.027 (R = 17): the same size at both radii, so no growth with R in the part I can see (dips
down to 0.6 P-bar). Two more rule layers change nothing measurable at R = 11. **Not tested: what the truncation does
to the last part of a death (below 0.5 P-bar) at R >= 13**; the R = 17 tail difference at 0.5 P-bar, -0.11 +- 0.07, is
compatible both with -0.02 and with an effect that grows with depth.

## (c) The sampler with fresh seeds: value CONFIRMED, error CORRECTED

`python3 research/blast/ref-dicehull/pool.py` (my runs: `hd` / `hd_anc` with split-hull's frozen arguments, seeds
770017, 880017, 990017, 880013):

POOLROWS

1. **The R = 17 number reproduces**: fresh seeds 29.420 +- 0.068 against 29.453 +- 0.042.
2. **Few ancestors.** At R = 17 the roughly 1,000 dying chains of a replication descend from 26 to 44 of its 4,096
   initial chains, effective number (sum n)^2 / sum n^2 = 5 to 13, largest ancestor 15 to 41% (`hd_anc.c`, lines
   `ANC`). The moves change about 34 of 20,160 coins per level, so a replication's rate is the weight of a handful of
   inherited dips. The estimator stays unbiased in the RATE (fixed levels, moves that keep the conditional law), which
   means its rare large replications are part of the answer.
3. **They exist.** Split-hull's own continued run (`split-hull/dice/sub_R15_s2.txt`, REP 4) has a replication of rate
   9.9e-10, 17.5 x the median, a tenth of the summed rate of about 145. With it R = 15 reads 23.37 +- 0.10; without it
   23.460 +- 0.040, which is +0.120 +- 0.040 above gump. (Split-hull has since written this into its table; its
   R = 17 line and its "errors above" table are unchanged.)
4. **Like with like, the offset grows.** The pooled value of runs that have not met a giant replication, minus gump:
   +0.001 +- 0.019, -0.044 +- 0.039, +0.053 +- 0.026, +0.120 +- 0.040 at 45, 63, 84, 108 cells. A constant is rejected
   (chi2 11.5 on 3); a line in the area gives **+0.143 +- 0.044 at 135 cells** (chi2 3.4 on 2). The R = 17 pool (146
   replications, largest 3.7 x the median) is such a run. Whether the growth is the unsampled tail of the estimator or a
   real chain-minus-gump offset I cannot say: at R = 9 and 11, where I have the chain's truth, chain - gump is +0.003
   and +0.022 and sampler - chain is -0.002 +- 0.020 and -0.066 +- 0.041.
5. So +- 0.042 (or 0.060) is the scatter of the replications seen, not the error of the rate: **not honest on the low
   side**. No single replication carries a large share at R = 17 (largest 2.2% of 146), which is the problem, not the
   reassurance: at R = 15 the first 48 replications looked the same.

DURROWS

## (d) What the owner may be told about the 135-cell face

- **Chain, as sampled:** ln tau = 29.447 +- 0.036 (146 replications, two agents' seeds). This is an upper estimate:
  the estimator's missing large replications can only lower it.
- **Offset to gump at that size:** +0.14 +- 0.04 (statistical, line through four sizes) with a model error I put at
  0.07 (a constant would say +0.02, a curve +0.2 or more): **+0.14 +- 0.08**. It is extrapolated, not measured at 135 cells.
- **Gump's 135-cell face by this method: ln tau = 29.30 +- 0.09.** On file from direct counting: 29.34 +- 0.25.
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
