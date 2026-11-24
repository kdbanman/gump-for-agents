/-
Theorem 3 of `research/blast/rigour/THEOREMS.md` (structure of the exponent), conditional on its
hypothesis (SSM), with the referee's repair (`research/blast/ref-proofs/REVIEW.md`, A2, point 2: an
additive K₀/A, without which (SSM) is false at s = 1 whenever ⟨E⟩₁ = O(1)).

A face is a finite killed chain with local death factors, a quasi-stationary law and, for each cell i, a
number r_i (for the source: the largest radius r for which the ball about i is that of the infinite
layer, coin counts included; nothing here depends on how r is defined).

  `SSM`              the hypothesis, uniform over a family of faces, cells and s ∈ [0, 1]:
                     |⟨ε_i⟩_{s,G} - e_∞(s)| ≤ K e^{-r_i/ξ} + K₀/A_G.
  `IntSSM`           the weaker hypothesis that is all the proof of (a) uses: the same bound for the
                     integrated local prices, |c_i(G) - c_∞| ≤ K e^{-r_i/ξ} + K₀/A_G.
  `SSM.toIntSSM`     (SSM) with e_∞ integrable on [0, 1] implies `IntSSM` for c_∞ = ∫₀¹ e_∞.
  `thm3a`            under `IntSSM`: |log τ(G) - c_∞ A_G| ≤ K ∑_i e^{-r_i/ξ} + K₀.
  `thm3b`            if every r_i ≥ (ℓ - 2)/2 (wrapped faces with shortest loop ℓ), the error is
                     ≤ K A e^{-(ℓ-2)/(2ξ)} + K₀.
  `thm3c`            if r_i ∈ ℕ and at most C·R cells sit at each distance r (polygons, R the rim), the
                     error is ≤ K C R / (1 - e^{-1/ξ}) + K₀.
  `thm3d`            along a sequence of faces with A → ∞ and ∑_i e^{-r_i/ξ} = o(A): log τ / A → c_∞.
-/
import Mathlib
import GumpMath.ChainTilt

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Real Filter Topology

/-- A face: a finite killed chain with local death factors, a quasi-stationary law, and a radius r_i for
every cell. -/
structure Face where
  σ : Type
  [fσ : Fintype σ]
  [dσ : DecidableEq σ]
  V : Type
  [fV : Fintype V]
  K : KilledChain σ
  L : K.LocalDeath V
  μ : σ → ℝ
  lam : ℝ
  qsd : K.IsQSD μ lam
  r : V → ℝ

attribute [instance] Face.fσ Face.dσ Face.fV

namespace Face
variable (G : Face)

/-- The number of cells, A. -/
def area : ℕ := Fintype.card G.V

/-- log τ. -/
noncomputable def logTau : ℝ := log (G.K.lifetime G.μ)

/-- The local tilted mean ⟨ε_i⟩_s. -/
noncomputable def localMean (i : G.V) (s : ℝ) : ℝ := tiltMean G.μ G.L.energy s (G.L.cost i)

/-- The local price c_i. -/
noncomputable def price (i : G.V) : ℝ := G.L.price G.μ i

theorem logTau_eq : G.logTau = ∑ i, G.price i := (KilledChain.tilt_identity G.L G.qsd).2.1

end Face

variable {ι : Type*}

/-- **(SSM)**, uniform strong spatial mixing along the tilt, with the referee's repair K₀/A. -/
def SSM (F : ι → Face) (einf : ℝ → ℝ) (K ξ K0 : ℝ) : Prop :=
  ∀ g (i : (F g).V), ∀ s ∈ Set.Icc (0:ℝ) 1,
    |(F g).localMean i s - einf s| ≤ K * exp (-((F g).r i / ξ)) + K0 / (F g).area

/-- The integrated form: all that the proof of Theorem 3 (a) uses. -/
def IntSSM (F : ι → Face) (cinf : ℝ) (K ξ K0 : ℝ) : Prop :=
  ∀ g (i : (F g).V), |(F g).price i - cinf| ≤ K * exp (-((F g).r i / ξ)) + K0 / (F g).area

theorem SSM.toIntSSM {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0)
    (hint : IntervalIntegrable einf MeasureTheory.volume 0 1) :
    IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0 := by
  intro g i
  have hP := (F g).qsd.isProb
  have hc : IntervalIntegrable (fun s => (F g).localMean i s) MeasureTheory.volume 0 1 :=
    (continuous_tiltMean hP _ _).intervalIntegrable 0 1
  have e : (F g).price i - ∫ s in (0:ℝ)..1, einf s =
      ∫ s in (0:ℝ)..1, ((F g).localMean i s - einf s) := by
    rw [intervalIntegral.integral_sub hc hint]; rfl
  rw [e]
  have := intervalIntegral.norm_integral_le_of_norm_le_const (a := 0) (b := 1)
    (C := K * exp (-((F g).r i / ξ)) + K0 / (F g).area)
    (f := fun s => (F g).localMean i s - einf s) (fun s hs => by
      rw [Set.uIoc_of_le zero_le_one] at hs
      exact h g i s ⟨hs.1.le, hs.2⟩)
  simpa using this

