# Review of `claude/gpu-local-1080` at 16271f3: the hull-face driver, the fix lists, nine tori

Reviewer: a CPU-side subagent of the lead, 2026-11-15 from 12:04 UTC. Branch read at 16271f3 in a detached worktree
(`git worktree add --detach research/scratch/wt_gl 16271f3`); nothing on the branch was edited. Code and small
tables: `research/audit/gpu_local_tori2/`. Commands below take the worktree path as `WT`.

**Top line for the running job: no flaw found in `hullface.py` that would spoil or bias the 108-cell run beyond
about 0.001 in ln τ_face. Let it run.** Three small things to add after it ends (section 1.4); none touches the rows
it is writing.

## 1. The hull-face driver (`research/gpu-local/hullface.py`)

### 1.1 What the driver is

`hullface.py run R MINUTES SEED` calls `research/gpu/facelaw.py run(R, wall, seed, guard=16, raw_cap=3e6, WB=2, J=1,
minb=1, blocks=#SM)` and writes one csv row from `out['agg'][200]`. Read against main:

- `research/gpu/gsim.py`, `kernel.cuh`, `kernel_shared.cuh` and `research/fluct/` are **unchanged** from main
  (`git diff 0e3b642 16271f3 -- research/fluct research/gpu/kernel*.cuh research/gpu/gsim.py` is empty). The only
  change to `facelaw.py` is the guard hook and three options (`max_gens`, `launch_gens`, `keep_reps`) that default to
  the old behaviour; with `guard=0` the loop is the old one line for line.
- Between the R = 11 calibration (commit fe6f5ff) and the head the driver changed only in `git_head()`
  (`git diff fe6f5ff 16271f3 -- research/gpu research/fluct research/gpu-local/hullface.py`), so the calibration
  row and the R = 15 rows come from the same stepping and counting code.
- Definitions, compared with the file (NOTEBOOK 2026-11-13, CLAIMS F4, GP1): soup 0.35 in |p|₁ ≤ R in the exact
  octahedral hull, 8 faces, a life ends at the first extinction of any of the 8 hull face layers (kind 1), or by
  settling (kind 2: period 1–2; kind 3: back to the launch-start state within 128 generations; kind 5: guard), or at
  the end of the run (kind 0); lives ending before T0 = 200 are excluded; τ_face = 8 × (exposure after T0)/(face
  deaths). This is the statistic of GP1's 23.376 exactly (same function, same T0, same face set), so the new number is
  comparable with it. A replica in which one face has died is frozen by the kernel and reseeded whole at the next
  launch boundary (first-peel statistic): correct for this definition.

### 1.2 Accounting, checked line by line

- **Exposure at a relaunch.** Ages are `G + tt − birth` for kernel events and `G − birth` for guard and end-of-run
  ends; `birth[reps] = G` is set after the reseed, so each life's exposure runs from its own birth. A run is one
  process: all 1,280 replicas are born at generation 0, and nothing carries over between the two runs (seeds 15001,
  15002 give disjoint hash streams `seed << 32 + round`). A crashed run writes no row (the row is written at the end),
  which loses time but adds no bias.
- **No double booking.** At a boundary the guard looks only at replicas whose freeze bit is clear *after* the launch
  (`live = ~frz`), so a replica the kernel froze in that launch (a face death) cannot also end as kind 5; the union
  of both sets is reseeded and the guard's snapshots of all of them are dropped (`gd.reset`) before the reseed.
- **Censoring.** Kinds 0, 2, 3, 5 are all exposure without a death; the estimator is the exponential MLE, unbiased
  for a flat hazard whatever the censoring. Lives open at the end are counted to the end.
- **The guard at this size.** A cycle of period ≤ 128 is caught by the kernel at the next launch start, ≤ K = 2¹⁸
  generations late (1.6 × 10⁻⁴ of a first-death mean). For an odd period above 128 the grid delay is ≥ P·K =
  3.4 × 10⁷, 0.021 first-death means; the snapshot delay (entry to the matching snapshot) is up to about the entry
  age and cannot be cut. The A10G run on file had **no settled life of any kind in 1.9 × 10¹² replica-generations
  at R = 15** (`R15_s1_A10G.json`), and the R = 11 calibration none in 6.4 × 10¹⁰; so the expected number of
  kind-5 lives in the new runs is of order one, and each can carry at most about its own age (≤ 6.8 × 10⁹) of
  unremovable zombie time against a total exposure of 1.8 × 10¹³: **at most about 4 × 10⁻⁴ in ln τ_face per such
  life.** The rows record `guard`, `exposure_guard` and `exposure_guard_past_snapshot`, and `summary` prints both
  conventions, as the fix lists ask.
