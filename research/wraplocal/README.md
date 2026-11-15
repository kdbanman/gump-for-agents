# What a tube's living state carries (research/wraplocal)

2026-11-15. Question: which local property of the living state of a wrapped face with one short loop (a tube)
tracks its price per cell (loop² 12: 0.20437 ± 0.00016, 13: 0.20602 ± 0.00033, 16: 0.20717 ± 0.00011, 19: 0.20898
± 0.00120, none: 0.20864 ± 0.00009; CLAIMS WL3), and why the effect ends between loop² 19 and 21. Marks: [proved],
[measured], [fitted], [post hoc] (a choice made after seeing the data it is tested on).

## Answer

- **The face-layer density tracks the price [measured, fitted on two girths].** On a torus with period lattice Λ
  the stationary density of the two face layers is, to the precision reached (± 0.00001),

      ρ_face = ρ∞ − Σ_{v ∈ Λ∖0, one per ±v} f(|v|²),    ρ∞ = 0.517742 ± 0.000006,

  with one f per loop length, the same for every torus (27 tori, 63–147 cells, 1 to 3 short directions; χ² 13.8 on
  14). f(9) = 0.006267, f(12) = 0.002317, f(13) = 0.001605, f(16) = 0.000768, f(19) = 0.000275, f(21) = 0.000181,
  f(25) = 0.000079, f(27) = 0.000029, f(28) = 0.000028 (errors 0.000004–0.000019; table below). The deficits of
  several loops add. The deficit is per cell: tubes of one girth at 66, 72 and 84 cells (loop² 12), 72 and 84 (13,
  16), 63, 72 and 90 (9) agree with the one f per loop length within 1.4σ (errors ± 0.00001–0.00002). The tube's discount per cell is **κ f(q) with κ = 1.85 ± 0.07** fixed
  on loop² 12 and 16; it then gives loop² 13 as 0.00298 ± 0.00012 against the measured 0.00262 ± 0.00034 (−1.0σ)
  and 19 as 0.00051 ± 0.00003 against −0.00034 ± 0.00120 (−0.7σ). Two girths fix κ, two are forecast, and the 19
  forecast is weak because the price at 19 is poorly known.
- **Only the differences follow, not the open price.** κ ρ∞ = 0.96, against 0.2086: the relation has a large
  intercept. As an elasticity, the price moves 4.6 times as much in relative terms as the density.
- **The density effect does not end between 19 and 21 [measured].** f falls smoothly, about as e^(−2.3|v|) (|v| in
  lattice units, |v|² = loop²): f(21)/f(19) = 0.67, f(21) = 0.000180 ± 0.000004 is 45σ from zero, f(25) is 20σ
  from zero, f(27) and f(28) 5σ. The exact neighbourhood has no feature there either (next section). By the
  relation, a loop of 21 costs 0.00033 per cell and one of 25 0.00015: below what the lifetimes on file resolve (the
  19-tube slope is ± 0.0012; the no-short-loop faces give κ = 1.9 ± 0.9 for their own long loops, consistent with
  1.85 and 2σ from 0, `pricefit.py`). So "the effect ends between 19 and 21" reads, from the living state, as "the
  effect falls below the resolution of the lifetimes there"; it is not a threshold [fitted; the lifetime side is
  not settled, see "Where to go next"].
- **Loop² 9 breaks the relation [measured].** Its density deficit is per cell (63–90 cells, once transverse
  firewalls are detected) and gives a price of 0.1970 ± 0.0005; the loop² 9 tube's lifetimes are curved instead
  (local slopes 0.200, 0.198, 0.1955, 0.1927 from 45 to 81 cells; 0.1944 ± 0.0005 over 63–81, run here), so the
  relation holds near 60 cells and fails by 0.0026 (−3.7σ) over 63–81. These tubes die mostly by transverse
  firewalls (6.5 firewalls per face death at 72 cells, 41 at 81), a channel the longer tubes do not have.
- **What does not track it [measured].** The birth (= death) rate of the face layer and the interior activity have
  the wrong loop-length profile: f(16)/f(12) = 0.12 ± 0.01 and 0.15 ± 0.03, against the price's 0.344 ± 0.036 (−6σ,
  −5σ). The face population's variance per cell has 0.439 ± 0.008 (+2.6σ) and a relative size 3.2 times the
  price's (6.5% against 2.0% at loop² 12); the interior density 0.474 ± 0.012 (+3.5σ). The equal-time correlation of
  a cell with the cell one loop vector away, on an open 147-cell torus, is below 10⁻⁴ at every loop length from 9
  to 28 and not resolved (± 1.5 × 10⁻⁵): the deficit is not a static image correlation. Statistics with the
  density's profile: dead face cells' mean live-neighbour count (in-layer and total), the share of live face cells
  with 3–5 live neighbours, the in-layer perpendicular-pair covariance — all, like the density, measures of
  occupation rather than of turnover.

