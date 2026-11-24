/-
Theorem 2 of `research/blast/rigour/THEOREMS.md` (the tilt identity) and Theorem 1 (the upper bound), for
an abstract finite killed Markov chain whose one-step death probability is a product of local factors.

The chain.  `σ` is a finite set of living states.  `Q x y ≥ 0` is the probability of going from x to the
living state y in one generation, with `∑ y, Q x y ≤ 1`; the rest, `death x = 1 - ∑ y, Q x y`, is the
probability of dying (for the surrogate: of reaching the empty face, `P(x, ∅)`).

A quasi-stationary law is a probability vector μ with μ Q = λ μ.  Then `P_μ(T > t) = λ ^ t` and
`τ = E_μ T = ∑_t P_μ(T > t) = 1 / h` with `h = ∑ μ d = 1 - λ` (`lifetime_eq`).

Local costs.  If `death x = ∏_i d_i x` with `0 < d_i ≤ 1` (the surrogate's product kernel and its
standing assumption (K)), put `ε_i = -log d_i` and `E = ∑_i ε_i`, so that `death = exp (-E)`.

The tilt.  `μ_s ∝ μ e^{-sE}`, `⟨f⟩_s` its mean, `Z(s) = E_μ e^{-sE}`.  Proved here:
  `tilt_identity`  log τ = ∫₀¹ ⟨E⟩_s ds = ∑_i ∫₀¹ ⟨ε_i⟩_s ds, s ↦ ⟨E⟩_s is antitone,
                   ⟨E⟩₁ ≤ log τ ≤ ⟨E⟩₀ = E_μ E, and each local price lies in [0, ε_max].
  `upper_bound`    (Theorem 1) log τ ≤ E_μ E ≤ ε_max · |V|.
  `last_living_law`  μ₁ is the law of the last living state: ∑_t P_μ(X_t = x) d(x) = μ(x) d(x) / h.
No spectral theory is used: Z is a finite sum of exponentials.  Existence and uniqueness of μ are in
`ChainPerron.lean`.
-/
import Mathlib

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Real Matrix

section Analytic
variable {σ : Type*} [Fintype σ]

/-- The tilted weight of a state: μ x · e^{-s E x}. -/
noncomputable def tw (μ E : σ → ℝ) (s : ℝ) (x : σ) : ℝ := μ x * exp (-(s * E x))

/-- The partition function of the tilt, Z(s) = E_μ e^{-sE}. -/
noncomputable def Z (μ E : σ → ℝ) (s : ℝ) : ℝ := ∑ x, tw μ E s x

/-- The tilted mean ⟨f⟩_s = E_μ[f e^{-sE}] / E_μ[e^{-sE}]: the mean of f under μ_s ∝ μ e^{-sE}. -/
noncomputable def tiltMean (μ E : σ → ℝ) (s : ℝ) (f : σ → ℝ) : ℝ :=
  (∑ x, tw μ E s x * f x) / Z μ E s

/-- A probability vector. -/
def IsProb (μ : σ → ℝ) : Prop := (∀ x, 0 ≤ μ x) ∧ ∑ x, μ x = 1

omit [Fintype σ] in
theorem tw_nonneg {μ : σ → ℝ} (hμ : ∀ x, 0 ≤ μ x) (E : σ → ℝ) (s : ℝ) (x : σ) : 0 ≤ tw μ E s x :=
  mul_nonneg (hμ x) (exp_pos _).le

theorem exists_pos_of_isProb {μ : σ → ℝ} (hμ : IsProb μ) : ∃ x, 0 < μ x := by
  by_contra h
  push Not at h
  have : ∑ x, μ x = 0 := Finset.sum_eq_zero (fun x _ => le_antisymm (h x) (hμ.1 x))
  rw [hμ.2] at this
  exact one_ne_zero this

