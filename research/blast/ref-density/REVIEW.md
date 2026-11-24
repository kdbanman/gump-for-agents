# ref-density: referee of `research/blast/density/README.md` (commit 9a105d3)

Referee session, 2026-11-24 (13:55–15:50 UTC). Subject: the sections of the density agent's README present at commit
9a105d3 (program `nzd.c` at that commit), not the section it is adding now. Everything below was computed with my own
code, `rd.c`, written from `reference/oracle.py` and from the prose of `research/blast/noisy/README.md` ("The chain,
exactly") and of the density README, before I read `nz.c` or `nzd.c` (I never opened `research/audit/blastnoisy/`).
`nzd.c` was then read critically and run as a black box, built from `git show 9a105d3:research/blast/density/nzd.c`.

## In brief

- **The numbers stand.** Every headline row I reran (11 lifetimes and the scan's zero, the layer densities, the lags, P₁) reproduces
  with independent code and seeds, all within 2σ (table; the d = 2 mean-density row is the farthest, +1.97σ). The
  layer densities and lagged correlations agree to the third decimal. Fair coins at d = 1 read −1.6σ on my first
  seed and −1.0σ with a second (note under the table).
- **The program does what the README says.** Two defects of form, none of substance: the noisy chains' layer
  densities are read after the darts (they include the fresh coins), and adjacent seeds share their coin stream.
- **The mechanism does not stand as stated.** "The lives order by the low-face density of the replaced core"
  [measured on their four chains] fails on three further chains of mine: the whole-layer copy has gump's low-face
  density (0.386 against 0.384; nzd.c's own diagnostic agrees, 0.386) and less clustering, yet lives 0.18 less
  (two seeds, 7.8σ); the scan chains
  at p = 0.1 and 0.2 have low-face densities below the core copy's or near it (0.311, 0.354 against 0.348) yet live
  0.12 and 0.45 longer.
- **The reading has further soft spots**: "the layer leads by 1–2 generations" (the cross-correlation peaks at lag 0;
  the asymmetry is real and points layer → face, the reverse of the causal sentence it is quoted for); "density
  accounts for a fifth" (coins at gump's mean density make a denser support than gump's at every replaced depth; on
  the realized density the share is about a third); "independence from the face" (the README's own face-dependent
  coins keep most of the gain); "gump's layers are worth coins of 0.19" (the chain at p = 0.2 has a support at 0.40
  after the darts, 0.46 before, not 0.2).

## My chain, exactly

- **Stepper** [measured]: `python3 research/blast/ref-density/validate.py <rd binary> 1200` → `VALIDATION PASSED`
  (`validate_1200.txt`). R = 11 (876 cells) and R = 9 (510 cells), two seeds each, three soups of density 0.35 per
  seed, 1,200 generations, against `oracle.step` on a box of side 2R + 4: every hull cell, no live cell outside the
  hull, the watched face's population, the eight faces' emptiness, identical at every generation. Negative control
  (`RD_NEGCTL=1`: one corner-touching neighbour of every x-normal cell replaced by the edge-sharing coplanar face)
  fails at generation 1 at both radii. Bit-sliced, 512 lanes. Group sizes come out as the README's (core 9, 9, 18,
  18, 21 at depths 1–5, 57 deeper; whole layers 63, 75, 75, 81, 81; |N| = 132, B = 1,024 at d = 1; at R = 9 |N| = 42,
  B = 256).
- **Noise law** [exact, by construction]: N = cells at depth ≥ d under the watched face (+,+,+) and ≥ 3 under each
  other face; B = smallest power of two ≥ 4|N|; after each generation, in each lane independently, M darts i.i.d.
  uniform on B squares, thrown in sequence, a dart on a cell of N setting it to its coin. Sampled in the
  law-equivalent form K ~ Binomial(M, |N|/B) (exact pmf, inversion), then K i.i.d. uniform cells of N in sequence.
  Coins: fair = one bit of a fresh 32-bit word; bias p = a fresh 32-bit word < round(p 2³²); copy = the current state
  (earlier darts of the same generation included) of a uniformly chosen cell of the source set at the same depth
  under the watched face, the dart's own cell included (source: N's cells at that depth = "core", or every hull cell
  at that depth = "whole layer"). A replaced cell is hit with probability q = 1 − (1 − 1/B)^M = 0.2213 per generation
  at ε = M/B = 1/4 (check: in the fair chain the replaced core of layer 1 goes from 0.4342 before the darts to 0.4487
  after, against 0.4342 (1 − q) + q/2 = 0.4488). RNG xoshiro256** seeded by splitmix64; my seeds only.
