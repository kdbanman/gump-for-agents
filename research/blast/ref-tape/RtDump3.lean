/-
ref-tape, third review: the objects of the third task, evaluated to explicit cell sets.

  cd <built tree>/research/blast/lean && lake env lean <this file> > dump3.txt

- `litList.N` (N = 13 .. 30) and `clockOf.N` (N = 21 .. 30, through `Xb_frame`, as RtDump2.lean);
- `readerC` (Gump.Clock) and `readerCall` (Gump.Reader) of a test word, on a box of units;
- `beamList.N` (N = 1 .. 12; `beam_eq`: beam N = lcfg (beamList N)) and `divList.N` (N = 3 .. 20).
-/
import Gump.ClockLitOdd
import Gump.ClockReader
import Gump.CallReader
import Gump.LineBeam
import Gump.LineDivider

open Gump Gump.Tape Gump.Bits

def fmt (L : List Pt) : String := " ".intercalate (L.map fun p => s!"{p.x},{p.y},{p.z}")
def emit (name : String) (L : List Pt) : IO Unit := IO.println s!"{name}|{fmt L}"
def ints (a b : Int) : List Int := (List.range (b - a + 1).toNat).map fun (i : Nat) => a + (i : Int)

def boxPts (a b : Int) : List Pt :=
  (ints (2 * a) (2 * b + 1)).flatMap fun x => (ints (-8) 8).flatMap fun y => (ints (-24) 24).map fun s => ⟨x, y, s - x⟩

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

/-- a test word: C on units ≡ 0 mod 3 and on unit 1, B elsewhere -/
def wTest (u : Int) : Letter := if u % 3 = 0 ∨ u = 1 then .C else .B

def main : IO Unit := do
  for N in (List.range 18).map (· + 13) do
    emit s!"litList.{N}" (Gump.Clock.litList N)
  for N in ((List.range 10).map (· + 21) : List Nat) do
    let j : Nat := N - 6
    let b : Int := (N : Int) + 5
    emit s!"clockOf.{N}" ((boxPts (-6) b).filter (clockYB j))
  emit "readerC" ((boxPts (-8) 12).filter (Gump.Clock.readerC wTest))
  emit "readerCall" ((boxPts (-4) 16).filter (Gump.Reader.readerCall wTest))
  for N in (List.range 12).map (· + 1) do
    emit s!"beamList.{N}" (Gump.Beam.beamList N)
  for N in (List.range 18).map (· + 3) do
    emit s!"divList.{N}" (Gump.Divider.divList N)

#eval main
