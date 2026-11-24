/-
ref-chain (fifth review): axiom sweep over every constant declared in the `GumpMath/Chain*.lean` (16) and
`GumpMath/Link*.lean` (17) modules.  For each constant: its kind, and the axioms `Lean.collectAxioms` finds
(what `#print axioms` prints).  Reports declared axioms, opaques, `implemented_by`/`extern` attributes, and any
constant whose axioms go beyond propext, Classical.choice, Quot.sound.

  cd research/blast/lean/mathlib && lake env lean /home/user/gump-for-agents/research/blast/ref-chain/Link5AxiomSweep.lean
-/
import Lean
import GumpMath.ChainTilt
import GumpMath.ChainPerron
import GumpMath.ChainExist
import GumpMath.ChainLemma0
import GumpMath.ChainCoins
import GumpMath.ChainRoutes
import GumpMath.ChainSeam
import GumpMath.ChainSSM
import GumpMath.ChainPrice
import GumpMath.ChainInst
import GumpMath.ChainTiltLimit
import GumpMath.ChainBits
import GumpMath.ChainKagome
import GumpMath.ChainTorus
import GumpMath.ChainRate
import GumpMath.ChainSharp
import GumpMath.LinkFaces
import GumpMath.LinkTorus202
import GumpMath.LinkNoCert
import GumpMath.LinkSurv
import GumpMath.LinkWrappedArea
import GumpMath.LinkWrappedFull
import GumpMath.LinkFaceAut
import GumpMath.DiceMean
import GumpMath.LinkHullSym

open Lean Elab Command

def chainSweep : CommandElabM Unit := do
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
    unless (m.toString.startsWith "GumpMath.Chain" || m.toString.startsWith "GumpMath.Link" || m.toString == "GumpMath.DiceMean") do continue
    names := names.push s!"{n}"
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
  logInfo m!"Chain modules: {perMod.toList}"
  logInfo m!"{nThm} theorems, {nDef} definitions, {nOther} other constants; axiom sets seen: {seen.toList}"
  for b in bad do logInfo m!"{b}"
  IO.FS.writeFile "/home/user/gump-for-agents/research/blast/ref-chain/link5_names.txt" (String.intercalate "\n" (names.qsort (· < ·)).toList ++ "\n")
  logInfo m!"{bad.size} findings (declared axioms, opaques, unsafe, implemented_by, extern, nonstandard axioms)"

#eval chainSweep
