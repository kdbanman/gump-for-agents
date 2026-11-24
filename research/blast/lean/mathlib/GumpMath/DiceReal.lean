/-
Bounds on -ln h from rational bounds on h, for the lifetime corollaries (ln τ = -ln(1 - λ)).
exp a is bounded by its Taylor sums (`Real.exp_bound`) at a/k ≤ 1, raised to the power k.
-/
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic.FieldSimp

namespace Gump.Dice
open Finset

/-- Taylor sum of exp. -/
noncomputable def expSum (x : ℝ) (n : ℕ) : ℝ := ∑ m ∈ range n, x ^ m / m.factorial

/-- The remainder bound of `Real.exp_bound`. -/
noncomputable def expErr (x : ℝ) (n : ℕ) : ℝ := x ^ n * ((n.succ : ℝ) / (n.factorial * n))

theorem exp_le_sum (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) (n : ℕ) (hn : 0 < n) :
    Real.exp x ≤ expSum x n + expErr x n := by
  have := Real.exp_bound (x := x) (by rw [abs_of_nonneg h0]; exact h1) hn
  rw [abs_of_nonneg h0] at this
  have := (abs_sub_le_iff.mp this).1
  unfold expSum expErr; linarith

theorem sum_le_exp (x : ℝ) (h0 : 0 ≤ x) (h1 : x ≤ 1) (n : ℕ) (hn : 0 < n) :
    expSum x n - expErr x n ≤ Real.exp x := by
  have := Real.exp_bound (x := x) (by rw [abs_of_nonneg h0]; exact h1) hn
  rw [abs_of_nonneg h0] at this
  have := (abs_sub_le_iff.mp this).2
  unfold expSum expErr; linarith

theorem exp_pow (x : ℝ) (k : ℕ) : Real.exp (k * x) = Real.exp x ^ k := Real.exp_nat_mul x k

/-- a < -ln h, from an upper bound on exp a (Taylor at a / k, to the power k). -/
theorem lt_neg_log (h a : ℝ) (k : ℕ) (hh : 0 < h) (hk : 0 < k) (ha0 : 0 ≤ a) (ha1 : a ≤ k) (n : ℕ) (hn : 0 < n)
    (key : h * (expSum (a / k) n + expErr (a / k) n) ^ k < 1) : a < -Real.log h := by
  have hk' : (0 : ℝ) < k := by exact_mod_cast hk
  have e1 := exp_le_sum (a / k) (div_nonneg ha0 hk'.le) ((div_le_one hk').mpr ha1) n hn
  have epos := Real.exp_pos (a / k)
  have e3 : Real.exp a ≤ (expSum (a / k) n + expErr (a / k) n) ^ k := by
    have ea : Real.exp a = Real.exp (a / k) ^ k := by rw [← exp_pow]; congr 1; field_simp
    rw [ea]
    exact pow_le_pow_left₀ epos.le e1 k
  have : h * Real.exp a < 1 := lt_of_le_of_lt (mul_le_mul_of_nonneg_left e3 hh.le) key
  have hl : Real.log h < -a := by
    rw [Real.log_lt_iff_lt_exp hh, Real.exp_neg, lt_inv_comm₀ hh (Real.exp_pos a)]
    rw [inv_eq_one_div, lt_div_iff₀ hh]; linarith [mul_comm h (Real.exp a)]
  linarith

/-- -ln h < b, from a lower bound on exp b. -/
theorem neg_log_lt (h b : ℝ) (k : ℕ) (hh : 0 < h) (hk : 0 < k) (hb0 : 0 ≤ b) (hb1 : b ≤ k) (n : ℕ) (hn : 0 < n)
    (hs : 0 ≤ expSum (b / k) n - expErr (b / k) n)
    (key : 1 < h * (expSum (b / k) n - expErr (b / k) n) ^ k) : -Real.log h < b := by
  have hk' : (0 : ℝ) < k := by exact_mod_cast hk
  have e1 := sum_le_exp (b / k) (div_nonneg hb0 hk'.le) ((div_le_one hk').mpr hb1) n hn
  have e3 : (expSum (b / k) n - expErr (b / k) n) ^ k ≤ Real.exp b := by
    have eb : Real.exp b = Real.exp (b / k) ^ k := by rw [← exp_pow]; congr 1; field_simp
    rw [eb]
    exact pow_le_pow_left₀ hs e1 k
  have : 1 < h * Real.exp b := lt_of_lt_of_le key (mul_le_mul_of_nonneg_left e3 hh.le)
  have hl : -b < Real.log h := by
    rw [Real.lt_log_iff_exp_lt hh, Real.exp_neg, inv_lt_comm₀ (Real.exp_pos b) hh]
    rw [inv_eq_one_div, div_lt_iff₀ hh]; linarith [mul_comm h (Real.exp b)]
  linarith

end Gump.Dice
