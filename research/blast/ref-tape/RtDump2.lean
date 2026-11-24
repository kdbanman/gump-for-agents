/-
ref-tape, second review: the objects of the call law and of `clockOf`, evaluated to explicit cell sets.

  cd <built tree>/research/blast/lean && lake env lean <this file> > dump2.txt

Lines `name|x,y,z ...`.
- `callStart.k`: the Lean `callStart k` at every cell with x in [16, 93], y in [-48, 24], x + z in [-56, 16]
  (units 8 .. 46 of the store wire, the whole line and the CALL).
- `Lf.t` (t = 0 .. 46): the Lean `Lf t`, read through the kernel-proved identity `Lf_frame`
  (Lf n q = Box.bcfg (Box.brun LS n) (q + lineFrame), n ≤ 46) at every cell of the 128 x 128 x 16 box's core.
- `clockOf.N` (N = 1 .. 20): `clockOf N`, for N ≤ 5 through `run_bcfg_of_core` on Gump.Bits (the lit list moved by
  `frame`, run N - 2 generations), for N ≥ 6 through `Xb_frame` as in RtDump.lean; on the box of units -6 .. N + 5.
-/
import Gump.Clock
import Gump.CallUnionLocal

open Gump Gump.Tape Gump.Bits

def fmt (L : List Pt) : String := " ".intercalate (L.map fun p => s!"{p.x},{p.y},{p.z}")
def emit (name : String) (L : List Pt) : IO Unit := IO.println s!"{name}|{fmt L}"
def ints (a b : Int) : List Int := (List.range (b - a + 1).toNat).map fun (i : Nat) => a + (i : Int)

def boxPts (a b : Int) : List Pt :=
  (ints (2 * a) (2 * b + 1)).flatMap fun x => (ints (-8) 8).flatMap fun y => (ints (-24) 24).map fun s => ⟨x, y, s - x⟩

def callPts : List Pt :=
  ((ints 16 93).flatMap fun x => (ints (-48) 24).flatMap fun y => (ints (-56) 16).map fun s => (⟨x, y, s - x⟩ : Pt)).filter
    (·.isCell)

def corePts : List Pt :=
  ((ints (-12) 107).flatMap fun x => (ints (-12) 107).flatMap fun y => (ints (-12) (-5)).map fun z => (⟨x, y, z⟩ : Pt)).filter
    (·.isCell)

def baseStates : Array Nat := Id.run do
  let mut S := Gump.Clock.bS
  let mut out : Array Nat := #[]
  for _ in [0:26] do
    out := out.push S
    S := bstep S
  return out

def XbB (s : Int) (q : Pt) : Bool := bcfg (baseStates[((s + 7) % 26).toNat]!) (q + Gump.Clock.frame)

def clockYB (j : Nat) (p : Pt) : Bool :=
  let i := Gump.Clock.cidx 3 j p
  XbB (Gump.Clock.chart j i 5) (shiftPt (-i) p)

def litB (N : Nat) : Config :=
  let S := brun (ofList ((Gump.Clock.litList N).map (· + Gump.Clock.frame))) (N - 2)
  fun q => bcfg S (q + Gump.Clock.frame)

def main : IO Unit := do
  for k in [1, 3] do
    emit s!"callStart.{k}" (callPts.filter (Gump.Call.callStart k))
  let neg : Pt := ⟨-(Gump.Call.lineFrame.x), -(Gump.Call.lineFrame.y), -(Gump.Call.lineFrame.z)⟩
  let mut S := Gump.Call.LS
  for t in [0:47] do
    emit s!"Lf.{t}" ((corePts.filter fun p => Gump.Call.Box.bcfg S p).map (· + neg))
    S := Gump.Call.Box.bstep S
  for N in (List.range 20).map (· + 1) do
    let c : Config := if N ≤ 5 then litB N else clockYB (N - 6)
    emit s!"clockOf.{N}" ((boxPts (-6) (N + 5)).filter c)
  emit "zoneZ" Gump.Call.zoneZ

#eval main
