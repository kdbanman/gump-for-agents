/-
Equal prices within a symmetry class, for `Face.P`: a permutation σ of the cells that preserves the dice
agent's tables (`Data.symOK`, checked by the kernel; `DiceSym.lean`'s `P_sym`, `alpha_sym`, `act_bij`) preserves
the killed chain and every cell's own death factor, so with the quasi-stationary law unique among λ > 0
(`face_lifetime`) the chain arm's `price_invariant` gives c_{σ i} = c_i (`price_sym`).
-/
import Mathlib
import GumpMath.LinkUnique
import GumpMath.DiceSym

set_option linter.unusedSectionVars false

namespace Gump.Link
open Finset Gump.Chain Gump.Chain.KilledChain Gump.Dice

section Sym
variable (F : Face) (c : Data) {σ : List ℕ} {I : Tree}

/-- The action on states, as a map of `Fin (2 ^ A)`. -/
def actF (hsym : c.symOK F.A σ I = true) : Fin (2 ^ F.A) → Fin (2 ^ F.A) :=
  fun y => ⟨I.get F.A y, ((c.symOK_spec hsym).2.2.2.2 y y.isLt).1⟩

theorem actF_zero_iff (hsym : c.symOK F.A σ I = true) (y : Fin (2 ^ F.A)) :
    ((actF F c hsym y : Fin (2 ^ F.A)) : ℕ) = 0 ↔ (y : ℕ) = 0 := by
  obtain ⟨-, -, -, -, hI⟩ := c.symOK_spec hsym
  have hlt := (c.symOK_spec hsym).2.2.1
  have bitsHigh : ∀ (z : ℕ), z < 2 ^ F.A → ∀ j, F.A ≤ j → z.testBit j = false := fun z hz j hj =>
    Nat.testBit_lt_two_pow (lt_of_lt_of_le hz (Nat.pow_le_pow_right (by norm_num) hj))
  constructor
  · intro h
    apply Nat.eq_of_testBit_eq
    intro j
    by_cases hj : j < F.A
    · rw [← (hI y y.isLt).2 j hj]
      show (I.get F.A y).testBit _ = _
      have : I.get F.A y = 0 := h
      rw [this, Nat.zero_testBit, Nat.zero_testBit]
    · rw [bitsHigh y y.isLt j (by omega), Nat.zero_testBit]
  · intro h
    show I.get F.A y = 0
    apply Nat.eq_of_testBit_eq
    intro j
    by_cases hj : j < F.A
    · obtain ⟨i, hi, rfl⟩ := c.sym_surj hsym j hj
      rw [(hI y y.isLt).2 i hi, h, Nat.zero_testBit, Nat.zero_testBit]
    · rw [bitsHigh _ ((hI y y.isLt).1) j (by omega), Nat.zero_testBit]

/-- The action on the living states. -/
noncomputable def actL (htab : c.tabOK F = true) (hsym : c.symOK F.A σ I = true) :
    {x : Fin (2 ^ F.A) // x ≠ F.empty} ≃ {x : Fin (2 ^ F.A) // x ≠ F.empty} :=
  Equiv.subtypeEquiv (Equiv.ofBijective (actF F c hsym) (by unfold actF; exact c.act_bij F htab hsym))
    (fun x => by
      show x ≠ F.empty ↔ actF F c hsym x ≠ F.empty
      rw [ne_eq, ne_eq, empty_iff, empty_iff, actF_zero_iff F c hsym])

/-- The permutation of the cells. -/
noncomputable def cellPerm (hsym : c.symOK F.A σ I = true) : Fin F.A ≃ Fin F.A :=
  Equiv.ofBijective (fun i => ⟨σ.getD i 0, (c.symOK_spec hsym).2.2.1 i i.2⟩)
    ((Finite.injective_iff_bijective).mp (fun i j e => Fin.ext
      (c.sym_inj hsym i i.2 j j.2 (by simpa using congrArg Fin.val e))))

/-- **Equal prices along a symmetry of the tables.** -/
theorem price_sym (htab : c.tabOK F = true) (hsym : c.symOK F.A σ I = true) {ρ1 ρ2 : ℚ} (hs : SDens ρ1 ρ2) (hρ1 : ρ1 = (c.n1 : ℚ) / c.d1)
    (hρ2 : ρ2 = (c.n2 : ℚ) / c.d2) (hc : CellsOK F) {μ : {x : Fin (2 ^ F.A) // x ≠ F.empty} → ℝ} {lam : ℝ}
    (hμ : (chain F hs.dens).IsQSD μ lam) (hlam : 0 < lam)
    (huniq : ∀ ν lam', (chain F hs.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam) (i : Fin F.A) :
    (localDeath F hs hc).price μ (cellPerm F c hsym i) = (localDeath F hs hc).price μ i := by
  obtain ⟨-, -, hlt, -, hI⟩ := c.symOK_spec hsym
  refine KilledChain.price_invariant (localDeath F hs hc) hμ hlam (fun ν lam' h h' => (huniq ν lam' h h').1)
    (actL F c htab hsym) (fun x y => ?_) (cellPerm F c hsym) (fun j x => ?_) i
  · show ((F.P ρ1 ρ2 (actF F c hsym x) (actF F c hsym y) : ℚ) : ℝ) = ((F.P ρ1 ρ2 x y : ℚ) : ℝ)
    congr 1
    subst hρ1 hρ2
    exact c.P_sym F htab hsym x y _ _
  · show 1 - ((F.a ρ1 ρ2 (actF F c hsym x) (σ.getD j 0) : ℚ) : ℝ) = 1 - ((F.a ρ1 ρ2 x j : ℚ) : ℝ)
    congr 2
    subst hρ1 hρ2
    obtain ⟨ha, hd⟩ := c.alpha_sym F htab hsym x x.1.isLt j j.2
    rw [c.a_eq F htab _ _ (hlt j j.2), c.a_eq F htab _ _ j.2]
    show (c.alpha (I.get F.A x) (σ.getD j 0) : ℚ) / c.den (σ.getD j 0) = _
    rw [ha, hd]

end Sym
end Gump.Link
