# Review of research/shape/: the shape of a periodic slab face (twisted tori)

Adversarial review, 2026-11-14. Object: `research/shape/` at commits 445d7e0 … 4e494aa (`PREDICTIONS.md`, `README.md`,
`lattice.py`, `tslab.py`, `rep_ring.c`, `drive.py`, `summary.py`, `fits.py`, `data/`). Scripts are in
`research/audit/shape/`. They share no code with `research/shape/`. The one exception is `geom_check.py`, which imports
`tslab.py` so that it can compare that file's graph with its own. Bulk output is in `research/scratch/audit_shape/`
(git-ignored).

    python3 research/audit/shape/geom_check.py      # lattices, classes, layer periods, graph vs tslab, embedding (2 s)
    python3 research/audit/shape/recompute.py       # tables and chi^2 from data/*.csv, robustness of the size claims
    python3 research/audit/shape/stages.py          # A = 60 difference before / in the top-up (from research/shape's raw npz)
    for L in "4 1 6 4000 24" "5 1 4 4000 20" "4 0 5 4000 20" "4 0 6 4000 24" "2 3 10 4000 20" "3 0 8 4000 24" "4 4 6 4000 24"; do
      python3 research/audit/shape/ts.py validate $L; done; python3 research/audit/shape/negctl.py   # stepper vs engine
    bash research/audit/shape/run_all.sh; bash research/audit/shape/run_more.sh; bash research/audit/shape/run_extra.sh  # ~1 h on 3 cores
    python3 research/audit/shape/compare.py         # review against research/shape
    python3 research/audit/shape/ts.py stats a k b  # one torus
    python3 research/audit/shape/prof.py 4 0 6 1500000 71; ... ; python3 research/audit/shape/prof.py show   # face-death profiles

**The independent stepper** is `ts.c`, driven by `ts.py`. It is bit-sliced, with 1,024 replicas. The graph is built from
AUTOMATON.md's cube-index table, not from the doubled offsets. Its RNG (splitmix64) is its own, and so is its layer
indexing. Each replica runs successive lives ("renewal"). A life starts from a fresh p = 0.4 soup and ends at its first
event: a face death, or three adjacent dead layers on a transverse diagonal with ≥ 3 layers. Settling (period dividing
840) and the cap of 5 × 10⁵ generations censor a life. So does the end of the run: the exposure is kept and there is no
event. Events are checked every 8 generations.

The stepper was checked against the engine. `validate` tiles the slab into the engine's cubic N-torus with the review's
own coset enumeration. On seven tori, (4,1),(0,6), (5,1),(0,4), 4×5, 4×6, (2,3),(0,10), 3×8 and (4,4),(0,6), the
population times the number of copies matches the engine at every one of 4,000 generations. A tiling with the wrong
lattice (`negctl.py`) mismatches at generation 1. The binary was rebuilt once during the runs (a profiling flag was
added; the stepping code did not change), and both builds pass.

## Summary

| claim | verdict |
|---|---|
| 1. At A = 72, ln τ_face is monotone in systole²; values agree within systole groups (χ² 1.8 / 7) | **stands with a correction.** Every number reproduces from the CSV. Only 4 of the 7 degrees of freedom test the hypothesis: the other 3 compare presentations of one torus, which are equal by symmetry. On distinct shapes the χ² is 1.1 / 4. An independent run puts systole² 21 at 15.035 ± 0.009, against 15.066 ± 0.014 (1.9σ lower). The ordering and the 4×6 value reproduce. |
| 2. At A = 60, 4×5 = 12.490 ± 0.003 and (5,1),(0,4) = 12.471 ± 0.003 differ (4.6σ, after a data-dependent top-up) | **stands.** An independent rerun gives 12.4883 ± 0.0030 and 12.4707 ± 0.0030, a difference of 0.0177 ± 0.0042 (4.2σ). The top-up alone, by its own seeds, already shows 0.021 ± 0.005 (4.0σ). "Systole alone" fails at A = 60. |
| 3. Hex systole and shortest kagome row are refuted | **stands.** Both forecasts put systole² 12 and 13 at or above 4×6, and they lie 4.6–8σ below it at A = 72 and 5–10σ below at A = 60. The independent runs confirm this for (4,4),(0,6) against 4×6: hex systole 4 both, 0.100 ± 0.018 apart. |
| 4. Twisting removes the firewall channel, and those tori fall on the curve; the systole effect is about twice as large at 72 as at 60 (1.8 ± 0.3); systole 3 lies 0.21 below the trend | **stands with corrections.** "None possible" is wrong: the firewalls are rare, not impossible, and the review sees 2 on (4,1),(0,6). Twisting alone does not remove the channel: (6,1),(0,4) and (6,3),(0,4) are twisted and have 5% firewalls. The ratio depends on which points enter: 1.3 ± 0.4 to 2.3 ± 0.4. The 0.21 gap is robust to the choice of fit (0.19–0.24). |
| 5. Face deaths: ~37 cells until ~10 generations before death, then empty in 6–8; same on three tori | **stands** for the profile, which reproduces with independent code. The "no band along the short loop" statistic was not rechecked. |

