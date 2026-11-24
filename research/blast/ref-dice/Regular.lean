/-
ref-dice: Lean's own `Face.regular` conjuncts, evaluated on faces beyond the three the kernel checked, and the
hypothesis `∀ q, F.coin q = true` of `lntau_le_all` on the hull (false: a point outside the octahedron has no coin).
  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-dice/Regular.lean
-/
import GumpMath.DiceBound2
open Gump Gump.Dice Finset

def regB (F : Face) : Bool :=
  decide ((∀ i < F.A, (F.nb i).length = 6) ∧ (∀ i < F.A, ∀ j ∈ F.nb i, j < F.A) ∧
    (∀ j < F.A, ∑ i ∈ range F.A, (F.nb i).count j = 6))

#eval [regB (torus 1 0 3), regB (torus 1 1 3), regB (torus 2 0 2), regB (torus 1 0 4), regB (torus 1 1 4),
  regB (torus 2 1 3), regB (torus 3 0 3), regB (torus 1 2 5), regB (torus 3 2 4)]
#eval [regB (strip 1 3), regB (strip 2 2), regB (patch 1 3), regB (patch 2 2), regB (hull 3), regB (hull 5)]
#eval ((hull 3).coin ⟨5, 0, 0⟩, (hull 3).coin ⟨0, 0, 1⟩, (torus 1 1 3).coin ⟨5, 0, 0⟩)
#eval (List.range (hull 3).A).map fun i => ((hull 3).m1 i, (hull 3).m2 i)
