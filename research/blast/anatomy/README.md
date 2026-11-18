# research/blast/anatomy: single deaths of a face, in space and time, shape against shape

Agent `anatomy` of the blast of 2026-11-18. Question: what is the cheapest route to an empty face for each shape
(wide wrapped face, tube, rimmed hull face), looked at one death at a time. Everything here is brute force at
45 to 84 cells with one stepper (`an.c`), validated against `reference/oracle.py` on every vessel used.
All times are generations; lengths are in hexagonal lattice units (1 unit = 2 kagome nearest-neighbour spacings;
the automaton's speed limit in a face is 1 unit per generation). Labels: **[measured]**, **[conjectured]**.

## The answer in four sentences

1. **A wrapped face (wide torus or tube) dies by boom and bust, not by a hole or a front** [measured, 48 to 75
   cells]. In 51–60% of deaths at least half of all the cells of the face die in one generation (in 84% at least
   24 of 63; the distribution has one hump): in a single generation the face and the layer beneath fill to about
   three quarters (33 → 48.5 of 63 cells), every live cell is then overcrowded, almost nothing is born, about 12
   scattered cells are left, and those starve within a few generations. From the last generation with a normal
   population to the first empty one takes 6 generations (3–10).
2. **A rimmed hull face dies differently: a tilted fade of about 10 generations (5–16), by starvation** [measured,
   45, 63 and 84 cells]. Only 1.6% of its deaths contain such a fall. A plane fitted to the last-alive times beats 95%
   of shuffles in 77% of deaths, with a speed of 0.6 units per generation.
3. **There is no band-first class on tubes** [measured]: a strip of width 1 right round the girth is finally empty
   4 generations before the last cell in 48–53% of deaths (loop² 12), no more often than a compact patch of the
   same 12 cells (54–58%) or than the strips of the wide torus (57%). The PI's reading (9–12% against under 5%) is
   refuted in both numbers; so were my own forecasts of a sweep.
4. **Where the shapes part, in 1/τ = ν(p)·q(p) at 63 cells** [measured]: a hull face reaches a quarter of its
   population 2.1 times as often as the wide torus, reaches 4 cells exactly as often (ratio e^(+0.035±0.01)), and
   from there dies 0.6 times as often (q(4) = 0.18 against 0.30): the whole 0.47 of ln τ is in the last four cells.
   The end-game does not depend on size: q(4) = 0.197, 0.183, 0.197 on hull faces of 45, 63, 84 cells and
   0.326, 0.302, 0.287 on wrapped faces of 48, 63, 75, so it is a constant factor and cannot be the source of
   the hull's higher price per cell.
   A loop²-9 tube against the wide torus is the opposite: all of its 0.31 is in the descent from 28 to 16 cells,
   none in the end-game.

## Vessels, lifetimes (check of the stepper against the anchors)

`sh run1.sh; sh run2.sh; sh run3.sh` (about 5, 2 and 20 minutes on one idle core; run3.sh also starts an 84-cell
torus, t84, which had not finished when this was written and is not used). ln τ_face = ln(faces·exposure/deaths).

| run | vessel | cells | deaths | ln τ_face here | anchor |
|---|---|---:|---:|---|---|
| t48 | torus (4,0),(0,4) | 48 | 13,422 | 9.9383 ± 0.0086 | 9.9251 ± 0.0004 |
| tube54 | (1,4),(0,18), loop² 12, 4.5 long | 54 | 9,604 | 11.1913 ± 0.0102 | 11.1935 ± 0.0030 (research/wrap/data/runs.csv) |
| tube60 | (1,8),(0,20), loop² 12, 5 long | 60 | 8,223 | 12.4168 ± 0.0110 | 12.4230 ± 0.0025 (same file) |
| t63 | torus (1,4),(0,21), loops² 21 | 63 | 7,899 | 13.1547 ± 0.0113 | 13.1622 ± 0.0007 |
| tube63 | (1,6),(0,21), loop² 9, 6.1 long | 63 | 8,023 | 12.8448 ± 0.0112 | none; 7,811 lives ended by a transverse firewall instead |
| t75 | torus (1,9),(0,25), loops² 19, 25 | 75 | 1,144 | 15.6501 ± 0.0296 | 15.6442 ± 0.0030 |
| h45 | hull radius 9 | 45 | 14,365 | 9.8142 ± 0.0083 | 9.819 |
| h63 | hull radius 11 | 63 | 7,390 | 13.6205 ± 0.0116 | 13.633 |
| h84 | hull radius 13 | 84 | 117 | 18.0636 ± 0.0925 | 18.141 ± 0.005 |

There is no loop²-12 lattice at 63 cells; the PI's "63" is answered at 54 and 60. The loop²-9 tube has a second
way to end (the chaos is cut right across: three empty transverse layers) as frequent as face death; its ln τ
is therefore not comparable with the anchors' tubes, and I use it only as the extreme case.

## 1. The last-alive field T_i of single deaths  (`python3 deaths.py VESSEL RUN 3000 100` → `out/RUN.txt`)

T_i = last generation at which face cell i was alive, relative to the first empty generation (window 128).
Plane: T = a + g·x (wrapped faces: positions unwrapped round the best centre cell, the same maximisation in the
null); null = T shuffled over the cells, 100 shuffles per death; first 3,000 deaths of each run. "Baseline" = the
same field built 100 generations before the death, i.e. on a living face. Hull fits use the 54 cells whose
stationary occupancy is ≥ 0.4 (the 3 corner cells, 0.175, and their 6 neighbours, 0.303, are rarely alive at all
and would fake a cone).

| | t63 | tube54 | tube60 | tube63 (loop² 9) | h63 |
|---|---|---|---|---|---|
| generations from last P ≥ 0.476·A to death, median (10–90%) | 6 (3–10) | 5 (3–10) | 5 (3–10) | 6 (4–11) | 10 (5–16) |
| mean T | −6.00 | −5.54 | −5.77 | −6.15 | −8.30 |
| s.d. of T over the cells of one death, median | 1.85 | 1.81 | 1.82 | 1.95 | 3.28 |
| plane beats 95% of shuffles (expected 0.05) | 0.325 | 0.311 | 0.325 | 0.464 | 0.767 |
| the same on the living face (baseline) | 0.119 | 0.139 | 0.155 | 0.171 | 0.334 |
| median R² of the plane (shuffles) | 0.151 (0.115) | 0.169 (0.131) | 0.152 (0.114) | 0.179 (0.120) | 0.241 (0.037) |
| speed 1/abs(g) where the plane beats the null, median (quartiles) | 1.00 (0.76–1.31) | 1.03 (0.77–1.39) | 1.22 (0.94–1.64) | 1.14 (0.86–1.50) | 0.60 (0.41–0.85) |
| cone (hole from a point / remnant to a point) beats 95% of shuffles | 0.21 / 0.27 | 0.25 / 0.31 | 0.25 / 0.29 | 0.42 / 0.42 | 0.74 / 0.77 |
| remnant cone fits better than the plane | 0.088 | 0.120 | 0.076 | 0.094 | 0.498 |

[measured] On wrapped faces the field is **flat with noise** (a flash): two thirds of deaths are no more
plane-like than a shuffle, and where a tilt is detected its speed is the speed limit (1 unit per generation),
which is what a timing jitter of a simultaneous event looks like. On the hull face the field is **tilted** in
three deaths out of four, at 0.6 units per generation: the 5-unit face is crossed in about 8 generations. Neither a
hole growing from a point nor a remnant shrinking to a point is preferred over a plane on any shape.
The robust fields: T3 (third-last time alive) gives 0.156 (t63) and 0.681 (h63) for the plane; TP (last time the
7-cell patch was non-empty) is smoothed by construction and beats shuffles trivially (0.925, 0.884): not evidence.
Fourier shares on tubes (loop² 12): the lowest mode along the tube carries 0.085–0.087 of the variance of T, the
lowest mode round the girth 0.063–0.067, shuffles 0.034–0.038; on the wide torus the three lowest modes 0.070 each
(0.032). Lopsidedness of the living set on the way down (lowest modes or dipole, 1 = random subset): t63 1.2 at
P = 32, 2.0 at P = 8 (living face 1.34); h63 1.8 at 32, 4.2 at 8 (living face 1.71).

## 2. Boom and bust  (`python3 crash.py VESSEL RUN` → `out/RUN_crash.txt`)

| | t48 | tube54 | tube60 | t63 | tube63 | t75 | h45 | h63 | h84 |
|---|---|---|---|---|---|---|---|---|---|
| deaths with a one-generation fall of ≥ half the face | 0.572 | 0.565 | 0.567 | 0.590 | 0.512 | 0.601 | 0.022 | 0.016 | 0 of 117 |
| the same in a 10-generation window of the living face | 0.0075 | 0.0050 | 0.0022 | 0.0015 | 0.0017 | 0.0009 | 0.0001 | 0.0000 | 0.0000 |
| largest one-generation fall, median (cells) | 25 | 28 | 31 | 32 | 31 | 39 | 10 | 13 | 16 |

[measured, t63, the 4,659 deaths with such a fall] Population before the fall 48.5 (10–90%: 46–52; the stationary
probability of P ≥ 46 is 0.0024, mean 32.6, s.d. 4.94), after it 11.6 (8–15); births in that generation 1.9; of
the cells that die in it 80.9% have ≥ 6 of the 8 neighbours I recorded alive (overcrowded for certain), 18.5%
have 5 (overcrowded if the ninth, unrecorded neighbour lives), 0.6% fewer. The other wrapped faces give the same
numbers (tube60: 46.4 → 10.8, 81.2% + 18.2%). A fall of half the face is not itself rare (about 1.5·10⁻⁴ per
generation on t63, from 12 such falls in 7,899 control windows, so ± 30%); roughly one in 130 is fatal
(0.59·e^(−13.155) / 1.5·10⁻⁴).
**The boom is one generation long** (`out/aligned_fall.txt`; populations aligned on the fall, t63, same 4,659
deaths) [measured]:

| generations from the fall | −8 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
|---|---|---|---|---|---|---|---|---|---|---|
| face (63 cells; stationary 32.6) | 32.5 | 33.8 | 31.0 | 33.2 | **48.5** | 11.6 | 5.5 | 2.6 | 1.6 | 1.4 |
| layer beneath (63 cells; stationary 27.4) | 27.2 | 29.0 | 26.9 | 25.2 | **39.9** | 9.8 | 10.1 | 11.6 | 14.7 | 19.4 |

Two generations before the fall the face looks normal; then 15 more cells than usual are born at once in the face
and 15 in the layer beneath, and the next generation both layers lose three quarters. The layer beneath is refilled
from below within a few generations; the face has nothing above it and dies a median 4 generations after the fall
(10–90%: 2–8). tube60 and t75 give the same table (46.4 → 10.8 of 60; 57.5 → 14.0 of 75). I recorded only two
layers, so how deep the surge reaches is not known.

What is unusual two generations before the fall is not the number of live cells but their arrangement
(`out/primed.txt`, t63) [measured]: with 33.2 cells alive (normal), 27.9 of them have 3–5 of their 8 recorded
neighbours alive (normally 22.0) and 18.8 dead cells have 4–5 (normally 12.6). The face is evenly spread: hardly
any cell is overcrowded or starved, so nearly all survive and nearly every gap is filled, in one step.

One class, not two (`out/fall_hist.txt`) [measured]: on t63 the largest one-generation fall is unimodal round
32–36 cells; 90% of deaths contain a fall of ≥ 20 cells and 84% one of ≥ 24 (living face: 6.4% and 2.0% of
10-generation windows); only 7% of deaths have no fall above 16. "Half the face" cuts this one hump in the middle.
On h63 the hump sits at 12–16 cells (living face 8–12); 10% of deaths contain a fall of ≥ 24.

A crude split of the price (`python3 split.py` → `out/split.txt`) [measured, small counts; tori and tubes mixed]:
falls of ≥ half the face happen in the living face at ln(rate per generation) = −7.20 ± 0.10 (48 cells, 101
falls), −7.60 ± 0.14 (54), −8.42 ± 0.24 (60), −8.80 ± 0.29 (63, 12 falls); the share of them that is fatal is
e^−3.30, e^−4.16, e^−4.56, e^−4.88. From 48 to 63 cells each factor falls by about 0.107 per cell: half of the
0.2145 per cell is the rarity of the fall, half the rarity of its leftover (8 of 48, 12 of 63, 14 of 75 cells)
failing to rebuild. The end-game proper is not where the area enters: q(1) = 0.872, 0.862, 0.868 and
q(4) = 0.326, 0.302, 0.287 at 48, 63, 75 cells.

Not an artefact of a slab of 8 layers [measured]: the same 48-cell torus on a slab of 12 layers
(`python3 validate.py slab 4 0 4 1100 12`, then `an slab_4_0_4_L12.bin run 41 0.4 300000 1000 23 128 100000 t48L12`,
`python3 crash.py slab_4_0_4_L12 t48L12`): ln τ 9.9208 ± 0.0086, share with a fall of half the face 0.563
(8 layers: 9.9383, 0.572), 37.3 → 8.4 cells in both.

Cross-check on another agent's stepper [measured]: the natural-death records of `split-slab` for the same 48-cell
torus (`research/scratch/blast/split-slab/paths_test.txt`, 1,268 deaths, read at 03:55 UTC; its populations by lag)
give a share of 0.565 ± 0.014 with a one-generation fall of ≥ 24 cells in the last 10 generations; mine is 0.572.

On the hull face deaths are starvation: of the cells dying in the last 8 generations 36% are starved for certain
(living face 17%), 24% overcrowded for certain (33%); on t63 the split is 24% / 44% (living face 11% / 46%).
The layer beneath the face is depleted too but never emptied: its mean population is 15.5 (t63) and 19.0 (h63) at
its lowest, against 27.4 and 27.8.

**Why the rim closes this route** (`python3 overfull.py` → `out/overfull.txt`; living faces: lags 41–127 of the
death records) [measured]. One generation after a generation with P ≥ 46:

| | generations found | mean P one generation later (10–90%) | share that fall to P ≤ 15 |
|---|---:|---|---|
| t63 | 1,609 | 22.9 (18–28) | 0.027 ± 0.004 (0.094 ± 0.016 after P ≥ 48) |
| h63 | 1,040 | 31.5 (25–38) | 0 of 1,040 (0 of 207 after P ≥ 48) |

On the hull face, a live cell of the rim line survives an over-full generation (P ≥ 44) with probability 0.69
(corner 0.81), a live cell inside (depth 1, 2, 3) with 0.42–0.43, and the rim line is the fuller part to begin with
(0.79 occupied against 0.68–0.72). The rim line is 33 of the 63 cells. The over-full state itself is only 1.6 times
rarer on the hull face (P(P ≥ 46) = 0.0015 against 0.0024).

## 3. The band test asked for by the PI  (same command; the PI's forecast is block 1 item 1 of ../PREDICTIONS.md)

Strip = all face cells whose coordinate across the shortest loop lies in [z0, z0 + 1); lead = generations between
the strip's last living generation and the face's; per death the best strip. Control with the same number of
cells: the best compact patch (the m cells nearest some cell). On the wide torus the best strip over its three
shortest loops.

| share of deaths with lead ≥ | tube54 band / patch (12 cells) | tube60 band / patch (12) | tube63 loop² 9 band / patch (11) | t63 strips / patch (16) |
|---|---|---|---|---|
| 2 | 0.927 / 0.962 | 0.949 / 0.974 | 0.973 / 0.990 | 0.968 / 0.956 |
| 4 | 0.485 ± 0.005 / 0.543 | 0.526 ± 0.006 / 0.576 | 0.650 / 0.682 | 0.572 ± 0.006 / 0.554 |
| 8 | 0.103 / 0.122 | 0.122 / 0.133 | 0.184 / 0.188 | 0.142 / 0.135 |
| 16 | 0.004 / 0.005 | 0.003 / 0.004 | 0.009 / 0.007 | 0.005 / 0.004 |

Lead of the best band: percentiles 10/50/90/99 = 2/4/8/13 (tube60); width of the widest stretch finally empty
≥ 4 generations early, where there is one: 1.5 / 2.75 / 4.25 units (10/50/90%, tube60, 5 units long).
[measured] Bands are not preferred over compact patches on any tube, and the tube is not different from the
torus control. The shares are large only because the whole death lasts six generations and half the cells of a
living face are dead at any moment. **The band-first reading is dead at 54–60 cells.**

Hull face of 84 cells (h84, 117 deaths; `out/h84.txt`) [measured]: fade of 10 generations (6–17), plane beats 95%
of shuffles in 0.80 (living face 0.37), speed 0.79 (0.52–1.09), s.d. of T 3.24, starved for certain 35% (living
face 16%), last cell on the rim line 0.51 ± 0.05 (0.44 by count × occupancy). The same death as at 63 cells.

## 4. Where the last cells sit on a hull face  (`deaths.py hull_11 h63`, 3,000 deaths)

| where | cells | stationary occupancy | P(the last cell is here) | share by count × occupancy | ratio |
|---|---:|---|---|---|---|
| corner | 3 | 0.175 | 0.007 ± 0.002 | 0.017 | 0.42 |
| rim line (a zero coordinate), not corner | 30 | 0.512 | 0.538 ± 0.009 | 0.491 | 1.10 |
| depth 1 | 12 | 0.499 | 0.195 ± 0.007 | 0.192 | 1.02 |
| depth 2 | 15 | 0.523 | 0.220 ± 0.008 | 0.251 | 0.88 |
| depth 3 (centre) | 3 | 0.516 | 0.040 ± 0.004 | 0.050 | 0.81 |

Along the rim line the ratio falls from 1.28 next to the corner's neighbour (class (0,2,9)) through 1.15, 1.07 to
1.02 at the middle of the side; the corner's neighbour (0,1,10) has 0.86. [measured] A mild, monotone preference
for the rim near the corners; not a strong localisation.

## 5. Shape against shape in 1/τ = ν(p)·q(p)  (`python3 decomp.py t63 h63 tube63` → `out/decomp63.txt`)

An excursion starts when P falls below 30 after being ≥ 30; ν(p) = excursions reaching ≤ p per face-generation,
q(p) = share of them ending in death. Differences of logarithms against the wide torus, 63 cells:

| p | 28 | 24 | 20 | 16 | 12 | 8 | 4 | 2 | 1 | 0 (= −Δ ln τ) |
|---|---|---|---|---|---|---|---|---|---|---|
| hull: Δ ln ν | −0.05 | +0.20 | +0.54 | +0.75 | +0.69 | +0.42 | +0.04 | −0.22 | −0.35 | −0.47 |
| tube loop² 9: Δ ln ν | +0.02 | +0.18 | +0.44 | +0.61 | +0.56 | +0.40 | +0.32 | +0.31 | +0.31 | +0.31 |

q itself: q(4) = 0.302 (t63), 0.183 (h63), 0.299 (tube63); q(1) = 0.862, 0.770, 0.864. At 45/48 cells:
q(4) = 0.326 (t48), 0.197 (h45); q(1) = 0.872, 0.780. At 75 cells (t75): q(4) = 0.287, q(1) = 0.868; at 84 cells (h84, 117 deaths): q(4) = 0.197, q(1) = 0.785. [measured]
The end-game is the same game on every wrapped face and a different, easier-to-survive game on a rimmed one, by a
size-independent factor. A hull face is *easier* to bring down to a quarter (its P has mean 31.25, s.d. 5.24,
against 32.58, 4.94), and all of its extra lifetime at 63 cells is won back below 8 cells.
Stationary upper tail: ln P(P ≥ 46) = −6.04 (t63), −6.04 (tube63), −6.50 (h63).

## 6. Holes and islands made by hand  (`python3 punch.py`, `python3 punch2.py` → `out/punch.txt`, `out/punch2.txt`)

Face cells killed in a living face (only the face layer; 800 generations of equilibration; 1,024 samples each).

| vessel | hole | cells | population back to half / to 90% | every cell alive again at least once, median (10–90%) | lowest occupancy of untouched cells within 1 unit |
|---|---|---:|---|---|---|
| torus (10,0),(0,10), 300 cells | disc | 7 | 1 / 2 | 5 (3–9) | 0.98 |
| | disc | 37 | 2 / 4 | 10 (7–13) | 0.99 |
| | disc | 127 | 4 / 8 | 15 (13–19) | 0.99 |
| | half the face | 150 | 5 / 8 | 16 (13–20) | 0.99 |
| tube (1,16),(0,36), 108 cells, 9 long | band of width 1 | 12 | 2 / 3 | 6 (4–10) | 0.96 |
| | band of width 2 | 24 | 3 / 4 | 9 (6–13) | 0.93 |
| | band of width 3 | 36 | 4 / 6 | 11 (8–15) | 0.94 |
| | band of width 4 | 48 | 4 / 8 | 13 (10–17) | 0.94 |
| | band of width 6 | 72 | 6 / 11 | 17 (14–21) | 0.95 |

[measured] A hole never grows (the neighbours lose 1–7% of their occupancy for one generation and no more); it
is retaken from its edge at 0.25–0.31 units per generation by first touch (slope of depth against median
first-alive time, discs of 19–127 cells), and a band of width 1, 2, 3, 4, 6 is back to half its population in
2, 3, 4, 4, 6 generations. No face died of a hole (1 in 1,024 for the 72-cell band). This is why a death cannot be a sweep on a
wrapped face: anything slower than about five generations is undone.

Islands: every face cell killed except the n nearest to one cell. Share of faces that regrow, by the number of
island cells that happened to be alive (1,024–2,048 samples per island size):

| live cells left | 1 | 2 | 3 | 4 | 5 | ≥ 6 |
|---|---|---|---|---|---|---|
| torus, 300 cells | 0.12–0.16 | 0.39–0.51 | 0.70–0.84 | 0.89–0.95 | 0.97–1.00 | ≥ 0.99 |
| torus, 63 cells | 0.12–0.15 | 0.43–0.49 | 0.72–0.88 | 0.88–0.96 | 0.96–1.00 | ≥ 0.99 |
| hull 63, centre | 0.16–0.19 | 0.47–0.55 | 0.80–0.85 | 0.94–0.95 | 0.99 | 1.00 |
| hull 63, middle of a rim line | 0.17–0.20 | 0.52–0.62 | 0.79–0.90 | 0.92–0.96 | 0.98 | 1.00 |
| hull 63, rim line by a corner | 0.20–0.28 | 0.56–0.63 | 0.78–0.85 | 0.93–0.95 | 0.96–0.97 | 0.94–0.98 |
| hull 63, corner | 0.22–0.24 | 0.55–0.71 | 0.79–0.88 | 0.91–0.93 | 0.93–0.96 | 0.94–0.99 |

(ranges over island sizes 3, 5, 8; each entry ± 0.02–0.04.) [measured] The point of no return is two live cells.
One live cell over living chaos regrows the face one time in seven on a wrapped face and one time in four or five
on the rim of a hull face; this matches the natural end-game (recovery from P ≤ 1: 1 − q(1) = 0.138 on t63, 0.230
on h63), so the natural end-game is this game. Regrowth to half the stationary population takes 11–18 generations
on the 300-cell face.

## 7. The mechanism, one paragraph per shape

**Wide wrapped face.** A hole cannot kill it: a hole of a third of the face is back at half its population in 4
generations and is never seen to grow (§6). What kills it is the face acting as one. One generation in 400 the
face is over-full, 46 or more cells of 63 where 33 is normal, and it gets there in a single generation, together
with the layer beneath, from a state that looks ordinary; when it reaches 48 nearly every live cell has six or
more live neighbours and dies, and every dead cell has too many to be born: about once in 6,700 generations half
the face goes in one step and 12 cells are left (§2). Usually those 12 rebuild the face; roughly one time in 130
(between 100 and 200) they starve first, in two to four generations.
The face is empty 6 generations after it was last normal (§1), the last-alive times are flat across the face with
a spread of 1.85 generations, and no place is preferred. Once it is down to 4 cells the chance of death is 0.30,
to 1 cell 0.86 (§5).

**Tube.** The same death, in the same six generations, with the same fall (51–57% of deaths) and the same
end-game (q(4) = 0.299 against 0.302). No band empties first (§3), and a band cut by hand refills in as many
generations as it is wide (§6). What a short loop changes at 63 cells and loop² 9 is the frequency of deep dips:
a dip to 16 cells is 1.85 times as frequent as on the wide torus, a dip to 4 cells 1.38 times, and nothing
changes after that (§5). At loop² 9 the chaos behind the face is also cut across the tube as often as a face dies.

**Rimmed hull face.** It almost never dies by the fall (1.6% of deaths; in the living face such a fall was not
seen once in 7,390 windows; at 84 cells in none of 117 deaths): its rim line, half of its cells at this size,
survives the over-full generation (0.69 per live cell against 0.42 inside) and the face is still at
31.5 cells a generation later where the wrapped face is at 22.9 (§2). So it has to die the slow way. It fades over 10
generations by starvation, lopsidedly: the last-alive times tilt across the face in 77% of deaths at 0.6 units per generation (§1), the living set at 8 cells is 4.2 times as
lopsided as a random subset, and the last cell is on the rim line 54% of the time, most often near a corner (§4).
A hull face reaches 16 cells twice as often as a wrapped face of the same area and 4 cells exactly as often, but
its last cells are harder to kill: 0.18 against 0.30 from 4 cells; by hand, one or two live cells on the rim
regrow the face more often than on a wrapped face (0.20–0.28 for one cell against 0.12–0.15; §6).

**Still inference, not measurement.**
- That the rim's protection lasts as faces grow. At 63 cells the rim line is 33 cells of 63 and survives the
  over-full generation (§2, measured); at 135 cells it is 51 of 135 and the inside may then bust on its own.
- Any link between these routes and the prices per cell (0.2087 wrapped, 0.231 rimmed). The end-game factor
  does not change with size, so the price difference must be in how ν(4), the rate of reaching 4 cells, scales
  with area on each shape. Measured only at 63 cells (hull/torus = e^(+0.035)). At 84 cells, from the anchors'
  lifetimes and q(4) = 0.197 (h84, measured) against about 0.28 (wrapped, extrapolated from 0.326, 0.302, 0.287),
  ln ν(4) is −16.52 for the hull face and about −16.27 for the wrapped one: the hull face would reach 4 cells
  only 0.78 times as often. So the rimmed face's extra price is in the descent, not in the end-game [conjectured
  from one size and one extrapolation].
