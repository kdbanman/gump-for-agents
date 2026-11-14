# Review of `research/theory/exponent.md` (adversarial, 2026-11-14)

Object: `research/theory/exponent.md` and `research/theory/exponent/` (theorems.md, PREDICTIONS.md, data, drivers)
as committed in 1d82192. All reviewer code is in `research/audit/exponent/` and shares no code with `drv.c`, `xp.py`,
`fg.c`, `game_check.py` or the critic's lab (`lead_check.py` there is the lead's and was not used). Bulk output is in
`research/scratch/audit_exponent/`; `results.jsonl` there holds every run below with seed, exposure, deaths,
censoring counts and hazard by age bin. Commands run from `research/audit/exponent/`. The toy half of verdict 1 was
left to the lead, as instructed.

## Summary

| verdict of the report | finding |
|---|---|
| 1, gump half (rule on 4–5 layers over coin flips ≈ deterministic faces) | **stands with corrections** |
| 2 (τ_edge = 12.1 / E(L − 6.5); "the exponent is the decay rate of E") | **stands with corrections** for the fit, **does not stand** for "the exponent is the decay rate of E" |
| 3 (0.416 ≈ 2 × 0.208 a coincidence; 0.403 per live cell) | **does not stand** as worded (neither half is shown) |
| 4 ([proved] bounds and theorems.md) | **stands with corrections** (proofs correct; one remark mis-proved, one hypothesis mis-described as measured) |
| 5 (exact small vessels: random map fails because of debris, not chaos) | enumeration **stands** (bit-identical); the inference **does not stand** |

## 0. Tools and their validation

| check | command | result |
|---|---|---|
| cell graph from the doubled coordinates of AUTOMATON §2 against `reference/oracle.py` | `python3 graphs.py validate` | torus H = 10, 60 generations equal; hull R = 9 inside a padded oracle box, 60 generations equal; a 12-layer slab 4 × 3 lifted periodically into a 64³ oracle box, 4,728 interior cells equal after 6 generations |
| bit-sliced C stepper `qs.c` against the numpy stepper of `graphs.py` | `python3 run.py validate` | hull R = 9, slab 4 × 4 × 12, hull model R = 11 w = 5, slab model 4 × 5 w = 5: 200 generations, 4 replicas, identical |
| toy strip stepper `toygap.c` against a naive stepper written from theorems.md's definition | `python3 toycheck.py` | 16 × 128 and 7 × 128 strips, 40–300 generations, identical |
| the hull models are the report's graphs | one-off comparison with `xp.gump_model` (read only) | R = 7 w = 4, 5 and R = 9 w = 4: same cells, same neighbour sets, same layers |
| fg.c's functional graphs | `python3 fgbrute.py strip 3 6 box 4 4 strip 2 8 box 4 5 strip 4 5 strip 4 6 strip 3 8 box 4 6` | all eight filed outputs (N = 16–24) **identical** in every field compared (immortal basin, death-time histogram, immortal cycles by period, all cycles by period, cyclic states) |
| Theorem B brute force | `python3 gamecheck.py 14` | L = 5…14: every ring emptied in ≤ 3; the configurations needing 3 are exactly the L rotations of `111` (L ≥ 9); L = 13: 989 / 7,189 / 13 as filed |
| corrected Lemma A(c) | `python3 facegame.py 3` | 187 of 512 R = 3 face configurations cannot be emptied in one generation (as filed); no face cell of the R = 3, 5, 9, 13 hulls is safe |

Definitions used by `qs.c` (taken from the report §1 and the board's "Definitions"): soups of density 0.35 on the
dynamic cells; a transition is *exposed* if the replica's age before it is ≥ T0 (200 hulls and hull models, 300
slabs); a death is a face layer empty after the step; censored and reseeded, not counted: a state equal to the state
two generations back or to the snapshot taken at the last power-of-two age (Brent's method: every period is caught
eventually; drv.c only compares with global snapshots at multiples of 64 / 4096 / 262,144, and only within one
chunk), three consecutive dead layers inside the vessel, and in slabs the three-layer firewalls of the three oblique
diagonals that wrap the torus. For models, `QS_SETTLE=1` also censors repeating dynamic states (see 1.3).
ln τ = −ln(deaths / (faces × exposure)), error 1/√deaths. Replicas are independent and each death is followed by a
fresh soup, so 1/√deaths is the right error for these hazards.

