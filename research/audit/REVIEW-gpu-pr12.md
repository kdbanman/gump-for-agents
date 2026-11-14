# Review of pull request 12 (research/gpu: the lead's experiments a, b, c)

Adversarial review, 2026-11-14. Branch `claude/awesome-cray-boq9vz` at **39f3978**. Worktree used read-only
(`research/scratch/pr12`, removed afterwards); no GPU, no Modal. Scripts: `research/audit/gpu_pr12/`. PR12 below means a
checkout of 39f3978. Every number in the PR's three tables was re-derived from the committed JSON with code written
here (own base64/zlib unpacking, own sums, own fits); none of the PR's analysis scripts were used except to compare output.

## Summary

| claim | verdict |
|---|---|
| a. octahedral rise is a rim effect (slabs A = 108, 126) | **not supported as stated.** Numbers, vessel and stepper confirmed. A = 108 confirmed on the CPU line. The A = 126 point, the slope 0.204 and "the bulk constant does not rise to A = 126" are not supported. The GPU run counts face deaths only, and at 6×7×8 the repository's own firewall rates predict that about a fifth (central estimate; the range runs to a half) of the 122 counted deaths come after a transverse firewall. Corrected central value 26.36, which puts the slope from 108 to 126 at about 0.216, the octahedral value. "Rim" is an untested attribution. |
| b. cube-centred death rate does not fall with age (R = 43) | **confirmed** (wording fix only). k = 1.020 (1.000–1.042), and 1.030 (1.002–1.059) from 0.05 τ, reproduced independently. k = 0.94 and 0.84 are excluded (p ≈ 10⁻¹⁴ and 10⁻⁷⁰). |
| c. cube-like seeds at vertex R = 40 are memoryless | **confirmed with a corrected statement.** The table re-derives exactly and the τ values are right. Each plateau is exponential. Waits at 40 and 38 are weakly correlated (ρ = +0.049, p = 0.002), which the PR does not report. The seeds are not the side-16 cube, and the design leaves out the lineages most like it. |
| forecasts committed first | **confirmed** from commit order. The JSON files carry no timestamps. |
| code | **no defect that changes a number.** One unreachable `except` in `jobs.py`. Nothing touched outside `research/gpu/` and `research/data/gpu_facelaw/` (checked through the merge commit as well). |

**Merge after the required fixes below.** They change wording, and they withdraw the A = 126 inference or replace it
with a run that detects firewalls. No committed number needs to change.

## Claim a: rim-free slab faces (A = 108, 126)

**Verdict: not supported as stated.** What stands:

- the vessel, the stepper and the arithmetic are right;
- at A = 108 a rim-free slab face sits on the CPU line −0.091 + 0.2088·A (22.470 ± 0.047 against 22.459);
- an octahedral face at A = 108 is 0.906 ± 0.057 nats tougher than a slab face, and this compares like with like (below).

What does not stand: the A = 126 point is not a measurement of the face channel. The slope 108 → 126 of
0.204 ± 0.006, and with it "the bulk constant does not rise to A = 126", rest on that point.

Ran:

    python3 research/audit/gpu_pr12/slab_rederive.py PR12             # table, raw vs stored aggregates, hazard in the window
    taskset -c 3 python3 research/audit/gpu_pr12/slab_kernel_check.py PR12   # vessel graph, kernel B vs engine and fl.c
    python3 research/audit/gpu_pr12/fw_competition.py PR12            # firewalls expected in the GPU runs
    taskset -c 3 python3 research/audit/gpu_pr12/fwrun.py 4 7 8 6000000 12002   # independent CPU slabs with firewall tracking
    taskset -c 3 python3 research/audit/gpu_pr12/fwrun.py 3 6 8 400000 12001
    taskset -c 2 python3 research/audit/gpu_pr12/density_check.py octa 9 0.35 100   # and 0.4; `slab 3 5 8 P 150`
    taskset -c 3 python3 research/audit/gpu_pr12/cohort_check.py 3 5 8 0.4 400000   # the stuck-replica trap (point 4)

