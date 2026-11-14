# Where the face-law exponent comes from

*Revised 2026-11-14 after `research/audit/REVIEW-exponent.md` (adversarial review; its sections are cited as R§n,
and its numbers come from the reviewer's own code in `research/audit/exponent/`, which shares none with this study's
drivers). The changes are listed in the last section. Parts the review lists under "Not checked" are marked
**[not independently checked]**.*

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

The question has no complete answer in this material. What stands after the review:

1. **[measured]** **The exponent is set by a thin boundary layer over a memoryless reservoir, to within a few
   hundredths of a nat.** Keep the rule on the top w rows (toy) or {111} layers (gump) and replace everything beneath
   by fresh coin flips every generation:
   - *Toy*, w = 8: within 0.05 nats of the deterministic 16 × L strips at L = 12–28 in the study (0.00–0.04). The
     lead's independent check (`research/audit/exponent/lead_check.py`: 5.654, 7.425, 9.136, 10.855 at
     L = 12, 16, 20, 24) is within 0.02 of the strips at the three smaller sizes and 0.067 ± 0.027 above at L = 24,
     so "within 0.05" holds at L = 12–20 and is at its edge at L = 24. The whole quasi-stationary law of the edge
     agrees too, and the coin density hardly matters (ρ = 0.30 or 0.60 moves ln τ by ≤ 0.02) **[not independently
     checked]**.
   - *Gump, periodic faces*: from w = 5 on the model equals the deterministic slab within 0.015 nats at A = 27, 48
     and 60 in the reviewer's runs, and at A = 75, where the reviewer measured the deterministic slab for the first time
     (15.660 ± 0.027, 1,341 deaths), within 0.02 ± 0.04 (R§1.2). w = 4 is +0.06–0.07 too tough at A = 48–60.
   - *Gump, hull (octahedral) faces*: w = 4–5 agree within 0.05 nats at A = 45–63, but this depth was noticed after
     the runs, when the committed forecast w* = 3 had missed by 0.3–1.0 nats (F5). Deeper models (w = 6, 8; R§1.1)
     do not approach the deterministic hull: they settle 0.03–0.04 nats *below* it at A = 45 and 63 (4–5σ at
     A = 45). The hull model agrees to ≈ 0.04 nats with a small systematic offset, not exactly; w = 4's closeness is
     partly a crossing (w = 3 too tough, w ≥ 5 low). At A = 84 (w = 4) the model gives 18.183 ± 0.037 (719 deaths)
     against the deterministic hull's 18.148 ± 0.028 (1,250 deaths), +0.035 ± 0.047 (R§1.4); the study's own
     78-death point (18.179 ± 0.113) is not a test. At A = 30 the model is 0.25 low (that hull has no bulk).
   - *The noise models can settle.* A cube of six live faces on the face, everything else dead, is a fixed point of
     gump's models whatever the noise does (R§1.3, `research/audit/exponent/trap.py`); model runs must censor
     repeating states. At the sizes measured the effect on the filed numbers is small (§5).

   So, at these precisions, the deterministic chaos of the bulk enters the law only as a source of noise (§3, §5;
   `jobs.py model1 | model2 | gump | slab | slabmodel`).
2. **[measured; a fit found after the runs]** **In the toy, τ_edge(L) = 12.1 / E(L − 6.5)**, E(ℓ) = probability that
   ℓ given consecutive cells of a long living edge are empty, fits the seven lifetimes L = 12–36 with residuals
   ≤ 0.07 nats but χ² = 17/5 (p ≈ 0.004, R§2). The formula was found after the runs (forecast F3 said only that the
   window decrement would lie within 10% of the lifetime slope). Fitted to L = 12–28 alone it predicts L = 32 and 36
   low by 0.08 ± 0.04 and 0.07 ± 0.05 (R§2). What it shows: over ℓ ≤ 30 the curvature of −ln E matches that of
   ln τ; the lifetimes do not reach the window lengths (ℓ > 30) where a decay rate would be read, so "the exponent is
   the decay rate of E" is compatible with the data, not supported by it. The window costs at ℓ > 30 carry honest
   errors of ± 0.006 (ℓ = 34 → 42) and ± 0.03 (42 → 50), and an independent run gives 0.387 ± 0.006 at 34 → 42
   against the filed 0.376 (R§2; §4). Not tested for gump.
3. **[measured]** **The two automata die differently; whether 0.416 ≈ 2 × 0.208 is a coincidence is not
   established.** The toy's edge starves in a two-generation flash together with the two rows beneath **[not
   independently checked]**; a gump face erodes over 5–12 generations with a straight tail (one periodic size,
   A = 60, and the octahedral model at A = 63: not a size law). Gump's periodic faces fit ln τ = a + b⟨n⟩ with
   a = 0.085 ± 0.025, b = 0.399, and the area law a + bA fits better (R§3): 0.40 per live cell is gump's area slope
   0.21 divided by its live density 0.52, not a second finding. The ratio of the two slopes is somewhere in 1.6–2.0:
   the toy's asymptotic slope is 0.36–0.41 (the lower end rests on a log-corrected fit alone; the window cost is
   ≈ 0.38–0.39 at ℓ = 30–42), gump's is 0.209 on rim-free faces (to A = 108, other work) and 0.218–0.221 and rising on
   octahedral faces (A = 84–135, other work). No reason for the factor 2 was found, and the data neither confirm nor
   exclude it (§2, §4, §5, §10, §12).
4. **[proved]** Only bounds of the right *form*: E T ≤ 3δ^{−3L} for a driven edge, E T ≤ ε^{−L} with noise, and
   τ ≥ θ^{−⌊L/m⌋} *if* the ring's own quasi-stationary edge law is ratio-mixing with constant θ. That hypothesis is
   not measured: the window ratios ≤ 0.688 (5 ≤ ℓ ≤ 41) come from a different system, a 16 × 128 strip, and make it
   plausible, not supplied (R§4). Whether decaying correlations alone can fail to give an exponential wait is open:
   the counterexample offered does not have decaying correlations (R§4); what it shows is that an additive
   correlation floor of order e^{−√L} suffices to break the implication. The geometric death law from every start
   is proved for the one-row toy model only, not for gump's models (they have noise-immune debris). No lower bound
   τ ≥ e^{cL} is proved for any system studied here, and no formula gives the constant: mean-field large deviations,
   the Gaussian and a single driven row all fail by 20–50% ([measured], §8, **[not independently checked]**).