- **Life protocol and estimator**: as the noisy README states it (soup 0.35, age 0; a lane-generation is exposure iff
  age > 200 after the step; a life ends when any face is empty; a watched death is a life ended with the watched face
  empty, alone or tied, at an exposure generation; re-seed). ln τ = ln(exposure / watched deaths) ± 1/√deaths. No
  settled-life guard; the longest life in every row is below 1.6 × 10⁶ generations, as in the agent's rows (no stuck lane). Diagnostics are
  read after the step and before the darts; for the replaced core of layer 1 also after the darts.
- Rows: `sh research/blast/ref-density/row.sh TAG R SEED GENS M D0 COIN [LAGGENS]`, full outputs in `data/rows/TAG.txt`
  (the line `SETUP` gives every parameter); `nzdrow.sh` runs nzd.c, outputs in `data/nzd/`. Every number below:
  `python3 research/blast/ref-density/collect.py` (reads `data/rows`, `data/nzd`).

## The table (63 cells, ε = 1/4, d = 1 unless noted; Δ = ln τ − 13.633; σ in quadrature)

| row | theirs: ln τ (Δ) | mine: ln τ (Δ) | deaths, mine | difference |
|---|---|---|---:|---:|
| gump | 13.633 ± 0.001 (own seed 13.644 ± 0.012) | 13.632 ± 0.014; all eight faces 13.631 ± 0.005 | 4,913 (39,315) | −0.1σ (−0.3σ) |
| fair coins | 14.311 ± 0.016 (+0.678) | seeds 1012, 1013: 14.264 ± 0.025, 14.324 ± 0.033; pooled 14.286 ± 0.020 (+0.653) | 2,554 | −1.0σ |
| mean-density coins | 14.165 ± 0.011 (+0.532) | 14.168 ± 0.026 (+0.535) | 1,437 | +0.1σ |
| copy from the replaced cells | 13.199 ± 0.013 (−0.434) | 13.188 ± 0.020 (−0.445) | 2,392 | −0.5σ |
| copy from the whole layer | 13.464 ± 0.011 (−0.169) | seeds 1008, 1014: 13.428 ± 0.026, 13.472 ± 0.026; pooled 13.450 ± 0.018 (−0.183) | 2,946 | −0.7σ |
| every depth at p = 0.1 | 13.312 ± 0.022 (−0.322) | 13.306 ± 0.024 (−0.327) | 1,701 | −0.2σ |
| every depth at p = 0.2 | 13.676 ± 0.024 (+0.043) | 13.635 ± 0.023 (+0.002) | 1,837 | −1.2σ |
| zero of the scan (linear, 0.1–0.2) | p* = 0.188 ± 0.007 | p* = 0.199 ± 0.007 | | +1.1σ |
| LOW10 coins | 14.096 ± 0.010 (+0.463) | 14.081 ± 0.029 (+0.448) | 1,176 | −0.5σ |
| mean-density coins, d = 2 | 13.877 ± 0.013 (+0.244) | 13.936 ± 0.027 (+0.303) | 1,359 | +2.0σ |
| fair coins, d = 2 | 13.965 ± 0.014 (+0.332) | 13.971 ± 0.028 (+0.338) | 1,313 | +0.2σ |
| mean-density coins, ε = 1/16 | 13.797 ± 0.013 (+0.164) | 13.830 ± 0.026 (+0.197) | 1,511 | +1.1σ |
| gump: replaced core of layer 1, all time | 0.4301 | 0.4301 | | |
| … the same, face ≤ 10 (≤ 4) | 0.3836 (0.401) | 0.3843 (0.4016) | | |
| … whole layer 1, face ≤ 10 | 0.3425 | 0.3422 | | |
| … core-1 count variance / binomial, face ≤ 10 | 1.81 | 1.80 (within each F, 1 ≤ F ≤ 10) | | |
| gump: face mean, sd | 31.25, 5.24 | 31.25, 5.24 | | |
| gump: P₁ (descent from ≥ 16 to ≤ 1 ends in death) | 0.771 ± 0.004 | 0.766 ± 0.005 | | −0.8σ |
| lag: corr(full 1 at t − L, face at t), L = 0, 1, 2, 4, 8 | 0.375, 0.30, 0.30, 0.17, 0.09 | 0.375, 0.296, 0.296, 0.173, 0.086 | | |
| lag: corr(face at t − L, full 1 at t), L = 1, 2, 4, 8 | 0.09, 0.08, 0.09, 0.06 | 0.091, 0.082, 0.088, 0.059 | | |
| lag: face autocorrelation, L = 1, 4, 8 | 0.52, 0.21, 0.09 | 0.517, 0.206, 0.087 | | |
| lag: replaced core 1 with face, L = 0 | 0.106 | 0.106 | | |
| excursions, fair: Δ ln f_k at k = 15, 4, 1 | −0.23, −0.60, −0.65 | −0.232, −0.592, −0.657 | | |

