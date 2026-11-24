# ref-dice: referee of the dice surrogate's lifetime theorems (Lean arm, agent `dice`, commit a65957b)

Referee `ref-dice`, 2026-11-24. Object: `research/blast/lean/mathlib/GumpMath/Dice*.lean`, `AxiomsDice.lean`,
`statements_dice.json`, `notes/dice.md` **as at a65957b** (the Dice files in the working tree were byte-identical to
it when I read them; the agent's later commits 9cde231, 333e171, 6f70d2d and the untracked `DiceBound3`, `DiceFlux`,
`DiceHull` were not refereed). Labels: **[proved]** by Lean's kernel or by me on paper; **[measured]** by a program
here; **[conjectured]**. Every script is in this directory; bulk output in `research/scratch/blast/ref-dice/`.

## Verdict

I could not break it. Every theorem says what its row says, and the five kernels are gump's rule on the face over
private coins entry for entry. Three points need care. The "ln τ" of the statements is −ln(1 − λ): that is the
source's own definition of τ, but the lemma cited for E_μT = 1/(1 − λ) does not exist. I have now proved it, in
`QsdSurvival.lean`. The bust share is the share of the death flux only through a prose step; I checked that step
on paper and to 10 digits numerically. The "surrogate"
is not gump over i.i.d. coins: with gump's own shared cells beneath, the one-step law differs by up to 0.33 in
total variation. The source says this; it is not a defect of the Lean.

| group | Lean statement vs its row and source | how checked |
|---|---|---|
| `Face.P`, `hull`, `torus`, `strip`, `patch` (DiceDef) | **the same** as the source's surrogate S(G) (private coins) | all 5 × 262,144 entries equal my kernel built from `oracle.py` alone, exactly; the alive table equal to one stepped by `oracle.step` [measured] |
| `*_lifetime` (5 faces) | **something different** from the row's "same fact": the decay rate λ to 19 digits with loose prefactors, not τ | constants re-derived; my λ to 25+ digits [measured] |
| `*_tau` (5 faces) | **the same** as README claim 3 (τ := 1/h), every QSD; λ > 0 assumed on the tori, as the rows say | λ by exact Collatz–Wielandt enclosure, width ≤ 2e-38 [proved by exact arithmetic, my code] |
| `hull3_bust`, `torus113_bust` | **the same** as `qsd.c halffall_share K=6`; "share of the death flux" is prose in Lean, true on paper | my recursion, an exact window propagation without μ, simulation [measured] |
| `survival_le_all`, `qsd_le_all`, `lntau_le_all` | **less** than THEOREMS.md Theorem 1, as the row says (no Jensen term, no hull faces) | hypotheses evaluated: true for tori, strips and patches, false on hulls |
| `survival_le_regular`, `lntau_le_regular` | **the same** as the row (beyond the source); `regular` proved for 3 tori only, as stated | `regular` true on 40 tori, false on strips, patches, hulls; δ₁ re-derived [measured] |
| `DiceSym` | sound, and **unused** at a65957b (no committed theorem depends on it) | read; checker evaluated on true and false symmetries |
| hygiene | clean | sweep over all 753 Dice constants: axioms ⊆ {propext, Classical.choice, Quot.sound} |

## Defects, ranked

1. **The lemma cited for τ = E_μT = 1/(1 − λ) does not exist.** `GumpMath/DiceLife.lean` line 10 (header) cites
   "P_μ(T > t) = λ ^ t (`qsd_survival`), so ln τ = −ln(1 − λ)". There is no `qsd_survival`: it is not among the 753
   constants of the 22 Dice modules (`dice_names.txt`, written by `DiceAxiomSweep.lean`; `grep qsd_survival` finds only
   the header). The τ theorems are therefore statements about −ln(1 − λ). That is exactly the source's τ := 1/h
   (`rigour/README.md` claim 3, THEOREMS.md Lemma 0), so the statements are honest. The sentence "τ = E_μ T = 1/(1 − λ)"
   in the docstrings of `hull3_tau` etc. is prose, not a theorem. **I proved it** [proved, kernel, standard axioms] in
   `QsdSurvival.lean`. `qsd_survival` gives Σ_x μ(x) P_x(T > t) = λ^t on every face whose ∅ row is absorbing.
   `qsd_mean` gives E_μT := Σ_t P_μ(T > t) = 1/(1 − λ). `qsd_mean_all` covers every face with all its coins, and
   `hull3_mean` covers hull 3 (∅ absorbing read off its checked tables by `P_sure`). With these the τ theorems say what
   their docstrings say. Fix: adopt these four theorems, or drop the citation. Matters: low to medium, because readers
   will take the docstring's "E_μ T" as kernel-checked.
