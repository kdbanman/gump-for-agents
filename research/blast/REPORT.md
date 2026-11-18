# Why a face dies at the rate it does: report of the night of 2026-11-18

For Kirby, from the session in charge of the blast. Everything is under `research/blast/`; each agent's directory
has a README with the command for every number, and `research/blast/README.md` is the index. Labels as in the
notebook: **[proved]**, **[measured]**, **[conjectured]**. "Refereed" means a second agent rebuilt the result with
its own code from the oracle; every finding below says whether that happened. The budget, not the clock, ended the
night: the Fable window filled at 30 to 45 points an hour with eight to ten agents, so the work ran from 03:10 to
about 06:25 UTC, not to 10:45. This report was itself refereed against its sources (`ref-report/REVIEW.md`) and
corrected.

## The short version

**A face does not thin out and die. A wrapped face dies of too much life, and a rimmed face cannot.**

- **A wrapped face (a wide torus or a tube) busts.** From an ordinary generation it over-fills in one step, to
  three quarters full (33 → 48.8 of 63 cells), together with the layers beneath it. Then four in five of its live
  cells have six or more live neighbours and die, almost nothing is born, and one generation later about 11
  scattered cells are left over layers that have crashed with them. Usually the fragments rebuild the face; about
  one time in 130 none of them is large enough, and the face is empty five to seven generations after it was
  normal. It happens everywhere on the face at once: no hole, no front, no band. Nearly every death of a wrapped
  face goes this way.
- **A hull face fades instead.** Its rim cells have 7 neighbours inside the vessel where an interior cell has 9, so
  they are rarely overcrowded; the face lives through an over-full generation and is back to normal one generation
  later. It dies by a lopsided fade of about ten generations (of the cells that die in it, 58% starve and 42% are
  overcrowded: a tilt towards starvation, not pure starvation).
- **This is the rule and the lattice, not the chaos.** A one-layer surrogate with coins in place of the chaos,
  solved exactly, has the same two exits with the same dependence on shape; so has gump's 2D relative.

That is the mechanism in plain words, and it is why the differences between shapes "are not in the living state":
the living states are the same and the exits differ. It is **not** a derivation of 0.2087 or of 0.231, and there
is no formula yet. The 135-cell hull face is **not decided**: a forecast of 29.22 ± 0.02 (conditional on a
four-point straight line) and a first measurement on a coin-driven surrogate, 29.30 ± 0.09 after its referee's
corrections, agree within errors and neither excludes "the wrapped price takes over" (29.163) by more than 1.5 to
3 errors.

## What was found

1. **Boom and bust on wrapped faces [measured by four independent codes: `anatomy/`, `split-slab/`, `tube1d/`,
   `boom/`; refereed by `ref-anatomy/` and `ref-boom/`, which could not break it].**
   - The launch of a death (the last generation with at least half the face alive) has a population in one hump
     at 0.738·A at 48, 57, 63 and 75 cells (referee: 0.7380 ± 0.0002, 0.7386, 0.7375, 0.7381; its width grows like
     A^0.58); the living mean is 0.517·A. On the 63-cell torus the fall is 48.83 → 11.18, and 99.5% of the cells
     that die in it are overcrowded.
   - The face does not breathe: lag-1 and lag-2 autocorrelations of its population are +0.136 and −0.031. The
     over-full generation comes in one step from a normal face. One generation earlier nothing carries the price
     (a static cost of 0.005 per cell): the price is paid in one generation.
   - It is a breath of at least four layers: at the launch layers 1 to 4 hold 0.738, 0.637, 0.562, 0.504 of A
     (normally 0.517, 0.435, 0.406, 0.416), after layers 2 to 4 were slightly under-full one generation before
     (0.400, 0.354, 0.376: real but weak, 0.4–0.6 standard deviations per layer); one generation later 0.222,
     0.152, 0.190, 0.301. (`ref-anatomy/` saw a fifth layer over-full too.) A fatal fall takes the layer beneath
     the face from 39.9 to 9.9 of 63 where a non-fatal fall of half the face takes it to 18.6, so the face
     population is not a Markov state: the same number of survivors is deadlier after a bust (0.334 against 0.236
     from four cells).
   - The kill is a fragmentation: among the survivors of a bust, clusters of 1, 2, 3, 4–6, 7–12 cells fail to
     regrow the face 0.900, 0.634, 0.276, 0.078, 0.0051 of the time. (A different experiment gives a like number:
     one live cell left by hand on an otherwise emptied face over living chaos regrows it 0.138 ± 0.002 of the
     time.)
   - The earlier "57–59% of deaths contain a fall of half the face" was a threshold cutting one hump in two; 84%
     contain a fall of 0.4 of the face. There are not two classes of death on a wrapped face.
