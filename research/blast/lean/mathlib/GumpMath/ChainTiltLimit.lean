/-
What remains of Theorem 3 when (SSM) fails at a jump of the tilt (the referee's measurement,
`research/blast/ref-proofs/REVIEW.md` A2.3: two kinds of face coexist near s ≈ 0.2–0.3 on wrapped faces).

Because s ↦ ⟨E⟩_s is non-increasing (Theorem 2), uniformity in s and spatial locality are not needed for
the price per cell; a jump of the limit curve costs nothing:
  `tilt_riemann_bounds`  for every face and n ≥ 1, the n + 1 tilted means at s = k/n bracket log τ:
                         (1/n) ∑_{k=1}^{n} ⟨E⟩_{k/n} ≤ log τ ≤ (1/n) ∑_{k=0}^{n-1} ⟨E⟩_{k/n},
                         a bracket of width (⟨E⟩₀ - ⟨E⟩₁)/n ≤ ε_max A / n;
  `price_of_pointwise`   along any sequence of faces, if the tilted energy per cell ⟨E⟩_{s,G}/A converges
                         at every s ∈ (0, 1] (pointwise, at any rate, with any jumps in the limit f),
                         then log τ / A → ∫₀¹ f.  So two families of faces (rimmed, wrapped) have the same
                         price as soon as their per-cell tilted energies have the same pointwise limit.
-/
import Mathlib
import GumpMath.ChainSSM

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Real Filter Topology MeasureTheory

section Riemann
variable {σ : Type*} [Fintype σ]

/-- On [a, b], an antitone continuous integrand lies between its values at the ends. -/
theorem integral_antitone_bounds {f : ℝ → ℝ} (hf : Antitone f) (hc : Continuous f) {a b : ℝ}
    (hab : a ≤ b) : (b - a) * f b ≤ ∫ s in a..b, f s ∧ ∫ s in a..b, f s ≤ (b - a) * f a := by
  have hi := hc.intervalIntegrable (μ := volume) a b
  constructor
  · have := intervalIntegral.integral_mono_on hab (intervalIntegrable_const (c := f b)) hi
      (fun s hs => hf hs.2)
    simpa [mul_comm] using this
  · have := intervalIntegral.integral_mono_on hab hi (intervalIntegrable_const (c := f a))
      (fun s hs => hf hs.1)
    simpa [mul_comm] using this

/-- **Riemann bounds for the tilt**: (1/n)∑_{k=1}^{n} ⟨E⟩_{k/n} ≤ ∫₀¹⟨E⟩_s ds ≤ (1/n)∑_{k=0}^{n-1} ⟨E⟩_{k/n}. -/
theorem integral_tilt_riemann {μ : σ → ℝ} (hμ : IsProb μ) (E : σ → ℝ) (n : ℕ) (hn : 0 < n) :
    (1 / n) * ∑ k ∈ range n, tiltMean μ E ((k + 1 : ℕ) / n) E ≤ ∫ s in (0:ℝ)..1, tiltMean μ E s E ∧
    ∫ s in (0:ℝ)..1, tiltMean μ E s E ≤ (1 / n) * ∑ k ∈ range n, tiltMean μ E ((k : ℕ) / n) E := by
  set f := fun s => tiltMean μ E s E with hf
  have hanti : Antitone f := tiltMean_antitone hμ E
  have hcont : Continuous f := continuous_tiltMean hμ E E
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  have hsplit : ∫ s in (0:ℝ)..1, f s = ∑ k ∈ range n, ∫ s in ((k : ℕ) / n : ℝ)..((k + 1 : ℕ) / n), f s := by
    have := intervalIntegral.sum_integral_adjacent_intervals (a := fun k : ℕ => (k : ℝ) / n)
      (f := f) (μ := volume) (n := n) (fun k _ => hcont.intervalIntegrable _ _)
    simp only [Nat.cast_zero, zero_div] at this
    rw [div_self hn'.ne'] at this
    rw [← this]
  have hstep : ∀ k : ℕ, ((k + 1 : ℕ) : ℝ) / n - (k : ℝ) / n = 1 / n := fun k => by
    push_cast; ring
  have hle : ∀ k : ℕ, (k : ℝ) / n ≤ ((k + 1 : ℕ) : ℝ) / n := fun k => by
    have := hstep k; have : (0:ℝ) < 1 / n := by positivity
    linarith
  rw [hsplit, Finset.mul_sum, Finset.mul_sum]
  constructor
  · refine Finset.sum_le_sum (fun k _ => ?_)
    have := (integral_antitone_bounds hanti hcont (hle k)).1
    rw [hstep k] at this; exact this
  · refine Finset.sum_le_sum (fun k _ => ?_)
    have := (integral_antitone_bounds hanti hcont (hle k)).2
    rw [hstep k] at this; exact this

