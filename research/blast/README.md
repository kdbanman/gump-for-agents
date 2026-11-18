# research/blast: why does a face die at the rate it does? (the night of 2026-11-18)

Standing account of the PI (the session in charge of the blast). One subdirectory per agent, each with its own
README; `BRIEF-COMMON.md` is what every agent was told; `PREDICTIONS.md` holds forecasts frozen before data;
`REPORT.md` is the account for the owner. Written to as results are checked; newest state at the top.

## Where it stands at the end (05:40 UTC): read `REPORT.md`; this is the index

**The account for the owner is `REPORT.md`.** The sections below it in this file are the night's earlier states,
kept as written; where they disagree with the report, the report is later and refereed.

| directory | what it is | status |
|---|---|---|
| `anatomy/` | single deaths in space-time on tori, tubes, hull faces (45–84 cells): boom and bust; starvation on hulls | refereed by `ref-anatomy/` (confirmed, sharpened) |
| `ref-anatomy/` | the referee's own stepper and numbers; `THEORY.md`: the two-layer map | the map refereed by `ref-map/` (wrapped half confirmed, hull half refuted) |
| `boom/` | launches, the two-part split of the wrapped price, four-layer breath, fragmentation, tubes | refereed by `ref-boom/` (numbers confirmed; "0.2099 against 0.2087" is bookkeeping) |
| `ref-boom/` | review; `STATIC.md`: is the price a static rarity of the four-layer state? | the second file is unrefereed |
| `model/` | the boom's law per cell from the card's histograms; fits of every form on file; hull forms | unrefereed except where `boom/` and `ref-boom/` overlap |
| `rigour/` | the exactly solved one-layer dice surrogate; Theorems 1–3, Lemma R | refereed by `ref-proofs/` (nothing proved broke; Theorem 3's hypothesis is failing) |
| `image/` | the seam identity (a torus as its cover conditioned on a seam's history) | identity refereed by `ref-proofs/`; its consequences for the density law are conjecture |
| `rim/` | corner-free prisms: strips with rims and no corners | unrefereed |
| `split-slab/` | why splitting fails on gump; the dice-chain sampler to 192 cells; the staggered crash (§9–§11) | sampler refereed by `ref-slab/` (confirmed; 120-cell tube 24.60 ± 0.07; 192-cell errors understated) |
| `tube1d/` | a band of a living tube is a closed tube; the one-curve fit with K = 2; loop² 16 saturates | unrefereed |
| `split-hull/` | forward flux on hulls fails; dip rates to radius 21 and the forecast 29.22; dice under the hull | dip rates refereed by `ref-hull/` (confirmed); the dice chain by `ref-dicehull/` |
| `toy/` | the 2D relative: the same two exits, prices reversed, a crossover | unrefereed |
| `pi/` | the PI's own arithmetic (`frontgas_check.py`, `patch_vs_torus.py`) | unrefereed |
| `holes/` | second phase: the chance that a patch of a living face is empty; hull interior = wrapped face; the 18-cell hull face | refereed by `ref-hull/HOLES.md` (numbers confirmed, two readings corrected) |
| `strips/` | second phase: `rim/`'s corner-free strips re-measured with independent code and extended; closed tubes of the same girth; firewalls in thin strips; the tetrahedron has no steady state | unrefereed (itself a check of `rim/`'s table, which stands) |
| `noisy/` | second phase: ε-noisy gump on the whole hull and a sampler over the noise, for the 135-cell face; `data/runs/` holds the long runs' raw rows | unrefereed; validated against brute force at 45 and 63 cells, blind at 108 cells (see `REPORT.md`) |
| `lean/` | gump in Lean 4: the rule, T1 to T4, sealed sets and the hull machine-checked in core Lean; the Lean rule tied to the oracle and the 2012 logs; `README.md` there holds the aim and the climb; `mathlib/` is the package for theorems that need Mathlib | unrefereed; `sh research/blast/lean/check.sh` |
| `ref-hull/WRAPPED.md`, `ref-hull/HOLES.md` | the hull referee's second and third tasks (rimmed against wrapped faces; the referee of `holes/`) | |
| `ref-report/` | the referee of the report itself against its sources (night) | |
| `PI.md` | the investigator's standing file: the owner's words, usage rules, what is running and owed | |
| `PREDICTIONS.md` | the PI's forecasts, blocks 0–7, each frozen before its data, each scored when the data came | |

Not done, for whoever comes next: nothing here has been recomputed by the lead; `research/check.sh` was not run
against these directories (they add no tests to it); no figure was made; several agents left compiled binaries
untracked in their directories (rebuild commands are in each README). The PI's safety snapshots in the git log
are commits of agents' work in progress made so that nothing was lost when the usage window closed.

## State (04:21 UTC): the referee's verdict, and the PI's reading of the whole

- **Boom and bust is confirmed by a referee with its own code (`ref-anatomy/REVIEW.md`) and sharpened.** Nearly
  every wrapped death goes through the over-full generation (84% contain a fall of at least 0.4 of the face; the
  "57–59%" was the threshold cutting one hump in half); the face does not breathe (the boom comes in one step);
  and **the layer beneath is the hidden variable**: a fatal fall takes it 39.9 → 9.9 of 63, a non-fatal fall of
  half the face 34.5 → 18.6. The death is a joint over-fill of two layers and a joint crash.
- **The emptiness principle [conjectured as a law; measured for tubes by `tube1d`; consistent for rhombi].** For a
  face without a rim, the death rate is the living state's probability that a region of the face's own shape is
  empty at one instant, times a boundary constant: τ(closed face of shape S) × P_living(patch S empty) =
  e^(−σ·perimeter − const). `tube1d`: constant to ± 0.02 over bands of 5, 6, 7 units of a loop-12 tube. Rhombi,
  my arithmetic on the 2026-11-14 patch counts and the tori on file (`python3 research/blast/pi/patch_vs_torus.py`):
  −ln P − ln τ = 9.496 ± 0.005, 10.878 ± 0.034, 12.74 ± 0.60 for 4×4, 4×5, 5×5, i.e. 0.69 per lattice unit of
  perimeter from the first two and 12.26 forecast for the third. Three shapes, two of them fixing the line, tori of
  different loop content: consistent with the law, not a test of it.
- **Why that should be so, and what it predicts [conjectured, the PI].** `image` proved that the space-time law of
  a tube is a transfer-matrix product along the tube. Then "ℓ consecutive bands empty at one instant" is a power
  of one constrained operator in both settings, between boundary vectors for a band of a living tube and as a
  trace for a closed tube. That gives `tube1d`'s one curve (same leading eigenvalue c∞, same gap ξ ≈ 2 lattice
  units) and says more: for a closed tube ln τ(L) = a + sL − ln(1 + K·e^(−L/ξ)) with K an integer, the multiplicity
  of the second eigenvalue (its free fit gave K = 2.2). `tube1d` has been asked to test K = 1 and K = 2.
