# research/phase — the chaotic state as a phase, and gump's neighbourhood in rule space

Scripts (all small; bulk output goes to `research/scratch/phase/`, `S` below). Engine `G=engine/target/release/gump`.

| script | what |
|---|---|
| `gl.py` | numpy stepper for any B/S rule on a torus, snapshot reader/writer (re-indexes by absolute cube, i.e. undoes the engine's `origin`) |
| `check_numpy.py` | `gl.step` vs engine, 5 rules, 7 gens: bit-exact |
| `soups_torus.py 64 2000 1 $S/ts64` | whole-torus soups at p0 = 0.02…0.98, every-generation density/turnover |
| `bulk.py $S/ss64_{1..4}.gump --gens 300 --out $S/bulk64.json` | neighbour-count histograms, same-orientation correlations C(r), single-cell ACF, run lengths (snapshots: `$G run --soup 0.3 --torus 64 --rng R --gens 5000 --no-halt --snapshot-out $S/ss64_R.gump`) |
| `sk.py $S/sk64.json $S/ss64_*.gump` | structure factor S(k), spherical and in 20° cones about ⟨100⟩, ⟨110⟩, ⟨111⟩ (12 snapshots of 64³) |
| `damage.py $S/damage64.npz 30 40 $S/ss64_{1..4}.gump` | damage spreading from one flipped cell |
| `front.py`, `front_planar.py $S/fplanar72.npz 72 110 4` | chaos→vacuum fronts (box seed; planar {100}/{110}/{111} fronts) |
| `survey.py torus/vessel` | rule survey (all B ⊆ {4..7} non-empty × S ⊆ {2..7}, 960 rules) |
| `rulemap.py $S/survey_torus.jsonl $S/survey_vessel.jsonl` | → `rules.csv` (one row per rule) and `../figures/phase_rulemap.png` |
| `fig_bulk.py` | → `../figures/phase_bulk.png`, `../figures/phase_spread.png` |

`rules.csv` columns: `torus` class over four whole-torus soups (24³, p0 0.15/0.3/0.5/0.7, 3000 gens:
*chaos* = still running with ≥10% of cells changing per gen; *slow* = running, <10%; *freeze*; *die*),
`rho`, `turnover` (tail means, the largest over the p0 that kept running), `basin` (C = chaos from that p0),
`med6/8/10` = median lifetime of 16 octahedral soups (p 0.35, L1 radius 6/8/10 doubled units, cap 10⁵),
`capped10`, `osc_frac` (fraction of vessel runs ending in a period > 1 cycle), `max_period`.

Results are in `research/NOTEBOOK.md` (entry "bulk phase and rule neighbourhood").
