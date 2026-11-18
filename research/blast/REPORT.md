# Why a face dies at the rate it does: report of the night of 2026-11-18

For Kirby, from the session in charge of the blast. Everything is under `research/blast/`; each agent's directory
has a README with the command for every number. Labels as in the notebook: **[proved]**, **[measured]**,
**[conjectured]**. "Refereed" means a second agent rebuilt it with its own code from the oracle; where that has
not happened it says so. The budget, not the clock, ended the night: the Fable window was filling at about 40
points an hour with eight agents, so the work ran from 03:10 to about 05:30 UTC and not to 10:45.

## The short version

**A face does not die one way. It has two exits, and which one is open depends on its shape.**

- **Bust.** A wrapped face (a wide torus or a tube) dies by filling up. In one generation it goes from its usual
  half-full state to three quarters full (33 → 48.5 of 63 cells). Then every live cell has six or more live
  neighbours and dies, every dead cell has too many to be born, and one generation later about 12 scattered cells
  are left. Usually they rebuild the face. About one time in 130 they starve first. The whole thing takes six
  generations and happens everywhere on the face at once: no hole, no front, no band.
- **Starve.** A hull face cannot do that. The cells along its rim have only 7 neighbours inside the vessel, where
  an interior cell has 9, so they are almost never overcrowded; they live through the over-full generation and
  the face is back to normal a generation later. A hull face has to die the slow way: it thins over about ten
  generations, lopsidedly, the last cell usually on the rim.

That is the mechanism you asked for in plain words, and it is why "the differences are not in the living state":
the living states are the same and the exits are different. It is not yet a derivation of 0.2087 or of 0.231.
What it does give, and what was checked, is below.

## What was found

1. **Boom and bust on wrapped faces [measured; three independent codes agree: `anatomy/`, `split-slab/`,
   `tube1d/`; referee: see "Referees"].** Share of deaths containing a one-generation fall of at least half the
   face: 0.57, 0.57, 0.57, 0.59, 0.60, 0.67 ± 0.05 at 48, 54, 60, 63, 75, 84 cells (in a living face such a fall
   is seen in 0.15% of ten-generation windows). Population 33.2 → 48.5 → 11.6 on the 63-cell torus; the layer
   beneath goes 25 → 40 → 10 with it; 99% of the cells that die in the crash are overcrowded. The last-alive
   times of the cells of one death differ by 1.85 generations across the whole face: a flash.
   `python3 research/blast/anatomy/crash.py slab_1_4_21 t63` after `sh research/blast/anatomy/run1.sh`.
2. **Starvation on hull faces [measured, `anatomy/`, `model/`; the GTX 1080's own study of hull deaths,
   `research/dying2/hull` on its branch, agrees on the time course].** 1.6% of deaths of the 63-cell hull face
   contain such a fall (0 of 117 at 84 cells). One generation after being over-full a wrapped face is at 22.9
   cells and a hull face at 31.5. A plane fitted to the last-alive times beats 95% of shuffles in 77% of hull
   deaths, at 0.6 lattice units per generation. Neighbours inside the vessel, by enumeration: interior 9, rim row
   7, corner 4 (`python3 research/blast/rim/budget.py`).
