/-
Symmetry reduction for the certificates: a permutation σ of the cells that preserves the face's tables
(neighbour multisets and coins) preserves the transition matrix, P(σx, σy) = P(x, y), so for a vector
invariant under σ the row (P v)(x) is the row at σx. A row check then needs to run only on one state of
each orbit of a group of such permutations (`rows_of_reps`): this is what brings 12-cell faces within the
kernel's reach (144 rows instead of 4,096 on the torus (2,0),(0,2), whose table group has 48 elements).

σ is given as a list (σ i = σ[i]) and its action on states as a tree `I` (I(x) = σx, the state with bit σ i
equal to bit i of x); `symOK` checks both against the tables.
-/
import GumpMath.DiceCert

namespace Gump.Dice
open Gump Finset Matrix

/-- A tree of depth n holding f(b + y) at index y (built lazily by the kernel; nothing about it is assumed:
`symOK` checks the entries it uses). -/
def Tree.build : ℕ → (ℕ → ℕ) → ℕ → Tree
  | 0, f, b => .leaf (f b)
  | n + 1, f, b => .node (Tree.build n f b) (Tree.build n f (b + 2 ^ n))

/-- The action of a cell permutation σ on a state x: bit σ i of the result is bit i of x. -/
def act (σ : List ℕ) (x : ℕ) : ℕ :=
  ((List.range σ.length).filter fun i => x.testBit i).foldl (fun acc i => acc + 2 ^ σ.getD i 0) 0

theorem getD_of_lt {α : Type*} (l : List α) (d : α) (i : ℕ) (h : i < l.length) : l.getD i d = l[i] := by
  rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem h]; rfl

namespace Data
variable (c : Data) (F : Face)

/-- The checks that (σ, I) is a symmetry of the tables, for a face of A cells. -/
def symOK (A : ℕ) (σ : List ℕ) (I : Tree) : Bool :=
  σ.length == A && σ.Nodup && σ.all (· < A) &&
  ((List.range A).all fun i =>
    (c.G.getD i []).all (· < A) &&
    (c.G.getD (σ.getD i 0) []).isPerm ((c.G.getD i []).map (σ.getD · 0)) &&
    c.C.getD (σ.getD i 0) (0, 0) == c.C.getD i (0, 0)) &&
  allRows (fun x => decide (I.get A x < 2 ^ A) &&
    (List.range A).all fun i => (I.get A x).testBit (σ.getD i 0) == x.testBit i) (2 ^ A)

/-- A vector invariant under the action I. -/
def invOK (A : ℕ) (I V : Tree) : Bool := allRows (fun y => V.get A (I.get A y) == V.get A y) (2 ^ A)

section
variable {A : ℕ} {σ : List ℕ} {I : Tree} (h : c.symOK A σ I = true)
include h

theorem symOK_spec : σ.length = A ∧ σ.Nodup ∧ (∀ i < A, σ.getD i 0 < A) ∧
    (∀ i < A, (∀ j ∈ c.G.getD i [], j < A) ∧
      (c.G.getD (σ.getD i 0) []).Perm ((c.G.getD i []).map (σ.getD · 0)) ∧
      c.C.getD (σ.getD i 0) (0, 0) = c.C.getD i (0, 0)) ∧
    (∀ x < 2 ^ A, I.get A x < 2 ^ A ∧ ∀ i < A, (I.get A x).testBit (σ.getD i 0) = x.testBit i) := by
  simp only [symOK, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, List.mem_range, decide_eq_true_eq,
    List.isPerm_iff] at h
  obtain ⟨⟨⟨⟨hl, hn⟩, hlt⟩, hg⟩, hr⟩ := h
  refine ⟨hl, by simpa using hn, fun i hi => ?_, fun i hi => ?_, fun x hx => ?_⟩
  · rw [getD_of_lt _ _ _ (by omega)]; exact hlt _ (List.getElem_mem _)
  · obtain ⟨⟨a, b⟩, d⟩ := hg i hi; exact ⟨a, b, d⟩
  · have := allRows_spec _ _ hr x hx
    simp only [Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range, beq_iff_eq] at this
    exact this

/-- σ as a function is a bijection of the cells. -/
theorem sym_inj : ∀ i < A, ∀ j < A, σ.getD i 0 = σ.getD j 0 → i = j := by
  obtain ⟨hl, hn, -, -, -⟩ := c.symOK_spec h
  intro i hi j hj e
  rw [getD_of_lt _ _ _ (by omega), getD_of_lt _ _ _ (by omega)] at e
  exact (List.Nodup.getElem_inj_iff hn).mp e

