# Review of GPU pull request 16: does the width of a periodic face change its lifetime at fixed area?

Adversarial review, 2026-11-14. Object: branch `origin/claude/awesome-cray-boq9vz`, commits 5cd9a83, 4f13f25, 42527e0,
0f14c27 on top of main: `research/gpu/fwslab.py`, `modal_app.py`, the new `width.py`, eleven new
`research/data/gpu_facelaw/fwslab*.json`, and text in `research/gpu/README.md` and `PREDICTIONS.md`.
Scripts are in `research/audit/gpu_pr16/`. Each one takes the directory that holds the PR's JSON files. Here that is a
detached worktree of the branch at `research/scratch/pr16/wt` (git-ignored):

    git worktree add --detach research/scratch/pr16/wt origin/claude/awesome-cray-boq9vz
    D=research/scratch/pr16/wt/research/data/gpu_facelaw
    python3 research/audit/gpu_pr16/recompute.py $D     # table, differences, fits, totals, hazard by age
    python3 research/audit/gpu_pr16/fits.py $D          # fits on subsets, alternative models, b(s) tests
    python3 research/audit/gpu_pr16/raw_checks.py $D    # per-life checks where raw exists
    research/audit/gpu_pr16/cpu_runs.sh; research/audit/gpu_pr16/cpu_runs_more.sh; research/audit/gpu_pr16/cpu_runs_4x6.sh   # CPU runs, 2 cores, ~40 min
    python3 research/audit/gpu_pr16/compare.py $D       # CPU against the GPU and the CPU table

## Summary

| claim | verdict |
|---|---|
| 1. At fixed area a narrower face dies sooner | **stands.** Every number reproduces. An independent CPU run gives 3×8×8 − 4×6×8 = −0.344 ± 0.020 against the GPU's −0.349 ± 0.004. Two of the three differences need their errors stated. |
| 2. The cost per cell depends on width; b(s) = 0.1959, 0.2072, 0.2082, 0.213; χ² 30,944 / 3,595 / 85 | **stands with a correction.** The numbers reproduce. The width-dependent slope rests on s = 3 alone. For s ≥ 4 a single cost per cell, 0.2072, with an intercept that rises with s fits (χ² 8.4 / 8). b(4) and b(5) do not differ (1.6σ). All of the χ² of 85 comes from the curvature of the s = 3 family. |
| 3. Orientation and burn-in controls | **stands with a correction.** Both reproduce. The burn-in cut is vacuous in 5 of the 12 slabs with histograms (no face death occurs below age 10³). The test that can bite is the hazard by decade of age, and that hazard is flat from about 200 generations on in every slab. |
| 4. Conjecture: wide faces cost 0.216–0.221 per cell, and 0.2088 is an average over narrow slabs | **does not stand.** b(5) = 0.2082 ± 0.0006 is 13σ below 0.216. b(4…6) agree on 0.2072 (χ² 3.5 / 2). The A-only slope over s ≥ 4 is 0.2085, which is *above* every family's own slope: the old line's 0.2088 is inflated by the width offsets, not dragged down by narrow slabs. The forecast was honestly reported as a miss. |

## Claim 1: at fixed area a narrower periodic face dies sooner — stands

**Recomputed from the JSON** (`recompute.py`). Exposure, face deaths, firewalls and ln τ_face = ln(2E/F) ± 1/√F match the
README table to every printed digit, for the 14 slabs in it and for 6×4×8. The one exception is a local slope
(claim 2). The hist totals (exposure, kinds 1–4) equal the summary fields in
every new file. `raw`, where present, sums to the exposure and reproduces every count.

| pair | A | GPU | firewall shares |
|---|---:|---|---|
| 4×9×8 − 6×6×8 | 108 | −0.196 ± 0.059 | 99.2% / 2.1% |
| 3×8×8 − 4×6×8 | 72 | −0.349 ± 0.004 (against 6×4×8: −0.351 ± 0.004) | 86.6% / 5.0% |
| 3×10×8 − 5×6×8 | 90 | −0.740 ± 0.016 | 99.6% / 1.7% |

