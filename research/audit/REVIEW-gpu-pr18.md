# Review of GPU pull request 18: empty patches on a large living face

Adversarial review, 2026-11-14. Object: branch `origin/claude/awesome-cray-boq9vz`, commits 312b0bc (forecast),
d6a5e71 (history record, tree unchanged), 70482e0 (code), fcb3f39 (data, README, outcome): `research/gpu/patches.py`,
`modal_app.py`, `jobs.py`, `research/data/gpu_patches/patches_s81{1,2,3}_A10G.{csv,json}`, the README section "Empty
patches on a large living face" and the `PREDICTIONS.md` entries 2026-11-14T21:25Z and 21:47Z. The GPU code was read,
not run. Scripts: `research/audit/gpu_pr18/` (bulk output in `research/scratch/pr18/`, git-ignored).

    python3 research/audit/gpu_pr18/engine_check.py      # pc.c stepper vs the engine (3 seeds, T = 1, 7, 300, 1000)
    python3 research/audit/gpu_pr18/brute_check.py       # pc.c patch counts vs a numpy count from the cell sets
    research/audit/gpu_pr18/runs.sh                      # CPU ensemble, 1 core, ~65 min (2 x 512 replicas x 3e6 gens)
    python3 research/audit/gpu_pr18/compare.py research/scratch/pr18/run_s9*.tsv -- research/data/gpu_patches/patches_s81*_A10G.csv
    python3 research/audit/gpu_pr18/recompute.py research/data/gpu_patches/patches_s81*_A10G.csv

## Summary

