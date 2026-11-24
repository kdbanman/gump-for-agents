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
