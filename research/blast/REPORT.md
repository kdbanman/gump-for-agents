# Why a face dies at the rate it does: report of the night of 2026-11-18

For Kirby, from the session in charge of the blast. Everything is under `research/blast/`; each agent's directory
has a README with the command for every number. Labels as in the notebook: **[proved]**, **[measured]**,
**[conjectured]**. "Refereed" means a second agent rebuilt the result with its own code from the oracle; where
that has not happened it says so. The budget, not the clock, ended the night: the Fable window filled at about 40
points an hour with eight to ten agents, so the work ran from 03:10 to about 05:45 UTC, not to 10:45.

## The short version

**A face does not thin out and die. A wrapped face dies of too much life, and a rimmed face cannot.**

- **A wrapped face (a wide torus or a tube) busts.** From an ordinary generation it over-fills in one step, to
  three quarters full (33 → 48.8 of 63 cells), together with the three layers beneath it. Then almost every live
  cell has six or more live neighbours and dies, every dead cell has too many to be born, and one generation
  later about 11 scattered cells are left over a layer that has crashed with them. Usually the fragments rebuild
  the face; about one time in 130 none of them is large enough, and the face is empty five to seven generations
  after it was normal. It happens everywhere on the face at once: no hole, no front, no band. Nearly every death
  of a wrapped face goes this way.
- **A hull face starves.** Its rim cells have 7 neighbours inside the vessel where an interior cell has 9, so they
  are almost never overcrowded; the face lives through an over-full generation and is back to normal one
  generation later. It has to die the slow way, a lopsided fade of about ten generations.
- **This is the rule and the lattice, not the chaos.** A one-layer surrogate with coins in place of the chaos,
  solved exactly, has the same two exits with the same dependence on shape.

That is the mechanism in plain words, and it is why the differences between shapes "are not in the living state":
the living states are the same and the exits differ. It is not a derivation of 0.2087 or of 0.231, and there is
no formula yet: the wrapped price splits into 0.079 for the over-full face and 0.136 for the layers beneath and
the kill, but a referee showed that their sum is bookkeeping on the same runs, not a prediction. The 135-cell
hull face has two readings that disagree: a forecast of 29.22 ± 0.02 that four routes agree on, and a first
measurement on a coin-driven surrogate, calibrated blind at 84 and 108 cells, that reads about 29.40 (+0.06,
−0.15). Neither says the wrapped price takes over (29.163).

## What was found

1. **Boom and bust on wrapped faces [measured by four independent codes: `anatomy/`, `split-slab/`, `tube1d/`,
   `boom/`; refereed by a fifth, `ref-anatomy/`, which could not break it].**
   - The launch of a death (the last generation with at least half the face alive) has a population in one hump
     at 0.738·A, the same at 48, 63, 75, 84 cells; 98% of launches are above 0.60·A, where the living mean is
     0.517·A (`boom/`). On the 63-cell torus the fall is 48.83 → 11.18 and 99.5% of the cells that die in it are
     overcrowded (`ref-anatomy/`).
   - The face does not breathe: lag-1 and lag-2 autocorrelations of its population are +0.136 and −0.031. The
     over-full generation comes in one step from a normal face.
   - It is a breath of four layers: at the launch layers 1 to 4 hold 0.73, 0.64, 0.56, 0.51 of A (normally 0.52,
     0.43, 0.41, 0.42), after layers 2 to 4 were under-full one generation before (0.40, 0.36, 0.38); one generation
     later 0.23, 0.15, 0.19, 0.30 (`boom/`; `ref-anatomy/` independently: "the boom is five layers deep", and a
     fatal fall takes the layer beneath from 39.9 to 9.9 of 63 where a non-fatal one takes it to 18.6).
   - The kill is a fragmentation: a surviving cluster of 7 or more cells regrows the face 99.4% of the time; one
     cell alone regrows it 0.138 ± 0.002 of the time, two about half.
   - The earlier "57–59% of deaths contain a fall of half the face" was a threshold cutting one hump in two; 84%
     contain a fall of 0.4 of the face. There are not two classes of death on a wrapped face.