5. **[exact]** In small vessels (N ≤ 32 cells) the enumeration is bit-identical to an independent brute force
   (R§0, N ≤ 24). The edge-death hazard is flat over about one e-fold of the death time (4 × 8 strip: 0.102–0.111
   for t = 6–16), which is weak evidence for "geometric". The "random map with killing" heuristic fails by orders of
   magnitude on all immortal states, 67–99% of which are debris (still lifes and period-2 patterns touching every
   edge). But the test of the chaotic component is **inconclusive**: 7 of the 17 vessels with N ≥ 24 have no
   immortal cycles of period ≥ 8 at all (|G|τ = 22–197 expected), cycles of period ≥ 3 still exceed |G|τ by 1–56×,
   the long cycles are clockwork, and with τ = 3–10 generations there is no long-lived chaotic component to compare
   with a random map (R§5; §6.2, `fg_run.py run 32`).

So, as far as this material goes: the exponent belongs to a few layers at the boundary, driven by noise, up to a
systematic offset of a few hundredths of a nat for hull faces. In the toy the lifetimes share their curvature with
the cost of an empty stretch of edge; whether they share its asymptotic decay rate is not tested. Its value is not
derived from the rule, and the numbers that the study tried to explain have themselves moved since (section 12).

## 1. Tools and validation

