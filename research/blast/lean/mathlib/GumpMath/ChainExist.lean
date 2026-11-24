/-
Every finite killed chain has a quasi-stationary law (the weak Perron theorem), with no irreducibility:
perturb Q to the positive matrix Q + J/(k+1), take its positive Perron row vector (`ChainPerron.lean`),
normalise, and pass to a convergent subsequence in the compact set (simplex) × [0, 1 + |σ|].

The law obtained is the **dominant** one (`IsDominantQSD`, repair D2 of `research/blast/ref-chain/REVIEW.md`):
its λ is at least the λ' of every quasi-stationary law, at least Q u u for every state u (so λ > 0, and
τ ≥ 1/(1 - Q u u), on any face with a state that can persist), and it is the exponential decay rate of the
longest-lived start: P_x(T > t) ≤ C_ε (λ + ε)^t for every x and ε > 0, and P_x(T > t) ≥ λ^t for some x at
every t.  (A point mass on a surely-dying state, λ = 0, is excluded on every such face.)

So Theorem 2 holds on every face, hull faces and strips included, for which irreducibility is not proved,
for that law: `tilt_identity_exists`.
-/
import Mathlib
import GumpMath.ChainPerron

set_option linter.unusedSectionVars false

namespace Gump.Chain
open Finset Matrix Filter Topology

variable {σ : Type*} [Fintype σ] [DecidableEq σ]

namespace KilledChain

/-- The dominant quasi-stationary law: λ maximal among all quasi-stationary laws, λ ≥ Q u u for every
state, and λ the exponential decay rate of max_x P_x(T > t), P_x(T > t) = ((Q^t) 1)(x). -/
structure IsDominantQSD (K : KilledChain σ) (μ : σ → ℝ) (lam : ℝ) : Prop where
  qsd : K.IsQSD μ lam
  max : ∀ ν lam', K.IsQSD ν lam' → lam' ≤ lam
  diag : ∀ u, K.Q u u ≤ lam
  decay_up : ∀ ε > 0, ∃ C, ∀ (t : ℕ) x, ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x ≤ C * (lam + ε) ^ t
  decay_lo : ∀ t : ℕ, ∃ x, lam ^ t ≤ ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x

omit [DecidableEq σ] in
theorem pow_entry_mono {A B : Matrix σ σ ℝ} [DecidableEq σ] (hA : ∀ i j, 0 ≤ A i j)
    (hAB : ∀ i j, A i j ≤ B i j) (t : ℕ) : ∀ i j, (A ^ t) i j ≤ (B ^ t) i j := by
  induction t with
  | zero => intro i j; exact le_refl _
  | succ t ih =>
    intro i j
    rw [pow_succ, pow_succ, Matrix.mul_apply, Matrix.mul_apply]
    exact Finset.sum_le_sum (fun l _ => mul_le_mul (ih i l) (hAB l j) (hA l j)
      ((pow_entry_nonneg hA t i l).trans (ih i l)))

