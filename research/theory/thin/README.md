# The thinnest face: what its cost per cell is, and why it is not derived

2026-11-14. Tags: **[proved]**, **[exact]** (a computation with no sampling), **[measured]** (error = one standard
deviation, 1/√deaths for a lifetime, jackknife over independent chunks for a window), **[conjectured]**.
Forecasts and their scores: `PREDICTIONS.md`. Every number below comes from the chunk files in
`research/scratch/thin/<TAG>/` (not in git; curated copies in `data/`, made by `python3 collect.py`); the
command that prints it is given, and the run that makes a tag is in "Reproduce".

## 1. Verdict

**No number here is derived from the rule.** The asked-for derivation of the cost per cell of the thinnest face
cannot be had by the route proposed (noise beneath, then an exact one-dimensional computation), for three
reasons, each measured or exact:

1. *Noise is enough, but only five layers deep* **[measured]**. The rule on the top w layers over coins
   reproduces the deterministic lifetime within 0.003–0.006 from w = 5 (rings and segments, §4); w = 4 is off by
   0.02–0.12 and w ≤ 3 by 0.4–2.3, growing with size. Five layers are 15 cells per site: a state space of 2^15
   per site, with a range of two sites.
2. *The one model that can be solved exactly does not give its own constant at the sizes that can be solved*
   **[exact] + [measured]**. One layer over coins is solved exactly on segments of n ≤ 7 sites and rings of
   b ≤ 5 (§6). Its exact steps of ln τ per added site are 0.476, 0.453, 0.461 at n = 5, 6, 7; its slope at
   n = 16–24 (simulated) is 0.369 and still falling. And that model is the wrong one: its slope is 20–25% above
   gump's.