end Riemann

/-- **Riemann bounds for log τ** on a face. -/
theorem tilt_riemann_bounds (G : Face) (n : ℕ) (hn : 0 < n) :
    (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k + 1 : ℕ) / n) G.L.energy ≤ G.logTau ∧
    G.logTau ≤ (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy := by
  have e : G.logTau = ∫ s in (0:ℝ)..1, tiltMean G.μ G.L.energy s G.L.energy :=
    (KilledChain.tilt_identity G.L G.qsd).1
  rw [e]
  exact integral_tilt_riemann G.qsd.isProb G.L.energy n hn

/-- **The price from pointwise convergence of the tilted energy per cell.**  Along a sequence of faces
with local costs at most ε_max, if ⟨E⟩_{s,G_n}/A_n → f(s) for every s ∈ (0, 1], then
log τ(G_n)/A_n → ∫₀¹ f. -/
theorem price_of_pointwise (F : ℕ → Face) (emax : ℝ) (hA : ∀ n, 0 < (F n).area)
    (hmax : ∀ n i x, (F n).L.cost i x ≤ emax) (f : ℝ → ℝ)
    (hlim : ∀ s ∈ Set.Ioc (0:ℝ) 1,
      Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (f s))) :
    Tendsto (fun n => (F n).logTau / (F n).area) atTop (𝓝 (∫ s in (0:ℝ)..1, f s)) := by
  set g : ℕ → ℝ → ℝ := fun n s => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area
  have hg : ∀ n, (F n).logTau / (F n).area = ∫ s in (0:ℝ)..1, g n s := fun n => by
    have e : (F n).logTau = ∫ s in (0:ℝ)..1, tiltMean (F n).μ (F n).L.energy s (F n).L.energy :=
      (KilledChain.tilt_identity (F n).L (F n).qsd).1
    rw [e, intervalIntegral.integral_div]
  simp_rw [hg]
  have hcont : ∀ n, Continuous (g n) := fun n =>
    (continuous_tiltMean (F n).qsd.isProb _ _).div_const _
  have hbound : ∀ n s, ‖g n s‖ ≤ emax := fun n s => by
    have hP := (F n).qsd.isProb
    have hE0 : ∀ x, 0 ≤ (F n).L.energy x := fun x =>
      Finset.sum_nonneg (fun i _ => (F n).L.cost_nonneg i x)
    have hE1 : ∀ x, (F n).L.energy x ≤ emax * (F n).area := fun x => by
      have := Finset.sum_le_sum (fun i (_ : i ∈ (univ : Finset (F n).V)) => hmax n i x)
      simpa [KilledChain.LocalDeath.energy, Face.area, mul_comm] using this
    have hm := tiltMean_mem hP (F n).L.energy (F n).L.energy s 0 (emax * (F n).area) hE0 hE1
    have hAn : (0:ℝ) < (F n).area := by exact_mod_cast hA n
    rw [Real.norm_eq_abs, abs_of_nonneg (div_nonneg hm.1 hAn.le), div_le_iff₀ hAn]
    exact hm.2
  apply intervalIntegral.tendsto_integral_filter_of_dominated_convergence (fun _ => emax)
  · exact Eventually.of_forall (fun n => (hcont n).aestronglyMeasurable)
  · exact Eventually.of_forall (fun n => ae_of_all _ (fun s _ => hbound n s))
  · exact intervalIntegrable_const
  · refine ae_of_all _ (fun s hs => ?_)
    rw [Set.uIoc_of_le zero_le_one] at hs
    exact hlim s hs

end Gump.Chain
