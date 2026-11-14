# Audit of the counting line (`research/theory/swarm/counting/claims.md`)

_Second reader, 2026-11-14. Audited: `counting/claims.md` and `counting/journal.md` at commit `7c018f9`.
Verdicts were formed from the statements and the journal's proofs and committed (`e769776`: from reading alone;
`7f7dd9c`: after recomputation) before anything of the critic's was opened (`critic/to-counting.md`,
`critic/board.md`, the lab); the section "Where I differ from the critic" was written afterwards and changed no
verdict. All code is the audit's own (`c0_lib.py` … `c5_measure.py` here, and `p0_lib.py` from the audit of the
path line), written from `docs/AUTOMATON.md` and, for the 2D rule and face12e, from their one-line definitions in
`PROBLEM.md`. The only import from the repository is `reference/oracle.py`; no data file is read. One script,
`c6_compare_critic.py`, written after the verdicts, calls the critic's lab code to compare numbers._

## Summary

Verdicts: *correct*; *correct after filling a gap*; *true but narrower than worded*; *wrong*; *not a proof*.
"Read" = statement and proof followed line by line, every number in it re-derived by hand. "Recomputed" = tested
with the scripts below, exhaustively where the size allows. A recomputation was never used in place of the reading.

| # | claim (journal entry) | verdict | how checked |
|---|---|---|---|
| 1 | union bound for μ-preserving maps; gap bound for bijections (2) | **correct** | read; recomputed in exact fractions on 3,000 random (g, μ, H) and 5,000 permutations; controls fail as they should (`c5`) |
| 2 | second-order lift: bijection, confined, "empty now" has frequency 2^{−A}, never dies (3) | **correct** | read; every pair-state of five vessels (three gump hulls of 6, 8, 10 cells; 2D strip 2 × 4; 2D box 3 × 3) (`c5`) |
| 3 | λ(T ≤ k) = \|f^{−k}H\|/\|X\| (1, 3) | **correct** | read (an identity once f(H) ⊆ H); f(H) ⊆ H on every state of the same vessels and on 200,000 states of the hull R = 3 (`c5`) |
| 4 | Theorem 3: trace formula, exponential bound, c_k as the rate of empty windows, 0 < c_{k+1} ≤ c_k < ln 2 (4) | **correct** | read; the window matrix M_1 (4,096 states) built from the stepper: tr(M_1^L) = brute count on rings L = 1…8, 1ᵀM_1^ℓ1 = brute count of open words ℓ = 1, 2, 3, the bound m_1e^{−c_1L}; table w(s, k), 2507, both hand bounds (0.2736 ≤ c_1 ≤ 0.5618); control W = 2 fails (`c1`) |
| 5 | c_1 = 0.551535, c_2 = 0.467693; 0.489963 and 0.4671 at density 0.472 (9); c_3 measured | first three **follow from claim 4 and are right**; the fourth is **0.4668** (0.466846), not 0.4671, §1. c_3: measured, out of scope | recomputed: ρ_1 = 4.608520, ρ_2 = 20.046271 from an independent 2^16-state matrix whose traces equal brute counts on rings 5 × 3, 5 × 4, 5 × 5 (8,663; 224,471; 7,043,564); the weighted matrix at 0.472 checked against a weighted brute sum on the ring 5 × 4 (`c1`) |
| 6 | fixed k: e^{−A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A} on a gump slab face; face12e wall with 3A ln 2 (4, 14) | **correct**, both halves | read (light-cone induction; an outside face sees ≤ 3 of a gump cube and ≤ 2 of a face12e cube); the guard cube against 1,800 (gump) and 1,500 (face12e) random outsides for k = 1, 2, 3 and 1, 2; control with a smaller box fails (`c2`, `c3`) |
| 7 | box edge: [M_k^{L+4k}]_{00}; c⁰_k ≥ c_k; equality for k = 1, 2 (5a, 9) | **correct** | read; [M_1^{L+4}]_{00} = brute count on boxes 3 × L, L = 1…7 (7, 35, 148, 656, 2977, 13850, 64434); k = 2: path sums of the 2^16-state matrix = brute counts on boxes 5 × L, L = 1…5; class of the all-dead state: strongly connected for k = 1; 54,591 of 65,536 for k = 2, every other class one state without a loop, ρ⁰ = ρ to 10⁻⁶ (`c1`) |
| 8 | mirror ≥ c_k/2; C4 or a diagonal mirror exactly c⁰_k; no symmetry inside a light cone (5b, c, e) | **correct** | read; mirror rings L = 8…22 (brute at L = 8) against the bound; C4 box 7 × 7: 502 of 8,192, 4,096 bands; C4 and diagonal boxes 7, 8: band counts between [M^{L−2}]_{00} and [M^{L+4}]_{00}; (e) on the C4 box 11 × 11 (`c1`) |
| 9 | "mirror = exactly half" | sketched: out of scope | |
| 10 | gump: the cells beneath belong to the top cubes; 40 of 64; emptiable cube by cube; λ(T ≤ 1) = 2^{−A}Σ_SΠ_qW_q (6, 8) | **correct** (with entry 8's "six") | read; offsets; B enumerated; K(s, k) from the rule; the product formula against every state of the hull R = 3 face and the cells beneath (2^24) and of a slab 2 × 1 (2^18); on a slab 2 × 2 (18 face configurations) and on the vertex-centred hull R = 4 (14 face configurations, six rim cells alone in their cubes) against all 2^24 states beneath (`c2`) |
| 11 | beneath empty: dies iff (live: k ≤ 2 or 6; dead: k ≤ 3 or 6); "a full face always dies" (6, 8) | first part **correct**; second **true but narrower than worded**: a rim-free face only, §2 | read; all 4,096 configurations of the slab 2 × 2 face over empty and over full layers; the full face of the hull R = 3 over empty layers keeps 6 of its 9 cells (`c2`) |
| 12 | gaps persist (10) | **correct** | read; every state of the ring 3 × 8 for ℓ = 1…4, j = 1; 200,000 random states for j = 2, 3; control with a narrower margin fails (`c1`) |
| 13 | c_k(p) ≤ −ln(1 − p) (10) | **correct** | read; c_1(p), c_2(p) at nine densities (`c1`) |
| 14 | dice hierarchy: D2(L, ½; w) has the true rule's λ(T ≤ k) for w ≥ 2k − 1 (10) | **correct** | read; the dice chain propagated exactly on rings L = 4, 5: equal for (w, k) = (1, 1), (2, 1), (3, 2), (4, 2); controls (1, 2), (2, 2) differ (`c1`) |
| 15 | Lemma 7: 85/128, 161/256; 76/128, 119/256 (11) | **correct** | read; every state of a 5 × 5 patch (2^25) (`c5`) |
| 16 | gump lone cell (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴; lone triangle (1 − ρ)⁶(1 − 2ρ³ + ρ⁵)⁶ (12) | **correct** | read; slab 3 × 3: 108,045 of 2^18; triangle exactly by groups found from the adjacency, 25⁶/2^36, and 2 × 10⁷ samples of the whole slab; four densities (`c2`) |
| 17 | μ(Y₁) ≤ (\|Y₁\| Σ μ(u)²)^{1/2}; its hypothesis false (7, 8) | **correct** (the inequality; the arithmetic of the atom argument). "False in every vessel enumerated" is a measurement, reproduced | read; strips 4 × 5 (j = 1…8), 4 × 6, 5 × 5 (j = 1, 2): excess 0.92–1.03 at j = 2, 1.73 at j = 8, living rows 0.64–0.73 (`c5`) |
| 18 | no finite pattern of the half-plane holds its cells against the outside (7) | **correct** | read; the proof's cell and recipe on all 78,728 (set, pattern, depth) cases in a 3 × 3 patch; control (a one-row vessel) fails (`c5`) |
| 19 | Lemma 8 and its corollary (13) | **correct after filling a gap**, §3 | read; 156,000 tests on random substochastic matrices, reducible ones included; control without the doom term fails; the one-row dice chain on rings L = 5…10 (`c5`) |
| 20 | Lemma 2′; "no relative with an invariant measure charging the living states has a face that dies" (16) | lemma **correct**; the second sentence **true but narrower than worded**, §4 | read; 3,000 random (g, μ, absorbing H) in exact fractions; gump on one cube as the example for the wording (`c5`) |
| 21 | face12e, Proposition F (14, 17) | **correct** | read; neighbour lists of every band cell of a wall 4 × 5; each item on 20,000–40,000 random states; Θ^j(full) = {d ≥ j} with the true rule on box walls n = 1…7; Θ^n ≡ ∅ on every sheet for n ≤ 4 (`c3`) |
| 22 | face12e, Proposition G; Π₁: 32^n(8^n + 2·6^n + 5^n), rigid rows (14) | **correct** | read; the table for every (state, a); formula (a) against every state of a wall 2 × 2 (2^24), band by band; Π₁ at n = 3 (35,028,992) and n = 4 (7,668,236,288), and against the true rule on 300,000 random patterns each (`c3`) |
| 23 | face12e lone cell: ladder polynomial, 3793/8192 (14) | **correct** | read; all 2^13 patterns on a wall 3 × 3: 3,793; six pairs of densities (`c3`) |
| 24 | O_h faces: equal area, orbits, adjacencies; triangle orientation and rim differ (15) | **correct** | read; every count listed for N = 1…9 and R = 35, 36 (`c4`) |
| C2 | c_∞(½) > 0 | guessed: out of scope | |

Count: of the 22 claims tagged proved, **19 correct**, **1 correct after filling a gap** (19), **2 with one sentence
narrower than worded** (11, 20), and the computed claim 5 has **one constant wrong in the fourth digit**.
Nothing tagged proved is wrong; no proof is missing.

### Scripts

All in this directory; each runs on one core; logs in `out/`.

| command | time | what |
|---|---|---|
| `python3 p0_lib.py` | 1 s | (path audit) the gump stepper against `reference/oracle.py`, bit for bit |
| `python3 c0_lib.py` | 2 s | the 2D stepper against a naive per-cell loop; the table w(s, k) |
| `python3 c1_transfer.py` | 4 min | claims 4, 5, 7, 8, 12, 13, 14 |
| `python3 c2_gump_face.py` | 8 min | claims 6 (gump), 10, 11, 16 |
| `python3 c3_face12e.py` | 2 min | claims 6 (face12e), 21, 22, 23 |
| `python3 c4_oh_faces.py` | 2 s | claim 24 |
| `python3 c5_measure.py` | 3 min | claims 1, 2, 3, 15, 17, 18, 19, 20 |
| `OMP_NUM_THREADS=1 python3 c6_compare_critic.py` | 1 min | after the verdicts: the critic's c_2(0.472) iterated to convergence; exact ring slopes at L = 20–32; the critic's counts recomputed |

## 1. Claim 5: the constants

Claim 4 gives c_k = (2k + 1) ln 2 − ln ρ(M_k). M_2 has 2^40 states; the reduction used here is: state = row 0 over
8 columns and rows 1, 2 over 4 columns (2^16 states), the cells (x, 3), (x, 4) are read by the judged cell only and
are summed out as a weight 0…4. Traces of all powers agree with those of M_2 (both count the L-periodic
configurations), so the spectral radii agree. The audit's matrix (`c0_lib.T2`) was written from the rule and
checked three ways: tr(T^L) against brute counts on rings 5 × 3, 5 × 4, 5 × 5; path sums against brute counts on
boxes 5 × 1 … 5 × 5; the weighted version against a weighted brute sum.

| constant | journal | audit |
|---|---|---|
| ρ_1, c_1 (density ½) | 4.608520, 0.551535 | 4.608520, 0.551535 |
| ρ_2, c_2 (density ½) | 20.046271, 0.467693 | 20.046271, 0.467693 |
| c_1 (density 0.472) | 0.489963 | 0.489963 |
| c_2 (density 0.472) | 0.4671 | **0.466846** |

The last one: at density 0.472 the two leading eigenvalues of the weighted matrix are 0.626977 and 0.620526
(power iteration and `scipy.sparse.linalg.eigs` agree; ring 5 × 4: weighted brute sum 0.2328125151 = tr(T⁴)). The
ratio 0.99 makes a power iteration slow, and that is where 0.4671 came from (the lab stops at 400 iterations; see
"Where I differ from the critic", 1). The value at 0.472 is 0.4668. No claim rests on the difference, and "one
more generation lowers the cost by 0.023 at density 0.472" (entry 9) stands (0.0231).

Corrected wording for `claims.md` 5: "… 0.489963, **0.4668** at density 0.472."

**A remark of entry 9 that the constants support only locally.** "The soup density matters at horizon 1 and no
longer at horizon 2" (entry 9 (i); the critic's reply to round 1 says the same; entry 10 builds "c_2 does not
depend on the density near ½" on it) holds on the stretch 0.467 ≤ p ≤ 0.5, in which both densities compared happen
to lie, and not outside it. The leading branch of the horizon-2 spectrum changes near p = 0.467 (`c6`, part B):
above it c_2(p) is flat (0.4671, 0.4668, 0.4662, 0.4664, 0.4677 at p = 0.47, 0.472, 0.48, 0.49, 0.5); below it c_2
rises steeply with the density (0.3344, 0.4110, 0.4518, 0.4623 at p = 0.40, 0.44, 0.46, 0.465); above 0.5 it rises
again (0.4737, 0.4844 at 0.52, 0.54) and is lower again in dense soups (0.4013 at 0.6455, 0.1167 at 0.8; `c1`).
The density 0.472 sits 0.005 above the change of branch, which is why its second eigenvalue is so close. For
comparison, the soups of the measured 2D law have density 0.4 (`research/toy2d/README.md`), where c_2 = 0.334.
No claim of the list rests on the remark (the guess C1′ that used it is withdrawn).

c_3 = 0.36 ± 0.01 is the examiner's sample and out of scope. One number that bears on how it is read (entry 13: "the
same samples give 0.542 and 0.479 at k = 1, 2"): the exact slopes of −ln D_k(L) between L = 20 and 32 are 0.55155
(k = 1, all 16 eigenvalues) and 0.4777 (k = 2, leading 40 eigenvalues). So the sample is right to 0.001 at k = 2 and
0.0095 low at k = 1 (where the events are of probability 10⁻⁵ … 10⁻⁸), and "a ring's slope at these lengths is
about 0.01 above its limit at k = 2" is confirmed exactly.

## 2. Claim 11: "a full face always dies"

The journal (entry 6, corollary) says "a full face (k = 6 everywhere) dies in one generation whatever lies beneath",
and that is correct: a cell with six live in-face neighbours has n ≥ 6. The list drops the parenthesis. On a hull
face the rim cells have fewer than six in-face neighbours, and the statement fails: the full face of the hull
R = 3 (in-face degrees 4⁶2³) over empty layers keeps its six cells of degree 4 (n = 4), `c2`.

Corrected wording for `claims.md` 11: "… **a full rim-free face (every cell with six in-face neighbours: a slab
face) always dies.**"

The first part (the iff, as corrected in entry 8) holds on any face, with k the number of live in-face neighbours.

## 3. Claim 19: Lemma 8 and its corollary

The lemma and its proof are correct as written (Q ≥ 0 and φ ≤ 1 give Q^k1 ≥ λ^kφ; a non-negative eigenvector for
the spectral radius exists for every non-negative matrix; for a reducible Q it need not be unique and the
inequality holds for each).

The gap is in the corollary. The lemma takes "a law π on the living states"; the corollary applies it to product
laws on the row, which charge the dead state (the empty row), where φ is not defined. Fill: put φ = 0 on the dead
state. Then P_x(T > k) ≥ λ^kφ(x) holds there too (0 ≥ 0), the lemma holds for every law π on all states, and
π(1 − φ) includes π(dead). Consequence worth stating: for the Bernoulli(p) row, θ⁻(π) ≤ −ln(1 − p) whatever the
chain, so the corollary can never give more than c_∞(π) ≥ min(γ⁻, −ln(1 − p)); this is claim 13 again.

Two readings to fix in the wording:
- "with product laws the left side is the c_k(π) of entries 4 and 10": those are defined for the true rule. In the
  corollary it must be the fixed-age exponent of the dice chain itself (which, by claim 14, equals the true rule's
  for k ≤ (w + 1)/2 only).
- h = 1 − λ is "the steady hazard" only when Q is primitive on the states that π can reach. For the one-row chain
  D2(L, ½) on a ring it is (from any living row the full row is reachable, and from the full row every row), `c5`
  uses that chain as an illustration: at L = 10, h = 0.0045 and π(1 − φ) = 0.016 for the fair product row.

Corrected wording for `claims.md` 19: "Lemma 8, any finite absorbing chain, any initial law π (φ = 0 on the dead
state): P_π(T ≤ k) ≤ (1 − λ^k) π(φ) + π(1 − φ) ≤ k h + π(1 − φ), φ a non-negative eigenvector for the spectral
radius λ with max 1. Hence for a family of dice chains with fixed-age exponents c_k(π) of their own,
c_∞(π) ≥ min(γ⁻, θ⁻(π)) …"