| claim | verdict |
|---|---|
| 1. The table of ln P(empty) and its errors | **stands.** Recomputed from the CSVs to every printed digit (and the lead's check agrees with mine). An independent CPU stepper and counter, 3.07 × 10⁹ replica-generations, reproduces it within errors from 1×1 to 4×4, the strips and the balls (|z| ≤ 1.9). The exception is 4×5, which comes out 2.6σ low on the CPU (43 hits). The 96 batches are independent enough for batch means. One definition is not stated: the two faces carry the two inequivalent orientations of each rhombus and strip, and the table averages them. |
| 2. The area-plus-perimeter form fails; the cost per cell is 0.32–0.42 and lies "well above" 0.205–0.221 | **the fit failure stands; the comparison does not.** c = 0.264, σ = 0.119, χ² 3,369 / 3 reproduce. But 0.32–0.42 is the *incremental* cost, and it includes the added perimeter. A dying face is periodic and has no perimeter, so it should be compared with the perimeter-free part. Second differences (post hoc) give 0.273, 0.252, 0.237, 0.219 ± 0.008, which is already inside the lifetime range at the largest size. The limit is not decided: defensible extrapolations give 0.16–0.24. |
| 3. Shape matters (1×12 vs 3×4: e^−4.5); persistence falls with size | **stands.** −4.481 reproduces. Persistence falls in both orientation classes separately. |
| 4. Forecasts before code and data; scoring | **stands.** 312b0bc (21:25:31) touches only `PREDICTIONS.md`. Then come d6a5e71 (no tree change), code 70482e0 (21:29:19), the runs (start 21:31:33Z per JSON) and data fcb3f39 (21:47:45). The forecast text is unchanged since 312b0bc. The scoring is honest, but the "missed" for the lead's band needs the qualifier in fix 4. |

**Recommendation: merge after fixes** (the text fixes below; no data or code change needed). One request is not text:
state whether `check_patches` was re-run on the committed kernel (fix 7).

## (a) Independent check of the counts

**Own code** (`gpu_pr18/geom18.py`, `pc.c`; no code shared with `research/gpu/` or `research/peeling/geom.py`). The
slab is the engine's own vessel: the 12-cube torus with the 8 d0 layers t = o … o+7. Here a cell p = 2c + e_a has layer
t = (c_x + c_y + c_z) mod 12. The 4 remaining layers start dead and stay dead (T3), and serve as a dead sentinel. The
stepper is bit-sliced over 64 replicas per word. `engine_check.py` compares it with `gump run --torus 12 --soup 0.4
--slab-layers 8 --diag 0 --rng 3|4|5` from the engine's own initial state, and the two are **identical at T = 1, 7, 300 and 1,000** for all
three seeds. `brute_check.py` checks the DAG of OR-nodes that counts patches against a numpy count from explicit cell
sets, on 64 replicas × 30 generations, and all 90 groups are **identical** (383,243 empty patches; samples, hits and
hits at t and t+1).

**Definitions.** In face layer t, cube positions (i, j) mod 12 index the in-layer triangular lattice. Each (i, j)
carries two kagome triangles:
- *up* U(i, j): the 3 +faces of cube (i, j, t−i−j);
- *down* D(i, j): the 3 −faces of cube (i, j, t+1−i−j).

A rhombus a × b is the union of K(i0+x, j0+y) for 0 ≤ x < a and 0 ≤ y < b, with K = U or D. A strip 1 × b is a rhombus
1 × b. A ball of radius r is the set of cells within graph distance r of a centre cell in the 6-neighbour in-layer graph
(the 4 kagome neighbours and the 2 coplanar neighbours across the hexagon). There are 144 translates per face, or 432
centres for balls. `patches.py` takes **U on both faces**: `v.key[(i, j, t, a)]` is the +a face of cube (i, j, t−i−j).
My "PR definition" column below uses the same.

**A finding of definition.** The two faces of the slab are swapped by inversion p → −p, and inversion maps U to D.
Every element of O_h that maps d0 to −d0 does the same: it is inversion times a permutation of the axes. So
U-patches on face 0 are equivalent in law to D-patches on face 1, and not to U-patches on face 1. On face 0 a U
triangle belongs to a cube that lies outside the slab (its other three faces are in the dead layer). On face 1 it
belongs to a cube inside the slab. The PR's pooled value is therefore the average of two inequivalent shapes:

- class **O** ("outer cube") = f0-U + f1-D;
- class **I** ("inner cube") = f0-D + f1-U.

The symmetry check passes. f0-U agrees with f1-D, and f0-D with f1-U, with |z| ≤ 2.3 and no trend. The classes differ
at every size, and the difference grows with the perimeter, at about 0.007 per perimeter pair:

| shape | PR ln P | mine (PR definition) | z | class O | class I | O − I | O − I per perimeter pair |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1×1 | −2.0174 | −2.0174 | −0.2 | −2.0652 | −1.9718 | −0.093 | 0.0077 |
| 2×2 | −6.2542 | −6.2541 ± 0.0000 | 0.8 | −6.3585 | −6.1597 | −0.199 | 0.0071 |
| 2×3 | −8.7927 | −8.7927 ± 0.0001 | −0.1 | −8.9256 | −8.6755 | −0.250 | 0.0069 |
| 3×3 | −12.1284 ± 0.0002 | −12.1280 ± 0.0007 | 0.6 | −12.2952 | −11.9852 | −0.310 ± 0.001 | 0.0070 |
| 3×4 | −15.3999 ± 0.0011 | −15.3936 ± 0.0030 | 1.9 | −15.6015 | −15.2263 | −0.375 ± 0.005 | 0.0072 |
| 4×4 | −19.4233 ± 0.0071 | −19.4194 ± 0.0223 | 0.2 | −19.702 | −19.224 | −0.478 ± 0.033 | 0.0080 |
| 4×5 | −23.318 ± 0.047 | −23.747 ± 0.159 (43 hits) | **−2.6** | −23.90 | −23.35 | −0.55 ± 0.22 | |
| strip 1×6 | −10.4052 | −10.4052 ± 0.0003 | −0.1 | −10.5814 | −10.2552 | −0.326 | 0.0063 |
| strip 1×9 | −15.3901 | −15.3930 ± 0.0032 | −0.9 | −15.656 | −15.186 | −0.469 | 0.0062 |
| strip 1×11 | −18.672 ± 0.010 | −18.685 ± 0.028 | −0.4 | −19.000 | −18.454 | −0.55 ± 0.04 | 0.0059 |
| strip 1×12 (wraps) | −19.881 ± 0.028 | −19.882 ± 0.082 | 0.0 | −20.13 | −19.69 | −0.44 ± 0.12 | |
| ball r=1 / 2 / 3 | −4.2175 / −11.5711 / −22.094 | −4.2175 / −11.5707 / −22.060 ± 0.044 | −0.2 / 1.1 / 0.7 | — | — | — | |

All strips 1×1 … 1×12 agree within 1.8σ; the full output is in `research/scratch/pr18/compare.out`. Persistence agrees
to the third digit wherever there are more than 10⁵ hits. **Caveat on my errors:** the two CPU runs (seeds 901 and 902)
differ by an rms of 1.4σ of their own batch-means errors (3×3: 2.9σ), so my errors are probably about 1.4× too small.
With that factor the 4×5 tension is 1.9σ. I do not know its cause. It is 43 hits against 66 expected from the PR's
value. It touches only the last second difference: from my data, 2×3 → 3×4 → 4×5 gives 0.29 ± 0.03 against the PR's
0.2185 ± 0.008.

What the classes do to the reading: O − I is a boundary term (it is linear in the perimeter), so it does **not** move the
perimeter-free cost. The second differences per class are O 0.2739 / I 0.2729 / pooled 0.2728 (1×1, 2×2, 3×3) and
0.2534 / 0.2502 / 0.2506 (1×2, 2×3, 3×4). The I class also persists longer (4×4: O 0.090, I 0.121). The finding is
interesting in its own right: the edge of an empty patch costs about 0.007 more per edge pair when its edge triangles
belong to the cubes that face the outside of the slab.

**Perimeters** were counted directly from my own in-layer graph, in both classes and on both faces. They are
rhombi 8(a+b) − 4, strips 8b + 4 except the wrapped 1×12 at 96, and balls 26, 50, 86, all as in the PR.

## (b) Errors

`recompute.py` (own code) reproduces every number in the README table and in the outcome entry: ln P, the errors (bm
or the Poisson floor), the persistences, the fit (c = 0.2641, σ = 0.1192, χ² 3,369.2 / 3), the increments and
e^−4.481. The lead's `gpu_pr18_lead_check.py` gives the same numbers.

Are the batches independent? Batches are 68,750 generations long; persistence at the sizes that carry the error is
≤ 0.18 per generation.
- The lag-1 autocorrelation of consecutive batch fractions within a seed, averaged over the 17 shapes with more than
  10⁶ hits, is **−0.023**. For independent batches the expected value is −1/32 = −0.031, with a spread of about 0.10
  per shape.
- Merging batches by 2, 4 or 8 leaves the batch-means error unchanged (3×4: 0.0011, 0.0012, 0.0010, 0.0011; 4×4:
  0.0071, 0.0071, 0.0069, 0.0063).
- Across the three seeds, χ² on 2 dof averages 1.6.

So the batch means are sound. The correlations between faces, translates and shapes inside a replica are absorbed
correctly. One thing is not absorbed: errors of *different shapes* are correlated, because they come from the same
states, so the fit's χ² overstates the significance somewhat. At χ² = 3,369 that changes nothing.

## (c) The reading: the cost per cell of a large empty patch

**The second-difference estimator.** For a×a, n = 3a² and P = 16a − 4. For a×(a+1), n = 3a² + 3a and P = 16a + 4.
In both families Δ²n = 6 and Δ²P = 0. The estimator removes the constant and every term that is linear in the side, and
that covers:
- the perimeter, whatever its coefficient;
- the anisotropy of the lattice: the rhombus has edges of two lattice directions, and opposite edges are inequivalent,
  because the face layer has only C3v and no in-plane inversion, but every edge length is linear in a or b;
- the four corners (2 × 60°, 2 × 120°), which are a constant;
- the O/I mixture, which shifts the estimate by less than 0.004 as measured above.

It does **not** remove corrections that are nonlinear in the side (a ln n term, 1/a, corner-edge interactions).
Those are exactly what decides the limit. The values are 0.273 (middle shape 12 cells), 0.252 (18), 0.237 (27) and
0.2185 ± 0.008 (36). If they decrease monotonically, c(∞) ≤ 0.235 (2σ). Their decline does not tell where they stop:

| form (rhombi 2×2 … 4×5 unless stated) | c | χ² / dof |
|---|---:|---:|
| k − c n − σP (the PR's) | 0.264 | 3,369 / 3 |
| same, from 18 cells / from 27 cells | 0.211 / 0.249 | 2,822 / 2, 6.8 / 1 |
| k − c n − σP − λ ln n | 0.266 (from 18 cells: 0.249) | 50 / 2 (3.6 / 1) |
| k − c n − σP − s√n | 0.240 (from 18 cells: 0.232) | 16 / 2 (2.7 / 1) |
| k − c n − s√n (perimeter ∝ √n) | 0.152 | 48,127 / 3 |
| k − c n − s√n − λ ln n, or − u/√n | 0.66, 0.52 (from 18 cells: −0.25, −0.09) | ~3,000 / 2 |
| second differences vs 1/n(middle), extrapolated | 0.209 ± 0.001 | 2.6 / 2 |
| second differences vs 1/√n, extrapolated | 0.158 ± 0.001 | 4.5 / 2 |

Every form that fits acceptably gives c between 0.16 and 0.25. The forms without a perimeter term fail, because P and
√n differ between the two families (P jumps by 8 from a×a to a×(a+1), while √n gains only half a step). The prescribed
fit's own c moves between 0.21 and 0.26 as its range changes, so 0.264 is not a measured quantity.

**Strips.** The cost is flat at 0.556 per cell (linear fit, b = 4…11, slope 0.5564 per cell), drifting slowly from
0.564 to 0.552. Read as a pure-perimeter object, a strip adds per unit cell 3 cells and 8 perimeter pairs, so
3c + 8σ = 1.669. That gives σ = 0.130 with c = 0.21, or 0.110 with the fit's c = 0.264. Both are close to the rhombus
fit's σ = 0.119, but one equation cannot separate c from σ. The constraint for c needs σ: c = 0.552 − 2.667σ, and
σ = 0.09–0.13 gives c = 0.20–0.31. A one-triangle-wide strip has its two edges in contact, so this is the weakest of
the readings.

**The wrapped strip as the end cost.** The 1×12 wrapped strip, at −19.881 ± 0.028, lies 0.45 (quadratic trend) to 0.54
(linear trend) above the unwrapped extrapolation, −20.33 to −20.42. Closing the ring removes 4 perimeter pairs, and at
σ ≈ 0.11–0.13 that is worth 0.45–0.54. The end cost is therefore fully accounted for by the removed perimeter pairs,
which supports reading a periodic object's cost as area plus edge, with no extra end or corner term of note.

**What the data can and cannot say.** The comparison with the lifetime laws must use a perimeter-free cost, because a
dying face is periodic in both directions and has no in-plane edge. That cost is measured directly at 0.237 ± 0.001
(27 cells) and 0.2185 ± 0.008 (36 cells). It is still falling, and at the largest size it is already inside
0.205–0.221. The data **cannot** say whether it settles at 0.21: the defensible extrapolations span 0.16–0.24, the 4×5
point that carries the last value is in mild tension with my CPU run, and patch sizes stay below 60 cells, against
A ≥ 100 for the faces whose lifetimes define 0.21. The data **can** say that nothing here contradicts the static
picture. My honest range for the asymptotic bulk cost per cell is **0.16–0.24**. The lifetime range lies inside it,
nearer the upper end.

## (d) Text fixes (numbered, as replacement sentences)

1. README, Set-up: replace "rhombi a×b unit cells (3ab cells; a unit cell = the 3 face-layer cells of one cube)" by
   "rhombi a×b unit cells (3ab cells; a unit cell = the three +faces of one cube (i, j, t − i − j) of face layer t — on
   face 0 that cube lies outside the slab, on face 1 inside, so the two faces carry the two inequivalent orientations
   of each rhombus and strip, related by the inversion that swaps the faces, and the table gives their average; the
   review's CPU run finds the inner-cube orientation more often empty, by 0.20 in ln P at 2×2 and 0.48 at 4×4, about
   0.007 per perimeter pair, with no effect on the second differences)".
2. README, "What this does and does not say": replace "Over 12–60 cells an empty patch costs 0.32–0.42 per cell, well
   above every lifetime law's 0.205–0.221, and the cost is still falling." by "Over 12–60 cells the incremental cost of
   enlarging an empty rhombus falls from 0.42 to 0.325 per cell; this includes the added perimeter, which a dying
   (periodic) face does not pay, so it is not comparable with the lifetime laws' 0.205–0.221. With the perimeter
   removed (second differences along a×a and a×(a+1), a post hoc reading) the cost per cell is 0.273, 0.252, 0.237,
   0.219 ± 0.008 at middle shapes of 12, 18, 27, 36 cells: still falling, and at the largest size already inside the
   lifetime range."
3. README, same item: replace "Whether it falls to ≈ 0.21 for patches the size of a dying face (A ≥ 100) is not
   reached: the 6×6 rhombus extrapolates to ln P ≈ −37, about 10¹³ times rarer than the 4×5." by "Whether it settles
   at ≈ 0.21 for patches the size of a dying face (A ≥ 100) is not reached: extrapolating the second differences gives
   0.21 (corrections ∝ 1/n) or 0.16 (∝ 1/√n), and both fit; the 6×6 rhombus extrapolates to ln P ≈ −37 to −39, about
   10⁶–10⁷ times rarer than the 4×5 (≈ 10⁻³ expected hits in this run)." (The 10¹³ is an arithmetic slip:
   e^(37 − 23.3) = e^13.7 ≈ 9 × 10⁵.)