2. **Starvation on hull faces [measured: `anatomy/`, `model/`, `boom/`, `ref-anatomy/`; the GTX 1080's own study
   of hull deaths on its branch agrees on the time course].** 1.1–1.6% of deaths of the 63-cell hull face contain
   a fall of half the face. Its return map has no cliff: one generation after 48 or more cells a wrapped face is at
   20.2 and a hull face at 29.9. Falls of half the face are 68 times rarer on the hull and, when they happen, as
   deadly. A plane fitted to the last-alive times beats 95% of shuffles in 77% of hull deaths, at 0.6 lattice units
   per generation; the last cell is on the rim line 54% of the time. Neighbours inside the vessel, by enumeration:
   interior 9, rim row 7, corner 4 (`python3 research/blast/rim/budget.py`).
3. **The two exits are in the rule, not in the chaos [exact, `rigour/`; refereed: `ref-proofs/` recomputed the
   shares to every digit with its own code].** The
   one-layer dice surrogate (the face layer on gump's rule, every cell drawing private coins for the three cells
   beneath it) was solved exactly on 25 small faces. The share of its death flux through a half-face fall is
   0.94, 0.57–0.79, 0.82 on wrapped faces of 9, 12, 15 cells and 0.017, 0.020, 0.003 on rimmed ones of 9, 12, 18.
   The referee's rider: a tube one unit cell round falls to 0.21 at 15 cells, so what matters is whether the cells
   can be overcrowded, not whether the face is wrapped.