## The neighbourhood, exactly [proved by enumeration]

`python3 research/wraplocal/nbhd.py` → `data/nbhd_out.txt` (1 s). In-plane lattice units: the translation (X, Y)
of research/wrap (cube offset (X, Y, −X−Y), |v|² = X² + XY + Y²).

- Of a face cell's 12 neighbours, 6 lie in its own layer: the 4 perpendicular ones (kagome nearest neighbours, at
  half a lattice vector) and the 2 coplanar ones, which are its own translates by ±1 lattice vector along one
  direction that depends on the sublattice (axis 0: (0,1), axis 1: (1,0), axis 2: (1,−1)). Of the other 6, 2 lie
  one layer in, 1 two layers in, and 3 outside the slab (dead). An interior cell has 6 in-layer neighbours and
  2 + 1 on each side.
- Graph distance d_a(w) from a cell of axis a to its own translate by a loop vector w, in the slab (shortest walks
  counted in the table); for every w with |w|² ≤ 31 it equals the distance within the face layer alone:

  | loop² | w | d_a, a = 0, 1, 2 | |w| |
  |---:|---|---|---:|
  | 1 | (0,1) | 1, 2, 2 | 1 |
  | 3 | (1,1) | 3, 3, 3 | 1.73 |
  | 4 | (0,2) | 2, 4, 4 | 2 |
  | 7 | (1,2) | 4, 5, 4 | 2.65 |
  | 9 | (0,3) | 3, 5, 5 | 3 |
  | 12 | (2,2) | 6, 6, 6 | 3.46 |
  | 13 | (1,3) | 5, 6, 5 | 3.61 |
  | 16 | (0,4) | 4, 6, 6 | 4 |
  | 19 | (2,3) | 7, 7, 7 | 4.36 |
  | 21 | (1,4) | 6, 7, 6 | 4.58 |
  | 25 | (0,5) | 5, 7, 7 | 5 |
  | 27 | (3,3) | 8, 8, 8 | 5.20 |
  | 28 | (2,4) | 8, 8, 8 | 5.29 |

  A cell is its own neighbour only at loop² 1 (one sublattice); it shares a neighbour with itself
  only at loop² 1 and 4; it meets itself in three steps only at loop² 3 and 9 (one sublattice). From loop² 12 on
  every distance is ≥ 4.
- **Consequence.** No count of this kind separates {12, 13, 16, 19} from {21, 25, …}: the graph distance is not
  monotone in |w| (a loop of 19 is 7 steps for every cell, a loop of 21 or 25 is 6 or 5 steps for two sublattices or
  one, a loop of 16 is 4 steps for one). If the price followed the shortest self-encounter, a loop of 21 or 25 would
  cost about as much as one of 12 or 13. Both the price and the density deficit follow the Euclidean length |w|
  instead. [proved: the table; the comparison with the price is by inspection]

## The living state: how it was measured

- **Stepper** (`live.py`): bit-sliced numpy, 64 replicas per word, on the 8-layer slab graph of research/wrap (the
  vessel files of research/audit/shape/ts.py, which `research/wrap/validate.py` checks against the oracle).
  `python3 research/wraplocal/live.py check 1 4 24 1500`: replica 0 equals `reference/oracle.py` on the cubic
  24-torus as a set of cells at every one of 1,500 generations, and a replica in another word equals its own
  single-replica run (MATCH; 13 s). Only this one torus was checked this way; the others use the same code on
  vessel graphs that research/wrap validated (all its tori) or that `validate.py` checked here ((1,7,24), (1,8,27)).
- **Runs** (`prod.sh`): per torus two seeds × 2,048 replicas from independent 0.4 soups, 500 generations burn-in,
  4,000 measured; a replica is dropped from the generation either face layer is empty (437 drops in all, most on the
  short-lived loop² 9 and 63–66-cell tubes). Errors are the scatter of 8 independent blocks of 512 replicas. About
  45 s of one core per seed at 72 cells; 64 runs ≈ 50 minutes. Transverse firewalls were *not* detected in these
  runs (see loop² 9).
