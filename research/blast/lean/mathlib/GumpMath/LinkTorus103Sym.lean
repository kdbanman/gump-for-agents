/-
Equal prices within the symmetry classes of the face `(torus 1 0 3)` (12 table automorphisms, found by the chain agent's
generator; each one used is checked by the kernel, `Data.symOK`, `decide +kernel`).  Classes of cells:
[[0, 1, 3, 4, 6, 7], [2, 5, 8]].
-/
import GumpMath.LinkTorus103
import GumpMath.LinkSym

set_option maxRecDepth 100000

namespace Gump.Link.Torus103
open Gump.Dice Gump.Chain Gump.Chain.KilledChain Gump.Link

/-- The class of each cell. -/
def cls : List ℕ := [0, 0, 1, 0, 0, 1, 0, 0, 1]
def σ0 : List ℕ := [1, 0, 2, 4, 3, 5, 7, 6, 8]
theorem sym0 : Torus103Data.data.symOK (torus 1 0 3).A σ0 (Tree.build (torus 1 0 3).A (act σ0) 0) = true := by decide +kernel
def σ1 : List ℕ := [3, 4, 5, 6, 7, 8, 0, 1, 2]
theorem sym1 : Torus103Data.data.symOK (torus 1 0 3).A σ1 (Tree.build (torus 1 0 3).A (act σ1) 0) = true := by decide +kernel
def σ2 : List ℕ := [4, 3, 5, 7, 6, 8, 1, 0, 2]
theorem sym2 : Torus103Data.data.symOK (torus 1 0 3).A σ2 (Tree.build (torus 1 0 3).A (act σ2) 0) = true := by decide +kernel
def σ3 : List ℕ := [0, 1, 5, 6, 7, 2, 3, 4, 8]
theorem sym3 : Torus103Data.data.symOK (torus 1 0 3).A σ3 (Tree.build (torus 1 0 3).A (act σ3) 0) = true := by decide +kernel
def σ4 : List ℕ := [6, 7, 2, 3, 4, 8, 0, 1, 5]
theorem sym4 : Torus103Data.data.symOK (torus 1 0 3).A σ4 (Tree.build (torus 1 0 3).A (act σ4) 0) = true := by decide +kernel
def σ5 : List ℕ := [7, 6, 2, 4, 3, 8, 1, 0, 5]
theorem sym5 : Torus103Data.data.symOK (torus 1 0 3).A σ5 (Tree.build (torus 1 0 3).A (act σ5) 0) = true := by decide +kernel
def σ6 : List ℕ := [3, 4, 8, 0, 1, 5, 6, 7, 2]
theorem sym6 : Torus103Data.data.symOK (torus 1 0 3).A σ6 (Tree.build (torus 1 0 3).A (act σ6) 0) = true := by decide +kernel
theorem hA9 : (torus 1 0 3).A = 9 := by decide +kernel

