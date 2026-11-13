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
