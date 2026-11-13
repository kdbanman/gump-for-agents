# Critic's journal (append-only)

A successor should read `board.md` first (the current state), then this file from the end backwards.
Commands are run from `research/theory/swarm/critic/lab/` unless a path is given.

## 2026-11-13, round 0

### Read

CLAUDE.md; swarm/PROBLEM.md; docs/AUTOMATON.md; theory/threshold.md; theory/thickness.md; toy2d/README.md and
PREDICTIONS.md; fluct/README.md; OPEN-PROBLEMS.md; theory/PROGRAM.md; AUDIT-2026-11-13.md; CLAIMS.md; lineage
README (§§2–5); NOTEBOOK entries of 2026-11-13; PRIOR-ART §3; theory/exponent.md (a stub: its verdict and body
are placeholders) with exponent/theorems.md and exponent/PREDICTIONS.md (through the 19:56Z entry); the code
that defines the measurements (`toy2d/geom.py`, the `qsd` mode of `toy2d/t2d.c`, `experiments/toy2d_check.py`,
`theory/check_threshold.py`, `reference/oracle.py`).

The solvers' directories were empty when I finished. The lead's "starting thoughts" are not in the repository
(searched for the phrase); if they exist only in the solvers' prompts I have not seen them.

### Tools built and how they were validated

- `exact.py`: for a vessel given as neighbour lists, the successor of every state (`full_map`, N ≤ 26), death
  times of every state for a caller-supplied "living" predicate (−1 = never dies), cyclic states, periods.
- `toy2d_lab.py`: the 2D rule on strips and boxes. `python3 toy2d_lab.py selftest` → ALL OK:
  (1) my neighbour-list stepper against the `step` function of `research/experiments/toy2d_check.py`, 15 strips
  × 200 generations, identical; (2) boxes against the same function on a strip with three extra dead columns
  (they stay dead and nothing crosses them: the firewall), 12 boxes × 200 generations, identical; (3)
  `full_map` against both on every state of strip 3 × 5, box 3 × 4, strip 2 × 7; (4) censuses of strips 2 × 5,
  2 × 7, 2 × 8 against the exponent agent's independent C program (`exponent/data/fg_summary.json`): cyclic
  states, immortal cyclic states, immortal basin, dead-at-0 all equal. Also strip 3 × 6: 2,259 cyclic states and
  an immortal basin of 20.0%, the two numbers quoted in exponent/PREDICTIONS.md.
- `gump_lab.py`: hulls (cube- and vertex-centred), faces, neighbour lists. `python3 gump_lab.py selftest` → ALL
  OK: T1 for 3 orientations × 8 signed diagonals; my vessel stepper = my open-lattice set stepper = the stepper
  of `research/theory/check_threshold.py` on 18 soups × 120 generations in hulls R = 5c, 7c, 6v (and nothing
  leaves the hull); my set stepper = `reference/oracle.py` `step` on a torus H = 24, 3 soups × 60 generations;
  `full_map` on the hulls R = 1c and 2v against the set stepper; face areas 30, 45, 63, 84 at R = 7, 9, 11, 13;
  hull R = 9 has 510 cells (the number in threshold.md). Census of the R = 2v hull reproduces CLAIMS T10 (107
  still lifes, 195 two-cycles, 2,750 states die, settle within 3).
- `sealed_min.py`: smallest sealed set of a vessel under side conditions, as an integer programme
  (scipy.optimize.milp / HiGHS); every answer is re-checked by `is_sealed`; "optimal" is the solver's proof.
- `face_one_step.py`: can a given configuration of one hull face be emptied in one generation by some choice of
  the cells beneath (SAT, pysat/Cadical)? Exhaustive over all configurations of the R = 3 and R = 5 faces.
  Cross-check: `face_game.py` (brute force over all 2^15 choices beneath the R = 3 face) gives the same 187
  configurations that need more than one generation.
- `checks_round0.py`: the structure facts listed on the board (rule texts, layer histograms, confinement and
  firewall widths, the edge-cell table, sealed sets by exhaustive enumeration of all subsets of small windows,
  the identity e + 2(a + b) = 4d, the hexagon ring, face-cell degrees). → ALL OK, about 50 s.

### Two statements of my own that the enumeration killed (recorded so nobody repeats them)

