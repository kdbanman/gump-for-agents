# ref-density: referee of `research/blast/density/README.md` (commit 9a105d3)

Referee session, 2026-11-24 (13:55–15:50 UTC). Subject: the sections of the density agent's README present at commit
9a105d3 (program `nzd.c` at that commit), not the section it is adding now. Everything below was computed with my own
code, `rd.c`, written from `reference/oracle.py` and from the prose of `research/blast/noisy/README.md` ("The chain,
exactly") and of the density README, before reading `nz.c` or `nzd.c` (I never opened `research/audit/blastnoisy/`).
`nzd.c` was then read critically and run as a black box, built from `git show 9a105d3:research/blast/density/nzd.c`.

## My chain, exactly

- **Stepper** [measured]: `python3 research/blast/ref-density/validate.py <rd binary> 1200` → `VALIDATION PASSED`
  (`validate_1200.txt`). R = 11 (876 cells) and R = 9 (510 cells), two seeds each, three soups of density 0.35 per
  seed, 1,200 generations, against `oracle.step` on a box of side 2R + 4: every hull cell, no live cell outside the
  hull, the watched face's population, the eight faces' emptiness, identical at every generation. Negative control
  (`RD_NEGCTL=1`: one corner-touching neighbour of every x-normal cell replaced by the edge-sharing coplanar face)
  fails at generation 1 at both radii. Bit-sliced, 512 lanes; group sizes come out as the README's (core 9, 9, 18, 18,
  21 at depths 1–5, 57 deeper; whole layers 63, 75, 75, 81, 81; |N| = 132, B = 1,024 at d = 1).
- **Noise law** [exact, by construction]: N = cells at depth ≥ d under the watched face (+,+,+) and ≥ 3 under each
  other face; B = smallest power of two ≥ 4|N|; after each generation, in each lane independently, M darts i.i.d.
  uniform on B squares, thrown in sequence, a dart on a cell of N setting it to its coin. Sampled in the
  law-equivalent form K ~ Binomial(M, |N|/B) (exact pmf, inversion), then K i.i.d. uniform cells of N in sequence.
  Coins: fair = one bit of a fresh 32-bit word; bias p = a fresh 32-bit word < round(p 2³²); copy = the current state
  (earlier darts of the same generation included) of a uniformly chosen cell of the source set at the same depth
  under the watched face, the dart's own cell included (source: N's cells at that depth = "core", or every hull cell
  at that depth = "whole layer"). A cell is hit with probability q = 1 − (1 − 1/B)^M = 0.2213 per generation at
  ε = M/B = 1/4. RNG: xoshiro256** seeded by splitmix64; my seeds (1001–1012, 9001–9013), none of theirs.
- **Life protocol and estimator**: as the noisy README states it (soup 0.35, age 0; a lane-generation is exposure iff
  age > 200 after the step; a life ends when any face is empty; a watched death is a life ended with the watched face
  empty, alone or tied, at an exposure generation; re-seed). ln τ = ln(exposure / watched deaths) ± 1/√deaths. No
  settled-life guard (longest life reported instead). All diagnostics are read after the step and before the darts;
  for the replaced core of layer 1 also after the darts (`DENS core1 after darts`, `BYFPOST`).
- Rows: `sh research/blast/ref-density/row.sh TAG R SEED GENS M D0 COIN [LAGGENS]` (output scratch `rows/TAG.txt`,
  copied to `data/rows/`); the table: `python3 research/blast/ref-density/collect.py`.

DRAFT — the table and the rest are being filled in.

## What `nzd.c` does, read against its README [read at 9a105d3; checked where a command is given]

Confirmed as stated (each read in the source; the first five also reproduced by my independent rows):
which cells are replaced (depth ≥ DW under the watched face and ≥ DO = 3 under every other face, `geom_init`);
ε = M/B with B the smallest power of two ≥ 4|N|, K ~ Binomial(M, |N|/B) darts on N per lane and generation from a
32-bit fixed-point CDF, cells by a 31-bit multiply-shift (`noise_random`); the fair coin is bit 0 of the dart's word,
independent of its 31 square bits; a biased coin is 16 bits of the second stream against round(p 2¹⁶); the copy
coin reads the current state, darts of the same generation included, of a uniform cell of the source set (self
included), the core source being the cells at that depth with depth ≥ 3 under every other face; a death is the
watched face's population 0 after the step (alone or tied); exposure = lane-generations at age > 200;
ln τ = ln(E/n₀) ± 1/√n₀; lanes are independent soups with independent darts; descents (`REC`) from ≥ round(A/4) = 16;
`LAG` = Pearson correlation of face(t − L) with group(t) and of group(t − L) with face(t), within a life.
"MEAN" and "LOW10" are the core densities of gump's own layers at M = 0 (after the step; my gump row gives the same
to 4 decimals, below).

Departures and defects, in order of consequence:

1. **The layer diagnostics of the noisy chains are read after the darts** (`step(); noise_random(M); observe();`).
   So "the coins' support does not fade (0.42–0.44)" and the support table's chain densities (0.348, 0.423, 0.435)
   are a mixture of the 22% of replaced cells that are fresh coins at that moment and the rule-made rest. In gump
   (no darts) nothing changes. The mixture is the state the next step reads, so it is a fair definition of "the
   support", but the README does not say so, and the rule-made part alone behaves differently (table below:
   before the darts the mean-density and fair chains' replaced cells are at gump's density or barely above it).
