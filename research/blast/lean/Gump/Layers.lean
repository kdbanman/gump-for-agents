/-
Layers along a body diagonal, and T1 (the layer histogram) of `docs/AUTOMATON.md`.

A body diagonal d ∈ {±1}³ slices the lattice into layers s = d·p. T1: for every orientation of a
cell and every d, its twelve neighbours lie at Δs = -4, -2, 0, +2, +4 in numbers 1, 2, 6, 2, 1.
-/
import Gump.Basic

namespace Gump

/-- A body diagonal: three signs (`true` is +1). -/
structure Diag where
  sx : Bool
  sy : Bool
  sz : Bool
deriving DecidableEq, Repr

/-- ±n. -/
def sg (b : Bool) (n : Int) : Int := if b then n else -n

/-- The layer of a point along a diagonal: s = d·p. -/
def Diag.dot (d : Diag) (p : Pt) : Int := sg d.sx p.x + sg d.sy p.y + sg d.sz p.z

/-- The opposite diagonal. -/
def Diag.neg (d : Diag) : Diag := ⟨!d.sx, !d.sy, !d.sz⟩

theorem sg_add (b : Bool) (m n : Int) : sg b (m + n) = sg b m + sg b n := by
  cases b <;> simp [sg] <;> omega

theorem Diag.dot_add (d : Diag) (p q : Pt) : d.dot (p + q) = d.dot p + d.dot q := by
  simp only [Diag.dot, Pt.add_x, Pt.add_y, Pt.add_z, sg_add]; omega

theorem Diag.neg_dot (d : Diag) (p : Pt) : d.neg.dot p = - d.dot p := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> simp [Diag.dot, Diag.neg, sg] <;> omega

/-- **T1 (layer histogram).** For every orientation and every body diagonal, the twelve neighbour
offsets lie in layers Δs = -4, -2, 0, +2, +4 in numbers 1, 2, 6, 2, 1. -/
theorem layer_histogram (a : Axis) (d : Diag) :
    [-4, -2, 0, 2, 4].map (fun v => ((offsets a).map d.dot).count v) = [1, 2, 6, 2, 1] := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- At most three neighbours lie in lower layers (1 + 2 of T1). -/
theorem below_le_three (a : Axis) (d : Diag) :
    (offsets a).countP (fun o => decide (d.dot o < 0)) ≤ 3 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- No neighbour is more than four layers away. -/
theorem dot_offset_le_four (a : Axis) (d : Diag) : ∀ o ∈ offsets a, d.dot o ≤ 4 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

theorem dot_offset_ge_neg_four (a : Axis) (d : Diag) : ∀ o ∈ offsets a, -4 ≤ d.dot o := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- For a point k layers into a band of six layers (1 ≤ k ≤ 6; three consecutive lattice layers), at
most three of its neighbours lie outside the band. -/
theorem outside_band_le_three (a : Axis) (d : Diag) (k : Int) (h1 : 1 ≤ k) (h6 : k ≤ 6) :
    (offsets a).countP (fun o => decide (d.dot o ≤ -k ∨ 6 - k < d.dot o)) ≤ 3 := by
  have hk : k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 ∨ k = 5 ∨ k = 6 := by omega
  obtain ⟨sx, sy, sz⟩ := d
  rcases hk with rfl | rfl | rfl | rfl | rfl | rfl <;>
    cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

end Gump
