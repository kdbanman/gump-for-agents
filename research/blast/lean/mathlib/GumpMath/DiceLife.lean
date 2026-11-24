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

/-! ### Faces with states that die surely (the full wrapped face) -/

/-- The checks for an upper vector `V` that is tiny on a set D of states that die surely (`Gs` is the
indicator of D): V(0) = Gs(0) = 0; off the empty state V ≤ hi, and V ≥ lo unless the state is in D. -/
def vecOK2 (V Gs : Tree) (A lo hi : ℕ) : Bool :=
  allRows (fun y => if y = 0 then V.get A y == 0 && Gs.get A y == 0 else
    decide (V.get A y ≤ hi) && (Gs.get A y == 1 || decide (lo ≤ V.get A y))) (2 ^ A)

/-- Every non-empty state where `W` vanishes dies surely (all its alive numerators are 0). -/
def sureOK (W : Tree) (A : ℕ) : Bool :=
  allRows (fun y => y == 0 || W.get A y != 0 || (List.range A).all fun i => c.alpha y i == 0) (2 ^ A)

theorem sureOK_spec (W : Tree) (h : c.sureOK W F.A = true) (y : Fin (2 ^ F.A)) (hy : (y : ℕ) ≠ 0)
    (hw : W.get F.A y = 0) : ∀ i < F.A, c.alpha y i = 0 := by
  have := allRows_spec _ _ h y y.isLt
  simp only [Bool.or_eq_true, beq_iff_eq, bne_iff_ne, ne_eq, List.all_eq_true, List.mem_range] at this
  rcases this with (h1 | h2) | h3
  · exact absurd h1 hy
  · exact absurd hw h2
  · exact h3

