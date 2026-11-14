# Where the face-law exponent comes from

*Exponent study. Runs, forecasts and theorems by the exponent agent, 2026-11-13 (stopped by a usage limit before
writing this report); report written 2026-11-14 by a successor from the files it left, with the re-runs marked
below. The author's unfinished section drafts survive in `research/scratch/exponent/body_*.md`; their text is used
here where it checked against the records. PROGRAM nodes M1–M4, E2; OPEN-PROBLEMS items 3–4.*

*Tags: **[proved]** — argument in `exponent/theorems.md`; **[exact]** — exact numerics (enumeration or power
iteration, no sampling); **[measured]** — sampled, with n, error and command; **[conjecture]**. Commands run from
`research/theory/exponent/`; bulk output in `research/scratch/exponent/` (git-ignored; present on 2026-11-14),
curated numbers in `exponent/data/`, forecasts and scores in `exponent/PREDICTIONS.md` (append-only, committed
before the runs). "Toy" = the 2D rule B34/S234 on the range-2 cross (`research/toy2d`); its edge is a row of L
cells, periodic. "Truth" for the toy = deterministic strips 16 × L measured here; for gump = `research/fluct`
(octahedral faces) plus periodic slabs measured here. ln τ errors are 1/√deaths. τ is always a hazard among living,
unsettled, uncut replicas older than T0 (board, "Definitions"), not a mean over initial states.*

## Verdict

The question has no complete answer in this material. What it supports:

1. **[measured]** **The exponent is set by a thin boundary layer over a memoryless reservoir.** Keep the rule on the
   top w rows (toy) or {111} layers (gump) and replace everything beneath by fresh coin flips every generation: with
   w = 8 (toy) and w = 4–5 (gump hull faces; w ≥ 5 for periodic faces) the lifetimes agree with the deterministic
   systems to ≤ 0.05 nats over L = 12–28 (toy), A = 45–63 (hull faces; A = 30 is 0.25 low, that hull has no bulk) and
   A = 27–60 (periodic faces), with 2,000–13,000 deaths per point and errors 0.01–0.02; in the toy the whole
   quasi-stationary law of the edge agrees too (§3, §5; `jobs.py model1 | model2 | gump | slab | slabmodel`). The coin density hardly matters (toy, w = 8: ρ = 0.30 or 0.60 moves ln τ by ≤ 0.02). The deterministic
   chaos of the bulk enters the law only as a source of noise. Not tested beyond A = 63 (A = 84: one point, 78 deaths,
   +0.10 ± 0.13).
2. **[measured]** **In the toy the lifetime is a static property of the infinite edge:** τ_edge(L) = 12.1 / E(L − 6.5),
   E(ℓ) = probability that ℓ given consecutive cells of a long living edge are empty, fits all seven lifetimes
   L = 12–36 to ≤ 0.07 nats (2.7×10¹¹ window samples; §4, `jobs.py gap 600; report.py gap`). The exponent is the decay
   rate of E. Not tested for gump.
3. **[measured]** **The two automata die differently, and 0.416 ≈ 2 × 0.208 is a coincidence.** The toy's edge
   starves in a two-generation flash together with the two rows beneath; a gump face erodes over 5–12 generations
   with a straight tail. Gump periodic faces cost 0.403 per live cell (ln τ = 0.403·⟨n⟩, A = 27–60). Neither number
   is settled: the toy's asymptotic slope is 0.36–0.41, gump's is 0.209 on rim-free faces (to A = 108, other work)
   and 0.218–0.221 and rising on octahedral faces (A = 84–135, other work) (§2, §5, §10, §12).
4. **[proved]** Only bounds of the right *form*: E T ≤ 3δ^{−3L} for a driven edge, E T ≤ ε^{−L} with noise, and
   τ ≥ θ^{−⌊L/m⌋} *if* the quasi-stationary edge is ratio-mixing (θ measured ≤ 0.688 per cell). Decaying
   correlations alone do not give an exponential wait. No lower bound τ ≥ e^{cL} is proved for any system studied
   here, and no formula gives the constant: mean-field large deviations, the Gaussian and a single driven row all fail
   by 20–50% ([measured], §8).
5. **[exact]** In small vessels (N ≤ 32 cells) the edge-death law is already geometric, and the "random map with
   killing" heuristic fails by orders of magnitude because of debris (still lifes and period-2 patterns touching every
   edge), not because chaos is unlike a random map (30 vessels, every state; §6.2, `fg_run.py run 32`).

So, as far as this material goes: the exponent belongs to a few layers at the boundary, driven by noise. In the toy
it is the cost of an empty stretch of edge. Its value is not derived from the rule, and the numbers that the study
tried to explain have themselves moved since (section 12).

## 1. Tools and validation

- `drv.c` + `xp.py`: bit-sliced replicas (256 per run) of an outer-totalistic rule on an arbitrary directed cell
  graph. Each cell is *dynamic*, *noise* (i.i.d. Bernoulli, redrawn every generation; density stored with 12 bits,
  so 0.472 is 0.47192) or dead. Optional death noise ε. Quasi-stationary sampling with restarts: states younger than
  T0 = 300 generations (200 for gump) are not measured. Censored and reseeded: settled states (period ≤ 2 checked
  every generation; snapshots at 64 / 4096 / 262,144), strips cut by three dead columns, interior firewalls, and in
  slabs the oblique three-layer firewalls that wrap the torus. Recorded: the boundary population's histogram and
  one-step transitions, empty-window statistics, and the last 64 generations before every death. Seeds depend on the
  record key and the chunk index only, so a run replays bit for bit while its chunks take under 10 s (see `rerun.py`).
- `exact1d.c`: the one-row model solved exactly (power iteration on the killed kernel, 2^L states).
- `fg.c`: the exact functional graph of the toy on every state of a small vessel (N ≤ 32).
- `regrow.py`, `clone_corr.py`, `sync_check.py`, `mfld.py`, `game_check.py`: single experiments, described where used.
- `jobs.py` (run lists), `report.py` (tables, writes `data/*.json`), `figures.py` (`research/figures/exponent_*.png`),
  `rerun.py` (the 2026-11-14 re-runs).

**[measured] Validation.** `python3 validate.py` → ALL OK, **re-run 2026-11-14 from an empty record file: identical
output**. It checks: bit-exact against a numpy stepper for 300 generations (strips 6 × 9 and 16 × 20); toy L = 12, 16:
τ = 284 ± 4, 1651 ± 18 (ln τ 5.650 ± 0.013, 7.409 ± 0.011; toy2d: 286 ± 6, 1679 ± 26); gump hull R = 9 (A = 45):
first-peel mean 2306 ± 36 (fluct: 2300 ± 6); ln τ_face 9.823 ± 0.015 (fluct 9.819 ± 0.003). The noise path is checked
against the exact solution of §6.1 (simulated ln τ 4.390 ± 0.018, 6.418 ± 0.010, 8.622 ± 0.012 against exact
4.3999, 6.4168, 8.6348 at L = 8, 12, 16; not re-simulated, exact side re-run, see §6.1).
`python3 fg_check.py` → ALL OK (fg.c against direct enumeration, vessels with N ≤ 18), re-run.
`python3 game_check.py 13` → reproduces Theorem B's counts (§7), re-run.
Independent: the swarm's examiner validated a copy of `drv.c` (noise precision raised to 16 bits) against three
references (`research/theory/swarm/exam/OUTCOMES.md`, V1–V3: exact D2 rings at L = 12, 16 within 1.2σ; toy2d's
16 × 16 strip, −1.6σ; this study's gump slab 3 × 4 × 12, 7.4023 ± 0.0154 against 7.398 ± 0.007, +0.3σ).

**Re-runs of 2026-11-14** (`python3 rerun.py all`, `python3 rerun.py gap 300`, `python3 rerun.py ratefn`, records
under tags `rerun`, `rerun_gap`; one core, each ≤ 5 min). All reproduce the filed records exactly.

| section | quantity | command | filed | re-run |
|---|---|---|---|---|
| 1 | validation suite | `python3 validate.py` | ALL OK | ALL OK, identical |
| 3 | toy, w = 8 on dice, L = 16 | `rerun.py model` | 7.432 ± 0.014 | 7.432 ± 0.014 (5,153 deaths, identical) |
| 4 | empty-window cost, strips 16 × 128 | `rerun.py gap 300` | 0.434 (ℓ = 10), 0.399 (20), 0.382 (30) | 0.434, 0.399, 0.383 (1.1×10¹¹ windows, a prefix of the filed 2.7×10¹¹) |
| 4 | rate-function table | `rerun.py ratefn` | table §4 | identical to 3 decimals |
| 5 | gump hull model R = 9, w = 4 | `rerun.py gump` | 9.808 ± 0.010 | 9.808 ± 0.010 (identical) |
| 5 | gump slab 4 × 4 × 12, A = 48 | `rerun.py slab` | 9.937 ± 0.016 | 9.937 ± 0.016 (identical) |
| 6.1 | exact one-row model, L = 16, 20 | `exact1d 20 0.471924 0.471924` (rebuilt from `exact1d.c`) | 8.6348, 10.7377 | identical output file |
| 6.2 | exact functional graph, strip 4 × 7 | `fg strip 4 7 out` (rebuilt from `fg.c`) | `fg_strip_4x7.txt` | identical file |
| 9 | noisy toy, L = 16, ε = 10⁻³ | `rerun.py noise` | 7.398 ± 0.011 | 7.398 ± 0.011 (identical) |
| 10 | range-3 cross, L = 24 | `rerun.py cross3` | 5.254 ± 0.011 | 5.254 ± 0.011 (identical) |

`report.py hier | gump | gap | noise | endgame truth` and `fg_run.py table` were re-run on the filed records; they
reproduce `data/hierarchy.json`, `data/gap.json`, `data/fg_summary.json` unchanged and the tables below, with one
exception noted in §3. `data/gump_model.json` now also holds the A = 84 point (§5).
Because the replay is exact, a re-run checks the pipeline and the arithmetic, not the statistics: it is not an
independent sample. The independent checks are the validations above and the swarm's V1–V3.

## 2. How a toy edge dies: a two-generation flash, not a retreat

`python3 jobs.py truth1; python3 jobs.py model2; python3 report.py endgame truth`: strips 16 × L, both edges pooled,
3,100–8,600 edge deaths per size, every death's last 64 generations kept. **[measured]** (table re-derived from the
records 2026-11-14; runs not re-run except L = 12, 16 inside `validate.py`).

