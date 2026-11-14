# counting: journal (append-only)

Line: the deterministic rule as a map with a trapdoor (exact counting, transfer matrices, escape rates, entropy).
A successor should read `claims.md` first, then this file. Tags: **[proved]** (complete argument here),
**[sketched]** (says what is missing), **[conjecture]**. Nothing here was simulated or enumerated by me; numbers
"by hand" are arithmetic on formulas written in the entry. Data quoted are from the committed files named.

---

## 2026-11-13 · 1 · Conventions (fixed for the whole line)

- **Vessel, map, trapdoor.** V a finite vessel, X = {0,1}^V, f : X → X the rule with the outside dead.
  F ⊂ V a face (gump) or an edge row (2D rule), A = |F| (L in 2D). H = {x : x|F ≡ 0}. f(H) ⊆ H (T2 and its
  2D analogue: a dead cell of an empty edge row sees ≤ 2 < 3). T(x) = min{t ≥ 0 : f^t(x) ∈ H} ∈ {0, 1, …, ∞}.
- **2D vessels.** Strip W × L: rows r = 0 … W−1, columns x ∈ Z_L, edge = row 0. Box: columns 0 … L−1, no wrap.
  For an edge cell: s = own state, k = live cells among x ± 1, x ± 2 in row 0, b ∈ {0,1,2} = live cells among
  (x,1), (x,2). Next state 1 iff k + b ≤ 4 and k + b + s ≥ 3. The cells (x,1), (x,2) are beneath no other edge cell.
- **Soup.** λ = uniform measure on X (Bernoulli ½ soup, no warm-up, no censoring). μ_k = f^k_* λ, i.e.
  μ_k(y) = |f^{−k}(y)| / |X|: *a state is weighted by its number of k-th ancestors*. This is what replaces the
  uniform measure when f is not a bijection.
- **Death-time law from soup.** D_k = λ(T ≤ k). Because H is absorbing, {T ≤ k} = f^{−k}(H), so
  **D_k = |f^{−k}(H)| / |X| = μ_k(H)**: the law of the death time from soup *is* the count of the trapdoor's
  k-th ancestors. D_k is non-decreasing in k.
- **Which τ.** Everything proved below is about λ(T ≤ k) at a *fixed horizon* k as the edge grows. The board's τ
  (hazard among living, unsettled replicas older than T0) is a different object. The bridge between them is
  conjecture C1 (entry 7), and every comparison with a measured slope below goes through it.

## 2026-11-13 · 2 · Lemma 1: maps that preserve a measure [proved]

Let g : X → X preserve a probability measure μ (finite X), H ⊆ X, T_H(x) = min{t ≥ 0 : g^t x ∈ H}.

**(a) Union bound.** μ(T_H ≤ k) ≤ (k + 1) μ(H). *Proof.* {T_H ≤ k} = ∪_{j ≤ k} g^{−j}H and μ(g^{−j}H) = μ(H). ∎
So at least half of the mass has T_H ≥ 1/(2μ(H)) − 1. No mixing, no bijectivity needed.