2. **The bust share is the share of the death flux only through prose. The step is right.** `Face.bustShare K μ λ =
   1 − μ·noBust K / (λ^(K−1)(1 − λ))` (`DiceExit.lean` 42–45) is P_μ(a fall ≥ ⌈A/2⌉ in the K transitions | T = K).
   The header argues that this is the share of the death flux. On paper [proved, by me]: from μ, P_μ(X_t = y, T > t)
   = λ^t μ(y), so for every t ≥ 0 the window of a death at t + K has the law of the K transitions from μ given T = K.
   The share among deaths at T ≥ K is therefore exactly `bustShare`, and it is the same formula `qsd.c` prints
   (`1 - D / (pow(lam, K - 1) * h)`, `qsd.c` 301). Numerically, without μ (`window_exact.py`): propagate (state,
   generations since the last fall) from the full hull face or from state 73 of the torus (1,1),(0,3). The bust
   share of the deaths at generation t is 0.0170176867 (hull) and 0.9368529753 (torus) for every t ≥ 60, equal to
   my μ-based value to 10 digits. The same holds on the other three faces (`window_exact.out`). By simulation (`numerics.py FACE --sim N`), from μ, deaths with T ≥ 6:
   hull 0.01678 ± 0.00017 (seed 12345, 1e6 deaths) and 0.01720 ± 0.00012 (SEED=777, 2e6); torus (1,1),(0,3)
   0.93687 ± 0.00030. From the full hull face, deaths at T ≥ 40: 0.01566 ± 0.00063 and 0.01672 ± 0.00046. All lie
   within 2.2σ of 0.017018 / 0.936853. Note that it is *not* the share among all deaths from a fixed start: 0.0127
   from μ and 0.152 from the full hull face, because early deaths have truncated windows. The rows say "share of
   the death flux" and add the caveat; that is honest. Matters: low.
3. **A reversed sentence in `notes/dice.md` (lines 84–86 at a65957b).** "the certificate agrees with qsd.c to its last
   digit and says dense.py's 13th digit is off by 2 units". Wrong way round. h = 1 − λ = 0.08343263440510986264…
   (`numerics.py hull3`) prints as `8.3432634405110e-02`, which is dense.py's value. qsd.c's
   `8.3432634405108e-02` is the one 2 units off (power iteration at tol 2e-12). Matters: low (notes only).
4. **`hull3_lifetime`'s row overstates what it is.** The row reads "A different form of the same fact, stronger in
   one respect". The theorem pins the *decay rate* of P(T > t) to [0.9165673655948901373, …374]. It does not give τ
   = E_μT, and its prefactors are loose. The true sup over x and t ≤ 200 of P_x(T > t)/λ^t is 1.63 against 1384, and
   inf_t P_full(T > t)/λ^t = 1.00 against 0.72 (`numerics.py hull3`). So by itself it bounds E_full T only within a
   factor ≈ 1900. The constants are what the certificate gives: w(full)/w_max = 0.7264 and v_max/v_min = 1383.41
   (`constants_check.py`). The lower bound is from the full face (`(hull 3).full` = 511, by `rfl` in the proof; my
   dump prints `FULL 511`). Same pattern on the other faces: 3.07, 9.86, 512, 1731 against true sups 1.12, 1.45,
   1.63, 3.92. Matters: low (wording).
