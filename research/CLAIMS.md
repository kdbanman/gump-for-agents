# Claims ledger

The headline claims that `README.md`, `docs/WHAT-I-SEE.md`, `research/STATUS.md` and the web tour (`web/src/tour.js`)
rest on, each with where it is recorded, how to reproduce it, and how well it has been checked. Started by the
auditor on 2026-11-13 (`research/AUDIT-2026-11-13.md` has the findings); **keep it current**: when a claim is added
to the README/essay/status/tour, add a row; when a check is re-run, update its level and date.

**Tag**: as recorded — proved / measured / conjecture (forecasts are conjectures).
**Level**: **A** = independently re-derived by different code or a different agent (named); **B** = re-run by the
auditor on 2026-11-13 and matched (statistical: within the stated error); **C** = has a command, not re-run;
**D** = no way to reproduce given. "B (table)" = re-derived from the committed curated table, not from raw runs.
Commands run from the repo root; `G=engine/target/release/gump`. `check.sh` = covered by `research/check.sh`.

## Rule, engines, legacy runs

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| R1 | Oracle reproduces the original's population logs of closed cubes side 8–11 at every generation | measured | NB 11-12 first contact; AUTOMATON §4 | `python3 reference/oracle.py legacy-cube 60 --compare reference/golden/legacy_cube_side11_H60.txt` (side 11, 46 s) | B (check.sh: 8–10; `--long`: 11) | 2026-11-13 |
| R2 | Oracle also matches side 12 (24,286 gens, H = 65, odd-H seam), no torus effect | measured | STATUS "sides 8–12" | `python3 reference/oracle.py legacy-cube 65 --compare <orig>/dev/cubic_init_results/population24.txt` (5.5 min) | B | 2026-11-13 |
| R3 | Engine matches oracle state-for-state and all six legacy logs (8–13) every generation, open space and (even H) legacy torus | measured | NB 11-12 engine; README | `python3 engine/scripts/check_golden.py [LOG H …]`, `check_oracle.py` | B (check.sh; 12/13 with `LEGACY_DIR`) | 2026-11-13 |
| R4 | Lifetimes of legacy sides 8–13 are free of torus artefacts | measured | NB 11-12 engine | oracle `--compare` reports "torus divergence: None" (11, 12); engine open == torus (8,9,11,13) | B | 2026-11-13 |
| R5 | Engine ≈4×10¹⁰ cell-updates/s/core; side 13 (169,049 gens) ≈1 s | measured | README, STATUS | `python3 engine/scripts/check_golden.py <orig>/population26.txt 70` prints elapsed | B (1.05 s; 4.4×10¹⁰ in cube16 summary) | 2026-11-13 |
| R6 | Web GPU stepper bit-exact on golden logs and vs CPU stepper; 49/49 tests | measured | STATUS, NB 11-12 | `cd web && node test/run.mjs` (needs Playwright) | C | — |
| R7 | numpy `gl.py`, `rep.c`, `fl.c` (orbit-reduced) steppers are bit-exact vs the engine | measured | phase/peeling/fluct READMEs | `research/phase/check_numpy.py`, `research/peeling/validate.py`, `research/fluct/validate.py` | B (check.sh) | 2026-11-13 |
| R8 | The original's unfinished `population38.txt` is a side-19 cube (gen-1 population 12n²−36n+48 = 3696), hull radius 55 > torus half-width 50; it sat at ≈0.40 of 375k cells | measured | NB 11-12; AUTOMATON §4 table | formula: `research/audit/independent.py` (cube); density: `tail -n 1` of the log (151,620 → 0.404) | A (auditor's code) | 2026-11-13 |

