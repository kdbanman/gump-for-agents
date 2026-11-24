/-
ref-chain: what the chain theorems' statements do and do not pin down.  Every item compiles against the
chain agent's modules as built (no edits to them).

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/RefChainVacuity.lean

1. `point_qsd`, `point_lifetime`: a living state that dies surely carries a quasi-stationary law with λ = 0
   and τ = 1 (log τ = 0).
2. `kagome_all_dies`: on the kagome layer (every wrapped face) the all-alive state dies surely.
   Hence `junk_tilt_identity_product`: the conclusion of `ProductKernel.tilt_identity_product` (and so of
   `tilt_identity_exists`, `surrogate_theorems`, `bit_surrogate`, whose μ is only "some QSD") is satisfied on
   every wrapped face by a law with log τ = 0, not the face's lifetime (ln τ = 3.98 on torus (2,0),(0,2)).
3. `lumped`, `lumped_price_zero`, `exists_lumped`: local death factors are not unique; one factor can carry
   the whole death probability.  So a conclusion "∃ L, log τ = ∑ i, L.price μ i" (as in `bit_surrogate`)
   says nothing about the per-cell prices: it holds with all prices but one equal to 0.
4. Inhabitants: a growing family of `Face`s satisfying `SSM` (so `SSM`, `IntSSM`, `Face` are not empty);
   `torus_2_0_2_one_price` instantiated with an actual `Fintype` instance at (0.44, 0.42).
