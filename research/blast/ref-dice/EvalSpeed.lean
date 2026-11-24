import GumpMath.DiceDef
open Gump Gump.Dice Finset
set_option maxRecDepth 100000
def entry (F : Face) (r1 r2 : ℚ) (x y : ℕ) : ℚ :=
  if h : x < 2 ^ F.A then if h2 : y < 2 ^ F.A then F.P r1 r2 ⟨x, h⟩ ⟨y, h2⟩ else 0 else 0
#eval (hull 3).cells
#eval (hull 3).A
#eval (List.range 512).map (fun y => entry (hull 3) ρ1 ρ2 511 y) |>.length
#eval ((List.range 512).map (fun y => entry (hull 3) ρ1 ρ2 5 y)).take 3
