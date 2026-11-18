/-
Which half-spaces are sealed. For a half-space of ℤ³ cut by an integer plane `u·p = C`, the cells strictly
beyond the plane form a sealed set (T2's confinement across that plane) **iff `u` is a multiple of a body
diagonal** (`|u_x| = |u_y| = |u_z|`), and then at every position `C`; for every other direction, at no position.

`research/audit/REVIEW-class.md` (Theorem A′ and its table, gump's row) found this by a scan of the primitive
directions with `|u_i| ≤ 5` and every plane position, and listed the completeness of that scan as not checked.
Here it is proved for every integer direction.

Directions are taken primitive, witnessed by an integer vector `w` with `u·w = 1` (every rational half-space
is cut by a plane with primitive normal, after dividing `u` and `C` by the gcd of `u`'s coordinates and
rounding `C` down).

Core Lean only: no Mathlib.
-/
import Gump.ThickSmall

namespace Gump

/-- The cells strictly beyond the plane `u·p = C`. -/
def beyond (u : Pt) (C : Int) : Pt → Bool := fun p => p.isCell && decide (C < dotv u p)

/-- One offset of each pair `±o`, for each orientation. -/
def reps : Axis → List Pt
  | .X => [⟨0, 2, 2⟩, ⟨0, 2, -2⟩, ⟨1, 1, 0⟩, ⟨1, -1, 0⟩, ⟨1, 0, 1⟩, ⟨1, 0, -1⟩]
  | .Y => [⟨2, 0, 2⟩, ⟨2, 0, -2⟩, ⟨1, 1, 0⟩, ⟨-1, 1, 0⟩, ⟨0, 1, 1⟩, ⟨0, 1, -1⟩]
  | .Z => [⟨2, 2, 0⟩, ⟨2, -2, 0⟩, ⟨1, 0, 1⟩, ⟨-1, 0, 1⟩, ⟨0, 1, 1⟩, ⟨0, -1, 1⟩]

theorem offsets_perm_reps (a : Axis) : (offsets a).Perm (reps a ++ (reps a).map Pt.neg) := by
  cases a <;> decide

theorem countP_or (l : List Pt) (P Q : Pt → Bool) (h : ∀ x ∈ l, P x = true → Q x = true → False) :
    l.countP P + l.countP Q = l.countP (fun x => P x || Q x) := by
  induction l with
  | nil => simp
  | cons a l ih =>
    have ih' := ih (fun x hx => h x (List.mem_cons_of_mem _ hx))
    have ha := h a (by simp)
    simp only [List.countP_cons]
    cases hp : P a <;> cases hq : Q a <;> simp_all <;> omega

/-- The number of offsets at least `δ` behind the plane is the number of pairs `±o` with `|u·o| ≥ δ`. -/
theorem behind_count (a : Axis) (u : Pt) (δ : Int) (hδ : 1 ≤ δ) :
    (offsets a).countP (fun o => decide (dotv u o ≤ -δ)) =
      (reps a).countP (fun o => decide (δ ≤ dotv u o ∨ dotv u o ≤ -δ)) := by
  rw [List.Perm.countP_eq _ (offsets_perm_reps a), List.countP_append, List.countP_map,
    countP_or _ _ _ (by
      intro x _ h1 h2
      simp only [Function.comp, decide_eq_true_eq, dotv_neg] at h1 h2
      omega)]
  apply List.countP_congr
  intro o _
  simp only [Function.comp, Bool.or_eq_true, decide_eq_true_eq, dotv_neg]
  omega

/-- The six values `u·o`, one for each pair `±o`, written out. -/
def pairVals (u : Pt) : Axis → List Int
  | .X => [2 * u.y + 2 * u.z, 2 * u.y - 2 * u.z, u.x + u.y, u.x - u.y, u.x + u.z, u.x - u.z]
  | .Y => [2 * u.x + 2 * u.z, 2 * u.x - 2 * u.z, u.x + u.y, -u.x + u.y, u.y + u.z, u.y - u.z]
  | .Z => [2 * u.x + 2 * u.y, 2 * u.x - 2 * u.y, u.x + u.z, -u.x + u.z, u.y + u.z, -u.y + u.z]

theorem pairVals_eq (u : Pt) (a : Axis) : (reps a).map (dotv u) = pairVals u a := by
  cases a <;> simp only [reps, List.map_cons, List.map_nil, dotv, pairVals, List.cons.injEq, and_true] <;>
    omega

theorem behind_count' (a : Axis) (u : Pt) (δ : Int) (hδ : 1 ≤ δ) :
    (offsets a).countP (fun o => decide (dotv u o ≤ -δ)) =
      (pairVals u a).countP (fun v => decide (δ ≤ v ∨ v ≤ -δ)) := by
  rw [behind_count a u δ hδ, ← pairVals_eq, List.countP_map]
  rfl

/-! ## Counts behind a plane, for a symbolic direction (each: 64 cases, `omega`) -/

/-- The orientation with the largest `|u_a|`, one step behind the plane: at least four neighbours. -/
theorem count_max_one (a : Axis) (u : Pt)
    (h1 : (u.get a.others.1).natAbs ≤ (u.get a).natAbs) (h2 : (u.get a.others.2).natAbs ≤ (u.get a).natAbs)
    (hnd : ¬ (u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs)) :
    4 ≤ (offsets a).countP (fun o => decide (dotv u o ≤ -1)) := by
  rw [behind_count' a u 1 (by decide)]
  cases a <;> simp only [pairVals, List.countP_cons, List.countP_nil, decide_eq_true_eq] <;>
    simp only [Pt.get, Axis.others] at h1 h2 <;>
    split <;> split <;> split <;> split <;> split <;> split <;> omega

/-- The orientation with the largest `|u_a|`, two steps behind the plane, all coordinates odd. -/
theorem count_max_two (a : Axis) (u : Pt)
    (h1 : (u.get a.others.1).natAbs ≤ (u.get a).natAbs) (h2 : (u.get a.others.2).natAbs ≤ (u.get a).natAbs)
    (hnd : ¬ (u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs))
    (hx : u.x % 2 = 1) (hy : u.y % 2 = 1) (hz : u.z % 2 = 1) :
    4 ≤ (offsets a).countP (fun o => decide (dotv u o ≤ -2)) := by
  rw [behind_count' a u 2 (by decide)]
  cases a <;> simp only [pairVals, List.countP_cons, List.countP_nil, decide_eq_true_eq] <;>
    simp only [Pt.get, Axis.others] at h1 h2 <;>
    split <;> split <;> split <;> split <;> split <;> split <;> omega

/-- An orientation whose coordinate differs in parity from another one, one step behind the plane. -/
theorem count_parity_one (a : Axis) (u : Pt)
    (h : (u.get a.others.1 - u.get a) % 2 = 1 ∨ (u.get a.others.2 - u.get a) % 2 = 1) :
    4 ≤ (offsets a).countP (fun o => decide (dotv u o ≤ -1)) := by
  rw [behind_count' a u 1 (by decide)]
  cases a <;> simp only [pairVals, List.countP_cons, List.countP_nil, decide_eq_true_eq] <;>
    simp only [Pt.get, Axis.others] at h <;>
    split <;> split <;> split <;> split <;> split <;> split <;> omega

/-- Along a body diagonal (all `|u_i|` equal), at most three offsets point behind. -/
theorem count_diag (a : Axis) (u : Pt) (h : u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs) :
    (offsets a).countP (fun o => decide (dotv u o ≤ -1)) ≤ 3 := by
  rw [behind_count' a u 1 (by decide)]
  cases a <;> simp only [pairVals, List.countP_cons, List.countP_nil, decide_eq_true_eq] <;>
    split <;> split <;> split <;> split <;> split <;> split <;> omega

/-! ## The theorem -/

/-- **Diagonal directions: sealed at every position.** If `|u_x| = |u_y| = |u_z|`, the cells beyond any
plane `u·p = C` form a sealed set. -/
theorem beyond_sealed_of_diag (u : Pt) (h : u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs) (C : Int) :
    Sealed (beyond u C) := by
  intro p hp
  simp only [beyond, Bool.and_eq_true, decide_eq_true_eq] at hp
  refine Nat.le_trans ?_ (count_diag p.axis u h)
  unfold nbrs
  rw [List.countP_map]
  apply List.countP_mono_left
  intro o ho hq
  have hc : (p + o).isCell = true := nbrs_isCell p hp.1 (p + o) (List.mem_map.2 ⟨o, ho, rfl⟩)
  simp only [Function.comp, beyond, hc, Bool.true_and, dotv_add, Bool.not_eq_true',
    decide_eq_false_iff_not] at hq
  simp only [decide_eq_true_eq]
  omega

/-- A cell of a given orientation at a given level of `u`, when the level has the right parity. -/
def cellAt (a : Axis) (k : Int) (w : Pt) : Pt :=
  ⟨a.unit.x + 2 * (k * w.x), a.unit.y + 2 * (k * w.y), a.unit.z + 2 * (k * w.z)⟩

theorem cellAt_isCell (a : Axis) (k : Int) (w : Pt) : (cellAt a k w).isCell = true := by
  cases a <;> simp [cellAt, Axis.unit, Pt.isCell] <;> omega

theorem cellAt_axis (a : Axis) (k : Int) (w : Pt) : (cellAt a k w).axis = a := by
  cases a <;> simp [cellAt, Axis.unit, Pt.axis] <;> omega

theorem dotv_cellAt (a : Axis) (u : Pt) (k : Int) (w : Pt) :
    dotv u (cellAt a k w) = u.get a + 2 * (k * dotv u w) := by
  have e : ∀ m n : Int, m * (2 * (k * n)) = 2 * (k * (m * n)) := by
    intro m n
    rw [← Int.mul_assoc, Int.mul_comm m 2, Int.mul_assoc, ← Int.mul_assoc m k n, Int.mul_comm m k,
      Int.mul_assoc]
  cases a <;> simp only [dotv, cellAt, Axis.unit, Pt.get, Int.mul_add, e, Int.mul_zero, Int.mul_one] <;>
    omega

/-- If the cells of orientation `a` at level `C + δ` have at least four neighbours `δ` or more behind, the
half-space beyond `C` is not sealed. -/
theorem not_sealed_of_count (u w : Pt) (hw : dotv u w = 1) (C : Int) (a : Axis) (δ : Int) (hδ : 1 ≤ δ)
    (hpar : (C + δ - u.get a) % 2 = 0)
    (h4 : 4 ≤ (offsets a).countP (fun o => decide (dotv u o ≤ -δ))) : ¬ Sealed (beyond u C) := by
  intro hS
  let p := cellAt a ((C + δ - u.get a) / 2) w
  have hlev : dotv u p = C + δ := by
    simp only [p, dotv_cellAt, hw, Int.mul_one]; omega
  have hp : beyond u C p = true := by simp [beyond, p, cellAt_isCell, hlev]; omega
  have := hS p hp
  have hge : (offsets a).countP (fun o => decide (dotv u o ≤ -δ)) ≤
      (nbrs p).countP (fun q => !beyond u C q) := by
    unfold nbrs
    rw [List.countP_map, cellAt_axis]
    apply List.countP_mono_left
    intro o _ ho
    simp only [decide_eq_true_eq] at ho
    simp only [Function.comp, beyond, dotv_add, hlev, Bool.not_eq_true', Bool.and_eq_false_imp,
      decide_eq_false_iff_not]
    intro _; omega
  omega

/-- **Every other direction: sealed at no position.** If `u` is primitive (`u·w = 1` for some integer `w`)
and not a multiple of a body diagonal, then for every `C` some cell beyond the plane `u·p = C` has at least
four neighbours on the near side: the far side is not sealed. -/
theorem beyond_not_sealed (u w : Pt) (hw : dotv u w = 1)
    (hnd : ¬ (u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs)) (C : Int) : ¬ Sealed (beyond u C) := by
  obtain ⟨x, y, z⟩ := u
  -- not all coordinates are even
  have hodd : x % 2 = 1 ∨ y % 2 = 1 ∨ z % 2 = 1 := by
    apply Classical.byContradiction
    intro hall
    have ex : x = 2 * (x / 2) := by omega
    have ey : y = 2 * (y / 2) := by omega
    have ez : z = 2 * (z / 2) := by omega
    simp only [dotv] at hw
    rw [ex, ey, ez, Int.mul_assoc, Int.mul_assoc, Int.mul_assoc] at hw
    omega
  by_cases hsame : x % 2 = y % 2 ∧ y % 2 = z % 2
  · -- all odd: the orientation with the largest coordinate, one or two steps behind
    have hx : x % 2 = 1 := by omega
    have hy : y % 2 = 1 := by omega
    have hz : z % 2 = 1 := by omega
    have pick : ∀ a : Axis, ((⟨x, y, z⟩ : Pt).get a.others.1).natAbs ≤ ((⟨x, y, z⟩ : Pt).get a).natAbs →
        ((⟨x, y, z⟩ : Pt).get a.others.2).natAbs ≤ ((⟨x, y, z⟩ : Pt).get a).natAbs →
        ¬ Sealed (beyond ⟨x, y, z⟩ C) := by
      intro a h1 h2
      have ha : ((⟨x, y, z⟩ : Pt).get a) % 2 = 1 := by cases a <;> simpa [Pt.get]
      by_cases hC : C % 2 = 0
      · exact not_sealed_of_count _ w hw C a 1 (by decide) (by omega) (count_max_one a _ h1 h2 hnd)
      · exact not_sealed_of_count _ w hw C a 2 (by decide) (by omega)
          (count_max_two a _ h1 h2 hnd hx hy hz)
    by_cases hX : y.natAbs ≤ x.natAbs ∧ z.natAbs ≤ x.natAbs
    · exact pick .X hX.1 hX.2
    · by_cases hY : x.natAbs ≤ y.natAbs ∧ z.natAbs ≤ y.natAbs
      · exact pick .Y hY.1 hY.2
      · exact pick .Z (by simp only [Pt.get, Axis.others]; omega) (by simp only [Pt.get, Axis.others]; omega)
  · -- mixed parities: an orientation one step behind with a partner of the other parity
    by_cases hX : (C + 1 - x) % 2 = 0
    · exact not_sealed_of_count _ w hw C .X 1 (by decide) (by simpa [Pt.get] using hX)
        (count_parity_one .X _ (by simp only [Pt.get, Axis.others]; omega))
    · by_cases hY : (C + 1 - y) % 2 = 0
      · exact not_sealed_of_count _ w hw C .Y 1 (by decide) (by simpa [Pt.get] using hY)
          (count_parity_one .Y _ (by simp only [Pt.get, Axis.others]; omega))
      · exact not_sealed_of_count _ w hw C .Z 1 (by decide) (by simp only [Pt.get]; omega)
          (count_parity_one .Z _ (by simp only [Pt.get, Axis.others]; omega))

/-- **The sealed half-spaces of gump.** For a primitive integer direction `u` and any position `C`, the cells
beyond the plane `u·p = C` are sealed iff `|u_x| = |u_y| = |u_z|`, i.e. `u` is a body diagonal. -/
theorem beyond_sealed_iff (u w : Pt) (hw : dotv u w = 1) (C : Int) :
    Sealed (beyond u C) ↔ (u.x.natAbs = u.y.natAbs ∧ u.y.natAbs = u.z.natAbs) := by
  constructor
  · intro hS
    apply Classical.byContradiction
    intro hnd
    exact beyond_not_sealed u w hw hnd C hS
  · intro h
    exact beyond_sealed_of_diag u h C

/-- **Axis-aligned half-spaces are never sealed** (the remark under T2: a cell just beyond the plane can have
four neighbours on the near side, which is why cubes grow into octahedra). -/
theorem axis_halfspace_not_sealed (C : Int) : ¬ Sealed (beyond ⟨1, 0, 0⟩ C) :=
  beyond_not_sealed ⟨1, 0, 0⟩ ⟨1, 0, 0⟩ (by decide) (by decide) C

/-! ## Theorem 3 along every generic direction -/

/-- For a direction orthogonal to no offset, exactly six of the twelve offsets point forward. -/
theorem forward_count (a : Axis) (v : Pt) (hv : ∀ o ∈ offsets a, dotv v o ≠ 0) :
    (offsets a).countP (fun o => decide (1 ≤ dotv v o)) = 6 := by
  have h := behind_count a v.neg 1 (by decide)
  have e1 : (offsets a).countP (fun o => decide (dotv v.neg o ≤ -1)) =
      (offsets a).countP (fun o => decide (1 ≤ dotv v o)) := by
    apply List.countP_congr; intro o _
    have : dotv v.neg o = - dotv v o := by simp only [dotv, Pt.neg, Int.neg_mul]; omega
    simp only [decide_eq_true_eq, this]; omega
  have e2 : (reps a).countP (fun o => decide (1 ≤ dotv v.neg o ∨ dotv v.neg o ≤ -1)) = 6 := by
    have hlen : (reps a).length = 6 := by cases a <;> rfl
    rw [← hlen, List.countP_eq_length]
    intro o ho
    have hmem : o ∈ offsets a := by
      have := (List.Perm.mem_iff (offsets_perm_reps a)).2 (List.mem_append_left _ ho)
      exact this
    have hne := hv o hmem
    have : dotv v.neg o = - dotv v o := by simp only [dotv, Pt.neg, Int.neg_mul]; omega
    simp only [decide_eq_true_eq, this]; omega
  rw [← e1, h, e2]

/-- A nonempty set on which an integer function is bounded above has a point where it is largest. -/
theorem exists_max_of_bdd (S : Pt → Bool) (f : Pt → Int) (M : Int) (hb : ∀ p, S p = true → f p ≤ M) :
    ∀ n : Nat, ∀ p₀, S p₀ = true → (M - f p₀).toNat ≤ n → ∃ p, S p = true ∧ ∀ q, S q = true → f q ≤ f p := by
  intro n
  induction n with
  | zero =>
    intro p₀ hp₀ hn
    refine ⟨p₀, hp₀, fun q hq => ?_⟩
    have := hb q hq; omega
  | succ n ih =>
    intro p₀ hp₀ hn
    by_cases h : ∃ q, S q = true ∧ f p₀ < f q
    · obtain ⟨q, hq, hlt⟩ := h
      exact ih q hq (by have := hb q hq; omega)
    · exact ⟨p₀, hp₀, fun q hq => by
        apply Classical.byContradiction; intro hn'; exact h ⟨q, hq, by omega⟩⟩

/-- **Theorem 3, full lattice, sharper: a nonempty sealed set is unbounded in every generic direction.** For
every integer `v` orthogonal to none of the 36 offsets and every bound `M`, a nonempty sealed set has a point
with `v·p > M`. (Genericity is needed: the half-spaces `d·p ≤ C` are sealed and bounded along `d`.) -/
theorem sealed_unbounded (S : Pt → Bool) (hS : Sealed S) (hne : ∃ p, S p = true) (v : Pt)
    (hv : ∀ a, ∀ o ∈ offsets a, dotv v o ≠ 0) (M : Int) : ∃ p, S p = true ∧ M < dotv v p := by
  apply Classical.byContradiction
  intro hno
  have hb : ∀ p, S p = true → dotv v p ≤ M := fun p hp => by
    apply Classical.byContradiction; intro h; exact hno ⟨p, hp, by omega⟩
  obtain ⟨p₀, hp₀⟩ := hne
  obtain ⟨p, hp, hmax⟩ := exists_max_of_bdd S (dotv v) M hb _ p₀ hp₀ (Nat.le_refl _)
  have h3 := hS p hp
  have h6 : 6 ≤ (nbrs p).countP (fun q => !S q) := by
    rw [← forward_count p.axis v (hv p.axis)]
    unfold nbrs
    rw [List.countP_map]
    apply List.countP_mono_left
    intro o _ ho
    simp only [decide_eq_true_eq] at ho
    simp only [Function.comp]
    cases hq : S (p + o) with
    | false => rfl
    | true => have := hmax _ hq; rw [dotv_add] at this; omega
  omega

end Gump