Errors on the layer densities are not computed (correlated samples); treating each descent to ≤ 10 cells as one
sample gives about ± 0.0005 for the face-≤-10 densities. The lag table is from 2 × 10⁶ generations × 512 lanes.

**The chain against nzd.c at R = 9 (45 cells), same settings, my seeds for both programs** (`r9_*` rows): gump
9.823 ± 0.010 against 9.817 ± 0.010 (+0.4σ); fair d = 1 (M = 64, B = 256) 10.081 ± 0.011 against 10.085 ± 0.011
(−0.3σ); core copy, two seeds each, 9.645 ± 0.006 against 9.655 ± 0.007 (−1.1σ); p = 0.2, 9.840 ± 0.010 against
9.832 ± 0.010 (+0.6σ). P₁ agrees in every pair (0.764–0.778; my first two R = 9 rows count descents from ≥ 16,
later ones and nzd from round(45/4) = 11).

**Fair coins, the one row that was ever in tension.** My first seed read 14.264 ± 0.025 (−1.6σ), its excess deaths
in P₁ (0.785 ± 0.009 against 0.761), not in the descent rates (Δ ln f₁ −0.657 against −0.654). nzd.c run by me at
R = 11 with my seed 9201 (4 × 10⁶ generations) gives 14.344 ± 0.029 (nzd pooled with the agent's seed: 14.319 ±
0.014); my second seed 14.324 ± 0.033 with P₁ 0.753. Pooled mine 14.286 ± 0.020: −1.0σ against the agent, −1.4σ
against nzd pooled. A fluctuation; I find no difference of law between the programs (both read; the law check above;
R = 9 agrees). The eight-face values agree too (mine 13.802 ± 0.007, theirs 13.808 ± 0.005).

## Defects, ranked by how much they matter