3. *The face dies by fronts* **[measured]**. A dying thin face is an island shrinking from both ends over a
   time proportional to its length (§5); the cost per site is a large-deviation rate of a front moving through a
   medium five layers deep. Nothing in it is small, and every finite-size quantity that could stand in for it
   (ring lifetimes, segment lifetimes, empty windows, the front's distance from a wall) approaches it slowly,
   with corrections of relative size 1/length (§3).

What can be said instead **[measured]**:

> The cost per cell of the thinnest face, in the limit of a long face, is **0.100 ± 0.003 per cell**
> (0.300 ± 0.008 per site of three cells). The census values 0.115 (A 48 → 60) and 0.111 (60 → 72) are
> reproduced (0.1144(3), 0.1104(6)) and are local slopes of a ring law that is still bending at A = 108, where
> the local slope is 0.103(2). A face with two free ends (a segment) shows 0.099 per cell from A = 75 on.

The error is dominated by the extrapolation, not by statistics: four different finite-size routes are given in
§3 with what each says.

## 2. The object

Gump (B45/S345 on the faces of the cubic honeycomb, `docs/AUTOMATON.md`) on the twisted torus with in-plane
periods (1,1), (0,b): the class "shortest loop squared 3" of `research/shape2`. Every cube of a {111} layer
t = i + j + k has a unique representative (0, c, t − c), c = (j − i) mod b. So a layer is a **ring of b sites
with three cells each**, X_c, Y_c, Z_c (the +x, +y, +z faces of the cube at site c); face area A = 3b.

- `python3 thin.py table` derives, from the doubled-coordinate offsets of `docs/AUTOMATON.md`, the 12 neighbours
  of each orientation as (layer shift, orientation, site shift), and checks that the answer does not depend on
  b, c, t **[exact]**. A cell has 1 + 2 neighbours in the two layers above, 6 in its own layer, 2 + 1 in the two
  layers below; site shifts are at most 2. The graph is simple for b ≥ 5 (at b = 4 a cell meets a neighbour twice).
- Along the axis the cells of a layer are ordered … Z_c, {Y_c, X_{c+1}}, Z_{c+1}, …. In everything about windows
  and walls "**site s**" means the contiguous triple {Z_s, Y_s, X_{s+1}}.
- **Deterministic slab**: m = 8 layers, two faces (layers 0 and 7), soup of density 0.4. **Model M(w)**: the rule
  on layers 0 … w − 1 (layer 0 is the face) over two layers of coins redrawn every generation with density
  102/256 = 0.3984, the measured density of the interior layers of the deterministic slab (an input, not derived).
- **Ring**: the face as it is. **Segment of n sites**: a ring of b = n + 3 sites in which the face cells of three
  sites are held dead (a wall); the face is then a strip with two free ends, and the layers beneath are untouched.
  Three sites is the least that keeps the two ends from seeing each other inside the face.
- **ln τ** is per face: τ = (faces × exposure)/deaths over the ages T0 ≤ age < 30 mean lives, T0 = 256
  generations after the soup (64 for the smallest systems). A life also ends, without a death, when the state
  repeats or when three adjacent interior layers are dead (see §8).
- **E(l)**: probability that l given consecutive sites of a living face are empty; **k(l)** = −ln E(l+1)/E(l).
  **W(x)**: in a segment, probability that the x sites next to a wall are empty; **k_wall(x)** likewise.
- **γ**: the limit of the cost per site, ln τ ≈ γ·(length) + smaller terms; cost per cell = γ/3.

## 3. The asymptotic cost: four routes

All four are local slopes that are still moving at the largest sizes reached. **[measured]** throughout.

`python3 analyze.py routes` prints everything in this section. Four quantities should each tend to γ per site as
their length grows; none has stopped moving at the largest length reached.

| route | quantity | largest length | value there | extrapolated |
|---|---|---|---|---|
| 1. rings | local slope of ln τ_ring(b) | b = 32 → 36 | 0.3103(62) | falls by about 0.007 per four sites; no stable fit |
| 2. segments | local slope of ln τ_seg(n) | n = 29 → 33 | 0.2971(13) | straight line through n ≥ 21: 0.2978(3); with a 1/n term: 0.293(3); with a ln n term: 0.288(5) |
| 3. empty windows, ring of 64 | k(l) | l = 34 | 0.3347(25) | g + a/(l + l0), l0 = 0, 1, 2 on l = 16 … 40: 0.309, 0.307, 0.305 (a = 0.8–1.0) |
| 4. front from a wall, segment of 61 | k_wall(x) | x = 30 | 0.3120(12) | g + a/x: 0.3033(3) on x = 12 … 32, 0.3031(6) on 16 … 36 (a = 0.30); g + a/√x fits worse and its g moves with the range (0.280, 0.285, 0.288) |

Local slopes, per site (per cell in brackets):

| length | rings (A = 3b) | segments (A = 3n) | windows k(l) | wall k_wall(x) |
|---|---|---|---|---|
| ≈ 18 | 0.3432(10) [0.1144] | 0.3018(5) [0.1006] at 19 | 0.3554(1) | 0.3199(2) |
| ≈ 22 | 0.3312(18) [0.1104] | 0.2990(7) [0.0997] at 23 | 0.3469(3) | 0.3170(4) |
| ≈ 26 | 0.3259(26) [0.1086] | 0.2967(9) [0.0989] at 27 | 0.3411(7) | 0.3156(6) |
| ≈ 30 | 0.3188(40) [0.1063] | 0.2971(13) [0.0990] at 31 | 0.3372(12) | 0.3120(12) |
| ≈ 34 | 0.3103(62) [0.1034] | (n = 37, 45: see below) | 0.3347(25) | 0.3151(26) |

SEGMORE

- The segment slope is the lowest and has been flat at 0.297 since n ≈ 25 (0.3093, 0.3018, 0.2990, 0.2967, 0.2971
  at n = 15, 19, 23, 27, 31); the three others are above it and falling towards 0.30–0.31.
- The front's distance from a wall is the cleanest: one front, nothing to nucleate, no deaths needed, and the
  form g + a/x gives the same g on every range of x. It says W(x) ∝ x^(−0.30) e^(−0.303 x).
- **Reading [conjectured].** One γ, the price per site of pushing a front back. A window needs a gap to be born
  and two fronts (hence a larger power: E(l) ∝ l^(−0.9) e^(−γ l)); a ring needs the same and dies when the island
  left is gone; a segment needs only its two wall fronts to meet, which for independent fronts with the law of
  route 4 gives ln τ_seg ≈ γ n − 0.4 ln n: a slope *below* γ, rising towards it, after the fall from above that
  the small sizes show. That would put the flat 0.297 at n = 25–33 at the turn of the curve and γ at 0.303. It is
  not established: the alternative that all four keep falling to about 0.29 is excluded only if the form g + a/x
  of route 4 is right.
- **Value.** γ = **0.300 ± 0.008 per site, 0.100 ± 0.003 per cell**: the interval runs from the segment fits with
  a correction term (0.293) to the window extrapolation (0.309), and the two routes with stable fits (segments,
  straight: 0.298; wall: 0.303) sit inside it.
- The static formulation fails as a short cut **[measured]**: ln τ_ring(b) + ln E(b − s) is not constant for any
  shift s (`python3 analyze.py static win_det_b64 'det_b[0-9]*'`): for s = 0 it falls from 0.77 at b = 16 to 0.41
  at b = 36. The ring's lifetime grows more slowly than 1/E(b), by a factor b^0.45 over this range.

## 4. Noise is enough from five layers

`python3 analyze.py life 'mod_b16_w*'`, `… 'mod_b24_w*'`, `… 'seg_m?_n13'`, `… 'seg_m?_n21'`. Model M(w) minus the
deterministic value of ln τ **[measured]**:

| w | ring b = 16 | ring b = 24 | segment n = 13 | segment n = 21 |
|---|---|---|---|---|
| 1 | +1.286(3) | +1.868(13) | +0.805(2) | +1.337(3) |
| 2 | +1.382(4) | +2.258(20) | +1.132(2) | +1.988(4) |
| 3 | +0.495(3) | +0.845(13) | +0.366(2) | +0.708(3) |
| 4 | +0.049(3) | +0.115(12) | +0.018(2) | +0.058(2) |
| 5 | +0.006(3) | +0.003(12) | −0.003(2) | +0.002(2) |
| 6 | +0.012(3) | +0.027(10) | +0.013(2) | |
| 8 | | | +0.004(2) | |

Also b = 20, w = 5: +0.007(7). Slopes per site between the two sizes: rings 0.410, 0.447, 0.381, 0.345, 0.337
for w = 1 … 5 against 0.337 deterministic; segments 0.372, 0.413, 0.348, 0.311, 0.306 against 0.306.

- Shallow models are **too tough**, not too weak, and the excess is a slope, not an offset: it grows with the
  size. It is not monotone in w (two layers are worse than one).
- Their faces are too dense and too quiet (`python3 analyze.py qsd mod_b24_w1` …): the face holds 0.5075, 0.4703,
  0.4494, 0.4448, 0.4442, 0.4440 of its cells for w = 1 … 6 against 0.4437 in the deterministic ring, and the
  variance of its population is 38.4, 39.9, 43.7, 46.3, 46.6, 46.5 against 46.6 (b = 24).
- What coins cannot do (`python3 under.py`, deterministic ring b = 48) **[measured]**: the layers beneath answer
  to the face. Beneath the middle of a gap of 4 empty face sites, layers 1 and 2 hold 0.26 and 0.36 of their
  cells (0.413 and 0.394 on average); beneath a gap of 8, 0.32–0.33 and 0.38–0.39; from layer 3 down nothing is seen
  (within 0.005). Four generations before a gap of 8 is seen, layers 1, 2, 3 at its middle are already thin
  (0.32, 0.36, 0.38); layer 4 is not. The number m of live cells among the three beneath a face cell has mean
  0.88 under a dead cell with no live face neighbour and 1.42 under a dead cell with six (binomial at the
  interior density: 1.19). So a gap of the face thins what is beneath it, which makes the gap harder to close;
  over coins the support under a gap is always fresh. It fits a depth of about five: the response reaches three
  layers, and each layer of the rule reads two more.
- The coin density matters a little even at w = 5: at b = 20, density 0.30 gives −0.069(8), density 0.55 gives
  +0.030(7) (`python3 analyze.py life 'mod_b20_w*'`). The model is therefore closed only with the measured
  interior density as input.
- From five layers on the residue is 0.003–0.03 and not monotone (w = 6 is consistently 0.012–0.027 too tough).
- Eight layers are enough for the deterministic slab (`python3 analyze.py life det12_b16 det_b16`, …): with
  twelve, ln τ is 8.6504(17) against 8.6470(16) on the ring b = 16, 6.7277(9) against 6.7262(14) on the segment
  n = 13, 9.1768(20) against 9.1708(15) at n = 21: +0.002 to +0.006, a slope change of +0.0006(4) per site.

## 5. How the thin face dies

`python3 analyze.py qsd det_b24 det_b32 seg_det_n21` **[measured]**.

- Looking back from a death, the mean face population falls steadily: 1.7, 4.1, 7.3, 10.1, 12.6, 14.8 cells at
  1 … 6 generations before the end, the same on every ring from b = 20 to 36 (segments: 1.7, 4.1, 7.0, 9.2, 11.0,
  12.5 at n = 21), about 2.7 cells = 2 sites per generation; the lag at which half of the living population
  (1.33 cells per site) is gone grows in proportion to the size: 4.2, 5.4, 6.6, 7.8, 8.9, 10.4 generations at
  b = 16, 20, …, 36 (0.29 per site), and 3.7, 6.6, 9.8, 11.5 at n = 13, 21, 29, 33 for segments (0.39 per site).
  The face does not vanish in a flash: an island shrinks from its ends, at 0.85–1 site per generation per end
  on a ring.
- The last step is the same at every size: 58.6% of deaths are from one live cell, 24.5% from two, 10% from
  three, 4% from four.
- In the living state the face holds 0.4437 of its cells (interior layers 0.397); a segment's face 0.371 of the
  cells between its walls, the deficit being at the ends.
- Windows on a ring factorise: E_b(l) ≈ E_∞(l)·χ(b − l). The last stretch is universal: k_b(b − 2) = 1.33,
  k_b(b − 3) = 1.02–1.03, k_b(b − 4) = 0.83, k_b(b − 5) = 0.71, k_b(b − 6) = 0.62 at b = 24, 28, 32, 36 alike
  (`python3 analyze.py win det_b32`), and the excess over E_∞ is still +0.026 in k at b − l = 14 and +0.003 at
  b − l = 22. Emptying the last fourteen sites of an island costs more than emptying fourteen sites of a long
  face. The same holds for the front's distance from a wall (k_wall at x = 9: 0.477, 0.387, 0.355, 0.343, 0.336 at
  n = 17, 21, 25, 29, 61).

