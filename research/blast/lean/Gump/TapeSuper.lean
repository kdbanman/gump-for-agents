/-
**Superposition** (for `research/signals/README.md` section 31, the meetings). Two configurations whose live cells
are farther apart than their light cones reach in n generations evolve independently for n generations: the run of
their union is the union of their runs (`run_or_far`; max-norm distance more than 4n, since each cell's influence
spreads 2n). The same along a wire, relative to any background (`superpose_units`): if Y differs from a background X
only on the units < a and Z only on the units > b, and b − a ≥ 2n − 1, then for n generations the configuration that
is Y on the units ≤ m and Z beyond (for any seam a + n − 1 ≤ m ≤ b − n) runs as Y on the units ≤ m and as Z beyond.
Both are consequences of the light cone (`Gump.light_cone`, `run_eq_of_units`) alone.
-/
import Gump.Speed
import Gump.TapeBase

namespace Gump

theorem near_triangle {r s : Nat} {p q x : Pt} (h1 : Near r x p) (h2 : Near s x q) : Near (r + s) p q := by
  unfold Near at *; omega

/-- **Two configurations farther apart than 4n evolve independently for n generations.** -/
theorem run_or_far (c₁ c₂ : Config) (n : Nat)
    (h : ∀ p q, c₁ p = true → c₂ q = true → ¬ Near (4 * n) p q) :
    run (fun p => c₁ p || c₂ p) n = fun p => run c₁ n p || run c₂ n p := by
  funext x
  have hx : Near 0 x x := by simp [Near]
  by_cases hA : ∃ p, Near (2 * n) x p ∧ c₁ p = true
  · obtain ⟨p, hp, hc⟩ := hA
    have off : ∀ q, Near (2 * n) x q → c₂ q = false := by
      intro q hq
      cases e : c₂ q
      · rfl
      · exact absurd (by have := near_triangle hp hq; rwa [show 2 * n + 2 * n = 4 * n by omega] at this)
          (h p q hc e)
    rw [light_cone (c := fun p => c₁ p || c₂ p) (c' := c₁) n 0
      (fun q hq => by rw [off q (by simpa using hq), Bool.or_false]) x hx, dead_ball n off, Bool.or_false]
  · have off : ∀ q, Near (2 * n) x q → c₁ q = false := by
      intro q hq
      cases e : c₁ q
      · rfl
      · exact absurd ⟨q, hq, e⟩ hA
    rw [light_cone (c := fun p => c₁ p || c₂ p) (c' := c₂) n 0
      (fun q hq => by rw [off q (by simpa using hq), Bool.false_or]) x hx, dead_ball n off, Bool.false_or]

open Tape in
/-- **Superposition along a wire, on any background.** -/
theorem superpose_units (X Y Z : Config) (a b m : Int) (n : Nat)
    (hY : ∀ q, a ≤ unitOf q → Y q = X q) (hZ : ∀ q, unitOf q ≤ b → Z q = X q)
    (hm1 : a + n ≤ m + 1) (hm2 : m + n ≤ b) :
    run (glue m Y Z) n = glue m (run Y n) (run Z n) := by
  funext p
  simp only [glue]
  split
  · rename_i hp
    apply run_eq_of_units n
    intro q h1 h2
    simp only [glue]
    split
    · rfl
    · rw [hZ q (by omega), hY q (by omega)]
  · rename_i hp
    apply run_eq_of_units n
    intro q h1 h2
    simp only [glue]
    split
    · rw [hY q (by omega), hZ q (by omega)]
    · rfl

end Gump