- **Statistics.** At 3.5 × 10⁸ replica-generations/s for 2 × 420 min: about 11,000 face deaths if ln τ_face =
  23.273, 9,900 if 23.376, so ± 0.0095–0.0100; the two candidate values are 0.103 apart, **ten errors of the new
  run.** The oldest lanes reach 4.2 first-death means (the A10G run stopped at 0.23: all its 4,608 lives were open
  at the end, so 23.376 measures the hazard at ages 200 to 4 × 10⁸ only). The ln(1/F) bias is 1/(2F) ≈ 5 × 10⁻⁵.
- **The kernel shape** (WB 2, J raised by gsim to ⌈2064/1024⌉ = 3, 20 blocks): the acceptance group `defaults`
  tested the production shape on R = 13–17 against `fl.c`, and the guard on/off test ran at R = 15; `hullface.py
  check` runs this WB/minb on the five small reference vessels (where J is smaller). Adequate.
- **Commit and dirty mark.** Read at the start (`git_head()` before `facelaw.run`). The R = 11 row says fe6f5ff,
  clean, started 11:43:04Z, which is 1 minute after fe6f5ff was committed (11:42:20Z). The dirty check covers
  `research/gpu`, `research/shape`, `research/gpu-local/*.py`, but **not `research/fluct/`**, where `fl.py` builds the
  vessel and its face groups (gsim imports it). Unchanged from main, so harmless now.

### 1.3 The calibration at R = 11 (A = 63)

`python3 research/audit/gpu_local_tori2/hull_check.py $WT` (output `hull_check_out.txt`):

| source | protocol | ln τ_face (A = 63) | card − it |
|---|---|---:|---:|
| the card, `hull_R11.csv` (614,098 deaths, seed 11001) | soup 0.35, T0 200, guard on | **13.6362 ± 0.0013** (recomputed; matches the README) | |
| A10G, `research/data/gpu_facelaw/R11_s1_A10G.json` (764,941) | same, no guard | 13.6347 ± 0.0011 | +0.0016 ± 0.0017 |
| `research/dying` round 4, CPU (48,939) | soup 0.4, T0 512 | 13.633 ± 0.005 | +0.003 ± 0.005 |
| `REVIEW-dying.md` round 4, CPU | soup 0.4, T0 512 | 13.626 ± 0.012 | +0.010 ± 0.012 |

All agree within 1σ. (The README's "13.635 ± 0.001 on file" is this A10G value rounded; +0.0016 ± 0.0017 rather
than "+0.001 ± 0.002".) Two codes on the CPU with another soup density and burn-in agree, so the counting of hull
faces and the face set are right at this size.

### 1.4 To add when the runs are in (none affects the running job)

1. **Commit the per-run age table.** `summary`'s hazard by age reads the per-run json under
   `research/scratch/gpu-local/`, which is on the card's machine only, as the tori's were before item 6 of 08:15.
   For the 108-cell face this table is the result that matters most besides the number (does the hazard at ages
   0.2–4 means equal the hazard below 4 × 10⁸ that gave 23.376?), so commit `out['bins']` and `out['guard']` as a
   small `hist_R15_s*.json`, as for the tori.
2. **`hullface.py summary` should refuse two rows with the same seed** (as `facelaw.summary` does): a run restarted
   with its seed after an interruption repeats its soups.
3. Add `research/fluct` to the dirty check.

One reading note for whoever scores block 4: the old 23.376 and the new value differ in which ages they weigh
(0–0.23 means against 0–4 means). If they differ, the age table (item 1) says whether that is noise or an ageing
hazard; the driver itself does not distinguish them.

## 2. The two fix lists

Checked against the branch at 16271f3 (README = `research/gpu-local/README.md`, line numbers at that commit). The
branch's own account is `AGENT.md` "Current state" and the messages of ecd01e9 and 16271f3.

