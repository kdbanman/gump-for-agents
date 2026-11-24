/-
**The call law** (`research/audit/REVIEW-signals-9.md` section 3, base facts `research/audit/signals9/proof9.py`;
push 9, `research/signals/push9/`). Stated here on the whole lattice, with the infinite store wire. Part (b) is proved
in `Gump/CallProof.lean` (`call_law_b`); part (a) is not (`notes/tape.md`: the line spans 65 doubled units in x and
in y, more than the bit box of `Gump.Bits`, so its run is not yet kernel-checked).

The store wire is wire B with the stretch d^k f on the units c + 1 .. c + k + 1, c = 35 the crossing unit; the call
line (`Gump.Call.line`, 162 cells, at rest at an even generation) lies across unit c; at generation 0 the two cells
of the CALL are made live. Lf is the orbit of the line with the CALL alone; V_k is the orbit of the store wire alone
in which the one cell e1 = (1,2,0) of unit c is made live at generation 29.

`CallLaw`: for every k ≥ 1, (a) at every generation the state is the disjoint union of V_k and Lf; (b) at every even
t ≥ 2k + 34, V_k(t) is plain wire B carrying exactly k units of wire C (`b`), at the units c + 3 − (t − 28)/2 + 2j,
j = 0 .. k − 1. `LineRest`: the free line is at rest (its even state is `line`) from generation 42.
-/
import Gump.Unzip
import Gump.CallData

namespace Gump.Call
open Gump Gump.Tape Gump.Unzip

/-- The store wire of push 9: wire B with the stretch d^k f on the units c + 1 .. c + k + 1. -/
def storeAt (k : Nat) : Config := hcfg (fun u => storeWord k (u - (cross + 1)))

/-- The line at rest with the two cells of the CALL. -/
def lineCall : Config := fun p => lcfg line p || lcfg callCells p

/-- The whole object at generation 0: the store wire, the line across it and the CALL. -/
def callStart (k : Nat) : Config := fun p => storeAt k p || lineCall p

/-- Lf: the line with the CALL, alone. -/
def Lf (t : Nat) : Config := run lineCall t

/-- e1, the cell (1,2,0) of the crossing unit. -/
def e1 : Pt := shiftPt cross ⟨1, 2, 0⟩

/-- V_k: the store wire alone, with e1 made live at generation 29. -/
def V (k t : Nat) : Config :=
  if t < 29 then run (storeAt k) t else run (fun p => run (storeAt k) 29 p || p == e1) (t - 29)

/-- **The call law** (REVIEW-signals-9 §3, (a) and (b)). -/
def CallLaw : Prop :=
  ∀ k : Nat, 1 ≤ k →
    (∀ t : Nat, run (callStart k) t = (fun p => V k t p || Lf t p) ∧ ∀ p, ¬ (V k t p = true ∧ Lf t p = true)) ∧
    (∀ n : Nat, k + 17 ≤ n → V k (2 * n) = tape (pulses k (cross + 3 - ((n : Int) - 14))))

/-- The free line is at rest from generation 42 (part B of `proof9.py`). -/
def LineRest : Prop := ∀ n : Nat, 21 ≤ n → Lf (2 * n) = lcfg line

/-- The pulses of (b) lie where the source says: unit c + 3 − (t − 28)/2 + 2j holds a `b` exactly for j < k. -/
theorem pulses_at (k n : Nat) (j : Int) (h0 : 0 ≤ j) :
    pulses k (cross + 3 - ((n : Int) - 14)) (cross + 3 - ((n : Int) - 14) + 2 * j) = .C ↔ j < k := by
  simp only [pulses]
  constructor
  · intro h
    by_cases hc : cross + 3 - ((n : Int) - 14) ≤ cross + 3 - ((n : Int) - 14) + 2 * j ∧
        cross + 3 - ((n : Int) - 14) + 2 * j < cross + 3 - ((n : Int) - 14) + 2 * k ∧
        (cross + 3 - ((n : Int) - 14) + 2 * j - (cross + 3 - ((n : Int) - 14))) % 2 = 0
    · omega
    · rw [if_neg hc] at h; exact absurd h (by decide)
  · intro h
    rw [if_pos (by omega)]

end Gump.Call
