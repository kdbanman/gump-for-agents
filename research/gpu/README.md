# GPU ensembles of gump on Modal

GPU agent, 2026-11-13. Question from Kirby: can small, cheap GPUs (Modal) run this automaton well?
Tags as elsewhere: **[measured]** (with the command), **[conjecture]**.

> **Lead's notes after review (2026-11-13).** An adversarial review (`research/audit/REVIEW-gpu-pr8.md`) re-derived
> every table here from the committed data, emulated kernel B on a CPU against `fl.c` and the engine (exact,
> including the A = 108 run's shape, and with three deliberately broken kernels caught), and ran an independent
> CPU measurement at A = 84 (18.154 ± 0.025 against 18.141 here). The lead re-derived the A = 108 and A = 135
> lifetimes from the raw death lists (23.376 ± 0.031, 29.34 ± 0.25). **The numbers stand. The first version
> of this page made the statements quoted below; they were wrong as worded and have since been corrected:**
> - "A = 108 sits 0.39 nats (13σ) above the line 0.2077·A + 0.55": that line never fitted the verified lifetimes
>   (it misses A = 45 and 84 by 0.08 nats). The finding is: local slopes rise, 0.201, 0.212, 0.212, 0.218, 0.221;
>   A = 108 is 0.21 ± 0.04 nats above the straight line through the verified A = 45–84 points; curvature is 2.6σ
>   from the GPU points alone, about 5σ with the CPU points.
> - "The `qsd.py` settle concern is real at R = 36 too": `qsd.py` detects every period dividing 840. What was shown
>   is the failure of a detector that sees only periods 1–2. No number recorded in this repository is shown biased.
> - "τ(R = 40 v) is 21% above the 7.1e7 on file": the file's number pools soups with copies of the side-16 cube.
>   The soup-only value on file (8.2×10⁷ ± 15%) agrees with 8.63×10⁷ here.
> - "Aftershock for the first 0.01τ": the excess is double peels, the next layer dying within about 20 generations.
> - Cube-centred symmetric runs (R = 43, 45): the death rate falls with age (p = 0.04, 0.01), so those τ are rates
>   over the ages observed, not necessarily the long-run mean. Bears on the side-17 forecast.
> - The review's requested fixes (checks that exit non-zero on failure, committed negative controls, a guard against
>   pooling duplicate runs, and the rewordings above) were made in pull request 10, merged the same day; the text
>   below is the corrected one. The lead spot-checked the diff, not the Modal runs.
> - Not checkable without a GPU: that the GPU executes the kernel as the CPU emulation does.

## Verdict

**Yes, for ensembles; no, for single trajectories.** [measured] One research state is tiny (the side-16 cube's O_h
orbit graph is 946 nodes, a radius-15 octahedron 2,064 cells), so a single trajectory cannot fill a GPU: keep long
single runs on the CPU engine. Many independent replicas of one vessel can: with the state bit-sliced across
replicas and held **on-chip for the whole launch**, an A10G steps 2.0–2.7 × 10¹² node-updates/s, ≈ 400 cores of
`fl.c` on Modal's CPUs and ≈ 17× more work per dollar. The obvious port (state in global memory) is memory-bound and
only 2–3× better per dollar than CPUs; keeping the state in shared memory is what makes the GPU worth it.

## What is here