## 4. Claim 20: Lemma 2′

The lemma (μ(g^{−1}H ∖ H) = 0, hence μ-almost no point outside H ever enters H) and its two-line proof are correct.

The second sentence of the claim, "no relative with an invariant measure charging the living states has a face that
dies", is true only if "charging" means *positive on every living state* (finite X), or if the conclusion is read as
"μ-almost every living state never dies". With the weaker reading (μ gives positive mass to the set of living
states) it is false, and gump itself is the counterexample: every finite map has invariant measures (uniform on a
cycle), and gump has cycles among living states. On the one-cube vessel the full cube is a fixed point with a live
face, the point mass on it is invariant, and 49 of the other 55 living states die (`c5`).

Corrected wording for `claims.md` 20: "… If g preserves μ and g(H) ⊆ H then μ-almost no point outside H enters H.
**So a relative with an invariant measure that is positive on every living state has no face that dies; in general
only the states the measure does not see can die.**"

(Entry 16's use of it is unaffected: the lift's invariant measure is uniform. Its last sentence, as corrected in
entry 17.4, says that an automaton whose living states die with positive product measure does not preserve the
product measure: correct, and it concerns another line's object, which was not examined.)

## 5. Smaller points (no verdict changes)

- **Claim 1 (a).** On a finite set a map that preserves μ is a bijection of the support of μ, so "no bijectivity
  needed" is true and, for the vessels of this project, empty; the statement is the same as for a bijection.
- **Claim 4.** "For every L ≥ 1" needs the ring Z_L read as the quotient of the line, neighbours with multiplicity
  (for L ≤ 4 the cells x ± 1, x ± 2 coincide). With that reading the trace formula holds at L = 1…4 too (7, 25,
  100, 449; `c1`). The dependence cone is {⌈|x′ − x|/2⌉ + ⌈r/2⌉ ≤ k}, a subset of the journal's
  {|x′ − x| + r ≤ 2k}; only the bounding box (4k + 1 columns, 2k + 1 rows) is used.
- **Claim 6.** The box of half-width 2k + 2 is sufficient, not tight: with half-width 2k the cube also survived every
  trial; with 2k − 2 it fails (k = 1, 2).
- **Claim 7.** The class of the all-dead window in M_1 itself (not the 16-state reduction) has 821 of 4,096 states;
  the other 3,275 classes are single states; ρ⁰ = ρ. For k = 2 the box count is not [T^{L+8}]_{00} of the reduced
  matrix (the reduced matrix sums the cells (x, 3), (x, 4) freely also at the padding columns); it is a path sum with
  boundary vectors, squeezed between [T^L]_{00} and [T^{L+8}]_{00}, so the exponent is that of the class of 0.
- **Claim 10.** The product formula needs the six cells beneath a top cube distinct and present (a slab at least
  three layers deep; in a hull, cells outside count 0, as the journal says). On small periodic faces in-face
  neighbours coincide and k must be counted with multiplicity; then the formula still holds (slab 2 × 1, 2 × 2).
- **Entry 13, "two one-line facts behind the crowded route [proved]"** (not in the list): read, correct. A live
  edge cell with four live in-row neighbours dies iff b ≥ 1, so a full ring (L ≥ 5) over cells of density ρ dies
  with probability (1 − (1 − ρ)²)^L (the table w(live, 4) = 3/4 at ½ is this); the gump half is claim 11.
- **Claim 21, F.4.** "Gone in n steps" is exact for odd n; for even n the sheet is gone in n − 1 steps (max d = n − 2).
- **Claim 23.** The lab request asks for a wall "at least 3 × 3"; 2 × 3 already has the six cubes distinct (also
  3,793). On 2 × 2 the count differs (376 of 2^10).
- **A remark outside the list** (entries 4 and 7, closing report point 2: "counting gives lifetimes ≥ c√L and no
  more"). The bound m_k e^{−c_kL} can be useful only while k ≲ √L: that is right. As a positive statement,
  "lifetimes ≥ c√L" needs inf_k c_k > 0, which is the guess C2. What is proved is c_k ≥ 2^{−(4k+1)(2k+1)}/(4k + 1)
  (the guard), which gives T > k with high probability only for k ≲ (log₂ L / 8)^{1/2}.

## Corrected wordings, gathered (ready to paste into `counting/claims.md`)

- **5.** "… **c_1 = 0.551535, c_2 = 0.467693** (density ½); 0.489963, **0.4668** at density 0.472 …" (also journal
  entry 9; `critic/to-counting.md` round 1; board L3.2 and lemma exchange "Finite-horizon law").
- **11.** "With the layers beneath empty a gump face dies iff every live cell has k ≤ 2 or k = 6 and every dead cell
  k ≤ 3 or k = 6; **a full rim-free face (every cell with six in-face neighbours) always dies**."
- **19.** "Lemma 8, any finite absorbing chain, **any initial law π (φ := 0 on the dead state)**: P_π(T ≤ k) ≤
  (1 − λ^k) π(φ) + π(1 − φ) ≤ k h + π(1 − φ), φ **a non-negative eigenvector for the spectral radius λ** with max 1.
  Hence for dice chains, **with c_k(π) the chain's own fixed-age exponents**, c_∞(π) ≥ min(γ⁻, θ⁻(π)) …"
- **20.** "Lemma 2′: if g preserves μ and g(H) ⊆ H then μ-almost no point outside H enters H. **A relative with an
  invariant measure that is positive on every living state has no face that dies.**"

## Where I differ from the critic

The critic (`critic/to-counting.md`, replies to rounds 1–3; board, closing table) confirms every claim tagged
proved. So do I, with the four reservations of the summary. Where the two readings overlap in numbers they agree:
2,507 … 209,825; 2,977, 13,850, 64,434; 224,471 and 7,043,564; ρ_1, ρ_2; 54,591; 502 of 8,192; 40 of 64; 185 of 2⁹,
20,941 of 2¹⁸, 2,662 of 4,096 and 112,744 of 262,144 (gump slabs); 108,045·2¹² = 45·56⁴ of 2³⁰ and 25⁶·2⁶ = 50⁶ of
2⁴²; 85/128 …; the collision excesses; 3,793; 35,028,992 and 7,668,236,288; the O_h counts; h, min φ, μ(1 − φ)/h,
π(1 − φ)/h and e(π)/h of the dice ring at L = 10, 12 (`c6`, part D).

**Differences.**

1. **c_2 at density 0.472 is 0.4668, not 0.4671** (claim 5; journal entry 9; the critic's reply to round 1; board
   L3.2 and "Finite-horizon law" in the lemma exchange). The number is the critic's, and it is an unconverged power
   iteration: `counting_r1.spectral` stops at 400 iterations, and at this density the second eigenvalue is 0.99 of
   the first. The lab's own output shows it (`counting_r1.py c2` prints c_2 = 0.467096 and c⁰_2 = 0.467079 for one
   and the same eigenvalue). The critic's matrix with 3,000 iterations gives 0.466846, the audit's value
   (`c6`, part A). At density ½ the gap is wide and 400 iterations suffice (0.467693 is right).
2. **Claim 11, "a full face always dies"**: confirmed by the critic without the restriction to rim-free faces (§2).
   The board knows the fact (its remark that a full face of a large hull keeps at most its rim); the list's sentence
   was not corrected.
3. **Claim 20, second sentence**: confirmed by the critic as it stands. The board's own form ("trapdoors" (iii):
   μ(H_k) = 0 for every invariant μ) is the correct one; the list's "no relative with an invariant measure charging
   the living states has a face that dies" is not, unless "charging" means positive on every living state (§4).