1. **Table re-derived exactly.** I computed ln(2 · exposure / deaths) from the raw lives. 6×6×8: 447 deaths,
   **22.470 ± 0.047**, 0.2081 per cell. 6×7×8 (two runs, seeds 411 and 412): 122 deaths, **26.138 ± 0.091**, 0.2074 per
   cell. Slope 0.2038 ± 0.0057. Octahedral 23.376 minus slab: 0.906 ± 0.057. The raw lives agree with the stored
   aggregates for T0 = 60, 200 and 1000, and with the stored death lists. For each replica the lives tile the run, except
   the frozen remainder of the launch after each death (1.2 × 10⁵ generations per death, 4 × 10⁻⁵ of the exposure),
   which correctly counts as exposure for no one. The result does not depend on T0 (0, 60, 200 and 1000 give the same
   value to 3 decimals). The run seeds differ, and reseeds use (seed << 32) + round, so no soup repeats.
2. **The estimator is the repository's.** `face_law_fit.py` fits ln(2 × mean first peel) for m = 8 slabs, p = 0.4,
   from generation 0, with frozen replicas leaving the risk set (`peeling/slabs.py`). The PR computes the same
   quantity, from T0 = 60 with settled replicas censored. The factor 2 is per face for a slab, as 8 is for an
   octahedron: both statistics are per-face rates under the same assumption that faces are independent. A is counted
   the same way in both: the cells of one outer {111} layer (3·N1·N2 for a slab, `AREA(R)` for an octahedron).
3. **Vessel and stepper.** `SlabVessel(N1, N2, 8)` was compared with an adjacency built from AUTOMATON.md's 12 offsets
   with an explicit skewed-torus wrap. Every neighbour list is equal for 6×6, 6×7 and 11×11, and the faces are layers
   0 and 7. I also ran the PR's kernel B, unchanged, through PR 8's CPU emulation (`gpu_pr8/shared_shim_uc.cpp`):
   - on SlabVessel(11, 11, 8) it equals `gump run --torus 11 --slab-layers 8 --diag 0` at every generation, 600
     generations × 5 lanes, with my own cell mapping; the negative control (one generation late) fails as it should;
   - in the production shapes of the committed runs (6×6×8 with J = 2, T = 448; 6×7×8 with J = 2, T = 512) it equals
     `fl.c` after launches of 1, 7, 250 and 1000 generations;
   - the kind-1 generations equal `fl.c`'s `run_until` (43 and 34 face deaths).

   (The engine cannot hold a 6×6×8 slab: a 6-torus has only 6 layers. That is why the PR checks the production sizes
   against `fl.c` only.)
4. **Density and start-up are not the issue.** The two estimators were compared with fl.c at A = 45, guarded against
   stuck replicas (`density_check.py`):

   | vessel | p = 0.35 | p = 0.4 |
   |---|---:|---:|
   | octahedron, ln τ_face | 9.823 ± 0.006 | 9.820 ± 0.005 |
   | slab 3×5×8, ln τ_face | 9.247 ± 0.003 | 9.249 ± 0.003 |

   The slab values agree with rep.c (9.231 ± 0.044, `fwrun.py 3 5 8 400000 12003`) and with `slab_area.csv` (9.27).
   **A trap I hit:** fl.c's `run_until` detects only period-1/2 settling. Without a guard, 1 in about 6,000 slab lives
   that falls into a longer cycle lives forever: one such replica took a single-cohort fl.c run to 9.53, and an
   unguarded renewal run to 9.48 (`cohort_check.py 3 5 8 0.4 400000`). The GPU kernel flags cycles up to period 128,
   so the most this can do to the committed slab runs is a stuck fraction of order 10⁻⁴ holding at most 4 × 10⁻³ of
   the exposure. Inside the observed window the slab hazard is flat: censored Weibull k = 0.994 (0.907–1.086) at
   A = 108 and 0.942 (0.79–1.12) at A = 126. The window is only 0.097 and 0.013 of the mean first peel, as the PR
   says. The CPU line's top batches (A = 75, 90) also see less than 10% of their means, so in this respect too the
   comparison is like with like.
