/-
Equal prices within the symmetry classes of the face `(hull 3)` (12 table automorphisms, found by the chain agent's
generator; each one used is checked by the kernel, `Data.symOK`, `decide +kernel`).  Classes of cells:
[[0, 3, 8], [1, 2, 4, 5, 6, 7]].
-/
import GumpMath.LinkHull3
import GumpMath.LinkSym

set_option maxRecDepth 100000

namespace Gump.Link.Hull3
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The class of each cell. -/
def cls : List ℕ := [0, 1, 1, 0, 1, 1, 1, 1, 0]
def σ0 : List ℕ := [3, 2, 1, 0, 5, 4, 7, 6, 8]
theorem sym0 : Hull3Data.data.symOK (hull 3).A σ0 (Tree.build (hull 3).A (act σ0) 0) = true := by decide +kernel
def σ1 : List ℕ := [0, 4, 5, 3, 1, 2, 7, 6, 8]
theorem sym1 : Hull3Data.data.symOK (hull 3).A σ1 (Tree.build (hull 3).A (act σ1) 0) = true := by decide +kernel
def σ2 : List ℕ := [3, 5, 4, 0, 2, 1, 6, 7, 8]
theorem sym2 : Hull3Data.data.symOK (hull 3).A σ2 (Tree.build (hull 3).A (act σ2) 0) = true := by decide +kernel
def σ3 : List ℕ := [8, 6, 2, 3, 7, 5, 1, 4, 0]
theorem sym3 : Hull3Data.data.symOK (hull 3).A σ3 (Tree.build (hull 3).A (act σ3) 0) = true := by decide +kernel
def σ4 : List ℕ := [8, 7, 1, 0, 6, 4, 2, 5, 3]
theorem sym4 : Hull3Data.data.symOK (hull 3).A σ4 (Tree.build (hull 3).A (act σ4) 0) = true := by decide +kernel
theorem hA9 : (hull 3).A = 9 := by decide +kernel

section
variable {μ : {x : Fin (2 ^ (hull 3).A) // x ≠ (hull 3).empty} → ℝ} {lam : ℝ}
  (hμ : (chain (hull 3) sdens.dens).IsQSD μ lam) (hlam : 0 < lam)
  (huniq : ∀ ν lam', (chain (hull 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
include hμ hlam huniq
theorem price0 (h0 : 0 < (hull 3).A) (h0r : 0 < (hull 3).A) : L.price μ ⟨0, h0⟩ = L.price μ ⟨0, h0r⟩ := rfl
theorem price1 (h1 : 1 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨1, h1⟩ = L.price μ ⟨1, h1r⟩ := rfl
theorem price2 (h2 : 2 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨2, h2⟩ = L.price μ ⟨1, h1r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym0 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨1, h1r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym0 ⟨1, h1r⟩ = ⟨2, h2⟩ := Fin.ext (show σ0.getD 1 0 = 2 by decide)
  rw [e] at this; exact this
theorem price3 (h3 : 3 < (hull 3).A) (h0r : 0 < (hull 3).A) : L.price μ ⟨3, h3⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym0 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym0 ⟨0, h0r⟩ = ⟨3, h3⟩ := Fin.ext (show σ0.getD 0 0 = 3 by decide)
  rw [e] at this; exact this
theorem price4 (h4 : 4 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨4, h4⟩ = L.price μ ⟨1, h1r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym1 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨1, h1r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym1 ⟨1, h1r⟩ = ⟨4, h4⟩ := Fin.ext (show σ1.getD 1 0 = 4 by decide)
  rw [e] at this; exact this
theorem price5 (h5 : 5 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨5, h5⟩ = L.price μ ⟨1, h1r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym2 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨1, h1r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym2 ⟨1, h1r⟩ = ⟨5, h5⟩ := Fin.ext (show σ2.getD 1 0 = 5 by decide)
  rw [e] at this; exact this
theorem price6 (h6 : 6 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨6, h6⟩ = L.price μ ⟨1, h1r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym3 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨1, h1r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym3 ⟨1, h1r⟩ = ⟨6, h6⟩ := Fin.ext (show σ3.getD 1 0 = 6 by decide)
  rw [e] at this; exact this
theorem price7 (h7 : 7 < (hull 3).A) (h1r : 1 < (hull 3).A) : L.price μ ⟨7, h7⟩ = L.price μ ⟨1, h1r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym4 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨1, h1r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym4 ⟨1, h1r⟩ = ⟨7, h7⟩ := Fin.ext (show σ4.getD 1 0 = 7 by decide)
  rw [e] at this; exact this
theorem price8 (h8 : 8 < (hull 3).A) (h0r : 0 < (hull 3).A) : L.price μ ⟨8, h8⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (hull 3) Hull3Data.data Hull3Data.tab sym3 sdens Hull3Data.hρ1 Hull3Data.hρ2 (cellsOK_of_tab (hull 3) Hull3Data.data Hull3Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (hull 3) Hull3Data.data sym3 ⟨0, h0r⟩ = ⟨8, h8⟩ := Fin.ext (show σ3.getD 0 0 = 8 by decide)
  rw [e] at this; exact this

/-- The representative of each class. -/
def rep : List ℕ := [0, 1, 1, 0, 1, 1, 1, 1, 0]

theorem price_rep (i : Fin (hull 3).A) :
    ∃ h : rep.getD i 0 < (hull 3).A, L.price μ i = L.price μ ⟨rep.getD i 0, h⟩ := by
  rcases i with ⟨i, hi⟩
  have hi2 : i < 9 := lt_of_lt_of_eq hi hA9
  interval_cases i
  · exact ⟨lt_of_lt_of_eq (show rep.getD 0 0 < 9 by decide) hA9.symm, price0 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 1 0 < 9 by decide) hA9.symm, price1 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 2 0 < 9 by decide) hA9.symm, price2 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 3 0 < 9 by decide) hA9.symm, price3 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 4 0 < 9 by decide) hA9.symm, price4 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 5 0 < 9 by decide) hA9.symm, price5 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 6 0 < 9 by decide) hA9.symm, price6 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 7 0 < 9 by decide) hA9.symm, price7 hμ hlam huniq hi (lt_of_lt_of_eq (show 1 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 8 0 < 9 by decide) hA9.symm, price8 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩

/-- **Equal prices within each symmetry class**: c_i = c_j whenever i and j are in the same class. -/
theorem hull3_prices (i j : Fin (hull 3).A) (hij : cls.getD i 0 = cls.getD j 0) : L.price μ i = L.price μ j := by
  obtain ⟨hi, ei⟩ := price_rep hμ hlam huniq i
  obtain ⟨hj, ej⟩ := price_rep hμ hlam huniq j
  have hr : rep.getD i 0 = rep.getD j 0 := by
    have hi2 : (i : ℕ) < 9 := lt_of_lt_of_eq i.2 hA9
    have hj2 : (j : ℕ) < 9 := lt_of_lt_of_eq j.2 hA9
    generalize (i : ℕ) = a at hi2 hij ⊢
    generalize (j : ℕ) = b at hj2 hij ⊢
    revert hij
    interval_cases a <;> interval_cases b <;> decide
  rw [ei, ej]
  congr 1
  exact Fin.ext hr

end
end Gump.Link.Hull3
