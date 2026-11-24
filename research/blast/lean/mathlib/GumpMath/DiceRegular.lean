/-
`Face.regular` (six neighbour slots per cell, each cell in six slots) checked by the kernel for the wrapped faces
of the README's tables beyond the three in `DiceBound2.lean` (added 2026-11-24, second task), so that
`lntau_le_regular` (ln τ < 1.9228 · A) applies to them. For every torus it is not proved (notes/dice.md).
-/
import GumpMath.DiceBound2

namespace Gump.Dice

theorem regular_torus104 : (torus 1 0 4).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus114 : (torus 1 1 4).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus105 : (torus 1 0 5).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus115 : (torus 1 1 5).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus106 : (torus 1 0 6).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus116 : (torus 1 1 6).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus203 : (torus 2 0 3).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel
theorem regular_torus303 : (torus 3 0 3).regular := by refine ⟨?_, ?_, ?_⟩ <;> decide +kernel

end Gump.Dice

namespace Gump.Dice

/-- ln τ < 1.9228 · A on the 27-cell wrapped face (3,0),(0,3), for every quasi-stationary law (an example of
`lntau_le_regular` with a kernel-checked `regular`). -/
theorem lntau_le_torus303 (μ : Fin (2 ^ (torus 3 0 3).A) → ℝ) (lam : ℝ) (hq : IsQSD (torus 3 0 3) ρ1 ρ2 μ lam) :
    -Real.log (1 - lam) < 1.9228 * (torus 3 0 3).A :=
  lntau_le_regular (torus 3 0 3) (fun _ => rfl) regular_torus303 μ lam hq (by decide)

end Gump.Dice