/-- **Upper bound on survival with a set of surely-dying states.** -/
theorem survival_up_sure (V Gs : Tree) (L M K N vmin vmax : ℕ) (htab : c.tabOK F = true)
    (hup : allRows (c.rowUp F.A (c.Dt F.A) L M V) (2 ^ F.A) = true)
    (hg : allRows (c.rowLe F.A (c.Dt F.A) K N Gs V) (2 ^ F.A) = true)
    (hv : vecOK2 V Gs F.A vmin vmax = true) (hM : 0 < M) (hN : 0 < N) (hvmin : 0 < vmin) (hL : 0 < L)
    (t : ℕ) (x : Fin (2 ^ F.A)) :
    F.survival ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) (t + 1) x ≤
      ((vmax : ℚ) / vmin + ((K : ℚ) / N) * vmax / ((L : ℚ) / M)) * ((L : ℚ) / M) ^ (t + 1) := by
  set P := F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2)
  have hP := c.P_nonneg F htab
  have hvmin' : (0 : ℚ) < vmin := by exact_mod_cast hvmin
  have hlam : (0 : ℚ) < (L : ℚ) / M := by positivity
  have hkap : (0 : ℚ) ≤ (K : ℚ) / N := by positivity
  have hspec : ∀ y : Fin (2 ^ F.A), ((y : ℕ) = 0 → V.get F.A y = 0 ∧ Gs.get F.A y = 0) ∧
      ((y : ℕ) ≠ 0 → V.get F.A y ≤ vmax ∧ (Gs.get F.A y = 1 ∨ vmin ≤ V.get F.A y)) := by
    intro y
    have := allRows_spec _ _ hv y y.isLt
    constructor
    · intro h0; simp only [h0, ite_true, Bool.and_eq_true, beq_iff_eq] at this
      rw [h0]; exact this
    · intro h0; simp only [h0, ite_false, Bool.and_eq_true, decide_eq_true_eq, Bool.or_eq_true,
        beq_iff_eq] at this
      exact this
  have hvnn : ∀ y, 0 ≤ vec V F.A y := fun y => Nat.cast_nonneg _
  have hvmax : ∀ y, vec V F.A y ≤ vmax := by
    intro y
    by_cases h0 : (y : ℕ) = 0
    · rw [vec, (hspec y).1 h0 |>.1]; positivity
    · simp only [vec]; exact_mod_cast ((hspec y).2 h0).1
  have hlive : ∀ y, F.live y ≤ (1 / (vmin : ℚ)) * vec V F.A y + vec Gs F.A y := by
    intro y
    by_cases h0 : (y : ℕ) = 0
    · rw [show F.live y = 0 by simp [Face.live, h0]]
      have : (0 : ℚ) ≤ vec Gs F.A y := Nat.cast_nonneg _
      have : (0 : ℚ) ≤ 1 / (vmin : ℚ) * vec V F.A y := mul_nonneg (by positivity) (hvnn y)
      linarith
    · rw [show F.live y = 1 by simp [Face.live, h0]]
      rcases ((hspec y).2 h0).2 with hG | hlo
      · rw [vec, vec, hG]; push_cast
        have : 0 ≤ 1 / (vmin : ℚ) * (V.get F.A y : ℚ) := by positivity
        linarith
      · have : (1 : ℚ) ≤ 1 / (vmin : ℚ) * vec V F.A y := by
          rw [vec, one_div_mul_eq_div, le_div_iff₀ hvmin', one_mul]; exact_mod_cast hlo
        have : (0 : ℚ) ≤ vec Gs F.A y := Nat.cast_nonneg _
        linarith
  have hPt := Certificate.pow_nonneg' P hP
  have hv1 := Certificate.pow_mulVec_le P hP (vec V F.A) _ hlam.le (c.rows_up F htab V L M hM hup)
  rw [Face.survival]
  have e1 : ((P ^ (t + 1)) *ᵥ F.live) x ≤
      ((P ^ (t + 1)) *ᵥ fun y => (1 / (vmin : ℚ)) * vec V F.A y + vec Gs F.A y) x :=
    Certificate.mulVec_mono _ (hPt (t + 1)) hlive x
  have e2 : ((P ^ (t + 1)) *ᵥ fun y => (1 / (vmin : ℚ)) * vec V F.A y + vec Gs F.A y) x =
      (1 / (vmin : ℚ)) * ((P ^ (t + 1)) *ᵥ vec V F.A) x + ((P ^ t) *ᵥ (P *ᵥ vec Gs F.A)) x := by
    have e2a : ((P ^ (t + 1)) *ᵥ fun y => (1 / (vmin : ℚ)) * vec V F.A y + vec Gs F.A y) x =
        ((P ^ (t + 1)) *ᵥ fun y => (1 / (vmin : ℚ)) * vec V F.A y) x + ((P ^ (t + 1)) *ᵥ vec Gs F.A) x := by
      simp only [Matrix.mulVec, dotProduct, mul_add, Finset.sum_add_distrib]
    have e2b : (P ^ (t + 1)) *ᵥ vec Gs F.A = (P ^ t) *ᵥ (P *ᵥ vec Gs F.A) := by
      rw [pow_succ, Matrix.mulVec_mulVec]
    rw [e2a, e2b, Certificate.mulVec_smul_fun]
  have e3 : ((P ^ t) *ᵥ (P *ᵥ vec Gs F.A)) x ≤ ((P ^ t) *ᵥ fun y => (K : ℚ) / N * vec V F.A y) x :=
    Certificate.mulVec_mono _ (hPt t) (c.rows_le F htab Gs V K N hN hg) x
  rw [Certificate.mulVec_smul_fun] at e3
  have e4 := hv1 (t + 1) x
  have e5 := hv1 t x
  have hx := hvmax x
  have hlt : ((L : ℚ) / M) ^ (t + 1) = ((L : ℚ) / M) ^ t * ((L : ℚ) / M) := pow_succ _ _
  calc ((P ^ (t + 1)) *ᵥ F.live) x
      ≤ (1 / (vmin : ℚ)) * (((L : ℚ) / M) ^ (t + 1) * vec V F.A x) +
          (K : ℚ) / N * (((L : ℚ) / M) ^ t * vec V F.A x) := by
        rw [e2] at e1
        have := mul_le_mul_of_nonneg_left e4 (by positivity : (0 : ℚ) ≤ 1 / (vmin : ℚ))
        have := mul_le_mul_of_nonneg_left e5 hkap
        linarith
    _ ≤ (1 / (vmin : ℚ)) * (((L : ℚ) / M) ^ (t + 1) * vmax) +
          (K : ℚ) / N * (((L : ℚ) / M) ^ t * vmax) := by gcongr
    _ = ((vmax : ℚ) / vmin + ((K : ℚ) / N) * vmax / ((L : ℚ) / M)) * ((L : ℚ) / M) ^ (t + 1) := by
        rw [hlt]; field_simp

/-- **Lower bound on survival** from a lower vector `0 ≤ Vl ≤ wmax`. -/
theorem survival_lo (Vl : Tree) (Ll Ml wmax : ℕ) (htab : c.tabOK F = true)
    (hlo : allRows (c.rowLo F.A (c.Dt F.A) Ll Ml Vl) (2 ^ F.A) = true)
    (hvl : vecOK Vl F.A 0 wmax = true) (hMl : 0 < Ml) (hwmax : 0 < wmax) (t : ℕ) (x : Fin (2 ^ F.A)) :
    ((vec Vl F.A x) / wmax) * ((Ll : ℚ) / Ml) ^ t ≤ F.survival ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) t x := by
  have hP := c.P_nonneg F htab
  have hwmax' : (0 : ℚ) < wmax := by exact_mod_cast hwmax
  have key := survival_ge_of _ hP F.live (vec Vl F.A) ((Ll : ℚ) / Ml) (wmax : ℚ) (by positivity)
    (c.rows_lo F htab Vl Ll Ml hMl hlo)
    (fun y => by
      obtain ⟨h0, h1⟩ := vecOK_spec Vl F.A 0 wmax hvl y
      by_cases hy : (y : ℕ) = 0
      · rw [h0 hy]; simp [Face.live, hy]
      · rw [show F.live y = 1 by simp [Face.live, hy], mul_one]; exact (h1 hy).2) t x
  rw [Face.survival, div_mul_eq_mul_div, div_le_iff₀ hwmax', mul_comm _ (wmax : ℚ)]
  linarith

/-- **The lower bound on a quasi-stationary eigenvalue λ > 0**, when the lower vector vanishes only on
states that die surely. -/
theorem qsd_lo_sure (Vl : Tree) (Ll Ml wmax : ℕ) (htab : c.tabOK F = true)
    (hlo : allRows (c.rowLo F.A (c.Dt F.A) Ll Ml Vl) (2 ^ F.A) = true)
    (hvl : vecOK Vl F.A 0 wmax = true) (hs : c.sureOK Vl F.A = true) (hMl : 0 < Ml)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) μ lam)
    (hlam : 0 < lam) : ((Ll : ℚ) / Ml : ℝ) ≤ lam := by
  have hμ := hq.nonneg
  have hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → vec Vl F.A y = 0 := fun y => (vecOK_spec Vl F.A _ _ hvl y).1
  have hpair := qsd_pair F _ _ μ lam hq (vec Vl F.A) hv0
  have hrow : ∑ x, μ x * (((Ll : ℚ) / Ml * vec Vl F.A x : ℚ) : ℝ) ≤
      ∑ x, μ x * ((F.P _ _ *ᵥ vec Vl F.A) x : ℝ) :=
    sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (by exact_mod_cast c.rows_lo F htab Vl Ll Ml hMl hlo x) (hμ x)
  rw [hpair] at hrow
  have e : ∑ x, μ x * (((Ll : ℚ) / Ml * vec Vl F.A x : ℚ) : ℝ) =
      ((Ll : ℚ) / Ml : ℝ) * ∑ y, μ y * (vec Vl F.A y : ℝ) := by
    rw [mul_sum]; refine sum_congr rfl fun x _ => ?_; push_cast; ring
  rw [e] at hrow
  have hnn : ∀ y ∈ (univ : Finset (Fin (2 ^ F.A))), 0 ≤ μ y * (vec Vl F.A y : ℝ) :=
    fun y _ => mul_nonneg (hμ y) (by simp [vec])
  rcases (sum_nonneg hnn).lt_or_eq with hpos | hzero
  · exact le_of_mul_le_mul_right hrow hpos
  · -- the sum vanishes: μ lives on states that die surely, so λ = 0
    exfalso
    have hz : ∀ y, μ y * (vec Vl F.A y : ℝ) = 0 := fun y =>
      (sum_eq_zero_iff_of_nonneg hnn).mp hzero.symm y (mem_univ y)
    have hP0 : ∀ x y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 →
        μ x * (F.P ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) x y : ℝ) = 0 := by
      intro x y hy
      by_cases hx0 : (x : ℕ) = 0
      · rw [hq.empty x hx0, zero_mul]
      by_cases hw : Vl.get F.A x = 0
      · rw [c.P_sure F htab x y (c.sureOK_spec F Vl hs x hx0 hw) hy]; simp
      · have : (vec Vl F.A x : ℝ) ≠ 0 := by simp [vec, hw]
        rw [(mul_eq_zero.mp (hz x)).resolve_right this, zero_mul]
    have hall : ∀ y : Fin (2 ^ F.A), (y : ℕ) ≠ 0 → μ y = 0 := by
      intro y hy
      have := hq.eigen y hy
      rw [sum_eq_zero fun x _ => hP0 x y hy] at this
      exact (mul_eq_zero.mp this.symm).resolve_left hlam.ne'
    have : ∑ x, μ x = 0 := sum_eq_zero fun x _ => by
      by_cases hx : (x : ℕ) = 0
      · exact hq.empty x hx
      · exact hall x hx
    rw [hq.total] at this; exact one_ne_zero this

