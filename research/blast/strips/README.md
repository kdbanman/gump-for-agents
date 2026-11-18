# blast/strips: rimmed faces without corners, refereed and extended; the tetrahedron (agent `strips`, 2026-11-18, second phase)

Task (the PI's, as corrected at 12:35 UTC): referee agent `rim`'s table of corner-free strips with independent
code, extend it to (4 unit rows, L = 7) and (5 unit rows, L = 6), compare a strip's row with the row of a closed
tube of the same girth, time the tetrahedron's faces, and say where a strip's width price and length price meet.
Labels: [proved], [measured], [conjectured]. `S` = `research/scratch/blast/strips`. Not read: `rim`'s code,
anything under `noisy/`.

A strip (w, L) is one of the four equivalent faces of the prism |x+y| + |z| ≤ R = 2w − 1 (doubled coordinates),
periodic along (1,−1,0) with period L·(2,−2,0): w = (R + 1)/2 unit rows (rim's 2w rows), 3wL = 3L(R + 1)/2 cells
(every cell with x + y + z = R and 0 ≤ z ≤ R, shared edge cells included), one obtuse rim (z = 0, the
octahedron's edge) and one sharp rim (x + y = 0), no corner. rim's (2w, 2w, L, 0) is the same vessel.

## 0. What stands

1. **rim's table stands [measured, independent code].** All nine entries reproduced: differences +0.000, −0.006,
   −0.017, −0.006 (4 rows, L = 3…6), +0.007, −0.019, +0.038 (5 rows, L = 3…5), −0.007, −0.018 (6 rows, L = 3, 4);
   the largest is 2.4 combined errors ((10,10,3)); χ² is 19 on 9, so the two codes differ by about 1.5 times
   their 1/√deaths (soup 0.4 against 0.5, T0 = 200 against 1,000 and the settled test differ; my own seeds scatter
   as Poisson, section 1), with no sign pattern. One derived number moves: the mixed second
   difference at (4.5 rows, L 4→5) is **0.2486 ± 0.0043** here against rim's 0.2262 ± 0.0078 (its four entries
   each deviate the unlucky way; the two tables pooled give 0.2436 ± 0.0037). So that quantity was not "0.6σ
   below the hull's 0.2307" at L 4→5; it is 4σ above it.
2. **Thin strips are cut across before a face dies, and that is what bends the lifetimes at large L [measured].**
   A "firewall" (three consecutive dead layers of one of the two diagonals that are not face normals; T3) cuts the
   prism across its axis. Share of lives ended by one before any face was empty: 4 rows: 0.0%, 0.0%, 0.2%, 3.0%,
   **32.6%** at L = 3…7; 5 rows: none in 2,142 lives at L = 6; 3 rows (rim's 6×6 rod): 0.3%, 6.1%, 44%, 86%, 97.4%,
   99.5% at L = 3…8. This settles rim's open point ("whether the thin rods die as rods"): they do, and the
   lead's booking (count only face deaths with no firewall before; exposure up to the firewall) removes it: the
   3-row strip's face lifetime then keeps growing, 8.609, 10.432, 12.146, 13.804 ± 0.020, 15.350 ± 0.046 (L = 4…8),
   where all first deaths saturate at 10.2.
3. **(4 unit rows, L = 7) [measured]: 18.716 ± 0.020 by all first deaths, 19.111 ± 0.024 with no firewall before.**
   Length price at L 6→7: **0.1874 ± 0.0018** (all first deaths: it plunges, because the rod is being cut) and
   **0.2177 ± 0.0021** (face deaths proper). In the second booking the sequence is 0.2450, 0.2301, 0.2210 ± 0.0009,
   0.2177 ± 0.0021 (steps −0.015, −0.009, −0.003): it is flattening near 0.217, not falling to 0.209.
4. **(5 unit rows, L = 6) [measured]: 20.3003 ± 0.0216 (2,142 deaths, three seeds; no firewall in any life).** Width price at
   L = 6 (4 → 5 rows, 18 cells, no firewall before): **0.2112 ± 0.0013**; the sequence is 0.1702 ± 0.0002, 0.1945 ± 0.0006,
   0.2052 ± 0.0007, 0.2112 at L = 3, 4, 5, 6 (steps +0.024, +0.011, +0.0061). Length price for 5 rows at L 5→6: 0.2251 ± 0.0016.
5. **At every girth reached a row of a rimmed strip costs no more than a row of a closed tube of that girth
   [measured].** Strip (4 → 5 rows) minus closed tube (8-layer slab, the lead's table and mine, firewall deaths
   set aside), per cell: −0.026 to −0.038 (girth 3, depending on the tube's length), **−0.013 ± 0.001 (4),
   −0.003 ± 0.001 (5), +0.0011 ± 0.0027 (6)**. At L = 3 and 4 a row costs the same two and three rows deep: 0.1702 against
   0.1716 ± 0.0005, 0.1945 against 0.1947 ± 0.0012. At L = 5 the thicker pair is CHEAPER: 0.1994 ± 0.0023 (5 → 6 rows;
   (6 rows, L = 5) = 19.916 ± 0.033, 927 deaths) against 0.2052 ± 0.0007 (4 → 5), 2.4 errors apart, and 0.009 ± 0.002
   below the closed tube of girth 5 (item 7).
6. **From 4 → 5 rows the strip's row price is still climbing where the tube's has stopped, so its mixed second
   difference is high [measured; partly thinness, item 7]:** 0.2675 ± 0.0023 (L 3→4), 0.2480 ± 0.0043 (4→5), **0.2415 ± 0.0086** (5→6) for 4 → 5 rows; 0.2643 ± 0.0049
   (3→4) and 0.218 ± 0.012 (4→5) for 5 → 6 rows. Closed faces 4 → 5 at the same girths: 0.2276 ± 0.0015, 0.2069 ± 0.0012,
   0.2134 ± 0.0040 (their row price: 0.2070, 0.2083, 0.2101 at girth 4, 5, 6). [proved, algebra] If ln τ = a(L) + w·g(L)
   and p(L) = g(L)/3L is the row price, the mixed difference is M(L+½) = (L+1)·p(L+1) − L·p(L) = p(L+1) +
   L·(p(L+1) − p(L)): the *marginal* price of a middle row's cells, above the *average* p for as long as p rises.
   In a strip a marginal price of 0.24 goes with an average row price of 0.21.
7. **A thin strip's faces die early, and the 4-row strip is thin from L = 5 on [measured at L = 5, 2.4 errors;
   conjectured beyond].** Against the straight line in w through 4 and 5 rows, the 3-row strip's ln τ (no firewall
   before) is +0.03, −0.14, −0.34, −0.55 at L = 3…6, where its firewall share is 0.3, 6, 44, 86%. The 4-row strip
   (firewall shares 0.2, 3.0, 32.6% at L = 5, 6, 7) lies 0.09 ± 0.04 under the line through 5 and 6 rows at L = 5 (and
   0.013 ± 0.005 and 0.003 ± 0.018 ABOVE it at L = 3, 4). If its deficit at L = 6 is 0.15 to 0.25, the row price at L = 6 is 0.197 to
   0.203 instead of 0.2112 and the mixed difference at 5→6 is 0.19 to 0.22 instead of 0.241. Everything in items 3,
   4 and 6 that uses (4 rows, L ≥ 5) carries this systematic, of the size of the effect sought.
8. **The tetrahedron is not a vessel with a steady state [measured; the cause proved from T2].** T2 holds for
   all eight diagonals, so the pattern's own hull is cut by the four directions opposite to the faces' normals,
   and those cuts shave the four corners irreversibly: 3.3 layers gone by generation 50, 6.1 by 800, 8.0 by
   12,800 (side 9), about half a layer more per doubling of the time; the octahedron: 0.00 throughout. The faces'
   population falls with it (58 → 21 of 135 cells) and the hazard of a face death climbs with age: side 9 reads
   ln τ_face = 15.9, 13.9, 11.8, 10.2, 9.42, 9.15 in the age bins from 400, 800, …, 12,800 generations. There is
   no τ for a tetrahedral face, no second difference, and no "sharp-rim row price" to be had this way.

**Verdict.** *Do the rows two deep in a rimmed strip cost what a wrapped face's rows cost at the same loop
length, or 0.02 more?* [measured] Bought as a whole row at fixed length, they cost less (L = 3, 4: by 0.03, 0.013;
L = 5: by 0.003 ± 0.001 from 4 → 5 rows, 0.009 ± 0.002 from 5 → 6) or the same (L = 6: +0.0011 ± 0.0027, from 4 → 5
rows only), and the same at depth 2 as at depth 3: there is no price by
depth, and no surplus of 0.02 in any row. Bought at the margin (the mixed difference, which is what the hull's
second difference is), they cost 0.040 ± 0.003, 0.041 ± 0.004, 0.028 ± 0.010 MORE than a closed face's at L 3→4, 4→5, 5→6.
Both are true because a strip's row price depends on the loop far more than a closed tube's (0.170, 0.1945,
0.205, 0.2112 against 0.197, 0.207, 0.208, 0.210). **The measurement does not pin where the row price ends.** From 4 → 5
rows it is bracketed by 0.2112 (rising by +0.0061 at the last step) and 0.241 (falling by 0.006). But the one test with
thicker strips, 5 → 6 rows at L = 5 (forecast block B), reads lower on both: row price 0.1994 ± 0.0023 against 0.2052 ±
0.0007, mixed difference at L 4→5 0.218 ± 0.012 against 0.2480 ± 0.0043, each about two errors down, and (4 rows, L = 5)
lies 0.09 ± 0.04 under the line through 5 and 6 rows. So the 4-row strip is probably thin already at L = 5 (item 7), more
so at L = 6 and 7, and part of the marginal surplus is thinness. From the thick pair alone the row price is
0.1716, 0.1947, 0.1994 at L = 3, 4, 5 (steps +0.023, +0.0047): levelling at or below the wrapped 0.209.
[conjectured] I lean to "no surplus in a corner-free strip's rows, average or marginal, once the strip is thick
enough" (0.65) and cannot exclude a marginal price near 0.23 (0.35). The same holds for "do width and length price meet":
0.2112 against 0.2177 ± 0.0021 at L = 6 to 7 for 4 rows, the gap halving at each step (0.050, 0.025, 0.010), but
the 4-row length price at 6→7 is the one most damaged by thinness (32.6% of lives cut), and the intercept
a(L) = ln τ(4, L) − 4·g(L) still falls (2.02, 1.75, 1.54, 1.29), so the two need not meet at the row price.
What would separate the readings: the row price at L = 6, 7, 8 from strips of 5 and 6 rows ((6, 6) ≈ 24, (5, 7) ≈
23.6, (6, 7) ≈ 28): beyond plain running, within reach of a splitting sampler on this prism.

**For the hull [conjectured].** (a) The hull's second differences (0.355, 0.266, 0.2313, 0.2301 at k = 4…7) are the
analogue of the strip's mixed difference (0.2675, 0.248, 0.241 from 4 → 5 rows; 0.264, 0.218 from 5 → 6), which reads
0.22 to 0.27 with no corner anywhere: corners are not needed for an excess of that size, and "the surplus sits
in the corners" is not supported. (b) "Rows" in holes' sense (a price by depth: rim row cheap, second dear,
third 0.231) is not supported either: rows cost the same at depth 2 and 3 and their price moves with the loop.
(c) What the strip shows is a row price that depends on the row's length and rises to about the wrapped price
by 5 to 6 units; while it rises, the mixed difference overshoots. A triangle's rows are 1 to k units long, so on
this reading its second difference stays inflated until its inner rows pass 5 or 6 units (k about 9 to 11) and
then sinks towards 0.21: **135 cells: 29.20 ± 0.03; 165 cells: 35.72 ± 0.07** (29.230 and 35.81 if 0.2307 repeats;
29.163 if 0.2087 takes over at once). This gives a reason, not precision: the strips cannot decide between 29.20
and 29.23, and a 135-cell value of 29.23 would not by itself make 0.231 a price.

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
the comparison of the whole array confirms it for the prism and the tetrahedron. The log is from the binary
of the committed source; the runs were made with earlier builds of the same stepper (`life` gained progress
lines, the `trunc` mode and the 4096-snapshot test on the way; `step` and the vessel builder were not touched).
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
(4 rows L = 5, 6, 7; 5 rows L = 4, 5, 6; 6 rows L = 3, 4; the slabs) were made before the snapshot test; their hazards are
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
| 5 | 9.6765 ± 0.0013 | 13.4191 ± 0.0058 | 16.9241 ± 0.0096 | 20.3003 ± 0.0216 | | |
| 6 | 11.2205 ± 0.0041 | 15.7560 ± 0.0129 | 19.916 ± 0.033 | | | |

Per cell, no firewall before:

| | L = 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|
| width price, 4 → 5 rows, at L | 0.1702 ± 0.0002 | 0.1945 ± 0.0006 | 0.2052 ± 0.0007 | 0.2112 ± 0.0013 | |
| width price, 5 → 6 rows | 0.1716 ± 0.0005 | 0.1947 ± 0.0012 | 0.1994 ± 0.0023 | | |
| width price, 3 → 4 rows (3 rows too thin) | 0.1666 | 0.2064 | 0.2277 | 0.2418 | 0.2527 ± 0.0015 |
| closed tube of that girth (a → a+1) | 0.197 to 0.208 | 0.2070 ± 0.0002 (5→6) | 0.2083 ± 0.0008 (5→6) | 0.2101 ± 0.0024 (5→6) | |
| length price, 4 rows, L−1 → L | | 0.2450 ± 0.0003 | 0.2301 ± 0.0005 | 0.2210 ± 0.0009 | 0.2177 ± 0.0021 |
| length price, 5 rows | | 0.2495 ± 0.0004 | 0.2337 ± 0.0007 | 0.2251 ± 0.0016 | |
| mixed difference, 4 → 5 rows, L−1 → L | | 0.2675 ± 0.0023 | 0.2480 ± 0.0043 | 0.2415 ± 0.0086 | |
| mixed difference, 5 → 6 rows, L−1 → L | | 0.2643 ± 0.0049 | 0.218 ± 0.012 | | |
| the same for closed faces 4 → 5 | | 0.2276 ± 0.0015 | 0.2069 ± 0.0012 | 0.2134 ± 0.0040 | |

g(L) = ln τ(5, L) − ln τ(4, L) = 1.5314 ± 0.0018, 2.3338 ± 0.0068, 3.0777 ± 0.0109, 3.802 ± 0.024 and the intercept
a(L) = ln τ(4, L) − 4·g(L) = 2.020 ± 0.008, 1.750 ± 0.029, 1.535 ± 0.046, 1.289 ± 0.098 at L = 3, 4, 5, 6.

**The rows formula against the strip** (holes' fit to the hull, the octahedron's row prices used at both rims
because the tetrahedron gives none): it has λ(w) = ln τ(w, L+1) − ln τ(w, L) = 2.543, 3.235, 3.927 for w = 4, 5, 6
at every L. Measured: λ(4) = 2.940, 2.761, 2.652 ± 0.011, 2.613 ± 0.026 (L 3→4 … 6→7); λ(5) = 3.743, 3.505 ± 0.011, 3.376 ± 0.024;
λ(6) = 4.536, 4.160 ± 0.035 (3→4, 4→5). The measured values depend on L, which the formula cannot; at the largest L they are 3 to
4% above it and still falling. Its increment per middle row, 0.692, against the measured 0.802, 0.744, 0.724 ± 0.026.
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

**The two exits have different length prices [measured, with this crude classifier].** Rate of each exit =
share / τ. For 4 rows the bust's rate falls by 3.032, 3.019, 3.000 per unit of length (L 3→4, 4→5, 5→6): **0.253,
0.252, 0.250 per cell, constant**; the fade's by 2.915, 2.704, 2.597: 0.243, 0.225, 0.216 per cell, falling (shares
0.227, 0.207, 0.160, 0.113 ± 0.003 and ln τ from section 2; e.g. [2.7611 − ln(0.160/0.207)]/12 = 0.2516). In the
width direction the two cost nearly the same (L = 5, 4 → 5 rows: 0.209 and 0.2045). So a rimmed strip's bust costs
0.25 per cell of added length where a closed face's costs 0.21, the fade is the cheaper exit and takes over as
L grows, and the falling length price of section 2 is the fade's. Not checked: any other definition of a bust.

