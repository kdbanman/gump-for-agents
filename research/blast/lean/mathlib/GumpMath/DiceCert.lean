/-
Kernel-checkable certificates for the lifetime of a face of the dice surrogate (`GumpMath/DiceDef.lean`).

A certificate is a vector v on the 2 ^ A states (a binary tree of natural numbers, `Tree`) and a rational
bound. The check `Data.allRows` runs, for every state x, the product (P v)(x) = Σ_y P(x,y) v(y) in exact
integer arithmetic, as a contraction over the cells one at a time (`Tree.eval`, 2 ^ (A+1) products per row;
P is a product over cells, so the sum over y factors along the tree), and compares it with λ v(x).
`rows_sound` proves that a passing check gives (P v)(x) ≤ λ v(x) (or ≥) for the matrix `Face.P` of the
definition, with the integer tables tied to `aliveProb` by `aliveProb_eq` and to the face's geometry by
`Data.tabOK` (decided by the kernel too). Then `survival_le_of`, `survival_ge_of` turn the inequality into
bounds on survival for every t, by the two inductions of `GumpMath/Certificate.lean`.
-/
import GumpMath.DiceDef
import GumpMath.Certificate
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

namespace Gump.Dice
open Gump Finset Matrix

/-- A vector on the states 0 ≤ y < 2 ^ n, as a perfect binary tree split on the top bit first. -/
inductive Tree where
  | leaf (a : ℕ)
  | node (l r : Tree)

namespace Tree

/-- The entry at y of a tree of depth n (bit n - 1 of y chooses the branch at the root). -/
def get : Tree → ℕ → ℕ → ℕ
  | leaf a, 0, _ => a
  | node l r, n + 1, y => if y.testBit n then r.get n y else l.get n y
  | _, _, _ => 0

/-- Σ_y (Π_{i < n} (f i).(bit i of y)) · t(y), contracted bit by bit from the top. -/
def eval : Tree → ℕ → (ℕ → ℕ × ℕ) → ℕ
  | leaf a, 0, _ => a
  | node l r, n + 1, f => (f n).1 * l.eval n f + (f n).2 * r.eval n f
  | _, _, _ => 0

theorem get_congr : ∀ (t : Tree) (n y y' : ℕ), (∀ i < n, y.testBit i = y'.testBit i) →
    t.get n y = t.get n y'
  | leaf _, 0, _, _, _ => rfl
  | leaf _, _ + 1, _, _, _ => rfl
  | node _ _, 0, _, _, _ => rfl
  | node l r, n + 1, y, y', h => by
      have h' : ∀ i < n, y.testBit i = y'.testBit i := fun i hi => h i (by omega)
      simp only [get, h n (by omega), l.get_congr n y y' h', r.get_congr n y y' h']

/-- Choose the second component on a set bit. -/
def sel (p : ℕ × ℕ) (b : Bool) : ℕ := if b then p.2 else p.1

