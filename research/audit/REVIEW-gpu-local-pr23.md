# Review of pull request 23: the GTX 1080 session's first work (guard, acceptance, 4 × 4 calibration)

Adversarial review, 2026-11-15. Object: branch `claude/gpu-local-1080` at 34cd2d3 (`git diff origin/main...34cd2d3`:
`research/gpu/guard.py`, the hook in `research/gpu/facelaw.py`, `research/gpu-local/*`, two data files). There is no
GPU here, so no kernel was re-run. Instead the review did three things: it ran `guard.py` itself on the CPU, with numpy
standing in for cupy; it wrote its own bit-sliced stepper for the 4 × 4 torus; and it re-ran research/shape2's pipeline.
Code and small outputs are in `research/audit/gpu_local_pr23/`, bulk output in `research/scratch/audit_gpu_local_pr23/`.
Commands are run from the repository root. `WT` is a checkout of 34cd2d3
(`git worktree add research/scratch/wt-gpu-local 34cd2d3`).

    D=research/audit/gpu_local_pr23; S=research/scratch/audit_gpu_local_pr23; mkdir -p $S
    gcc -O3 -march=native -o $S/t4 $D/t4.c && python3 $D/geom4.py $S/g44.bin
    python3 $D/validate4.py 3000 5                    # t4 vs engine every generation + 2 negative controls (seconds)
    python3 $D/replay4.py 40000 3; python3 $D/replay4.py 300000 4 8   # t4's event logic vs a numpy replay (2 min)
    ./$S/t4 $S/g44.bin 8 101 29000000 $S/prod_s101.bin & ./$S/t4 $S/g44.bin 8 102 29000000 $S/prod_s102.bin   # 2 cores, ~15 min
    python3 $D/analyze4.py $S/prod_s101.bin $S/prod_s102.bin          # -> analyze4_out.txt
    RERUN_DIR=orig python3 $D/rerun_shape2.py $(seq 1008000 1008075); RERUN_DIR=orig python3 $D/rerun_shape2.py --stats
    RERUN_DIR=fresh python3 $D/rerun_shape2.py $(seq 5008000 5008151); RERUN_DIR=fresh python3 $D/rerun_shape2.py --stats
    python3 $D/soups.py gpu 240; python3 $D/soups.py rep 150          # early hazard of the three pipelines' soups
    python3 $D/repseed.py 6; python3 $D/repseed.py --cross; python3 $D/shape2_raw.py
    python3 $D/guard_cpu.py WT/research/gpu                           # guard.py on the CPU, planted cycles (~3 min)
    python3 $D/launch_bias.py research/data/gpu_facelaw; python3 $D/eq_forecast_patched.py

## Verdicts

| item | verdict |
|---|---|
| 1. Guard | **confirmed, with corrections.** It is sound and complete, and it is inert when off. Two things need correcting. The detection latency for long odd periods is larger than the README's conjecture allows for the queued runs. `guard_test.predict` restates the rule rather than checking it independently. |
| 2. 4 × 4 calibration | **GPU value confirmed; the value on file is refuted as an anchor.** Own value **9.9246 ± 0.0006**. The file's 9.9324 is a high draw of its 76 seeds. Its own pipeline, re-run on 152 fresh seeds, gives 9.9240 ± 0.0014. No systematic cause exists. |
| 3. `fwslab.py` and settling firewalls | **confirmed** (the 18% at 4 × 4 is reproduced independently). Already recorded at 3 × 6 × 8 by `REVIEW-gpu-pr14.md`. On the ledger it touches only small-slab ln τ_fw, by at most 0.034, at 4 × 5 × 8. |
| 4. Launch length | **confirmed.** In earlier GPU runs the effect is negligible wherever per-life data exist, and it is unbounded but possibly 0.003–0.005 on the s = 3 slabs. |
| 5. Acceptance | **confirmed as a port.** Every Modal check entry point is called with the same functions and arguments. Not covered: the face-law driver calibration in "Correctness". The slab-12 cases are reconstructed. Throughput: not checkable here. |
| 6. Forecasts | **committed before the runs (confirmed).** The hull-face forecast is partly a restatement of the value it re-measures, and one premise of the kind-5 forecast is false. |
| 7. README / AGENT | **corrections needed**: the provenance of the 4 × 4 row; the unresolved-disagreement paragraph; the latency conjecture; a missing citation. |

