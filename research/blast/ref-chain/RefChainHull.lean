/-
ref-chain, fourth review: `Lemma0F`, `autOK` and `hull R` (LinkHull.lean, LinkFaceAut.lean).

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/RefChainHull.lean

1. `hull R` has no cells for even R and 3, 9, 18 cells for R = 1, 3, 5: `hA : 0 < (hull R).A` holds exactly for odd R
   (checked here for R ≤ 6), so `hull_theorems R hA` is vacuous for even R and says nothing there.
2. `Lemma0F` is false on a face whose QSD with λ > 0 is not unique (`two_not_lemma0`): two cells of one layer
   too far apart to be neighbours, three coins each; each cell alone is a closed class with λ = ρ1²ρ2.
3. `autOK` rejects a permutation that keeps the neighbour lists but not the coins (`aut_rejects_coins`, on a
   two-cell face whose second cell has no coins), and one that keeps the coins but not the neighbours
   (`aut_rejects_nbrs`, two corners of hull 3 swapped alone); the identity passes.
-/
import GumpMath.LinkFaceAut
import GumpMath.DiceMean

open Gump Gump.Dice Gump.Link

namespace RefChainHull

example : (Gump.Dice.hull 0).A = 0 ∧ (Gump.Dice.hull 1).A = 3 ∧ (Gump.Dice.hull 2).A = 0 ∧
    (Gump.Dice.hull 3).A = 9 ∧ (Gump.Dice.hull 4).A = 0 ∧ (Gump.Dice.hull 5).A = 18 ∧
    (Gump.Dice.hull 6).A = 0 := by decide +kernel

/-- Two cells of the layer x + y + z = 1, far apart, every coin present. -/
def twoCells : Face where
  cells := [⟨1, 0, 0⟩, ⟨21, -10, -10⟩]
  diag := d111
  red := id
  coin := fun _ => true

theorem two_A : twoCells.A = 2 := rfl

theorem two_facts : twoCells.nb 0 = [] ∧ twoCells.nb 1 = [] ∧ twoCells.m1 0 = 2 ∧ twoCells.m2 0 = 1 ∧
    twoCells.m1 1 = 2 ∧ twoCells.m2 1 = 1 := by decide +kernel

theorem two_step1 : ∀ y < 4, y ≠ 0 → stepF twoCells 1 y = true → y = 1 := by decide +kernel

theorem two_not_lemma0 : ¬ Lemma0F twoCells := by
  rintro ⟨u, hu, hu0, hall, hreach⟩
  have h1 := hreach 1 (by rw [two_A]; norm_num) one_ne_zero ⟨0, by rw [two_A]; norm_num, by decide +kernel⟩
  have inv : ∀ y, Relation.ReflTransGen (StepN twoCells) 1 y → y = 1 := by
    intro y h
    induction h with
    | refl => rfl
    | tail _ hst ih =>
      subst ih
      obtain ⟨hy, hy0, hs⟩ := hst
      rw [two_A] at hy
      exact two_step1 _ hy hy0 hs
  have hu1 := inv u h1
  subst hu1
  have := hall 1 (by rw [two_A]; norm_num)
  revert this
  decide +kernel

/-- The same two cells, the second with no coins beneath (coin only for points with x < 10). -/
def twoCellsNoCoin : Face where
  cells := [⟨1, 0, 0⟩, ⟨21, -10, -10⟩]
  diag := d111
  red := id
  coin := fun q => decide (q.x < 10)

theorem aut_coins_differ : twoCellsNoCoin.m1 1 = 0 ∧ twoCellsNoCoin.m1 0 = 2 ∧ twoCellsNoCoin.nb 0 = [] ∧
    twoCellsNoCoin.nb 1 = [] := by decide +kernel

theorem aut_rejects_coins : autOK twoCellsNoCoin [1, 0] = false := by decide +kernel
theorem aut_identity : autOK twoCellsNoCoin [0, 1] = true := by decide +kernel
theorem aut_rejects_nbrs : autOK (Gump.Dice.hull 3) [3, 1, 2, 0, 4, 5, 6, 7, 8] = false := by decide +kernel

end RefChainHull

#print axioms RefChainHull.two_not_lemma0
#print axioms RefChainHull.aut_rejects_coins
#print axioms RefChainHull.aut_rejects_nbrs
#print axioms Gump.Link.cellsOK_hull
#print axioms Gump.Link.hull_theorems
#print axioms Gump.Link.hull_theorems_at
#print axioms Gump.Link.hull_full_all
#print axioms Gump.Link.hull_full_sym
#print axioms Gump.Link.price_aut
#print axioms Gump.Link.lemma0_of_cert
#print axioms Gump.Link.face_full_of
#print axioms Gump.Dice.qsd_survival
#print axioms Gump.Dice.qsd_mean
#print axioms Gump.Dice.qsd_mean_all
#print axioms Gump.Dice.hull3_mean
#print axioms Gump.Dice.qsd_mean_hull