## Geometry

`geom_check.py`, output in `research/scratch/audit_shape/geom_check.txt`.

- **Classes.** The slab's in-plane point group is generated from O_h itself, as the 12 signed permutations that map
  (1,1,1) to ±(1,1,1), acting on (x, y, −x−y). Grouping by that group gives the same partition as grouping by reduced
  Gram matrix, for all 42 index-20 and all 60 index-24 lattices (10 and 15 classes). So "same Gram" means "same torus
  for the automaton" here, and no pair of tori is isometric without being equivalent. −1 fixes every lattice, so the
  slab flip adds nothing beyond the coordinate permutations.
- **Index, systole², class, periods.** Every one of the 20 tori matches the README and PREDICTIONS tables: index,
  systole² (brute force), Gram, class, and the transverse periods (gcd over all short lattice vectors, not only the two
  generators). Each claimed "same torus" is one class: (4,0)/(4,2),(0,6); (4,3)/(4,5),(0,6)/(3,1),(0,8); 4×5/5×4;
  (5,1),(0,4)/(2,3),(0,10). Each claimed "different shape" is a different class.
- **Neighbour graph.** On (4,1),(0,6), (5,1),(0,4), 4×5, (2,5),(0,12), (8,2),(0,3), (4,4),(0,6), (2,2),(0,10) and
  (2,3),(0,10), the graph built from the cube-index table equals `tslab.py`'s cell by cell. No cell has a repeated
  neighbour, and every transverse layer partition is identical.
- **Embedding.** N Z² ⊂ Λ holds for every torus (N = 24 at index 24, N = 20 at index 20). The cubic torus's slab
  period lattice is N Z² in (i, j), because the identification (i+N, j, k−N) is the in-plane vector N·u1. The region
  outside the slab is N − 8 ≥ 12 d0-layers wide and starts dead. By T2/T4 it stays dead, and three dead layers suffice;
  two would not, which is why N ≥ m + 3. So the embedding tests the twisted graph, and the 3,999-generation MATCH is
  meaningful. The review's own embedding gives MATCH as well.

## Claim 2: the A = 60 pair (independent rerun)

| torus | review (ts.c) | research/shape (shape pooled) | review − shape |
|---|---|---|---|
| 4×5 (16,12,21) | 12.4883 ± 0.0030 (111,193 face deaths) | 12.4900 ± 0.0029 | −0.002 ± 0.004 |
| (5,1),(0,4) (16,4,19) | 12.4707 ± 0.0030 (113,173) | 12.4713 ± 0.0029 | −0.001 ± 0.004 |
| difference | **+0.0177 ± 0.0042 (4.2σ)** | +0.0186 ± 0.0041 (4.6σ) | |