## 1. Verdict 1, gump half — stands with corrections

### 1.1 Hull faces (octahedral), own runs

Deterministic hull, all 8 faces, settled states censored (`python3 run.py hull R SECONDS [T0] [SEED]`):

| A (R) | mine | report / fluct |
|---|---|---|
| 30 (7) | 6.784 ± 0.002 (every face death counted); 6.809 if a generation in which two faces die counts once | 6.804 ± 0.003 |
| 45 (9) | 9.821 ± 0.004, 9.826 ± 0.006 (two seeds) | 9.819 ± 0.003 |
| 63 (11) | 13.650 ± 0.009 (T0 = 200), 13.638 ± 0.009 (T0 = 2000) | 13.633 ± 0.008 |

The hazard is flat in age (bins T0 … 2¹⁴ T0; `results.jsonl`, `age_bins_T0_units`) and T0 = 2000 changes nothing.
At A = 30, 2.5% of first peels take two faces at once; the definition of "a face death" moves ln τ there by 0.025.

Driven-face model `hull_model(R, w)` (top w layers of the hull face follow the rule, the next two layers are
Bernoulli(0.4155) every generation; `python3 run.py model R w SECONDS`), ln τ_face, and model − my truth:

| w | A = 45 | Δ | A = 63 | Δ | report A = 45 / 63 |
|---|---|---|---|---|---|
| 3 | | | 14.591 ± 0.035 | +0.94 | 10.542 / 14.653 |
| 4 | 9.798 ± 0.008 | −0.025 | 13.633 ± 0.023 | −0.011 | 9.808 / 13.653 |
| 5 | 9.793 ± 0.006 | −0.030 | 13.601 ± 0.024 | −0.043 | 9.782 / 13.592 |
| 6 | 9.795 ± 0.006 | −0.028 | 13.609 ± 0.026 | −0.035 | not run |
| 8 | 9.779 ± 0.007 | −0.044 | 13.610 ± 0.028 | −0.034 | not run |

(Truth for Δ: pooled 9.823 ± 0.004 and 13.644 ± 0.006.) Every model value agrees with the report's within 1.3σ.
**The deeper models (w = 6, 8, new here) do not move towards the truth; they settle 0.03–0.04 nats below it at both
sizes** (at A = 45: −0.028 ± 0.007 and −0.044 ± 0.008, i.e. 4–5σ; at A = 63 the same size with ± 0.026). So the hull model is not "the deterministic
system": it converges in depth to a value about 0.035 nats below it. "≤ 0.05 nats" is true of every entry with
w ≥ 4, but it is a statement about a small systematic offset, not statistical agreement; and w = 4's closeness
(−0.01 to −0.025) is partly a crossing (w = 3 is +0.7 to +0.9 too tough, w ≥ 5 is low), not convergence.

### 1.2 Periodic faces, own runs

Deterministic 12-layer slab (`python3 run.py slab a b SECONDS`) and the periodic model (`QS_SETTLE=1 python3 run.py
slabmodel a b w SECONDS`):

| A | slab, mine | report | w = 3 | w = 4 | w = 5 | w = 6 |
|---|---|---|---|---|---|---|
| 27 | 5.501 ± 0.003 | 5.501 ± 0.012 | +0.102 | +0.018 | +0.002 | +0.001 |
| 48 | 9.929 ± 0.006 | 9.937 ± 0.016 | | +0.057 ± 0.008 | +0.014 ± 0.008 | |
| 60 | 12.491 ± 0.010 | 12.496 ± 0.019 | +0.242 | +0.068 ± 0.017 | −0.001 ± 0.017 | +0.005 ± 0.018 |
| 75 | **15.660 ± 0.027** (new; 1,341 deaths) | – | | | **+0.018 ± 0.042** (15.678 ± 0.032) | +0.002 ± 0.043 (15.662 ± 0.033) |

(Model errors at A = 27: ± 0.0015.) For periodic faces the claim is **confirmed, and more strongly than stated**:
from w = 5 on the model equals the slab to ≤ 0.014 at every size, including A = 75, where the report had the model
only (its 15.640 ± 0.025 and my 15.678 ± 0.032 both sit within 1σ of my deterministic 15.660 ± 0.027). Convergence
in depth is monotone. w = 4 is +0.06–0.07 at A = 48–60 in my runs (6σ at A = 48), so "w ≥ 5" (not 4) is the right
statement for periodic faces, as the report has it.