theorem Z_pos {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) (s : ℝ) : 0 < Z μ E s := by
  obtain ⟨x, hx⟩ := exists_pos_of_isProb hμ
  exact Finset.sum_pos' (fun y _ => tw_nonneg hμ.1 E s y) ⟨x, mem_univ x, mul_pos hx (exp_pos _)⟩

theorem Z_zero {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) : Z μ E 0 = 1 := by
  simp [Z, tw, hμ.2]

theorem tiltMean_zero {μ : σ → ℝ} (hμ : IsProb μ) (E f : σ → ℝ) :
    tiltMean μ E 0 f = ∑ x, μ x * f x := by
  simp [tiltMean, Z_zero hμ, tw]

/-- d/ds of a numerator ∑ μ f e^{-sE}. -/
theorem hasDerivAt_num (μ E f : σ → ℝ) (s : ℝ) :
    HasDerivAt (fun s => ∑ x, tw μ E s x * f x) (-∑ x, tw μ E s x * (E x * f x)) s := by
  have h : ∀ x ∈ (univ : Finset σ),
      HasDerivAt (fun s => tw μ E s x * f x) (-(tw μ E s x * (E x * f x))) s := by
    intro x _
    have h1 : HasDerivAt (fun s => -(s * E x)) (-(1 * E x)) s :=
      ((hasDerivAt_id s).mul_const (E x)).neg
    have h2 := ((h1.exp).const_mul (μ x)).mul_const (f x)
    convert h2 using 1; simp only [tw]; ring
  rw [← Finset.sum_neg_distrib]
  exact HasDerivAt.fun_sum h

theorem hasDerivAt_Z (μ E : σ → ℝ) (s : ℝ) :
    HasDerivAt (fun s => Z μ E s) (-∑ x, tw μ E s x * E x) s := by
  have := hasDerivAt_num μ E (fun _ => 1) s
  simp only [mul_one] at this
  exact this

theorem continuous_num (μ E f : σ → ℝ) : Continuous (fun s => ∑ x, tw μ E s x * f x) :=
  continuous_iff_continuousAt.2 (fun s => (hasDerivAt_num μ E f s).continuousAt)

theorem continuous_Z (μ E : σ → ℝ) : Continuous (fun s => Z μ E s) :=
  continuous_iff_continuousAt.2 (fun s => (hasDerivAt_Z μ E s).continuousAt)