## 1. The guard

**Logic (read line by line).** One snapshot is kept per replica, taken at the first boundary at which the replica's age
is at least `first`·2^j. The snapshot is replaced at each new threshold, and `next_age` doubles past the current age. At
each boundary the guard first compares the live (unfrozen) replicas that hold a snapshot, then takes the snapshots that
are due. The reset at reseed is correct, and so are the word layouts of both kernels (`(WT, n+1)` and `(n+1, WT)`; the
sentinel row is compared too, and it is always zero). Exact equality of the whole state of a deterministic replica
implies that it is periodic from the snapshot on. A recognised life is therefore truly in a cycle, its face can never
die (T2), and censoring it is right. The age is `G − birth` at the boundary. In `facelaw.py`, kind 5 is counted with the
censored kinds (`compact`: `kinds >= 2`) and its exposure stays in. The thresholds and the per-life
(replica, age, snapshot age) triples are stated in `out['guard']`, and `eqtorus.py` writes `exposure_guard` to the csv.

**`guard=0` is inert in `facelaw.run`.** `K = launch_gens or 1024` is 1024. The extra loop condition
`max_gens is None or G < max_gens` is always true. `repl` is an extra list that is never used unless `keep_reps` is set.
The guard block is skipped, the reseed is unchanged, and the doubling condition is unchanged (`not launch_gens`). No
`guard` or `raw_reps` key is added. No caller passes the new keywords positionally or through `**cfg`
(`modal_app.py:264`). Nothing else under `research/gpu/` changed.

**On the CPU** (`guard_cpu.py`, `guard_cpu_out.txt`). The script imports `guard.py` unmodified, with a numpy reduction in
place of the cupy kernel and a stand-in for gsim's arrays in both layouts. It plants state sequences of its own: 64
nodes, random distinct states until an entry age e, then a cycle of period P from 1 to 12,345, or no cycle at all (15%
of lives). It also freezes and reseeds 0.2% of replicas at each boundary. The schedules tried are fixed launches of
1024, prime launches of 997, mixed launches of 997/1024/4096, and facelaw's doubling to 2¹⁸, each in both layouts:
8 settings and about 7,600 lives in all. The results:

- No life was recognised before entering its cycle, and no chaotic life was recognised at all (0 unsound).
- No frozen replica was recognised.
- Every recognition agrees with a prediction of our own. That prediction is a search over the life's own boundary ages,
  written from guard.py's docstring and not ported from `guard_test.predict`.
- No life due for recognition was missed.

Two broken guards were also run. Snapshot-before-compare gives 132,444 unsound recognitions, and thresholds that never
double give 169 misses: both are caught. Not exercised: a frozen replica whose kept state equals its snapshot (with
K_KEEP this can happen after a kernel kind-3 event), so the `live` mask is read, not tested.

**`guard_test.predict` is not independent of what it tests.** It is the same algorithm in the same order (compare,
then snapshot; `while nxt <= b: nxt *= 2`). It therefore catches implementation errors but not errors in the rule.
The reformulation above agrees with it, which covers that gap.

**Exposure and latency.** A kind-5 life contributes its whole age, including the time spent in the cycle before
recognition. That is stated in `guard.py`, and the snapshot age needed to cut the exposure is recorded. The latency is
b − e = (s − e) + (b − s):

- **Snapshot delay s − e.** This is up to about one doubling (about e), more if the grid delay forces the next snapshot.
- **Grid delay b − s.** This is a multiple of the launch grid, so for odd P with launches of length K it is P·K.

Measured on the CPU over the four schedules, the maximum of (b − e)/e for lives with e > 10⁴ is 21–68 with fixed
launches and about 640 with doubling launches. It is dominated by the long periods. The guard matters only for
P > pw = 128. With `eqtorus.py`'s cap of K = 2¹⁸ the grid delay is then at least 3.4 × 10⁷ for odd P, and with
facelaw's 2²⁴ it is at least 2.2 × 10⁹. The queued tori at A = 81–93 have τ_face ≈ 2 × 10⁷ – 3 × 10⁸, and their mean
lives are half that. **So the README's conjecture "both delays are small against a mean life" is false for an odd
period above 128 at A ≤ 93.** Each such kind-5 life can carry more than one mean life of unrecognised exposure.
This is not "until the run ends", but it is not small either.