| L | ln τ_edge | deaths from n > L/2 | ln τ, sparse deaths only | h/p₁ | P(die \| n = 1) | p₁/p₂ | edge density 1, 2, 3, 6, 12 generations before death |
|---|---|---|---|---|---|---|---|
| 12 | 5.644 ± 0.013 | 20.5% | 5.873 | 0.527 | 0.292 | 0.50 | 0.29, 0.61, 0.60, 0.58, 0.58 |
| 16 | 7.407 ± 0.011 | 10.6% | 7.519 | 0.456 | 0.245 | 0.45 | 0.19, 0.55, 0.58, 0.56, 0.58 |
| 20 | 9.142 ± 0.011 | 5.1% | 9.194 | 0.397 | 0.202 | 0.40 | 0.13, 0.46, 0.54, 0.56, 0.57 |
| 24 | 10.788 ± 0.012 | 2.7% | 10.816 | 0.361 | 0.176 | 0.38 | 0.10, 0.39, 0.50, 0.54, 0.57 |
| 28 | 12.434 ± 0.018 | 1.2% | 12.446 | 0.314 | 0.153 | 0.37 | 0.07, 0.33, 0.45, 0.52, 0.57 |

Living means: rows 0–3 have densities 0.577, 0.507, 0.452, 0.470, so the edge row is *denser* than the bulk (0.472).
toy2d has 5.657 ± 0.019, 7.426 ± 0.016, 9.055 ± 0.030, 10.768 ± 0.031, 12.368 ± 0.033 at the same sizes; these agree
except at L = 20 (2.7σ; this run has eight times the deaths). The "deaths from n > L/2" and "sparse only" columns
come from the death-by-population tallies; `report.py endgame` prints the coarser split n ≥ 7 (20%, 11%, 5%, 3%,
1%); the finer columns were not re-derived.

- **The plunge takes two generations at every size.** Two generations before death the edge still holds 57–106% of
  its living density; one generation before, 12–50%; then nothing. Rows 1 and 2 fall with it (to 0.21–0.29 and
  0.26–0.29 one generation before, from 0.51 and 0.45); row 3 hardly moves (0.41 against 0.47). The top three rows
  starve together (`research/figures/exponent_flash.png`). A shallow sag before the flash grows with L (at L = 28
  the edge is at 0.52 six generations before). Forecast F2 ("the plunge lengthens with L") was wrong.
- **Two channels.** Some deaths come straight from a *dense* edge (n > L/2: an overcrowded row wiped out in one
  step): 20% at L = 12, 1% at L = 28. That channel costs 0.60 ± 0.02 per cell; the sparse (starvation) channel costs
  0.411, 0.419, 0.405, 0.408 ± 0.005 per cell between L = 12, 16, 20, 24, 28. Most of the curvature of ln τ(L) at
  small L (total local slopes 0.441, 0.434, 0.412, 0.411) is the fading dense channel.
- **The end-game depends on size.** P(die | one cell left) falls from 0.29 to 0.15: a single surviving cell dies
  only if the rows beneath it are starved too, and a surviving cell is one that sits where they are not.
- **No straight tail.** ln(p_{k+1}/p_k) at L = 28 runs 1.00, 1.19, 1.09, 0.91, 0.79, 0.73, 0.67, 0.60, 0.53, 0.45
  for k = 1…10. The tail is straight over its three lowest points only.
- **Splitting cannot work.** `python3 clone_corr.py 20 3000 3` (not re-run): two clones of one state, each with one
  cell flipped at depth ≥ 3, have outcome correlation 0.98, 0.97, 0.97 across three successive interfaces
  (n ≤ 8 → 6 → 4 → 2; 2,900 parents each); 87%, 74%, 57% of clone pairs have identical edge histories to the end of
  the trial (2.6–5.6 generations). A perturbation three rows down cannot reach the edge before the flash is over.
  Forward-flux sampling along n is useless here, as in gump (fluct §2: 0.86–0.95).
- **[proved]** (theorems.md, Lemma A, Theorem B): a live edge cell with exactly two live in-row neighbours survives
  whatever lies beneath, so an edge that dies had no such cell one generation earlier; with the two rows beneath
  chosen freely, every edge can be emptied in three generations, and the lone triple `111` cannot be emptied in two.

## 3. The exponent belongs to a boundary layer: rows of the rule on coin flips

**Model.** Keep the rule on the top w rows; replace rows w and w + 1 by i.i.d. Bernoulli(ρ) cells redrawn every
generation (`xp.toy_model(w, L)`; the swarm calls it D2(L, ρ; w)). No fitted parameter; ρ = 0.472 is the toy's bulk
density. It is a finite-range probabilistic cellular automaton with one absorbing event, so its death law is
exactly geometric from its quasi-stationary state (Theorem D), and nothing can settle.

`python3 jobs.py model1; python3 jobs.py model2; python3 report.py hier` (2,500–12,800 deaths per entry)
**[measured]**; table re-derived 2026-11-14, w = 8 at L = 16 re-run (identical):

| w | L = 12 | 16 | 20 | 24 | 28 | slope, L = 12–28 | vs truth |
|---|---|---|---|---|---|---|---|
| 1 | 6.418 | 8.622 | 10.734 | 12.823 | 14.877 | 0.5308 | +25% |
| 2 | 5.932 | 8.006 | 9.904 | 11.848 | 13.740 | 0.4904 | +15% |
| 3 | 5.564 | 7.462 | 9.291 | 11.057 | 12.812 | 0.4553 | +7% |
| 4 | 5.640 | 7.441 | 9.217 | 10.987 | 12.642 | 0.4420 | +4% |
| 6 | 5.631 | 7.434 | 9.150 | 10.870 | 12.521 | 0.4326 | +2% |
| 8 | 5.645 | 7.432 | 9.165 | 10.828 | 12.445 | 0.4273 | +0.5% |
| truth (16 × L) | 5.644 | 7.407 | 9.142 | 10.788 | 12.434 | 0.4252 | |

(Errors 0.009–0.020 per entry; `research/figures/exponent_hierarchy.png`. The slopes are weighted straight-line
fits with χ² of 37–63 on 3 degrees of freedom: the lines curve, so their nominal errors of ± 0.001 mean nothing.
The author's unfinished draft quoted 0.4281 for w = 8 and 0.4254 for the truth; `report.py hier` on the filed
records gives 0.4273 and 0.4252.)

