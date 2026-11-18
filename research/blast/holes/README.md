# blast/holes: the price of a hole in a living face (agent `holes`, 2026-11-18, second phase)

The question: is the price per cell of a face's lifetime the bulk cost of emptiness in the living state,
−ln P(Ω empty at an instant) = c·|Ω| + σ·|∂Ω| + O(1) with c = 0.2087, and does the hull's 0.231 sit in the rim
rows of the living state? **Answer: no to both, at every size plain running reaches.** Labels: [proved],
[measured], [conjectured]. `S` below is `research/scratch/blast/holes` (binary: `gcc -O3 -march=native -o
$S/holes holes.c -lm`). Full tables: `data/torus_table.txt`, `data/hull_table.txt` (output of `ana.py`);
lifetimes: `data/life.txt`, `data/life_tori.txt`; forecasts: `PREDICTIONS.md`.

## 0. What stands

1. **The bulk cost of a hole is about 0.26 per cell, not 0.2087, and it is flat [measured].** On the 12 × 12 × 8
   torus, the mixed second difference of −ln P over rhombi of a × b unit cells (3ab cells; it removes every term
   that depends on a alone or on b alone, so perimeter and corners), per cell, is 0.2932, 0.2646 ± 0.0002, 0.2543 ± 0.0045 on the diagonal (a = b = 1.5, 2.5, 3.5), 0.2595 ± 0.0005, 0.2592 ±
   0.0019, 0.265 ± 0.010 along a = 2.5 (b = 3.5, 4.5, 5.5), and 0.2575 ± 0.0008, 0.2562 ± 0.0030 at (1.5, 5.5), (1.5,
   6.5): every value with the short side at 2.5 or more, or the long side at 4.5 or more, lies in 0.254–0.265 (6.3·10⁹
   replica-generations; the rim zone of the hull face gives 0.246–0.260, item 4). No value
   reached is inside the PI's 0.195–0.222. The earlier "0.226 at 36 cells, falling into the lifetime range"
   (notebook, 2026-11-15) was the second difference along a × a, a × (a+1), which is not free of the single-variable
   curvature (f(3,4) − 2f(3,3) + f(2,3) = −0.064).
