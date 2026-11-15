# research/gpu-local — results on the owner's GTX 1080

Tags as elsewhere: **[measured]** (with the command that reproduces it), **[conjecture]**. Agents: read `AGENT.md`
first. Commands run from the repository root with the venv python of `AGENT.md`
(`python` below), after `python -u research/gpu-local/acceptance.py cases`.

## Correctness on this card [measured]

All acceptance checks of `research/gpu/README.md` "Correctness" were ported to a local runner that calls the same
`check.*` functions with the same arguments as the Modal entry points (`research/gpu-local/acceptance.py`, one group
per entry point). Reference cases rebuilt here with the Windows build of the engine; the settle-test set again has
253 cycles of period 3-66 and 120 others, as on the machine that built the originals.

| group (Modal entry point) | what | result |
|---|---|---|
| `every` (`check_every`) | engine every generation, 5 cases × 5 lanes, 2,000-3,000 gens; kernel B default, kernel B J=3 WB=2 blocks=6, kernel A | all equal |
| `every` | negative controls (engine one generation later; deepest node flipped) | every case fails from generation 1, as required |
| `periodic` (`check_periodic`) | settle detection on the 373 engine-run soups, pw = 128, 32, 1024, and a non-default shape | all as expected (pw = 32: the period-48 and -66 soups unflagged) |
| `patches` (`check_patches`) | 12 × 12 × 8 slab every generation (2 seeds); patch counter vs brute force on 24 states | all equal / identical |
| `check` (`check_remote`) | final states vs the engine (3 kernel shapes); vs `fl.c` every 250 gens and face-death generations, R = 7, 9, 13 | all equal, event generations identical |
| `defaults` (`check_defaults`) | production shape on R = 13-17 vs `fl.c`, sparse soups; reseed (2 kernels) | all equal |
| `keep` (`check_keep`) | K_KEEP vs `fl.c` | all equal |
| `slab` (`check_slab`) | 11 × 11 × 8 slab every generation vs the engine; 6 × 6, 6 × 7 slabs vs `fl.c` | all equal |
| `cpu` (`check.py all cpu`) | the CPU build of kernel A (`cpu.c`) vs the engine and `fl.c` | all equal |

Commands: `python -u research/gpu-local/acceptance.py every periodic patches` (about 2.5 min on this card) and
`python -u research/gpu-local/acceptance.py check defaults keep slab cpu` (needs gcc on PATH; about 5.5 min).
`fl.c` and `cpu.c` were built with MinGW-w64 gcc 16.2 (`-O3`/`-O2 -march=native -shared -fPIC`, a DLL under a `.so`
name). Not checked here: the Modal entry points themselves (unchanged; they need Modal), and `check_engine_every` for
kernel A on the CPU beyond what `cpu` runs.

## Throughput and shared-memory fit [measured]

`python -u research/gpu-local/bench_local.py` → `research/data/gpu_local_bench/bench_shared_GTX1080.jsonl` (every row;
same 12 kernel-B shapes per vessel as `modal_app.SHARED_CONFIGS`, and kernel A at three widths). Node-updates/s:

| vessel (nodes) | kernel B, gsim defaults | kernel B, best shape | kernel A | A10G kernel B (on file) |
|---|---:|---:|---:|---:|
| asym R = 15 (2,064) | 7.2 × 10¹¹ | 7.5 × 10¹¹ (WB 2, J 3) | 7.4 × 10¹⁰ | 2.4 × 10¹² |
| asym R = 19 (4,020) | 7.8 × 10¹¹ | 8.6 × 10¹¹ (WB 1, J 4) | 7.3 × 10¹⁰ | 2.5 × 10¹² |
| O_h vertex hull 45 (1,366) | 7.5 × 10¹¹ | 9.1 × 10¹¹ (WB 2, J 2, 2 blocks/SM) | 7.7 × 10¹⁰ | 2.7 × 10¹² |
| slab 6 × 6 × 8 (864) | 6.4 × 10¹¹ | 1.0 × 10¹² (WB 4, J 2, 2 blocks/SM) | 7.4 × 10¹⁰ | |
| torus (1,5),(0,31) × 8 (744) | 6.3 × 10¹¹ | 9.7 × 10¹¹ (WB 2 or 4, J 2, 2 blocks/SM) | 7.5 × 10¹⁰ | |