4. **The price of a wrapped face in two parts: a split, not a formula [measured, `boom/`, `model/`; refereed by
   `ref-boom/`, which confirmed the numbers and refuted the headline].** The rate is exactly a sum over
   launches, 1/τ = Σ_p ν(p)·d(p): ν the frequency of a generation with face population p in the living state, d the
   chance that it is the launch of a death. At the launch point θ = p/A = 0.738 (referee: 0.7380 ± 0.0002, 0.7386,
   0.7375, 0.7381 at 48, 57, 63, 75 cells; the hump's width grows like A^0.58, not like A) the two slopes in the
   area are **0.079 for the over-full face and 0.136 ± 0.001 for the rest** (the layers beneath and the kill).
   `boom` reported their sum, 0.2099, against the measured 0.2087 as if it were a test. It is not: the sum rule is
   an identity, so the sum at the hump returns the lifetime slope of the very runs used (0.2154 ± 0.0011 from 48
   and 63 cells, whose lifetimes have slope 0.2156); landing near 0.2087 was an accident of the sizes. What is
   real: the split, and that the first part is a property of the living state alone
   (−ln P(population = xA) = 1.9 + ψ(x)·A with ψ = 0.056, 0.075, 0.098, 0.127 at x = 0.70, 0.73, 0.76, 0.79, from
   the card's histograms of 16 faces, 1.27 times a Gaussian's, and identical on tubes and wide faces). The second
   is still measured from deaths.
   **A measured two-layer map finds the wrapped route and four fifths of its price; it does not give the hull's
   [computed, `ref-anatomy/THEORY.md`, `boom/`; refereed by `ref-map/`].** Take the face population P and the
   population B of the layer beneath, measure their one-step map in living gump, and let a face be a Markov chain
   on (P, B) with Gaussian noise. With nothing fitted its cheapest way to an empty wrapped face is one jump up and
   a crash, (33, 25) → (45, 43) → (16, 6), where gump's dying faces go (33.3, 25.2) → (48.6, 39.7) → (12.1, 9.9); its
   action is 0.1606 per cell at 63 cells (three codes agree on 0.160–0.165), 23% short of 0.2087. The shortfall is
   mostly the non-Gaussian tail of the single jump (+0.80 ± 0.03 nats at 63 cells by the referee; +0.42, 0.76, 1.19
   at 48, 63, 84 cells by the author, about +0.025 per cell); with it and smaller measured corrections added
   linearly the author gets 0.200–0.207 [conjectured: a ledger, not re-optimised]. **For the hull the same chain
   gave 0.2313 per cell at 63 cells, the rimmed price to three digits, and the referee refuted it as a price:** it
   is the action at one size divided by the area (0.209, 0.226, 0.232 at 30, 45, 63 cells); the increments per cell
   are 0.2605, 0.2477 where gump's are 0.2010, 0.2119; the chain's own lifetimes run above gump's by 0.37, 0.75,
   about 1.0 at 45, 63, 84 cells; and which route the hull chain takes depends on what is called "the layer
   beneath". One map does not hold two prices.
5. **Tubes [measured; the reading in the last bullet is conjecture].**
   - "1.85" and "3.0" are two slopes of one curve: against the wide-face line the discount of a loop²-12 tube is
     0.0046·L² from 54 to 108 cells (L the tube's length in lattice units).
   - A tube's living state does not depend on its length; a tube booms exactly as often as a wide face of its
     area and its crash leaves the same survivors; **the discount is in the chance of death given the launch**
     (`boom/`, `model/`).
   - **A band of a living tube and a whole tube are the same object** (`tube1d/`): the probability that a band
     of width w right round the girth of a long living tube is momentarily empty, times the lifetime of a closed
     tube of length w, is e^(−3.855 ± 0.022), e^(−3.893 ± 0.053), e^(−3.98 ± 0.20) at w = 5, 6, 7 units (loop² 13:
     the same curve, constant 4.06 ± 0.05). The price of one more unit falls with the length already emptied on
     one curve for both: 0.236 per cell at 2 units, 0.219 at 4, 0.206 at 6, 0.2013 at 9. Fitted jointly:
     ln τ(L) = a + sL − ln(1 + K·e^(−L/ξ)) with c∞ = 0.2004 per cell, ξ = 1.95 lattice units, and K = 2 (χ² 3.4 on
     9; K = 1: 11.1; K = 3: 3.2). A power of the length in front (τ ∝ L^0.75·e^(0.194·cells)) fits the tubes alone.
   - **Beyond brute force, on a surrogate** (`split-slab/`: six layers of the true rule over two layers of coins,
     sampled by subset simulation over the coins; against gump's anchors +0.01 ± 0.04, −0.01 ± 0.06, +0.09 ± 0.07,
     +0.02 ± 0.06, −0.01 ± 0.09 at 63, 84, 96, 108 (tube) and 108 (wide) cells, the last three blind; being
     refereed by `ref-slab/`; final pooled offsets +0.03 ± 0.03, +0.02 ± 0.05, +0.09 ± 0.07, +0.07 ± 0.05, +0.07 ±
     0.07): **24.64 ± 0.07 for the 120-cell tube**, 38.71 ± 0.18 for the 192-cell tube and 40.59 ± 0.19 for a wide
     192-cell torus (the agent puts ± 0.3 on the last two: two wide runs read −0.33 and +0.51 against the wide-face
     line, so "0.2087 at 192 cells" is neither confirmed nor refuted). Wide faces keep dying by a face-wide fall
     up to 192 cells (share 0.54–0.59 at 63, 108, 192); long tubes do not (0.50, 0.50, 0.38, 0.26, 0.17 at 84,
     108, 120, 144, 192).
   - Loop² 16 is a different problem at length: a cut right through the slab neither heals nor spreads, and a
     168-cell tube lives only ln τ = 17.42 ± 0.17 (`tube1d/`). The lifetime saturates.
   - **A long tube does not stop busting; it stops busting all at once [measured on the surrogate's deaths, with
     gump's natural deaths at 63 and 84 cells matching it row for row; `split-slab/` §9; my forecast of it was
     frozen first, `PREDICTIONS.md` block 3].** Cut into sections two units long, every section of a dying tube
     goes from 0.69–0.73 full to 0.22 in one generation at every length (in living faces the largest falls go
     0.69 → 0.37), and at least one section busts in 95–98% of deaths. What changes with length is the timing: the
     two halves of the tube crash in different generations in 0.17, 0.21, 0.26, 0.29, 0.65 of deaths at 84, 108,
     120, 144, 192 cells, where the two halves of a wide torus do so in 0.03 at 108 and at 192 cells: a wide face
     is rigid in time, a tube is not. Neighbouring sections crash together 77–90% of the time; sections 6–8 units
     apart on the 192-cell tube only 25%. So the falling share of face-wide falls on long tubes is not a second
     route: it is the same crash, out of step. [conjectured, the PI] Each freedom of timing multiplies the rate,
     which is the discount; a boundary between sections that crash at different times costs per unit of its
     length, which is why the discount needs a short girth and ends near loop² 21; and the K = 2 of the trace form
     is a count of timings. Tested the same hour (`split-slab/` §10, forecast in block 4): if timings formed a
     simple chain, −ln P(neighbouring sections crash together) per cell would be the discount, whatever the
     section length. It is 0.019, 0.007, 0.004, 0.003 per cell for sections of 1, 2, 3, 4 units among sections that
     crash, and 0.013–0.03 without that selection, against a measured 0.008–0.010: **the order of magnitude, not
     the number, and not independent of the section length.** The discount is of the size of the entropy of timing;
     the simple chain is not its law. Not tested: whether one section's crash triggers the next.
6. **Rims [measured, `rim/`, `split-hull/`; `ref-hull/` checking the second].**
   - Corner-free strips (prisms bounded by two diagonal families, periodic along their common direction) have
     the hull's number in their mixed second difference, 0.2262 ± 0.0078 per cell with no corner anywhere, so the
     excess is not made by corners. But a strip has no single price: a cell of added width costs 0.2017 ± 0.0015,
     a cell of added length 0.2455, 0.2308, 0.2177 as the strip grows from 3 to 6 units; its bust share is
     0.15–0.20.
   - **Where the hull's rim term lives.** With ν(p) the rate of dips to p times the usual population (plain
     running, measured from radius 7 to 21) and q = 1/(τν): −ln q(0.6) is a straight line in the area with no rim
     term over 45, 63, 84, 108 cells, −2.049 + 0.17014·A (χ² 1.1 on 2). Nine tenths of the lifetime's rim term is
     in how often the face dips to 0.6 of its population; from there to empty a hull face pays 0.170 per cell.
7. **The same two exits in gump's 2D relative, with the prices the other way round [measured and exact,
   `toy/`].** In B34/S234 on the range-2 cross an edge row that is a ring dies by boom and bust (the row
   over-fills to 19.4 of 24 where 13.9 is normal, the cap takes it to one or two cells), and the edge of a box,
   whose end cells are protected, fades over 6–8 generations. There the flash is the DEARER exit per cell: the
   ring's deaths are two exponential laws, flash 0.30 + 0.455·L and no flash 4.03 + 0.327·L, the flash share falls
   from 0.90 at 12 cells to 0.47 at 32 (and, forecast first, 0.290 ± 0.024 at 36 against 0.298), and the ring's
   local price falls with it, 0.441 → 0.384, towards the box's steady 0.34. So the "0.416 against 0.343" on file
   for that rule is a crossover between exits, and the box outlives the ring only below about 25 cells. The
   exactly solved one-row surrogate has two prices that do not converge by 24 cells (open segment 0.4593 ±
   0.0003, ring 0.519–0.528), and a control rule whose end cells can be overcrowded has one price, the difference
   dying as e^(−L/2.0). Which shape is dearer depends on which exit is cheaper per cell.
