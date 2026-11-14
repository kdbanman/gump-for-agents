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

---

_Round 3 (2026-11-14) was written by a successor from this directory, the critic's reply to round 2 (lab L7) and
`exam/OUTCOMES.md`. Nothing below was simulated or enumerated by me; polynomials were evaluated with a calculator._

## 2026-11-14 · 13 · Exam C-E2 failed (c₃ ≈ 0.36); Lemma 8; the fixed-age programme is closed

**The outcome** (`exam/OUTCOMES.md`, C-E2). True 2D rule, fair soups, rings of L = 20, 24, 28, 32:
−ln P₃ = 7.2385, 8.7149, 10.1824, 11.6366, slope 0.3676 ± 0.0006. The entry said 0.447 ± 0.012. The same samples
give 0.542 and 0.479 at k = 1, 2 against the exact limits 0.5515, 0.4677 (a ring's slope at these lengths is about
0.01 above its limit at k = 2, as in the critic's exact table for D2), so **c₃ = 0.36 ± 0.01**. The theorem
c₃ ≤ c₂ holds. Decrements of the true rule: 0.084, then 0.10–0.11. Of D2 over fresh dice from the same soup:
0.042, 0.017, 0.009, 0.005, 0.003 (lab L7).

**Why the estimate was wrong.** Both guides treated the third generation as a correction to a route already
there. (i) "D2's decrement shifted by the offset at horizon 2" joined numbers from two routes: at horizon 2 the
true rule dies by filling the edge (987 cells alive in 1000 at generation 1) and overcrowding it, one row over
dice dies thin (critic, round 2, §4, §7). (ii) "The steady window cost at the length a gap keeps for three
generations" used a steady-state price for an event of the soup's transient. The true rule's decrement does not
shrink, D2's does: at a fixed age the true rule's cheap deaths use the rows beneath as part of one fluctuation,
which a row over fresh dice cannot do. Which three-generation route costs 0.36 is not known (the window matrix
has 2³⁶ states and the dying ensemble was not sampled).

**What it says about ages.** Hazard at age 2 from the same samples, h₂ = (P₃ − P₂)/(1 − P₂):
−ln h₂ = 7.400, 8.816, 10.247, 11.675 (slope 0.356). Steady ln τ of the same rings (`research/toy2d`; the exam's
control row agrees, slope 0.412 ± 0.005): 9.055, 10.768, 12.368, 14.051. A fair soup loses an edge at age 2 about
5, 7, 8, 11 times as often as a steady state does in one generation, and the factor grows like e^{0.06 L}. (Two
ensembles by design: fair soups with no warm-up against soups of density 0.4 older than 300.) So for the true
rule, as for D2 with fair or sparse soups (lab L7, table of ages), deaths of the soup's own transient outnumber
steady deaths at a fixed age, by a factor exponential in L at every size that can be reached. The alternative,
that the ring's steady exponent comes down to 0.36 or less beyond L = 32, is not excluded by anything proved.

**Lemma 8 (dice chains: a fixed-age death is a steady death or a doomed start) [proved].** Let Q be the
substochastic matrix of a finite absorbing Markov chain on its living states, λ its spectral radius, h = 1 − λ,
and φ ≥ 0 a right eigenvector, Qφ = λφ, normalised by max φ = 1. For every law π on the living states and k ≥ 1,

    P_π(T ≤ k) ≤ (1 − λ^k) π(φ) + π(1 − φ) ≤ k h + π(1 − φ).

*Proof.* 1 ≥ φ pointwise and Q ≥ 0, so Q^k 1 ≥ Q^k φ = λ^k φ, i.e. P_x(T > k) ≥ λ^k φ(x) for every x. Integrate
against π: P_π(T ≤ k) ≤ 1 − λ^k π(φ) = (1 − λ^k) π(φ) + π(1 − φ), and 1 − λ^k ≤ k(1 − λ). ∎
(Irreducibility is not used. When Q is primitive, h is the quasi-stationary hazard and φ(x) is the limit of
P_x(T > k) / max_y P_y(T > k): the chance of x to reach the steady state, relative to the best start. Call 1 − φ(x)
the *doom* of x.)
*Smallest case.* Living states g, d; g stays with probability 1 − h and dies with h; d dies at once. Q = diag(1 − h,
0), φ = (1, 0). For π = (1 − ε, ε): P_π(T ≤ k) = (1 − ε)(1 − (1 − h)^k) + ε, equality in the first inequality: both
terms are needed.

**Corollary [proved].** For a family of such chains indexed by L (D2 on rings or intervals, any depth w, any
family of initial laws π_L), put γ⁻ = liminf −(1/L) ln h_L and θ⁻(π) = liminf −(1/L) ln π_L(1 − φ_L). Then for
every k, liminf_L −(1/L) ln P_{π_L}(T ≤ k) ≥ min(γ⁻, θ⁻(π)); with product laws the left side is the c_k(π) of
entries 4 and 10, so **c_∞(π) ≥ min(γ⁻, θ⁻(π))**. Hence:
(i) if c_k(π) < γ⁻ for some k, then θ⁻(π) ≤ c_k(π): the soup has doomed starts cheaper than a steady death;
(ii) if θ⁻(π) > c_k(π) for some k, then γ⁻ ≤ c_k(π): a fixed-age count is then an upper bound on the steady
exponent.
This replaces C1′. Its first half ("c_∞ ≤ γ under a uniform hazard from a fixed age") was a tautology; what is
true without hypothesis is the opposite inequality up to the doom term, and the hypothesis needed for (ii) is a
lower bound on the cost of doomed starts, which no count of this line gives (φ is the steady state's own vector).

**With the lab's exact numbers** (L7; D2(·, 0.472) on rings, c₆ = 0.4104, 0.4992 for the sparse and the dense soup;
D2(·, ½), c₆ = 0.4757 for the fair soup). Each is ≥ min(γ⁻_ring, θ⁻). So for each soup, either the ring's steady
exponent is at most that number (its exact local step at L = 15–18 is 0.52–0.53), or product rows of that density
have doomed starts at that cost or less. For the dense soup (the steady density, 0.6455) the first reading is
what the probability line's exam P-E1 predicts (0.48 ± 0.03 at L = 30–38); for the sparse soup the second is
plain (thin rows wither: density 0.14 at generation 0 in the dying ensemble).
**No such statement for the true rule.** A finite deterministic map with a trapdoor has no conditionally
invariant measure (board, "trapdoors" (v)), hence no φ and no h. What is exact there is only
D_k ≤ Σ_{j<k} h_j with h_j the from-soup hazard at age j.

**Two one-line facts behind the crowded route [proved].** 2D rule: a live edge cell with four live in-row
neighbours dies iff b ≥ 1, so a full row over cells of density ρ dies with probability (1 − (1 − ρ)²)^L,
0.288 per cell at ρ = ½, and the rest of the cost of that route is the cost of filling. Gump: a face cell with six
live in-face neighbours is dead next whatever lies beneath (claim 11), so a full face dies for nothing.

**Decision.** The fixed-age programme is closed. It is a complete theory of the image measures μ_k of a soup
(Theorem 3, Proposition 4, Lemma 6, the dice hierarchy, the exact c₁, c₂ and the sampled c₃), and those measures
are about the soup: their cheap deaths are a filled and overcrowded edge, which the steady state does not use
(in D2 the share of deaths from a nearly full row falls with L, board E9). C1′ is withdrawn in both halves; the
candidate "equality at density ½ for the 2D rule" (entry 10) is dead, since c₃ is already below the steady slope
of the same rings.

**Correction to entry 11.** The crude count there ("the feedback makes the last step dearer") has the wrong sign
for the two-generation exponent: exactly, V2 − V3 = +0.0030 (the own-column feedback makes dying by generation 2
cheaper), and the whole gap V1 − V0 = 0.042 is the change of route (lab L7, `gap2`, `tilt`). Lemma 7 itself stands.

## 2026-11-14 · 14 · face12e: the wall is a band, and what this line's counts give there

**Lattice.** Cells as gump. A face with normal a has neighbours ±e_a ± e_b, ±e_a ± e_c (as gump) and ±2e_b, ±2e_c
(coplanar, sharing an edge). Rule B45/S345. A wall is the plane z = Z, Z odd, with z > Z dead (sealed:
`research/audit/REVIEW-class.md` §1.2).

**Notation.** Λ = the square lattice of *top cubes* (centres at z = Z − 1); a periodic n_x × n_y wall or a box
wall; A = |Λ| wall faces. σ_q = the top face of q (the sheet S, z = Z). The layer B (z = Z − 1) holds the side
faces: one cell p = {q, q′} for each edge of Λ, 2A cells on a periodic wall. β_q = the bottom face of q
(z = Z − 2). r_p = the face directly below p (z = Z − 3). Write h(i, j) for the side face between cubes (i, j) and
(i + 1, j), v(i, j) for the one between (i, j) and (i, j + 1). In B, h(i, j) is adjacent to h(i, j ± 1), v(i, j),
v(i, j − 1), v(i + 1, j), v(i + 1, j − 1), and v(i, j) to v(i ± 1, j), h(i, j), h(i − 1, j), h(i, j + 1),
h(i − 1, j + 1): the four edges of Λ perpendicular to p at its ends, and the two parallel to it across the two
squares of Λ that contain it. (The four edges of a square of Λ, i.e. the four faces round a vertical cube edge,
are mutual neighbours.) k_p = number of live in-layer neighbours of p.

**Proposition F [proved; every item is read off the offsets].**
1. *Counts.* n(σ_q) = (live among the four sheet neighbours) + (live among the four side faces of q).
   For p = {q, q′}: n(p) = k_p + σ_q + σ_q′ + β_q + β_q′ + r_p. The band reads nothing else below it. β_q is read
   by the four side faces of q and by no other cell of the band; r_p by p only.
2. H = {S = 0 and B = 0} is absorbing (a sheet cell then sees 0, a cell of B at most 3). Neither {S = 0} nor
   {B = 0} is: a cube with four live sides gives birth to its top, and under a full sheet a dead cell of B with
   k = 0 is born iff two of its three cells beneath are alive.
3. *The sheet reads only the band:* S(t + 1) is a function of (S(t), B(t)).
4. *No sheet without the layer.* If B(t) = 0 then σ_q(t + 1) = 1 iff (live sheet neighbours of q) + σ_q(t) ≥ 4:
   a monotone threshold map Θ. On a box wall n × n, Θ^j(full sheet) = {q : d(q) ≥ j}, d = least ℓ¹ distance to a
   corner cell, so Θ^n ≡ ∅: if B is empty for n generations running, the sheet is empty at the end.
   *Proof.* A cell with d = j has its two neighbours towards the nearest corner dead or outside: at most 2, it
   dies and is not reborn. A cell with d ≥ j + 1 is not a corner, has at least 3 neighbours in the box, all with
   d ≥ j. Monotonicity gives the rest. ∎ On a periodic wall the Θ-persistent sets wrap the torus (every cell of
   one has 3 neighbours in it; the lowest left-most cell of a finite set has at most 2), e.g. two adjacent rows.
5. *The layer without the sheet.* If S(t) = 0 then σ_q(t + 1) = 1 iff the four side faces of q are alive at t,
   and each p follows gump's rule on the count k_p + β_q + β_q′ + r_p: six in the layer, two one layer in, one two
   layers in. These are the counts of a gump face cell, with another in-layer graph and another sharing of the
   cells beneath.
6. *Thin route.* On E = {S = 0, no cube has four live sides}: the band is empty at t + 1 iff B(t + 1) = 0, a
   condition on B and its cells beneath with the kill sets of Lemma 5.5 unchanged.

**One generation.** Put a_p = k_p + σ_q + σ_q′ (0 … 8) and b_p = β_q + β_q′ + r_p. A cell p is dead next iff
b_p ∈ K(s_p, a_p), the table of Lemma 5.5 with k replaced by a. With r_p free, the condition on m = β_q + β_q′ is:

| class | when | allowed m |
|---|---|---|
| free | dead, a ∈ {0, 1, 5} or a ≥ 6; live, a ∈ {0, 5} or a ≥ 6 | 0, 1, 2 |
| not both | dead, a = 2; live, a = 1 | 0, 1 |
| **equal** | dead, a = 3 (K = {0, 3}) | 0, 2 |
| at least one | a = 4 | 1, 2 |
| both dead | live, a = 2 | 0 |
| both alive | live, a = 3 | 2 |

**Proposition G (the one-generation trapdoor is a vertex model on Λ, not a product over cubes) [proved].**
(a) Uniform soup, periodic wall: λ(T ≤ 1) = 2^{−4A} Σ_{(S,B)} 1[S(1) = 0] Σ_{β ∈ {0,1}^Λ} Π_{p = {q,q′}} W_p(β_q + β_q′),
W_p(m) = ½ (1[a_p + m ∈ D] + 1[a_p + m + 1 ∈ D]), D = the dead counts for s_p (all but 4, 5 for a dead cell, all but
3, 4, 5 for a live one). The interaction has finite range, so on strips of fixed width Theorem 3 holds as stated.
(b) A band configuration can be emptied in one generation iff S(1) = 0 and a 2-SAT instance on Λ (the table) is
satisfiable. This is not decided cube by cube and the cells beneath are not independent given the band.
*Example* Π₁, wall n × 4, n ≥ 3: a row of top cubes with tops and sides alive, i.e. live cells h(i, 1), v(i, 0),
v(i, 1), σ_{(i,1)} for all i, nothing else in the band. Then: σ_{(i,1)} has n = 2 + 4 = 6 and dies; σ_{(i,0)},
σ_{(i,2)} have n = 1 + 1 and stay dead; h(i, 1) has a = 4 + 2 (free); v(i, 0), v(i, 1) have a = 4 + 1 = 5 (need
b ≥ 1); **h(i, 0) and h(i, 2) are dead with a = 3: "equal"**; h(i, 3), v(i, 2), v(i, 3) have a = 0. So the band
is emptied iff β is constant along row 0 with r_{h(i,0)} equal to that constant, the same along row 2, and
β_{(i,0)} + β_{(i,1)} + r_{v(i,0)} ≥ 1, β_{(i,1)} + β_{(i,2)} + r_{v(i,1)} ≥ 1 for each i. Count: of the 2^{12n}
patterns of the 4n bottoms and 8n cells below B, **32^n (8^n + 2·6^n + 5^n)** empty the band (n = 3: 35,028,992 of
2³⁶), and in every one of them the n bottoms of row 0 are equal: a rigid line of hidden cells of any length. ∎
In gump the same sum is Π_q W_q (Lemma 5): given the face, the cells beneath different top cubes are
independent in the killing ensemble. The frustration of board E10 is local in gump and lattice-wide in face12e.

**The lone cell [proved].** S = 0, one live cell p in B, the 6 bottoms concerned alive with probability ρ_β and
the 7 private cells with ρ_r, independently. The band is empty next iff none of seven cells (p and its six
in-layer neighbours, each dead with k = 1) has b = 3. Their cube pairs are the seven edges of a 2 × 3 ladder
(three rungs, four rail edges). With x = 1 − ρ_r, a = ρ_β, ā = 1 − a, counting vertex sets of the ladder by size
and number of induced edges (1; 6; 8 + 7x; 2 + 8x + 10x²; 5x² + 8x³ + 2x⁴; 2x⁴ + 4x⁵; x⁷):

    P = ā⁶ + 6aā⁵ + a²ā⁴(8 + 7x) + a³ā³(2 + 8x + 10x²) + a⁴ā²(5x² + 8x³ + 2x⁴) + a⁵ā(2x⁴ + 4x⁵) + a⁶x⁷.

At ρ_β = ρ_r = ½: **3793/8192 = 0.4630** (gump's lone cell: 0.4122, entry 12). At 0.52: 0.4214 (gump 0.3668); at the
bulk densities 0.398 and 0.4155: 0.672 and 0.606. Independent threats would give (7/8)⁷ = 0.393 in both lattices;
sharing raises it, more in face12e (each bottom is under up to three of the seven cells).

**At a fixed horizon** entry 4's weak form holds verbatim: e^{−3A ln 2} ≤ λ(T ≤ k) ≤ e^{−c⁻_k A}, c⁻_k > 0. The
guard is a lone closed cube under the wall: each of its faces sees the four that share an edge with it, and a
cell outside shares an edge with at most two faces of one cube (it contains one edge of the cube, which lies in
two of its faces), so the cube is a still life here too.

**What counting gives for the second lattice.**

| | gump | face12e |
|---|---|---|
| set that must be empty | face layer, A cells | band, 3 cells per wall face |
| invertible relative (Lemma 2), frequency of "empty now" | ln 2 per face cell | 3 ln 2 = 2.08 per wall face |
| measured | 0.212 per face cell | 0.410 per wall face = 0.137 per cell of the band = 0.205 per cell of B |
| cells beneath a cell of the layer whose death is final | 2 + 1 | 2 + 1 (and 2 outward, in the sheet) |
| sharing of the cells beneath | within one top cube (a 6-cycle) | every side face belongs to two cubes: all of Λ is coupled |
| one-generation emptiability | cube by cube | 2-SAT on Λ, rigid lines |
| lone cell over fair dice | 0.4122 | 0.4630 |

1. *The unit is not the trapdoor's cell.* Any account that prices the set that must be empty at a fixed cost per
   cell (the starting point of this line; Lemma 2 for the invertible relative) gives face12e three times gump's
   cost per wall face over gump's per face cell: 0.64. Measured: 0.410. What the two lattices share to 3% is the
   cost per cell that has three cells beneath it.
2. *Why the sheet can be free* (Proposition F): it reads only the band, cannot live without the layer (item 4),
   is not born over a thin layer (item 5), and on the thin route the band's death is the layer's death over its
   cells beneath (item 6). This agrees with the review's measurements (the sheet alone empties 4–10 times as
   often as a wall dies and comes back; the first emptiness of B has the wall's own ln τ). It is a statement
   about one generation, not a derivation of 0.205.
3. *What differs does not show.* The in-layer graph, the sharing beneath and the one-generation frustration all
   differ between the two lattices, the last one in kind (Proposition G), and the cost per cell differs by 3%.
   Either the exponent is insensitive to them or their effects cancel; nothing here decides which.
4. This line has no formula for either exponent. Its fixed-age exponents would be, in face12e as in the 2D rule,
   properties of a soup's first generations (entry 13); I do not ask for them.

## 2026-11-14 · 15 · O_h faces: the vertex factor is not a count of independent cells

Side fact: vertex-centred O_h hulls live 1.5–1.7 times longer than cube-centred ones at equal face area.
Coordinates relative to the centre; the face d = (1,1,1) is {x + y + z = R, x, y, z ≥ 0}; T_j = j(j + 1)/2.
- Cube-centred, R = 2N + 1: cells q + e_a, q = 2(a, b, c), a + b + c = N. Vertex-centred, R = 2N + 2: cells
  u − e_a, u = 2(a, b, c) + (1,1,1), a + b + c = N. Both have **A = 3T_{N+1}** cells (R = 35 and 36: 513).
- Under the face's symmetry group C3v (order 6) no cell is fixed by the rotation and each mirror fixes
  m = ⌊N/2⌋ + 1 cells (the cells (x, x, R − 2x) of the type whose normal is z), in both. Burnside:
  **(A + 3m)/6 orbits in both** (N = 3: 6; N = 17: 90). The two faces also have the same number of in-layer
  adjacencies: 3(N + 1)² kagome bonds and 3T_N pairs across hexagons.
- They are different patches. Cube-centred: T_{N+1} complete top-cube triangles (every cell in one), T_{N−1}
  complete triangles of the other orientation, T_N complete hexagons, three tip cells. Vertex-centred: T_{N+1}
  complete triangles of the *other* orientation, T_N complete top-cube triangles, T_{N−1} complete hexagons, and
  **3(N + 1) rim cells each alone in its top cube** (the cube's other two top faces lie outside the hull), so
  that by Lemma 5 they share no cell beneath with any face cell.
- Cells shared with one neighbouring face (third coordinate 0): 2(N + 1) against N + 1.
*Smallest case, N = 1 (A = 9), by hand.* Cube-centred: (3,0,0), (2,1,0), (2,0,1) and permutations: three top-cube
triangles joined by three bonds round the hexagon at (1,1,1); in-layer degrees 4⁶ 2³. Vertex-centred: (2,1,1),
(3,0,1), (3,1,0) and cyclic images: one top-cube triangle (2,1,1), (1,2,1), (1,1,2) with a triangle of the other
orientation on each corner; degrees 4³ 3⁶. Twelve bonds and three hexagon pairs each.
So the factor is not in the number of independent cells, nor in the number of in-layer bonds. It is a boundary
effect of how the layers beneath are attached (which triangle orientation is the top-cube one, and the rim), and
a boundary term in ln τ of order one is what a factor constant in A needs. I have no derivation of its size.
(Hand counts; a check by listing is in the report's requests.)

## 2026-11-14 · 16 · Lemma 2′: with an invariant measure an absorbing event never happens [proved]

Let g preserve a probability measure μ and let g(H) ⊆ H. Then μ(g^{−1}H ∖ H) = 0, hence μ(∪_k g^{−k}H ∖ H) = 0:
almost no point outside H ever enters it. *Proof.* H ⊆ g^{−1}H and μ(g^{−1}H) = μ(H). ∎
This is Lemma 2(ii) without bijectivity (*smallest case:* the doubling map of the circle with Lebesgue measure and
H = {0}: g^{−1}H = {0, ½}). It settles what the lead's starting point for this line can give. For any relative
with an invariant measure that charges the living states (the second-order lift; any rule made
measure-preserving by a permutive reservoir) "face empty" is a recurrent event of frequency μ(H) per generation
(Lemma 1), and a face that is empty for good is never produced. The measured law is the waiting time for an
absorbing event; it exists only because the rule loses measure, and for a finite deterministic map nothing
replaces the uniform measure exactly (no conditionally invariant measure: board, "trapdoors" (v)). The source
line's automaton (edge over a parity bulk; exam S-E1 holds) does die: by this lemma it does not preserve the
product measure, although its bulk alone does.

## 2026-11-14 · 17 · Corrections to entries 13–16 (found on re-reading, same day)

1. Entry 14, Proposition F.2: under a full sheet a dead cell of B with k = 0 is born iff **at least two** of its
   three cells beneath are alive (n = 2 + b ∈ {4, 5}).
2. Entry 14, lone cell, the sentence on bulk densities should read: face12e's polynomial is 0.672 at its bulk
   density 0.398 (and 0.638 at 0.4155); gump's is 0.606 at its bulk density 0.4155.
3. Entry 13, "Decision": the cheap fixed-age deaths are of two kinds, a thin start that withers (D2 from fair or
   sparse soups) and a filled and overcrowded edge (D2 from the dense soup; the true rule at horizon 2). Neither is
   the steady route as far as the lab's tables show.
4. Entry 16, last sentence: delete "although its bulk alone does". I have not proved that and have not read the
   source line's journal. What the lemma gives is only: that automaton does not preserve the product measure on
   (edge, bulk).

---

## Closing report (round 3, 2026-11-14)

**Verdict.** This line has given what its toolkit can give. I see no route by counting to a further proved step
towards the law, and say why below. The directory is in a state to be read cold: `claims.md`, then entries 1–17.

**State of every claim** (numbers as in `claims.md`).
- *Proved and confirmed by the critic:* 1–8, 10–16, 18, and the inequality of 17. In one line each: union and
  gap bounds for maps with an invariant measure; the invertible lift never dies; at every fixed age the death
  probability from a soup is a transfer-matrix trace, exponential in L, with c₁ = 0.551535, c₂ = 0.467693 for the
  2D rule; ring and box edge agree for k = 1, 2; symmetries enter as counted; gump's cells beneath belong to top
  cubes; gaps persist; at a fixed age the true rule is a dice model; exact one-generation numbers over dice.
- *Proved this round, not yet checked:* 19 (Lemma 8 and its corollary), 20 (Lemma 2′), 21–23 (face12e: band
  structure, vertex model with a rigid example, lone cell 3793/8192), 24 (O_h faces: equal orbit counts).
- *Sketched:* 9 ("mirror = exactly half" at a fixed age). Not worth finishing: fixed-age exponents do not bear on τ.
- *Guessed:* C2 (c_∞(½) > 0). No evidence either way; c₃ ≈ 0.36 and the decrements are not shrinking.
- *Fallen:* C1 (round 2); **C1′ (this round**: its hypothesis fails in D2 exactly and, by the exam, in the true
  rule at L ≤ 32); the estimate of exam entry **C-E2 (failed: 0.3676 ± 0.0006 against 0.447 ± 0.012)**; the
  collision-entropy hypothesis; entry 5's comparison with measured slopes; the sign of entry 11's crude count.
- *Exam:* C-E2 failed (entry 13 says what that does: it removes the last candidate for a fixed-age exponent equal
  to a steady one). C-E1 as revised (one mirror on gump hulls, 0.105 ± 0.009) had not been run when this was
  written; no theorem of this line reaches it, its basis is a count of independent cells with a fitted mirror
  term. C-E3 (face12e, the lone cell) is filed today.

**Weakest step.** Of this round: entries 14 and 15 are hand verifications of finite configurations (Π₁, the
ladder polynomial, the two face patches) that no enumeration has checked. Of the line: there is no proved link,
in either direction, between anything counted here and the board's τ. Lemma 8 is the most that is true for dice
chains, and the hypothesis it leaves (doomed starts of a product measure cost more than a steady death) is a
statement about the steady state's own eigenvector, as hard as the law.

**Why counting stops here, and what a different approach would need.**
1. *A measure that counting cannot write down.* A count prices a set under a measure given in closed form.
   The only such measures are a soup and its images μ_k, and their cheap deaths belong to the soup (entry 13).
   With an invariant measure the event never happens (Lemma 2′); a finite deterministic map has no conditionally
   invariant one. The object that carries γ is the rate of empty windows under the stationary measure of the
   *infinite* edge or face, if it exists; Theorem 3(2) is exactly that statement for μ_k, and the limit k → ∞
   does not commute with the rate (Lemma 6). A successor needs that stationary measure, or a dice model's
   quasi-stationary one, with a ratio-type regularity; that is the source and probability lines' ground.
2. *Uniformity in time.* Counting gives lifetimes ≥ c√L (entry 4) and no more. Every known lower bound e^{cL}
   uses monotonicity, which the cap breaks, or a certificate valid from every state (a function whose expected
   value does not fall); the cap forces such a function to be small on full rows as well as on thin ones, and the
   population alone is too coarse (board L5.3). That is the path line's ground.
3. *A deterministic theorem* is nearest by another road: a reservoir that provably delivers dice (exam S-E1
   holds: a deterministic automaton with exactly D2's lifetime), then a dice theorem. Counting adds nothing to it.
4. *The unit.* face12e says the cost is per cell with three cells beneath (0.205 against 0.212), not per cell of
   the set that must be empty (0.137), and that the fine structure of the one-generation constraints does not
   show (entry 14). Any formula for γ should be asked for 0.410 per wall face there, with a sheet that costs
   nothing, and for 0.181 on fcc.

**Lab requests** (checks of this round's hand work; none is needed for a decision).
1. face12e, periodic wall at least 3 × 3, slab at least two cubes deep, sheet empty, one live cell in the layer
   beneath: of the 2¹³ patterns of the 6 bottoms and 7 cells below that matter, 3,793 leave the band empty next.
2. face12e, wall 3 × 4, band configuration Π₁ of entry 14: 35,028,992 of the 2³⁶ patterns of the 12 bottoms and
   24 cells below the layer empty the band (a count by columns or by SAT), and "bottoms (0,0) and (1,0) differ"
   is unsatisfiable. Also Proposition F.4 on a box wall 5 × 5: the full sheet over an empty layer is empty after
   5 steps of Θ and not after 4.
3. Entry 15 by listing the cells of the faces R = 3, 5, 7 (cube-centred) and R = 4, 6, 8 (vertex-centred):
   cells, C3v-orbits, kagome bonds, hexagon pairs, complete triangles of each orientation, rim cells.
Not requested: face12e's c₁, the 2D rule's c₄, the dying ensemble at k = 3. They would describe soups.

**Exam.** C-E3 in `PREDICTIONS.md`: in face12e slabs, a wall whose sheet is empty and whose layer beneath has one
live cell is dead at the next generation with probability 0.44 ± 0.05.

**If the line is recalled**, the two things it can still do quickly are exact one-generation counts for another
lattice (the method of Lemma 5 and Proposition G), and reading the outcome of C-E1.

Round 3 is written; the counting line is finished.

Correction, 2026-11-14: c_2 at soup density 0.472 is 0.466846 (0.4668), not 0.4671 as given in entry 9 (twice: the constants line and the comparison "0.4677 against 0.4671"); 0.4671 came from a power iteration stopped at 400 steps, where the second eigenvalue is 0.99 of the first. The decrement 0.023 at 0.472 stands (0.0231). See `../audit/AUDIT-counting.md` §1.