- Kernel B here is about a T4 (8.7-9.4 × 10¹¹ on file) and 30-40% of an A10G. Kernel A is a third of a T4's.
- **Two blocks per SM (`minb=2, blocks=40`) help on this card for vessels under about 1,400 nodes** (+50% on the
  slabs), where on the A10G they did not; for 2,064 nodes and more they spill registers and lose up to 4×.
  The torus runs use WB 2, J 2, 2 blocks/SM (`eqtorus.sim_cfg`; with K_KEEP: 1.29 × 10⁹ replica-generations/s at
  A = 93, 2,560 replicas, no spills; `python -u research/gpu-local/eqtorus.py tune 1 5 31`).
- **Fit in 48 KB per block:** kernel B needs 4·WB·(n + 31) bytes, so WB = 1 holds n ≤ 12,257 nodes, WB = 2 n ≤ 6,113,
  WB = 4 n ≤ 3,041 (R = 19 with WB = 4 is refused: 64,816 bytes). gsim's default WB already adapts to the card's
  limit. Two blocks per SM need 2 × that within 96 KB per SM, the same bound.
- `bench.bench_gpu` (used by `modal_app.bench`) no longer measures kernel A: `gsim.Sim`'s default kernel on the GPU is
  B, which ignores `WT`. `bench_local.bench_global` passes `kernel='global'`.

## The torus driver, calibrated on 4 × 4 [measured] — and a disagreement with the value on file

`research/gpu-local/eqtorus.py`: `fwslab.py`'s driver for any lattice (a, k), (0, b) of `research/shape/tslab.py`,
with the guard. `eqtorus.py check A K B` = `tslab.check`, then the GPU against the engine every generation (the torus
tiled into the engine's cubic torus; engine cells reduced to torus nodes, the engine state required to be
lattice-periodic), in the shape the runs use, gsim's default shape and kernel A, with the two negative controls.
Passed for (1,5),(0,31) and (4,0),(0,4): 2,000 generations × 5 lanes × 3 kernels all equal, controls fail from
generation 1.

Calibration on the 4 × 4 torus (A = 48; on file 9.9324 ± 0.0020, 247,338 face deaths, `research/shape2/data/A48.csv`,
CPU, cap 16,384): `python -u research/gpu-local/eqtorus.py run 4 0 4 3 48002 max_launch=2048 raw_cap=20000000`

| | this card | on file (CPU) |
|---|---:|---:|
| face deaths | 7,478,823 | 247,338 |
| ln τ_face = ln(2E/F) | **9.9251 ± 0.0004** | 9.9324 ± 0.0020 |
| the same, lives censored at age 10,000 / 17,783 / 31,623 | 9.9237 / 9.9247 / 9.9249 | (cap 16,384) |
| hazard of a face death by age, ×10⁵ per generation | 12.47 (0-60), then 9.76 to 9.79 in every bin from 60 to 100,000 | |
| ln τ_fw, fwslab's convention (face death on a firewalled state) | 15.384 ± 0.008 | 15.128 ± 0.038 |
| ln τ_fw, also counting lives that settle on a firewalled state | 15.189 ± 0.007 | |

- **ln τ_face differs by 0.0073, 3.6σ of the file's error.** The hazard here is flat in age, so the file's cap does
  not explain it; the stepper is bit-exact against the engine on this torus. Not resolved: a CPU cross-check with the
  repository's own pipeline is running. Until it is, the 4 × 4 anchor of `research/constant/PREDICTIONS.md` part C
  should be read with this in mind (0.007 is larger than several of the planned errors there).
- **`fwslab.py` undercounts firewalls where lives can settle.** A firewalled slab often settles (period 1-2) before a
  face dies; the kernel then reports kind 2 and the driver keeps it as "settled". Here 3,420 of 5,023 settled lives
  were on a firewalled state: 18% of all firewalls, and ln τ_fw moves by 0.20. `eqtorus.py` counts them
  (`fw_settled`); ln τ_face is unaffected (both kinds are censored for it).
- **Launch length matters when lives are short.** The first calibration run (launches up to 2¹⁸ = 26 mean lives) had
  39 lives that sat to a launch boundary (firewalled without a face death, or in a cycle of period 3-128, which
  kernel B only recognises at the next launch start): 0.16% of the exposure, +0.0016 on ln τ. The cap `max_launch`
  must stay well below the mean life (the queued tori have mean lives ≥ 10⁷, so 2¹⁸ is safe there).

## The cycle guard [measured]

