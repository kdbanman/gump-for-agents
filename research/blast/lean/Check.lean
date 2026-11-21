/-
gumpcheck: this development's rule against the oracle and the 2012 logs.

  gumpcheck states FILE         FILE holds successive generations written by oracle_states.py
                                ("G g n" then n lines "x y z"); generation 0 is the seed. Each later
                                generation must equal stepFin of the one before it, as a set.
  gumpcheck cube LO HI GENS     populations of the legacy closed-cube seed (every cell with all three
                                doubled coordinates in [LO, HI]) for GENS generations, in the format
                                of the 2012 logs ("0 0", then "g population").
-/
import Gump.Finite
open Gump

def parsePt (s : String) : Option Pt :=
  match (s.splitOn " ").filter (· ≠ "") with
  | [a, b, c] => do
    let x ← a.toInt?
    let y ← b.toInt?
    let z ← c.toInt?
    pure ⟨x, y, z⟩
  | _ => none

def sameSet (a b : Pattern) : Bool := a.size == b.size && a.all (fun p => b.contains p)

def checkStates (file : String) : IO UInt32 := do
  let lines ← IO.FS.lines file
  let mut gens : Array Pattern := #[]
  let mut cur : Pattern := {}
  let mut started := false
  for l in lines do
    if l.startsWith "G" then
      if started then gens := gens.push cur
      cur := {}
      started := true
    else
      match parsePt l with
      | some p => cur := cur.insert p
      | none => pure ()
  if started then gens := gens.push cur
  let mut bad := 0
  for i in [1:gens.size] do
    let mine := stepFin gens[i-1]!
    if !(sameSet mine gens[i]!) then
      bad := bad + 1
      IO.println s!"MISMATCH at generation {i}: oracle {gens[i]!.size} cells, Lean {mine.size} cells"
  IO.println s!"{file}: {gens.size - 1} generations compared with the oracle state for state, {bad} mismatches (seed {gens[0]!.size} cells, last {gens[gens.size-1]!.size} cells)"
  return (if bad == 0 then 0 else 1)

def cubeSeed (lo hi : Int) : Pattern := Id.run do
  let n := (hi - lo + 1).toNat
  let mut s : Pattern := {}
  for i in [0:n] do
    for j in [0:n] do
      for k in [0:n] do
        let p : Pt := ⟨lo + i, lo + j, lo + k⟩
        if p.isCell then s := s.insert p
  return s

def cubePops (lo hi : Int) (gens : Nat) : IO UInt32 := do
  let mut s := cubeSeed lo hi
  IO.println "0 0"
  for g in [1:gens+1] do
    s := stepFin s
    IO.println s!"{g} {s.size}"
  return 0

def main (args : List String) : IO UInt32 :=
  match args with
  | ["states", file] => checkStates file
  | ["cube", lo, hi, gens] =>
    match lo.toInt?, hi.toInt?, gens.toNat? with
    | some lo, some hi, some g => cubePops lo hi g
    | _, _, _ => do IO.eprintln "cube LO HI GENS"; return 2
  | _ => do IO.eprintln "usage: gumpcheck states FILE | gumpcheck cube LO HI GENS"; return 2