- `drv.c` + `xp.py`: bit-sliced replicas (256 per run) of an outer-totalistic rule on an arbitrary directed cell
  graph. Each cell is *dynamic*, *noise* (i.i.d. Bernoulli, redrawn every generation; density stored with 12 bits,
  so 0.472 is 0.47192) or dead. Optional death noise ε. Quasi-stationary sampling with restarts: states younger than
  T0 = 300 generations (200 for gump) are not measured. Censored and reseeded: settled states (period ≤ 2 checked
  every generation; snapshots at 64 / 4096 / 262,144, compared within one chunk only, R§0), strips cut by three dead columns, interior firewalls, and in
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
3,100–8,600 edge deaths per size, every death's last 64 generations kept. **[measured]** **[not independently
checked]**: the flash and channel tables of this section and the toy lifetimes themselves were outside the review
(R§8). (Table re-derived from the
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
- **Splitting cannot work.** `python3 clone_corr.py 20 3000 3` (not re-run; **[not independently checked]**): two clones of one state, each with one
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
exactly geometric from its quasi-stationary state (Theorem D). From an arbitrary start this is proved for w = 1
only (Proposition D′, irreducibility). For w ≥ 2 nothing proved here excludes a second absorbing class, and the
corresponding gump models do have one: noise-immune fixed points (§5, R§1.3). Whether the toy models with w ≥ 2
have such debris was not checked; model runs should censor repeating states, as the deterministic runs censor
settled ones.

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

- **With eight rows the model is close to the deterministic strip:** ln τ within 0.00, 0.03, 0.02,
  0.04, 0.01 (errors 0.02). The lead's independent check of the eight-row model
  (`research/audit/exponent/lead_check.py`, numpy, no shared code; results in its docstring) gives 5.654 ± 0.010,
  7.425 ± 0.010, 9.136 ± 0.013, 10.855 ± 0.018 at L = 12, 16, 20, 24: the study's eight-row numbers are reproduced
  (largest difference 0.029, 1.5σ), and against the strips the model is within 0.02 at L = 12–20 and
  0.067 ± 0.027 above at L = 24 (the study's own point there: +0.040). So "within 0.05" holds at the three smaller
  sizes and is at its edge at L = 24; L = 28 was not re-checked. **[not independently checked]** from here to the
  end of this section (R§8): the whole quasi-stationary distribution of the edge population agrees too:
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

Window samples overlap in space (one empty stretch of length r gives r − ℓ + 1 windows of length ℓ) and persist in
time, so the counts are not independent, and the filed figure "0.376 ± 0.002 over ℓ = 34–41" is too precise. The
honest errors (R§2): the spatial part alone, exact from the filed counts (compound Poisson over maximal empty runs,
`research/audit/exponent/verdict2.py errors`), is ± 0.0010 at ℓ = 30 → 31, ± 0.003 over 34 → 42 (33,822 runs of
length ≥ 34) and ± 0.009 over 42 → 50 (1,701 runs); with the time correlation included (the reviewer's own
16 × 128 run, 5.0×10¹¹ samples, jackknife over 1,033 batches of 2×10⁶ generations) they are ± 0.0015, ± 0.006 and
± 0.03. The reviewer's run is also an independent value:

| window cost −ln[E(ℓ+1)/E(ℓ)] | ℓ = 10 → 11 | 20 → 21 | 30 → 31 | mean 34 → 42 | mean 42 → 50 |
|---|---|---|---|---|---|
| filed (2.7×10¹¹ samples) | 0.4342 | 0.3992 | 0.3817 | 0.3763 | 0.3824 |
| independent run, R§2 (5.0×10¹¹ samples) | 0.4342 ± 0.0000 | 0.3995 ± 0.0002 | 0.3852 ± 0.0015 | 0.3874 ± 0.0064 | 0.378 ± 0.027 |

So the filed 0.3817 at 30 → 31 and 0.376 at 34 → 42 are not reproduced (2.3σ and 1.7σ); ≈ 0.38–0.39 at
ℓ = 30–42 is what two independent runs support, and the ℓ = 42 → 50 entries carry no information at the level
discussed here. (The row for the eight-row model was not discussed by the author, and its window statistics were
not independently checked, R§8.)

- **[measured; a fit found after the runs] τ_edge(L) = 12.1 / E(L − 6.5).** One shift and one prefactor fit all
  seven lifetimes from L = 12 to 36 (this study's to 28, toy2d's at 32 and 36; ln τ from 5.6 to 15.6) with residuals
  +0.03, −0.02, −0.01, −0.01, +0.03, +0.07, +0.05 nats, ≤ 0.07 nats in size but **χ² = 17.3 on 5 degrees of freedom
  (p ≈ 0.004)**: at the quoted errors the fit is rejected (2.2σ at L = 12, 1.9σ at L = 32; R§2,
  `research/audit/exponent/verdict2.py fit`, which reproduces shift 6.5 and prefactor 12.05). Re-derived 2026-11-14
  for L = 12–28 with log-linear interpolation of E: +0.025, −0.026, −0.009, −0.017, +0.022; R§2 gives all seven:
  +0.030, −0.022, −0.005, −0.013, +0.026, +0.071, +0.054. The formula was found after the runs; forecast F3 said only
  that the window decrement at ℓ = 20–40 would lie within 10% of the lifetime slope.
  - *How much is fit* (R§2). The shift is not degenerate with the prefactor (χ² = 52.6, 20.7, 17.3, 23.8, 63.4 at
    shift 5, 6, 6.5, 7, 8; 1σ range 6.05–6.80 after scaling by χ²/dof), so the two constants fix level and
    curvature: the content is that −ln E(ℓ) over ℓ = 5.5–29.5 has the same curvature as ln τ(L) over L = 12–36. A
    three-constant smooth curve does better (a + bL + c ln L: χ² 4.6/4).
  - *Out of sample* (R§2). Fitted to the five L = 12–28 points only (shift 6.25, χ² 11.0/3), the formula predicts
    toy2d's L = 32, 36 low: residuals +0.083 ± 0.038 and +0.068 ± 0.045 (+0.074, +0.056 with the shift held at 6.5).
    Lifetimes rise faster than 1/E at the largest L; the last two residuals of the seven-point fit are the same effect.
  - *What it does not reach.* The largest window used is ℓ = 29.5. The eight-row model's E, whose cost beyond
    ℓ = 34 is 0.396–0.417, fits the same seven lifetimes as well (χ² 13.5); the one-row model's fails (χ² ≈ 15,000).
    With the independent E of the table above the residuals are the same (χ² 16.2).

  A ring of L cells dies about as often as a window 6.5 cells shorter is found empty in an endless edge, over
  the range measured. For the contact process the Durrett–Schonmann picture (extinction exponent of a finite system =
  decay rate of the empty-interval probability of the infinite one) is a theorem; here the data show only part of
  it. Forecast F3: hit as forecast (the decrement band); the formula is post hoc.
- So, **in the toy, over ℓ ≤ 30 the curvature of −ln E matches that of ln τ; the lifetimes do not reach the window
  lengths (ℓ > 30) where the decay rate would be read.** "The exponent is the decay rate of E" is compatible with the
  data, not supported by it, and the out-of-sample residuals lean the other way. The hypothesis of Theorem E(a) is
  not a measured fact either: it would follow if the ring's own quasi-stationary law had the window ratios measured
  in the 16 × 128 strip for ℓ ≤ 41 (E(ℓ+1)/E(ℓ) ≤ 0.688 for 5 ≤ ℓ ≤ 41), at every ℓ < L; that is not measured (the
  strip is a different, deterministic system, for which no quasi-stationary law exists, and ℓ stops at 41; R§4).
  The measurement makes the bound τ ≥ 0.688^{−L} plausible; it does not make it a theorem.
- **"0.416" is not the asymptotic constant.** Three estimates of where the slope ends: the window cost, ≈ 0.38–0.39
  at ℓ = 30–42 (two independent runs; the filed 0.376–0.382 at ℓ = 34–50 is not reproduced, and ℓ > 42 has ± 0.03,
  table above); the fit ln τ = a + I·L + b·ln L to the seven lifetimes, I = 0.364 ± 0.006, b = 1.14 ± 0.12 (χ²
  4.6/4; a straight line has χ² 95/5, I = 0.4215); the sparse channel alone, 0.41 ± 0.005 and nearly straight over
  L = 12–28 (§2). The eight-row model, which reproduces every lifetime, has a window cost of 0.396–0.417 beyond
  ℓ = 34 [not independently checked]. Range for the toy's asymptotic slope: **0.36–0.41**, whose lower end now rests
  on the log-corrected fit (0.364) alone: the window cost no longer supports it. toy2d's 0.416 ± 0.0014 is an
  effective slope for L = 12–36 (the swarm's critic, board E1, independently: 0.36–0.42).

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
| 4 | 6.550 ± 0.009 | 9.808 ± 0.010 | 13.653 ± 0.022 | 18.179 ± 0.113 (78 deaths; not a test) |
| 5 | 6.580 ± 0.009 | 9.782 ± 0.010 | 13.592 ± 0.022 | |
| measured hull (`research/fluct`) | 6.804 ± 0.003 | 9.819 ± 0.003 | 13.633 ± 0.008 | 18.077 ± 0.054 |
| *independent runs, R§1.1, R§1.4 (repeating states censored):* | | | | |
| 4 | 6.541 ± 0.001 | 9.798 ± 0.008 | 13.633 ± 0.023 | **18.183 ± 0.037** (719 deaths) |
| 5 | | 9.793 ± 0.006 | 13.601 ± 0.024 | |
| 6 (new) | | 9.795 ± 0.006 | 13.609 ± 0.026 | |
| 8 (new) | | 9.779 ± 0.007 | 13.610 ± 0.028 | |
| deterministic hull | 6.784 ± 0.002 (6.809, see below) | 9.823 ± 0.004 (pooled) | 13.644 ± 0.006 (pooled) | **18.148 ± 0.028** (1,250 deaths) |

(R§1.1: w = 3 at A = 63 is 14.591 ± 0.035. Every reviewer model value agrees with the study's within 1.3σ. The
independent CPU value at A = 84 is 18.154 ± 0.025, `research/audit/REVIEW-gpu-pr8.md`.)

**The depth that works was found after the forecast failed.** At w = 3 the model is too tough by 0.32, 0.72,
1.02 nats. At w = 4 and 5 the study's runs reproduce the measured faces at A = 45 and 63 to −0.01, +0.02 and
−0.04, −0.04 nats; this was noticed in the table that scored F5, not forecast. **The deeper models do not converge
to the deterministic hull** (R§1.1): against the reviewer's pooled truth, w = 4, 5, 6, 8 are −0.025, −0.030,
−0.028, −0.044 at A = 45 (the w = 6, 8 offsets 4–5σ) and −0.011, −0.043, −0.035, −0.034 at A = 63 (± 0.026). The
hull model settles about 0.035 nats below the deterministic system as w grows; "within 0.05" is true of every entry
with w ≥ 4, but it describes a small systematic offset, not statistical agreement, and w = 4's closeness is partly a
crossing (w = 3 is +0.7 to +0.9 too tough, w ≥ 5 low). At A = 84 (w = 4) the reviewer's 719-death run gives
18.183 ± 0.037 against the deterministic hull's 18.148 ± 0.028, model − truth = **+0.035 ± 0.047** (+0.029 ± 0.045
against the CPU value); the study's 78-death point (+0.10 ± 0.13 against fluct, +0.03 against the CPU value;
forecast F10, hit) has ± 0.11 and is not a test on its own. The w = 4 offset runs −0.025, −0.011, +0.035 at A = 45, 63,
84, all within about 2σ of −0.01. The reviewer's hull value at A = 84 sides with the CPU review (18.154) against
fluct's 18.077 ± 0.054.
At A = 30 the deterministic hull's value depends on a definition: counting a generation in which two faces die as
two deaths gives 6.784 ± 0.002, counting it once gives 6.809 (2.5% of first peels take two faces at once; R§1.1,
R§1.5); fluct's 6.804 is the second convention. The model comparison there (0.25 low) is unaffected in
conclusion. The known end-game is
reproduced too: h/p₁ = 0.60–0.62 (fluct: 0.60–0.61), deaths from n = 1/2/3 in the proportions 62/24/9% (63/23/9%),
p₁/p₂ = 0.66–0.67 (0.65–0.66), and the excess at three cells (ln p₄/p₃ = 0.32 between neighbours of 0.60 and 0.44);
these end-game numbers were not re-derived. At A = 30 the model is 0.25 low: the R = 7 hull has no bulk under its
faces (its fifth layer is the centre). In the hull, convergence in depth is not monotone (w = 1 too weak, w = 2, 3
too tough, w ≥ 5 slightly low); one layer deeper than the toy's 10% criterion was needed. Slopes over A = 30–63:
0.2159 (w = 4), 0.2128 (w = 5), 0.2060 (truth); over A = 45–63: 0.2136, 0.2117, 0.2119 (fitted slopes; their
nominal errors inherit the poor χ² noted in §3, R§6).

**The noise models can settle** (R§1.3). The models are not free of absorbing debris other than death. In
`xp.gump_model(7, 4)` the six faces of the cube centred at (6,0,0) — (7,0,0), (6,1,0), (6,0,1) in the face layer,
(5,0,0), (6,−1,0), (6,0,−1) one layer in — alive, with every other dynamic cell dead, is a fixed point *whatever the
noise does*: every dynamic cell's next state is forced, and the face never dies (`python3 trap.py` in
`research/audit/exponent/`). The vertex cube is immune in every hull model with w ≥ 4 (R = 7, 11, 13), and a cube in
the face interior is immune in every hull or periodic model with w ≥ 5 (not at w ≤ 4). So the death law of these
models is not exactly geometric from an arbitrary start (Theorem D gives it from the quasi-stationary state of the
living, unsettled chain only), and **model runs must censor repeating dynamic states**, as the deterministic runs
censor settled ones. Without that censoring the reviewer's R = 7, w = 4 run lost a third of its exposure to trapped
replicas (ages to 3×10⁶, no deaths) and gave ln τ = 6.944; with it, 6.541 ± 0.001 (187 trapped replicas per 533,295
deaths). The study's runs have no censoring of repeating dynamic states beyond `drv.c`'s settled-state checks (period
≤ 2 and snapshots compared within one chunk; whether these catch the trap in the models was not established), but
they restart every replica at every chunk, which limits the bias: the filed 6.550 is close to the censored value.
Which filed numbers could be
affected: every hull-model entry with w ≥ 4 and every periodic-model entry with w ≥ 5, most at the smallest sizes
(in the reviewer's runs repeating states occurred 163–741 times per 0.45–0.76 million deaths in the A = 27 slab
models, 3 times at A = 48 (w = 4), never at A ≥ 60, and not in the A = 84 run). Where the reviewer's censored runs
and the filed ones both exist they agree at the quoted errors, which bounds the effect for those entries; the
others (the slab models at A = 36 and at w = 8, the hull models at A = 30 for w = 5, and the toy models with
2 ≤ w ≤ 6 and the eight-row toy model at L = 28, whose debris was not examined; the lead's check bounds w = 8 at
L = 12–24) are not bounded by a check.

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
| 75 | **15.660 ± 0.027** (R§1.2, 1,341 deaths; new) | | | | −0.02 (filed model 15.640 ± 0.025, 1,585 deaths) | | |
| *independent runs, R§1.2:* | | | | | | | |
| 27 | 5.501 ± 0.003 | | +0.102 | +0.018 | +0.002 | +0.001 | |
| 48 | 9.929 ± 0.006 | | | +0.057 ± 0.008 | +0.014 ± 0.008 | | |
| 60 | 12.491 ± 0.010 | | +0.242 | +0.068 ± 0.017 | −0.001 ± 0.017 | +0.005 ± 0.018 | |
| 75 | 15.660 ± 0.027 | | | | +0.018 ± 0.042 | +0.002 ± 0.043 | |