## Structure theorems

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| T1 | Layer histogram of the 12 neighbours along any body diagonal: 1, 2, 6, 2, 1 | proved | AUTOMATON §3 | `python3 reference/check_theory.py`; `python3 research/audit/independent.py` | A (auditor: neighbourhood rebuilt from face geometry) | 2026-11-13 |
| T2 | No birth across a `{111}` plane (≤3 neighbours across one dead layer, ≤1 across two) ⇒ every finite seed stays in its diagonal hull; no spaceships; eventually periodic | proved | AUTOMATON §3; README 1 | same | A (auditor) | 2026-11-13 |
| T3 | Three consecutive dead layers are permanent; two are not (a gap cell can see 1+2+1 = 4) | proved | AUTOMATON §3 | same | A (auditor) | 2026-11-13 |
| T4 | Each `{111}` layer is a closed kagome automaton (6 in-layer neighbours); coupling 6 / 2+2 / 1+1 | proved | AUTOMATON §3 | same | A (auditor; kagome = every cell on exactly two in-layer triangles) | 2026-11-13 |
| T5 | Axis-aligned half-spaces do not confine; information moves ≤ one cube per generation | proved | AUTOMATON §3 | same | A (auditor) | 2026-11-13 |
| T6 | Side-n closed cube: 3n²(n+1) cells, hull radius 3n−2; side-13 hull (R = 37) has N = 27,474 cells, R = 33 has 19,686 | proved | AUTOMATON §4; OPEN-PROBLEMS 1; NB | `research/audit/independent.py` (cube, hullN) | A (auditor) | 2026-11-13 |
| T7 | Twist lemma: P = m·L, m ∈ {1,2,3,4,6}; cells fixed by the twist have period dividing L | proved | clockwork README; NB 11-13 | proof in clockwork README | A (auditor re-derived the proof; see audit §2) | 2026-11-13 |
| T8 | Threshold lemma (S5): ΔE = D − Q exactly; no O1 event from some time on ⇒ period ≤ 2 within 26N+1 steps; every period-≥3 orbit has an O1 event | proved (theory agent; not yet lead-checked) | theory/threshold.md; PROGRAM S5 | proof; `python3 research/theory/check_threshold.py`, `energy.py selftest` | A (auditor re-derived the algebra) + B (check.sh) | 2026-11-13 |
| T9 | In ≥3 layers (and 3D) there are no finite sealed sets; in 1 layer the hexagon ring (6) is sealed, in 2 layers a 36-cell set | proved (existence; minimality computer-checked in a patch) | theory/thickness.md §2 | proof; `python3 research/theory/sealed.py minsat 2 7 36` | A for Theorem 3 (auditor read and re-derived the proof); minimality C | 2026-11-13 |
| T10 | The vertex star (12 faces at a vertex) is a closed vessel; all 4,096 states settle within 3 gens, 2,750 die; 107 still lifes, 195 two-cycles; 10 / 14 classes up to symmetry | proved | NB atlas; tour; WHAT-I-SEE | `python3 research/atlas/vertex_star.py`; `research/audit/independent.py` (star) | A (lead; auditor) | 2026-11-13 |

