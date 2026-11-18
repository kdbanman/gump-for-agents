# WRAPPED.md: where the 0.022 per cell between rimmed and wrapped faces lives (ref-hull, 06:10 UTC, 2026-11-18)

**Answer.** It lives mostly in what follows the dip, and in the last stretch of it: on wide wrapped faces −ln q(0.6)
grows by 0.157 per cell (63–108 cells; 0.158 then 0.156, not quite a straight line) against the hull's 0.170, the
same deficit of 0.013 shows at 0.5 P̄ and 0.4 P̄ while the stretch from 0.6 P̄ to 0.4 P̄ costs 0.051 per cell on both,
so the difference sits below 0.4 P̄; the remaining 0.008 is in the hull's rim-carrying dip term (0.059·A − 0.31·k
against the torus's 0.051 per cell), the part whose curvature is already drifting down. A wrapped face in fact dips
LESS often than a hull face of the same area (by 0.26, 0.37, 0.53 in ln ν(0.6 P̄) at 63, 84, 108 cells) and dies
sooner only because its dips are 2 to 3.8 times more often fatal, and they are a different event: 11–24% of its dips
to 0.6 P̄, 40–48% of those to 0.4 P̄ and two thirds of those to 0.2 P̄ come within 3 generations of an over-full
face (P ≥ 0.7·A), against 1–3% at every depth on the hull, and 71% of its DEATHS at 63 cells come within 10
generations of one (chance 5%), against 5% on the hull face of 63 cells (chance 3%); a tube's discount is the opposite case, all in ν and
twice over (tubes reach 0.4–0.5 P̄ e^0.46 and e^0.85 times more often than a wide face at 84 and 108 cells, and
those dips are less often fatal by 0.24 and 0.47).

Everything below is **[measured]** unless marked; the lifetimes are the anchors', taken as given.

## Stepper and validation

`sl.c` (written from `reference/oracle.py` and `docs/AUTOMATON.md`; shares the bit-sliced kernel of `rh.c`): cells
with one odd doubled coordinate and x+y+z ∈ {−7 … 7}, outside dead; in-plane basis e1 = (2,−2,0), e2 = (2,0,−2)
(60° apart, |a e1 + b e2|² ∝ a² + ab + b²), periods H·e1 + K·e2 and D·e2; 24·H·D cells, 3·H·D per face; faces are
the layers x+y+z = ±7. `gcc -O3 -march=native -o sl sl.c -lm`.

    python3 validate_slab.py 12 0 12 1 1200 0 3   # PASSED: 3 lanes x 1,200 generations = the oracle on the cubic torus of side 24
    python3 validate_slab.py 12 0 12 1 1200 1 3   # negative control (one neighbour swapped): FAILS at generation 3-4
    python3 validate_slab.py 1 4 21 2 1000 0 1    # PASSED: skew torus (1,4),(0,21) against the oracle on its 21-fold cover (side 42)

(The oracle knows only cubic tori; a cube of side 2n holds the slab torus (n,0),(0,n) with n − 8 dead layers. A
skew lattice containing (n,0),(0,n) is checked on that cover, all copies compared. Output: `out/validation_slab.txt`.)
Further checks from the runs themselves: P̄/A = 0.51772 on (6,0),(0,6) and 0.51720 on (1,4),(0,21) (on file:
ρ∞ = 0.517742, minus 3·f(21) = 0.00054); brute-force lifetimes ln(2E/D) = 11.876 ± 0.009 (11,356 first deaths),
13.161 ± 0.018, 15.66 ± 0.07, tube 84: 17.32 ± 0.16 against anchors 11.8751, 13.1622, 15.6442, 17.3175.

## Dip rates (plain running, both faces, same definitions as for the hull)

`sh wchain.sh DIR; python3 wnu.py DIR` (rows kept in `out/w/`: `python3 wnu.py out/w` gives `out/W-ANALYSIS.txt`).
256 slabs, soups 0.35, a slab replaced when a face is empty, ageing-in 200, λ_A = ⌈P̄⌉ from a pilot, 8 seeds,
1.2–1.6 × 10⁹ face-generations per torus; ln ν(p·P̄) interpolated linearly in the level; errors from seeds.