Fix: estimate with the kind-5 exposure cut at the snapshot age by default (it is recorded) and report both values.
Alternatively, compare also at launch-internal ages that are not on the grid, or replay a recognised life offline from
(seed, round, replica), as the README itself suggests.

The guard cannot miss a cycle forever: K is capped, so a snapshot interval eventually exceeds lcm(K, P).

## 2. The 4 × 4 calibration: 9.9251 against 9.9324

**Own stepper** (`t4.c`, `geom4.py`). Nothing is imported from research/. The graph is built from AUTOMATON.md's
doubled-coordinate offsets on the cube lattice mod (4,0,−4), (0,4,−4) with t = i+j+k in [0, 8): 384 nodes. Each node
has 12 distinct neighbours with symmetric adjacency, and there are no T1 violations on the three transverse diagonals
mod 16. The counter is a ripple adder, the RNG a splitmix hash, and lives are renewed. Every generation is checked for:

- a transverse firewall: three cyclically consecutive dead layers of 48 cells; ties with a face death go to the
  firewall, as in both pipelines;
- a face death: layer t = 0 or 7 extinct;
- a return to a Brent snapshot taken at ages 1, 2, 4, …: any period.

**Validation.** The stepper is bit-exact against `gump run --torus 12 --trace` on the 9-fold tiling, every generation for
3,000 generations, on three soups (`validate4.py`). Both negative controls fail, as they should: the engine shifted by one
generation fails 2,999 times, and a flipped node fails at 300 of 300 generations. A numpy replay of 582 lives, from their
life ids with an independent rule implementation, reproduces every first event's (age, kind, snapshot age) exactly
(`replay4.py`). One of those lives is of kind 5.

**Result** (`analyze4_out.txt`): 2 runs (seeds 101, 102), 2,916,565 lives, E = 2.9696 × 10¹⁰,
F = 2,907,478 face deaths, 7,454 firewalls, 609 settled (2.8 × 10⁻⁴ of the exposure).
**ln τ_face = ln(2E/F) = 9.9246 ± 0.0006**. The two seeds give 9.9252 ± 0.0008 and 9.9241 ± 0.0008. This **supports the
GPU's 9.9251 ± 0.0004** (Δ = −0.0005, 0.7σ) and not the file's 9.9324 ± 0.0020 (Δ = −0.0078, 3.7σ).

**The same lives under research/shape2's conventions:**

| convention | ln τ_face |
|---|---:|
| exact | 9.9246 |
| settled lives censored at the snapshot age | 9.9246 |
| cap 16,384 | 9.9240 |
| death times on rep.c's 16-generation grid (D = la + 1, la rounded up) | 9.9254 |
| both cap and grid | 9.9251 |
| exposure after T0 = 60 / 200 / 1000 | 9.9265 / 9.9264 / 9.9262 |

Exposure convention, cap, grid, settling and burn-in each move ln τ_face by ≤ 0.002, and the shape2 combination by
+0.0005. **None of them explains 0.0078.**

**The cause: a high draw, not a pipeline difference.**

- *The file is what the code produces.* All 76 original jobs, re-run with research/shape2's own code
  (`tslab.run`, `rep.c`, W = 64, cap 16,384, K = 16, seeds 1008000–1008075), are **bit-identical** to
  `research/scratch/shape2/ch_4_0_4_s*.npz` (`rerun_orig_out.txt`).
- *The same pipeline on fresh seeds disagrees with the file.* With seeds 5008000–5008151 (152 jobs, 496,278 face
  deaths) it gives **9.9240 ± 0.0014** (`rerun_fresh_out.txt`). That is −0.0084 ± 0.0024 from the original seeds.
