# Forecasts for the exponent study (append-only)

Each entry is written and committed before the run that tests it. Outcomes are appended below the entry they
score, never edited in. "Truth" for the toy = `research/toy2d/README.md` §4.1 (ln τ_edge = 0.73 + 0.416·L, strips
16 × L, L = 12–36); for gump = `research/fluct/README.md` §1 (−ln h/A = 0.2268, 0.2182, 0.2164, 0.2152 at
A = 30, 45, 63, 84; I(0) = 0.2077 + 0.55/A).

## 2026-11-13T17:57Z — before any run except the engine validation

What I had seen when writing this: the validation runs (`validate.py`: toy L = 12, 16 and gump R = 9 reproduce the
published numbers), the `fg_check.py` cases (N ≤ 18: e.g. strip 3 × 6 has 2,259 cyclic states and 20% of all states
never lose an edge), and a mean-field iteration of the w = 1 model (edge density 0.68 against a measured ≈ 0.5).

**F1. Random map with killing (PROGRAM E2, OPEN-PROBLEMS item 4), exact small vessels, N = 24–32.**
The heuristic predicts ≈ |G|·τ states on immortal cycles and an immortal basin of ≈ |G|·τ²/2^N of all states
(τ = mean edge-death time, |G| = order of the vessel's symmetry group), i.e. basins of order 10⁻⁶ at N = 30.
*My forecast: it fails by orders of magnitude, in a specific way.* (a) The immortal basin is between 3% and 60% of
all states in every vessel with N ≥ 24. (b) States on immortal cycles number between 10⁴ and 10⁶ in the 4 × 8 strip
(N = 32) and ≥ 90% of them have period 1 or 2 — they are debris that happens to touch every edge, which a random
map does not have. (c) Restricted to cycles of period ≥ 8 the heuristic is not absurd: the number of states on
immortal cycles of period ≥ 8 is within a factor 30 of |G|·τ_tail, where τ_tail is the reciprocal of the hazard of
the death-time distribution at t ≥ 20 (confidence 50%). (d) The death-time distribution over all states is not
exponential at these sizes: > 95% of mortal states die within 10 generations, and whatever tail exists has a rate
whose dependence on L at fixed H ≤ 5 is much weaker than the law's (slope of −ln hazard per unit L below 0.2).

**F2. The final plunge in the toy.** In gump a dying face is ordinary until ≈ 16 generations before death at every
size. *Forecast: in the toy the plunge lengthens with L* — the lag at which the mean pre-death edge population
crosses half the living mean grows by at least a factor 1.5 from L = 16 to L = 32 (confidence 60%; my reason is
that h/p₁ falls with L in the toy and not in gump, which smells like a slow retreat with the rows beneath
relaxing). If it does not lengthen, the two automata die the same way and splitting methods fail in both.

**F3. Death = a gap as long as the edge.** Define E(ℓ) = probability that a given window of ℓ consecutive cells of
a long living edge (L = 128) is empty. *Forecast: −d ln E/dℓ at ℓ = 20–40 equals the local slope of ln τ(L) at
L = 20–36 within 10%* (i.e. lies in 0.37–0.45; confidence 60%), so that the exponent is a static property of the
infinite edge's stationary state, as γ is for the contact process (Durrett–Schonmann).

**F4. The driven-edge model** (`xp.toy_model(w, L)`): rows 0..w−1 follow the rule, rows w, w+1 are i.i.d.
Bernoulli(0.472) redrawn every generation (0.472 = bulk density of the toy on a torus, `research/toy2d` §4.3).
*Forecast:* w = 1 is long-lived with a clean exponential law, but its slope is **not** within 15% of 0.416 (I lean
to "higher", 60/40: mean field makes the lone row denser than the real edge); the slope converges to the truth
within 10% only for w ≥ 4.

**F5. The same recipe for gump — recipe fixed now, number to be entered below before any comparison.**
Let w* be the smallest w whose toy-model slope (fit of ln τ over L = 12–28, same L as available) is within 10% of
0.416. The gump prediction is the slope of ln τ against A, A = 30, 45, 63 (R = 7, 9, 11), of
`xp.gump_model(R, w*)`: the top w* {111} layers of the octahedral hull follow B45/S345 and the next two layers are
i.i.d. Bernoulli(0.4155) (gump's bulk density, PROGRAM D4). No parameter is tuned on gump. *Forecast: the gump
model's ln τ at A = 30, 45, 63 is within 0.5 nats of the measured 6.80, 9.82, 13.63 and its slope within 10% of the
measured (13.63 − 6.80)/33 = 0.207* (confidence 50%).

**F6. Noise.** Toy with independent deaths at rate ε per live cell per generation, strips 16 × L. *Forecast:*
ln τ is continuous at ε → 0 (ε = 10⁻⁴ and 10⁻³ within 3% of ε = 0 at L = 16 and 20), and the slope decreases
linearly, I(ε) ≈ I(0) − c·ε with 1 < c < 6.

**F7. The coincidence 0.416 = 2 × 0.208.** *Forecast: chance.* Tests I will run: (a) the asymptotic toy slope from
F3 / longer edges differs from 2 × 0.2077 = 0.415 by more than 3%; (b) gump with *periodic* faces (a slab of {111}
layers on a torus — the like-for-like partner of the toy's periodic strip) has a slope different from 0.208 by
more than 5%, as the toy's box edges (0.343) differ from its strip edges (0.416); (c) a third family member,
B45/S345 on the 2D range-3 cross (12 neighbours, 6 in-row, 3 below: gump's counts with a 1D edge), if it
sustains chaos at all, has a slope that is neither 0.208 nor 0.416 within 10%.

## 2026-11-13T18:20Z — w* fixed (F5), before any gump-model run

Toy-model slopes, fit of ln τ over L = 12–28 (`python3 report.py hier`; w = 6, 8 and my own truth run only to L = 24
at this moment): w = 1: 0.5308 ± 0.0011, w = 2: 0.4904 ± 0.0010, **w = 3: 0.4553 ± 0.0009**, w = 4: 0.4434 ± 0.0010,
w = 6: 0.4377 ± 0.0015, w = 8: 0.4342 ± 0.0015; truth (strips 16 × L, L = 12–24, this engine): 0.4288 ± 0.0014;
toy2d's published fit 0.416. The smallest w within 10% of 0.416 (≤ 0.4576) is **w* = 3** (w = 2 misses both 0.416
and 0.429 by more than 10%). So the gump prediction of F5 is the output of `xp.gump_model(R, 3)` with noise density
0.4155 at R = 7, 9, 11; I will also run w = 1, 2, 4, 5 to see the convergence, but w = 3 is the forecast.

Sub-forecast, from the toy's pattern (model at w = 3 is +0.01, +0.05, +0.15, +0.27 nats above the truth at
L = 12, 16, 20, 24, i.e. slightly too tough, increasingly with size): the gump model at w = 3 will come out *above*
the measured ln τ, by 0.1–0.6 nats at A = 63, with slope 0.21–0.23 against the measured 0.207.

Interim scores (details in exponent.md once written):
- F4: **hit** so far — w = 1 has a clean law with slope 0.531 (28% above 0.416, "higher" as leaned); but
  convergence within 10% is reached at w = 3, not "only for w ≥ 4" (that clause: **miss**).
- F2: **miss** — in strips 16 × L the mean edge density one generation before death is 0.29, 0.19, 0.13, 0.10 of
  the row (L = 12, 16, 20, 24) and two generations before it is already 0.61, 0.55, 0.46, 0.39 against a living mean of
  0.58: the edge dies in a two-generation flash at every size (`python3 report.py endgame`). Only a mild sag
  (≤ 12% over the previous ten generations) grows with L.

## 2026-11-13T18:41Z — periodic faces (written with the hull runs R = 7, 9 at w ≤ 4 on screen, R = 11 not yet run)

Seen so far for hull faces: A = 30: ln τ = 5.88, 6.38, 7.13, 6.55, 6.58 for w = 1…5 (measured 6.80); A = 45: 8.73, 9.91,
10.54, 9.81 for w = 1…4 (measured 9.82). The convergence in w is not monotone in gump (w = 3 is the *worst* depth),
and the R = 7 hull is too small to have a bulk under its faces (its fifth layer is the centre).

**F8. Like for like: periodic faces.** `xp.gump_slab(a, b, 12)` (a slab of twelve {111} layers on a torus, two
faces of 3ab cells, deterministic) against `xp.gump_slab_model(a, b, w)` (top w layers on Bernoulli(0.4155) noise),
A = 27, 36, 48, 60. *Forecasts:* (a) the model converges to the slab's truth: |Δ ln τ| ≤ 0.15 at every A for
w = 6 and w = 8 (confidence 65%); (b) w = 3 is again the worst of w ≥ 2 and too tough; (c) the periodic face's
slope differs from the hull's 0.208 by more than 5% (this is F7b; I lean "higher", because half the cells of a
hull face of A ≤ 84 are rim cells with only 4 in-layer neighbours).
**F9.** With eight rows the toy model does not care what the noise density is: ln τ at L = 16, 20 for ρ = 0.30 and
0.60 within 0.1 of the ρ = 0.472 values (confidence 55%) — i.e. the bulk density is not really an input.

## 2026-11-13T18:57Z — outcome of F5 (gump, the committed recipe) and a follow-up forecast

`python3 jobs.py gump; python3 report.py gump` — ln τ_face of `xp.gump_model(R, w)`, noise density 0.4155:

| w | A = 30 (R = 7) | A = 45 (R = 9) | A = 63 (R = 11) |
|---|---|---|---|
| 1 | 5.877 ± 0.016 | 8.731 ± 0.012 | 12.463 ± 0.014 |
| 2 | 6.378 ± 0.009 | 9.914 ± 0.011 | 14.274 ± 0.024 |
| **3 (the forecast)** | **7.126 ± 0.012** | **10.542 ± 0.015** | **14.653 ± 0.032** |
| 4 | 6.550 ± 0.009 | 9.808 ± 0.010 | 13.653 ± 0.022 |
| 5 | 6.580 ± 0.009 | 9.782 ± 0.010 | 13.592 ± 0.022 |
| measured hull (research/fluct) | 6.804 ± 0.003 | 9.819 ± 0.003 | 13.633 ± 0.008 |

- **F5: miss.** At the committed depth w* = 3 the model is too tough by 0.32, 0.72 and 1.02 nats (I allowed 0.5) and
  its slope over A = 30–63 is 0.228 against 0.207 (10.2% high; I allowed 10%). The sub-forecast "above by 0.1–0.6
  at A = 63, slope 0.21–0.23" got the sign and the slope and missed the size.
- What the same table shows without a forecast behind it: at **w = 4 and 5 the model reproduces the measured
  faces at A = 45 and 63 to −0.01, +0.02 (w = 4) and −0.04, −0.04 (w = 5) nats**, slope 0.2136 / 0.2117 against the
  measured 0.2119. At A = 30 it is 0.25 low: the R = 7 hull has no bulk under its faces. The depth chosen from the
  toy by a 10% criterion was one layer too shallow; w = 3 is the worst depth in gump.

**F10 (forecast, before the run).** `xp.gump_model(13, 4)` (A = 84) gives ln τ within 0.2 nats of the measured
18.077 ± 0.054 (confidence 65%; the run will have few deaths, ± 0.15 or so).

## 2026-11-13T19:14Z — outcomes of F3 and F7(a)

`python3 jobs.py gap 600; python3 report.py gap` (strips 16 × 128, 2.7×10¹¹ window samples, E(ℓ) down to 5×10⁻¹⁰):
the cost of one more empty cell, −ln[E(ℓ+1)/E(ℓ)], is 0.471 at ℓ = 5, 0.434 at 10, 0.397 at 20, 0.382 at 30 and
0.376 ± 0.002 over ℓ = 34–41, still creeping down.

- **F3: hit, and sharper than forecast.** Over ℓ = 20–40 the decrement is 0.376–0.397 against lifetime slopes of
  0.412, 0.411 (mine, L = 20–28) and 0.421, 0.382 (toy2d, L = 28–36): inside the 10% band. More: with one shift and
  one prefactor, **τ_edge(L) = 12.1 / E(L − 6.5)** reproduces all seven measured lifetimes from L = 12 to 36 (ln τ
  5.6 … 15.6) with residuals +0.03, −0.02, −0.01, −0.01, +0.03, +0.07, +0.05 nats.
- **F7(a): hit.** The toy's exponent is not 0.416. The lifetime slope falls with L (0.441, 0.434, 0.412, 0.411 per cell
  between L = 12, 16, 20, 24, 28), the static decrement has reached 0.376 at ℓ ≈ 40, and a + I·L + b·ln L fitted to
  the seven lifetimes gives I = 0.364 ± 0.006, b = 1.14 ± 0.12 (χ² 4.6/4; the straight line: χ² 95/5). The asymptotic
  value is 0.36–0.38, i.e. 1.75–1.83 × gump's 0.2077, not 2.000.

