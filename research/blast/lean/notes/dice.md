# The dice surrogate's lifetime, kernel-checked (Lean arm, agent `dice`, 2026-11-24)

The first theorems in the repository about a **lifetime**: the one-layer dice surrogate of `research/blast/rigour/`
defined in Lean as a killed finite Markov chain with rational transition probabilities, two-sided bounds on the
survival probability of small faces for every t, checked by Lean's kernel from certificates found outside it, the
corollary in ln τ to ten digits, both exits (bust and fade) proved at 9 cells, and Theorem 1 of `THEOREMS.md`
(ln τ < 2.5095·A) for every face with all its coins, at every size.

Every theorem below compiles with no `sorry` and depends only on `propext`, `Classical.choice`, `Quot.sound`
(`lake env lean AxiomsDice.lean` in `mathlib/`). Nothing uses `native_decide`; the certificates are evaluated by
`decide +kernel`. Labels: **[proved]** = kernel-checked theorem; **[measured]** = computed by a program, not proved.

## 1. The definition (`GumpMath/DiceDef.lean`) and what τ means

- `Face`: a list of cells (`Gump.Pt`), a body diagonal (`Gump.Diag`), a reduction `red` (identity on a free face,
  reduction modulo the period lattice on a wrapped one) and `coin : Pt → Bool` (which points beneath exist).
- Cell i at p: in-layer neighbours = `Gump.nbrs p` with d·q = d·p, mapped by `red`, kept if a cell of the face
  (`Face.nb`, with multiplicity); coins = neighbours at d·q = d·p − 2 (density ρ1) and d·p − 4 (ρ2) with `coin q`
  (`Face.m1`, `Face.m2`); alive next iff `Gump.rule s (k + heads)`; the probability is `aliveProb` (binomial sums).
- A state is x < 2^A with cell i alive iff bit i (the indexing of `dense.py`); `Face.P` is the product kernel on
  `Fin (2^A)`, `Face.survival t x = ((P^t) *ᵥ live) x` = P_x(T > t) (T = first empty generation; ∅ is absorbing,
  `Face.P_empty_row` for faces with all coins, and for the checked faces through their tables).
- Faces of `geom.py`, cell for cell in its order: `hull R`, `torus H K D`, `strip W D`, `patch W D`; ρ1 = 11/25,
  ρ2 = 21/50 (0.44, 0.42).
- **τ.** `rigour/README.md` defines τ := E_μ T = 1/h, h = 1 − λ, μ the quasi-stationary law (λ the dominant
  eigenvalue of the killed chain), and its ln τ = 2.4837157463 is −ln(1 − λ). `IsQSD F ρ1 ρ2 μ λ` (`DiceLife.lean`):
  μ a probability vector on the non-empty states with Σ_x μ(x) P(x,y) = λ μ(y) for y ≠ ∅. From such μ the death time
  is geometric, P_μ(T > t) = λ^t, so E_μ T = 1/(1 − λ); the theorems bound λ for **every** QSD and then −ln(1 − λ).
  Existence and uniqueness of the QSD (Lemma 0) are not proved in these files (the chain arm's `ChainLemma0.lean`
  proves an abstract Lemma 0; I did not depend on it, as briefed). On wrapped faces a QSD with λ = 0 exists (the
  point mass on the full face, which dies surely), so those theorems assume λ > 0.

**The tie to `dense.py`** [measured]: `python3 research/blast/lean/dice_tie.py` (90 s) has Lean `#eval` its own
`Face.P` and `Face.a` and compares with `dense.kernel` (floats) and an exact Fraction re-derivation, on 12 faces
(3, 6 and 9 cells: hull 1, 3; tori (1,0,1), (1,0,2), (1,1,2), (2,0,1), (1,0,3), (1,1,3); strips 1×2, 1×3; patches
1×2, 1×3): neighbour multisets and coin counts identical, every alive probability equal exactly, every entry of P
equal to dense.py to ≤ 7e-16 (all rows for ≤ 6 cells, 24 random rows of 512 for 9 cells), every row sum exactly 1.
`--mutant` (ρ1 = 12/25 in Lean) fails on every face. *What it does not cover:* rows not sampled at 9 cells; faces
not listed (the 12-cell torus is tied only through the certificate's own table check, which compares `geom.py`'s
graph with `Face.nb` exactly, and through its ln τ agreeing with README to 11 digits); the survival function and
matrix power are definitions on top of P and are not compared with anything.
In addition, every certificate's tables are checked by the kernel against the definition (`Data.tabOK`: neighbour
lists = `Face.nb`, coins = `Face.m1/m2`, alive numerators = `aliveNum`, which `aliveProb_eq` proves equal to
`aliveProb` · d1^m1 d2^m2), so the theorems are about `Face.P` itself, not about the Python tables.

