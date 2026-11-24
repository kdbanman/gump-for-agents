/-
ref-tape, second review: a false claim at the edges of the second bit box (`Gump/CallBox.lean`, the box
[-16, 112) x [-16, 112) x [-16, 0), interior [-14, 110)^2 x [-14, -2), core [-12, 108)^2 x [-12, -4)).

Three cube still lifes with faces in the box but outside the interior (the face z = -15; the faces z = -1 and the four
at z = -2; the faces x = 111 and the four at x = 110): the unchecked `Box.bstep` keeps only the interior faces, while
`Gump.step` keeps the cube. Every spec of the box needs `Box.inCore`,
which fails for each, so a "line check" built like `lineCheck` (`boxCoreRun` + `boxEqOn`) rejects the false successor;
the same cube in the core is stepped correctly.

  cd <built tree>/research/blast/lean && lake env lean <path>/RtCert2.lean
-/
import Gump.CallLine

open Gump Gump.Call

def cubeAt (q : Pt) : List Pt :=
  [q + ⟨1, 0, 0⟩, q + ⟨-1, 0, 0⟩, q + ⟨0, 1, 0⟩, q + ⟨0, -1, 0⟩, q + ⟨0, 0, 1⟩, q + ⟨0, 0, -1⟩]

def lowZ : List Pt := cubeAt ⟨2, 2, -14⟩      -- face (2, 2, -15): in the box, not in the interior
def highZ : List Pt := cubeAt ⟨2, 2, -2⟩      -- faces at z = -1 and -2 not in the interior
def highX : List Pt := cubeAt ⟨110, 2, -8⟩    -- faces at x = 111 and 110 not in the interior
example : (lowZ.filter Box.interior).length = 5 ∧ (highZ.filter Box.interior).length = 1 ∧
    (highX.filter Box.interior).length = 1 := by decide
def inside : List Pt := cubeAt ⟨50, 50, -8⟩

def drop (L : List Pt) (p : Pt) : List Pt := L.filter (· != p)

/-- a claim "S steps to T" in the style of `lineCheck`: S in the core for one step, and agreement on the list M -/
def claim (S T : Nat) (M : List Pt) : Bool := boxCoreRun S 1 && boxEqOn M (Box.bstep S) T

-- the unchecked stepper is wrong at three edges
example : Box.bstep (Box.ofList lowZ) = Box.ofList (lowZ.filter Box.interior) := by decide +kernel
example : Box.bstep (Box.ofList highZ) = Box.ofList (highZ.filter Box.interior) := by decide +kernel
example : Box.bstep (Box.ofList highX) = Box.ofList (highX.filter Box.interior) := by decide +kernel
-- none of the three is in the core, so no spec of the box applies to them
example : Box.inCore (Box.ofList lowZ) = false ∧ Box.inCore (Box.ofList highZ) = false ∧
    Box.inCore (Box.ofList highX) = false := by decide +kernel
-- the false successor is rejected
example : claim (Box.ofList lowZ) (Box.ofList (lowZ.filter Box.interior)) lowZ = false := by decide +kernel
example : claim (Box.ofList highZ) (Box.ofList (highZ.filter Box.interior)) highZ = false := by decide +kernel
example : claim (Box.ofList highX) (Box.ofList (highX.filter Box.interior)) highX = false := by decide +kernel
-- in the core: the still life is stepped correctly, the true claim accepted, a false one rejected
example : Box.bstep (Box.ofList inside) = Box.ofList inside := by decide +kernel
example : claim (Box.ofList inside) (Box.ofList inside) inside = true := by decide +kernel
example : claim (Box.ofList inside) (Box.ofList (drop inside ⟨51, 50, -8⟩)) inside = false := by decide +kernel
