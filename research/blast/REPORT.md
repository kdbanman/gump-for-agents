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
the living states are the same and the exits differ. It is not a derivation of 0.2087 or of 0.231. The nearest
thing to a formula is a split of the wrapped price into two measured parts, 0.078 for the over-fill and 0.132 for
its being fatal, 0.2099 together against 0.2087 (being refereed as I write). The 135-cell hull face was **not**
measured: the sampler built for it is biased, for a reason now understood, and what stands in its place is a
forecast of 29.22 that four routes agree on.

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
3. **The two exits are in the rule, not in the chaos [exact, `rigour/`; being refereed by `ref-proofs/`].** The
   one-layer dice surrogate (the face layer on gump's rule, every cell drawing private coins for the three cells
   beneath it) was solved exactly on 25 small faces. The share of its death flux through a half-face fall is
   0.94, 0.57–0.79, 0.82 on wrapped faces of 9, 12, 15 cells and 0.017, 0.020, 0.003 on rimmed ones of 9, 12, 18.
4. **The price of a wrapped face in two parts [measured, `boom/`, `model/`; being refereed by `ref-boom/`].**
   The rate is exactly a sum over launches, 1/τ = Σ_p ν(p)·d(p): ν the frequency of a generation with face
   population p in the living state, d the chance that it is the launch of a death. Both are exponential in the
   area at fixed filling θ = p/A, and min_θ [I_up(θ) + J(θ)] = **0.2099 at θ = 0.74: 0.078 for the over-fill, 0.132
   ± 0.003 for the kill**, against 0.2087 measured. The first part is a property of the living state alone
   (−ln P(population = xA) = 1.9 + ψ(x)·A with ψ = 0.056, 0.075, 0.098, 0.127 at x = 0.70, 0.73, 0.76, 0.79, from
   the card's histograms of 16 faces, 1.27 times a Gaussian's, and identical on tubes and wide faces). The second
   is still measured from deaths. No small map reproduces the price with nothing fitted: face and layer beneath
   as a Gaussian pair give 0.160–0.165 (right route, price 23% short, found by two agents independently); the face
   with one generation of memory and measured tails gives 0.191–0.194.
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
     refereed by `ref-slab/`): 24.68 ± 0.09 for the 120-cell tube, 29.44 ± 0.22 at 144 cells, 38.6 ± 0.25 for the
     192-cell tube, 40.7 ± 0.26 for a wide 192-cell torus (the wide-face line gives 40.07; the agent allows a drift
     of ± 0.3 on the last two). Wide faces keep dying by a face-wide fall up to 192 cells (share 0.54–0.59 at 63,
     108, 192); long tubes do not (0.50, 0.50, 0.38, 0.26, 0.17 at 84, 108, 120, 144, 192).
   - Loop² 16 is a different problem at length: a cut right through the slab neither heals nor spreads, and a
     168-cell tube lives only ln τ = 17.42 ± 0.17 (`tube1d/`). The lifetime saturates.
   - My reading, frozen as forecasts before anyone looked (`PREDICTIONS.md` block 3): a long tube does not stop
     busting, it stops busting all at once. Sections more than two units apart crash a generation or so apart,
     each such freedom multiplies the rate, and a boundary between sections costs per unit of its length, so the
     freedom pays only on a short girth (the end near loop² 21) and a wide face stays rigid in time. K = 2 would
     be three timings. PENDING_STAGGER
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
7. **Why rare-event sampling fails on gump itself [measured, three agents].** On wrapped faces there is no ladder
   of levels: the rare step is the over-full generation, the crash jumps every level at once, and sixteen clones
   of one parent count as two, because the fate is sealed at the launch. On hull faces forward flux is biased
   where it is not starved (estimate − anchor = −0.027 ± 0.018, −0.173 ± 0.044, −0.35 ± 0.26 at 45, 63, 84 cells):
   a dip lasts ten generations and a flip deep in the chaos needs several to reach the face. What does work is to
   put honest dice two layers under six layers of rule and sample the dice (item 5).

## What was proved

- **The tilt identity [proved for the dice surrogate; `rigour/THEOREMS.md`, Theorem 2; PENDING_PROOFS].** Let
  ε_i(x) = −ln P(cell i is dead next | x), E = Σ_i ε_i, and μ_s ∝ μ·e^(−sE) with μ the quasi-stationary law. Then
  ln τ = ∫₀¹ ⟨E⟩_s ds: the lifetime is exactly a sum over cells of local costs along a tilt, and
  ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ ≤ 2.509·A. Checked to 12 digits on the exact solutions.
- **One price, conditionally [Theorem 3].** If local means along the tilt depend on far geometry only up to
  K·e^(−r/ξ), then wrapped and rimmed faces have one bulk price, loops give discounts per cell, and a discount
  growing like length² cannot persist. Gump's measurements contradict the conclusion at the sizes measured, so
  either the hypothesis fails (two exits is how it would fail) or the rimmed slope has not converged.
- **The seam identity [proved; `image/README.md`; checked by enumeration on small automata].** A torus is its
  loop-free cover conditioned on the whole history of a seam, two graph steps thick, recurring one loop along,
  reweighted by one over that history's probability. From it: the density deficits of several loops add to first
  order, the deficit is per cell, and it does not depend on the tube's length, the three structural facts of the
  density law. Its numbers were not derived: the picture at one instant carries none of f(9), a cell's own
  six-generation history 10% of it.
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
extrapolation seen four ways, not a measurement. PENDING_REFHULL
What would measure it: the surrogate route that worked for wrapped faces (honest coins a few layers under the
watched face of a hull), calibrated on 45–108 cells. Nobody built it tonight.

## Forecasts frozen before the data

| what | forecast | by |
|---|---|---|
| 120-cell tube (1,18),(0,40) | 24.56 ± 0.03 | PI, block 0 |
| | 24.563 ± 0.030 | `tube1d` (K = 2 fit made later: 24.571) |
| | 24.575 ± 0.025 | `model` |
| | 24.570 ± 0.025 | `rigour` |
| | 24.59 ± 0.05 | `split-slab`, bookkeeping (blind test on the 108-cell tube: 22.171 ± 0.057 against 22.160) |
| | 24.68 ± 0.09 | `split-slab`, surrogate sampler (the only one that is a measurement of anything) |
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
PENDING_REFEREES_2

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
- My own forecasts: PENDING_SCORE

## What is not known, in order of what I would do next

1. **Measure the 135- and 165-cell hull faces** with coins under the face (the method that worked on slabs).
2. **The kill.** 0.132 of the 0.21 is still only measured. The state that decides it is at least four layers
   deep and two generations long; a derivation needs the joint law of that state in the living chaos.
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