4. README, same item: replace "The lead's acceptance band (c in 0.17–0.25) is missed, but by a fit that does not
   describe the data, so this is a failure of the linear form over this range, not a measured asymptote." by "By the
   forecast's own rule the lead's band (c in 0.17–0.25) is missed (the prescribed fit gives 0.264), but that fit does
   not describe the data (χ² 3,369 / 3, and its c moves to 0.211 or 0.249 when the smallest shapes are dropped), so the
   miss is a failure of the linear form, not evidence against the static picture: the perimeter-free cost per cell is
   compatible with 0.21 and does not establish it (defensible extrapolations give 0.16–0.24)."
5. PREDICTIONS.md, 21:47Z entry: replace "What is shown: over 12–60 cells an empty patch costs 0.32–0.42 per cell, well
   above the lifetime laws' 0.205–0.221, and still decreasing; whether it decreases to ≈ 0.21 at larger patches is not
   reached." by "What is shown: the incremental cost (area and added perimeter together) falls from 0.42 to 0.325 per
   cell over 12–60 cells; its perimeter-free part (second differences, post hoc) falls from 0.273 to 0.219 ± 0.008 and
   at the largest sizes lies within the lifetime laws' 0.205–0.221; whether it settles there is not reached."
6. PREDICTIONS.md, same entry: replace "the cost per cell is still falling at 60 cells (0.325) and has not approached
   any asymptote." by "the incremental cost per cell, perimeter included, is still falling at 60 cells (0.325)."
