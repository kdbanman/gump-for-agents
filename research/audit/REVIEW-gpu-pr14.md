# Review of PR 14: firewall-resolved slab faces (GPU round two, rerun)

Branch `origin/claude/awesome-cray-boq9vz` (2f9b262, 37bf879, 3fa1bf5): `research/gpu/README.md`,
`research/gpu/PREDICTIONS.md`, five `research/data/gpu_facelaw/fwslab*.json`. Code: `research/gpu/fwslab.py` (on main,
unreviewed until now). Reviewer's scripts: `research/audit/gpu_pr14/`. Date 2026-11-14.

## Verdicts

| claim | verdict |
|---|---|
| 1. Validation at 3×6×8 and 4×7×8 | **stands, with a correction** (wording of the direction count; the 3×6×8 share is not a deficit) |
| 2. Production 6×7×8: 92 / 29, ln τ_face = 26.405 ± 0.104, ln τ_fw(216) = 26.866 ± 0.186, forecasts hit | **stands** |
| 3. Control 6×6×8, pooled A = 108, slope 0.215 ± 0.006 "not decided" | **numbers stand; the reading needs a correction** ("leans toward a mild rise" is not supported over a shape effect; the README's ln τ_fw column mixes per-slab and per-direction rates) |

Reproduce everything below with:

    B=origin/claude/awesome-cray-boq9vz; mkdir -p research/scratch/pr14
    for f in fwslab3x6x8_s601_A10G fwslab4x7x8_s602_A10G fwslab6x6x8_s621_A10G fwslab6x7x8_s611_A10G fwslab6x7x8_s612_A10G; do
      git show $B:research/data/gpu_facelaw/$f.json > research/scratch/pr14/$f.json; done
    python3 research/audit/gpu_pr14/recompute.py research/scratch/pr14       # every table number, from raw where it exists
    python3 research/audit/gpu_pr14/cpu_channels.py validate 3 6 8 3000      # rep.c on the skewed slab vs the engine
    for s in $(seq 14002 14007); do taskset -c 3 python3 research/audit/gpu_pr14/cpu_channels.py run 3 6 8 400000 $s 64; done
    python3 research/audit/gpu_pr14/cpu_channels.py analyze 3 6 8            # independent channel-resolved CPU check
    python3 research/audit/gpu_pr14/shape.py                                 # face channel residuals by shape

RESULTS_PLACEHOLDER
