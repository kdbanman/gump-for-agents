/-
**Equal prices along the automorphisms of a face's tables** (`price_aut`), for `Face.P` on any face with its
coins and a quasi-stationary law unique among λ > 0: if π permutes the cells, carries each neighbour list to the
neighbour list of the image (up to order) and keeps the coins (`autOK`, a Boolean the kernel evaluates), then
c_{π i} = c_i. The state map is the relabelling of the live set (`LinkWrapped.stateEquiv`), and the chain arm's
`price_invariant` does the rest.

On the hull faces (`hull_full_sym`): every clause of `hull_full_all`, and equal prices along every such π; the
rotation (x,y,z) ↦ (y,z,x) and the reflection (x,y,z) ↦ (y,x,z) of the triangle are checked to be automorphisms by
the kernel in `LinkHullCert.lean`.
-/
import GumpMath.LinkHull
import GumpMath.LinkWrapped

set_option linter.unusedSectionVars false

namespace Gump.Link
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Chain.Bits Finset

section Aut
variable (F : Face)

/-- π (cell i ↦ π[i]) is an automorphism of the face's tables. -/
def autOK (π : List ℕ) : Bool :=
  (π.length == F.A) && (List.range F.A).all (fun i => decide (π.getD i 0 < F.A)) && decide π.Nodup &&
    (List.range F.A).all fun i => ((F.nb i).map (π.getD · 0)).isPerm (F.nb (π.getD i 0)) &&
      (F.m1 (π.getD i 0) == F.m1 i) && (F.m2 (π.getD i 0) == F.m2 i)

variable {F} {π : List ℕ} (hπ : autOK F π = true)
include hπ

theorem autOK_spec : π.length = F.A ∧ (∀ i < F.A, π.getD i 0 < F.A) ∧ π.Nodup ∧
    ∀ i < F.A, ((F.nb i).map (π.getD · 0)).Perm (F.nb (π.getD i 0)) ∧
      F.m1 (π.getD i 0) = F.m1 i ∧ F.m2 (π.getD i 0) = F.m2 i := by
  simp only [autOK, Bool.and_eq_true, beq_iff_eq, List.all_eq_true, List.mem_range, decide_eq_true_eq] at hπ
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := hπ
  exact ⟨h1, h2, h3, fun i hi => ⟨List.isPerm_iff.1 (h4 i hi).1.1, (h4 i hi).1.2, (h4 i hi).2⟩⟩

/-- The permutation of the cells. -/
noncomputable def autPerm : Fin F.A ≃ Fin F.A :=
  Equiv.ofBijective (fun i => ⟨π.getD i 0, (autOK_spec hπ).2.1 i i.2⟩)
    ((Finite.injective_iff_bijective).mp (fun i j e => by
      have h := congrArg Fin.val e
      simp only at h
      obtain ⟨hl, -, hnd, -⟩ := autOK_spec hπ
      have hi : (i : ℕ) < π.length := by rw [hl]; exact i.2
      have hj : (j : ℕ) < π.length := by rw [hl]; exact j.2
      rw [List.getD_eq_getElem _ _ hi, List.getD_eq_getElem _ _ hj] at h
      exact Fin.ext ((List.Nodup.getElem_inj_iff hnd).1 h)))

theorem autPerm_val (i : Fin F.A) : ((autPerm hπ i : Fin F.A) : ℕ) = π.getD i 0 := rfl

/-- The action on the living states: relabel the live set. -/
noncomputable def autState : {x : Fin (2 ^ F.A) // x ≠ F.empty} ≃ {x : Fin (2 ^ F.A) // x ≠ F.empty} :=
  ((Wrapped.stateEquiv F (Equiv.refl _)).trans
    (Equiv.subtypeEquiv (Equiv.finsetCongr (autPerm hπ)) (fun s => by simp [Equiv.finsetCongr_apply]))).trans
    (Wrapped.stateEquiv F (Equiv.refl _)).symm

theorem autState_bit (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}) (i : Fin F.A) :
    ((autState hπ x).1 : ℕ).testBit (autPerm hπ i) = (x.1 : ℕ).testBit i := by
  have key : (Wrapped.stateEquiv F (Equiv.refl _) (autState hπ x)).1 =
      (Wrapped.E F (Equiv.refl _) x.1).map (autPerm hπ).toEmbedding := by
    simp only [autState, Equiv.trans_apply, Equiv.apply_symm_apply, Equiv.subtypeEquiv_apply,
      Equiv.finsetCongr_apply, Wrapped.stateEquiv_val]
  have h1 := Wrapped.mem_E F (Equiv.refl _) (autState hπ x).1 (autPerm hπ i)
  have h2 := Wrapped.mem_E F (Equiv.refl _) x.1 i
  rw [← Wrapped.stateEquiv_val, key, Finset.mem_map_equiv] at h1
  simp only [Equiv.refl_apply, Equiv.symm_apply_apply] at h1 h2
  rw [Bool.eq_iff_iff, ← h1, ← h2]