`research/gpu/guard.py`, hooked into `facelaw.run(..., guard=FIRST)`; off by default (`guard=0`), and with the guard
off the driver's code path is the previous one. Rule (`research/gpu/AGENT.md` "To do", option (i)): one snapshot per
replica, taken at the first launch boundary at which its age is ≥ FIRST · 2^j, j = 0, 1, …; at every launch boundary a
live replica equal to its snapshot ends as **kind 5** (censored, like kinds 2 and 3), at the boundary generation.
Results with the guard state the thresholds (`out['guard']`: `first`, and per kind-5 life the replica, the age at
recognition and the snapshot's age).

Tests, `python -u research/gpu-local/guard_test.py all` (about 3 min):

- **Planted cycles, exact.** The 373 engine-run R = 9 soups (cycle start c and period P from `gump ensemble`, P = 1 to
  66), tiled over all 1,280 lanes, faces off, the kernel's own freezing off. Two states at generations s < b are equal
  iff s ≥ c and P | (b − s), so the guard's detection boundary is a function of (c, P, boundaries, thresholds),
  computed in plain Python (`predict`). Launch lengths 1024, 1000, 997 (prime) and a mixed cycle 997, 1024, 4096;
  FIRST = 16 and 1000: **every lane recognised exactly at the predicted boundary** (8 settings × 1,280 lanes).
- **As in production** (freezing on, pw = 32, K = 1000 and 4096): the 7 lanes holding the period-48 and -66 soups end
  as kind 5 exactly at the predicted boundary; the other 1,273 end by the kernel (kind 2 at c + 2, kind 3 at L + P,
  as `check_periodic` requires) and none as kind 5.
- **Negative controls** (each must fail the exact test): snapshot taken before the comparison (1,280 lanes wrong),
  comparison with the neighbouring column's snapshots (1,277 wrong), thresholds that never double (1,082 wrong):
  all caught.
- **Guard on vs off, same seed, fixed launch length and generation cap** (`facelaw.run(..., launch_gens=K,
  max_gens=G, keep_reps=True)`): lives (age, kind, birth, replica) equal lane for lane on R = 15 (2^20 gens), R = 9
  (2^21 gens, 979,357 lives; also with pw = 32 and pw = 1), R = 11 (pw = 16, K = 997, FIRST = 1000). No kind-5 life
  occurred in these runs: at R = 9-11 a face dies long before a soup settles into a long cycle.
- **The driver's kind-5 path, on natural cycles** (R = 9, faces off, pw = 1, so a life ends only by settling and the
  kernel recognises only periods 1-2): 7,851 lives recognised by the guard in 2^19 generations; guard off, the same
  lanes are held to the end by those cycles (19,260 lives against 125,107). 1,272 lanes agree exactly up to their
  first kind-5 life, and guard off that life (same birth) is still running at the age the guard ended it.

**A guarded run is not bit-identical to an unguarded one after the first kind-5 life.** The drivers draw each reseed
from (seed, a counter that advances at every boundary where some life ended). The first time the guard ends a life at
a boundary where the kernel ended none, the counters part and every later soup differs (same distribution, different
draws). The test above compares lives born before that boundary. A run with no kind-5 life is bit-identical to the
unguarded run.

**Detection latency (a property of option (i), measured in the exact test).** A replica that enters a cycle of
period P at age e is recognised at the first boundary b with a snapshot s on the cycle (s ≥ e) and P | (b − s).
Two delays add:
- *Snapshot delay* s − e: snapshots are taken at doubling ages, so s − e is up to about e (+ one launch). A life
  that settles at age e can therefore stay unrecognised for up to about e more generations.
- *Grid delay* b − s: comparisons happen only at boundaries, so b − s runs over the launch grid. With a fixed launch
  length K a match comes within lcm(K, P) of s; if the snapshot interval is shorter than that, the next (doubled)
  snapshot is needed. In the test, horizon 2^17 left 4-25 lanes unrecognised for K = 997 or mixed launches (as the
  prediction said), 2^19 found all. The drivers' launches are powers of two (K doubles from 1024), so for odd P
  (the clockwork objects' 9, 11, 13) the grid delay is P launches, about P × K generations.
So the guard turns zombie exposure from "until the run ends" into "at most about the settling age plus P launches"
per recognised life. Both terms are bounded per life by what is recorded: zombie time ≤ b − birth, and the
snapshot age shows how much of it can be grid delay. Not removed: lives still open at the end of a run.

**[conjecture]** For the measurements queued (τ ≈ 10^8-10^10 generations, launches of 10^5-10^6 generations on this
card), both delays are small against a mean life except the snapshot delay of lives that settle very old. If kind-5
lives turn up in numbers, exact entry ages can be recovered offline: every life is a deterministic function of
(seed, reseed round, replica), so it can be re-run from its birth.