2. **The fade on hull faces [measured: `anatomy/`, `model/`, `boom/`, `ref-anatomy/`; the GTX 1080's own study of
   hull deaths on its branch agrees on the time course].** 1.1–1.6% of deaths of the 63-cell hull face contain a
   fall of half the face. Its return map has no cliff: one generation after 48 or more cells a wrapped face is at
   20.2 and a hull face at 29.9. Falls of half the face are 68 times rarer on the hull and, when they happen, as
   deadly. A plane fitted to the last-alive times beats 95% of shuffles in 77% of hull deaths, at 0.6 lattice units
   per generation (this fit and the next number were not refereed); the last cell is on the rim line 54% of the
   time, which is only 1.10 times the rim line's share of live cells. Neighbours inside the vessel, by enumeration:
   interior 9, rim row 7, corner 4 (`python3 research/blast/rim/budget.py`).
3. **The two exits are in the rule, not in the chaos [exact, `rigour/`; refereed: `ref-proofs/` recomputed the
   shares to every digit with its own code].** The one-layer dice surrogate (the face layer on gump's rule, every
   cell drawing private coins for the three cells beneath it) was solved exactly on 25 small faces. The share of
   its death flux through a half-face fall is 0.94, 0.57–0.79, 0.82 on wrapped faces of 9, 12, 15 cells and 0.017,
   0.020, 0.003 on rimmed ones of 9, 12, 18. The referee's rider: a tube one unit cell round falls to 0.21 at 15
   cells, so what matters is whether the cells can be overcrowded, not whether the face is wrapped.
