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
