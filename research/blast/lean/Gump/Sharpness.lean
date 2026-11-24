/-
Two sharpness remarks of `docs/AUTOMATON.md` section 3, as theorems:
  T2: "Axis-aligned half-spaces do not confine (a cell just outside can have 4 neighbours inside)."
  T3: "Two dead layers are not enough (1 + 2 from one side plus 1 from the other = 4)."
Each is the negation of the would-be theorem, with an explicit four-cell witness.
-/
import Gump.Sealed

namespace Gump

/-- **Axis-aligned half-spaces do not confine.** The analogue of T2 for the half-space x > 0 is false:
the X cell (1, 0, 0) has four neighbours in the plane x = 0, and is born when they are alive. -/
theorem axis_halfspace_not_confining :
    ¬ ∀ c : Config, (∀ p : Pt, 0 < p.x → c p = false) → ∀ p : Pt, 0 < p.x → step c p = false := by
  intro h
  have := h (fun q => decide (q ∈ [⟨0, 1, 0⟩, ⟨0, -1, 0⟩, ⟨0, 0, 1⟩, ⟨0, 0, -1⟩])) (by
    intro p hp
    simp only [decide_eq_false_iff_not, List.mem_cons, List.not_mem_nil, or_false]
    rintro (rfl | rfl | rfl | rfl) <;> simp at hp) ⟨1, 0, 0⟩ (by decide)
  revert this
  decide

/-- **Two dead layers are not a firewall.** The analogue of T3 for two consecutive layers (here s = 1
and s = 3 along the diagonal (1, 1, 1)) is false: the cell (1, 0, 0) in layer 1 has one live neighbour
in layer -3, two in layer -1 and one in layer 5, and is born. -/
theorem two_layers_not_firewall :
    ¬ ∀ c : Config, (∀ p : Pt, -1 < (⟨true, true, true⟩ : Diag).dot p → (⟨true, true, true⟩ : Diag).dot p ≤ 3 →
        c p = false) →
      ∀ p : Pt, -1 < (⟨true, true, true⟩ : Diag).dot p → (⟨true, true, true⟩ : Diag).dot p ≤ 3 →
        step c p = false := by
  intro h
  have := h (fun q => decide (q ∈ [⟨1, -2, -2⟩, ⟨0, -1, 0⟩, ⟨0, 0, -1⟩, ⟨1, 2, 2⟩])) (by
    intro p h1 h2
    simp only [decide_eq_false_iff_not, List.mem_cons, List.not_mem_nil, or_false]
    rintro (rfl | rfl | rfl | rfl) <;> simp [Diag.dot, sg] at h1 h2) ⟨1, 0, 0⟩ (by decide) (by decide)
  revert this
  decide

end Gump
