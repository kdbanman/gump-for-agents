# Forecasts of the blast (2026-11-18), frozen before the data

Each block: who, UTC time, what was known, the numbers with errors and probabilities. Scored below each block
when the data arrive. Agents' own forecasts are in `research/blast/<agent>/PREDICTIONS.md`.

## Block 0: the PI, 03:19 UTC by the machine clock (commit d1af672), before reading "Chain 3" of research/gpu-local/README.md and before any agent has run

Known to me: the anchors in BRIEF-COMMON.md and nothing about the 96-cell faces with loop² 16 and 13 or the extra
seeds on the long tubes. These are quick, by hand, and I hold them weakly.

| face | cells | my forecast | reasoning | P(within my error) |
|---|---:|---|---|---:|
| (1,3),(0,32), one loop² 13 | 96 | 19.820 ± 0.012 | 15.5250 at 75 cells, slope bending from 0.2060 to about 0.2045 as the 12-tube's did | 45% |
| (4,0),(0,8) or (1,8),(0,32), one loop² 16 | 96 | 19.935 ± 0.012 | wide line less 0.054 at 63 cells, slope 0.2072 with a slight bend (length 6.9 units) | 45% |
| (1,18),(0,40), one loop² 12 | 120 | 24.56 ± 0.03 | 22.1557 at 108 cells plus 12 × 0.2005; I expect the local slope to keep falling slowly (0.2019 from 84 to 96, 0.2013 from 96 to 108) | 50% |

Qualitative, same time:
- P(the local slope of the loop-12 tube from 108 to 120 cells is below 0.2030) = 85%; below 0.2000: 35%.
- P(tubes of loop² 13 and 16 also fall below their 54–84-cell lines by 96 cells, by more than 0.010) = 65% and 45%.
- P(the 135-cell hull face, once someone reaches it to ± 0.03, is nearer 29.230 than 29.163) = 50%. I have no view
  yet; a prefactor A^(−1.5) on the wrapped price would put it at 29.205.

### Block 0 scored (03:30 UTC, after reading "Chain 3")

- Loop² 13 at 96 cells: forecast 19.820 ± 0.012; the card has 19.8109 ± 0.0062 (−0.009). Held.
- Loop² 16 at 96 cells: forecast 19.935 ± 0.012; the card has 19.9366 ± 0.0064 and 19.9284 ± 0.0063. Held.
- "Tubes of 13 and 16 also fall below their short-tube lines by more than 0.010": both did (0.040, 0.014–0.019). Held.
- The 120-cell tube and the 135-cell hull face are still blind.

## Block 1: the PI, 03:31 UTC by the machine clock (commit 10753e8): the front-gas reading of tubes, before any agent of the blast has reported