- **Reduction** (`ana.py`, `dens.py`): per-torus statistics; the image-sum fit (IMG above, linear least squares,
  free f per loop length ≤ 37, weights from the block errors). `python3 research/wraplocal/dens.py rho_face --price`
  → `data/dens_rho_face.txt`; `python3 research/wraplocal/dens.py --ratios` → `data/ratios.txt` (17 statistics);
  `python3 research/wraplocal/ana.py --all` → `data/ana_all_out.txt` (every statistic, every torus).

Tori (h, k, d), loops² ≤ 39: tubes 12: (1,5,22) 66, (2,2,12) 72, (1,12,28) 84; 13: (1,3,24) 72, (1,3,28) 84;
16: (1,5,24) 72, (1,7,28) 84; 19: (1,4,22) 66 [19,21,28], (1,4,23) 69 [19,21], (1,9,24) 72 [19,27,28], (1,5,28) 84;
long loops only: (1,4,21) 63 [21×3], (1,4,24) 72 [21×2], (1,4,25) 75 [21,25], (5,0,5) 75 [25×3], (3,3,9) 81 [27×3],
(1,4,28) 84 [21,28], (2,4,14) 84 [28×3], (1,4,34) 102 [21], (1,6,35) 105 [25], (6,0,6) 108 [36×3], (1,6,38) 114
[28], (1,6,39) 117 [27], (1,18,49) 147 [none ≤ 48]; loop² 9: (1,6,21) 63, (1,7,24) 72, (1,10,30) 90.

## Numbers

Face density deficit per loop direction (`data/dens_rho_face.txt`) and the profile of each statistic,
f(q)/f(12), against the price discount's profile (`data/ratios.txt`; price: 13: 0.614 ± 0.084, 16: 0.344 ± 0.036,
19: −0.08 ± 0.28; loop² 9 at 63–81 cells: 3.3, at 54–63: 2.5):

| statistic | value at ρ∞ | f(12)/value | f(9)/f(12) | f(13)/f(12) | f(16)/f(12) | f(19)/f(12) | f(21)/f(12) | f(25)/f(12) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| face density | 0.517742 | 0.448% | 2.705 ± 0.012 | 0.693 ± 0.007 | 0.332 ± 0.008 | 0.119 ± 0.004 | 0.078 ± 0.002 | 0.034 ± 0.002 |
| dead face cell, mean live in-layer neighbours | 3.0175 | 0.76% | 3.06 | 0.722 | 0.350 | 0.127 | 0.081 | 0.039 |
| live face cells with 3–5 live neighbours | 0.31956 | 0.54% | 2.03 | 0.688 | 0.397 | 0.114 | 0.077 | 0.038 |
| in-layer perpendicular pair covariance | 0.011012 | −7.2% | 2.95 | 0.744 | 0.341 | 0.115 | 0.086 | 0.032 |
| face births per cell per generation | 0.198191 | 0.31% | 4.54 | 0.697 | **0.122 ± 0.013** | 0.136 | 0.084 | 0.029 |
| interior activity | 0.414974 | 0.10% | 3.26 | 0.802 | **0.146 ± 0.029** | 0.138 | 0.071 | 0.023 |
| interior density | 0.418775 | 0.12% | 2.47 | 0.731 | 0.477 ± 0.012 | 0.137 | 0.095 | 0.036 |
| face population variance per cell | 0.37767 | −6.5% | 2.26 | 0.777 | 0.439 ± 0.008 | 0.199 | 0.131 | 0.057 |

(The signs: a short loop lowers density, births and activity, and raises the variance and the in-layer covariance.)
Every statistic tried falls in the order 12 > 13 > 16 > 19 > 21 > 25, and none has a break between 19 and 21.

Price relation (`dens.py rho_face --price`): κ = 1.854 ± 0.073 from the slopes of loop² 12 and 16.

| loop² | measured discount per cell | κ f(q) | (m − f)/σ |
|---:|---:|---:|---:|
| 12 | 0.00427 ± 0.00018 | 0.00430 ± 0.00017 | −0.1 (fit) |
| 9 | 0.0142 ± 0.0005 (63–81 cells; curved) | 0.0116 ± 0.0005 | −3.7 (forecast after F6, see below) |
| 13 | 0.00262 ± 0.00034 | 0.00298 ± 0.00012 | −1.0 (forecast) |
| 16 | 0.00147 ± 0.00014 | 0.00142 ± 0.00007 | +0.3 (fit) |
| 19 | −0.00034 ± 0.00120 | 0.00051 ± 0.00003 | −0.7 (forecast) |
| 21 | — | 0.00033 ± 0.00002 | |
| 25 | — | 0.00015 ± 0.00001 | |
| 27, 28 | — | 0.00005 ± 0.00001 | |