**Independent CPU check at A = 72.** The CPU run uses the `rep.c` stepper through `research/audit/gpu_pr14/cpu_channels.py`.
`validate` re-checks the stepper on each slab against the engine, every generation, with the slab tiled into a 24-torus
(3×8×8) or a 12-torus (4×6×8): MATCH, and the graph equals AUTOMATON.md's offsets. Each replica lives one life from a
p = 0.4 soup. The run records face-layer death times and the first T3 firewall per transverse diagonal, at a resolution
of 16 generations, with caps of 5 × 10⁵ (3×8×8) and 2 × 10⁶ (4×6×8). "(T)" is the channel-resolved truth. "(G)" applies
`fwslab.py`'s detection rules at the GPU's launch cap.

| slab | lives (runs) | face / firewall | CPU (T) ln τ_face | CPU (G) | GPU | GPU − CPU (G) | CPU table |
|---|---|---|---|---|---|---|---|
| 3×8×8, K = 2¹¹ | 25,600 (40) | 3,315 / 21,413 (86.6%) | 14.611 ± 0.017 | 14.617 | 14.621 ± 0.003 | +0.005 ± 0.018 | 14.64 ± 0.12 |
| 4×6×8, K = 2¹⁶ | 16,000 (50) | 11,232 / 592 (5.0%) | 14.955 ± 0.009 | 14.956 | 14.970 ± 0.002 | +0.014 ± 0.010 | 14.89 ± 0.05 |
| 3×6×8, K = 2¹¹ (PR 14 histories) | 25,088 (7) | 21,896 / 3,188 | 11.076 ± 0.007 | 11.079 | 11.081 ± 0.001 (s711) | +0.002 ± 0.007 | 11.10 ± 0.05 |
| **3×8×8 − 4×6×8** | | | **−0.344 ± 0.020** | −0.339 | **−0.349 ± 0.004** | | −0.25 ± 0.13 |

The firewall channels agree too: CPU 12.052 ± 0.007 against GPU 12.063 at 3×8×8, and 17.205 ± 0.041 against 17.227 at
4×6×8. The face hazard in equal-exposure age thirds is flat on the CPU as well: 14.63, 14.58, 14.63 (± 0.03) at 3×8×8 and
14.94, 14.97, 14.96 (± 0.016) at 4×6×8.

The 4×6×8 run was extended once, because of the data: after 25 runs GPU − CPU stood at +0.033 ± 0.013 (2.5σ). A third
batch of 25 (`cpu_runs_4x6.sh`) gave 14.973 by itself, and the 50-run value above is 1.4σ. Read it as agreement, with
the GPU at most about 0.03 high at s = 4.

The width effect at A = 72 is reproduced by code that shares nothing with the GPU path except the rule.

**Detection-time bias under the new launch caps.** The bias is the exposure counted between a firewall's formation and
its detection.
- **s = 3, K = 2¹¹.** It adds +0.003 at 3×6×8 (the PR 14 histories re-analysed at K = 2048; it was +0.006 at 2¹⁸) and
  +0.006 at 3×8×8 (G − T above). The GPU's own two 3×6×8 runs differ by 11.084 − 11.081 = +0.003 ± 0.001 between caps
  2¹⁸ and 2¹¹, as predicted.
- **s = 4, K = 2¹⁶.** At most +0.0015 at 4×9×8 and +0.0013 at 4×8×8 (`raw_checks.py`: 68,307 of 69,124 and 26,879 of
  28,656 firewall lives end at a launch boundary; K/2 each).
- **The old 4×7×8 run, K = 2¹⁸.** Up to +0.005, which is most of its +0.006 residual in the s = 4 family.
- **Effect on the claim.** All of these push the narrow slabs *up*, so correcting them would widen the differences. They
  are 1–2 orders of magnitude below the effect.

**What the comparison is.** The quantity measured is the face hazard of lives that have no firewall yet. At 4×9×8 and
3×10×8 nearly every life ends in a firewall. The pair at A = 108 therefore compares 99.2% against 2.1% firewall shares,
and the design makes width and firewall-proneness the same variable (cheapest cut 36·s). See claim 3 for what the data
say about that.

**Errors not given.** The README and PREDICTIONS print the differences at A = 72 and A = 90 without errors (fix 1).

## Claim 2: the cost per cell depends on width — stands with a correction