**What I noticed in numbers already on file** (`python3` arithmetic in `research/blast/README.md`, section "The
front gas"; no new run). Against the wide-face line 13.1623 + 0.20861 (A − 63), the discount D of a tube with one
loop² of 12 is 0.091, 0.114, 0.164, 0.226, 0.302, 0.390 at 54, 60, 72, 84, 96, 108 cells, and D/L² (L = A/12, the
tube's length in lattice units) is 0.0045, 0.0046, 0.0046, 0.0046, 0.0047, 0.0048. So the "1.85" and the "3.0"
are one thing: **the discount is quadratic in the tube's length** (exponent 2.1 to 2.5 as a share of the rate).
Loop² 13 the same (0.141 at L = 6.0, 0.236 at 7.7: ratio 1.67 against 1.64). And across girths the coefficient
falls as e^(−2σg) with σ = 0.65–0.67 per lattice unit (girths √12, √13, 4: 2β = 0.0092, 0.0078, 0.0046), which is
the cost of the edge of an empty patch in a living face read from the patch counts of 2026-11-14 (0.58–0.72 per
unit of perimeter, depending on the bulk price assumed).

**The reading [conjectured].** A face can die in two stages: a band right round the girth empties first (cost: its
cells at the bulk price, plus two fronts of length g at σ each), and the rest follows before the band refills.
The number of bands is ∝ L² (where it starts, how long it is), times a window that grows with the band. So

    1/τ_tube = e^(−a − c·A) · (1 + K·e^(−2σg)·L^m + more bands …),   m between 2 and 3, K of order 1,

a gas of fronts in space-time. For long tubes the gas has a free energy per unit length, and ln τ becomes
straight again with a girth-dependent price below the wide one: c − μ(g)/n_g with μ of the order of e^(−σg).

Forecasts (probabilities are mine, now):

1. **Band-first deaths exist and their share is the discount.** In dying trajectories of a loop-12 tube, the
   fraction in which some band right round the girth is finally empty at least 4 generations before the last cell
   of the face dies is 1 − e^(−D) within a factor 1.5: about 9% at 54 cells, 12% at 63, 20% at 84, 32% at 108; and
   below 5% on wide tori of 63 cells. P = 55%. (If deaths on tubes show no band-first class at all, the reading
   is dead.)
2. **The 12-tube's local slope stops falling.** Between 240 and 360 cells it is 0.198 ± 0.004 per cell; it is
   nowhere below 0.190 up to 360 cells. P = 50%. P(the discount stays quadratic, slope 0.193 at 240 cells and
   0.185 at 360) = 20%. P(ln τ saturates: slope below 0.15 somewhere up to 360 cells) = 5%.
3. **One σ for patches and tubes.** A direct measurement of the cost of a front (empty half of a long tube or
   strip, or large patches by a rare-event sampler) gives σ = 0.66 ± 0.08 per lattice unit of front. P = 50%.
4. **Wide tori carry the same term, small.** K·e^(−2σs)·L² with s the shortest period: about 0.03, 0.017, 0.008 at
   63, 84, 108 cells for the equilateral faces, so the fitted wide-face slope 0.2086 overstates the bulk price by
   about 0.0005 and "a loop of 21 costs nothing" was a statement about a baseline that carries its own loops.
   P = 45%.
5. Not a forecast, a gap: this reading gives a hull face nothing but constants (a front can cut off a corner
   cheaply, but the number of cheap cuts does not grow with the face), so it does not explain 0.231.

### Block 1 scored so far (03:50 UTC)

- Item 1 (band-first deaths, share ≈ 1 − e^(−D), under 5% on the torus): **refuted** by `anatomy`
  (research/blast/anatomy/README.md §3): a band right round the girth is finally empty 4 generations early in
  48–53% of deaths on loop-12 tubes, 57% on the wide torus, and no more often than a compact patch of the same
  cells (54–58%). There is no band-first class; the statistic does not even discriminate. The front gas is dead.
  (The quadratic growth of the tube discount with length stands as a description: χ² 61 on 34 for one exponent.)
- Item 4 (wide tori carry the same term): contradicted by my own fit (README, 03:36).
- Items 2 and 3: open; item 3's premise is gone.

## Block 2: the PI, 03:50 UTC, after reading anatomy's account and before any sampler has reported

What changed: `anatomy` finds two routes to an empty face [measured at 45–84 cells, one code, not yet refereed].
Wrapped faces **bust**: the face over-fills (48.5 of 63 cells), overcrowding kills more than half of it in one
generation, about 12 scattered cells remain and starve; flat in space, 6 generations. Hull faces **starve**: a
tilted fade over 10 generations; their rim line has too few neighbours to be overcrowded and survives the
over-full generation. A hole is retaken from its edge at 0.25–0.31 units per generation.

My reading [conjectured]: there are two prices because there are two ways to empty a cell. Bust is cheap (about
0.209 per cell) and needs the cell to be far from anything that survives a bust: a rim line, or living face.
Starve is dear (about 0.231). "Far" means further than life comes back while the survivors of a bust starve and
the rim itself is starved: about 0.3 units per generation × 10 generations ≈ 3 units. Every hull face measured so
far (inradius 1.4 to 2.3 units) is inside that zone throughout; an empty patch in a living face is too (its
perimeter-free price falls 0.273, 0.252, 0.237, 0.226 as it grows); a wrapped face has no zone at all.

Forecasts:
1. **The 135-cell hull face is nearer 29.230 than 29.163**: P = 80%. Point forecast 29.22 ± 0.03 (the second
   difference stays 0.68–0.69). The 165-cell face: 35.79 ± 0.05; P(its second difference is still above 0.66) = 65%.
2. **The hull's second difference does fall, later**: a face whose inradius exceeds about 3 units (k ≥ 11, 198
   cells and up) has an interior that can bust; P(second difference below 0.66 somewhere by k = 12) = 50%.
3. **Corner-free strips with two rims** (agent `rim`): at widths under about 5 units the price per cell of added
   width is nearer 0.231 than 0.209: P = 70%.
4. **Boom and bust persists on wrapped faces at 108–240 cells**: the share of deaths with a one-generation fall of
   half the face does not drop below 40%: P = 55%. (If it drops, something local takes over and the wrapped
   price must bend; the 12-tube's bend might be exactly that.)
5. **The tube's advantage is in the boom or the bust, not the end-game**: at equal area a loop-12 tube has a
   larger variance of the face population than a wide torus (more frequent over-full generations) or fewer
   survivors of the bust; P(one of the two accounts for more than half of the discount) = 60%.

### Block 2 scored so far (04:20 UTC)

- Item 3 (corner-free strips: price per cell of added width nearer 0.231 than 0.209 under about 5 units): **failed
  as worded.** `rim`: 0.169–0.173, 0.195, 0.2017 ± 0.0015 per cell of added width at row lengths 3, 4, 5 units, with
  no change from 8 to 14 rows: below both, and no support zone that ends within 7 rows. What the strips do show is
  the hull's number in the mixed second difference (0.2262 ± 0.0078 with no corner anywhere), a length price that
  falls with length (0.2455, 0.2308, 0.2177 per cell for 3→4, 4→5, 5→6 units) and a bust share of 0.15–0.20
  (hull 0.016, wrapped 0.57). My "zone that life retakes from the rim" is not what the strips show.
- Item 1 (135 cells): open; `rim` forecasts 29.210 ± 0.035, `model` 29.215 ± 0.030, both blind to the samplers.
- "Two routes, two prices" in its simple form is weakened by `model`: on a wrapped face the route without a bust
  costs only 0.004–0.005 per cell more than the route with one (the bust share rises 0.57 → 0.60 → 0.67 from 48
  to 84 cells), and at equal area a hull face starves more readily than a wrapped face's own no-bust route; it
  lives longer only because it has no bust route at all (worth 0.85–0.9 at 63 cells).
- Items 2, 4, 5: open.

## Block 3: the PI, 04:45 UTC: the staggered crash, before anyone has looked at where along a long tube the crash falls

What I know: `split-slab` (surrogate sampler, calibrated to ± 0.06 against gump at 63–108 cells) reports that the
share of deaths with a one-generation fall of half the face stays 0.54–0.59 on wide tori to 192 cells and falls on
loop-12 tubes: 0.50, 0.50, 0.38, 0.26, 0.17 at 84, 108, 120, 144, 192 cells. `tube1d`: in 84-cell tube deaths the
death times of 0.5-unit bands differ by 1.2 generations r.m.s. and are uncorrelated beyond 2.5 units; band and
tube lie on one curve c∞ + B·e^(−ℓ/ξ), ξ = 1.95, and the trace form wants K = 2. `boom`: a tube booms as often as
a wide face and its crash leaves the same survivors; the discount is in the chance of death given the launch.
Nobody has looked at the crash section by section.

**Reading [conjectured].** A long tube does not stop busting; it stops busting all at once. Sections further apart
than about two lattice units crash a generation or so apart, and each such freedom multiplies the death rate. A
boundary between sections that crash at different times costs something per unit of its length, so the freedom
pays only while the girth is short (hence the end near loop² 21), and a wide face stays rigid in time at every
size (hence no bend in the wide price). In a tube the timings form a one-dimensional chain: the trace of a small
transfer matrix on W timings, ln τ = a + sL − ln(1 + (W − 1)·e^(−L/ξ)); K = 2 is W = 3 (a generation early, on
time, a generation late).

Forecasts:
1. Cut each dying tube into its two halves along the length and take each half's crash generation (the generation
   of its largest one-generation fall). The share of deaths in which the halves crash in different generations
   rises with length: about 30–45% at 84 cells, above 65% at 192. P = 60%.
2. Each half's own crash is still a bust: in more than half of deaths of the 192-cell tube at least one half loses
   half of its own cells in one generation. P = 60%. (If long tubes die by thinning with no local bust at all, the
   reading is dead and the change of route is real.)
3. On wide tori of 108 and 192 cells the two halves crash in the same generation in more than 75% of deaths. P = 55%.
4. Crash times of sections 2 units long, along a 144- or 192-cell tube: r.m.s. difference between neighbours
   1.0–1.6 generations, no growth with separation beyond 3 units. P = 50%.

### Block 3 scored (05:08 UTC; `split-slab/README.md` §9, definitions committed by the agent before it read this block)

- Item 1 (halves crash in different generations: 30–45% at 84 cells, above 65% at 192): **half right.** 0.17 ± 0.02
  at 84 (gump's own natural deaths: 0.17 ± 0.04), 0.21, 0.26, 0.29 at 108, 120, 144, and 0.65 ± 0.08 at 192. It
  rises as forecast and I had the short tubes twice too staggered.
- Item 2 (at 192 cells at least one HALF loses half its cells in one generation in more than half of deaths):
  **failed as worded** (0.22 ± 0.06). The unit that busts is a section of 2–4 units, not a half: at least one
  2-unit section busts locally in 0.98 of deaths at 192 cells and 3.7 of 8 sections do. The reading survives, my
  number did not.
- Item 3 (wide tori of 108 and 192 cells: halves crash together in more than 75%): **held** (0.97 at both).
- Item 4 (neighbouring sections differ by 1.0–1.6 generations r.m.s., no growth with separation beyond 3 units):
  **half right** (the size is about right once sections that do not crash are set aside; it does grow, out to about
  6 units).
- So: "a long tube does not stop busting, it stops busting all at once" stands [measured on the surrogate; gump
  matches at 63 and 84 cells]; the link from the freedom of timing to the size of the discount is still conjecture.

## Block 4: the PI, 05:10 UTC: the timing chain, before `split-slab` computes the bond statistic

If crash timings along a dying tube form a chain in which every change between neighbours carries a weight, then
in the dying ensemble P(two neighbouring sections crash in the same generation) = 1/λ₁ exactly, and the tube's
discount per cell against a tube that could only crash at once is −ln P / (cells per section), with nothing
fitted. From the 77–90% quoted for 2-unit sections that is 0.004–0.011 per cell, against a measured 0.008–0.010
(wide price 0.2087 less the loop-12 tube's asymptote 0.199–0.2004).

1. Computed properly in the bulk of the 144- and 192-cell tubes, the implied discount is 0.006–0.011 per cell for
   2-unit sections: P = 55%.
2. It does not depend on the section length (1 to 4 units) by more than a third: P = 35%. (Crashes shorter than
   a section's own coherence would break this at 1 unit.)
3. On the wide 192-cell torus the same statistic between neighbouring quarters gives a discount below 0.001 per
   cell: P = 70%.
4. If item 1 fails by more than a factor two either way, the discount is not the entropy of timing and I do not
   know what it is.

### Block 4 scored (05:25 UTC; `split-slab/README.md` §10)

- Item 1 (implied discount 0.006–0.011 per cell for 2-unit sections): **held only under one of two definitions**:
  0.0073 ± 0.0013 between sections that both crash with a half-fall, 0.0163 ± 0.0018 over all sections; the agent's
  selection-free reading is 0.013–0.03 against the measured 0.008–0.010. I count it failed.
- Item 2 (independent of section length within a third): **failed**: 0.019, 0.007, 0.004, 0.003 per cell for 1, 2,
  3, 4 units.
- Item 3 (wide 192-cell torus: discount below 0.001): not in the tables I have read; the halves of wide tori
  crash together in 0.97 of deaths, which is 0.0003 per cell at 108 cells. Counted held.
- Item 4: by my own rule the failure is within a factor of two to three: "the order of magnitude, not the number".
  The entropy of timing is the right size for the tube's discount; the simple chain is not its law.

### Final scoring of the PI's blocks (05:58 UTC), after the report's referee recounted them (`ref-report/REVIEW.md`)

Corrections to the scores above:
- Block 2 item 4 (boom and bust persists on wrapped faces at 108–240 cells, share never under 40%): **half right.**
  On the surrogate, wide tori keep 0.54–0.70 to 192 cells; loop-12 tubes fall to 0.15–0.17 at 192 (they bust in
  sections out of step). Gump itself has not been seen above 84 cells.
- Block 2 item 5 (the tube's advantage is a more frequent over-full face or fewer survivors): **failed.** `boom`: a
  tube's face is over-full exactly as often as a wide face's and its crash leaves the same survivors; the
  discount is in the chance of death given the launch.
- Block 4 item 2 (the timing statistic does not depend on section length): **held on the 192-cell tube** (0.0136,
  0.0129, 0.0135 per cell for 2, 3, 4 units); the 144-cell tube, on which I first scored it failed, is too short
  to test it. Item 1 stays failed (1.4–1.6 times the measured discount). Item 3 held (0.998 together on the wide
  192-cell torus).
- Block 1 item 3 (one edge cost of 0.66 ± 0.08 for patches and tubes): **failed** (`model`: 0.50–0.73 depending on
  the shape family; its premise is gone with the front gas).

Count: sixteen scored. Held 6 (block 0: three; block 3 item 3; block 4 items 2 and 3). Half right 3 (block 2 item
4; block 3 items 1 and 4). Failed 7 (block 1 items 1, 3, 4; block 2 items 3 and 5; block 3 item 2; block 4 item
1). Open 6: the 120-cell tube and its slope (block 0), the 135-cell face (blocks 0 and 2: forecast 29.22 ± 0.03;
surrogate 29.30 ± 0.09, not decided), the 12-tube's slope at 240–360 cells (block 1 item 2), the hull's second
difference by k = 12 (block 2 item 2).

## Block 5: the second phase (PI; frozen 11:15 UTC 2026-11-18, before any agent of the second phase has started)

What I had seen when writing this: the report as it stands; the GTX 1080 session's interim for the 120-cell tube,
six of eight runs, 24.497 ± 0.019 (its `AGENT.md`, addendum of 09:00Z; so the tube forecasts of block 0 are no
longer blind to me and I add none); its study of dying faces (`research/dying2/` on `claude/gpu-local-1080`).

Two experiments are about to be briefed. **Holes:** the chance that a patch of a living face is empty at an
instant, on wide tori and inside large hull faces. **Noisy hull:** gump on the whole hull with a low rate ε of
honest coin replacements deep under the watched face, sampled by subset simulation over the noise, extrapolated
to ε = 0 at the target size.

1. On a wide torus the bulk cost of an empty patch, from mixed second differences over two-parameter families of
   patches, is the lifetime price: **0.2087 ± 0.008 per cell (65%)**. If it is outside 0.195–0.222 the reading
   "the price of a face is the price of a hole in an unbounded face" is dead.
2. Inside a large hull face (198 cells or more), patches three or more rows from every rim have the same bulk
   cost as on the wide torus, **within 0.010 per cell (70%)**: the hull's interior is a wrapped face.
3. Patches that include the rim row cost more per cell than interior patches of the same shape **by at least
   0.02 per cell (60%)**; the surplus is confined to the first two or three rows (55%).
4. Hence "0.231 is a long transient": a model built from the two measurements (interior price, rim-zone surplus,
   one fitted constant) reproduces the hull anchors at 45–108 cells within 0.05 each **(45%)** and puts the
   135-cell face at **29.19–29.24 (50% given that it fits)**.
5. Noisy hull: at 84 cells the offset from gump at ε = 0.03 is below 0.03 in absolute value **(60%)** and is
   linear in ε between 0.01 and 0.1 within errors (55%). The sampler survives small ε with usable errors (0.05 or
   better at 135 cells in under 30 core-hours): **50%**.
6. The 135-cell hull face of gump, whatever method gets there: **in 29.19–29.27 with 55%; above 29.27 with 20%;
   below 29.19 with 25%.** (29.230 is "the second difference repeats", 29.163 "the wrapped price takes over".)
7. The 120-cell tube's final value will be within 0.03 of the interim (24.47–24.53): 85%. So my 24.56 ± 0.03 will
   score as missed by about two of its errors, and the dice chain's 24.60 ± 0.07 as 1.4 errors high.

### Block 5b (PI; 11:17 UTC): the card's recorder against boom and bust

The card's own study of dying faces on gump (`research/dying2/` on its branch; another code, another machine)
tabulates the dying face's population by lag before death, with quantiles. I have seen the 63-cell torus's table
(four generations before death the 90th percentile is 1.44 of the mean population, the living 90th percentile
1.20, the median 0.34) and none of the others. If boom and bust is right:
1. The 84-cell torus and the two tubes (84, 96 cells) show a 90th percentile of at least 1.35 at lag 4, 5 or 6: 80%.
2. The hull faces (63 and 84 cells) do not: their 95th percentile stays at or below 1.25 at every lag from 2 to 12: 75%.