theorem sym_surj : ∀ k < A, ∃ i < A, σ.getD i 0 = k := by
  obtain ⟨hl, hn, hlt, -, -⟩ := c.symOK_spec h
  intro k hk
  have hsub : (range A).image (fun i => σ.getD i 0) = range A := by
    apply Finset.eq_of_subset_of_card_le
    · intro y hy; simp only [mem_image, mem_range] at hy; obtain ⟨i, hi, rfl⟩ := hy; exact mem_range.mpr (hlt i hi)
    · rw [card_image_of_injOn (fun i hi j hj e => c.sym_inj h i (mem_range.mp hi) j (mem_range.mp hj) e)]
  have : k ∈ (range A).image (fun i => σ.getD i 0) := by rw [hsub]; exact mem_range.mpr hk
  simp only [mem_image, mem_range] at this
  exact this

end

/-- The tables are invariant: σ preserves the alive numerators and the denominators. -/
theorem alpha_sym (htab : c.tabOK F = true) {σ : List ℕ} {I : Tree} (h : c.symOK F.A σ I = true)
    (x : ℕ) (hx : x < 2 ^ F.A) (i : ℕ) (hi : i < F.A) :
    c.alpha (I.get F.A x) (σ.getD i 0) = c.alpha x i ∧ c.den (σ.getD i 0) = c.den i := by
  obtain ⟨-, -, hlt, hg, hI⟩ := c.symOK_spec h
  obtain ⟨hGa, hP, hC⟩ := hg i hi
  obtain ⟨-, -, -, -, ht⟩ := c.tabOK_spec F htab
  have hσi := hlt i hi
  obtain ⟨hG1, hC1, hT1, -⟩ := ht _ hσi
  obtain ⟨hG2, hC2, hT2, -⟩ := ht _ hi
  have hlen : (c.G.getD (σ.getD i 0) []).length = (c.G.getD i []).length := by rw [hP.length_eq, List.length_map]
  have hm : (F.m1 (σ.getD i 0), F.m2 (σ.getD i 0)) = (F.m1 i, F.m2 i) := by rw [← hC1, ← hC2, hC]
  have hT : c.T.getD (σ.getD i 0) [] = c.T.getD i [] := by
    rw [hT1, hT2, hlen, (Prod.mk.inj hm).1, (Prod.mk.inj hm).2]
  have hk : c.kk (I.get F.A x) (σ.getD i 0) = c.kk x i := by
    unfold kk
    rw [hP.countP_eq, List.countP_map]
    refine List.countP_congr fun j hj => ?_
    simp only [Function.comp, (hI x hx).2 j (hGa j hj)]
  refine ⟨?_, ?_⟩
  · unfold alpha; rw [hT, hk, (hI x hx).2 i hi]
  · unfold den; rw [hC]

