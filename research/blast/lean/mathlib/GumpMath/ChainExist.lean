/-
Every finite killed chain has a quasi-stationary law (the weak Perron theorem), with no irreducibility:
perturb Q to the positive matrix Q + J/(k+1), take its positive Perron row vector (`ChainPerron.lean`),
normalise, and pass to a convergent subsequence in the compact set (simplex) × [0, 1 + |σ|].

So Theorem 2 holds on every face, hull faces and strips included, for which irreducibility is not proved:
`tilt_identity_exists`.
-/
import Mathlib
import GumpMath.ChainPerron

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Matrix Filter Topology

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

namespace KilledChain

/-- **Existence of a quasi-stationary law** for every finite killed chain on a nonempty set of states. -/
theorem exists_qsd [Nonempty σ] (K : KilledChain σ) : ∃ μ lam, K.IsQSD μ lam := by
  let ε : ℕ → ℝ := fun k => 1 / ((k : ℝ) + 1)
  have hε : ∀ k, 0 < ε k := fun k => by simp only [ε]; positivity
  let A : ℕ → Matrix σ σ ℝ := fun k => K.Q + Matrix.of (fun _ _ => ε k)
  have hA : ∀ k x y, A k x y = K.Q x y + ε k := fun k x y => rfl
  have hApos : ∀ k x y, 0 < A k x y := fun k x y => by
    rw [hA]; exact add_pos_of_nonneg_of_pos (K.nonneg x y) (hε k)
  have hirr : ∀ k, Irreducible (A k) := fun k x y => ⟨1, by simpa using hApos k x y⟩
  choose r hr v hv he using
    fun k => exists_pos_left_eigenvector (fun x y => (hApos k x y).le) (hirr k)
  let m : ℕ → σ → ℝ := fun k x => v k x / ∑ y, v k y
  have hsum : ∀ k, 0 < ∑ y, v k y := fun k => Finset.sum_pos (fun y _ => hv k y) univ_nonempty
  have hm : ∀ k, m k ∈ probSet σ := fun k =>
    ⟨fun x => (div_pos (hv k x) (hsum k)).le, by
      simp only [m, ← Finset.sum_div]; exact div_self (hsum k).ne'⟩
  have heig : ∀ k y, ∑ x, m k x * A k x y = r k * m k y := fun k y => by
    have := congrFun (he k) y
    simp only [Matrix.vecMul, dotProduct, Pi.smul_apply, smul_eq_mul] at this
    simp only [m, div_mul_eq_mul_div, ← Finset.sum_div, this]; ring
  have hrb : ∀ k, r k ≤ 1 + Fintype.card σ := fun k => by
    have e : ∑ y, ∑ x, m k x * A k x y = r k := by
      simp_rw [heig, ← Finset.mul_sum, (hm k).2, mul_one]
    rw [← e, Finset.sum_comm]
    have hrow : ∀ x, ∑ y, A k x y ≤ 1 + Fintype.card σ := fun x => by
      simp only [hA, Finset.sum_add_distrib, Finset.sum_const, card_univ, nsmul_eq_mul]
      have h1 := K.sub x
      have h2 : ε k ≤ 1 := by
        simp only [ε]; rw [div_le_one (by positivity)]; linarith [(Nat.cast_nonneg k : (0:ℝ) ≤ k)]
      nlinarith [(Nat.cast_nonneg (Fintype.card σ) : (0:ℝ) ≤ Fintype.card σ)]
    calc ∑ x, ∑ y, m k x * A k x y = ∑ x, m k x * ∑ y, A k x y := by simp_rw [Finset.mul_sum]
      _ ≤ ∑ x, m k x * (1 + Fintype.card σ) :=
          Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hrow x) ((hm k).1 x))
      _ = 1 + Fintype.card σ := by rw [← Finset.sum_mul, (hm k).2, one_mul]
  obtain ⟨⟨μ, l⟩, hmem, φ, hφ, hlim⟩ :=
    (isCompact_probSet.prod (isCompact_Icc (a := (0:ℝ)) (b := 1 + Fintype.card σ))).tendsto_subseq
      (x := fun k => (m k, r k)) (fun k => ⟨hm k, hr k, hrb k⟩)
  refine ⟨μ, l, ⟨hmem.1.1, hmem.1.2, fun y => ?_⟩⟩
  have hμlim : Tendsto (fun k => m (φ k)) atTop (𝓝 μ) := (continuous_fst.tendsto _).comp hlim
  have hrlim : Tendsto (fun k => r (φ k)) atTop (𝓝 l) := (continuous_snd.tendsto _).comp hlim
  have hεlim : Tendsto (fun k => ε (φ k)) atTop (𝓝 0) :=
    tendsto_one_div_add_atTop_nhds_zero_nat.comp hφ.tendsto_atTop
  have hcoord : ∀ x, Tendsto (fun k => m (φ k) x) atTop (𝓝 (μ x)) := fun x =>
    ((continuous_apply x).tendsto μ).comp hμlim
  have hT : Tendsto (fun k => ∑ x, m (φ k) x * A (φ k) x y - r (φ k) * m (φ k) y) atTop
      (𝓝 (∑ x, μ x * (K.Q x y + 0) - l * μ y)) := by
    apply Tendsto.sub _ (hrlim.mul (hcoord y))
    apply tendsto_finsetSum
    intro x _
    simp only [hA]
    exact (hcoord x).mul (tendsto_const_nhds.add hεlim)
  have hz : (fun k => ∑ x, m (φ k) x * A (φ k) x y - r (φ k) * m (φ k) y) = fun _ => 0 := by
    funext k; rw [heig]; ring
  rw [hz] at hT
  have := tendsto_nhds_unique hT tendsto_const_nhds
  simp only [add_zero] at this
  linarith

/-- **Theorem 2 on every face**: every finite killed chain with local death factors has a
quasi-stationary law, and for it log τ = ∫₀¹ ⟨E⟩_s ds = ∑_i c_i. -/
theorem tilt_identity_exists [Nonempty σ] {V : Type*} [Fintype V] (K : KilledChain σ)
    (L : K.LocalDeath V) :
    ∃ μ lam, K.IsQSD μ lam ∧
      Real.log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧
      Real.log (K.lifetime μ) = ∑ i, L.price μ i := by
  obtain ⟨μ, lam, hμ⟩ := K.exists_qsd
  obtain ⟨h1, h2, -⟩ := tilt_identity L hμ
  exact ⟨μ, lam, hμ, h1, h2⟩

end KilledChain
end Gump.Chain