**(b) Bijections (the lead's lemma, with the hypothesis it needs).** Let g be a bijection, μ uniform, X′ the union
of the cycles that meet H, and R(x) ≥ 1 the return time of x ∈ H. Then Σ_{x∈H} R(x) = |X′| (Kac), and
Σ_{x∈X′} T_H(x) = Σ_{x∈H} R(x)(R(x) − 1)/2 ≥ |X′| (|X′|/|H| − 1)/2, so the mean of T_H over X′ is at least
|X′|/(2|H|) − 1/2. On X \ X′, T_H = ∞. *Proof.* On a cycle the points of H cut it into gaps; the gap after x ∈ H
is x, gx, …, g^{R−1}x with hitting times 0, R−1, R−2, …, 1, sum R(R−1)/2. Gaps partition X′. Cauchy–Schwarz:
Σ R² ≥ (Σ R)²/|H|. ∎ The bound "|X|/(2|H|) − 1/2" of PROBLEM.md is this with X′ = X; when some cycle misses H the
mean over X is infinite and the bound over the states that do fall has |X′|, which can be as small as |H|.
*Smallest case.* X = Z_n, g = +1, H = {0}: T_H(x) = n − x (x ≠ 0), mean (n − 1)/2: equality.

**Reading.** For a relative with an invariant measure the law reduces to one number, μ(H): rate ≤ μ(H) per
generation, and the long-run frequency of "face empty" is exactly μ(H).

## 2026-11-13 · 3 · Lemma 2: an invertible relative never peels [proved]

**Second-order lift.** Φ(u, v) = (v, f(v) ⊕ u) on X² (state = two consecutive generations). Φ is a bijection
(inverse (v, w) ↦ (f(v) ⊕ w, v)). It is confined to the same hulls: if every cell with s > C is dead in u and in
v, a cell with s > C has f(v) = 0 there (it sees ≤ 3, T2) and u = 0, so it is dead in the next generation. Same
for rows of the 2D rule. So Φ on a hull or strip is the restriction of the lifted rule on the whole lattice.

**(i)** H = {(u, v) : v|F ≡ 0} has |H|/|X²| = 2^{−A} and uniform measure is invariant, so by Lemma 1: the
fraction of pair-states whose face is empty at some generation ≤ k is ≤ (k + 1) 2^{−A}, and the frequency of
"face empty now", averaged over all starts, is exactly 2^{−A}. For this relative the area law is a theorem with
exponent **ln 2 per face cell**, the full entropy.
**(ii)** H₂ = {(u, v) : u|F ≡ v|F ≡ 0} satisfies Φ(H₂) ⊆ H₂, hence Φ(H₂) = H₂ = Φ^{−1}(H₂) (bijection of a
finite set). *No state outside H₂ ever enters it: a face of the lift never dies.* The same holds for any
bijective relative and any absorbing set.
*Smallest case.* One isolated cell (f ≡ 0): Φ(u, v) = (v, u); (1,0) ↔ (0,1) blinks for ever, (0,0) and (1,1)
are fixed; "empty now" holds for 2 of 4 states = 2^{−1}; H₂ = {(0,0)} is never entered.

**Reading.** Peeling exists only because f is many-to-one, and γ measures by how much: with D_k = e^{−c A},
|f^{−k}(H)|/|H| = 2^A D_k = e^{(ln 2 − c)A}. An empty-face state has on average e^{(ln 2 − c)A} times as many
k-th ancestors as an average state (average = 1). With the measured exponents this *ancestor surplus* is
ln 2 − γ ≈ 0.48 per face cell for gump and ≈ 0.28–0.35 per edge cell for the 2D rule. A bijection has surplus 0.

## 2026-11-13 · 4 · Theorem 3: at every fixed horizon the law is exactly exponential in L [proved, 2D rule]

**Setting.** 2D rule, half-plane of rows r ≥ 0, uniform soup. The state of (x, 0) at generation k is a function
G_k of the generation-0 states of the cells (x′, r) with |x′ − x| + r ≤ 2k (each generation reaches 2 cells, along
one axis). So "edge empty at generation k" is a sliding-window condition on the columns of rows 0 … 2k. Let M_k
be the 0/1 matrix indexed by windows of 4k consecutive columns of rows 0 … 2k (m_k = 2^{4k(2k+1)} states), with
M_k(u, u′) = 1 iff u′ is u shifted by one new column and G_k = 0 on the resulting 4k + 1 columns. ρ_k = ρ(M_k).

**Theorem 3.** Define **c_k = (2k + 1) ln 2 − ln ρ_k**.
1. *Ring.* In a strip W × L with W ≥ 2k + 1, for every L ≥ 1: D_k(L) = tr(M_k^L) / 2^{(2k+1)L}. Hence
   D_k(L) ≤ m_k e^{−c_k L} for all L, and limsup_L (1/L) ln D_k(L) = −c_k.
2. *Infinite edge.* In the half-plane, q_k(ℓ) = P(ℓ given consecutive edge cells are all dead at generation k)
   = 1ᵀ M_k^ℓ 1 / 2^{(2k+1)(ℓ+4k)}, so **c_k = lim_ℓ −(1/ℓ) ln q_k(ℓ)** exactly (a true limit).
3. **0 < c_{k+1} ≤ c_k ≤ c_1 < ln 2.** So c_∞ = lim c_k = inf c_k exists, 0 ≤ c_∞ < ln 2.

*Proof.* 1: a state of the ring is an L-periodic configuration of the line; tr(M^L) counts L-periodic sequences
of columns all of whose windows are allowed (true for every L ≥ 1, windows may wrap); rows below 2k are free and
cancel. tr(M^L) = Σ λ_i^L ≤ m_k ρ^L, and limsup tr(M^L)^{1/L} = ρ for a non-negative matrix. 2: the event depends
on ℓ + 4k columns; allowed words of that length are the paths of ℓ steps; (1ᵀM^ℓ1)^{1/ℓ} → ρ (Gelfand). 3:
*c_k > 0*: the lone triple 111 in row 0, all else dead, is a still life of the half-plane (its three cells see 2;
the row-0 cells next to it see 2 and 1; the cells beneath see 1), so the window "triple at the centre, rest dead"
has G_k = 1 and M_k ≤ M_full with M_k ≠ M_full; M_full (de Bruijn) is irreducible with ρ = 2^{2k+1}, so
ρ_k < 2^{2k+1} (Perron–Frobenius). *Monotone*: a dead edge cell whose four in-row neighbours are dead stays dead
(k = 0, b ≤ 2 < 3), so an empty window of ℓ cells at generation k contains an empty window of ℓ − 4 cells at
generation k + 1: q_{k+1}(ℓ − 4) ≥ q_k(ℓ). *c_k ≤ ln 2*: if ℓ + 4k edge cells are dead at generation 0 the
middle ℓ are dead at generation k, so q_k(ℓ) ≥ 2^{−(ℓ+4k)}. *c_1 < ln 2*: next paragraph. ∎

**The case k = 1 in closed form.** The two cells beneath an edge cell are private, so summing them out gives
D_1(L) = 2^{−L} Σ_{S ⊆ Z_L} Π_x w(S_x, k_S(x)), with w(s, k) = P(cell dead next | s, k), b ~ (¼, ½, ¼):

| k | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| w(dead, k) | 1 | 3/4 | 1/4 | 1/4 | 3/4 |
| w(live, k) | 3/4 | 1/4 | **0** | 1/4 | 3/4 |

a 16 × 16 transfer matrix on windows of four edge cells (this is the critic's `iid_flash.py` at p_e = ρ = ½).
*Worked case, L = 5* (every cell's four in-row neighbours are the other four cells; j live cells):
j = 0: 1; j = 1: 5·(3/4)^5; j = 2: 10·(1/4)^5; j = 3: 0 (every live cell has k = 2); j = 4: 5·(3/4)(1/4)^4;
j = 5: (3/4)^5. Sum = 2507/1024. So **exactly 2507 of the 32,768 states of a 3 × 5 strip have row 0 empty one
generation later** (D_1(5) = 2507/32768 = 0.0765). [Lab check requested.]
*Hand bounds.* (i) Restrict S to isolated live cells with ≥ 4 dead cells between them: each live cell carries
(3/4)^5 (itself and its four neighbours, each with k = 1), growth rate the root of λ^5 = λ^4 + (3/4)^5,
λ = 1.1403: **c_1 ≤ ln 2 − ln 1.1403 = 0.562 < ln 2**. (ii) w ≤ 3/4 on every cell of S ∪ N(S) (N(S) = dead cells
within 2 of S) and ≤ 1 elsewhere; Σ_S (3/4)^{|S ∪ N(S)|} has growth rate the root of
1 = λ^{−1} + (3/4)^5 λ^{−6} / (1 − y − y² − y³ − y⁴ − y⁵), y = 3/(4λ) (runs of S ∪ N(S) of length ℓ ≥ 5 contain
a_{ℓ−5} sets S, a_n = compositions of n into parts ≤ 5), λ = 1.5213: **c_1 ≥ 0.273**. Exact value: lab.

**Gump (faces are two-dimensional).** [proved, weaker form] On a slab face of A cells, for every fixed k and A
large: e^{−A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A} with c⁻_k > 0. Lower bound: H ⊆ f^{−k}H. Upper bound: the six
faces of a top cube with every other cell of the box of half-width 2k + 2 (doubled units) around it dead is a
still life for k generations whatever lies outside the box (a lone cube is a still life; influence travels one
cube per generation); disjoint boxes are independent under the soup and ≥ A/(Ck²) of them fit. This gives
c⁻_k ≥ 2^{−C′k³}/(Ck²): positive for each k, useless as k → ∞. The exact exponent is the entropy deficit of a
two-dimensional shift of finite type; a transfer matrix exists for faces of fixed width only.

**What Theorem 3 does and does not say.** For every fixed horizon the law "exponential in the length (area), not
the perimeter" is a theorem for the rules themselves, with an exactly computable constant. It is not the
measured law: the bound m_k e^{−c_k L} is useful only while k ≲ √L. *The whole open problem is the uniformity in
k*: whether c_∞ > 0, and whether D_k(L) ≤ C k e^{−cL} for all k and L (entry 7).

## 2026-11-13 · 5 · Proposition 4: at a fixed horizon, boundary conditions and symmetry enter only as counted [proved]

Notation of entry 4. Let 0 denote the all-dead window, ρ⁰_k = lim_n ([M_k^n]_{00})^{1/n} (the spectral radius of
the communicating class of 0; the limit exists because M_k(0,0) = 1), and c⁰_k = (2k+1) ln 2 − ln ρ⁰_k ≥ c_k.

**(a) Free ends** (edge row = an interval of L cells whose two ends abut the dead outside: the edge of a box, any
depth ≥ 2k + 1). λ(T ≤ k) = [M_k^{L+4k}]_{00} / 2^{(2k+1)L} exactly; exponent c⁰_k ≥ c_k. *Proof.* Columns confine,
so the box is the half-plane with dead columns outside; the configuration is a word w with 0^{4k} w 0^{4k}
allowed, i.e. a closed walk of L + 4k steps at 0. ∎
**(b) Mirror perpendicular to the edge** (ring Z_L, σ : x ↦ −x, soup uniform on the σ-symmetric states).
liminf_L −(1/L) ln λ^σ(T ≤ k) ≥ c_k/2. *Proof.* A symmetric state of rows 0 … 2k is determined by its columns
0 … ⌊L/2⌋, which form an allowed open word; there are ≤ 1ᵀM_k^{⌊L/2⌋+1−4k}1 of those, against
2^{(2k+1)(⌊L/2⌋+1)} symmetric states. ∎ The same proof gives c ≥ c_k/2 for the D4 box.
**(c) Symmetries that fix no edge** (box L × L, L ≥ 4k + 3; C4, or one diagonal mirror). The exponent of
λ^G(top edge dead by k) is **exactly c⁰_k, the same as without symmetry**. *Proof for C4.* Under the rotation a
cell (x, r) of the top band (r ≤ 2k) has its images in the band only if it lies in the left corner square
(x ≤ 2k), whose image is the right corner square. So the band is uniform on configurations whose right corner
square is the rotated left one: 2^{(2k+1)(L−2k−1)} of them. Killable ones number at most [M_k^{L+4k}]_{00} and at
least [M_k^{L−2}]_{00} (both corner squares dead, middle arbitrary). Both have growth rate ρ⁰_k. The diagonal
mirror only makes one corner square symmetric. ∎
**(d) Equality in (a), (b)** (c⁰_k = c_k, and c^σ_k = c_k/2) holds iff a dominant class of M_k contains the
window 0 (resp. a palindromic connecting word). [sketched: for k = 1 a live-free "00" in the edge row is a cut
point (the cells before it keep their k, the two dead cells always have a kill option), and the full row can be
capped as …1111 0 1 00, each cell keeping a non-empty kill set; a complete proof is a strong-connectivity check
on 16 states, requested from the lab. For k ≥ 2 I have no proof.]
**(e) No symmetry inside a light cone.** If the cells within k generations' reach of a set U of cells contain no
two cells of one G-orbit, the law of the history of U up to generation k is the same under the G-symmetric soup as
under the free soup (the G-uniform measure restricted to one cell per orbit is the product measure). In the C4
box this covers the stretch of the top edge at distance ≥ 4k + 1 from both corners (its cone misses both corner
squares, and only those are identified inside the band). So at age k < L/8 the fate of all but 8k + 2 cells of
the edge has exactly the same law in the two boxes, and only the end stretches can differ: *a C4 effect on the
exponent, if real, is made at ages comparable to L, by influence that has crossed a corner or the box.*
*Smallest case of (a).* L = 1, k = 1: the lone edge cell has k = 0; live it dies unless b = 2 (3 of 4), dead it
stays dead (4 of 4): 7 of the 8 states of (edge, two beneath).

**Consequence, if measured exponents are limits of finite-horizon ones (C1 of entry 7):**

  γ(C4 box) = γ(diagonal box) = γ(box) ≥ γ(ring),  γ(mirror ring) ≥ γ(ring)/2,  γ(D4 box) ≥ γ(ring)/2.

**Against the data** (per-edge ln τ in `research/toy2d/data/law_cross2_B34S234*.json`; local slopes mine, by hand):
box without symmetry, L = 12 … 32: 0.331, 0.347, 0.324, 0.357, 0.342 (flat, mean 0.340); C4 box, L = 16 … 36:
0.298, 0.266, 0.283, 0.267, 0.282 (flat, mean 0.279); ring: 0.44 falling to 0.38; mirror ring, L = 16 … 56: 0.173
(flat); D4 box 0.171. Also ln τ(mirror ring, 2m) − ln τ(box, m) = −0.79, −0.71, −0.69, −0.64, −0.69 at
m = 12 … 28: a mirror ring is a box edge of half the length up to a constant factor ≈ ½.
- γ(mirror ring) ≥ γ(ring)/2 reads 0.173 ≥ 0.19–0.22: **violated** unless the ring's slope falls to ≤ 0.347.
- γ(box) ≥ γ(ring) reads 0.340 ≥ 0.38–0.44: **violated** unless the ring's slope falls to ≤ 0.34.
- γ(C4 box) = γ(box) reads 0.279 = 0.340: **violated**, with two straight laws and no visible approach.
So either the three slopes 0.28, 0.34, 0.41 converge at sizes beyond those measured (then *the 2D exponent is not
known to better than 0.28–0.41*, and the lowest straight law is the best guide to the common limit), or C1 is false:
the measured exponent is not a locally determined cost, and something about the long-time state depends on the
global geometry. The C4 case is the sharp one: nothing local to the dying edge distinguishes the two boxes.
(The first two tensions were also noticed by the path line, whose exam entry E1 in `PREDICTIONS.md` tests the
ring; I had not read their journal. The proofs above and the C4 statement are what this line adds.)

## 2026-11-13 · 6 · Lemma 5: beneath a gump face, the cells belong to the top cubes [proved]

Face layer s = d·p = R, d = (1,1,1) (other diagonals by symmetry). A *top cube* is a cube centre q (all even)
with d·q = R − 1; its faces q + e_a are in layer R and q − e_a in layer R − 2.
1. Every cell p of layer R is q + e_a for exactly one top cube (q = p − e_a, a the odd coordinate). The three
   cells q + e_x, q + e_y, q + e_z are mutual in-layer neighbours (a kagome triangle).
2. The two neighbours of p = q + e_a one layer in are q − e_b and q − e_c (offsets −e_a − e_b, −e_a − e_c), and
   q − e_a lies beneath q + e_b and q + e_c. So "beneath" is, cube by cube, the 6-cycle
   (+x) — (−y) — (+z) — (−x) — (+y) — (−z) — (+x). The neighbour two layers in, p − 2e_b − 2e_c, is beneath p only.
3. Hence with α, β, γ′ the states of q − e_x, q − e_y, q − e_z and r_u, r_v, r_w the private cells:
   b_u = β + γ′ + r_u, b_v = α + γ′ + r_v, b_w = α + β + r_w (u, v, w = q + e_x, q + e_y, q + e_z), and the
   nine cells beneath different top cubes are disjoint.
4. The set B of achievable (b_u, b_v, b_w) ∈ {0,1,2,3}³ has **40 of 64** elements: all except the 18 triples
   containing both a 0 and a 3, the 3 permutations of (0,0,2) and the 3 permutations of (3,3,1).
   *Proof.* b ∈ base + {0,1}³ with base ∈ {000, 011, 101, 110, 112, 121, 211, 222}. b_u = 3 forces β = γ′ = 1,
   so b_v, b_w ≥ 1; b_v = b_w = 0 forces α = β = γ′ = 0, so b_u ≤ 1; the rest by the symmetry b ↦ 3 − b, and the
   24 triples in {0,1,2}³ other than permutations of (0,0,2) are checked one by one. ∎
5. **Criterion.** A face cell with state s and k live in-face neighbours is dead next iff b ∈ K(s, k):
   live: K = {0,1,2}, {0,1}, {0}, {3}, {2,3}, {1,2,3}, all for k = 0 … 6; dead: all, {0,1,2}, {0,1}, {0,3},
   {2,3}, {1,2,3}, all. *A configuration of a slab face can be emptied in one generation iff for every top cube
   (K_u × K_v × K_w) ∩ B ≠ ∅*, and under the soup
   λ(T ≤ 1) = 2^{−A} Σ_S Π_q W_q(S), W_q = #{(α, β, γ′, r) ∈ {0,1}⁶ : b ∈ K_u × K_v × K_w} / 64.
   The frustration of board E10 is confined to single cubes. (In a hull, cells beneath that fall outside count 0.)
*Worked case* (the critic's counterexample): (4,4,5), (4,5,4), (5,4,4) are the + faces of the cube (4,4,4);
(4,4,5) is live with k = 3, K = {3}; (4,5,4) is live with k = 2, K = {0}; a triple with a 3 and a 0 is not in B.
*Two corollaries.* A full face (k = 6 everywhere) dies in one generation whatever lies beneath. With the layers
beneath empty (b ≡ 0) a face dies iff every live cell has k ≤ 2 and every dead cell k ≤ 3; with them full (b ≡ 3)
iff every live cell has k ≥ 3 and no dead cell has k ∈ {1, 2}.
*Rough size of gump's c_1* [by hand, not a bound]: sparse and dense faces both give ≈ ln 2 − 0.15 ≈ 0.54 (a
lone live cell costs (45/64)(7/8)⁴ = 0.41, a lone hole in a full face (7/8)⁶-like), 2.5 times the measured
0.21. In gump the cost from soup must fall by more than half between horizon 1 and the steady state; in the 2D
rule by at most a third. This matches the lengths of the plunges (ten generations against two).

## 2026-11-13 · 7 · What I aim to prove, and what I think cannot be done this way

**C1 [conjecture].** For each geometry the measured exponent equals c_∞ = lim_k c_k of that geometry (limit of
exactly computable entropy deficits; from the rule alone). What is proved: c_∞ exists (Theorem 3). What is true
if the hazard from soup is stationary from a fixed age on, uniformly in L: c_∞ ≤ γ. Evidence for equality:
the exponent study's τ(L) = 12.1/E(L − 6.5) (unchecked). Evidence against: entry 5.

**Aims, in order.**
1. Exact c_1, c_2 for the 2D rule (lab) and the shape of the dominant killing ensemble; whether ρ⁰ = ρ.
2. A conditional theorem with a countable hypothesis. First form [proved, two lines]: for any measure μ on the
   top three rows and Y₁ = the one-step death set, μ(Y₁) ≤ (|Y₁| Σ_u μ(u)²)^{1/2} (Cauchy–Schwarz). So if at
   generation j two independent soups agree on the top three rows with probability ≤ 2^{−3L} e^{(c_1 − δ)L}, then
   λ(T = j + 1) ≤ m_1^{1/2} e^{−δL/2}. The hypothesis says the top three rows keep collision entropy
   ≥ 3 ln 2 − c_1 + δ per column; it is exactly computable in small vessels and is a ratio-type statement, not a
   covariance statement. To do: the Hölder version against a product or Markov reference measure, and whether
   the hypothesis is credible (it fails as soon as an empty band of three rows costs less than (3 ln 2 − c_1)/2).
3. Gump's c_1 from Lemma 5 on faces of small width (lab), and the cost of the two pure strategies b ≡ 0, b ≡ 3.

**What I think is out of reach, and why.** A proof of c_∞ > 0 by counting needs a bound on the trapdoor's k-th
ancestors uniform in k, i.e. control of every image measure μ_k of a non-surjective, non-monotone, non-additive
automaton. Finite-horizon counting gives lifetimes ≥ c√L and no more (entry 4). The guard argument cannot be made
uniform: a finite pattern that keeps the edge alive for ever against an arbitrary outside would do it, and for
still patterns there is none in the half-plane (the lowest cell of the right-most column of such a pattern has
4 free neighbours, so if live it can be overcrowded or starved and if dead it cannot be kept dead; the same
furthest-cell argument as T6). For general cellular automata questions of this kind about the limit behaviour
are undecidable (Kari; cited from memory, not opened), so any proof must use what is special here: T5, T6.
I do not see how either gives a quantitative statement about μ_k. I expect this line to deliver exact
finite-horizon constants, inequalities between geometries and symmetries, and conditional theorems, not the law.

---

## Round 1 report (2026-11-13)

**Claims.**
- Lemma 1 [proved]: union bound and Kac/gap bound for measure-preserving maps; the lead's bound needs "every
  cycle meets H".
- Lemma 2 [proved]: the second-order lift of gump (and of the 2D rule) is a bijection confined to the same
  hulls; "face empty" has frequency exactly 2^{−A}; a face of an invertible relative never dies.
- Theorem 3 [proved, 2D rule; weaker two-sided bound proved for gump]: λ(T ≤ k) = tr(M_k^L)/2^{(2k+1)L};
  exponents c_k with 0 < c_{k+1} ≤ c_k ≤ c_1 < ln 2; c_k is also the decay rate of empty windows of the infinite
  edge at generation k; by hand 0.273 ≤ c_1 ≤ 0.562; D_1(5) = 2507/32768.
- Proposition 4 [proved; equalities in (a), (b) sketched]: free ends cost at least as much as a ring; a mirror
  through the edge at least half; C4 and the diagonal mirror exactly as much as no symmetry.
- Lemma 5 [proved]: top-cube decomposition of gump's one-step trapdoor; B has 40 of 64 triples.
- C1 [conjecture]: measured exponent = lim_k c_k.

**Weakest step.** C1. Proposition 4 is rigorous at every fixed horizon, and three of its four consequences are
contradicted by the measured slopes at L ≤ 36–56 (entry 5). I cannot tell from the mathematics whether the
measured slopes are far from their limits or whether the two limits (L → ∞, age → ∞) fail to commute. The C4
box is where to look: flat law, slope 0.279 against 0.340, and a state that visibly differs from asymmetric
chaos (in the data file: settles are a third of all exits at L = 36, h/p₁ = 0.03 against 0.27, bulk activity
lower by 0.04 at L = 16 and 0.01 at L = 32).
Second: for gump everything with a transfer matrix is stated for the 2D rule; the 2D-face versions of
Proposition 4 (O_h faces: exponent ≥ γ/6) are not written out.

**Lab requests** (exact; rule = B34/S234 on the cross unless stated; soup = uniform on all states).
1. *c_1.* `iid_flash.cost(0.5, 0.5)`: this is c_1. Check 0.273 ≤ c_1 ≤ 0.562. Check that exactly 2507 of the
   2^15 states of the strip 3 × 5 have row 0 empty after one generation.
2. *Classes for k = 1.* In the 16-state graph of that matrix (edges of positive weight), restricted to states on
   bi-infinite paths: is it strongly connected? What is ρ⁰ (growth rate of closed walks at 0000) against ρ?
3. *c_2.* Number of L-periodic configurations of rows 0–4 whose row 0 is empty at generation 2 (rows ≥ 5 do
   not matter): growth rate ρ_2, c_2 = 5 ln 2 − ln ρ_2. A reduced state suffices: row 0 over 8 columns, rows 1–2
   over 4 columns (16 bits); rows 3–4 of the centre column are summed out (weight 0–4). Check against brute
   force on the strip 5 × 5 (2^25 states). Also ρ⁰_2, and the same two numbers at soup density 0.472.
4. *Lemma 5.* Does `startpoints.py triangles` give 40 achievable triples with the complement of entry 6? On a
   periodic face (slab, 2 × 2 or 2 × 3 top cubes, ≥ 3 layers): number of face configurations that can be emptied
   in one generation, by SAT, against the per-cube criterion.
5. *Gump c_1* (if cheap): slab face of width 2 or 3 top cubes, growth rate of Σ_S Π_q W_q(S) per face cell.
6. *Collision entropy* (aim 2), exactly, strips 4 × L and 5 × L with N ≤ 25: Σ_u μ_j(u)² for the top three rows
   at j = 1 … 8, where μ_j is the law at generation j from the uniform soup, restricted to (i) all states,
   (ii) states whose row 0 is alive at generation j.

**Next.** Aims 1–3 of entry 7 in that order; if the lab finds ρ⁰_1 < ρ_1, Proposition 4(d) changes and I
rewrite the consequences. Exam entry filed in `PREDICTIONS.md` (provisional; see there).

---

## 2026-11-13 · 8 · Corrections to round 1 (after the critic's reply)

1. **Entry 6, item 3:** "the nine cells beneath" should read **six**: three shared (q − e_x, q − e_y, q − e_z) and
   three private (q + e_a − 2e_b − 2e_c). The formulas there (six bits, 64 cases) are right.
2. **Entry 6, corollary for b ≡ 0:** a cell with k = 6 is dead next whatever lies beneath. Correct statement: with
   the layers beneath empty a face dies iff every live cell has k ≤ 2 or k = 6 and every dead cell has k ≤ 3 or
   k = 6; with them full (b ≡ 3) iff every live cell has k ≥ 3 and no dead cell has k ∈ {1, 2}.
3. **Claim 15 (collision entropy): the inequality stands, the hypothesis is dead.** Lab L3.5: the excess
   (1/L) ln(8^L Σ_u μ_j(u)²) is 0.92–1.03 at generation 2 and 1.7 at generation 8 in strips 4 × 5, 4 × 6, 5 × 5,
   against the c_1 = 0.5515 it must stay below; restricting to living rows does not save it (0.64–0.73 at j = 2).
   *Why it cannot be repaired in this form:* Σ μ² ≥ (largest atom)², so one configuration of the three rows with
   probability above 2^{−1.5L} e^{(c_1−δ)L/2} breaks it, and a non-injective map makes such atoms (the empty band;
   debris). A global Rényi entropy of order > 1 sees the heaviest configuration, not the typical one. A usable
   version must bound a *conditional* law block by block (the board's "mixing ⇒ exponential"; the source line's
   class of drive kernels). I leave it to them.
4. **C1 is withdrawn** (entry 10 says why), and with it the paragraph "Consequence … Against the data" of
   entry 5: the fixed-horizon statements of Proposition 4 are theorems, but nothing proved connects them to
   the measured slopes of rings, boxes and C4 boxes. Two facts from the critic bear on that paragraph and should
   travel with it: in the committed C4 file settling is 97% … 32% of all exits at L = 16 … 36, so its slope 0.28
   is a hazard among the few replicas that have not settled; and the one-row dice model D2 on a segment is
   longer-lived than on a ring at every L ≤ 14 with smaller steps (0.45–0.50 against 0.52–0.53), so "free ends
   below ring in slope at small sizes" needs nothing deterministic and nothing global.

## 2026-11-13 · 9 · The exact constants (lab L3.1–L3.4), for the record

2D rule, uniform soup (density ½): **c_1 = 0.551535** (ρ_1 = 4.608520 of 8), **c_2 = 0.467693**
(ρ_2 = 20.046271 of 32). Soup of density 0.472: c_1 = 0.489963, c_2 = 0.4671. The class of the all-dead window is
dominant for k = 1 (the 16-state graph is strongly connected) and k = 2 (54,591 of 65,536 window states; every
other class is a single state): **c⁰_k = c_k for k = 1, 2**, so at horizons 1 and 2 a box edge and a ring have the
same exponent exactly. Counts confirmed on every state: strips 3 × 5 … 3 × 8: 2,507, 10,846, 47,383, 209,825;
boxes 3 × 5 … 3 × 7: 2,977, 13,850, 64,434; strips 5 × 4, 5 × 5 at generation 2: 224,471, 7,043,564; C4 box 7 × 7:
502 of 8,192 symmetric states = 251 of 4,096 constrained bands. c_3 would need 2^36 window states.
*What the numbers show.* (i) The soup density matters at horizon 1 (0.552 against 0.490) and no longer at
horizon 2 (0.4677 against 0.4671). (ii) One more generation lowers the cost by 0.084 (density ½) or 0.023
(density 0.472). (iii) Successive counts approach the eigenvalue slowly from below (ratios 4.326, 4.369, 4.428
against 4.6085 at L = 5 … 8): a local slope read at L < 10 is 4–6% low.

## 2026-11-13 · 10 · Lemma 6 (gaps persist) and why a fixed-age exponent is not the measured one

**Lemma 6 [proved].** For the edge row of the 2D rule, whatever lies beneath it (true rule, dice, anything): if
the edge cells of a window of ℓ + 4j consecutive cells are dead at generation k, the middle ℓ are dead at
generation k + j. Hence for every translation-invariant initial law, q_{k+j}(ℓ) ≥ q_k(ℓ + 4j).
*Proof.* A dead edge cell whose four in-row neighbours are dead has n = b ≤ 2 < 3 and stays dead; so an empty
window loses at most two cells at each end per generation. ∎ (Gump: the path line's rim lemma gives the same
with in-face speed 1.)

**Consequences [proved].** Write c_k(π) for the exponent of entry 4 with the soup replaced by a product (or any
finite-range Markov) initial law π; Theorem 3 holds verbatim with weights.
1. c_k(π) ≤ c_0(π), the cost of an empty window under π itself: for the Bernoulli(p) soup **c_k(p) ≤ −ln(1 − p)
   for every k**, so c_∞(p) → 0 as p → 0. *The fixed-age exponent is a property of the rule and the soup, not of
   the rule.* (Round 1 said "from the rule alone": wrong.)
2. A gap of length ℓ made at any age is still there, in part, ℓ/4 generations later. So in the limit "L → ∞ at
   fixed age", which is the limit of Theorem 3, the first generations are never forgotten: c_k(π) is the cost per
   cell of the cheapest way to make *long gaps by age k, starting from π*. The measured law is the other order,
   age → ∞ at fixed L. The two can only agree if no route through the soup's first generations is cheaper than
   the routes of the steady state, and counting at a fixed age cannot tell whether that is so.
3. **Dice hierarchy.** For D2(L, ½; w) (true rule in the top w rows over two rows of fresh fair dice) started
   uniform, P(row 0 empty at generation k) equals the true rule's D_k(L) whenever w ≥ 2k − 1. *Proof.* Row 0 at
   generation k reads rows ≤ 2(k − t) of generation t; for t = 0 these are uniform in both systems (rows ≤ 2k ≤ w + 1);
   for t ≥ 1 they are rows ≤ 2k − 2 ≤ w − 1, computed by the rule from rows ≤ 2k of generation t − 1, and no die
   later than generation 0 is read. ∎ So the true rule and the dice models share c_1 (all w), c_2 (w ≥ 3), c_3
   (w ≥ 5): *at a fixed age the true rule is a dice model.* What the true rule has and the dice models lack is
   only visible at ages beyond (w + 1)/2.

**What survives of C1.** The following is the most that I think is true, and none of it is proved.
C1′ [guessed]: if the hazard of soup-started replicas of age ≥ j₀ is e^{−γ L + o(L)} uniformly in L for some
fixed j₀, then c_∞(π) ≤ γ for every π (deaths at ages j₀ … k are among the deaths by age k); equality holds for
those soups that have no cheaper route through their first generations. For the 2D rule at density ½ the first
two generations are not cheaper than any measured slope (c_1, c_2 > 0.44), and c_2 does not depend on the
density near ½, so density ½ is a candidate for equality; nothing more can be said without c_k for larger k.
Requested (report): the same sequence for D2, where c_1 … c_4 need 2⁴ … 2¹⁶ window states and the
quasi-stationary exponent is exact (lab L0b.4). That is a place where the two orders of limit can be compared
with no sampling on either side.

**Dead end recorded: the measured exponent as a limit of fixed-age transfer-matrix exponents.** To see a window
of ℓ cells in its steady state one needs age ≳ ℓ/4 (Lemma 6), i.e. M_k with k ≳ L/4, of size 2^{4k(2k+1)}:
larger than the vessel's own state space. Finite-horizon counting gives the transient law exactly and the
steady law not at all. This is the same obstruction as "the bound is useful only while k ≲ √L" of entry 4, seen
from the other side.

## 2026-11-13 · 11 · The dice gap at horizon 2: what can be said by hand, and the exact comparison to run

The lead's question for this line: one row over dice has the right form and too large a constant (2D rule:
0.52–0.53 per cell, exact, against 0.36–0.42; board E13). By the hierarchy identity (entry 10) the true rule and
D2 agree exactly at horizon 1 and first differ at horizon 2, where the rows beneath are no longer fresh. So the
gap can be isolated, exactly, in its first generation.

**Lemma 7 (a live edge cell thins its own support) [proved, by hand].** Uniform soup, half-plane. Given the
state s of the edge cell (x, 0) at generation 0, the cells beneath it are alive at generation 1 with probability

| | (x, 1) | (x, 2) | expected b₁(x) |
|---|---|---|---|
| s = 0 | 85/128 = 0.664 | 161/256 = 0.629 | 331/256 = 1.293 |
| s = 1 | 76/128 = 0.594 | 119/256 = 0.465 | 271/256 = 1.059 |

*Proof.* (x, 1) has seven neighbours in the half-plane: (x, 0) and six others, m ~ Bin(6, ½), n = s + m. Born iff
n ∈ {3, 4}, survives iff n ∈ {2, 3, 4}, own state fair. s = 0: (35 + 50)/128. s = 1: m ∈ {2, 3} or m ∈ {1, 2, 3}:
(35 + 41)/128. (x, 2) has eight: (x, 0) and seven others, m ~ Bin(7, ½). s = 0: (70 + 91)/256. s = 1:
(56 + 63)/256. ∎
At density ½ a cell beneath is more often overcrowded than starved, so one more live neighbour above removes
0.23 live cells beneath on average. Which way this moves the cost of emptying the edge is **not decided by the
lemma**: a sparse edge dies when b is low under its live cells (kill sets {0,1} for k = 0, {0} for k = 1) *and*
low under their dead neighbours (dead, k = 1: {0,1}; k = 2: {0}); the feedback lowers b under the former and
raises it under the latter. Crude count for one isolated live cell with four dead neighbours, cells beneath
treated as independent with the densities of the table: (1 − 0.594·0.465)(1 − 0.664·0.629)⁴ = 0.083, against
(1 − 0.588²)⁵ = 0.120 for dice of the same mean density: the feedback makes the *last* step dearer, not cheaper.
So if the true two-step cost is below the dice one, it is not because of this column-by-column feedback.

**The exact comparison (lab request 2).** Four numbers at horizon 2, each a transfer-matrix exponent:
- V0, the true rule: c_2 = 0.467693.
- V1, fresh fair dice at generation 1 (= D2(L, ½) from a uniform row).
- V2, fresh dice at generation 1 with the true one-column law of the pair ((x,1), (x,2)) at generation 1,
  independent between columns and of row 0 (isolates the density: 0.629 and 0.547 instead of ½).
- V3, the same with the true law of that pair given (s₀(x), s₁(x)), the edge cell's own two states (isolates the
  feedback of Lemma 7).
V1 − V2 is the effect of the density, V2 − V3 of the own-column feedback, V3 − V0 of everything spatial.

## 2026-11-13 · 12 · Gump: exact one-step death probabilities of the smallest faces over dice [proved]

Corollaries of Lemma 5, for a slab face over cells beneath that are independent with density ρ (D3 with one face
layer; at ρ = ½ also the true rule's first generation from soup).
- **Lone cell** (one live face cell, k = 0). It dies iff b ≤ 2; its two cube-mates stay dead iff b ≤ 2 (k = 1);
  its four other in-face neighbours lie in four different cubes and stay dead iff b ≤ 2. So
  **P(face empty next) = (1 − 3ρ³ + 3ρ⁵ − ρ⁶)(1 − ρ³)⁴** = (45/64)(7/8)⁴ = 0.412 at ρ = ½; 0.607 at ρ = 0.4155.
- **Lone triangle** (the three top faces of one cube; each has k = 2, kill set {0}). It dies iff **all six cells
  beneath its cube are dead**; its twelve dead neighbours (k = 1 each) lie two by two in six cubes and none is
  born iff no b = 3 there. So **P(face empty next) = (1 − ρ)⁶ (1 − 2ρ³ + ρ⁵)⁶** = 0.0036 at ρ = ½; 0.017 at
  ρ = 0.4155. A cell of the triangle survives iff at least one of its three cells beneath is alive.
*Smallest case check by hand:* ρ = ½, lone cell: of the 64 states beneath its cube 64 − 3·8 + 3·2 − 1 = 45 give no
b = 3 in the cube.
*Reading (for the path line, not a claim of mine).* The measured one-step death probabilities of gump's faces
are 0.37–0.41 from one cell and 0.019 from three (board L1.1; 38% of three-cell faces are triangles). The
lone-cell formula gives that value at ρ ≈ 0.50–0.52, not at the bulk density 0.4155 (0.61): under a nearly dead
face the cells beneath behave like fair dice. The triangle is 100 times harder to lose than a cell at ρ = ½,
which is the size of the excess at n = 3 in the tail (p₂/p₃ ≈ 0.5, p₃/p₄ ≈ 0.8).

---

## Round 2 report (2026-11-13)

**Claims now** (full list in `claims.md`).
- Standing from round 1, confirmed by the critic: Lemmas 1, 2, 5; Theorem 3 with **c_1 = 0.551535,
  c_2 = 0.467693**; Proposition 4 with c⁰_k = c_k for k = 1, 2 [all proved].
- New: Lemma 6 (gaps persist: q_{k+j}(ℓ) ≥ q_k(ℓ + 4j)) and its consequences: the fixed-age exponent depends on the
  soup (c_k(p) ≤ −ln(1 − p)); the true rule is a dice model at every fixed age (D2 with w ≥ 2k − 1 rows) [proved].
- New: Lemma 7 (a live edge cell lowers the expected live count beneath it from 331/256 to 271/256) [proved];
  exact one-step death probabilities of a lone cell and a lone triangle of a gump face over dice [proved].
- Withdrawn: C1 and the comparison of Proposition 4 with measured slopes; the hypothesis of claim 15.
- Guess C1′: c_∞(π) ≤ γ for every soup, with equality when the soup's first generations offer no cheaper route.

**Weakest step.** There is no proved link, in either direction, between any number this line can compute and
the measured law. Lemma 6 shows why the natural link fails (order of limits), and I see no way round it by
counting: the steady state of a window of ℓ cells needs horizon ≳ ℓ/4. What the line has are exact statements
about the first generations of a soup, and exact one-step probabilities over dice. C1′ is untested; request 1
would test it where both sides are exact.

**Lab requests** (exact; in order of use to me).
1. *Fixed-age exponents of D2 against its quasi-stationary exponent.* D2(L, ρ) on a ring, row 0 started
   Bernoulli(p), event "row empty at generation k" (absorbing): c_k = −ln of the Perron eigenvalue of the
   transfer matrix on windows of four cells of each of the rows S_0 … S_{k−1} (2^{4k} states; weight
   p^{s}(1−p)^{1−s} for S_0, P(S_{t+1}(x) | S_t window) between rows, w(S_{k−1} window) at the end). k = 1 … 4 at
   (p, ρ) = (½, ½), (0.472, 0.472), (0.6455, 0.472). And the exact steps of ln τ of D2(L, ½) at L = 15 … 18 to
   set beside them. Question: does c_k level off, and at the ring's step (0.52–0.53) or below it?
2. *The dice gap at horizon 2* (entry 11): the exponents V1, V2, V3 (V1 is request 1 at k = 2, p = ρ = ½). For
   V2, V3 the pair law at generation 1 is that of the true rule from the uniform soup in the half-plane (a
   function of a 5 × 5 neighbourhood; exact by enumeration).
3. *What a dying soup looks like:* in the Perron (tilted) measures of M_1 and M_2 at density ½, the density of
   live edge cells at generation 0 and (k = 2) at generation 1, and the frequency of the windows 00000 and of
   isolated live cells.
4. *Gump's c_1* on a slab face three top cubes wide (the critic's offer: 2^18 states): growth rate per face cell
   of Σ_S Π_q W_q(S), at density ½ and at 0.4155. My hand estimate is 0.54; the point is the ratio to the measured
   0.21, against 0.55/0.41 for the 2D rule.
5. *Check of entry 12:* slab face 3 × 3 top cubes (or any face without doubled neighbours), cells beneath
   uniform: number of states beneath (of those that matter) for which a lone cell, and a lone triangle, leave
   the face empty next generation; against 0.41216 and 0.003553.

**Next.** If request 1 shows c_k levelling at the quasi-stationary step, C1′ becomes a usable conjecture and I
state it as the line's formula for the 2D rule, with c_3 (exam C-E2) as its test on the true rule. If c_k falls
through the quasi-stationary step, transient deaths dominate at fixed age even for fair soups and the
finite-horizon programme has no bearing on γ; I would then stop it and spend the remaining effort on exact
one-step counts for gump faces over dice (entry 12 extended to all states with ≤ 4 cells), which the path and
source lines can use.
