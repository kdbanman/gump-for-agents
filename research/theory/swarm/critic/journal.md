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

## 2026-11-13, round 0b (second critic): the revised PROBLEM.md, its four starting points

I am the successor of the critic who wrote everything above. I took over `board.md`, this journal and `lab/` as
they stood (commit 0fc0da1). Both self-tests still print ALL OK (`python3 toy2d_lab.py selftest`, 5 s;
`python3 gump_lab.py selftest`, 1 s). PROBLEM.md was revised twice after round 0: it now has "Starting points"
(board E11 said they were missing), a fourth line (**source**) and a librarian (commit 13bbdad). New scripts this
round: `startpoints.py` (subcommands below; `python3 startpoints.py all` → ALL OK in 12 s) and `dice_w1.py`.

### 1. Counting: the bijection lemma is true, with a convention; a stronger form; what it cannot reach

Let f be a bijection of a finite set X, H ⊆ X non-empty, T(x) = min{t ≥ 0 : fᵗ(x) ∈ H}, T = ∞ if the cycle of x
misses H. **Claim (PROBLEM.md): the mean of T over X is ≥ |X|/(2|H|) − 1/2.** Proof. If a cycle misses H the mean
is infinite. Otherwise a cycle of length ℓ carrying m points of H is cut into gaps g₁ + … + g_m = ℓ, and the points
of a gap have T = 0, 1, …, g − 1, so the cycle contributes Σ g_i(g_i − 1)/2 ≥ (ℓ²/m − ℓ)/2. The function (ℓ, m) ↦ ℓ²/m
is convex and homogeneous, hence subadditive, so Σ_cycles ℓ²/m ≥ |X|²/|H|. ∎ Equality iff all gaps are equal.
Checked exhaustively for every permutation of n ≤ 7 points and every H (689,569 cases; `startpoints.py bijection`).
Three things a user of the lemma must know.
- *Convention.* With the mean taken over the points that do fall, the bound is |X′|/(2|H|) − 1/2, X′ = the union of
  the cycles that meet H, and can be far below |X|/(2|H|) − 1/2 (identity map, H one point: 0 against (n − 1)/2).
- *It bounds a mean. The union bound is stronger and simpler:* #{x : T(x) ≤ t} ≤ (t + 1)|H|, because {T ≤ t} is the
  union of the t + 1 sets f⁻ˢ(H). It needs only that the measure is invariant: for any map F and any F-invariant
  probability μ, P_μ(T ≤ t) ≤ (t + 1) μ(H). It bounds the whole law of T and implies the mean bound.
- *For gump and the 2D rule in a finite vessel no invariant measure charges the trapdoor.* Every invariant
  probability measure of a map of a finite set sits on cycles. Let H_k = {face non-empty now, empty k generations
  later}. A periodic state in H_k would have an empty face at time k, hence at all later times (T2), hence at a
  multiple of its period, hence now: contradiction. So μ(H_k) = 0 for every invariant μ and the bound is empty.
  For a uniform start and a map that is not a bijection, P(T ≤ t) ≤ Σ_{s ≤ t} |F⁻ˢ(H)|/|X|: the object to count is
  the k-step preimage, as the starting point says.
How far from invertible (`startpoints.py image`, every state): one generation loses 2.5 of 20 bits (2D box 4 × 5),
2.4 of 24 (strip 4 × 6), 1.7 of 12 (gump hull R = 2v), counted as log₂(|X|/|F(X)|); |Fᵗ(X)|/|X| = 0.19, 0.076, 0.037,
0.019, 0.011, 0.0066 for t = 1…6 in the 4 × 6 strip; the eventual image is 0.05–0.2% of the states (12% in the
12-cell hull).

### 2. Probability: the capped rule against the monotone rule (two-line lemmas)

G = gump (or the 2D rule), F = the uncapped threshold rule (alive next iff n + x ≥ 4, resp. 3). F is monotone,
G ≤ F at every cell, and they differ exactly at cells with n ≥ 6 (resp. 5) (`startpoints.py monotone`).
- **Majorant.** Gᵗ(S) ⊆ Fᵗ(S) for all t (induction: G(Gᵗ⁻¹S) ⊆ F(Gᵗ⁻¹S) ⊆ F(Fᵗ⁻¹S)); the same with shared dice
  beneath a driven face. So the monotone rule bounds the capped lifetime from *above* only.
- **No monotone minorant.** If H is monotone and H ≤ G then H(S) ⊆ H(V) ⊆ G(V) for every S (V = all cells alive),
  and H(H(S)) ⊆ H(G(V)) ⊆ G(G(V)). Computed: G(V) is the six vertex cells of a cube-centred hull (in-vessel degree
  4; R = 5, 7, 9), the four corners of a 2D box, and empty in vertex-centred hulls (R = 6), slabs, strips and tori;
  G(G(V)) = ∅ in every case. So **every monotone map below the capped rule dies within two generations from every
  state.** For a driven periodic face the same holds dice by dice: a full face has k = 6 in-face neighbours at
  every cell, so G_ω(full face) = ∅ for every ω.
Consequence for the starting point "the cap as a bounded perturbation of a monotone rule in the regime that
matters": a sandwich from below on the whole state space does not exist; the regime (a class of configurations)
has to be named, and it is not invariant under the dynamics for free.

### 3. The cube lemma: how a gump face shares the cells beneath it

