# Review of GPU pull request 18: empty patches on a large living face

Adversarial review, 2026-11-14. Object: branch `origin/claude/awesome-cray-boq9vz`, commits 312b0bc (forecast),
d6a5e71 (history record, tree unchanged), 70482e0 (code), fcb3f39 (data, README, outcome): `research/gpu/patches.py`,
`modal_app.py`, `jobs.py`, `research/data/gpu_patches/patches_s81{1,2,3}_A10G.{csv,json}`, the README section "Empty
patches on a large living face" and the `PREDICTIONS.md` entries 2026-11-14T21:25Z and 21:47Z. The GPU code was read,
not run. Scripts: `research/audit/gpu_pr18/` (bulk output in `research/scratch/pr18/`, git-ignored).

    python3 research/audit/gpu_pr18/engine_check.py      # pc.c stepper vs the engine (3 seeds, T = 1, 7, 300, 1000)
    python3 research/audit/gpu_pr18/brute_check.py       # pc.c patch counts vs a numpy count from the cell sets
    research/audit/gpu_pr18/runs.sh                      # CPU ensemble, 1 core, ~65 min (2 x 512 replicas x 3e6 gens)
    python3 research/audit/gpu_pr18/compare.py research/scratch/pr18/run_s9*.tsv -- research/data/gpu_patches/patches_s81*_A10G.csv
    python3 research/audit/gpu_pr18/recompute.py research/data/gpu_patches/patches_s81*_A10G.csv

@@BODY@@