## 6. What is exact

`python3 sweep.py table` (rings 5–6, segments 2–8; n = 8 needs 8.6 GB and over an hour and was not run),
`python3 sweep.py seq`, `python3 exact1.py 5`.

For M(1) the kernel is a product over the triples T_c = {X_{c+1}, Y_{c−1}, Z_c}: the three cells of a triple share
their two-plus-one cells beneath pairwise through the three coins X_c, Y_c, Z_c of the layer beneath and have one
private coin each two layers down; cells of different triples share no coin **[proved]** (`exact1.triples`
asserts it from the neighbour table). The quasi-stationary law and its death rate are then found by power
iteration, the kernel applied triple by triple **[exact]**:

| system | ln τ (exact) | simulation of the same model |
|---|---|---|
| ring b = 5 | 3.967199 (two independent codes) | 3.96708(69) |
| segment n = 2 … 7 | 2.453108, 2.755960, 3.716420, 4.192750, 4.646105, 5.107427 | 4.1927(3), 4.6456(3), 5.1079(4) at n = 5, 6, 7 |

Steps per added site: 0.303, 0.960, 0.476, 0.453, 0.461. Simulated continuation (`python3 analyze.py life
'seg_m1_n*'`): 0.437 (7 → 8), 0.410 (8 → 10), 0.391 (10 → 12), 0.382, 0.376 (13 → 16), 0.371 (16 → 20), 0.368
(20 → 24). So **the exact numbers are numbers about M(1) on short segments, not about its constant, and not about
gump**: M(1)'s slope at n ≈ 20 is 0.37 per site (0.123 per cell) and falling, gump's is 0.30.