| note, item | what was asked | state | where |
|---|---|---|---|
| 05:30-1 | 4 × 4: "not resolved" replaced by the resolution, pointer to `REVIEW-gpu-local-pr23.md` | **closed** | README 77–80 (9.9249 ± 0.0003 best value, both reviews cited) |
| 05:30-2 | latency conjecture corrected; kind-5 exposure cut at the snapshot age as default, or both reported | **closed** | README 319–333 ("The cut value is the one to quote"; both printed by `eq_analyze.py` 49–54 and `hullface.py summary` 104–106; hull rows carry `exposure_guard_past_snapshot`). No kind-5 life exists in any row, so the two coincide everywhere (README 163) |
| 05:30-3 | 4 × 4 row's `code_commit`; `git_head()` marks a dirty tree | **closed** | `eqtorus_4_0_4.csv` field "ea43aaf+dirty (the uncommitted code that became 95fc5bf)"; `eqtorus.py` 272–279 and 315 (head read before the run); `hullface.py` 30–37, 74. The mark looks at `research/gpu`, `research/shape`, `research/gpu-local/*.py` only, not `research/fluct` (section 1.4, item 3). Verified: no stepping or counting code changed from 95fc5bf to 16271f3 (`git diff --stat 95fc5bf 16271f3 -- research/gpu research/shape research/fluct research/gpu-local/eqtorus.py` shows only `git_head`) |
| 05:30-4 | cite `REVIEW-gpu-pr14.md` for the settled-firewall undercount; at most 0.034, small-slab ln τ_fw only | **closed** | README 126–128 |
| 05:30-5 | `PREDICTIONS.md` new block: the hull forecast is centred on the old value; "0 settled at A ≥ 90" is false | **closed** | `PREDICTIONS.md` 104–109 (block 4, committed ecd01e9 11:48Z, before any R = 15 run) |
| 08:15-2 | the "16 generations over the mean life" sentence replaced by the measured table, `REVIEW-shape2.md` claim 1 cited | **closed** | README 102–118 |
| 08:15-3 | the bend: on how many degrees of freedom it rests; no smooth decaying correction fits, only a kink near 61; the 0.2088 column | **closed, with two inaccuracies** | README 175–200: the column now uses the fitted 13.1621 + 0.20867(A − 63). But "χ² 68 to 117 on 1 in the review's fits" mixes two tables (it is 113–117 for the four decaying forms, 59–70 with the 57 error inflated, 15 for the stretched one), and "which the four new ones sharpen" overstates what they add (section 3.3) |
| 08:15-4 | the CPU value at 57 cells as the second code | **closed** | README 152 |
| 08:15-5 | `eqtorus.py` records the commit with a dirty mark at the start | **closed** | `eqtorus.py` 315 (rows from 57003 on carry it: 2ed297d, clean) |
| 08:15-6 | commit the `eqtorus.py check` outputs and the per-run age tables | **closed** | `research/data/gpu_local_eqtorus/checks/` (nine files; 4 × 4 and 93 are reruns made after the runs, as README 139–141 says) and `hist_*.json` (nine). Checked: for every run the table's exposure and face deaths sum exactly to its csv row (`nine.py`, column "hist == rows") |

"Can follow" items of 05:30: the R = 11 facelaw calibration is done (section 1.3); a guard test with K_KEEP and the
post-firewall exposure of the s = 3 slabs are not (neither was a merge condition).

**As far as these two lists go, pull request 23 can be merged.** The two README inaccuracies of 08:15-3 and the
others of section 3.5 are corrections of wording, not of any number on the branch.

## 3. The nine tori as science

`python3 research/audit/gpu_local_tori2/nine.py $WT` → `nine_out.txt` (every number in this section). Values are
recomputed from the csv rows (ln(2E/F) ± 1/√F); they match the README to the last digit.

### 3.1 Are the errors honest?

- **Seeds.** χ² of face deaths against exposure between the seeds of each torus, summed over the eight tori with
  more than one run: **19.0 on 16 (p = 0.27).** The Poisson errors hold. The 57-cell torus alone gives 9.25 on 3
  (p = 0.026), from seed 57002 (11.8771 against 11.8742, 11.8748, 11.8742); one such torus in eight is unremarkable,
  and 57 sits below the bend, so its error does not enter the line (scaling it by √(9.25/3) changes no conclusion
  below: second block of `nine_out.txt`).
- **Age tables** (committed `hist_*.json`; they sum exactly to the rows). Hazard of a face death by age relative to
  the torus's mean, bins of ≥ 300 deaths: flat for 75, 81, 84, 93 (χ² 10.7/14, 5.6/13, 15.6/13, 12.2/10), and for
  48, 57, 63 after the known excess at ages 0–60 (1.27, 1.67, 2.0 times; 0.6%, 0.08%, 0.02% of a mean life). In
  absolute ages, 93 is flat within 1–2% from 0 to 3 × 10⁸ generations. **108 and 111 are runs of 0.20 and 0.18 mean
  lives**, so their values are the hazard at ages below 1.1 × 10⁹ only; 108 is flat (χ² 2.2/2), **111 is not quite**
  (χ² 8.9 on 2: 0.87 ± 0.05 of its mean below 0.03 mean lives, 1.06 ± 0.04 at ages 3 × 10⁸ to 1.1 × 10⁹). The
  README calls 111 "flat within errors". If its late hazard were the true one, 111 would be 0.05 lower and the
  slope 93 → 111 would be 0.207, not 0.2105; at 2.5σ in one of nine tables this is a caveat, not a finding.