**Reproduced exactly.** The χ² values for the three models:
- A: 30,944.4 / 13;
- O: 3,595.4 / 10;
- W: 85.2 / 7.

The family slopes, with the errors the text leaves out:
- b(3) = 0.1959 ± 0.0001;
- b(4) = 0.2072 ± 0.0001;
- b(5) = 0.2082 ± 0.0006;
- b(6) = 0.2131 ± 0.0062 (two points, an exact line).

The degrees of freedom are right. There are 15 points: 6×4×8 enters as its own point in the s = 4 family.

**Where the χ² of 85 lives.**
- The s = 3 family has 3 points and 1 dof, and contributes 80.3. 3×10×8 sits at −8.0σ and 3×8×8 at +4.1σ. The family is
  curved: a quadratic term of −1.8 × 10⁻⁴ ± 2.0 × 10⁻⁵ is 9σ, and the local slopes are 0.1966 then 0.1902. b(3) is a chord
  through a curve, not a cost per cell.
- s = 4 contributes 4.6 / 4, s = 5 contributes 0.3 / 2, and s = 6 contributes nothing (0 dof).
- The two s = 6 points play no part in the misfit.

**s = 4 → 5 → 6 is not established** (`fits.py`).
- b(5) − b(4) = +0.0010 ± 0.0006 (1.6σ), b(6) − b(4) = +0.0059 ± 0.0062 (1.0σ), b(6) − b(5) = 0.8σ.
- On the 12 points with s ≥ 4:

  | model | χ² / dof |
  |---|---|
  | A | 512 / 10 |
  | **O, one slope 0.2072 ± 0.0001 with a(4) = 0.053, a(5) = 0.121, a(6) = 0.203** | **8.4 / 8** |
  | W | 4.9 / 6 |

- W improves on O by Δχ² = 3.5 for 2 more parameters, which is nothing.
- By the design's own rule, which was committed before the runs ("slopes b(s) differing by more than 3σ favours W"),
  s ≥ 4 is reading **O**. Only s = 3 against the rest is reading W.
- So the defensible statement has two parts. First, the width enters as an *offset*, about +0.07 per unit of short side
  at fixed area for s = 4–6. Second, the width-3 family is separately cheaper per cell and curved.

**The long side.** Within a family A = 3sM, so a dependence on M cannot be told apart from a dependence on A.
- Across families, a + bA + cM fits s ≥ 4 as well as O does: χ² 5.6 / 9, b = 0.2117, c = −0.054 per unit of the long
  side.
- Adding a separate s term gives d = −0.005 ± 0.042.
- Over all 15 points it fails (184.8 / 11), again because of s = 3.

The data do not decide between "an offset in s" and "a deficit per unit of the long side" for s ≥ 4. The text should
not single out width as the variable (fix 2).

**"Only the narrowest faces (width 3, and perhaps 4) get cheaper per cell as they lengthen."** The width-3 part is true
(9σ). The "perhaps 4" has no support: the s = 4 quadratic term is +4.7 × 10⁻⁶ ± 1.4 × 10⁻⁵, and the last local slope,
0.2025 ± 0.0038, is 1.2σ low.

A small point: the table's first s = 4 local slope, 0.2072, uses 6×4×8. With 4×6×8 it is 0.2070.

## Claim 3: the controls — stands with a correction

**Orientation.** 4×6×8 − 6×4×8 = −0.002 ± 0.003 reproduces, and so do the firewall rates (17.227 and 17.227). This checks
the code's symmetry, not the physics of width.

