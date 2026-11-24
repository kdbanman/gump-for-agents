/-
Lemma R of `research/blast/rigour/THEOREMS.md` (routes; curvature is minus the variance of the branch
prices), with the referee's correction of its discrete form (`research/blast/ref-proofs/REVIEW.md`, A3).

The deaths of a family of faces indexed by a size A are split into finitely many routes r with death rates
h_r(A) > 0; τ = 1/∑_r h_r, p_r = h_r/∑ h, and c_r = -d log h_r/dA (stated as h_r' = -c_r h_r).
  `routes_first`   d log τ/dA = ∑_r p_r c_r.
  `routes_second`  d/dA (∑_r p_r c_r) = -∑_r p_r (c_r - c̄)² + ∑_r p_r c_r'  (c̄ = ∑ p c): so
                   d² log τ/dA² = -Var_p(c) + ∑ p c'.
  `log_odds`       for two routes, d log(h₁/h₂)/dA = c₂ - c₁.
  `routes_concave` routes with constant prices give a concave log τ.
  `two_routes_step` the exact step for two exponential routes:
                   log τ(D+1) - log τ(D) = c_s - log(1 - p(D)(1 - e^{-(c_b - c_s)})).
Nothing here is specific to the surrogate: any partition of the deaths, any differentiable rates.
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace Gump.Chain.Routes
open Finset Real

variable {ι : Type*} [Fintype ι]

/-- The share of route r. -/
noncomputable def share (h : ι → ℝ → ℝ) (r : ι) (A : ℝ) : ℝ := h r A / ∑ q, h q A

/-- The mean price ∑_r p_r c_r. -/
noncomputable def meanPrice (h c : ι → ℝ → ℝ) (A : ℝ) : ℝ := ∑ r, share h r A * c r A

theorem sum_pos_of [Nonempty ι] {h : ι → ℝ → ℝ} {A : ℝ} (hpos : ∀ r, 0 < h r A) :
    0 < ∑ q, h q A :=
  Finset.sum_pos (fun r _ => hpos r) univ_nonempty

/-- **Lemma R, first derivative**: d log τ/dA = ∑_r p_r c_r. -/
theorem routes_first [Nonempty ι] (h c : ι → ℝ → ℝ) (A : ℝ) (hpos : ∀ r, 0 < h r A)
    (hd : ∀ r, HasDerivAt (h r) (-(c r A) * h r A) A) :
    HasDerivAt (fun B => -log (∑ r, h r B)) (meanPrice h c A) A := by
  have hS := sum_pos_of hpos
  have hsum : HasDerivAt (fun B => ∑ r, h r B) (∑ r, -(c r A) * h r A) A :=
    HasDerivAt.fun_sum (fun r _ => hd r)
  have := (hsum.log hS.ne').neg
  convert this using 1
  simp only [meanPrice, share, neg_mul, Finset.sum_neg_distrib, neg_div, neg_neg, Finset.sum_div]
  exact Finset.sum_congr rfl (fun r _ => by ring)

/-- **Lemma R, second derivative**: d/dA ∑ p c = -∑ p (c - c̄)² + ∑ p c'. -/
theorem routes_second [Nonempty ι] (h c c' : ι → ℝ → ℝ) (A : ℝ) (hpos : ∀ r, 0 < h r A)
    (hd : ∀ r, HasDerivAt (h r) (-(c r A) * h r A) A) (hc : ∀ r, HasDerivAt (c r) (c' r A) A) :
    HasDerivAt (meanPrice h c)
      (-(∑ r, share h r A * (c r A - meanPrice h c A) ^ 2) + ∑ r, share h r A * c' r A) A := by
  have hS := sum_pos_of hpos
  set S0 := ∑ q, h q A with hS0
  set S1 := ∑ q, h q A * c q A with hS1
  set S2 := ∑ q, h q A * c q A ^ 2 with hS2
  set T := ∑ q, h q A * c' q A with hT
  have hN : HasDerivAt (fun B => ∑ r, h r B * c r B) (∑ r, (-(c r A) * h r A * c r A + h r A * c' r A)) A :=
    HasDerivAt.fun_sum (fun r _ => (hd r).mul (hc r))
  have hH : HasDerivAt (fun B => ∑ r, h r B) (∑ r, -(c r A) * h r A) A :=
    HasDerivAt.fun_sum (fun r _ => hd r)
  have hF := hN.div hH hS.ne'
  have heq : meanPrice h c = (fun B => ∑ r, h r B * c r B) / (fun B => ∑ r, h r B) := by
    funext B; simp only [meanPrice, share, Pi.div_apply, Finset.sum_div]
    exact Finset.sum_congr rfl (fun r _ => by ring)
  have hF' : HasDerivAt (meanPrice h c)
      (((∑ r, (-(c r A) * h r A * c r A + h r A * c' r A)) * ∑ r, h r A -
        (∑ r, h r A * c r A) * ∑ r, -(c r A) * h r A) / (∑ r, h r A) ^ 2) A := by
    rw [heq]; exact hF
  convert hF' using 1
  rw [← hS0, ← hS1]
  have hm : meanPrice h c A = S1 / S0 := by
    simp only [meanPrice, share, hS1, hS0, Finset.sum_div]
    exact Finset.sum_congr rfl (fun r _ => by ring)
  have e1 : ∑ r, share h r A * (c r A - meanPrice h c A) ^ 2 = (S2 - 2 * (S1 / S0) * S1 + (S1 / S0) ^ 2 * S0) / S0 := by
    rw [hm]
    have : ∀ r, share h r A * (c r A - S1 / S0) ^ 2 =
        (h r A * c r A ^ 2) / S0 - (2 * (S1 / S0)) * (h r A * c r A) / S0 + (S1 / S0) ^ 2 * h r A / S0 :=
      fun r => by simp only [share, ← hS0]; ring
    simp_rw [this, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_div, ← Finset.mul_sum]
    ring
  have e2 : ∑ r, share h r A * c' r A = T / S0 := by
    simp only [share, hT, ← hS0, Finset.sum_div]
    exact Finset.sum_congr rfl (fun r _ => by ring)
  have e3 : ∑ r, (-(c r A) * h r A * c r A + h r A * c' r A) = -S2 + T := by
    rw [Finset.sum_add_distrib, hS2, hT, ← Finset.sum_neg_distrib]
    congr 1; exact Finset.sum_congr rfl (fun r _ => by ring)
  have e4 : ∑ r, -(c r A) * h r A = -S1 := by
    rw [hS1, ← Finset.sum_neg_distrib]; exact Finset.sum_congr rfl (fun r _ => by ring)
  rw [e1, e2, e3, e4]
  field_simp
  ring

/-- **Two routes: the log-odds.**  d log(h₁/h₂)/dA = c₂ - c₁. -/
theorem log_odds (h1 h2 : ℝ → ℝ) (c1 c2 A : ℝ) (p1 : 0 < h1 A) (p2 : 0 < h2 A)
    (d1 : HasDerivAt h1 (-c1 * h1 A) A) (d2 : HasDerivAt h2 (-c2 * h2 A) A) :
    HasDerivAt (fun B => log (h1 B / h2 B)) (c2 - c1) A := by
  have := (d1.div d2 p2.ne').log (div_pos p1 p2).ne'
  convert this using 1
  simp only [Pi.div_apply]
  field_simp
  ring

/-- **Routes with constant prices give a concave log τ** (curvature -p(1-p)(c₁-c₂)² for two). -/
theorem routes_concave [Nonempty ι] (a c : ι → ℝ) (ha : ∀ r, 0 < a r) :
    ConcaveOn ℝ Set.univ (fun B => -log (∑ r, a r * exp (-(c r * B)))) := by
  set h : ι → ℝ → ℝ := fun r B => a r * exp (-(c r * B)) with hh
  have hpos : ∀ r B, 0 < h r B := fun r B => mul_pos (ha r) (exp_pos _)
  have hd : ∀ r B, HasDerivAt (h r) (-((fun r _ => c r) r B) * h r B) B := fun r B => by
    have h1 : HasDerivAt (fun y => -(c r * y)) (-(c r * 1)) B := ((hasDerivAt_id B).const_mul (c r)).neg
    have := (h1.exp).const_mul (a r)
    convert this using 1
    simp only [hh]; ring
  have hderiv : ∀ B, HasDerivAt (fun B => -log (∑ r, h r B)) (meanPrice h (fun r _ => c r) B) B :=
    fun B => routes_first h (fun r _ => c r) B (fun r => hpos r B) (fun r => hd r B)
  apply Antitone.concaveOn_univ_of_deriv
  · exact fun B => (hderiv B).differentiableAt
  · have : deriv (fun B => -log (∑ r, h r B)) = meanPrice h (fun r _ => c r) :=
      funext fun B => (hderiv B).deriv
    rw [this]
    apply antitone_of_deriv_nonpos
    · exact fun B => (routes_second h (fun r _ => c r) (fun _ _ => 0) B (fun r => hpos r B)
        (fun r => hd r B) (fun r => hasDerivAt_const B (c r))).differentiableAt
    · intro B
      rw [(routes_second h (fun r _ => c r) (fun _ _ => 0) B (fun r => hpos r B)
        (fun r => hd r B) (fun r => hasDerivAt_const B (c r))).deriv]
      simp only [mul_zero, Finset.sum_const_zero, add_zero, neg_nonpos]
      exact Finset.sum_nonneg (fun r _ => mul_nonneg
        (div_nonneg (hpos r B).le (sum_pos_of (fun q => hpos q B)).le) (sq_nonneg _))

/-- An exactly exponential route: a · e^{-c D}. -/
noncomputable def expRoute (a c D : ℝ) : ℝ := a * exp (-(c * D))

/-- **The exact discrete step for two exponential routes** (the referee's correction):
with h_b(D) = α e^{-c_b D}, h_s(D) = β e^{-c_s D} and p(D) = h_b/(h_b + h_s) the bust share,
log τ(D+1) - log τ(D) = c_s - log(1 - p(D)(1 - e^{-(c_b - c_s)})), where log τ = -log(h_b + h_s). -/
theorem two_routes_step (α β cb cs D : ℝ) (hα : 0 < α) (hβ : 0 < β) :
    -log (expRoute α cb (D + 1) + expRoute β cs (D + 1)) - (-log (expRoute α cb D + expRoute β cs D)) =
      cs - log (1 - expRoute α cb D / (expRoute α cb D + expRoute β cs D) *
        (1 - exp (-(cb - cs)))) := by
  have hbp : 0 < expRoute α cb D := mul_pos hα (exp_pos _)
  have hsp : 0 < expRoute β cs D := mul_pos hβ (exp_pos _)
  have hsum : 0 < expRoute α cb D + expRoute β cs D := add_pos hbp hsp
  set p := expRoute α cb D / (expRoute α cb D + expRoute β cs D) with hp
  have key : expRoute α cb (D + 1) + expRoute β cs (D + 1) =
      exp (-cs) * (expRoute α cb D + expRoute β cs D) * (1 - p * (1 - exp (-(cb - cs)))) := by
    rw [hp]
    field_simp
    have e1 : exp (-(cb * (D + 1))) = exp (-(cb * D)) * exp (-cs) * exp (-(cb - cs)) := by
      rw [← exp_add, ← exp_add]; ring_nf
    have e2 : exp (-(cs * (D + 1))) = exp (-(cs * D)) * exp (-cs) := by
      rw [← exp_add]; ring_nf
    simp only [expRoute, e1, e2]; ring
  have hq : 0 < 1 - p * (1 - exp (-(cb - cs))) := by
    have h1 : 0 < exp (-cs) * (expRoute α cb D + expRoute β cs D) := mul_pos (exp_pos _) hsum
    have h2 : 0 < expRoute α cb (D + 1) + expRoute β cs (D + 1) :=
      add_pos (mul_pos hα (exp_pos _)) (mul_pos hβ (exp_pos _))
    rw [key] at h2
    exact pos_of_mul_pos_right h2 h1.le
  rw [key, log_mul (mul_pos (exp_pos _) hsum).ne' hq.ne', log_mul (exp_pos _).ne' hsum.ne', log_exp]
  ring

end Gump.Chain.Routes
