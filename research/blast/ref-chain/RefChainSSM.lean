/-
ref-chain: the referee's objection to (SSM) in full, from the chain agent's `SSM.einf_continuousOn` plus the
step it leaves out (under (SSM) the per-cell tilted energy converges to e_∞ at every tilt).

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/RefChainSSM.lean

`SSM.tilt_limit`: under (SSM), A → ∞ and ∑_i e^{-r_i/ξ} = o(A), ⟨E⟩_{s,G_n}/A_n → e_∞(s) for every s ∈ [0,1].
`jump_refutes_SSM`: so if the per-cell tilted energies of such a family converge on [0,1] to a limit that is
not continuous there (a first-order jump), no (SSM) holds for the family, whatever e_∞, K, K₀.
-/
import GumpMath.ChainTiltLimit

open Finset Filter Topology Real
open Gump.Chain

namespace RefChain

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

/-- **A jump of the limiting per-cell tilted energy refutes (SSM)** for any family with large faces. -/
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

end RefChain

#print axioms RefChain.SSM.tilt_limit
#print axioms RefChain.jump_refutes_SSM