Seeds were fixed before the run, with three runs of 1,024 replicas × 4.8 × 10⁶ generations per torus. There was no
stopping rule. The hazard is flat in age: the equal-exposure thirds give 12.489, 12.487, 12.489 and 12.471, 12.471,
12.470 (± 0.005). Firewall rates are ln τ_fw = 17.15 and 17.23, and ties (face and firewall at the same check) are 37
and 44, negligible. Split by stage from the shape experiment's own raw files (`stages.py`), the difference is
0.015 ± 0.006 before the top-up and 0.021 ± 0.005 in the top-up alone. The top-up's size was fixed when it started (60,000 face
deaths per torus), so it was an independent confirmation already. The optional stopping did not create the effect.

## Claim 1 and the A = 72 pair

`recompute.py` reproduces every row of both CSVs from exposure and face deaths: ln(2E/F), 1/√F and systole². It also
reproduces the README's pooled values and χ²: systole² groups give 1.77 / 7 at A = 72 and 24.5 / 4 at A = 60.

- The χ² of 1.8 / 7 includes 3 degrees of freedom that compare presentations of one torus, which agree by symmetry.
  Pooling presentations first, the test of "systole alone" has 1.1 / 4 at A = 72 and 22.2 / 2 at A = 60. The A = 72
  statement is right, but it rests on four comparisons: two shapes at 9, two at 12, three at 16.
- At A = 72 the three systole-16 shapes span 0.019 ± 0.017, so the A = 60 shape effect could not have been seen there.
  The ordering of second loops does not carry over either. At A = 60 the shorter second loop (19) dies sooner. At
  A = 72, (16,0,27), with the shortest second loop, is the highest of the three (not significant).

Independent run (ts.c, four runs × 1,024 × 5.5 × 10⁶ generations each):

| torus | review | research/shape | review − shape |
|---|---|---|---|
| 4×6 (16,8,28) | 14.9662 ± 0.0084 (14,256; 5.2% firewalls, ln τ_fw 17.18) | 14.9711 ± 0.0098 | −0.005 ± 0.013 |
| (4,1),(0,6) (21,6,21) | 15.0347 ± 0.0087 (13,313; 2 firewalls) | 15.0657 ± 0.0140 | −0.031 ± 0.017 |
| difference | **−0.068 ± 0.012 (5.7σ)** | −0.095 ± 0.017 | |

One more run each (1,024 × 5.5 × 10⁶ generations; `run_extra.sh`) on three more shapes:

| torus | review | research/shape | review − shape |
|---|---|---|---|
| 3×8 (9,6,49) | 14.614 ± 0.014 (5,068; 86.6% firewalls, ln τ_fw 12.054) | 14.610 ± 0.014 (ln τ_fw 12.058) | +0.004 ± 0.020 |
| (4,4),(0,6) (12,0,36) | 14.866 ± 0.016 (3,939; no firewalls, no two adjacent dead layers) | 14.875 ± 0.014 | −0.009 ± 0.021 |
| (2,3),(0,12) (19,18,27) | 15.020 ± 0.017 (3,376; none) | 15.011 ± 0.014 | +0.009 ± 0.022 |

The review's own values alone are 14.614 (9), 14.866 (12), 14.966 (16), 15.020 (19) and 15.035 (21). They are
monotone in systole², but 19 and 21 are only 0.8σ apart.

The systole² 21 point is 1.9σ lower in the review's run. Both runs together give 15.043 ± 0.007. With 4×6 pooled the same
way (14.968 ± 0.006), that is +0.075 ± 0.010 above 4×6 (README: +0.093 ± 0.016). The direction and the monotone
ordering stand. The README's "magnitudes miss (21 is +0.093, forecast +0.04)" weakens to about 3.5σ from the forecast. For the review's 4×6 the hazard thirds are 14.998,
14.929, 14.973 (± 0.015): not a monotone trend, but χ² ≈ 11 / 2 about flat. Nothing comparable appears in
(4,1),(0,6) (15.034, 15.055, 15.015) or in research/shape's 4×6 (14.978, 14.971, 14.956 ± 0.024). I read it as a
fluctuation and have not chased it.

## Claim 3: alternatives refuted — stands

