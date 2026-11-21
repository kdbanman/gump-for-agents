/-
An executable stepper for finite patterns, built on `step` itself: the next generation of a finite
set of live cells is found by evaluating `Gump.step` (the function the theorems are about) at every
live cell and every neighbour of a live cell.

Used by `Check.lean` to compare this development's rule with `reference/oracle.py` state for state.
-/
import Gump.Basic
import Std.Data.HashSet

namespace Gump

abbrev Pattern := Std.HashSet Pt

/-- The configuration of a finite pattern. -/
def Pattern.config (live : Pattern) : Config := fun p => live.contains p

/-- One generation of a finite pattern. Only live cells and their neighbours are looked at: a dead
point with no live neighbour stays dead. -/
def stepFin (live : Pattern) : Pattern :=
  let cand : Pattern := live.fold (fun acc p => (nbrs p).foldl (fun a q => a.insert q) (acc.insert p)) {}
  cand.fold (fun acc p => if step live.config p then acc.insert p else acc) {}

end Gump