Face layer d·p = R for a diagonal d (say d = (1,1,1)). A cell p of it with normal axis a is the "top" face q + e_a
of the cube with centre q = p − e_a (all even, d·q = R − 1). That cube's six faces are q ± e_x, q ± e_y, q ± e_z:
three in the face layer and three in the layer R − 2. From the offsets (AUTOMATON §2), with {a, b, c} = {x, y, z}:
the two neighbours of p one layer in are p − e_a − e_b = q − e_b and p − e_a − e_c = q − e_c (the two bottom faces
of its own cube that are perpendicular to it); two of its in-layer neighbours are q + e_b, q + e_c (the other two
top faces of its cube); its neighbour two layers in is p − 2e_b − 2e_c, and p ↦ p − 2e_b − 2e_c is injective.
**So the face layer is the disjoint union of triples (the three top faces of one cube, a kagome triangle of one
of the two orientations, one cell of each normal axis); beneath a triple lie the three bottom faces u_x, u_y, u_z of
the same cube and three private cells v_x, v_y, v_z; and the number of live cells beneath the face cell of axis a is
b_a = u_b + u_c + v_a.** Different cubes share nothing. Checked on the R = 13 hull face (`startpoints.py
triangles`): all 84 cells fall into 28 triples, rim included; 84 cells one layer in, each beneath exactly two face
cells; cells two layers in private. Of the 64 values of (b_x, b_y, b_z) ∈ {0..3}³ exactly 40 occur; (3, 0, ·) does
not (b_x = 3 forces u_z = 1, so b_y ≥ 1): this is the frustration of board E10 in closed form. One-generation
emptiability of a face is therefore a condition cube by cube; recomputed that way it reproduces the SAT counts of
round 0 (187 of 512 at R = 3; 180,615 of 262,144 at R = 5 cannot be emptied in one generation).
**Face game on hull faces** (`startpoints.py game 3`, `game 5`; the latter takes 2¼ minutes): with the cells beneath
chosen freely each generation, every configuration of the R = 3 face (9 cells) and of the R = 5 face (18 cells) can
be emptied in at most **two** generations (R = 5: 81,528 in one, 180,615 in two, none in more). Not known for
larger or periodic faces (the first periodic face without doubled neighbours is 3 × 3, 27 cells).

### 4. The one-row dice model of the 2D rule, exactly

Model **D2(L, ρ)** (= `toy_model(1, L)` of `exponent/xp.py`): a ring of L edge cells follows B34/S234; the two cells
beneath each edge cell are i.i.d. Bernoulli(ρ), redrawn every generation. Given the row the cells update
independently with P(alive | own state s, k live in-row neighbours) = P(k + b ≤ 4, k + b + s ≥ 3); (dead, k = 0)
stays dead and (live, k = 2) stays alive with probability one, every other case is random. `dice_w1.py` builds
the kernel on the orbits of the dihedral group and takes its Perron eigenvalue λ; τ = 1/(1 − λ).
Validation (`python3 dice_w1.py check` → ALL OK): kernel against direct enumeration of the 2L cells beneath (L = 5);
reduced against full kernel (L = 8); and against the exponent study's *sampled* values: exact ln τ = 4.4000, 6.4169,
8.6350 at L = 8, 12, 16 against 4.390 ± 0.018, 6.418 ± 0.010, 8.622 ± 0.012. So graveyard 7's first number is now
checked. Table (`python3 dice_w1.py 0.472 18`, 15 s):

| L | 8 | 10 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|
| ln τ | 4.4000 | 5.3838 | 6.4169 | 7.0061 | 7.5765 | 8.1122 | 8.6350 | 9.1571 | 9.6834 |
| step from L − 1 | 0.615 | 0.428 | 0.550 | 0.589 | 0.570 | 0.536 | 0.523 | 0.522 | 0.526 |
| h/p₁ | 0.428 | 0.409 | 0.399 | 0.396 | 0.394 | 0.394 | 0.394 | 0.394 | 0.395 |
| deaths from n = 1 | 66% | 69% | 71% | 72% | 72% | 72% | 72% | 72% | 72% |
| deaths from n ≥ 7 | 30% | 23% | 17% | 15% | 12% | 11% | 9% | 8% | 7% |

Quasi-stationary density 0.645–0.650; second eigenvalue 0.47–0.52 (L = 9–13), so the model forgets its state in
about 1.5 generations. **The step per cell oscillates with L (0.43 at L = 10, 0.59 at L = 13) and is 0.52–0.53 from
L = 16**: no slope should be read from exact data at L < 15. Unlike the real 2D rule, h/p₁ is flat (0.394) from
L = 13. ρ = 0.5 instead of 0.472 changes ln τ by +0.04 at L = 16 (8.6764; step 0.528).
Product-measure one-step cost (`iid_flash.py`), for comparison: 0.760 per cell at the model's own density 0.6455,
0.5515 at p_e = ρ = 1/2 (i.e. a fraction 0.5761ᴸ of all states of edge + two rows has an empty edge next).

### 5. Path: crossing times; sealed sets beyond the face

- `startpoints.py crossing`: the farthest two cells of a hull face are 5, 6, 7, 8, 9, 10 generations apart at
  R = 7, 9, 11, 13, 15, 17 (graph distance; the same through the vessel as inside the face layer); from the
  best-placed cell everything is within 4–8. The measured plunge takes 10–12 generations at A = 30–84 (ordinary
  until −16): longer than the crossing time of every face on which it was measured.
- Hulls (`sealed_min.py`, integer programme): the smallest non-empty sealed set is one whole face, proved optimal,
  for R = 3c, 4v, 5c, 6v, 7c (round 0) and now 8v, 9c, 10v (30, 45, 45 cells; 1–14 s). R = 11, 13: not proved within
  100 s. The "smallest sealed set containing no whole face" of round 0 (57 cells at R = 7) is a face minus three
  cells thickened into the next layer (27 of the 30 cells of one face), not a different kind of object.
- Periodic slabs (`startpoints.py slab`; my slab stepper is validated there against the open-lattice stepper on the
  unrolled pattern): three consecutive layers of any of the other three diagonals close up on the torus and are
  sealed (two are not). For an N × N torus the band has 13N cells at m = 3, 36N at m = 8, 54N at m = 12 layers
  (≈ 4.5·m·N) against 3N² for a face: **smaller than the face once N > about 1.5·m** (65 < 75 at 5 × 5 × 3; 468 < 507
  at 13 × 13 × 8). The integer programme proves the face is the smallest sealed set at 3 × 3 × 3, 4 × 4 × 3, 4 × 4 × 4,
  3 × 3 × 8, and finds the 65-cell band at 5 × 5 × 3 (optimality not proved within the time limit). This is thickness.md's remark
  and the notebook's measured "transverse firewall" channel (2026-11-12: ln τ_fw ≈ −1.4 + 0.54·N·m + 0.22·N, about
  0.12 per band cell); PROBLEM.md's facts table does not mention it.

### 6. Source: permutive automata as dice