## 2026-11-13T19:34Z — gump beyond A = 84: curvature and asymptote (F11), written at the lead's request

**Disclosure.** The lead's note that prompts this entry quotes an unverified GPU report (ln τ_face = 13.635, 18.141,
23.376 ± 0.031, 29.34 ± 0.25 at A = 63, 84, 108, 135), so this forecast is *not blind* to it. What I can commit is
what my own runs imply, with the reasoning, before the review settles the numbers. I have not used the GPU numbers
below. Nothing in my comparisons so far used the constant 0.208 as the target: the model was tested against the
directly measured lifetimes at A = 30, 45, 63 (`research/fluct`), and from here on I will not quote "reproduces
0.208" as a test.

Inputs (all mine, `python3 jobs.py slab; python3 jobs.py slabmodel; python3 jobs.py gump`):
1. *Periodic faces* (no rim), truth pooled with the w = 5, 6, 8 models that agree with it: ln τ = 5.503 ± 0.005,
   7.398 ± 0.007, 9.936 ± 0.006, 12.496 ± 0.009 at A = 27, 36, 48, 60. Local slope per site **0.2106 ± 0.0010,
   0.2114 ± 0.0008, 0.2134 ± 0.0009**: it *rises* with size (2.5σ), and so does the cost per live cell (deterministic
   slabs alone: 0.394 ± 0.005, 0.398 ± 0.004, 0.408 ± 0.004). This cannot be a rim effect.
