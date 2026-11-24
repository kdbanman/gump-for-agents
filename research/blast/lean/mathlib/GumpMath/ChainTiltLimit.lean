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

/-- **Comparing two faces from finitely many tilts.**  If the per-cell tilted energies of two faces differ by at
most δ at s = k/n (k = 0, …, n), and each curve falls by at most w over [0, 1], then their prices per cell differ
by at most δ + w/n.  (w ≤ ε_max always; jumps between grid points cost nothing more.) -/
theorem price_compare (G G' : Face) (hA : 0 < G.area) (hA' : 0 < G'.area) (n : ℕ) (hn : 0 < n)
    (δ w : ℝ)
    (hδ : ∀ k ≤ n, |tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy / G.area -
      tiltMean G'.μ G'.L.energy ((k : ℕ) / n) G'.L.energy / G'.area| ≤ δ)
    (hw : (tiltMean G.μ G.L.energy 0 G.L.energy - tiltMean G.μ G.L.energy 1 G.L.energy) / G.area ≤ w)
    (hw' : (tiltMean G'.μ G'.L.energy 0 G'.L.energy - tiltMean G'.μ G'.L.energy 1 G'.L.energy) / G'.area ≤ w) :
    |G.logTau / G.area - G'.logTau / G'.area| ≤ δ + w / n := by
  set f : ℝ → ℝ := fun s => tiltMean G.μ G.L.energy s G.L.energy / G.area
  set f' : ℝ → ℝ := fun s => tiltMean G'.μ G'.L.energy s G'.L.energy / G'.area
  have hAr : (0:ℝ) < G.area := by exact_mod_cast hA
  have hAr' : (0:ℝ) < G'.area := by exact_mod_cast hA'
  have hn' : (0:ℝ) < n := by exact_mod_cast hn
  -- Riemann brackets per cell
  obtain ⟨lo, up⟩ := tilt_riemann_bounds G n hn
  obtain ⟨lo', up'⟩ := tilt_riemann_bounds G' n hn
  set Lo := (1 / n) * ∑ k ∈ range n, f ((k + 1 : ℕ) / n)
  set Up := (1 / n) * ∑ k ∈ range n, f ((k : ℕ) / n)
  set Lo' := (1 / n) * ∑ k ∈ range n, f' ((k + 1 : ℕ) / n)
  set Up' := (1 / n) * ∑ k ∈ range n, f' ((k : ℕ) / n)
  have hlo : Lo ≤ G.logTau / G.area := by
    rw [le_div_iff₀ hAr]
    simp only [Lo, f, Finset.mul_sum, Finset.sum_mul]
    calc ∑ k ∈ range n, 1 / n * (tiltMean G.μ G.L.energy ((k + 1 : ℕ) / n) G.L.energy / G.area) * G.area
        = (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k + 1 : ℕ) / n) G.L.energy := by
          rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun k _ => by field_simp)
      _ ≤ _ := lo
  have hup : G.logTau / G.area ≤ Up := by
    rw [div_le_iff₀ hAr]
    simp only [Up, f, Finset.mul_sum, Finset.sum_mul]
    calc G.logTau ≤ (1 / n) * ∑ k ∈ range n, tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy := up
      _ = ∑ k ∈ range n, 1 / n * (tiltMean G.μ G.L.energy ((k : ℕ) / n) G.L.energy / G.area) * G.area := by
          rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun k _ => by field_simp)
  have hlo' : Lo' ≤ G'.logTau / G'.area := by
    rw [le_div_iff₀ hAr']
    simp only [Lo', f', Finset.mul_sum, Finset.sum_mul]
    calc ∑ k ∈ range n, 1 / n * (tiltMean G'.μ G'.L.energy ((k + 1 : ℕ) / n) G'.L.energy / G'.area) * G'.area
        = (1 / n) * ∑ k ∈ range n, tiltMean G'.μ G'.L.energy ((k + 1 : ℕ) / n) G'.L.energy := by
          rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun k _ => by field_simp)
      _ ≤ _ := lo'
  have hup' : G'.logTau / G'.area ≤ Up' := by
    rw [div_le_iff₀ hAr']
    simp only [Up', f', Finset.mul_sum, Finset.sum_mul]
    calc G'.logTau ≤ (1 / n) * ∑ k ∈ range n, tiltMean G'.μ G'.L.energy ((k : ℕ) / n) G'.L.energy := up'
      _ = ∑ k ∈ range n, 1 / n * (tiltMean G'.μ G'.L.energy ((k : ℕ) / n) G'.L.energy / G'.area) * G'.area := by
          rw [Finset.mul_sum]; exact Finset.sum_congr rfl (fun k _ => by field_simp)
  -- the brackets have width (f 0 - f 1)/n
  have hwid : Up - Lo = (f 0 - f 1) / n := by
    simp only [Up, Lo, ← mul_sub, ← Finset.sum_sub_distrib]
    rw [Finset.sum_range_sub' (fun k => f ((k : ℕ) / n)) n]
    simp [div_self hn'.ne']
    ring
  have hwid' : Up' - Lo' = (f' 0 - f' 1) / n := by
    simp only [Up', Lo', ← mul_sub, ← Finset.sum_sub_distrib]
    rw [Finset.sum_range_sub' (fun k => f' ((k : ℕ) / n)) n]
    simp [div_self hn'.ne']
    ring
  -- the lower sums are within δ
  have hLL : |Lo - Lo'| ≤ δ := by
    simp only [Lo, Lo', ← mul_sub, ← Finset.sum_sub_distrib, abs_mul]
    rw [abs_of_pos (by positivity : (0:ℝ) < 1 / n)]
    calc 1 / n * |∑ k ∈ range n, (f ((k + 1 : ℕ) / n) - f' ((k + 1 : ℕ) / n))|
        ≤ 1 / n * ∑ k ∈ range n, |f ((k + 1 : ℕ) / n) - f' ((k + 1 : ℕ) / n)| :=
          mul_le_mul_of_nonneg_left (Finset.abs_sum_le_sum_abs _ _) (by positivity)
      _ ≤ 1 / n * ∑ _k ∈ range n, δ :=
          mul_le_mul_of_nonneg_left (Finset.sum_le_sum (fun k hk => hδ (k + 1)
            (by have := mem_range.1 hk; omega))) (by positivity)
      _ = δ := by simp; field_simp
  have h0 : f 0 - f 1 ≤ w := by simpa [f, sub_div] using hw
  have h0' : f' 0 - f' 1 ≤ w := by simpa [f', sub_div] using hw'
  have hw1 : (f 0 - f 1) / n ≤ w / n := div_le_div_of_nonneg_right h0 hn'.le
  have hw1' : (f' 0 - f' 1) / n ≤ w / n := div_le_div_of_nonneg_right h0' hn'.le
  rw [abs_le] at hLL ⊢
  constructor <;> linarith

/-- **(SSM) forbids a jump along the tilt.**  If (SSM) holds for a family containing faces and cells with
arbitrarily small error term K e^{-r_i/ξ} + K₀/A (large balls in large faces), then e_∞ is a uniform limit of the
continuous curves s ↦ ⟨ε_i⟩_{s,G}, hence continuous on [0, 1].  So a jump of the limiting tilted energy (two kinds
of face coexisting at one tilt, as measured by the referee) refutes (SSM) for that family. -/
theorem SSM.einf_continuousOn {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ}
    (h : SSM F einf K ξ K0)
    (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) :
    ContinuousOn einf (Set.Icc 0 1) := by
  rw [Metric.continuousOn_iff]
  intro b hb ε hε
  obtain ⟨g, i, hgi⟩ := hlarge (ε / 3) (by positivity)
  have hc : Continuous (fun s => (F g).localMean i s) := continuous_tiltMean (F g).qsd.isProb _ _
  obtain ⟨δ, hδ, hδb⟩ := Metric.continuous_iff.1 hc b (ε / 3) (by positivity)
  refine ⟨δ, hδ, fun a ha hab => ?_⟩
  have h1 := h g i a ha
  have h2 := h g i b hb
  have h3 := hδb a hab
  rw [Real.dist_eq] at h3 ⊢
  calc |einf a - einf b|
      = |(einf a - (F g).localMean i a) + ((F g).localMean i a - (F g).localMean i b) +
          ((F g).localMean i b - einf b)| := by ring_nf
    _ ≤ |einf a - (F g).localMean i a| + |(F g).localMean i a - (F g).localMean i b| +
          |(F g).localMean i b - einf b| := abs_add_three _ _ _
    _ < ε / 3 + ε / 3 + ε / 3 := by
        rw [abs_sub_comm (einf a)]
        have := h1.trans_lt hgi
        have := h2.trans_lt hgi
        linarith
    _ = ε := by ring

/-! ### Taken over from the referee (`research/blast/ref-chain/RefChainVacuity.lean`, `RefChainSSM.lean`,
agent `ref-chain`, 2026-11-24): the a.e. form of `price_of_pointwise`, (SSM) without the integrability
hypothesis, and the referee's objection to (SSM) in full.  Proofs as the referee wrote them. -/

/-- **The price from convergence at almost every tilt** (referee's `price_of_ae`): at a first-order jump the
finite curves need not converge at the jump point itself; dominated convergence needs only a.e. s. -/
theorem price_of_ae (F : ℕ → Face) (emax : ℝ) (hA : ∀ n, 0 < (F n).area)
    (hmax : ∀ n i x, (F n).L.cost i x ≤ emax) (f : ℝ → ℝ)
    (hlim : ∀ᵐ s ∂volume, s ∈ Set.Ioc (0:ℝ) 1 →
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
  · refine hlim.mono (fun s hs hs' => ?_)
    rw [Set.uIoc_of_le zero_le_one] at hs'
    exact hs hs'

/-- **(SSM) gives the integrated hypothesis with no integrability assumption** (referee's `SSM.toIntSSM'`),
for any family with arbitrarily small error terms. -/
theorem SSM.toIntSSM' {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ}
    (h : SSM F einf K ξ K0)
    (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) :
    IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0 :=
  h.toIntSSM ((SSM.einf_continuousOn h hlarge).intervalIntegrable_of_Icc zero_le_one)

/-- The same, under a name the statement table can find. -/
theorem SSM.toIntSSM_of_small {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ}
    (h : SSM F einf K ξ K0)
    (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) :
    IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0 :=
  SSM.toIntSSM' h hlarge

/-- **Under (SSM) the per-cell tilted energy converges to e_∞ at every tilt** (referee's `SSM.tilt_limit`). -/
theorem SSM.tilt_limit {F : ℕ → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ} (h : SSM F einf K ξ K0)
    (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop)
    (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0))
    (s : ℝ) (hs : s ∈ Set.Icc (0:ℝ) 1) :
    Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (einf s)) := by
  have hbound : ∀ᶠ n in atTop,
      |tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area - einf s| ≤
        K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area := by
    filter_upwards [hA.eventually_gt_atTop 0] with n hn
    have hsum : tiltMean (F n).μ (F n).L.energy s (F n).L.energy =
        ∑ i, (F n).localMean i s := tiltMean_sum _ _ s _
    have e : tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area - einf s =
        (∑ i, ((F n).localMean i s - einf s)) / (F n).area := by
      rw [hsum, Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
      simp only [Face.area] at hn ⊢
      field_simp
    rw [e, abs_div, abs_of_pos hn, div_le_iff₀ hn]
    calc |∑ i, ((F n).localMean i s - einf s)| ≤ ∑ i, |(F n).localMean i s - einf s| :=
          Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ i, (K * exp (-((F n).r i / ξ)) + K0 / (F n).area) :=
          Finset.sum_le_sum (fun i _ => h n i s hs)
      _ = (K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area) * (F n).area := by
          rw [Finset.sum_add_distrib, ← Finset.mul_sum, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
          simp only [Face.area] at hn ⊢
          field_simp
  have hlim : Tendsto (fun n => K * ((∑ i, exp (-((F n).r i / ξ))) / (F n).area) + K0 / (F n).area)
      atTop (𝓝 0) := by
    have h1 := hloc.const_mul K
    have h2 := (tendsto_const_nhds (x := K0)).div_atTop hA
    simpa using h1.add h2
  rw [tendsto_iff_norm_sub_tendsto_zero]
  apply squeeze_zero' (Eventually.of_forall (fun n => norm_nonneg _)) _ hlim
  filter_upwards [hbound] with n hn
  simpa [Real.norm_eq_abs] using hn

/-- **A jump of the limiting per-cell tilted energy refutes (SSM)** for any family with large faces
(referee's `jump_refutes_SSM`): whatever e_∞, K, K₀. -/
theorem jump_refutes_SSM {F : ℕ → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ}
    (hA : Tendsto (fun n => ((F n).area : ℝ)) atTop atTop)
    (hloc : Tendsto (fun n => (∑ i, exp (-((F n).r i / ξ))) / (F n).area) atTop (𝓝 0))
    (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * exp (-((F g).r i / ξ)) + K0 / (F g).area < δ)
    (f : ℝ → ℝ)
    (hf : ∀ s ∈ Set.Icc (0:ℝ) 1,
      Tendsto (fun n => tiltMean (F n).μ (F n).L.energy s (F n).L.energy / (F n).area) atTop (𝓝 (f s)))
    (hjump : ¬ ContinuousOn f (Set.Icc 0 1)) :
    ¬ SSM F einf K ξ K0 := by
  intro h
  apply hjump
  have heq : Set.EqOn f einf (Set.Icc 0 1) := fun s hs =>
    tendsto_nhds_unique (hf s hs) (SSM.tilt_limit h hA hloc s hs)
  exact (SSM.einf_continuousOn h hlarge).congr heq

end Gump.Chain
