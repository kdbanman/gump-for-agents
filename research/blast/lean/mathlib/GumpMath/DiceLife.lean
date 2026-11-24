/-
From checked certificates to statements about the lifetime of a face of the dice surrogate.

`lifetime_of_cert`: two vectors that pass the kernel's row checks give, for every t,
  (w(x₀)/w_max) · μ_lo ^ t ≤ P_{x₀}(T > t)   and   P_x(T > t) ≤ (v_max/v_min) · λ_up ^ t for every x.

`qsd_bounds`: for every quasi-stationary law (μ, λ) of the chain (`IsQSD`, over ℝ), μ_lo ≤ λ ≤ λ_up.
`rigour/README.md` defines τ := E_μ T = 1/h, h = 1 - λ, for the quasi-stationary law μ (unique there by
Lemma 0 on wrapped faces, numerically on the others); from μ the death time is geometric,
P_μ(T > t) = λ ^ t (`qsd_survival`), so ln τ = -ln(1 - λ), and the bounds on λ are bounds on ln τ.
-/
import GumpMath.DiceCert
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Rat.BigOperators
import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Ring.Finset

namespace Gump.Dice
open Gump Finset Matrix

/-- A quasi-stationary law of the killed chain: a probability vector μ on the non-empty states, a left
eigenvector of the chain restricted to them, Σ_x μ(x) P(x, y) = λ μ(y) for every non-empty y. -/
structure IsQSD (F : Face) (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) : Prop where
  nonneg : ∀ x, 0 ≤ μ x
  empty : ∀ x : Fin (2 ^ F.A), (x : ℕ) = 0 → μ x = 0
  total : ∑ x, μ x = 1
  eigen : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → ∑ x, μ x * (F.P ρ1 ρ2 x y : ℝ) = lam * μ y

namespace Data
variable (c : Data) (F : Face)

/-- The vector checks: v(0) = 0 and v_min ≤ v(y) ≤ v_max off the empty state. -/
def vecOK (V : Tree) (A lo hi : ℕ) : Bool :=
  allRows (fun y => if y = 0 then V.get A y == 0 else decide (lo ≤ V.get A y) && decide (V.get A y ≤ hi)) (2 ^ A)

theorem vecOK_spec (V : Tree) (A lo hi : ℕ) (h : vecOK V A lo hi = true) (y : Fin (2 ^ A)) :
    ((y : ℕ) = 0 → vec V A y = 0) ∧ ((y : ℕ) ≠ 0 → (lo : ℚ) ≤ vec V A y ∧ vec V A y ≤ hi) := by
  have hy := allRows_spec _ _ h y y.isLt
  constructor
  · intro h0
    simp only [h0, ite_true, beq_iff_eq] at hy
    simp only [vec, h0, hy, Nat.cast_zero]
  · intro h0
    simp only [h0, ite_false, Bool.and_eq_true, decide_eq_true_eq] at hy
    simp only [vec]
    exact ⟨by exact_mod_cast hy.1, by exact_mod_cast hy.2⟩

