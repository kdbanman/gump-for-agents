/-
Theorem 1 of `research/blast/rigour/THEOREMS.md` (the upper bound B1, "ln τ ≤ ε_max · A ≤ 2.509 · A") for the chain
of `GumpMath/DiceDef.lean`, for every face whose cells all have their three coins (every wrapped face and every
strip of `geom.py`, at every size), at all densities 0 ≤ ρ1, ρ2 ≤ 1.

* `death_cell`: a cell with coins (2, 1) dies with probability ≥ delta0 = min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) whatever its
  state and its neighbours (the death event contains "all three coins tails" or "all three heads").
* `coins_of_all`: on such a face every cell has m1 = 2, m2 = 1 (from T1, `Gump.layer_histogram`).
* `survival_le_all`: P_x(T > t) ≤ (1 - delta0 ^ A) ^ t for every state x and every t.
* `qsd_le_all`: every quasi-stationary law (μ, λ) has λ ≤ 1 - delta0 ^ A, i.e. ln τ = -ln(1 - λ) ≤ A · (-ln delta0);
* `lntau_le_all`: at (0.44, 0.42), ln τ < 2.5095 · A (THEOREMS.md: ε_max = 2.509).
What is not proved here: the middle term E_μ[E] of Theorem 1 (Jensen), and hull faces (their corner cells have
two coins; the bound holds there too by `death_cell`-type reasoning, not formalised for every R).
-/
import GumpMath.DiceLife
import GumpMath.DiceReal
import Mathlib.Algebra.Order.BigOperators.GroupWithZero.Finset

namespace Gump.Dice
open Gump Finset Matrix

