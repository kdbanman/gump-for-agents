/-
The death time from a quasi-stationary law is geometric: P_μ(T > t) = Σ_x μ(x) P_x(T > t) = λ ^ t (`qsd_survival`),
so τ = E_μ T = Σ_t P_μ(T > t) = 1 / (1 - λ) (`qsd_mean`). This is the identity `DiceLife.lean`'s header cites as
`qsd_survival`, which did not exist at a65957b. Credit: proved by the referee `ref-dice`
(`research/blast/ref-dice/QsdSurvival.lean`, commit 003cb73), taken over here unchanged except for the namespace,
plus the instance for every hull face (`qsd_mean_hull`, from `DiceHull.lean`'s absorbing ∅). Added 2026-11-24.
-/
import GumpMath.DiceHull3
import GumpMath.DiceBound
import GumpMath.DiceHull
import Mathlib.Analysis.SpecificLimits.Basic

namespace Gump.Dice
open Gump Finset Matrix

theorem survival_zero_of_absorbing (F : Face) (ρ1 ρ2 : ℚ)
    (h0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → F.P ρ1 ρ2 F.empty y = 0) : ∀ t, F.survival ρ1 ρ2 t F.empty = 0
  | 0 => by simp [Face.survival, Face.live, Face.empty]
  | t + 1 => by
      rw [Face.survival_succ]
      refine sum_eq_zero fun y _ => ?_
      by_cases hy : (y : ℕ) = 0
      · have : y = F.empty := Fin.ext hy
        rw [this, survival_zero_of_absorbing F ρ1 ρ2 h0 t, mul_zero]
      · rw [h0 y hy, zero_mul]

theorem qsd_survival (F : Face) (ρ1 ρ2 : ℚ) (h0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → F.P ρ1 ρ2 F.empty y = 0)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) :
    ∀ t : ℕ, ∑ x, μ x * (F.survival ρ1 ρ2 t x : ℝ) = lam ^ t
  | 0 => by
      simp only [Face.survival, pow_zero, Matrix.one_mulVec]
      rw [← hq.total]
      refine sum_congr rfl fun x _ => ?_
      by_cases hx : (x : ℕ) = 0
      · simp [Face.live, hx, hq.empty x hx]
      · simp [Face.live, hx]
  | t + 1 => by
      have h := Data.qsd_pair F ρ1 ρ2 μ lam hq (F.survival ρ1 ρ2 t) (fun y hy => by
        have : y = F.empty := Fin.ext hy
        rw [this]; exact survival_zero_of_absorbing F ρ1 ρ2 h0 t)
      have e : ∀ x, (F.P ρ1 ρ2 *ᵥ F.survival ρ1 ρ2 t) x = F.survival ρ1 ρ2 (t + 1) x := fun x => by
        rw [Face.survival_succ]; rfl
      simp only [e] at h
      rw [h, qsd_survival F ρ1 ρ2 h0 μ lam hq t, pow_succ]
      ring

/-- E_μ T = Σ_t P_μ(T > t) = 1 / (1 - λ). -/
theorem qsd_mean (F : Face) (ρ1 ρ2 : ℚ) (h0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → F.P ρ1 ρ2 F.empty y = 0)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam) (hl0 : 0 ≤ lam) (hl1 : lam < 1) :
    ∑' t : ℕ, ∑ x, μ x * (F.survival ρ1 ρ2 t x : ℝ) = 1 / (1 - lam) := by
  simp_rw [qsd_survival F ρ1 ρ2 h0 μ lam hq]
  rw [tsum_geometric_of_lt_one hl0 hl1, one_div]

/-- Faces with all their coins. -/
theorem qsd_mean_all (F : Face) (ρ1 ρ2 : ℚ) (hc : ∀ q, F.coin q = true) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ)
    (hq : IsQSD F ρ1 ρ2 μ lam) (hl0 : 0 ≤ lam) (hl1 : lam < 1) :
    ∑' t : ℕ, ∑ x, μ x * (F.survival ρ1 ρ2 t x : ℝ) = 1 / (1 - lam) :=
  qsd_mean F ρ1 ρ2 (fun y hy => Face.P_empty_row F ρ1 ρ2 hc y hy) μ lam hq hl0 hl1

/-- The 9-cell hull face: ∅ absorbing from its kernel-checked tables. -/
theorem hull3_empty_row (y : Fin (2 ^ (hull 3).A)) (hy : (y : ℕ) ≠ 0) : (hull 3).P ρ1 ρ2 (hull 3).empty y = 0 := by
  rw [Hull3Data.hρ1, Hull3Data.hρ2]
  exact Hull3Data.data.P_sure (hull 3) Hull3Data.tab (hull 3).empty y (by decide +kernel) hy

theorem hull3_mean (μ : Fin (2 ^ (hull 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull 3) ρ1 ρ2 μ lam) :
    ∑' t : ℕ, ∑ x, μ x * ((hull 3).survival ρ1 ρ2 t x : ℝ) = 1 / (1 - lam) := by
  obtain ⟨l1, l2, -, -⟩ := hull3_tau μ lam hq
  exact qsd_mean (hull 3) ρ1 ρ2 hull3_empty_row μ lam hq (by linarith) (by linarith)

/-- Every hull face: E_μ T = 1 / (1 - λ) for every quasi-stationary law with 0 ≤ λ < 1. -/
theorem qsd_mean_hull (R : ℕ) (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam)
    (hl0 : 0 ≤ lam) (hl1 : lam < 1) :
    ∑' t : ℕ, ∑ x, μ x * ((hull R).survival ρ1 ρ2 t x : ℝ) = 1 / (1 - lam) :=
  qsd_mean (hull R) ρ1 ρ2 (fun y hy => Face.hull_P_empty_row R ρ1 ρ2 y hy) μ lam hq hl0 hl1

end Gump.Dice