4. **The price of a wrapped face: a split and a static part, not a formula [measured, `boom/`, `model/`;
   refereed by `ref-boom/`].**
   - The rate is exactly a sum over launches, 1/τ = Σ_p ν(p)·d(p): ν the frequency of a generation with face
     population p in the living state, d the chance that it is the launch of a death. At the launch point the two
     slopes in the area are **0.079 for the over-full face and 0.136 ± 0.001 for the rest** (0.147 ± 0.006 between
     63 and 75 cells). `boom` reported their sum, 0.2099, against the measured 0.2087 as if it were a test. The
     referee showed it is not: the sum rule is an identity, so the sum at the hump returns the lifetime slope of
     the very runs used (0.2154 ± 0.0011 from 48 and 63 cells, whose lifetimes have slope 0.2156).
   - The first part is a property of the living state alone: −ln P(population = xA) = 1.9 + ψ(x)·A with ψ = 0.056,
     0.075, 0.098, 0.127 at x = 0.70, 0.73, 0.76, 0.79, from the card's histograms of 16 faces of 54–120 cells; 1.27
     times a Gaussian's; identical on loop-12 tubes and wide faces to 0.001 per cell (`model/`, unrefereed except
     for one row).
   - **Three quarters of the price is static [measured, `ref-boom/STATIC.md`; not refereed].** By plain running on
     tori of 48–108 cells: the living state's frequency of "all four layers at or above the launch profile" falls
     as e^(−0.166 ± 0.003 per cell), and given that state the chance of death is 0.273, 0.162, 0.117, 0.061 at 48,
     57, 63, 75 cells, i.e. e^(−0.057 ± 0.003 per cell). Tightening the state raises the chance of death towards 1
     (0.85 at 48 cells), but the state of near-certain death costs 0.23–0.25 per cell, more than the price: the
     face launches from a shallower state and takes its chance on the kill. Out of sample, with the kill law fitted
     on 48–63 cells and only living-state frequencies at the target size: 15.53 ± 0.16, 17.33 ± 0.10, 22.13 ± 0.11
     at 75, 84, 108 cells against 15.64, 17.54, 22.54; low, and lower with size.
   - **A measured two-layer map finds the wrapped route and falls 23% short of its price; it does not give the
     hull's [computed, `ref-anatomy/THEORY.md`, `boom/`; refereed by `ref-map/`].** Let a face be a Markov chain
     on (face population, population of the layer beneath) with the drift and covariance measured in living gump
     and Gaussian noise. With nothing fitted its cheapest way to an empty wrapped face is one jump up and a crash,
     (33, 25) → (45, 43) → (16, 6), where gump's dying faces go (33.3, 25.2) → (48.6, 39.7) → (12.1, 9.9); its action
     is 0.1606 per cell at 63 cells (three codes: 0.160–0.165) against 0.2087. The shortfall is mostly the
     non-Gaussian tail of the single jump (+0.80 ± 0.03 nats at 63 cells, about +0.025 per cell); with it and
     smaller corrections added linearly the author gets 0.200–0.207 [conjectured: a ledger]. For the hull the same
     chain gave 0.2313 per cell at 63 cells, the rimmed price to three digits, and the referee refuted it as a
     price: it is the action at one size divided by the area (0.209, 0.226, 0.232 at 30, 45, 63 cells), its
     increments per cell are 0.2605, 0.2477 where gump's are 0.2010, 0.2119, and its route depends on what is called
     "the layer beneath". One map does not hold two prices.