2. *Hull faces*, driven-face model: slope between A = 45 and 63 is 0.2136 ± 0.0013 (w = 4), 0.2117 ± 0.0014 (w = 5);
   measured 0.2119. The mean population of a hull face is linear in A to three figures in fluct's table
   (⟨n⟩ = 0.532·A − 2.3 for A = 30…165), so a rim term in ⟨n⟩ does not bend the law either.
3. Hull and periodic faces cost the same per live cell at these sizes (0.395–0.398 against 0.394–0.408).

**F11.** (a) *Direction:* the local slope of ln τ_face against A does **not** keep falling towards 0.2077 beyond A = 84;
it stays level or rises. Specifically ln τ(108) − ln τ(84) = 24 × (0.216 ± 0.004) = **5.18 ± 0.10** and
ln τ(135) − ln τ(108) = 27 × (0.218 ± 0.006) = **5.89 ± 0.16** (fluct's 0.2077·A + 0.55 implies 4.98 and 5.61).
(b) *Asymptote:* the per-site exponent of large asymmetric faces lies in **0.214–0.225** (confidence 70%); it is not
0.2077 ± 0.0014 (confidence 85%). The basis is the weak rise in input 1 extrapolated to saturation, so the upper end
is soft. (c) *My own model, testable here:* the periodic model at A = 75 (`xp.gump_slab_model(5, 5, 5)`) has
ln τ(75) − ln τ(60) = 15 × (0.2145 ± 0.0030), i.e. **ln τ(75) = 15.74 ± 0.05**, slope not below 0.2115.
(d) I have no mechanism for the rise. Candidate, untested: at small areas faster collapse routes supplement
cell-by-cell erosion (the toy has such a second channel, 20% of deaths at L = 12 and 1% at L = 28), and they fade.

## 2026-11-13T19:56Z — outcomes of F1, F6, F7(b, c), F8, F9; an amendment to the F7(a) entry

- **F1 (random map with killing; `python3 fg_run.py run 32`, exact, 30 vessels to N = 32): the headline hit, three
  clauses missed.** The heuristic fails by orders of magnitude because of debris, as forecast: 20–1,000 times more
  states on immortal cycles than |G|τ, and 5–94% of all states never lose an edge against a predicted 10⁻⁷–10⁻⁴.
  (a) *miss as stated*: the immortal basin is 5–29% in strips with H ≥ 4 and in boxes, but 49–94% in two- and
  three-row strips (I said 3–60% everywhere). (b) *half*: the 4 × 8 strip has 42,493 states on immortal cycles
  (inside 10⁴–10⁶) but only 72% of them have period ≤ 2 (I said ≥ 90%; periods 3–7 are common). (c) *hit where it
  can be tested*: states on immortal cycles of period ≥ 8 exist in 10 of 17 vessels with N ≥ 24 and number 0.3–8
  times |G|τ there. (d) **miss**: I said no clean exponential and a rate hardly depending on L. In fact the exact
  hazard over all initial states is flat — 0.102–0.111 for generations 6–16 in the 4 × 8 strip, 0.13–0.15 for 4–20
  in 4 × 7 — and −ln h rises by 0.43, 0.64, 0.29 per cell at H = 4, L = 5…8.
- **F6 (noise; `python3 jobs.py noise`): continuity hit, slope missed.** ln τ at L = 16, 20 is 7.433, 7.398 / 9.139,
  9.136 at ε = 10⁻⁴, 10⁻³ against 7.407 / 9.142 at ε = 0 (within 0.4%). But 3% noise changes the slope by only
  −0.023 ± 0.004 (c = 0.8 ± 0.15; I said 1 < c < 6). At L = 12 the limit is singular for the reason the brief warns
  about: uncensored debris (ln τ = 7.11 at ε = 10⁻⁴ against 5.64).
- **F7(b), F8(c) (periodic gump faces): miss.** Periodic and octahedral faces have the same slope (0.2095, 0.2126,
  0.2133 against 0.2010, 0.2119, 0.2116); I had forecast a difference above 5%.
- **F7(c) (third family member; `python3 jobs.py cross3`): hit.** B45/S345 on the 2D range-3 cross sustains chaos
  and loses edges memorylessly (CV 0.97–1.02) with ln τ = 4.08, 5.25, 5.98, 6.60, 7.16, 7.67, 8.15 at L = 16…64: the
  local slope falls from 0.147 to 0.060 per cell and has not levelled; neither 0.21 nor 0.42.
- **F8(a) hit, F8(b) miss.** Periodic model against periodic slab: w = 6, 8 within 0.03 nats at all four areas
  (allowed 0.15); w = 4, 5 within 0.05. w = 3 is too tough by 0.11–0.26 but is *not* the worst depth (w = 2:
  +0.6–1.2); the hull's non-monotone convergence does not recur.
- **F9 hit.** Eight-row toy model at noise density 0.30 / 0.60: ln τ = 7.432 / 7.417 (L = 16), 9.151 / 9.182 (L = 20)
  against 7.432, 9.165 at 0.472; all within 0.02.
- **Amendment to the F7(a) outcome above.** "The asymptotic value is 0.36–0.38" was too strong. Splitting the
  deaths by channel (`report.py` §2 table) shows that most of the curvature of ln τ(L) below L = 20 is the fading
  dense channel; the sparse channel alone has local slopes 0.411, 0.419, 0.405, 0.408 ± 0.005 between L = 12 and 28.
  The static decrement (0.376 at ℓ ≈ 40) and the log-corrected fit (0.364) still point lower, toy2d's last step
  (0.382 ± 0.015 between L = 32 and 36) agrees with them at 2σ, and my last two residuals against 12.1/E(L − 6.5)
  are positive. Honest range for the toy's asymptotic exponent: **0.36–0.41**; F7(a)'s claim (more than 3% below
  0.415) is supported by two of three estimators, not settled. Runs at L = 32–40 on the six- and eight-row models are
  queued; forecast for them: sparse-channel slope between L = 32 and 40 in 0.385–0.410 (i.e. it does not follow
  the window cost down to 0.376 by L = 40; confidence 55%).
