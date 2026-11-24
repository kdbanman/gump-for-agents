/-
A sharper Theorem 1 for regular faces, from a finite certificate that bounds an infinite family.

On a face where every cell has its three coins, exactly six in-layer neighbour slots and is itself the neighbour
of exactly six slots (every wrapped face), the one-step death probability P(x, ∅) = Π_i d_i(x) is rewritten with
a weight w on every edge between a live and a dead cell: a live cell with k live neighbours takes w^(6-k), a dead
one w^(-k). The weights cancel in the product (the live-to-dead slots and the dead-to-live slots are equally many,
`up_sum_eq_down_sum`), and every weighted cell factor is at least δ₁ (a check over the 14 cases (s, k), with
w = 152/125): P(x, ∅) ≥ δ₁^A for every state of every such face, whatever its size. With δ₁ = 0.1462 this gives
ln τ < 1.9228 · A, against 2.5095 · A for the unweighted bound (`DiceBound.lean`). The local inequality is the
finite certificate; the cancellation is what lets it bound the infinite family.
-/
import GumpMath.DiceExit

namespace Gump.Dice
open Gump Finset Matrix

/-- A list of indices below A counts as a sum over the indices. -/
theorem countP_eq_sum_count (A : ℕ) (p : ℕ → Bool) : ∀ l : List ℕ, (∀ j ∈ l, j < A) →
    l.countP p = ∑ j ∈ range A, if p j then l.count j else 0
  | [], _ => by simp
  | a :: l, h => by
      have ha : a < A := h a (List.mem_cons_self ..)
      have ih := countP_eq_sum_count A p l (fun j hj => h j (List.mem_cons_of_mem _ hj))
      rw [List.countP_cons, ih]
      have : ∑ j ∈ range A, (if p j then (a :: l).count j else 0) =
          ∑ j ∈ range A, (if p j then l.count j else 0) + ∑ j ∈ range A, (if p j ∧ a = j then 1 else 0) := by
        rw [← sum_add_distrib]
        refine sum_congr rfl fun j _ => ?_
        rw [List.count_cons]
        by_cases hp : p j <;> by_cases hj : a = j <;> simp [hp, hj, beq_iff_eq]
      rw [this]
      congr 1
      have e : (∑ j ∈ range A, if p j ∧ a = j then 1 else 0) = ∑ j ∈ range A, if a = j then (if p j then 1 else 0) else 0 :=
        sum_congr rfl fun j _ => by by_cases h1 : a = j <;> by_cases h2 : p j <;> simp [h1, h2]
      rw [e, sum_ite_eq]
      simp [ha]

namespace Face
variable (F : Face)

/-- The regularity of a wrapped face: six neighbour slots per cell, each cell in six slots, all slots cells. -/
def regular : Prop :=
  (∀ i < F.A, (F.nb i).length = 6) ∧ (∀ i < F.A, ∀ j ∈ F.nb i, j < F.A) ∧
  (∀ j < F.A, ∑ i ∈ range F.A, (F.nb i).count j = 6)

/-- Σ_i k_i(x) = 6 · (number of live cells). -/
theorem sum_k (hr : F.regular) (x : ℕ) :
    ∑ i ∈ range F.A, F.k x i = 6 * ∑ j ∈ range F.A, (if x.testBit j then 1 else 0) := by
  obtain ⟨-, hlt, hin⟩ := hr
  have : ∀ i ∈ range F.A, F.k x i = ∑ j ∈ range F.A, (if x.testBit j then (F.nb i).count j else 0) :=
    fun i hi => countP_eq_sum_count F.A _ _ (hlt i (mem_range.mp hi))
  rw [sum_congr rfl this, sum_comm, mul_sum]
  refine sum_congr rfl fun j hj => ?_
  by_cases hx : x.testBit j
  · simp only [hx, if_true, mul_one]; exact hin j (mem_range.mp hj)
  · simp [hx]

/-- Live-to-dead slots: (6 - k) at a live cell, 0 at a dead one; dead-to-live: k at a dead cell. -/
def up (x i : ℕ) : ℕ := if x.testBit i then 6 - F.k x i else 0
def down (x i : ℕ) : ℕ := if x.testBit i then 0 else F.k x i

