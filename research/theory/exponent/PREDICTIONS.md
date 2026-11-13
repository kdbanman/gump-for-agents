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