7. README, Acceptance: after "… item by item." add "The check was run at commit 70482e0; fcb3f39 then changed the
   kernel's thread-to-(item, word) mapping and the matching reshape in `totals` — `check_patches` [was / was not]
   re-run on the committed kernel; the review's independent CPU count agrees with the table." (The change is
   consistent as read: `idx = w·nitems + item`, and `totals` reshapes to (WT, nitems). The CPU agreement confirms the
   counts in any case.)
8. README, Not checked: replace "independence of the two faces and of overlapping translates (they are correlated,
   which the batch-means errors absorb only as far as batches are independent)" by "the two faces and overlapping
   translates are correlated; the batch-means errors absorb this, since consecutive batches are uncorrelated (lag-1
   autocorrelation −0.02, against −0.03 expected for independent batches; errors unchanged when batches are merged by
   2, 4 or 8; the three seeds agree), but errors of different shapes are correlated, so the fit's χ² is somewhat
   overstated".

## Not checked

- The GPU code was read, not run. kernel B against the engine on this slab, the GPU firewall test and the masking were
  not exercised. No replica froze or was dropped, so the masking never acted. I also did not run a firewall test in my
  CPU runs. Faces and settling were checked (none).
- The cause of the 4×5 tension: CPU 43 hits against about 66 expected. It is 2.6σ with my errors, 1.9σ with them
  scaled by the run-to-run factor 1.4.