H0 (hex systole) and H0′ (shortest row) both predicted the systole² 12 and 13 tori at or above 4×6. At A = 72 they lie
0.096 ± 0.012 and 0.051 ± 0.011 below it. At A = 60 they lie 0.051 ± 0.005 and 0.038 ± 0.007 below the systole-16
group. Even against the lower systole-16 shape, (5,1),(0,4), the differences are 0.042 ± 0.006 and 0.029 ± 0.008. The
grouping χ² values reproduce (hex 76.6 / 10, rows 109 / 8 at A = 72). With independent code, (4,4),(0,6) is
14.866 ± 0.016 and 4×6 is 14.966 ± 0.008, both at hex systole 4. The refutation does not depend on the A = 60
shape effect, which is half the size of these gaps.

## Claim 4: firewalls and the size claims

**Firewall detection on twisted tori is right. "None possible" is not.**

- Layer index: the period P_d of s = d·p on the quotient is the gcd of d·(2v) over all lattice vectors. For all 20
  tori it equals `tslab.periods`, and the review's partitions into transverse layers are identical to `tslab`'s.
  `ring_firewall` takes the layers in residue order 1, 3, …, P−1 cyclically, which is the T3 adjacency.
  Where the channel is open, the review's independent detector reproduces its rates: 3×8 ln τ_fw 12.054 against
  12.058 (on its 16-layer diagonal), 4×6 17.18 against 17.12–17.27, 4×5 17.15 against 17.15–17.19.
- With the review's own indexing and online detection, (4,1),(0,6) has 8 layers of 72 cells on one diagonal and 2 on
  the others. In 2.25 × 10¹⁰ life-generations it shows two firewalls, one of them a tie with a face death. Two adjacent
  dead layers appear at only 8 checks. On (4,4),(0,6) there are none in 1.5 × 10⁹. research/shape's 0 in 5,096 face
  deaths on (4,1),(0,6) is what this rate predicts (0.8 expected). The channel is present but about e^23.8; it is not
  undetected.
- The README table's "none possible" for (4,4),(0,6), (2,5),(0,12), (4,3),(0,6), (2,3),(0,12) and (4,1),(0,6) should
  read "none observed". Each of them has a diagonal with 4 or 8 layers, with cut 216–432. At A = 60, (4,2),(0,5) and
  (4,3),(0,5), with cut 180, did record 2 and 3 firewalls.
- "Twisting removes the transverse-firewall channel" is too broad. The twisted (6,1),(0,4) and (6,3),(0,4) keep cut 144
  and a 4.5–5.2% share, the same as 4×6. What closes the channel is a shortest row closure ≥ 6 (cut ≥ 216), not the
  twist. The weaker claim stands: the firewall-free tori (systole² 12, 13, 19, 21) and the firewall-prone systole-16
  tori lie on one line in σ (χ² 5.6 / 6).
- Capped lives: in `tslab.stats` a life that reaches the cap without settling ends at `gen_end` with no event, so its
  exposure is kept and it is not counted as a death. Settled lives end at min(settle, lc2), and face deaths that tie
  with a firewall go to the firewall. All of this is right. At A = 72, 70% of lives are capped. The review's renewal
  runs with the same cap reproduce 4×6, so the cap does no visible harm.

**The ratio "1.8 ± 0.3" depends on the points** (`recompute.py`):

| measure of the systole effect | A = 72 | A = 60 | ratio |
|---|---|---|---|
| 12 → 16, both systole-16 shapes pooled (README) | 0.096 ± 0.012 | 0.051 ± 0.005 | 1.87 ± 0.31 |
| 12 → 16, A = 60 shape 4×5 only | 0.096 ± 0.012 | 0.061 ± 0.006 | 1.58 ± 0.25 |
| 12 → 16, A = 60 shape (5,1),(0,4) only | 0.096 ± 0.012 | 0.042 ± 0.006 | 2.29 ± 0.43 |
| 13 → 16 | 0.051 ± 0.011 | 0.038 ± 0.007 | 1.34 ± 0.38 |
| slope of a line in σ over systole² 12–16 | 0.161 ± 0.020 | 0.096 ± 0.009 (χ² 22 / 3) | 1.68 ± 0.27 |