5. **The surrogate is gump over *private* coins.** It is not gump's face over coins on gump's own cells beneath.
   The DiceDef header says so ("gump's cells beneath, made private") and so does the source (README "The surrogate",
   the cube lemma), so this is not a Lean defect. A reader should know the size of the difference. On the R = 3
   hull face the 24 private coins stand for 15 distinct gump cells. 12 of those 15 lie on the octahedron's *other
   faces*, so in gump they are face cells, not interior (`shared.py`). Make the 15 cells i.i.d. coins of their layer's
   density and step `oracle.step` exactly over all 2^15 patterns. The one-step law then differs from `Face.P` by
   total variation 0.330 from the full face, 0.185 from x = 341 (5 live) and 0.194 from x = 22 (3 live). From x = 22
   the death probability is 0.0356 shared against 0.0174 private [measured, exact]. This bears on the owner's
   journal note "the isolation": the surrogate's coins are further from gump than "fresh coins on gump's cells".
6. **`DiceSym` has no client.** At a65957b the 12-cell files were removed, so `rows_of_reps`,
   `ineq_up_of_reps`/`ineq_lo_of_reps` and the `*_ineq` theorems of `DiceLife.lean` (347–508) are used by nothing. They
   are not in `AxiomsDice.lean`. The notes say the 12-cell theorem is "generated, not built". Honest, but the notes'
   §4 heading "DiceSym.lean proved" should not be read as a 12-cell result. Matters: none for correctness.

No defect found in: the certificate checkers, the five λ intervals, the ln bounds, the exits' intervals,
Theorem 1 and its sharpening, the definitions of `IsQSD`, `survival`, `full`, `hull`, `torus`, `strip`, `patch`.

## 1. Is `Face.P` the surrogate, and is the surrogate gump's face over coins