theorem eval_eq : ∀ (t : Tree) (n : ℕ) (f : ℕ → ℕ × ℕ),
    t.eval n f = ∑ y ∈ range (2 ^ n), (∏ i ∈ range n, sel (f i) (y.testBit i)) * t.get n y
  | leaf a, 0, f => by simp [eval, get]
  | node l r, 0, f => by simp [eval, get]
  | leaf a, n + 1, f => by simp [eval, get]
  | node l r, n + 1, f => by
      rw [eval, l.eval_eq n f, r.eval_eq n f, pow_succ, mul_two, sum_range_add, mul_sum, mul_sum]
      congr 1
      · refine sum_congr rfl fun y hy => ?_
        have hy' : y < 2 ^ n := mem_range.mp hy
        have hb : y.testBit n = false := Nat.testBit_lt_two_pow hy'
        rw [prod_range_succ, get, hb, sel]
        simp only [Bool.false_eq_true, ite_false]
        ring
      · refine sum_congr rfl fun y hy => ?_
        have hy' : y < 2 ^ n := mem_range.mp hy
        have hb : (2 ^ n + y).testBit n = true := by
          rw [Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow hy']; rfl
        have hlow : ∀ i < n, (2 ^ n + y).testBit i = y.testBit i := fun i hi =>
          Nat.testBit_two_pow_add_gt hi y
        have hprod : ∏ i ∈ range n, sel (f i) ((2 ^ n + y).testBit i) =
            ∏ i ∈ range n, sel (f i) (y.testBit i) :=
          prod_congr rfl (fun i hi => by rw [hlow i (mem_range.mp hi)])
        rw [prod_range_succ, get, hb, sel, r.get_congr n (2 ^ n + y) y hlow, hprod]
        simp only [ite_true]
        ring

end Tree

/-! ### The alive numerators -/

/-- With ρ1 = n1/d1 and ρ2 = n2/d2: d1 ^ m1 · d2 ^ m2 times `aliveProb`, as a natural number. -/
def aliveNum (n1 d1 n2 d2 m1 m2 k : ℕ) (s : Bool) : ℕ :=
  ∑ j ∈ range (m1 + 1), ∑ l ∈ range (m2 + 1),
    if rule s (k + j + l) then
      m1.choose j * n1 ^ j * (d1 - n1) ^ (m1 - j) * (m2.choose l * n2 ^ l * (d2 - n2) ^ (m2 - l))
    else 0

theorem bin_eq (m j n d : ℕ) (hd : 0 < d) (hn : n ≤ d) (hj : j ≤ m) :
    bin m ((n : ℚ) / d) j = (m.choose j * n ^ j * (d - n) ^ (m - j) : ℕ) / (d : ℚ) ^ m := by
  have hd' : (d : ℚ) ≠ 0 := by exact_mod_cast hd.ne'
  have e : (d : ℚ) ^ m = (d : ℚ) ^ j * (d : ℚ) ^ (m - j) := by rw [← pow_add, Nat.add_sub_cancel' hj]
  rw [bin, e]
  push_cast [Nat.cast_sub hn]
  rw [eq_div_iff (mul_ne_zero (pow_ne_zero _ hd') (pow_ne_zero _ hd'))]
  calc ((m.choose j : ℕ) : ℚ) * ((n : ℚ) / d) ^ j * (1 - (n : ℚ) / d) ^ (m - j) * ((d : ℚ) ^ j * (d : ℚ) ^ (m - j))
      = (m.choose j : ℚ) * (((n : ℚ) / d * d) ^ j) * (((1 - (n : ℚ) / d) * d) ^ (m - j)) := by
        rw [mul_pow, mul_pow]; ring
    _ = (m.choose j : ℚ) * (n : ℚ) ^ j * ((d : ℚ) - n) ^ (m - j) := by
        rw [div_mul_cancel₀ _ hd', sub_mul, one_mul, div_mul_cancel₀ _ hd']

theorem aliveProb_eq (n1 d1 n2 d2 m1 m2 k : ℕ) (s : Bool) (h1 : 0 < d1) (hn1 : n1 ≤ d1)
    (h2 : 0 < d2) (hn2 : n2 ≤ d2) :
    aliveProb ((n1 : ℚ) / d1) ((n2 : ℚ) / d2) m1 m2 k s =
      (aliveNum n1 d1 n2 d2 m1 m2 k s : ℚ) / ((d1 : ℚ) ^ m1 * (d2 : ℚ) ^ m2) := by
  rw [aliveProb, aliveNum]
  push_cast
  rw [sum_div]
  refine sum_congr rfl fun j hj => ?_
  rw [sum_div]
  refine sum_congr rfl fun l hl => ?_
  have hj' : j ≤ m1 := Nat.lt_succ_iff.mp (mem_range.mp hj)
  have hl' : l ≤ m2 := Nat.lt_succ_iff.mp (mem_range.mp hl)
  split_ifs
  · rw [bin_eq m1 j n1 d1 h1 hn1 hj', bin_eq m2 l n2 d2 h2 hn2 hl']
    push_cast [Nat.cast_sub hn1, Nat.cast_sub hn2]
    have : (d1 : ℚ) ≠ 0 := by exact_mod_cast h1.ne'
    have : (d2 : ℚ) ≠ 0 := by exact_mod_cast h2.ne'
    field_simp
  · simp

/-! ### The certificate data and its checks -/

/-- Tables for a face at densities n1/d1, n2/d2: in-layer neighbour lists `G`, coin numbers `C`, alive
numerators `T` (T[i][2k + s] = `aliveNum` for cell i with k live neighbours and state s). -/
structure Data where
  n1 : ℕ
  d1 : ℕ
  n2 : ℕ
  d2 : ℕ
  G : List (List ℕ)
  C : List (ℕ × ℕ)
  T : List (List ℕ)

namespace Data
variable (c : Data)

/-- The denominator of cell i's probabilities. -/
def den (i : ℕ) : ℕ := c.d1 ^ (c.C.getD i (0, 0)).1 * c.d2 ^ (c.C.getD i (0, 0)).2

/-- Live in-layer neighbours of cell i in state x, by the table. -/
def kk (x i : ℕ) : ℕ := (c.G.getD i []).countP fun j => x.testBit j

/-- The alive numerator of cell i in state x, by the table. -/
def alpha (x i : ℕ) : ℕ := (c.T.getD i []).getD (2 * c.kk x i + if x.testBit i then 1 else 0) 0

/-- The two factors of cell i in row x: (dies, alive). -/
def fac (x i : ℕ) : ℕ × ℕ := (c.den i - c.alpha x i, c.alpha x i)

/-- The tables agree with the face: geometry (`Face.nb`, `Face.m1`, `Face.m2`), the alive numerators
(`aliveNum`) for every k up to the degree, and numerators at most their denominators. -/
def tabOK (F : Face) : Bool :=
  decide (0 < c.d1) && decide (c.n1 ≤ c.d1) && decide (0 < c.d2) && decide (c.n2 ≤ c.d2) &&
  (List.range F.A).all fun i =>
    c.G.getD i [] == F.nb i && c.C.getD i (0, 0) == (F.m1 i, F.m2 i) &&
    c.T.getD i [] == (List.range (2 * ((c.G.getD i []).length + 1))).map
      (fun j => aliveNum c.n1 c.d1 c.n2 c.d2 (F.m1 i) (F.m2 i) (j / 2) (j % 2 == 1)) &&
    (c.T.getD i []).all fun a => decide (a ≤ c.den i)

/-- `p n` for every n below the bound. -/
def allRows (p : ℕ → Bool) : ℕ → Bool
  | 0 => true
  | n + 1 => p n && allRows p n

theorem allRows_spec (p : ℕ → Bool) : ∀ n, allRows p n = true → ∀ x < n, p x = true
  | 0, _, x, hx => absurd hx (Nat.not_lt_zero x)
  | n + 1, h, x, hx => by
      simp only [allRows, Bool.and_eq_true] at h
      rcases Nat.lt_succ_iff_lt_or_eq.mp hx with hx | rfl
      · exact allRows_spec p n h.2 x hx
      · exact h.1

/-- Row check with two vectors: M · (N u)(x) ≤ L · D · w(x). -/
def rowLe (A Dt L M : ℕ) (U W : Tree) (x : ℕ) : Bool :=
  decide (M * U.eval A (c.fac x) ≤ L * Dt * W.get A x)

/-- Upper row check: M · (N v)(x) ≤ L · D · v(x). -/
def rowUp (A Dt L M : ℕ) (V : Tree) (x : ℕ) : Bool := c.rowLe A Dt L M V V x

/-- Lower row check: L · D · v(x) ≤ M · (N v)(x). -/
def rowLo (A Dt L M : ℕ) (V : Tree) (x : ℕ) : Bool :=
  decide (L * Dt * V.get A x ≤ M * V.eval A (c.fac x))

end Data

/-! ### Soundness -/

namespace Data
variable (c : Data) (F : Face)

theorem tabOK_spec (h : c.tabOK F = true) :
    0 < c.d1 ∧ c.n1 ≤ c.d1 ∧ 0 < c.d2 ∧ c.n2 ≤ c.d2 ∧ ∀ i < F.A,
      c.G.getD i [] = F.nb i ∧ c.C.getD i (0, 0) = (F.m1 i, F.m2 i) ∧
      c.T.getD i [] = (List.range (2 * ((c.G.getD i []).length + 1))).map
        (fun j => aliveNum c.n1 c.d1 c.n2 c.d2 (F.m1 i) (F.m2 i) (j / 2) (j % 2 == 1)) ∧
      ∀ a ∈ c.T.getD i [], a ≤ c.den i := by
  simp only [tabOK, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true, List.mem_range,
    beq_iff_eq] at h
  obtain ⟨⟨⟨⟨h1, h2⟩, h3⟩, h4⟩, h5⟩ := h
  refine ⟨h1, h2, h3, h4, fun i hi => ?_⟩
  obtain ⟨⟨⟨a, b⟩, d⟩, e⟩ := h5 i hi
  exact ⟨a, b, d, e⟩

theorem alpha_le (h : c.tabOK F = true) (x i : ℕ) (hi : i < F.A) : c.alpha x i ≤ c.den i := by
  obtain ⟨-, -, -, -, h⟩ := c.tabOK_spec F h
  obtain ⟨-, -, -, hle⟩ := h i hi
  unfold alpha
  rw [List.getD_eq_getElem?_getD]
  cases hget : (c.T.getD i [])[2 * c.kk x i + if x.testBit i then 1 else 0]? with
  | none => simp
  | some a => exact hle a (List.mem_of_getElem? hget)

/-- The table gives the definition's alive probabilities. -/
theorem a_eq (h : c.tabOK F = true) (x i : ℕ) (hi : i < F.A) :
    F.a ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x i = (c.alpha x i : ℚ) / c.den i := by
  obtain ⟨h1, h2, h3, h4, h⟩ := c.tabOK_spec F h
  obtain ⟨hG, hC, hT, -⟩ := h i hi
  have hk : F.k x i = c.kk x i := by rw [Face.k, kk, hG]
  have hkle : c.kk x i ≤ (c.G.getD i []).length := List.countP_le_length
  have hidx : 2 * c.kk x i + (if x.testBit i then 1 else 0) < 2 * ((c.G.getD i []).length + 1) := by
    split <;> omega
  have hal : c.alpha x i = aliveNum c.n1 c.d1 c.n2 c.d2 (F.m1 i) (F.m2 i) (c.kk x i) (x.testBit i) := by
    unfold alpha
    rw [hT, List.getD_eq_getElem?_getD, List.getElem?_map, List.getElem?_range hidx]
    simp only [Option.map_some, Option.getD_some]
    congr 1
    · split <;> omega
    · cases x.testBit i <;> simp
  have hden : c.den i = c.d1 ^ F.m1 i * c.d2 ^ F.m2 i := by rw [den, hC]
  rw [Face.a, hk, hal, hden, aliveProb_eq _ _ _ _ _ _ _ _ h1 h2 h3 h4]
  push_cast
  rfl

/-- The product of the denominators. -/
def Dt (A : ℕ) : ℕ := ∏ i ∈ range A, c.den i

theorem den_pos (h : c.tabOK F = true) (i : ℕ) : 0 < c.den i := by
  obtain ⟨h1, -, h3, -, -⟩ := c.tabOK_spec F h
  exact Nat.mul_pos (pow_pos h1 _) (pow_pos h3 _)

/-- The definition's transition probabilities are the integer products over the common denominator. -/
theorem P_eq (h : c.tabOK F = true) (x y : Fin (2 ^ F.A)) :
    F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x y =
      ((∏ i ∈ range F.A, Tree.sel (c.fac x i) ((y : ℕ).testBit i) : ℕ) : ℚ) / (c.Dt F.A : ℚ) := by
  rw [Face.P, Dt]
  push_cast
  rw [← prod_div_distrib]
  refine prod_congr rfl fun i hi => ?_
  have hi' := mem_range.mp hi
  have hpos : (0 : ℚ) < c.den i := by exact_mod_cast c.den_pos F h i
  rw [c.a_eq F h x i hi', Tree.sel, fac]
  split
  · rfl
  · push_cast [c.alpha_le F h x i hi']
    field_simp

theorem P_nonneg (h : c.tabOK F = true) (x y : Fin (2 ^ F.A)) :
    0 ≤ F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x y := by
  rw [c.P_eq F h]; exact div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)

/-- The vector of a tree. -/
def vec (V : Tree) (A : ℕ) : Fin (2 ^ A) → ℚ := fun y => (V.get A y : ℚ)

theorem mulVec_eq (h : c.tabOK F = true) (V : Tree) (x : Fin (2 ^ F.A)) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec V F.A) x =
      (V.eval F.A (c.fac x) : ℚ) / (c.Dt F.A : ℚ) := by
  rw [Tree.eval_eq]
  simp only [mulVec, dotProduct, vec, c.P_eq F h]
  rw [Fin.sum_univ_eq_sum_range (fun y => ((∏ i ∈ range F.A, Tree.sel (c.fac x i) (y.testBit i) : ℕ) : ℚ)
    / (c.Dt F.A : ℚ) * (V.get F.A y : ℚ)) (2 ^ F.A)]
  push_cast
  rw [sum_div]
  refine sum_congr rfl fun y _ => ?_
  ring

/-- **Soundness of the two-vector check**: (P u)(x) ≤ (L/M) w(x) for every state. -/
theorem rows_le (h : c.tabOK F = true) (U W : Tree) (L M : ℕ) (hM : 0 < M)
    (hr : allRows (c.rowLe F.A (c.Dt F.A) L M U W) (2 ^ F.A) = true) (x : Fin (2 ^ F.A)) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec U F.A) x ≤ ((L : ℚ) / M) * vec W F.A x := by
  have hx := allRows_spec _ _ hr x x.isLt
  simp only [rowLe, decide_eq_true_eq] at hx
  rw [c.mulVec_eq F h, vec]
  have hD : (0 : ℚ) < c.Dt F.A := by
    rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F h i
  have hM' : (0 : ℚ) < M := by exact_mod_cast hM
  have hx' : (M : ℚ) * U.eval F.A (c.fac x) ≤ L * c.Dt F.A * W.get F.A x := by exact_mod_cast hx
  rw [div_le_iff₀ hD, div_mul_eq_mul_div, div_mul_eq_mul_div, le_div_iff₀ hM']
  nlinarith

/-- **Soundness of the upper check**: (P v)(x) ≤ (L/M) v(x) for every state. -/
theorem rows_up (h : c.tabOK F = true) (V : Tree) (L M : ℕ) (hM : 0 < M)
    (hr : allRows (c.rowUp F.A (c.Dt F.A) L M V) (2 ^ F.A) = true) (x : Fin (2 ^ F.A)) :
    (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec V F.A) x ≤ ((L : ℚ) / M) * vec V F.A x :=
  c.rows_le F h V V L M hM hr x

/-- A state whose cells all die surely (every alive numerator 0) goes to no non-empty state. -/
theorem P_sure (h : c.tabOK F = true) (x y : Fin (2 ^ F.A)) (hx : ∀ i < F.A, c.alpha x i = 0)
    (hy : (y : ℕ) ≠ 0) : F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x y = 0 := by
  rw [c.P_eq F h]
  obtain ⟨i, hi⟩ := Nat.exists_testBit_of_ne_zero hy
  have hiA : i < F.A := by
    by_contra hc
    have := Nat.ge_two_pow_of_testBit hi
    have : 2 ^ F.A ≤ 2 ^ i := Nat.pow_le_pow_right (by norm_num) (by omega)
    have := y.isLt
    omega
  have : ∏ j ∈ range F.A, Tree.sel (c.fac x j) ((y : ℕ).testBit j) = 0 :=
    prod_eq_zero (mem_range.mpr hiA) (by simp [Tree.sel, hi, fac, hx i hiA])
  rw [this]; simp

/-- **Soundness of the lower check**: (L/M) v(x) ≤ (P v)(x) for every state. -/
theorem rows_lo (h : c.tabOK F = true) (V : Tree) (L M : ℕ) (hM : 0 < M)
    (hr : allRows (c.rowLo F.A (c.Dt F.A) L M V) (2 ^ F.A) = true) (x : Fin (2 ^ F.A)) :
    ((L : ℚ) / M) * vec V F.A x ≤ (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) *ᵥ vec V F.A) x := by
  have hx := allRows_spec _ _ hr x x.isLt
  simp only [rowLo, decide_eq_true_eq] at hx
  rw [c.mulVec_eq F h, vec]
  have hD : (0 : ℚ) < c.Dt F.A := by
    rw [Dt]; push_cast; exact prod_pos fun i _ => by exact_mod_cast c.den_pos F h i
  have hM' : (0 : ℚ) < M := by exact_mod_cast hM
  have hx' : (L : ℚ) * c.Dt F.A * V.get F.A x ≤ M * V.eval F.A (c.fac x) := by exact_mod_cast hx
  rw [le_div_iff₀ hD, div_mul_eq_mul_div, div_mul_eq_mul_div, div_le_iff₀ hM']
  nlinarith

end Data

/-! ### From a certificate to survival, for every t -/

section Survival
variable {n : ℕ} (P : Matrix (Fin n) (Fin n) ℚ) (hP : ∀ x y, 0 ≤ P x y)
include hP

/-- An upper certificate bounds survival: if P v ≤ λ v and the live indicator is ≤ c v, then
(P ^ t live)(x) ≤ c λ ^ t v(x). -/
theorem survival_le_of (live v : Fin n → ℚ) (lam c : ℚ) (hlam : 0 ≤ lam) (hc : 0 ≤ c)
    (h : ∀ x, (P *ᵥ v) x ≤ lam * v x) (hv : ∀ y, live y ≤ c * v y) (t : ℕ) (x : Fin n) :
    ((P ^ t) *ᵥ live) x ≤ c * (lam ^ t * v x) := by
  have hPt := Certificate.pow_nonneg' P hP t
  calc ((P ^ t) *ᵥ live) x ≤ ((P ^ t) *ᵥ (fun j => c * v j)) x := Certificate.mulVec_mono (P ^ t) hPt hv x
    _ = c * ((P ^ t) *ᵥ v) x := Certificate.mulVec_smul_fun (P ^ t) c v x
    _ ≤ c * (lam ^ t * v x) :=
        mul_le_mul_of_nonneg_left (Certificate.pow_mulVec_le P hP v lam hlam h t x) hc

/-- A lower certificate bounds survival: if P v ≥ μ v and v ≤ C · live, then
μ ^ t v(x) ≤ C (P ^ t live)(x). -/
theorem survival_ge_of (live v : Fin n → ℚ) (mu C : ℚ) (hmu : 0 ≤ mu)
    (h : ∀ x, mu * v x ≤ (P *ᵥ v) x) (hv : ∀ y, v y ≤ C * live y) (t : ℕ) (x : Fin n) :
    mu ^ t * v x ≤ C * ((P ^ t) *ᵥ live) x := by
  have hPt := Certificate.pow_nonneg' P hP t
  calc mu ^ t * v x ≤ ((P ^ t) *ᵥ v) x := Certificate.le_pow_mulVec P hP v mu hmu h t x
    _ ≤ ((P ^ t) *ᵥ (fun j => C * live j)) x := Certificate.mulVec_mono (P ^ t) hPt hv x
    _ = C * ((P ^ t) *ᵥ live) x := Certificate.mulVec_smul_fun (P ^ t) C live x

end Survival

end Gump.Dice