5. **The firewall channel (the finding).** A slab dies by a peel *or* by a transverse T3 firewall
   (NOTEBOOK, "Thin slabs and the cheapest cut"; CLAIMS F11). The GPU kernel records only outer-layer extinction.
   After a firewall the face dies soon, and the GPU counts that death as a peel:
   - independent CPU run, 4×7×8, 512 replicas (`fwrun.py`): 94 firewalls came before the first peel, and all 94
     replicas then peeled, a median of 5.6 × 10⁴ generations later against a mean first peel of 1.1 × 10⁷;
   - 3×6×8: 65 of 65, median 864 generations later.

   So the PR's statistic measures face rate + firewall rate. **What that does at a size where both channels compete
   (independent run, 4×7×8, A = 84, the same single cheapest cut direction as 6×7×8):**

   | statistic | value | minus the line |
   |---|---:|---:|
   | PR's statistic | 16.934 ± 0.068 | **−0.515** |
   | the same with firewall-first replicas censored | 17.506 ± 0.091 | +0.058 |

   This reproduces `slab_area.csv` / `slab_fw.csv` for that size (−0.51 and −0.02). The CPU line excludes such
   batches by selection: firewall-first must be under 6% of replicas, so 4×7, 3×6, 3×8 and 2×8 are not in it.
   The GPU points were not screened.

   **How many firewalls the GPU runs should contain.** The cheapest transverse cut is computed from the geometry:
   - 6×7×8: 216 cells (3 layers of 72), attained by **one** diagonal. The third diagonal's ring has only 2 layers
     because gcd(6, 7) = 1.
   - 6×6×8: also 216 cells, but attained by **three** diagonals.

   The m = 8 batches with one cheapest direction and at least 10 firewall-first events give ln τ_fw = 12.04–12.18 at
   cut 108 and 16.92–17.16 at cut 144. A linear fit over cut ≥ 108 (rms 0.09) gives **ln τ_fw(216) = 27.05 ± 0.30**.
   The batch at cut 180 (5×6, only 2 events, 21.1) lies a little below that fit, i.e. on the side of more firewalls.
   Including the 2×N2 slabs at cut 72 gives 25.33 ± 0.60; that would predict more firewalls than the run has deaths,
   so it overshoots. The observed deaths do bound the rate: ln τ_fw ≥ 25.44. With the cut ≥ 108 fit:

   | run | expected firewalls (±1σ) | counted deaths | ln τ_face corrected | minus the line |
   |---|---:|---:|---:|---:|
   | 6×6×8 (3 directions) | 7 (5–9) | 447 | 22.485 | +0.03 |
   | 6×7×8 (1 direction) | 25 (18–34) | 122 | **26.36 (26.30–26.46)** | **+0.14** |

   With the corrected values the local slope 108 → 126 is **0.216 ± 0.006 (stat) ± ~0.006 (firewall)**. That is the
   octahedral 0.218–0.221, not the slab line's 0.2088. The correction rests on a two-cut extrapolation by a factor of
   1.5 in cut size, so I do not claim the corrected value either. I claim only that the committed data cannot tell
   0.204 from 0.216. At A = 108 the correction is small under either fit (+0.03, or +0.10 with the other fit).
6. **"Rim effect" is an attribution, not a result.** The 0.906 nats at A = 108 (0.88 after the firewall correction)
   separates octahedral from slab faces. It does not separate the rim from the other differences:
   - 8 faces sharing edges against 2 independent ones;
   - an interior that is thick (octahedron) against 8 layers (slab);
   - triangular against periodic faces.

   Density (point 4) and estimator (point 2) are excluded as causes. Thickness 8 is near saturation at A ≤ 60 (4×5:
   m = 8 against 10 differ by 0.03 ± 0.06, `slab_area.csv`); at A ≥ 108 it was not tested.

