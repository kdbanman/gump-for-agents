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

> The cost per cell of the thinnest face, in the limit of a long face, is **PENDING_GAMMA_CELL per cell**
> (PENDING_GAMMA_SITE per site of three cells). The census values 0.115 (A 48 → 60) and 0.111 (60 → 72) are
> reproduced (0.1144(3), 0.1104(6)) and are local slopes of a ring law that is still bending at A = 108, where
> the local slope is 0.103(2).

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

PENDING_ROUTES

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
| 6 | +0.012(3) | +0.027(10) | PENDING_M6 | |
| 8 | | | PENDING_M8 | |

Also b = 20, w = 5: +0.007(7). Slopes per site between the two sizes: rings 0.410, 0.447, 0.381, 0.345, 0.337
for w = 1 … 5 against 0.337 deterministic; segments 0.372, 0.413, 0.348, 0.311, 0.306 against 0.306.

- Shallow models are **too tough**, not too weak, and the excess is a slope, not an offset: it grows with the
  size. It is not monotone in w (two layers are worse than one).
- The cells beneath a face cell look like coins at any one time: in the deterministic ring the number alive among
  the three cells beneath a face cell, given the cell's state and its number of live face neighbours, is within
  a few per cent of binomial(3, 0.398). What the coins lack is memory: where a real interior has thinned it stays
  thin for a while. (Not quantified beyond this; see "Not checked".)
- The coin density matters a little even at w = 5: at b = 20, density 0.30 gives −0.069(8), density 0.55 gives
  +0.030(7) (`python3 analyze.py life 'mod_b20_w*'`). The model is therefore closed only with the measured
  interior density as input.
- Eight layers are enough for the deterministic slab: PENDING_M12

## 5. How the thin face dies

`python3 analyze.py qsd det_b24 det_b32 seg_det_n21` **[measured]**.

- Looking back from a death, the mean face population falls steadily: 1.7, 4.1, 7.3, 10.1, 12.6, 14.8 cells at
  1 … 6 generations before the end, the same on every ring from b = 24 to 36 (segments: 1.7, 4.1, 7.0, 9.2, 11.0,
  12.5 at n = 21), about 2.4 cells = 1.8 sites per generation; the lag at which half of the living population
  (1.33 cells per site) is gone grows with the size: 3.2, 5.6, 7.9, 9.4 generations at b = 16, 24, 32, 36. The
  face does not vanish in a flash; an island shrinks from its ends at about 0.9 sites per generation per end.
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

## 7. Wider faces

PENDING_WIDER

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
- **Firewall.** A deterministic life is also cut when three adjacent interior layers are dead (looked for every
  840 generations): 72 of 376,301 lives at b = 16, 4 at b = 20, none above. The tags `det_b16`, `det_b20` and the
  first chunks of `det_b24` were run when the rule was "one empty interior layer"; the difference is below the
  statistical error at b = 16 (the census value, made with other code, is 1.7σ away).
- **Ring and segment are different laws with the same γ.** A ring must first open a gap; a segment has two from
  the start. ln τ_ring(b) − ln τ_seg(b − 3) = 1.921, 2.174, 2.370, PENDING_RS36 at b = 16, 24, 32, 36: it grows like
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
- **One layer with an effective coin density.** The conditional one-time law of the cells beneath a face cell is
  already binomial at the plain density, so there is nothing to correct at that level; the failure of M(1) is in
  time correlations, which a product measure cannot hold.
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
- **Why shallow models are too tough.** "The coins have no memory" is a reading; coins with persistence were not
  tried.
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