## 2. The certificate (`DiceCert.lean`, `DiceLife.lean`)

A vector v > 0 with P v ≤ λ v entrywise gives P_x(T > t) ≤ (max v / min v) λ^t; a vector w ≥ 0 with P w ≥ μ w gives
P_x(T > t) ≥ (w(x)/max w) μ^t (`GumpMath/Certificate.lean`'s inductions). For a QSD, λ (μ·v) = μ·(Pv) gives
μ_lo ≤ λ ≤ λ_up (`qsd_bounds`, `qsd_up`, `qsd_lo_sure`). v is the right Perron vector rounded to integers
(`dice_cert.py`: numpy eigenvector refined by 400 exact power iterations in Python integers, 200 bits).

The kernel checks P v ≤ λ v row by row in exact integer arithmetic. The representation that makes it feasible:
**P is a product over cells, so (Pv)(x) = Σ_y Π_i f_i(y_i) v(y) is a contraction of v, stored as a binary tree, one
cell per level** (`Tree.eval`, 2^(A+1) multiplications per row instead of A·2^A; `Tree.eval_eq` proves it equal to
the sum). Measured kernel speed on this machine (4 cores shared with four agents): about 35 µs per tree node with
200-bit entries (5 µs with small numbers), so one pass over the 512 rows of a 9-cell face takes 18–25 s.

States that die surely (the full wrapped face) have r = 0; there v_up is set to 1 and the bound on survival carries
an extra term through the indicator of those states (`survival_up_sure`, one more row check P·1_D ≤ κ v).

## 3. Results [proved], with the numbers behind them

`dice_cert.py <face>` writes `GumpMath/Dice<Name>Data.lean` and `Dice<Name>.lean`; `lake build GumpMath.Dice<Name>`.

| face (A) | theorem | λ certified in | ln τ stated | README ln τ | build |
|---|---|---|---|---|---|
| hull R = 3 (9) | `hull3_lifetime`, `hull3_tau` | [0.9165673655948901373, …374] | (2.4837157463, 2.4837157464) | 2.4837157463 | 57 s |
| torus (1,0),(0,3) (9) | `torus103_lifetime`, `_tau` (λ > 0) | [0.9664099275695942426, …427] | (3.3935247190, 3.3935247191) | 3.3935247191 | 61 s |
| torus (1,1),(0,3) (9) | `torus113_lifetime`, `_tau` (λ > 0) | [0.9324323935928482210, …211] | (2.6946266059, 2.6946266060) | 2.6946266059 | 51 s |
| strip 1×3 (9) | `strip13_lifetime`, `_tau` | [0.9391216736592712685, …686] | (2.7988780569, 2.7988780570) | 2.7988780569 | 90 s |
| patch 1×3 (9) | `patch13_lifetime`, `_tau` | see file | see file | 1.8804189341 | 111 s |
| torus (2,0),(0,2) (12) | `torus202_lifetime`, `_tau` (λ > 0) | [0.9813486469939093, …113] | (3.9818365882, 3.9818365883) | 3.9818365883 | see §5 |

The headline, verbatim (`GumpMath/DiceHull3.lean`):

    theorem hull3_lifetime (t : ℕ) :
        (0.72 : ℚ) * 0.9165673655948901373 ^ t ≤ (hull 3).survival ρ1 ρ2 t (hull 3).full ∧
        ∀ x, (hull 3).survival ρ1 ρ2 t x ≤ 1384 * 0.9165673655948901374 ^ t
    theorem hull3_tau (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
        (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
        2.4837157463 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.4837157464

So h = 1 − λ ∈ [0.0834326344051098626, 0.0834326344051098627] (dense.py 8.3432634405110e-02, qsd.c
8.3432634405108e-02: the certificate agrees with qsd.c to its last digit and says dense.py's 13th digit is off by
2 units). The certified interval for ln τ is [2.48371574633378442, 2.48371574633378443] (`dice_cert.py` prints it);
the theorem states the 10-digit form the README quotes. The ln bound is proved from Taylor bounds on exp at a/k
(`DiceReal.lean`, `Real.exp_bound`), not from floating point.

**Theorem 1 at every size** (`DiceBound.lean`): for every face whose points beneath all carry coins (every wrapped
face and every strip, every size) and every 0 ≤ ρ1, ρ2 ≤ 1: `survival_le_all`: P_x(T > t) ≤ (1 − δ₀^A)^t,
δ₀ = min(ρ1²ρ2, (1−ρ1)²(1−ρ2)) (each cell dies on all-tails or on all-heads, `rule_k_or_k3`; the coin counts 2 and
1 come from T1, `Gump.layer_histogram`'s offsets); `qsd_le_all`: λ ≤ 1 − δ₀^A for every QSD; `lntau_le_all`:
ln τ < 2.5095·A at (0.44, 0.42). Says less than THEOREMS.md Theorem 1: the middle term E_μ[E] (Jensen) is not
formalised, and hull faces are not covered (their corners have two coins; true there too, not formalised for all R).

**A sharper Theorem 1 from a finite certificate that bounds an infinite family** (`DiceBound2.lean`). The question
"what inequality lets a finite face bound an infinite family" has, on the upper side, this answer: a *local*
inequality whose error terms cancel globally. Put a weight w = 152/125 on every slot between a live and a dead cell
(a live cell with k live neighbours carries w^(6−k), a dead one w^(−k)). On a regular face (six neighbour slots per
cell and each cell in six slots: every wrapped face) the live→dead and dead→live slots are equally many
(`up_sum_eq_down_sum`, from Σ_i k_i = 6·(live cells)), so the weights cancel in P(x, ∅) = Π_i d_i(x), and each
weighted factor is ≥ δ₁ = 0.1462 (`weighted_cell`, 14 cases decided by the kernel). Hence P(x, ∅) ≥ δ₁^A for every
state of every regular face of every size: `survival_le_regular`, and `lntau_le_regular`: **ln τ < 1.9228·A**
(against 2.5095·A; the brute-force maximum of E(x)/A on the tori of 9–12 cells is 1.52–1.82 [measured], so the
local certificate is within 6–25% of the worst state). Says less than "every wrapped face": `Face.regular` is a
hypothesis, checked by the kernel for the tori (1,0),(0,3), (1,1),(0,3), (2,0),(0,2); the general torus lemma
(six slots per cell, in-degree six, for every H, K, D) is not formalised. The lower side of the price (ln τ ≥ c·A,
B2) is not touched.

**Both exits at 9 cells** (`DiceExit.lean`, `DiceTorus113Exit.lean`, `DiceHull3Exit.lean`; `dice_exit.py`). The bust,
as `qsd.c` defines it (`halffall_share`): the last K = 6 transitions before the death (the death included) contain
a fall of at least ⌈A/2⌉ = 5 cells in one generation. `Face.noBust K x` = P_x(T = K and no such fall) (a recursion
through P), and `Face.bustShare K μ λ = 1 − μ·noBust K / (λ^(K−1)(1 − λ))`. Proved: for every QSD,

    0.936852 < (torus 1 1 3).bustShare ρ1 ρ2 6 μ lam < 0.936853   (λ > 0)     README claim 4: 0.9369
    0.017017 < (hull 3).bustShare ρ1 ρ2 6 μ lam < 0.017018                    README claim 4: 0.0170

so the wrapped face dies through the bust and the rimmed one through the fade, as theorems at this size. The
certificate: exact integer vectors D^k noBust k (k ≤ 6), checked by a masked contraction (`Tree.mask`), and a
**Poisson certificate** p, w with |noBust K − p d − (λ'w − Pw)| ≤ ε d, |w| ≤ ω d (d = P(·, ∅)), which gives
|μ·noBust K/μ·d − p| ≤ ε + |λ' − λ| ω for every QSD with no knowledge of μ (`poisson_bound`): this is how a
left-eigenvector quantity (a share of the QSD's death flux) is certified with right-vector checks only. ε = 1.7e-10
(torus), 2.4e-8 (hull), from a float solve; an exact refinement would tighten it. *Says less than claimed in one
respect:* that `bustShare` is the share of the death flux whose last 6 transitions contain the fall rests on the
stationarity of the window under the QSD (from μ, X_t given T > t is μ, so every death window starts from μ);
that argument is in the file header, in prose, not formalised.

## 4. 12 cells: symmetry (`DiceSym.lean`, `dice_sym.py`)

Row-by-row checking costs 2^(2A+1) node operations: 12 cells would take ~20 min per pass. A permutation σ of the
cells that preserves the tables (neighbour multisets, coins) preserves P (`P_sym`: P(σx, σy) = P(x, y), the
product reindexed), so for vectors invariant under σ the row at σx is the row at x (`mulVec_sym`), and the rows need
checking only at one state per orbit (`rows_of_reps`, `ineq_up_of_reps`). The group is all 48 table automorphisms of
the torus (2,0),(0,2), found by `dice_sym.py` (backtracking) and checked by the kernel (`symOK`, actions built
lazily as trees, `Tree.build`/`act`); 144 orbit representatives instead of 4,096 states. Orbit counts measured for
other faces: torus (1,1),(0,4): 128 automorphisms, 213 orbits; (1,0),(0,4): 16, 354; strip 2×2: 4, 1,104;
patch 2×2: 2, 2,112; 15-cell tori (1,0),(0,5): 20, 1,884 and (1,1),(0,5): 320, 888 (58M node operations per pass,
~35 min: beyond this machine's kernel budget per check).

## 5. What is not done, and the obstacle as a fact

- **15 and 18 cells.** Not certified. With the row method and the symmetry reduction, one pass over the 888 orbit
  representatives of the 15-cell torus (1,1),(0,5) is 58M tree nodes, about 35 minutes of kernel time at the
  measured 35 µs per node, three passes per face; the 18-cell faces are 64× larger. The way past it is the transfer
  (variable-elimination) product of `qsd.c`, A·2^(A+frontier) per pass (18 cells: ~300M operations, still hours in
  the kernel); its correctness proof (tensors over changing variable sets) is not written. Second tier
  (`native_decide`) was not used: `check.sh --mathlib` greps every `GumpMath/*.lean` for the word and runs every
  `Axioms*.lean` with the strict axiom filter, so a `*Native.lean` file in this package would fail the check as
  written.
- **The price per cell for an infinite family.** Only the upper side, Theorem 1 (2.5095 per cell, every size).
  A lower bound ln τ ≥ c·A for an infinite family is B2 of THEOREMS.md, open for every density; no finite
  certificate bounds it with what is here. What would bound an infinite family from a finite certificate: on the
  upper side a local inequality (a cluster decomposition of E = Σ_i ε_i with pair potentials, an LP over the star
  configurations of one cell), which would give max_x E(x)/A < 2.509 for all tori at once; it is not done.
- Lemma 0 (existence/uniqueness of the QSD) is not used: the λ theorems are "for every QSD", vacuous if none existed.
- The second 12-cell tori and the 12-cell strips are not certified (time, not an obstacle: §4 gives their costs).
- Not refereed. The statements were read against `rigour/README.md` by me only.

## Reproduce

    cd research/blast/lean
    python3 dice_tie.py                      # the tie of Face.P to dense.py (PASS; --mutant must FAIL)
    python3 dice_cert.py hull 3              # certificate + theorem file; also torus 1 0 3, torus 1 1 3, strip 1 3, patch 1 3
    python3 dice_exit.py torus 1 1 3 6       # exits; also hull 3 6
    python3 dice_sym.py torus 2 0 2          # 12 cells with the symmetry reduction
    cd mathlib && lake build GumpMath.DiceHull3 && lake env lean AxiomsDice.lean
    sh research/blast/lean/check.sh --mathlib