**The long loops in the lifetimes on file** (`python3 research/wraplocal/pricefit.py` → `data/pricefit_out.txt`).
The 14 faces with no loop² ≤ 20 (63–126 cells) all carry loops of 21–31, three each for the precise equilateral ones
(63: 21×3; 75: 25×3; 81: 27×3; 84: 28×3; 93: 31×3), fewer and longer as the area grows. A straight line fits them
with χ² 17.4 on 12; the line with the density's discounts subtracted (κ = 1.9, the tube lines' meeting point A0 =
30 cells) fits with 16.2 (A0 = 20: 21.5; 40: 13.2); κ free gives 1.94 ± 0.94 (A0 = 40). The lifetimes on file
cannot tell. If the relation holds, the price of a face with no loop at all is about 0.2075 (A0 = 30), not 0.2086,
and the open line bends down: forecasts in `data/pricefit_out.txt`, e.g. (6,0,6) at 108 cells 22.535 against
22.551 on the straight line, (1,16,39) at 117 cells 24.403 against 24.429.

## Loop² 9

- **Density [measured].** With replicas dropped at a transverse firewall (three consecutive empty transverse
  layers, `live.py run … --fw`), the face density of the loop² 9 tubes is 0.511504 ± 0.000016 (63 cells),
  0.511466 ± 0.000009 (72), 0.511462 ± 0.000008 (90): per cell, f(9) = 0.006267 ± 0.000008, f(9)/f(12) = 2.70.
  Without firewall detection (the first production runs, kept in `research/scratch/wraplocal/nofw/`) the same tubes
  read 0.0013–0.0023 lower, drifting with area and with ten times the block scatter: 2–3% of the replicas pass a
  firewall in a 4,500-generation window. The (1,12,28) tube rerun with detection is unchanged (0 firewalls).
- **Lifetimes [measured; one code, ts3, validated on both tori here].** `python3 research/wrap/validate.py 1 7 24 1500`
  and `1 8 27 1500`: MATCH. `python3 research/wraplocal/tsjob.py job 1 7 24 22000000 309001` (7 min) and
  `job 1 8 27 100000000 309002` (26 min) → `data/runs9.csv`, `data/runs9_table.txt`:

  | torus | cells | face deaths F | firewalls W | ln τ_face |
  |---|---:|---:|---:|---:|
  | (1,6,21), research/shape3 (on file) | 63 | 495,056 | 484,881 | 12.8588 ± 0.0014 |
  | (1,7,24) | 72 | 10,086 | 65,093 | 14.6191 ± 0.0100 |
  | (1,8,27) | 81 | 8,090 | 333,463 | 16.3538 ± 0.0111 |

  The 72-cell value agrees with the GPU slab value on file for the same area (14.6214 ± 0.0029). A line through
  63–81: slope **0.19444 ± 0.00054** (χ² 1.2 on 1); local slopes 0.1955 ± 0.0011 (63–72), 0.1927 ± 0.0017 (72–81).
  With the file's 45–63 values (0.200, 0.198) the loop² 9 tube's price per cell falls with its length, unlike the
  tubes of 12–16; its density per cell does not.
- **F6 as frozen passes** (0.1944 ± 0.0005 against 0.1947 ± 0.0010), **but for the wrong reason**: it used the
  pilot's f(9) = 0.00737, which was firewall-contaminated. With the clean f(9) the relation gives 0.1970 ± 0.0005,
  3.7σ above the 63–81 slope and close to the 54–63 one. At loop² 9 the density gives the price near 60 cells and
  not its fall with length.

## Forecasts (written before any living-state statistic was measured) and scores

The exact neighbourhood table had been computed when F1–F5 were written; no stepping had been run.