The effect is larger at A = 72 in every version, but the ratio is anywhere from 1.3 to 2.3. The README's pooled A = 60
group averages two shapes that differ by 4σ. State it as "larger at 72, by a factor 1.3–2.3 depending on the
comparison".

**"Systole 3 sits 0.21 below the trend" is robust.** Fitting a line in σ to every subset of three or more of the
systole² 12, 13, 16, 19, 21 shapes and extrapolating to σ = 3 gives gaps of 0.187–0.235 (± 0.015–0.031). A line in σ²
gives 0.222 ± 0.014. The review's run at systole² 9 (below) agrees. As the README says, this point is still confounded
with an 86% firewall share.

## Claim 5: face-death profile — stands

`prof.py` stores a ring buffer of both face layers in `ts.c` and, at each face death, records the dying face's population
over the 24 generations before its death generation. With 905, 917 and 1,066 deaths on 4×6, (4,1),(0,6) and
(4,4),(0,6), the mean live count is 37.0–37.4 down to −15. It is 36.9 at −13, 35.0–35.4 at −10, 32.6–33.2 at −8,
27.7–28.6 at −6, 17.8–19.5 at −4, 9.6–10.5 at −3, 3.9–4.1 at −2 and 1.7 at −1. The README's sequence (35, 33, 28, 19,
11, 4.3, 1.7) reproduces, and the three tori agree within 1.7 cells at every step. The −1 value is ≥ 1 by construction.
The collapse begins at about −13, a little earlier than "about 10".

## Corrections the write-up needs

1. README results tables: "none possible" → "none observed". The channel exists, with cut 216–432 on these tori. The
   review sees 2 firewalls on (4,1),(0,6) in 2.25 × 10¹⁰ life-generations (ln τ_fw ≈ 24). PREDICTIONS' "mostly closed"
   is the accurate phrase.
2. "Twisting removes the firewall channel" → "a shortest row closure ≥ 6 removes it". The twisted (6,1),(0,4) and
   (6,3),(0,4) keep 5% firewalls.
3. The grouping χ² 1.8 / 7 includes 3 symmetry-trivial degrees of freedom. Give 1.1 / 4 over distinct shapes as the
   test of "systole alone".
4. Systole² 21 at A = 72: an independent run gives 15.035 ± 0.009 against 15.066 ± 0.014. Report the combined
   15.043 ± 0.007 (+0.075 ± 0.010 over 4×6, both pooled), or say that the +0.093 is 1.9σ high against an independent run.
5. Ratio of the systole effect between areas: replace "1.8 ± 0.3" with "1.3–2.3 depending on the comparison". The
   pooled A = 60 systole-16 group is internally inconsistent.
6. Claim 2: add that an independent rerun with fixed seeds and no stopping rule gives 0.0177 ± 0.0042, and that the
   top-up alone gave 0.021 ± 0.005. "One more independent run should confirm" can be marked done.
7. Minor: the collapse starts about 13 generations before death, not 10.

## Not checked

- The "no band along the short loop" wave statistic of claim 5, and `rep_ring.c` / `faceend.py` themselves. Only the
  population profile was reproduced, with independent code.
- The A = 72 tori not rerun: (8,2),(0,3), (2,5),(0,12), the three (13,12,36) presentations, (6,1),(0,4), (6,3),(0,4)
  and (4,2),(0,6). 3×8, (4,4),(0,6) and (2,3),(0,12) had one run each, at ± 0.014–0.017. The other A = 60 tori,
  (4,2),(0,5), (4,3),(0,5) and (2,2),(0,10), were not rerun at all.
- `loopsum.py` and its χ² 36 / 10, and the "no three-parameter form fits" statement.
- Whether interior d0 firewalls matter. Neither code treats three dead interior layers as an event. The review counts
  them: about 1 per 900 face deaths at A = 60, and 1–7 in 13,000–14,000 face deaths at A = 72. They are too rare to
  move any rate here.
- Event detection was not validated against the engine. Only the stepping was. The detectors are checked by the
  agreement of face and firewall rates with research/shape and the GPU on 4×5 and 4×6.
- The elevated χ² of the review's 4×6 hazard thirds.