8. **Why rare-event sampling fails on gump itself [measured, four agents].** On wrapped faces there is no ladder
   of levels: the rare step is the over-full generation, the crash jumps every level at once, and sixteen clones
   of one parent count as two, because the fate is sealed at the launch. On hull faces forward flux is biased
   where it is not starved (estimate − anchor = −0.027 ± 0.018, −0.173 ± 0.044, −0.35 ± 0.26 at 45, 63, 84 cells):
   a dip lasts ten generations and a flip deep in the chaos needs several to reach the face (`ref-hull/` built a
   second sampler of another design and met the same wall: −0.032 ± 0.010 at 45 cells). What does work is to put
   honest dice under six layers of rule and sample the dice (item 5).

## What was proved

- **The tilt identity [proved for the dice surrogate; `rigour/THEOREMS.md`, Theorem 2; refereed: `ref-proofs/`
  found no gap and checked it to 10⁻¹⁴ on ten shapes with its own code].** Let
  ε_i(x) = −ln P(cell i is dead next | x), E = Σ_i ε_i, and μ_s ∝ μ·e^(−sE) with μ the quasi-stationary law. Then
  ln τ = ∫₀¹ ⟨E⟩_s ds: the lifetime is exactly a sum over cells of local costs along a tilt, and
  ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ ≤ 2.509·A (the upper exponential bound, with its constant). The referee's correction to the
  reading: the split into costs per cell is not canonical, and all the non-locality sits in the tilted measures.