- **Own construction** (`myface.py`, from `reference/oracle.py`'s `offsets`, `BIRTH`, `SURVIVE` only). Face cells
  are built as sets of gump cells. Hull R: the cells with |x|+|y|+|z| ≤ R and x+y+z = R. That is the (1,1,1) face of
  the octahedron, which is the diagonal hull of docs/AUTOMATON.md T2 with C_d = R; such a cell has x, y, z ≥ 0
  automatically. Torus (H,K),(0,D): layer x+y+z = 1 modulo the lattice spanned by H·E1 + K·E2 and D·E2. Strip:
  modulo D·E2 only. Patch: no identification. Neighbours come from the 12 oracle offsets. In-layer neighbours that
  stand for no cell are dead. Coins are the neighbours at Δs = −2 (ρ1) and −4 (ρ2) that exist: on the hull, those
  inside the octahedron; elsewhere, all. Neighbours above are dead. Alive probabilities are B45/S345 over
  Bin(m1, ρ1) + Bin(m2, ρ2) in Fractions, and P(x, y) is the product over cells.
- **Every entry compared** (`compare_kernel.py DUMP --oracle`, output `compare_kernel.out`). Lean `#eval`s its own
  `Face.cells`, `Face.nb`, `Face.m1/m2`, `Face.a` (512 × 9) and **every entry of `Face.P` (512 × 512)**, via
  `LeanDump.lean.tmpl` and the dumps in scratch (7–9 min of Lean per face). Result for hull 3, torus (1,0),(0,3),
  torus (1,1),(0,3), strip 1×3 and patch 1×3: cells equal as sets, neighbour multisets and coins equal, **1,310,720
  entries of P compared, 0 mismatches**, every row sums to 1, ∅ absorbing, `full` = 511. Negative controls on hull 3:
  ρ1 = 12/25 in my kernel gives FAIL (106,971 mismatches); dropping one neighbour of cell 0 gives FAIL (54,880).
  [measured, exact]
- **One step through the oracle** (`oracle_alive.py`). For each of the 5 faces, each of the 512 states and each cell
  i, the face's layer goes on a real 24³ gump array, with periodic images on wrapped faces and dead rim elsewhere.
  Cell i's own existing beneath neighbours are set to each of their 2^m patterns, everything else is dead, and one
  `oracle.step` is run. The weighted alive probability equals `Face.a` at all 5 × 4,608 (state, cell) pairs.
  [measured, exact] So `Face.P` is gump's rule on the face with each cell's own cells beneath replaced by
  independent coins. That is the surrogate of README "The surrogate" and THEOREMS.md "The chain". Larger faces:
  Lean's `nb/m1/m2` equal mine on tori (2,1,3), (3,2,4), (1,3,5), strip 2×3, patch 3×2 and hulls R = 5, 7
  (`Regular.lean`, `nb_compare.py regular.out`: PASS).
- **Hull, as AUTOMATON.md defines it**: yes. Face cells = the octahedron's cells in its (1,1,1) face. "Exists" =
  inside the octahedron, so corners get coins (2,0) and the rest (2,1) (my build and Lean agree).
  `(hull 3).coin ⟨5,0,0⟩ = false`. By T2 the cells outside are dead forever in gump.
- **With gump's shared cells beneath**: different, see defect 5.

## 2. Numbers (`numerics.py FACE`, output `numerics.out`; `constants_check.py`)

Exact integer power iteration, from numpy's eigenvectors, 200 steps (700 for the patch, |λ₂/λ₁| = 0.927), then an
exact Collatz–Wielandt enclosure over the states with v > 0. The only states with v = 0 are the full wrapped faces,
which die surely (checked). λ to 25 digits; ln τ via `decimal` at 40 digits:

| face | λ (mine) | Lean interval | ln τ (mine) | bust share K=6 (mine) |
|---|---|---|---|---|
| hull 3 | 0.9165673655948901373589070 | […373, …374] ✓ | 2.48371574633378442986 | 0.0170176867 ∈ (0.017017, 0.017018) ✓ |
| torus (1,0),(0,3) | 0.9664099275695942426060723 | […426, …427] ✓ | 3.39352471905166397625 | 0.6465904363 |
| torus (1,1),(0,3) | 0.9324323935928482210249284 | […210, …211] ✓ | 2.69462660594438826266 | 0.9368529753 ∈ (0.936852, 0.936853) ✓ |
| strip 1×3 | 0.9391216736592712685176338 | […685, …686] ✓ | 2.79887805692471638801 | 0.0083587156 |
| patch 1×3 | 0.8474738060566295030494555 | […030, …031] ✓ | 1.88041893412125736745 | 0.0014056307 |

Each certificate's L/M brackets my λ with gaps of 7e-24 to 9e-23 (`constants_check.py`). Every stated ln τ interval
contains mine. The README's 10-digit values are the rounded ones. The constants (0.72, 1384; 0.96, 3.07; 0.71, 9.86;
0.97, 512; 0.99, 1731) are what the certificates give (defect 4). On the tori the lower bound starts from x₀ = 73,
the three cells of orientation x (Lean's cells 0, 3, 6 are x-odd), because the full face dies surely; the rows say so.

## 3. Statements against their rows

- **`IsQSD` is inhabited** on every face. On paper [proved; standard]: weak Perron–Frobenius gives the nonnegative
  matrix Q (P on non-empty states) a nonnegative left eigenvector for ρ(Q); put μ(∅) = 0 and normalise. On wrapped
  faces ρ(Q) > 0 (state 73 returns to itself with positive probability), so the hypothesis λ > 0 is met. Numerically:
  μ ≥ 0, sum 1, max |μQ − λμ| ≤ 3.5e-17 on all five faces (`numerics.out`). On the tori λ = 0 QSDs exist (δ_full).
  The theorems `torus103_tau`, `torus113_tau` and `torus113_bust` carry `(hlam : 0 < lam)` (`#check` in
  `axiom_sweep.out`), and their rows say "λ > 0". The hull, strip and patch theorems need no such hypothesis: their
  lower vectors are positive on every non-empty state.
- **`survival t x = (P^t *ᵥ live) x`** = P_x(X_t ≠ ∅) = P_x(T > t), since ∅ is absorbing. That is proved for faces
  with all coins (`P_empty_row`). It holds on every face anyway: m1 + m2 ≤ 3 by T1 and birth needs 4. Measured on
  all 5 dumps. **`full`** = 2^A − 1. **`Real.log`** has no junk value here: 1 − λ ∈ (0.03, 0.16) on every face, and
  `bustShare`'s denominator is pinned away from 0.
- **`lntau_le_all`'s hypothesis** `∀ q, F.coin q = true` holds by definition for every `torus`, `strip` and `patch`
  (`coin := fun _ => true`). It fails for every hull (`Regular.lean`). The row says "hull faces are not covered".
- **`Face.regular`**: Lean's own conjuncts are true on 9 tori up to 36 cells, false on strips, patches and hulls
  (`Regular.lean`). Mine are true on all 40 tori with 1 ≤ H, D ≤ 4, 0 ≤ K < D (`regular_check.py`). `weighted_cell`
  re-derived exactly: min over (k, s) of the weighted factor = 0.146203 ≥ 0.1462 at w = 152/125, and 1.216 is the
  best w on a 0.001 grid. So 1.9228 is the best constant of this one-parameter local certificate. Its gap to the
  worst state, max_x −ln P(x, ∅)/A = 1.579, 1.717, 1.519, 1.718, 1.819 on tori (1,0,3), (1,1,3), (2,0,2), (1,0,4),
  (1,1,4), confirms the notes' "1.52–1.82". [measured]
- **`DiceSym`** [read; sound]. `symOK` checks σ bijective on cells, G[σi] a permutation of σ(G[i]), C[σi] = C[i], and
  the tree I equal to σ's action on all 2^A states. Then `P_sym` (P(σx, σy) = P(x, y), product reindexed),
  `mulVec_sym` (rows of σ-invariant vectors) and `rows_of_reps` (each state is a listed symmetry's image of a marked
  representative) together prove that one state per orbit suffices. The listed maps need not form a group. On the
  hull-3 tables the checker accepts the rotation (x,y,z) → (y,z,x) and rejects a corner–edge swap and an
  edge–edge swap that is not an automorphism. The committed `Vup` is rotation-invariant (`Regular.lean`).
- **Rows.** Each row's difference from the source is honest, apart from defect 4's wording and the docstring
  citation of defect 1. All 13 row names and all 25 names of `AxiomsDice.lean` exist (`#check`s in
  `DiceAxiomSweep.lean`, no error).

## 4. The certificate checkers (`Perturb.lean`, output `perturb.out`)

Read: `Tree.eval_eq` (contraction = Σ_y Π sel · v(y)), `P_eq` (P = integer product / Dt, using `tabOK`'s
alive ≤ den), `rows_le`/`rows_lo`, `allRows_spec` (all of 0 … 2^A − 1), `vecOK_spec`, `sureOK_spec`, `nbRow_spec`,
`poisson_bound`, `share_interval`. A passing check implies (P v)(x) ≤ (L/M) v(x) (resp. ≥) at every state for the
vector in the file, with P the definition's `Face.P` [proved, kernel; I found no gap reading the statements].
Attacks on copies of the hull-3 data, all as expected:

| perturbation | checker result |
|---|---|
| none | tabOK, up, lo, vecOK: all true |
| λ_up lowered by 2e-22 (below λ) | `up` false, first failing row 1 |
| λ_lo raised by 2e-22 | `lo` false |
| v(300) lowered by 1 part in 10⁶ | false, at row 300 |
| v(300) raised by 1 part in 10⁶ | false, at row 204 (a predecessor of 300) |
| v(300) ± 1 unit (1e-60 relative) | **accepted**, correctly: still a valid certificate (row slack ≈ 1e-23 relative) |
| v(∅) set to 1 | `vecOK` false |
| one alive numerator +1 / one neighbour list changed / one coin count changed | `tabOK` false (all three) |
| kernel `decide +kernel` on the bad `tabOK`; `norm_num` on λ_up ≤ …373 | both fail to elaborate (the errors in `perturb.out` are the result) |

## 5. Hygiene

- `grep` over `GumpMath/Dice*.lean` and `AxiomsDice.lean`: no `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`,
  `implemented_by`, `opaque`, `extern`, `csimp`, `macro`, `elab`, `syntax`. Only `set_option maxRecDepth 100000`.
  The Data files contain only `def`s and comments.
- `DiceAxiomSweep.lean` (output `axiom_sweep.out`, names in `dice_names.txt`) covers all 753 constants (471 theorems,
  269 definitions) of the 22 Dice modules. The axiom sets seen are ∅, {propext}, {propext, Quot.sound} and
  {propext, Classical.choice, Quot.sound}: no `sorryAx`, no declared axiom, no opaque. The only "unsafe /
  implemented_by" constants are compiler artefacts: `*._unsafe_rec` of `Tree.get`, `Tree.eval`, `allRows`,
  `Tree.build`, `Tree.mask`, `Face.noBust`, and `Tree.ctorIdx._impl`, which Lean generates for every inductive type.
  No proof uses them, and `decide +kernel` reduces in the kernel.
- The oleans of the Dice modules are newer than their sources, and the sources equal a65957b (`git diff a65957b`
  empty for them). I did not rebuild anything (brief), so the kernel's acceptance of the 9-cell certificates is
  taken from the existing build plus `check.sh` as the notes report it. I did not re-run `check.sh`.

## Not checked

- No rebuild of any Dice module: the `decide +kernel` certificate checks were not re-run by me. My evidence that they
  hold is independent: my λ lie inside every certified interval, and the checkers reject perturbed certificates.
- Faces other than the five 9-cell ones: only their neighbour lists (7 larger faces). No 12-cell theorem exists at
  a65957b.
- I did not read the agent's Python (`dice_cert.py`, `dice_exit.py`, `dice_sym.py`, `dice_tie.py`) nor
  `geom.py`/`dense.py`/`qsd.c` beyond `qsd.c`'s bust prose and lines 236–310. My kernel was built without them. The
  agreement with the source's values runs through the README's numbers.
- The window-stationarity step of the bust share is a paper argument here, not proved in Lean. E_μT = 1/(1 − λ) is
  proved (`QsdSurvival.lean`) only for faces with all coins and for hull 3.
- The simulations are 1–2·10⁶ deaths: ±1e-4 on the hull share, ±3e-4 on the torus. The 6-digit intervals are
  confirmed by my exact recursion and window propagation (float64 for the latter), not by sampling.
- The agent's commits after a65957b (`torus_regular`, `lntau_le_torus`, the hull-weighted bound, `DiceFlux`).

## Reproduce (from this directory; Python one at a time, Lean one at a time)

    export PATH=$HOME/.elan/bin:$PATH; L=../lean/mathlib; S=../../scratch/blast/ref-dice
    for n in hull3 torus103 torus113 strip13 patch13; do               # 7-9 min of Lean each
      { cat LeanDump.lean.tmpl; echo "#eval dump \"$n\" (<face>)"; } > $S/Dump_$n.lean   # <face> = (hull 3) etc.
      (cd $L && lake env lean $PWD/$S/Dump_$n.lean) > $S/dump_$n.txt; done
    PYTHONPATH=../../../reference python3 compare_kernel.py $S/dump_hull3.txt --oracle   # PASS; --mutant must FAIL
    python3 numerics.py hull3 [--sim 1e6]; ITERS=700 python3 numerics.py patch13
    python3 window_exact.py hull3; python3 window_exact.py torus113
    PYTHONPATH=../../../reference python3 shared.py
    python3 regular_check.py; python3 constants_check.py
    (cd $L && lake env lean $OLDPWD/DiceAxiomSweep.lean)   # also Perturb.lean (2 expected errors), Regular.lean,
                                                           # QsdSurvival.lean (E_mu T = 1/(1-lambda), ~1 min)
    python3 nb_compare.py regular.out

## Second review (2026-11-24, 15:40–16:20 UTC): the dice commits after a65957b, up to 6f70d2d

Object: `DiceFlux.lean`, `DiceHull.lean`, `DiceBound3.lean`, `DiceHullAll.lean`, `DiceRegular.lean`,
`DiceTorusReg.lean`, `AxiomsDice.lean`, the rows of `statements_dice.json` and the dated "Second task" section of
`notes/dice.md`, all as at 6f70d2d (the six modules were byte-identical in the working tree and their oleans newer;
nothing rebuilt). Not refereed: the Link* modules (another arm), and `DiceMean.lean` and the row edits made in the
working tree after 6f70d2d.

**Verdict: no defect in the statements.** `flux_share` makes defect 2 above a theorem. `torus_regular`,
`hull_type` and `hull_balanced` are what my oracle-built faces show. The three new bounds are true, with room.

1. **`DiceFlux.lean`.**
   - Read: `pathE n f x` = Σ over every ω : Fin n → states of `pathWeight (x :: ω)` · f(x :: ω), where
     `pathWeight` is the product of P over consecutive pairs. That is E_x[f(X₀..Xₙ)].
   - `dies` means "last state ∅, no earlier one", i.e. T = n exactly.
   - `bustLast K` means "a fall pop u ≥ pop v + ⌈A/2⌉ among the last K transitions, the death included". That is
     `qsd.c`'s marker (m − n' ≥ half, half = (A+1)/2) as I read it in the first review.
   - `flux_share` holds for every QSD with 0 < λ < 1, every K ≥ 1 and every generation m + K: P_μ(T = m+K, bust in
     the last K) / P_μ(T = m+K) = `bustShare`. `death_flux` gives P_μ(T = n+1) = λⁿ(1 − λ).
   - Checked: Lean's own `pathE` with `dies` and with `dies ∧ bustLast`, on `hull 1` and `torus 1 1 1`, n = 3 and 4,
     K = 2 and 3, every start. It equals an exact Python enumeration of all paths: 24 cases, 0 mismatches, bust mass
     non-zero (`Review2.lean`, `review2_paths.py review2.out`) [measured, exact].
   - My window propagation **started from μ** (`review2.py e`, `review2_de.out`) gives bust share 0.0170176867
     (hull 3) and 0.9368529753 (torus (1,1),(0,3)) at every generation t = 6 … 12. It also gives
     P_μ(T = t)/(λ^(t−1)(1 − λ)) = 1.000000000000. At t < 6 the share is smaller (truncated windows), which is why
     the theorem needs m + K [measured, float64].
   - So `hull3_bust_flux` and `torus113_bust_flux` are theorems about the exits. My defect 2 is closed. The sum over
     all generations ≥ K is not formed; that is trivial, since every term has the same ratio.