/-- Σ over the 2 ^ n states of a product over bits is the product of the two-term sums. -/
theorem sum_prod_bits (g : ℕ → Bool → ℚ) : ∀ n : ℕ,
    ∑ y ∈ range (2 ^ n), ∏ i ∈ range n, g i (y.testBit i) = ∏ i ∈ range n, (g i false + g i true)
  | 0 => by simp
  | n + 1 => by
      rw [pow_succ, mul_two, sum_range_add]
      have hL : ∑ y ∈ range (2 ^ n), ∏ i ∈ range (n + 1), g i (y.testBit i) =
          (∑ y ∈ range (2 ^ n), ∏ i ∈ range n, g i (y.testBit i)) * g n false := by
        rw [sum_mul]
        refine sum_congr rfl fun y hy => ?_
        rw [prod_range_succ, Nat.testBit_lt_two_pow (mem_range.mp hy)]
      have hR : ∑ y ∈ range (2 ^ n), ∏ i ∈ range (n + 1), g i ((2 ^ n + y).testBit i) =
          (∑ y ∈ range (2 ^ n), ∏ i ∈ range n, g i (y.testBit i)) * g n true := by
        rw [sum_mul]
        refine sum_congr rfl fun y hy => ?_
        have hy' := mem_range.mp hy
        have hb : (2 ^ n + y).testBit n = true := by
          rw [Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow hy']; rfl
        rw [prod_range_succ, hb]
        congr 1
        exact prod_congr rfl fun i hi => by rw [Nat.testBit_two_pow_add_gt (mem_range.mp hi) y]
      rw [hL, hR, sum_prod_bits g n, prod_range_succ]
      ring

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

/-- The rows of P sum to one. -/
theorem P_row_sum (x : Fin (2 ^ F.A)) : ∑ y, F.P ρ1 ρ2 x y = 1 := by
  simp only [P]
  rw [Fin.sum_univ_eq_sum_range (fun y => ∏ i ∈ range F.A,
    if y.testBit i then F.a ρ1 ρ2 x i else 1 - F.a ρ1 ρ2 x i) (2 ^ F.A)]
  rw [sum_prod_bits (fun i b => if b then F.a ρ1 ρ2 x i else 1 - F.a ρ1 ρ2 x i) F.A]
  simp

/-- The empty state. -/
def empty : Fin (2 ^ F.A) := ⟨0, pow_pos (by norm_num) _⟩

theorem P_zero_col (x : Fin (2 ^ F.A)) : F.P ρ1 ρ2 x F.empty = F.death ρ1 ρ2 x := by
  simp [P, death, empty]

end Face

/-- The offsets one and two layers beneath: T1 gives 2 and 1 of them. -/
theorem countP_below2 (a : Axis) (d : Diag) : (offsets a).countP (fun o => decide (d.dot o = -2)) = 2 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

theorem countP_below4 (a : Axis) (d : Diag) : (offsets a).countP (fun o => decide (d.dot o = -4)) = 1 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- On a face where every point beneath carries a coin, every cell has two coins one layer in and one two
layers in. -/
theorem coins_of_all (F : Face) (hc : ∀ q, F.coin q = true) (i : ℕ) : F.m1 i = 2 ∧ F.m2 i = 1 := by
  constructor
  · rw [Face.m1, nbrs, List.countP_map, ← countP_below2 (F.cell i).axis F.diag]
    congr 1; funext o
    simp only [Function.comp, hc, Bool.and_true, Diag.dot_add]
    congr 1; apply propext; omega
  · rw [Face.m2, nbrs, List.countP_map, ← countP_below4 (F.cell i).axis F.diag]
    congr 1; funext o
    simp only [Function.comp, hc, Bool.and_true, Diag.dot_add]
    congr 1; apply propext; omega

/-- No cell is alive next both with all three coins tails and with all three heads. -/
theorem rule_k_or_k3 (s : Bool) (k : ℕ) : rule s k = false ∨ rule s (k + 3) = false := by
  cases s <;> simp only [rule] <;> by_cases h : k ≤ 2 <;> simp_all <;> omega

/-- **Every cell with its three coins can die**: whatever its state and its live neighbours, it is dead next
with probability at least min(ρ1² ρ2, (1 - ρ1)² (1 - ρ2)). Also 0 ≤ aliveProb ≤ 1. -/
theorem death_cell (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) (k : ℕ) (s : Bool) :
    0 ≤ aliveProb ρ1 ρ2 2 1 k s ∧ aliveProb ρ1 ρ2 2 1 k s ≤ 1 ∧
    min (ρ1 ^ 2 * ρ2) ((1 - ρ1) ^ 2 * (1 - ρ2)) ≤ 1 - aliveProb ρ1 ρ2 2 1 k s := by
  have r1 : 0 ≤ 1 - ρ1 := by linarith
  have r2 : 0 ≤ 1 - ρ2 := by linarith
  have w1 : 0 ≤ (1 - ρ1) ^ 2 * (1 - ρ2) := by positivity
  have w2 : 0 ≤ (1 - ρ1) ^ 2 * ρ2 := by positivity
  have w3 : 0 ≤ 2 * ρ1 * (1 - ρ1) * (1 - ρ2) := by positivity
  have w4 : 0 ≤ 2 * ρ1 * (1 - ρ1) * ρ2 := by positivity
  have w5 : 0 ≤ ρ1 ^ 2 * (1 - ρ2) := by positivity
  have w6 : 0 ≤ ρ1 ^ 2 * ρ2 := by positivity
  have hsum : (1 - ρ1) ^ 2 * (1 - ρ2) + (1 - ρ1) ^ 2 * ρ2 + 2 * ρ1 * (1 - ρ1) * (1 - ρ2) +
      2 * ρ1 * (1 - ρ1) * ρ2 + ρ1 ^ 2 * (1 - ρ2) + ρ1 ^ 2 * ρ2 = 1 := by ring
  have hm1 := min_le_left (ρ1 ^ 2 * ρ2) ((1 - ρ1) ^ 2 * (1 - ρ2))
  have hm2 := min_le_right (ρ1 ^ 2 * ρ2) ((1 - ρ1) ^ 2 * (1 - ρ2))
  have key := rule_k_or_k3 s k
  have e3 : k + 2 + 1 = k + 3 := by omega
  simp only [aliveProb, bin, sum_range_succ, sum_range_zero, zero_add, Nat.choose, add_zero, e3,
    Nat.cast_one, Nat.cast_ofNat, pow_zero, pow_one, one_mul, mul_one, Nat.sub_zero, Nat.sub_self]
  norm_num
  rcases key with hk | hk <;> simp only [hk] <;> split_ifs <;> refine ⟨?_, ?_, ?_⟩ <;>
    first | contradiction | linarith | (left; linarith) | (right; linarith)

namespace Face
variable (F : Face) (ρ1 ρ2 : ℚ)

theorem a_all (hc : ∀ q, F.coin q = true) (x i : ℕ) :
    F.a ρ1 ρ2 x i = aliveProb ρ1 ρ2 2 1 (F.k x i) (x.testBit i) := by
  rw [a, (coins_of_all F hc i).1, (coins_of_all F hc i).2]

theorem a_empty (hc : ∀ q, F.coin q = true) (i : ℕ) : F.a ρ1 ρ2 0 i = 0 := by
  rw [a_all F ρ1 ρ2 hc]
  have hk : F.k 0 i = 0 := by simp [k]
  rw [hk]
  simp [aliveProb, sum_range_succ, rule, Nat.testBit]

/-- The empty face is absorbing: from it, every non-empty state has probability 0. -/
theorem P_empty_row (hc : ∀ q, F.coin q = true) (y : Fin (2 ^ F.A)) (hy : (y : ℕ) ≠ 0) :
    F.P ρ1 ρ2 F.empty y = 0 := by
  obtain ⟨i, hi⟩ := Nat.exists_testBit_of_ne_zero hy
  have hiA : i < F.A := by
    by_contra hcon
    have := Nat.ge_two_pow_of_testBit hi
    have : 2 ^ F.A ≤ 2 ^ i := Nat.pow_le_pow_right (by norm_num) (by omega)
    have := y.isLt
    omega
  exact prod_eq_zero (mem_range.mpr hiA) (by simp [hi, empty, a_empty F ρ1 ρ2 hc i])

theorem survival_succ (t : ℕ) (x : Fin (2 ^ F.A)) :
    F.survival ρ1 ρ2 (t + 1) x = ∑ y, F.P ρ1 ρ2 x y * F.survival ρ1 ρ2 t y := by
  simp only [survival]
  rw [pow_succ', ← Matrix.mulVec_mulVec]
  rfl

theorem survival_empty (hc : ∀ q, F.coin q = true) : ∀ t, F.survival ρ1 ρ2 t F.empty = 0
  | 0 => by simp [survival, live, empty]
  | t + 1 => by
      rw [survival_succ]
      refine sum_eq_zero fun y _ => ?_
      by_cases hy : (y : ℕ) = 0
      · have : y = F.empty := Fin.ext hy
        rw [this, survival_empty hc t, mul_zero]
      · rw [P_empty_row F ρ1 ρ2 hc y hy, zero_mul]

end Face

/-- The constant of Theorem 1: e^{-ε_max} = min(ρ1² ρ2, (1 - ρ1)² (1 - ρ2)). -/
def delta0 (ρ1 ρ2 : ℚ) : ℚ := min (ρ1 ^ 2 * ρ2) ((1 - ρ1) ^ 2 * (1 - ρ2))

theorem death_ge (F : Face) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (hc : ∀ q, F.coin q = true) (x : Fin (2 ^ F.A)) : delta0 ρ1 ρ2 ^ F.A ≤ F.death ρ1 ρ2 x := by
  have r1 : 0 ≤ 1 - ρ1 := by linarith
  have r2 : 0 ≤ 1 - ρ2 := by linarith
  have e : delta0 ρ1 ρ2 ^ F.A = ∏ _i ∈ range F.A, delta0 ρ1 ρ2 := by rw [prod_const, card_range]
  rw [Face.death, e]
  refine prod_le_prod₀ (fun i _ => ?_) (fun i _ => ?_)
  · simp only [delta0]; exact le_min (by positivity) (by positivity)
  · rw [Face.a_all F ρ1 ρ2 hc]; exact (death_cell ρ1 ρ2 h1 h1' h2 h2' _ _).2.2

/-- **Theorem 1, survival form, for every face with all its coins** (every wrapped face and strip, every size):
P_x(T > t) ≤ (1 - delta0 ^ A) ^ t for every state and every t. -/
theorem survival_le_all (F : Face) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (hc : ∀ q, F.coin q = true) : ∀ (t : ℕ) (x : Fin (2 ^ F.A)),
    F.survival ρ1 ρ2 t x ≤ (1 - delta0 ρ1 ρ2 ^ F.A) ^ t
  | 0, x => by
      simp only [Face.survival, pow_zero, Matrix.one_mulVec, Face.live]
      split <;> norm_num
  | t + 1, x => by
      have hP : ∀ y, 0 ≤ F.P ρ1 ρ2 x y := fun y => prod_nonneg fun i _ => by
        have := death_cell ρ1 ρ2 h1 h1' h2 h2' (F.k x i) ((x : ℕ).testBit i)
        rw [Face.a_all F ρ1 ρ2 hc]; split <;> linarith [this.1, this.2.1]
      set B := (1 - delta0 ρ1 ρ2 ^ F.A) ^ t
      have hB : ∀ y, F.survival ρ1 ρ2 t y ≤ B - (if y = F.empty then B else 0) := by
        intro y
        split
        · rename_i h; rw [h, Face.survival_empty F ρ1 ρ2 hc]; simp
        · simpa using survival_le_all F ρ1 ρ2 h1 h1' h2 h2' hc t y
      rw [Face.survival_succ]
      calc ∑ y, F.P ρ1 ρ2 x y * F.survival ρ1 ρ2 t y
          ≤ ∑ y, F.P ρ1 ρ2 x y * (B - (if y = F.empty then B else 0)) :=
            sum_le_sum fun y _ => mul_le_mul_of_nonneg_left (hB y) (hP y)
        _ = B * (1 - F.death ρ1 ρ2 x) := by
            simp only [mul_sub, mul_ite, mul_zero, sum_sub_distrib, sum_ite_eq', mem_univ, ite_true]
            rw [← sum_mul, Face.P_row_sum, Face.P_zero_col]; ring
        _ ≤ B * (1 - delta0 ρ1 ρ2 ^ F.A) := by
            have hB0 : 0 ≤ B := by
              have := survival_le_all F ρ1 ρ2 h1 h1' h2 h2' hc t F.empty
              rw [Face.survival_empty F ρ1 ρ2 hc] at this; exact this
            have := death_ge F ρ1 ρ2 h1 h1' h2 h2' hc x
            nlinarith
        _ = (1 - delta0 ρ1 ρ2 ^ F.A) ^ (t + 1) := by rw [pow_succ]

/-- **Theorem 1, eigenvalue form**: every quasi-stationary law (μ, λ) of a face with all its coins has
λ ≤ 1 - delta0 ^ A. -/
theorem qsd_le_all (F : Face) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (hc : ∀ q, F.coin q = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) :
    lam ≤ 1 - ((delta0 ρ1 ρ2 ^ F.A : ℚ) : ℝ) := by
  -- the vector 1 off the empty state: Σ_x μ(x) (P v)(x) = λ Σ_x μ(x) v(x) = λ
  set v : Fin (2 ^ F.A) → ℚ := F.live
  have hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → v y = 0 := fun y hy => by simp [v, Face.live, hy]
  have hpair := Data.qsd_pair F ρ1 ρ2 μ lam hq v hv0
  have hmass : ∑ y, μ y * (v y : ℝ) = 1 := by
    rw [← hq.total]; refine sum_congr rfl fun y _ => ?_
    by_cases hy : (y : ℕ) = 0
    · simp [v, Face.live, hy, hq.empty y hy]
    · simp [v, Face.live, hy]
  have hrow : ∀ x : Fin (2 ^ F.A), ((F.P ρ1 ρ2 *ᵥ v) x : ℝ) ≤ 1 - ((delta0 ρ1 ρ2 ^ F.A : ℚ) : ℝ) := by
    intro x
    have hP : ∀ y, 0 ≤ F.P ρ1 ρ2 x y := fun y => prod_nonneg fun i _ => by
      have := death_cell ρ1 ρ2 h1 h1' h2 h2' (F.k x i) ((x : ℕ).testBit i)
      rw [Face.a_all F ρ1 ρ2 hc]; split <;> linarith [this.1, this.2.1]
    have e : (F.P ρ1 ρ2 *ᵥ v) x = 1 - F.death ρ1 ρ2 x := by
      have : v = fun y => 1 - (if y = F.empty then 1 else 0) := by
        funext y; simp only [v, Face.live]
        by_cases hy : (y : ℕ) = 0
        · have : y = F.empty := Fin.ext hy
          rw [ite_eq_left_iff.mpr (fun h => absurd this h)]; simp [hy]
        · have : y ≠ F.empty := fun h => hy (by rw [h]; rfl)
          rw [if_neg this]; simp [hy]
      rw [this]
      simp only [mulVec, dotProduct, mul_sub, mul_one, mul_ite, mul_zero, sum_sub_distrib, sum_ite_eq',
        mem_univ, ite_true, Face.P_row_sum, Face.P_zero_col]
    have := death_ge F ρ1 ρ2 h1 h1' h2 h2' hc x
    rw [e]; push_cast; exact_mod_cast (by linarith : 1 - F.death ρ1 ρ2 x ≤ 1 - delta0 ρ1 ρ2 ^ F.A)
  have : ∑ x, μ x * ((F.P ρ1 ρ2 *ᵥ v) x : ℝ) ≤ ∑ x, μ x * (1 - ((delta0 ρ1 ρ2 ^ F.A : ℚ) : ℝ)) :=
    sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (hrow x) (hq.nonneg x)
  rw [hpair, hmass, ← sum_mul, hq.total] at this
  linarith

/-- **Theorem 1 at (0.44, 0.42), in nats**: for every face with all its coins and every quasi-stationary
law (μ, λ) with λ < 1, ln τ = -ln(1 - λ) < 2.5095 · A. -/
theorem lntau_le_all (F : Face) (hc : ∀ q, F.coin q = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ)
    (hq : IsQSD F ρ1 ρ2 μ lam) (hA : 0 < F.A) :
    -Real.log (1 - lam) < 2.5095 * F.A := by
  have hl := qsd_le_all F ρ1 ρ2 (by norm_num [ρ1]) (by norm_num [ρ1]) (by norm_num [ρ2]) (by norm_num [ρ2]) hc μ lam hq
  have hδ : delta0 ρ1 ρ2 = 0.081312 := by norm_num [delta0, ρ1, ρ2]
  rw [hδ] at hl
  push_cast at hl
  have hpos : (0 : ℝ) < 0.081312 ^ F.A := by positivity
  have h1 : (0.081312 : ℝ) ^ F.A ≤ 1 - lam := by linarith
  have hlog : -Real.log (1 - lam) ≤ -Real.log ((0.081312 : ℝ) ^ F.A) := by
    have := Real.log_le_log hpos h1; linarith
  rw [Real.log_pow] at hlog
  -- -ln 0.081312 < 2.5095
  have hb : -Real.log (0.081312 : ℝ) < 2.5095 := by
    refine neg_log_lt _ _ 3 (by norm_num) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_ ?_
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  have hA' : (0 : ℝ) < F.A := by exact_mod_cast hA
  nlinarith

end Gump.Dice