4. **Claim 19.** The critic checks the lemma with π "restricted to living rows"; the corollary as written uses
   product laws, which charge the dead row (§3: put φ = 0 there). The critic's caution E21 (with max φ = 1 the term
   π(1 − φ) is a few h even for the steady state itself, so "doomed start" is a figure of speech) is right and I
   had not seen it before reading the reply; `c6` reproduces its numbers at L = 10, 12.
5. **Things the critic left as "read" or "unchecked" that are checked here.**
   - Claim 6 for face12e, the light-cone step: read line by line (same induction as for gump; the speed is one cube
     per generation in both lattices) and tested against random outsides (`c3`).
   - Claim 14 for k ≥ 2 ("by the argument only: the lab has no dice model with w ≥ 3"): the dice chain with w = 3
     and w = 4 propagated exactly on rings of 4 and 5; equal to the true rule at k = 2; w = 1, 2 differ (`c1`).
   - Claim 24 beyond N = 4: listed to N = 9 and at R = 35, 36 (`c4`).
   - Claim 8 (b): the mirror-ring count against the bound for L = 8…22; (c) for the diagonal mirror (`c1`).
   - Claim 4 at L = 1…4 (the quotient reading) and the open-word form 1ᵀM^ℓ1 by brute force.
   - Claim 10 on a hull (cells outside count 0): every state of the R = 3 face and the cells beneath.