2. **A hole pays more per cell than the death of a closed face of its own shape [measured].** Lifetimes of the
   small closed tori a × b measured with the same stepper (`data/life_tori.txt`) have mixed second differences per
   cell of 0.2148 ± 0.003 at (3.5, 3.5) and 0.226 ± 0.009 at (3.5, 4.5) (errors doubled, section 4); holes of the same shapes (mean of the two
   orientation classes) 0.2586 ± 0.0043 and 0.245 ± 0.026: **dearer by 0.044 ± 0.005 at (3.5, 3.5)**, by 0.016 ±
   0.003 at (2.5, 4.5), by 0.069 at (2.5, 3.5) (there the tori are two units wide, loop² 4, and scatter: 0.193,
   0.244, 0.260). "−ln P(hole) − ln τ(closed torus of that shape)" is not a function of the perimeter alone: at
   perimeter 16 it is 8.77 (2 × 6), 9.42 ± 0.01 (3 × 5), 9.55 ± 0.02 (4 × 4); at 12, 5.90 and 6.65. (For 3 × 6
   against 4 × 5, the PI's pair, it is: 11.00 ± 0.03 and 10.98 ± 0.08.)
3. **The interior of a hull face is a wrapped face to one part in ten thousand per cell [measured].** In the hull
   of radius 29 (faces of side 15, 360 cells) rhombi of 12 to 27 cells with every unit cell three or more rows from
   every rim have the torus's −ln P within 0.001 (2 × 2: −0.0005 ± 0.0001; 2 × 3: −0.0009 ± 0.0003; 3 × 3: −0.001 ± 0.002); two rows
   in, the same (+0.0001, +0.0007, +0.0014 ± 0.0011, 3 × 4: 0.000 ± 0.003); one row in, a 3 × 3 patch is 0.010 ± 0.002
   DEARER (11.995 against 11.985).
4. **The rim zone of the living state carries no surplus [measured].** A patch that touches the rim is CHEAPER:
   3 × 3 on the rim −0.98, in the corner −3.21; a strip against the rim is cheaper than the same rhombus in the
   interior by 0.34, 0.37, 0.40 per unit of rim for 1, 2, 3 rows. The rim row itself costs 0.436 per cell of added
   length (0.547 for a one-row strip in the interior). The cost per cell of each further row, from the mixed
   second difference of strips of w rows by l units against the rim, is at or below the torus value at the same
   (w, l): 0.2500 ± 0.0002 against 0.2618 at (1.5, 4.5), 0.2541 ± 0.0011 against 0.2595 at (2.5, 3.5), 0.2593 ±
   0.0007 against 0.2595 at (3.5, 2.5), 0.254 ± 0.004 against 0.254 ± 0.005 at (3.5, 3.5); every rim value with an
   error under 0.005 lies in 0.247–0.261. (If one charges the strip's one living edge at the torus's 0.43 per unit,
   the rim row alone is dearer than an interior row by about 0.03 per cell: a term per unit of rim, one row deep.)
   The 0.022 between 0.231 and 0.2087 is not in the living state's cost of emptiness near
   the rim.
5. **Hull-face-shaped holes: the rims cooperate [measured].** For an upright triangle of side s (the shape of a
   hull face of 3s(s+1)/2 cells) turning one living edge into a real rim lowers −ln P by 0.86, 1.32, 1.76 (s = 3,
   4, 5); the second edge by 2.21, 2.75, 3.31; and the lifetime of the hull face of that side (all three) lies
   another 0.82, 2.44, 3.67 below the corner triangle, 5.03 ± 0.06 at s = 6 (increments 1.62, 1.23, 1.36 ± 0.06). Edge costs do not add, and "corner
   triangle = hull face + an edge cost linear in s" fails.
6. **How a patch empties: a local boom and bust, deeper than a dying face's [measured].** In the interior 83%,
   71%, 70% of new emptyings of 2 × 2, 3 × 3, 4 × 4 patches contain a one-generation fall of at least half the
   patch's cells ("busts"). In those the patch is **0.826, 0.805, 0.787 full** in the generation before the fall
   (normal 0.517; a dying closed face launches from 0.738) with the cells of the second layer under it at 0.67
   (normal 0.435), and one generation later the patch holds 0.11, 0.13, 0.15 of its cells and the layer beneath
   0.16, 0.13, 0.13; 89%, 96%, 95% of busts start from a patch at least 0.7 full. The launch comes two or three
   generations before the empty instant, so the mean path by lag hides it (3 × 3: 0.52, 0.545, 0.41, 0.13, 0).
   On the rim the bust share is 66%, 50%, 49% (launched from 0.84, 0.81, 0.78 full); in the corner 33%, 23%, 22%
   (from 0.79, 0.78, 0.77): corners mostly fade.
   [conjectured] The extra 0.05 per cell of a hole over a death is the price of the deeper boom: with the
   night's ψ(x) for the frequency of an over-full face (0.075, 0.098, 0.127 per cell at x = 0.73, 0.76, 0.79) a
   launch from 0.79–0.80 costs about 0.05–0.06 per cell more than one from 0.738. A death may leave a tenth of
   the cells to die out over five to seven generations; a hole must be empty at one instant, and its edge is
   retaken at 0.25 units per generation (`tube1d`), so every hole reached here (short side at most 4 units) is all
   edge zone. Whether holes more than 6 to 8 units wide return to 0.2087 cannot be reached by plain running.
7. **A new anchor, and what it does to the formulas [measured; the reading is conjecture].** The 18-cell hull
   face (radius 5): ln τ_face = 4.855 ± 0.015 (`data/life.txt`; the same mode gives 6.808 ± 0.002 (five seeds), 9.824 ±
   0.007, 13.63 ± 0.03 at 30, 45, 63 cells against the anchors 6.804, 9.819, 13.633). The hull's second differences per
   cell are then 0.355, 0.266, 0.231, 0.230 at k = 4…7. The rows formula (a price per row of depth, which makes
   the second difference step every third side) fits the five anchors with χ² 0.02 and misses the 18-cell face by
   0.27. A rim term, one asymptotic price and one geometric transient (formula S, `model.py`) fits all six with
   χ² 0.6 on 1 at a price of **0.223 (0.2175 … 0.227)**; with the price fixed at 0.2087, χ² 6.4 on 2; at 0.2307,
   4.1 on 2.

Frozen forecast (`PREDICTIONS.md`, block B, commit e2e2b6e, before looking at `noisy/`): **135 cells 29.21 ± 0.03,
165 cells 35.75 ± 0.06, 198 cells 42.96 ± 0.11.** These are extrapolations of the anchors (plus the 18-cell face):
the static measurement supplied no number for them.

## 1. Stepper, validation, definitions

`holes.c`: own bit-sliced graph stepper (256 lanes = independent replicas, random soup of density 1/2), written
from `reference/oracle.py` and `docs/AUTOMATON.md`. Vessels: `slab n L` (L `{111}` layers, period lattice
(n,0),(0,n)), `hull R` (octahedron |x|+|y|+|z| ≤ R).

Validation (`validate_log.txt`; `$S/holes val slab 12 8 21 1200 0 F && python3 validate.py F`, `… val hull 29 0 22
1000 0 F`): three lanes compared with the oracle state for state at every generation, slab 12 × 12 × 8 over 1,200
generations and hull R = 29 over 1,000 (the whole oracle array, so a birth outside the vessel would show): identical,
all states distinct. With one swapped neighbour (`NEG = 1`) the comparison fails at generation 3 (slab) and 7
(hull). Hull R = 21 over 1,500 generations: identical. The log is from the binary of the committed source; the two long runs
were made with an earlier build of the same stepper and counters, and the final build reproduces its counts line
for line on short runs of both vessels (same seeds; `T` lines identical).

Counter check: with the two orientation classes averaged as the GPU table did, 2 × 2, 2 × 3, 3 × 3, 3 × 4 read
6.2542, 8.7926, 12.1281, 15.4008 ± 0.0019 against 6.254, 8.793, 12.128, 15.3999/15.3979 on file.

Definitions. A **unit cell** is the three cells of the face layer that are faces of one cube and point out of
the vessel (a kagome triangle); on the hull face (1,1,1) they are (i, j, m) = (⌊x/2⌋, ⌊z/2⌋, ⌊y/2⌋), i + j + m =
k − 1, and i, j, m are the distances in rows from the three rims. A **rhombus a × b** at (I0, J0) is the unit
cells I0 ≤ I < I0 + a, J0 ≤ J < J0 + b; a **triangle of side s** is I ≥ I0, J ≥ J0, I + J ≤ I0 + J0 + s − 1 (a
hull face's shape). **Class P** uses the outward triangles (the only kind that tiles a hull face), **class Q** the
inward ones (the three faces of a cube that point into the vessel); on the torus both exist and P is the likelier
to be empty (2 × 2: 6.160 against 6.358). Hull tables are class P; torus numbers are class P unless said.
f = −ln P(empty at an instant), counted every generation over every translate (torus: 144 positions, two faces)
or by position (hull: 8 faces × 3 rotations, with the mirror image pooled). M(a+½, b+½) = f(a+1, b+1) − f(a+1, b) −
f(a, b+1) + f(a, b). **Errors: delete-one jackknife over the 8 groups of 32 lanes of a run (independent
replicas), never over translates.**

Runs (one each): `$S/holes run slab 12 8 101 56000000 1000 $S/slab12_s101.txt 1` (stopped by hand at 24,640,000 generations ×
256 lanes = 6.3·10⁹ replica-generations; face density 0.51774; no face ever empty) and `$S/holes run hull 29 0 201 10400000 1000
$S/hull29_s201.txt 1` (stopped by hand at 6,240,000 generations × 256 lanes = 1.6·10⁹ replica-generations, 1.3·10¹⁰ face-generations;
face density 0.52195; no face ever empty). A second slab run with the launch recorder (`$S/holes run slab 12 8 102 2400000 1000 F 1`, `data/slab12_launch.txt`)
gives the `busts:` lines of item 6. Tables: `python3 ana.py torus
$S/slab12_s101.txt`, `python3 ana.py hull $S/hull29_s201.txt --torus $S/slab12_s101.txt`. The raw counts are in
`data/slab12_s101.txt` and `data/hull29_s201.txt.gz`; `sh finalize.sh` rebuilds every table of this file from them.
A third, short hull run with the launch recorder: `$S/holes run hull 29 0 202 300000 1000 F 1`
(`data/hull29_launch.txt.gz`, `data/hull_launch_table.txt`). Check on the size of the face: `$S/holes run hull 21 0 203
300000 1000 F 0` (198-cell faces) gives the corner rhombi 1 × 1 … 3 × 4 as 0.5440, 1.9948, 4.0556, 6.0608, 8.775 ± 0.002,
11.519 ± 0.010 and the corner triangles of side 4, 5 as 9.234 ± 0.003, 13.46 ± 0.03: the R = 29 values within 0.01.

## 2. The wide torus [measured]

−ln P of an empty a × b rhombus, class P (the full table, class Q and the hit counts are in `data/torus_table.txt`):

```
-ln P(a x b rhombus empty), class P (outward triangles, the hull kind); a down, b across
  a=1   1.9718±0.0000   3.6260±0.0000   5.2975±0.0000   6.9565±0.0001   8.6081±0.0000  10.2553±0.0001  11.8998±0.0003  13.5418±0.0006
  a=2   6.1598±0.0001   8.6753±0.0001  11.1417±0.0002  13.5786±0.0007  15.9981±0.0026  18.4114±0.0114  20.8134±0.0421
  a=3  11.9849±0.0007  15.2298±0.0022  18.4443±0.0071  21.6599±0.0323  24.7780±0.1325  27.5349±0.6239
  a=4  19.2377±0.0151  23.2513±0.0448  27.5349±0.6239         -               -      
```

Bulk cost per cell, M(a+½, b+½)/3, class P (class Q is 0.001 to 0.005 higher):

```
bulk cost per cell from mixed second differences, M(a+1/2, b+1/2)/3, class P; a down, b across (b >= a)
  a=1.5   0.2932±0.0000   0.2814±0.0000   0.2691±0.0000   0.2618±0.0002   0.2575±0.0008   0.2562±0.0030   0.2533±0.0111
  a=2.5   0.2646±0.0002   0.2595±0.0005   0.2592±0.0019   0.2654±0.0102   0.2350±0.0432   0.1183±0.1896
  a=3.5   0.2543±0.0045   0.2663±0.0156   0.3560±0.2044         -               -      
```

- Along a = 1.5 it falls slowly with the long side; along a = 2.5 it is flat at 0.26 from b = 2.5 to 5.5; the one
  value at a = 3.5 agrees. A geometric continuation of the diagonal (0.2932, 0.2646, 0.2543 ± 0.0045) would end near
  0.25. No torus value with an error under 0.01 is below 0.254. Not reached: any M at a ≥ 4.5 (it needs the 5 × 5 patch, −ln P ≈ 28).
- Perimeter: a strip one unit cell wide costs 1.642 per unit of length (0.547 per cell), two wide 2.413 ± 0.009,
  three wide 3.216 ± 0.03 (last increments reached); with c = 0.26 the edge costs about 0.43 per lattice unit of perimeter (with c = 0.2087 it would be
  0.66: the "0.66 to 0.69 per unit" on file is tied to the assumed bulk price).
- The cost of one more unit of length of a strip keeps falling with the length for strips 2 and 3 wide (2.534,
  2.516, 2.467, 2.437, 2.420, 2.413 for a = 2): the single-variable curvature that made the old estimator fall.
- Triangles of side s, upright (class P): 1.9718, 4.9190, 8.7452, 13.3087 ± 0.0012, 18.563 ± 0.016, 24.4 ± 0.2
  (s = 1…6); their second differences per cell, 0.2930, 0.2457 ± 0.0004, 0.2304 ± 0.0050, are not perimeter-free
  (the same triangles turned by 180°: 4.8777, 8.6479, 13.1449, 18.349).

Holes against closed tori of the same shape (`data/life_tori.txt`: `$S/holes life slab NX NY SEED BATCHES T0
TMAX`, first empty face, hazard after T0, τ_face = 2/hazard; 4 × 4 reads 9.928 ± 0.003 against 9.9251/9.9324 on
file, 4 × 5 12.471 ± 0.013 against 12.4865):

```
an empty patch against the closed torus of the same shape (lifetimes: data/life_tori.txt, this stepper, first empty face):
  shape cells perimeter   -ln P (mean of the two classes)   ln tau_face      difference D
  2x3   18   10           8.800±0.000          4.0739±0.0007   4.727±0.001
  2x4   24   12          11.295±0.000          5.3944±0.0005   5.901±0.001
  2x5   30   14          13.762±0.001          6.5264±0.0009   7.236±0.001
  2x6   36   16          16.214±0.003          7.4392±0.0015   8.774±0.003
  2x8   48   20          21.099±0.028          8.4504±0.0037   12.649±0.028
  3x3   27   12          12.140±0.001          5.4873±0.0006   6.653±0.001
  3x4   36   14          15.419±0.002          7.3856±0.0012   8.033±0.002
  3x5   45   16          18.666±0.007          9.2507±0.0037   9.415±0.008
  3x6   54   18          21.945±0.030          10.9428±0.0081   11.002±0.031
  3x7   63   20          25.133±0.119          12.1809±0.0115   12.952±0.120
  4x4   48   16          19.473±0.015          9.9282±0.0034   9.545±0.015
  4x5   60   18          23.455±0.079          12.4708±0.0129   10.984±0.080
  bulk cost per cell by the mixed second difference, hole | closed torus | hole less torus
  (2.5, 3.5): 0.2613±0.0004 | 0.1926±0.0005 | +0.0687±0.0007
  (2.5, 4.5): 0.2598±0.0018 | 0.2444±0.0013 | +0.0155±0.0022
  (2.5, 5.5): 0.2759±0.0097 | 0.2598±0.0030 | +0.0162±0.0102
  (3.5, 3.5): 0.2586±0.0043 | 0.2148±0.0014 | +0.0438±0.0045
  (3.5, 4.5): 0.2450±0.0259 | 0.2258±0.0046 | +0.0191±0.0263
```

Caution: my 3 × 6 and 2 × 8 tori read 10.943 ± 0.008 and 8.450 ± 0.004 where `research/constant/out/points.txt`
has 11.0824 and 9.4888. Those shapes are the ones with a large "fw%" there; I did not find out which lives that
table drops. The 4 × 4 and 4 × 5 values agree.

## 3. The hull face of 360 cells [measured]

Interior against torus (difference in −ln P, hull − torus):

```
  margin 4:
    1x1  hull   1.9717±0.0000 hits 32023479384   torus   1.9718±0.0000   hull-torus -0.0001±0.0000
    1x2  hull   3.6258±0.0000 hits 6125399328   torus   3.6260±0.0000   hull-torus -0.0002±0.0000
    2x2  hull   6.1589±0.0002 hits   81066024   torus   6.1598±0.0001   hull-torus -0.0008±0.0002
  margin 3:
    1x1  hull   1.9719±0.0000 hits 112065939432   torus   1.9718±0.0000   hull-torus +0.0001±0.0000
    1x2  hull   3.6259±0.0000 hits 30622689296   torus   3.6260±0.0000   hull-torus -0.0001±0.0000
    2x2  hull   6.1592±0.0001 hits  810415248   torus   6.1598±0.0001   hull-torus -0.0005±0.0001
    2x3  hull   8.6745±0.0003 hits   78621810   torus   8.6753±0.0001   hull-torus -0.0009±0.0003
    3x3  hull  11.9841±0.0014 hits     718016   torus  11.9849±0.0007   hull-torus -0.0008±0.0015
    3x4  hull  15.2073±0.0093 hits      19065   torus  15.2298±0.0022   hull-torus -0.0225±0.0095
  margin 2:
    1x1  hull   1.9708±0.0000 hits 240398477952   torus   1.9718±0.0000   hull-torus -0.0010±0.0000
    1x2  hull   3.6252±0.0000 hits 73543364960   torus   3.6260±0.0000   hull-torus -0.0008±0.0000
    2x2  hull   6.1599±0.0001 hits 2267723040   torus   6.1598±0.0001   hull-torus +0.0001±0.0001
    2x3  hull   8.6760±0.0002 hits  274749967   torus   8.6753±0.0001   hull-torus +0.0007±0.0002
    3x3  hull  11.9862±0.0008 hits    3582386   torus  11.9849±0.0007   hull-torus +0.0014±0.0011
    3x4  hull  15.2298±0.0026 hits     186398   torus  15.2298±0.0022   hull-torus +0.0000±0.0034
    4x4  hull  19.1870±0.0313 hits       1069   torus  19.2377±0.0151   hull-torus -0.0507±0.0348
```

The same rhombus against its distance d from a rim (the other rims three or more rows away):

```
  1 along x 1 deep:   1.941±0.000   1.976±0.000   1.970±0.000   1.972±0.000   1.972±0.000   1.972±0.000   | 1.972±0.000
  1 along x 2 deep:   3.517±0.000   3.626±0.000   3.625±0.000   3.626±0.000   3.626±0.000   3.626±0.000   | 3.626±0.000
  2 along x 1 deep:   3.328±0.000   3.623±0.000   3.624±0.000   3.626±0.000   3.626±0.000   3.626±0.000   | 3.626±0.000
  2 along x 2 deep:   5.688±0.000   6.155±0.000   6.160±0.000   6.159±0.000   6.159±0.000   6.159±0.000   | 6.160±0.000
  2 along x 3 deep:   8.082±0.000   8.677±0.000   8.676±0.000   8.674±0.000   8.675±0.000   8.674±0.000   | 8.675±0.000
  3 along x 2 deep:   7.829±0.000   8.677±0.000   8.677±0.000   8.675±0.000   8.674±0.000   8.675±0.000   | 8.675±0.000
  3 along x 3 deep:  11.003±0.001  11.995±0.001  11.986±0.001  11.984±0.001  11.984±0.002        -        | 11.985±0.001
  3 along x 4 deep:  14.184±0.003  15.242±0.007  15.235±0.007  15.207±0.009        -             -        | 15.230±0.002
  4 along x 3 deep:  13.849±0.004  15.248±0.006  15.230±0.005  15.207±0.009        -             -        | 15.230±0.002
  4 along x 4 deep:  17.792±0.017  19.270±0.027  19.099±0.046        -             -             -        | 19.238±0.015
```

Corner rhombi (two sides on rims): 
```
  1x1  corner   0.5442±0.0000 hits 22248844272   torus   1.9718±0.0000  corner-torus -1.428±0.000
  1x2  corner   1.9952±0.0000 hits 10427464448   torus   3.6260±0.0000  corner-torus -1.631±0.000
  2x2  corner   4.0558±0.0001 hits 664114880   torus   6.1598±0.0001  corner-torus -2.104±0.000
  2x3  corner   6.0613±0.0001 hits 178759812   torus   8.6753±0.0001  corner-torus -2.614±0.000
  3x3  corner   8.7763±0.0007 hits   5917428   torus  11.9849±0.0007  corner-torus -3.209±0.001
  3x4  corner  11.5140±0.0023 hits    765940   torus  15.2298±0.0022  corner-torus -3.716±0.003
  4x4  corner  14.9701±0.0172 hits     12084   torus  19.2377±0.0151  corner-torus -4.268±0.023
  4x5  corner  18.4481±0.0387 hits       746   torus  23.2513±0.0448  corner-torus -4.803±0.059
  5x5  corner  22.9834±0.3806 hits         4   torus      28.2280(?)  corner-torus -5.245±inf
```

Strips of w rows against a rim and l units along it, ends three or more rows from the other rims, g(w, l):

```
  w=1   1.941±0.000   3.328±0.000   4.688±0.000   6.012±0.000   7.327±0.000   8.639±0.000   9.949±0.001  11.257±0.002
  w=2   3.517±0.000   5.688±0.000   7.829±0.000   9.913±0.001  11.979±0.001  14.031±0.003  16.085±0.009  18.107±0.040
  w=3   5.140±0.000   8.082±0.000  11.003±0.001  13.849±0.004  16.656±0.016  19.459±0.044  22.018±0.199             -
  w=4   6.771±0.000  10.486±0.000  14.184±0.003  17.792±0.017  21.522±0.160       -                   -             -
  w=5   8.405±0.000  12.884±0.001  17.349±0.012  22.042±0.158       -                   -             -             -
```

Cost per cell of row w+1 from the mixed second difference, rim strips | the torus at the same (w, l):

```
  w=1   1.941±0.000   3.328±0.000   4.688±0.000   6.012±0.000   7.327±0.000   8.639±0.000   9.949±0.001  11.257±0.002
  w=2   3.517±0.000   5.688±0.000   7.829±0.000   9.913±0.001  11.979±0.001  14.031±0.003  16.085±0.009  18.107±0.040
  w=3   5.140±0.000   8.082±0.000  11.003±0.001  13.849±0.004  16.656±0.016  19.459±0.044  22.018±0.199             -
  w=4   6.771±0.000  10.486±0.000  14.184±0.003  17.792±0.017  21.522±0.160       -                   -             -
  w=5   8.405±0.000  12.884±0.001  17.349±0.012  22.042±0.158       -                   -             -             -
```M

Triangles of side s as holes, with two, one and no real rim, and the hull face itself (ln τ; 18 cells: this work):

```
  s=1 cells   3: corner 0.544±0.000 [22248844272]  rim 1.941±0.000 [49540834120] (1.937±0.000 [60787506656])  interior 1.972±0.000 [112065939432] (1.971±0.000 [240398477952])  torus 1.972±0.000
  s=2 cells   9: corner 2.824±0.000 [2275437360]  rim 4.504±0.000 [3394505424] (4.501±0.000 [4254177304])  interior 4.919±0.000 [4203343920] (4.919±0.000 [10087827120])  torus 4.919±0.000
  s=3 cells  18: corner  5.675±0.000 [131478424]  rim  7.882±0.000 [101347304] (7.878±0.000 [130784630])  interior 8.744±0.000 [61104990] (8.746±0.000 [170815710])  torus 8.745±0.000
  s=4 cells  30: corner    9.239±0.001 [3726921]  rim   11.990±0.002 [1427106] (11.986±0.001 [1910551])  interior  13.307±0.004 [382665] (13.310±0.003 [1334625])  torus 13.309±0.001
  s=5 cells  45: corner     13.488±0.005 [53180]  rim      16.803±0.015 [9668] (16.804±0.012 [13517])  interior    18.512±0.043 [1050] (18.527±0.028 [5169])  torus 18.563±0.016
  s=6 cells  63: corner       18.663±0.062 [301]  rim        22.578±0.263 [24] (22.498±0.245 [39])  interior                      - (25.574(?) [3])  torus 24.399±0.227
  s=7 cells  84: corner                        -  rim                        - (-)  interior                      - (-)  torus       -      
  s=8 cells 108: corner                        -  rim                        - (-)  interior                      - (-)  torus       -      
  edge-to-rim conversions: rim - corner, interior - rim (torus for the interior if given), and 2*corner - rim against ln tau
  s=1: rim-corner 1.397±0.000  torus-rim 0.031±0.000   2*corner-rim -0.853±0.000
  s=2: rim-corner 1.679±0.000  torus-rim 0.415±0.000   2*corner-rim 1.145±0.000
  s=3: rim-corner 2.206±0.000  torus-rim 0.864±0.000   2*corner-rim 3.469±0.000
  s=4: rim-corner 2.752±0.002  torus-rim 1.318±0.002   2*corner-rim 6.487±0.002   ln tau 6.804  difference -0.317
  s=5: rim-corner 3.314±0.013  torus-rim 1.761±0.022   2*corner-rim 10.174±0.013   ln tau 9.819  difference 0.355
  s=6: rim-corner 3.835±0.229  torus-rim 1.901±0.334   2*corner-rim 14.827±0.229   ln tau 13.633  difference 1.194
  second differences in s, per cell (divided by 3): corner | rim (margin 2) | ln tau of hull faces: k=5 0.2663, k=6 0.2313, k=7 0.2300
  s=2:    0.1903±0.0000 |    0.2709±0.0001
  s=3:    0.2374±0.0003 |    0.2439±0.0004
  s=4:    0.2288±0.0013 |    0.2364±0.0033
  s=5:    0.3082±0.0217 |    0.2921±0.0775
  s=6:                - |                -
```

How a patch empties, by position (`P` lines; an event is a patch empty now and not empty in any of the four
generations before; "bust" = a one-generation fall of at least half the patch's cells within the last nine):

```
  shape  where          events  not-new  flicker  bust-share  over-full-share   patch density at lags 1..5 | layer beneath at lags 0..4
  2x2 corner              3808671  6197155  378524   0.331±0.000     0.423        0.147 0.346 0.425 0.430 0.431 | 0.225 0.177 0.314 0.369 0.383
  2x2 on a rim           15682145 12148871  567770   0.664±0.000     0.869        0.182 0.459 0.548 0.538 0.536 | 0.255 0.188 0.381 0.448 0.448
  2x2 one row in         10292394  4669801  285228   0.836±0.000     0.888        0.333 0.535 0.530 0.514 0.519 | 0.240 0.292 0.434 0.432 0.429
  2x2 interior(>=3)       8646117  3798215  227411   0.829±0.000     0.885        0.323 0.532 0.536 0.515 0.518 | 0.241 0.285 0.433 0.440 0.431
  2x2 interior(>=2)      24205219 10609335  634973   0.829±0.000     0.885        0.324 0.532 0.536 0.514 0.518 | 0.241 0.286 0.433 0.440 0.431
  3x3 corner              3049400  2750060  117966   0.229±0.000     0.455        0.076 0.213 0.369 0.424 0.443 | 0.243 0.184 0.234 0.341 0.375
  3x3 on a rim            4422094  1893151   70892   0.500±0.000     0.790        0.090 0.289 0.487 0.518 0.522 | 0.238 0.162 0.258 0.408 0.427
  3x3 one row in          1499791   377773   16408   0.712±0.000     0.850        0.129 0.413 0.532 0.516 0.516 | 0.220 0.165 0.346 0.432 0.424
  3x3 interior(>=3)        575019   137421    5576   0.714±0.001     0.854        0.126 0.408 0.545 0.521 0.516 | 0.218 0.162 0.340 0.446 0.428
  3x3 interior(>=2)       2870513   684261   27608   0.715±0.000     0.855        0.127 0.408 0.545 0.520 0.516 | 0.218 0.163 0.340 0.446 0.428
  4x4 corner                 7560     4358     166   0.215±0.005     0.330        0.049 0.141 0.296 0.395 0.440 | 0.261 0.199 0.205 0.295 0.356
  4x4 on a rim               3453      832      29   0.493±0.009     0.641        0.060 0.194 0.434 0.508 0.514 | 0.230 0.160 0.195 0.373 0.418
  4x4 one row in              557       97       2   0.668±0.020     0.754        0.065 0.264 0.501 0.527 0.514 | 0.210 0.142 0.236 0.416 0.430
  4x4 interior(>=2)           930      137       2   0.712±0.015     0.747        0.072 0.285 0.554 0.537 0.514 | 0.206 0.139 0.244 0.455 0.430
```

Busts by position, from the short run with the launch recorder (the hit counts in brackets of the interior
triangles above are three times the number of events: the three rotations of a triangle are the same cells):

```
  2x2 corner             busts: patch 0.786 -> 0.193 in the generation of the largest fall; layer beneath 0.658 -> 0.174; share launched from >= 0.7 full: 0.760, from < 0.6 full: 0.033
  2x2 on a rim           busts: patch 0.843 -> 0.186 in the generation of the largest fall; layer beneath 0.697 -> 0.150; share launched from >= 0.7 full: 0.924, from < 0.6 full: 0.020
  2x2 one row in         busts: patch 0.828 -> 0.107 in the generation of the largest fall; layer beneath 0.670 -> 0.155; share launched from >= 0.7 full: 0.895, from < 0.6 full: 0.025
  2x2 interior(>=3)      busts: patch 0.826 -> 0.111 in the generation of the largest fall; layer beneath 0.671 -> 0.158; share launched from >= 0.7 full: 0.893, from < 0.6 full: 0.025
  2x2 interior(>=2)      busts: patch 0.826 -> 0.111 in the generation of the largest fall; layer beneath 0.671 -> 0.158; share launched from >= 0.7 full: 0.893, from < 0.6 full: 0.025
  3x3 corner             busts: patch 0.777 -> 0.185 in the generation of the largest fall; layer beneath 0.645 -> 0.155; share launched from >= 0.7 full: 0.914, from < 0.6 full: 0.011
  3x3 on a rim           busts: patch 0.809 -> 0.178 in the generation of the largest fall; layer beneath 0.675 -> 0.138; share launched from >= 0.7 full: 0.963, from < 0.6 full: 0.004
  3x3 one row in         busts: patch 0.806 -> 0.129 in the generation of the largest fall; layer beneath 0.664 -> 0.128; share launched from >= 0.7 full: 0.961, from < 0.6 full: 0.005
  3x3 interior(>=3)      busts: patch 0.805 -> 0.132 in the generation of the largest fall; layer beneath 0.665 -> 0.129; share launched from >= 0.7 full: 0.964, from < 0.6 full: 0.004
  3x3 interior(>=2)      busts: patch 0.805 -> 0.132 in the generation of the largest fall; layer beneath 0.665 -> 0.130; share launched from >= 0.7 full: 0.964, from < 0.6 full: 0.004
  4x4 corner             busts: patch 0.770 -> 0.194 in the generation of the largest fall; layer beneath 0.632 -> 0.154; share launched from >= 0.7 full: 0.903, from < 0.6 full: 0.014
  4x4 on a rim           busts: patch 0.783 -> 0.179 in the generation of the largest fall; layer beneath 0.652 -> 0.152; share launched from >= 0.7 full: 0.873, from < 0.6 full: 0.013
  4x4 one row in         busts: patch 0.796 -> 0.149 in the generation of the largest fall; layer beneath 0.673 -> 0.114; share launched from >= 0.7 full: 1.000, from < 0.6 full: 0.000
  4x4 interior(>=2)      busts: patch 0.759 -> 0.149 in the generation of the largest fall; layer beneath 0.646 -> 0.126; share launched from >= 0.7 full: 0.889, from < 0.6 full: 0.000
```

## 4. Lifetimes by first face death [measured]

`$S/holes life hull R 0 SEED BATCHES T0 TMAX`: 256 lanes from soup, a lane leaves the risk set when one of its
faces is empty (death) or its state repeats with a period of 12 or less (censored); hazard = deaths / lane-
generations at risk after T0; τ_face = 8/hazard. `data/life.txt`:

| hull radius | cells | this mode | anchor |
|---|---:|---|---|
| 5 | 18 | **4.855 ± 0.015** (4.8556 ± 0.0006 over generations 41–100; 4.857, 4.852, 4.856 in windows of 20; the error is my allowance for the window: 21–40 reads 4.899, 101–120 reads 4.879) | none |
| 7 | 30 | 6.8048 ± 0.0019; four more seeds 6.8148, 6.8041, 6.8086, 6.8058 (mean of the five 6.808 ± 0.002) | 6.804 ± 0.003 |
| 9 | 45 | 9.8239 ± 0.0033 | 9.819 ± 0.003 |
| 11 | 63 | 13.6315 ± 0.0139 | 13.633 ± 0.008 |

Radius 3 (9 cells) has no steady hazard (4.28, 4.44, 4.56, 4.82 in successive windows): not a number.
The errors printed by this mode are 1/√deaths; four more seeds at radius 7 (6.8148, 6.8041, 6.8086, 6.8058,
each ± 0.0026) scatter 1.8 times that, so read every `life` error as doubled (the table of holes against closed
tori in section 2 prints them undoubled). A hull of radius 5 has 114 cells and its eight faces share most of them; whether its faces belong to the same
family as the larger ones is a judgement (the forecasts are given with and without it).

## 5. Formulas for the hull face and the forecasts

`python3 model.py`. Anchors: 6.804, 9.819, 13.633, 18.141, 23.3392 at k = 4…8, plus 4.855 at k = 3.

- **Rows formula R**: ln τ = C + Σ_r c_r·A_r(k), A_r the number of cells r rows from the nearest rim. [proved]
  The second difference of A_r in k is 3 for k − 3r ∈ {0, 1, 2} and 0 otherwise, so the second difference of ln τ
  is 3c_⌊k/3⌋: constant over three consecutive sides. Fitted: C = 1.7585, c_0 = 0.1572, c_1 = 0.2666, c_2 = 0.2307,
  χ² 0.02 on 1; from 30–84 cells it gives the 108-cell face as 23.343 ± 0.028 (23.3392). It says 4.589 at 18
  cells; measured 4.855 ± 0.015. **Refuted as an exact form** (if the 18-cell face counts). Its 135-cell value is
  "the second difference repeats", 29.231 ± 0.025.
- **A power of the area in front** (τ ∝ A^(−p)·e^(0.2087·A + b·k)), fitted on 45–108 cells: p = 1.55, χ² 0.26 on
  1, but 6.741 at 30 cells (anchor 6.804) and 29.202 at 135.
- **Formula S**: ln τ = a + b·k + 1.5·c·k(k+1) + B·r^k. All six anchors: c free 0.2230 (0.2175 … 0.2270), r = 0.31,
  χ² 0.61 on 1 → 29.207 (29.177 … 29.232), 35.746 (35.677 … 35.801), 42.954 (42.830 … 43.051). c = 0.2087: χ² 6.42
  on 2 (29.137); c = 0.2307: χ² 4.05 on 2 (29.256). Without the 18-cell face: c free 0.2295 (0.2175 … 0.2320),
  29.225; c = 0.2087 is then χ² 1.51 on 1 with r = 0.535 (29.179): the five anchors alone do not refute a
  geometric transient towards the wrapped price.

None of these has "at most one fitted number", and none takes a number from the living state: sections 2 and 3
say why it could not be done (no rim surplus to put in; a bulk cost of emptiness that is neither price).

## 6. Forecasts and scores

Mine, block A (`PREDICTIONS.md`, commit 7ebacea, before any code), 11 held, 5 missed, 2 half:
- A1 (torus bulk cost). "Above 0.225 at the largest sizes": held. "Still falling with size": **missed** (flat at
  0.26). 0.240 ± 0.012 at (3.5, 4.5): measured 0.266 ± 0.016, not scorable. 0.250 ± 0.012 at (2.5, 4.5): held at its
  edge (0.2592). "Depends mainly on the short side": half (true along a = 2.5, false along a = 1.5).
  "Extrapolates to 0.2087 ± 0.015": **missed**; there is nothing to extrapolate.
- A2 (how a patch empties). Bust shares 0.65 ± 0.12 and 0.55 ± 0.15: held (0.715, 0.697). Falling with size: held.
  Layer beneath below 0.30: held (0.22).
- A3 (interior = torus within 0.03, within 0.05 two rows in): both held (within 0.002).
- A4 (rim map). Rim patch likelier empty, 3 × 3 at −1.0 ± 1.0: held (−0.98). Corner likelier still: held.
  "Monotone in the distance and within 0.05 from distance 2": half (one row in is dearer than the interior).
- A5 (rim rows). Rim row 0.45 ± 0.05 per cell: held (0.436). Row prices 0.27 ± 0.03 and 0.245 ± 0.02: held (0.254,
  0.250 and 0.254, 0.248 at l = 3.5, 4.5). "The static row prices equal the hull's second differences" (I gave
  0.3): they do not.
- A6. I gave "the data reject the hypothesis" 0.15 and "support it" 0.4: **missed**.
- A7. My frozen 135-cell value inside 29.23 ± 0.04: held (29.21), which says little.
- Block B's side forecast, the corner triangle of side 6 at 18.75 ± 0.15: held (18.66 ± 0.06 on 301 hits).

The PI's block 5: (1) bulk cost on the torus 0.2087 ± 0.008: **missed** (0.26; outside 0.195–0.222, so by its own
criterion "the price of a face is the price of a hole in an unbounded face" is dead, with the caveat of item 1
that only holes up to 3 × 6 and 4 × 5 unit cells were reached). (2) interior patches within 0.010 per cell of
the torus: **held** (within 0.0001). (3) rim-row patches dearer by 0.02 per cell or more: **missed** (they are
cheaper, and the mixed differences show no surplus). (4) a model from the two measurements: **could not be
built**. (6) is for the 135-cell measurement.

## 7. Failed, not checked, next

Failed or dropped: the rows formula (killed by the 18-cell face); "2·corner − rim = ln τ + constant" for triangle
holes (off by −0.32, +0.36 at s = 4, 5); extrapolating the bulk cost with a sum of two decaying functions (χ² 43
on 9; the fitted "asymptote" moves from 0.19 to 0.25 with the cut); a lifetime for the 9-cell hull face.

Not checked: more than one long run per vessel (errors come from the eight lane groups of one run each); another
hull radius (beyond the short corner check at R = 21), slab thickness or torus size; patches beyond −ln P ≈ 24; why two of my narrow-torus lifetimes differ
from the table on file; whether the censoring of the `life` mode (periods up to 12) lets long-period debris into
the 18-cell number; the triangle "turned by 180°" on the hull; nobody has rewritten the stepper or the counters.

Next step I would take: lifetimes of rimmed faces that are not triangles. A vessel cut by eight diagonal
half-spaces with unequal constants has hexagonal and trapezoidal faces. A hexagon of 57 cells already has a unit
cell in the third row from every rim (a triangle needs 84 cells for that), one of 111 cells a cell in the fourth
row (a triangle needs 165), and such faces come in two-parameter families, so their price can be read from mixed
second differences at lifetimes plain running reaches. If it is 0.209, the hull's 0.231 is the triangle's
transient; if 0.23, it is the rim's price. (The side faces must be made to outlive the watched one.) On the static side: count patches that hold at most
two or three cells, not none, to see whether the 0.05 per cell is the price of the instant.