- *The soups are the same in all three pipelines.* Face-death hazard over ages 0–60, × 10⁻⁵ (`soups_out.txt`,
  `hazard_gpu_bins.txt`):

  | soups and stepper | hazard, ages 0–60 |
  |---|---:|
  | t4's own soups | 12.95 ± 0.09 (12.76 over ages [0, 60)) |
  | the GPU's `soup_bit`, stepped by t4 | 12.77 ± 0.19 |
  | rep.c's xoshiro soups and rep.c's stepper, K = 1 | 12.71 ± 0.19 |

  rep.c's streams have density 0.400 and no repeated soup among 24,576. Adjacent seeds' soups differ in 0.480 of their
  bits (independent soups: 0.48), and the face times of adjacent original jobs have lane-by-lane correlation
  +0.0001 ± 0.016 (`repseed_out.txt`).
- *The vessel is the same.* It is the lattice (4,0),(0,4) with 8 layers in both pipelines (`tslab.tslab(4,0,4)`). The
  GPU uses that graph, checked against the engine, and t4 builds its own graph, also checked against the engine.
- *Ruled out as the cause:* the early hazard (identical soups; the hazard is flat after about 200 generations in every
  data set), the cap, the grid, settled lives (139 in the file, ZL1's bound ≤ 0.0004), firewalled lives (0.28% of
  events; GPU boundary exposure about +0.0002), and the seeds.
- *What remains is chance.* The per-job dispersion is mildly super-Poisson in both sets (χ² 100/75 original, 169/151
  fresh). With the error scaled by √(100/75), the original set lies 3.4σ above the pooled independent value. A 3.4σ
  draw is rare, but no mechanism was found.

**The best value:** pooled over own (9.9246 ± 0.0006), GPU (9.9251 ± 0.0004) and the fresh rep.c run
(9.9240 ± 0.0014), **9.9249 ± 0.0003**. The shape2 review's independent `ts.c` value, 9.9275 ± 0.0015, is 1.7σ above it.

**Other values on file that use the high draw.** The cause is statistical, so nothing else shares it; but these
values consume the (4,0,4) row of `research/shape2/data/A48.csv`:

- **`research/constant/PREDICTIONS.md` part C.** Re-run with the anchor replaced (`eq_forecast_patched.py`, against
  `research/constant/out/eq_forecast.txt`):
  - The flat line moves to c = 0.21244 (from 0.21214), with χ² 6.3/1.
  - A = 57 moves by −0.005 (flat) and −0.004 (massive), more than its planned ± 0.0032. A = 63 moves by −0.004 and −0.002.
  - A = 93 and 111 move by +0.005 and +0.010 (flat); the massive reading barely moves there.
  - The forecast local slope 48 → 57 moves by +0.0003 to +0.0004, against a planned error of 0.0004.

  These forecasts are committed and must not be edited. The scoring should say that the anchor was 0.0078 high.
- **CLAIMS SH4.** The census gap between (1,6,16) and 4 × 4 becomes 0.0138 instead of 0.0061. With the review's 0.0135,
  the χ² 4.4/1 tension disappears.
- **SH3.** The loop² 16 slope 48 → 60 is about 0.2131 instead of 0.2125.
- **`research/constant`'s pooled periodic table** (`load.periodic`) includes the row.

## 3. `fwslab.py` and firewalled lives that settle

Confirmed by reading: `fwslab.py:82` remaps only kind 1 on a firewalled state to kind 4, so a settle (kind 2 or 3) on a
firewalled state stays "settled". This leaves ln τ_face unaffected, since both kinds are censored for it. The 4 × 4
numbers check out independently. t4 ends a life at the firewall's formation, and its 7,454 firewalls give
ln τ_fw = 15.198 ± 0.012. That matches the branch's 15.189 ± 0.007, which counts settled firewalled lives, not
fwslab's convention at 15.384: so about 18% of firewalls are hidden at 4 × 4.

**Not new.** `REVIEW-gpu-pr14.md`, "Firewalls labelled settled", found 0.9% at 3 × 6 × 8. The README should cite it.

**Which recorded numbers it touches.** An upper bound is settled/fw per committed fwslab slab (all settled lives taken
as firewalled; `research/data/gpu_facelaw/fwslab*.json`):