**Lemma.** Let a cellular automaton on Z^d over a finite alphabet have neighbourhood N and local rule f, let
e ∈ N, e ≠ 0, be a vertex of N in the sense that some linear ℓ has ℓ(e) > ℓ(n) for all other n ∈ N, and let f be
permutive in the variable at e (a bijection of it for every setting of the others). Start from the uniform product
measure. If P is a set of cells no two of which differ by an integer multiple of e, then
{x_p(t) : p ∈ P, t ≥ 0} are i.i.d. uniform.
*Proof.* x_p(t) depends on the initial cells p + N_t (N_t the t-fold sumset), on which ℓ is maximal exactly at
p + te. (i) For fixed values of the other cells of p + N_t, x_{p+te}(0) ↦ x_p(t) is a bijection: by induction, in
x_p(t+1) = f(x_{p+n}(t) : n ∈ N) only the variable n = e involves the cell p + (t+1)e (the others live on
p + n + N_t, where ℓ < ℓ(p) + (t+1)ℓ(e)), that variable is a bijection of it, and f is permutive there. (ii) Take
finitely many (p_i, t_i) with the cells q_i = p_i + t_i e distinct (that is the hypothesis on P), ordered by ℓ(q_i).
The last value is a bijection of x_{q_m}(0) given all other initial cells, and no earlier value depends on q_m
(ℓ(q_m) ≥ ℓ(q_i) and q_m ≠ q_i). So it is uniform and independent of the earlier ones; induct. ∎
So the statement in PROBLEM.md ("bipermutive, one cell") is true and needs permutivity on one side only (rule 30
qualifies). The classical bipermutive statement (r − l adjacent columns of a one-dimensional rule with
neighbourhood {l..r}) is a different sufficient condition. `startpoints.py source` checks both by enumeration:
rule 30, one cell, t ≤ 6: all 128 words equally often; rule 30, two adjacent cells: 200 of 1,024 words; rule 90, two
adjacent cells: uniform, three: not; x′ = x₊₂ ⊕ (x₀ ∧ x₊₁) (e = 2), cells 0 and 1: uniform, cells 0 and 2: not; in two
dimensions the linear rule on offsets (0,0), (1,0), (0,2) makes rows 1 and 2 (5 columns, t ≤ 4) independent (rank 50
of 50 over GF(2)), the rule on (0,0), (1,0), (0,1) does not (rank 34).
Two cautions. **Entropy.** A deterministic system started from N random bits emits at most N bits of exact dice;
in the lemma each die x_p(t) uses up the fresh cell p + te, so dice for T generations need a source T·|e| deep. A
confined vessel of N cells cannot supply exact dice to a face for the e^{cA} generations a lifetime theorem is
about; "word for word" transfer needs an unbounded reservoir. **Confinement.** A binary rule with a quiescent
dead state that is permutive at e gives birth from a single live neighbour (the cell p − e of a lone live cell p),
so T2 and T3 fail inside any such source; what survives is that an empty face over it is absorbing, which uses only
the face rule and the number of cells beneath a face cell (3 < 4; in 2D 2 < 3).

### 7. T5 re-derived (threshold.md §2–3; the first critic had checked the rule text only)

ΔE = −Σ_i (x_i(t+1) − x_i(t−1))(h_i(t) − 3.5) follows from the symmetry of W in two lines; the case analysis
(non-overcrowded mismatch: ≤ −1/2; overcrowded and alive at t − 1: h − 3.5 ≥ 2.5; overcrowded and dead at t − 1: 0)
is right; −6N ≤ E ≤ 7N; hence with no O1 event from some time on the orbit has period ≤ 2 within 26N + 1 steps.
"Freezes" in the source starting point means "reaches period ≤ 2".

### Decisions about the board

E11 closed (the starting points are now in PROBLEM.md) and replaced by a section "The lead's starting points: what
I checked"; E12–E14 added; graveyard items 14–16 added (monotone minorant; exact dice from a finite reservoir;
"not sealed ⇒ cannot nucleate"); the dice models get names (D2, D3) so that lines can be pointed at one object;
library and source added to the map. Citations: the shelf (`library/shelf.md`) exists since 22:30; board lemmas
taken from the literature are marked with whether they are on it.

## 2026-11-13, reply to path, round 1 (`to-path.md`)

Script: `lab/path_r1.py`. What was established (the reply has the short form, the board the tables).

- **Checked and found correct:** path's rim lemma L1(a, b); Theorem P and Corollary P1 (proof followed line by line:
  the recursion w_{t+1} ≤ (a w_t + ε)/(1 − s̄) needs y = a w_t + ε ≤ 1 − s, which is the hypothesis a + ε ≤ 1 − s̄; the
  geometric series needs a < 1 − s̄); its worked numbers (`psharp`); L3 (sealed ⟺ complement bootstrap-closed) and
  L4 (top-layer rigidity).
- **Counterexample to L1(c) as worded** ("each constraint involves a private cell beneath"): the three corner cells
  of a hull face have two cells beneath and both are shared (R = 5, 7, 13; one-off enumeration with
  `startpoints.face_setup`). Every other face cell has exactly one private cell.
- **Path's hypothesis H (Theorem P with φ = r^{min(n,K)}, Z = face population) is false**, on the measured gump
  table (`lr1`: a₁(r) > 1 for all r ≤ 0.9 at A = 30…84) and in the exact dice model (`lr2`: best bound ≈ 1).
  Reason: row n = 1. **With φ free it holds** (linear programme, `lr2b`, `lr1b`): D2: bound within a factor 9–14
  of h for L = 8…16; gump's measured rows (k < A/2): −ln(bound) = 2.82, 5.78, 9.53, 14.02 against 6.81, 9.82, 13.63,
  18.08, a loss of 4.0 nats at all four sizes, so the slope is carried entirely by the row-wise contraction.
  Formulation that matters (I got it wrong once): φ free on 1…K − 1, constant from K on, ε a variable, constraints
  for every measured row including those above K; minimise ε; bound ε/(1 − a). Forcing ε = (1 − a)·φ(K) instead
  lets the programme put φ(K) = 0 and reports nonsense.
- **Gump's collapse lengthens with the face** (`lr3`, existing pre-death histories): half-way lag 3.2, 4.7, 5.9,
  6.8 generations at A = 30, 45, 63, 84; the mean population looking back from death is one curve at all sizes
  until it saturates. Board E14 rewritten accordingly. This contradicts the reading "a ~10-generation plunge at
  every size" of fluct README (which describes the largest faces).