| forecast | | outcome |
|---|---|---|
| **F1 (60%)** face density on a loop² 12 tube differs from a no-short-loop torus by > 5 SE | | **passes**: 0.00231, about 100 SE |
| **F2 (50%)** variance per cell larger on tubes, ordered as the prices, relative excess within a factor 2 of the price discount | | **fails** the last part: ordered, but 6.5% against 2.0% (factor 3.2), and its 16/12 profile is 2.6σ off |
| **F3 (35%)** one statistic, one parameter fixed on 12 and 16, forecasts 13 within 0.00066 | | **passes** (density: off by 0.00035). Seventeen statistics were tried; the density was the one named in F1, and the others of its family pass too |
| **F4 (60%)** on an open torus \|C(w)\| ordered 12 > 13 > 16 > 19 > 21 | | **fails**: not resolved at any loop length (all < 10⁻⁴, errors 1.5 × 10⁻⁵, no order) |
| **F5 (70%)** a loop² 9 tube's price is more than 2.0% below the open price | | **passes on the data on file** (local slopes 0.200 at 45–54 and 0.198 at 54–63 cells, 4–5% below; these were on file but not looked at when F5 was written) |
| **F6 (35%)** loop² 9 slope 63–81 cells within 2σ of 0.1947 ± 0.0010 | | **passes as frozen** (0.1944 ± 0.0005), by luck: the frozen f(9) was firewall-contaminated; the clean value misses by 3.7σ (section Loop² 9) |

The lead's forecasts (`research/wrap/PREDICTIONS.md`, end), scored here for the lead to overrule:

| forecast | outcome |
|---|---|
| **L1 (70%)** a one-point or nearest-pair statistic differs between a loop² 12 tube and a no-short-loop torus by > 5 SE | **passes** (density 100 SE; births, pair covariances, neighbour counts 30–200 SE) |
| **L2 (55%)** that difference ordered 12 > 13 > 16 > 19 and zero within error at 21 | **fails on its second half**: ordered, but at 21 it is 45 SE from zero (f(21) = 0.000180 ± 0.000004) |
| **L3 (30%)** a one-parameter relation fixed on 12 and 16 forecasts 13 within 0.00066 | **passes** (density: 0.00297 against 0.00262 ± 0.00034) |
| **L4 (30%)** the end between 19 and 21 comes out as an exact statement about the neighbourhood, checked on an unmeasured loop | **fails**: the exact counts have no feature there (table above), and the living state has no end there either |
| **L5 (35%)** nothing local tracks it | **fails** |

## Not checked

- The stepper was checked against the oracle on one torus ((1,4,24)); the other tori use the same code on graphs
  validated by research/wrap (or here by `validate.py`). No second code measured any statistic.
- Transverse firewalls were detected only in the loop² 9 runs and one control ((1,12,28)). On tubes of loop² ≥ 12
  research/wrap's lifetime runs saw 0–30 firewalls per 10⁴–10⁵ face deaths, so in a 4,500-generation window they
  are negligible; not counted here.
- A negative control for `live.py check` (a broken rule or neighbour entry must fail) was not run.
- Burn-in: 500 generations from a 0.4 soup; not varied. A pilot with 300 generations and 3,000 measured
  (`pilot.sh`, 2 blocks per torus) agrees with production to 2–3 × 10⁻⁵, which is inside the pilot's (underestimated)
  errors; a slow transient of that size is not excluded.
- The price side is the lead's tube lines (CLAIMS WL3) taken as given; the companion loops of the tubes (second
  loops ≥ 21, which change with the tube's length) were not corrected for in the slopes, nor in κ.
- Space-time correlations (a cell with its translate by w some generations later) were not measured; the equal-time
  one is unresolved, so whatever carries the deficit round the loop is dynamical and is not identified here.
- Why κ ≈ 1.9, and why the density rather than the turnover: not explained.

## Where to go next

- **Decide the long loops in the lifetimes.** The density relation says a loop of 21 costs 0.00033 per cell and
  the open price is ≈ 0.2075 rather than 0.2086; the line on file says neither. The deciding faces are the
  equilateral ones without loops below 36: (6,0,6) at 108 cells (forecast 22.529 against 22.551, card value on file
  22.560 ± 0.022) and (1,16,39) at 117 cells (24.396 against 24.429) to ± 0.008, or a single loop of 21 at large area,
  (1,4,34) at 102 cells against (1,10,37)-type faces. GPU work.
- Measure the price of tubes of 21 and 25 directly at long length ((1,4,34), (1,4,38), (1,6,35), (1,7,40)); the
  relation gives slopes 0.2083 and 0.2085 against an open 0.2086, so ± 0.0001 per cell is needed: very long runs.
- Space-time correlation C(w, τ) on an open torus, to find what travels round the loop (speed ≤ 1 lattice unit per
  generation along a kagome line, so a loop of 12 is felt after 6 generations at the earliest).
- Why the loop² 9 tube's price per cell falls with its length while its density does not: the firewall channel
  (W/F = 1 at 63 cells, 6.5 at 72, 41 at 81) is the obvious suspect; the face hazard of lives near a firewall
  was not looked at.
