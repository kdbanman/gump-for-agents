# The 4 x 4 torus on the CPU: research/shape2's pipeline rerun, and its counting rule against the GPU's

Why this exists: `research/gpu-local/README.md`, "The torus driver, calibrated on 4 x 4". Written by a subagent of the
GPU session (2026-11-15); results in `results_fresh.txt`, `results_orig.txt`, `results_adj.txt`.

Build (no tracked file is changed; `rep.c` is the repository's, `rep_cyc.c` is a copy with an any-period cycle
detector and two extra output columns): from the repository root, with gcc on PATH,
`gcc -O3 -march=native -o research/gpu-local/cpu4x4/rep.exe research/peeling/rep.c` and
`gcc -O3 -march=native -o research/gpu-local/cpu4x4/rep_cyc.exe research/gpu-local/cpu4x4/rep_cyc.c`.

- `w.py`: `research/shape/tslab.py` with its paths redirected here (`w.py validate 4 0 4 3000 12`, `w.py run ...`,
  `w.py stats 4 0 4`, `w.py raw ...` for per-generation output from `rep_cyc`).
- `drive_orig.py 0 76 3`: the 76 jobs of the repository's row (seeds 1,008,000..075); reproduces
  `research/shape2/data/A48.csv` "4 0 4" exactly. `drive.py 0 1024 10`: 1,024 fresh jobs (seeds 7,700,000..);
  `drive_adj.py 0 304 3`: seeds next to the originals. Third argument: parallel processes.
- `an.py out raw`: ln(2E/F) under the repository's rule (ends in 16-generation windows) and under the GPU's
  (per generation), hazards by age, cycles. `xtab.py`: the cross-table of life kinds under the two rules.
- `detcheck.py 200 16384 99`: last-alive of every layer against an independent numpy stepper.

Per-life output (`out*/`, `raw*/`, some GB) is not kept in git.
