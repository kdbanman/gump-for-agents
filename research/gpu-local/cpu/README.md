# research/gpu-local/cpu — a CPU face-torus runner (second code for ln tau_face)

`fr.c` (C, gcc) + `fr.py` (build, vessel export, validation, runs, summary). Shares no code with the GPU kernel or
its drivers; the vessel is `research/shape/tslab.py`'s `tslab(a, kk, b, m)` (cells, neighbour graph).

## What it computes

256 lanes per thread (W = 4 words of 64; bit-sliced, AVX2 vectors). Each lane runs successive lives from fresh
density-0.4 soups (all nodes, from generation 0). Every generation, on the state after the step:

- kind 4, transverse firewall: some transverse diagonal with >= 3 layers has three cyclically consecutive dead
  layers (permanent, AUTOMATON.md T3); also a face death in the same generation (ties go to the firewall, as in
  `fwslab.py`/`eqtorus.py`: a face death on a firewalled state is kind 4);
- kind 1, face death: layer t = 0 or t = m - 1 has no live cell;
- kind 2, period 1 or 2: state(g) = state(g - 2); after a reseed state(g - 1) := the soup (as the GPU's reseed);
- kind 3, longer cycle: state(g) equals one of three snapshots of the same life (taken at global generations that
  are multiples of 2^10, 2^14, 2^18; set to the soup at reseed), compared every generation.

A life ends at its first event and the lane is reseeded in the same generation, so exposure = lanes x generations
exactly. ln tau_face = ln(2E/F) +- 1/sqrt(F). Differences from `eqtorus.py` (all in the direction of a cleaner
definition, none affects which lives are face deaths except through firewall timing): firewalls are detected when
they form, not at the next launch boundary; cycles of period 3..2^18 are caught within 2^(k+1) + P generations
(GPU: kind 3 for P <= 128 at the next launch start, the guard for longer ones, with latencies up to P launches).

Seeds: thread t of a run uses seed SEED0 + t (xoshiro256** from splitmix64); `run` refuses seeds already in the csv.
Each thread appends one csv row per chunk (default 15 min, <= 20): counts within that chunk; lives continue across
chunks, so rows add. Process priority: below normal (set by fr.exe itself).

## Commands (from the repository root; P = C:\Users\kdbanman\.venvs\gump-gpu\Scripts\python.exe)

    P -u research/gpu-local/cpu/fr.py build
    P -u research/gpu-local/cpu/fr.py step A KK B [m=8] [gens=2000]
    P -u research/gpu-local/cpu/fr.py events A KK B GENS SEED
    P -u research/gpu-local/cpu/fr.py bench A KK B [m=8]
    P -u research/gpu-local/cpu/fr.py run A KK B HOURS SEED0 [m=8] [threads=4] [chunk=15]
    P -u research/gpu-local/cpu/fr.py summary [A KK B [m=8]]

Rows: `research/data/gpu_local_cpu/fr_A_KK_B_mM.csv`. Binary and scratch: `research/scratch/gpu-local-cpu/`.

## Validation

2026-11-17 [measured]; logs in `research/scratch/gpu-local-cpu/` (not kept).

- **Stepper = engine, every generation** (`fr.py step A KK B [m=16]`): a 0.4 soup tiled into the engine's cubic
  Nt-torus (tslab.validate's construction), `gump run --trace`, each engine cell reduced to its slab node (engine
  state required lattice-periodic); fr.c's production step, 2,000 generations, 3 engine soups x 3 lanes each (lanes
  0, 63, 64, 100, 127, 128, 129, 200, 255; the other lanes random): all equal on (1,4),(0,21) x8 and x16,
  (1,4),(0,28), (1,17),(0,32), (4,0),(0,4). Negative controls (next generation; one node flipped): 300 of 300
  generations differ on each.
- **Events, life by life** (`fr.py events A KK B GENS SEED [m=M]`): an independent numpy implementation (counting
  rule, its own face lists and ring layers from the cells, the same definitions, every generation) steps lanes 0-127
  from fr.c's soups (dumped at each reseed) and must end the same lives at the same generations with the same kinds:
  IDENTICAL on (4,0),(0,4) x8 (100k gens, 1,382 lives: 1,250 face, 3 firewall, 1 settled), (2,0),(0,8) x8 (50k gens,
  2,974 lives: 980 face, 1,866 firewall), (2,0),(0,2) x4 (40k gens, 320,534 lives incl. 6,549 kind 2, 228 kind 3,
  10,472 kind 4) and (3,0),(0,3) x3 (68,848 lives, 405 kind 3, 56,811 kind 4). Negative control (numpy tests faces
  every 2nd generation): differs on all four.
- **4 x 4 calibration** (`fr.py run 4 0 4 0.0833 1000 threads=3 chunk=5`): ln tau_face = **9.9252 +- 0.0006**
  (3,009,239 face deaths; chi2 1.5 on 2 seeds) against the pooled 9.9249 +- 0.0003 (README one level up): +0.5 sigma.

- **63-cell calibration** (1,4),(0,21): x8, `fr.py run 1 4 21 0.1333 2000 threads=4 chunk=8` and the same with
  seed 2010: **13.1607 +- 0.0017** (361,543 face deaths, 8 seeds, chi2 10.6 on 7; GPU 13.1622 +- 0.0007: -0.8 sigma;
  the first 4 seeds alone read 13.1576 +- 0.0021). x16, `fr.py run 1 4 21 0.25 2100 m=16 threads=4 chunk=15`:
  **13.1619 +- 0.0025** (156,800 face deaths, chi2 4.1 on 3).

## Throughput (4 threads, while another 8-thread CPU job shared the machine)

Single thread, idle machine (`fr.py bench`): 3.7e7 (504 nodes), 2.6e7 (672), 2.3e7 (768), 1.9e7 (1008)
replica-generations/s. In the 5-minute runs with 4 threads beside the other job: 672 nodes 3.9e7 total (9.7e6 per
thread; 527 face deaths in 5 min, about 6,300 per hour); 768 nodes 3.8e7 total (9.5e6 per thread; 61 deaths in
5 min, about 700 per hour, +-13%). These rows (seeds 9000-9003) are in the csv files and count as data.

## Not checked

Lanes 128-255 against numpy (same code as 0-127); cycles of period > 2^18 (not caught: the life stays open);
the csv summary against an independent recount; behaviour under a hard kill mid-row (rows are written whole, one
fopen/fclose per row under a mutex).