| torus | cells | P̄/A | ln τ (anchor) | −ln ν: 0.8 | 0.7 | 0.6 | 0.5 | 0.4 |
|---|---:|---|---|---|---|---|---|---|
| (1,7),(0,19) | 57 | 0.51661 | 11.8751 | 2.6324 | 3.6726 | 4.9119 | 6.2227 | 7.4972 |
| (1,4),(0,21) | 63 | 0.51720 | 13.1622 | 2.7061 | 3.8451 | 5.2216 | 6.6935 | 8.1390 |
| (1,9),(0,25) | 75 | 0.51740 | 15.6442 | 2.8758 | 4.1944 | 5.8075 | 7.5762 | 9.359 |
| (1,4),(0,28) | 84 | 0.51754 | 17.5387 | 3.0093 | 4.4668 | 6.2708 | 8.2682 | 10.288 ± 0.006 |
| (6,0),(0,6) | 108 | 0.51772 | 22.5405 | 3.3432 | 5.1942 | 7.5367 ± 0.0013 | 10.140 ± 0.005 | 12.735 ± 0.020 |
| tube (1,12),(0,28) | 84 | 0.51542 | 17.3175 | 3.0006 | 4.3321 | 5.9541 | 7.8104 | 9.825 ± 0.004 |
| tube (1,17),(0,32) | 96 | 0.51542 | 19.7446 | 3.1540 | 4.6418 | 6.4648 | 8.5553 | 10.848 ± 0.007 |
| tube (1,16),(0,36) | 108 | 0.51543 | 22.1599 | 3.3053 | 4.9483 | 6.9736 | 9.304 ± 0.003 | 11.864 ± 0.011 |
| hull R = 11, 13, 15 | 63, 84, 108 | 0.496, 0.505, 0.511 | 13.633, 18.141, 23.339 | | | 4.966, 5.898, 7.010 | 6.241, 7.678, 9.367 | 7.660, 9.664, 11.997 |

(Errors not shown are below 0.002. The 48-cell torus (4,0),(0,4) is excluded: my runs give ln(2E/D) = 9.942 ± 0.004
against the anchor 9.9251 and P̄/A = 0.5093, 0.006 below what its loops predict; about 1.7% of the exposure seems
to be slabs that froze with both faces occupied [conjectured, not verified], which corrupts P̄ and ν there.)

## 1. Is −ln q a straight line in the area on wide faces, and with what slope?

−ln q(p) = ln τ + ln ν(p P̄) on the three cleanest wide tori (63, 84, 108 cells), slope per cell on 63–84 and 84–108:

| p | −ln q at 63, 84, 108 | torus slopes | hull slopes (same intervals) | hull − torus | −ln ν slopes, torus | −ln ν slopes, hull |
|---|---|---|---|---|---|---|
| 0.8 | 10.456 14.529 19.197 | 0.1940, 0.1945 | (no line on the hull) | | 0.0144, 0.0139 | |
| 0.7 | 9.317 13.072 17.346 | 0.1788, 0.1781 | (0.1901, 0.1904) | 0.012 | 0.0296, 0.0303 | |
| 0.6 | 7.941 11.268 15.004 | 0.1584, 0.1557 | 0.1703, 0.1702 | 0.012, 0.015 | 0.0500, 0.0527 | 0.0444, 0.0463 |
| 0.5 | 6.469 9.270 12.400 | 0.1334, 0.1304 | 0.1462, 0.1462 | 0.013, 0.016 | 0.0750, 0.0780 | 0.0685, 0.0704 |
| 0.4 | 5.023 7.251 9.806 | 0.1061, 0.1065 | 0.1192, 0.1194 | 0.013, 0.013 | 0.1023, 0.1019 | 0.0954, 0.0972 |

- Slope errors are 0.0002–0.0004 (anchors), so at 0.6 and 0.5 the torus's −ln q is concave by 0.003 per cell (7 and
  5 errors) and −ln ν convex by the same amount; ln τ itself is straight (0.2084, 0.2084). At 0.8, 0.7 and 0.4 both
  are straight. With the 57- and 75-cell tori (loops² 19) the picture is the same but noisier in shape:
  −ln q(0.6) = 6.963, 7.941, 9.837, 11.268, 15.004 at 57, 63, 75, 84, 108. So: **a line to about 2% in slope, slope
  0.157 at p = 0.6, against the hull's 0.170.**