| slabs | settled / firewalls | effect on ln τ_fw |
|---|---:|---|
| 4×5×8 | 164 / 4,892 = 3.4% | at most −0.033, against ± 0.014 |
| 5×5×8 | 0.5% | small |
| 3×6×8 | 0.3% | small |
| 6×4, 4×6 | 0.15% and 0.12% | small |
| all others | < 0.03% | small |
| 6×6×8, 6×7×8 | 0 settled | GP8's per-direction firewall rates (26.79, 26.87) are untouched |

GP9's firewall shares move by < 0.3% at s = 3. CLAIMS F11 and K2 are CPU results, outside this pipeline.

## 4. Launch length

**The reasoning is right.** Firewalls are tested only at boundaries, and kernel B recognises kind 3 (periods 3–128) only
at the next launch start. The time from the event to its recognition therefore stays in the exposure, up to one launch.
The +0.0016 at 2¹⁸ is the branch's own run (not committed), so it was not re-checked. The calibration row itself uses
`max_launch=2048`.

**Earlier GPU runs** (`launch_bias.py`, `launch_bias_out.txt`). Where per-life data exist, the bound is the sum of
(boundary − previous boundary) over boundary-detected firewalls, plus one launch + 128 per kind-3 life. It comes to:

| slabs | bound on ln τ_face | statistical error |
|---|---:|---:|
| 4×8×8 | 0.0026 | ± 0.018 |
| 4×9×8 | 0.0031 | ± 0.042 |
| 5×5, 5×6, 5×7, 5×8, 6×6, 6×7 (×8) | ≤ 0.0002 | |

No raw lives exist for 3×6, 3×8, 3×10 (launch cap 2048) or for 4×5, 4×6, 6×4 (cap 65,536). There the crude bound
W·K/E is:

| slabs | crude bound | statistical error |
|---|---:|---:|
| 3×6×8 | 9 × 10⁻³ | ± 0.0004 |
| 3×8×8 | 1.2 × 10⁻² | ± 0.003 |
| 3×10×8 | 1.5 × 10⁻² | ± 0.011 |
| 4×5, 4×6, 6×4 | about 2.3 × 10⁻³ | ± 0.001–0.002 |

At 3 × 6 × 8 a face dies a median of 1,088 generations after its firewall (REVIEW-gpu-pr14). With launches of 2048
that suggests about +0.003, which is many times that slab's error. It matters for GP9's s = 3 rows and for the
3×8 − 4×6 pair (−0.349 ± 0.004), but not at all for ln τ_fw. The octahedral facelaw runs have no firewall channel;
their kind-3 latency is already bounded in `research/gpu/README.md`, "Zombie lives".

## 5. Acceptance and throughput

`acceptance.py` against `modal_app.py`, function by function:

| `acceptance.py` | Modal entry point or command | same calls and arguments |
|---|---|---|
| `g_check` | `check_remote` | yes |
| `g_every` | `check_every_remote`, including the negative controls | yes |
| `g_periodic` | `check_periodic_remote` (4 calls) | yes |
| `g_defaults` + `g_reseed` | `check_defaults_remote` / `check_reseed_remote` | yes |
| `g_keep` | `check_keep_remote` | yes |
| `g_slab` | `check_slab_remote` | yes |
| `g_patches` | `check_patches_remote` | yes |
| `g_cpu` | `check.py all cpu CASES` | yes |

- **Not in the runner:** the face-law driver calibration of "Correctness" ("reproduces known numbers": R = 11, 13). It
  was not repeated on this card for `facelaw.py`, which job 3 will use.
- **Reconstructed:** the 12 × 12 × 8 cases (`slab_cases(N=12, m=8, T=300, rng=3/4)`). No upstream file documents how
  the originals were built.
- **Unstated:** the reference cases were rebuilt with a Windows build of the engine, and that build's golden checks
  (`reference/golden/`) are not reported.
- **Throughput, the shared-memory fit and the TDR behaviour cannot be checked here.** The fit formula
  4·WB·(n + 31) bytes matches `gsim.Sim`'s `smem`.

## 6. Forecasts (`PREDICTIONS.md` at 0a997a1)

**Order: confirmed.** The forecasts were committed at 04:18:56Z. The first measurement run (4 × 4) started at 04:34:17Z
(csv `start_utc`), and the A = 93 and hull runs had not started.