- **With eight rows the model is indistinguishable from the deterministic strip:** ln τ within 0.00, 0.03, 0.02,
  0.04, 0.01 (errors 0.02), and so is the whole quasi-stationary distribution of the edge population:
  max over k = 1…L−2 of |ln P_model(n = k) − ln P_truth(n = k)| = 0.026, 0.017, 0.025 at L = 16, 24, 28 (w = 4: 0.06,
  0.17, 0.23; w = 1: 1.3, 2.4, 3.0). So do h/p₁, P(die | n = k), the dense-channel share and the pre-death profiles of
  rows 0–3. (Histogram distances: not re-derived.)
- **Not even the density matters** (F9, hit): with w = 8, ρ = 0.30 and 0.60 give ln τ = 7.432, 7.417 at L = 16 and
  9.151, 9.182 at L = 20, against 7.432, 9.165 at ρ = 0.472 (± 0.015). With w = 4, ρ from 0.35 to 0.60 moves ln τ(20)
  from 9.24 to 9.11 (`python3 jobs.py rhoscan; python3 jobs.py rhoscan8`; not re-run; from `runs_rhoscan.json`).
- **What one row lacks.** A single row on white noise is 25% too steep and dies differently: a decline of four to
  five generations that lengthens with L, with P(die | n = 1) = (1 − ρ²)⁵ = 0.284 at every L. Feeding the single row
  the *real* rows 7–8 of an independent deterministic strip, without feedback (`xp.toy_slave`, `python3 jobs.py
  slave`; not re-run), gives ln τ = 6.128, 8.175, 10.125 at L = 12, 16, 20: slope +14% instead of +25%. So about
  half of the single row's error is that real rows are not white noise; the other half is that the rows directly
  beneath must be able to starve *with* the edge (w ≥ 3). Feeding it the rows that really lie beneath an edge is not
  a clean test: the slave slowly synchronises with the donor's own edge (`python3 sync_check.py`: 31% of 64-cell
  rows after 2,000 generations; not re-run).
- Convergence in depth is slow: excess slope 0.105, 0.065, 0.030, 0.017, 0.007, 0.002 at w = 1, 2, 3, 4, 6, 8, and the
  depth needed grows with L (at L = 12 four rows suffice, at L = 28 eight).

## 4. The static formulation: an edge dies at the rate at which a window is empty

**Empty windows.** In a long living edge (strips 16 × 128, both edges) let E(ℓ) be the probability that a given
window of ℓ consecutive edge cells is empty. `python3 jobs.py gap 600; python3 report.py gap` (2.7×10¹¹ window
samples; E measured down to 1×10⁻¹⁰ at ℓ ≈ 56) **[measured]**; re-run as a 300 s prefix (`rerun.py gap 300`), and
the table re-derived from `data/gap.json`:

| ℓ | 1 | 5 | 10 | 14 | 18 | 22 | 26 | 30 | mean over 34 → 42 | mean over 42 → 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| −ln[E(ℓ+1)/E(ℓ)] | 0.609 | 0.471 | 0.434 | 0.417 | 0.404 | 0.395 | 0.388 | 0.382 | 0.376 | 0.382 |
| the same, eight-row model (`gap_w8_L128`) | 0.610 | 0.472 | 0.436 | 0.418 | 0.406 | 0.396 | 0.390 | 0.387 | 0.396 | 0.417 |
| the same, one-row model (`gap_w1_L128`) | 0.808 | 0.601 | 0.575 | 0.554 | 0.537 | 0.522 | 0.511 | 0.514 | – | – |

Window samples overlap (one empty stretch of length 60 contributes 13 windows of length 48), so the counts are not
independent; at ℓ ≥ 40 there are only 10³–10⁴ counted windows, from far fewer empty stretches. The filed figure
"0.376 ± 0.002 over ℓ = 34–41" treats them as independent and is too precise. The ℓ ≥ 34 entries should be read
as ± 0.01–0.02 at best. (The row for the eight-row model was not discussed by the author.)

- **[measured] τ_edge(L) = 12.1 / E(L − 6.5).** One shift and one prefactor reproduce all seven lifetimes from
  L = 12 to 36 (this study's to 28, toy2d's at 32 and 36; ln τ from 5.6 to 15.6) with residuals +0.03, −0.02, −0.01,
  −0.01, +0.03, +0.07, +0.05 nats (χ² 17/5). Re-derived 2026-11-14 for L = 12–28 with log-linear interpolation of E:
  +0.025, −0.026, −0.009, −0.017, +0.022 (the L = 32, 36 residuals not re-derived). A ring of L cells dies about as
  often as a window 6.5 cells shorter is found empty in an endless edge. For the contact process this is the
  Durrett–Schonmann picture (extinction exponent of a finite system = decay rate of the empty-interval probability
  of the infinite one); here it is observed in a non-monotone deterministic automaton. Forecast F3: hit.
- So, **in the toy, the exponent is a static property of the stationary edge**, and the hypothesis of Theorem E(a)
  holds as a measured fact: E(ℓ+1)/E(ℓ) ≤ 0.688 for every 5 ≤ ℓ ≤ 41. Under that hypothesis alone, τ ≥ 0.688^{−L}
  is a theorem.
- **"0.416" is not the asymptotic constant.** Three estimates of where the slope ends: the window cost, 0.376–0.382
  at ℓ = 34–50; the fit ln τ = a + I·L + b·ln L to the seven lifetimes, I = 0.364 ± 0.006, b = 1.14 ± 0.12 (χ²
  4.6/4; a straight line has χ² 95/5, I = 0.4215); the sparse channel alone, 0.41 ± 0.005 and nearly straight over
  L = 12–28 (§2). They disagree by up to 0.04. The eight-row model, which reproduces every lifetime, has a window cost
  of 0.396–0.417 beyond ℓ = 34, not 0.376: either the ℓ > 34 window costs are noise at the ± 0.02 level, or window
  cost and lifetime part company there. Honest range for the toy's asymptotic slope: **0.36–0.41**. toy2d's
  0.416 ± 0.0014 is an effective slope for L = 12–36 (the swarm's critic, board E1, independently: 0.36–0.42).

**The rate function** I_L(x) = −ln P_qs(n ≤ xL)/L (this study's strips to L = 28, toy2d's raw histogram at 36;
log-linear interpolation in n) **[measured]**; re-derived 2026-11-14 (`rerun.py ratefn`), identical:

| L | x = 0.50 | 0.40 | 0.30 | 0.20 | 0.10 | 0.05 | 0 (−ln h/L) |
|---|---|---|---|---|---|---|---|
| 12 | 0.081 | 0.135 | 0.207 | 0.295 | 0.399 | – | 0.470 |
| 20 | 0.053 | 0.097 | 0.157 | 0.239 | 0.349 | 0.411 | 0.457 |
| 28 | 0.043 | 0.084 | 0.142 | 0.218 | 0.321 | 0.384 | 0.444 |
| 36 | 0.036 | 0.076 | 0.132 | 0.207 | 0.303 | 0.366 | 0.433 |
| slope of L·I_L, L = 20–36 | 0.015 | 0.049 | 0.101 | 0.167 | 0.246 | 0.309 | 0.403 |
| Gaussian (0.577 − x)²/(2·0.397) | 0.007 | 0.039 | 0.097 | 0.179 | 0.287 | 0.350 | 0.419 |

- **It does not collapse** as gump's does: at fixed x, I_L(x) ≈ I_∞(x) + b(x)/L with b = 0.8–2.1 nats (gump: ≤ 0.25,
  fluct). The "slope of L·I_L" row is the size-independent part.
- **Shape:** convex, with slope −dI/dx ≈ 0.3–0.5 near x = 0.4, 0.7–0.8 near 0.2 and 1.3–1.9 below 0.1, steepening
  towards zero. A nearly empty edge is not "a living stretch plus a gap" (that would give a straight I); it is a thin
  scatter of survivors over starved rows.
- **A coincidence to distrust.** The Gaussian value at zero, mean²/(2·variance) = 0.577²/(2 × 0.397) = 0.419 per cell,
  equals the fitted 0.416–0.4215. The parabola crosses the measured curve twice (half the true value at x = 0.5,
  right at 0.3, 17% high at 0.1), and the same formula gives 0.30–0.33 for gump, whose faces cost 0.21.

## 5. Gump: the same recipe works at four layers, and the face dies differently