theorem autState_k (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}) (i : Fin F.A) :
    F.k (autState hπ x).1 (autPerm hπ i) = F.k x.1 i := by
  obtain ⟨-, hlt, -, hnb⟩ := autOK_spec hπ
  unfold Face.k
  rw [autPerm_val, ← (hnb i i.2).1.countP_eq, List.countP_map]
  refine List.countP_congr (fun j hj => ?_)
  have hjA : j < F.A := (Face.nb_lt' F i j hj)
  have := autState_bit hπ x ⟨j, hjA⟩
  rw [autPerm_val] at this
  show ((autState hπ x).1 : ℕ).testBit (π.getD j 0) = true ↔ _
  rw [this]

theorem autState_a {ρ1 ρ2 : ℚ} (x : {x : Fin (2 ^ F.A) // x ≠ F.empty}) (i : Fin F.A) :
    aR F ρ1 ρ2 (autState hπ x).1 (autPerm hπ i) = aR F ρ1 ρ2 x.1 i := by
  obtain ⟨-, -, -, hnb⟩ := autOK_spec hπ
  simp only [aR]
  rw [autState_k hπ x i, autState_bit hπ x i, autPerm_val, (hnb i i.2).2.1, (hnb i i.2).2.2]

theorem autState_Q {ρ1 ρ2 : ℚ} (hd : Dens ρ1 ρ2) (x y : {x : Fin (2 ^ F.A) // x ≠ F.empty}) :
    (chain F hd).Q (autState hπ x) (autState hπ y) = (chain F hd).Q x y := by
  rw [chain_Q, chain_Q, P_cast, P_cast]
  unfold bitP
  rw [Finset.prod_range, Finset.prod_range, ← Equiv.prod_comp (autPerm hπ)]
  refine prod_congr rfl (fun i _ => ?_)
  rw [autState_bit hπ y i, autState_a hπ x i]

/-- **Equal prices along an automorphism of the tables.** -/
theorem price_aut {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hc : CellsOK F)
    {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ} {lam : ℝ} (hμ : (chain F hs.dens).IsQSD μ lam) (hlam : 0 < lam)
    (huniq : ∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) (i : Fin F.A) :
    (localDeath F hs hc).price μ (autPerm hπ i) = (localDeath F hs hc).price μ i := by
  refine KilledChain.price_invariant (localDeath F hs hc) hμ hlam (fun ν lam' h h' => (huniq ν lam' h h').1)
    (autState hπ) (fun x y => autState_Q hπ hs.dens x y) (autPerm hπ) (fun j x => ?_) i
  rw [localDeath_dc, localDeath_dc, a_cast, a_cast, autState_a hπ x j]

end Aut

/-- **Every hull face at (0.44, 0.42) under `Lemma0F (hull R)`**: every clause of `hull_full_all`, and the prices
are equal along every automorphism of the tables (`autOK`; the triangle's rotation and reflection are checked to be
ones in `LinkHullCert.lean`). -/
theorem hull_full_sym (R : ℕ) (hA : 0 < (Gump.Dice.hull R).A) (h0 : Lemma0F (Gump.Dice.hull R)) :
    ∃ μ lam, (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsDominantQSD μ lam ∧
      IsQSD (Gump.Dice.hull R) ρ1 ρ2 (extend (Gump.Dice.hull R) μ) lam ∧ 0 < lam ∧ (∀ x, 0 < μ x) ∧
      (∀ ν lam', (chain (Gump.Dice.hull R) Hull3.sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) ∧
      (∀ i x, (LH R Hull3.sdens).dc i x = 1 - (((Gump.Dice.hull R).a ρ1 ρ2 x i : ℚ) : ℝ)) ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) = ∑ i, (LH R Hull3.sdens).price μ i ∧
      Real.log ((chain (Gump.Dice.hull R) Hull3.sdens.dens).lifetime μ) < 2.2165 * (Gump.Dice.hull R).A ∧
      (∃ m M : ℝ, 0 < m ∧ m ≤ M ∧
        (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).CanSurvive x →
          m / M * lam ^ t ≤ (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x) ∧
        (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom (t + 1) x ≤ M / m * lam ^ t)) ∧
      (∀ t x, (chain (Gump.Dice.hull R) Hull3.sdens.dens).survFrom t x =
        (((Gump.Dice.hull R).survival ρ1 ρ2 t x : ℚ) : ℝ)) ∧
      (∀ (π : List ℕ) (hπ : autOK (Gump.Dice.hull R) π = true) (i : Fin (Gump.Dice.hull R).A),
        (LH R Hull3.sdens).price μ (autPerm hπ i) = (LH R Hull3.sdens).price μ i) := by
  obtain ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, hb, hdec, hsurv⟩ := hull_full_all R hA h0
  exact ⟨μ, lam, hD, hdice, hlam, hpos, huniq, hdc, hpr, hb, hdec, hsurv,
    fun π hπ i => price_aut hπ Hull3.sdens (cellsOK_hull R) hD.qsd hlam huniq i⟩

end Gump.Link