**The hull-face forecast is not fully a forecast.** Its "0.2181 ± 0.0013" is the 84 → 108 slope computed from the A = 108
value being re-measured ((23.376 − 18.141)/24). The range "23.36 to 23.38", and the forecast 23.37 ± 0.03, bracket that
value with its own error. Only the lower end (0.2173) comes from extrapolating A ≤ 84. The block should be scored as a
consistency test of the old run, not as an out-of-sample prediction.

**A premise of the kind-5 forecast is false.** It says detected settling "was 0 in every slab run of A ≥ 90 on file".
In fact fwslab 3 × 10 × 8 (A = 90) has 21 settled lives and 4 × 9 × 8 (A = 108) has 3 (`research/data/gpu_facelaw`).
The forecast numbers may still stand, but their stated basis does not.

## 7. Other points in README and AGENT

- **The csv row's `code_commit` is wrong.** The 4 × 4 row says ea43aaf, but ea43aaf's `eqtorus.py run` accepts no
  `max_launch=` / `raw_cap=` arguments and computes no `fw_settled`. The row was made with the uncommitted code that
  became 95fc5bf. Stepping, events and exposure did not change between the two, so the numbers stand; the provenance
  does not. `git_head()` should mark a dirty tree.
- README "Not resolved: a CPU cross-check … is running" is now resolved (item 2). The 4 × 4 anchor should read
  9.925, not 9.9324.
- **The early hazard.** README gives 12.47 × 10⁻⁵ over ages 0–60. Three independent measurements give 12.76 ± 0.09
  over the same bin [0, 60), which is about 3σ apart. No cause was found. Its effect on ln τ_face is ≤ 0.0002.
- The latency conjecture (item 1) should be corrected, and the kind-5 exposure convention stated in each result.
- `fwslab.py` has no guard hook. Tori use `eqtorus.py`, which has one; any future fwslab lifetime run would be
  unguarded, contrary to "the guard on for every lifetime run".
- The branch's commit trailers carry a model name. The squash-merge message should drop it.

## Must fix before merge

1. README: replace "not resolved" with this result. The file's 9.9324 is a high draw. The best value is
   9.9249 ± 0.0003. Point the reader to this review.
2. README: correct the latency conjecture. For odd P > 128 the grid delay is P·K: at least 3.4 × 10⁷ at K = 2¹⁸, which is
   at least a mean life at A ≤ 93. Then either make the snapshot-age cut of kind-5 exposure the stated default, or
   report both estimates in every guarded result.
3. The 4 × 4 csv row: correct `code_commit` (or annotate it), and make `git_head()` mark a dirty tree.
4. README: cite `REVIEW-gpu-pr14.md` for the settled-firewall undercount. Say it touches only small-slab ln τ_fw
   (≤ 0.034, at 4×5×8).
5. PREDICTIONS (in a new block; the old one stays as it is): the hull forecast's centre is the old value, and the
   "0 settled at A ≥ 90" premise is false.

## Can follow

- Lead: a note under `research/constant/PREDICTIONS.md` part C (new block). The anchor was 0.0078 high, and
  `eq_forecast_patched_out.txt` gives the shifted readings for scoring.
- Lead: amend CLAIMS SH4 (the census gap becomes 0.0138, and the tension with the review disappears) and SH3 (the
  loop² 16 slope 48 → 60 becomes about 0.2131).
- Measure the post-firewall exposure of the s = 3 slabs, which is possibly 0.003–0.005 on ln τ_face (item 4). It needs
  per-life data or a short CPU run with exact firewall times.
- Add a guard test where a frozen replica's kept state equals its snapshot (the K_KEEP case).
- Run the facelaw calibration (R = 11 against the stored value) on the card before job 3.

## Not checked

- Anything on the GPU: kernels, throughput, the shared-memory and TDR claims, the GPU guard tests and their counts
  (1,280 lanes, 7,851 kind-5 lives and so on), and whether `acceptance.py` passed there. Only its source was read.
- The GPU's 4 × 4 per-run json (raw lives, hazard bins). It is not committed; only the csv row was used.
- The +0.0016 of the 2¹⁸ calibration run.
- `eqtorus.py check` on (1,5),(0,31).
- The R = 9 guard-on/guard-off identity runs.
- The fwslab bounds for runs without raw lives. Those are crude upper bounds, not measurements.