/-- **P is invariant**: P(σx, σy) = P(x, y). -/
theorem P_sym (htab : c.tabOK F = true) {σ : List ℕ} {I : Tree} (h : c.symOK F.A σ I = true)
    (x y : Fin (2 ^ F.A)) (hx' : I.get F.A x < 2 ^ F.A) (hy' : I.get F.A y < 2 ^ F.A) :
    F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) ⟨I.get F.A x, hx'⟩ ⟨I.get F.A y, hy'⟩ =
      F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x y := by
  obtain ⟨-, -, hlt, -, hI⟩ := c.symOK_spec h
  rw [c.P_eq F htab, c.P_eq F htab]
  congr 2
  symm
  refine Finset.prod_nbij (fun i => σ.getD i 0) (fun i hi => mem_range.mpr (hlt i (mem_range.mp hi)))
    (fun i hi j hj e => c.sym_inj h i (mem_range.mp hi) j (mem_range.mp hj) e)
    (fun k hk => by
      obtain ⟨i, hi, e⟩ := c.sym_surj h k (mem_range.mp hk)
      exact ⟨i, mem_range.mpr hi, e⟩) (fun i hi => ?_)
  have hi' := mem_range.mp hi
  obtain ⟨ha, hd⟩ := c.alpha_sym F htab h x x.isLt i hi'
  simp only [Tree.sel, fac, ha, hd, (hI y y.isLt).2 i hi']

/-- The action on states is a bijection of Fin (2 ^ A). -/
theorem act_bij (htab : c.tabOK F = true) {σ : List ℕ} {I : Tree} (h : c.symOK F.A σ I = true) :
    Function.Bijective (fun y : Fin (2 ^ F.A) => (⟨I.get F.A y, ((c.symOK_spec h).2.2.2.2 y y.isLt).1⟩ :
      Fin (2 ^ F.A))) := by
  obtain ⟨-, -, -, -, hI⟩ := c.symOK_spec h
  refine (Finite.injective_iff_bijective).mp ?_
  intro y y' e
  simp only [Fin.mk.injEq] at e
  apply Fin.ext
  apply Nat.eq_of_testBit_eq
  intro j
  by_cases hj : j < F.A
  · rw [← (hI y y.isLt).2 j hj, ← (hI y' y'.isLt).2 j hj, e]
  · rw [Nat.testBit_lt_two_pow (lt_of_lt_of_le y.isLt (Nat.pow_le_pow_right (by norm_num) (by omega))),
      Nat.testBit_lt_two_pow (lt_of_lt_of_le y'.isLt (Nat.pow_le_pow_right (by norm_num) (by omega)))]

/-- **Rows of an invariant vector are invariant**: (P u)(σx) = (P u)(x). -/
theorem mulVec_sym (htab : c.tabOK F = true) {σ : List ℕ} {I : Tree} (h : c.symOK F.A σ I = true)
    (U : Tree) (hU : invOK F.A I U = true) (x : Fin (2 ^ F.A)) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) ⟨I.get F.A x, ((c.symOK_spec h).2.2.2.2 x x.isLt).1⟩ =
      (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x := by
  have hb := c.act_bij F htab h
  simp only [mulVec, dotProduct]
  rw [← Function.Bijective.sum_comp hb]
  refine sum_congr rfl fun y _ => ?_
  rw [c.P_sym F htab h x y]
  congr 1
  simp only [vec]
  have := allRows_spec _ _ hU y y.isLt
  simp only [beq_iff_eq] at this
  rw [this]

/-- **Row inequalities from the representatives of the orbits.** `gens` is a list of symmetries (σ, I) of the
tables under which U and W are invariant; every state x is σx' for the symmetry `gens[Wg x]` and the
representative x' = `Wr x`, which is marked in `Rm`; the inequality holds at every marked state. Then it holds at
every state. (Here for the upper form; the lower form is `rows_of_reps_ge`.) -/
def repsOK (A : ℕ) (gens : List (List ℕ × Tree)) (Wg Wr Rm : Tree) : Bool :=
  allRows (fun x => Rm.get A (Wr.get A x) == 1 && decide (Wr.get A x < 2 ^ A) && decide (Wg.get A x < gens.length) &&
    ((gens.getD (Wg.get A x) ([], .leaf 0)).2.get A (Wr.get A x) == x)) (2 ^ A)

theorem rows_of_reps (htab : c.tabOK F = true) (gens : List (List ℕ × Tree)) (Wg Wr Rm : Tree)
    (hg : ∀ g ∈ gens, c.symOK F.A g.1 g.2 = true) (U W : Tree)
    (hU : ∀ g ∈ gens, invOK F.A g.2 U = true) (hW : ∀ g ∈ gens, invOK F.A g.2 W = true)
    (hr : repsOK F.A gens Wg Wr Rm = true) (R : ℚ → ℚ → Prop)
    (hrow : ∀ x : Fin (2 ^ F.A), Rm.get F.A x = 1 →
      R ((F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x) (vec W F.A x))
    (x : Fin (2 ^ F.A)) :
    R ((F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x) (vec W F.A x) := by
  have hx := allRows_spec _ _ hr x x.isLt
  simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at hx
  obtain ⟨⟨⟨hm, hlt⟩, hglt⟩, himg⟩ := hx
  set g := gens.getD (Wg.get F.A x) ([], .leaf 0)
  have hgm : g ∈ gens := by
    simp only [g]; rw [getD_of_lt _ _ _ hglt]; exact List.getElem_mem _
  have hs := hg g hgm
  set r : Fin (2 ^ F.A) := ⟨Wr.get F.A x, hlt⟩
  have hrx : (⟨g.2.get F.A r, ((c.symOK_spec hs).2.2.2.2 r r.isLt).1⟩ : Fin (2 ^ F.A)) = x := Fin.ext himg
  have key := hrow r hm
  rw [← c.mulVec_sym F htab hs U (hU g hgm) r] at key
  have hWr : vec W F.A ⟨g.2.get F.A r, ((c.symOK_spec hs).2.2.2.2 r r.isLt).1⟩ = vec W F.A r := by
    simp only [vec]
    have := allRows_spec _ _ (hW g hgm) r r.isLt
    simp only [beq_iff_eq] at this
    rw [this]
  rw [← hWr, hrx] at key
  exact key

/-- One row of the two-vector check. -/
theorem row_le_at (htab : c.tabOK F = true) (U W : Tree) (L M : ℕ) (hM : 0 < M) (x : Fin (2 ^ F.A))
    (hx : c.rowLe F.A (c.Dt F.A) L M U W x = true) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x ≤ ((L : ℚ) / M) * vec W F.A x := by
  simp only [rowLe, decide_eq_true_eq] at hx
  rw [c.mulVec_eq F htab, vec]
  have hD : (0 : ℚ) < c.Dt F.A := by
    rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F htab i
  have hM' : (0 : ℚ) < M := by exact_mod_cast hM
  have hx' : (M : ℚ) * U.eval F.A (c.fac x) ≤ L * c.Dt F.A * W.get F.A x := by exact_mod_cast hx
  rw [div_le_iff₀ hD, div_mul_eq_mul_div, div_mul_eq_mul_div, le_div_iff₀ hM']
  nlinarith

/-- One row of the lower check. -/
theorem row_lo_at (htab : c.tabOK F = true) (V : Tree) (L M : ℕ) (hM : 0 < M) (x : Fin (2 ^ F.A))
    (hx : c.rowLo F.A (c.Dt F.A) L M V x = true) :
    ((L : ℚ) / M) * vec V F.A x ≤ (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec V F.A) x := by
  simp only [rowLo, decide_eq_true_eq] at hx
  rw [c.mulVec_eq F htab, vec]
  have hD : (0 : ℚ) < c.Dt F.A := by
    rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F htab i
  have hM' : (0 : ℚ) < M := by exact_mod_cast hM
  have hx' : (L : ℚ) * c.Dt F.A * V.get F.A x ≤ M * V.eval F.A (c.fac x) := by exact_mod_cast hx
  rw [le_div_iff₀ hD, div_mul_eq_mul_div, div_mul_eq_mul_div, div_le_iff₀ hM']
  nlinarith

/-- A row check run only on the marked states. -/
def marked (A : ℕ) (Rm : Tree) (row : ℕ → Bool) : Bool := allRows (fun x => Rm.get A x != 1 || row x) (2 ^ A)

theorem marked_spec (A : ℕ) (Rm : Tree) (row : ℕ → Bool) (h : marked A Rm row = true) (x : ℕ) (hx : x < 2 ^ A)
    (hm : Rm.get A x = 1) : row x = true := by
  have := allRows_spec _ _ h x hx
  simp only [Bool.or_eq_true, bne_iff_ne, ne_eq, hm, not_true_eq_false, false_or] at this
  exact this

/-- **Upper rows from the orbit representatives.** -/
theorem ineq_up_of_reps (htab : c.tabOK F = true) (gens : List (List ℕ × Tree)) (Wg Wr Rm : Tree)
    (hg : ∀ g ∈ gens, c.symOK F.A g.1 g.2 = true) (U W : Tree)
    (hU : ∀ g ∈ gens, invOK F.A g.2 U = true) (hW : ∀ g ∈ gens, invOK F.A g.2 W = true)
    (hr : repsOK F.A gens Wg Wr Rm = true) (L M : ℕ) (hM : 0 < M)
    (hrows : marked F.A Rm (c.rowLe F.A (c.Dt F.A) L M U W) = true) (x : Fin (2 ^ F.A)) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x ≤ ((L : ℚ) / M) * vec W F.A x :=
  c.rows_of_reps F htab gens Wg Wr Rm hg U W hU hW hr (fun a b => a ≤ ((L : ℚ) / M) * b)
    (fun y hy => c.row_le_at F htab U W L M hM y (marked_spec _ _ _ hrows y y.isLt hy)) x

/-- **Lower rows from the orbit representatives.** -/
theorem ineq_lo_of_reps (htab : c.tabOK F = true) (gens : List (List ℕ × Tree)) (Wg Wr Rm : Tree)
    (hg : ∀ g ∈ gens, c.symOK F.A g.1 g.2 = true) (V : Tree)
    (hV : ∀ g ∈ gens, invOK F.A g.2 V = true)
    (hr : repsOK F.A gens Wg Wr Rm = true) (L M : ℕ) (hM : 0 < M)
    (hrows : marked F.A Rm (c.rowLo F.A (c.Dt F.A) L M V) = true) (x : Fin (2 ^ F.A)) :
    ((L : ℚ) / M) * vec V F.A x ≤ (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec V F.A) x :=
  c.rows_of_reps F htab gens Wg Wr Rm hg V V hV hV hr (fun a b => ((L : ℚ) / M) * b ≤ a)
    (fun y hy => c.row_lo_at F htab V L M hM y (marked_spec _ _ _ hrows y y.isLt hy)) x

end Data

end Gump.Dice