- **What this makes of "the price".** The price per cell of a wrapped face is the rate at which emptiness of the
  living state decays with area: a static property of the living chaos, measurable without a single death. Shape
  enters as finite-size terms of the emptied ensemble, whose correlation length is about 2 lattice units, four
  times the living state's: every face measured so far (2.3 to 6 units across, tubes to 10 long) is within a few
  of those lengths, which is why no two shapes agree on a price. A rim does not only add a boundary term: it
  closes the bust exit near it, and the emptied ensemble then has to be the starved one.

## State (04:15 UTC): what wave 1 found (four agents reported; referees running)

Each line names the agent's directory, where the command for every number is. Nothing here is refereed yet
unless it says so. [measured] = one code unless two are named.

1. **How a wrapped face dies: boom and bust [measured, three independent codes: `anatomy`, `split-slab`,
   `tube1d`; referee `ref-anatomy` running].** The face over-fills in one generation (33 → 48.5 of 63 cells; the
   layer beneath 25 → 40), then every live cell is overcrowded and nothing is born (→ 11.6 cells), and about one
   time in 130 the scattered survivors starve within four generations. Share of deaths with a one-generation fall
   of at least half the face: 0.57, 0.57, 0.57, 0.59, 0.60, 0.67 ± 0.05 at 48 … 84 cells; flat in space (the
   last-alive times of the cells of one death spread by 1.85 generations); no hole, no front, no band first.
   A hole or band made by hand is retaken from its edge at 0.25–0.31 units per generation and never grows.
