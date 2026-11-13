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

Semantics of both kernels: every replica is stepped exactly (B45/S345 on the vessel graph; outside the vessel is dead
forever by T2). After every generation, a replica whose initial-hull face layer (any of the 8; for O_h vessels, the
one representative face) is extinct gets a kind-1 event at that generation, one that is unchanged from two generations
back (period 1 or 2) a kind-2 event; it is then frozen (state forced to 0) until the host reseeds it. Longer periods
are not detected. Events are exact to the generation; face extinction is permanent (T2), so it is never missed.

## Correctness [measured]

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

## Running on Modal from this environment

- `input-plane.us-east.modal.com` had to be added to the environment's allowed hosts for `modal run` (done
  2026-11-13). Function results larger than a few MB come back through a CloudFront blob host that is **not**
  allowed; `facelaw.py` therefore returns a compact summary (exact per-T0 aggregates, age-binned deaths and exposure,
  raw death ages only if < 50,000). Keep other results small too.
- Several `modal run`s started within seconds of each other hit "App create rate limit exceeded"; stagger them.
- Budget: $30/month of Modal credits. `modal billing report --for "this month" --show-resources` shows the spend.
