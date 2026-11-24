/-
torus check: `Gump.Torus.tstep` (the oracle's array-index torus, proved equal to `Gump.step` on the periodic
configuration by `Gump.Torus.lift_tstep`) against reference/oracle.py, entry by entry.

  lake env lean --run TorusCheck.lean FILE H

FILE holds successive oracle generations on the H×H×H torus ("G g n", then n lines "i j k", array indices).
Every entry of every generation after the first must equal `tstep H` of the generation before.
Run by difftest.py; not part of the library (the lakefile is not this agent's to edit, so it is interpreted).
-/
import Gump.Torus
open Gump Gump.Torus

def parse3 (s : String) : Option (Nat × Nat × Nat) :=
  match (s.splitOn " ").filter (· ≠ "") with
  | [a, b, c] => do pure (← a.toNat?, ← b.toNat?, ← c.toNat?)
  | _ => none

def main (args : List String) : IO UInt32 := do
  match args with
  | [file, hs] =>
    let H := hs.toNat!
    let N := H * H * H
    let lines ← IO.FS.lines file
    let mut gens : Array (Array Bool) := #[]
    let mut cur : Array Bool := Array.replicate N false
    let mut started := false
    for l in lines do
      if l.startsWith "G" then
        if started then gens := gens.push cur
        cur := Array.replicate N false
        started := true
      else
        match parse3 l with
        | some (x, y, z) => cur := cur.set! (x + H * (y + H * z)) true
        | none => pure ()
    if started then gens := gens.push cur
    let mut bad := 0
    for g in [1:gens.size] do
      let a := gens[g-1]!
      let b := gens[g]!
      let h : TState := fun i j k => a[i + H * (j + H * k)]!
      let mut diff := 0
      for idx in [0:N] do
        if tstep H h (idx % H) (idx / H % H) (idx / (H * H)) != b[idx]! then diff := diff + 1
      if diff > 0 then
        bad := bad + 1
        IO.println s!"MISMATCH at generation {g}: {diff} entries"
    IO.println s!"{file}: {gens.size - 1} generations of the torus H={H} compared with the oracle entry by entry, {bad} mismatches"
    return (if bad == 0 then 0 else 1)
  | _ => do IO.eprintln "usage: lake env lean --run TorusCheck.lean FILE H"; return 2