- That boom and bust persists beyond 75 cells. A face over-full everywhere at once is a collective state; at
  some size it should lose to something local. The trend of its share with size is in the table of §2.
- Why a short loop makes deep dips more frequent.

## 8. Forecasts (PREDICTIONS.md; block 1 committed in 9008dc1 before any run, block 2 in 21bf6e0 before analysis)

| # | forecast | measured | |
|---|---|---|---|
| 1 | plane beats 95% of shuffles in 0.50 of deaths on t63 (60%: 0.35–0.65) | 0.325 | miss |
| 2 | median R² 0.30 against 0.12 | 0.151 against 0.115 | miss |
| 3 | sweep speed 0.35 (0.2–0.6) | 1.00 (the speed limit) | miss |
| 4 | remnant cone better than plane in 60% | 8.8% | miss |
| 5 | last cell of a hull face: corner / rim line / inside = 0.02 / 0.60 / 0.38; rim enriched; corners depleted | 0.007 / 0.538 / 0.455; ratio 1.10; 0.42 | numbers near, both qualitative calls right |
| 6 | tube (loop² 9): axial mode > girth mode in 70% of deaths | 0.655 (loop² 12: 0.56; shuffles 0.50; `out/axial_vs_girth.txt`) | near; a weak preference |
| 7 | hull and torus part late (under half of the 0.47 present at p = 10) | at p = 10 the hull is ahead by 0.57; all of it comes below 8 cells | hit |
| 8 | tube and torus part early | +0.475 at p = 10 against +0.310 in the end | hit |
| 9 | hole retaken at 0.4 units/generation (0.25–0.6) | 0.25–0.31 | hit, at the edge |
| 10 | holes do not grow (80%) | they do not | hit |
| 11 | islands of 3 / 7 / 12 cells regrow 0.5 / 0.9 / 0.99 | 0.34–0.39 / 0.74–0.75 / 0.90–0.94 | 3-cell value inside my interval; all three lower than forecast |
| 12 | band share at lead ≥ 4 on tube60: 0.45 (60%: above 0.25) | 0.526 | hit |
| 13 | the same on t63: 0.30 (0.15–0.45) | 0.572 | miss |
| 14 | a compact patch does at least as well as a band | 0.576 against 0.526 | hit |
| 15 | tube excess over the torus real (ratio > 1.3; I gave 50%) | ratio 0.92 | no |
| PI | band share 9% (54 cells), 12% (63), under 5% on the torus | 48%, 53% (60 cells), 57% | miss; no band-first class |

