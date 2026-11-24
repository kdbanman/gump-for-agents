/-
ref-tape: the Lean objects of the tape files, evaluated to explicit cell sets (`#eval`), for comparison with the
catalogue's objects built from the JSON files by `rt_objects.py` (`python3 rt_compare.py`).

Run against a built copy of the core package (never in research/blast/lean/ itself):
  cd <copy>/research/blast/lean && lake env lean <this file> > dump.txt

Each line is `name|x,y,z x,y,z ...` (the live points), or `name|value`.
Configurations of the whole lattice (`tape w`, `train t`, `store k`, `countRead k`, `storeAt k`, `clockY j`) are
evaluated at every point of a box: units a .. b (x in [2a, 2b+1]), y in [-8, 8], x + z in [-24, 24].
`clockY j` is evaluated through the kernel-proved identity `Xb_frame` (Xb s q = bcfg (brun bS ((s+7)%26).toNat)
(q + frame)), i.e. with Lean's own `chart`, `cidx` and the bit-parallel run of the base; the naive `run` would take
13^n calls.
-/
import Gump.Tape
import Gump.Line
import Gump.TapeSignals
import Gump.Clock
import Gump.Call
import Gump.UnzipProof
import Gump.CallProof

open Gump Gump.Tape Gump.Bits

def fmt (L : List Pt) : String := " ".intercalate (L.map fun p => s!"{p.x},{p.y},{p.z}")

def emit (name : String) (L : List Pt) : IO Unit := IO.println s!"{name}|{fmt L}"

def ints (a b : Int) : List Int := (List.range (b - a + 1).toNat).map fun (i : Nat) => a + (i : Int)

/-- every point of the box over units a .. b -/
def boxPts (a b : Int) : List Pt :=
  (ints (2 * a) (2 * b + 1)).flatMap fun x => (ints (-8) 8).flatMap fun y => (ints (-24) 24).map fun s => ⟨x, y, s - x⟩

def live (c : Config) (a b : Int) : List Pt := (boxPts a b).filter c

/-- a test word: C on units ≡ 0 mod 3 and on unit 1, B elsewhere -/
def wTest (u : Int) : Letter := if u % 3 = 0 ∨ u = 1 then .C else .B

/-- the base states of the clock, in the box -/
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

def main : IO Unit := do
  emit "cellsOf.B" (cellsOf .B)
  emit "cellsOf.C" (cellsOf .C)
  emit "tape.wTest.-6.8" (live (tape wTest) (-6) 8)
  for N in [2, 3, 4, 5, 7, 12, 20, 31] do
    emit s!"lineList.{N}" (Gump.Line.lineList N)
  for N in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] do
    emit s!"litList.{N}" (Gump.Clock.litList N)
  emit "X0" Gump.Clock.X0
  for j in [0, 1, 2, 3, 4, 5, 6] do
    emit s!"clockY.{j}" (live (clockYB j) (-6) (11 + j))
  for t in [0, 1, 2, 3] do
    for par in [0, 1] do
      emit s!"trainBase.{t}.{par}" (Gump.Tape.Signals.trainBase t par)
    emit s!"train.{t}.-4.5" (live (Gump.Tape.Signals.train t) (-4) 5)
  for K in [Gump.Tape.Signals.Kind.E, .U, .H, .K0, .K3, .N1, .N2, .N3, .N4] do
    IO.println s!"kind|{repr K}|{K.par}|{K.dir}|{fmt K.cells}"
  for k in [1, 2, 3, 5] do
    emit s!"store.{k}" (live (Gump.Unzip.store k) (-5) (k + 5))
    emit s!"countRead.{k}" (live (Gump.Unzip.countRead k) (-5) (k + 5))
    emit s!"pulsesTape.{k}.-3" (live (tape (Gump.Unzip.pulses k (-3))) (-6) (2 * k + 2))
  for h in List.range 16 do
    emit s!"hexCells.{h}" (Gump.Unzip.hexCells h)
  for k in [1, 2, 4] do
    emit s!"storeAt.{k}" (live (Gump.Call.storeAt k) 30 (40 + k))
  emit "callLine" Gump.Call.line
  emit "callCells" Gump.Call.callCells
  emit "e1" [Gump.Call.e1]
  IO.println s!"cross|{Gump.Call.cross}"

#eval main