theorem up_sum_eq_down_sum (hr : F.regular) (x : ℕ) :
    ∑ i ∈ range F.A, F.up x i = ∑ i ∈ range F.A, F.down x i := by
  have hk6 : ∀ i ∈ range F.A, F.k x i ≤ 6 := fun i hi => by
    have := hr.1 i (mem_range.mp hi); unfold k; rw [← this]; exact List.countP_le_length
  have e1 : ∀ i ∈ range F.A, F.up x i + (if x.testBit i then F.k x i else 0) = 6 * (if x.testBit i then 1 else 0) := by
    intro i hi; unfold up; have := hk6 i hi; split <;> omega
  have e2 : ∀ i ∈ range F.A, F.down x i + (if x.testBit i then F.k x i else 0) = F.k x i := by
    intro i hi; unfold down; split <;> omega
  have s1 := sum_congr rfl e1
  have s2 := sum_congr rfl e2
  rw [sum_add_distrib, ← mul_sum] at s1
  rw [sum_add_distrib, sum_k F hr x] at s2
  omega

end Face

/-- The weight and the weighted per-cell bound. -/
def wt : ℚ := 152 / 125
def delta1 : ℚ := 1462 / 10000

/-- **The local certificate**: for a cell with coins (2, 1) and k ≤ 6 live neighbours, its probability of being
dead next, weighted by w^(6-k) if alive and w^(-k) if dead, is at least δ₁ = 0.1462 (14 cases). -/
theorem weighted_cell : ∀ k ≤ 6, ∀ s : Bool,
    delta1 * (if s then 1 else wt ^ k) ≤ (1 - aliveProb ρ1 ρ2 2 1 k s) * (if s then wt ^ (6 - k) else 1) := by
  decide +kernel

theorem death_ge_regular (F : Face) (hc : ∀ q, F.coin q = true) (hr : F.regular) (x : Fin (2 ^ F.A)) :
    delta1 ^ F.A ≤ F.death ρ1 ρ2 x := by
  have hw : (0 : ℚ) < wt := by norm_num [wt]
  have hd0 : (0 : ℚ) ≤ delta1 := by norm_num [delta1]
  -- Π_i d_i · w^up_i = Π_i (d_i w^up_i)  and  Π w^up = w^Σup = w^Σdown = Π w^down
  have hcell : ∀ i ∈ range F.A, delta1 * wt ^ F.down x i ≤ (1 - F.a ρ1 ρ2 x i) * wt ^ F.up x i := by
    intro i hi
    have hk : F.k x i ≤ 6 := by
      have := hr.1 i (mem_range.mp hi); unfold Face.k; rw [← this]; exact List.countP_le_length
    have := weighted_cell (F.k x i) hk ((x : ℕ).testBit i)
    rw [Face.a_all F ρ1 ρ2 hc]
    unfold Face.up Face.down
    by_cases hs : (x : ℕ).testBit i
    · simp only [hs, ite_true, pow_zero, mul_one] at this ⊢; exact this
    · simp only [hs, Bool.false_eq_true, ite_false, pow_zero, mul_one] at this ⊢; exact this
  have hprod := prod_le_prod₀ (fun i _ => mul_nonneg hd0 (pow_nonneg hw.le _)) hcell
  rw [prod_mul_distrib, prod_mul_distrib, prod_pow_eq_pow_sum, prod_pow_eq_pow_sum,
    Face.up_sum_eq_down_sum F hr x, prod_const, card_range] at hprod
  have hpos : (0 : ℚ) < wt ^ ∑ i ∈ range F.A, F.down x i := pow_pos hw _
  rw [Face.death]
  exact le_of_mul_le_mul_right hprod hpos

