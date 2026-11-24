/-
ref-dice: try to make the dice certificate checkers accept a wrong certificate (hull 3, copies of the data only;
nothing under research/blast/lean/ is changed). Each `#eval` prints the Bool the kernel would have to reduce to
`true`; the last block runs the kernel itself (`decide +kernel`) on two perturbed checks, which must FAIL to elaborate
(the errors are expected and are the result).

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-dice/Perturb.lean
-/
import GumpMath.DiceHull3
set_option maxRecDepth 100000

namespace RefDice
open Gump Gump.Dice Gump.Dice.Hull3Data

/-- Replace the entry at index y of a tree of depth n by f(entry). -/
def setAt : Tree → ℕ → ℕ → (ℕ → ℕ) → Tree
  | .leaf a, 0, _, f => .leaf (f a)
  | .node l r, n + 1, y, f => if y.testBit n then .node l (setAt r n y f) else .node (setAt l n y f) r
  | t, _, _, _ => t

def A9 : ℕ := (hull 3).A
def up (L M : ℕ) (V : Tree) : Bool := Data.allRows (data.rowUp A9 (data.Dt A9) L M V) (2 ^ A9)
def lo (L M : ℕ) (V : Tree) : Bool := Data.allRows (data.rowLo A9 (data.Dt A9) L M V) (2 ^ A9)
/-- the first failing row of the upper check, if any -/
def firstBadUp (L M : ℕ) (V : Tree) : Option ℕ :=
  (List.range (2 ^ A9)).find? fun x => !(data.rowUp A9 (data.Dt A9) L M V x)

-- 0. the certificate as committed: true, true, true, true
#eval (data.tabOK (hull 3), up Lup Mup Vup, lo Llo Mlo Vlo, Data.vecOK Vup A9 vmin vmax)
-- 1. eigenvalue's last digit: lambda_up lowered by 2e-22 (below lambda = 0.91656736559489013735890..): must be false
#eval up (Lup - 2) Mup Vup
#eval firstBadUp (Lup - 2) Mup Vup
-- 1b. lambda_lo raised by 2e-22 (above lambda): must be false
#eval lo (Llo + 2) Mlo Vlo
-- 2. one entry of v lowered by one part in 10^6 (beyond the certificate's slack, ~1e-23): must be false at that row
#eval up Lup Mup (setAt Vup 9 300 fun a => a - a / 1000000)
#eval firstBadUp Lup Mup (setAt Vup 9 300 fun a => a - a / 1000000)
-- 2b. one entry of v raised by one part in 10^6: the rows that lead to state 300 must fail
#eval firstBadUp Lup Mup (setAt Vup 9 300 fun a => a + a / 1000000)
-- 2c. one entry of v changed by 1 unit (relative 1e-60, far inside the slack): STILL A VALID certificate, accepted
#eval (up Lup Mup (setAt Vup 9 300 fun a => a + 1), up Lup Mup (setAt Vup 9 300 fun a => a - 1))
-- 2d. the empty-state entry made non-zero: vecOK must be false
#eval Data.vecOK (setAt Vup 9 0 fun _ => 1) A9 vmin vmax
-- 3. a table row: one alive numerator of cell 1 changed by 1; one neighbour list permuted; one coin count changed
def dataT : Data := ⟨11, 25, 21, 50, G, C, T.set 1 ((T.getD 1 []).set 3 (12518 + 1))⟩
def dataG : Data := ⟨11, 25, 21, 50, G.set 0 [1, 4, 4], C, T⟩
def dataC : Data := ⟨11, 25, 21, 50, G, C.set 0 (2, 1), T⟩
#eval (dataT.tabOK (hull 3), dataG.tabOK (hull 3), dataC.tabOK (hull 3))
-- 3b. with the wrong numerator the upper check itself would still pass or fail? (it is the tabOK that must stop it)
#eval Data.allRows (dataT.rowUp A9 (dataT.Dt A9) Lup Mup Vup) (2 ^ A9)

-- 4. the kernel on two perturbed checks: both must FAIL (errors below are the expected result)
theorem bad_tab : dataT.tabOK (hull 3) = true := by decide +kernel
theorem bad_lam : ((Lup : ℚ) / Mup) ≤ 0.9165673655948901373 := by norm_num [Lup, Mup]

end RefDice