1. **The ordering variable fails on a fifth, sixth and seventh chain** [measured]. The README: "the four annealed
   chains are in the same order by this low-face density as by their lives (0.348, 0.384, 0.423, 0.435 →
   −0.43, 0, +0.46, +0.53)", density = the replaced core of layer 1 after the darts, face ≤ 10. Mine, same quantity:

   | chain | Δ ln τ (mine) | core 1 after darts, face ≤ 10 | before darts, face ≤ 10 | var/binom (before, within F) |
   |---|---:|---:|---:|---:|
   | every depth at 0.1 | −0.327 | **0.311** | 0.371 | 1.75 |
   | copy from the replaced cells | −0.445 | 0.348 | 0.348 | 2.10 |
   | every depth at 0.2 | +0.002 | **0.354** | 0.397 | 1.69 |
   | gump | 0 | 0.384 | 0.384 | 1.80 |
   | copy from the whole layer (2 seeds) | −0.183 | **0.386** | 0.398 | 1.77 |
   | LOW10 coins | +0.448 | 0.422 | 0.433 | 1.58 |
   | mean-density coins | +0.535 | 0.435 | 0.436 | 1.58 |
   | fair coins | +0.653 | 0.457 | 0.445 | 1.54 |

   The whole-layer copy has gump's low-face density and (before the darts) gump's clustering and lives 0.18
   shorter (7.8σ); the p = 0.2 chain is thinner than gump under a low face and lives as long; p = 0.1 is the thinnest
   of all and outlives the core copy. The scan chains also change the deeper replaced layers (their rule-made density
   is 0.44–0.46 at depths 2–4, against gump's 0.41–0.42), so they are not a clean test of layer 1 alone; the
   whole-layer copy is (its deeper replaced layers are within 0.004 of gump's before the darts). Whatever sets the
   life, it is not the low-face density of the replaced core, nor its clustering, alone.
   `python3 research/blast/ref-density/collect.py` (section "Descents"; the after-dart column is `BYFPOST`).
   **Confirmed with the agent's own program and measure**: `NZD_LAYERS=1 nzd 11 brute 9301 1000000 256 1 3 s` (the
   whole-layer copy, `data/nzd/lay_shufwhole_d1_s9301.txt`) gives LAYER core1 at pop ≤ 10 = 0.3858 (gump 0.3838 in
   their `lay2_gump_d1_s6002.txt`), VAR core1 at pop ≤ 10 = 1.65 of binomial (gump 1.81: *less* clustered), and
   core 2 after the darts 0.423 all time, 0.447 at pop ≤ 10 (gump 0.409, 0.428: *denser*) — with Δ ln τ = −0.183 ±
   0.018 over my two seeds (7.8σ below my gump). A support that is as dense as gump's in layer 1, denser in layer 2
   and less clustered under a low face, and a shorter life.
2. **"Gump's layer 1 leads the face's population by one to two generations" contradicts the loop it supports**
   [numbers measured, reading inference]. The lagged correlations reproduce to three decimals (table), but the
   cross-correlation of the whole layer 1 with the face **peaks at lag 0** (+0.375 > +0.296 at lags 1 and 2):
   nothing leads in the sense of a displaced peak. What is measured is an asymmetry. The layer's own autocorrelation
   is +0.056 at lag 1 and +0.177 at lag 2 (a period-2 component; the face's is +0.517 at lag 1), which is why lags 1
   and 2 tie. A Granger comparison (`python3 research/blast/ref-density/lagdump.py` on a 64-lane, 300,000-generation
   dump, VAR(4), standardized; `data/lagdump_gump_R11_s1101.txt`) says the asymmetry is directional: the layer's past
   raises the explained share of the face's variance from 0.279 to 0.317 (+0.038), the face's past raises the layer's
   from 0.053 to 0.060 (+0.007). The README's causal sentence is "when the face thins, layer 1's cells lose their
   face neighbours and thin too (gump's layer 1 leads …), which removes the supply …": a layer that thins because
   the face thinned would lag it. The data's strong arrow is layer → face; the face → layer arrow that closes the
   proposed loop is the weak one. The replaced cells carry almost none of either (core 1: +0.106 at lag 0; Granger
   +0.002 and +0.004).
3. **"Density accounts for a fifth" depends on what is matched** [measured; the share is an attribution]. The split is
   gump → independent coins at gump's density → coins at 0.5; the other order needs "gump's correlations at density
   0.5", which is not a chain, so the split is an attribution along one path, not a property of the system. Along
   it, coins at the mean density do not make gump's density: in my mean-density chain the replaced cells' rule-made
   density is 0.4405, 0.4202, 0.4257, 0.4280 at depths 1–4 against gump's 0.4301, 0.4094, 0.4149, 0.4165 (+0.010 to
   +0.011 at every depth; after the darts 0.438 at depth 1, theirs 0.438). Fresh coins at gump's density hold up more
   rule-made life than gump's correlated layer does. The chain whose replaced core is at gump's realized density is
   LOW10 (0.428 after the darts in theirs and in mine; the README says so); on it the density share is
   0.678 − 0.463 = 0.215 ± 0.019 in theirs, 0.653 − 0.448 = 0.205 ± 0.035 in mine: a third, not "a fifth to a
   quarter" (mine along the README's own path, fair − mean: 0.118 ± 0.033 at d = 1; at d = 2 0.035 ± 0.039 against
   their 0.088 ± 0.019, my mean-density d = 2 row sitting 2.0σ above theirs). Even LOW10 is matched only at depth 1:
   its rule-made deeper layers are at 0.421, 0.426, 0.428 (depths 2–4) against gump's 0.409, 0.415, 0.417.
4. **"Independence from the face" is narrower than what the rows show** [inference]. Their conditioned coins (bias
   = gump's P(alive | m live face neighbours), overall or under a low face) are not independent of the face, yet keep
   +0.497 and +0.446 of the +0.532 (not rerun by me). Gump's local dependence on the face is weak (0.375 / 0.450 /
   0.445 for m = 0, 1, 2 at depth 1), and the replaced core correlates +0.106 with the face (reproduced). With item 1,
   what coins remove is something other than a cell's correlation with the face above it or the core's low-face
   density: candidates are the layer's memory (its own autocorrelation) and the correlations among the replaced cells
   and their unreplaced neighbours. The copy rows (−0.17, −0.43) add correlation of a kind gump does not have (a voter
   move; the core copy's within-F variance 2.10 against gump's 1.80): "random placement is not what helps;
   independence from the face is" is an inference they do not carry.
5. **"Gump's own layers are worth independent coins of 0.19, less than half their own density"** [p* measured;
   the reading is not]. p* is a coin bias. The chain at p = 0.2, which lives as gump does (+0.002 ± 0.023), has its
   replaced core of layer 1 at 0.399 after the darts and 0.456 before (gump 0.430), its deeper replaced layers at
   0.44–0.45 before the darts: sparse coins make the rule fill in (fewer overcrowded cells). The support that is
   "worth gump's" is not at 0.19, and not half of anything; "an independent support of 0.19" is not what that chain has.
6. **"An independent bath of gump's density overestimates the life by 0.53"** [inference stated as a number]. 0.53 is
   the effect of darts that refresh 22% of the replaced cells per generation; the README shows the effect grows with
   the rate (+0.164 at ε = 1/16). A bath (every replaced cell fresh every generation) was not run at 9a105d3.
7. **The noisy chains' layer densities are read after the darts** (`step(); noise_random(M); observe();` in
   nzd.c). The support table's chain densities (0.348, 0.423, 0.435) mix the 22% of replaced cells that are fresh
   coins at that moment with the rule-made rest. It is the state the next step reads, a fair definition, but unstated;
   before the darts the same cells read differently (columns above).