2. **How a hull face dies: it starves [measured, `anatomy`, `model`].** Its rim line has too few neighbours
   inside the vessel to be overcrowded (7 against 9: `rim`, by enumeration), survives the over-full generation
   (0.69 per live cell against 0.42 inside) and the fall stops at 0.40–0.48 of the face where a wrapped face
   reaches 0.19; 1.6% of hull deaths contain such a fall. The face fades over about 10 generations, tilted at
   0.6 units per generation, the last cell on the rim line 54% of the time.
3. **The same two exits exist with no chaos beneath [exact, `rigour`; referee `ref-proofs` running].** In the
   one-layer dice surrogate solved exactly (6–18 cells) the share of the death flux through a half-face fall is
   0.94 / 0.57–0.79 / 0.82 on wrapped faces and 0.017 / 0.020 / 0.003 on rimmed ones. So bust-on-wrapped,
   starve-on-rimmed is the rule's cap and the lattice, not the chaos.
4. **The boom has a law per cell and is blind to shape [measured, `model`, from the card's histograms].**
   −ln P(P = xA) = 1.9 + ψ(x)·A, ψ = 0.056, 0.075, 0.098, 0.127 at x = 0.70, 0.73, 0.76, 0.79 (1.27 times the
   Gaussian value), the same on loop-12 tubes and wide faces to 0.001 per cell. The wrapped price splits about
   0.08–0.10 for the boom and 0.11–0.13 for the kill (the survivors failing to rebuild). The kill is not derived.
5. **Tubes [measured; readings differ].** A tube's living state does not depend on its length (`model`); its
   over-full deaths are as frequent as a wide face's of the same area (506 against 513 at 66 cells, `model`); its
   extra deaths are thinnings without a bust. `tube1d`: the probability that a band of width w right round the
   girth of a long living tube is empty is e^(−3.81 ± 0.02) / τ(closed tube of length w) at 5, 6, 7 units: a
   band and a tube are the same object, and the marginal price of both falls as c∞ + B·e^(−ℓ/ξ) with
   c∞ = 0.1989 (0.198–0.200) for loop² 12 and ξ = 2.05 lattice units. `model`'s one-number formula
   D = ln(b + (1 − b)·e^Δ) (b the bust share, Δ the tube's lead in the stationary lower tail) gives 0.118, 0.207,
   0.301, 0.394 against 0.125, 0.220, 0.302, 0.381 at 66–108 cells. Not settled: whether the bend is a shift
   between exits (the exact surrogate's tube: bust share 0.81 → 0.23 and a step that saturates, `rigour`) or a
   correlation length (`tube1d`: the bust share of whole tubes is flat, 0.59, 0.56, 0.51 ± 0.05 at 48, 72, 84).
6. **Rims without corners pay the hull's price [measured, `rim`, small strips].** In corner-free prisms the mixed
   second difference in width and length is 0.231 ± 0.011; width and length do not cost the same; the data
   want ln τ = a + 0.23·A − 0.21 per row, the shape of the hull's own fit (0.2306·A − 0.337·k). So the 0.231 is
   not made by corners. `model`: 0.2086·A + b·k + d + e/k also fits the hull's five faces (χ² 17 on 2).
7. **The density law has a proof of its form, not of its numbers [proved, `image`; under referee].** A torus is
   its cover conditioned on the whole history of a seam recurring one loop along; additivity over loops, a
   deficit per cell and independence of the tube's length follow. The equal-time picture carries none of f.
8. **A theorem [proved for the dice surrogate, `rigour`; under referee].** ln τ = ∫₀¹⟨E⟩_s ds under a tilt of the
   quasi-stationary law by the one-step emptying cost E = Σ_i ε_i: the lifetime is exactly a sum of local costs,
   and ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀ ≤ 2.509·A.
9. **Samplers.** Downward levels on the face population do not help on wrapped faces, because the rare step is
   the over-full generation and the crash jumps every level at once (`split-slab`, `tube1d`: both built it, both
   found this). On hull faces the route is a fade and forward flux applies (`split-hull`, calibrating; `ref-hull`
   building a second code). `boom` is building the two-stage estimate (over-fill, then kill by cloning).
10. **Dead:** the PI's front gas (no band-first class); the tangent construction as a predictor; "two prices =
    two routes" in its simple form (the no-bust route of a wrapped face costs 0.004–0.005 per cell more than its
    bust route, not 0.022).

Forecasts for the 120-cell tube (1,18),(0,40), all frozen before any measurement of it: PI 24.56 ± 0.03; `tube1d`
24.563 ± 0.030; `model` 24.575 ± 0.025; `rigour` 24.570 ± 0.025; `split-slab` in its PREDICTIONS.md.

## State (03:20 UTC)

Wave 1 launching: eight Fable agents, one angle each.

## The front gas (the PI's reading at 03:31 UTC; conjecture; forecasts in PREDICTIONS.md block 1)

Arithmetic on anchors already on file (BRIEF-COMMON.md and `research/gpu-local/README.md`, chain 3):

    python3 -c "
    import math
    w=lambda a:13.1623+0.20861*(a-63)
    for a,v in ((54,11.1935),(60,12.4219),(72,14.8755),(84,17.3175),(96,19.7446),(108,22.1599)):
        D=w(a)-v; L=a/12; print(a, round(D,3), round(D/L**2,5), round(math.exp(D)-1,3))"

gives D/L² = 0.0045 … 0.0048 for tubes of loop² 12 over a factor two in length: the tube discount is quadratic in
length, and its coefficient falls with girth as e^(−2σg), σ ≈ 0.66 per lattice unit, the edge cost of an empty
patch. Reading: two-stage deaths through a band right round the girth; a gas of fronts.

### The PI's own check of the front-gas form on the faces on file (03:36 UTC) [fitted; one code; loader of research/wrap]

`python3 research/blast/pi/frontgas_check.py 64 48` (10 s; 54 pooled wrapped faces of 48 cells and up; errors floored
at 0.0015).

- **Single short loop: a rate share ∝ L^m with one m for every girth fits.** On the 45 faces with at most one loop²
  ≤ 19: ln τ = a + c(A − 63) − ln(1 + ε_q·L^m), L = area/girth, gives χ² 60.7 on 34 with m = 2.32, c = 0.20878,
  ε = e^(−5.87), e^(−6.06), e^(−6.51), e^(−7.64) at loop² 12, 13, 16, 19 and **nothing at 21 and beyond** (the free
  strengths go to zero). So the growth with length is common to all girths, and the lead's "the discount ends
  between 19 and 21" survives in this form: ε_q ≈ 0.00033·(20.5 − q), linear in loop², not e^(−2σg) (the three
  girths 12, 13, 16 alone give σ = 0.58–0.60; the step to 19 is three times steeper). **My block-1 item 4 (wide
  tori carry the same term through loops of 21–36) is not supported by the data on file.**
- **Several short loops: rates do not simply add.** All 54 faces with one term per loop direction: χ² 200 on 43 and
  m drops to 1.6; the 4 × 4 (three loops of 16) and the long 12-tubes pull opposite ways. With ε_q = K e^(−2σg)
  imposed for every loop: χ² 971 on 49. So the form is a description of tubes, not yet a law of all wrapped faces.
- An exponential share with a site factor, r = B·L·e^(gL) with g = 0.19–0.20 per lattice unit (0.016 per cell),
  fits the loop-12 family as well as the power: the measured d ln r/d ln L is 2.26, 2.12, 2.30, 2.48, 2.56 at
  L = 4.75 … 8.5, and 1 + 0.195·L is 1.93, 2.07, 2.27, 2.46, 2.66. The two readings (bands with an entropy ∝ L^m;
  a collapse that spreads at a lower price per cell after starting somewhere) part at 200+ cells: slope returning
  towards a girth price near 0.198–0.201, against levelling at 0.192.
- Not checked: no second code; the choice of error floor; faces below 48 cells.