**Required fixes (claim a).**
- R1. Withdraw "local slope 108 → 126: 0.204 ± 0.006" and "the bulk constant does not rise to A = 126". Either state
  the A = 126 value as a lower bound on ln τ_face (≥ 26.14 ± 0.09), with the expected firewall share (≈ 20%, range
  15–50%; this review), or rerun 6×7×8 with firewall detection. For example: run with `keep=True` and, at each kind-1
  event, test the kept state for three consecutive dead transverse layers; or add the 2·N2 transverse layers of the
  cheap diagonal as groups.
- R2. Restate the conclusion as: "Through A = 108, rim-free slab faces stay on the line fitted to A = 27–90; octahedral
  faces at A = 108 are 0.91 ± 0.06 nats tougher. What makes them tougher (rim, eight faces sharing edges, interior
  thickness, shape) is not separated." Do not call it a rim effect.
- R3. The same rewording in `PREDICTIONS.md`'s outcome line for a. The forecast's numbers held (+0.01, −0.08), but
  its reading ("0.2088 per cell holds") does not follow at A = 126.

Optional: mark 6×6 as a square slab (three cheapest directions) and 6×7 as non-square (one) wherever slab sizes are
compared; avoid square/non-square mixes in a slope.

## Claim b: cube-centred hazard at R = 43

**Verdict: confirmed.** Ran:

    python3 research/audit/gpu_pr12/weibull_own.py PR12    # joint 2-parameter MLE (scipy), profile intervals, own unpacking

- **τ re-derived:** symcR43_s501 has 8,275 lives from T0 = 1000, 5,971 deaths and 1 settled life (kind 3);
  τ = 3.201 × 10⁹ (ln 21.887 ± 0.013), ages to 2.59 τ. Raw lives = stored aggregates = stored death list.
- **Weibull fits:**
  - all ages: k = **1.020 (1.000–1.042)**, p(k = 1) = 0.054;
  - left-truncated at 0.05 τ: k = **1.030 (1.002–1.059)**, p(k = 1) = 0.039.

  `weibull.py` gives the same (its profile over k is correct for left truncation). Likelihood-ratio p for the shapes
  of the earlier runs:
  - k = 0.94: 1.4 × 10⁻¹⁴ (all ages), 6.8 × 10⁻¹⁰ (from 0.05 τ);
  - k = 0.84: 10⁻⁷⁰ and 10⁻³⁹;
  - k = 1.05: excluded over all ages (p = 0.006) but not from 0.05 τ (p = 0.18).

  **The data exclude k ≤ 0.98 and k ≥ 1.05 over all ages** (95%).
- **Earlier runs re-derived:** s201 gives k = 0.942 (0.889–0.997), and 0.830 from 0.05 τ; s202 (R = 45) gives 0.836
  (0.724–0.959). These match the PR and the PR 8 review. Censored at the same windows, the new run gives
  0.992 (0.946–1.040) at 0.23 τ and 0.974 (0.871–1.086) at 0.04 τ. So s201 and s501 differ by 1.4σ over the same
  ages, and "noise at R = 43" is fair. Pooled R = 43 (two seeds): k = 1.011 (0.993–1.028), ln τ = 21.889 ± 0.012.
- **Hazard by age** (deaths / expected; the 95% Poisson range of the ratio in brackets): [0, 0.01) 1.11 (0.79–1.22);
  [0.01, 0.03) **0.82** (0.85–1.16); [0.03, 0.1) 0.99; [0.1, 0.2) 0.93; [0.2, 0.3) 1.03; [0.3, 0.5) 0.99;
  [0.5, 0.75) 0.99; [0.75, 1) 1.04; [1, 1.5) 1.00; [1.5, 2) **1.13** (0.90–1.10); [2, 3) 1.02. The PR's table omits
  the first two bins. Two of 11 bins fall outside their 95% band where about 0.5 would be expected, so "flat within
  Poisson error" is slightly generous. If anything the hazard rises a little (k > 1 at p ≈ 0.05).