5. **Tubes [measured; unrefereed except the sampler; the reading in the last bullet is conjecture].**
   - "1.85" and "3.0" are two slopes of one curve: against the wide-face line the discount of a loop²-12 tube is
     0.0046·L² from 54 to 108 cells (L the tube's length in lattice units).
   - A tube's living state does not depend on its length; at 54–84 cells a tube's face is over-full exactly as
     often as a wide face's of its area and its crash leaves the same survivors; **the discount is in the chance
     of death given the launch** (`boom/`, `model/`). At 72 cells a more frequent four-layer launch state accounts
     for 0.076 ± 0.011 of the tube's 0.164.
   - **A band of a living tube and a whole tube are the same object** (`tube1d/`): the probability that a band of
     width w right round the girth of a long living tube is momentarily empty, times the lifetime of a closed tube
     of length w, is e^(−3.855 ± 0.022), e^(−3.893 ± 0.053), e^(−3.98 ± 0.20) at w = 5, 6, 7 units (loop² 13: the same
     curve, constant 4.06 ± 0.05). The price of one more unit falls with the length already emptied on one curve
     for both: 0.236 per cell at 2 units, 0.219 at 4, 0.206 at 6, 0.2013 at 9. Fitted jointly: ln τ(L) = a + sL −
     ln(1 + K·e^(−L/ξ)) with c∞ = 0.2004 per cell and ξ = 1.95 lattice units at K = 2 (χ² 3.4 on 9; K = 3 fits as
     well, 3.2; K = 1 does not, 11.1). A power of the length in front (τ ∝ L^0.75·e^(0.194·cells)) fits the tubes
     alone.
   - **Beyond brute force, on a surrogate** (`split-slab/`: six layers of the true rule over two layers of coins,
     sampled by subset simulation over the coins; refereed by `ref-slab/`: surrogate and sampler confirmed, exact to
     0.02–0.03 where truth is cheap; whether its 96- and 108-cell calibrations were really blind was not audited).
     **The 120-cell tube: 24.60 ± 0.07** (the referee's pooled value for gump, nine runs, χ² 2.8 on 8). At 192
     cells, the agent's final values for gump with the errors it would defend: **tube 38.85 ± 0.12, wide torus
     40.49 ± 0.20**, wide minus tube 1.65 ± 0.2. The wide-face line gives 40.07: the surrogate is 0.42 above it, two
     of its errors and inside the possible drift of the surrogate's offset beyond 108 cells (the referee's own
     pooling: 40.25 ± 0.26, "above the line not established"). So 0.2087 at 192 cells is neither confirmed nor
     refuted. The tube against `tube1d`'s forecasts (39.17, 39.01, 38.92, 38.86 for K = 1, 2, 3 and the power law):
     K = 1 is disfavoured at 2.7 errors, the others are not separated. The errors at 192 cells are limited by a
     heavy tail: the dying chains of one replication descend from few initial states, and one replication can
     carry a quarter to a half of the summed rate.
   - **A long tube does not stop busting; it stops busting all at once [measured on the surrogate's deaths, with
     gump's natural deaths at 63 and 84 cells matching it row for row; `split-slab/` §9; unrefereed].** The share
     of deaths with a face-wide fall of half the face stays 0.54–0.70 on wide tori to 192 cells and falls on
     loop-12 tubes (about 0.50, 0.50, 0.42–0.45, 0.26, 0.15–0.17 at 84, 108, 120, 144, 192 cells; the last two good
     to ± 0.1). Cut into sections two units long, every section of a dying tube still goes from 0.69–0.73 full to
     0.22 in one generation at every length, and at least one section busts in 95–98% of deaths. What changes is
     the timing: the two halves of a tube crash in different generations in 0.17, 0.21, 0.26, 0.29, 0.65 of deaths
     at 84 … 192 cells; the two halves of a wide torus in 0.03 at 108 and at 192 cells. A wide face is rigid in
     time, a tube is not.
   - [conjectured, the PI; forecast frozen before the measurement, block 3] Each freedom of timing multiplies the
     rate, which is the discount; a boundary between sections that crash at different times costs per unit of its
     length, which is why the discount needs a short girth and ends near loop² 21. Tested the same hour (block 4;
     `split-slab/` §10): if timings formed a simple chain, −ln P(neighbouring sections crash together) per cell
     would be the discount. On the 192-cell tube it is 0.0136 ± 0.0021, 0.0129, 0.0135 for sections of 2, 3, 4 units
     (constant in the section length, as a chain requires), 1.4–1.6 times the measured discount of 0.008–0.010; the
     number is soft (0.008–0.011 with a stricter definition of a crash, 0.019–0.032 with a looser one), and no
     one-parameter chain fits both it and the decay of the timing correlation. On the wide 192-cell torus
     neighbouring quarters crash together in 0.998 of deaths: no discount. **The order of magnitude, not the
     number.**
   - Loop² 16 is a different problem at length: a cut right through the slab neither heals nor spreads, and a
     168-cell tube lives only ln τ = 17.42 ± 0.17 (`tube1d/`). The lifetime saturates.
6. **Rims [measured, `rim/` (unrefereed) and `split-hull/` (dip rates refereed by `ref-hull/`)].**
   - Corner-free strips (prisms bounded by two diagonal families, periodic along their common direction) show an
     excess over the wrapped price with no corner anywhere: their mixed second difference in width and length is
     0.274, 0.259 and 0.2262 ± 0.0078 per cell in three determinations (the last, at the largest sizes, is 0.6
     errors from the hull's 0.2307 and 2.2 from 0.2087). So the excess is not made by corners. But a strip has no
     single price: a cell of added width costs 0.2017 ± 0.0015, a cell of added length 0.2455, 0.2308, 0.2177 as
     the strip grows from 3 to 6 units; its bust share is 0.15–0.20.
   - **Where the hull's rim term lives.** With ν(p) the rate of dips to p times the usual population (plain
     running, radius 7 to 21) and q = 1/(τν): −ln q(0.6) is a straight line in the area with no rim term over 45,
     63, 84, 108 cells, −2.049 + 0.17014·A (χ² 1.1 on 2). About nine tenths of the lifetime's rim term is in how
     often the face dips to 0.6 of its population; from there to empty a hull face pays 0.170 per cell.
7. **The same two exits in gump's 2D relative, with the prices the other way round [measured and exact, `toy/`;
   unrefereed].** In B34/S234 on the range-2 cross an edge row that is a ring dies by boom and bust (the row
   over-fills to 19.4 of 24 where 13.9 is normal, the cap takes it to one or two cells), and the edge of a box,
   whose end cells are protected, fades over 6–8 generations. There the flash is the DEARER exit per cell: the
   ring's deaths are two exponential laws, flash 0.30 + 0.455·L and no flash 4.03 + 0.327·L, the flash share falls
   from 0.90 at 12 cells to 0.47 at 32 (and, forecast first, 0.290 ± 0.024 at 36 against 0.298), and the ring's
   local price falls with it, 0.441 → 0.384, towards the box's steady 0.34. So the "0.416 against 0.343" on file for
   that rule is a crossover between exits. The exactly solved one-row surrogate has two prices that do not
   converge by 24 cells (open segment 0.4593 ± 0.0003, ring 0.519–0.528), and a control rule whose end cells can be
   overcrowded has one price, the difference dying as e^(−L/2.0). Which shape is dearer depends on which exit is
   cheaper per cell.
8. **Why rare-event sampling fails on gump itself, and what works [measured, four agents].** On wrapped faces
   there is no ladder of levels: the rare step is the over-full generation, the crash jumps every level at once,
   and sixteen clones of one parent count as two, because the fate is sealed at the launch. On hull faces forward
   flux is biased where it is not starved (estimate − anchor = −0.027 ± 0.018, −0.173 ± 0.044, −0.35 ± 0.26 at 45,
   63, 84 cells; `ref-hull/` built a second sampler of another design and met the same wall): a dip lasts ten
   generations and a flip deep in the chaos needs several to reach the face. What works is to put honest dice
   under six layers of rule and sample the dice. Its limit is a heavy tail in the rates of single replications,
   which is the common cause of the soft numbers at 192 cells (item 5) and at 135 cells (below).

## What was proved

- **The tilt identity [proved for the dice surrogate; `rigour/THEOREMS.md`, Theorem 2; refereed: `ref-proofs/`
  found no gap and checked it to 10⁻¹⁴ on ten shapes with its own code].** Let ε_i(x) = −ln P(cell i is dead next |
  x), E = Σ_i ε_i, and μ_s ∝ μ·e^(−sE) with μ the quasi-stationary law. Then ln τ = ∫₀¹ ⟨E⟩_s ds, and ⟨E⟩₁ ≤ ln τ ≤
  ⟨E⟩₀ ≤ 2.509·A (the upper exponential bound, with its constant). The referee's correction to the reading: the
  split into costs per cell is not canonical, and all the non-locality sits in the tilted measures.
- **One price, conditionally [Theorem 3].** If local means along the tilt depend on far geometry only up to
  K·e^(−r/ξ), then wrapped and rimmed faces have one bulk price, loops give discounts per cell, and a discount
  growing like length² cannot persist. The referee: a valid implication (as written it needs a K₀/A added at the
  end of the tilt), whose hypothesis is plausibly false on wide tori "and probably on rimmed faces too". Its
  evidence [measured, exact to 15 cells and by simulation to 30]: on wide tori the tilted law is a mixture of
  sparse faces and over-full faces, the valley between the two humps deepening as 1.2, 3.9, 15 at 12, 18, 27 cells,
  while triangles keep one hump through 30 cells; in both families the steepest slope of ⟨E⟩_s/A rises with size.
  [conjectured, the PI's reading] In the language of the theorem the two exits are a first-order transition in the
  emptying ensemble.
- **The seam identity [proved; `image/README.md`; refereed: `ref-proofs/` enumerated it on gump's own one-layer
  rule to 10⁻¹⁵; a seam one unit thick fails].** A torus is its loop-free cover conditioned on the whole history
  of a seam, two graph steps thick, recurring one loop along, reweighted by one over that history's probability.
  What does NOT follow from it without more: that density deficits add over loops, are per cell and do not depend
  on the tube's length, and that the decay rate is a gap of the transfer matrix. Those are [conjectured]. The
  numbers of the density law were not derived: the picture at one instant carries none of f(9), a cell's own
  six-generation history 10% of it.
- No lower bound e^(cA) was proved for any model with the cap, and no inequality between shapes: the exact rows
  show that "a tube never outlives a wide face" and "a rim always costs" are both false as general statements.

## The 135-cell face: not decided

`split-hull/` built forward-flux sampling for hull faces and it failed calibration (item 8). Two things stand in
its place.

**A forecast, 29.22 ± 0.02, conditional.** The dip rate to 0.6 of the population, measured by plain running at 135
cells, plus the line −2.049 + 0.17014·A, gives 29.223 ± 0.014; `ref-hull/` rebuilt it with its own stepper (dip
rates agree value by value from radius 9 to 21; line slope 0.17016 ± 0.00014) and gets 29.219 ± 0.010, or 29.232 ±
0.023 from a quadratic through the same four values. Its verdict: 29.22 ± 0.02 if the line has no rim term, which
the fit knows only as −0.027 ± 0.043; about that the method is silent. It favours 29.230 over 29.163 half on
evidence (the dip to 0.4 of the population, 14.65 of the 29.2 with all of the rim term, is measured at 135 cells
and sits on trend) and half by construction. Two more forecasts, blind to the samplers, agree: 29.210 ± 0.035
(`rim/`) and 29.215 ± 0.030 (`model/`); mine was 29.22 ± 0.03. They are extrapolations of the same five faces.
Beyond 135 cells the dip rate's own second difference shrinks (−0.176, −0.181, −0.176, −0.168 ± 0.002, −0.160 ±
0.004 from 63 to 198 cells): this route puts the 165- and 198-cell faces at 35.780 ± 0.014 and 43.011 ± 0.019,
below "the second difference repeats" (35.812, 43.085), with levels disagreeing by ± 0.03 and ± 0.05 there.

**A first measurement on a surrogate, 29.30 ± 0.09 after its referee** (`split-hull/README.md`, "Dice under the
hull"; `ref-dicehull/REVIEW.md`). Gump's true rule on every hull cell within five layers of the watched face, fair
coins on the two layers below, sampled by subset simulation over the coins; parameters frozen before any run above
63 cells. The referee confirmed the chain with its own code (chain minus gump −0.003 ± 0.005 at 45 cells, +0.024 ±
0.019 at 63; living state right at 135 cells; coins at density 0.42 or two layers deeper shift ln τ by 0.03 or
less). The sampler's readings, chain minus gump: +0.001 ± 0.019 and −0.044 ± 0.039 at the tuning sizes, +0.047 ±
0.024 at 84 cells and +0.126 ± 0.034 at 108 (both blind; the last without one giant replication, 17 times the
median rate, with which it is +0.05 ± 0.08). At 135 cells the chain reads 29.420 ± 0.042 on 156 replications,
drifting down as replications accumulate (29.453 at 120). The agent first read this as 29.40 for gump, "above
every forecast". The referee's corrections: the ± 0.042 is not an honest error (the dying chains of one
replication descend from 25–44 of 4,096 initial chains; the estimator is unbiased in the rate but heavy-tailed, so
the value can only come down as rare large replications arrive); a constant offset is rejected (χ² 14.2 on 3) and
a line in the area gives +0.147 ± 0.040 at 135 cells. **Gump by this method: 29.30 ± 0.09**, with the offset
extrapolated, not measured: 0.8 errors above 29.230 and 1.5 above 29.163. On the chain a hull face still dies by a
fade at every size (11 generations; a fall of half the face in 0.1%, 1.3%, 0.3% of deaths at 84, 108, 135 cells,
though falls of 0.4 of the face rise from 3% to 9%).

So: forecast 29.22 ± 0.02 (conditional), surrogate 29.30 ± 0.09, the old GPU value 29.34 ± 0.25. They agree with
each other and with "the second difference repeats"; the wrapped price taking over is 1.5 to 3 errors away on
each, on evidence that is partly by construction. Nothing is decided. PENDING_LASTRUN
The deciding test, named by the referee: brute-force the chain itself at 84 cells (0.03 in about an hour on four
cores), which separates "the chain is not gump" from "the sampler's unsampled tail"; then many more initial states
per replication, and the 165-cell face.

## Forecasts frozen before the data

| what | forecast | by |
|---|---|---|
| 120-cell tube (1,18),(0,40) | 24.56 ± 0.03 | PI, block 0 |
| | 24.563 ± 0.030 | `tube1d` (its later K = 2 fit: 24.571) |
| | 24.575 ± 0.025 | `model` |
| | 24.570 ± 0.025 | `rigour` |
| | 24.59 ± 0.05 | `split-slab`, bookkeeping (blind test on the 108-cell tube: 22.171 ± 0.057 against 22.160) |
| | 24.60 ± 0.07 | `split-slab`'s surrogate sampler as pooled by its referee: the only measurement of anything |
| 135-cell hull face | 29.22 ± 0.02 (conditional); surrogate 29.30 ± 0.09 | see above |
| 165-cell hull face | 35.780 ± 0.014 (dip-rate route), 35.79 ± 0.05 (PI), 35.74 ± 0.09 (`rim`), 35.76 ± 0.08 (`model`) | |
| 192-cell tube (1,30),(0,64) | 39.17 / 39.01 / 38.92 / 38.86 for K = 1 / 2 / 3 / a power law; surrogate 38.85 ± 0.12 | `tube1d`; `split-slab` |
| wide 192-cell torus | 40.07 (the line); 40.35 ± 0.25 (`split-slab`, for gump) | |
| 240-cell tube | 48.63 (K = 2); 48.40 ± 0.25 (`model`) | |
| 200-cell wide torus | 41.716 ± 0.05 (`model`'s form; the straight line gives 41.742) | |

The first five numbers for the 120-cell tube extrapolate the same three anchors and are not independent; that
face separates only K = 1 (24.608) from the rest. The GPU's value for it lands after this report.

## Referees, in one line each (details in the items above and in each `REVIEW.md`)

- `ref-anatomy/`: boom and bust confirmed with its own code and sharpened (one hump, no breathing, the layer
  beneath as the hidden variable). Not checked: holes, the band test, anything above 63 cells.
- `ref-boom/`: launch hump, four-layer profile and island table confirmed; "0.2099 against 0.2087" refuted as
  evidence. Its sentence for you: there is no formula yet; a formula must produce 0.738, 0.079 and 0.136 from the
  rule.
- `ref-proofs/`: nothing marked proved broke; 14 exact rows recomputed to every digit; the seam identity's
  consequences and Theorem 3's hypothesis are not established.
- `ref-map/`: the two-layer map's wrapped half confirmed at 63 cells; its hull half refuted.
- `ref-slab/`: the dice chain and its sampler confirmed; 120-cell tube 24.60 ± 0.07; 192-cell numbers are not
  measurements to their first quoted errors; long-tube shares are a trend.
- `ref-hull/`: dip rates confirmed; 29.22 ± 0.02 fair and conditional; its own sampler failed like the first.
- `ref-dicehull/`: the hull chain confirmed; the 135-cell reading corrected from "29.40, above every forecast" to
  29.30 ± 0.09, nothing decided.
- `ref-report/`: this report against its sources; its corrections are applied here.
- Unrefereed: `rim/`, `toy/`, `tube1d/`, `model/` (mostly), `split-slab/` §9–§11, `ref-boom/STATIC.md`,
  `ref-anatomy/THEORY.md` beyond what `ref-map/` checked, `pi/`.

## What failed

- **My front gas.** I read the quadratic tube discount as two-stage deaths through a band right round the girth.
  `anatomy` measured it within the hour: no band-first class. With one edge cost for every loop the form has χ²
  3,160 on 49 (`model/`). Dead.
- **"Two prices because two routes", as I first wrote it,** and my forecast that a strip's added width would cost
  nearer 0.231 (it costs 0.2017). On a wrapped face there is one route; a hull face at equal area fades more readily
  than a wrapped face thins, and lives longer only because it cannot bust.
- **Sampling gump itself** with clones and levels: four samplers built, none calibrated (item 8).
- **A formula for the price:** the tangent construction (spread 0.63 in ln τ over 48–66 cells); min over x of
  [boom + tail price × survivors] (0.275 against 0.207); one-variable maps (0.188–0.219, launched from the wrong
  place); the two-layer Gaussian map (0.160–0.165, and nothing for the hull); "every surviving cluster fails on
  its own" (right to a factor 1.5 only by two errors of a factor 2–5 cancelling); the launch split read as a test.
- **The numbers of the density law** from a response round the loop; the simple timing chain as the law of the
  tube's discount.
- **Exact solution at gump's own loop lengths:** a synchronous product costs 2^(A + frontier); exact reach is 18
  cells.
- **My own forecasts** (`PREDICTIONS.md`, blocks 0–4), sixteen scored: 6 held (the two 96-cell faces and the bend
  of loops 13 and 16; wide faces rigid in time; the timing statistic constant in section length on the 192-cell
  tube and absent on the wide torus), 3 half right (boom and bust persisting on wide faces but not tubes; the
  halves of long tubes crashing apart; the size of the timing jitter), 7 failed (band-first deaths; one edge cost
  for patches and tubes; wide tori carrying the front term; the strip's width price; the tube's advantage sitting
  in a more frequent over-fill or fewer survivors; a half of a 192-cell tube busting as one; the timing chain's
  number). Six are still open, the 120-cell tube and the 135-cell face among them.

## What is not known, in order of what I would do next

1. **Settle the 135-cell hull face** (item above: brute force of the chain at 84 cells, then more initial states
   per replication), and the 165-cell one. The forecast route's own second difference is shrinking beyond 135
   cells; whether "0.231" is a price or a long transient is still the question you asked.
2. **The kill, or: is the price static?** Of the 0.21 per cell, 0.079 is the rarity of an over-full face, 0.166 the
   rarity of an over-full stack of four layers, and the remaining 0.057 is still only measured from deaths. The
   next state to try is one the rule itself names: the number of face cells that will be alive next generation
   (a function of the present state). If "over-full now and nearly empty next" has a static rarity equal to the
   price, the price is a large deviation of the living state, measurable at any size without a death.
   PENDING_LOOKAHEAD
3. **Whether 0.2087 lasts.** On the surrogate a wide 192-cell face still busts as one; its lifetime is 0.42 ± 0.20
   above the line with a possible drift of the surrogate underneath. Nobody has seen gump itself above 126 cells.
4. **A tube's asymptote** (0.2004 with K = 2, or lower with a power in front): tubes of 240–360 cells on the
   surrogate, with the timing of their sections recorded.
5. **`ref-hull`'s cheap test:** dip rates to 0.6 and 0.4 of the population on wrapped tori, to see whether the
   0.022 per cell between rimmed and wrapped faces lives in the dips or in what follows.
6. **A lower bound.** Nothing with the cap in it has one.

## What I found beautiful

A face dies of too much life. For a week the price per cell was read off the lower tail of a face's population,
because a face that is dying is thinning. The route is through the upper tail: the face fills in one step, four
layers together, and the rule's cap turns a full face into an almost empty one in the next. The rim of a hull face
is safe from that for the plainest of reasons, a rim cell can hardly count to six, and so the same rule gives a
hull face a different death. The exactly solved surrogate, which has no chaos in it at all, does the same, and so
does the 2D relative, where the prices come out the other way round.

And one identity nobody had asked for: in a long living tube, the chance that a stretch of it is empty at this
instant is the death rate of a closed tube of that length, up to a constant. The dead tube is already there,
momentarily, inside the living one.
