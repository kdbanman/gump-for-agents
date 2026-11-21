/-
The neighbourhood is symmetric: for cells p and q, q is a neighbour of p iff p is a neighbour of q.

The proof reduces the statement to a finite check. The axis of a point depends only on its coordinates
mod 2, a cell of axis a is congruent to the unit vector e_a mod 2, so the axis of p + o is the axis of
e_a + o; and for each of the 36 pairs (a, o ∈ offsets a), -o is an offset of that axis (`decide`).
-/
import Gump.Spec

namespace Gump

/-- The negative of a point. -/
def Pt.neg (o : Pt) : Pt := ⟨-o.x, -o.y, -o.z⟩

/-- The unit vector along an axis. -/
def Axis.unit : Axis → Pt
  | .X => ⟨1, 0, 0⟩
  | .Y => ⟨0, 1, 0⟩
  | .Z => ⟨0, 0, 1⟩

theorem Pt.ext' {p q : Pt} (hx : p.x = q.x) (hy : p.y = q.y) (hz : p.z = q.z) : p = q := by
  cases p; cases q; simp_all

/-- The axis depends only on the coordinates mod 2. -/
theorem axis_congr {p q : Pt} (hx : p.x % 2 = q.x % 2) (hy : p.y % 2 = q.y % 2)
    (_hz : p.z % 2 = q.z % 2) : p.axis = q.axis := by
  simp only [Pt.axis, hx, hy]

/-- A cell is congruent mod 2 to the unit vector of its axis. -/
theorem cell_mod_two {p : Pt} (hp : p.isCell = true) :
    p.x % 2 = p.axis.unit.x % 2 ∧ p.y % 2 = p.axis.unit.y % 2 ∧ p.z % 2 = p.axis.unit.z % 2 := by
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq] at hp
  simp only [Pt.axis, bne_iff_ne, ne_eq]
  split
  · simp only [Axis.unit]; omega
  · split
    · simp only [Axis.unit]; omega
    · simp only [Axis.unit]; omega

/-- The finite check: for every axis a and offset o of a, the negated offset is an offset of the axis
of e_a + o. -/
theorem neg_offset_mem : ∀ a : Axis, ∀ o ∈ offsets a, o.neg ∈ offsets (a.unit + o).axis := by
  intro a; cases a <;> decide

/-- **One direction of symmetry, for any cell p.** If q is a neighbour of the cell p, then p is a
neighbour of q. -/
theorem mem_nbrs_symm {p q : Pt} (hp : p.isCell = true) (h : q ∈ nbrs p) : p ∈ nbrs q := by
  simp only [nbrs, List.mem_map] at h ⊢
  obtain ⟨o, ho, rfl⟩ := h
  obtain ⟨h1, h2, h3⟩ := cell_mod_two hp
  have hax : (p + o).axis = (p.axis.unit + o).axis := by
    apply axis_congr <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  refine ⟨o.neg, ?_, ?_⟩
  · rw [hax]; exact neg_offset_mem _ o ho
  · apply Pt.ext' <;> simp [Pt.neg] <;> omega

/-- **The neighbourhood is symmetric** on cells. -/
theorem nbrs_symm {p q : Pt} (hp : p.isCell = true) (hq : q.isCell = true) :
    q ∈ nbrs p ↔ p ∈ nbrs q :=
  ⟨mem_nbrs_symm hp, mem_nbrs_symm hq⟩

/-- Without the hypothesis that p is a cell the statement is false: (1, 1, 0) is not a cell, (2, 2, 0)
is its neighbour, and it is not a neighbour of (2, 2, 0). -/
theorem nbrs_not_symm_off_cells :
    (⟨2, 2, 0⟩ : Pt) ∈ nbrs ⟨1, 1, 0⟩ ∧ (⟨1, 1, 0⟩ : Pt) ∉ nbrs ⟨2, 2, 0⟩ := by decide

end Gump