8. **Adjacent seeds share the coin stream** [proved; `python3 research/blast/ref-density/seedstream.py`]: in nzd.c
   `sm2 = seed·G + 99991` and the stream advances by the same G, so word i of seed s + 1 is word i + 1 of seed s. The
   "two seeds" of rows (b) (5111, 5112) and (c) (5121, 5122) and adjacent scan seeds draw their biased or copied coins
   from one sequence offset by four coins. Their darts are independent, so the coins land on unrelated cells and
   times; I expect no measurable effect (argued, not measured), but "two seeds that agree to 0.001" is not two fully
   independent replications. Fair rows are unaffected (their coin is in the main stream).
9. **Minor.** Δ is taken against the eight-face anchor; the watched-face estimator counts ties for each face, so it
   sits a few thousandths below at ε = 0 (R = 9, mine 9.823 against 9.827). "P₁ is gump's 0.77 to within ± 0.02 in every
   chain": true in mine (0.762–0.790), but with a drift along the scan in both programs (theirs 0.786 at p = 0.1 to
   0.745 at p = 0.7; mine 0.790 at 0.1, 0.771 at 0.2, against gump 0.766); its share of Δ ln τ is ≤ 0.03.

## Sentences of the README's conclusions: measured or inference

| sentence (9a105d3) | status |
|---|---|
| fair +0.678, mean +0.532, LOW10 +0.463, copies −0.17 / −0.43, scan, p* ≈ 0.19 | measured; reproduced (table) |
| "mostly correlation (loss of correlation)" | attribution along one path (defect 3); "correlation" is everything but the mean |
| "gump's support fades with its face (0.430 → 0.384)" | measured; reproduced |
| "the coins' does not (0.42–0.44)" | measured after the darts (defect 7) |
| "the lives order by that low-face density" | measured on four chains; fails on three more (defect 1) |
| "a face down to one cell dies as often (0.77) with coins as without" | measured; reproduced (± 0.03) |
| "the coins slow the whole descent rather than rescue the last cell" | measured (Δ ln f_k); reproduced |
| "for its face, gump's own layers are worth independent coins of 0.19" | inference; misleading (defect 5) |
| "random placement is not what helps; independence from the face is" | inference (defect 4) |
| "layer 1 leads the face by one to two generations" | numbers measured; "leads" not (defect 2) |
| "the face and its first two layers fail together … a loop" | conjecture; its face → layer arrow is the weak one (defect 2) |
| "an independent bath overestimates the life by 0.53" | inference (defect 6) |
| "frozen coins are a disorder effect" | not checked |