- Why my CPU batch-means errors look about 1.4× too small with 512 replicas. The GPU's own seed-to-seed scatter is
  normal.
- Patch sizes beyond 4×4 at useful precision. I did not try a biased or splitting estimator.
- Dependence on the slab's thickness, the soup density, or the face size: whether a 12×12 face's patch statistics
  match those of the faces of the small dying slabs.
- Emptiness in layers below the face. Balls by class (balls have no orientation class, so there is none to check).


## Follow-up 2026-11-14: the 4×5 point (plan, committed before the run)

The lead asked for this follow-up after the review, because the perimeter-free estimate 0.2185 ± 0.008 (2×3 → 3×4 → 4×5)
rests on the 4×5 point, where the CPU run above and the GPU table differ by 1.9–2.6σ.

**Plan, fixed before any of these runs.** The code is the same `pc.c` with the same geometry. The program is `geom18.py`'s
`lean` variant, with rhombi 1×1 … 4×5 only. I checked that it gives counts identical to the full program on a test run.
`pc.c` now has a hit log (`-e`/`-E`); it does not change the counts.
- `research/audit/gpu_pr18/runs2.sh`: 16 chunks with fresh seeds 921–936. Each chunk is 512 replicas × 3 × 10⁶
  generations after 2,000 burn-in generations, with 30 batches, so 2.46 × 10¹⁰ replica-generations in all.
- Expected 4×5 hits (both classes, PR definition): about 350 at the first CPU run's rate and about 530 at the GPU's.
  With the first run's 43 that is about 400–570. All 16 chunks are run whatever the counts, so there is no optional
  stopping.
- Reported: ln P for 3×4, 4×4 and 4×5 from the CPU alone. This uses the two first runs plus the 16 chunks, 18 runs in
  all, with (i) batch-means errors and (ii) the run-to-run scatter, sd/√18.
- Also reported: the second differences along a×a and a×(a+1) from CPU-only values, and z against the GPU table.
- Clustering, from the hit logs of 3×4, 4×4 and 4×5. An *event* is a connected component of hits, where two hits are
  linked if they have the same replica and face, generations at most 1 apart, and patches (either orientation) that
  share a cell. I report hits per event (mean, and the ratio Σsize²/Σsize) and the compound-Poisson error
  √(Σsize²)/Σsize beside the batch-means error.