### 6b. The face alone, with the right one-generation statistics **[exact] + [measured]**

`python3 pca.py table tab_det_b32 det32; python3 pca.py exact det32 6; python3 analyze.py life 'pca_det32_n*'`.

The closure one step beyond coins: forget the layers beneath, and let every face cell be alive next with the
probability p(s, k) that the deterministic system shows for a face cell in state s with k live face neighbours
(14 numbers, measured to 2 × 10⁻⁵ on the ring b = 32; b = 16 gives the same to 2 × 10⁻⁴), independently of the other
cells. Against independent coins beneath, p differs little where the face is thin (birth with k = 1: 0.0628 against
0.0633; with k = 2: 0.3515 against 0.3498) and much where it is dense (birth with k = 4: 0.571 against 0.650;
survival with k = 4: 0.578 against 0.650). The kernel is a product over cells, so the same exact machinery applies:

| segment n | 5 | 6 | 7 | 8 | 13 | 21 | slope 13 → 21 |
|---|---|---|---|---|---|---|---|
| deterministic | 3.8671(9) | 4.2795(8) | 4.6767(5) | 5.0515(6) | 6.7262(14) | 9.1708(15) | 0.3056 |
| face-only automaton, measured p | 3.977059 exact; 3.9774(9) | 4.441084 exact; 4.4420(7) | | | 7.1483(21) | 9.8572(52) | 0.3386 |
| one layer over coins, M(1) | 4.192750 exact | 4.646105 exact | 5.107427 exact | 5.5453(4) | 7.5311(8) | 10.5080(26) | 0.3721 |

