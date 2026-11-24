/-
ref-tape, check 3: trying to make the bit-level checkers accept something false at the edge of the box.

The cube still life (six faces of the cube with centre (-14, 0, 0)) has its face (-15, 0, 0) in the box of
`Gump.Bits` but outside the interior, where `bstep` never sets a bit. So `bstep` is wrong there: it kills that face,
while `Gump.step` keeps the cube (a still life). A false claim built on that wrong answer ("one generation removes
the face (-15,0,0)") is offered to `pieceCheck` (the checker behind `pieceCheck_spec`, the train, the signals, the
tape windows and the zones) and to `oscCert`; both must reject it, and do, because their `inCore` / `coreRun`
conjunct fails. The same pattern moved into the core is accepted as the still life it is.

  cd <built copy>/research/blast/lean && lake env lean <path>/RtCert.lean
-/
import Lean
import Gump.TapeSignals
import Gump.CallProof

open Gump Gump.Tape Gump.Bits

/-- the six faces of the cube with even centre q -/
def cubeAt (q : Pt) : List Pt :=
  [q + ⟨1, 0, 0⟩, q + ⟨-1, 0, 0⟩, q + ⟨0, 1, 0⟩, q + ⟨0, -1, 0⟩, q + ⟨0, 0, 1⟩, q + ⟨0, 0, -1⟩]

def edgeCube : List Pt := cubeAt ⟨-14, 0, 0⟩
def falseNext : List Pt := edgeCube.filter (· != ⟨-15, 0, 0⟩)

-- the unchecked bit stepper is wrong at the edge: it drops the face (-15,0,0) ...
example : bstep (ofList edgeCube) = ofList falseNext := by decide +kernel
-- ... while the cube is a still life of `Gump.step` (moved into the core, by the certificate)
example : oscCert (cubeAt ⟨2, 2, 2⟩) 1 = true := by decide +kernel
-- the false claim, as a piece check: no wire (f = g = empty), σ = the edge cube, σ' = the wrong successor,
-- one generation, units -8 .. -7 (where the cube lies), no translation: REJECTED
example : pieceCheck (fun _ => []) (fun _ => []) (-8) 3 edgeCube falseNext 1 (-8) (-7) ⟨0, 0, 0⟩ = false := by
  decide +kernel
-- the true claim at the edge is rejected too (the checker is conservative, not wrong)
example : pieceCheck (fun _ => []) (fun _ => []) (-8) 3 edgeCube edgeCube 1 (-8) (-7) ⟨0, 0, 0⟩ = false := by
  decide +kernel
-- and the same claims moved into the core: the true one accepted, the false one rejected
example : pieceCheck (fun _ => []) (fun _ => []) 0 3 (cubeAt ⟨2, 2, 2⟩) (cubeAt ⟨2, 2, 2⟩) 1 1 1 ⟨0, 0, 0⟩ = true := by
  decide +kernel
example : pieceCheck (fun _ => []) (fun _ => []) 0 3 (cubeAt ⟨2, 2, 2⟩)
    ((cubeAt ⟨2, 2, 2⟩).filter (· != ⟨3, 2, 2⟩)) 1 1 1 ⟨0, 0, 0⟩ = false := by
  decide +kernel
-- oscCert on the edge cube: rejected
example : oscCert edgeCube 1 = false := by decide +kernel
-- the forced-cell checker of the call law's start, on the edge: rejected
example : Gump.Call.forcedCheck (fun _ => []) (fun _ => []) (-8) 10 ⟨-15, 0, 0⟩ (-8) (-8) ⟨0, 0, 0⟩ = false := by
  decide +kernel

/-! Controls for the axiom audit of RtAxioms.lean: `collectAxioms` sees `sorry` and `native_decide`. -/
open Lean Elab Command in
theorem refTapeCtlSorry : (1 : Nat) = 2 := sorry
theorem refTapeCtlNative : (2 : Nat) + 2 = 4 := by native_decide
open Lean Elab Command in
#eval show CommandElabM Unit from do
  let a ← liftCoreM <| Lean.collectAxioms ``refTapeCtlSorry
  let b ← liftCoreM <| Lean.collectAxioms ``refTapeCtlNative
  logInfo m!"controls: sorry -> {a.toList}; native_decide -> {b.toList}"
