/-
The definitions of `Gump/Basic.lean` restated in the terms of `reference/oracle.py` and
`docs/AUTOMATON.md` section 2, so that a reader checks a few statements and not 36 triples.

oracle.py, `offsets(axis)`: with a the normal axis and b, c the other two, the offsets are
  ±2 on b and ±2 on c, 0 on a                      (4 coplanar faces touching only at a corner)
  ±1 on a and ±1 on one of b, c, 0 on the other    (8 perpendicular faces sharing an edge).
oracle.py, `masks`: a cell of axis a has coordinate a odd and the other two even.
-/
import Gump.Basic

namespace Gump

/-- The coordinate of a point along an axis. -/
def Pt.get (p : Pt) : Axis → Int
  | .X => p.x
  | .Y => p.y
  | .Z => p.z

/-- The two other axes. -/
def Axis.others : Axis → Axis × Axis
  | .X => (.Y, .Z)
  | .Y => (.X, .Z)
  | .Z => (.X, .Y)

/-- **The neighbourhood, in the oracle's terms.** An offset is one of the twelve of a face with normal
axis a iff it is ±2 along both other axes and 0 along a, or ±1 along a and ±1 along exactly one
other axis. -/
theorem mem_offsets_iff (a : Axis) (o : Pt) :
    o ∈ offsets a ↔
      (o.get a = 0 ∧ (o.get a.others.1).natAbs = 2 ∧ (o.get a.others.2).natAbs = 2) ∨
      ((o.get a).natAbs = 1 ∧
        (((o.get a.others.1).natAbs = 1 ∧ o.get a.others.2 = 0) ∨
         (o.get a.others.1 = 0 ∧ (o.get a.others.2).natAbs = 1))) := by
  obtain ⟨x, y, z⟩ := o
  by_cases hb : (-2 ≤ x ∧ x ≤ 2) ∧ (-2 ≤ y ∧ y ≤ 2) ∧ (-2 ≤ z ∧ z ≤ 2)
  · -- inside the box [-2, 2]³: 125 points for each axis, each decided
    obtain ⟨hx, hy, hz⟩ := hb
    have hx' : x = -2 ∨ x = -1 ∨ x = 0 ∨ x = 1 ∨ x = 2 := by omega
    have hy' : y = -2 ∨ y = -1 ∨ y = 0 ∨ y = 1 ∨ y = 2 := by omega
    have hz' : z = -2 ∨ z = -1 ∨ z = 0 ∨ z = 1 ∨ z = 2 := by omega
    rcases hx' with rfl | rfl | rfl | rfl | rfl <;> rcases hy' with rfl | rfl | rfl | rfl | rfl <;>
      rcases hz' with rfl | rfl | rfl | rfl | rfl <;> cases a <;> decide
  · -- outside it both sides are false
    constructor
    · intro h
      exfalso; apply hb
      cases a <;> simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, Pt.mk.injEq] at h <;> omega
    · intro h
      exfalso; apply hb
      cases a <;> simp only [Pt.get, Axis.others] at h <;> omega

/-- The twelve offsets are distinct. -/
theorem offsets_nodup (a : Axis) : (offsets a).Nodup := by cases a <;> decide

/-- **Cells, in the oracle's terms** (`masks`): a point is a cell of axis a iff coordinate a is odd and
the other two are even. -/
theorem isCell_iff (p : Pt) :
    p.isCell = true ↔ ∃ a : Axis, p.get a % 2 = 1 ∧ p.get a.others.1 % 2 = 0 ∧ p.get a.others.2 % 2 = 0 := by
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq]
  constructor
  · rintro ((⟨⟨h1, h2⟩, h3⟩ | ⟨⟨h1, h2⟩, h3⟩) | ⟨⟨h1, h2⟩, h3⟩)
    · exact ⟨.X, by simp only [Pt.get, Axis.others]; omega⟩
    · exact ⟨.Y, by simp only [Pt.get, Axis.others]; omega⟩
    · exact ⟨.Z, by simp only [Pt.get, Axis.others]; omega⟩
  · rintro ⟨a, h⟩
    cases a <;> simp only [Pt.get, Axis.others] at h <;> omega

/-- The axis of a cell is its odd coordinate. -/
theorem axis_odd (p : Pt) (h : p.isCell = true) : p.get p.axis % 2 = 1 := by
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq] at h
  simp only [Pt.axis, bne_iff_ne, ne_eq]
  split
  · simp only [Pt.get]; omega
  · split
    · simp only [Pt.get]; omega
    · simp only [Pt.get]; omega

/-- **The rule, in the oracle's terms** (`step`): born with 4 or 5 live neighbours, stays with 3, 4
or 5. -/
theorem rule_iff (alive : Bool) (n : Nat) :
    rule alive n = true ↔ (alive = false ∧ (n = 4 ∨ n = 5)) ∨ (alive = true ∧ (n = 3 ∨ n = 4 ∨ n = 5)) := by
  cases alive <;> simp [rule] <;> omega

/-- Neighbours of cells are cells. -/
theorem nbrs_isCell (p : Pt) (h : p.isCell = true) : ∀ q ∈ nbrs p, q.isCell = true := by
  obtain ⟨x, y, z⟩ := p
  intro q hq
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq] at h
  simp only [nbrs, List.mem_map] at hq
  obtain ⟨o, ho, rfl⟩ := hq
  obtain ⟨ox, oy, oz⟩ := o
  simp only [Pt.axis, bne_iff_ne, ne_eq] at ho
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, beq_iff_eq, ne_eq, Pt.add_x,
    Pt.add_y, Pt.add_z]
  split at ho
  · simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, Pt.mk.injEq] at ho; omega
  · split at ho
    · simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, Pt.mk.injEq] at ho; omega
    · simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, Pt.mk.injEq] at ho; omega

end Gump
