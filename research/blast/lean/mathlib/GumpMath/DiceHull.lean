/-
Theorem 1 of `rigour/THEOREMS.md` on the hull faces, for every R (added 2026-11-24, second task).

`DiceBound.lean` proved ln τ < 2.5095 · A for faces whose cells all have three coins; on the hull face `hull R`
the three corner cells have only two (the point two layers beneath a corner lies outside the hull). Here, for
every R: every cell of `hull R` has coins (2, 1) except the corners, which have (2, 0) and at most two in-layer
neighbours (`hull_cells`, by a case analysis on the orientation of the cell with `omega`); a corner dies when both
its coins are tails whatever its state (`corner_cell`), with probability (1 - ρ1)² ≥ δ₀. So every cell of every hull
face dies with probability ≥ δ₀ = min(ρ1²ρ2, (1-ρ1)²(1-ρ2)) from every state:
`survival_le_hull`: P_x(T > t) ≤ (1 - δ₀^A)^t, `lntau_le_hull`: ln τ < 2.5095 · A for every quasi-stationary law.
-/
import GumpMath.DiceExit

namespace Gump.Dice
open Gump Finset Matrix

theorem mem_hullCells (R : ℕ) (p : Pt) :
    p ∈ hullCells R ↔ 0 ≤ p.x ∧ 0 ≤ p.y ∧ 0 ≤ p.z ∧ p.x + p.y + p.z = R ∧ p.isCell = true := by
  unfold hullCells
  simp only [List.mem_filter, List.mem_flatMap, List.mem_map, List.mem_range]
  constructor
  · rintro ⟨⟨x, hx, y, hy, rfl⟩, hc⟩
    refine ⟨by simp, by simp, by simp, ?_, hc⟩
    simp only; omega
  · rintro ⟨h1, h2, h3, h4, hc⟩
    refine ⟨⟨p.x.toNat, by omega, p.y.toNat, by omega, ?_⟩, hc⟩
    obtain ⟨a, b, c⟩ := p
    simp only at h1 h2 h3 h4 ⊢
    congr 1 <;> omega

theorem filterMap_length_countP {α β : Type*} (f : α → Option β) (l : List α) :
    (l.filterMap f).length = l.countP fun a => (f a).isSome := by
  induction l with
  | nil => simp
  | cons a l ih =>
      rw [List.filterMap_cons, List.countP_cons]
      cases h : f a <;> simp [h, ih]

/-- The in-layer degree of a point of the hull face is at most the number of its in-layer neighbours with
non-negative coordinates. -/
theorem hull_deg_le (R : ℕ) (p : Pt) :
    ((nbrs p).filterMap fun q => if d111.dot q = d111.dot p then (hullCells R).idxOf? q else none).length ≤
      (nbrs p).countP fun q => decide (d111.dot q = d111.dot p) && decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z) := by
  rw [filterMap_length_countP]
  refine List.countP_mono_left fun q _ h => ?_
  by_cases hc : d111.dot q = d111.dot p
  · simp only [hc, ite_true, List.isSome_idxOf?, mem_hullCells] at h
    simp [hc, h.1, h.2.1, h.2.2.1]
  · simp [hc] at h

section cases
variable (R : ℕ) (x y z : ℤ) (h1 : 0 ≤ x) (h2 : 0 ≤ y) (h3 : 0 ≤ z) (h4 : x + y + z = R)
include h1 h2 h3 h4

/-- The counts for a cell of orientation x (x odd, y and z even). -/
theorem cell_X (hx : x % 2 = 1) (hy : y % 2 = 0) (hz : z % 2 = 0) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 2) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 2 ∧
    ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 1 ∨
     ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 0 ∧
      (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
        decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) ≤ 2)) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .X := by simp [Pt.axis, hx]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : y = 0 ∧ z = 0
  · obtain ⟨rfl, rfl⟩ := hc
    refine ⟨?_, Or.inr ⟨?_, ?_⟩⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega
  · have hc' : y ≠ 0 ∨ z ≠ 0 := by tauto
    refine ⟨?_, Or.inl ?_⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega

theorem cell_Y (hx : x % 2 = 0) (hy : y % 2 = 1) (hz : z % 2 = 0) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 2) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 2 ∧
    ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 1 ∨
     ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 0 ∧
      (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
        decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) ≤ 2)) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Y := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : x = 0 ∧ z = 0
  · obtain ⟨rfl, rfl⟩ := hc
    refine ⟨?_, Or.inr ⟨?_, ?_⟩⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega
  · have hc' : x ≠ 0 ∨ z ≠ 0 := by tauto
    refine ⟨?_, Or.inl ?_⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega

theorem cell_Z (hx : x % 2 = 0) (hy : y % 2 = 0) (hz : z % 2 = 1) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 2) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 2 ∧
    ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 1 ∨
     ((nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = 0 ∧
      (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
        decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) ≤ 2)) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Z := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : x = 0 ∧ y = 0
  · obtain ⟨rfl, rfl⟩ := hc
    refine ⟨?_, Or.inr ⟨?_, ?_⟩⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega
  · have hc' : x ≠ 0 ∨ y ≠ 0 := by tauto
    refine ⟨?_, Or.inl ?_⟩ <;> (try simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false, Bool.false_and,
      ite_true, ite_false, Bool.false_eq_true]) <;> omega

end cases

/-- **The cells of every hull face**: two coins one layer in; one coin two layers in, except at the corners,
which have at most two in-layer neighbours. -/
theorem hull_cells (R : ℕ) (i : ℕ) (hi : i < (hull R).A) :
    (hull R).m1 i = 2 ∧ ((hull R).m2 i = 1 ∨ ((hull R).m2 i = 0 ∧ ((hull R).nb i).length ≤ 2)) := by
  have hp : (hull R).cell i ∈ hullCells R := by
    unfold Face.cell; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]
    exact List.getElem_mem _
  have hdeg := hull_deg_le R ((hull R).cell i)
  have e1 : (hull R).m1 i = (nbrs ((hull R).cell i)).countP (fun q => decide (d111.dot q =
      d111.dot ((hull R).cell i) - 2) && decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) := rfl
  have e2 : (hull R).m2 i = (nbrs ((hull R).cell i)).countP (fun q => decide (d111.dot q =
      d111.dot ((hull R).cell i) - 4) && decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) := rfl
  have e3 : (hull R).nb i = (nbrs ((hull R).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((hull R).cell i) then (hullCells R).idxOf? q else none := rfl
  rw [e1, e2, e3]
  obtain ⟨h1, h2, h3, h4, hc⟩ := (mem_hullCells R _).mp hp
  generalize (hull R).cell i = p at h1 h2 h3 h4 hc hdeg ⊢
  obtain ⟨x, y, z⟩ := p
  simp only at h1 h2 h3 h4
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hc
  have hpar : (x % 2 = 1 ∧ y % 2 = 0 ∧ z % 2 = 0) ∨ (x % 2 = 0 ∧ y % 2 = 1 ∧ z % 2 = 0) ∨
      (x % 2 = 0 ∧ y % 2 = 0 ∧ z % 2 = 1) := by omega
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · obtain ⟨a, b⟩ := cell_X R x y z h1 h2 h3 h4 hx hy hz
    exact ⟨a, b.imp id fun h => ⟨h.1, hdeg.trans h.2⟩⟩
  · obtain ⟨a, b⟩ := cell_Y R x y z h1 h2 h3 h4 hx hy hz
    exact ⟨a, b.imp id fun h => ⟨h.1, hdeg.trans h.2⟩⟩
  · obtain ⟨a, b⟩ := cell_Z R x y z h1 h2 h3 h4 hx hy hz
    exact ⟨a, b.imp id fun h => ⟨h.1, hdeg.trans h.2⟩⟩

/-- A cell with two coins one layer in, none two layers in, and at most two live neighbours dies when both coins
are tails: 1 - aliveProb ≥ (1 - ρ1)² (and 0 ≤ aliveProb ≤ 1). -/
theorem corner_cell (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (k : ℕ) (hk : k ≤ 2) (s : Bool) :
    0 ≤ aliveProb ρ1 ρ2 2 0 k s ∧ aliveProb ρ1 ρ2 2 0 k s ≤ 1 ∧ (1 - ρ1) ^ 2 ≤ 1 - aliveProb ρ1 ρ2 2 0 k s := by
  have r1 : 0 ≤ 1 - ρ1 := by linarith
  have w1 : 0 ≤ (1 - ρ1) ^ 2 := by positivity
  have w2 : 0 ≤ 2 * ρ1 * (1 - ρ1) := by positivity
  have w3 : 0 ≤ ρ1 ^ 2 := by positivity
  have hsum : (1 - ρ1) ^ 2 + 2 * ρ1 * (1 - ρ1) + ρ1 ^ 2 = 1 := by ring
  have h0 : rule s k = false := by cases s <;> simp [rule] <;> omega
  simp only [aliveProb, bin, sum_range_succ, sum_range_zero, zero_add, Nat.choose, Nat.cast_one, Nat.cast_ofNat,
    pow_zero, pow_one, one_mul, mul_one, Nat.sub_zero, Nat.sub_self, add_zero, h0, Bool.false_eq_true, ite_false]
  norm_num
  split_ifs <;> refine ⟨?_, ?_, ?_⟩ <;> first | linarith | nlinarith

namespace Face

theorem hull_a (R : ℕ) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (x i : ℕ) (hi : i < (hull R).A) :
    0 ≤ (hull R).a ρ1 ρ2 x i ∧ (hull R).a ρ1 ρ2 x i ≤ 1 ∧ delta0 ρ1 ρ2 ≤ 1 - (hull R).a ρ1 ρ2 x i := by
  obtain ⟨hm1, hm2⟩ := hull_cells R i hi
  unfold a
  rw [hm1]
  rcases hm2 with hm2 | ⟨hm2, hdeg⟩
  · rw [hm2]; exact death_cell ρ1 ρ2 h1 h1' h2 h2' _ _
  · rw [hm2]
    have hk : (hull R).k x i ≤ 2 := le_trans List.countP_le_length hdeg
    obtain ⟨a1, a2, a3⟩ := corner_cell ρ1 ρ2 h1 h1' _ hk (x.testBit i)
    refine ⟨a1, a2, le_trans ?_ a3⟩
    have r2 : 0 ≤ 1 - ρ2 := by linarith
    have : (1 - ρ1) ^ 2 * (1 - ρ2) ≤ (1 - ρ1) ^ 2 := by
      have : 0 ≤ (1 - ρ1) ^ 2 := by positivity
      nlinarith
    exact (min_le_right _ _).trans this

theorem hull_a_empty (R : ℕ) (ρ1 ρ2 : ℚ) (i : ℕ) (hi : i < (hull R).A) : (hull R).a ρ1 ρ2 0 i = 0 := by
  obtain ⟨hm1, hm2⟩ := hull_cells R i hi
  unfold a
  have hk : (hull R).k 0 i = 0 := by simp [k]
  rw [hm1, hk]
  rcases hm2 with hm2 | ⟨hm2, -⟩ <;> rw [hm2] <;> simp [aliveProb, sum_range_succ, rule, Nat.testBit]

theorem hull_P_empty_row (R : ℕ) (ρ1 ρ2 : ℚ) (y : Fin (2 ^ (hull R).A)) (hy : (y : ℕ) ≠ 0) :
    (hull R).P ρ1 ρ2 (hull R).empty y = 0 := by
  obtain ⟨i, hi⟩ := Nat.exists_testBit_of_ne_zero hy
  have hiA : i < (hull R).A := by
    by_contra hcon
    have := Nat.ge_two_pow_of_testBit hi
    have : 2 ^ (hull R).A ≤ 2 ^ i := Nat.pow_le_pow_right (by norm_num) (by omega)
    have := y.isLt
    omega
  exact prod_eq_zero (mem_range.mpr hiA) (by simp [hi, empty, hull_a_empty R ρ1 ρ2 i hiA])

theorem hull_survival_empty (R : ℕ) (ρ1 ρ2 : ℚ) : ∀ t, (hull R).survival ρ1 ρ2 t (hull R).empty = 0
  | 0 => by simp [survival, live, empty]
  | t + 1 => by
      rw [survival_succ]
      refine sum_eq_zero fun y _ => ?_
      by_cases hy : (y : ℕ) = 0
      · have : y = (hull R).empty := Fin.ext hy
        rw [this, hull_survival_empty R ρ1 ρ2 t, mul_zero]
      · rw [hull_P_empty_row R ρ1 ρ2 y hy, zero_mul]

end Face

theorem hull_death_ge (R : ℕ) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1)
    (x : Fin (2 ^ (hull R).A)) : delta0 ρ1 ρ2 ^ (hull R).A ≤ (hull R).death ρ1 ρ2 x := by
  have r1 : 0 ≤ 1 - ρ1 := by linarith
  have r2 : 0 ≤ 1 - ρ2 := by linarith
  have e : delta0 ρ1 ρ2 ^ (hull R).A = ∏ _i ∈ range (hull R).A, delta0 ρ1 ρ2 := by rw [prod_const, card_range]
  rw [Face.death, e]
  refine prod_le_prod₀ (fun i _ => ?_) (fun i hi => (Face.hull_a R ρ1 ρ2 h1 h1' h2 h2' x i (mem_range.mp hi)).2.2)
  simp only [delta0]; exact le_min (by positivity) (by positivity)

/-- **Theorem 1 on every hull face, survival form**: P_x(T > t) ≤ (1 - δ₀^A)^t. -/
theorem survival_le_hull (R : ℕ) (ρ1 ρ2 : ℚ) (h1 : 0 ≤ ρ1) (h1' : ρ1 ≤ 1) (h2 : 0 ≤ ρ2) (h2' : ρ2 ≤ 1) :
    ∀ (t : ℕ) (x : Fin (2 ^ (hull R).A)), (hull R).survival ρ1 ρ2 t x ≤ (1 - delta0 ρ1 ρ2 ^ (hull R).A) ^ t
  | 0, x => by
      simp only [Face.survival, pow_zero, Matrix.one_mulVec, Face.live]
      split <;> norm_num
  | t + 1, x => by
      have hP : ∀ y, 0 ≤ (hull R).P ρ1 ρ2 x y := fun y => prod_nonneg fun i hi => by
        have := Face.hull_a R ρ1 ρ2 h1 h1' h2 h2' x i (mem_range.mp hi)
        split <;> linarith [this.1, this.2.1]
      set B := (1 - delta0 ρ1 ρ2 ^ (hull R).A) ^ t
      have hB : ∀ y, (hull R).survival ρ1 ρ2 t y ≤ B - (if y = (hull R).empty then B else 0) := by
        intro y
        split
        · rename_i h; rw [h, Face.hull_survival_empty R ρ1 ρ2]; simp
        · simpa using survival_le_hull R ρ1 ρ2 h1 h1' h2 h2' t y
      rw [Face.survival_succ]
      calc ∑ y, (hull R).P ρ1 ρ2 x y * (hull R).survival ρ1 ρ2 t y
          ≤ ∑ y, (hull R).P ρ1 ρ2 x y * (B - (if y = (hull R).empty then B else 0)) :=
            sum_le_sum fun y _ => mul_le_mul_of_nonneg_left (hB y) (hP y)
        _ = B * (1 - (hull R).death ρ1 ρ2 x) := by
            simp only [mul_sub, mul_ite, mul_zero, sum_sub_distrib, sum_ite_eq', mem_univ, ite_true]
            rw [← sum_mul, Face.P_row_sum, Face.P_zero_col]; ring
        _ ≤ B * (1 - delta0 ρ1 ρ2 ^ (hull R).A) := by
            have hB0 : 0 ≤ B := by
              have := survival_le_hull R ρ1 ρ2 h1 h1' h2 h2' t (hull R).empty
              rw [Face.hull_survival_empty R ρ1 ρ2] at this; exact this
            have := hull_death_ge R ρ1 ρ2 h1 h1' h2 h2' x
            nlinarith
        _ = (1 - delta0 ρ1 ρ2 ^ (hull R).A) ^ (t + 1) := by rw [pow_succ]

/-- **Theorem 1 on every hull face, in nats**: every quasi-stationary law of `hull R` at (0.44, 0.42) has
ln τ = -ln(1 - λ) < 2.5095 · A. -/
theorem lntau_le_hull (R : ℕ) (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam)
    (hA : 0 < (hull R).A) : -Real.log (1 - lam) < 2.5095 * (hull R).A := by
  have hd := Data.qsd_death (hull R) ρ1 ρ2 μ lam hq
  have hle : (((delta0 ρ1 ρ2 ^ (hull R).A : ℚ)) : ℝ) ≤ 1 - lam := by
    rw [← hd]
    calc (((delta0 ρ1 ρ2 ^ (hull R).A : ℚ)) : ℝ) = ∑ x, μ x * (((delta0 ρ1 ρ2 ^ (hull R).A : ℚ)) : ℝ) := by
          rw [← sum_mul, hq.total, one_mul]
      _ ≤ ∑ x, μ x * ((hull R).P ρ1 ρ2 x (hull R).empty : ℝ) := by
          refine sum_le_sum fun x _ => mul_le_mul_of_nonneg_left ?_ (hq.nonneg x)
          rw [Face.P_zero_col]
          exact_mod_cast hull_death_ge R ρ1 ρ2 (by norm_num [ρ1]) (by norm_num [ρ1]) (by norm_num [ρ2])
            (by norm_num [ρ2]) x
  have hδ : delta0 ρ1 ρ2 = 0.081312 := by norm_num [delta0, ρ1, ρ2]
  rw [hδ] at hle
  push_cast at hle
  have hd1 : (0 : ℝ) < 0.081312 := by norm_num
  have hpos : (0 : ℝ) < (0.081312 : ℝ) ^ (hull R).A := pow_pos hd1 _
  have hlog : -Real.log (1 - lam) ≤ -Real.log ((0.081312 : ℝ) ^ (hull R).A) := by
    have := Real.log_le_log hpos hle; linarith
  rw [Real.log_pow] at hlog
  have hb : -Real.log (0.081312 : ℝ) < 2.5095 := by
    refine neg_log_lt _ _ 3 (by norm_num) (by norm_num) (by norm_num) (by norm_num) 15 (by norm_num) ?_ ?_
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
    · simp only [expSum, expErr, Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]; norm_num
  have hA' : (0 : ℝ) < (hull R).A := by exact_mod_cast hA
  nlinarith

end Gump.Dice