(Model errors 0.009–0.018; in the reviewer's rows ± 0.0015 at A = 27 unless given.) Here the convergence is
monotone, as in the toy, and **from five layers on the model is the slab**: in the reviewer's runs within 0.015 at
A = 27, 48, 60 and +0.02 ± 0.04 at A = 75, where the deterministic slab has now been measured (R§1.2; the filed
model differs from it by −0.02 ± 0.04). w = 4 is +0.06–0.07 too tough at A = 48–60 in the reviewer's runs (6σ at
A = 48; filed +0.05), so the statement is "w ≥ 5", not "w ≥ 4". (F8a hit: all eight entries at w = 6, 8 within 0.03;
F8b miss: w = 3 is not the worst depth here.)
Independent checks: the swarm's examiner got 7.4023 ± 0.0154 for the 3 × 4 × 12 slab (V3) and 12.480 ± 0.018 for a
5 × 4 × 8 slab at A = 60 (its entry E3), against 7.386 / 7.398 (pooled) and 12.496 here.

**Periodic and octahedral faces: same slope up to A ≈ 63, not beyond.** Local slopes of ln τ per cell: periodic
0.2095 ± 0.0028, 0.2126 ± 0.0023, 0.2133 ± 0.0021 (A = 27 → 36 → 48 → 60), then **0.208 ± 0.002 (60 → 75, w = 5
model)**, or 0.211 ± 0.002 with the deterministic A = 75 slab of R§1.2 ((15.660 − 12.496)/15, arithmetic of this
revision); octahedral 0.2010, 0.2119, 0.2116 (A = 30 → 45 → 63 → 84, fluct). On that range the author concluded that
the rim changes the prefactor and not the exponent (forecasts F7b / F8c, "different by more than 5%": miss). At equal
area the octahedral face lives longer: interpolated ln τ ≈ 13.0 at A = 60 against 12.50, a factor 1.6. Half the cells
of an octahedral face of this size are rim cells with four in-layer neighbours instead of six (at A = 63: 30 interior,
30 rim, 3 corners). **Since then** (section 12) octahedral faces have been measured at A = 108, 135 with local slopes
0.218–0.221, and rim-free slab faces stay on 0.2088 through A = 108, the octahedral face being 0.91 ± 0.06 nats
tougher there. So the gap grows from ≈ 0.5 nats at A = 60 to ≈ 0.9 at A = 108: beyond A ≈ 84 the two kinds of face do
*not* have the same slope, and "the rim changes only the prefactor" holds on A ≤ 63 only.