/-- **Existence of the dominant quasi-stationary law** for every finite killed chain on a nonempty set of
states (the weak Perron theorem, with the law identified). -/
theorem exists_qsd [Nonempty σ] (K : KilledChain σ) : ∃ μ lam, K.IsDominantQSD μ lam := by
  let ε : ℕ → ℝ := fun k => 1 / ((k : ℝ) + 1)
  have hε : ∀ k, 0 < ε k := fun k => by simp only [ε]; positivity
  let A : ℕ → Matrix σ σ ℝ := fun k => K.Q + Matrix.of (fun _ _ => ε k)
  have hA : ∀ k x y, A k x y = K.Q x y + ε k := fun k x y => rfl
  have hApos : ∀ k x y, 0 < A k x y := fun k x y => by
    rw [hA]; exact add_pos_of_nonneg_of_pos (K.nonneg x y) (hε k)
  have hQA : ∀ k x y, K.Q x y ≤ A k x y := fun k x y => by rw [hA]; linarith [hε k]
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
  -- right Perron vectors, with the same eigenvalue
  choose r' hr' w hw hwe using
    fun k => exists_pos_eigenvector (fun x y => (hApos k x y).le) (hirr k)
  have hleft : ∀ k, m k ᵥ* A k = r k • m k := fun k => by
    funext y; simp only [Matrix.vecMul, dotProduct, Pi.smul_apply, smul_eq_mul]; exact heig k y
  have hrr : ∀ k, r k = r' k := fun k =>
    left_eigenvalue_eq (hw k) (hwe k) (ξ := m k) ⟨(hm k).1, (hm k).2⟩ (hleft k)
  -- every quasi-stationary law has λ' ≤ r k
  have hmaxk : ∀ ν lam', K.IsQSD ν lam' → ∀ k, lam' ≤ r k := by
    intro ν lam' hν k
    have h1 : ν ⬝ᵥ (A k *ᵥ w k) = (ν ᵥ* A k) ⬝ᵥ w k := Matrix.dotProduct_mulVec ν (A k) (w k)
    rw [hwe k, dotProduct_smul, smul_eq_mul] at h1
    have h2 : lam' * (ν ⬝ᵥ w k) ≤ (ν ᵥ* A k) ⬝ᵥ w k := by
      simp only [dotProduct, Matrix.vecMul, Finset.mul_sum]
      refine Finset.sum_le_sum (fun y _ => ?_)
      have hy : lam' * ν y ≤ ∑ x, ν x * A k x y := by
        rw [← hν.eigen y]
        exact Finset.sum_le_sum (fun x _ => mul_le_mul_of_nonneg_left (hQA k x y) (hν.nonneg x))
      calc lam' * (ν y * w k y) = (lam' * ν y) * w k y := by ring
        _ ≤ (∑ x, ν x * A k x y) * w k y := mul_le_mul_of_nonneg_right hy (hw k y).le
    have hpos : 0 < ν ⬝ᵥ w k := by
      obtain ⟨x, hx⟩ := exists_pos_of_isProb hν.isProb
      simp only [dotProduct]
      exact Finset.sum_pos' (fun y _ => mul_nonneg (hν.nonneg y) (hw k y).le)
        ⟨x, mem_univ x, mul_pos hx (hw k x)⟩
    rw [hrr k]
    by_contra hc
    push Not at hc
    have : r' k * (ν ⬝ᵥ w k) < lam' * (ν ⬝ᵥ w k) := mul_lt_mul_of_pos_right hc hpos
    linarith
  -- r k ≥ Q u u
  have hdiagk : ∀ u k, K.Q u u ≤ r k := by
    intro u k
    have hmu : 0 < m k u := div_pos (hv k u) (hsum k)
    have h1 : m k u * A k u u ≤ ∑ x, m k x * A k x u :=
      single_le_sum (f := fun x => m k x * A k x u)
        (fun x _ => mul_nonneg ((hm k).1 x) (hApos k x u).le) (mem_univ u)
    rw [heig k u] at h1
    have h2 : A k u u ≤ r k := by
      by_contra hc; push Not at hc
      have := mul_lt_mul_of_pos_left hc hmu
      linarith
    linarith [hQA k u u]
  obtain ⟨⟨μ, l⟩, hmem, φ, hφ, hlim⟩ :=
    (isCompact_probSet.prod (isCompact_Icc (a := (0:ℝ)) (b := 1 + Fintype.card σ))).tendsto_subseq
      (x := fun k => (m k, r k)) (fun k => ⟨hm k, hr k, hrb k⟩)
  have hμlim : Tendsto (fun k => m (φ k)) atTop (𝓝 μ) := (continuous_fst.tendsto _).comp hlim
  have hrlim : Tendsto (fun k => r (φ k)) atTop (𝓝 l) := (continuous_snd.tendsto _).comp hlim
  have hεlim : Tendsto (fun k => ε (φ k)) atTop (𝓝 0) :=
    tendsto_one_div_add_atTop_nhds_zero_nat.comp hφ.tendsto_atTop
  have hcoord : ∀ x, Tendsto (fun k => m (φ k) x) atTop (𝓝 (μ x)) := fun x =>
    ((continuous_apply x).tendsto μ).comp hμlim
  have hq : K.IsQSD μ l := by
    refine ⟨hmem.1.1, hmem.1.2, fun y => ?_⟩
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
  have hl0 : 0 ≤ l := hq.lam_nonneg
  refine ⟨μ, l, hq, fun ν lam' hν => ?_, fun u => ?_, fun e he => ?_, fun t => ?_⟩
  · exact ge_of_tendsto hrlim (Eventually.of_forall (fun k => hmaxk ν lam' hν (φ k)))
  · exact ge_of_tendsto hrlim (Eventually.of_forall (fun k => hdiagk u (φ k)))
  · -- decay from above, through the perturbed chain whose root is within e of l
    obtain ⟨k0, hk0⟩ := (hrlim.eventually (gt_mem_nhds (show l < l + e by linarith))).exists
    set k := φ k0
    set mn := univ.inf' univ_nonempty (w k)
    set mx := univ.sup' univ_nonempty (w k)
    have hmn : 0 < mn := by rw [Finset.lt_inf'_iff]; exact fun x _ => hw k x
    refine ⟨mx / mn, fun t x => ?_⟩
    have hQt : ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x ≤ ((A k ^ t) *ᵥ fun _ => (1 : ℝ)) x := by
      simp only [Matrix.mulVec, dotProduct, mul_one]
      exact Finset.sum_le_sum (fun y _ => pow_entry_mono K.nonneg (hQA k) t x y)
    have hsurv := Gump.Certificate.survival_le (A k) (fun a b => (hApos k a b).le) (w k) (r k) (1 / mn)
      (hr k) (by positivity) (fun i => by rw [hwe k, hrr k]; simp)
      (fun i => by rw [one_div, inv_mul_eq_div, le_div_iff₀ hmn, one_mul]; exact Finset.inf'_le _ (mem_univ i))
      t x
    have hwx : w k x ≤ mx := Finset.le_sup' _ (mem_univ x)
    have hpow : r k ^ t ≤ (l + e) ^ t := pow_le_pow_left₀ (hr k) hk0.le t
    calc ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x ≤ ((A k ^ t) *ᵥ fun _ => (1 : ℝ)) x := hQt
      _ ≤ 1 / mn * (r k ^ t * w k x) := hsurv
      _ ≤ 1 / mn * ((l + e) ^ t * mx) := by
          apply mul_le_mul_of_nonneg_left _ (by positivity)
          exact mul_le_mul hpow hwx (hw k x).le (by positivity)
      _ = mx / mn * (l + e) ^ t := by ring
  · -- decay from below: the μ-average of P_x(T > t) is l^t
    have havg : ∑ x, μ x * ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x = l ^ t := by
      rw [← hq.survival_eq t]
      simp only [survival, Matrix.vecMul, Matrix.mulVec, dotProduct, mul_one, Finset.mul_sum]
      rw [Finset.sum_comm]
    by_contra hc
    push Not at hc
    obtain ⟨x0, hx0⟩ := exists_pos_of_isProb hq.isProb
    have : ∑ x, μ x * ((K.Q ^ t) *ᵥ fun _ => (1 : ℝ)) x < ∑ x, μ x * l ^ t :=
      Finset.sum_lt_sum (fun x _ => mul_le_mul_of_nonneg_left (hc x).le (hq.nonneg x))
        ⟨x0, mem_univ _, mul_lt_mul_of_pos_left (hc x0) hx0⟩
    rw [← Finset.sum_mul, hq.total, one_mul, havg] at this
    exact lt_irrefl _ this

/-- **Theorems 1 and 2 on every face, for the dominant law**: every finite killed chain with local death
factors has a dominant quasi-stationary law (λ maximal, λ ≥ Q u u, the decay rate of the longest-lived start),
and for it log τ = ∫₀¹ ⟨E⟩_s ds = ∑_i c_i, log τ ≤ E_μ[E], and τ ≥ 1/(1 - Q u u) for every state u. -/
theorem tilt_identity_exists [Nonempty σ] {V : Type*} [Fintype V] (K : KilledChain σ)
    (L : K.LocalDeath V) :
    ∃ μ lam, K.IsDominantQSD μ lam ∧
      Real.log (K.lifetime μ) = ∫ s in (0:ℝ)..1, tiltMean μ L.energy s L.energy ∧
      Real.log (K.lifetime μ) = ∑ i, L.price μ i ∧
      Real.log (K.lifetime μ) ≤ ∑ x, μ x * L.energy x ∧
      ∀ u, 1 / (1 - K.Q u u) ≤ K.lifetime μ := by
  obtain ⟨μ, lam, hD⟩ := K.exists_qsd
  obtain ⟨h1, h2, -, -, h5, h6⟩ := tilt_identity L hD.qsd
  refine ⟨μ, lam, hD, h1, h2, h6 ▸ h5, fun u => ?_⟩
  have hh : 0 < K.hazard μ := by rw [L.hazard_eq_Z]; exact Z_pos hD.qsd.isProb _ _
  rw [hD.qsd.lifetime_eq hh]
  have hl := hD.qsd.lam_eq
  have hu := hD.diag u
  exact one_div_le_one_div_of_le hh (by linarith)

end KilledChain
end Gump.Chain