- **One price, conditionally [Theorem 3].** If local means along the tilt depend on far geometry only up to
  K·e^(−r/ξ), then wrapped and rimmed faces have one bulk price, loops give discounts per cell, and a discount
  growing like length² cannot persist. The referee: a valid implication (as written it needs a K₀/A added at the
  end of the tilt), **and its hypothesis is failing, visibly** [measured, exact to 15 cells and by simulation to
  30]: on wide tori the tilted law is a mixture of sparse faces and over-full faces, with the valley between the
  two humps deepening as 1.2, 3.9, 15 at 12, 18, 27 cells, while triangles keep one hump through 30 cells. A jump
  is forming along the tilt on wrapped faces. In the language of the theorem, the two exits are a first-order
  transition in the emptying ensemble, which a rimmed face does not have at these sizes.
- **The seam identity [proved; `image/README.md`; checked by enumeration on small automata].** A torus is its
  loop-free cover conditioned on the whole history of a seam, two graph steps thick, recurring one loop along,
  reweighted by one over that history's probability. Refereed: `ref-proofs/` enumerated it on gump's own
  one-layer rule (agreement to 10⁻¹⁵; a seam one unit thick fails). What does NOT follow from it without more, by
  the referee's reading: that deficits add over loops, are per cell and do not depend on the tube's length, and
  that the decay rate is a gap of the transfer matrix. Those are [conjectured] consequences. The numbers of the
  density law were not derived: the picture at one instant carries none of f(9), a cell's own six-generation
  history 10% of it.
- No lower bound e^(cA) was proved for any model with the cap, and no inequality between shapes: the exact rows
  show that "a tube never outlives a wide face" and "a rim always costs" are both false as general statements.

## The 135-cell face

**Not measured.** `split-hull/` built forward-flux sampling for hull faces and it failed calibration (item 7). In
its place there are four forecasts, by different routes, all frozen before any of the others was read:

| route | 135 cells | 165 cells | 198 cells |
|---|---|---|---|
| `split-hull/`: dip rate to 0.6 of the population measured at that size, plus the line −2.049 + 0.17014·A | 29.223 ± 0.014 | 35.779 ± 0.020 | 43.007 ± 0.027 |
| `rim/`: from strips and the hull's own values | 29.210 ± 0.035 | 35.74 ± 0.09 | |
| `model/`: forms fitted to the five hull faces | 29.215 ± 0.030 | 35.76 ± 0.08 | |
| PI (block 2) | 29.22 ± 0.03 | 35.79 ± 0.05 | |
| if the second difference repeats / if the wrapped price takes over | 29.230 / 29.163 | 35.812 / 35.613 | 43.085 / 42.689 |

They agree, and they favour "the second difference repeats" (implied 0.683 ± 0.009 through 198 cells). But the
first rests on a four-point straight line, and the others on forms fitted to the same five faces: this is one
extrapolation seen four ways, not a measurement. **The referee (`ref-hull/REVIEW.md`)** rebuilt the first route with its own stepper: the dip rates agree value
by value from radius 9 to 21 (largest difference 2.3 combined errors), the line is reproduced (slope 0.17016 ±
0.00014, χ² 0.5 on 2) and gives 29.219 ± 0.010; a quadratic in the side through the same four values gives 29.232
± 0.023. Its verdict: an honest figure is **29.22 ± 0.02, conditional** on the line having no rim term, which the
fit knows only as −0.027 ± 0.043. It favours 29.230 over 29.163 half on evidence (the dip to 0.4 of the
population, which is 14.65 of the 29.2 and carries all of the rim term, is measured at 135 cells and sits on
trend) and half by construction ("the wrapped price takes over" would be a 2% bend in the part no dip rate can
test). Beyond 135 cells the dip rate's own second difference shrinks (−0.176, −0.181, −0.176, −0.168 ± 0.002,
−0.160 ± 0.004 from 63 to 198 cells), so this route puts the 165- and 198-cell faces at 35.780 ± 0.014 and 43.011
± 0.019, below "the second difference repeats" (35.812, 43.085), and levels disagree by ± 0.03 and ± 0.05 there.
**A first measurement on a surrogate, late in the night (`split-hull/README.md`, "Dice under the hull").** The
method that worked on slabs, moved to the hull: gump's true rule on every hull cell within five layers of the
watched face, fair coins on the two layers below, sampled by subset simulation over the coins; parameters frozen
before any run above 63 cells.