The automaton has the face's one-generation statistics right by construction and is still 11% too tough in
slope (M(1): 22%). Its living face is denser (0.401 of the cells of a 21-site segment against 0.371) and quieter
(variance of the population 39 against 46), and it collapses more slowly (looking back from a death: 1.4, 2.8,
4.5, 6.4 cells against 1.7, 4.1, 7.0, 9.2). What is missing is that cells fail together: face cells share the
cells beneath them, and those stay thin for several generations (§4). **The one-generation statistics of the
face do not fix its lifetime.** (The deterministic values at n ≤ 6 are themselves rough: there the hazard depends
on age, 1% of lives end in a repeating state and the two faces often die together; see `python3 run.py stats
'seg_det_n[5-9]'`.)

## 7. Wider faces

**[measured]** for the torus (1,2),(0,b), shortest loop squared 7 (`ringk.c`; `python3 analyze.py life 'det_k2_b*'`):

PENDING_K2

What the same method says as the face widens, and what it would take:

- The tori (1,k),(0,b) are rings of b sites of three cells for every k (the site index is j − k·i mod b; shifts
  reach k + 1 sites), so everything of §3 can be asked of them; `ringk.c` steps k = 1 … 5 (shortest loop squared
  3, 7, 13, 21, 31), validated cell by cell. The census's 0.141 belongs to shortest loop squared 4, which is not
  of this form (two cubes per ring position) and was not stepped here.
- The census slopes of wider tori are local slopes of ring laws too, and should come down with length as the
  thin torus's did (0.115 → 0.103 between A = 54 and 102, limit 0.100). How much of the rise 0.10 → 0.19 → 0.21
  with the loop is asymptotic and how much is the ring's bend is not known.
- Reading **[conjectured]**: the cost per cell is the price of pushing a front line back by one cell, and a longer
  front line is harder to push because its cells hold each other up sideways; on the thinnest torus the line is
  one site long and "sideways" is the face's own tail. The saturation near 0.21 would then be the price per cell
  for a straight front line in a wide face, or the point where a wide face stops dying by fronts at all.
- **To reach the wide face by derivation** one would need (i) a closure, and the cheapest one that works is five
  layers over coins, with the interior density as an input; (ii) the large-deviation rate of a front line in that
  model, a two-dimensional problem with 15 cells per site. Exact enumeration is out by many orders: even the
  one-layer model on the thinnest torus needs more than twenty sites, 2^60 states. A rate of this kind can be
  *computed* without waiting for deaths by sampling the tilted front process (cloning), on the deterministic
  system itself; that would extend the measurements to faces whose lifetime cannot be simulated, but it is a
  measurement, not a derivation. No small parameter was found that would make one possible: the cost per cell is
  0.1–0.2 nats, the events behind it involve three to five layers and tens of sites, and the two simplest
  closures (coins beneath: +22% in slope; the face's own one-generation statistics: +11%) fail in the same
  direction for a reason that is measured (§4, §6b).

## 8. Subtle points

- **A life that stops dying.** In the deterministic segment of 13 sites one lane of sixteen entered a state of the
  whole slab that repeats with a period not dividing 840 and kept both faces alive for 3.6 × 10⁷ generations; the
  first binary tested for repetition only every 840 generations against the state 840 earlier, missed it, and the
  lane's exposure raised ln τ from 6.726 to 6.810. That wrong value stood for an hour (it made the segment law
  look straight, and the five-layer model look 0.087 too weak) and was found because the two chunks of the tag
  disagreed by 100σ. Now: (i) `ring.c` compares the state with a snapshot every generation (snapshots at ages
  16, 32, 64, …), so any period is found; (ii) `run.py lntau` uses only ages below 30 mean lives and `run.py
  stats` reports exposure beyond (none in any tag in use; the bad chunk is kept as
  `seg_det_n13/stuck_c1.txt`); (iii) `validate_dump` re-derives every end of a life. In a model with w ≥ 4
  the same happens when layers 1 … w − 1 all die: a cell of layer w − 1 sees only three coins and B needs four,
  so the face runs alone for ever (2–17 such lives per 10⁵ deaths at b = 16; they are cut at the snapshot).
  With w ≥ 6 the same happens behind any three adjacent dead layers while deeper layers flicker on with the coins:
  the first runs of M(6) and M(8) on the 13-site segment ended with every lane stuck. The firewall rule (next
  point) now applies to the models too, and those two tags were rerun; the model tags with w = 4, 5, 6 run before
  that have no exposure beyond 30 mean lives.