| file | |
|---|---|
| `kernel.cuh` | kernel A: one thread per 32-replica word-column, state in global memory (`fl.c`'s layout). Also compiles as plain C (`cpu.c`) to check the logic without a GPU. Holds the shared device code (rule, soup RNG, reseed kernel). |
| `kernel_shared.cuh` | kernel B (default): one block per `WB` word-columns, the whole vessel's state in shared memory for the whole launch, neighbour indices in registers, per-generation face / settle reductions by warp-OR. |
| `gsim.py` | host driver (CuPy + NVRTC): `Sim(vessel)` → `reseed`, `step` (returns face-death / settle events), `get_all` / `set_all`. Vessels are `research/fluct/fl.py`'s exact diagonal hulls (asymmetric, or O_h orbit-reduced). |
| `check.py` | bit-exact checks (below). |
| `bench.py` | throughput of both kernels and of `fl.c`. |
| `facelaw.py` | the face-law measurement (time to the first face-layer death of octahedral soups). |
| `modal_app.py` | Modal entry points: `check`, `bench`, `bench_shared`, `cpubench`, `facelaw`. |

Semantics: every replica is stepped exactly (B45/S345 on the vessel graph; outside the vessel is dead forever by T2).
After every generation, a replica whose initial-hull face layer (any of the 8; for O_h vessels, the one representative
face) is extinct gets a kind-1 event at that generation, one that is unchanged from two generations back (period 1 or
2) a kind-2 event; kernel B also compares every replica with its launch-start state during the first 128 generations
of each launch, so a replica in any cycle of period 3..128 gets a kind-3 event (at generation p of the first launch
that starts inside the cycle). The replica is then frozen (state forced to 0) until the host reseeds it. Face
extinction is permanent (T2), so it is never missed; kind 1 and 2 are exact to the generation.

**Why kind 3 matters** [measured]: O_h soups at vertex-centred R = 36 settle into debris of period > 2 that keeps
the face layer occupied in ≈ 0.04% of lives; a detector that sees only periods 1–2 (this kernel before kind 3)
lets those replicas live forever, and a 90-second run with it (not committed) showed a hazard of 0.61 ± 0.05 per τ at
ages 6–10 τ and a CV of 1.012. With kind 3: CV 0.998, hazard flat to 10 τ. This is about a period-1/2 detector only:
`research/fluct/qsd.py` (via `fl.c`'s `fl_run`) detects every period dividing 840, and no number recorded in this
repository is shown to be biased by settling (the bound at R = 36 is ≲ 1%; `research/audit/REVIEW-gpu-pr8.md`,
claim 5). The asymmetric runs below predate kind 3; they recorded no period-1/2 settling and their hazards are flat
to ~10 τ, which bounds a stuck fraction far below anything that would move their lifetimes.

## Correctness [measured]

**The acceptance bar (bit-exact against the engine every generation):** `modal run research/gpu/modal_app.py::check_every`
— the five cases below, each in five lanes, compared every generation for 2,000–3,000 generations through an
order-independent hash of the live-cell set (`check.cell_hash`; the expected hashes come from `gump run --trace`), for
kernel B in its production shape, in a non-default shape, and for kernel A: all equal. **Negative controls**
(`check.check_negative_controls`, run by the same entry point and by `check.py all cpu CASES`): the same comparison
against the engine's state one generation later, and from a start state with its deepest node flipped, must fail in
every case — they do (every generation mismatches). Every check exits non-zero on a failure (`check.py`, and each
Modal check entry point via `_report`).
**Settling:** `modal run research/gpu/modal_app.py::check_periodic` (cases from
`python3 research/gpu/check.py periodic-cases research/scratch/gpu/periodic_cases.npz`) — 373 R = 9 soups that `gump ensemble` ran to
their end (still, extinct, period 2, and 253 cycles of period 3–66): kind 2 exactly at cycle_start + 2, kind 3
exactly at (first launch start ≥ cycle_start) + period, and with a 32-generation window the period-48 and -66 cases
unflagged.

`modal run research/gpu/modal_app.py::check --gpu T4` (engine cases from
`python3 research/gpu/check.py engine-cases research/scratch/gpu/engine_cases.npz`; the CPU build of kernel A:
`python3 research/gpu/check.py all cpu research/scratch/gpu/engine_cases.npz`). All `ALL OK`:

- **Against the engine**, kernels A and B and B with a non-default shape: the five cases of
  `research/fluct/validate.py` (asymmetric soups R = 11, 19; O_h soups, cube- and vertex-centred; the side-16
  checkpoint at generation 1,025,000,000), each started in six lanes spread over the words (others random soups),
  2,000–3,000 generations: final cell sets identical to `gump run`'s.
- **Against `fl.c`**: every replica's full state every 250 generations (R = 7, 9, 13; 384–20,480 replicas), and the
  generation of every face death: 36,000+ events identical. (Two R = 7 soups started with an empty face: `fl.c` reports
  generation 0, the kernels generation 1, as they check after each step.)
- The face-law driver reproduces known numbers (below).

## Throughput [measured]

`modal run research/gpu/modal_app.py::bench_shared --gpu A10G` (and `::bench` for kernel A, `::cpubench` for `fl.c`
on a Modal CPU container; the measured rows are in `research/data/gpu_bench/`). Node-updates/s = nodes × replicas × generations / s.
Prices: Modal's list prices, 2026-11-13 (T4 $0.59/h, A10 $1.10/h, CPU $0.047 per physical core-hour).

| | asym R = 15 (2,064 nodes) | asym R = 19 (4,020) | O_h vertex hull 45 (1,366 orbits) | node-updates per $ |
|---|---:|---:|---:|---:|
| `fl.c`, 1 thread, this container (Xeon, AVX-512) | 1.0 × 10¹⁰ | 1.0 × 10¹⁰ | 0.9 × 10¹⁰ | |
| `fl.c`, 1 thread, Modal CPU container | 6.1 × 10⁹ | 6.2 × 10⁹ | 6.3 × 10⁹ | ≈ 4.7 × 10¹⁴ |
| kernel A (global memory), T4 | 2.3 × 10¹¹ | 2.2 × 10¹¹ | 2.5 × 10¹¹ | ≈ 1.5 × 10¹⁵ |
| kernel A, A10G | 2.3 × 10¹¹ | 2.3 × 10¹¹ | 2.4 × 10¹¹ | ≈ 7.5 × 10¹⁴ |
| **kernel B (shared memory), T4** | 8.7 × 10¹¹ | 9.0 × 10¹¹ | 9.4 × 10¹¹ | ≈ 5.5 × 10¹⁵ |
| **kernel B, A10G** | 2.4 × 10¹² | 2.5 × 10¹² | 2.6 × 10¹² | **≈ 8 × 10¹⁵** |

Kernel A moves ≈ 9 bytes of DRAM per node-update (every warp's working set is hundreds of KB, so nothing stays in
cache); both cards saturate at the same rate. Kernel B touches DRAM only at launch boundaries. Its shared-memory
gathers average 1.8 wavefronts per load (computed from the layout), so it is not bandwidth-bound either; it is
limited by latency around its three `__syncthreads` per generation and by register pressure: configurations that spill
(`lmem` > 0 in the rows) lose up to 3×. Best shapes: `J` = twice the minimum nodes per thread, `WB` = 1–4 columns per
block (the defaults are J = 2·⌈n/1024⌉, WB = 2). Two blocks per SM did not help (the register cap forces spills).
L4 (Ada, $0.80/h) could not be measured: no capacity for 10 minutes on 2026-11-13.

Kernel B runs only a few thousand replicas per GPU (A10G: 72 blocks × 2 words × 32 = 4,608), so each replica
advances ≈ 2 × 10⁵ generations per second: ensembles reach old ages, which is what a hazard measurement needs.

## First use: the asymmetric face law beyond A = 84 [measured]

`modal run research/gpu/modal_app.py::facelaw --r R --minutes M --seed S [--copies K]` (A10G), then
`python3 research/gpu/facelaw.py summary "research/data/gpu_facelaw/*.json"`. Asymmetric octahedral soups,
p = 0.35 in |p|₁ ≤ R, open space; wait from age T0 = 200 to the first extinct face layer (any of 8); mean = exposure /
deaths. τ_face = 8 × mean (8 independent faces). The R = 9 row is the fluctuation agent's (`research/fluct/README.md`).

| R | A | peels | A10G time | first-peel mean | ln τ_face | per cell | local slope |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 45 | 137,243 | (CPU) | 2,300 ± 6 | 9.820 | 0.2182 | |
| 11 | 63 | 764,941 | 2 min | 1.043 × 10⁵ ± 0.1% | 13.635 ± 0.001 | 0.2164 | 0.2119 |
| 13 | 84 | 34,026 | 4 min | 9.45 × 10⁶ ± 0.5% | 18.141 ± 0.005 | 0.2160 | 0.2146 |
| 15 | 108 | 1,059 | 30 min | 1.77 × 10⁹ ± 3% | 23.376 ± 0.031 | 0.2164 | 0.2181 ± 0.0013 |
| 17 | 135 | 16 | 3.5 h | 6.9 × 10¹¹ ± 25% | 29.34 ± 0.25 | 0.2173 | 0.221 ± 0.009 |

- **Calibration:** R = 11 and 13 reproduce the fluctuation agent's 1.04 × 10⁵ ± 0.008 and 8.86 × 10⁶ ± 0.48 (and
  the hazard is flat in age from 200 to 10⁶ at R = 11, within ±1% per bin; at R = 15 from 3 × 10⁵ to 6 × 10⁸).
- **The cost per cell keeps rising past A = 84** (restated after review, `research/audit/REVIEW-gpu-pr8.md`,
  claim 2). Local slopes of measured lifetimes, verified CPU points then GPU: 0.201 (30→45), 0.212 (45→63), 0.212
  (63→84), 0.218 (84→108), 0.221 ± 0.009 (108→135). A = 108 is **0.21 ± 0.04 nats above the straight line through the
  verified A = 45–84 lifetimes** and consistent (1.2σ) with curved fits to them; the curvature is 2.6σ from the GPU
  points alone and ≈ 5σ with the CPU points. The slope was already rising from A = 30 to 63, so this is not a new bend
  beyond A = 84. (An earlier version of this README measured A = 108 against 0.2077·A + 0.55 — "0.39 nats, 13σ" —
  but that line is a quasi-stationary endpoint fit that misses verified lifetimes by 0.08 nats at A = 45 and 84; it
  measures nothing about curvature.) Octahedral faces at A ≥ 45 cost **more** per cell than rim-free slab faces
  (0.2088 ± 0.0009 for A = 27–90). [conjecture] Extrapolations at 0.208–0.209 per cell for large octahedral faces are
  lower bounds; whether the rise is a rim effect (these faces are mostly rim) or the bulk constant is open
  (experiment a in `PREDICTIONS.md`).
- Caveats: at R = 17 the replicas reach ages ≤ 8 × 10⁸, ≈ 1/900 of the mean; the estimate assumes the hazard stays
  flat beyond (it is flat over 3–4 decades at R = 11–15, and the 16 deaths at R = 17 spread over 3 × 10⁷–10⁹ without
  a trend beyond Poisson noise). Only period-1/2 settling was detected in these runs; none occurred.
- **Bug found and fixed on the way:** the first R = 17 batch (3 containers, seeds 1–3) repeated the same soups —
  `soup_bit` combined seed and replica as `seed ^ (r << 32)` while the driver passed `seed << 32`, so (s, r) and
  (s′, r ⊕ s ⊕ s′) collided. Identical death ages across containers gave it away. R = 11–15 were single runs and are
  unaffected (within a run all (seed, replica) pairs differ); of that batch only the seed-3 container is kept
  (`R17_s3_A10G.json`, 4 of the 16 peels; it is independent of the later seeds 11–12, which use the new hash). It was
  kept because its 5,120 soups contain the other two containers' 4,608 (the collision maps them into it), so it is
  the whole batch without repeats; I had seen all three containers' deaths (2, 2, 4, the same events) when choosing.
  `facelaw.py summary` refuses to merge two runs with the same (vessel, seed) and warns when files share death ages.

## Second use: the lead's experiments 1 and 2 (O_h-symmetric soups) [measured]

Forecasts were committed first (`PREDICTIONS.md`, 18:05Z); outcomes are appended there. Kernel with settle detection
to period 128; T0 = 1000; τ = mean residence (the eight faces of a symmetric state die together).

| O_h soups | A | deaths | A10G time | ln τ | forecast |
|---|---:|---:|---:|---:|---|
| vertex R = 36 | 513 | 99,763 | 1.5 min | 14.625 ± 0.003 | (τ 2.2e6) |
| vertex R = 38 | 570 | 112,545 | 8 min | 16.345 ± 0.003 | (τ 1.2e7) |
| vertex R = 40 | 630 | 45,785 | 30 min | 18.273 ± 0.005 | (soups on file 8.2e7 ± 15%) |
| cube R = 43 | 759 | 1,057 | 30 min | **21.903 ± 0.031** | 21.6–22.0 |
| vertex R = 44 | 759 | 637 | 30 min | **22.409 ± 0.040** | 22.3 ± 0.4 |
| cube R = 45 | 828 | 192 | 45 min | **24.175 ± 0.072** | 24.0 ± 0.4 |

- **Side 17 without running it:** its first plateau is the cube-centred A = 828 hull; τ = 3.2 × 10¹⁰ (68%:
  2.9–3.4 × 10¹⁰), inside the forecast. Local cube-centred slope 759 → 828: 0.0329 ± 0.0011 per site (0.209/6 =
  0.0348; the lead's a + (0.209/6)A − 0.195√A has slope 0.031 there and lies 0.14 / 0.25 nats below the two new
  points). Vertex/cube factor at A = 759: 1.66 ± 0.08. **Caveat (review):** in both cube-centred runs the hazard
  falls with age (Weibull shape 0.94 and 0.84; p = 0.04 and 0.01; ages ≤ 0.23 τ and ≤ 0.04 τ), so these τ are rates
  over the ages observed, not established long-run means; if young cube-centred soups die faster, the side-17 mean is
  higher than 3.2 × 10¹⁰. A longer R = 43 run is experiment b in `PREDICTIONS.md`.
- **The 7.1 × 10⁷ for vertex R = 40 on file** (the lead's message) pools fresh soups with copies of the side-16 cube's
  own states (`research/experiments/cube_vs_ensemble.py`); the soup-only value on file, 8.2 × 10⁷ ± 15%
  (`research/fluct/data/sym_residence.csv`), agrees with 8.63 × 10⁷ here. (`PREDICTIONS.md`'s "+21%" compared soups
  with that pool.)
- **Single lineages are memoryless** (R = 36, 38, 40): CV, P(> 4τ), P(< 0.05τ), KS and the hazard to 10 τ all match
  an exponential (numbers in `PREDICTIONS.md`), once settled debris of any period ≤ 128 is removed. The R = 40
  numbers use a 5 τ window: `python3 research/gpu/lineage.py research/data/gpu_facelaw/symvR40_s103_A10G.json 5`.
- **The wait immediately after a peel** (`postpeel.py`; `modal run research/gpu/modal_app.py::postpeel --r 40
  --centre v --states 9216 --tau-b 1.254e7`): fresh soups peel at R; their post-peel states (kept by the K_KEEP freeze,
  checked against `fl.c`) run on in the hull one layer smaller. 9,216 post-peel states each:
  R = 38 → 36: mean wait **0.989 ± 0.010** of the stationary τ(36), CV 0.991; R = 40 → 38: **0.998 ± 0.010** of
  τ(38), CV 1.002. One deviation: **double peels** — 36 and 24 of the 9,216 next layers die within 20 generations of
  the peel (22 and 17 within 2), where ≈ 0.1 are expected; from ≈ 10⁻⁴ τ on the hazard is the stationary one. (An
  earlier version called this an "aftershock over 0.01 τ"; binned at 0.01 τ it looked like a 1.4–1.55× hazard, but
  the excess is the next layer dying together with the old one, ≈ 0.3–0.4% of peels.) Stage A collects the first
  9,216 peels in time, so lineages with long first plateaus are under-represented; this would bias the post-peel mean
  low only if consecutive plateaus were correlated.
- **For OPEN-PROBLEMS 6** (cube plateaus over-dispersed): neither a fresh lineage nor the plateau right after a peel
  shows memory in the direction of long plateaus; double peels shorten a few plateaus to nothing. Whatever makes the cubes'
  plateaus long is not in O_h soup lineages at R = 36–40. [conjecture] It is in the cube's own lineage (its states
  are not typical O_h soup states; see the lead's copies-vs-soups comparison at R = 42).

## Third use: the lead's experiments after review (a, b, c) [measured]

Forecasts committed first (`PREDICTIONS.md`, commit 3b3ceb7, 23:14Z); outcomes appended there.

**a. Through A = 108, rim-free slab faces stay on the line fitted to A = 27–90; octahedral faces at A = 108 are
0.91 ± 0.06 nats tougher. What makes them tougher (rim, eight faces sharing edges, interior thickness, shape) is not
separated.** (Restated after review, `research/audit/REVIEW-gpu-pr12.md`; an earlier version called it a rim effect.)
`modal run research/gpu/modal_app.py::facelaw --slab 6x6x8 --minutes 10 --seed 401` and (through `jobs.py`) two
60-min runs of `--slab 6x7x8`; `python3 research/gpu/facelaw.py summary "research/data/gpu_facelaw/slab*.json"`.
Slabs of 8 {111} layers, periodic in plane (`vessels.SlabVessel` = `research/peeling/geom.slab`; checked every
generation against the engine's torus slab and against `fl.c` on these graphs: `::check_slab`), p = 0.4, the
statistic of `research/peeling/face_law_fit.py` (ln τ_face = ln(2 × mean first peel), line −0.091 + 0.2088·A for
A = 27–90):

| slab | A | cheapest transverse cut | first deaths | ln τ (first outer-layer extinction) | line | per cell |
|---|---:|---|---:|---:|---:|---:|
| 6×6×8 (square) | 108 | 216 cells, 3 directions | 447 | 22.470 ± 0.047 | 22.46 | 0.2081 |
| 6×7×8 (non-square) | 126 | 216 cells, 1 direction | 122 | **≥ 26.14 ± 0.09** (lower bound) | 26.22 | — |

**The kernel records only outer-layer extinction, and a slab also dies by a transverse 3-layer firewall, after which
a face dies soon** (`research/peeling/`, CLAIMS F11). The CPU line excludes slab sizes where firewalls come first in
more than 6% of replicas; these GPU points were not screened. From the repository's firewall rates (cuts 108 and 144,
extrapolated to 216) the review expects ≈ 7 of the 447 first deaths at 6×6×8 to follow a firewall (correction +0.03:
A = 108 on the line stands) and ≈ 25 (18–34; the range runs to about half) of the 122 at 6×7×8, which would put
ln τ_face(126) near 26.36 and the slope 108 → 126 near 0.216, the octahedral value. So the A = 126 value is a lower
bound on the face channel, and the committed data cannot tell a slope of 0.204 from 0.216. (An earlier version of this
section claimed "local slope 108 → 126: 0.204 ± 0.006" and "the bulk constant does not rise"; both are withdrawn.)
At A = 108 the octahedral face (23.376) is 0.91 ± 0.06 nats tougher than the slab face, comparing like with like
(same estimator, same per-face convention, density and start-up excluded by the review). Thickness 8 was not tested
against thicker slabs at A ≥ 108. Octahedral A = 165 was not run (≈ 10⁶ GPU-seconds per death).

**a (rerun). The firewall channel measured** (the review's request; `fwslab.py`, forecasts before the runs in
`PREDICTIONS.md`). Every launch boundary and every face death (state kept, K_KEEP) is tested for a transverse
3-layer firewall (three cyclically consecutive dead layers in a transverse ring); a firewall ends the life as its own
channel. Validated first against `research/peeling/slab_fw.csv` and the review's independent CPU run:

| slab | cheapest cut | first events: face / firewall (share) | ln τ_face | ln τ_fw | target (CPU) |
|---|---|---|---:|---:|---|
| 3×6×8 | 108, 1 direction | 1,917,760 / 276,769 (12.6%) | 11.084 ± 0.001 | 12.327 ± 0.002 | 11.10, 12.18 |
| 4×7×8 | 144, 1 direction | 45,878 / 32,840 (41.7%) | 17.465 ± 0.005 | 17.106 ± 0.006 | 17.43–17.51, 17.16 |
| **6×7×8** | **216, 1 direction** | **92 / 29 (24.0%)** | **26.405 ± 0.104** | **26.866 ± 0.186** | — |

At 4×7×8 the unscreened statistic (16.925) reproduces the review's CPU value (16.934 ± 0.068), 0.54 nats below the
face channel. At 6×7×8 all 29 firewalls are on the cut-216 diagonal; exposure 1.349 × 10¹³; nothing settled (settled
lives — any period ≤ 128 — would be censored; longer periods are not detected and none has been seen). The A = 126
face channel lies **0.19 ± 0.10 above the slab line** (26.218), and the slope 108 → 126 from it and the unscreened
22.470 is 0.219 ± 0.006 — the octahedral value. That compares a square slab (three cheapest directions) with a
non-square one; the control 6×6×8 with the firewall channel resolved is below when it is in.

**b. The cube-centred death rate does not fall with age.** One 3-hour run at R = 43 (A = 759), 2,304 replicas
(`WB = 1`, so each ages twice as fast), settle window 1,024: 5,971 deaths, ages to 2.6 τ, τ = 3.201 × 10⁹
(ln 21.887 ± 0.013; earlier run 3.253 × 10⁹). `python3 research/gpu/weibull.py research/data/gpu_facelaw/symcR43_s501_A10G.json`:
censored Weibull shape 1.020 (95% 1.000–1.041), 1.030 (1.002–1.059) beyond 0.05 τ. Hazard × τ by age (deaths /
expected), from age 0: [0, 0.01) τ 1.11; [0.01, 0.03) 0.82; [0.03, 0.1) 0.99; [0.1, 0.2) 0.93; [0.2, 0.3) 1.03;
[0.3, 0.5) 0.99; [0.5, 0.75) 0.99; [0.75, 1) 1.04; [1, 1.5) 1.00; [1.5, 2) 1.13; [2, 3) 1.02 — flat to ±13% per bin
(two of eleven bins, 0.82 and 1.13, fall just outside their 95% Poisson bands); Weibull k = 1.02 (1.00–1.04). The k = 0.94 / 0.84 of the two shorter runs (ages ≤ 0.23 τ, ≤ 0.04 τ) were noise at R = 43;
R = 45 was not re-run.

**c. Cube-like seeds at vertex-centred R = 40 are memoryless.** `python3 research/gpu/cubelike.py prepare
research/scratch/gpu/cubelike_v40.npz` (fl.c, local, 2 s), `modal run research/gpu/modal_app.py::cubelike` (A10G,
28 min), `python3 research/gpu/cubelike.py analyse research/data/gpu_facelaw/cubelike_v40.json`. 7,807 deterministic O_h
seeds — the closed cube 14 plus the bounding *surface* of side 16 (not the side-16 cube: 10,356 cells, a subset of
`--cube 16`'s 13,056), minus 1, 2 or 3 of that surface's 36 orbits (`seeds.py`'s `sc`, `sc2`, and the same with
three) — run 1,000 generations; 3,893 are then at exactly R = 40, 3,857 distinct. The design leaves out the 2,152
seeds already below 40 and the 1,762 still at R = 42–46 at generation 1000 — among them the lineages most like side
16, whose R = 40 plateau was a second plateau after ≈ 2.5 × 10⁹ generations at 42. Each lineage is followed
through its plateau at 40 (from generation 1000), then at 38 and 36 (state kept at each peel), cap 12 τ (never reached).
T/τ with the fresh-soup τ of this directory:

| plateau | lineages | settled (excluded) | mean T/τ | CV | > 4τ (exp.) | < 0.05τ (exp.) | KS (5% crit.) |
|---|---:|---:|---:|---:|---:|---:|---:|
| R = 40, first | 3,849 | 8 | 0.991 ± 0.016 | 0.999 | 71 (70.5) | 195 (188) | 0.008 (0.022) |
| R = 38, after a peel | 3,845 | 4 | 1.011 ± 0.016 | 0.992 | 69 (70.4) | 186 (188) | 0.015 (0.022) |
| R = 36, after a peel | 3,832 | 13 | 0.983 ± 0.016 | 0.986 | 62 (70.2) | 218 (187) | 0.013 (0.022) |

Each plateau's waits are exponential: 1.8% beyond 4τ against the cubes' 3 of 16; waits ≥ 6.1 τ (side 16's second
plateau): 8 of 3,857 (8.7 expected). The excess of short waits at 36 (218 vs 187, 2.3σ) is where double peels would
put it. **Successive plateaus are weakly correlated:** 40 → 38 Spearman ρ = +0.049 (permutation p = 0.0015;
`research/audit/gpu_pr12/cubelike_own.py`, re-checked here), 38 → 36 ρ = −0.004; the review traces the 40 → 38
correlation to lineages that peel early at 40 (a transient left by the burst). So "memoryless" holds for each
plateau's marginal distribution. For OPEN-PROBLEMS 6: seeds of this family that reach R = 40 within 1,000 generations
wait Exp(τ) at 40, 38 and 36, which bounds a long-lived subpopulation among them (mean 3 τ: under 1.8%; mean 6 τ:
under 0.9%, 95%). The cube's own lineage, and lineages entering R = 40 after a long plateau at 42, are not tested.

## Using it for a new ensemble experiment

Anything that is "many independent replicas of one vessel, stopped at an event" fits: write a driver like `facelaw.py`
(build a `fl.Vessel`, `Sim(v, seedable=...)`, loop `step` / `reseed`, record lives), add a Modal function next to
`facelaw_remote`, and return a **compact** result (see below). Things to know:

- Replicas of one `Sim` share the vessel (graph and face groups). Different vessels or rules need different `Sim`s;
  the rule is fixed to B45/S345 in `rule12` (a different rule is a different carry-save tail, a few lines).
- Events are per replica: kind 1 = some face group's OR is 0 (any of up to 8 groups; for O_h vessels the one
  representative face), kind 2 = period 1 or 2, kind 3 = period 3..`pw` (default 128). Anything else (a population
  threshold) needs a new reduction in phase C of `kernel_shared.cuh`. Censor what settles: a replica that settles
  with its face alive never dies, so it must be counted out, not left running.
- Seeds: `reseed(reps, seed, p)` is a pure function of (seed, replica, node); give every run and every reseed round
  its own seed. Two runs with equal seeds repeat each other exactly (that is how the collision bug was found).
- Validate any change with `modal run research/gpu/modal_app.py::check` and `::check_defaults` (≈ 3 min, a few cents).
- Cost guide (A10G, $1.10/h): ≈ 10⁹ replica-generations per second for a 2,000-node vessel.

## Running on Modal from this environment

- `input-plane.us-east.modal.com` had to be added to the environment's allowed hosts for `modal run` (done
  2026-11-13). Function results larger than a few MB come back through a CloudFront blob host that is **not**
  allowed; `facelaw.py` therefore returns a compact summary (exact per-T0 aggregates, age-binned deaths and exposure,
  raw death ages only if < 50,000). Keep other results small too.
- Several `modal run`s started within seconds of each other hit "App create rate limit exceeded"; stagger them.
- `modal run` ties a run to the local client: when this session's worker restarted (2026-11-13, 23:50Z) the
  ephemeral apps of three running jobs stopped and their results were lost (≈ $2 of compute). Long runs now go
  through the deployed app: `modal deploy research/gpu/modal_app.py` once, then `python3 research/gpu/jobs.py spawn
  facelaw '{...}'` and later `python3 research/gpu/jobs.py collect` (call ids in `research/scratch/gpu/jobs.json`).
  A spawned call's result goes through the blocked blob host above ~100 KB (the 140 KB R = 43 result did); `collect`
  then fetches it through `relay_remote`, which reads the result inside Modal and returns it zlib-compressed.
- Budget: $30/month of Modal credits. `modal billing report --for "this month" --show-resources` shows the spend.
