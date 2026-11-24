/-
Referee's axiom audit (research/blast/ref-lean/REVIEW.md, section 3): every theorem of every module under the root
`Gump` (or `GumpMath`, when run in the Mathlib package), not only those listed in Axioms.lean, with the axioms its
proof rests on (`Lean.collectAxioms`, which is what `#print axioms` prints). Prints one summary line and every
theorem whose axioms are not within propext, Classical.choice, Quot.sound.

  cd <a built copy of research/blast/lean> && lake env lean <path>/AllAxioms.lean
  cd <a built copy of research/blast/lean/mathlib> && lake env lean -DgumpRoot=GumpMath <path>/AllAxioms.lean
  (the second form is emulated by AllAxiomsMath.lean, which imports GumpMath instead)
-/
import Lean
import Gump

open Lean Elab Command

def auditRoot (root : Name) : CommandElabM Unit := do
  let env ← getEnv
  let mods := env.header.moduleNames
  let std : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut nThm : Nat := 0
  let mut nDef : Nat := 0
  let mut nOther : Nat := 0
  let mut bad : Array String := #[]
  let mut seen : Std.HashMap String Nat := {}
  for (n, ci) in env.constants.map₁.toList do
    let some idx := env.getModuleIdxFor? n | continue
    let m := mods[idx.toNat]!
    unless m.getRoot == root do continue
    match ci with
    | .thmInfo _ => nThm := nThm + 1
    | .defnInfo _ => nDef := nDef + 1
    | .axiomInfo _ => bad := bad.push s!"AXIOM DECLARED: {n} in {m}"
    | .opaqueInfo _ => bad := bad.push s!"OPAQUE: {n} in {m}"
    | _ => nOther := nOther + 1
    let axs ← liftCoreM <| Lean.collectAxioms n
    let key := toString (axs.qsort Name.lt |>.toList)
    seen := seen.insert key (seen.getD key (0 : Nat) + 1)
    for a in axs do
      unless std.contains a do
        bad := bad.push s!"{n} ({m}) depends on {a}"
  logInfo m!"root {root}: {nThm} theorems, {nDef} definitions, {nOther} other constants audited; axiom sets seen: {seen.toList}"
  for b in bad do logInfo m!"{b}"
  logInfo m!"root {root}: {bad.size} constants with an axiom beyond propext, Classical.choice, Quot.sound"

#eval auditRoot `Gump

/-! Negative controls: the audit's tool sees `sorry` and `native_decide` (these two declarations are local to this
file, not part of the library). -/
theorem refereeCtlSorry : (1 : Nat) = 2 := sorry
theorem refereeCtlNative : (2 : Nat) + 2 = 4 := by native_decide
#eval show CommandElabM Unit from do
  let a ← liftCoreM <| Lean.collectAxioms ``refereeCtlSorry
  let b ← liftCoreM <| Lean.collectAxioms ``refereeCtlNative
  logInfo m!"controls: sorry -> {a.toList}; native_decide -> {b.toList}"