**How a gump face dies** (same runs; `research/fluct` §1 has the octahedral case; not re-derived). The columns are
one periodic size (A = 60) and the octahedral *model* at one size (A = 63), so the generation counts below are not a
size law (board E14 finds from the fluct histories that the octahedral collapse lengthens with A; R§4):

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
- **[measured] Gump's law per live cell: a re-expression of the area law.** For periodic faces the ratio
  ln τ_face/⟨n⟩ is 0.403 ± 0.002 at all four sizes A = 27–60 (⟨n⟩ = mean living population of the face, 13.536,
  18.323, 24.733, 31.002, i.e. 0.501–0.517 of A). But a free fit ln τ = a + b⟨n⟩ gives **a = 0.085 ± 0.025** (3.4σ
  from zero), b = 0.399 ± 0.001, χ² 6.2/2, and the area law a + bA fits better (a = −0.223 ± 0.026,
  b = 0.2118 ± 0.0006, χ² 1.2/2; R§3, the reviewer's ⟨n⟩ and ln τ agreeing with the filed ones to 0.01). The ratio is
  constant because ⟨n⟩/A rises (0.501 → 0.517) just where the area law's negative intercept needs it. So "no
  intercept" is wrong, and 0.40 per live cell is the area slope 0.21 divided by 0.52 live cells per site: one
  unexplained number re-expressed, not a second finding. For octahedral
  faces the same cost per live cell appears with an intercept: ln τ = 0.40·⟨n⟩ + 1.1–1.2 for A = 45–84 (increments
  0.395, 0.398 per live cell from fluct's table; ⟨n⟩ = 0.532·A − 2.3 there). "0.21 per site" is 0.40 per live cell
  times 0.52–0.53 live cells per site. Between successive periodic sizes the cost per live cell is 0.394 ± 0.005,
  0.398 ± 0.004, 0.408 ± 0.004: not exactly constant.
- **Regrowth** **[not independently checked]** (`python3 regrow.py gump 11 5`, `regrow.py toy 8 28`, and the slab
  5 × 5 at w = 5; not re-run; JSON
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
  0.208 (F11c: miss). The rise did not continue. The deterministic slab at A = 75 (15.660 ± 0.027, R§1.2) is also
  below the forecast, by 0.08.

## 6. Exact small systems

### 6.1 One row on noise, solved exactly

The w = 1 model is a Markov chain on the 2^L rows with a product kernel: given the row, cells update independently,
alive with probability q(state, k), k = live in-row neighbours. For ρ = 0.472, q(dead, ·) = 0, 0.223, 0.721,
0.777, 0.279 and q(live, ·) = 0.223, 0.721, **1**, 0.777, 0.279 (k = 0…4; the 1 is Lemma A's safe cell).
`exact1d L 0.471924 0.471924` applies the killed kernel site by site (O(L·2^(L+4)) per step) and iterates to the
quasi-stationary distribution; the death rate is then exact, and by Theorem D′ the geometric law is a theorem for
this chain. **[exact]**; L = 16 and 20 re-run 2026-11-14 from a fresh build: identical output. **[not independently
checked]** by the review (R§8); the swarm's lab solved the same chain independently (below).

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
re-run from a fresh build (identical file). Independently: eight filed outputs with N = 16–24 are identical in every
field to the reviewer's brute force (`research/audit/exponent/fgbrute.py`, R§0); the vessels with N = 25–32 were
**[not independently checked]**.

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

- **[exact] The death-time law is flat over about one e-fold at 28–32 cells.** In the 4 × 8 strip, over all
  4.29×10⁹ initial states, the hazard of losing an edge is 0.102–0.111 at every generation from 6 to 16 (0.107 at 20;
  later it sinks to 0.06–0.08, a slower sub-population); 36% of the mortal states outlive 10 generations and 2%
  outlive 40. With τ ≈ 9 the flat stretch is about one e-fold: correct as an exact statement, weak as "geometric"
  (R§5).
  Memorylessness is there as soon as the vessel can hold any chaos (H ≥ 4; three-row strips have a hazard ≈ 0.2 that
  does not depend on L — they only settle).
- **Its rate grows with the edge at the right order of magnitude:** at H = 4, −ln h = 0.87, 1.30, 1.94, 2.23 for
  L = 5…8, steps of 0.43, 0.64, 0.29, mean 0.45 per cell, against 0.44 for deep strips at L = 12–16. The steps are too
  irregular and the strip too thin (τ = 9 against 33 for the eight-row model at L = 8) for an extrapolation.
- **[exact] The random map with killing fails by orders of magnitude, in the way forecast (F1).** It predicts
  ≈ |G|τ states on immortal cycles and a basin of |G|τ²/2^N. The vessels have 20–1,000 times more such states, and
  between 5% and 94% of *all* states never lose an edge, against a predicted 10⁻⁷–10⁻⁴. Debris dominates:
  67–99% of the states on immortal cycles are still lifes or period-2 patterns that touch every edge (98% and 99% in
  the 2 × 12 and 2 × 13 strips; R§5), and their number grows exponentially with N (H = 4: 3,374 → 8,443 → 42,493 for
  L = 6, 7, 8) while τ grows like e^{0.45L}.
- **The test of the chaotic component is inconclusive** (R§5, from `data/fg_summary.json`). States on immortal
  cycles of period ≥ 8 exist in only 10 of the 17 vessels with N ≥ 24, where they number 0.3–8 times |G|τ (4 × 8
  strip: 2,120 against 298; 5 × 6 box: 40 against 41); in the other **7 of the 17** (strips 2 × 12, 2 × 13, 3 × 9,
  4 × 6, 4 × 7, 5 × 5, box 4 × 6) there are none, against |G|τ = 22–197 predicted, so "0.3–8 × |G|τ" is conditioned
  on existence. Removing only periods 1–2 does not rescue the heuristic: states on immortal cycles of period ≥ 3 are
  1–56 × |G|τ (median ≈ 20). The longest immortal periods — 70 (2 × 14), 60 (3 × 8), 44 (box 4 × 7), 26 (4 × 8) —
  are the toy's clockwork, not chaos, and with τ = 3–10 generations these vessels have no long-lived chaotic
  component to compare with a random map. What the computation shows: in vessels of ≤ 32 cells the soup's fate is
  dominated by short-period debris; whether chaos behaves like a random map with killing is not tested. A candidate
  reading of E2 — *a random map with killing for the chaotic component, plus a debris component whose count is
  exponential in N, which a soup in a small vessel reaches with probability of order one* — is therefore
  untested in its first half. What fraction of debris a soup reaches in a large vessel is the open half of
  OPEN-PROBLEMS item 4.

## 7. What is proved (`exponent/theorems.md`)

- **A (safe cells).** A live toy edge cell with exactly two live in-row neighbours survives whatever lies beneath; a
  dead one with none stays dead; every other (state, k) can go either way. A gump face cell is never safe on its
  own. *Corrected 2026-11-14:* the old sentence "a gump face can always die in one generation" was false (§12).
  The review re-checked the per-cell statement for interior, rim and corner face cells (R = 3, 5, 9, 13) and the
  187 of 512 (R§0, R§4); the two-generation statement and the R = 5 count 180,615 are **[not independently
  checked]**.
- **B (three generations).** With the two rows beneath chosen freely, every edge configuration on a ring of L ≥ 5
  can be emptied in three generations, and the lone triple `111` (L ≥ 9) cannot be emptied in two. Brute force
  (`python3 game_check.py 13`, re-run): for L = 9…13 the L rotations of the lone triple are the only configurations
  that need three (L = 13: 989 in one, 7,189 in two, 13 in three). The swarm's critic read the proof and found it
  correct (board, lemma exchange); the review confirms it line by line and by an independent brute force for
  L = 5…14 (R§0, R§4). **B′:** an edge driven by any field giving each b conditional probability ≥ δ
  dies within three generations with probability ≥ δ^{3L}, so E T ≤ 3δ^{−3L}: for the w = 1 model ln τ ≤ 4.5·L + 1.1
  (true: 0.53·L).
- **C (noisy toy).** With independent deaths at rate ε, E T ≤ ε^{−L} from every state.
- **D, D′ (quasi-stationarity).** From a quasi-stationary state the death time is exactly geometric with
  h = Σ μ(x)·P_x(die next step); the w = 1 model is irreducible and aperiodic on the living rows, so this holds
  asymptotically from every start. No such statement exists for the deterministic automata (§6.2 shows why:
  conditioning on survival selects immortal debris), and D′ does not extend to gump's driven-face models: they have
  noise-immune fixed points, a second absorbing class (§5, R§1.3, R§4).
- **E (which mixing).** If under the quasi-stationary law the probability that the next block of m edge cells is
  empty, given that all previous blocks are, is at most θ < 1, then τ ≥ θ^{−⌊L/m⌋}; ψ-mixing implies this; a finite
  energy bound gives the matching upper bound (proofs checked, R§4). *Remark withdrawn in part:* the example offered
  to show that exponentially decaying correlations do not suffice (a mixture with an e^{−√L} atom on the empty row)
  does not have exponentially decaying correlations with constants uniform in L — its covariances stay ≈ e^{−√L}/4
  at every distance (R§4) — so it is not a counterexample to PROGRAM M2 / OPEN-PROBLEMS item 3 as worded. What it
  shows is that an additive correlation floor of order e^{−√L} suffices to break the implication; whether "ratio
  (ψ-) mixing" is really needed in place of correlation decay is open. The hypothesis of (a) is not measured: the
  window ratios of §4 (≤ 0.688 per cell for 5 ≤ ℓ ≤ 41) belong to the 16 × 128 strip, not to the ring's own
  quasi-stationary law at every ℓ < L. The critic's board (lemma exchange; graveyard 3, "checked") repeats the same
  example and has the same gap.
- **Not proved:** any lower bound τ ≥ e^{cL}. For the w = 1 model this is the survival of a non-attractive
  one-dimensional probabilistic automaton. The author's reason why the block/percolation route fails had two parts;
  the critic accepts only the second (an unknown outside contaminates two cells per side per generation) and notes
  that the comparison theorem needs no monotonicity (board, graveyard 6; note added to theorems.md).

## 8. Closed forms that do not survive

**[not independently checked]** (R§8).

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
(strips 16 × L; no settling needs detecting once ε > 0) **[measured]** **[not independently checked]**; table
re-derived, L = 16, ε = 10⁻³ re-run (identical):

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

## 10. Is 0.416 = 2 × 0.208 a coincidence? Not established

No reason for the factor 2 was found, and the data neither confirm nor exclude it (R§3). Items 1–2 show that the
ratio of the asymptotic slopes is somewhere in 1.6–2.0: a range with 2.0 at its edge does not show the identity is a
coincidence, only that it is not established. Items 3–5 are reasons to expect no identity, not evidence against it.

1. **The toy's number is not 0.416.** It is an effective slope for L = 12–36 containing a fading second channel; the
   sparse channel alone is 0.41, the window cost is ≈ 0.38–0.39 at ℓ = 30–42 (the filed 0.376–0.382 at ℓ = 34–50 is
   not reproduced; R§2, §4), a log-corrected fit gives 0.364 ± 0.006 (§4), which alone supports the lower end of
   0.36–0.41. The planned lifetimes at L = 32–40 on the six- and eight-row models (`python3 jobs.py model3`)
   were never run.
2. **Gump's number is not 0.208 either.** Rim-free faces: 0.209 (A = 27–108, this study and other work); octahedral
   faces: local slopes 0.201, 0.212, 0.212, 0.218–0.221, 0.221 from A = 30 to 135 (section 12). With 0.36–0.41 over
   0.209–0.221 the ratio is somewhere in 1.6–2.0.
3. **Geometry moves the toy's number and not gump's** (on the sizes compared here). Toy box edges cost 0.343 per cell
   (toy2d §5) against 0.41–0.44 for periodic edges at the same lengths; gump's periodic and octahedral faces cost the
   same per cell up to A ≈ 63 (§5; this no longer holds beyond A = 84).
4. **The mechanisms differ** (§5): a two-generation starvation flash with a convex rate function, against an
   erosion over five to twelve generations with a straight tail (gump measured at one periodic size and on the
   octahedral model; not a size law).
5. **A third member of the family lands elsewhere** (F7c, hit; **[not independently checked]**, R§8). Gump's rule B45/S345 on the 2D range-3 cross
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
| F1 headline | random map with killing fails by orders of magnitude, because of debris | 20–1,000× more immortal-cycle states than \|G\|τ; 5–94% of states never lose an edge | **hit** for the failure; "because of debris" as against chaos not shown (R§5; revision of 2026-11-14) |
| F1(a) | immortal basin 3–60% in every vessel with N ≥ 24 | 5–29% for H ≥ 4 and boxes, 49–94% in 2- and 3-row strips | miss |
| F1(b) | 4 × 8 strip: 10⁴–10⁶ immortal states, ≥ 90% period ≤ 2 | 42,493; 72% | half |
| F1(c) | period ≥ 8 immortal states within 30× of \|G\|τ_tail (50%) | 0.3–8× in the 10 of 17 vessels where they exist; none in the other 7 (\|G\|τ = 22–197; R§5) | hit as filed; contradicted in 7 of 17 vessels (R§5; revision of 2026-11-14) |
| F1(d) | no clean exponential; −ln hazard slope in L < 0.2 | flat hazard; slope 0.43, 0.64, 0.29 per cell | miss |
| F2 | toy's plunge lengthens with L (×1.5 from 16 to 32; 60%) | two-generation flash at every size | miss |
| F3 | window decrement at ℓ = 20–40 = lifetime slope within 10% (60%) | 0.376–0.397 against 0.38–0.42 (independently 0.385–0.400, R§2); τ = 12.1/E(L − 6.5) found after the runs, not forecast | **hit** (the band) |
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
| F10 | gump model R = 13, w = 4 within 0.2 of 18.077 (65%) | 18.179 ± 0.113 (78 deaths): +0.10; independently 18.183 ± 0.037 (719 deaths) against the deterministic hull 18.148 ± 0.028 and fluct's 18.077 (R§1.4) | **hit** *(2026-11-14)*; the filed point alone (± 0.11) is not a test |
| F11(a) | octahedral slope level or rising beyond A = 84: Δ(84→108) = 5.18 ± 0.10, Δ(108→135) = 5.89 ± 0.16 | GPU, reviewed: 5.235 (GPU's own A = 84) or 5.30 ± 0.06 (verified A = 84); 5.96 ± 0.25. Slopes 0.218–0.221, 0.221 | **hit** *(2026-11-14)*; not blind (author disclosed having seen the GPU numbers) |
| F11(b) | asymptote 0.214–0.225 (70%); not 0.2077 (85%) | octahedral local slope 0.221 at A = 135 and still rising; limit unknown. The forecast's stated basis (rising periodic slopes) failed (F11c) | not decided *(2026-11-14)*; "not 0.2077" consistent with all data since |
| F11(c) | periodic model A = 75: ln τ = 15.74 ± 0.05, slope 60 → 75 ≥ 0.2115 | 15.640 ± 0.025; slope 0.208 | **miss** *(2026-11-14)* |
| L = 32–40 (amendment of 19:56Z) | sparse-channel slope 0.385–0.410 between L = 32 and 40 (55%) | runs never made | unscored *(2026-11-14)* |

Tally: 8 hits, 7 misses, 4 split, 3 open or unscored. (As filed; the revision of 2026-11-14 does not rescore, but F1(c) is contradicted in 7 of 17
vessels and the F1 headline's "because of debris, not chaos" is not shown, R§5; a dated note is appended to
`PREDICTIONS.md`.) The misses that taught the most were F5 (the depth fixed
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
  model w = 5; the deterministic slab of R§1.2, 15.660 ± 0.027, is 0.09 above the line); its "rising" periodic slopes of 0.2106–0.2134 are a ±0.07-nat wiggle about a slope of 0.209, not a
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
    "checked" there; the review finds the example invalid, R§4, and graveyard 3 has the same gap, §7); the random map with killing fails (§6.2); the block construction fails, but for one of the study's two
    reasons only (§7; note added to theorems.md); shallow dice models are not a formula for the constant (§3, §8);
    0.416 = 2 × 0.208 (§10; "coincidence" is not established); 0.2077 as gump's asymptote; the plunge lengthening with L (F2, false).
  - Claims of the swarm that bear on the study but are its own and not checked here: a lower bound e^{cL} for an edge
    over dice near the law "b = 0 or 2 by a fair coin" (probability's Theorem A, modulo two cited percolation facts);
    "one exponent in every geometry, the ring's excess being a power of L" (board E15, a guess with exact support in
    dice models), which would make §6.1's ring slope 0.52 an effective value above an interval exponent of 0.46.

## 13. Not checked / known weaknesses

- **Re-runs are replays.** The pipeline is deterministic (§1), so the re-runs confirm the code and the arithmetic, not
  the statistical error bars. The independent samples are the validations against toy2d and fluct, the swarm's
  V1–V3 and E3, and, since the revision, the review's own runs (R§0–R§2) and the lead's check of the eight-row toy
  model (`research/audit/exponent/lead_check.py`).
- **Not re-run, taken from the filed records:** every simulated number not in the re-run table of §1 — in particular
  the toy model at w ≠ 8 and L ≠ 16, the truth strips at L = 20–28, the gump model at R ≠ 9 or w ≠ 4, the A = 84 and
  A = 75 points, the slab models, `rhoscan`, `slave`, `clone_corr.py`, `sync_check.py`, `regrow.py`, `mfld.py`, the
  pre-death profiles and the histogram distances of §3, the end-game numbers of the gump model in §5, and the
  "sparse only" columns of §2. Exact N = 32 functional graphs were not re-run (one N = 28 vessel was).
- **Few deaths at the largest sizes:** the study's A = 84 model point has 78 deaths (± 0.11; the review's has 719),
  A = 75 has 1,585 (the review's slab and models 936–1,341), toy2d's L = 36 has 495.
- **Error bars on slopes** from straight-line fits are not meaningful (χ²/dof ≈ 12–21 in §3; the same holds for the
  "excess slope" figures of §3 and the slopes 0.2159 / 0.2128 / 0.2060 of §5, R§6); the local slopes are the honest
  numbers.
- **The window costs beyond ℓ ≈ 30** have errors ± 0.006 (ℓ = 34 → 42) and ± 0.03 (42 → 50) once spatial overlap
  and time correlation are counted, and the filed values at ℓ = 30–42 are not reproduced by an independent run
  (§4, R§2); the eight-row model, which matches the lifetimes, does not reproduce the deterministic strip's window
  cost there either. The identity τ = 12.1/E(L − 6.5) is a two-parameter fit found after the runs, χ² 17/5 on seven
  points, and under-predicts the two largest lifetimes out of sample.
- **Small numerical discrepancies between the files:** hierarchy slopes for w = 8 and the truth (0.4281, 0.4254 in
  the author's draft; 0.4273, 0.4252 from `report.py hier`); the window cost "0.397 at ℓ = 20" in PREDICTIONS
  (F3 outcome) is the step 21 → 22 in the table's convention (the step 20 → 21 is 0.399); residuals of
  12.1/E(L − 6.5) differ by ≤ 0.01 from the filed ones depending on how E is interpolated. None changes a conclusion.
- **The noise density is 12-bit** (0.47192, 0.41553): a 10⁻⁴ effect on ln τ (§6.1), irrelevant to every conclusion.
- **T0 and the quasi-stationary state.** The rate measured after T0 is the quasi-stationary rate only if T0 exceeds
  the relaxation time (board, from Méléard–Villemonais). For the dice models the second eigenvalue is ≈ 0.5 (board),
  so T0 = 200–300 is ample; for the deterministic vessels no relaxation time is known.
- **Censoring.** Settled states, cuts and firewalls are reseeded, not counted; the lifetimes are conditional on chaos
  and on not being cut. `drv.c` compares snapshots within one chunk only; undetected long cycles would be counted as
  living. The review (Brent's method, every period) found no settled state in deterministic hulls and slabs at
  A ≥ 45 (R§1.5), so this does not matter there. In the noise models repeating dynamic states (noise-immune debris,
  §5) were not censored by this study; the bias is limited by chunk restarts and is small wherever the review
  re-measured, but not bounded elsewhere (R§1.3, R§8).
- **Gump's mechanism claims** (erosion over 5–12 generations) rest on one periodic size (A = 60) and the model at
  A = 63; the octahedral ones on the driven model, not on the deterministic hull. The per-live-cell constant is a
  re-expression of the area law (§5, R§3).
- **The study never tested its static formulation (§4) on gump**, nor whether gump's per-live-cell ratio 0.40
  survives at the sizes where octahedral and periodic faces part (A ≥ 84).
- **Outside the review** (R§8), and marked [not independently checked] where they appear: the toy half of verdict 1
  beyond the lead's check (L = 28, other densities, the strips themselves, the histogram distances), §2's flash and
  channel tables, §6.1, §8, §9, §10.5, regrowth, clone correlations, rhoscan, slave runs, fg.c on vessels with
  N = 25–32, the gump face game in two generations and the R = 5 count, the window statistics of the eight-row model,
  and the toy lifetimes (taken from the records and toy2d).
- **The figures** (`research/figures/exponent_{flash,hierarchy,gump}.png`) were made by the author from these records
  and were not regenerated; `figures.py rate` and `figures.py fg` would write two more that were never committed.

## 14. Changes in the revision of 2026-11-14

Required by `research/audit/REVIEW-exponent.md` §7 (items numbered as there):

1. *Hull depth post hoc; deep models low.* Verdict 1 and §5 say that w = 4–5 was noticed after the committed w* = 3
   missed (F5), and give the review's w = 4, 5, 6, 8 runs and deterministic hull values (new rows of the §5 table),
   with the 0.03–0.04-nat offset below the deterministic hull at A = 45, 63 and the crossing reading of w = 4.
2. *Periodic faces.* Verdict 1 and §5: "from w = 5 on within 0.015" with the review's numbers; the deterministic
   A = 75 slab (15.660 ± 0.027) added to §5's table with the review's model differences; w = 4 at +0.06–0.07 at
   A = 48–60. See inconsistency (a) below.
3. *"Nothing can settle".* Deleted from §3; the counterexample (cube at (6,0,0) in `gump_model(7, 4)`; any face cube
   immune once w ≥ 5; `research/audit/exponent/trap.py`), the censoring rule and the list of filed model numbers that
   could be affected added to §5; Verdict 1, §7 and theorems.md (after D′) say D′ does not extend to gump's models.
4. *A = 84.* §5 table and text, Verdict 1, §11 (F10): the review's 18.183 ± 0.037 against 18.148 ± 0.028; the
   78-death point kept but marked ± 0.11, "not a test".
5. *Window formula.* Verdict 2 and §4: χ² 17.3/5 (p ≈ 0.004); found after the runs; the out-of-sample test
   (+0.083, +0.068); "the exponent is the decay rate of E" replaced by the curvature statement; the review's
   "how much is fit" analysis added.
6. *Window-cost errors.* §4: the filed "± 0.01–0.02 at best" replaced by the review's spatial and batch-jackknife
   errors, with a table of the independent window costs.
7. *Theorem E(a)'s hypothesis.* §4 second bullet, Verdict 4, §7 and theorems.md Remark 2: not a measured fact.
8. *Remark 1 of E.* theorems.md: the example withdrawn (struck through), the review's covariance computation and
   the weakened statement ("an additive correlation floor of order e^{−√L} suffices to break the implication")
   given, the question marked open; Verdict 4 and §7 changed to match; §7 and §12 flag that board graveyard 3 has
   the same gap. **Not applied:** flagging it in the board itself (`research/theory/swarm/critic/board.md`), which is
   outside the paths this revision may edit.
9. *Verdict 3.* "A coincidence" → "not established (ratio 1.6–2.0)"; the free fit with intercept 0.085 ± 0.025 and
   the better area law in Verdict 3 and §5; §10's title and preamble changed to match.
10. *Verdict 5 / §6.2.* "Not because chaos is unlike a random map" → "the test of the chaotic component is
    inconclusive", with the 7-of-17 count, the 1–56× for period ≥ 3 and the clockwork reading; 67–97% → 67–99%;
    "geometric" qualified as about one e-fold of flat hazard (R§5).
11. *A = 30 hull truth.* §5: 6.784 (two deaths counted twice) against 6.809; the comparison is unaffected.
12. *theorems.md.* B′ 4.51 → 4.50 (with δ and −3 ln δ shown); E(a) "h = ν(∩A_j)" → "h ≤ ν(∩A_j)".
13. *Toy asymptotic slope.* §4 third bullet, §10.1 and Verdict 3: window cost ≈ 0.38–0.39 at ℓ = 30–42; the lower
    end of 0.36–0.41 now rests on the log-corrected fit (0.364) alone.

Other changes, from the review's sections or the lead's check, not numbered in its §7:
- The lead's independent check of the eight-row toy model (`research/audit/exponent/lead_check.py`) added to
  Verdict 1 and §3: "within 0.05" holds at L = 12–20 and is at its edge at L = 24.
- Parts listed under the review's "Not checked" (R§8) are marked [not independently checked] in §2, §3, §6.1, §6.2,
  §7, §8, §9, §10.5, the regrowth bullet and Verdict 1, 3, 4; a summary bullet is added to §13.
- §5: the dying-face generation counts are flagged as one size each, not a size law (R§4, board E14); fitted-slope
  errors flagged (R§6); the 60 → 75 slope with the deterministic A = 75 slab, (15.660 − 12.496)/15 = 0.211 ± 0.002,
  is this revision's arithmetic on the review's number, not a new measurement.
- §1: `drv.c` compares snapshots within one chunk only (R§0). §13: censoring, window costs, few-deaths, slope-error
  and mechanism bullets updated.
- §11: annotations on F1, F1(c), F3, F10 (no rescoring); a dated note appended to `exponent/PREDICTIONS.md` for F1,
  F1(c), F3, F10, F11(c); filed entries there unchanged.
- theorems.md: Lemma A consequence (a)'s example needs L ≥ 6; E(b) needs Ψ ≥ 0 and uses ⌊J/2⌋ odd blocks (R§4); two
  cross-references corrected (debris count is exponent.md §6.2, not §5; noise is §9, not §8).

Inconsistencies not resolved here:
- (a) Item 2 asks for "within 0.015 at A = 27–75", and R§1.2 says "≤ 0.014 at every size, including A = 75", but the
  review's own A = 75 entry at w = 5 is +0.018 ± 0.042, the review did not run A = 36, and the study's filed w ≥ 5
  differences reach 0.03 (A = 27, w = 6). The text states the numbers: within 0.015 at A = 27, 48, 60 in the review's
  runs, +0.02 ± 0.04 at A = 75; the filed table is unchanged.
- (b) R§1.3 criticises "nothing can settle" for gump's models, but in §3 the phrase was said of the toy models; the
  review shows debris only in gump's. The revision deletes the phrase and says that debris in the toy models with
  w ≥ 2 was not examined; it does not claim they have any.