theorem card_mul_div_le (A : ℕ) {K0 : ℝ} (hK0 : 0 ≤ K0) : (A : ℝ) * (K0 / A) ≤ K0 := by
  rcases eq_or_ne (A : ℝ) 0 with h | h
  · simp [h, hK0]
  · rw [mul_div_cancel₀ _ h]

/-- **Theorem 3 (a).**  Under the integrated hypothesis, |log τ(G) - c_∞ A| ≤ K ∑_i e^{-r_i/ξ} + K₀. -/
theorem thm3a {F : ι → Face} {cinf K ξ K0 : ℝ} (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0) (g : ι) :
    |(F g).logTau - cinf * (F g).area| ≤ K * ∑ i, exp (-((F g).r i / ξ)) + K0 := by
  rw [Face.logTau_eq]
  have e : ∑ i, (F g).price i - cinf * (F g).area = ∑ i, ((F g).price i - cinf) := by
    rw [Finset.sum_sub_distrib]; simp [Face.area, mul_comm]
  rw [e]
  calc |∑ i, ((F g).price i - cinf)| ≤ ∑ i, |(F g).price i - cinf| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, (K * exp (-((F g).r i / ξ)) + K0 / (F g).area) := Finset.sum_le_sum (fun i _ => h g i)
    _ ≤ K * ∑ i, exp (-((F g).r i / ξ)) + K0 := by
      rw [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, card_univ, nsmul_eq_mul]
      have := card_mul_div_le (F g).area hK0
      simp only [Face.area] at this ⊢
      linarith

/-- **Theorem 3 (b)** (wrapped faces): if every r_i ≥ (ℓ - 2)/2, the error of (a) is at most
K A e^{-(ℓ-2)/(2ξ)} + K₀. -/
theorem thm3b {F : ι → Face} {cinf K ξ K0 ℓ : ℝ} (hK : 0 ≤ K) (hξ : 0 < ξ) (hK0 : 0 ≤ K0)
    (h : IntSSM F cinf K ξ K0) (g : ι) (hr : ∀ i, (ℓ - 2) / 2 ≤ (F g).r i) :
    |(F g).logTau - cinf * (F g).area| ≤ K * (F g).area * exp (-((ℓ - 2) / (2 * ξ))) + K0 := by
  have ha := thm3a hK0 h g
  have hs : ∑ i, exp (-((F g).r i / ξ)) ≤ (F g).area * exp (-((ℓ - 2) / (2 * ξ))) := by
    have : ∀ i, exp (-((F g).r i / ξ)) ≤ exp (-((ℓ - 2) / (2 * ξ))) := fun i => by
      apply exp_le_exp.2
      rw [neg_le_neg_iff, div_le_div_iff₀ (by positivity) hξ]
      have := hr i
      nlinarith
    calc ∑ i, exp (-((F g).r i / ξ)) ≤ ∑ _i : (F g).V, exp (-((ℓ - 2) / (2 * ξ))) :=
          Finset.sum_le_sum (fun i _ => this i)
      _ = (F g).area * exp (-((ℓ - 2) / (2 * ξ))) := by simp [Face.area]
  calc |(F g).logTau - cinf * (F g).area| ≤ K * ∑ i, exp (-((F g).r i / ξ)) + K0 := ha
    _ ≤ K * ((F g).area * exp (-((ℓ - 2) / (2 * ξ)))) + K0 := by
        have := mul_le_mul_of_nonneg_left hs hK; linarith
    _ = K * (F g).area * exp (-((ℓ - 2) / (2 * ξ))) + K0 := by ring