2. **Consecutive seeds share the coin stream** [proved; `python3 research/blast/ref-density/seedstream.py`]:
   `sm2 = seed·G + 99991` and the stream advances by the same constant G, so word i of seed s + 1 is word i + 1 of
   seed s. The "two seeds" of rows (b) (5111, 5112) and (c) (5121, 5122) and every pair of adjacent scan seeds draw
   their biased or copied coins from one sequence, offset by four 16-bit coins. Their darts (the main stream) are
   independent, so the coins land on unrelated cells, lanes and times, and I expect no measurable effect (argued,
   not measured); but "two seeds that agree to 0.001" is not two fully independent replications. Fair rows are
   unaffected (their coin is in the main stream).
3. **Estimator against anchor** (minor): every Δ is "watched-face ln τ − 13.633", the anchor being an eight-face
   value 8E/D. The watched-face estimator counts tied deaths for each face, so at ε = 0 it sits slightly below the
   eight-face value (R = 9: 9.823 against 9.827 in my row, 9.817 against 9.829 in nzd's). The bias is a few
   thousandths, inside every quoted error.

## The reading (sentences of the README at 9a105d3, labelled)

**R1. "Leads by one to two generations" [the numbers reproduce; the word does not].** My gump row (independent code,
seed 1001, 2 × 10⁶ generations × 512 lanes) gives, to three decimals, the README's lagged correlations (table
below). They are computed correctly (Pearson within a life, both times past the ageing-in, same in `nzd.c` and in my
code). But the cross-correlation of the whole layer 1 with the face **peaks at lag 0** (+0.375), not at lag 1–2
(+0.296, +0.296): nothing leads in the sense of a displaced peak. What is measured is an asymmetry: the side where
the layer is earlier decays slowly, the other side drops at once to +0.09. The layer's own autocorrelation is +0.056
at lag 1 and +0.177 at lag 2 (a period-2 component; the face's is +0.517 at lag 1), which is why lags 1 and 2 tie.
A Granger comparison on a 64-lane, 300,000-generation dump (`lagdump.py`, VAR(4) on standardized series) says the
direction is real: the layer's past raises the share of the face's variance explained by its own past from 0.279 to
0.317 (+0.038); the face's past raises the layer's from 0.053 to 0.060 (+0.007) [measured]. So "the layer drives the
face more than the face drives the layer" is supported. **This contradicts the sentence the number is cited for**:
"when the face thins, layer 1's cells lose their face neighbours and thin too (gump's layer 1 leads the face's
population by one to two generations …)" — a layer that thins *because* the face thinned would follow it, not lead
it; the data's strong arrow is layer → face, and the face → layer arrow of the proposed loop is the weak one. The
replaced cells themselves (core 1) carry almost none of this: +0.106 at lag 0, Granger +0.002 and +0.004.

**R2. "Density alone is the smaller part … +0.146 ± 0.020, a fifth to a quarter" [measured along one path; the share
depends on what is matched].** The decomposition is gump → independent coins at gump's density → independent coins at
0.5. The other order needs "gump's correlations at density 0.5", which is not a defined chain, so the split is an
attribution along one path, not a property of the system. Along that path the answer depends on which density is
matched: the coin bias matched to the all-time mean (row b) leaves 0.146 for density; but in that chain the replaced
core sits at 0.438 after the darts (their `lay2_mean_d1_s6112.txt`) against gump's 0.430, i.e. it is not
density-matched; the chain whose replaced core *is* at gump's all-time density is LOW10 (0.428, their
`lay2_low10_d1_s6122.txt`; the README says so itself), which leaves 0.678 − 0.463 = 0.215 ± 0.019 for density, a
third. "A fifth to a third" is the fair range [inference from their numbers; my rows below].

**R3. "Independence from the face" [inference; their own conditioned rows argue against the literal reading].** Coins
whose bias follows the cell's live face neighbours (gump's own P(alive | m), overall or under a low face) are not
independent of the face, yet keep +0.497 and +0.446 of the +0.532 (their rows; not rerun by me). Gump's local
dependence on the face is weak (0.375 / 0.450 / 0.445 for m = 0, 1, 2 at depth 1), and the lagged correlation of
the replaced core with the face is +0.106 at lag 0 and ≤ 0.05 after (reproduced). What the coins remove is not a
cell's correlation with the face above it but everything else gump's layer has and a fresh coin lacks: memory, the
in-layer correlation among the replaced cells, and the collective thinning of the layer while the face is low. The
README's own mechanism paragraph says the last; its headline word "independence" says less than that.

**R4. "Random placement is not what helps; independence from the face is" (from the copy coins) [inference].** A
copy coin is not gump's correlation: copying a random replaced cell into another is a voter move that clusters the
9 replaced cells of layer 1 far beyond gump (their count's variance 2.47 of binomial under a low face, gump 1.81).
The two copy rows show that adding correlation of this kind shortens the life; they do not show that gump's own
correlations are what shortens gump's life relative to coins.

**R8. "A face law that treats the support as an independent bath of gump's density overestimates the life (by 0.53
in ln τ at 63 cells)" [inference stated as a number].** 0.53 is the effect of darts that refresh 22% of the replaced
cells per generation (ε = 1/4); the README itself shows it grows with the rate (+0.164 at ε = 1/16). An independent
bath (every replaced cell fresh every generation) was not run at 9a105d3, so its offset is not 0.53; it is
presumably larger.