## Forecasts, scored (`PREDICTIONS.md`, committed before each row)

| # | forecast | P | outcome |
|---|---|---:|---|
| 1 | gump baseline within 3σ | 0.95 | **hit** (−0.1σ) |
| 2 | fair d = 1 | 0.85 | **hit** (−1.0σ pooled; first seed −1.6σ) |
| 3 | mean density d = 1 | 0.80 | **hit** (+0.1σ) |
| 4 | copy from the replaced cells | 0.65 | **hit** (−0.5σ) |
| 5 | p = 0.1 | 0.80 | **hit** (−0.2σ) |
| 6 | p = 0.2 | 0.80 | **hit** (−1.2σ) |
| 7 | sign change between 0.1 and 0.2, p* ≈ 0.19 | 0.80 | **hit** (0.199 ± 0.007) |
| 8 | core-1 density, all time | seen | 0.4301 = 0.4301 |
| 9 | core-1 density, face ≤ 10 | 0.85 | **hit** (0.3843 against 0.3836) |
| 10 | P₁ the same with and without coins (± 0.02) | 0.75 | **hit, barely**: 0.762–0.790 against gump's 0.766; p = 0.1 is +0.024 |
| 11 | lag correlations as stated | 0.70 | **hit** (to the third decimal) |
| 12 | R = 9 chain against nzd.c | 0.90 | **hit** (all four pairs within 1.1σ) |
| — | conjecture: the lag asymmetry is from different autocorrelations, not a lead | 0.60 | **half wrong**: no lead in the peak sense, but the asymmetry is directional (Granger), not only autocorrelation |
| — | the mean-density chain's replaced core sits above 0.435 all time | 0.70 | **hit** (0.4405 rule-made, 0.438 after the darts) |
| 13 | copy from the whole layer | 0.80 | **hit** (−1.3σ; two seeds −0.7σ) |
| 14 | the ordering by low-face density survives a fifth chain | 0.60 | **miss** (0.386, gump's density, Δ −0.18) |
| 15 | LOW10 d = 1 | 0.80 | **hit** (−0.5σ) |
| 16 | mean density d = 2 | 0.80 | **hit** (+2.0σ) |
| 17 | the p = 0.2 chain's support above 0.35 after the darts (informed by R = 9) | 0.80 | **hit** (0.399) |
| 18 | fair d = 2 | 0.80 | **hit** (+0.2σ) |
| 19 | mean density, ε = 1/16 | 0.80 | **hit** (+1.1σ) |
| 20 | my second fair seed lands above the first | 0.65 | **hit** (14.324 against 14.264) |
| 21 | second whole-layer copy seed: core 1 at face ≤ 10 within 0.005 of 0.384, Δ < −0.10 | 0.80 | **hit** (0.3853, −0.161) |
| 22 | nzd.c's own LAYER core1 at pop ≤ 10 on that chain within 0.01 of 0.384 | 0.80 | **hit** (0.3858) |

Score: 21 hits, 1 miss (14), 1 half-wrong conjecture, 1 not blind (8). I was too cautious on the reproductions
(mean stated probability 0.80, outcome 18 of 18) and right to doubt the mechanism.

## Not checked

- The conditioned coins (+0.497, +0.446), frozen coins (+1.18), the scan at 0.3, 0.4, 0.7, LOW10 at d = 2, second
  seeds of the d = 2 rows, the births-per-supply and drift columns of the support table, the agent's `validate.py`,
  its REC recount.
- Errors of the layer densities (correlated samples; only the rough per-descent estimate above).
- Whether the dart law's small departures from independent per-cell coins matter (both programs share the law).
- A full bath (every replaced cell fresh every generation); the decomposition's other order (no chain defines it).
- Whether depths ≥ 2 or the layer's memory are what orders the chains (defect 1 says what it is not, not what it is).
- 84 cells; any radius but 9 and 11.

## Second review (2026-11-24, 17:04–17:40 UTC): the skin depth at full replacement (section 2 at commit 2d67675)

Claim refereed: **a face with four real layers (the face and depths 1–3) over fresh independent coins dies at gump's
rate and in gump's way; with three real layers it lives longer.** Column A only (coins at depth ≥ d under the watched
face and ≥ 3 under the other seven), every coin fresh every generation at gump's mean density for its depth.

