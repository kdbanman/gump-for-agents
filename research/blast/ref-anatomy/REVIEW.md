# REVIEW of `anatomy` by the referee `ref-anatomy` (blast of 2026-11-18)

**Verdict in five lines.** The headline survives: I could not break it. With my own stepper, my own statistics
and fresh seeds, every number of anatomy's that I could reach comes back within its error or within one cell of
a threshold. What I add is what the claim *means*: (i) "57–59%" is the median of one broad hump cut by an
arbitrary line (one cell of threshold moves it by 5 points; 84% of deaths contain a fall of 0.4 of the face, 98%
one of 0.3 within 47 generations); (ii) it is not a breathing mode (lag-1 autocorrelation of the face population
+0.14, the boom comes in one step from a normal face); (iii) the bust is also how most *non-fatal* deep dips are
made (46–67% of them), so most of it sits in ν(p), not q(p); but (iv) q is not a function of p alone: at 4 cells a
dip made by a bust is 1.41 times as deadly as one that was not, because the bust empties the layer beneath as
well; (v) the hull face differs already alive: its population is a slow variable (lag-1 autocorrelation +0.52) and
its return map has no cliff.

All labels **[measured]** unless said. Error bars are binomial or 1/√deaths. Nothing here is proved.

## 0. What was done, and the conventions

- **Code** (written from `docs/AUTOMATON.md` and `reference/oracle.py` alone; none of anatomy's files other than
  its README was opened): `vessel.py` (vessels as graphs), `fd.c` (bit-sliced graph stepper, 256 replicas, face
  bookkeeping), `validate.py`, `analyse.py`, `island.py`.
- **Validation** (`python3 validate.py NAME [swap] [REPLICA]`, results in `validate.out`, `validate_t48.out`):
  state for state against the oracle for 1,100 generations on the 63-cell torus (1,4),(0,21) (replicas 0, 201),
  the tube (1,8),(0,20) (replicas 0, 130), the hull of radius 11 (replicas 0, 77) and the 48-cell torus; the same
  graph with one swapped neighbour fails at generation 1, 2, 10 (and see `validate_t48.out`). A slab of index n is
  embedded in the oracle's cubic torus of side 2n (21 or 20 images of every cell, ≥ 12 dead layers between images).