- **D2 on a segment** (`seg`; equals D2 on a ring with two adjacent cells removed, the dice-model version of path's
  exam E1): ln τ at L = 5…14 in the board's lab table (L1.5); longer-lived than the ring of equal length at every
  L ≤ 14, with smaller steps per cell (0.45–0.50 against 0.52–0.53). Cannot separate "same exponent, power of L"
  from "different exponents" at these sizes.
- **Decision: tallies in `research/scratch/fluct/` are admissible for arithmetic** (no new runs), after checking
  deaths and exposure against the committed `qsd_summary.json` (identical for R = 7, 9, 11, 13). Stated on the
  board under "The lab". Field meanings (from `research/fluct/qsd.py`): `Tr[k, k′]` counts one-step transitions of
  each of the 8 faces from population k < KMAX = (A + 1)//2 to k′ (k′ = 0: that face died), over replicas with all
  faces alive and age ≥ T0; `pre[d, 64 − s, 0]` is the population of the dying face s generations before death d.
- **Refits of the window decrement** (`data`): the extrapolated limit depends on the assumed approach (0.348 to
  0.373 on ℓ ≥ 20). My error model treats numerator and denominator counts as independent, which overstates the
  errors; the χ² values are for ranking the forms only.

## 2026-11-13, reply to source, round 1 (`to-source.md`); the librarian's first pass; curated tallies

Script: `lab/source_r1.py`.

- **Checked and found correct:** source's Lemma 1 (exact source with feedback; the triangular-bijection proof, and
  `l1`: a bijection of {0,1}²¹ on the 3 × 7 box); Lemma 2 (chain rule); Lemma 3 (one-step projection) and its
  transfer identity; Lemma 4 (weighted pair energy K = Σ a_i a_j W_ij x_i(t) x_j(t−1) − θ′ Σ a_i²(x_i(t) + x_i(t−1));
  proof followed; `l2`: identity and inequality on all 2²⁴ pairs of states of the hull R = 2v and of the box 3 × 4,
  and the termwise bounds over every local picture, where the minima equal m and −c′ exactly). Corollary 4a
  (uncapped rule on infinite configurations: at most C_U mismatches per cell, hence cellwise period ≤ 2) follows
  and closes the open item of `research/theory/threshold.md` §6. For gump at λ = 1.1, S = 13,336 and
  C_U = 1.4×10⁶.
- **Corrections sent:** "constant hazard ⇔ constant conditional law" is only ⇐; Lemma 2(b) excludes conditioning
  on the whole past, not on a window (a maximal-length shift register is nearly uniform given fewer than N
  previous bits); two wordings in Corollary 4b.
- **A two-line lemma of mine, put on the board ("starvation"):** in a face with ≤ 3 live cells a live face cell has
  k ≤ 2 and b ≤ 3, so n ≤ 5: never overcrowded. Deaths from n ≤ 3 are deaths by n ≤ 2.
- **L3** (`l3`): the 2D strip 4 × 6 has no quasi-stationary window (the unsettled population with row 0 alive is
  gone by t = 21), and in it the rows beneath a one- or two-cell edge are far more lethal than dice of the same
  density (×2 at one cell, ×16 to ×250 at two). No vessel that can be enumerated will have a window.
- **The librarian's remark "a finite deterministic system has no non-trivial conditionally invariant measure"
  is right.** My proof: let μ on M (the complement of the hole) satisfy Σ_{x ∈ M, Tx = y} μ(x) = λ μ(y), 0 < λ < 1.
  Every y in the support has a preimage in the support, so following preimages the support contains a cycle
  y, Ty, …, T^k y = y inside M. Along it λ μ(Ty) ≥ μ(y), so μ(y) ≤ λ^k μ(y) and μ(y) = 0: contradiction. (The
  librarian's `qsd.md` gives another proof: the map restricted to M is a 0/1 matrix whose non-zero eigenvalues
  are roots of unity.) Board: lemma exchange "trapdoors" (v); graveyard 19.
- **Library items taken to the board, each compared with the note (not with the paper):** Durrett's comparison
  theorem has no monotonicity hypothesis and needs uniformity over the outside (graveyard 6 reworded);
  Galves–Schmitt 1990 and Abadi–Chazottes–Redig–Verbitskiy under "mixing ⇒ exponential"; Mountford 1993 Prop. 1.2
  and Schapira–Valesin Prop. 2.9, with where they use monotonicity; Méléard–Villemonais as the readable source for
  Darroch–Seneta; supertransients.
- **Decision (at the lead's request): the tallies the lab reads are now a committed file,**
  `lab/data/fluct_tables.npz` (66 kB), written by `lab/curate_fluct.py` from `research/scratch/fluct/qsd_R*.npz`.
  It holds Tr, H, J, deaths, exposure, and per-lag histograms of the pre-death population (the raw `pre` arrays
  are 30 MB). `path_r1.py lr1`, `lr1b`, `lr3` read only that file and reproduce the numbers of the reply to path
  (re-run after the change). The "first lag with n ≥ half the living mean" histogram is stored too (`lasthalf`).

## 2026-11-13, reply to counting, round 1 (`to-counting.md`)

Script: `lab/counting_r1.py`.

- **Checked and found correct:** counting's Lemma 1 (same as mine), Lemma 2 (second-order lift: `lift`, every
  pair-state of two small vessels), Theorem 3 (finite-horizon transfer matrix; `c1`, `c2`), Proposition 4 (a) at
  k = 1 on boxes and (c) at k = 1 on the C4 box 7 × 7 (`c4`), Lemma 5 (= the cube lemma; `lemma5`, SAT against the
  criterion on periodic faces 2 × 2 and 3 × 2), claims 7, 9, 12, 14, 15 (inequality), 16 (arguments read).
- **Exact constants:** c₁ = 0.551535, c₂ = 0.467693 at soup density ½; 0.489963, 0.4671 at 0.472. The horizon-2
  matrix lives on 2¹⁶ window states (row 0 over 8 columns, rows 1–2 over 4), rows 3–4 of the centre column summed
  out; it is validated by `ring_sum` against the full map of the strips 5 × 4 and 5 × 5 (the trace of Mᴸ is
  computed as a sum over L-periodic sequences of new-column bits, 8ᴸ terms, not by matrix powers).
