/-
**Every wrapped face, for `Face.P` itself** (`wrapped_full`), under the single hypothesis `TorusNb H K D`
(`LinkWrapped.lean`). Under it `Face.P` on `torus H K D` is, entry by entry, the kagome kernel of the chain arm
over `Torus H K D` (`Q_eq`), and the chain arm's theorems on the wrapped layer transport along the relabelling.
`TorusNb` is checked by the kernel (`decide +kernel`) on the tori at the end (`wrapped_full_<H>_<K>_<D>`).
-/
import GumpMath.LinkWrapped

set_option linter.unusedSectionVars false

namespace Gump.Link.Wrapped
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Chain.Kagome Gump.Chain.Bits Gump.Link Finset

theorem _root_.Gump.Link.SDens.r0 {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) : (0 : ℝ) < ρ1 := by exact_mod_cast hs.h0
theorem _root_.Gump.Link.SDens.r1 {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) : (ρ1 : ℝ) < 1 := by exact_mod_cast hs.h1
theorem _root_.Gump.Link.SDens.r2 {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) : (0 : ℝ) < ρ2 := by exact_mod_cast hs.h2
theorem _root_.Gump.Link.SDens.r3 {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) : (ρ2 : ℝ) < 1 := by exact_mod_cast hs.h3

/-- The local death factors of `Face.P` on the wrapped face (all its coins). -/
noncomputable abbrev LT (H K D : ℕ) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) :=
  localDeath (torus H K D) hs (cellsOK_of_allcoins (torus H K D) (fun _ => rfl))

