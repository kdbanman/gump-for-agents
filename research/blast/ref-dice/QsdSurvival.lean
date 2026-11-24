/-
ref-dice: the identity that DiceLife.lean's header cites as `qsd_survival` (no such theorem at a65957b): from a
quasi-stationary law the death time is geometric, P_μ(T > t) = Σ_x μ(x) P_x(T > t) = λ ^ t, hence
E_μ T = Σ_t P_μ(T > t) = 1 / (1 - λ). Proved for every face on which ∅ is absorbing (`qsd_survival`), instantiated
for faces with all their coins and for `hull 3` (whose ∅ row is read off its checked tables). Written by the referee
to show the gap is small; not part of the dice arm's files.
  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-dice/QsdSurvival.lean
-/
import GumpMath.DiceHull3
import GumpMath.DiceBound
import Mathlib.Analysis.SpecificLimits.Basic

namespace RefDice
open Gump Gump.Dice Finset Matrix

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

#print axioms qsd_mean_all
#print axioms hull3_mean

end RefDice