5. `SSM.toIntSSM'`: the integrability hypothesis of `SSM.toIntSSM` is redundant for any family with
   arbitrarily small error terms (by the chain agent's own `SSM.einf_continuousOn`).
6. `price_of_ae`: `price_of_pointwise` with convergence required only for almost every s (the hypothesis
   as stated, convergence at every s ∈ (0,1], can fail exactly at the jump point of a first-order
   transition).
7. `card_torus_2_0_2`: |T| = 4 for the 12-cell torus, so `torus_2_0_2_one_price` does give log τ = 12 c.
8. `noDeath_lifetime`: `lifetime` is 0 (a junk tsum) for a chain that never dies; no headline theorem is
   affected, since each carries `LocalDeath` (death > 0 everywhere) or a hypothesis r < 1.
-/
import GumpMath.ChainTilt
import GumpMath.ChainKagome
import GumpMath.ChainTorus
import GumpMath.ChainBits
import GumpMath.ChainTiltLimit

open Finset Filter Topology MeasureTheory
open Gump.Chain

namespace RefChain

/-! ### 1. A surely-dying state carries a QSD with λ = 0 and τ = 1 -/

theorem point_qsd {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ) (z : σ)
    (hz : ∀ y, K.Q z y = 0) : K.IsQSD (fun x => if x = z then 1 else 0) 0 := by
  refine ⟨fun x => by split_ifs <;> norm_num, by simp, fun y => ?_⟩
  simp [ite_mul, hz]

theorem point_lifetime {σ : Type*} [Fintype σ] [DecidableEq σ] (K : KilledChain σ) (z : σ)
    (hz : ∀ y, K.Q z y = 0) : K.lifetime (fun x => if x = z then 1 else 0) = 1 := by
  have hq := point_qsd K z hz
  have hh : K.hazard (fun x => if x = z then 1 else 0) = 1 := by
    simp [KilledChain.hazard, KilledChain.death, hz, ite_mul]
  rw [hq.lifetime_eq (by rw [hh]; norm_num), hh]; norm_num

/-! ### 2. On every wrapped face the all-alive state dies surely -/

section Kagome
open Gump.Chain.Kagome
variable {T : Type*} [AddCommGroup T] [Fintype T] [DecidableEq T] (e1 e2 : T)
variable {ρ1 ρ2 : ℝ} (h1 : 0 < ρ1) (h1' : ρ1 < 1) (h2 : 0 < ρ2) (h2' : ρ2 < 1)

/-- The all-alive state. -/
def allLive : Living (Cell T) := ⟨univ, ⟨(Orient.X, 0), mem_univ _⟩⟩

theorem k_univ (c : Cell T) : k e1 e2 (univ : Finset (Cell T)) c = 6 := by
  unfold k
  rw [List.countP_eq_length.2 (fun d _ => by simp)]
  exact length_nbrs e1 e2 c

theorem kagome_all_dies (y : Living (Cell T)) :
    (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.Q allLive y = 0 := by
  show (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').P univ y.1 = 0
  obtain ⟨c, hc⟩ := y.2
  apply Finset.prod_eq_zero (mem_univ c)
  have hd : death3 ρ1 ρ2 true 6 = 1 := by
    have := coin3_total ρ1 ρ2
    simp only [death3, aliveNext]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero] at this ⊢
    norm_num at this ⊢
    linarith
  simp only [hc, ite_true, kernel, k_univ, mem_univ, decide_true, hd, sub_self]

/-- **The existential Theorem 2 is met by a junk law.**  On every wrapped face there is a QSD (λ = 0, the
point mass on the all-alive state) for which every clause of `tilt_identity_product` holds and log τ = 0. -/
theorem junk_tilt_identity_product :
    ∃ μ lam, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.IsQSD μ lam ∧ lam = 0 ∧
      Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) =
        ∫ s in (0:ℝ)..1, tiltMean μ (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.energy s
          (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.energy ∧
      Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) =
        ∑ i, (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath.price μ i ∧
      Real.log ((kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed.lifetime μ) = 0 := by
  set K := (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').toSubsetChain.killed
  set z : Living (Cell T) := allLive
  have hz := kagome_all_dies e1 e2 h1 h1' h2 h2'
  have hq := point_qsd K z hz
  obtain ⟨t1, t2, -⟩ := KilledChain.tilt_identity (kernel e1 e2 ρ1 ρ2 h1 h1' h2 h2').localDeath hq
  refine ⟨_, 0, hq, rfl, t1, t2, ?_⟩
  rw [point_lifetime K z hz, Real.log_one]

/-- The junk law is not the law of `wrapped_lemma0`/`kagome_lemma0` (that one charges every state). -/
theorem junk_ne_physical (μ : Living (Cell T) → ℝ) (hμ : ∀ x, 0 < μ x)
    (x : Living (Cell T)) (hx : x ≠ allLive) :
    μ ≠ fun y => if y = allLive then 1 else 0 := by
  intro h
  have := hμ x
  rw [h] at this
  simp [hx] at this

end Kagome

/-! ### 3. Local death factors are not unique: one factor can carry everything -/

section Lumped
variable {σ V : Type*} [Fintype σ] [DecidableEq σ] [Fintype V] [DecidableEq V]

omit [DecidableEq σ] in
theorem death_le_one (K : KilledChain σ) (x : σ) : K.death x ≤ 1 := by
  have : 0 ≤ ∑ y, K.Q x y := Finset.sum_nonneg (fun y _ => K.nonneg x y)
  simp only [KilledChain.death]; linarith

/-- The whole death probability on the cell i0, factor 1 on every other cell. -/
noncomputable def lumped (K : KilledChain σ) (hpos : ∀ x, 0 < K.death x) (i0 : V) : K.LocalDeath V where
  dc := fun i x => if i = i0 then K.death x else 1
  pos := fun i x => by split_ifs; exacts [hpos x, one_pos]
  le_one := fun i x => by split_ifs; exacts [death_le_one K x, le_refl _]
  prod := fun x => by simp [Finset.prod_ite_eq']

theorem lumped_price_zero (K : KilledChain σ) (hpos : ∀ x, 0 < K.death x) (i0 : V) (μ : σ → ℝ)
    (i : V) (hi : i ≠ i0) : (lumped K hpos i0).price μ i = 0 := by
  simp [KilledChain.LocalDeath.price, KilledChain.LocalDeath.cost, lumped, hi, tiltMean]

/-- **"∃ L, log τ = ∑ L.price" is empty of per-cell content**: whenever some local factorisation exists,
another one gives log τ = ∑_i c_i with c_i = 0 for every i ≠ i0. -/
theorem exists_lumped (K : KilledChain σ) (L : K.LocalDeath V) {μ : σ → ℝ} {lam : ℝ}
    (hμ : K.IsQSD μ lam) (i0 : V) :
    ∃ L' : K.LocalDeath V, Real.log (K.lifetime μ) = ∑ i, L'.price μ i ∧
      ∀ i, i ≠ i0 → L'.price μ i = 0 := by
  have hpos : ∀ x, 0 < K.death x := fun x => by
    rw [L.prod x]; exact Finset.prod_pos (fun i _ => L.pos i x)
  exact ⟨lumped K hpos i0, (KilledChain.tilt_identity (lumped K hpos i0) hμ).2.1,
    fun i hi => lumped_price_zero K hpos i0 μ i hi⟩

end Lumped

/-! ### 4. Inhabitants: a growing family of faces satisfying (SSM); the 12-cell torus instantiated -/

section Inhabit

/-- n independent cells, each dying w.p. 1/2 each generation; the face dies when all do. -/
noncomputable def fam (n : ℕ) : Face where
  σ := Unit
  V := Fin (n + 1)
  K := ⟨fun _ _ => 1 - (1 / 2 : ℝ) ^ (n + 1),
    fun _ _ => by have : (1 / 2 : ℝ) ^ (n + 1) ≤ 1 := pow_le_one₀ (by norm_num) (by norm_num); linarith,
    fun _ => by
      simp only [Finset.univ_unique, Finset.sum_singleton]
      have : (0 : ℝ) ≤ (1 / 2) ^ (n + 1) := by positivity
      linarith⟩
  L := ⟨fun _ _ => 1 / 2, fun _ _ => by norm_num, fun _ _ => by norm_num, fun _ => by
    simp [KilledChain.death]⟩
  μ := fun _ => 1
  lam := 1 - (1 / 2 : ℝ) ^ (n + 1)
  qsd := ⟨fun _ => by norm_num, by simp, fun _ => by simp⟩
  r := fun _ => (n : ℝ)

theorem fam_area (n : ℕ) : (fam n).area = n + 1 := by simp [Face.area, fam]

theorem fam_localMean (n : ℕ) (i : (fam n).V) (s : ℝ) : (fam n).localMean i s = Real.log 2 := by
  have hc : ∀ x, (fam n).L.cost i x = Real.log 2 := fun x => by
    simp [KilledChain.LocalDeath.cost, fam]
  have hZ := Z_pos (fam n).qsd.isProb (fam n).L.energy s
  simp only [Face.localMean, tiltMean, hc]
  rw [← Finset.sum_mul, show (∑ x, tw (fam n).μ (fam n).L.energy s x) = Z (fam n).μ (fam n).L.energy s
    from rfl, mul_comm, mul_div_assoc, div_self hZ.ne', mul_one]

theorem fam_SSM : SSM fam (fun _ => Real.log 2) 0 1 0 := by
  intro g i s _
  rw [fam_localMean]; simp

theorem fam_price : Tendsto (fun n => (fam n).logTau / (fam n).area) atTop (𝓝 (Real.log 2)) := by
  have hI : IntSSM fam (Real.log 2) 0 1 0 := by
    have := fam_SSM.toIntSSM intervalIntegrable_const
    simpa using this
  have hA : Tendsto (fun n => ((fam n).area : ℝ)) atTop atTop := by
    have : (fun n => ((fam n).area : ℝ)) = fun n : ℕ => (n : ℝ) + 1 := by
      funext n; simp [Face.area, fam]
    rw [this]; exact tendsto_atTop_add_const_right _ 1 tendsto_natCast_atTop_atTop
  have hloc : Tendsto (fun n => (∑ i, Real.exp (-((fam n).r i / 1))) / ((fam n).area : ℝ)) atTop (𝓝 0) := by
    have : (fun n => (∑ i, Real.exp (-((fam n).r i / 1))) / ((fam n).area : ℝ)) =
        fun n : ℕ => Real.exp (-(n : ℝ)) := by
      funext n
      have hs : (∑ i : (fam n).V, Real.exp (-((fam n).r i / 1))) =
          ((fam n).area : ℝ) * Real.exp (-(n:ℝ)) := by
        have hr : ∀ i : (fam n).V, Real.exp (-((fam n).r i / 1)) = Real.exp (-(n:ℝ)) := fun i => by
          simp [fam]
        rw [Finset.sum_congr rfl (fun i _ => hr i), Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
        rfl
      rw [hs, fam_area]
      push_cast
      field_simp
    rw [this]
    exact Real.tendsto_exp_neg_atTop_nhds_zero.comp tendsto_natCast_atTop_atTop
  exact thm3d le_rfl hI hA hloc

open Gump.Chain.Kagome in
/-- `torus_2_0_2_one_price` with a real `Fintype` instance and the densities (0.44, 0.42). -/
theorem torus_2_0_2_instantiated : True := by
  haveI : Finite (Torus 2 0 2) := torus_finite 2 0 2 (by norm_num) (by norm_num)
  haveI := Fintype.ofFinite (Torus 2 0 2)
  classical
  have := torus_2_0_2_one_price (ρ1 := 0.44) (ρ2 := 0.42) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num)
  trivial

end Inhabit

/-! ### 5. The integrability hypothesis of `SSM.toIntSSM` is redundant for families that matter -/

theorem SSM.toIntSSM' {ι : Type*} {F : ι → Face} {einf : ℝ → ℝ} {K ξ K0 : ℝ}
    (h : SSM F einf K ξ K0)
    (hlarge : ∀ δ > 0, ∃ g, ∃ i : (F g).V, K * Real.exp (-((F g).r i / ξ)) + K0 / (F g).area < δ) :
    IntSSM F (∫ s in (0:ℝ)..1, einf s) K ξ K0 :=
  h.toIntSSM ((SSM.einf_continuousOn h hlarge).intervalIntegrable_of_Icc zero_le_one)

/-! ### 6. `price_of_pointwise` from convergence at almost every tilt -/

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

/-! ### 7. The 12-cell torus has |T| = 4 -/

section Card
open Gump.Chain.Kagome

theorem lattice_202_even (p : ℤ × ℤ) (hp : p ∈ lattice 2 0 2) : 2 ∣ p.1 ∧ 2 ∣ p.2 := by
  let E : AddSubgroup (ℤ × ℤ) :=
    { carrier := {p | 2 ∣ p.1 ∧ 2 ∣ p.2}
      add_mem' := fun ha hb => ⟨dvd_add ha.1 hb.1, dvd_add ha.2 hb.2⟩
      zero_mem' := ⟨dvd_zero 2, dvd_zero 2⟩
      neg_mem' := fun ha => ⟨(dvd_neg).2 ha.1, (dvd_neg).2 ha.2⟩ }
  have hle : lattice 2 0 2 ≤ E := by
    rw [lattice, AddSubgroup.closure_le]
    rintro _ (rfl | rfl) <;> exact ⟨by norm_num, by norm_num⟩
  exact hle hp

theorem card_torus_2_0_2 [Fintype (Torus 2 0 2)] : Fintype.card (Torus 2 0 2) = 4 := by
  let f : Fin 2 × Fin 2 → Torus 2 0 2 := fun p => QuotientAddGroup.mk ((p.1 : ℤ), (p.2 : ℤ))
  have hinj : Function.Injective f := by
    rintro ⟨a, b⟩ ⟨a', b'⟩ h
    have h' := QuotientAddGroup.eq.1 h
    have he := lattice_202_even _ h'
    have ha2 : (2:ℤ) ∣ -((a : ℕ) : ℤ) + ((a' : ℕ) : ℤ) := by simpa using he.1
    have hb2 : (2:ℤ) ∣ -((b : ℕ) : ℤ) + ((b' : ℕ) : ℤ) := by simpa using he.2
    have := a.isLt; have := a'.isLt; have := b.isLt; have := b'.isLt
    have ha : (a : ℕ) = a' := by omega
    have hb : (b : ℕ) = b' := by omega
    simp [Fin.ext_iff, ha, hb]
  have hsurj : Function.Surjective f := by
    intro x
    induction x using QuotientAddGroup.induction_on with
    | H z =>
      obtain ⟨a, b⟩ := z
      refine ⟨(⟨(a % 2).toNat, by omega⟩, ⟨(b % 2).toNat, by omega⟩), ?_⟩
      simp only [f]
      rw [QuotientAddGroup.eq]
      have hmem : (-(((a % 2).toNat : ℤ), ((b % 2).toNat : ℤ)) + (a, b) : ℤ × ℤ) =
          (a / 2) • ((2 : ℤ), (0 : ℤ)) + (b / 2) • ((0 : ℤ), (2 : ℤ)) := by
        have e1 : (((a % 2).toNat : ℤ)) = a % 2 := Int.toNat_of_nonneg (Int.emod_nonneg a (by norm_num))
        have e2 : (((b % 2).toNat : ℤ)) = b % 2 := Int.toNat_of_nonneg (Int.emod_nonneg b (by norm_num))
        rw [e1, e2]
        ext <;> simp <;> omega
      show _ ∈ lattice 2 0 2
      rw [hmem]
      exact add_mem (zsmul_mem (AddSubgroup.subset_closure (by simp)) _)
        (zsmul_mem (AddSubgroup.subset_closure (by simp)) _)
  rw [← Fintype.card_of_bijective ⟨hinj, hsurj⟩]
  simp

end Card

/-! ### 8. `lifetime` is a junk 0 for a chain that never dies -/

def noDeath : KilledChain Unit := ⟨fun _ _ => 1, fun _ _ => zero_le_one, fun _ => by simp⟩

theorem noDeath_qsd : noDeath.IsQSD (fun _ => 1) 1 := ⟨fun _ => zero_le_one, by simp, fun _ => by simp [noDeath]⟩

theorem noDeath_lifetime : noDeath.lifetime (fun _ => 1) = 0 := by
  have hs : ∀ t, noDeath.survival (fun _ => 1) t = 1 := fun t => by
    rw [noDeath_qsd.survival_eq t, one_pow]
  simp only [KilledChain.lifetime, hs]
  exact tsum_eq_zero_of_not_summable (fun h => by
    have := h.tendsto_atTop_zero
    have h1 : Tendsto (fun _ : ℕ => (1 : ℝ)) atTop (𝓝 1) := tendsto_const_nhds
    exact one_ne_zero (tendsto_nhds_unique h1 this))

end RefChain

#print axioms RefChain.junk_tilt_identity_product
#print axioms RefChain.exists_lumped
#print axioms RefChain.fam_price
#print axioms RefChain.price_of_ae
#print axioms RefChain.card_torus_2_0_2
#print axioms RefChain.noDeath_lifetime
