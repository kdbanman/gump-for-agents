/-
ref-dice: axiom sweep over every constant declared in the `GumpMath/Dice*.lean` modules at commit 6f70d2d (second review; not
only the names in `AxiomsDice.lean`). For each constant: its kind and the axioms `Lean.collectAxioms` finds (what
`#print axioms` prints). Reports declared axioms, opaques, unsafe/partial definitions, `implemented_by`/`extern`,
and any constant whose axioms go beyond propext, Classical.choice, Quot.sound. Then `#check`s every name of
`AxiomsDice.lean` and `statements_dice.json`.

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-dice/DiceAxiomSweep2.lean
-/
import Lean
import GumpMath.DiceDef
import GumpMath.DiceCert
import GumpMath.DiceLife
import GumpMath.DiceReal
import GumpMath.DiceBound
import GumpMath.DiceBound2
import GumpMath.DiceExit
import GumpMath.DiceSym
import GumpMath.DiceHull3Data
import GumpMath.DiceHull3
import GumpMath.DiceHull3ExitData
import GumpMath.DiceHull3Exit
import GumpMath.DiceTorus103Data
import GumpMath.DiceTorus103
import GumpMath.DiceTorus113Data
import GumpMath.DiceTorus113
import GumpMath.DiceTorus113ExitData
import GumpMath.DiceTorus113Exit
import GumpMath.DiceStrip13Data
import GumpMath.DiceStrip13
import GumpMath.DicePatch13Data
import GumpMath.DicePatch13
import GumpMath.DiceFlux
import GumpMath.DiceHull
import GumpMath.DiceBound3
import GumpMath.DiceHullAll
import GumpMath.DiceRegular
import GumpMath.DiceTorusReg

open Lean Elab Command

def diceSweep : CommandElabM Unit := do
  let env ← getEnv
  let mods := env.header.moduleNames
  let std : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut nThm : Nat := 0
  let mut nDef : Nat := 0
  let mut nOther : Nat := 0
  let mut bad : Array String := #[]
  let mut seen : Std.HashMap String Nat := {}
  let mut perMod : Std.HashMap String Nat := {}
  let mut names : Array String := #[]
  for (n, ci) in env.constants.map₁.toList do
    let some idx := env.getModuleIdxFor? n | continue
    let m := mods[idx.toNat]!
    unless (m.toString.startsWith "GumpMath.Dice") do continue
    names := names.push s!"{n} {m}"
    perMod := perMod.insert m.toString (perMod.getD m.toString (0 : Nat) + 1)
    match ci with
    | .thmInfo _ => nThm := nThm + 1
    | .defnInfo d =>
        nDef := nDef + 1
        if d.safety != .safe then bad := bad.push s!"UNSAFE/PARTIAL DEF: {n} in {m}"
    | .axiomInfo _ => bad := bad.push s!"AXIOM DECLARED: {n} in {m}"
    | .opaqueInfo _ => bad := bad.push s!"OPAQUE: {n} in {m}"
    | _ => nOther := nOther + 1
    if (Compiler.getImplementedBy? env n).isSome then bad := bad.push s!"IMPLEMENTED_BY: {n}"
    if isExtern env n then bad := bad.push s!"EXTERN: {n}"
    let axs ← liftCoreM <| Lean.collectAxioms n
    let key := toString (axs.qsort Name.lt |>.toList)
    seen := seen.insert key (seen.getD key (0 : Nat) + 1)
    for a in axs do
      unless std.contains a do
        bad := bad.push s!"{n} ({m}) depends on {a}"
  logInfo m!"Dice modules: {perMod.toList}"
  logInfo m!"{nThm} theorems, {nDef} definitions, {nOther} other constants; axiom sets seen: {seen.toList}"
  for b in bad do logInfo m!"{b}"
  IO.FS.writeFile "/home/user/gump-for-agents/research/blast/ref-dice/dice_names2.txt" (String.intercalate "\n" (names.qsort (· < ·)).toList ++ "\n")
  logInfo m!"{bad.size} findings (declared axioms, opaques, unsafe, implemented_by, extern, nonstandard axioms)"

#eval diceSweep

open Gump.Dice
-- every name of AxiomsDice.lean and statements_dice.json
#check @hull3_lifetime
#check @hull3_tau
#check @torus103_lifetime
#check @torus103_tau
#check @torus113_lifetime
#check @torus113_tau
#check @strip13_lifetime
#check @strip13_tau
#check @patch13_lifetime
#check @patch13_tau
#check @survival_le_all
#check @qsd_le_all
#check @lntau_le_all
#check @survival_le_regular
#check @lntau_le_regular
#check @regular_torus202
#check @hull3_bust
#check @torus113_bust
#check @Data.lifetime_of_cert
#check @Data.survival_up_sure
#check @Data.qsd_bounds
#check @Data.qsd_lo_sure
#check @Data.poisson_bound
#check @Data.rows_le
#check @Tree.eval_eq
#check @Data.rows_of_reps
#check @Data.P_sym
#check @flux_share
#check @death_flux
#check @hull3_bust_flux
#check @torus113_bust_flux
#check @survival_le_hull
#check @lntau_le_hull
#check @qsd_le_balanced
#check @lntau_le_hull_small
#check @Face.hull_balanced
#check @Face.hull_type
#check @lntau_le_hull_all
#check @regular_torus303
#check @lntau_le_torus303
#check @Face.torus_regular
#check @Face.torus_count_symm
#check @lntau_le_torus