**Burn-in.** The ≥ 10³ and ≥ 10⁴ cuts reproduce: no slab moves by more than 0.002. Where most deaths are old the cut
tests nothing, though. In 4×8×8, 4×9×8, 5×6×8, 5×7×8 and 5×8×8, at most 3 face deaths occur below age 10⁴ and none below 10³.
(The old 6×6×8 and 6×7×8 runs have no histograms, and the PR's check skips them.) The informative test is the face hazard by decade of age (`recompute.py`, last block).

| slab | [0, 200) | [200, 10³) | [10³, 10⁴) | [10⁴, 10⁵) | [10⁵, 10⁶) | exposure ≥ 10³ |
|---|---|---|---|---|---|---:|
| 3×6×8 | 10.970 ± 0.006 | 11.083 ± 0.003 | 11.082 ± 0.001 | 11.082 ± 0.001 | 11.083 ± 0.003 | 96.5% |
| 3×8×8 | 14.20 ± 0.07 | 14.59 ± 0.04 | 14.621 ± 0.012 | 14.623 ± 0.005 | 14.622 ± 0.004 | 99.4% |
| 3×10×8 | 17.3 ± 0.2 | 18.2 ± 0.2 | 18.060 ± 0.046 | 18.041 ± 0.017 | 18.049 ± 0.016 | 99.3% |
| 4×5×8 | 12.29 ± 0.02 | 12.492 ± 0.012 | 12.487 ± 0.004 | 12.487 ± 0.001 | 12.486 ± 0.001 | 99.2% |

**How to read the table.**
- **Early lives.** The hazard is higher in the first 200 generations by 0.1–0.7 nats, but that bin holds at most 0.7% of
  the exposure (a shift of ≤ 0.001).
- **After that.** From 200 generations on the hazard is flat to the per-bin errors in every slab. In 3×8×8 and 3×10×8
  this holds over three decades, and lives there end at a mean of 1.4–1.5 × 10⁵ generations.
- **For slabs with per-life data** (`raw_checks.py`), the hazard in equal-exposure age thirds is also flat. For example,
  4×9×8 gives 22.36, 22.35, 22.41 (± 0.07) and 4×8×8 gives 19.95, 19.95, 19.92 (± 0.03).
- **Relaxation.** The p = 0.4 soup has relaxed to the face channel's quasi-stationary state long before exposure
  accumulates. The face rate is not a young-life rate in the sense of a transient.

**Competing risks.** What is identified is the face hazard of the population that has no firewall yet. That needs no
independence assumption. "Independent" only matters for a counterfactual (the face rate if firewalls could not form),
which the design cannot reach and the claim does not need. The live question is whether near-firewall states inside
that population raise the face hazard, so that "narrow" partly means "firewall-prone". What the data say:
- **Against it, in s = 4.** The firewall share runs 0.5% → 5% → 42% → 91% → 99% along the family and the line holds
  (χ² 4.6 / 4). 4×8×8 sits at 90.7% and −0.1σ.
- **Possibly for it, in s = 3.** The most firewall-dominated slab, 3×10×8 (99.6%), is the −8σ point of the s = 3 curve,
  and 4×9×8 (99.2%) is −1.4σ.
- **Not decided.** The data cannot separate long-side curvature from firewall proximity in s = 3, because the per-life
  data were dropped in every s = 3 slab (see below).

**The 150,000 cap on `raw`.** It does not truncate: `raw` is written whole or not at all (`if len(a) <= raw_cap`).
- The summary fields and histograms are always complete, and there is no prefix bias.
- But `raw` is missing exactly where the competing-risk questions are sharpest: all three s = 3 slabs, 4×5×8, 4×6×8 and
  6×4×8.
- The per-life analyses here exist only for 4×8×8, 4×9×8, s = 5, 6×6×8 and 6×7×8.

**The code path for firewall-then-face within one launch.**
- A face death on a firewalled kept state (`K_KEEP`) is relabelled kind 4 at the death's generation, so it is never
  counted as a face death. A face death before the firewall is a face death.
- The residual biases are the detection exposure (claim 1) and settle-after-firewall lives censored as settled (PR 14
  review: ≤ 0.9% of firewall lives at 3×6×8, fewer at 2¹¹).
- In 4×9×8, 817 of 69,124 firewall lives end at a face death inside the launch, and in 4×8×8, 1,777 of 28,656.

## Claim 4: the conjecture — does not stand

- **b(5) = 0.2082 ± 0.0006**, 13σ below 0.216 and 21σ below 0.221. b(4) = 0.2072 ± 0.0001. **b(4), b(5) and b(6) are
  one value, 0.2072 (χ² 3.5 / 2).** Only b(6), from two points with ± 0.0062, is within 1σ of 0.216.
- **Extrapolating with b(s) = b∞ − c/s.**
  - Over s = 4–6: b∞ = 0.2127 ± 0.0031, 1σ below 0.216 and 2.7σ below 0.221, with c = 0.022 ± 0.013 (2σ from zero).
  - With s = 3 included the form fails (χ² 76 / 2).
  - Nothing in the data points to 0.216–0.221. It is an extrapolation carried by the two s = 6 points.
- **"The slab line's 0.2088 is an average over narrow slabs."** The data say the reverse.
  - Fitted over s ≥ 4 with area only, the slope is 0.2085 ± 0.0001. That is above every s ≥ 4 family's own slope
    (0.2072), because the intercepts rise with s and in these samples s rises with A.
  - The old line's 0.2088 came from CPU slabs A = 27–90 of mixed s. It is most plausibly an A-only slope inflated by the
    width offsets, not an average of narrow-slab costs pulling a wide-face 0.216 down.
- **The forecast.** It was committed at 09:49:44Z (5cd9a83), before the first run started (start_utc 09:50:16Z). It is
  reported as a miss, which is correct: reading A was rejected. The outcome text then claims reading W, though for
  s ≥ 4 the pre-registered criterion gives O (claim 2).

## Required fixes before merge

1. **Errors on every difference.** In README and PREDICTIONS give the errors for 3×8 − 4×6 (−0.349 ± 0.004) and
   3×10 − 5×6 (−0.740 ± 0.016), and the errors of b(3), b(4) and b(5) (± 0.0001, ± 0.0001, ± 0.0006).
2. **Restate claim 2.** Something like: "s = 3 is cheaper per cell and curved (local slopes 0.1966 → 0.1902, 9σ). For
   s = 4–6 one cost per cell, 0.2072 ± 0.0001, with an intercept rising with s (0.053, 0.121, 0.203), fits (χ² 8.4 / 8).
   b(4) and b(5) agree (1.6σ). By the committed criterion s ≥ 4 is reading O, not W. An alternative, a deficit per unit
   of the long side, fits as well." Drop "rises from width 3 to 5–6" and "perhaps 4".
3. **Say where the χ² lives.** All but 4.9 of the 85.2 is the s = 3 family, chiefly 3×10×8 at −8σ.
4. **Withdraw or rewrite the conjecture.** b(5) is 13σ below 0.216. The s ≥ 4 area-only slope (0.2085) is above the
   family slopes, so "0.2088 is an average over narrow slabs" has the sign wrong. If kept, state it as "b(6) =
   0.213 ± 0.006 is consistent with both 0.207 and 0.216; a 6×8×8 or 7×7×8 point would decide."
5. **The burn-in sentence.** Replace "restricting to ages ≥ 10³ or ≥ 10⁴ moves nothing" with the hazard-by-decade
   statement: flat from about 200 generations on; vacuous for the wide slabs, whose deaths are all older than 10⁴.
6. **Name the confound.** Cut 36·s makes width and firewall share one variable. Within s = 4 the share runs from 0.5% to
   99% without bending the line. In s = 3 the 99.6% slab is the −8σ point, so curvature and firewall proximity are not
   separated there. Replace "competing risks are taken as independent (not tested)" with this.
7. **Mixed launch caps.** State them: 3×6×8 pools caps 2¹⁸ (s601) and 2¹¹ (s711), and 4×7×8, 6×6×8 and 6×7×8 are 2¹⁸ runs,
   with detection biases of ≤ +0.003 to +0.006 (s = 3) and ≤ +0.005 (old 4×7×8). These do not change a conclusion.

## Not checked

- The GPU runs themselves (no second GPU run; no Modal access). The new caps' code path was read, not executed.
- A CPU check at A = 90 or 108 (3×10×8 against 5×6×8, 4×9×8 against 6×6×8): τ_face of e^18–e^22 is beyond the compute
  budget.
- Whether near-firewall states raise the face hazard in s = 3. That needs per-life or per-state data the PR did not
  keep, or a CPU run that records the transverse layers' occupancy before each face death.
- `research/check.sh` on the merged tree.
- The CPU table's own s = 5 entries beyond the 1–2σ comparison (5×5×8: 15.68 ± 0.05 against 15.661; 5×6×8:
  18.95 ± 0.17 against 18.786).

## Recommendation

Merge after fixes 1–4 (text only; data and code are sound); 5–7 are wording.