### 1.3 Definitions: the models can settle

The report (§3, and theorems D/D′ as applied there) says the noise models are finite-range probabilistic automata in
which "nothing can settle". False for gump's models. **Counterexample** (found with `QS_DUMP=1 ../../scratch/audit_exponent/qs
../../scratch/audit_exponent/g_model_R7_w4.bin 200 999 20 1000000000`, which prints the oldest replica; checked by
`python3 trap.py`): in `hull_model(7, 4)` the six faces of the cube centred at (6,0,0) — (7,0,0), (6,1,0), (6,0,1) in the face
layer, (5,0,0), (6,−1,0), (6,0,−1) one layer in — with every other dynamic cell dead is a fixed point *whatever the
noise does* (every dynamic cell's next state is forced). The face never dies. In my R = 7, w = 4 run without
settling censored, a third of the exposure ended in trapped replicas (ages up to 3×10⁶ with no deaths) and ln τ came
out 6.944; censoring repeating states (`QS_SETTLE=1 python3 run.py model 7 4 20 200 514`) gives 6.541 ± 0.001 with
187 trapped replicas per 533,295 deaths (the report's chunked runs restart every replica every chunk and got
6.550). `python3 trap.py`: the vertex cube is immune in every hull model with w ≥ 4 (R = 7, 11, 13), and a cube in the
face interior is immune in every hull or periodic model with w ≥ 5 (not at w ≤ 4). Repeating dynamic states were censored in 163–741 cases per 0.45–0.76 million deaths in the A = 27 slab
models and 3 times at A = 48 (w = 4) and never at A ≥ 60. So the effect on the report's numbers is small at the sizes measured, but: the
models have absorbing debris other than death, the death law is not "exactly geometric" from an arbitrary start, and
results from long runs without settle-censoring can be badly biased (6.94 vs 6.54 here).

### 1.4 The largest sizes

- **Periodic: A = 75** is now the largest size with both: model − truth = +0.02 ± 0.04 (w = 5, mine), −0.02 ± 0.04
  (w = 5, the report's model against my truth).
- **Hull: A = 84.** Report: model 18.179 ± 0.113 (78 deaths) against 18.077 ± 0.054 (fluct) or 18.154 ± 0.025
  (independent CPU, REVIEW-gpu-pr8). Mine: model w = 4 (repeating states
  censored; none occurred) **18.183 ± 0.037** (719 deaths, five 20-minute pieces with seeds 401–405:
  `QS_SETTLE=1 python3 run.py model 13 4 1200 200 40s`), deterministic hull **18.148 ± 0.028** (1,250 deaths,
  `python3 run.py hull 13 2400 200 601`). Model − truth = **+0.035 ± 0.047** (+0.029 ± 0.045 against the CPU value).
  So at the largest hull size the w = 4 model still agrees within 0.05, now with a 7× larger sample than the report's
  F10 point; the sign of the w = 4 offset is −0.025, −0.011, +0.035 at A = 45, 63, 84, all within about 2σ of
  −0.01. My hull value also sides with the CPU review (18.154) against fluct's 18.077 ± 0.054 (1.2σ).

### 1.5 Censoring and burn-in

Checked: which layers are dynamic and which are noise (identical graphs); death = the face layer empty; cuts
(three dead layers among the dynamic ones) censored in models; in slabs interior and oblique firewalls censored
(my counts: 8,756 cuts against 141,018 deaths at A = 27, 7 against 9,602 at A = 60, none at A = 75); settled states
of every period (Brent) in deterministic vessels — none occurred in hulls and slabs at A ≥ 45 in my runs, so drv.c's
coarser snapshot scheme does not matter there. T0 = 200 is adequate (hull R = 11: T0 = 2000 gives the same).
Not the report's error: the hull truth at A = 30 depends at 0.025 nats on whether simultaneous face deaths count
once or twice.

## 2. Verdict 2 — the fit stands with corrections; "the exponent is the decay rate of E" does not stand

`python3 verdict2.py fit` (filed E(ℓ) from `data/gap.json`, log-linear interpolation; lifetimes: this study's
16 × L strips L = 12–28 and toy2d's L = 32, 36):

- Reproduced: shift 6.5, prefactor 12.05, residuals +0.030, −0.022, −0.005, −0.013, +0.026, +0.071, +0.054,
  **χ² = 17.3 on 5 degrees of freedom (p ≈ 0.004)**. "Fits all seven to ≤ 0.07 nats" is true in nats but the fit is
  rejected at the quoted errors (residuals of 2.2σ at L = 12 and 1.9σ at L = 32).
- **How much is fit.** The shift is not degenerate with the prefactor: χ²(s) = 52.6, 20.7, 17.3, 23.8, 63.4 at s = 5,
  6, 6.5, 7, 8 (best 6.40, 1σ range 6.05–6.80 after scaling by χ²/dof). So the two constants fix the level and the
  curvature; the content is that −ln E(ℓ) over ℓ = 5.5–29.5 has the same curvature as ln τ(L) over L = 12–36. A
  three-constant smooth curve does better (a + bL + c ln L: χ² 4.6/4; a + bL + c/L: 7.8/4); a straight line is far
  worse (94.9/5).
- **Out of sample.** No lifetime outside the seven exists for the deterministic strips (the study's L = 8 record has
  no exposure). Fitting the five L = 12–28 points only (shift 6.25, χ² 11.0/3) and predicting toy2d's L = 32, 36
  gives residuals **+0.083 ± 0.038 and +0.068 ± 0.045**; with the shift held at 6.5, +0.074 and +0.056. The formula
  under-predicts both larger lifetimes; the two last residuals of the seven-point fit are the same effect.
- **Window costs beyond ℓ ≈ 30 are not probed.** The largest window used is ℓ = 29.5. The eight-row model's E, whose
  cost beyond ℓ = 34 is 0.396–0.417 instead of 0.376–0.382, fits the same seven lifetimes as well (χ² 13.5, best
  shift 6.05); the one-row model's E fails completely (χ² ≈ 15,000). So the lifetimes discriminate the shape of E
  for ℓ ≤ 30 and say nothing about its decay rate as ℓ → ∞. **"The exponent is the decay rate of E" is compatible with
  the data, not supported by it**; and the out-of-sample residuals lean the other way (lifetimes rising faster than
  1/E at the largest L).
- **The right error on the window cost.** Window samples overlap in space (one empty run of length r gives r − ℓ + 1
  windows) and persist in time (batches of consecutive generations below). (a) Spatial part only, exact from the filed counts (compound Poisson over maximal
  empty runs, `python3 verdict2.py errors`): 0.3763 ± 0.0033 over ℓ = 34 → 42 (33,822 runs of length ≥ 34),
  0.3824 ± 0.0085 over 42 → 50 (1,701 runs), 0.3817 ± 0.0010 at 30 → 31. (b) Including the time correlation, from
  my own 16 × 128 run in 1,033 batches of 2×10⁶ generations (`../../scratch/audit_exponent/toygap run 777 600 2000000`, then
  `python3 verdict2.py errors ../../scratch/audit_exponent/toygap_777.txt`, jackknife over batches): 

  | window cost | filed (2.7×10¹¹ samples) | spatial error only (filed counts) | mine (5.0×10¹¹ samples), jackknife over 1,033 batches |
  |---|---|---|---|
  | ℓ = 10 → 11 | 0.4342 | ± 0.0000 | 0.4342 ± 0.0000 |
  | 20 → 21 | 0.3992 | ± 0.0001 | 0.3995 ± 0.0002 |
  | 30 → 31 | 0.3817 | ± 0.0010 | 0.3852 ± 0.0015 |
  | mean 34 → 42 | 0.3763 | ± 0.0033 | **0.3874 ± 0.0064** |
  | mean 42 → 50 | 0.3824 | ± 0.0085 | 0.378 ± 0.027 |

  E(1) = 0.4235 in both. The honest error over ℓ = 34 → 42 is ± 0.006 (three times the filed ± 0.002 and about twice
  the spatial-only estimate), and over 42 → 50 it is ± 0.03: those entries carry no information at the level the
  report discusses. My independent value at 34 → 42 is 0.387 ± 0.006, against the filed 0.376 (1.7σ apart); at
  30 → 31, 0.3852 ± 0.0015 against 0.3817 (2.3σ). So the "0.376–0.382" that sets the bottom of the report's range
  0.36–0.41 for the toy's asymptotic slope is not reproduced; 0.38–0.39 is what two independent runs support at
  ℓ ≈ 30–42, and nothing beyond ℓ ≈ 42. With my E the formula gives the same residuals (+0.029 … +0.042, χ² 16.2).

## 3. Verdict 3 — does not stand as worded

- **"0.416 ≈ 2 × 0.208 is a coincidence."** The report's own evidence is that the toy's asymptotic slope is
  0.36–0.41 and gump's 0.209–0.221, a ratio "somewhere in 1.6–2.0" (§10). A range that has 2.0 at its edge does not
  show the identity is a coincidence; it shows the identity is *not established*. The other arguments (different
  death mechanisms, geometry moves one and not the other, a third rule lands elsewhere) are reasons to expect no
  identity, not evidence against it. Correct statement: no reason for the factor 2 was found and the data neither
  confirm nor exclude it.
- **"ln τ_face = 0.403 ⟨n⟩, with no intercept."** From the filed slab records (and mine, which agree to 0.01 in
  ⟨n⟩ and ln τ): ⟨n⟩ = 13.536, 18.323, 24.733, 31.002 at A = 27, 36, 48, 60. A free fit ln τ = a + b⟨n⟩ gives
  a = **0.085 ± 0.025** (3.4σ from zero), b = 0.399 ± 0.001, χ² 6.2 / 2; the area law a + bA fits better
  (a = −0.223 ± 0.026, b = 0.2118 ± 0.0006, χ² 1.2 / 2). The ratio ln τ/⟨n⟩ is constant to ± 0.002 because ⟨n⟩/A
  rises (0.501 → 0.517) just where the area law's negative intercept needs it. 0.403 is 0.21 per site divided by
  0.52 live cells per site: one unexplained number re-expressed, not a second finding, and "no intercept" is wrong.

## 4. Verdict 4 and theorems.md — stands with corrections

Checked line by line; brute force where possible (§0).

- **Lemma A (i)–(iii)** (toy): correct; table re-derived from the rule (`gamecheck.py`). Consequences (a), (b):
  correct (with (a)'s example needing L ≥ 6 so that the two cells beyond an end are distinct from the run).
- **Lemma A(c)** as corrected: the per-cell statement is correct for interior face cells (6 in-layer + 3 beneath),
  and also for the hull's rim cells (4 + 3) and corners (2 + 2) — checked for R = 3, 5, 9, 13. The struck sentence is
  false (187 of 512 at R = 3, reproduced independently). Consistent with board E10.
- **Theorem B** (a), (b): correct line by line; brute force L = 5…14 confirms, independent of game_check.py.
- **Corollary B′**: correct. The constant: −3 ln δ = 4.505 (δ = 0.472² = 0.2228), so "4.51·L" should read 4.50·L
  (immaterial).
- **Theorem C**: correct.
- **Theorem D**: correct (finite chain, Perron–Frobenius). **D′**: correct for the w = 1 toy model. It does **not**
  extend to gump's models (§1.3: noise-immune fixed points exist, a second absorbing class), and exponent.md §3's
  "nothing can settle" must not be read as covering D3.
- **Theorem E (a)–(c)**: correct (in (a), "h = ν(∩A_j)" should be "h ≤ ν(∩A_j)" when mJ < L; (b) needs Ψ ≥ 0 and
  uses ⌊J/2⌋ odd blocks, which handles the wrap-around).
- **Remark 1 of E (decaying correlations are not enough): the counterexample does not satisfy its own hypothesis.**
  For the mixture ν = (1 − a)ν₀ + aδ_∅ with a = e^{−√L}, the covariance of the indicators "cell x empty", "cell y
  empty" is a(1 − a)(1 − ν₀(x empty))(1 − ν₀(y empty)) + (1 − a)Cov₀ ≈ a/4 at *every* distance. Correlations
  therefore stop decaying at distance ≈ ξ√L: the family does not have exponentially decaying correlations with
  constants uniform in L, which is what PROGRAM M2 / OPEN-PROBLEMS item 3 mean. (For the single-cell covariances to stay below Ce^{−r/ξ} up to r = L/2, the
  weight must be a ≲ e^{−L/(2ξ)}, which makes the wait exponential again: no mixture of this kind can be a
  counterexample.) The
  conclusion ("ratio mixing, not covariance decay, is what multiplies") may well be right, but this example does
  not prove it. The critic's graveyard item 3 ("checked") repeats the same example and has the same gap.
- **The hypothesis of E(a) is not "a measured fact".** exponent.md §4 says E(ℓ+1)/E(ℓ) ≤ 0.688 for 5 ≤ ℓ ≤ 41
  makes τ ≥ 0.688^{−L} a theorem. The hypothesis concerns the quasi-stationary law of the *ring of L cells itself*
  for every prefix length up to L; what was measured is a different system (a 16 × 128 strip, deterministic, for
  which theorems.md itself says no quasi-stationary law exists) for ℓ ≤ 41 only. The measurement makes the
  hypothesis plausible for ℓ ≤ 41; it does not supply it.
- **What is not proved** section: accurate; consistent with the board (graveyard 6: only the second reason stands;
  the note added says so).
- Board items E1–E15 and the graveyard: §12 of the report reports them faithfully. One tension: E14 says a dying
  gump face's collapse lengthens with A; §5's table shows the periodic face at one size (A = 60) and the octahedral
  face from the model only, so "erodes over 5–12 generations" is not a size law and should not be read as one.

## 5. Verdict 5 — enumeration stands; the inference does not

- fg.c is bit-identical to an independent brute force on eight vessels (§0).
- "The death law is already geometric": the 4 × 8 hazard is flat (0.102–0.111) for t = 6–16 and then sinks to
  0.06–0.08; with τ ≈ 9 that is about one e-fold of flatness. Correct as an exact statement, weak as "geometric".
- **"Fails because of debris, not because chaos is unlike a random map" does not follow.** From
  `data/fg_summary.json` (17 vessels with N ≥ 24): (i) in **7 of the 17** there are *no* states on immortal cycles
  of period ≥ 8 at all, against |G|τ = 22–197 predicted (strips 2 × 12, 2 × 13, 3 × 9, 4 × 6, 4 × 7, 5 × 5, box 4 × 6);
  the report's "0.3–8 × |G|τ" is conditioned on existence. (ii) Removing only periods 1–2 does not rescue the
  heuristic: states on immortal cycles of period ≥ 3 are 1–56 × |G|τ (median ≈ 20). (iii) The long immortal cycles
  are what the report itself calls the toy's clockwork, not chaos; and τ = 3–10 generations in these vessels, so
  there is no long-lived chaotic component to compare with a random map. What the computation shows: in vessels of
  ≤ 32 cells the soup's fate is dominated by short-period debris; whether chaos behaves like a random map with
  killing is not tested. Minor: the period ≤ 2 share is 67–99%, not 67–97% (2 × 12, 2 × 13: 98%, 99%).

## 6. Statistics and forecast order

- 1/√deaths: right for these replica-restart estimators (deaths are of independent replicas). Not right for window
  counts (§2) or for slopes from fits with χ² 37–63 on 3 degrees of freedom (the report already says so; the
  "excess slope" column of §3 and the slopes 0.2159 / 0.2128 / 0.2060 of §5 inherit the problem).
- Few deaths: the report's A = 84 model (78 deaths; now 719 here), toy2d L = 36 (495), the A = 75 slab and models
  here (936–1,341).
- Order (`git log --format='%h %cI %s' -- research/theory/exponent`; file times in `research/scratch/exponent/`):
  F1–F7 at 17:57Z, w* = 3 at 18:19Z before any gump-model record, F8/F9 at 18:40Z with hull runs on screen (stated),
  F10 at 18:56Z before the R = 13 run, F11 at 19:34Z not blind (stated). No forecast was back-dated. But two headline
  results are **post hoc and presented in the Verdict without saying so**: the depth w = 4–5 for hull faces (chosen
  after F5's w* = 3 missed; §5 is explicit, the Verdict is not) and the formula τ = 12.1/E(L − 6.5) (found after
  the runs; F3 only forecast "decrement within 10% of the slope"). F10, the one genuine forecast for w = 4 at a new
  size, has ± 0.11 against an allowance of 0.2.

## 7. Required corrections to `exponent.md`

1. Verdict 1 and §5: say that w = 4–5 for hull faces was chosen after the committed w* = 3 failed, and add: deeper
   hull models (w = 6, 8; this review) settle 0.03–0.04 nats *below* the deterministic hull at A = 45 and 63
   (4–5σ at A = 45), so the hull model agrees to ≈ 0.04 nats with a small systematic offset, not exactly.
2. Verdict 1: for periodic faces, replace "w ≥ 5 … ≤ 0.05" by "from w = 5 on within 0.015 at A = 27–75" and add the
   A = 75 deterministic slab (15.660 ± 0.027, this review) to §5's table; w = 4 is +0.06–0.07 at A = 48–60.
3. §3 / §7 / theorems.md D′: delete "nothing can settle" for gump's models; add the counterexample of 1.3 (the cube
   at (6,0,0) is a noise-immune fixed point of `gump_model(7, 4)`; a cube anywhere on the face is immune once
   w ≥ 5) and state that model runs must censor repeating dynamic states, as the deterministic runs censor settled
   ones.
4. §5, A = 84: replace the 78-death point by the pooled value of this review (model 18.183 ± 0.037 against hull 18.148 ± 0.028) or mark it ± 0.11 and
   "not a test".
5. Verdict 2 and §4: give χ² = 17/5 next to "≤ 0.07 nats"; state that the formula was found after the runs; add the
   out-of-sample test (fit on L = 12–28 predicts L = 32, 36 low by 0.08 and 0.07); replace "The exponent is the
   decay rate of E" by "over ℓ ≤ 30 the curvature of −ln E matches that of ln τ; the lifetimes do not reach the
   window lengths (ℓ > 30) where the decay rate would be read".
6. §4: replace "0.376 ± 0.002 (too precise) … ± 0.01–0.02 at best" by the errors of §2 of this review (spatial part
   ± 0.003 at ℓ = 34 → 42, ± 0.009 at 42 → 50; with time correlation ± 0.006 at ℓ = 34 → 42 and ± 0.03 at 42 → 50 by batch jackknife, and an independent value 0.387 ± 0.006 at 34 → 42 against the filed 0.376).
7. §4, second bullet: "the hypothesis of Theorem E(a) holds as a measured fact … τ ≥ 0.688^{−L} is a theorem" →
   "the hypothesis would follow if the ring's own quasi-stationary law had the window ratios measured in the
   16 × 128 strip for ℓ ≤ 41, at every ℓ < L; that is not measured". Same change in verdict 4 ("θ measured").
8. theorems.md E, remark 1 (and verdict 4's "decaying correlations alone do not give an exponential wait"): the
   mixture's correlations do not decay at distances beyond ≈ √L, so it is not a counterexample to M2 as worded.
   Either give a different example or weaken to "an additive correlation floor of order e^{−√L} suffices to break
   the implication". Flag the same in board graveyard 3.
9. Verdict 3: replace "a coincidence" by "not explained and not established (ratio 1.6–2.0)"; replace "ln τ = 0.403⟨n⟩
   to three figures, with no intercept" by the free fit (intercept 0.085 ± 0.025; the area law fits better) and say
   that 0.40 per live cell is the area slope divided by the live density.
10. Verdict 5 / §6.2: replace "not because chaos is unlike a random map" by "the test of the chaotic component is
    inconclusive: 7 of 17 vessels with N ≥ 24 have no long immortal cycles (|G|τ = 22–197 expected), period ≥ 3
    cycles still exceed |G|τ by 1–56×, and the long cycles are clockwork"; "67–97%" → "67–99%".
11. §5, hull truth at A = 30: note that counting a generation in which two faces die as two deaths moves ln τ by
    −0.025 (6.784 against 6.809); the model comparison there is unaffected in conclusion.
12. theorems.md B′: 4.51 → 4.50; E(a): "h = ν(∩A_j)" → "h ≤ ν(∩A_j)".
13. §4 third bullet, §10.1 and verdict 3: the window-cost estimate "0.376–0.382 at ℓ = 34–50" of the toy's asymptotic
    slope is not reproduced by an independent run (0.387 ± 0.006 at ℓ = 34 → 42; ℓ > 42 has ± 0.03). Use
    "≈ 0.38–0.39 at ℓ = 30–42" and drop the window cost as support for the lower end of 0.36–0.41 (the log-corrected
    fit, 0.364, then stands alone there).

## 8. Not checked

- The toy half of verdict 1 (the lead's), §2's flash and channel tables, §6.1 (exact one-row model; the board's lab
  solved it independently), §8 (mean field), §9 (noise), §10.5 (range-3 cross), regrowth, clone correlations,
  rhoscan, slave runs.
- fg.c on vessels with N > 24 (25–32): only N ≤ 24 brute-forced.
- The gump face game in two generations (board claim) and the R = 5 count 180,615.
- Window statistics of the eight-row model; the toy lifetimes themselves (taken from the records and toy2d).
- Whether drv.c's chunk-restart scheme biases any other filed model number through settled debris; my values agree
  with the report's wherever both exist, which bounds that effect at the quoted errors for those entries.
