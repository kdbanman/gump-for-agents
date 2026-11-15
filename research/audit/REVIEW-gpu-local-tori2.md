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