- **c⁰_k = c_k for k = 1, 2** (free ends cost the same exponent as a ring at those horizons): the k = 1 graph is
  strongly connected; for k = 2 the strong component of the all-dead window has 54,591 of 65,536 states and all
  others are singletons.
- **A mistake of mine, caught by the exact count:** for the box I first applied the closed-walk formula to the
  reduced 16-state matrix with L + 4 steps; that gives the padding cells the weight of a dead cell with random
  cells beneath. In the reduced form the walk has L steps, from a window 00** to a window **00.
- **Claim 15's hypothesis fails from generation 2** in strips 4 × 5, 4 × 6, 5 × 5 (`coll`); structural reason:
  Σ μ² ≥ (largest atom)².
- **The C4 slope is measured under heavy settling** (`data`: 97% of exits at L = 16 down to 32% at L = 36). I told
  counting it is the weakest of the three slopes to rest a contradiction on.
- **Counting's exam entry C-E1** (one mirror in gump: slope 0.110 ± 0.010, refuted if < 0.098) bets against the
  measured trend that symmetric faces are cheaper per independent cell (A/7.7; new GPU points 0.197 per
  independent cell at A = 759–828). Told them; the entry is theirs.
- **News from the lead taken to the board:** the GPU numbers at A = 108, 135 are reviewed (E2); new symmetric
  points at A = 759, 828 (E5). I read the review's summary and CLAIMS GP1/GP2; I recomputed nothing.
- **Overlap recorded:** counting's Proposition 4 with C1 implies path's guess G1 ("one exponent in every
  geometry"); path keeps the data reading and the power of L, counting the finite-horizon exponents. Counting's
  claim 15 and source's class 𝒦 are both hypotheses on an equal-time law of a few rows.

## 2026-11-13, reply to probability, round 1 (`to-probability.md`); addendum to source

Script: `lab/prob_r1.py`.

- **A faster exact tool.** For one row over dice the kernel never has to be stored: (Qf)(S) = Σ_{S′} Π_y P(S′_y | S) f(S′)
  is contracted one cell at a time (probability's own cost note), by `einsum` on arrays with at most M + 5 binary
  axes. `prob_r1.py check` agrees with the orbit-reduced dense kernel (`dice_w1.py`), with `path_r1.py seg`, and,
  for reflecting ends, with the dense kernel of the mirror-symmetric ring with mirrored dice, to 10⁻⁸. Rings to
  L = 18–19 and intervals to M = 19 take a few minutes; L = 20 would take about five minutes per law.
- **Checked and found correct:** probability's table a(x, k); its minorant table (enumeration over completions,
  203 laws); the three-generation bound at π₁ = 0; Theorem A's block step; Lemma 2(a); Lemma 2(b)'s κ (and the
  exact supremum of the contraction ratio on a ring of 14, which is below κ); claim 8. Theorem A rests on two
  percolation facts cited from memory (critical density of two-parent oriented site percolation ≤ 0.7491; survival
  for e^{cK} on a cylinder at any supercritical density). Neither is on the shelf; request appended to
  `library/requests.md` (the one file outside my directory I have written to).
- **The result of the round (lab L4.2, board E15).** D2(·, 0.472) on an interval: dead ends and reflecting ends both
  have steps of ln τ equal to 0.460 from M = 16 on, and ln τ_dead − ln τ_refl = 0.837 ± 0.001 from M = 15. The ring's
  steps are 0.52–0.53 at L = 15–19. The three ratios of the deterministic 2D rule that looked anomalous (mirror
  ring / ring = 0.42; box / ring ≈ 0.83–0.89; box = half-mirror) are reproduced by the dice model (0.44; 0.88;
  equal). ln τ_ring − ln τ_dead over L = 11…19 is fitted by −4.30 + 1.21 ln L (rms 0.016) and by −2.27 + 0.082 L
  (rms 0.028): a power of L in the ring's lifetime is the better description but the two are not separated.
  This is what path guessed for the real rule (its G1) and what probability's T2 and counting's C1 need.
- **Reconciliation.** My "no monotone minorant" (round 0b) is about deterministic maps and about gump faces over
  dice. For a single row over dice a monotone minorant *in law* exists (probability's Lemma 1: the dice are
  redrawn as a function of the state in the coupling) and is subcritical for independent rows (Lemma 2).
  Graveyard 14 reworded.
- **Pointer given to source** (addendum in `to-source.md`): the probability line's model is E₁(π); what is proved is
  near the anchor (½, 0, ½), which a binary deep-permutive bulk does not realise (it gives Bin(2, ½)).

## 2026-11-13, reply to path, round 2 (appended to `to-path.md`)

Script: `lab/path_r2.py`; `lab/curate_fluct.py` now also saves the face-population histograms of A = 108, 135, 165.

- **Checked and found correct:** Theorem P̄ (identity (I): Σ_z F(z, z′) = N(z′) − P(start at z′) + P(end at z′), which
  uses S_{t+1} ⊆ S_t; then the cancellation of the finite double sum); Lemma 1′; Proposition S; Proposition R (proof,
  and the absorption equations solved for every starting set on four graphs); the "d-deep" inequalities of
  Corollary 4a (hulls R = 7, 9, 11).
- **The committor of the pooled table (LR4).** ψ*_K = (I − T̄_{<K})⁻¹ d̄ is insensitive to K and is *not* the same at
  the four sizes: it steepens with A (log-slope 0.52, 0.55, 0.58 at A = 45, 63, 84 over k = 5…10). Only ψ*(1), ψ*(2),
  ψ*(3) are nearly common. So path's H′ with size-independent constants is not supported; a limit at large A is
  not excluded (63 and 84 differ within the noise for k ≤ 7).
  Caution for a successor: the "identity deaths = Σ entries × ψ*" comes out exact to four digits in `lr4` because the
  arrivals from untallied rows are *defined* there by identity (I); it is algebra, not a test.
  The table's deaths are face deaths (120,863 at A = 30) while `qsd_summary.json` counts dying replicas (117,851):
  2.6% of deaths at A = 30 take more than one face at once (0.2% at A = 45).
- **The population is not Markov along death paths (LR6).** Reversing the pooled table from the death shares
  gives a pre-death curve that rises about half as fast as the recorded one. This qualifies path's "remnant" and
  its exam E3, and it is where source's kernel κ_t (the drive given more than n) has to enter.
- **Relation (M) (LR7).** The histogram is not a parabola joined tangentially to a line: between n ≈ 14 and 28 at
  A = 84 its slope is below both branches. With each face's own mean, variance and tail slope the formula is 0.92
  and 1.56 nats above ln p(mean) − ln p(1) at A = 63, 84. Path's agreement "to ± 0.01 in the slope" came from
  differentiating at fixed θ.
- **D2, window probabilities under the exact quasi-stationary law (LR8′)**, with a new left-multiplication routine
  (`make_apply_left`, same contraction as `prob_r1.make_apply`): corner windows of a segment cost 0.475–0.53 per
  cell at ℓ = 3…8 (18 cells; decreasing with the length of the segment), interior windows and ring windows 0.605–0.61.
  Together with the exponent study's sampled windows on a ring of 128 (which equal mine at ℓ ≤ 4 and then fall to
  0.51 at ℓ = 25), the ring's window cost in D2 extrapolates to the interval's exact exponent 0.46 with a power
  ℓ^{−1.3}. Recorded on the board under E15 as support for "one exponent, the ring carries a power".