/-- **Theorem 1, sharpened, survival form**: on every regular face with all its coins (every wrapped face),
P_x(T > t) ≤ (1 - δ₁ ^ A) ^ t with δ₁ = 0.1462. -/
theorem survival_le_regular (F : Face) (hc : ∀ q, F.coin q = true) (hr : F.regular) :
    ∀ (t : ℕ) (x : Fin (2 ^ F.A)), F.survival ρ1 ρ2 t x ≤ (1 - delta1 ^ F.A) ^ t
  | 0, x => by
      simp only [Face.survival, pow_zero, Matrix.one_mulVec, Face.live]
      split <;> norm_num
  | t + 1, x => by
      have h1 : (0 : ℚ) ≤ ρ1 := by norm_num [ρ1]
      have h1' : ρ1 ≤ 1 := by norm_num [ρ1]
      have h2 : (0 : ℚ) ≤ ρ2 := by norm_num [ρ2]
      have h2' : ρ2 ≤ 1 := by norm_num [ρ2]
      have hP : ∀ y, 0 ≤ F.P ρ1 ρ2 x y := fun y => prod_nonneg fun i _ => by
        have := death_cell ρ1 ρ2 h1 h1' h2 h2' (F.k x i) ((x : ℕ).testBit i)
        rw [Face.a_all F ρ1 ρ2 hc]; split <;> linarith [this.1, this.2.1]
      set B := (1 - delta1 ^ F.A) ^ t
      have hB : ∀ y, F.survival ρ1 ρ2 t y ≤ B - (if y = F.empty then B else 0) := by
        intro y
        split
        · rename_i h; rw [h, Face.survival_empty F ρ1 ρ2 hc]; simp
        · simpa using survival_le_regular F hc hr t y
      rw [Face.survival_succ]
      calc ∑ y, F.P ρ1 ρ2 x y * F.survival ρ1 ρ2 t y
          ≤ ∑ y, F.P ρ1 ρ2 x y * (B - (if y = F.empty then B else 0)) :=
            sum_le_sum fun y _ => mul_le_mul_of_nonneg_left (hB y) (hP y)
        _ = B * (1 - F.death ρ1 ρ2 x) := by
            simp only [mul_sub, mul_ite, mul_zero, sum_sub_distrib, sum_ite_eq', mem_univ, ite_true]
            rw [← sum_mul, Face.P_row_sum, Face.P_zero_col]; ring
        _ ≤ B * (1 - delta1 ^ F.A) := by
            have hB0 : 0 ≤ B := by
              have := survival_le_regular F hc hr t F.empty
              rw [Face.survival_empty F ρ1 ρ2 hc] at this; exact this
            have := death_ge_regular F hc hr x
            nlinarith
        _ = (1 - delta1 ^ F.A) ^ (t + 1) := by rw [pow_succ]

/-- **Theorem 1, sharpened, in nats**: on every regular face with all its coins, every quasi-stationary law
has ln τ = -ln(1 - λ) < 1.9228 · A. -/
theorem lntau_le_regular (F : Face) (hc : ∀ q, F.coin q = true) (hr : F.regular) (μ : Fin (2 ^ F.A) → ℝ)
    (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (hA : 0 < F.A) :
    -Real.log (1 - lam) < 1.9228 * F.A := by
  -- λ = Σ_x μ(x) (1 - d(x)) ≤ 1 - δ₁^A
  have hd := Data.qsd_death F ρ1 ρ2 μ lam hq
  have hle : (((delta1 ^ F.A : ℚ)) : ℝ) ≤ 1 - lam := by
    rw [← hd]
    calc (((delta1 ^ F.A : ℚ)) : ℝ) = ∑ x, μ x * (((delta1 ^ F.A : ℚ)) : ℝ) := by rw [← sum_mul, hq.total, one_mul]
      _ ≤ ∑ x, μ x * (F.P ρ1 ρ2 x F.empty : ℝ) := by
          refine sum_le_sum fun x _ => mul_le_mul_of_nonneg_left ?_ (hq.nonneg x)
          rw [Face.P_zero_col]; exact_mod_cast death_ge_regular F hc hr x
  push_cast at hle
  have hd1 : (0 : ℝ) < delta1 := by norm_num [delta1]
  have hpos : (0 : ℝ) < (delta1 : ℝ) ^ F.A := pow_pos hd1 _
  have hlog : -Real.log (1 - lam) ≤ -Real.log ((delta1 : ℝ) ^ F.A) := by
    have := Real.log_le_log hpos hle; linarith
  rw [Real.log_pow] at hlog
  have hb : -Real.log (delta1 : ℝ) < 1.9228 := by
    have e : (delta1 : ℝ) = 0.1462 := by norm_num [delta1]
    rw [e]
    refine neg_log_lt _ _ 2 (by norm_num) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_ ?_
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  have hA' : (0 : ℝ) < F.A := by exact_mod_cast hA
  nlinarith

/-- The wrapped faces of the tables are regular (checked; the general torus is not formalised here). -/
theorem regular_torus103 : (torus 1 0 3).regular := by
  refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus113 : (torus 1 1 3).regular := by
  refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus202 : (torus 2 0 2).regular := by
  refine ⟨?_, ?_, ?_⟩ <;> decide +kernel

end Gump.Dice