- The stretch between 0.6 P̄ and 0.4 P̄ costs the same on both: (−ln ν(0.4)) − (−ln ν(0.6)) grows by 0.0507 per cell
  on the torus and 0.0510 on the hull (63–108 cells). **The hull's extra 0.013 per cell in q is therefore below
  0.4 P̄**, in the final emptying.
- The dip part: −ln ν(0.6 P̄) on wide tori has slope 0.050–0.053 per cell. The hull's is 0.044–0.046 at the same
  sizes, i.e. its 0.059·A − 0.31·k; the hull's second difference/3 falls from 0.059 to 0.053 by R = 19 (REVIEW.md),
  toward the torus's value.
- Bookkeeping of the 0.022 (0.231 − 0.2087, coefficients of the area): 0.170 − 0.157 = 0.013 in q, 0.059 − 0.051 =
  0.008 in the dip term. In marginal prices at 84–108 cells (0.2166 against 0.2084) it is +0.015 in q and −0.006 in ν.

## 2. More dips, or deadlier dips? And what the decomposition means on a wrapped face

At equal area (63, 84, 108 cells), hull minus wide torus:

| p | −ln ν (negative: the hull dips more often) | −ln q (positive: the hull's dip is less often fatal) | ln τ |
|---|---|---|---|
| 0.6 | −0.256, −0.373, −0.527 | +0.726, +0.976, +1.326 | +0.471, +0.602, +0.799 |
| 0.5 | −0.453, −0.590, −0.773 | +0.923, +1.193, +1.572 | |
| 0.4 | −0.479, −0.624, −0.737 | +0.950, +1.226, +1.536 | |

**The wrapped face is cheaper because its dips are deadlier, not because it dips more.** The same at equal ABSOLUTE
level L = x·A (`python3 samelevel.py`, `out/SAMELEVEL.txt`; the hull's P̄/A is 1–4% lower than the torus's): at
x = 0.31 the hull dips more often by 0.55, 0.61, 0.70 and its dip is less often fatal by 1.02, 1.22, 1.50 (63, 84,
108 cells); at x = 0.21 by 0.73, 0.83, 0.88 and 1.21, 1.43, 1.68. Slopes of −ln q per cell at fixed x, hull against
torus: 0.187 / 0.177 (x = 0.36), 0.167 / 0.157 (0.31), 0.144 / 0.132 (0.26), 0.118 / 0.108 (0.21): the hull's
q is dearer by 0.010–0.012 per cell at every level down to 0.21·A, so the difference is below that.

Share of first passages that come within 3 generations of an over-full face (P ≥ 0.7·A), by depth
(`wnu.py` PART 4; hull: `./rh nu R SEED 120000 LAMA | grep NUB`, 6 seeds each at R = 11, 13, 15):

| vessel | cells | at 0.8 P̄ | 0.6 P̄ | 0.4 P̄ | 0.2 P̄ |
|---|---:|---|---|---|---|
| wide torus | 63 | 6.1% | 23.8% | 47.7% | 62.6% |
| wide torus | 84 | 4.2% | 17.1% | 47.5% | 65% (386/595) |
| wide torus | 108 | 1.4% | 10.8% | 40.1% (1,219/3,039) | |
| tube | 84 | 4.0% | 14.5% | 32.2% | 55% (439/798) |
| tube | 96 | 1.7% | 8.0% | 23.8% | 49% (65/132) |
| tube | 108 | 1.3% | 6.2% | 19.2% | 28% (10/36) |
| hull | 63 | 1.7% | 2.0% | 2.7% | 2.7% |
| hull | 84 | 1.2% | 1.6% | 2.5% | 2.5% (24/958) |
| hull | 108 | 0.4% | 0.7% | 1.6% (142/8,784) | |

(An over-full face occurs in 0.5%, 0.24%, 0.06% of face-generations on the wide tori of 63, 84, 108 cells, so
chance would give 1.5%, 0.7%, 0.2%.) Reading:
- On the hull a dip is never the rebound of a bust (the share is chance-like and does not grow with depth; `anatomy`
  found 1.6–2.2% among deaths). On a wide torus the deeper the dip, the more likely it is the down-stroke of an
  over-fill: a bust-preceded dip to 0.6 P̄ goes on to 0.4 P̄ 4.4 times (84 cells) to 5.5 times (108) more often than
  a plain one.
**Deaths** (`python3 win.py out/win`; window W as last argument of `sl nu` / `rh nu`; 4 seeds each): share of first
deaths of a face that come within W generations of an over-full face, and the share chance alone would give
(1 − (1 − r)^W, r the rate of over-full face-generations):

| vessel | cells | r | W = 6 | W = 10 | W = 20 |
|---|---:|---|---|---|---|
| wide torus (1,7),(0,19) | 57 | 1.2e-2 | 61.7% (chance 6.8%) | 76.0% (11%) of 4,348 | 82% (21%) |
| wide torus (1,4),(0,21) | 63 | 4.9e-3 | 57.7% (2.9%) | **71.3% (4.8%) of 1,494** | 74% (9.3%) |
| hull R = 9 | 45 | 9.1e-3 | 3.9% (5.3%) | 7.4% (8.7%) of 40,720 | 13.9% (16.6%) |
| hull R = 11 | 63 | 3.1e-3 | 2.7% (1.8%) | **5.3% (3.1%) of 2,447** | 9% (6%) |

At least seven wrapped deaths in ten are the end of a bust that began with an over-full face at most ten generations
earlier; on the hull the share is at chance (below it at 45 cells). An over-full face is still far from fatal: at 63
cells about 0.7 × e^−13.16 / 4.9e-3 = 3 × 10⁻⁴ of over-full face-generations end in death.

- So on a wrapped face ν(0.6)·q(0.6) is a mixture of two events with different odds, and "−ln q" is not "what
  follows a dip": for most deep dips the attempt began one to three generations earlier, going UP. They should be
  counted separately. The honest decomposition for a wrapped face is rate of over-full generations × chance that
  one ends in death (3 × 10⁻⁴ at 63 cells for the threshold 0.7·A), plus the plain route (at most 29% of deaths at
  63 cells); I did not measure how the two factors scale with the area, nor a better threshold than 0.7·A.
- [conjectured] The rim is what removes the bust route on the hull (a fuller rim row, empty corners: the face
  cannot over-fill and crash as one), and the hull pays for it below 0.4 P̄, where its q-slope is 0.013 per cell
  dearer; that is the durable part of "two prices".

## 3. Tubes against wide faces of the same area

Discount of the tube (wide minus tube), split at each level:

| cells | ln τ discount | level | in −ln ν (tube dips more often) | in −ln q |
|---:|---|---|---|---|
| 84 | 0.221 ± 0.004 | 0.8 | +0.009 | +0.213 |
| | | 0.7 | +0.135 | +0.087 |
| | | 0.6 | +0.317 ± 0.001 | −0.096 ± 0.005 |
| | | 0.5 | +0.458 ± 0.002 | −0.237 ± 0.005 |
| | | 0.4 | +0.463 ± 0.007 | −0.242 ± 0.008 |
| 108 | 0.381 ± 0.014 | 0.8 | +0.038 | +0.343 |
| | | 0.7 | +0.246 | +0.135 |
| | | 0.6 | +0.563 ± 0.002 | −0.183 ± 0.014 |
| | | 0.5 | +0.837 ± 0.006 | −0.456 ± 0.015 |
| | | 0.4 | +0.871 ± 0.023 | −0.490 ± 0.027 |

**The tube's discount sits in ν, and ν over-pays it by a factor two.** The tube's extra dips build up between
0.8 P̄ and 0.5 P̄ and stop growing below (0.458 → 0.463; 0.837 → 0.871): getting a tube down to half its population
is cheaper by 0.46 (84 cells) and 0.85 (108), and from there it is harder to finish than a wide face by 0.24 and
0.47–0.49. The tube's extra dips are not busts (share at 0.4 P̄: 19–32% against 40–48% on wide faces).
[conjectured] This is what a band emptied around the short loop would look like: cheap to open, then two straight
fronts that still have to be pushed across the rest.

## Not checked

- The anchors (taken as given), and whether the anchors' protocol matches mine exactly at 48 cells (it does at 57–84
  to within my brute-force errors). The 48-cell torus is not used.
- Other thresholds than 0.7·A for "over-full" (its integer rounding differs between sizes); the share of deaths
  that follow an over-full face above 63 cells (no deaths in plain running there); how the rate of over-full
  generations and their lethality scale with the area.
- Wide tori above 108 cells and tubes other than loop² 12; (1,9),(0,25) and (1,7),(0,19) are not strictly "wide"
  (loops² 19).
- The slab stepper on the tubes' lattices against the oracle (one skew lattice was checked on its cover).
