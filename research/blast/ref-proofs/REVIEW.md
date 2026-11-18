# blast/ref-proofs: referee's review of `rigour` (proofs, exact numbers) and `image` (seam identity)

Agent `ref-proofs`, 2026-11-18, 04:15–04:50 UTC. Verdicts: CONFIRMED / CORRECTED / REFUTED / NOT TESTED.
All of my numbers come from my own code, written from `docs/AUTOMATON.md` and the definition of the surrogate S
alone (`ref.py`: geometry from the 12 offsets, coins enumerated, dense 2^A kernel, numpy; `ref15.py`: the same
kernel lumped over a tube's translations; `seam.py`; `lemmaR.py`). I read rigour's `geom.py` only for the *names*
of shapes (which lattice "torus H K D" is, which unit cell a strip uses). Outputs are in `data/`.

Summary: **nothing marked [proved] broke as mathematics, and every exact number I recomputed agrees to all
printed digits.** Four readings are corrected (A1 reading, A2 hypothesis, A3 discrete form, B consequences),
and one new exact fact bears on Theorem 3's hypothesis (A2, point 3).

## A. `rigour`

### A4. Exact numbers — CONFIRMED (12 rows, all printed digits)

`python3 ref.py <kind> <args> --eig --tilt --bust --lemma0` (9 cells: seconds; 12 cells: under a minute);
`python3 ref15.py 1 5` and `ref15.py 0 5` (15 cells, 40 s each). ln τ = −ln h, h = 1 − λ₁ of the killed kernel.

| row of `exact.csv` | rigour ln τ | mine | h (mine) |
|---|---|---|---|
| hull_R3 (rimmed triangle, 9) | 2.483715746334 | 2.483715746334 | 8.3432634405111e-02 |
| torus_1_1_3 (9) | 2.694626605944 | 2.694626605944 | 6.7567606407153e-02 |
| torus_1_0_3 (tube girth 1, 9) | 3.393524719052 | 3.393524719052 | 3.3590072430405e-02 |
| strip_1_3 (9) | 2.798878056925 | 2.798878056925 | 6.0878326340731e-02 |
| patch_1_3 (9) | 1.880418934121 | 1.880418934121 | 1.5252619394337e-01 |
| torus_2_0_2 (12) | 3.981836588280 | 3.981836588280 | 1.8651353006089e-02 |
| torus_1_1_4 (tube, 12) | 3.711833898815 | 3.711833898815 | 2.4432675106801e-02 |
| torus_1_0_4 (tube girth 1, 12) | 4.133012406313 | 4.133012406313 | 1.6034503556457e-02 |
| patch_2_2 (12) | 3.385498701050 | 3.385498701050 | 3.3860751741881e-02 |
| strip_2_2 (12) | 4.489319585589 | 4.489319585589 | 1.1228281095304e-02 |
| torus_1_1_5 (tube, 15) | 4.387194740124 | 4.387194740124 | 1.2435565327880e-02 |
| torus_1_0_5 (tube girth 1, 15) | 4.633525444726 | 4.633525444726 | 9.7204297869186e-03 (theirs …197: 12 digits) |

Density, the shares of deaths from 1, 2, 3 live cells and p₁..p₄ also agree to the digits printed (`data/exact9.txt`,
`data/exact12.txt`, `data/exact15_*.txt`). `numpy.linalg.eigvals` on the full killed kernel gives the same h for
all five 9-cell shapes and for torus_2_0_2 (4095 × 4095; `data/eig12.txt`), with |λ₂/λ₁| = 0.62 (triangle), 0.81,
0.66, 0.76, 0.93 (patch 1×3), 0.62 (12-cell torus): one dominant eigenvalue, as rigour says (its "0.62–0.81"
leaves out the 1×3 patch at 0.93). An independent simulation (`ref.py … --mc 300000`, deaths later than 40
generations after a fair start) gives ln τ = 2.6948 ± 0.0018 and 2.4838 ± 0.0018 on torus_1_1_3 and the triangle.
NOT TESTED: the 18-cell rows, every Monte Carlo row, `mc.c`, the `hull2` rim.

### A4′. Bust share ("wrapped faces bust, rimmed faces starve") — CONFIRMED at 9, 12, 15 cells, with three riders

Definition taken from `qsd.c`: from the quasi-stationary law, share of the death flux whose last 6 transitions
(the death included) contain a fall of ≥ ⌈A/2⌉ live cells in one generation. My method: the exact law of the
last K transitions, P_μ(T = K, no half-fall)/P_μ(T = K), by powers of the dense kernel with the half-fall
transitions deleted (`--bust`), and a plain simulation (`--mc`).

| face | rigour | mine, exact | mine, simulation | of which the death step itself is the half-fall |
|---|---|---|---|---|
| torus_1_1_3 (9) | 0.9369 | 0.936853 | 0.9365 ± 0.0004 | 0.3797 |
| triangle R=3 (9) | 0.0170 | 0.017018 | 0.0170 ± 0.0002 | 0.0003 |
| torus_2_0_2 (12) | 0.5675 | 0.567517 | | 0.0987 |
| torus_1_1_4 (12) | 0.7909 | 0.790945 | | 0.1684 |
| torus_1_0_4 (12, girth 1) | 0.4466 | 0.446610 | | 0.1081 |
| patch_2_2 (12) | 0.0196 | 0.019558 | | 0.0001 |
| strip_2_2 (12) | 0.2875 | 0.287524 | | 0.0009 |
| torus_1_1_5 (15) | 0.8177 | 0.817663 | | 0.1186 |

The "living" baselines also agree (0.267530 and 0.006333 at 9 cells; `data/living_baseline.txt`). So the claim
that matters stands: **in a model with nothing but private coins beneath, small wrapped faces die after a
crash and small rimmed faces thin out.** Riders, none of which rigour hides but which the owner's report should
carry:
1. *Half-falls are ordinary life on a small wrapped face.* 27% of all 6-generation windows of a living 9-cell
   torus contain one (0.6% on the triangle). The death flux is enriched over that baseline by a factor 3.5
   (wrapped) against 2.7 (triangle); in odds, 40 against 2.7 at 9 cells, 5.5–10 against 2.5 at 12 (the 12-cell
   baselines are rigour's; I recomputed the baselines at 9 cells only). The contrast
   between shapes is first of all a contrast in how often faces crash at all, then in how deadly a crash is. The
   triangle is as often populous as the torus (P(≥ 7 of 9 alive) = 0.133 against 0.161) but a populous triangle
   does not crash: its rim cannot be overcrowded. That is rigour's mechanism and my numbers agree with it.
2. *Part of the bust share is a one-generation annihilation of an over-full face* (last column): 38% of all
   deaths at 9 cells, 10–17% at 12, 12% at 15; by rigour's Monte Carlo column `halffall_death` it falls to 0.3% at
   36 cells (about e^(−0.18·A)). The marker "half the whole face" is tied to the face's size.
3. *"Wrapped" is not sufficient.* Girth-one tubes (wrapped, 6 neighbours per cell): 0.6466 at 9 cells, 0.4466
   at 12, **0.2073 at 15** (mine; rigour's table shows only the 12-cell value). The periodic strip 1×3 is at
   0.0084. The share is graded by how overcrowdable the face is, not by wrapped/rimmed as such.
NOT TESTED: 0.0030 on the 18-cell triangle; all shares above 15 cells (Monte Carlo); anything about gump.

### A1. Theorem 2 (tilt identity) — CONFIRMED as an identity; its reading CORRECTED

Checked line by line and numerically on the 10 shapes of 9 and 12 cells (`--tilt`: ∫₀¹⟨E⟩_s ds − ln τ = 4·10⁻¹⁵ to 1.4·10⁻¹⁴, 48-point
Gauss–Legendre; price map and cumulants of the triangle equal rigour's to 8 digits).
- τ is E_μT = 1/h, h = Σμ(x)d(x) = 1 − λ₁: the mean death time from the quasi-stationary law. Correct, and
  P_μ(T > t) = λ₁^t is standard.
- The identity is exact. It uses exactly two facts: h = E_μ[d] and d(x) = P(x, ∅) = Π_i d_i(x) (product kernel),
  plus (K) so that E < ∞ on every state. Nothing else about the chain enters; "death in one step from any
  state" is (K) itself. If (K) failed on a set of μ-mass m the identity would read
  ln τ = −ln(1 − m) + ∫₀¹⟨E⟩_s ds; on every graph I ran min d_i = ρ1²ρ2 = 0.081312 > 0.
- Convexity is used correctly: (ln Z)″ = Var_s(E) ≥ 0, so ⟨E⟩_s falls and ⟨E⟩₁ ≤ ln τ ≤ ⟨E⟩₀.
- ε_max = −ln(ρ1²ρ2) = 2.509462 (a live cell with three live neighbours dies only on three heads), by my own
  enumeration over (state, k, coins) on every graph, corners included. 2.509·A is right.
- μ₁ ∝ μ·d is the law of the last living state. Correct (Σ_t λ^t μ(x)d(x)).
- **Reading, corrected.** "ln τ is exactly a sum of local costs" is true of the *observables* and of nothing else:
  (i) the identity is −ln E[e^(−E)] = ∫₀¹⟨E⟩_s ds, valid for any positive random variable; (ii) the price map c_i
  is not canonical: the chain rule h = Π_i P_μ(i dead next | cells before i dead next) is an equally exact "sum of
  local costs" with other values (triangle, corners: 0.048 by the tilt; 0.170, 0.037, 0.006 by the chain rule in
  cell order; both sum to 2.483715746334; `--tilt` prints both). "A wrapped face has exactly one price per cell"
  is the statement that ln τ/A is a number. (iii) All non-locality sits in μ_s. At s = 1 the measure is the last
  living state: 57–76% one live cell, ⟨E⟩₁ = 0.70–1.63 in total at 9–12 cells. So the lower bound ⟨E⟩₁ ≤ ln τ is
  O(1), and for large faces the identity says ln τ ≈ −ln μ(nearly empty states): the whole problem (the tail of
  the quasi-stationary law) is inside the tilted measure, untouched. The upper bound is honest and weak
  (⟨E⟩₀/A = 0.69–1.19 against ln τ/A = 0.21–0.38).

### A2. Theorem 3 (structure, conditional on SSM) — CONFIRMED as an implication; hypothesis CORRECTED; scope CORRECTED

1. *The implication is valid and nearly empty.* (a) is the hypothesis summed over cells and integrated over s;
   (b)–(d) are geometry. Nothing is smuggled, and nothing is gained beyond "if the local means are local, the
   exponent is local".
2. *(SSM) as written is false at s = 1, for a trivial reason.* On wide tori all cells of an orientation are
   alike, so the mean of ⟨ε_i⟩₁ over cells is ⟨E⟩₁/A. ⟨E⟩₁ ≥ P(death from one live cell)·E(one live cell)
   ≥ 0.57 × 0.594 (7 cells × −ln(1 − ρ1²ρ2); the 0.57 is measured), and it stays O(1) when deaths come from O(1)
   cells. So ⟨ε_i⟩₁ = Θ(1/A), its limit e_∞(1) is 0, and K·e^(−r_i/ξ) with r_i ~ √A cannot bound 1/A. **Missing
   step, and its repair (closed):** state the hypothesis as |⟨ε_i⟩_{s,G} − e_∞(s)| ≤ K e^(−r_i/ξ) + K₀/A. Then
   (a) gains an additive K₀ and (b)–(d) are unchanged.
3. *Is the hypothesis plausibly false for wrapped faces? Yes, and it is visible exactly at 9–15 cells, in a
   quantity rigour's test cannot see.* [measured, exact, mine] Under μ_s the population of a wrapped face is
   two-humped for every s ≳ 0.1: a sparse hump and an over-full hump, e.g. tube (1,1),(0,5), s = 0.3:
   P(≤ 4 alive) = 0.61, P(≥ 10 of 15) = 0.28, valley 0.014 at 8; the valley at s = 0.3 deepens with size (0.029,
   0.026, 0.014 at 9, 12, 15 cells on the (1,1) tubes). Rimmed faces (triangle, patch 2×2, patch 1×3) have one
   hump at every s. The reason is plain: an over-full face has E ≈ 0 as surely as an empty one (every cell with 6
   live neighbours dies), so e^(−sE) selects both. rigour's proposed test (does Var_s(E)/A grow like A?) is
   blind to this, because E is small on *both* humps; the test must be on the population (or on the occupancy)
   under μ_s. Whether the mixture survives in large faces is open: at s = 1 its weight is the one-generation
   annihilation share, which dies like e^(−0.18·A); at s = 0.2 the two humps are of comparable weight at 15 cells (0.55 sparse, 0.37 over-full).
   (Also: rigour's "largest slope 2.3 on the 9-cell triangle" is 2.60–2.63 = Var_s(E)/A at s = 0–0.1 by my code
   and by its own cumulant k2 = 2.5998; the 12-cell torus's 1.5 is right.)
4. *The link "two exits ⇒ SSM fails" is not an implication.* The exits are properties of paths (six
   generations); μ_s is a reweighting of one instant. Only the one-generation part of "bust" (10–38% of deaths
   here, vanishing with size) appears in μ_s as a second kind of face. A death that crashed three generations ago
   and one that starved look the same to μ₁.
5. *What the theorem licenses.* The contrapositive only: two bulk prices ⇒ the tilted local means are not
   uniformly local. Not: "two prices are impossible", nor "the rimmed slope must fall towards the wrapped one".
   And it is a theorem about S; for gump E is not a sum over cells (rigour says so), and S does not have gump's
   order in the first place (triangles die sooner than wrapped faces in S), so the sentence "under this theorem
   gump's two prices mean one of two things, and nothing else" is an analogy, not a consequence.
6. *The refinement* (ln τ = c_∞A + b·rim + corners; additivity over loop vectors as "first order of an image
   expansion") is marked "stated, proof the same". It is NOT proved by the same proof: (SSM) bounds the effect
   of the far geometry, it does not say that two images act additively. That needs a second hypothesis (the
   joint effect of two perturbations differs from the sum by a product of their sizes). Label: [conjectured].
7. *"A length² discount cannot persist"* is true unconditionally and says little: 0 ≤ ln τ ≤ ε_max·A, so any
   discount is ≤ c_∞·A, linear in length at fixed girth. For gump's loop² 12 tubes (discounts of a few tenths of
   a nat against c·A ≈ 20) that bound allows quadratic growth for another factor of about 7 in length.

### A3. Lemma R — CONFIRMED (calculus); discrete form CORRECTED; the 0.29 reading CONFIRMED within errors

- The three formulas are derivatives of −ln Σ_r h_r. Correct. They hold for *any* partition of deaths, so
  "step − p·(slope of the log-odds)" is identically −d ln h_starve/dA: the measured content is that h_starve is
  exponential in the tube's length, nothing more.
- "For integer A … exact for the mixture of exponentials" is wrong as written. The exact step is
  ln τ(D+1) − ln τ(D) = c_s − ln(1 − p(D)(1 − e^(−(c_b − c_s)))), not c_s + p(c_b − c_s) (Jensen; the difference is
  0.007–0.011 per unit here, the size of the errors).
- `python3 lemmaR.py` (rigour's rows, weighted; `data/lemmaR.txt`): −Δ ln h_starve per unit of length =
  0.566, 0.594, 0.562, 0.571, 0.626, 0.594 (± 0.014–0.024) for D = 8→9 … 14→16: constant at 0.585 within the errors (χ² about 9 on 5; neighbouring steps share a point).
  −Δ ln h_bust = 0.92, 0.92, 0.84, 0.90, 0.88, 0.79, 0.87: 0.87 with scatter beyond its errors (0.918 ± 0.008
  against 0.842 ± 0.011 on neighbouring steps). The log-odds fall by 0.30 per unit over D = 7–12 and by
  0.22 ± 0.02 over D = 12–16: "0.29 per unit" is the early slope, not a constant. The README's list of shares has
  no entry for D = 13 (it runs 5…12, then 14) without saying so.
- Rider (rigour states it): the second branch is defined by exclusion, with a marker tied to the whole face.

### Other statements marked [proved] in `THEOREMS.md`

- (K) — CONFIRMED by enumeration on the 10 graphs of 9 and 12 cells (min d_i = 0.0813; hull corners have coins (2,0), two
  neighbours).
- Lemma 0 — CONFIRMED: proof read (steps (1)–(4) hold; in (4) the lines' Y cells have k = 1 or 2 as claimed), and
  checked by exhaustive reachability on five tori (`--lemma0`): one class of 2^A − 2 states containing u, the
  single state outside it (all alive) goes to ∅ surely, every state is a successor of u, u → u.
- Theorem 1 — CONFIRMED (Jensen; ⟨E⟩₀/A = 0.8398 on torus_2_0_2 as stated; cumulant sums 10.08, 1.82 reproduced).
- Covering relation P(lift x → lift y) = P(x → y)^m — CONFIRMED on (1,0),(0,2) under (2,0),(0,2), all 64 × 64
  pairs, 10⁻¹⁶ (`data/cover.txt`).
- NOT TESTED: the three "refuted inequalities" beyond the rows above (they rest on 18-cell and Monte Carlo rows).

## B. `image`: the seam identity

**The identity (★) — CONFIRMED.** The algebra is right, and I enumerated it on gump's own rule:
`python3 seam.py` (6 s). Vessel: one {111} layer (closed by T4) as the girth-one kagome tube (1,0),(0,4), 12 cells,
against its double cover (24 cells), deterministic B45/S345, soups of density 0.6, 0.5, 0.7, histories over 3, 4, 2
generations, every initial state of the torus and every completion of the cover. In the sharp form for K = 2,

    P_C(seam = s₀, rest = s₁, image of the seam = s₀) = P_T(s₀, s₁) · P_T(seam = s₀),

it holds for all 4,096 histories to 10⁻¹⁵, normalisation included, and no cover history with a recurring seam
falls off the torus's support (529–572 seam histories are shared by several strip histories, so the test is not
vacuous). With a seam ONE unit cell thick: 3,354 off-support histories, relative error 6.3. `chk_identity.py`
rerun: PASS (its fourth case, rule 30 with L = 4, has no seam class with more than one strip history and tests
nothing).

Answers to the three questions:
1. *Is a seam two steps thick a separator?* Yes, with the condition stated exactly: no rule factor (a cell and
   its neighbours at t, the cell at t+1) may hold cells on both sides of the seam, and no factor centred in the
   seam may touch both sides. With δ the largest reach of a neighbour offset along the tube, that is thickness
   ≥ 2δ, over all layers of the slab and all generations. The rest of the strip needs no thickness condition.
2. *Is a soup start at finite time enough for the living state?* The identity is exact at every finite t₁. Two
   steps are missing for "and so for the living state", both closable: (i) conditioning on "alive" is
   conditioning on the *strip* being alive at t₁, an event of the torus's whole history; for seam histories with
   a live cell at t₁ the factor P_C(C alive) cancels and (★) holds verbatim between the two living states, with
   Z replaced by P_T(alive at t₁); for seam histories dead at t₁ it does not, and the cover's dead histories
   enter. (ii) For a deterministic rule from a normalised soup Tr 𝒯^n = 1 for every n (the weights of all
   histories sum to 1), so 𝒯 has the single non-zero eigenvalue 1 and **Z = 1 exactly**; at finite t₁ bands
   further apart than the light cone are exactly independent. "The rate e^(−2.3|v|) is the gap of 𝒯" therefore
   has no meaning at finite t₁; it is a statement about the limit t₁ → ∞ taken inside the lifetime, which is not
   made. Label of that bullet: [conjectured].
3. *Does additivity follow?* No; it is assumed. Unwrapping one loop at a time gives the exact telescoping
   ρ_T − ρ_plane = (ρ_T − ρ_{C_v}) + (ρ_{C_v} − ρ_plane); "loops add" is the claim that closing v on a face that
   already has the loop w costs what it costs without w, which (★) does not give. Further: Q − 1 is not small for
   a whole seam history (it is a ratio of two exponentially small probabilities; only its effect on a local
   window is small), and when the unwrapped loop is the tube's short one the seam runs the tube's whole length, so
   "per cell, whatever the tube's length" needs Q to factorise along the seam (mixing of histories along the
   seam). Both are plausible for the living state and neither is proved; image's own first-order sum over
   neighbouring windows overshoots f by 2.9. **Correct statement: (★) is proved; "deficits add over loops to
   first order, per cell, independent of tube length" is [conjectured] (a first-order cluster ansatz on (★)),
   consistent with the measured density law.** It is about the living density only; it says nothing about
   lifetimes.

## How hard I tried, and what I did not do

- Tried to break: the identity of Theorem 2 on 10 shapes (holds to 10⁻¹⁴); its constant (own enumeration);
  Lemma 0 by exhaustive reachability; the bust shares by a different exact formulation and by simulation; the seam
  identity on gump's rule with a negative control. None broke.
- Not done: 18 cells and beyond; any Monte Carlo row of rigour's; `mc.c`, `qsd.c` read only for the definition of
  the marker; the 18-cell triangle's price map and tilt path; fair coins (½, ½); image's measurements (items 2–5 of
  its README: one torus, one stepper, not rerun); the seam identity on a slab of several layers or a tube of
  girth > 1 (2^24 torus states); a proof that the two-humped tilted law persists at large size.
