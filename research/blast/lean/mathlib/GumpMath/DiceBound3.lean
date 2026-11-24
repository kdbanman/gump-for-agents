/-
The weighted Theorem 1 for faces with a rim (added 2026-11-24, second task).

`DiceBound2.lean` weights every live–dead slot by w and needs every cell to have six slots. With a rim the degrees
vary; the cancellation only needs the neighbour relation to be balanced (every cell is the neighbour of as many
slots as it has, `Face.balanced`: true on every face whose relation is symmetric, as on hull faces). A live cell
with k live neighbours among deg carries w^(deg - k), a dead one w^(-k); the weights cancel in P(x, ∅) and the
local check `wcheck` (every cell, every k ≤ deg, both states, with the cell's own coins) gives P(x, ∅) ≥ δ^A.

For the hull faces the best single weight is w = 1341/1000 (the edge cells, four neighbours, are the binding
case): δ = 0.109 and **ln τ < 2.2165 · A** (`lntau_le_hull_weighted`, checked by the kernel for R = 3, 5, 7, 9, 11, `lntau_le_hull_small`;
the classification of the hull's cells behind it, degree 6 inside, 4 on an edge, 2 at a corner, is not proved for
every R). Against 2.5095 · A unweighted (`DiceHull.lean`, every R).
-/
import GumpMath.DiceBound2
import GumpMath.DiceHull

namespace Gump.Dice
open Gump Finset Matrix

namespace Face
variable (F : Face)

/-- Every slot is a cell, and every cell is in as many slots as it has neighbours. -/
def balanced : Prop :=
  (∀ i < F.A, ∀ j ∈ F.nb i, j < F.A) ∧ (∀ j < F.A, ∑ i ∈ range F.A, (F.nb i).count j = (F.nb j).length)

def bup (x i : ℕ) : ℕ := if x.testBit i then (F.nb i).length - F.k x i else 0
def bdown (x i : ℕ) : ℕ := if x.testBit i then 0 else F.k x i

theorem sum_k_bal (hb : F.balanced) (x : ℕ) :
    ∑ i ∈ range F.A, F.k x i = ∑ j ∈ range F.A, (if x.testBit j then (F.nb j).length else 0) := by
  obtain ⟨hlt, hin⟩ := hb
  have : ∀ i ∈ range F.A, F.k x i = ∑ j ∈ range F.A, (if x.testBit j then (F.nb i).count j else 0) :=
    fun i hi => countP_eq_sum_count F.A _ _ (hlt i (mem_range.mp hi))
  rw [sum_congr rfl this, sum_comm]
  refine sum_congr rfl fun j hj => ?_
  by_cases hx : x.testBit j
  · simp only [hx, ite_true]; exact hin j (mem_range.mp hj)
  · simp [hx]

theorem bup_sum_eq_bdown_sum (hb : F.balanced) (x : ℕ) :
    ∑ i ∈ range F.A, F.bup x i = ∑ i ∈ range F.A, F.bdown x i := by
  have hk : ∀ i, F.k x i ≤ (F.nb i).length := fun i => List.countP_le_length
  have e1 : ∀ i ∈ range F.A, F.bup x i + (if x.testBit i then F.k x i else 0) =
      (if x.testBit i then (F.nb i).length else 0) := by
    intro i _; unfold bup; have := hk i; split <;> omega
  have e2 : ∀ i ∈ range F.A, F.bdown x i + (if x.testBit i then F.k x i else 0) = F.k x i := by
    intro i _; unfold bdown; split <;> omega
  have s1 := sum_congr rfl e1
  have s2 := sum_congr rfl e2
  rw [sum_add_distrib] at s1
  rw [sum_add_distrib, sum_k_bal F hb x] at s2
  omega

/-- The local check, cell by cell, with the cell's own degree and coins. -/
def wcheck (ρ1 ρ2 w δ : ℚ) : Bool :=
  (List.range F.A).all fun i => (List.range ((F.nb i).length + 1)).all fun k => [false, true].all fun s =>
    decide (δ * (if s then 1 else w ^ k) ≤
      (1 - aliveProb ρ1 ρ2 (F.m1 i) (F.m2 i) k s) * (if s then w ^ ((F.nb i).length - k) else 1))

end Face

theorem death_ge_balanced (F : Face) (ρ1 ρ2 w δ : ℚ) (hw : 0 < w) (hδ : 0 ≤ δ) (hb : F.balanced)
    (hc : F.wcheck ρ1 ρ2 w δ = true) (x : Fin (2 ^ F.A)) : δ ^ F.A ≤ F.death ρ1 ρ2 x := by
  have hcell : ∀ i ∈ range F.A, δ * w ^ F.bdown x i ≤ (1 - F.a ρ1 ρ2 x i) * w ^ F.bup x i := by
    intro i hi
    have hk : F.k x i ≤ (F.nb i).length := List.countP_le_length
    simp only [Face.wcheck, List.all_eq_true, List.mem_range, decide_eq_true_eq, List.mem_cons,
      List.not_mem_nil, or_false] at hc
    have := hc i (mem_range.mp hi) (F.k x i) (by omega) ((x : ℕ).testBit i) (by cases (x : ℕ).testBit i <;> simp)
    unfold Face.a Face.bup Face.bdown
    by_cases hs : (x : ℕ).testBit i
    · simp only [hs, ite_true, pow_zero, mul_one] at this ⊢; exact this
    · simp only [hs, Bool.false_eq_true, ite_false, pow_zero, mul_one] at this ⊢; exact this
  have hprod := prod_le_prod₀ (fun i _ => mul_nonneg hδ (pow_nonneg hw.le _)) hcell
  rw [prod_mul_distrib, prod_mul_distrib, prod_pow_eq_pow_sum, prod_pow_eq_pow_sum,
    Face.bup_sum_eq_bdown_sum F hb x, prod_const, card_range] at hprod
  rw [Face.death]
  exact le_of_mul_le_mul_right hprod (pow_pos hw _)

/-- **The weighted bound for a balanced face**: every quasi-stationary law has 1 - λ ≥ δ^A. -/
theorem qsd_le_balanced (F : Face) (ρ1 ρ2 w δ : ℚ) (hw : 0 < w) (hδ : 0 ≤ δ) (hb : F.balanced)
    (hc : F.wcheck ρ1 ρ2 w δ = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) :
    ((δ : ℚ) : ℝ) ^ F.A ≤ 1 - lam := by
  rw [← Data.qsd_death F ρ1 ρ2 μ lam hq]
  calc ((δ : ℚ) : ℝ) ^ F.A = ∑ x, μ x * (((δ ^ F.A : ℚ)) : ℝ) := by
        rw [← sum_mul, hq.total, one_mul]; push_cast; rfl
    _ ≤ ∑ x, μ x * (F.P ρ1 ρ2 x F.empty : ℝ) := by
        refine sum_le_sum fun x _ => mul_le_mul_of_nonneg_left ?_ (hq.nonneg x)
        rw [Face.P_zero_col]; exact_mod_cast death_ge_balanced F ρ1 ρ2 w δ hw hδ hb hc x

/-- From 1 - λ ≥ 0.109^A: ln τ < 2.2165 · A. -/
theorem lntau_of_109 (A : ℕ) (hA : 0 < A) (lam : ℝ) (h : (0.109 : ℝ) ^ A ≤ 1 - lam) :
    -Real.log (1 - lam) < 2.2165 * A := by
  have hd1 : (0 : ℝ) < 0.109 := by norm_num
  have hpos : (0 : ℝ) < (0.109 : ℝ) ^ A := pow_pos hd1 _
  have hlog : -Real.log (1 - lam) ≤ -Real.log ((0.109 : ℝ) ^ A) := by
    have := Real.log_le_log hpos h; linarith
  rw [Real.log_pow] at hlog
  have hb : -Real.log (0.109 : ℝ) < 2.2165 := by
    refine neg_log_lt _ _ 3 (by norm_num) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_ ?_
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  have hA' : (0 : ℝ) < A := by exact_mod_cast hA
  nlinarith

/-- The hull's weight and bound. -/
def wHull : ℚ := 1341 / 1000
def deltaHull : ℚ := 109 / 1000

/-- **The weighted Theorem 1 on a hull face** whose balance and local check the kernel has run. -/
theorem lntau_le_hull_weighted (R : ℕ) (hb : (hull R).balanced) (hc : (hull R).wcheck ρ1 ρ2 wHull deltaHull = true)
    (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam) (hA : 0 < (hull R).A) :
    -Real.log (1 - lam) < 2.2165 * (hull R).A := by
  have := qsd_le_balanced (hull R) ρ1 ρ2 wHull deltaHull (by norm_num [wHull]) (by norm_num [deltaHull]) hb hc μ lam hq
  have e : ((deltaHull : ℚ) : ℝ) = 0.109 := by norm_num [deltaHull]
  rw [e] at this
  exact lntau_of_109 _ hA lam this

theorem hull3_balanced : (hull 3).balanced := ⟨by decide +kernel, by decide +kernel⟩
theorem hull3_wcheck : (hull 3).wcheck ρ1 ρ2 wHull deltaHull = true := by decide +kernel
theorem hull5_balanced : (hull 5).balanced := ⟨by decide +kernel, by decide +kernel⟩
theorem hull5_wcheck : (hull 5).wcheck ρ1 ρ2 wHull deltaHull = true := by decide +kernel
theorem hull7_balanced : (hull 7).balanced := ⟨by decide +kernel, by decide +kernel⟩
theorem hull7_wcheck : (hull 7).wcheck ρ1 ρ2 wHull deltaHull = true := by decide +kernel
theorem hull9_balanced : (hull 9).balanced := ⟨by decide +kernel, by decide +kernel⟩
theorem hull9_wcheck : (hull 9).wcheck ρ1 ρ2 wHull deltaHull = true := by decide +kernel
theorem hull11_balanced : (hull 11).balanced := ⟨by decide +kernel, by decide +kernel⟩
theorem hull11_wcheck : (hull 11).wcheck ρ1 ρ2 wHull deltaHull = true := by decide +kernel

/-- **ln τ < 2.2165 · A on the hull faces R = 3, 5, 7, 9, 11** (9 to 63 cells), every quasi-stationary law. -/
theorem lntau_le_hull_small (R : ℕ) (hR : R = 3 ∨ R = 5 ∨ R = 7 ∨ R = 9 ∨ R = 11)
    (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam) :
    -Real.log (1 - lam) < 2.2165 * (hull R).A := by
  rcases hR with rfl | rfl | rfl | rfl | rfl
  · exact lntau_le_hull_weighted 3 hull3_balanced hull3_wcheck μ lam hq (by decide)
  · exact lntau_le_hull_weighted 5 hull5_balanced hull5_wcheck μ lam hq (by decide)
  · exact lntau_le_hull_weighted 7 hull7_balanced hull7_wcheck μ lam hq (by decide)
  · exact lntau_le_hull_weighted 9 hull9_balanced hull9_wcheck μ lam hq (by decide)
  · exact lntau_le_hull_weighted 11 hull11_balanced hull11_wcheck μ lam hq (by decide)

end Gump.Dice