- **Firewall.** A deterministic life is also cut when three adjacent interior layers are dead (looked for every
  840 generations): 72 of 376,301 lives at b = 16, 4 at b = 20, none above. The tags `det_b16`, `det_b20` and the
  first chunks of `det_b24` were run when the rule was "one empty interior layer"; the difference is below the
  statistical error at b = 16 (the census value, made with other code, is 1.7σ away).
- **Ring and segment are different laws with the same γ.** A ring must first open a gap; a segment has two from
  the start. ln τ_ring(b) − ln τ_seg(b − 3) = 1.921, 2.174, 2.370, 2.42(2) at b = 16, 24, 32, 36: it grows like
  0.65 ln b. Reading a cost per cell off rings at A ≤ 72 overstates it by 10–15%.
- **Left and right ends of a segment are mirror images** (the reflection x ↔ y maps site c to −c), and the
  measured k_wall agree on the two sides from x = 2 on; at x = 1 they differ (0.410, 0.462) because the triple
  {Z_s, Y_s, X_{s+1}} is not mirror-symmetric.
- **T0.** Hazards by age class are flat from age 64 on in every tag looked at (`python3 run.py stats TAG`, columns
  "by age", for the classes above T0); T0 = 256 is safe, and so is 64 for the smallest systems.
- **Coins.** One layer of the rule sees two layers of coins (2 + 1 cells), so "over two layers of coins" is the
  whole of what M(w) needs. Bernoulli words are made with a 16-bit density; `validate_dump` checks the density and
  the correlations of the dumped coins in time, between cells and between lanes.

## 9. Methods that failed, and why