2. **`DiceTorusReg.lean`.**
   - Read: `Tr` reduces modulo the lattice (Int ediv/emod with H, D > 0). `Tr_shift`, `Tr_sub`, `Tr_id` and the
     decided `offsets_table` give `red_symm`, then `torus_count_symm`, `red_mem` and six slots. That proves
     `torus_regular` for every H, D > 0 and every K, including K ≥ D. `lntau_le_torus` is `lntau_le_regular`
     applied to it. Its hypothesis `hA : 0 < A` is redundant (A = 3HD).
   - Thin and skewed tori I had not tried: (1,1),(0,1), (1,5),(0,1), (2,1),(0,1), (3,2),(0,1), (1,3),(0,2),
     (1,5),(0,2), (2,3),(0,2), (5,3),(0,2), (1,7),(0,3), (4,6),(0,5). On these, cells are their own neighbours
     (6 self-slots at H = D = 1, 4 at A = 6) and slots repeat (multiplicity 2). Lean's `Face.nb`, `m1`, `m2` equal
     mine on all ten, and Lean's three `regular` conjuncts evaluate true on all ten (`Review2.lean`,
     `nb_compare.py review2.out`). Mine are regular on 16 such tori (`review2.py c`).
   - **The constant**: ln τ/A on every torus with A ≤ 12 that I can diagonalise is 0.299 to 0.471 (`review2.py d`),
     so 1.9228 lies 4.1 to 6.4 times above the truth: 4.1× at 3 cells, 5.1–6.4× at 9, 5.6–6.2× at 12. It is close to
     the worst single state, max_x −ln P(x, ∅)/A = 1.52–1.82, which is what a one-step bound can reach.