/-- **Lifetime from a certificate.** Upper vector `Vu` (bounds `vmin ≤ Vu ≤ vmax` off the empty state, ratio
`Lu / Mu`), lower vector `Vl` (`0 ≤ Vl ≤ wmax`, ratio `Ll / Ml`), both checked row by row. -/
theorem lifetime_of_cert (Vu Vl : Tree) (Lu Mu Ll Ml vmin vmax wmax : ℕ)
    (htab : c.tabOK F = true)
    (hup : allRows (c.rowUp F.A (c.Dt F.A) Lu Mu Vu) (2 ^ F.A) = true)
    (hlo : allRows (c.rowLo F.A (c.Dt F.A) Ll Ml Vl) (2 ^ F.A) = true)
    (hvu : vecOK Vu F.A vmin vmax = true) (hvl : vecOK Vl F.A 0 wmax = true)
    (hMu : 0 < Mu) (hMl : 0 < Ml) (hvmin : 0 < vmin) (hwmax : 0 < wmax) (t : ℕ) :
    (∀ x, ((vec Vl F.A x) / wmax) * ((Ll : ℚ) / Ml) ^ t ≤
        F.survival ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) t x) ∧
    ∀ x, F.survival ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) t x ≤ ((vmax : ℚ) / vmin) * ((Lu : ℚ) / Mu) ^ t := by
  have hP := c.P_nonneg F htab
  have hvmin' : (0 : ℚ) < vmin := by exact_mod_cast hvmin
  have hwmax' : (0 : ℚ) < wmax := by exact_mod_cast hwmax
  constructor
  · intro x
    have key := survival_ge_of _ hP F.live (vec Vl F.A) ((Ll : ℚ) / Ml) (wmax : ℚ) (by positivity)
      (c.rows_lo F htab Vl Ll Ml hMl hlo)
      (fun y => by
        obtain ⟨h0, h1⟩ := vecOK_spec Vl F.A 0 wmax hvl y
        by_cases hy : (y : ℕ) = 0
        · rw [h0 hy]; simp [Face.live, hy]
        · rw [show F.live y = 1 by simp [Face.live, hy], mul_one]; exact (h1 hy).2) t x
    rw [Face.survival, div_mul_eq_mul_div, div_le_iff₀ hwmax', mul_comm _ (wmax : ℚ)]
    linarith
  · intro x
    have key := survival_le_of _ hP F.live (vec Vu F.A) ((Lu : ℚ) / Mu) (1 / (vmin : ℚ)) (by positivity)
      (by positivity) (c.rows_up F htab Vu Lu Mu hMu hup)
      (fun y => by
        obtain ⟨h0, h1⟩ := vecOK_spec Vu F.A vmin vmax hvu y
        by_cases hy : (y : ℕ) = 0
        · rw [h0 hy]; simp [Face.live, hy]
        · rw [show F.live y = 1 by simp [Face.live, hy], one_div_mul_eq_div, le_div_iff₀ hvmin', one_mul]
          exact (h1 hy).1) t x
    rw [Face.survival]
    have hvx : vec Vu F.A x ≤ vmax := by
      obtain ⟨h0, h1⟩ := vecOK_spec Vu F.A vmin vmax hvu x
      by_cases hx : (x : ℕ) = 0
      · rw [h0 hx]; positivity
      · exact (h1 hx).2
    calc ((F.P _ _ ^ t) *ᵥ F.live) x ≤ 1 / (vmin : ℚ) * (((Lu : ℚ) / Mu) ^ t * vec Vu F.A x) := key
      _ ≤ 1 / (vmin : ℚ) * (((Lu : ℚ) / Mu) ^ t * vmax) := by gcongr
      _ = ((vmax : ℚ) / vmin) * ((Lu : ℚ) / Mu) ^ t := by ring

/-- For a quasi-stationary law and a vector v with v(0) = 0, Σ_x μ(x) (P v)(x) = λ Σ_x μ(x) v(x). -/
theorem qsd_pair (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam)
    (v : Fin (2 ^ F.A) → ℚ) (hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → v y = 0) :
    ∑ x, μ x * ((F.P ρ1 ρ2 *ᵥ v) x : ℝ) = lam * ∑ y, μ y * (v y : ℝ) := by
  simp only [mulVec, dotProduct, Rat.cast_sum, Rat.cast_mul]
  simp_rw [mul_sum]
  rw [sum_comm]
  refine sum_congr rfl fun y _ => ?_
  by_cases hy : (y : ℕ) = 0
  · simp [hv0 y hy]
  · have := hq.eigen y hy
    calc ∑ x, μ x * ((F.P ρ1 ρ2 x y : ℝ) * (v y : ℝ)) = (∑ x, μ x * (F.P ρ1 ρ2 x y : ℝ)) * (v y : ℝ) := by
          rw [sum_mul]; exact sum_congr rfl fun x _ => by ring
      _ = lam * (μ y * (v y : ℝ)) := by rw [this]; ring

/-- Σ_x μ(x) v(x) ≥ lo when v ≥ lo off the empty state and μ is a probability on the non-empty states. -/
theorem qsd_mass (ρ1 ρ2 : ℚ) (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ρ1 ρ2 μ lam)
    (v : Fin (2 ^ F.A) → ℚ) (lo : ℚ) (hv : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → lo ≤ v y) :
    (lo : ℝ) ≤ ∑ y, μ y * (v y : ℝ) := by
  calc (lo : ℝ) = ∑ y, μ y * (lo : ℝ) := by rw [← sum_mul, hq.total, one_mul]
    _ ≤ ∑ y, μ y * (v y : ℝ) := by
        refine sum_le_sum fun y _ => ?_
        by_cases hy : (y : ℕ) = 0
        · simp [hq.empty y hy]
        · exact mul_le_mul_of_nonneg_left (by exact_mod_cast hv y hy) (hq.nonneg y)

/-- **The quasi-stationary eigenvalue lies between the certified bounds** (when the lower vector is
positive off the empty state). -/
theorem qsd_bounds (Vu Vl : Tree) (Lu Mu Ll Ml vmin vmax wmin wmax : ℕ)
    (htab : c.tabOK F = true)
    (hup : allRows (c.rowUp F.A (c.Dt F.A) Lu Mu Vu) (2 ^ F.A) = true)
    (hlo : allRows (c.rowLo F.A (c.Dt F.A) Ll Ml Vl) (2 ^ F.A) = true)
    (hvu : vecOK Vu F.A vmin vmax = true) (hvl : vecOK Vl F.A wmin wmax = true)
    (hMu : 0 < Mu) (hMl : 0 < Ml) (hvmin : 0 < vmin) (hwmin : 0 < wmin)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) μ lam) :
    ((Ll : ℚ) / Ml : ℝ) ≤ lam ∧ lam ≤ ((Lu : ℚ) / Mu : ℝ) := by
  have hμ := hq.nonneg
  constructor
  · have hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → vec Vl F.A y = 0 := fun y => (vecOK_spec Vl F.A _ _ hvl y).1
    have hpair := qsd_pair F _ _ μ lam hq (vec Vl F.A) hv0
    have hS := qsd_mass F _ _ μ lam hq (vec Vl F.A) wmin fun y hy => (vecOK_spec Vl F.A _ _ hvl y).2 hy |>.1
    have hwmin' : (0 : ℝ) < wmin := by exact_mod_cast hwmin
    have hrow : ∑ x, μ x * (((Ll : ℚ) / Ml * vec Vl F.A x : ℚ) : ℝ) ≤
        ∑ x, μ x * ((F.P _ _ *ᵥ vec Vl F.A) x : ℝ) :=
      sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (by exact_mod_cast c.rows_lo F htab Vl Ll Ml hMl hlo x) (hμ x)
    rw [hpair] at hrow
    have e : ∑ x, μ x * (((Ll : ℚ) / Ml * vec Vl F.A x : ℚ) : ℝ) = ((Ll : ℚ) / Ml : ℝ) * ∑ y, μ y * (vec Vl F.A y : ℝ) := by
      rw [mul_sum]; refine sum_congr rfl fun x _ => ?_; push_cast; ring
    rw [e] at hrow
    have hpos : (0 : ℝ) < ∑ y, μ y * (vec Vl F.A y : ℝ) := by
      have : ((wmin : ℚ) : ℝ) = (wmin : ℝ) := by push_cast; rfl
      linarith
    exact le_of_mul_le_mul_right hrow hpos
  · have hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → vec Vu F.A y = 0 := fun y => (vecOK_spec Vu F.A _ _ hvu y).1
    have hpair := qsd_pair F _ _ μ lam hq (vec Vu F.A) hv0
    have hS := qsd_mass F _ _ μ lam hq (vec Vu F.A) vmin fun y hy => (vecOK_spec Vu F.A _ _ hvu y).2 hy |>.1
    have hvmin' : (0 : ℝ) < vmin := by exact_mod_cast hvmin
    have hrow : ∑ x, μ x * ((F.P _ _ *ᵥ vec Vu F.A) x : ℝ) ≤
        ∑ x, μ x * (((Lu : ℚ) / Mu * vec Vu F.A x : ℚ) : ℝ) :=
      sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (by exact_mod_cast c.rows_up F htab Vu Lu Mu hMu hup x) (hμ x)
    rw [hpair] at hrow
    have e : ∑ x, μ x * (((Lu : ℚ) / Mu * vec Vu F.A x : ℚ) : ℝ) = ((Lu : ℚ) / Mu : ℝ) * ∑ y, μ y * (vec Vu F.A y : ℝ) := by
      rw [mul_sum]; refine sum_congr rfl fun x _ => ?_; push_cast; ring
    rw [e] at hrow
    have hpos : (0 : ℝ) < ∑ y, μ y * (vec Vu F.A y : ℝ) := by
      have : ((vmin : ℚ) : ℝ) = (vmin : ℝ) := by push_cast; rfl
      linarith
    exact le_of_mul_le_mul_right hrow hpos

end Data

end Gump.Dice