- **Fixed-age transfer matrices** (the counting line's c_k): they give the probability that the face is empty at
  generation k from the soup. That is an entropy of initial conditions; it depends on the soup's density and its
  decay rate in A is not the steady one (their claims 12, 13, 19). Nothing in it sees a front.
- **Local structure theory / cluster closures of the quasi-stationary law.** They reproduce the short-window
  costs (k(2) = 0.55, k(4) = 0.49), which are far from the limit: k(l) is still 0.335 at l = 34. The constant
  lives at the scale of tens of sites.
- **A front table.** Pool the one-generation moves of the front, find the root of the tilted moment (Lundberg).
  With the moves measured in the living state the root reproduces k(l) by construction; it is the same
  information as E(l), not a derivation.
- **One layer over coins of another density.** No single density can be right: the support beneath a face cell
  depends on what the face is doing there (§4: mean 0.88 to 1.42 live cells of three). The next closure, a
  face-only probabilistic automaton whose birth and survival probabilities p(state, live face neighbours) are
  read from the deterministic system, was not run (see "Not checked"); its fourteen numbers would still be
  measured, not derived.
- **Exact enumeration to the straight part.** The sweep costs 2^(3n+5) numbers for a segment of n sites of M(1)
  (n ≤ 8), 2^(3b+10) for a ring (b ≤ 6); M(2) reaches n = 3. M(1) needs n > 20 to be within 3% of its own slope.
- **A tilted front chain** (a window of K sites behind the front, the rest replaced by the living state): not
  implemented. K ≤ 6 is feasible for M(1); the end-game data of §5 (corrections still 0.026 at fourteen sites)
  say it would not have converged.

## 10. Not checked

- **Whether the four routes of §3 have one limit.** They are ordered and separate at every size reached; that
  they meet is the front picture's expectation **[conjectured]**, not a measurement.
- **Anything beyond 45 sites by lifetime.** Rings of b = 40 and 48 (forecast F2) were not run: a ring of 48 sites
  lives e^19 generations.
- **The form of the corrections.** Powers of the length, logarithms and stretched exponentials fit equally; none
  is derived. The quoted error is the spread between them.
- **A face-only closure.** §4 measures how the layers beneath answer to the face; whether a probabilistic
  automaton on the face alone, with the measured one-step probabilities p(state, live face neighbours),
  reproduces the lifetimes was not tried. Nor were coins with persistence in time.
- **The coin density** was varied only at b = 20, w = 5; whether its effect grows with size is unknown.
- **Models deeper than six layers on rings**, and deeper than eight anywhere.
- **Statistical errors** are 1/√deaths. Over all lifetime tags the scatter between chunks has χ² = 186 on 162
  degrees of freedom: the quoted errors may be about 7% too small.
- **Old firewall rule** in `det_b16`, `det_b20` (§8): not rerun.
- **Other soups.** Every life starts from density 0.4; hazards are flat in age, so no dependence is expected, and
  none was looked for.
- **The engine** was compared with `ring.c` on populations only (five sizes, up to 3,000 generations); lifetimes
  were compared with the census (other code) at b = 16, 20, 24 and for the torus (1,2).
- **The random generator** (xoshiro256++, one stream per lane) was checked on the dumped coins, not by repeating
  a lifetime with another generator.
- **Exact:** the ring of six sites and the segment of eight were not run. The two exact codes share
  `exact1.triple_table` (the 8-outcome table of one triple); it is checked only through the agreement with
  simulation at five sizes.
- **The torus with shortest loop squared 4** (the census's 0.141) is not of the form (1,k),(0,b) and no code here
  steps it. The tori k = 3, 4, 5 are validated cell by cell but no lifetime was run.

## 11. Reproduce

```
python3 thin.py table                 # the neighbour table, derived
python3 thin.py oracle 16 8 300       # reference stepper = reference/oracle.py, every cell (also: 11 8 300; 12 5 200; k = 2, 3, 4)
python3 run.py validate               # ring.c, ringk.c against the reference stepper and the engine: ALL OK (2 min)
python3 run.py stats 'seg_det_n*'     # one line per tag: deaths, ln tau, ends without death, hazard by age class
python3 analyze.py routes             # §3: the four routes side by side, with the fits
python3 analyze.py life 'det_b[0-9]*' # one family per call (slopes are between successive tags)
python3 analyze.py win win_det_b64 46 ; python3 analyze.py wall seg_det_n61 ; python3 analyze.py qsd det_b32
python3 analyze.py static win_det_b64 'det_b[0-9]*'
python3 sweep.py seq ; python3 exact1.py 5
python3 collect.py                    # data/lifetimes.json, data/windows.json from the chunk files
```

`runs.sh` lists the run behind every tag. Validation, in full: (i) `thin.py oracle` embeds b copies of the slab in
the cubic b-torus and compares every cell of every copy with `reference/oracle.py`; (ii) `validate_dump` takes a
dump of every lane at every generation and checks that each next state is the reference stepper's image of the
one before (walls included), and re-derives every end of a life (deaths, repeating states, firewalls) and the
exposure by the rules stated at the head of `ring.c`, on 30 configurations including small ones where lives end
in every way; (iii) `validate_engine` compares populations with the Rust engine on the cubic torus; (iv) the
simulated one-layer model agrees with the exact solution at five sizes (§6).

Files: `thin.py` (geometry, reference stepper), `ring.c` (packed stepper for k = 1, walls, statistics),
`ringk.c` (the same for (1,k), no walls or windows), `nbr.h`, `nbrk.h` (generated by `thin.py header`), `run.py`
(driver, validation, estimator), `analyze.py`, `exact1.py`, `sweep.py` + `sweep.c` (exact one-layer model),
`collect.py`, `runs.sh`, `PREDICTIONS.md`, `data/`.