3. **`DiceHull.lean`, `DiceBound3.lean`, `DiceHullAll.lean`.**
   - My oracle-built hulls R = 1, 3, …, 15 (`review2.py a`) show exactly the types (degree, m1, m2) = (6,2,1)
     inside, (4,2,1) on the edges and (2,2,0) at the three corners. The counts are 3 corners, 6(R−1)/2 edge cells
     and the rest inside; R = 1 has only corners.
   - Every neighbour relation is symmetric with no repeated neighbour, so in-degree = out-degree. That is
     `balanced`, and it is exactly what the weighted cancellation Σ bup = Σ bdown needs: in-degree equal to degree
     cell by cell. The wrapped faces' "six" is a special case.
   - Weighted check re-derived exactly: at w = 1341/1000 the minimum weighted factor over the three types is
     0.109039 ≥ 0.109, giving 2.2160·A, or 2.2165 with δ rounded to 0.109. 1.341 is the best uniform w on a 0.001
     grid, as the notes say. `hull_cells` / `corner_cell` (corners die on two tails, (1 − ρ1)² ≥ δ₀) is consistent
     with my tables.
   - **With room on the 9-cell triangle**: ln τ = 2.4837 against 2.2165·9 = 19.95 (8.0×) and 2.5095·9 = 22.6. For
     R = 5: 4.2317 (README) against 39.9. The per-state quantity the bound controls, max_x −ln P(x, ∅)/A, is 1.745
     on hull 3 against 2.2165.
   - One stale sentence: `DiceBound3.lean`'s header (lines 11–13) still says the classification "is not proved for
     every R". `DiceHullAll.hull_type` now proves it. Docstring only.