| radius | cells | replications | chain − gump |
|---|---:|---:|---|
| 9 (tuning) | 45 | 32 | +0.001 ± 0.019 |
| 11 (tuning) | 63 | 32 | −0.044 ± 0.039 (brute force of the chain, 1,097 deaths: +0.006 ± 0.030) |
| 13 (blind) | 84 | 234 | +0.051 ± 0.026 |
| 15 (blind) | 108 | 184 | +0.008 ± 0.086 |
| 17 | 135 | 125 | chain 29.445 ± 0.041 |

Less the pooled blind offset (+0.047 ± 0.025, no clear drift with size) the 135-cell face reads **29.398 ± 0.048**:
3.5 errors above the dip-rate forecast and above "the second difference repeats" (29.230), 4.9 above "the wrapped
price takes over" (29.163). The agent's own caution, which I share: the rates of single replications are
heavy-tailed (at 108 cells one replication in 130 came out at 13 times the typical rate and moved the pooled value
by 0.07; none such has appeared yet at 135 cells), so the error is lopsided: **about 29.40, +0.06, −0.15**; its
odds are 3 to 2 that gump's value is above 29.30 and 1 in 10 that it is below 29.20. Coins two layers deeper change
nothing at 63 cells; coins at the living density move the chain by +0.06 ± 0.04. On the chain a hull face still
dies by a fade at every size (11 generations; a fall of half the face in 0.1%, 1.3%, 0.3% of deaths at 84, 108,
135 cells; last cells on the rim line 1.2–1.3 times its share): no sign of the hull crossing to the other exit.
PENDING_DICEHULL_FINAL

So the forecast and the first measurement disagree by about 0.18, and the measurement sits on the side nobody
forecast: the hull's second difference growing (0.86 ± 0.05 at face value), not repeating and not relaxing to the
wrapped price. Both readings agree on the one thing the question was asked for: there is no sign at 135 cells
that "two prices" is a small-size effect that goes away. Which of them is right is open, and the old GPU value
(29.34 ± 0.25) sits between them.

What would settle it: about 500 replications each at 108 and 135 cells of the same chain (three core-hours),
watching the largest replication's share of the sum, and the 165-cell face.

## Forecasts frozen before the data

| what | forecast | by |
|---|---|---|
| 120-cell tube (1,18),(0,40) | 24.56 ± 0.03 | PI, block 0 |
| | 24.563 ± 0.030 | `tube1d` (K = 2 fit made later: 24.571) |
| | 24.575 ± 0.025 | `model` |
| | 24.570 ± 0.025 | `rigour` |
| | 24.59 ± 0.05 | `split-slab`, bookkeeping (blind test on the 108-cell tube: 22.171 ± 0.057 against 22.160) |
| | 24.60 ± 0.07 | `split-slab`'s surrogate sampler as pooled by its referee (the only one that is a measurement of anything) |
| 192-cell tube (1,30),(0,64) | 39.17 / 39.01 / 38.92 / 38.86 for K = 1 / 2 / 3 / a power law | `tube1d` |
| 240-cell tube | 48.63 (K = 2); 48.40 ± 0.25 (`model`) | |
| 200-cell wide torus | 41.716 ± 0.05 (the line) | `model` |

The first five numbers for the 120-cell tube extrapolate the same three anchors and are not independent; that
face separates only K = 1 (24.608) from the rest. The 192-cell tube decides between forms.

## Referees

