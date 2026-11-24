/-
ref-dice, second review: Lean's own definitions evaluated on faces the dice arm did not check.
(1) `Face.pathE` / `dies` / `bustLast` on the 3-cell faces `hull 1` and `torus 1 1 1`, 4 generations, every start,
    compared with an exact path enumeration in Python (review2_paths.py);
(2) `Face.nb` and the conjuncts of `Face.regular` on thin and skewed tori (neighbours coincide), compared with
    myface.py (nb_compare.py).
  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-dice/Review2.lean
-/
import GumpMath.DiceFlux
import GumpMath.DiceTorusReg
open Gump Gump.Dice Finset

def pathRow (name : String) (F : Face) (n K : ℕ) : IO Unit := do
  for x in List.range (2 ^ F.A) do
    if h : x < 2 ^ F.A then
      let d := F.pathE ρ1 ρ2 n (fun l => if F.dies l = true then 1 else 0) ⟨x, h⟩
      let b := F.pathE ρ1 ρ2 n (fun l => if (F.dies l && F.bustLast K l) = true then 1 else 0) ⟨x, h⟩
      IO.println s!"PATH {name} {n} {K} {x} {d} {b}"
#eval pathRow "hull1" (hull 1) 4 2
#eval pathRow "torus111" (torus 1 1 1) 4 2
#eval pathRow "hull1" (hull 1) 3 3

def regB (F : Face) : Bool :=
  decide ((∀ i < F.A, (F.nb i).length = 6) ∧ (∀ i < F.A, ∀ j ∈ F.nb i, j < F.A) ∧
    (∀ j < F.A, ∑ i ∈ range F.A, (F.nb i).count j = 6))
def ptS (p : Pt) : String := s!"{p.x},{p.y},{p.z}"
def dumpNb (name : String) (F : Face) : IO Unit := do
  IO.println s!"FACE {name} {F.A}"
  IO.println s!"CELLS {" ".intercalate (F.cells.map ptS)}"
  for i in List.range F.A do
    IO.println s!"NB {i} {F.nb i} {F.m1 i} {F.m2 i}"
  IO.println s!"REG {name} {regB F}"
#eval dumpNb "torus 1 1 1" (torus 1 1 1)
#eval dumpNb "torus 1 5 1" (torus 1 5 1)
#eval dumpNb "torus 2 1 1" (torus 2 1 1)
#eval dumpNb "torus 3 2 1" (torus 3 2 1)
#eval dumpNb "torus 1 3 2" (torus 1 3 2)
#eval dumpNb "torus 1 5 2" (torus 1 5 2)
#eval dumpNb "torus 2 3 2" (torus 2 3 2)
#eval dumpNb "torus 5 3 2" (torus 5 3 2)
#eval dumpNb "torus 1 7 3" (torus 1 7 3)
#eval dumpNb "torus 4 6 5" (torus 4 6 5)