4. **Hygiene, rows, names.**
   - `DiceAxiomSweep2.lean` (`axiom_sweep2.out`, `dice_names2.txt`) covers all 1,808 constants (1,470 theorems)
     of the 28 Dice modules at 6f70d2d. The axiom sets are ⊆ {propext, Classical.choice, Quot.sound}: no sorryAx,
     no declared axiom, no opaque. The only flags are compiler artefacts (`_unsafe_rec` of `pathWeight`, `dies`,
     `noFallAll`, `Nm`, `Dm` and the earlier ones; `Tree.ctorIdx._impl`).
   - All 16 new `AxiomsDice.lean` names exist (`#check`, no error).
   - The 6f70d2d rows for `flux_share`, `death_flux`, the two `*_bust_flux`, `lntau_le_hull`, `lntau_le_hull_all`,
     `torus_regular` and `lntau_le_torus` say what the theorems say.
   - Aside, on the working tree after 6f70d2d (not refereed): the `torus113_bust_flux` row repeats "from the full
     hull face it is about 0.152". That number is the hull's. On that torus the full face dies surely; from x₀ = 73
     the share of all deaths is 0.934 (`window_exact.out`).

Not checked in this round: no rebuild, so the kernel checks (`offsets_table`, `type_check`, `hull*_wcheck`,
`regular_torus*`) are taken from the existing oleans. I did not run 12-cell or larger exact diagonalisations
beyond A = 12. The proofs of `deg_X/Y/Z` and `m2_X/Y/Z` were read only through their statements; my hull tables
for R ≤ 15 are the independent check.

Reproduce: `python3 review2.py` (a–e; about 3 min); `(cd ../lean/mathlib && lake env lean $PWD/Review2.lean) >
review2.out`, then `python3 review2_paths.py review2.out` and `python3 nb_compare.py review2.out`;
`lake env lean .../DiceAxiomSweep2.lean`.
