# blast/strips: rimmed faces without corners, refereed and extended; the tetrahedron (agent `strips`, 2026-11-18, second phase)

Task (the PI's, as corrected at 12:35 UTC): referee agent `rim`'s table of corner-free strips with independent
code, extend it to (4 unit rows, L = 7) and (5 unit rows, L = 6), compare a strip's row with the row of a closed
tube of the same girth, time the tetrahedron's faces, and say where a strip's width price and length price meet.
Labels: [proved], [measured], [conjectured]. `S` = `research/scratch/blast/strips`. Not read: `rim`'s code,
anything under `noisy/`.

A strip (w, L) is one of the four equivalent faces of the prism |x+y| + |z| ≤ R = 2w − 1 (doubled coordinates),
periodic along (1,−1,0) with period L·(2,−2,0): w unit rows (rim's 2w rows), 3wL cells, one obtuse rim (z = 0, the
octahedron's edge) and one sharp rim (x + y = 0), no corner. rim's (2w, 2w, L, 0) is the same vessel.

## 0. What stands

1. **rim's table stands [measured, independent code].** All nine entries reproduced: differences +0.000, −0.006,
   −0.017, −0.006 (4 rows, L = 3…6), +0.007, −0.019, +0.038 (5 rows, L = 3…5), −0.007, −0.018 (6 rows, L = 3, 4);
   the largest is 2.4 combined errors ((10,10,3)), χ² 19 on 9. One derived number moves: the mixed second
   difference at (4.5 rows, L 4→5) is **0.2486 ± 0.0043** here against rim's 0.2262 ± 0.0078 (its four entries
   each deviate the unlucky way; the two tables pooled give 0.2436 ± 0.0037). So that quantity was not "0.6σ
   below the hull's 0.2307" at L 4→5; it is 4σ above it.
2. **Thin strips are cut across before a face dies, and that is what bends the lifetimes at large L [measured].**
   A "firewall" (three consecutive dead layers of one of the two diagonals that are not face normals; T3) cuts the
   prism across its axis. Share of lives ended by one before any face was empty: 4 rows: 0.0%, 0.0%, 0.2%, 3.0%,
   **32.6%** at L = 3…7; 5 rows: none in FWN96 lives at L = 6; 3 rows (rim's 6×6 rod): 0.3%, 6.1%, 44%, 86%, 97.4%,
   99.5% at L = 3…8. This settles rim's open point ("whether the thin rods die as rods"): they do, and the
   lead's booking (count only face deaths with no firewall before; exposure up to the firewall) removes it: the
   3-row strip's face lifetime then keeps growing, 8.609, 10.432, 12.146, 13.804 ± 0.020, 15.350 ± 0.046 (L = 4…8),
   where all first deaths saturate at 10.2.
3. **(4 unit rows, L = 7) [measured]: 18.716 ± 0.020 by all first deaths, 19.111 ± 0.024 with no firewall before.**
   Length price at L 6→7: **0.1874 ± 0.0018** (all first deaths: it plunges, because the rod is being cut) and
   **0.2177 ± 0.0021** (face deaths proper). In the second booking the sequence is 0.2450, 0.2301, 0.2210 ± 0.0009,
   0.2177 ± 0.0021 (steps −0.015, −0.009, −0.003): it is flattening near 0.217, not falling to 0.209.
4. **(5 unit rows, L = 6) [measured]: LT96.** Width price at L = 6 (4 → 5 rows, 18 cells, no firewall before):
   **WP6**. The sequence is 0.1702 ± 0.0002, 0.1945 ± 0.0006, 0.2052 ± 0.0007, WP6S at L = 3, 4, 5, 6 (steps +0.024,
   +0.011, STEP6). Length price for 5 rows at L 5→6: LP56.
5. **A row of a rimmed strip costs what a row of a closed tube of the same girth costs, or less; never 0.02 more
   [measured].** Strip (4 → 5 rows) minus closed tube (8-layer slab, girth g, the lead's table and mine, firewall
   deaths set aside), per cell: −0.026 to −0.038 (g = 3, depending on the tube's length), **−0.013 ± 0.001 (g = 4),
   −0.003 ± 0.001 (g = 5), DIFF6 (g = 6)**. Where it can be tested (L = 3, 4) a row costs the same two and three
   rows deep: 0.1702 against 0.1716 ± 0.0005 (L = 3), 0.1945 against 0.1947 ± 0.0012 (L = 4).
6. **The mixed second difference is another quantity and it is still high [measured]:** 0.2675 ± 0.0023 (L 3→4),
   0.2480 ± 0.0043 (4→5), **M56** (5→6) for 4 → 5 rows; 0.2643 ± 0.0049 for 5 → 6 rows at L 3→4. Closed faces
   a = 4 → 5 at the same girths: 0.2276 ± 0.0015, 0.2069 ± 0.0012, 0.2134 ± 0.0040. [proved, algebra] If ln τ = a(L) +
   w·g(L) (measured for w ≥ 4 at L = 3, 4), then with p(L) = g(L)/3L the row price, M(L+½) = (L+1)·p(L+1) −
   L·p(L) = p(L+1) + L·(p(L+1) − p(L)): the mixed difference exceeds the row price for as long as the row price
   is still rising with L. In the strip a "second difference" of 0.24 coexists with a row price of 0.21.
7. **The tetrahedron is not a vessel with a steady state [measured; the cause proved from T2].** T2 holds for
   all eight diagonals, so the pattern's own hull is cut by the four directions opposite to the faces' normals,
   and those cuts shave the four corners irreversibly: 3.3 layers gone by generation 50, 6.1 by 800, 8.0 by
   12,800 (side 9), growing by about half a layer per doubling of the time; the octahedron: 0.00 throughout. The faces'
   population falls with it (58 → 21 of 135 cells) and the hazard of a face death climbs with age: side 9 reads
   ln τ_face = 15.9, 13.9, 11.8, 10.2, 9.42, 9.15 in the age bins from 400, 800, …, 12,800 generations. There is
   no τ for a tetrahedral face, no second difference, and no "sharp-rim row price" to be had this way.

**Verdict [measured, with one conjecture marked].** In a corner-free strip the rows two and three deep do not
cost 0.02 more than a wrapped face's rows at the same loop length: they cost less at L = 3 and 4 and the same at
L = 5 and 6 (item 5; a surplus of 0.02 at L = 6 is excluded by SIG6 errors). The strip's row price is still rising
(WP6S at L = 6) and its mixed second difference still falling (M56S at L 5→6); the asymptotic price of a row lies
between them. [conjectured] Continuing either sequence geometrically gives 0.210 to 0.223; I put it at
**0.215 ± 0.006**: at or slightly above the wrapped 0.2087, and below the hull's 0.2307. Width price and length
price need not meet: the intercept a(L) = ln τ(4, L) − 4·g(L) goes on falling (AL6), so the length price of a
strip of fixed width tends to the row price plus a′/(3w), which is below it if that continues; what the two
sequences bracket is the row price, and the length price of 4 rows is at 0.2177 only because −a′/12 ≈ 0.015
is subtracted from a mixed difference of about 0.23.
What could spoil it: (i) the 4-row strip may itself be too thin at L = 6 (the 3-row strip is: its step to 4 rows
costs 0.242 per cell at L = 6 against 0.21 for 4 → 5), which would make the true row price at L = 6 LOWER than
WP6S; (ii) (5 rows, L = 6) rests on N96 deaths; (iii) the sharp rim: a strip measures only the sum of an obtuse
and a sharp rim, and the tetrahedron cannot isolate the sharp one (item 7).

**For the hull [conjectured].** The hull's second differences (0.355, 0.266, 0.2313, 0.2301 at k = 4…7) are the
analogue of the strip's mixed difference (0.2675, 0.248, M56S), not of its row price (0.170, 0.1945, 0.205, WP6S).
The strip shows, with no corner, that a mixed difference of 0.23 to 0.25 goes with a row price at the wrapped
value; so two equal second differences of 0.231 do not make 0.231 a price, and "rows" in holes' sense (a price by
depth: rim row cheap, second dear, third 0.231) is not what a strip shows: rows cost the same at depth 2 and 3
and their price depends on the loop. "The wrapped price takes over at once" is not what it shows either: at 75
to 90 cells the mixed difference is still M56S. If the hull's second difference now sinks as the strip's does
(by 0.008 ± 0.006 per step of the side), the 135-cell face is at **29.20 ± 0.02** and the 165-cell face at **35.72 ±
0.06** (29.230 and 35.81 if 0.2307 repeats; 29.163 if 0.2087 takes over). The strips cannot decide between
29.20 and 29.23. What would: the width price at L = 7 and 8 (strips of 5 and 6 rows at ln τ 23 to 30: a
sampler's job, not plain running), or the 135-cell face itself to ± 0.02.

## 1. Code, conventions, validation, calibration

`strips.c` (`gcc -O3 -march=native -o $S/strips strips.c -lm`): AVX-512 bit-sliced graph stepper, 512 replicas,
written from `reference/oracle.py` and `docs/AUTOMATON.md`; a vessel is a set of diagonal half-spaces plus up to
two period vectors (`oct R`, `prism R L`, `tet S`, `slab A L` = 8 layers with period lattice (A,0),(0,L)); a face
is every cell of the vessel in the outermost layer of one half-space (shared edge cells included).
`$S/strips info VESSEL P1 P2` prints the cell counts: strip faces have 3wL cells; per unit of length 2 cells of
the obtuse rim row lie in two face layers and have 7 neighbours inside, 1 cell of the sharp rim row has 6, 2
cells next to it have 8, all others 9 (agrees with rim's budget table).

**Life mode** (`$S/strips life VESSEL P1 P2 SEED T0 MAXDEATHS MAXSECS 1`): every lane starts from soup of density
1/2; a life ends at the first generation at which any face is empty (booked every generation), or when the lane
is periodic (period ≤ 12, or equal to a snapshot at the last multiple of 4096; censored), and the lane restarts
from soup. Deaths and exposure count for lanes older than T0. ln τ_face = ln(faces × exposure / deaths), error
1/√deaths. Second booking ("no firewall before", the lead's `fw%` column): the life ends at the first firewall
(three cyclically consecutive dead layers of a diagonal whose layers wind round the period; looked for every 8
generations and exactly in the generation before each death) and only face deaths with none before count.
Output also has the hazard by age (bins T0·2^j) and the dying face's population by lag.
T0: the hazard of a strip is not steady before about 1,000 generations ((4 rows, L = 4): ln τ 11.19, 11.14, 11.11
in the age bins from 200, 400, 800; 11.09–11.10 after; `data/other/p_7_4_s704.txt`), so T0 = 1000 is used except
where lives are short (T0 = 200 to 400 at L = 3, with flat age bins).

**Validation** (`sh validate.sh > validate_log.txt`, 2 minutes): three lanes against the oracle, state for
state, 1,000 generations, the whole oracle array compared (a birth outside the vessel would fail): octahedron
R = 9; prisms (R, L) = (7,5), (9,3), (11,4), (5,6) lifted 3, 5, 5, 2 times into the 30-, 30-, 40-, 24-torus; slabs
4×3 and 5×4 lifted into the 48- and 40-torus; tetrahedra of side 5, 6, 7 (their chaos dies within 130 to 1,000
generations: 126 to 1,001 distinct states). All identical; with one swapped neighbour every one fails within 8
generations. Eight diagonal half-spaces are separately invariant: T2's proof uses one direction at a time, and
the comparison of the whole array confirms it for the prism and the tetrahedron. The log is from the build
before the last edit of `life` (the 4096-snapshot); the stepper and `val` were not touched by it.
Not oracle-checked: the booking of deaths and firewalls (checked only through the anchors and the lead's table
below).

**Calibration** (`data/table_out.txt`, last sections): octahedron R = 7: **6.8046 ± 0.0018** (anchor 6.804 ±
0.003); R = 9: **9.8219 ± 0.0018** (anchor 9.819 ± 0.003; rim 9.8214; holes 9.8239). Closed faces booked the
lead's way against `research/constant/out/points.txt`: 4×4 9.9235 ± 0.0041 (9.9324 ± 0.0020), 4×5 12.4921 ± 0.0058
(12.4865), 5×5 15.6692 ± 0.0142 (15.6614), 3×6 11.0819 ± 0.0044 (11.0824), 4×6 14.9846 ± 0.0132 (14.9710), 3×8
14.6348 ± 0.0195 (14.6209); firewall shares 0.2, 0.5, 0.4, 12.4, 5.0, 86.8% against 0.3, 0.5, 0.3, 12.6, 5.0, 86.6%.
Seed scatter: eight seeds of (5 rows, L = 3), 60,000 deaths each, have a standard deviation of 0.0027 against
the Poisson 0.0041 (`data/runs/seedtest_9_3_*.txt`): the errors are honest for this mode.

**A trap found on the way [measured].** Debris of period above 12 that keeps a cell on every face is never
booked dead and piles up exposure: with only the period-≤-12 test the octahedron R = 7 at T0 = 400 read 7.0018
(three lanes 2.2 million generations old); with the snapshot test 6.8046. It matters only in vessels of under
about 300 cells (3-row rods moved by 0.02; the 2-row prisms, 24L cells, are not chaos at all). The long runs
(4 rows L = 5, 6, 7; 5 rows L = 4, 5, 6; 6 rows; the slabs) were made before the snapshot test; their hazards are
flat in age and their periodic-censored counts are 0 to 3, and (4 rows, L = 3) re-run with it reads 8.1457 ±
0.0018 against 8.1444 ± 0.0018 without.

## 2. Tables [measured]

`sh collect.sh` copies the run outputs to `data/runs/` and writes `data/table_out.txt` (`python3 table.py`).
Runs: `data/runs/*.txt`, first line = the command's parameters (`# life VESSEL P1 P2 seed S T0 T …`); the queue
that made them is in `data/queue*.sh`. ln τ_face of strips, **no firewall before** (all first deaths in
brackets where they differ):

| unit rows w \ L | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| 3 (too thin: see 0.2) | 6.646 | 8.609 [8.549] | 10.432 [9.850] | 12.146 [10.211] | 13.804 ± 0.020 [10.155] | 15.350 ± 0.046 [10.045] |
| 4 | 8.1451 ± 0.0013 | 11.0853 ± 0.0035 | 13.8464 ± 0.0050 [13.8443] | 16.4981 ± 0.0093 [16.4680] | 19.1106 ± 0.0239 [18.7164 ± 0.0196] | |
| 5 | 9.6765 ± 0.0013 | 13.4191 ± 0.0058 | 16.9241 ± 0.0096 | T96 | | |
| 6 | 11.2205 ± 0.0041 | 15.7560 ± 0.0129 | | | | |

Per cell, no firewall before:

| | L = 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|
| width price, 4 → 5 rows, at L | 0.1702 ± 0.0002 | 0.1945 ± 0.0006 | 0.2052 ± 0.0007 | WP6 | |
| width price, 5 → 6 rows | 0.1716 ± 0.0005 | 0.1947 ± 0.0012 | | | |
| width price, 3 → 4 rows (3 rows too thin) | 0.1666 | 0.2064 | 0.2277 | 0.2418 | 0.2527 ± 0.0015 |
| closed tube of that girth (a → a+1) | 0.197 to 0.208 | 0.2070 ± 0.0002 (5→6) | 0.2083 ± 0.0008 (5→6) | 0.2101 ± 0.0024 (5→6) | |
| length price, 4 rows, L−1 → L | | 0.2450 ± 0.0003 | 0.2301 ± 0.0005 | 0.2210 ± 0.0009 | 0.2177 ± 0.0021 |
| length price, 5 rows | | 0.2495 ± 0.0004 | 0.2337 ± 0.0007 | LP56 | |
| mixed difference, 4 → 5 rows, L−1 → L | | 0.2675 ± 0.0023 | 0.2480 ± 0.0043 | M56 | |
| the same for closed faces 4 → 5 | | 0.2276 ± 0.0015 | 0.2069 ± 0.0012 | 0.2134 ± 0.0040 | |

g(L) = ln τ(5, L) − ln τ(4, L) = 1.5314 ± 0.0018, 2.3338 ± 0.0068, 3.0777 ± 0.0109, G6 and the intercept
a(L) = ln τ(4, L) − 4·g(L) = 2.020 ± 0.008, 1.750 ± 0.029, 1.535 ± 0.046, A6 at L = 3, 4, 5, 6.

**The rows formula against the strip** (holes' fit to the hull, the octahedron's row prices used at both rims
because the tetrahedron gives none): it has λ(w) = ln τ(w, L+1) − ln τ(w, L) = 2.543, 3.235, 3.927 for w = 4, 5, 6
at every L. Measured: λ(4) = 2.940, 2.761, 2.652 ± 0.011, 2.613 ± 0.026 (L 3→4 … 6→7); λ(5) = 3.743, 3.505 ± 0.011, L56;
λ(6) = 4.536 (3→4). The measured values depend on L, which the formula cannot; at the largest L they are 3 to
4% above it and still falling. Its increment per middle row, 0.692, against the measured 0.802, 0.744, INC56.
Not confirmed, not excluded as a limit.

**Closed tubes, both bookings** (mine; `data/table_out.txt`): 3×4 7.3920 / 7.3959; 3×5 9.2467 / 9.2672; 3×6 10.9535
/ 11.0819; 3×7 12.1799 / 12.8519 ± 0.0071 (firewalls 49.6%); 3×8 12.6400 / 14.6348 ± 0.0195 (86.8%); 4×4 9.9219 /
9.9235; 4×5 12.4876 / 12.4921; 4×6 14.9347 / 14.9846 (5.0%); 5×5 15.6652 / 15.6692.

## 3. The tetrahedron [measured]

`tet S`: d·p ≤ S for the four alternate diagonals (S odd; for S even the centre is the cube vertex (1,1,1)); four
equivalent faces of 3S(S+1)/2 cells with whole unit cells, all rims sharp (5 or 6 neighbours inside for edge
cells). ln τ_face = ln(4·exposure/deaths) by age since the soup (`data/runs/tet_*.txt`):

| side (cells) | by age bin (generations from) |
|---|---|
| 5 (45) | 100: 4.65, 200: 4.93 |
| 6 (63) | 150: 5.78, 300: 5.39 |
| 7 (84) | 200: 7.78, 400: 6.83, 800: 6.36 |
| 8 (108) | 300: 11.14, 600: 9.46, 1200: 8.41, 2400: 7.90, 4800: 7.63 ± 0.02 |
| 9 (135) | 400: 15.9, 800: 13.9, 1600: 11.81, 3200: 10.21, 6400: 9.42, 12800: 9.15 ± 0.01 |
| 10 (165) | 3200: 16.1, 6400: 14.26, 12800: 12.57, 25600: 11.52, 51200: 11.01, 102400: 10.75 ± 0.09 |
| 11 (198) | 25600: 16.9, 51200: 14.72, 102400: 13.42, 204800: 13.00 ± 0.03 |

(The octahedron: 9.82 at 45 cells, 13.63 at 63, flat in age.) `$S/strips trunc tet 9 0 77 30000`
(`data/runs/trunc_*.txt`): layers shaved off each corner, mean over lanes with no face yet empty: 3.34, 4.12,
4.80, 5.48, 6.10, 6.56, 7.15, 7.76, 7.96 at generations 50, 100, …, 12,800; mean face population 58.3 → 20.8 of
135. Side 11: 3.28 … 8.45 at 25,600. Octahedron R = 9: 0.00 at every time, population 21.6 of 45 throughout.
[proved] T2 applies to −d for each face normal d of the tetrahedron: once every cell beyond a layer of −d is dead
it stays dead, so the live region is confined to a truncated tetrahedron whose four small faces can only move
inward. A small truncation face dies quickly (it is a hull face of a few cells), so the corners erode until
those faces are large enough to last as long as the big ones: the tetrahedron turns itself into an octahedron-
like body, and its "face lifetime" is the time that takes. [conjectured] The late hazard is that of the hull it
ends as: side 9 settles at 9.15, between the octahedron's 6.80 (side 4) and 9.82 (side 5).
Consequence for the brief: a vessel bounded by fewer than all eight diagonals holds a steady face only where the
missing diagonals' layers close on themselves (the prism, the slab); there the firewall is the same erosion.

## 4. How they die [measured] (`data/table_out.txt`, last section)

Share of deaths with a one-generation fall of at least half the face among the 12 steps before the death, and
the dying face's 95th percentile four generations before, as a fraction of the face:
octahedron R = 7, 9: 0.030, 0.015; q95 0.60, 0.56 (the living q95: 0.67, 0.64): **no over-full generation**.
Closed faces 4×4, 4×5, 5×5, 4×6: 0.58, 0.57, 0.57, 0.55; dying q90 0.75, q95 0.78 to 0.79 (living q99 0.68 to 0.71):
**over-full**. Strips, 4 rows L = 3…6: 0.227, 0.207, 0.160, 0.113; 5 rows L = 3, 4, 5: 0.167, 0.197, 0.151; 6 rows L = 3, 4:
0.149, 0.190; dying q95 at lag 4: 0.64 to 0.78 (living q99 0.69 to 0.75), dying q90 0.38 to 0.69: **a mixture: one
death in five to nine is a bust, the rest fade**, and the bust share falls with L (rim's 0.203, 0.196, 0.158,
0.150 at the same four vessels: reproduced, 0.207, 0.197, 0.160, 0.149). Tetrahedron: 0.000 (its faces are a
fifth full when they die). The shares for (4 rows, L = 7) (0.063) and the 3-row rods mix in deaths after a cut.

## 5. Forecasts scored

Mine, `PREDICTIONS.md` block A (commit 993537c, 12:36 UTC, before any lifetime):
SCORES

## 6. Failed, not checked, next

Failed or dropped: the row-price profile from w = 1 up (prisms of 1 and 2 unit rows do not hold chaos; the 3-row
strip is too thin to be a face: its step to 4 rows costs 0.21, 0.23, 0.24, 0.25 per cell at L = 4…7 where 4 → 5
costs 0.19 to 0.21, so "is the second row dearer?" cannot be separated from "is the body too thin?"); the
tetrahedron as a source of sharp-rim prices (section 3); a first version of the periodic censoring (section 1).
Not checked: the long runs with a second seed each except (5 rows, L = 3), (5 rows, L = 5), (5 rows, L = 6);
whether 4 rows are thick enough at L = 6, 7 (needs 5 → 6 rows at L = 5, 6: ln τ 20 and 24); strips with the other
rim kinds (odd numbers of half-rows, unequal constants); the firewall test against any code but the lead's
table; nobody has rewritten this stepper; the hull forecasts are an analogy, not a derivation.
Next step: the width price at L = 7 (5 rows, L = 7, ln τ ≈ 23.5 — a splitting sampler on the prism, which `strips.c`
could drive), because the row price there decides between an asymptote at 0.209–0.212 and one at 0.22.