theorem continuous_tiltMean {μ : σ → ℝ} (hμ : IsProb μ) (E f : σ → ℝ) :
    Continuous (fun s => tiltMean μ E s f) :=
  (continuous_num μ E f).div (continuous_Z μ E) (fun s => (Z_pos hμ E s).ne')

/-- (log Z)' = -⟨E⟩_s. -/
theorem hasDerivAt_logZ {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) (s : ℝ) :
    HasDerivAt (fun s => log (Z μ E s)) (-tiltMean μ E s E) s := by
  have := (hasDerivAt_Z μ E s).log (Z_pos hμ E s).ne'
  convert this using 1
  simp only [tiltMean, neg_div]

/-- **The analytic tilt identity**: -log E_μ e^{-E} = ∫₀¹ ⟨E⟩_s ds, for any probability vector μ and
any real E. -/
theorem neg_log_Z_one {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) :
    -log (Z μ E 1) = ∫ s in (0:ℝ)..1, tiltMean μ E s E := by
  have hint : IntervalIntegrable (fun s => -tiltMean μ E s E) MeasureTheory.volume 0 1 :=
    ((continuous_tiltMean hμ E E).neg).intervalIntegrable 0 1
  have := intervalIntegral.integral_eq_sub_of_hasDerivAt
    (fun s _ => hasDerivAt_logZ hμ E s) hint
  rw [intervalIntegral.integral_neg, Z_zero hμ, log_one, sub_zero] at this
  linarith

/-- The tilted mean is linear in the observable: ⟨∑_i g_i⟩_s = ∑_i ⟨g_i⟩_s. -/
theorem tiltMean_sum {V : Type*} [Fintype V] (μ E : σ → ℝ) (s : ℝ) (g : V → σ → ℝ) :
    tiltMean μ E s (fun x => ∑ i, g i x) = ∑ i, tiltMean μ E s (g i) := by
  simp only [tiltMean, Finset.mul_sum, ← Finset.sum_div]
  rw [Finset.sum_comm]

/-- A tilted mean of an observable with values in [a, b] lies in [a, b]. -/
theorem tiltMean_mem {μ : σ → ℝ} (hμ : IsProb μ) (E f : σ → ℝ) (s a b : ℝ)
    (ha : ∀ x, a ≤ f x) (hb : ∀ x, f x ≤ b) : a ≤ tiltMean μ E s f ∧ tiltMean μ E s f ≤ b := by
  have hZ := Z_pos hμ E s
  constructor
  · rw [tiltMean, le_div_iff₀ hZ, Z, Finset.mul_sum]
    exact Finset.sum_le_sum (fun x _ => by
      rw [mul_comm a]; exact mul_le_mul_of_nonneg_left (ha x) (tw_nonneg hμ.1 E s x))
  · rw [tiltMean, div_le_iff₀ hZ, Z, Finset.mul_sum]
    exact Finset.sum_le_sum (fun x _ => by
      rw [mul_comm b]; exact mul_le_mul_of_nonneg_left (hb x) (tw_nonneg hμ.1 E s x))

/-- Cauchy–Schwarz for the tilt: (∑ w E)² ≤ (∑ w E²)(∑ w), i.e. Var_s(E) ≥ 0. -/
theorem num_sq_le {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) (s : ℝ) :
    (∑ x, tw μ E s x * E x) ^ 2 ≤ (∑ x, tw μ E s x * (E x * E x)) * Z μ E s := by
  set N := ∑ x, tw μ E s x * E x
  set M := ∑ x, tw μ E s x * (E x * E x)
  set W := Z μ E s
  have hW : 0 < W := Z_pos hμ E s
  have key : 0 ≤ ∑ x, tw μ E s x * (E x * W - N) ^ 2 :=
    Finset.sum_nonneg (fun x _ => mul_nonneg (tw_nonneg hμ.1 E s x) (sq_nonneg _))
  have expand : ∑ x, tw μ E s x * (E x * W - N) ^ 2 = W * (M * W - N ^ 2) := by
    have : ∀ x, tw μ E s x * (E x * W - N) ^ 2 =
        W ^ 2 * (tw μ E s x * (E x * E x)) - (2 * W * N) * (tw μ E s x * E x) + N ^ 2 * tw μ E s x :=
      fun x => by ring
    simp_rw [this, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]
    simp only [M, N, W, Z]; ring
  rw [expand] at key
  nlinarith [key, hW]

/-- d/ds ⟨E⟩_s = -Var_s(E) ≤ 0, written as (N² - M Z)/Z². -/
theorem hasDerivAt_tiltMean {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) (s : ℝ) :
    HasDerivAt (fun s => tiltMean μ E s E)
      (((-∑ x, tw μ E s x * (E x * E x)) * Z μ E s - (∑ x, tw μ E s x * E x) *
        (-∑ x, tw μ E s x * E x)) / Z μ E s ^ 2) s :=
  (hasDerivAt_num μ E E s).div (hasDerivAt_Z μ E s) (Z_pos hμ E s).ne'

/-- **s ↦ ⟨E⟩_s is non-increasing** ((log Z)'' = Var_s E ≥ 0). -/
theorem tiltMean_antitone {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) :
    Antitone (fun s => tiltMean μ E s E) := by
  apply antitone_of_deriv_nonpos
  · exact fun s => (hasDerivAt_tiltMean hμ E s).differentiableAt
  · intro s
    rw [(hasDerivAt_tiltMean hμ E s).deriv]
    apply div_nonpos_of_nonpos_of_nonneg _ (sq_nonneg _)
    nlinarith [num_sq_le hμ E s]

/-- ⟨E⟩₁ ≤ ∫₀¹ ⟨E⟩_s ds ≤ ⟨E⟩₀. -/
theorem integral_tiltMean_bounds {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) :
    tiltMean μ E 1 E ≤ ∫ s in (0:ℝ)..1, tiltMean μ E s E ∧
    ∫ s in (0:ℝ)..1, tiltMean μ E s E ≤ tiltMean μ E 0 E := by
  have hc := (continuous_tiltMean hμ E E).intervalIntegrable (μ := MeasureTheory.volume) 0 1
  have hanti := tiltMean_antitone hμ E
  constructor
  · have := intervalIntegral.integral_mono_on (zero_le_one' ℝ)
      (intervalIntegrable_const (c := tiltMean μ E 1 E)) hc
      (fun s hs => hanti hs.2)
    simpa using this
  · have := intervalIntegral.integral_mono_on (zero_le_one' ℝ) hc
      (intervalIntegrable_const (c := tiltMean μ E 0 E))
      (fun s hs => hanti hs.1)
    simpa using this

end Analytic

/-! ## The killed chain -/

/-- A finite killed Markov chain: `Q x y` is the probability of moving from the living state x to the
living state y in one generation; `1 - ∑ y, Q x y` is the probability of dying. -/
structure KilledChain (σ : Type*) [Fintype σ] where
  Q : Matrix σ σ ℝ
  nonneg : ∀ x y, 0 ≤ Q x y
  sub : ∀ x, ∑ y, Q x y ≤ 1

namespace KilledChain
variable {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ)

/-- d(x): the probability of dying in one generation from x (for the surrogate, P(x, ∅)). -/
def death (x : σ) : ℝ := 1 - ∑ y, K.Q x y

theorem death_nonneg (x : σ) : 0 ≤ K.death x := by
  have := K.sub x; simp only [death]; linarith

/-- A quasi-stationary law with eigenvalue `lam`: a probability vector with μ Q = lam μ. -/
structure IsQSD (μ : σ → ℝ) (lam : ℝ) : Prop where
  nonneg : ∀ x, 0 ≤ μ x
  total : ∑ x, μ x = 1
  eigen : ∀ y, ∑ x, μ x * K.Q x y = lam * μ y

/-- h = ∑ μ d: the death rate from μ. -/
def hazard (μ : σ → ℝ) : ℝ := ∑ x, μ x * K.death x

/-- P_μ(T > t) = ∑_y (μ Q^t)_y: the probability of being alive after t generations. -/
def survival (μ : σ → ℝ) (t : ℕ) : ℝ := ∑ y, (μ ᵥ* (K.Q ^ t)) y

/-- τ = E_μ T = ∑_{t ≥ 0} P_μ(T > t): the mean lifetime from μ. -/
noncomputable def lifetime (μ : σ → ℝ) : ℝ := ∑' t, K.survival μ t

variable {K}

theorem IsQSD.isProb {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) : IsProb μ := ⟨h.nonneg, h.total⟩

theorem IsQSD.vecMul {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) : μ ᵥ* K.Q = lam • μ := by
  funext y; simp [Matrix.vecMul, dotProduct, h.eigen y]

theorem IsQSD.vecMul_pow {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (t : ℕ) :
    μ ᵥ* (K.Q ^ t) = lam ^ t • μ := by
  induction t with
  | zero => simp
  | succ t ih =>
    rw [pow_succ, ← Matrix.vecMul_vecMul, ih, Matrix.smul_vecMul, h.vecMul, smul_smul, pow_succ]

/-- λ = 1 - h. -/
theorem IsQSD.lam_eq {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) : lam = 1 - K.hazard μ := by
  have e1 : ∑ y, ∑ x, μ x * K.Q x y = lam := by
    simp_rw [h.eigen, ← Finset.mul_sum, h.total, mul_one]
  rw [Finset.sum_comm] at e1
  simp only [hazard, death, mul_sub, mul_one, Finset.sum_sub_distrib, h.total, ← Finset.mul_sum] at *
  linarith

theorem IsQSD.lam_nonneg {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) : 0 ≤ lam := by
  have e1 : ∑ y, ∑ x, μ x * K.Q x y = lam := by
    simp_rw [h.eigen, ← Finset.mul_sum, h.total, mul_one]
  rw [← e1]
  exact Finset.sum_nonneg (fun y _ => Finset.sum_nonneg (fun x _ => mul_nonneg (h.nonneg x) (K.nonneg x y)))

/-- P_μ(T > t) = λ^t. -/
theorem IsQSD.survival_eq {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (t : ℕ) :
    K.survival μ t = lam ^ t := by
  simp [survival, h.vecMul_pow t, ← Finset.mul_sum, h.total]

/-- τ = E_μ T = 1 / h. -/
theorem IsQSD.lifetime_eq {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (hh : 0 < K.hazard μ) :
    K.lifetime μ = 1 / K.hazard μ := by
  have hl := h.lam_eq
  simp only [lifetime, h.survival_eq]
  rw [tsum_geometric_of_lt_one h.lam_nonneg (by linarith)]
  rw [hl]; simp

/-- **μ₁ is the law of the last living state**: ∑_t P_μ(X_t = x) d(x) = μ(x) d(x) / h. -/
theorem IsQSD.last_living_law {μ : σ → ℝ} {lam : ℝ} (h : K.IsQSD μ lam) (hh : 0 < K.hazard μ)
    (x : σ) : ∑' t, (μ ᵥ* (K.Q ^ t)) x * K.death x = μ x * K.death x / K.hazard μ := by
  have hl := h.lam_eq
  simp only [h.vecMul_pow, Pi.smul_apply, smul_eq_mul]
  have : (fun t => lam ^ t * μ x * K.death x) = fun t => (μ x * K.death x) * lam ^ t := by
    funext t; ring
  rw [this, tsum_mul_left, tsum_geometric_of_lt_one h.lam_nonneg (by linarith), hl]
  simp [div_eq_mul_inv]

/-- The one-step death probability is a product of local factors `0 < d_i ≤ 1` (the product kernel and
the standing assumption (K) of THEOREMS.md). -/
structure LocalDeath (K : KilledChain σ) (V : Type*) [Fintype V] where
  dc : V → σ → ℝ
  pos : ∀ i x, 0 < dc i x
  le_one : ∀ i x, dc i x ≤ 1
  prod : ∀ x, K.death x = ∏ i, dc i x

namespace LocalDeath
variable {V : Type*} [Fintype V] (L : K.LocalDeath V)

/-- The local cost ε_i(x) = -log d_i(x). -/
noncomputable def cost (i : V) (x : σ) : ℝ := -log (L.dc i x)

/-- E(x) = ∑_i ε_i(x). -/
noncomputable def energy (x : σ) : ℝ := ∑ i, L.cost i x

/-- The price of the cell i: c_i = ∫₀¹ ⟨ε_i⟩_s ds. -/
noncomputable def price (μ : σ → ℝ) (i : V) : ℝ := ∫ s in (0:ℝ)..1, tiltMean μ L.energy s (L.cost i)

theorem cost_nonneg (i : V) (x : σ) : 0 ≤ L.cost i x := by
  simp only [cost, neg_nonneg]; exact log_nonpos (L.pos i x).le (L.le_one i x)

theorem death_eq_exp (x : σ) : K.death x = exp (-L.energy x) := by
  rw [L.prod x, energy, ← Finset.sum_neg_distrib, exp_sum]
  exact Finset.prod_congr rfl (fun i _ => by simp [cost, exp_log (L.pos i x)])

theorem hazard_eq_Z (μ : σ → ℝ) : K.hazard μ = Z μ L.energy 1 := by
  simp [hazard, Z, tw, L.death_eq_exp]

end LocalDeath

open LocalDeath

/-- **Theorem 2 (the tilt identity).**  For a finite killed chain whose death probability is a product of
local factors in (0, 1], and any quasi-stationary law μ:
log τ = ∫₀¹ ⟨E⟩_s ds = ∑_i c_i with c_i = ∫₀¹ ⟨ε_i⟩_s ds; s ↦ ⟨E⟩_s is non-increasing; and
⟨E⟩₁ ≤ log τ ≤ ⟨E⟩₀ = E_μ[E]. -/
theorem tilt_identity {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) :
    log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧
    log (K.lifetime μ) = ∑ i, L.price μ i ∧
    Antitone (fun s => tiltMean μ L.energy s L.energy) ∧
    tiltMean μ L.energy 1 L.energy ≤ log (K.lifetime μ) ∧
    log (K.lifetime μ) ≤ tiltMean μ L.energy 0 L.energy ∧
    tiltMean μ L.energy 0 L.energy = ∑ x, μ x * L.energy x := by
  have hP := hμ.isProb
  have hh : 0 < K.hazard μ := by rw [L.hazard_eq_Z]; exact Z_pos hP _ _
  have e0 : log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy := by
    rw [hμ.lifetime_eq hh, one_div, log_inv, L.hazard_eq_Z, neg_log_Z_one hP]
  have hb := integral_tiltMean_bounds hP L.energy
  refine ⟨e0, ?_, tiltMean_antitone hP _, e0 ▸ hb.1, e0 ▸ hb.2, tiltMean_zero hP _ _⟩
  rw [e0]
  have : (fun s => tiltMean μ L.energy s L.energy) = fun s => ∑ i, tiltMean μ L.energy s (L.cost i) := by
    funext s; exact tiltMean_sum μ L.energy s L.cost
  rw [this, intervalIntegral.integral_finsetSum]
  · rfl
  · exact fun i _ => (continuous_tiltMean hP _ _).intervalIntegrable 0 1

/-- Each local price lies in [0, ε_max] when every local cost is at most ε_max. -/
theorem price_mem {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) (emax : ℝ) (hmax : ∀ i x, L.cost i x ≤ emax) (i : V) :
    0 ≤ L.price μ i ∧ L.price μ i ≤ emax := by
  have hP := hμ.isProb
  have hm := fun s => tiltMean_mem hP L.energy (L.cost i) s 0 emax (L.cost_nonneg i) (hmax i)
  have hc := (continuous_tiltMean hP L.energy (L.cost i)).intervalIntegrable
    (μ := MeasureTheory.volume) 0 1
  constructor
  · have := intervalIntegral.integral_mono_on (zero_le_one' ℝ)
      (intervalIntegrable_const (c := (0:ℝ))) hc (fun s _ => (hm s).1)
    simpa [price] using this
  · have := intervalIntegral.integral_mono_on (zero_le_one' ℝ) hc
      (intervalIntegrable_const (c := emax)) (fun s _ => (hm s).2)
    simpa [price] using this

/-- **Theorem 1 (the upper bound).**  log τ ≤ E_μ[E] ≤ ε_max · |V|. -/
theorem upper_bound {V : Type*} [Fintype V] (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) (emax : ℝ) (hmax : ∀ i x, L.cost i x ≤ emax) :
    log (K.lifetime μ) ≤ ∑ x, μ x * L.energy x ∧
    ∑ x, μ x * L.energy x ≤ emax * Fintype.card V := by
  obtain ⟨-, -, -, -, h5, h6⟩ := tilt_identity L hμ
  refine ⟨h6 ▸ h5, ?_⟩
  have hE : ∀ x, L.energy x ≤ emax * Fintype.card V := fun x => by
    have := Finset.sum_le_sum (fun i (_ : i ∈ (univ : Finset V)) => hmax i x)
    simpa [energy, mul_comm] using this
  calc ∑ x, μ x * L.energy x ≤ ∑ x, μ x * (emax * Fintype.card V) :=
        Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hE x) (hμ.nonneg x))
    _ = emax * Fintype.card V := by rw [← Finset.sum_mul, hμ.total, one_mul]

end KilledChain
end Gump.Chain