- **Boom and bust (`ref-anatomy/REVIEW.md`): confirmed, with the corrections already written into item 1.** Own
  stepper from the oracle, fresh seeds, lifetimes within 1σ of the anchors at five vessels. Fall share 0.559 ±
  0.006 (torus), 0.572 ± 0.006 (tube), 0.0108 ± 0.0014 (hull); q(4) = 0.3019 ± 0.0029 against 0.1827 ± 0.0023;
  the same count of survivors is deadlier after a bust (0.334 against 0.236), so the face population is not a
  Markov state and the layer beneath is the hidden variable. Its own split of the price from 48 to 63 cells:
  0.130 per cell for the rarity of the fall, 0.088 for its fatality (a different cut of the same sum as item 4).
  Not checked: holes, the band test, anything above 63 cells.
- **Proofs and exact numbers (`ref-proofs/REVIEW.md`): nothing marked proved broke.** 14 exact rows recomputed to
  every digit with its own dense code; bust shares confirmed; Theorem 2, Lemma R (with its discrete form
  corrected) and the seam identity confirmed; Theorem 3's hypothesis measured to be failing (above). Not checked:
  the 18-cell exact rows, anything on gump itself.
- **The 135-cell forecast (`ref-hull/REVIEW.md`): rates confirmed, forecast fair at 29.22 ± 0.02, conditional;**
  see "The 135-cell face". Its own forward-flux sampler failed in the same way as the first.
- **The two-part price (`ref-boom/REVIEW.md`): numbers confirmed, headline refuted.** One hump of launches at
  0.738·A, the four-layer profile at the launch, the under-full layers one generation before (real but weak: 0.4–0.6
  standard deviations per layer, a fifth to a third of it generic to any over-full face) and the island table
  (clusters of 1, 2, 3, 4–6, 7–12 cells fail 0.900, 0.634, 0.276, 0.078, 0.0051) all reproduced by its own code.
  "min(I_up + J) = 0.2099 against 0.2087" is arithmetic on the same runs. Its sentence for you: there is no formula
  yet; a formula must produce 0.738, 0.079 and 0.136 from the rule.
- **The surrogate sampler for wrapped faces (`ref-slab/REVIEW.md`): confirmed, with two corrections.** Own stepper
  for the dice chain: chain minus gump +0.012 ± 0.004 (48 cells), −0.008 ± 0.011 (63), +0.015 ± 0.057 (84-cell
  tube); half-face-fall shares equal to gump's to 0.004. No fault found in the sampler's code (the score is a
  minimum over a window of the whole path, so the over-fill is not conditioned against); sampler minus brute force
  of the same chain −0.010 ± 0.005, +0.029 ± 0.021, −0.02 ± 0.08 at 48, 63, 84 cells. Corrections: the 120-cell
  tube pools to **24.60 ± 0.07 for gump** over nine runs (χ² 2.8 on 8); "the wide 192-cell face is above the line"
  is not established (its fresh runs 39.75 ± 0.46, all pooled 40.25 ± 0.26, line 40.07, and one replication
  carries a quarter to a half of the rate), the 192-cell tube reads 38.73 ± 0.18, about 1.5 ± 0.3 below the wide
  face; the long-tube shares are a trend (192 cells: tube 0.15 ± 0.06, wide 0.70 ± 0.05), not numbers.
- **The two-layer map (`ref-map/REVIEW.md`): the wrapped half confirmed at 63 cells, the hull half refuted** (item
  4).
- **Is the wrapped price a static rarity of the four-layer state? (`ref-boom/STATIC.md`, an investigation, not
  refereed): three quarters of it.** By plain running on tori of 48–108 cells: the living state's frequency of
  "all four layers at or above the launch profile" falls as e^(−0.166 ± 0.003 per cell), and given that state the
  chance of death is 0.273, 0.162, 0.117, 0.061 at 48, 57, 63, 75 cells, i.e. e^(−0.057 ± 0.003 per cell), where
  given the face alone it falls as e^(−0.136). Tightening the state raises the chance of death towards 1 (0.85 at
  48 cells, six hundredths above the profile) but the state of near-certain death costs 0.23–0.25 per cell, more
  than the price: the face launches from a shallower state and takes its chance on the kill. Out of sample, with
  the kill law fitted on 48–63 cells and only living-state frequencies at the target size: 15.53 ± 0.16, 17.33 ±
  0.10, 22.13 ± 0.11 at 75, 84, 108 cells against 15.64, 17.54, 22.54; low, and lower with size. One generation
  before the launch nothing carries the price (a static cost of 0.005 per cell): **the price is paid in one
  generation.**
