/-
ref-tape, check 4 (hygiene), third review (the modules up to 40520c7: also ClockLit, ClockLitData,
ClockLitFirst, ClockLitOdd, ClockReader, CallReader, CallReaderData, LineBeam, LineBeamData, LineDivider, LineDividerData): the axioms of EVERY constant declared in the tape modules (and of every constant of
their `Gump` dependencies), not only those listed in AxiomsTape.lean; constants declared as `axiom` or `opaque`;
and whether each name of AxiomsTape.lean and statements_tape.json resolves.

  cd <built copy>/research/blast/lean && lake env lean <path>/RtAxioms.lean
-/
import Lean
import Gump.Tape
import Gump.Line
import Gump.TapeSignals
import Gump.Clock
import Gump.Call
import Gump.UnzipProof
import Gump.CallProof
import Gump.CallUnionLocal
import Gump.ClockLitOdd
import Gump.ClockReader
import Gump.CallReader
import Gump.LineBeam
import Gump.LineDivider

open Lean Elab Command

def tapeMods : List Name := [`Gump.TapeBase, `Gump.Tape, `Gump.TapeSignalsData, `Gump.TapeSignals, `Gump.LineData,
  `Gump.Line, `Gump.ClockData, `Gump.Clock, `Gump.Unzip, `Gump.UnzipProof, `Gump.CallData, `Gump.Call,
  `Gump.CallProof, `Gump.CallBox, `Gump.CallLine, `Gump.CallUnion, `Gump.CallUnionData, `Gump.CallUnionLocal,
  `Gump.ClockLit, `Gump.ClockLitData, `Gump.ClockLitFirst, `Gump.ClockLitOdd, `Gump.ClockReader, `Gump.CallReader,
  `Gump.CallReaderData, `Gump.LineBeam, `Gump.LineBeamData, `Gump.LineDivider, `Gump.LineDividerData]

def audit : CommandElabM Unit := do
  let env ← getEnv
  let mods := env.header.moduleNames
  let std : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut nTape : Nat := 0
  let mut nDep : Nat := 0
  let mut bad : Array String := #[]
  let mut seen : Std.HashMap String Nat := {}
  let mut perMod : Std.HashMap Name Nat := {}
  for (n, ci) in env.constants.map₁.toList do
    let some idx := env.getModuleIdxFor? n | continue
    let m := mods[idx.toNat]!
    unless m.getRoot == `Gump do continue
    if tapeMods.contains m then
      nTape := nTape + 1
      perMod := perMod.insert m (perMod.getD m 0 + 1)
    else nDep := nDep + 1
    match ci with
    | .axiomInfo _ => bad := bad.push s!"AXIOM DECLARED: {n} in {m}"
    | .opaqueInfo _ => bad := bad.push s!"OPAQUE: {n} in {m}"
    | _ => pure ()
    let axs ← liftCoreM <| Lean.collectAxioms n
    if tapeMods.contains m then
      let key := toString (axs.qsort Name.lt |>.toList)
      seen := seen.insert key (seen.getD key (0 : Nat) + 1)
    for a in axs do
      unless std.contains a do
        bad := bad.push s!"{n} ({m}) depends on {a}"
  logInfo m!"tape modules: {nTape} constants ({perMod.toList}); their Gump dependencies: {nDep} constants; axiom sets seen in the tape modules: {seen.toList}"
  for b in bad do logInfo m!"{b}"
  logInfo m!"{bad.size} constants (tape modules and their dependencies) with an axiom beyond propext, Classical.choice, Quot.sound, or declared axiom/opaque"

#eval audit

/-- every name of statements_tape.json's rows, resolved by its last component among the tape modules' constants -/
def rowNames : List String := ["tape_run", "tape_local_run", "line_orbit", "line_period_four", "S_succ", "train_step",
  "signal_run", "glue_run", "orbit_classify", "clock_every_length", "clock_cycle", "lit_clock_small",
  "unzip_law_sharp", "unzip_law", "stretch_stands", "glue_run_moving", "call_law_b",
  -- named in the brief and in notes/tape.md
  "train_shift", "surg_step", "chartA", "chartB", "hex_local", "pieceCheck_spec", "forcedCheck_spec",
  "lineC_N_period_four", "CallLaw", "UnzipLawSharp", "UnzipLaw", "LineRest",
  -- second review
  "call_law", "call_law_a", "V_HV", "Lf_HL", "V_Lf_disjoint", "step_or", "zone_cover", "LC_spec", "local_union",
  "bstep_spec", "line_rest", "Lf_period", "Lf_snap", "clockOf_period", "X0_lit", "clockY_zero_lit",
  -- third review
  "lit_word", "lit_enters", "FL_entry", "lit_odd_entry", "lit_enters_at", "lit_first", "lit_clock_exact", "lit_clock",
  "lit_enters_exact", "reader_run", "reader_step", "reader9_run", "reader_run_gen", "beam_period", "divider_period"]

#eval show CommandElabM Unit from do
  let env ← getEnv
  let mods := env.header.moduleNames
  for s in rowNames do
    let mut hits : Array String := #[]
    for (n, _) in env.constants.map₁.toList do
      let some idx := env.getModuleIdxFor? n | continue
      let m := mods[idx.toNat]!
      unless m.getRoot == `Gump do continue
      if n.getString! == s && !n.isInternal then hits := hits.push s!"{n} ({m})"
    logInfo m!"name {s}: {hits.size} constant(s) {hits.toList}"
