import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Gump

/-- A first statement that needs Mathlib: the number of live neighbours as a sum. -/
theorem Gump.count_le_twelve (c : Gump.Config) (p : Gump.Pt) : Gump.count c p ≤ 12 := by
  unfold Gump.count
  exact (List.countP_le_length).trans (by simp [Gump.nbrs_length])