PENDING_REFEREES_6

## What failed

- **My front gas.** I read the quadratic tube discount as two-stage deaths through a band right round the girth.
  `anatomy` measured it within the hour: no band-first class. With one edge cost for every loop the form has χ²
  3,160 on 49 (`model/`). Dead.
- **"Two prices because two routes", as I first wrote it,** and my forecast that a strip's added width would cost
  nearer 0.231 (it costs 0.2017). On a wrapped face there is one route; a hull face at equal area starves more
  readily than a wrapped face thins, and lives longer only because it cannot bust.
- **Sampling gump itself** with clones and levels: three samplers built, none calibrated (item 7). The 135-cell
  face was not reached.
- **Small maps and closed forms for the price:** the tangent construction (spread 0.63 in ln τ over 48–66 cells);
  min over x of [boom + tail price × survivors] (0.275 against 0.207); one-variable maps (0.188–0.219, launched
  from the wrong place); the two-layer Gaussian map (0.160–0.165); "every surviving cluster fails on its own"
  (right to a factor 1.5 only by two errors of a factor 2–5 cancelling).
- **The numbers of the density law** from a response round the loop.
- **Exact solution at gump's own loop lengths:** a synchronous product costs 2^(A + frontier); exact reach is 18
  cells.
- **What in the kill grows like the square of a tube's length:** not found (`boom/`); at 72 cells a more
  frequent four-layer launch state accounts for 0.076 ± 0.011 of the tube's 0.164.
- My own forecasts, 14 scored: 7 held (the two 96-cell faces and the bend of loops 13 and 16, block 0; wide faces
  rigid in time and the staggered crash in substance, block 3; item 5 of block 2: the tube's advantage is not in
  the end-game), 7 failed or half failed (band-first deaths; wide tori carrying the front term; the strip's width
  price; "two prices = two routes"; one edge cost for patches and tubes; and two numbers of block 3). The 120-cell
  tube and the 135-cell hull face are still blind.

## What is not known, in order of what I would do next

1. **Settle the 135-cell hull face** (29.22 forecast against 29.40 on the coin-driven chain) and measure the
   165-cell one, with enough replications to tame the heavy tail.
2. **The kill.** Of the 0.21 per cell, 0.079 is the rarity of an over-full face, 0.166 the rarity of an
   over-full stack of four layers, and the remaining 0.05 is still only measured from deaths. The next step is
   within-layer structure of the top two layers at the launch (how many cells will be overcrowded next
   generation): if the remainder goes to zero at a static cost near the price, the price is a static large
   deviation of the living state, measurable at any size without a death.
3. **Whether 0.2087 lasts.** On the surrogate a wide 192-cell face still busts as one and sits at or above the
   line. Nobody has seen gump itself above 126 cells.
4. **Whether 0.231 is a price.** The dip rate keeps its second difference to 198 cells; the 0.170 per cell from
   0.6 of the population to empty is known only to 108 cells.
5. **A tube's asymptote** (0.2004 with K = 2, or lower with a power in front): the 192-cell tube.
6. **A lower bound.** Nothing with the cap in it has one.

## What I found beautiful

A face dies of too much life. For a week the price per cell was read off the lower tail of a face's population,
because a face that is dying is thinning. The route is through the upper tail: the face fills in one step, four
layers together, and the rule's cap turns a full face into an almost empty one in the next. The rim of a hull face
is safe from that for the plainest of reasons, a rim cell cannot count to six, and so the same rule gives a hull
face a different and dearer death. The exactly solved surrogate, which has no chaos in it at all, does the same.

And one identity nobody had asked for: in a long living tube, the chance that a stretch of it is empty at this
instant is the death rate of a closed tube of that length, up to a constant. The dead tube is already there,
momentarily, inside the living one. The price per cell is a property of the living state.