1. "Every sealed set of a box contains a whole *edge* row or column." False: three adjacent whole rows anywhere
   are sealed; so are large bent bands; and boxes with ≤ 5 rows have small extra ones (rows {1, 3} of a 5-row
   box: row 1 has only rows 0 and 2 outside the set, because row −1 is outside the vessel).
2. "A sealed set of a periodic strip that contains no whole row contains three adjacent whole columns." False on
   short rings: alternate whole columns (101010, L even) are sealed.
What survived: the *smallest* sealed set is a whole edge row or column (boxes 4 × 5, 5 × 5, 8 × 8, 9 × 10; strips
3 × 6, 4 × 6, 8 × 9); in the infinite strip of 3 or 4 rows every sealed set inside a window contains a whole
column (the toy2d README's statement, which is about the unrolled strip).

Hand argument I trust for large vessels (2D box, H, L ≥ 6): let W be sealed with largest column index X ≤ L − 3.
The two right neighbours of every cell of W in column X are in the vessel and outside W, so all its vertical
neighbours in the vessel must be in W. Taking the direction (1, ε) and then (1, −ε), column X contains a cell of
W in the bottom row and one in the top row, and then by induction the whole column. So a sealed set with no
whole column reaches within two cells of both the left and the right side; likewise for rows.
The same argument in a gump hull. Take v = −e_x plus a small generic vector and let c maximise v·p over a sealed
W. Six of c's twelve offsets have v·o > 0 (four with o_x < 0, two with o_x = 0, for every orientation of c);
those inside the vessel are outside W, so at least three of the six leave the vessel, hence at least one with
o_x < 0 does. An offset with o_x < 0 has d·o ≤ 0 for every diagonal with d_x = +1 (the offsets are (−1, ±1, 0),
(−1, 0, ±1), (−2, 0, ±2), (−2, ±2, 0)), so it can leave only through a face with d_x = −1. So the least-x cell
of any sealed set is adjacent to the outside across a face with d_x = −1, and likewise for the other five axis
directions: a sealed set reaches round the hull; none sits at one vertex or along part of one edge. I did not
turn this into a bound on the size of a sealed set; the integer programme says the minimum is one face for
R ≤ 7.

### Facts table of PROBLEM.md

Results are on the board (section "Errors in the problem statement" E1–E11 and the table after it).
How each was obtained:
- E1: weighted least squares on the seven (L, ln τ, error) rows of `research/toy2d/data/law_cross2_B34S234.json`:
  a + I·L → 0.7295 ± 0.028, 0.4160 ± 0.0014, χ² 28.9/5; L ≥ 20 → 0.4097 ± 0.0029, χ² 6.4/3; a + I·L + b ln L →
  I = 0.3744 ± 0.0088, b = 0.87 ± 0.18, χ² 5.8/4; a + I·L + c/L → I = 0.3954 ± 0.0045, χ² 5.4/4. These reproduce
  the README's own numbers; the README states the χ² too. The point is that PROBLEM.md quotes only the line.
- E2: ln τ = A·(−ln h/A) from the first row of the facts table = `ln_h` in `fluct/data/qsd_summary.json`
  (−6.805, −9.820, −13.632, −18.077); errors 1/√deaths with deaths 117,851, 137,243, 16,240, 342.
- E3, E10, sealed sets, sizes: scripts above.
- E8, E9: fields `fw`, `exposure`, `frm` of the same toy2d data file; `frm[7]` counts deaths whose edge had ≥ 7
  live cells one generation earlier (t2d.c, `from[]`). Exposure per terminating event at L = 28, 32, 36: 18,634,
  18,665, 16,860 generations.
- Tail ratios: `lnp` and `ln_h` of `qsd_summary.json`.

Not checked, and I say so on the board: every measured rate of gump and of the 2D rule (I can re-read tables,
not re-run ensembles); the GPU numbers; the symmetric fits; the lineage numbers; whether depth 16 is converged
for the 2D law beyond L = 16 (toy2d checked the depth only at L = 16); the 36-cell two-layer sealed set; the
measured items of the exponent study.

### Proofs read this round

- thickness.md Theorem 3 (no finite sealed set in ≥ 3 layers): correct; the identity it rests on checked for all
  3 orientations × 8 signed diagonals.
- exponent/theorems.md: Lemma A (i)–(iii) correct (table checked by hand and in `checks_round0.py`). Lemma A
  consequence (c) second sentence **false** (board E10). Theorem B (a), (b) correct as written; I followed (a)
  through arcs of length exactly 5, gaps of length 1, and the short rings L = 6, 7. Corollary B′, Theorems C, D,
  E, Proposition D′ correct. Remark 1 after Theorem E (covariance decay is not enough): the counterexample is
  valid as a statement about which implication holds.

### Unassigned ideas (mine; not given to any solver; the lead decides)

1. **Rim decomposition of the octahedral data.** With A = 3k(k+1)/2 the verified ln τ at k = 4…7 have first
   differences 3.015, 3.814, 4.444 and second differences 0.799, 0.630; an asymptotic per-cell cost would be
   (second difference)/3 = 0.27, 0.21. With the GPU numbers: 0.23, 0.24, 0.24. So if a perimeter term is allowed
   the octahedral data do not pin the area coefficient better than 0.21–0.27. A two-coefficient form
   (interior cells × g_i + rim cells × g_r) fitted to k = 4, 5, 6 gives g_i = 0.266, g_r = 0.103 and then
   over-predicts the next step (4.61 against 4.44 ± 0.05). Nothing here is a theory; it is a warning about what
   "γ" the octahedral numbers can support, and a reason to prefer the slab numbers as the target.
2. **Product-measure flash cost by transfer matrix** (`iid_flash.py`). If the edge row is i.i.d. Bernoulli(p_e)
   and the cells beneath i.i.d. Bernoulli(ρ), the probability that a periodic edge of L cells is empty one
   generation later is trace(T^L) for a 16 × 16 transfer matrix (checked against brute force at L = 8). Cost per
   cell −ln λ_max = 0.672 at p_e = 0.58, ρ = 0.472; 0.490 at p_e = ρ = 0.472; 0.389 at p_e = 0.40. So a one-step
   death from a product state at the measured densities costs 1.6 times the measured exponent: correlations or
   more than one step carry the rest. The same construction for a k-step death, or with the edge law replaced
   by a tilted (not product) law, would be a computable variational family whose infimum is a candidate formula
   for the exponent of a dice model. This sits exactly between "counting" and "probability".
3. **The dense channel as a second exponent** (2D). A fully live row dies in one step with probability
   (1 − (1 − ρ)²)^L from the rows beneath, cost 0.33 per cell at ρ = 0.472, which is below 0.41; yet the dense
   channel fades with L (22% of deaths at L = 12, none at L = 36). So the cost per cell of *filling* the row
   must exceed 0.08. Two exponents competing, with the cheaper total winning at large L, is a concrete instance
   of "least unlikely route".
4. **The face game for gump.** On the R = 3 face the adversary empties any configuration in two generations
   (324 configurations in one, 187 in two). Whether the depth stays bounded as the face grows (the 2D edge:
   three, for every L) is a clean exact question; for R = 5 it needs the reachable-set computation, which I did
   not do.

### State at the end of round 0

board.md written; no replies owed. Next: when a solver's round is announced, read its journal and claims.md,
write `to-<solver>.md` (section "Reply to round k"), update the board's three-lines, who-uses-what, lemma
exchange and lab tables.

### Addendum, same round: an interior counterexample for E10

The first counterexample to "a gump face can always die in one generation" used a corner cell of the hull face,
which has only four neighbours in the vessel. `face_one_step_interior.py` imposes only the constraints of
cells deep inside the R = 13 face (all nine neighbours present, and the same for their face neighbours), so
the rim plays no part and the obstruction holds on any larger or periodic face. Smallest case: the kagome
triangle (4,4,5), (4,5,4), (5,4,4) plus (3,4,6) in the layer x + y + z = 13. By hand: (4,4,5) is a z-normal
cell whose face neighbours are (5,4,4), (3,4,6), (4,5,4), (4,3,6), (6,2,5), (2,6,5): three alive; beneath it
(3,4,4), (4,3,4), (2,2,5). (4,5,4) is a y-normal cell whose face neighbours are (5,4,4), (3,6,4), (4,4,5),
(4,6,3), (6,5,2), (2,5,6): two alive; beneath it (3,4,4), (4,4,3), (2,5,2). The first needs (3,4,4) alive,
the second needs it dead.