**The committed forecast (F5) missed.** The depth was fixed from the toy before any gump run: w* = 3, the smallest
depth within 10% of the toy's slope. `python3 jobs.py gump; python3 jobs.py gump13 4; python3 report.py gump`:
the top w {111} layers of the octahedral hull |p|₁ ≤ R follow B45/S345, the next two layers are Bernoulli(0.4155)
(`xp.gump_model(R, w)`; the swarm's D3); ln τ_face, 78–12,800 deaths per entry **[measured]**; table re-derived,
R = 9, w = 4 re-run (identical):

| w | A = 30 (R = 7) | A = 45 (R = 9) | A = 63 (R = 11) | A = 84 (R = 13) |
|---|---|---|---|---|
| 1 | 5.877 ± 0.016 | 8.731 ± 0.012 | 12.463 ± 0.014 | |
| 2 | 6.378 ± 0.009 | 9.914 ± 0.011 | 14.274 ± 0.024 | |
| **3 (forecast)** | **7.126 ± 0.012** | **10.542 ± 0.015** | **14.653 ± 0.032** | |
| 4 | 6.550 ± 0.009 | 9.808 ± 0.010 | 13.653 ± 0.022 | 18.179 ± 0.113 (78 deaths) |
| 5 | 6.580 ± 0.009 | 9.782 ± 0.010 | 13.592 ± 0.022 | |
| measured hull (`research/fluct`) | 6.804 ± 0.003 | 9.819 ± 0.003 | 13.633 ± 0.008 | 18.077 ± 0.054 |

At w = 3 the model is too tough by 0.32, 0.72, 1.02 nats. **At w = 4 and 5 it reproduces the measured faces at
A = 45 and 63 to −0.01, +0.02 and −0.04, −0.04 nats**, and at A = 84 (w = 4) to +0.10 ± 0.13 (+0.03 against the
independent CPU value 18.154 ± 0.025, `research/audit/REVIEW-gpu-pr8.md`; forecast F10, hit). The known end-game is
reproduced too: h/p₁ = 0.60–0.62 (fluct: 0.60–0.61), deaths from n = 1/2/3 in the proportions 62/24/9% (63/23/9%),
p₁/p₂ = 0.66–0.67 (0.65–0.66), and the excess at three cells (ln p₄/p₃ = 0.32 between neighbours of 0.60 and 0.44);
these end-game numbers were not re-derived. At A = 30 the model is 0.25 low: the R = 7 hull has no bulk under its
faces (its fifth layer is the centre). In the hull, convergence in depth is not monotone (w = 1 too weak, w = 2, 3
too tough); one layer deeper than the toy's 10% criterion was needed. Slopes over A = 30–63: 0.2159 (w = 4), 0.2128
(w = 5), 0.2060 (truth); over A = 45–63: 0.2136, 0.2117, 0.2119.

**Like for like: periodic faces.** A slab of twelve {111} layers on a torus (`xp.gump_slab(a, b, 12)`, two faces of
3ab cells, deterministic, censoring settled states, interior firewalls and the oblique firewalls that wrap the
torus), against the model with a periodic face (`xp.gump_slab_model(a, b, w)`). `python3 jobs.py slab; python3 jobs.py
slabmodel; python3 jobs.py slab75` **[measured]**; table re-derived from the records, A = 48 slab re-run (identical):

| A | deterministic slab, ln τ_face | model − slab: w = 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| 27 | 5.501 ± 0.012 | +0.62 | +0.11 | +0.00 | −0.01 | +0.03 | −0.01 |
| 36 | 7.386 ± 0.022 | +0.78 | +0.16 | +0.03 | +0.02 | +0.01 | +0.01 |
| 48 | 9.937 ± 0.016 | +0.93 | +0.21 | +0.05 | +0.01 | +0.00 | −0.02 |
| 60 | 12.496 ± 0.019 | +1.19 | +0.26 | +0.05 | +0.02 | −0.01 | −0.01 |
| 75 | – | | | | 15.640 ± 0.025 (model alone, 1,585 deaths) | | |

(Model errors 0.009–0.018.) Here the convergence is monotone, as in the toy, and **from five layers on the model is
the slab** (F8a hit: all eight entries at w = 6, 8 within 0.03; F8b miss: w = 3 is not the worst depth here).
Independent checks: the swarm's examiner got 7.4023 ± 0.0154 for the 3 × 4 × 12 slab (V3) and 12.480 ± 0.018 for a
5 × 4 × 8 slab at A = 60 (its entry E3), against 7.386 / 7.398 (pooled) and 12.496 here.

**Periodic and octahedral faces: same slope up to A ≈ 63, not beyond.** Local slopes of ln τ per cell: periodic
0.2095 ± 0.0028, 0.2126 ± 0.0023, 0.2133 ± 0.0021 (A = 27 → 36 → 48 → 60), then **0.208 ± 0.002 (60 → 75, w = 5
model)**; octahedral 0.2010, 0.2119, 0.2116 (A = 30 → 45 → 63 → 84, fluct). On that range the author concluded that
the rim changes the prefactor and not the exponent (forecasts F7b / F8c, "different by more than 5%": miss). At equal
area the octahedral face lives longer: interpolated ln τ ≈ 13.0 at A = 60 against 12.50, a factor 1.6. Half the cells
of an octahedral face of this size are rim cells with four in-layer neighbours instead of six (at A = 63: 30 interior,
30 rim, 3 corners). **Since then** (section 12) octahedral faces have been measured at A = 108, 135 with local slopes
0.218–0.221, and rim-free slab faces stay on 0.2088 through A = 108, the octahedral face being 0.91 ± 0.06 nats
tougher there. So the gap grows from ≈ 0.5 nats at A = 60 to ≈ 0.9 at A = 108: beyond A ≈ 84 the two kinds of face do
*not* have the same slope, and "the rim changes only the prefactor" holds on A ≤ 63 only.

**How a gump face dies** (same runs; `research/fluct` §1 has the octahedral case; not re-derived):

| | toy edge, L = 28 | gump periodic face, A = 60 | gump octahedral face, A = 63 (model, w = 5) |
|---|---|---|---|
| boundary density 1, 2, 3, 4, 6, 8, 12 generations before death (living mean) | 0.07, 0.33, 0.45, 0.47, 0.52, 0.55, 0.57 (0.58) | 0.03, 0.07, 0.18, 0.30, 0.41, 0.47, 0.51 (0.52) | 0.03, 0.06, 0.10, 0.15, 0.25, 0.33, 0.44 (0.50) |
| next layer, 1 generation before (living mean) | 0.22 (0.51) | 0.25 (0.44) | 0.33 (0.44) |
| ln(p_{k+1}/p_k) for k = 4…12 | 0.91 → 0.31, falling | 0.36 … 0.41 | 0.44 … 0.47 |
| ln τ / ⟨n⟩ | 0.80 → 0.77, drifting | 0.406, 0.403, 0.402, 0.403 at A = 27…60 | 0.45, 0.44, 0.43 |
| P(die \| n = 1) | 0.29 → 0.15, falling with L | 0.54, 0.50, 0.46, 0.46 | 0.38–0.39 |

- **The toy flashes; gump erodes.** A gump face loses its population over five (periodic) to twelve (octahedral)
  generations, with only the layer just beneath sagging (to 57–75% of its mean). Its quasi-stationary tail is
  straight, a constant cost per cell lost over k = 4…0.25A, so its rate function is close to a tent, where the toy's
  is convex. The two automata do not share a mechanism. (The swarm's critic, board E14, adds from the fluct
  histories that the octahedral collapse lengthens with A: half-way lag 3.2 → 6.8 generations from A = 30 to 84.)
- **[measured] Gump's law per live cell.** For periodic faces **ln τ_face = 0.403·⟨n⟩** to three figures at all four
  sizes A = 27–60, with no intercept (⟨n⟩ = mean living population of the face, 0.501–0.517 of A). For octahedral
  faces the same cost per live cell appears with an intercept: ln τ = 0.40·⟨n⟩ + 1.1–1.2 for A = 45–84 (increments
  0.395, 0.398 per live cell from fluct's table; ⟨n⟩ = 0.532·A − 2.3 there). "0.21 per site" is 0.40 per live cell
  times 0.52–0.53 live cells per site. Between successive periodic sizes the cost per live cell is 0.394 ± 0.005,
  0.398 ± 0.004, 0.408 ± 0.004: not exactly constant.
- **Regrowth** (`python3 regrow.py gump 11 5`, `regrow.py toy 8 28`, and the slab 5 × 5 at w = 5; not re-run; JSON
  in `research/scratch/exponent/regrow_*.json`). Clear the boundary layer of an equilibrated model except one cell
  and follow its population. A one-cell seed takes (reaches 22–26 cells before dying) with probability 0.22 on the
  A = 63 hull face, 0.13 on the A = 75 periodic face, 0.70 on the toy edge (L = 28, reaching 9). Read the increments
  of the regrowing population as a random walk, and the Cramér–Lundberg root κ of E e^{−κΔn} = 1 would be the tail
  slope ln(p_{k+1}/p_k) of the living boundary. Measured: κ = 0.65 (one-generation steps; 0.57 for four-generation
  steps) on the hull face, against a tail slope of 0.44–0.47; κ falls with n, from 1.0 at n = 4 to 0.47 at n = 14, so
  it matches the tail only at the top of the measured range. Periodic face: κ = 0.79 (0.61–1.17 by n) against a tail
  of 0.36–0.41. Toy: κ = 0.90, falling from 2.2 at n = 3 to 0.62 at n = 8, against tail ratios 1.09, 0.91, 0.79, 0.73,
  0.67, 0.60 at k = 3…8, close for n ≥ 6. **[measured; interpretation open]** A dying boundary is not simply the
  time-reverse of a random walk of regrowth; the author left no conclusion from this experiment.
- **Curvature (F11).** The author's periodic local slopes 0.2106 ± 0.0010, 0.2114 ± 0.0008, 0.2134 ± 0.0009 (slab
  pooled with the w = 5, 6, 8 models that agree with it) rose with size. That rise was the basis of forecast F11; the
  A = 75 model point (15.640 ± 0.025) then came out 0.10 below the forecast 15.74 ± 0.05 and the 60 → 75 slope at
  0.208 (F11c: miss). The rise did not continue.

## 6. Exact small systems

### 6.1 One row on noise, solved exactly

The w = 1 model is a Markov chain on the 2^L rows with a product kernel: given the row, cells update independently,
alive with probability q(state, k), k = live in-row neighbours. For ρ = 0.472, q(dead, ·) = 0, 0.223, 0.721,
0.777, 0.279 and q(live, ·) = 0.223, 0.721, **1**, 0.777, 0.279 (k = 0…4; the 1 is Lemma A's safe cell).
`exact1d L 0.471924 0.471924` applies the killed kernel site by site (O(L·2^(L+4)) per step) and iterates to the
quasi-stationary distribution; the death rate is then exact, and by Theorem D′ the geometric law is a theorem for
this chain. **[exact]**; L = 16 and 20 re-run 2026-11-14 from a fresh build: identical output.

| L | ln τ (exact) | deaths from n > L/2 | ln τ, sparse deaths | h/p₁ | p₁/p₂ |
|---|---|---|---|---|---|
| 8 | 4.3999 | 29.9% | 4.7555 | 0.428 | 0.616 |
| 12 | 6.4168 | 17.1% | 6.6048 | 0.399 | 0.530 |
| 16 | 8.6348 | 9.0% | 8.7295 | 0.394 | 0.476 |
| 18 | 9.6832 | 6.6% | 9.7511 | 0.395 | 0.465 |
| 20 | 10.7377 | 4.7% | 10.7860 | 0.396 | 0.458 |

(Simulated with `drv.c`: 4.390 ± 0.018, 6.418 ± 0.010, 8.622 ± 0.012, 10.734 ± 0.016 at L = 8, 12, 16, 20, and
12.823 ± 0.014, 14.877 ± 0.020 at L = 24, 28. The swarm's lab solved the same chain independently, `dice_w1.py` at
ρ = 0.472 exactly: 4.4000, 5.3838, 6.4169, 7.5765, 8.6350, 9.6834 at L = 8…18, board lab L0b.4; the 10⁻⁴ differences
are the 12-bit ρ here.)

- **The one-row slope is 0.52 ± 0.01**: exact steps 0.529, 0.524, 0.527 per cell between L = 14, 16, 18, 20 (sparse
  channel 0.511, 0.511, 0.517); simulated 0.522, 0.514 between 20, 24, 28. Below L = 14 the step oscillates by ± 0.05
  with L (0.598, 0.492, 0.517, 0.580 from L = 6).
- It shows the two channels cleanly — the dense one (a full row wiped by overcrowding; 0.69 per cell) carries 30% of
  deaths at L = 8 and 5% at L = 20 — and an end-game that *is* size-independent: h/p₁ → 0.395, with
  P(die | n = 1) = (1 − ρ²)⁵ = 0.284. The falling h/p₁ of the real toy is a property of the rows beneath, not of a
  one-dimensional edge as such.
- This is the cleanest object here on which a lower bound could be proved (§7).

### 6.2 Every state of small vessels: the random map with killing (PROGRAM E2), tested

`python3 fg_run.py run 32`: `fg.c` follows all 2^N states of the deterministic toy (strips H × L periodic along the
edge, and H × L boxes) to their cycles. It gives the exact histogram of the edge-death time T over all initial
states, every cycle by period, the cycles that keep every edge occupied ("immortal") and the size of their basin.
N = 32 takes six minutes. **[exact]**; `fg_run.py table` re-run (unchanged `data/fg_summary.json`), strip 4 × 7
re-run from a fresh build (identical file).

| vessel | N | \|G\| | never lose an edge | plateau hazard, t = 6–16 (range) | τ = 1/h | states on immortal cycles | of which period ≤ 2 | period ≥ 8 (longest) | heuristic: \|G\|τ states | heuristic basin \|G\|τ²/2^N |
|---|---|---|---|---|---|---|---|---|---|---|
| strip 4 × 5 | 20 | 20 | 22.6% | 0.42 (0.33–1) | 2.4 | 3,816 | 94% | 0 (4) | 48 | 1×10⁻⁴ |
| strip 4 × 6 | 24 | 24 | 20.9% | 0.274 (0.23–0.40) | 3.7 | 3,374 | 82% | 0 (4) | 88 | 2×10⁻⁵ |
| strip 4 × 7 | 28 | 28 | 20.4% | 0.144 (0.131–0.152) | 6.9 | 8,443 | 67% | 0 (7) | 194 | 5×10⁻⁶ |
| **strip 4 × 8** | 32 | 32 | **28.8%** | **0.108 (0.102–0.111)** | 9.3 | **42,493** | 72% | 2,120 (26) | 298 | 6×10⁻⁷ |
| strip 5 × 5 | 25 | 20 | 5.3% | 0.300 (0.23–0.32) | 3.3 | 17,876 | 92% | 0 (4) | 67 | 7×10⁻⁶ |
| strip 5 × 6 | 30 | 24 | 11.6% | 0.237 (0.228–0.241) | 4.2 | 11,310 | 78% | 360 (18) | 101 | 4×10⁻⁷ |
| strip 3 × 8 | 24 | 32 | 48.6% | 0.23 (0.18–0.27) | 4.3 | 10,544 | 81% | 1,040 (60) | 138 | 4×10⁻⁵ |
| strip 3 × 9 | 27 | 36 | 60.1% | 0.198 (0.19–0.23) | 5.1 | 26,085 | 91% | 0 (6) | 182 | 7×10⁻⁶ |
| strip 3 × 10 | 30 | 40 | 73.2% | 0.197 (0.19–0.22) | 5.1 | 74,803 | 89% | 120 (12) | 204 | 1×10⁻⁶ |
| strip 2 × 14 | 28 | 56 | 90.7% | 0.23 (0.11–0.29) | 4.4 | 53,647 | 96% | 504 (70) | 248 | 4×10⁻⁶ |
| strip 2 × 16 | 32 | 64 | 94.1% | 0.21 (0.16–0.45) | 4.9 | 187,938 | 97% | 2,032 (24) | 311 | 4×10⁻⁷ |
| box 5 × 5 | 25 | 8 | 20.3% | 0.124 (0.10–0.15) | 8.0 | 1,378 | 79% | 20 (10) | 64 | 2×10⁻⁵ |
| box 5 × 6 | 30 | 4 | 17.1% | 0.099 (0.090–0.106) | 10.1 | 6,917 | 85% | 40 (8) | 41 | 4×10⁻⁷ |
| box 4 × 7 | 28 | 4 | 21.1% | 0.133 (0.11–0.15) | 7.5 | 7,852 | 92% | 204 (44) | 30 | 8×10⁻⁷ |
| box 4 × 8 | 32 | 4 | 21.9% | 0.107 (0.09–0.12) | 9.4 | 39,244 | 95% | 112 (8) | 38 | 8×10⁻⁸ |

("Hazard" = fraction of the mortal states still holding all their edges at generation t that lose one at t + 1;
|G| = order of the vessel's symmetry group; "period ≥ 8" counts states, with the longest immortal period in
brackets. The full table, 30 vessels from N = 10, is `data/fg_summary.json`, `python3 fg_run.py table`.)

- **[exact] The death-time law is already geometric at 28–32 cells.** In the 4 × 8 strip, over all 4.29×10⁹ initial
  states, the hazard of losing an edge is 0.102–0.111 at every generation from 6 to 16 (0.107 at 20; later it sinks
  to 0.06–0.08, a slower sub-population); 36% of the mortal states outlive 10 generations and 2% outlive 40.
  Memorylessness is there as soon as the vessel can hold any chaos (H ≥ 4; three-row strips have a hazard ≈ 0.2 that
  does not depend on L — they only settle).
- **Its rate grows with the edge at the right order of magnitude:** at H = 4, −ln h = 0.87, 1.30, 1.94, 2.23 for
  L = 5…8, steps of 0.43, 0.64, 0.29, mean 0.45 per cell, against 0.44 for deep strips at L = 12–16. The steps are too
  irregular and the strip too thin (τ = 9 against 33 for the eight-row model at L = 8) for an extrapolation.
- **[exact] The random map with killing fails by orders of magnitude, in the way forecast (F1).** It predicts
  ≈ |G|τ states on immortal cycles and a basin of |G|τ²/2^N. The vessels have 20–1,000 times more such states, and
  between 5% and 94% of *all* states never lose an edge, against a predicted 10⁻⁷–10⁻⁴. The reason is debris:
  67–97% of the states on immortal cycles are still lifes or period-2 patterns that touch every edge, and their
  number grows exponentially with N (H = 4: 3,374 → 8,443 → 42,493 for L = 6, 7, 8) while τ grows like e^{0.45L}.
- **For long cycles the heuristic has the right size.** States on immortal cycles of period ≥ 8 exist in 10 of the
  17 vessels with N ≥ 24 and number 0.3–8 times |G|τ there (4 × 8 strip: 2,120 against 298; 5 × 6 box: 40 against
  41). The longest immortal periods — 70 (2 × 14), 60 (3 × 8), 44 (box 4 × 7), 26 (4 × 8) — are the toy's clockwork.
  E2 should therefore read: *a random map with killing for the chaotic component, plus a debris component whose
  count is exponential in N, which a soup in a small vessel reaches with probability of order one.* What fraction it
  reaches in a large vessel is the open half of OPEN-PROBLEMS item 4.

## 7. What is proved (`exponent/theorems.md`)

- **A (safe cells).** A live toy edge cell with exactly two live in-row neighbours survives whatever lies beneath; a
  dead one with none stays dead; every other (state, k) can go either way. A gump face cell is never safe on its
  own. *Corrected 2026-11-14:* the old sentence "a gump face can always die in one generation" was false (§12).
- **B (three generations).** With the two rows beneath chosen freely, every edge configuration on a ring of L ≥ 5
  can be emptied in three generations, and the lone triple `111` (L ≥ 9) cannot be emptied in two. Brute force
  (`python3 game_check.py 13`, re-run): for L = 9…13 the L rotations of the lone triple are the only configurations
  that need three (L = 13: 989 in one, 7,189 in two, 13 in three). The swarm's critic read the proof and found it
  correct (board, lemma exchange). **B′:** an edge driven by any field giving each b conditional probability ≥ δ
  dies within three generations with probability ≥ δ^{3L}, so E T ≤ 3δ^{−3L}: for the w = 1 model ln τ ≤ 4.5·L + 1.1
  (true: 0.53·L).
- **C (noisy toy).** With independent deaths at rate ε, E T ≤ ε^{−L} from every state.
- **D, D′ (quasi-stationarity).** From a quasi-stationary state the death time is exactly geometric with
  h = Σ μ(x)·P_x(die next step); the w = 1 model is irreducible and aperiodic on the living rows, so this holds
  asymptotically from every start. No such statement exists for the deterministic automata (§6.2 shows why:
  conditioning on survival selects immortal debris).
- **E (which mixing).** If under the quasi-stationary law the probability that the next block of m edge cells is
  empty, given that all previous blocks are, is at most θ < 1, then τ ≥ θ^{−⌊L/m⌋}; ψ-mixing implies this; a finite
  energy bound gives the matching upper bound. *Exponentially decaying correlations do not suffice* (a mixture with
  an e^{−√L} atom on the empty row has them and a sub-exponential wait), so PROGRAM M2 and OPEN-PROBLEMS item 3
  should say "ratio (ψ-) mixing". The hypothesis is the measured statement of §4 (θ = 0.688 per cell for
  5 ≤ ℓ ≤ 41). Checked by the critic (board, lemma exchange; graveyard 3).
- **Not proved:** any lower bound τ ≥ e^{cL}. For the w = 1 model this is the survival of a non-attractive
  one-dimensional probabilistic automaton. The author's reason why the block/percolation route fails had two parts;
  the critic accepts only the second (an unknown outside contaminates two cells per side per generation) and notes
  that the comparison theorem needs no monotonicity (board, graveyard 6; note added to theorems.md).

## 8. Closed forms that do not survive

- **Mean-field large deviations** (`python3 mfld.py toy 1 2 3; python3 mfld.py gump 1 2`; not re-run; output in
  `research/scratch/exponent/mfld_*.txt`). Treat the cells of each row as independent given the row densities, charge
  a Kullback–Leibler cost for every forced density, minimise over paths to an empty edge. Result I_MF = 0.424, 0.347,
  0.239 for the toy at w = 1, 2, 3 (model: 0.531, 0.490, 0.455) and 0.171, 0.131 for gump at w = 1, 2 (model: 0.20,
  0.23–0.24). These are values at the longest horizon computed (T = 12–16 intermediate generations), still falling
  with T, so they are upper bounds on the method's own answer. 20–50% low, worse with depth, and the optimal path is
  wrong: it first *fills* the edge (density 0.86–0.90) and lets overcrowding wipe it, the dense channel, which in the
  real toy is expensive because of the safe cells. That 0.424 lands on the toy's 0.42 is an accident of w = 1.
- **The Gaussian** mean²/(2·variance): 0.419 for the toy (accident, §4), 0.30–0.33 for gump.
- **Splitting / forward flux** along n: clones stay 97–98% correlated (§2).
- **A single driven row:** 25% too steep for the toy; for gump's octahedral faces about one nat too short-lived at
  nearly the right slope (5.88, 8.73, 12.46 against 6.80, 9.82, 13.63; the critic's board E13 reads the same numbers
  the same way). The end-game is wrong in both.

## 9. Noise

`python3 jobs.py noise; python3 report.py noise`: every live cell also dies with probability ε per generation
(strips 16 × L; no settling needs detecting once ε > 0) **[measured]**; table re-derived, L = 16, ε = 10⁻³ re-run
(identical):

| ε | L = 12 | L = 16 | L = 20 |
|---|---|---|---|
| 0 (settled states censored) | 5.644 ± 0.013 | 7.407 ± 0.011 | 9.142 ± 0.011 |
| 10⁻⁴ | 7.108 ± 0.015 | 7.433 ± 0.011 | 9.139 ± 0.011 |
| 10⁻³ | 6.866 ± 0.014 | 7.398 ± 0.011 | 9.136 ± 0.011 |
| 10⁻² | 5.975 ± 0.013 | 7.414 ± 0.011 | 9.126 ± 0.011 |
| 3×10⁻² | 5.655 ± 0.012 | 7.381 ± 0.011 | 9.025 ± 0.010 |

- At L = 16 and 20, where a deterministic strip essentially never settles, **the deterministic rule is the ε → 0
  limit**: ln τ is flat to 0.03 up to ε = 10⁻², and 3% noise lowers ln τ(20) by only 0.12 (dI/dε ≈ −0.8 ± 0.2; F6's
  "1 < c < 6" was wrong).
- At L = 12 the limit is singular: 3% of the residences of deterministic 16 × 12 strips end by settling into debris
  that keeps cells in both edge rows. With ε = 0 they are censored; with small ε they are living edges that only
  noise can kill, and the mean wait *rises* to e^{7.1} as ε → 0. The noisy law converges to the deterministic law
  *of the chaotic states*, and to something else (the noise-lifetime of debris, growing like a power of 1/ε)
  wherever debris has non-negligible weight. (`report.py noise` also prints slopes over L = 12–20; at small ε they
  are dominated by the L = 12 singularity and mean nothing.)
- Theorem C's bound ε^{−L} is ln τ ≤ 3.5·L at ε = 0.03: true and useless, like B′.

## 10. Is 0.416 = 2 × 0.208 a coincidence? Yes

1. **The toy's number is not 0.416.** It is an effective slope for L = 12–36 containing a fading second channel; the
   sparse channel alone is 0.41, the window cost is 0.376–0.382 at ℓ = 34–50, a log-corrected fit gives
   0.364 ± 0.006 (§4). The planned lifetimes at L = 32–40 on the six- and eight-row models (`python3 jobs.py model3`)
   were never run.
2. **Gump's number is not 0.208 either.** Rim-free faces: 0.209 (A = 27–108, this study and other work); octahedral
   faces: local slopes 0.201, 0.212, 0.212, 0.218–0.221, 0.221 from A = 30 to 135 (section 12). With 0.36–0.41 over
   0.209–0.221 the ratio is somewhere in 1.6–2.0.
3. **Geometry moves the toy's number and not gump's** (on the sizes compared here). Toy box edges cost 0.343 per cell
   (toy2d §5) against 0.41–0.44 for periodic edges at the same lengths; gump's periodic and octahedral faces cost the
   same per cell up to A ≈ 63 (§5; this no longer holds beyond A = 84).
4. **The mechanisms differ** (§5): a two-generation starvation flash with a convex rate function, against an
   erosion over five to twelve generations with a straight tail.
5. **A third member of the family lands elsewhere** (F7c, hit). Gump's rule B45/S345 on the 2D range-3 cross
   (12 neighbours; an edge cell sees 6 in-row and 3 below, gump's counts with a one-dimensional edge;
   `python3 jobs.py cross3`, strips 24 × L; L = 24 re-run, identical) sustains chaos and loses edges memorylessly
   (coefficient of variation of the ages at death beyond T0: 0.97–1.02, re-derived from the records) with ln τ = 4.077, 5.254, 5.979, 6.602, 7.159, 7.672, 8.148 at
   L = 16, 24, …, 64 (3,300–9,000 deaths each). The local slope falls from 0.147 to 0.060 per cell and has not
   levelled: neither 0.21 nor 0.42, and possibly not linear at all.

## 11. Forecasts, scored

All entries are in `exponent/PREDICTIONS.md`, filed before the runs that test them (commit order). Scores as filed
by the author unless marked *(2026-11-14)*, which are appended there with this report.

| forecast | what was said | outcome | score |
|---|---|---|---|
| F1 headline | random map with killing fails by orders of magnitude, because of debris | 20–1,000× more immortal-cycle states than \|G\|τ; 5–94% of states never lose an edge | **hit** |
| F1(a) | immortal basin 3–60% in every vessel with N ≥ 24 | 5–29% for H ≥ 4 and boxes, 49–94% in 2- and 3-row strips | miss |
| F1(b) | 4 × 8 strip: 10⁴–10⁶ immortal states, ≥ 90% period ≤ 2 | 42,493; 72% | half |
| F1(c) | period ≥ 8 immortal states within 30× of \|G\|τ_tail (50%) | 0.3–8× where they exist | hit |
| F1(d) | no clean exponential; −ln hazard slope in L < 0.2 | flat hazard; slope 0.43, 0.64, 0.29 per cell | miss |
| F2 | toy's plunge lengthens with L (×1.5 from 16 to 32; 60%) | two-generation flash at every size | miss |
| F3 | window decrement at ℓ = 20–40 = lifetime slope within 10% (60%) | 0.376–0.397 against 0.38–0.42; plus τ = 12.1/E(L − 6.5) | **hit** |
| F4 | w = 1 clean law, slope not within 15% of 0.416, "higher"; within 10% only for w ≥ 4 | 0.531 (+28%); within 10% already at w = 3 | hit / miss |
| F5 | gump model at the committed w* = 3: within 0.5 nats and slope within 10% (50%) | +0.32, +0.72, +1.02 nats; slope 0.228 (+10.2%) | **miss** |
| F5 sub | w = 3 above by 0.1–0.6 at A = 63, slope 0.21–0.23 | above by 1.02; slope 0.228 | sign and slope hit, size miss |
| F6 | continuity at ε → 0 (within 3%); slope falls with 1 < c < 6 | continuity hit (L = 16, 20; singular at 12); c = 0.8 ± 0.15 | hit / miss |
| F7(a) | toy's asymptotic slope differs from 0.415 by > 3% | supported by two estimators of three; amended to "0.36–0.41, not settled" | open (author's amendment) |
| F7(b) = F8(c) | periodic gump faces' slope differs from 0.208 by > 5% | same slope as octahedral, 0.2095–0.2133 against 0.2010–0.2119 | miss |
| F7(c) | range-3 cross: slope neither 0.208 nor 0.416 within 10% | 0.147 → 0.060 | hit |
| F8(a) | periodic model converges: \|Δ\| ≤ 0.15 at w = 6, 8 (65%) | all within 0.03 | hit |
| F8(b) | w = 3 again the worst depth, too tough | too tough, but w = 2 is worse | miss |
| F9 | eight-row toy model insensitive to ρ (0.30, 0.60 within 0.1; 55%) | all within 0.02 | hit |
| F10 | gump model R = 13, w = 4 within 0.2 of 18.077 (65%) | 18.179 ± 0.113 (78 deaths): +0.10 | **hit** *(2026-11-14)* |
| F11(a) | octahedral slope level or rising beyond A = 84: Δ(84→108) = 5.18 ± 0.10, Δ(108→135) = 5.89 ± 0.16 | GPU, reviewed: 5.235 (GPU's own A = 84) or 5.30 ± 0.06 (verified A = 84); 5.96 ± 0.25. Slopes 0.218–0.221, 0.221 | **hit** *(2026-11-14)*; not blind (author disclosed having seen the GPU numbers) |
| F11(b) | asymptote 0.214–0.225 (70%); not 0.2077 (85%) | octahedral local slope 0.221 at A = 135 and still rising; limit unknown. The forecast's stated basis (rising periodic slopes) failed (F11c) | not decided *(2026-11-14)*; "not 0.2077" consistent with all data since |
| F11(c) | periodic model A = 75: ln τ = 15.74 ± 0.05, slope 60 → 75 ≥ 0.2115 | 15.640 ± 0.025; slope 0.208 | **miss** *(2026-11-14)* |
| L = 32–40 (amendment of 19:56Z) | sparse-channel slope 0.385–0.410 between L = 32 and 40 (55%) | runs never made | unscored *(2026-11-14)* |

Tally: 8 hits, 7 misses, 4 split, 3 open or unscored. The misses that taught the most were F5 (the depth fixed
from the toy was one layer too shallow for gump), F2 and F7b (the author expected the two automata to share a death
mechanism and a geometry effect; they share neither), and F11c (the periodic rise on which F11 rested).

## 12. What has changed around the study since it stopped (to 2026-11-14)

- **Lemma A (c) was false.** `theorems.md` said, tagged [proved]: "a gump face can always die in one generation given
  suitable layers beneath". The per-cell part (no face cell is safe) is true; the statement about a whole face is not,
  because neighbouring face cells share the cells beneath them. Counterexample (board item E10, critic's lab
  `face_one_step.py`, `face_one_step_interior.py`): in the layer x + y + z = 13, live (4,4,5), (4,5,4), (5,4,4),
  (3,4,6). (4,4,5) dies only if all three cells beneath it are alive and (4,5,4) only if all three beneath it are
  dead, and both sets contain (3,4,4). Re-checked here by enumerating the neighbourhood of `docs/AUTOMATON.md` §2, and
  `python3 face_one_step.py 3` (re-run): 187 of 512 configurations of the R = 3 hull face cannot be emptied in one
  generation; at R = 5, 180,615 of 262,144 (lab L0b.3, not re-run). All can be emptied in two (R = 3, 5 and the
  periodic faces 2 × 2, 3 × 2; larger faces unknown). `theorems.md` is corrected in place, with the false sentence
  kept struck through. **Nothing else in the study leaned on it**: Theorem B, B′, C and D′ concern the toy and its
  driven models, where the cells beneath are not shared, and every gump result here is a measurement.
- **The fit −ln h/A → 0.2077 + 0.55/A is retired** (`research/fluct/README.md`, note of 2026-11-13; it misses its own
  A = 45 point by 28 standard errors). The study's forecasts quote it as the target; the author stopped using it as a
  test in the F11 entry, and none of the model comparisons in §5 used it (they compare with measured lifetimes).
  Octahedral faces (GPU, reviewed; `research/audit/REVIEW-gpu-pr8.md`): ln τ = 23.376 ± 0.031, 29.34 ± 0.25 at
  A = 108, 135; local slopes 0.218–0.221, then 0.221. **Rim-free slab faces** (eight layers, periodic in plane):
  ln τ_face = 22.470 ± 0.047 at A = 108, on the line −0.091 + 0.2088·A fitted to A = 27–90 (`research/NOTEBOOK.md`,
  2026-11-14, "GPU round two"; `research/CLAIMS.md` GP7); the A = 126 point (26.138 ± 0.091) is only a lower bound
  because transverse firewalls were not detected (corrected estimate ≈ 26.36). An octahedral face at A = 108 is
  0.91 ± 0.06 nats tougher than a slab face.
  What this does to the study: (i) its own periodic faces (twelve layers) agree with that line within 0.07 nats at
  A = 27–60 (5.501, 7.386, 9.937, 12.496 against 5.547, 7.426, 9.931, 12.437) and at A = 75 (15.640 against 15.569,
  model w = 5); its "rising" periodic slopes of 0.2106–0.2134 are a ±0.07-nat wiggle about a slope of 0.209, not a
  trend. (ii) "Periodic and octahedral faces have the same slope" (§5) holds only where the study measured,
  A ≤ 63–84; beyond, octahedral faces are steeper (0.218–0.221 against 0.209). What makes them tougher (rim, eight
  faces sharing edges, a thicker interior, shape) is not separated (notebook, 2026-11-14). (iii) F11(a)'s direction
  for octahedral faces came true; its basis did not.
- **The swarm of theory agents** (`research/theory/swarm/`) uses this study's drivers and numbers: its dice models
  D2 and D3 are `xp.toy_model`, `xp.gump_model`, `xp.gump_slab_model`; its examiner validated a copy of `drv.c`
  (V1–V3, §1). Where the critic's board (`critic/board.md`) touches this study:
  - **E10** (Lemma A c): agrees with the correction above.
  - **E1** (toy law not a straight line; target 0.36–0.42): agrees with §4's 0.36–0.41, reached independently.
  - **E2** (gump slope does not fall; rim-free 0.2088): agrees with §12 above; it overturns the study's F11 basis
    and its "same slope" statement beyond A ≈ 84.
  - **E3** (octahedral faces mostly rim; 30 interior cells of 63): agrees with §5.
  - **E8, E12** (competing hazards: in strips, cuts by dead columns outnumber edge deaths; in slabs, sealed bands of
    another diagonal): the study censors and reseeds these events, so its τ is a hazard conditional on not being
    cut, as the board's definition of τ requires. In the study's 16 × 28 strip there were 17,825 other events
    against 3,109 edge deaths. Its slabs (twelve layers, widths ≤ 5 cubes) are in the face regime by E12's criterion.
  - **E9** (2D: some deaths from a nearly full row): agrees with §2's dense channel (20% at L = 12 to 1% at L = 28).
  - **E13** (an i.i.d. outside gives too steep a constant in 2D only; gump over dice is a nat short-lived at one layer
    and right at four to five): reads this study's numbers and agrees with §3, §5, §8 (marked there "sampled,
    unchecked").
  - **E14** (death takes a few generations: two statements of different standing): the board accepts the toy's
    two-generation flash as reported (unchecked) and finds, from the fluct histories, that a gump face's collapse
    lengthens with A. Consistent with §5's "five to twelve generations"; it contradicts the premise of the study's F2
    ("in gump a dying face is ordinary until ≈ 16 generations before death at every size"), which was taken from the
    fluct README. The board also finds (lab L8.3) that one row over dice dies by a collapse that lengthens with L, as
    §3 says for the w = 1 model.
  - **Graveyard 3, 4, 6, 7, 9, 10, 12** cite this study: decaying correlations are not enough (Theorem E remark,
    checked); the random map with killing fails (§6.2); the block construction fails, but for one of the study's two
    reasons only (§7; note added to theorems.md); shallow dice models are not a formula for the constant (§3, §8);
    0.416 = 2 × 0.208 (§10); 0.2077 as gump's asymptote; the plunge lengthening with L (F2, false).
  - Claims of the swarm that bear on the study but are its own and not checked here: a lower bound e^{cL} for an edge
    over dice near the law "b = 0 or 2 by a fair coin" (probability's Theorem A, modulo two cited percolation facts);
    "one exponent in every geometry, the ring's excess being a power of L" (board E15, a guess with exact support in
    dice models), which would make §6.1's ring slope 0.52 an effective value above an interval exponent of 0.46.

## 13. Not checked / known weaknesses

- **Re-runs are replays.** The pipeline is deterministic (§1), so the re-runs confirm the code and the arithmetic, not
  the statistical error bars. The only independent samples are the validations against toy2d and fluct, and the
  swarm's V1–V3 and E3.
- **Not re-run, taken from the filed records:** every simulated number not in the re-run table of §1 — in particular
  the toy model at w ≠ 8 and L ≠ 16, the truth strips at L = 20–28, the gump model at R ≠ 9 or w ≠ 4, the A = 84 and
  A = 75 points, the slab models, `rhoscan`, `slave`, `clone_corr.py`, `sync_check.py`, `regrow.py`, `mfld.py`, the
  pre-death profiles and the histogram distances of §3, the end-game numbers of the gump model in §5, and the
  "sparse only" columns of §2. Exact N = 32 functional graphs were not re-run (one N = 28 vessel was).
- **Few deaths at the largest sizes:** A = 84 has 78 deaths (± 0.11), A = 75 has 1,585.
- **Error bars on slopes** from straight-line fits are not meaningful (χ²/dof ≈ 12–21 in §3); the local slopes are
  the honest numbers.
- **The window costs beyond ℓ ≈ 34** are less precise than filed (§4, overlapping windows), and the eight-row model,
  which matches the lifetimes, does not reproduce the deterministic strip's window cost there. The identity
  τ = 12.1/E(L − 6.5) is a two-parameter fit tested on seven points, with the last two residuals both positive.
- **Small numerical discrepancies between the files:** hierarchy slopes for w = 8 and the truth (0.4281, 0.4254 in
  the author's draft; 0.4273, 0.4252 from `report.py hier`); the window cost "0.397 at ℓ = 20" in PREDICTIONS
  (F3 outcome) is the step 21 → 22 in the table's convention (the step 20 → 21 is 0.399); residuals of
  12.1/E(L − 6.5) differ by ≤ 0.01 from the filed ones depending on how E is interpolated. None changes a conclusion.
- **The noise density is 12-bit** (0.47192, 0.41553): a 10⁻⁴ effect on ln τ (§6.1), irrelevant to every conclusion.
- **T0 and the quasi-stationary state.** The rate measured after T0 is the quasi-stationary rate only if T0 exceeds
  the relaxation time (board, from Méléard–Villemonais). For the dice models the second eigenvalue is ≈ 0.5 (board),
  so T0 = 200–300 is ample; for the deterministic vessels no relaxation time is known.
- **Censoring.** Settled states, cuts and firewalls are reseeded, not counted; the lifetimes are conditional on chaos
  and on not being cut. Undetected long cycles (period > 262,144 and not caught by the snapshots) would be counted as
  living; not checked here (the examiner's protocol reports the oldest replica's age; this study did not).
- **Gump's mechanism claims** (erosion over 5–12 generations, ln τ = 0.403⟨n⟩) rest on one periodic size series
  (A ≤ 60) and the model at A = 63; the octahedral ones on the driven model, not on the deterministic hull.
- **The study never tested its static formulation (§4) on gump**, nor whether gump's per-live-cell constant 0.40
  survives at the sizes where octahedral and periodic faces part (A ≥ 84).
- **The figures** (`research/figures/exponent_{flash,hierarchy,gump}.png`) were made by the author from these records
  and were not regenerated; `figures.py rate` and `figures.py fg` would write two more that were never committed.