Seven of fifteen. Every forecast that assumed a sweep was wrong.

## 9. What was not checked

- Nothing above 84 cells (wrapped faces: 75; an 84-cell torus run was cut by the deadline), and no reactive paths from the samplers of `split-slab`, `split-hull`, `tube1d` (their
  files had not appeared by 03:45 UTC). Whether boom and bust is the route at 108–360 cells is the open question.
- "Align before averaging": I fitted every death singly but did not build the aligned average profile T(r).
- The third layer is not in the death records (8 of a face cell's 9 neighbours are), hence "overcrowded for
  certain / if the unseen neighbour lives".
- Lives ended as "settled" (state equal to a snapshot 840·m generations earlier, m ≤ 32) are 0–2 per run; a
  zombie with a longer period would go unseen. Lifetimes agree with the anchors to within 1.5 standard errors.
- The stepper was validated by me (state for state against the oracle for ≥ 1,100 generations on every vessel,
  with a failing negative control); the statistics code (`deaths.py`, `crash.py`, `decomp.py`, `punch*.py`) has had
  no second reader. The excursion bookkeeping in `an.c` was not cross-checked against `research/dying/ex.c`.
- The shuffle null destroys all spatial correlation, so a living face already "beats" it 12–33% of the time;
  the baseline row is the fair comparison, and no null with the living face's short-range correlations was built.
- Island experiments leave the layers beneath at their stationary state; in a natural death the layer beneath
  is at 60–70% of normal. The match of the one-cell numbers suggests this matters little; not tested further.

## Files

`an.c` stepper (run / trace / punch); `geom.py` vessels; `validate.py` oracle check; `run1.sh`–`run3.sh` batches;
`deaths.py` fields and fits; `crash.py` falls, causes, band test; `decomp.py` ν·q by shape; `punch.py`, `punch2.py`
holes and islands; `out/` every table above as text and JSON; `PREDICTIONS.md`. Bulk records are under
`research/scratch/blast/anatomy/` (not in git; regenerate with the run scripts, same seeds).