**My chain** [`rd.c`, `RD_FULL=1`]: after every step, every cell of N in every lane whose life did not just end is set
to a fresh coin of its depth's bias (a 32-bit half of a fresh xoshiro word < round(p 2³²)); the next step reads the
coins; the faces are not in N. Validation: `python3 research/blast/ref-density/validate.py <rd> 1200` passes on the
new binary (the stepper is untouched; the dart path's output is unchanged, same RESULT line on a 20,000-generation
test); `RD_FULL=1 RD_FULLTEST=400 rd 9 run 778 1 0 3 <biases>` and `RD_FULLTEST=200 rd 11 run 779 1 0 4 <biases>`
(`data/fulltest.txt`): from all-alive, all-dead and striped states the redrawn cells' density matches the bias at
every depth (18 tests, |z| ≤ 2.2), the same test against bias + 0.01 fails (z −17 to −22), the covariances between
neighbouring N cells, adjacent lanes and two successive draws of one cell are zero (|z| ≤ 2.1), and no cell outside
N changes (0 of 10⁷ words). The region is theirs: |N| = 27 at R = 9, d = 4 (their 9 + 9 + 9) and 96 at R = 11 (their
18 + 21 + 21 + 18 + 18). **Biases, my own measurement** (gump rows `r9_gump_s9001`, `gump_R11_s1001`): 45 cells,
depths 3–6: 0.41448, 0.41678, 0.41677, 0.41448 (theirs 0.41451, 0.41679, 0.41679, 0.41451); 63 cells, depths 3–8:
0.41490, 0.41655, 0.41565, 0.41564, 0.41655, 0.41490 (theirs 0.4150, 0.41650, 0.41570, 0.41570, 0.41650, 0.41499):
agreement to 10⁻⁴. Rows: `RD_FULL=1 sh research/blast/ref-density/row.sh TAG R SEED GENS 0 d b:<biases>` (files
`data/rows/full{9,11}_A_d*`); table: `python3 research/blast/ref-density/skin2.py`. My gump references, same code
and estimator: 45 cells 9.8190 ± 0.0026 (two seeds; theirs 9.8177 ± 0.0036), 63 cells 13.6336 ± 0.0108 (two seeds).

| row (column A) | theirs Δ | mine Δ (against my gump) | difference |
|---|---:|---:|---:|
| 45 cells, d = 3 | +0.169 ± 0.008 | +0.169 ± 0.005 (65,569 deaths) | 0.0σ |
| **45 cells, d = 4** | +0.004 ± 0.007 | **+0.007 ± 0.004** (76,807) | +0.3σ |
| 63 cells, d = 3 | +0.295 ± 0.023 | +0.311 ± 0.024 (2,247) | +0.5σ |
| **63 cells, d = 4** | +0.016 ± 0.012 | **+0.013 ± 0.018** (4,840) | −0.1σ |
| 45 cells, d = 4, every bias −0.01 | — | +0.003 ± 0.004 | |
| 45 cells, d = 4, every bias +0.01 | — | +0.001 ± 0.004 | |
| 63 cells, d = 4, every bias +0.01 | — | +0.019 ± 0.021 | |

Way of dying at d = 4, against my gump in my code (dips = descents from ≥ H to ≤ H − 1 per lane-generation, H = 11
and 16; deadliness = share of them that die before the face is back at H; P₁ from ≤ 1 cell):