**Required fix (b):** R4. Give the full hazard table, or say that it starts at 0.03 τ; replace "flat within Poisson
error" with "flat to ±13% per bin; Weibull k = 1.02 (1.00–1.04)". R = 45 remains untested (the PR says so).

## Claim c: cube-like lineages at vertex-centred R = 40

**Verdict: confirmed with a corrected statement.** Ran:

    python3 research/audit/gpu_pr12/cubelike_own.py PR12

- **τ per plateau:** re-derived as exposure / deaths after T0 = 1000 of the fresh vertex O_h soup files:
  8.630 × 10⁷, 1.254 × 10⁷ and 2.247 × 10⁶ (45,785, 112,545 and 99,763 deaths). These are what `cubelike.py`
  hard-codes. Seed count: 1 + C(36,1) + C(36,2) + C(36,3) = 7,807.
- **Table re-derived exactly:**

  | plateau | n | mean T/τ | CV | > 4τ | < 0.05τ |
  |---|---:|---:|---:|---:|---:|
  | 40 | 3,849 | 0.991 ± 0.016 | 0.999 | 71 | 195 |
  | 38 | 3,845 | 1.011 ± 0.016 | 0.992 | 69 | 186 |
  | 36 | 3,832 | 0.983 ± 0.016 | 0.986 | 62 | 218 (z = +2.3) |

  KS 0.0084, 0.0151 and 0.0125 (p = 0.95, 0.34, 0.59). Every lineage at R = 38 died at 40, and every one at 36 died
  at 38. No lineage reached the cap.
- **Selection.**
  - *Conditioning on "exactly R = 40 at generation 1000" does not bias the waits.* The time each lineage spent at 40
    before generation 1000 is under 1.2 × 10⁻⁵ τ, and the waits show no excess of short values at R = 40 (195 against
    188).
  - *It does decide which lineages are studied:* 3,893 of 7,807 seeds. 2,152 are already below 40 at generation
    1000, and 1,762 are still at 42–46. The left-out set includes the lineages whose R = 40 plateau would follow a long
    outer plateau.
  - *Distinctness:* removing exact duplicates is right (the dynamics is deterministic). No near-duplicate lineages:
    among waits ≥ 1000 generations, equal-wait pairs number 0, 0 and 2 against chance 0.04, 0.29 and 1.62. The other
    coincidences are double peels with waits of 1–11 generations (0, 7 and 22 of them).
  - *Settled lineages* (8, 4, 13) are excluded rather than censored; censoring them instead changes the mean by
    ≤ 0.001.
- **Memory between plateaus (not in the PR).**
  - 40 → 38: Spearman ρ = **+0.049 (p = 0.002; permutation p = 0.001)**.
  - 38 → 36: −0.004.

  The 40 → 38 correlation is carried by lineages that peel early at 40. The mean R = 38 wait in the lowest quartile of
  R = 40 waits (≤ 0.29 τ) is 0.943 ± 0.030 τ; for R = 40 waits above 0.3 τ, ρ = +0.004. This reads as a transient
  left by the burst, not a slow variable. Even so, "no memory" holds only for each plateau's marginal distribution.