## 2026-11-13, reply to source, round 2 (appended to `to-source.md`)

Script: `lab/source_r2.py`.

- **Checked and found correct:** source's Lemma 1′ and Proposition 1″; Lemma 5 (`frozen`); Theorems H and U as
  conditional statements; the lone-cell formula of S11 (`l5`: enumeration of the 18 drive cells that matter on a
  4 × 4 periodic face). Its "smallest case" identity P(death | one cell) = (1 − ρ²)⁵ holds in my D2 eigenvectors to
  16 digits (share of deaths from one cell × h/p₁), an independent check of `dice_w1.py`.
- **The measured row from one cell is the dice row at ρ ≈ 0.52 across all of n′ = 0…4** (`l4`), not only in the
  two numbers source fitted. **But the layer beneath a face of 1–12 cells is poorer than usual** (0.33–0.39 against
  0.44; curated `J`). So "richer drive beneath a precarious face" can only be local. Recorded as lab L6.1, L6.2.
- **No screening at depth 2** (`l6`, with a new exact two-row kernel `lntau_w2`, columns as units, validated
  against enumeration of the dice): the dependence of ln τ on the dice density is as large or larger with two
  rows than with one, at L = 5…8. The exponent study's sampled value for two rows at L = 8, 3.929 ± 0.010, is 2.4σ
  below my exact 3.9535; its one-row values agree with mine within 1.1σ.
- **Face game on periodic faces** (`l7`): two generations suffice on 2 × 2 and 3 × 2 (as on hull faces R = 3, 5).
  The 18-cell case takes five minutes; a 27-cell face would need a compiled or vectorised version.
- **Strict finite energy fails in the 4 × 6 strip** from t = 3 (`l8`).
- **Routing.** Source's monotone-kernel comparison for the population is correct and is on the board (lemma
  exchange) for path. Source's Lemma 1′ realises probability's anchor: the board now records "a deterministic
  automaton on a half-plane with the law as a theorem, modulo two cited percolation facts" as the joint result of
  those two lines.

## 2026-11-13, pause (usage budget). State for a successor

The lead paused the group while I was on counting's round 2. **`board.md` now opens with "Where the queue
stands"**: what each line is owed, which lab work is half done, the overlaps being watched, the exam entries on
file. Read that first. What follows is what is not on the board.

- **Counting round 2: what I did and did not do.** Re-derived by hand: its Lemma 6 and consequences (including
  "the fixed-age exponent depends on the soup" and the dice hierarchy w ≥ 2k − 1), Lemma 7 (also run:
  `counting_r2.py lemma7`), the lone-triangle formula of its entry 12 (from the offsets: the six neighbouring
  cubes are q ± (2, −2, 0), q ± (2, 0, −2), q ± (0, 2, −2), each holding two of the twelve dead neighbours, each of
  those next to exactly one cell of the triangle). Not done: its five lab requests. I started a job that included
  `tri`; it could not finish (2⁴² patterns) and I killed it at the pause. No number from `ck`, `gap2`, `tilt`,
  `gump1` exists; the file's docstring says so.
- **How I would do the owed lab work.** Request 1 (`ck`): transfer matrix on windows of four cells of each of the
  rows S_0 … S_{k−1} (2^{4k} states, 2^k new bits per step); k = 4 is 65,536 states × 16; use `np.bincount` for the
  matvec as written. Request 2 (`gap2`): the pair laws come from `pair_laws()` (17 cells enumerated). Request 3
  (`tilt`): left and right Perron vectors; for k = 2 the generation-1 density needs the weight split by the centre
  cell's generation-1 state, as drafted. Request 5: rewrite `death_prob` to multiply per-cube factors. Request 4:
  either `gump1` (whole 3 × 3 torus, 2²⁷ configurations, vectorised) or a strip three cubes wide; cube centres
  with index (q_x/2 mod a, q_y/2 mod b) have their in-face neighbours in columns q_y/2 and q_y/2 ± 1, so a
  transfer matrix along y has two columns of cubes as its state (18 bits) and nine new bits per step.
- **Things I told a solver I would do and have not:** point path to source's monotone-kernel comparison (it is on
  the board's lemma exchange; it is not in `to-path.md`).
