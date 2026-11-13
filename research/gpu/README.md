# GPU ensembles of gump on Modal

GPU agent, 2026-11-13. Question from Kirby: can small, cheap GPUs (Modal) run this automaton well?
Tags as elsewhere: **[measured]** (with the command), **[conjecture]**.

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
the face layer occupied in ≈ 0.04% of lives; without kind 3 those replicas never die, and a 90-second run already
showed a hazard of 0.61 ± 0.05 per τ at ages 6–10 τ and a CV of 1.012 (the lead's warning about `qsd.py`'s settle
test, which applies at R = 36 too, not only below 30). With kind 3: CV 0.998, hazard flat to 10 τ.
The asymmetric runs below predate kind 3; they recorded no settling at all and their hazards are flat to ~10 τ.

## Correctness [measured]

**The acceptance bar (bit-exact against the engine every generation):** `modal run research/gpu/modal_app.py::check_every`
— the five cases below, each in five lanes, compared every generation for 2,000–3,000 generations through an
order-independent hash of the live-cell set (`check.cell_hash`; the expected hashes come from `gump run --trace`), for
kernel B in its production shape, in a non-default shape, and for kernel A: all equal. Negative controls (expected
hashes shifted by one generation; one orbit flipped at the start) fail as they should.
**Settling:** `modal run research/gpu/modal_app.py::check_periodic` — 373 R = 9 soups that `gump ensemble` ran to
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
on a Modal CPU container; raw rows in `research/scratch/gpu/`). Node-updates/s = nodes × replicas × generations / s.
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

| R | A | peels | A10G time | first-peel mean | ln τ_face | straight line 0.2077·A + 0.55 | excess | local slope |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 9 | 45 | 137,243 | (CPU) | 2,300 ± 6 | 9.820 | 9.90 | −0.08 | |
| 11 | 63 | 764,941 | 2 min | 1.043 × 10⁵ ± 0.1% | 13.635 ± 0.001 | 13.635 | 0.00 | 0.2119 |
| 13 | 84 | 34,026 | 4 min | 9.45 × 10⁶ ± 0.5% | 18.141 ± 0.005 | 17.997 | +0.14 | 0.2146 |
| 15 | 108 | 1,059 | 30 min | 1.77 × 10⁹ ± 3% | 23.376 ± 0.031 | 22.982 | **+0.39** | 0.2181 ± 0.0013 |
| 17 | 135 | 16 | 3.5 h | 6.9 × 10¹¹ ± 25% | 29.34 ± 0.25 | 28.59 | **+0.75** | 0.221 ± 0.009 |

- **Calibration:** R = 11 and 13 reproduce the fluctuation agent's 1.04 × 10⁵ ± 0.008 and 8.86 × 10⁶ ± 0.48 (and
  the hazard is flat in age from 200 to 10⁶ at R = 11, within ±1% per bin; at R = 15 from 3 × 10⁵ to 6 × 10⁸).
- **The face law curves upward.** The local slope rises steadily, 0.212 → 0.215 → 0.218 → 0.221 per site, and the
  straight line fitted to the stationary-distribution endpoints at A ≤ 84 (I(0) = 0.2077 + 0.55/A) falls 0.39 nats
  (13σ) short at A = 108 and 0.75 nats (3σ) short at A = 135. A quadratic in A fits all five sizes
  (ln τ_face ≈ 0.479 + 0.2045·A + 6.9 × 10⁻⁵·A², χ² = 0.1 for 2 degrees of freedom); the quadratic through only the
  three precise points (A = 63, 84, 108) gives 29.37 at A = 135, against the measured 29.34 ± 0.25. Cost per site,
  ln τ_face / A: 0.2164, 0.2160, 0.2164, 0.2173 at A = 63 … 135 — a minimum near A ≈ 80, then rising. This is the
  same direction as the symmetric faces (whose cost per site also rises with face size, `research/fluct/sym_fit.py`).
  [conjecture] Extrapolations that use 0.208–0.209 per site for large asymmetric faces are lower bounds.
- Caveats: at R = 17 the replicas reach ages ≤ 8 × 10⁸, ≈ 1/900 of the mean; the estimate assumes the hazard stays
  flat beyond (it is flat over 3–4 decades at R = 11–15, and the 16 deaths at R = 17 spread over 3 × 10⁷–10⁹ without
  a trend beyond Poisson noise). Only period-1/2 settling is detected; none occurred.
- **Bug found and fixed on the way:** the first R = 17 batch (3 containers, seeds 1–3) repeated the same soups —
  `soup_bit` combined seed and replica as `seed ^ (r << 32)` while the driver passed `seed << 32`, so (s, r) and
  (s′, r ⊕ s ⊕ s′) collided. Identical death ages across containers gave it away. R = 11–15 were single runs and are
  unaffected (within a run all (seed, replica) pairs differ); of that batch only the seed-3 container is kept
  (`R17_s3_A10G.json`, 4 of the 16 peels; it is independent of the later seeds 11–12, which use the new hash).
  `facelaw.py summary` now warns when runs share death ages.

## Using it for a new ensemble experiment

Anything that is "many independent replicas of one vessel, stopped at an event" fits: write a driver like `facelaw.py`
(build a `fl.Vessel`, `Sim(v, seedable=...)`, loop `step` / `reseed`, record lives), add a Modal function next to
`facelaw_remote`, and return a **compact** result (see below). Things to know:

- Replicas of one `Sim` share the vessel (graph and face groups). Different vessels or rules need different `Sim`s;
  the rule is fixed to B45/S345 in `rule12` (a different rule is a different carry-save tail, a few lines).
- Events are per replica: kind 1 = some face group's OR is 0 (any of up to 8 groups; for O_h vessels the one
  representative face), kind 2 = period 1 or 2. Anything else (a population threshold, a hash for long periods) needs
  a new reduction in phase C of `kernel_shared.cuh`.
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
- Budget: $30/month of Modal credits. `modal billing report --for "this month" --show-resources` shows the spend.