## The chaotic phase

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| P1 | Bulk density ρ* = 0.41552 ± 0.00002 at all torus sizes | measured | NB phase; STATUS 3; README 3; tour | `$G run --soup 0.3 --torus 64 --rng 7 --gens 30000 --every 1 --lite --format csv --out F` | A (lead, 32³: 0.4152) + B (64³: 0.415516 ± 0.000003) | 2026-11-13 |
| P2 | Susceptibility χ = 3.16 ± 0.05; global-density autocorrelation −0.44, −0.10, +0.34, −0.23 | measured | NB phase | same run | B (3.158 ± 0.037; −0.44, −0.10, +0.33, −0.24) | 2026-11-13 |
| P3 | Mean field: fixed points 0.178 (unstable), 0.444 (slope −1.55); attractor a 4-cycle 0.319→0.486→0.369→0.511 (mean 0.421) | proved (calculation) | NB phase; STATUS 3 | binomial formula in NB | A (auditor's own calculation) | 2026-11-13 |
| P4 | Correlations isotropic, ξ = 0.68 ± 0.01 cube; S(0) ≈ χ | measured | NB phase; STATUS; README 3 | `research/phase/sk.py` (needs snapshots) | C | — |
| P5 | Damage from one flip spreads as a sphere, 0.83/0.87/0.85 cube/gen; 40/40 spread | measured | NB phase; STATUS; tour | `research/phase/damage.py …` | C | — |
| P6 | Planar fronts into vacuum: {100} 0.177, {110} 0.165, {111} exactly 0 cube/gen | measured ({111} = 0 follows from T2) | NB phase; STATUS 1; tour; WHAT-I-SEE | `research/phase/front_planar.py $S/fplanar72.npz 72 110 4` | C ({111}: A via T2) | — |
| P7 | O_h-symmetric states are depleted on mirror planes (≈0.31–0.35); symmetric octahedra run at ≈0.39; asymmetric confined chaos ≈0.43 with faces ≈0.51 | measured | NB phase, lead 11-12; STATUS 3; tour | `research/phase/sym.py classes …`; `$G occupancy --cube 13 --from 10000 --to 110000 --layer 33` | A (phase agent and lead's occupancy run agree) | — |
| P8 | Whole-torus soups (no faces): mean life 1.18×10³ (N = 4), 8.7×10⁵ (N = 5), none of 512 end within 10⁶ at N ≥ 6 | measured | NB peeling (bulk); STATUS 4; tour | `python3 research/peeling/torus.py 5 0.3 1000000`; or `$G ensemble --soup 0.3 --torus N --runs …` | A (phase agent 40 soups) + B (N=4: 1194 ± 53; N=5: 8.6 ± 0.8 ×10⁵ and 1.3 ± 0.2 ×10⁶ in two batches) | 2026-11-13 |

## Faces, peeling and the face law

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| F1 | The staircase is peeling: side 11 loses one layer from every face at gens 3290, 3477, 3796 after 3285 gens at R = 27; no interior firewall before the final collapse | measured | NB 11-12; tour; WHAT-I-SEE | `$G run --cube 11 --events F` | B (check.sh) | 2026-11-13 |
| F2 | Side-11 plateau heights 0.79, 0.61, 0.48 of the first vs hull-volume ratios 0.79, 0.62, 0.47 | measured | NB 11-12; WHAT-I-SEE | `python3 research/experiments/kymo11.py` | C (ratios (R/27)³ checked) | — |
| F3 | Side 13 peels at ≈130,200, 145,850, 156,800, 166,650, 168,200; ends 169,049 | measured | NB engine | `$G run --cube 13 --events F` | B (check.sh) | 2026-11-13 |
| F4 | Flat faces: τ_face = exp[(−0.09 ± 0.06) + (0.209 ± 0.002)·A], A = 27–90, residuals ≤ 0.18 | measured | NB peeling; STATUS 4; README 4; tour; WHAT-I-SEE | runs: `python3 research/peeling/slabs.py N1 N2 8 CAP`; fit: `python3 research/peeling/face_law_fit.py` | B (table: weighted refit of `slab_area.csv` gives −0.091 + 0.2088·A, `research/audit/data_claims.py`) + A (slope: fluct agent's QSD, lead's octahedra) | 2026-11-13 |
| F5 | Face waits are memoryless (CV ≈ 1, KS p 0.5–0.96 for A ≥ 36) | measured | NB peeling | `slab_area.csv` cv/ks_p columns | A (lead: CV 1.03, 0.99 on octahedra) | — |
| F6 | Octahedral faces obey the same law, 1.7–1.9× tougher (A = 45, 63, 84) | measured | NB peeling; STATUS 4 | `python3 research/peeling/octa.py 11 0.3 1000000` … | B (arithmetic on the regenerated `octa_first.csv`: 1.66, 1.66, 1.93) + A (lead: 1.6–1.9×); the old R = 9 row (1,620, CV 1.26) counted runs whose hull had shrunk before t0, fixed in `octa_hazard.py` (now 2,287, CV 1.03; engine 2,459 ± 97) — audit W3 | 2026-11-13 |
| F7 | Lead's engine-only check: R = 9 mean wait 2.60×10³ ± 0.17×10³ (221 runs), slope 0.199 ± 0.006 between R = 9, 11 | measured, **superseded** for R = 9 (fluct: 2300 ± 6; the lead's 240-run sample was a 1.7σ high draw, not a T0 effect) | NB 11-12 "independent check" (with correction notes); STATUS 4 now cites `face_endgame_check.py` (−ln h/A = 0.2183) | `python3 engine/scripts/face_law.py 9 240` | B (2599.8 ± 174.9, same seeds; 1,024 soups: 2,313 ± 75 at T0 = 60, 2,307 ± 77 at T0 = 200) | 2026-11-13 |
| F8 | A face dies off the end of its stationary tail: ln P(n = k) straight to k = 1 (ratio ≈ 0.65), h/P(1) ≈ 0.6, 62% of deaths from one cell, 23% from two | measured | NB fluct; fluct README; STATUS 4; README 4; WHAT-I-SEE | `python3 research/experiments/face_endgame_check.py 9 16000` | A (lead, engine-only) + B (3000 soups, 1 job: mean 2314 ± 45, −ln h/A 0.2184, h/p₁ 0.616, 62/23/10%) | 2026-11-13 |
| F9 | −ln h/A → I(0) = 0.2077 ± 0.0014 + 0.55/A (A = 30–84) | measured | fluct README; STATUS 4 | `python3 research/fluct/analyze_qsd.py` (needs scratch tallies) | B (table: refit of `fluct/data/qsd_summary.json`) | 2026-11-13 |
| F10 | Last ember is a kagome triangle: 38% of 3-cell faces | measured | NB fluct; STATUS; WHAT-I-SEE | `python3 research/experiments/near_death_shapes.py 9 300 1000` | C | — |
| F11 | Interior 3-layer firewall costs ≈0.12 per band cell (ln τ_fw = −1.4 + 0.54Nm + 0.22N); first event switches firewall → peel at m ≈ N | measured | NB peeling; STATUS 4 | `peeling/slab_fw.csv`; `slab_report.py` | C | — |
| F12 | A dying face is ordinary until ≈16 gens before death, plunges in 10–12; FFS gains nothing (clone fates 55–95% correlated) | measured | NB fluct; fluct README; STATUS 4 | `predeath.py`, `ffs.py`, `clone_corr.py` | C | — |
| F13 | Asymmetric soup in the side-13 hull would hold each face ~10⁴¹ gens | conjecture: extrapolation of F4 from A ≤ 90 to A = 459 (tour, README, STATUS, essay now say so) | README 5; STATUS 4; tour; WHAT-I-SEE | arithmetic: exp(−0.09 + 0.209·459) = 4×10⁴¹ | B (arithmetic) — untestable | 2026-11-13 |

## Symmetry and the closed cubes

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| S1 | O_h-symmetric faces: effective area A/7.7 (ln τ = −0.14 + 0.0272·A, A = 198–513) | measured; **superseded** beyond A ≈ 460 by S2 | NB peeling; tour ("about seven times smaller") | `research/peeling/octa_hazard.py` | C | — |
| S2 | Cube-centred O_h faces: ln τ ≈ 0.69 + (0.209/6)·A − 0.195·√A to A = 693 | measured (fit) | STATUS 4; fluct README | `python3 research/fluct/sym_fit.py` | B (table: 0.698, −0.196 from `sym_residence.csv`) + A (lead's engine batches and fluct agent's orbit stepper agree at A = 408–630) | 2026-11-13 |
| S3 | Vertex-centred (even) cubes ≈1.5× tougher at equal area (A = 360–630); 2.0 ± 0.4 at A = 693 (fresh soups only) | measured | STATUS 4; OPEN-PROBLEMS 7; NB 11-13 | `python3 research/fluct/sym_fit.py` | B for 1.5 (1.52, 1.53, 1.60, 1.49, 1.31); `sym_fit.py` prints both at A = 693: 2.02 for fresh soups only (the quoted 2.0) and 2.39 with the cube's copies pooled into the vertex value | 2026-11-13 |
| S4 | Symmetry acts by lockstep: symmetric systems live like asymmetric ones of c × (volume / order of G), c ≈ 1.5–3.5, on tori too | measured → conjecture | NB phase (symmetry); STATUS 4; README 5; WHAT-I-SEE | `research/phase/sym_torus_life.sh`, vessel ensembles | C | — |
| C1 | Closed cubes 14: 4,460,298 gens, ends period 2 (528 cells); 15: 37,367,092, extinct | measured | NB 11-12; STATUS | `research/experiments/cubes.sh 14 15` (30 s + 4 min) | B (`check.sh --long`; event logs identical to the recorded ones) | 2026-11-13 |
| C2 | Side 16 lives 2,919,617,676 gens, ends as 96 cells (12 × S8b); first peel 2,362,434,048, second 2,886,100,480; all 8 faces in lockstep | measured | NB 11-13; STATUS; README 5; WHAT-I-SEE | `research/experiments/cube_ckpt.sh 16` (days); data `research/data/cube16_*` | B (data: schedule and summary re-derived, `data_claims.py`); run itself not repeated; "12 × S8b" C | 2026-11-13 |
| C3 | The pre-run prediction for side 16 (2.4×10⁸, 90% 3.9×10⁷–6.3×10⁸) failed by ×12 | measured | NB; README 5; WHAT-I-SEE; tour | `python3 research/peeling/cubes_report.py`; `peeling/cube_lifetime.csv` | B (arithmetic; prediction in the csv) | 2026-11-13 |
| C4 | Clone forecast of the first peel (median 2.2×10⁹, 90% 1.50–5.2×10⁹) committed at 01:28:41Z, ≈2 h before the peel; outcome at its ≈58th percentile | measured | NB; fluct/PREDICTIONS.md; README 5; STATUS | `git show 2e72d57`; `python3 research/fluct/predict.py …` | B (commit time and arithmetic; the peel's wall-clock time C) | 2026-11-13 |
| C5 | Second peel: fit-only forecast inside (95th pct); clone forecast (τ = 8.2×10⁷) missed; the cube stayed 7.4 pooled means at R = 40 (P = 6×10⁻⁴) | measured | NB; PREDICTIONS.md; STATUS; WHAT-I-SEE | `python3 research/experiments/cube_vs_ensemble.py` | B (arithmetic, csv) | 2026-11-13 |
| C6 | Cube lineages over-dispersed vs memoryless ensembles: 3 of 16 large plateaus > 4 means (P = 0.003), sum 27.2 vs 16 (P = 0.008) | measured → conjecture | NB 11-13; STATUS; OPEN-PROBLEMS 6; WHAT-I-SEE | `python3 research/experiments/cube_vs_ensemble.py` (needs `research/scratch/cubes/ev13–15.jsonl` from `cubes.sh`) | B (arithmetic and the 16 ratios); **method finding**: P ≈ 0.18 without side 16 | 2026-11-13 |
| C7 | Cubes n = 11–15 sit at quantiles 0.37, 0.45, 0.33, 0.93, 0.73 of the symmetric-law predictions | measured | NB peeling; STATUS 4 | `python3 research/peeling/cubes_report.py` | C (values in `cube_lifetime.csv`) | — |
| C8 | R = 42 is an ordinary size: fresh vertex O_h soups τ = 7.1×10⁸ (45 deaths) | measured | NB 11-13; STATUS | `QSD_SALT=xa python3 research/fluct/qsd.py sym 42 v 3500 1 lite` (1 h each) | C (pooled value re-derived from csv: B) | 2026-11-13 |
| C9 | Side 17 first plateau forecast ln τ = 24.0 ± 0.4 (mean 2.6×10¹⁰; first-peel median 2×10¹⁰) | conjecture (forecast) | PREDICTIONS.md; STATUS; WHAT-I-SEE; OPEN-PROBLEMS 8 | `python3 research/fluct/sym_fit.py` | B (fits give 23.74–24.23 at A = 828) | 2026-11-13 |
| C10 | Side-19 legacy cube properly confined would last 10¹³–10¹⁴ (essay, tour and NB now agree) | conjecture (extrapolation) | WHAT-I-SEE; tour; NB 11-12 | `python3 research/fluct/sym_fit.py` (prints ln τ = 31.0–32.1 at A = 1053) | B (arithmetic) | 2026-11-13 |

## Fauna and clockwork

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| Z1 | Smallest still lifes have 6 cells; exactly 4 classes | proved (exhaustive) | NB atlas; WHAT-I-SEE | `$S/sl 16 -s` | A (auditor: own enumeration finds no still life of 4–5 cells and 21 rooted 6-cell ones = 1+4+4+12 orientations) + B | 2026-11-13 |
| Z2 | Strict still lifes n = 6…16: 4, 2, 7, 9, 27, 45, 228, 851, 3388, 12255, 47578 | proved (exhaustive) | NB atlas | `$S/sl 16 -s` (30 CPU-min) + `still_stats.py` | B for n ≤ 13 (`sl 13 -s`, 19 s); 14–16 C | 2026-11-13 |
| Z3 | Period 2: smallest union 9; classes by union 9–13: 3, 6, 4, 11, 10; all with union ≤ 11 are hinge flips | proved (exhaustive) | NB atlas; tour | `$S/osc 2 13` (11 min) | B for union ≤ 11 (`osc 2 11`, 21 s: 3, 6, 4); 12–13 and the flip property C | 2026-11-13 |
| Z4 | No p3 with union ≤ 12, no p4 with union ≤ 10; smallest p3 union exactly 13 | proved (exhaustive) | NB atlas | `$S/osc 3 12` (20 min), `osc 4 10` | C | — |
| Z5 | Soup ash periods 1–16, 20, 22, 48, 66 (26,900 octahedral soups) | measured | NB atlas; README 6 | `python3 research/atlas/harvest.py …` | C | — |
| Z6 | P66.27a: a 45-cell box filled completely; phase t+33 = mirror image of phase t; per-cell periods 66 (40), 33 (3, the mirror line), 1 (2) | proved | NB 11-13; clockwork README; README 6; WHAT-I-SEE | `python3 research/clockwork/verify.py …` | A (lead's set stepper; auditor's `research/audit/clockwork_check.py`) | 2026-11-13 |
| Z7 | Every twist order occurs: C48.24a 48 = 6×8 (screw), C36.33a 36 = 4×9, C12.43a 12 = 6×2, C40.24a 40 = 2×20, P15.22a 15 = 3×5, P48.34a 48 = 2×24 | measured | clockwork README; NB; README 6; STATUS 5; tour | `python3 research/clockwork/portrait.py …` (search); facts: `research/audit/clockwork_check.py` | A (lead; auditor) | 2026-11-13 |
| Z8 | 249 of the 9,700 census objects are compound (no cell of full period), e.g. C44.26a = 4 with 11 | measured | NB; clockwork README; STATUS 5; WHAT-I-SEE | `python3 research/experiments/census_twist.py` (7 s; needs `research/scratch/clockwork/census_3_objects.json`) | A (C44.26a: auditor) + B (count) | 2026-11-13 |
| Z9 | Twisted loops are a steady 3–8% at every quotient length; the longest plain loop is C35.29a (L = 35, 37 of 47 cells full period) | measured | NB; STATUS 5; WHAT-I-SEE | same | B (295/9278, 30/670, 9/120, 5/66) + A (C35.29a: auditor) | 2026-11-13 |
| Z10 | P66.27a: basin 4.1×10⁻⁴ in its own box; 6,600 flips → 30% heal, 43% broken by a lone outside cell, 5 of 2,001 heals phase-shifted | measured | clockwork README; NB; WHAT-I-SEE | `python3 research/clockwork/portrait.py P66.27a 1000000`; `perturb.py P66.27a` | C | — |
| Z11 | Legacy ash: side 9 = central cube + 8 kagome hexagons (54 cells); side 11 = 6 cubes at the octahedron vertices (36) | measured | NB atlas; tour | `python3 research/atlas/legacy_ash.py` | C (final populations B via golden logs) | — |

## Thickness, kagome, rule space

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| K1 | One or two `{111}` layers cannot sustain chaos (lifetimes ∝ log area: m = 1: 4.6–11.9, m = 2: 44–101); three can (ln τ linear in N) | measured | NB atlas; README 2; STATUS 2; tour; WHAT-I-SEE | `python3 research/atlas/thickness.py N m NSOUPS 0.4 SEED` | C; T9 gives the proved geometric counterpart | — |
| K2 | Thin slabs die by a transverse T3 firewall (30/30 soups at m = 3, 4) | measured | NB atlas; tour | `python3 research/atlas/slab_firewall.py 5 3 30 0.4 31` | C | — |
| K3 | The one-layer automaton has oscillators of periods 3–12 (so no energy proof of freezing) | measured (oracle-verified objects) | theory/thickness.md | `kagome_osc.json`, `lattice.oracle_verify` | C | — |
| Q1 | 960-rule survey: 421 rules chaotic on tori; 146 long-lived in vessels (142 with 4 ∈ B); gump median 3420, a minimal element (one of 50): removing any one count collapses it (104, 21, 20, 22, 36) | measured | NB phase; README 7; STATUS 6; tour | `research/phase/survey.py`, `rulemap.py` (hours) | B (table: `rules.csv`, `data_claims.py`) | 2026-11-13 |
| Q2 | Adding S2 or S7 extends lifetimes ≥30× | measured | STATUS 6; tour | `rules.csv` | B (table) — the medians are at the 10⁵ cap: ≥29× | 2026-11-13 |
| Q3 | B45/S3457 grows ~100× per radius step: medians 79, 3.5×10⁴, ≥10⁶ at R = 6, 8, 10 | measured | NB phase; WHAT-I-SEE; OPEN-PROBLEMS 15 | `$G ensemble --soup 0.35 --radius R --runs 16 --rule B45/S3457 --gens 1000000 --hash-window 65536` for R = 6, 8, 10 (the NB's command says radii 5, 7, 9) | B (79, 34,970, all 16 running at 10⁶) | 2026-11-13 |
| Q4 | Birth at 3 breaks confinement (B3x/S345 invade vacuum across `{111}`) | measured | NB phase; WHAT-I-SEE | `survey.py` / ensembles | C (consistent with T2's hypothesis min B ≥ 4) | — |

## Added after the first audit

| id | claim | tag | where | reproduce | level | checked |
|---|---|---|---|---|---|---|
| G1 | 2D gump: B34/S234 on the range-2 cross has memoryless edge death with ln τ_edge = 0.73 + 0.416·L (L = 12–36) | measured | NB 2026-11-13; toy2d README | `research/toy2d/` (`law.py`, `analyze.py`) | A (lead's own stepper, L = 12–24: slope 0.42; `python3 research/experiments/toy2d_check.py 12 16 20 24`) | 2026-11-13 |
| G2 | 2D toy: box confinement, T5 and no finite sealed set | proved | toy2d README | `python3 research/toy2d/structure2d.py` | C (lead re-derived confinement and the 3-row firewall by hand only) | 2026-11-13 |
| G3 | 2D toy: mirror symmetry multiplies the slope by 0.42, full square symmetry by 0.50; four-fold rotation also shortens life (forecast failed) | measured | NB 2026-11-13; toy2d PREDICTIONS | `research/toy2d/` | C | — |
| G4 | No capped-threshold Moore rule sustains confined chaos; 93 of 711 long-lived Moore rules die edge by edge | measured | toy2d README | `research/toy2d/` | C | — |

## Counts (2026-11-13)

71 claims: **A** 25 (alone or with B) · **B** 25 · **C** 20 · **D** 1. Two are marked superseded (F7, S1) and
one has a method problem (C6). Details and the open items are in `research/AUDIT-2026-11-13.md`.