- **Between lattices.** The line from 63 has χ² 7.8 on 5. Adding an extra scatter t in quadrature: the median
  estimate of t is 0.004, its 95% upper bound **0.014** (χ²(t) = 1.15, the 5% point on 5). The README's "room for
  a scatter of about 0.003 between lattices, no more" is the median, not a bound; the data allow lattice-to-lattice
  differences up to ~0.014 at 95%.

### 3.2 What fits the nine

Fits to all nine, 5 degrees of freedom for the four-parameter forms (`nine_out.txt`, first block):

| form | χ² (dof) | c_∞ = lim d ln τ/dA | slope 93 → 111 in the model |
|---|---:|---:|---:|
| **B: broken line, kink fitted (A₀ = 61.39)** | **7.8 (5), p = 0.17** | **0.20867 ± 0.00011** | 0.20867 |
| E: a + cA − g e^{−(l−4)/λ} (decaying in the loop) | 174 (5) | — | 0.2053 |
| P: a + cA − g (48/A)^q | 177 (5) | — | 0.2051 |
| M: a + A[c − g e^{−l/ξ}] (per-cell, massive-like) | 164 (5) | — | 0.2061 |
| Q: a + cA + g₁/A + g₂/A² | 176 (5) | — | 0.2049 |
| S: a + cA − g e^{−(A/A₀)⁶} | 31 (5) | — | 0.2078 |
| H: a + cA − g (A₀ − A)₊² | 77 (5) | — | 0.2079 |
| R: a + cA + g/A | 178 (6) | — | 0.2053 |
| Kq: a + c(A−63) + κ(A−63)² | 344 (6) | — | 0.1995 |

With the error at 57 scaled by √(9.25/3): E, P, M, Q, R, X 133–154 on 5, S 30, H 61; B unchanged. **No smooth
finite-size form fits the nine; only the broken line does.** The 81-cell value does not rescue them: their residual
pattern (48 +0.7σ, 57 −4σ, 63 +9σ, 75 −7σ, then +3σ and +4σ at 108, 111) is the five-point failure plus the absent
downturn above 93.

But note what carries this. **On the eight tori from 57 up every decaying form fits as well as the line (χ² 7.8 on
4)**, with its scale parameter run to a step (λ → 0.02, q → 178, ξ → 0.025; S with A₀ = 32 and g ≈ 8 × 10¹¹: the whole deficit put
on 57 alone). So "smooth or kinked" is decided by three points, 48, 57 and 63, of three different lattice kinds (48 is
axis-aligned with 8 transverse layers and a firewall channel; 57 and 63 are oblique with 2). The four new tori add
nothing to that question. What they add is the part above 63: a straight line through seven tori, which no form with
a correction large enough to make the 48 → 57 → 63 bend can follow.

**Above 63 cells** (seven tori, `nine_out.txt` third block):

| description | χ² (dof) | price per cell at large A |
|---|---:|---:|
| line | 7.8 (5) | **0.20867 ± 0.00009** (± 0.00019 with the median lattice scatter, ± 0.0005 at its 95% bound) |
| line + κ(A − 63)² | 7.6 (4); κ = (0.4 ± 1.0) × 10⁻⁵, Δχ² 0.2 | slope at 150 cells 0.2093 ± 0.0021 (no limit) |
| a + cA + g/A (slope approaches c from below if g > 0) | 7.6 (4), g = +2.0 | 0.2090 ± 0.0013 |
| line + offset for 2-layer tori | 7.7 (4), d = −0.0008 | 0.2086 ± 0.0002 |
| line from 75 only | 7.3 (4) | 0.2088 ± 0.0003 |

