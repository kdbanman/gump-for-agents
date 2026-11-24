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

**What the surrogate is not** [measured by the referee, `research/blast/ref-dice/REVIEW.md`, 003cb73]: its private
coins are not gump's cells beneath. Taking gump's shared cells beneath as i.i.d. coins of the same densities, the
one-step law from the full hull face R = 3 differs from the surrogate's by total variation 0.33; and 12 of the 15
cells beneath that face lie on the hull's other faces, not in its interior. The surrogate is a model of the
mechanism (as `rigour/README.md` says), and the theorems here are about it, not about gump.

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
| patch 1×3 (9) | `patch13_lifetime`, `_tau` | [0.8474738060566295030, …031] | (1.8804189341, 1.8804189342) | 1.8804189341 | 111 s |
| torus (2,0),(0,2) (12) | `torus202_lifetime`, `_tau` (λ > 0): **generated, not built** (§4) | [0.9813486469939093, …113] (Python, exact at the 144 orbit rows) | (3.9818365882, 3.9818365883) | 3.9818365883 | > 20 min |

The headline, verbatim (`GumpMath/DiceHull3.lean`):

    theorem hull3_lifetime (t : ℕ) :
        (0.72 : ℚ) * 0.9165673655948901373 ^ t ≤ (hull 3).survival ρ1 ρ2 t (hull 3).full ∧
        ∀ x, (hull 3).survival ρ1 ρ2 t x ≤ 1384 * 0.9165673655948901374 ^ t
    theorem hull3_tau (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
        (0.9165673655948901373 : ℝ) ≤ lam ∧ lam ≤ 0.9165673655948901374 ∧
        2.4837157463 < -Real.log (1 - lam) ∧ -Real.log (1 - lam) < 2.4837157464

So h = 1 − λ ∈ [0.0834326344051098626, 0.0834326344051098627] (dense.py 8.3432634405110e-02, qsd.c
8.3432634405108e-02: the certificate agrees with dense.py to its last printed digit; it is qsd.c's last digit that
is 2 units off. Corrected 2026-11-24 after the referee; the first version of this note had it backwards). The certified interval for ln τ is [2.48371574633378442, 2.48371574633378443] (`dice_cert.py` prints it);
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

## 4. 12 cells: symmetry (`DiceSym.lean` proved; the 12-cell theorem file generated but not built)

*Clients of `DiceSym.lean`* (added 2026-11-24): none of my modules uses it (at a65957b, nor later: the 12-cell file
that would have was removed). Its only client is the chain agent's `GumpMath/LinkSym.lean` (`P_sym`, `alpha_sym`,
`act_bij`), through which `LinkTorus103Sym`/`LinkTorus113Sym` use it.

