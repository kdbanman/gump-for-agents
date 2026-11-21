/-
Gump: the cellular automaton B45/S345 on the faces of the cubic honeycomb, as coded in 2012
(`reference/oracle.py` is the ground truth; `docs/AUTOMATON.md` sections 1 and 2 are the prose).

Doubled coordinates: a cell is a point of ℤ³ with exactly one odd coordinate (the face's normal axis).
A cell has 12 neighbours: with normal axis a and other axes b, c, the offsets ±2e_b ± 2e_c (the four
coplanar faces that touch it at a corner) and ±e_a ± e_b, ±e_a ± e_c (the eight perpendicular faces
that share an edge with it).

Core Lean only: no Mathlib.
-/
namespace Gump

/-- A point of ℤ³ (doubled coordinates). -/
structure Pt where
  x : Int
  y : Int
  z : Int
deriving DecidableEq, Repr, Hashable

instance : Add Pt := ⟨fun p q => ⟨p.x + q.x, p.y + q.y, p.z + q.z⟩⟩

@[simp] theorem Pt.add_x (p q : Pt) : (p + q).x = p.x + q.x := rfl
@[simp] theorem Pt.add_y (p q : Pt) : (p + q).y = p.y + q.y := rfl
@[simp] theorem Pt.add_z (p q : Pt) : (p + q).z = p.z + q.z := rfl

/-- The orientation of a face: which coordinate is odd. -/
inductive Axis where
  | X | Y | Z
deriving DecidableEq, Repr

/-- A cell is a point with exactly one odd coordinate. -/
def Pt.isCell (p : Pt) : Bool :=
  (p.x % 2 != 0 && p.y % 2 == 0 && p.z % 2 == 0) ||
  (p.x % 2 == 0 && p.y % 2 != 0 && p.z % 2 == 0) ||
  (p.x % 2 == 0 && p.y % 2 == 0 && p.z % 2 != 0)

/-- The normal axis of a cell (for a point that is not a cell the value is not used). -/
def Pt.axis (p : Pt) : Axis :=
  if p.x % 2 != 0 then .X else if p.y % 2 != 0 then .Y else .Z

/-- The twelve neighbour offsets of a face with the given normal axis. -/
def offsets : Axis → List Pt
  | .X => [⟨0, 2, 2⟩, ⟨0, 2, -2⟩, ⟨0, -2, 2⟩, ⟨0, -2, -2⟩,
           ⟨1, 1, 0⟩, ⟨1, -1, 0⟩, ⟨-1, 1, 0⟩, ⟨-1, -1, 0⟩,
           ⟨1, 0, 1⟩, ⟨1, 0, -1⟩, ⟨-1, 0, 1⟩, ⟨-1, 0, -1⟩]
  | .Y => [⟨2, 0, 2⟩, ⟨2, 0, -2⟩, ⟨-2, 0, 2⟩, ⟨-2, 0, -2⟩,
           ⟨1, 1, 0⟩, ⟨-1, 1, 0⟩, ⟨1, -1, 0⟩, ⟨-1, -1, 0⟩,
           ⟨0, 1, 1⟩, ⟨0, 1, -1⟩, ⟨0, -1, 1⟩, ⟨0, -1, -1⟩]
  | .Z => [⟨2, 2, 0⟩, ⟨2, -2, 0⟩, ⟨-2, 2, 0⟩, ⟨-2, -2, 0⟩,
           ⟨1, 0, 1⟩, ⟨-1, 0, 1⟩, ⟨1, 0, -1⟩, ⟨-1, 0, -1⟩,
           ⟨0, 1, 1⟩, ⟨0, -1, 1⟩, ⟨0, 1, -1⟩, ⟨0, -1, -1⟩]

/-- The twelve neighbours of a cell. -/
def nbrs (p : Pt) : List Pt := (offsets p.axis).map (p + ·)

/-- A configuration: which points are alive. -/
abbrev Config := Pt → Bool

/-- The number of live neighbours. -/
def count (c : Config) (p : Pt) : Nat := (nbrs p).countP c

/-- B45/S345: a dead cell is born with 4 or 5 live neighbours, a live cell survives with 3, 4 or 5. -/
def rule (alive : Bool) (n : Nat) : Bool :=
  if alive then (3 ≤ n && n ≤ 5) else (n == 4 || n == 5)

/-- One synchronous generation. Points that are not cells are dead. -/
def step (c : Config) : Config := fun p => p.isCell && rule (c p) (count c p)

/-- `run c n` is the configuration after `n` generations. -/
def run (c : Config) : Nat → Config
  | 0 => c
  | n + 1 => step (run c n)

theorem offsets_length (a : Axis) : (offsets a).length = 12 := by cases a <;> rfl

theorem nbrs_length (p : Pt) : (nbrs p).length = 12 := by simp [nbrs, offsets_length]

/-- Nothing is born with fewer than four live neighbours. -/
theorem rule_dead_of_le_three {n : Nat} (h : n ≤ 3) : rule false n = false := by
  simp [rule]; omega

/-- A dead cell with at most three live neighbours stays dead. -/
theorem step_dead_of_count_le_three {c : Config} {p : Pt} (hp : c p = false) (h : count c p ≤ 3) :
    step c p = false := by
  simp [step, hp, rule_dead_of_le_three h]

end Gump