| | d ln dips | d ln deadliness | P₁ (gump) |
|---|---:|---:|---:|
| 45 cells, d = 4 (theirs +0.005, −0.004, 0.771) | **+0.0046 ± 0.0004** | −0.011 ± 0.004 | 0.7712 ± 0.0013 (0.7715 ± 0.0009) |
| 45 cells, d = 4 at bias −0.01 / +0.01 | +0.0058 / +0.0041 | −0.008 / −0.005 | 0.7722 / 0.7714 |
| 63 cells, d = 4 (theirs +0.002 and +0.001, +0.003 and −0.010) | +0.0016 ± 0.0005 | −0.015 ± 0.018 | 0.770 ± 0.005 (0.769 ± 0.004) |
| 45 cells, d = 3 (theirs −0.055, −0.111) | −0.0554 | −0.113 | 0.7655 (gump 0.7715) |
| 63 cells, d = 3 (theirs −0.088, −0.196) | −0.0877 | −0.223 | 0.768 |

**Findings.**
1. **The claim reproduces at both sizes** [measured]: four rows within 0.5σ, independent code, RNG, seeds and bias
   measurement. Three real layers add +0.17 and +0.31; four add nothing measurable (+0.007 ± 0.004, +0.013 ± 0.018).
2. **No tuning is hidden in "gump's mean density"** [measured at 45 cells, one row at 63]. Shifting every bias by
   ± 0.01 moves Δ(4) by nothing measurable (+0.003, +0.007, +0.001 ± 0.004; slope −0.07 ± 0.31 per unit of density,
   against ≈ 2.5–3 per unit for darts at d = 1). Below three real layers the coins' density hardly matters at all, so
   the null result does not rest on matching it to four decimals.
3. **"In gump's way" holds to 1%, not exactly** [measured]. At d = 4 the face dips more often: +0.46% at 45 cells
   (11σ by counts; my two gump seeds differ by 0.10%, about Poisson, so the counting error is not much larger; the
   same +0.4% to +0.6% in all three d = 4 rows at different biases, and +0.005 in the agent's independent row) and
   +0.16% at 63 cells (3σ); the deadliness moves the other way (−1.1 ± 0.4% at 45 cells), so the life does not
   change. A coin bath under three real layers leaves a resolved trace in the living face's excursions, too small
   to show in the lifetime. The README's bound "|Δ ln dips| ≤ 0.005" is correct; "as frequent as gump's" reads as
   stronger than what is measured.
4. **The order "coins drawn, then the rule reads them" is the same in both codes and cannot matter** [read; proved].
   Both do step → redraw N → face check, and the next step reads the coins (`step(); noise_full(); observe();` in
   nzd.c). The rule's output on N is overwritten before any cell reads it, and N holds no face cell. So "draw, then
   step" and "step, then draw" differ only in the first generation of each life (soup instead of coins), which lies
   inside the 200 generations of ageing-in.
5. **The coin stream of their skin rows** [read]. The 45-cell skin rows (seeds 9101–9104) and the 63-cell ones before
   the agent's fix (7c64966) use the old second stream, in which consecutive seeds' coins are one sequence offset by
   one word. At full replacement the consumption is fixed (16 words per cell and 64 lanes per generation), so the
   d = 3 and d = 4 rows reuse each other's raw words at other cells and times. Each row is a valid sample of its
   chain; the rows are not independent of each other in their coins. My independent rows reproduce them, so it did
   not matter here.

Forecasts (`PREDICTIONS.md`, block "Second review", committed 17:07:22, rows from 17:07:44): S1–S4 **hit** (0.0σ,
+0.3σ, +0.5σ, −0.1σ); S5 **miss** (P₁ and deadliness yes, the dips' frequency at 45 cells no: +0.46%, 11σ); S6 **miss**
(I expected the density to matter a little below the skin; it does not, to ± 0.004).

Not checked (second review): column B; d = 1, 2, 5, 6 at full replacement; d = 4 with darts (ε < 1); faces above 63
cells; the bias shift at 63 cells beyond one row (+0.01 only, ± 0.021); the dips' overdispersion beyond two gump
seeds per size; the agent's `cells.py`.