- **Runs** (`sh run.sh`, one core, 10 minutes; seeds 2026111801–04, none of them anatomy's): soup of density 0.375,
  1,000 generations of burn-in (a face lost in burn-in restarts the replica, uncounted), then every generation of
  a replica is exposure until the first generation in which a face layer is empty (that face's death; the replica
  restarts). τ_face = F·exposure/deaths, F = 2 (slab), 8 (hull). No replica settled (checked every 2,520
  generations against a snapshot).
- **Statistics** (`sh analyse_all.sh` → `out/NAME.txt`, every line tagged; `data/returnmap.csv`,
  `data/autocorr.csv`): P(t) = live cells of the face layer; t = 0 the first empty generation; fall at k =
  P(k−1) − P(k); "half the face" = fall ≥ 32 of 63, ≥ 30 of 60, ≥ 24 of 48; unless said, the largest fall is looked
  for in the last 12 generations (k = −11…0); excursion = from the first P < P0 after P ≥ P0 to the next P ≥ P0 or
  death (P0 = 30 of 63, 29 of 60); ν(p) = excursions reaching ≤ p per face-generation; q(p) = share of them fatal.
  Overcrowded = ≥ 6 of **all 12** neighbours alive (from the full state, which is kept for the last 16
  generations of every death); starved = ≤ 2. Thresholds given for 63 cells are scaled by A/63 and rounded on
  the tube (44 → 42, 46 → 44, 16/12/8/4 → 15/11/8/4).

## 1. Lifetimes (attack point d)

| vessel | cells | exposure (replica-generations) | deaths | ln τ_face here | anchor | anatomy |
|---|---:|---:|---:|---|---|---|
| torus (1,4),(0,21) | 63 | 1,913,863,923 | 7,379 | 13.1591 ± 0.0116 | 13.1622 ± 0.0007 | 13.1547 ± 0.0113 |
| tube (1,8),(0,20), loop² 12 | 60 | 1,031,150,521 | 8,218 | 12.4330 ± 0.0110 | 12.4230 ± 0.0025 | 12.4168 ± 0.0110 |
| hull radius 11 | 63 | 543,379,399 | 5,268 | 13.6234 ± 0.0138 | 13.633 | 13.6205 ± 0.0116 |
| torus (4,0),(0,4) | 48 | 600,572,609 | 58,668 | 9.9269 ± 0.0041 | 9.9251 ± 0.0004 | 9.9383 ± 0.0086 |

All within 1σ of the anchors (`out/NAME.txt`, line `[lifetime]`). The 48-cell torus was added late for §3e; 36 of
its lives ended settled (a state repeating with a period dividing 2,520 while both faces lived) and are not
counted as deaths; none on the other vessels.

## 2. Verdicts, claim by claim

Command for every row: `sh run.sh && sh analyse_all.sh`, then the tagged line of `out/t63.txt`, `out/tube60.txt`,
`out/h63.txt`, `out/island.txt`.

### Claim 1: wrapped faces die by boom and bust

| statement of anatomy | anatomy | referee | verdict |
|---|---|---|---|
| deaths with a one-generation fall of ≥ half the face, t63 | 0.590 | 0.559 ± 0.006 (≥ 32 cells, last 12 generations); 0.576 (last 47); 0.610 at ≥ 31 | CONFIRMED to within one cell of threshold (5 points per cell) |
| the same, tube60 | 0.567 | 0.572 ± 0.006 (≥ 30, last 12); 0.592 (last 47) | CONFIRMED |
| population before the fall, t63 | 48.5 (46–52) | 48.83 ± 0.05 (46–52) | CONFIRMED |
| population after it | 11.6 (8–15) | 11.18 ± 0.05 (8–14) | CONFIRMED (the 0.4 is the threshold: mine is ≥ 32 and the largest fall) |
| tube60: before → after | 46.4 → 10.8 | 46.36 → 10.89 | CONFIRMED |
| births in the generation of the fall | 1.9 | 1.78 (tube 1.79) | CONFIRMED |
| the dying cells are overcrowded (80.9% for certain + 18.5% if the unseen neighbour lives) | | 99.46% have ≥ 6 of 12 neighbours alive (tube 99.40%); 0.54% starved | CONFIRMED; the caveat is closed: the unseen neighbour was alive |
| "every live cell is then overcrowded" | | 80.3% of the live cells of the over-full generation are (tube 79.9%; living face 27.4%) | CORRECTED: four in five |
| the survivors starve in 2–4 generations (later text: median 4, 10–90% 2–8) | | fall → empty face: median 4, 10–90% 2–8, mean 4.41; 98.5% of the cells dying after the fall are starved | "2–4" CORRECTED to 2–8; the later text CONFIRMED |
| stationary: mean 32.6, s.d. 4.94, P(P ≥ 46) = e^−6.04 | | 32.583, 4.942, e^−6.035 (3.8·10⁹ face-generations) | CONFIRMED |
| a fall of half the face: 1.5·10⁻⁴ per generation (± 30%) | | 1.350·10⁻⁴ ± 0.002·10⁻⁴ (tube60: 2.354·10⁻⁴) | CONFIRMED, now exact |
| about one such fall in 130 is fatal | | 1 in 125 ± 2 (tube60: 1 in 103) | CONFIRMED |
| one generation after P ≥ 46: P = 22.9 (18–28) | | 23.01 (18–28), 9.2·10⁶ generations | CONFIRMED |
| share of those falling to ≤ 15: 0.027 ± 0.004; after P ≥ 48: 0.094 ± 0.016 | | 0.0353 ± 0.0001; 0.1173 ± 0.0003 | CORRECTED (anatomy low by 2σ and 1.5σ; its living sample is the 87 generations before a death) |
| layer beneath: 15.5 at its lowest against 27.4 | | 15.2 (t = −2) against 27.52 | CONFIRMED |
| layer beneath over-full with the face (39.9 → 9.8; added to anatomy's README after my brief) | | 39.90 → 9.88 (tube 37.95 → 9.41) | CONFIRMED |
| one hump, not two (added later) | | one hump, mode 33–35 cells; see (b) | CONFIRMED |

### Claim 2: hull faces do not

| statement | anatomy | referee | verdict |
|---|---|---|---|
| deaths with a fall of ≥ half the face | 0.016 | 0.0108 ± 0.0014 (≥ 32, last 12); 0.0122 (last 47); 0.0152 at ≥ 31 | CONFIRMED in substance, CORRECTED to 1.1–1.5% |
| largest fall, median | 13 | 14 (10–90%: 6–24) | CONFIRMED |
| fade of about 10 generations (5–16) from the last P ≥ 30 | 10 (5–16) | median 9 (5–16), mean 10.3; torus median 5 (3–10), mean 6.3 | CONFIRMED |
| plane fitted to last-alive times beats 95% of shuffles | 0.767; living 0.334 | 0.790 ± 0.009; living 0.333 ± 0.011 (my field: 16 generations, censored at −16, 54 cells, 2,000 deaths, 100 shuffles) | CONFIRMED |
| speed | 0.60 (0.41–0.85) | 0.62 (0.45–0.90) units per generation | CONFIRMED |
| rim line survives the over-full generation: 0.69 per live cell against 0.42 inside (P ≥ 44) | | 0.688 against 0.386 (P ≥ 46; 3,000 generations) | CONFIRMED |
| one generation after P ≥ 46: 31.5 (25–38); 0 of 1,040 fall to ≤ 15 | | 31.18 (25–37); 0.00040 ± 0.00001 (2,603 of 6.6·10⁶) | CONFIRMED (0.4 expected in 1,040) |
| P(P ≥ 46) = 0.0015; mean 31.25, s.d. 5.24 | | 0.00151 (e^−6.495); 31.252, 5.242 | CONFIRMED |
| "deaths are starvation" (36% starved for certain, 24% overcrowded for certain) | | of the face cells dying in the last 8 generations 57.8% are starved, 42.2% overcrowded (living hull face 39.3 / 60.7; dying torus face 38.6 / 61.4, living 29.3 / 70.7) | CORRECTED: a tilt towards starvation, not starvation alone |
| layer beneath: 19.0 at its lowest against 27.8 | | 18.98 (t = −3) against 27.74 | CONFIRMED |

### Claim 3: where the shapes part

| statement | anatomy | referee | verdict |
|---|---|---|---|
| q(4), torus | 0.302 | 0.3019 ± 0.0029 (tube60 0.3060 ± 0.0028) | CONFIRMED |
| q(4), hull | 0.183 | 0.1827 ± 0.0023 | CONFIRMED |
| q(1) | 0.862 / 0.770 | 0.8619 ± 0.0037 / 0.7794 ± 0.0050 | CONFIRMED |
| hull reaches 4 cells as often: ratio e^(+0.035 ± 0.01) | | e^(+0.038 ± 0.009) | CONFIRMED |
| Δ ln ν (hull − torus) at p = 28, 24, 20, 16, 12, 8, 4, 2, 1, 0 | −0.05, +0.20, +0.54, +0.75, +0.69, +0.42, +0.04, −0.22, −0.35, −0.47 | −0.053, +0.195, +0.539, +0.755, +0.688, +0.419, +0.038, −0.222, −0.364, −0.464 | CONFIRMED to the last digit |
| the same ratio at 45/48 cells | 0.326 / 0.197 | torus 48: q(4) = 0.3297 ± 0.0011, q(1) = 0.8737 ± 0.0013; hull 45 not run | torus half CONFIRMED; hull half NOT TESTED |

### Claim 4: holes and islands made by hand

| statement | anatomy | referee | verdict |
|---|---|---|---|
| a hole is retaken from its edge at 0.25–0.31 units per generation and never grows | | | NOT TESTED |
| one live cell regrows a wrapped face 0.12–0.15 of the time | | 0.1376 ± 0.0020 (t63), 0.1372 ± 0.0020 (tube60); natural end-game 1 − q(1) = 0.138 | CONFIRMED |
| 0.20–0.28 on a hull's rim | | rim line next to a corner 0.275 ± 0.003, rest of the rim line 0.221 ± 0.002 | CONFIRMED |
| "because one or two live cells **on the rim** regrow the face more often" (§7) | | the row one inside the rim is best (0.303 ± 0.003); min coordinate 2: 0.240; centre (3 cells) 0.181; the corner cell itself 0.154; all 30 inside cells 0.258 against 0.242 for the 30 rim-line cells | CORRECTED: it is the hull face, not its rim line; even its centre beats a wrapped face (0.181 against 0.138, 14σ) |

(`python3 island.py 120`: soup, 1,000 generations, then in each replica one live cell of the class is kept and
every other cell of that face layer is killed; "regrown" = back to ≥ 30 cells before the face is empty; about
29,000 trials per row. Anatomy cut islands of 3, 5, 8 cells and sorted by the number alive; mine keeps exactly one
live cell, so its "corner" row (0.22–0.24, mostly a neighbour of the corner) is not my "corner cell" row.)

**NOT TESTED at all:** the band test (§3 of anatomy), where the last cell sits (§4), cones, anything on wrapped
faces' last-alive fields, the loop²-9 tube, 45, 54, 75 and 84 cells, the 12-layer slab, `primed.txt` (the
arrangement two generations before the fall), holes.

## 3. The attack points

### (a) A route or a tautology?

**No breathing.** Autocorrelation of P in the living state (`data/autocorr.csv`; all face-generations for lags
1, 2; replicas 0–31 for the rest):

| lag | 1 | 2 | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|---|---|
| torus 63 | +0.1363 | −0.0314 | +0.0286 | +0.0054 | +0.0010 | +0.0022 | +0.0010 |
| tube 60 | +0.1698 | −0.0034 | +0.0420 | +0.0138 | +0.0052 | +0.0038 | +0.0014 |
| hull 63 | +0.5166 | +0.3399 | +0.2641 | +0.2069 | +0.1651 | +0.1309 | +0.0879 |

A period-2 mode would give a negative lag 1 and a positive lag 2; the wrapped faces have the opposite signs and are
nearly white. There is a faint alternation (lag 2 below zero, lag 3 above), nothing that grows.

**The return map** (`data/returnmap.csv`: vessel, p, n, mean and variance of P(t+1), the same for P(t+2), share
falling to ≤ a quarter, share dead next generation; every p from 1 to 55 or more is populated; the 48-cell torus is in the file too). Mean of P(t+1) given
P(t) = p (s.d. in brackets):

| p | 1 | 2 | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 46 | 48 | 50 | 52 | 54 | 56 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| torus 63 | 0.88 (1.0) | 2.10 (1.4) | 4.80 (2.1) | 9.77 (2.8) | 14.5 (3.3) | 19.3 (3.8) | 24.3 (4.1) | 28.8 (4.3) | 32.3 (4.5) | 34.0 (4.6) | 33.7 (4.4) | 31.3 (4.2) | 26.9 (4.0) | 24.2 (3.9) | 21.2 (3.8) | 18.0 (3.6) | 14.8 (3.5) | 11.6 (3.1) | 8.6 (2.8) |
| tube 60 | 0.87 | 2.08 | 4.80 | 9.79 | 14.6 | 19.4 | 24.2 | 28.5 | 31.5 | 32.6 | 31.4 | 28.0 | 22.8 | 19.7 | 16.5 | 13.3 | 9.9 | 7.4 | |
| hull 63 | 1.00 (1.0) | 2.30 (1.4) | 4.90 (1.8) | 9.65 (2.5) | 14.3 (3.0) | 18.7 (3.3) | 22.9 (3.6) | 26.8 (3.9) | 30.1 (4.2) | 32.5 (4.4) | 33.8 (4.6) | 33.9 (4.8) | 32.7 (4.8) | 31.7 (4.8) | 30.4 (4.7) | 28.9 (4.6) | 27.1 (4.4) | 25.2 (4.3) | 22.4 (3.6) |

On a wrapped face the map is a hump with a cliff: flat (34) round the mean, falling by 1.5 cells per cell above
44, with noise of 3.5–4.5 cells at every p. On the hull face it falls by 0.7–0.9 per cell. Below 20 cells the three
maps are the same (growth by a factor 1.2 per generation), the hull slightly the slower between 12 and 28.
Chance of dying in one step from 1, 2, 3, 4 cells: torus 0.439, 0.138, 0.038, 0.013; hull 0.381, 0.096, 0.020, 0.0055.

**Is every deep dip preceded by an over-full generation?** Excursions reaching ≤ L: share whose first generation
at ≤ L was preceded by P ≥ 44 one generation before / within 2 / within 4 (chance level: P ≥ 44 has stationary
probability 0.0094 per generation on the torus, 0.0060 on the hull):

| | L = 16, not fatal | fatal | L = 12, not fatal | fatal | L = 8, not fatal | fatal | L = 4, not fatal | fatal |
|---|---|---|---|---|---|---|---|---|
| torus 63: n | 4,149,370 | 7,379 | 708,211 | 7,379 | 122,723 | 7,379 | 17,059 | 7,379 |
| lag 1 | 0.162 | 0.691 | 0.079 | 0.366 | 0.019 | 0.091 | 0.001 | 0.006 |
| within 2 | 0.392 | 0.811 | 0.423 | 0.779 | 0.309 | 0.617 | 0.105 | 0.236 |
| within 4 | 0.460 | 0.817 | 0.602 | 0.814 | 0.673 | 0.804 | 0.644 | 0.745 |
| tube 60, within 2 | 0.349 | 0.779 | 0.391 | 0.737 | 0.320 | 0.617 | 0.121 | 0.243 |
| tube 60, within 4 | 0.419 | 0.788 | 0.563 | 0.783 | 0.631 | 0.775 | 0.629 | 0.725 |
| hull 63, within 2 | 0.016 | 0.065 | 0.013 | 0.047 | 0.007 | 0.020 | 0.001 | 0.004 |
| hull 63, within 4 | 0.035 | 0.084 | 0.040 | 0.073 | 0.040 | 0.059 | 0.032 | 0.038 |

(errors ≤ 0.006 on the fatal columns, ≤ 0.004 elsewhere.) So the suspicion in my brief is half right. On a
wrapped face the bust is how deep dips are made, fatal or not: two thirds of the *surviving* dips to 8 or 4 cells
came out of an over-full generation (0.67, 0.64), against 0.80 and 0.75 of the fatal ones. Most of "boom and bust" is therefore a
statement about ν(p), the supply of deep dips, and anatomy's own 1/τ = ν·q table hides it.

**But the fatal step is not elsewhere either: q depends on the way down.** q(L) split by whether the dip came
within 4 generations of P ≥ 44 (line `[does the way down matter?]`):

| | q(16) bust / not | q(12) | q(8) | q(4) |
|---|---|---|---|---|
| torus 63 | 0.0032 / 0.0006 | 0.0139 ± 0.0002 / 0.0048 ± 0.0001 | 0.0670 ± 0.0008 / 0.0348 ± 0.0009 | 0.3337 ± 0.0037 / 0.2362 ± 0.0048 |
| tube 60 | 0.0049 / 0.0010 | 0.0222 / 0.0080 | 0.0709 / 0.0366 | 0.3371 ± 0.0036 / 0.2462 ± 0.0045 |
| hull 63 | 0.0013 / 0.0005 | 0.0059 / 0.0031 | 0.0341 ± 0.0019 / 0.0230 | 0.211 ± 0.013 / 0.182 ± 0.002 |

At the same 4 live cells a wrapped face that got there by a bust dies 1.41 ± 0.03 times as often (16σ); at 12
cells 2.9 times. The face population is not a Markov state near the end: "a death is memoryless" holds for the
waiting time, not for the path. The hidden variable is at least the layer beneath: before a fatal fall it holds
39.9 cells and after it 9.9 (stationary 27.5 ± 4.8); before a *non-fatal* fall of half the face 34.5 → 18.6; in
an ordinary over-full generation (P ≥ 46) 30.7 → 23.6. The face is left with 11.2 cells in a fatal fall and
14.9 in a non-fatal one: the difference between a fall that kills and one that does not is much more in the layer
beneath (9.9 against 18.6) than in the face. A route, then, and of two layers; and about half of the gap between the
torus's q(4) = 0.302 and the hull's 0.183 is the route (the torus's q(4) without a bust is 0.236).

### (b) The threshold, the whole distribution, the trajectories

Largest one-generation fall (line `[claim 1/2]` and the histogram under it; living = windows of the same length
taken at random times from living faces: 7,471 torus, 4,030 tube, 7,066 hull):

| | torus 63, deaths | living | tube 60, deaths | living | hull 63, deaths | living |
|---|---|---|---|---|---|---|
| median (10/25/75/90%), last 12 generations | 33 (21/27/38/42) | 12 (7/9/15/19) | 31 (19/25/36/39) | 11 (7/9/15/18) | 14 (6/10/19/24) | 9 (6/7/12/14) |
| share ≥ 0.3 of the face | 0.932 | 0.100 | 0.921 | 0.124 | 0.277 | 0.020 |
| ≥ 0.4 | 0.809 | 0.014 | 0.811 | 0.023 | 0.067 | 0.0008 |
| ≥ 0.5 | 0.559 | 0.0025 | 0.572 | 0.0035 | 0.011 | 0 of 7,066 |
| ≥ 0.6 | 0.252 | 0.0003 | 0.256 | 0.0002 | 0.0004 | 0 |
| last 47 generations: ≥ 0.3 / 0.4 / 0.5 | 0.978 / 0.841 / 0.576 | 0.344 / 0.048 / 0.007 | 0.969 / 0.847 / 0.592 | 0.396 / 0.084 / 0.013 | 0.356 / 0.076 / 0.012 | 0.073 / 0.003 / 0.0001 |

One hump on every vessel (torus: mode 33–35 cells, 16% of deaths per 3 cells; hull: mode 12–14). "Half the face"
cuts the torus's hump at its median, which is the whole content of "57–59%": at 31, 32, 33 cells the share is
0.610, 0.559, 0.511. The torus and tube have a second small bump at 0–8 cells (3.7% of deaths): faces that hung
on at about 9 cells for more than 12 generations; their big fall is further back (median 30 cells in the last 47
generations), and with 47 generations of history only 0.01% of deaths have no fall above 8. So it is not a second
route. A fairer one-line statement: **80% of wrapped deaths come out of an over-full face** (peak P ≥ 44 in the 12
generations before death: 0.792 torus, 0.769 tube at ≥ 42; living windows 0.106, 0.128; hull deaths 0.080 against
0.070 living, i.e. no excess at all).

Mean P(t) before death (10/50/90%), and the layer beneath (lines `[mean P(t)…]`, `[layer beneath…]`, all t in `out/`):

| t | −12 | −10 | −8 | −6 | −5 | −4 | −3 | −2 | −1 |
|---|---|---|---|---|---|---|---|---|---|
| torus 63, face | 31.8 (25/33/39) | 31.0 (22/32/39) | 29.2 (9/32/40) | 25.4 (3/30/43) | 23.3 (3/26/47) | 18.6 (2/12/48) | 10.9 (1/6/37) | 4.3 (1/3/9) | 1.7 (1/1/3) |
| torus 63, beneath (living 27.5) | 27.0 | 26.5 | 25.8 | 23.7 | 23.4 | 21.0 | 16.9 | 15.2 | 16.1 |
| tube 60, face | 30.4 (24/31/37) | 29.6 (20/31/38) | 27.8 (9/30/38) | 24.4 (3/29/42) | 22.0 (3/25/44) | 18.1 (2/11/45) | 10.4 (1/6/31) | 4.2 (1/3/8) | 1.7 (1/1/3) |
| tube 60, beneath (living 26.3) | 25.6 | 25.3 | 24.4 | 22.8 | 22.0 | 20.1 | 16.0 | 14.5 | 15.2 |
| hull 63, face | 27.4 (15/29/37) | 25.2 (10/27/37) | 21.3 (6/22/35) | 16.3 (3/14/33) | 13.2 (3/10/29) | 10.1 (2/7/22) | 6.5 (1/5/14) | 3.6 (1/3/7) | 1.6 (1/1/3) |
| hull 63, beneath (living 27.7) | 25.2 | 24.0 | 22.5 | 20.8 | 20.0 | 19.5 | 19.0 | 19.4 | 20.1 |

The death-aligned mean hides the wrapped route (at t = −4 the torus's 10% and 90% points are 2 and 48 cells: some
faces are already finished, others are at the peak); aligned on the fall it is 33.3 → 48.8 → 11.2. The hull's
quantiles slide down together.

### (c) What makes the over-full generation?

One step from a normal face, on wrapped faces; a slow build-up on the hull (lines `[one generation before…]`,
`[two generations before…]`, from the complete joint histograms of (P(t), P(t+1)) and (P(t), P(t+2))):

| | P one generation before P ≥ 46 (10/50/90%) | two before | share of the "one before" at ≤ mean − 1 s.d. (stationary) | at ≥ mean + 1 s.d. (stationary) |
|---|---|---|---|---|
| torus 63 | 32.99 (30/33/36) | 31.10 (26/31/36) | 0.016 (0.149) | 0.039 (0.158) |
| tube 60 (P ≥ 44) | 31.42 (28/31/35) | 29.58 (25/30/34) | 0.009 (0.134) | 0.050 (0.174) |
| hull 63 | 36.48 (33/36/40) | 34.59 (30/35/40) | 0.0002 (0.178) | 0.495 (0.156) |

On the torus the over-full generation is born of a face that is *more* ordinary than ordinary (33 ± 2.4, the top
of the return map; under-full and over-full predecessors are both suppressed tenfold and fourfold): no oscillation
growing over cycles. Before a fatal fall the six generations before the peak read 32.9, 32.5, 32.2, 33.7, 30.8,
33.3 (a dip of 2 cells two generations before the peak is all there is; the same 30.6–31.2 shows before non-fatal
falls and before plain over-full generations). The boom is +15.6 cells in one generation where the one-step noise is
4.5: a 3.4σ event of the map's noise, followed by the cliff (mean 20.2 after P ≥ 48) and another −2.4σ.

Over-full everywhere, not only on average: dispersion of the live count over thirds of the face (bands across
each of the two shortest loops; hull: the three corners' thirds), divided by its value for a random subset of the
same size (lines `dispersion over thirds`):

| | living face, any generation | over-full living generation (P ≥ 46) | before a non-fatal fall of half | before a fatal fall |
|---|---|---|---|---|
| torus 63 | 1.82 ± 0.02 | 1.56 ± 0.02 | 1.73 ± 0.02 | 1.47 ± 0.02 |
| tube 60 | 1.89 ± 0.02 | 1.59 ± 0.02 | 1.71 ± 0.02 | 1.43 ± 0.02 |
| hull 63 | 2.45 ± 0.05 | 1.79 ± 0.03 | 2.37 ± 0.04 | 3.1 ± 0.5 (45 deaths) |

A wrapped face about to bust fatally is the most evenly filled face there is.

### (e) Other things in anatomy's README

- "8 of 9 neighbours recorded": closed above (99.5% of the cells dying in the fall are overcrowded on the full count).
- Split of the price (its §2): fall rate ln −8.80 ± 0.29 and fatal share e^−4.88 at 63 cells; exact here:
  ln rate = −8.910 ± 0.001, fatal share e^(−4.83 ± 0.02) (tube60: −8.354, e^−4.64; anatomy −8.42 ± 0.24, e^−4.56).
  CONFIRMED at 60 and 63. At 48 cells anatomy has −7.20 ± 0.10 and e^−3.30; exact here (1,144,679 falls):
  ln rate = −6.955 ± 0.001, fatal share e^(−3.512 ± 0.005) (`out/t48.txt`; share of deaths with a fall of ≥ 24
  cells 0.582 ± 0.002, anatomy 0.572; 37.31 → 8.46 cells, anatomy 37.3 → 8.4). So anatomy's "each factor falls by
  about 0.107 per cell: half of the price is the rarity of the fall, half the rarity of its leftover failing to
  rebuild" is CORRECTED: between the 48- and 63-cell wide tori the fall's rate falls by **0.1303 ± 0.0001 per
  cell** and its fatal share by **0.0879 ± 0.0011 per cell** (sum 0.2182; ln τ rises by 0.2155 per cell and the
  share of deaths with a fall changes by the rest). Three fifths rarity, two fifths fatality. [two sizes only;
  loops² 16 against 21]
- "Such a fall was not seen once in 7,390 windows" on the hull: its rate is 1.98·10⁻⁶ ± 0.02·10⁻⁶ per generation
  (8,620 falls), 68 times rarer than on the torus, and one in 151 is fatal against one in 125: on a hull face the
  fall is as deadly as on a torus, it just does not happen. That is a sharper form of anatomy's "the rim closes
  this route".
- Generations from the last P ≥ 30 to death on the torus: anatomy 6 (3–10), mine median 5 (3–10), mean 6.27: a
  rounding of a median between 5 and 6, no more.

## 4. The referee's additions

1. **The return maps and autocorrelations** (`data/returnmap.csv`, `data/autocorr.csv`; §3a). For whoever builds a
   one-variable model: the wrapped map is a hump with a cliff and nearly white noise; P alone is *not* Markov near
   the end (next item), and on the hull it is not Markov even alive (lag 2 = +0.34 against 0.52² = 0.27).
2. **q depends on the way down** (§3a): q(4) = 0.334 after a bust against 0.236 otherwise (torus), because the bust
   is a two-layer event. Any theory with one population variable will get ν·q right only on average.
3. **The living states do differ, in time.** The brief says the differences between shapes are not in the living
   state; in density, yes. But the hull face's population has lag-1 autocorrelation +0.52 (torus +0.14), a return
   map without a cliff (after P ≥ 48: 29.9 against 20.2), over-full generations that are built up over several
   generations (36.5 the generation before, against 33.0), and falls of half the face 68 times rarer at a 1.6
   times rarer over-full state.
4. **The fall is equally deadly everywhere it happens** (1 in 125 torus, 1 in 103 tube60, 1 in 151 hull): what a
   shape changes is its frequency (1.35·10⁻⁴, 2.35·10⁻⁴, 1.98·10⁻⁶ per generation).
5. **One live cell by place on the hull face** (claim 4's table above): 0.154 corner cell, 0.275 and 0.221 rim
   line, 0.303 one row in, 0.240 two rows in, 0.181 centre; wrapped 0.138.

## 5. What I did not check

- Sizes other than 60 and 63 cells (and the 48-cell torus for §3e and q); nothing above 63. Whether boom and
  bust is the route at 108 cells and beyond is as open as anatomy says.
- Claim 4's holes, the band test, the last cell's place, the wrapped faces' plane fits, `primed.txt`.
- My tilt statistic uses 16 generations of history with censoring, not anatomy's 128; that the two agree
  (0.790 / 0.333 against 0.767 / 0.334) is some evidence that the censoring does not matter, not a proof.
- "Bust" in the ν/q tables is defined by P ≥ 44 of the face only; a definition on both layers would sharpen it.
- Excursions in progress on the other faces of a hull when one face dies are discarded (22,625 of them); they are
  short, and I did not estimate the bias (it cannot touch q(4) by more than the 0.4% of excursions lost).
- The statistics code has had no second reader. The stepper is validated; `analyse.py` is not, except by its
  agreement with anatomy's independent numbers, which is close everywhere.
- Soup density 0.375 and a burn-in of 1,000 generations are my choices; not varied.

## 6. Forecasts (`PREDICTIONS.md`, hull block committed in 0c3014d before the hull output was read)

| # | forecast | measured | |
|---|---|---|---|
| 1 | ln τ within 0.03 of 13.633 | 13.6234 | hit |
| 2 | lag-1 autocorrelation +0.10 to +0.25, lag 2 within 0.05 of zero | +0.517, +0.340 | miss, badly: I expected the hull to look like the torus alive |
| 3 | share of deaths with a fall of half: 0.01–0.03 | 0.0108 | hit, at the edge |
| 4 | P after P ≥ 46 between 30 and 33; share to ≤ 15 below 0.001 | 31.18; 0.0004 | hit |
| 5 | q(4) 0.17–0.20; ν(4) within e^±0.06 of the torus | 0.1827; e^+0.038 | hit |
| 6 | fatal excursions preceded by P ≥ 44 within 4 generations: under 0.15 | 0.084 | hit |
| 7 | plane beats shuffles in 0.60–0.85 of deaths | 0.790 | hit |
| 8 | one hump, median 12–14 | one hump, median 14 | hit |

Seven of eight on the hull; no forecasts were written for the torus and tube (measured first, for lack of time).