6. **Agreement on two cautions of the critic that I reached separately.** "c_3 = 0.36 ± 0.01" leans on a
   finite-size allowance taken from k = 2 (the critic: the approach is slower at k = 3; here: the exact slope at
   L = 20–32 is 0.4777 at k = 2 and 0.5516 at k = 1, so the sample quoted at k = 1, 0.542, is itself 0.0095 off). And
   F.4 is a box-wall statement (critic's E19, with the period-2 orbits on periodic walls, which I did not enumerate;
   the checkerboard is verified in `c6`).

Nothing the critic confirmed is wrong in substance; the only wrong number in the line's list came from the lab.

## Not checked

- Claims 9 (sketched), C2 (guessed), c_3 and everything else quoted from the exam or from the lab's samples (the
  decrements of D2, the hazards at age 2, c_6 of D2, V1–V3 of entry 11, the Perron-measure statistics): measured or
  computed by others, out of scope.
- The "Reading" paragraphs (entries 3, 6, 12, 14 points 1–4, 15's last paragraph) and the closing report's "why
  counting stops here": interpretation, not claims. Their arithmetic was checked where a number appears (0.137,
  0.205, (7/8)⁷ = 0.393, 0.607, 0.017, 0.4214, 0.3668, 0.672, 0.638, 0.606).
- Theorem 3 for k ≥ 3 by computation (M_3 has 2^84 states; the reduced matrix 2^36). The proof does not depend on k.
- Claim 8 (b), (c) for k = 2 by computation; (b) for the D4 box by computation (read only).
- Claim 14 for k = 3 by computation (the 7 × 5 strip has 2^35 states).
- Claim 10's product formula on the vertex-centred hull R = 4 for every face configuration (33 cells): 14 of the 512
  face configurations were enumerated against all 2^24 states beneath; the cube-centred hull R = 3 and the slab
  2 × 1 were enumerated completely.
- Proposition G (a)'s remark that Theorem 3 carries over to face12e strips of fixed width, and entry 10's
  parenthesis that the path line's rim lemma gives Lemma 6 for gump with in-face speed 1: read, nothing computed
  (the rim lemma is L1 of the path line, audited in `AUDIT-path.md`).
- The statement quoted in entry 14 that the plane above a face12e wall is sealed was checked from the offsets (a
  cell above sees at most 3 below); `research/audit/REVIEW-class.md` was not read.
- No library source was opened; the line cites none in a proof (Kari is cited from memory in a remark).