Row-by-row checking costs 2^(2A+1) node operations: 12 cells would take ~20 min per pass. A permutation σ of the
cells that preserves the tables (neighbour multisets, coins) preserves P (`P_sym`: P(σx, σy) = P(x, y), the
product reindexed), so for vectors invariant under σ the row at σx is the row at x (`mulVec_sym`), and the rows need
checking only at one state per orbit (`rows_of_reps`, `ineq_up_of_reps`). The group is all 48 table automorphisms of
the torus (2,0),(0,2), found by `dice_sym.py` (backtracking) and checked by the kernel (`symOK`, actions built
lazily as trees, `Tree.build`/`act`); 144 orbit representatives instead of 4,096 states. Orbit counts measured for
other faces: torus (1,1),(0,4): 128 automorphisms, 213 orbits; (1,0),(0,4): 16, 354; strip 2×2: 4, 1,104;
patch 2×2: 2, 2,112; 15-cell tori (1,0),(0,5): 20, 1,884 and (1,1),(0,5): 320, 888 (58M node operations per pass,
~35 min: beyond this machine's kernel budget per check).

**Status of the 12-cell theorem [not proved].** `python3 dice_sym.py torus 2 0 2` writes `GumpMath/DiceTorus202Data.lean`
and `DiceTorus202.lean` (certified λ ∈ [0.9813486469939093, 0.9813486469939113] at the orbit rows in exact Python
arithmetic; ln τ ∈ (3.9818365882, 3.9818365883), README 3.9818365883). In the kernel: with the 48 symmetry checks in
one declaration the build was killed at 12 GB of memory; split into one declaration per automorphism it ran for
more than 25 minutes (peak 5.5 GB) without finishing before my deadline, so the files are **not committed** (an
unbuilt file in `GumpMath/` would fail `check.sh`). Measured on the way: one automorphism's checks plus the 144-row
upper pass, 126 s. The cost is in `symOK`/`invOK` (48 × 4,096 states, each evaluating the lazily built action
tree); the next attempt should check invariance under a generating set (2–3 permutations) and carry the witness
as a chain of generators, which needs one more induction in `rows_of_reps`.

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
- No 12-cell face is certified in the kernel (§4: the symmetry machinery is proved, the 12-cell build did not finish
  in time). Memory is a real constraint here: the exit checks peak at 6.9 GB (`DiceTorus113Exit`, measured), and
  builds run in parallel by `lake` were killed by the machine's out-of-memory killer twice; build them one at a time.
- Not refereed. The statements were read against `rigour/README.md` by me only.

## 6. Checks run

- `sh research/blast/lean/check.sh --mathlib` (13:08–13:10 UTC, with every Dice module built): **all checks passed**,
  "mathlib package: 119 theorems, no sorry, no axiom beyond the standard three" (`AxiomsDice.lean` included).
- Build times, one module at a time on this shared machine: 9-cell face files 51–115 s each; `DiceHull3Exit` 338–402 s,
  `DiceTorus113Exit` 188–368 s (peak 6.9 GB); everything else under 20 s. A clean build of all Dice modules is about
  20 minutes; build them sequentially (`lake build GumpMath.DiceHull3`, then the next), not in parallel.
- `python3 research/blast/lean/statements.py` runs with `statements_dice.json` (123 statements); I did not commit the
  regenerated `STATEMENTS.md` (not my file).
- Not checked: no second agent has read these statements or tried to break the certificates; the tie of `Face.P`
  to `dense.py` samples 24 of 512 rows at 9 cells; `Face.regular` is not proved for the general torus.

## Reproduce

    cd research/blast/lean
    python3 dice_tie.py                      # the tie of Face.P to dense.py (PASS; --mutant must FAIL)
    python3 dice_cert.py hull 3              # certificate + theorem file; also torus 1 0 3, torus 1 1 3, strip 1 3, patch 1 3
    python3 dice_exit.py torus 1 1 3 6       # exits; also hull 3 6
    python3 dice_sym.py torus 2 0 2          # 12 cells with the symmetry reduction
    cd mathlib && lake build GumpMath.DiceHull3 && lake env lean AxiomsDice.lean
    sh research/blast/lean/check.sh --mathlib

## Second task (2026-11-24, 14:00–15:30 UTC): the exits as path statements, Theorem 1 on every hull face

All [proved], standard three axioms (`AxiomsDice.lean`), each module built alone.

1. **The bust share is the share of the death flux through a bust** (`GumpMath/DiceFlux.lean`). Paths are explicit:
   `pathE n f x` sums f over every list x = X₀, …, Xₙ of states with the product of its transition probabilities
   (`pathWeight`); `dies l` (the last state is empty, no earlier one), `bustLast K l` (a fall pop u ≥ pop v + ⌈A/2⌉
   among the last K transitions, the death included; `qsd.c`'s halffall marker). `pathE_succ` (one step of the
   Markov property, by `Fin.consEquiv`), `pathE_noBust` (P_x(T = K, no fall) = `noBust K x`), `pathE_window`
   (the window recursion), `death_flux` (P_μ(T = n+1) = λ^n (1 − λ)), and **`flux_share`**: for every QSD with
   0 < λ < 1, every K ≥ 1 and every generation m + K, P_μ(T = m+K, bust in the last K)/P_μ(T = m+K) =
   `bustShare K μ λ`. Hence `hull3_bust_flux` (∈ (0.017017, 0.017018)) and `torus113_bust_flux`
   (∈ (0.936852, 0.936853), λ > 0) are statements about the exits themselves. The prose step of §3 is gone. Not
   formed: the sum over all generations (each generation has the same ratio, so it is the same number).
2. **Theorem 1 on every hull face** (`DiceHull.lean`): `hull_cells` (every R, by orientation with `simp` + `omega`):
   every cell has two coins one layer in; the corners have none two layers in and at most two in-layer neighbours.
   A corner dies on both coins tails whatever its state (`corner_cell`). `survival_le_hull`: P_x(T > t) ≤
   (1 − δ₀^A)^t; `lntau_le_hull`: ln τ < 2.5095·A, every R, every QSD.
3. **The weighted bound with a rim** (`DiceBound3.lean`, `DiceHullAll.lean`). The weights cancel on any
   *balanced* face (every cell is in as many slots as it has neighbours); a live cell carries w^(deg − k).
   `hull_balanced` (every R: the hull's relation is symmetric with no repetitions, from `Gump.nbrs_symm` and the
   nodup lists), `hull_type` (every R: (degree, m1, m2) ∈ {(6,2,1), (4,2,1), (2,2,0)}), `type_check` (kernel).
   With the best single weight w = 1341/1000 (binding: an edge cell, live with 3 of 4 neighbours, against a dead
   one with 3) δ = 0.109 and **`lntau_le_hull_all`: ln τ < 2.2165·A for every hull face**, every R. (2.2160 is
   the optimum of a uniform weight over the three types [computed, `python3` scan of w in steps of 0.001]; a
   weight per type of cell would do better and is not tried.) `lntau_le_hull_small` is the earlier kernel-checked
   form for R ≤ 11.

**Not done.**
4. **`Face.regular` for every wrapped face** (`DiceTorusReg.lean`, done after all): `torus_regular H K D` for
   H, D > 0. In the cell coordinates (o, a, b) the reduction is Tr(a, b) = (a mod H, (b − ⌊a/H⌋K) mod D):
   invariant under the period lattice (`Tr_shift`), equal to the identity up to a lattice vector (`Tr_sub`), the
   identity on the fundamental domain (`Tr_id`); hence `red_symm` (the neighbour of i across v reduces to j iff the
   neighbour of j across −v reduces to i), `torus_count_symm` (v ↦ −v between the slots), six slots per cell
   (every reduction is a cell, `red_mem`), so in-degree six. **`lntau_le_torus`: ln τ < 1.9228·A on every wrapped
   face**, every QSD. (`DiceRegular.lean`'s per-face checks are now special cases.)
- The 12-cell torus: skipped, as the brief allowed (no build was attempted under the 4 GB rule).

Reproduce: `cd research/blast/lean/mathlib && lake build GumpMath.DiceFlux` (then DiceHull, DiceBound3,
DiceHullAll, one at a time; DiceBound3 about 2 minutes, the others under a minute), `lake env lean AxiomsDice.lean`.

## Repairs after the referee (2026-11-24, 15:05 UTC)

- `DiceLife.lean`'s header cites `qsd_survival` (P_μ(T > t) = λ^t, so τ = E_μ T = 1/(1 − λ)); it did not exist.
  It does now: `GumpMath/DiceMean.lean` takes over the referee's proof (`research/blast/ref-dice/QsdSurvival.lean`,
  credit to `ref-dice`): `qsd_survival`, `qsd_mean`, `qsd_mean_all`, `hull3_mean`, and `qsd_mean_hull` (every R).
  `DiceLife.lean` itself was not edited (its comment now names an existing theorem; editing it would rebuild every
  module downstream, the chain agent's `Link*` included).
- The h comparison in §3 was backwards (corrected there).
- `hull3_lifetime` pins the decay rate, with loose constants: the true sup of P_x(T > t)/λ^t is about 1.63 against
  the stated 1384 (referee). The bust shares (`hull3_bust`, `torus113_bust`, `flux_share` and its instances) are the
  stationary share of the death flux, deaths from the quasi-stationary law, not the share of all deaths from a fixed
  start: from the full hull face that share is about 0.152 (referee). The statement rows say so.
