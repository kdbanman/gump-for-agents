/-
The constant of Theorem 1 (`research/blast/rigour/THEOREMS.md`): one cell of the one-layer dice surrogate.

A cell with three coins (two of density ρ1, one of density ρ2) and k ≤ 6 live in-layer neighbours is alive
next under B45/S345 with n = k + b, b the number of heads.  Every death event of such a cell contains the
atom b = 0 or the atom b = 3 (`threeCoins_death_ge`), so its death probability is at least
min(ρ1²ρ2, (1-ρ1)²(1-ρ2)).  A hull corner (two coins of density ρ1, k ≤ 2) obeys the same bound
(`twoCoins_death_ge`).  Hence ε_max ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)), and with Theorem 1:
  `upper_bound_coins`: log τ ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) · A for every face whose cells are of these
                       two kinds;
  `emax_main`:  -log(0.44² · 0.42) ≤ 2.51   (the source's "2.509" is the truncation of 2.50946…);
  `emax_fair`:  -log(1/8) ≤ 2.08            (fair coins; the source's 2.079).
-/
import Mathlib
import GumpMath.ChainTilt

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Real

/-- gump's rule B45/S345: alive next iff (dead and n ∈ {4,5}) or (alive and n ∈ {3,4,5}). -/
def aliveNext (alive : Bool) (n : ℕ) : Bool :=
  if alive then decide (3 ≤ n ∧ n ≤ 5) else decide (n = 4 ∨ n = 5)

/-- The law of the number of heads of two coins of density ρ1 and one of density ρ2. -/
def coin3 (ρ1 ρ2 : ℝ) : ℕ → ℝ
  | 0 => (1 - ρ1) ^ 2 * (1 - ρ2)
  | 1 => 2 * ρ1 * (1 - ρ1) * (1 - ρ2) + (1 - ρ1) ^ 2 * ρ2
  | 2 => ρ1 ^ 2 * (1 - ρ2) + 2 * ρ1 * (1 - ρ1) * ρ2
  | 3 => ρ1 ^ 2 * ρ2
  | _ => 0

/-- The law of the number of heads of two coins of density ρ1 (a hull corner). -/
def coin2 (ρ1 : ℝ) : ℕ → ℝ
  | 0 => (1 - ρ1) ^ 2
  | 1 => 2 * ρ1 * (1 - ρ1)
  | 2 => ρ1 ^ 2
  | _ => 0

/-- Probability that a three-coin cell is dead next. -/
def death3 (ρ1 ρ2 : ℝ) (alive : Bool) (k : ℕ) : ℝ :=
  ∑ b ∈ range 4, if aliveNext alive (k + b) then 0 else coin3 ρ1 ρ2 b

/-- Probability that a two-coin cell is dead next. -/
def death2 (ρ1 : ℝ) (alive : Bool) (k : ℕ) : ℝ :=
  ∑ b ∈ range 3, if aliveNext alive (k + b) then 0 else coin2 ρ1 b

theorem coin3_total (ρ1 ρ2 : ℝ) : ∑ b ∈ range 4, coin3 ρ1 ρ2 b = 1 := by
  simp [Finset.sum_range_succ, coin3]; ring

theorem coin2_total (ρ1 : ℝ) : ∑ b ∈ range 3, coin2 ρ1 b = 1 := by
  simp [Finset.sum_range_succ, coin2]; ring

/-- The smallest atom: min(ρ1²ρ2, (1-ρ1)²(1-ρ2)). -/
noncomputable def atomMin (ρ1 ρ2 : ℝ) : ℝ := min (ρ1 ^ 2 * ρ2) ((1 - ρ1) ^ 2 * (1 - ρ2))

theorem atomMin_pos {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1) :
    0 < atomMin ρ1 ρ2 := by
  unfold atomMin
  apply lt_min
  · positivity
  · have : 0 < 1 - ρ1 := by linarith
    have : 0 < 1 - ρ2 := by linarith
    positivity

/-- **Every death of a three-coin cell contains b = 0 or b = 3.** -/
theorem threeCoins_death_ge {ρ1 ρ2 : ℝ} (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (alive : Bool) (k : ℕ) (hk : k ≤ 6) : atomMin ρ1 ρ2 ≤ death3 ρ1 ρ2 alive k := by
  have a : 0 ≤ 1 - ρ1 := by linarith
  have b : 0 ≤ 1 - ρ2 := by linarith
  have p0 : 0 ≤ (1 - ρ1) ^ 2 * (1 - ρ2) := by positivity
  have p1 : 0 ≤ 2 * ρ1 * (1 - ρ1) * (1 - ρ2) + (1 - ρ1) ^ 2 * ρ2 := by positivity
  have p2 : 0 ≤ ρ1 ^ 2 * (1 - ρ2) + 2 * ρ1 * (1 - ρ1) * ρ2 := by positivity
  have p3 : 0 ≤ ρ1 ^ 2 * ρ2 := by positivity
  unfold atomMin
  rw [min_le_iff]
  interval_cases k <;> cases alive <;>
    simp [death3, Finset.sum_range_succ, aliveNext, coin3] <;>
    first
    | (left; linarith)
    | (right; linarith)

/-- A hull corner (two coins of density ρ1, at most two neighbours) obeys the same bound. -/
theorem twoCoins_death_ge {ρ1 ρ2 : ℝ} (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (alive : Bool) (k : ℕ) (hk : k ≤ 2) : atomMin ρ1 ρ2 ≤ death2 ρ1 alive k := by
  have a : 0 ≤ 1 - ρ1 := by linarith
  have b : 0 ≤ 1 - ρ2 := by linarith
  have q0 : (1 - ρ1) ^ 2 * (1 - ρ2) ≤ (1 - ρ1) ^ 2 := by
    have : 0 ≤ (1 - ρ1) ^ 2 := by positivity
    nlinarith
  have q1 : 0 ≤ 2 * ρ1 * (1 - ρ1) := by positivity
  have q2 : (1 - ρ1) ^ 2 * (1 - ρ2) ≤ (1 - ρ1) ^ 2 + 2 * ρ1 * (1 - ρ1) := by linarith
  have q3 : 0 ≤ ρ1 ^ 2 := by positivity
  unfold atomMin
  rw [min_le_iff]
  interval_cases k <;> cases alive <;>
    simp [death2, Finset.sum_range_succ, aliveNext, coin2] <;>
    (right; nlinarith)

namespace KilledChain
variable {σ : Type*} [Fintype σ] [DecidableEq σ] {K : KilledChain σ}

/-- **Theorem 1 with its constant.**  If every local death factor is at least the smallest atom
(as `threeCoins_death_ge` and `twoCoins_death_ge` give for the surrogate's cells), then
log τ ≤ -log min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) · A. -/
theorem upper_bound_coins {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1)
    (hdc : ∀ i x, atomMin ρ1 ρ2 ≤ L.dc i x) :
    log (K.lifetime μ) ≤ -log (atomMin ρ1 ρ2) * Fintype.card V := by
  have hm := atomMin_pos h1 h1' h2 h2'
  have hmax : ∀ i x, L.cost i x ≤ -log (atomMin ρ1 ρ2) := fun i x => by
    simp only [LocalDeath.cost, neg_le_neg_iff]
    exact log_le_log hm (hdc i x)
  obtain ⟨h, h'⟩ := upper_bound L hμ _ hmax
  linarith

end KilledChain

/-- At the main densities (0.44, 0.42): the smallest atom is 0.44² · 0.42 = 0.081312. -/
theorem atomMin_main : atomMin 0.44 0.42 = 0.44 ^ 2 * 0.42 := by
  unfold atomMin; rw [min_eq_left]; norm_num

/-- ε_max ≤ 2.51 at (0.44, 0.42). -/
theorem emax_main : -log (atomMin 0.44 0.42) ≤ 2.51 := by
  rw [atomMin_main, neg_le]
  have hpos : (0:ℝ) < 0.44 ^ 2 * 0.42 := by norm_num
  rw [le_log_iff_exp_le hpos]
  have hs := sum_le_exp_of_nonneg (x := (2.51 : ℝ)) (by norm_num) 16
  have h : 1 ≤ (0.44 ^ 2 * 0.42) * ∑ i ∈ range 16, (2.51 : ℝ) ^ i / (i.factorial) := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    norm_num
  rw [exp_neg]
  rw [inv_le_iff_one_le_mul₀ (exp_pos _)]
  nlinarith [exp_pos (2.51 : ℝ)]

/-- ε_max ≤ 2.08 at fair coins (½, ½), where both atoms are 1/8. -/
theorem emax_fair : -log (atomMin 0.5 0.5) ≤ 2.08 := by
  have e : atomMin 0.5 0.5 = 1 / 8 := by unfold atomMin; norm_num
  rw [e, neg_le]
  rw [le_log_iff_exp_le (by norm_num)]
  have hs := sum_le_exp_of_nonneg (x := (2.08 : ℝ)) (by norm_num) 14
  have h : 1 ≤ (1 / 8) * ∑ i ∈ range 14, (2.08 : ℝ) ^ i / (i.factorial) := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    norm_num
  rw [exp_neg, inv_le_iff_one_le_mul₀ (exp_pos _)]
  nlinarith [exp_pos (2.08 : ℝ)]

end Gump.Chain