## 5. Forecasts scored

Mine, `PREDICTIONS.md` block A (commit 993537c, 12:36 UTC, before any lifetime):
- A1 (my code reproduces rim's nine entries within 3 combined errors; I gave 0.70): **held** (largest 2.4).
- A2 ((4 rows, L = 7) = 18.97 ± 0.10; length price 6→7 = 0.208 ± 0.008): **missed** in both bookings (18.716 and
  19.111; 0.1874 and 0.2177). The branch I gave 0.20, "the rod begins to die as a rod", is what happened.
- A3 ((5 rows, L = 6) = 20.15 ± 0.12: **missed**, 20.3003 ± 0.0216. Width price at L = 6 = 0.2045 ± 0.006: **missed** narrowly,
  0.2112. "Goes on rising" (0.65): held. "Exceeds 0.2087" (0.2): it does, by about one error. Mixed difference at
  L 5→6 = 0.218 ± 0.03: held (0.241); "below the value one step earlier": held against my own 0.248, not against
  rim's 0.2262, which is what I meant.
- A4 (the two prices cross between L = 6 and 8 at 0.205 ± 0.007): not reached; at L = 6 to 7 they stand at 0.2112 and
  0.2177, both above my band: **missed** as far as it can be scored.
- A5 (firewall shares: (4 rows, L = 4) < 2%, (4 rows, L = 6) < 10%, (3 rows, L = 6) > 50%): **all three held**
  (0.0%, 3.0%, 85.6%).
- A6 (closed tubes: my 4×4, 4×5, 4×6, 5×5 within 0.02 of the lead's): **held** (−0.009, +0.006, +0.014, +0.008).
  Unseen 3×4, 3×5, 3×7 = 7.39 ± 0.03, 9.27 ± 0.05, 12.85 ± 0.15: **all held** (7.396, 9.267, 12.852).
- A7 (tetrahedron 4.0, 5.9, 8.6, 12.0, 16.0 at sides 3…7; second differences): **missed**: there is no steady
  lifetime at all. "Shorter-lived than the octahedron at every side" held in the trivial sense.
- A8 (tetrahedron faces fade, bust share < 0.05): held (0.000).
- Block B (commit c7ac402, 13:30 UTC): B1 (6 rows, L = 5) = 20.00 ± 0.06, width price 5 → 6 rows 0.205 ± 0.004:
  measured 19.916 ± 0.033 and 0.1994 ± 0.0023: both **missed** low by 1.4 of my errors; the branch I gave 0.15,
  "four rows already too thin at L = 5", is what the data say, at 2.4 of theirs. B2 mixed difference at (5.5 rows,
  L 4→5) = 0.246 ± 0.015: **missed**, 0.218 ± 0.012.

The PI's block 6 (`research/blast/PREDICTIONS.md`), items 2 to 8: (2) "row prices not monotone in depth": not
decidable (3 rows are too thin; from 4 rows up the price is flat in depth). (3) "tetrahedron faces live shorter
than the octahedron's at 45 and 63 cells": held, for a reason that empties the question; "second difference
within 0.015 of 0.231": not defined. (4) "mixed differences clean to 0.008 with controls": held at L 3→4 and 4→5
(0.003, 0.004), at the edge at 5→6 (0.028 ± 0.010 for the difference), and the thinness of item 7 is a systematic of
that size. (5) "length price at 6→7 below 0.2177": by all first deaths yes (0.1874), for face deaths proper no
(0.2177 ± 0.0021); "0.209 to 0.216": no in either booking. (6) "width price at L = 6 in 0.203 to 0.208":
0.2112 ± 0.0013, above (inside if (4 rows, L = 6) is low by 0.1 for thinness). (7) "reproduces rim's nine entries": held.
(8) "a strip's row is cheaper than a closed tube's at L = 4 and 5": held (−0.013 ± 0.001, −0.003 ± 0.001).

## 6. Failed, not checked, next

Failed or dropped: the row-price profile from w = 1 up (prisms of 1 and 2 unit rows do not hold chaos; the 3-row
strip is too thin to be a face: its step to 4 rows costs 0.21, 0.23, 0.24, 0.25 per cell at L = 4…7 where 4 → 5
costs 0.19 to 0.21, so "is the second row dearer?" cannot be separated from "is the body too thin?"); the
tetrahedron as a source of sharp-rim prices (section 3); a first version of the periodic censoring (section 1).
Not checked: a second seed for the long runs other than (5 rows, L = 3, 5, 6) and (4 rows, L = 3); whether 4
rows are thick enough at L = 6 and 7 (item 0.7 is an analogy with 3 rows; the direct test is 5 → 6 rows at L = 6,
ln τ ≈ 24); strips with the other rim kinds (odd numbers of half-rows, unequal constants); the firewall
booking against anything but the lead's table; the bust classifier against another definition; nobody has
rewritten this stepper; the hull forecasts are an analogy, not a derivation.
Next step: the row price at L = 6 and 7 from strips of 5 and 6 rows ((6, 6) ≈ 24, (5, 7) ≈ 23.6): a splitting
sampler on this prism (the `life` loop already restarts lanes; cloning lanes at low face population is a small
change). That one number decides between a row price that levels at the wrapped 0.21 and one that climbs to the
hull's 0.23.