/-- A geometric sum over any finite set of distances: ∑_{r ∈ S} q^r ≤ 1/(1 - q). -/
theorem sum_pow_le (S : Finset ℕ) {q : ℝ} (h0 : 0 ≤ q) (h1 : q < 1) :
    ∑ r ∈ S, q ^ r ≤ 1 / (1 - q) := by
  obtain ⟨N, hN⟩ : ∃ N, S ⊆ range N := ⟨S.sup id + 1, fun r hr => by
    rw [mem_range]; exact Nat.lt_succ_of_le (le_sup (f := id) hr)⟩
  calc ∑ r ∈ S, q ^ r ≤ ∑ r ∈ range N, q ^ r :=
        Finset.sum_le_sum_of_subset_of_nonneg hN (fun r _ _ => pow_nonneg h0 r)
    _ = (1 - q ^ N) / (1 - q) := by
        rw [geom_sum_eq h1.ne, div_eq_div_iff (sub_ne_zero.2 h1.ne) (sub_pos.2 h1).ne']; ring
    _ ≤ 1 / (1 - q) := by
        apply div_le_div_of_nonneg_right _ (by linarith)
        linarith [pow_nonneg h0 N]

/-- **Theorem 3 (c)** (polygons): if every r_i is a whole number d_i and at most C·R cells sit at each
distance, the error of (a) is at most K C R / (1 - e^{-1/ξ}) + K₀. -/
theorem thm3c {F : ι → Face} {cinf K ξ K0 C R : ℝ} (hK : 0 ≤ K) (hξ : 0 < ξ) (hK0 : 0 ≤ K0)
    (h : IntSSM F cinf K ξ K0) (g : ι) (d : (F g).V → ℕ) (hd : ∀ i, (F g).r i = d i)
    (hcount : ∀ r : ℕ, ((univ.filter (fun i => d i = r)).card : ℝ) ≤ C * R) (hCR : 0 ≤ C * R) :
    |(F g).logTau - cinf * (F g).area| ≤ K * (C * R / (1 - exp (-(1 / ξ)))) + K0 := by
  have ha := thm3a hK0 h g
  set q := exp (-(1 / ξ)) with hq
  have hq0 : 0 ≤ q := (exp_pos _).le
  have hq1 : q < 1 := by rw [hq, exp_lt_one_iff, neg_lt_zero]; exact div_pos one_pos hξ
  have hpow : ∀ i, exp (-((F g).r i / ξ)) = q ^ d i := fun i => by
    rw [hd i, hq, ← exp_nat_mul]; ring_nf
  have hs : ∑ i, exp (-((F g).r i / ξ)) ≤ C * R / (1 - q) := by
    simp_rw [hpow]
    rw [Finset.sum_comp (fun r => q ^ r) d]
    calc ∑ b ∈ univ.image d, (univ.filter (fun i => d i = b)).card • q ^ b
        ≤ ∑ b ∈ univ.image d, (C * R) * q ^ b := Finset.sum_le_sum (fun b _ => by
          rw [nsmul_eq_mul]; exact mul_le_mul_of_nonneg_right (hcount b) (pow_nonneg hq0 b))
      _ = (C * R) * ∑ b ∈ univ.image d, q ^ b := by rw [Finset.mul_sum]
      _ ≤ (C * R) * (1 / (1 - q)) := mul_le_mul_of_nonneg_left (sum_pow_le _ hq0 hq1) hCR
      _ = C * R / (1 - q) := by ring
  calc |(F g).logTau - cinf * (F g).area| ≤ K * ∑ i, exp (-((F g).r i / ξ)) + K0 := ha
    _ ≤ K * (C * R / (1 - q)) + K0 := by have := mul_le_mul_of_nonneg_left hs hK; linarith

/-- **Theorem 3 (d)**: along a sequence of faces with A → ∞ and ∑_i e^{-r_i/ξ} / A → 0,
log τ / A → c_∞: the same number for every such sequence, rimmed or wrapped. -/
theorem thm3d {F : ℕ → Face} {cinf K ξ K0 : ℝ} (hK0 : 0 ≤ K0) (h : IntSSM F cinf K ξ K0)
    (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop)
    (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0)) :
    Tendsto (fun n => (F n).logTau / (F n).area) atTop (𝓝 cinf) := by
  have hbound : ∀ᶠ n in atTop, |(F n).logTau / (F n).area - cinf| ≤
      K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area := by
    filter_upwards [hA.eventually_gt_atTop 0] with n hn
    have ha := thm3a hK0 h n
    rw [show (F n).logTau / (F n).area - cinf = ((F n).logTau - cinf * (F n).area) / (F n).area by
      field_simp]
    rw [abs_div, abs_of_pos hn, div_le_iff₀ hn]
    have : (K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area) * (F n).area =
        K * ∑ i, exp (-((F n).r i / ξ)) + K0 := by field_simp
    rw [this]; exact ha
  have hlim : Tendsto (fun n => K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area)
      atTop (𝓝 0) := by
    have h1 := hloc.const_mul K
    have h2 := (tendsto_const_nhds (x := K0)).div_atTop hA
    simpa using h1.add h2
  rw [tendsto_iff_norm_sub_tendsto_zero]
  apply squeeze_zero' (Eventually.of_forall (fun n => norm_nonneg _)) _ hlim
  filter_upwards [hbound] with n hn
  simpa [Real.norm_eq_abs] using hn

end Gump.Chain