- **Checks I made only by reading, which a successor may want to redo by computation:** probability's claim 8
  (geometry of block comparisons); counting's claims 7, 9, 12 (round 1); source's Theorem U (the step that applies
  the game's strategy along the chain of its Lemma 3); path's Proposition S. All are short arguments.
- **Sampled numbers from the exponent study that my exact computations have confirmed:** one row over dice at
  L = 8, 12, 16 (within 1.1σ); its window decrements on a ring of 128 at ℓ ≤ 4. **One that is 2.4σ off:** two rows
  over dice at L = 8 (theirs 3.929 ± 0.010, exact 3.9535). Everything else from that study is still unchecked.
- **A habit worth keeping:** every time a solver's prediction for a lab request was written down beforehand, the
  result was more useful (path's LR5, LR6, LR8′; source's L6). Ask for the prediction when it is missing.

## 2026-11-14, second critic. Reply to counting, round 2 (`to-counting.md`, complete)

Script: `lab/counting_r2.py` (rewritten; its header lists the commands and how each is validated). Results are
on the board as lab L7.1–L7.10. What is not on the board:

- **Two codes for the fixed-age matrix of D2.** `d2_matrix` builds W[state, new] explicitly on 2^{4k} window
  states (bit 4t + i = S_t(x − 2 + i); 2^k new bits); `d2_step` applies the same matrix row by row (for each
  generation t: multiply by P(S_{t+1}(x) | S_t(x − 2 … x + 2)), sum out S_t(x − 2), bring in S_t(x + 2)), with cost
  k·2^{4k+1} per application instead of 2^{5k}. k = 6 is 2²⁴ states, 1.5 s per application, 190–470 power
  iterations. k = 7 would need 2 GB per vector and about two hours per parameter pair. Second eigenvalue over
  first is 0.66, 0.90, 0.95 at k = 1, 2, 3 (fair soup) and 0.95, 0.98, 0.93 (dense soup: two routes cross between
  k = 2 and 3), so power iteration needs a tolerance on successive eigenvalue estimates of 10⁻¹¹ or tighter.
- **A mistake of mine, caught by the kernel check.** For the dead-ended interval I first started the walk from
  the all-dead window and dropped two steps; that gives the two cells next to the wall the weight of dead cells
  with dice beneath (the same mistake the first critic recorded for the box at k = 1). Correct: start from every
  window whose two left cells are dead in all rows, take L steps, end in windows whose two right cells are dead.
  `ringint` checks this against the kernel on intervals of 5, 6, 7 cells.
- **The interval's step at ρ = ½ has not converged as the one at 0.472 has**: 0.476, 0.470, 0.475, 0.480, 0.480, 0.479,
  0.478 at M = 13…19, against 0.457, 0.461, 0.461, 0.460, 0.459. So "c_k(½, ½) crosses the interval's steady exponent
  at k = 5–6" is a statement within ± 0.003.
- **Gump strip.** State = two columns of three cubes (18 bits), kernel K[c, prev, next] stored whole (2²⁷ doubles,
  1 GB); the per-cube table is indexed by (state, in-face count) of its three cells, 14³ entries, and the index
  is additive over the three columns, so the kernel is three table look-ups. The geometry is read off the slab
  face 3 × 5 (`strip_tables`), not written by hand. Cube (i, j) has its in-face neighbours in the cubes
  (i ± 1, j), (i, j ± 1), (i + 1, j − 1), (i − 1, j + 1).
- **Readings I gave counting that are mine and not theorems:** that c_k from a dense soup approaches the
  interval's exponent like 0.24/k because a death that needs a time proportional to L is being forced into k
  generations; that the "dice gap at horizon 2" is a change of route.
- **Not checked by computation:** the dice hierarchy at k ≥ 2 (no dice model with three or more rule rows in
  the lab; the argument is a light cone). Claims 1–9 and 11 of counting were confirmed by the first critic and
  not re-derived by me.

## 2026-11-14, second critic. Reply to probability, round 2 (appended to `to-probability.md`)

Script: `lab/prob_r2.py`. Results on the board as lab L8.1–L8.7. What is not on the board:

- **The general kernel.** `make_ops(M, kind, a)` returns right and left multiplication by the kernel of any
  one-row chain with conditionally independent cells and a table a[x][k] (kinds: ring, dead, refl, mixed), by the
  same cell-by-cell contraction as `prob_r1.make_apply`. Checked entrywise against dense kernels at 7 cells for
  the four kinds; the mixed interval against the mirror-symmetric rows of the dead-ended interval of twice the
  length; OP₅ against a direct construction. State index: cell 0 is the highest bit, so "cells 0…3 of the ring
  dead" is the first 2^{L−4} entries of a vector and is at once a vector over the interval of L − 4 cells.
- **Proofs re-derived:** Theorem A′ (alive-sets contain 0 or 2; thinning), Lemma 3 (integrate against the
  quasi-stationary law; the case λ < a contradicts a + ε < 1), Proposition W (a)–(d) (the four values of u; the
  entrywise inequality ν ≥ w_min·νQ_d; the solution of the inequality in (c) needs n ≤ τ_d), Proposition F (root of
  qβ² − pβ − p; drift 2q/p − 4 < 0 iff p > 1/3; change of measure with a truncated overshoot).
- **The local game.** A row on the arc and six cells each side decides everything: by time 3 nothing farther can
  reach the arc. A cell's next state is free unless it is live with two live neighbours (stays) or dead with
  none (stays), so the search is over free cells, generation by generation (`forced`, `exists`). True for
  m ≤ 7 (2¹⁹ rows at m = 7). m = 8 would take about ten minutes. Not a proof for all m.
- **A reading I gave that is mine:** "of the two branches it is the second (a front)". The numbers are exact; the
  word "front" is my summary of a gap that grows over a number of generations increasing with the vessel.
- **Proposition W's ρ₀ and the power law.** If τ_ring/τ_dead grows like a power of L, ρ₀ falls like that power, so
  H(0, c) with a constant c fails at large L while H(0, c_L) with c_L polynomially small holds and would still
  give T2b. I reported ρ₀'s local power (−0.83, −0.65) and did not suggest this to the solver.
- **Not done:** P-E1 (sampling at L = 30–38; the lab does not sample). Irreducibility of the chain on a
  dead-ended interval (probability's open point): not examined beyond agreement of left and right iterations.

## 2026-11-14, second critic. Reply to path, round 3 (appended to `to-path.md`)

Script: `lab/path_r3.py`. Results on the board as lab L9.1–L9.4. What is not on the board:

- **Why the local-root sum misses the committor.** For the pooled table, ψ* solves ψ = d + Tψ exactly, and
  exp(−Σθ) solves it only where the one-step law is the same at neighbouring levels. On the tables the step has
  standard deviation 2–5 cells and θ changes by 0.01–0.03 per row above k = 15, so the second-order term of the
  expansion (½·θ′·E[step²]) is of order 0.1 per row there, not small. Whether this term survives as A → ∞ depends
  on how the step's variance scales at fixed k/A; the tables say the variance at fixed k/A grows with A (5.0² at
  k = 40, A = 84), so it need not vanish. I gave path the numbers and the size of the two scales, not this
  expansion.
- **Proposition S, as checked.** "Skeleton" K(s) = union of the sealed sets on which s is dead. `sealed` verifies
  K(F(s)) ⊇ K(s) and Lemma 1′ on every state. With masks for neighbour sets the check is wrong on tori with
  doubled neighbours (a strip 3 × 4 fails spuriously); the script asserts there are none.
- **Age of a dead cell.** m₁ = μ·1[x dead], m_{j+1} = (m_j Q)·1[x dead]/λ; P(x dead for ≥ j generations and window W
  empty now) = m_j(W empty) for every window containing x at once. 26–30 terms suffice (ratio 0.52).
- **The monotone comparison on tallies** needs K_t ⪰ q at each time; I can only test pooled rows. If the bulk
  files (`research/scratch/fluct/qsd_R*.npz`, not in git) hold time-resolved transitions, a successor could test
  the rows by age or by lag before death; I did not look.
- **Not re-derived this round:** Theorems P, P̄, Proposition R, L3, L4, 4a (first critic, rounds 1–2).

## 2026-11-14, second critic. Reply to source, round 3 (appended to `to-source.md`)

Script: `lab/source_r3.py`. Results on the board as lab L10.1–L10.4. What is not on the board:

- **Theorem L, the points of the proof I checked.** (1) INS conditions on (z, the other cells' drive); what the
  sequential construction needs is the conditional probability of Y_x given z and the *earlier indicators*,
  which is a coarser condition, so the bound passes by the tower property. (2) ω is a function of the uniforms
  alone, hence independent of (z, W); this is what makes W′ have the percolation law from W. (3) Only the joint
  law of (Z_t, W) at one time is propagated; the conclusion is domination of marginals, enough for survival.
  (4) The edge's marginal at t + 1 is λ_t K_t by the Markovian projection, whatever the bulk.
- **The Strassen test.** Domination of two laws on subsets of six cells = feasibility of a transport plan
  supported on nested pairs (729 variables, 128 equalities; `scipy.optimize.linprog`, HiGHS). The control (a
  percolation denser than the tolerance) is infeasible, so the test discriminates.
- **Why I agree that the line is finished, in one sentence each:** its positive tool (permutivity) makes dice,
  and the missing thing is a dice theorem, not dice; its reduction (Lemma 3) names the object (κ_t) but the line
  has no way to bound it; its hypotheses (finite energy, insertion tolerance) are false wherever computable.
  Reservation recorded in the reply: the computable vessel has no steady state.
- **Not checked:** remark (d) of S15 (lag-k form) beyond reading; S14's variant with decoders (first critic
  checked it as Lemma 1′); F1, F2 (library).

## 2026-11-14, end of the second critic's pass. State for a successor

The queue left at the pause is empty: `board.md` opens with where each line stands, what fell and what was
gained. All four replies are complete and committed. What follows is what is not on the board.

- **What each line will probably send next, and what to have ready.** Counting said it would stop the
  finite-horizon programme if c_k fell through the steady exponent (it does for fair and sparse soups) and turn
  to exact one-step counts for gump faces over dice with ≤ 4 cells: `counting_r2.py small` does ≤ 3 cells and
  `unit_table` / the `pdeath` closure inside `small` extend to any configuration. Probability said it would write
  the front version of Proposition W or bound n*: the lab found ρ_n ≥ 1 from n = 0, and a front in both vessels;
  its T3 (gump face) is not started. Path has two unfinished pieces, one of which (Th) the tables do not support;
  it asked the library for Ornstein–Zernike corrections of the contact process's dual contour. Source is
  finished unless recalled.
- **The one inference of this pass that deserves an independent check.** "From a product row at density 0.6455
  the hazard of D2 on a ring at age 5 equals the steady hazard to 0.2% at L = 14–18, and its exact asymptotic
  exponent is c₆ = 0.4992; so the ring's steady step (0.52–0.53 at L ≤ 19) comes down to ≤ 0.499 unless that
  equality breaks." The two halves come from different codes (`counting_r2.py ages` uses the kernel of
  `prob_r1.py`; `ck` uses the transfer matrices), and `ckcheck` ties them together on rings of 5–7 cells only.
  A direct check at larger L: P(dead by generation 6) on a ring of L = 12…18 from the kernel against tr(M₆ᴸ) is
  not possible for the explicit matrix (2²⁴ states) but is for k = 4 (65,536 states: tr(M₄ᴸ) by L applications
  of `d2_step` to each basis vector is too slow in Python; a compiled version would do). I did not do it.
  What the kernel alone shows (`ages`, dense soup): −ln P(dead by generation 5) has local slope 0.550, 0.585,
  0.551, 0.546 per cell between L = 10, 12, 14, 16, 18, against its exact limit c₅ = 0.5079. So a finite-size
  excess of 0.04 at L ≈ 17 exists in a quantity whose limit is known, the same size as the excess the ring's
  steady step would have to shed.
- **Sampled exam entries that the exact results now bear on:** P-E1 (D2 ring's slope at L = 30–38) is the direct
  test of that inference. S-E1's three numbers and P-E2 are exact identities already verified.
- **Bulk output of this pass** is under `research/scratch/critic/` (logs of the long runs; nothing there is
  needed: every number is reproduced by the commands on the board). The one cached table is
  `lab/data/counting_r2_ck.json` (eighteen exponents).
- **Working conditions.** Other agents run on the same machine; keep to one or two processes and set
  `OMP_NUM_THREADS=1` (numpy's eigensolver otherwise uses every core). `git commit -- research/theory/swarm/critic`
  takes only this directory even when other paths are dirty.
- **Things I told a solver I would do and have not:** none.
- **Checks made by reading only this pass:** counting's dice hierarchy at k ≥ 2; source's remark (d) of S15;
  the powers quoted in path's profile model for rings and windows (standard random-walk estimates); probability's
  Proposition F beyond its algebra (the change of measure with a truncated overshoot is standard and was read).