- **What it shows about side 16.**
  - The seeds are not the side-16 cube. `sc:14:-1` is the closed cube 14 plus the bounding *surface* of side 16:
    10,356 cells, a subset of `--cube 16`'s 13,056.
  - The side-16 cube itself is at R = 42 at generation 1000 (engine). Its 6.1 τ plateau at R = 40 was a *second*
    plateau, after about 2.5 × 10⁹ generations at R = 42. Here the R = 40 plateau is the first, entered straight out
    of the burst.
  - So the experiment shows that lineages which reach R = 40 within 1000 generations wait Exp(τ) at 40, 38 and 36. It
    bounds a long-lived subpopulation among them: mean 3 τ for under 1.8%, mean 6 τ for under 0.9% (95%, from the
    > 4 τ count). Waits ≥ 6.1 τ: 8 of 3,857 (8.7 expected).
  - It does not test the cube's own lineage, or lineages entering R = 40 after a long plateau at 42.

**Required fix (c):** R5. Say what the seeds are (cube 14 + the side-16 surface, not side 16) and that the experiment
leaves out the lineages still at R ≥ 42 at generation 1000; drop "OPEN-PROBLEMS 6 is not explained by structured seeds
either" or restrict it to "seeds that reach R = 40 within 1000 generations". Report the 40 → 38 correlation.

## Forecasts

3b3ceb7 (2026-11-13T23:14:58Z) holds the forecasts for a, b and c. Data commits, in order:

| commit | time | data | run length |
|---|---|---|---|
| 0a0a910 | 23:45:04Z | cubelike, slab 6×6 | 28 min, 10 min |
| a023645 | 01:00:51Z | slab 6×7, two runs | 60 min each, spawned after `jobs.py` at 23:55 |
| 6c78b87 | 03:07:54Z | R = 43 | 3 h |

Each run fits after 23:15. The JSON files carry no timestamps (only `wall_s`), so the order rests on commit times
alone. d40c1f1 changed only the two hand-typed header times (23:25Z → 23:14Z); `git diff 3b3ceb7 39f3978` shows the
forecast text unchanged. All forecasts held numerically: a +0.01 and −0.08 (±0.15 allowed); b k = 1.030 (0.95–1.05
allowed), τ within 2%; c every sub-forecast.

## Code

- `vessels.py`: correct (claim a, point 3). `facelaw.py`: slab mode uses nf = 2 and T0 = 60, and the summary groups
  slab runs by (geometry, A) with the duplicate-seed guard intact; the summary now skips non-facelaw files. Correct.
- `check.py`: `check_slab_every` (engine, N = 11) and `check_fl_slab` (fl.c, production sizes) are sound; the CPU
  emulation above reproduces both in kind. Their GPU outcome was not seen.
- `cubelike.py`: the chain 40 → 38 → 36 keeps the state at the peel (`keep=True`) and maps it with `node_map` /
  `shrink` (as `postpeel.py`, reviewed in PR 8). It cross-checks two seeds against `seeds.py`. Correct.
- `weibull.py`: the profile likelihood with left truncation is correct.
- `jobs.py`: the second `except Exception` is unreachable, because the first catches everything and re-raises
  non-proxy errors. One failed job therefore aborts `collect` before `save(jobs)`, and results already written are not
  marked done (a later collect rewrites the same files). No number is affected. Optional fix.
- `modal_app.py`: `facelaw` now has two docstrings (the second is a dead expression; cosmetic). The image adds
  `peeling/geom.py`, which the slab vessel needs. Settle check gains pw = 1024.
- Paths: `git diff origin/main...39f3978` and `git diff 05a420e^2 39f3978` (through the merge) touch only
  `research/gpu/` and `research/data/gpu_facelaw/`.

## Not checked

- That the GPU executes kernel B as the CPU emulation does (no GPU), and the Modal runs themselves; the PR's
  `check_slab` and `check_periodic` GPU outcomes.
- The firewall rate at cut 216. It is extrapolated from cuts 108 and 144 (and 2 events at 180), so the A = 126
  correction is an estimate, not a measurement.
- Thickness dependence of slab faces at A ≥ 108; independence of a slab's two faces (the factor 2 is shared with the
  CPU line, so slab against line is unaffected).
- Whether the octahedral excess is from the rim; whether the 40 → 38 correlation persists in fresh soups.
- R = 45's falling hazard (not re-run by the PR).