section
variable {μ : {x : Fin (2 ^ (torus 1 0 3).A) // x ≠ (torus 1 0 3).empty} → ℝ} {lam : ℝ}
  (hμ : (chain (torus 1 0 3) sdens.dens).IsQSD μ lam) (hlam : 0 < lam)
  (huniq : ∀ ν lam', (chain (torus 1 0 3) sdens.dens).IsQSD ν lam' → 0 < lam' → ν = μ ∧ lam' = lam)
include hμ hlam huniq
theorem price0 (h0 : 0 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨0, h0⟩ = L.price μ ⟨0, h0r⟩ := rfl
theorem price1 (h1 : 1 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨1, h1⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym0 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym0 ⟨0, h0r⟩ = ⟨1, h1⟩ := Fin.ext (show σ0.getD 0 0 = 1 by decide)
  rw [e] at this; exact this
theorem price2 (h2 : 2 < (torus 1 0 3).A) (h2r : 2 < (torus 1 0 3).A) : L.price μ ⟨2, h2⟩ = L.price μ ⟨2, h2r⟩ := rfl
theorem price3 (h3 : 3 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨3, h3⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym1 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym1 ⟨0, h0r⟩ = ⟨3, h3⟩ := Fin.ext (show σ1.getD 0 0 = 3 by decide)
  rw [e] at this; exact this
theorem price4 (h4 : 4 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨4, h4⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym2 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym2 ⟨0, h0r⟩ = ⟨4, h4⟩ := Fin.ext (show σ2.getD 0 0 = 4 by decide)
  rw [e] at this; exact this
theorem price5 (h5 : 5 < (torus 1 0 3).A) (h2r : 2 < (torus 1 0 3).A) : L.price μ ⟨5, h5⟩ = L.price μ ⟨2, h2r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym3 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨2, h2r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym3 ⟨2, h2r⟩ = ⟨5, h5⟩ := Fin.ext (show σ3.getD 2 0 = 5 by decide)
  rw [e] at this; exact this
theorem price6 (h6 : 6 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨6, h6⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym4 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym4 ⟨0, h0r⟩ = ⟨6, h6⟩ := Fin.ext (show σ4.getD 0 0 = 6 by decide)
  rw [e] at this; exact this
theorem price7 (h7 : 7 < (torus 1 0 3).A) (h0r : 0 < (torus 1 0 3).A) : L.price μ ⟨7, h7⟩ = L.price μ ⟨0, h0r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym5 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨0, h0r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym5 ⟨0, h0r⟩ = ⟨7, h7⟩ := Fin.ext (show σ5.getD 0 0 = 7 by decide)
  rw [e] at this; exact this
theorem price8 (h8 : 8 < (torus 1 0 3).A) (h2r : 2 < (torus 1 0 3).A) : L.price μ ⟨8, h8⟩ = L.price μ ⟨2, h2r⟩ := by
  have := price_sym (torus 1 0 3) Torus103Data.data Torus103Data.tab sym6 sdens Torus103Data.hρ1 Torus103Data.hρ2 (cellsOK_of_tab (torus 1 0 3) Torus103Data.data Torus103Data.tab cells) hμ hlam huniq ⟨2, h2r⟩
  have e : cellPerm (torus 1 0 3) Torus103Data.data sym6 ⟨2, h2r⟩ = ⟨8, h8⟩ := Fin.ext (show σ6.getD 2 0 = 8 by decide)
  rw [e] at this; exact this

/-- The representative of each class. -/
def rep : List ℕ := [0, 0, 2, 0, 0, 2, 0, 0, 2]

theorem price_rep (i : Fin (torus 1 0 3).A) :
    ∃ h : rep.getD i 0 < (torus 1 0 3).A, L.price μ i = L.price μ ⟨rep.getD i 0, h⟩ := by
  rcases i with ⟨i, hi⟩
  have hi2 : i < 9 := lt_of_lt_of_eq hi hA9
  interval_cases i
  · exact ⟨lt_of_lt_of_eq (show rep.getD 0 0 < 9 by decide) hA9.symm, price0 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 1 0 < 9 by decide) hA9.symm, price1 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 2 0 < 9 by decide) hA9.symm, price2 hμ hlam huniq hi (lt_of_lt_of_eq (show 2 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 3 0 < 9 by decide) hA9.symm, price3 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 4 0 < 9 by decide) hA9.symm, price4 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 5 0 < 9 by decide) hA9.symm, price5 hμ hlam huniq hi (lt_of_lt_of_eq (show 2 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 6 0 < 9 by decide) hA9.symm, price6 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 7 0 < 9 by decide) hA9.symm, price7 hμ hlam huniq hi (lt_of_lt_of_eq (show 0 < 9 by decide) hA9.symm)⟩
  · exact ⟨lt_of_lt_of_eq (show rep.getD 8 0 < 9 by decide) hA9.symm, price8 hμ hlam huniq hi (lt_of_lt_of_eq (show 2 < 9 by decide) hA9.symm)⟩

/-- **Equal prices within each symmetry class**: c_i = c_j whenever i and j are in the same class. -/
theorem torus103_prices (i j : Fin (torus 1 0 3).A) (hij : cls.getD i 0 = cls.getD j 0) : L.price μ i = L.price μ j := by
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
end Gump.Link.Torus103