/-- **The upper bound on a quasi-stationary eigenvalue**, from an upper vector positive off the empty state. -/
theorem qsd_up (V : Tree) (L M vmin vmax : ℕ) (htab : c.tabOK F = true)
    (hup : allRows (c.rowUp F.A (c.Dt F.A) L M V) (2 ^ F.A) = true)
    (hv : vecOK V F.A vmin vmax = true) (hM : 0 < M) (hvmin : 0 < vmin)
    (μ : Fin (2 ^ F.A) → ℝ) (lam : ℝ) (hq : IsQSD F ((c.n1 : ℚ) / c.d1) ((c.n2 : ℚ) / c.d2) μ lam) :
    lam ≤ ((L : ℚ) / M : ℝ) := by
  have hμ := hq.nonneg
  have hv0 : ∀ y : Fin (2 ^ F.A), (y : ℕ) = 0 → vec V F.A y = 0 := fun y => (vecOK_spec V F.A _ _ hv y).1
  have hpair := qsd_pair F _ _ μ lam hq (vec V F.A) hv0
  have hS := qsd_mass F _ _ μ lam hq (vec V F.A) vmin fun y hy => (vecOK_spec V F.A _ _ hv y).2 hy |>.1
  have hvmin' : (0 : ℝ) < vmin := by exact_mod_cast hvmin
  have hrow : ∑ x, μ x * ((F.P _ _ *ᵥ vec V F.A) x : ℝ) ≤
      ∑ x, μ x * (((L : ℚ) / M * vec V F.A x : ℚ) : ℝ) :=
    sum_le_sum fun x _ => mul_le_mul_of_nonneg_left (by exact_mod_cast c.rows_up F htab V L M hM hup x) (hμ x)
  rw [hpair] at hrow
  have e : ∑ x, μ x * (((L : ℚ) / M * vec V F.A x : ℚ) : ℝ) = ((L : ℚ) / M : ℝ) * ∑ y, μ y * (vec V F.A y : ℝ) := by
    rw [mul_sum]; refine sum_congr rfl fun x _ => ?_; push_cast; ring
  rw [e] at hrow
  have hpos : (0 : ℝ) < ∑ y, μ y * (vec V F.A y : ℝ) := by
    have : ((vmin : ℚ) : ℝ) = (vmin : ℝ) := by push_cast; rfl
    linarith
  exact le_of_mul_le_mul_right hrow hpos

end Data

end Gump.Dice