section Kernel
variable (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (hnb : TorusNb H K D)
variable [Fintype (Torus (H : ℤ) K D)] [DecidableEq (Torus (H : ℤ) K D)]
variable {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2)

/-- The kagome kernel over `Torus H K D` at (ρ1, ρ2). -/
noncomputable abbrev ker : ProductKernel (Cell (Torus (H : ℤ) K D)) :=
  kernel (te1 (H : ℤ) K D) (te2 (H : ℤ) K D) (ρ1 : ℝ) (ρ2 : ℝ) hs.r0 hs.r1 hs.r2 hs.r3

include hnb in
theorem k_eq (i : Fin (torus H K D).A) (x : Fin (2 ^ (torus H K D).A)) :
    (torus H K D).k x i =
      Kagome.k (te1 (H : ℤ) K D) (te2 (H : ℤ) K D) (E (torus H K D) (cellEquiv H K D hH hD hnb.1) x)
        (cellEquiv H K D hH hD hnb.1 i) := by
  have hp := hnb.2 i (hnb.1 ▸ i.2)
  unfold Face.k Kagome.k
  rw [hp.countP_eq, cellEquiv_apply, ← kIdx_map H K D hH hD, List.countP_map]
  refine List.countP_congr (fun j hj => ?_)
  have hjA : j < (torus H K D).A := Face.nb_lt' _ i j (hp.mem_iff.2 hj)
  have : phi H K D j = cellEquiv H K D hH hD hnb.1 ⟨j, hjA⟩ := rfl
  simp only [Function.comp, this, decide_eq_true_eq, mem_E]

include hnb in
theorem a_eq (i : Fin (torus H K D).A) (x : Fin (2 ^ (torus H K D).A)) :
    aR (torus H K D) ρ1 ρ2 x i =
      (ker H K D hs).a (cellEquiv H K D hH hD hnb.1 i) (E (torus H K D) (cellEquiv H K D hH hD hnb.1) x) := by
  obtain ⟨h1, h2⟩ := coins_of_all (torus H K D) (fun _ => rfl) i
  show aliveProbR (ρ1 : ℝ) (ρ2 : ℝ) ((torus H K D).m1 i) ((torus H K D).m2 i) ((torus H K D).k x i)
      ((x : ℕ).testBit i) = 1 - death3 (ρ1 : ℝ) (ρ2 : ℝ) _ _
  rw [h1, h2, ← one_sub_aliveProbR_three, k_eq H K D hH hD hnb i x]
  have : decide (cellEquiv H K D hH hD hnb.1 i ∈ E (torus H K D) (cellEquiv H K D hH hD hnb.1) x) =
      (x : ℕ).testBit i := by
    rw [Bool.eq_iff_iff, decide_eq_true_iff, mem_E]
  rw [this]; ring

include hnb in
/-- **`Face.P` on the wrapped face is the kagome kernel**, entry by entry, along the relabelling. -/
theorem Q_eq (x y : {x : Fin (2 ^ (torus H K D).A) // x ≠ (torus H K D).empty}) :
    (ker H K D hs).toSubsetChain.killed.Q (stateEquiv (torus H K D) (cellEquiv H K D hH hD hnb.1) x)
      (stateEquiv (torus H K D) (cellEquiv H K D hH hD hnb.1) y) = (chain (torus H K D) hs.dens).Q x y := by
  rw [chain_Q, P_cast]
  show ProductKernel.P _ _ _ = _
  unfold ProductKernel.P bitP
  rw [stateEquiv_val, stateEquiv_val, Finset.prod_range]
  refine Eq.trans (Equiv.prod_comp (cellEquiv H K D hH hD hnb.1) _).symm ?_
  refine prod_congr rfl (fun i _ => ?_)
  rw [a_eq H K D hH hD hnb hs i x]
  by_cases hb : ((y.1 : Fin _) : ℕ).testBit i = true
  · rw [if_pos ((mem_E _ _ _ _).2 hb), if_pos hb]
  · rw [if_neg (fun h => hb ((mem_E _ _ _ _).1 h)), if_neg hb]

include hH hD hnb in
theorem dc_eq (i : Fin (torus H K D).A) (x : {x : Fin (2 ^ (torus H K D).A) // x ≠ (torus H K D).empty}) :
    (ker H K D hs).localDeath.dc (cellEquiv H K D hH hD hnb.1 i)
      (stateEquiv (torus H K D) (cellEquiv H K D hH hD hnb.1) x) = (LT H K D hs).dc i x := by
  rw [localDeath_dc, a_cast, a_eq H K D hH hD hnb hs i x]
  rfl

end Kernel

/-- **Every wrapped face, for `Face.P` itself**, at every strict densities 0 < ρ1, ρ2 < 1, under `TorusNb`:
a dominant quasi-stationary law (the dice agent's `IsQSD` too) with λ > 0, positive on every living state and
unique among λ > 0; ln τ is the sum of the cells' prices, with one price per orientation (cells i, j with
i ≡ j mod 3); survival from every state that can survive decays at exactly λ; the chain's survival function is
the dice agent's `Face.survival`; and on a rotation-invariant torus, one price per cell. -/
theorem wrapped_theorems (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (hnb : TorusNb H K D) {ρ1 ρ2 : ℚ}
    (hs : SDens ρ1 ρ2) :
    ∃ μ lam, (chain (torus H K D) hs.dens).IsDominantQSD μ lam ∧
      IsQSD (torus H K D) ρ1 ρ2 (extend (torus H K D) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (torus H K D) hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, (LT H K D hs).dc i x = 1 - (((torus H K D).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (torus H K D) hs.dens).lifetime μ) = ∑ i, (LT H K D hs).price μ i ∧
      (∀ i j : Fin (torus H K D).A, (i : ℕ) % 3 = (j : ℕ) % 3 → (LT H K D hs).price μ i = (LT H K D hs).price μ j) ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (torus H K D) hs.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (torus H K D) hs.dens).survFrom t x) ∧
        (∀ t x, (chain (torus H K D) hs.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧
      (∀ t x, (chain (torus H K D) hs.dens).survFrom t x = (((torus H K D).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧
      (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D →
        ∀ i j, (LT H K D hs).price μ i = (LT H K D hs).price μ j) := by
  classical
  have hHz : (0 : ℤ) < H := by exact_mod_cast hH
  have hDz : (0 : ℤ) < D := by exact_mod_cast hD
  let _ : Fintype (Torus (H : ℤ) K D) := (torus_fintype (H : ℤ) K D hHz hDz).some
  set F := torus H K D with hF
  have hA := hnb.1
  have hApos : 0 < F.A := by rw [hA]; positivity
  set f := cellEquiv H K D hH hD hA with hf
  set eL := stateEquiv F f with heL
  have hQ := Q_eq H K D hH hD hnb hs
  have hc := dc_eq H K D hH hD hnb hs
  obtain ⟨hirr, hout, hin, μ', lam', hq', hlam', hpos', huniq'⟩ :=
    wrapped_lemma0 (H : ℤ) K D hs.r0 hs.r1 hs.r2 hs.r3
  obtain ⟨μ, lam, hDom, hdice, hdc, hpr, -, -⟩ := face_theorems_allcoins F (fun _ => rfl) hs hApos
  have huniqF : ∀ ν l, (chain F hs.dens).IsQSD ν l → 0 < l → ν = (fun x => μ' (eL x)) ∧ l = lam' := by
    intro ν l hν hl
    obtain ⟨h1, h2⟩ := huniq' _ _ (transport_qsd' eL hQ hν) hl
    refine ⟨funext fun x => ?_, h2⟩
    have := congrFun h1 (eL x)
    simpa using this
  have hqF := transport_qsd eL hQ hq'
  have hlam : 0 < lam := lt_of_lt_of_le hlam' (hDom.max _ _ hqF)
  obtain ⟨hμeq, hlameq⟩ := huniqF μ lam hDom.qsd hlam
  have hprice : ∀ i, (LT H K D hs).price μ i = (ker H K D hs).localDeath.price μ' (f i) := by
    intro i
    rw [hμeq]
    exact transport_price eL hQ (LT H K D hs) (ker H K D hs).localDeath f (fun i x => hc i x) μ' i
  refine ⟨μ, lam, hDom, hdice, hlam, fun x => by rw [hμeq]; exact hpos' _,
    fun ν l hν hl => ?_, hdc, hpr, fun i j hij => ?_, ?_,
    survFrom_cast F hs.dens (absorbing_of_coins F ρ1 ρ2 (fun _ => rfl)), fun hl1 hl2 i j => ?_⟩
  · obtain ⟨h1, h2⟩ := huniqF ν l hν hl
    exact ⟨h1.trans hμeq.symm, h2.trans hlameq.symm⟩
  · obtain ⟨μ2, lam2, hq2, hlam2, -, hor, -⟩ :=
      wrapped_one_price_HD (H : ℤ) K D hHz hDz hs.r0 hs.r1 hs.r2 hs.r3
    obtain ⟨rfl, -⟩ := huniq' μ2 lam2 hq2 hlam2
    rw [hprice, hprice, hf, cellEquiv_apply, cellEquiv_apply]
    unfold phi
    rw [hij]
    exact hor _ _ _
  · -- decay, from the kagome chain
    set C := (ker H K D hs).toSubsetChain with hC
    have hcl : ∀ y, C.killed.CanSurvive y → C.canLive y := fun y ⟨z, hz⟩ => by
      by_contra hn
      rw [hout y hn z] at hz
      exact lt_irrefl 0 hz
    haveI : Nonempty {x // C.canLive x} :=
      ⟨⟨⟨uX, uX_nonempty⟩, hcl _ ⟨⟨uX, uX_nonempty⟩, hin _⟩⟩⟩
    obtain ⟨r, m, M, -, hm, hmM, hrate, hlo, hup⟩ := decay_bounds C.killed C.canLive hirr hout
    have hr : lam = r := by rw [hlameq]; exact hrate μ' lam' hq' hlam'
    refine ⟨m, M, hm, hmM, fun t x hx => ?_, fun t x => ?_⟩
    · rw [transport_survFrom eL hQ, hr]
      exact hlo t _ (hcl _ ((transport_canSurvive eL hQ x).1 hx))
    · rw [transport_survFrom eL hQ, hr]
      exact hup t _
  · obtain ⟨μ3, lam3, hq3, hlam3, hall, -⟩ :=
      wrapped_rotation_HD (H : ℤ) K D hHz hDz hs.r0 hs.r1 hs.r2 hs.r3 hl1 hl2
    obtain ⟨rfl, -⟩ := huniq' μ3 lam3 hq3 hlam3
    rw [hprice, hprice]
    exact hall _ _

/-- **Every wrapped face at (ρ1, ρ2) = (0.44, 0.42)**: `wrapped_theorems`, and ln τ < 1.9228·A
(the dice agent's `lntau_le_torus`, every wrapped face). -/
theorem wrapped_full (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (hnb : TorusNb H K D) :
    ∃ μ lam, (chain (torus H K D) Hull3.sdens.dens).IsDominantQSD μ lam ∧
      IsQSD (torus H K D) ρ1 ρ2 (extend (torus H K D) μ) lam ∧
      0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (torus H K D) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, (LT H K D Hull3.sdens).dc i x = 1 - (((torus H K D).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) = ∑ i, (LT H K D Hull3.sdens).price μ i ∧
      (∀ i j : Fin (torus H K D).A, (i : ℕ) % 3 = (j : ℕ) % 3 →
        (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j) ∧
      Real.log ((chain (torus H K D) Hull3.sdens.dens).lifetime μ) < 1.9228 * (torus H K D).A ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (torus H K D) Hull3.sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (torus H K D) Hull3.sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧
      (∀ t x, (chain (torus H K D) Hull3.sdens.dens).survFrom t x =
        (((torus H K D).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧
      (((K : ℤ), -(H : ℤ) - K) ∈ lattice (H : ℤ) K D → ((D : ℤ), -(D : ℤ)) ∈ lattice (H : ℤ) K D →
        ∀ i j, (LT H K D Hull3.sdens).price μ i = (LT H K D Hull3.sdens).price μ j) := by
  obtain ⟨μ, lam, hDom, hdice, hlam, hpos, huniq, hdc, hpr, hor, hdec, hsurv, hrot⟩ :=
    wrapped_theorems H K D hH hD hnb Hull3.sdens
  have hApos : 0 < (torus H K D).A := by rw [hnb.1]; positivity
  refine ⟨μ, lam, hDom, hdice, hlam, hpos, huniq, hdc, hpr, hor, ?_, hdec, hsurv, hrot⟩
  rw [log_lifetime_eq (LT H K D Hull3.sdens) hDom.qsd]
  exact lntau_le_torus H K D hH hD _ lam hdice hApos

/-! ### The hypothesis, checked by the kernel -/

theorem torusNb_1_0_1 : TorusNb 1 0 1 := torusNb_of (by decide +kernel)
theorem torusNb_2_0_2 : TorusNb 2 0 2 := torusNb_of (by decide +kernel)

end Gump.Link.Wrapped