3. **The two exits are in the rule, not in the chaos [exact, `rigour/`].** The one-layer dice surrogate (the face
   layer on gump's rule, every cell drawing private coins for the three cells beneath it) was solved exactly on
   25 small faces. The share of its death flux that passes through a half-face fall is 0.94, 0.57–0.79, 0.82 on
   wrapped faces of 9, 12, 15 cells and 0.017, 0.020, 0.003 on rimmed ones of 9, 12, 18 cells. A model with no
   chaos beneath has the same two exits with the same dependence on shape.
4. **The boom has a law per cell, and it is blind to shape [measured, `model/`, from the card's histograms of
   16 faces of 54–120 cells].** −ln P(population = x·A) = 1.9 + ψ(x)·A with ψ = 0.056, 0.075, 0.098, 0.127 at
   x = 0.70, 0.73, 0.76, 0.79, the same on tubes and wide faces to 0.001 per cell, and 1.27 times what a Gaussian
   with the living variance would give. What a crash leaves depends on the filling alone (0.75, 0.79, 0.83 full →
   0.36, 0.29, 0.23 of the face left). Of the 0.2087 a wrapped face pays per cell, about 0.08–0.10 is the price
   of the boom and about 0.11–0.13 the price of its survivors failing to rebuild. The first comes from the living
   state alone, with no fitted number. The second is still measured from deaths; nobody has derived it.
5. **Tubes [measured; the reading is not settled].**
   - A tube's living state does not depend on its length, and its upper tail is the wide face's (`model/`).
   - Your "1.85" and "3.0" are two slopes of one curve: against the wide-face line the discount of a loop²-12
     tube is 0.0046·L² from 54 to 108 cells (L the tube's length in lattice units), and one exponent 2.3 fits the
     single-loop faces of every girth (χ² 61 on 34; `python3 research/blast/pi/frontgas_check.py 64 48`).
   - **A band of a living tube and a whole tube are the same object** (`tube1d/`): the probability that a band of
     width w right round the girth of a long living tube is momentarily empty, times the lifetime of a closed tube
     of length w, is e^(−3.81 ± 0.02), e^(−3.80 ± 0.06), e^(−3.86 ± 0.20) at w = 5, 6, 7 units. So "a face dies as
     an empty patch of its own size" is true of tubes to a constant, and the price of emptying one more unit
     falls with the length already emptied on one curve for both: 0.2365 per cell at 2 units, 0.218 at 4, 0.210 at
     5, 0.2013 at 9. One form fits all twelve slopes: c∞ + B·e^(−ℓ/ξ) with c∞ = 0.199 and ξ = 2.05 lattice units.
     A power of the length in front of the exponential fits them too (τ ∝ ℓ^1.4·e^(0.186·cells)).
   - The lead's density relation is not the reason for the discount: `model/`'s one-number formula
     D = ln(b + (1 − b)·e^Δ) (b the bust share, Δ the tube's lead over the wide face in the lower tail of the
     living population at 0.52 of the mean) gives 0.118, 0.207, 0.301, 0.394 against 0.125, 0.220, 0.302, 0.381
     measured at 66, 84, 96, 108 cells.
6. **Rims without corners pay the hull's price [measured, `rim/`, strips of 48–84 cells].** Prisms bounded by two
   diagonal families and periodic along their common direction have strip faces with rims and no corner anywhere.
   Their mixed second difference in width and length is 0.2262 ± 0.0078 per cell, against the hull's 0.2307 and
   the wrapped 0.2087: the excess is not made by corners. But a strip has no single price: a cell of added width
   costs 0.2017 ± 0.0015 (rows 5 units long; no change from 8 to 14 rows), a cell of added length 0.2455, 0.2308,
   0.2177 as the strip grows from 3 to 6 units. Their bust share is 0.15–0.20, between the hull's 0.016 and the
   wrapped 0.57.
7. **Why rare-event sampling had not worked [measured, `split-slab/`, `tube1d/`].** Two agents built samplers
   with levels on a falling face population and both found the same thing before either knew of the other: there
   is no ladder. The rare step is the over-full generation, which comes before any level, and the crash then
   jumps every level at once; half of the variance of the outcome is decided before the population first crosses
   half. On hull faces, which fade, forward flux does apply (`split-hull/`).

## What was proved

- **The tilt identity [proved for the dice surrogate; `rigour/THEOREMS.md`, Theorem 2; referee: see below].** Let
  ε_i(x) = −ln P(cell i is dead next | x), E = Σ_i ε_i, and μ_s ∝ μ·e^(−sE) with μ the quasi-stationary law. Then
  ln τ = ∫₀¹ ⟨E⟩_s ds. The lifetime is exactly a sum over cells of local costs along a tilt, and
  ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ ≤ 2.509·A: the upper exponential bound, with its constant. Checked to 12 digits on the
  exact solutions.
- **One price, conditionally [proved under a stated hypothesis; Theorem 3].** If local means along the tilt
  depend on far geometry only up to K·e^(−r/ξ), then wrapped and rimmed faces have one bulk price, loops give
  discounts per cell, and a discount growing like length² cannot persist. Gump's measurements contradict the
  conclusion at the sizes measured, so either the hypothesis fails for gump (two exits is exactly how it would
  fail) or the rimmed slope has not converged. The theorem says which measurement decides.
- **The seam identity [proved; `image/README.md`; checked by enumeration on small automata].** A torus is its
  loop-free cover conditioned on the whole history of a seam, two graph steps thick, recurring one loop along,
  reweighted by one over that history's probability. It holds for any cellular automaton started from a product
  measure. From it: the density deficits of several loops add to first order, the deficit is per cell, and it
  does not depend on the tube's length, which are the three structural facts of the density law. Its numbers
  were not derived: the picture at one instant carries none of f(9), a cell's own six-generation history carries
  10% of it.
- No lower bound e^(cA) was proved for any model with the cap. No inequality between shapes was proved; the
  exact rows show that "a tube is never longer-lived than a wide face" and "a rim always costs" are both false
  as general statements about the surrogate.

## Forecasts frozen before the data

| what | forecast | by | frozen in |
|---|---|---|---|
| 120-cell tube (1,18),(0,40) | 24.56 ± 0.03 | PI | `PREDICTIONS.md` block 0 |
| | 24.563 ± 0.030 | `tube1d` | its block B |
| | 24.575 ± 0.025 | `model` | its M1, M5 |
| | 24.570 ± 0.025 | `rigour` | its R6 |
| | 24.57 ± 0.04 | `split-slab` | its block 1 |
| 135-cell hull face | 29.22 ± 0.03, nearer 29.230 with 80% | PI | block 2 |
| | 29.210 ± 0.035, nearer 29.230 with 62% | `rim` | its block 6 |
| | 29.215 ± 0.030 | `model` | its M4 |
| 165-cell hull face | 35.79 ± 0.05 (PI), 35.74 ± 0.09 (`rim`), 35.76 ± 0.08 (`model`) | | |
| loop²-12 tube at 192 cells | 39.0 if the price levels at 0.199; 38.6 if a power of the length is in front | `tube1d` | its §5 |
| 240-cell tube | 48.40 ± 0.25 | `model` | |
| 200-cell wide torus | 41.716 ± 0.05 | `model` | |

The five numbers for the 120-cell tube are not independent: all extrapolate the same three anchors, and every
form that fits them gives 24.54–24.59. That face will not decide between readings; a 192-cell tube would.
The 135-cell face: see "The 135-cell face" below.

## The 135-cell face

PENDING_135

## Referees

PENDING_REFEREES

## What failed

- **My front gas.** I noticed that the tube discount is quadratic in length and that its dependence on girth for
  loop² 12, 13, 16 matches the edge cost of an empty patch, and read it as two-stage deaths: a band right round
  the girth empties first. `anatomy` measured it within the hour: there is no band-first class (a band is finally
  empty four generations early in 48–53% of tube deaths, 57% on the wide torus, and no more often than a compact
  patch). With one edge cost for every loop the form has χ² 3,160 on 49 (`model/`). Dead.
- **"Two prices because two routes", as I first wrote it.** A wrapped face's deaths without a bust cost only
  0.004–0.005 per cell more than its deaths with one, not 0.022; and my forecast that a strip's added width would
  cost nearer 0.231 failed (0.2017).
- **Samplers with falling levels on wrapped faces** (two built, both useless there, for the reason in item 7).
- **The tangent construction** (a parabola joined to a straight tail) as a predictor of the price: spread 0.63
  in ln τ over 48–66 cells. **min over x of [boom + tail price × survivors]**: 0.275 per cell against 0.207.
- **Deriving the numbers of the density law** from a response round the loop.
- **Exact solution at gump's own loop lengths.** For a synchronous rule one matrix-vector product costs
  2^(A + frontier), not A·2^A: exact reach is 18 cells, and loop² ≥ 9 is out of it.
- My own record: of the forecasts I froze that have been scored, PENDING_SCORE.

## What is not known, in order of what I would do next

1. **The kill.** The price of the survivors of a crash failing to rebuild (0.11–0.13 per cell) is the half of
   0.2087 that is still only measured. If it is "every surviving clump fails on its own" it can be computed from
   the clump statistics after a crash and regrowth probabilities by clump size (one cell 0.12–0.16, two about
   0.5, measured), and then the wrapped price is a formula with no fitted number.
2. **Whether 0.2087 itself lasts.** Boom and bust needs the whole face over-full at once. Its share of deaths
   rises slowly to 84 cells; nobody has seen a death above 108 cells. Nothing measured here says what a
   300-cell wrapped face does.
3. **Whether 0.231 is a price.** The hull's second difference and the strips' mixed difference agree, but strips
   are anisotropic and their length price is still falling at 6 units. The 165- and 198-cell faces decide.
4. **A tube's asymptote**: 0.199 or lower for loop² 12. A 192-cell tube decides between a levelling price and a
   power of the length.
5. **A lower bound.** Nothing with the cap in it has an exponential lower bound on the lifetime.

## What I found beautiful

A face dies of too much life. For a week the question was how a face thins out, and the price per cell was read
off the lower tail of its population. The route is through the upper tail: the face fills, and the rule's cap
(six or more neighbours kills) turns a full face into an almost empty one in a single step. The rim of a hull
face is protected from that by having too few neighbours to be overcrowded, and so the same rule gives a hull
face a different death. The exactly solved surrogate, which has no chaos in it at all, does the same.

And one identity I did not expect: in a long living tube, the chance that a stretch of it is empty at this
instant is the death rate of a closed tube of that length, up to a constant. The dead tube is already there,
momentarily, inside the living one.