**The data do not prefer a slope that rises with size.** The curvature term buys Δχ² = 0.2; the difference of the
data's local slopes, (93 → 111) − (63 → 93) = +0.0021 ± 0.0014, is 1.5σ and rests on 111, the torus with the
weakest age test (3.1). Every surviving description gives a price per cell of **0.2087–0.2090 with errors 0.0001
(line) to 0.0013–0.0021 (if a drift is allowed)**; once a drift is allowed, neither 0.2084 nor 0.2105 is excluded at 2σ. The hull
faces' local slopes (0.212–0.218) lie 1.3–4σ above the quadratic's slope at 150 cells and 2.3–7σ above the g/A
form's limit: a wrapped face reaching the hull's price would need a curvature these tori do not show.

### 3.3 Is "one line from 63 cells, the break near 61 stands, sharper" fair?

- "One line from 63 cells": **fair** (p = 0.17, no curvature, no lattice offset needed).
- "The break near 61 stands": **fair, with its basis stated**: it is the only form of those tried that fits all
  nine, and it rests on 48, 57, 63 alone; drop 48 and no form can be told from the line.
- "Sharper": **not fair as written.** The kink's position and shape are fixed by the same three tori as at five
  (A₀ 61.39 now, 61.35 before). What is sharper is the exclusion of smooth forms through their predicted bending
  above 63.

### 3.4 Scoring the forecasts committed before the rows

From `research/audit/gpu_local_tori/predictions.txt` (720ee7e) and the card's block 3 (6b2dc2b; block 3 has had no line
changed since, `git diff 6b2dc2b 16271f3 -- research/gpu-local/PREDICTIONS.md` deletes nothing), measured −
forecast in combined errors at 81, 84, 108, 111:

| forecast | 81 | 84 | 108 | 111 | χ² on 4 |
|---|---:|---:|---:|---:|---:|
| line from 63, five-point fit (± 0.002–0.006) | +2.5 | +1.8 | +0.9 | +1.6 | 12.8 |
| card block 3 (same line, slope ± 0.0003) | +1.4 | +1.0 | +0.8 | +1.4 | 5.4 |
| smooth forms E, M (± 0.023–0.18) | −0.2 | 0.0 | +0.6 | +0.7 | 1.0 |
| stretched S | +0.9 | +0.8 | +1.2 | +1.7 | 5.8 |

Two things follow, and the second concerns the earlier review as much as the branch.
- As forecasts, the smooth forms scored best and the five-point line worst: all four tori fell above the line, so
  its slope 0.20840 ± 0.00014 was too precise (the nine-point slope 0.20867 is 1.9σ from it). The card's block 3,
  with its slope error ± 0.0003, was honest; the review's line was not.
- **The 81-cell torus could not have been "the sharp test".** The review put line and smooth forms 0.014 apart at
  81, but the smooth forms' own forecast error there was ± 0.023, so no value at 81 could have refuted them. Block 4's
  "3.0 statistical errors above the first and 1.5 below the second" counts only the measurement error. In combined
  errors 81 is 2.5σ above the line's forecast and 0.2σ from the smooth ones. The smooth forms fail on the refit, not
  on 81.
- Block 4's arithmetic is right: 1.4, 1.0, 0.8, 1.4 combined errors; slope 93 → 111 = 0.2105 ± 0.0013, 0.0021 from
  0.2084 against a criterion of 0.002, a fail by the letter; its "one time in eight" is right (P(|z| > 1.52) = 0.13).
  The earlier review's own criterion for the line (81 or 84 more than 3 combined σ off, or 108 and 111 both more than
  0.03 off on one side) is not met: the line survives by its letter (81 at 2.5σ; 108 only +0.020).

### 3.5 Corrections the README needs (wording; no number on the branch changes)

1. Line 197: "χ² 68 to 117 on 1 in the review's fits" → 113–117 for the four decaying forms (59–70 with 57's error
   inflated), 15 for the stretched one; on nine tori 164–177 on 5 (S 31, H 77).
2. Line 195: "which the four new ones sharpen" → the four new tori exclude smooth forms more strongly through the
   straightness above 63; the bend itself still rests on 48, 57, 63, and without 48 no form can be told from a line.
3. Line 205: "room for a scatter of about 0.003 between lattices, no more" → median 0.004, 95% upper bound 0.014.
4. The 111 hazard: "flat within errors" → χ² 8.9 on 2, a 2.5σ hint of a rising hazard in a run of 0.18 mean lives;
   and the slope 93 → 111 that would make the price rise rests on that torus.
5. Block 4 (in a new block, as the file's rule requires): the 81-cell comparison in combined errors (2.5σ from the
   line's forecast, 0.2σ from the smooth forms'), as above.
6. Hull section: the A10G value is 13.6347 ± 0.0011, so the difference is +0.0016 ± 0.0017 (the README rounds both).
