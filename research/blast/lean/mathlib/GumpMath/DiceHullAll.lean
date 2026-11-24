/-
The weighted Theorem 1 on every hull face (added 2026-11-24, second task): ln τ < 2.2165 · A for `hull R`, every R.

`DiceBound3.lean` proves the weighted bound for any balanced face that passes the local check `wcheck`, and runs
both by the kernel for R ≤ 11. Here both are proved for every R: the hull's neighbour relation is symmetric with no
repetitions (`hull_count_symm`, from `Gump.nbrs_symm`), hence balanced; and every cell is of one of three types,
(degree, coins one layer in, coins two layers in) = (6, 2, 1) inside, (4, 2, 1) on an edge, (2, 2, 0) at a corner
(`hull_type`), so the local check reduces to the three types (`type_check`, decided by the kernel).
-/
import GumpMath.DiceBound3
import GumpMath.Threshold

namespace Gump.Dice
open Gump Finset Matrix

theorem hullCells_nodup (R : ℕ) : (hullCells R).Nodup := by
  unfold hullCells
  refine List.Nodup.filter _ ?_
  rw [List.nodup_flatMap]
  refine ⟨fun x _ => ?_, ?_⟩
  · refine (List.nodup_range).map ?_
    intro a b h
    simp only [Pt.mk.injEq] at h
    omega
  · refine List.Pairwise.imp_of_mem ?_ (List.nodup_range)
    intro a b _ _ hab
    simp only [Function.onFun]
    intro p hp hq
    simp only [List.mem_map, List.mem_range] at hp hq
    obtain ⟨y, _, rfl⟩ := hp
    obtain ⟨y', _, e⟩ := hq
    simp only [Pt.mk.injEq] at e
    omega

theorem count_filterMap {α : Type*} (g : α → Option ℕ) (j : ℕ) (l : List α) :
    (l.filterMap g).count j = l.countP fun q => g q == some j := by
  induction l with
  | nil => simp
  | cons a l ih =>
      rw [List.filterMap_cons, List.countP_cons]
      cases h : g a with
      | none => simp [ih]
      | some b =>
          rw [List.count_cons, ih]
          by_cases hb : b = j <;> simp [hb]

theorem idxOf?_nodup {l : List Pt} (hl : l.Nodup) {q : Pt} {j : ℕ} (hj : j < l.length) :
    l.idxOf? q = some j ↔ l[j] = q := by
  rw [List.idxOf?_eq_some_iff]
  constructor
  · rintro ⟨_, h, _⟩; exact h
  · intro h
    refine ⟨hj, h, fun k hk e => ?_⟩
    have := (List.Nodup.getElem_inj_iff hl).mp (e.trans h.symm)
    omega

theorem countP_eq_ind_nodup {l : List Pt} (hl : l.Nodup) (c : Pt) (C : Prop) [Decidable C] :
    l.countP (fun q => decide (C ∧ q = c)) = if C ∧ c ∈ l then 1 else 0 := by
  have hc : l.countP (fun q => decide (q = c)) = l.count c := by
    rw [List.count]; congr 1
  by_cases hC : C
  · simp only [hC, true_and]
    rw [hc]
    by_cases hm : c ∈ l
    · rw [if_pos hm]; exact List.count_eq_one_of_mem hl hm
    · rw [if_neg hm]; exact List.count_eq_zero_of_not_mem hm
  · simp [hC]

section degX
variable (x y z : ℤ) (h1 : 0 ≤ x) (h2 : 0 ≤ y) (h3 : 0 ≤ z)
include h1 h2 h3

theorem deg_X (hx : x % 2 = 1) (hy : y % 2 = 0) (hz : z % 2 = 0) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
      decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) = 2 + (if y = 0 then 0 else 2) + (if z = 0 then 0 else 2) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .X := by simp [Pt.axis, hx]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hy0 : y = 0 <;> by_cases hz0 : z = 0 <;>
    simp (disch := omega) only [hy0, hz0, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

theorem deg_Y (hx : x % 2 = 0) (hy : y % 2 = 1) (hz : z % 2 = 0) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
      decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) = 2 + (if x = 0 then 0 else 2) + (if z = 0 then 0 else 2) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Y := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hx0 : x = 0 <;> by_cases hz0 : z = 0 <;>
    simp (disch := omega) only [hx0, hz0, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

theorem deg_Z (hx : x % 2 = 0) (hy : y % 2 = 0) (hz : z % 2 = 1) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩) &&
      decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) = 2 + (if x = 0 then 0 else 2) + (if y = 0 then 0 else 2) := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Z := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hx0 : x = 0 <;> by_cases hy0 : y = 0 <;>
    simp (disch := omega) only [hx0, hy0, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

theorem m2_X (hx : x % 2 = 1) (hy : y % 2 = 0) (hz : z % 2 = 0) (R : ℕ) (h4 : x + y + z = R) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = if y = 0 ∧ z = 0 then 0 else 1 := by
  have hax : Pt.axis ⟨x, y, z⟩ = .X := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : y = 0 ∧ z = 0
  · obtain ⟨h5, h6⟩ := hc
    simp (disch := omega) only [h5, h6, and_self, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega
  · have hc' : y ≠ 0 ∨ z ≠ 0 := by tauto
    rw [if_neg hc]
    simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

theorem m2_Y (hx : x % 2 = 0) (hy : y % 2 = 1) (hz : z % 2 = 0) (R : ℕ) (h4 : x + y + z = R) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = if x = 0 ∧ z = 0 then 0 else 1 := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Y := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : x = 0 ∧ z = 0
  · obtain ⟨h5, h6⟩ := hc
    simp (disch := omega) only [h5, h6, and_self, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega
  · have hc' : x ≠ 0 ∨ z ≠ 0 := by tauto
    rw [if_neg hc]
    simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

theorem m2_Z (hx : x % 2 = 0) (hy : y % 2 = 0) (hz : z % 2 = 1) (R : ℕ) (h4 : x + y + z = R) :
    (nbrs ⟨x, y, z⟩).countP (fun q => decide (d111.dot q = d111.dot ⟨x, y, z⟩ - 4) &&
      decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) = if x = 0 ∧ y = 0 then 0 else 1 := by
  have hax : Pt.axis ⟨x, y, z⟩ = .Z := by simp [Pt.axis, hx, hy]
  simp only [nbrs, hax, offsets, List.map_cons, List.map_nil, List.countP_cons, List.countP_nil, d111, Diag.dot,
    sg, ite_true, Pt.add_x, Pt.add_y, Pt.add_z]
  by_cases hc : x = 0 ∧ y = 0
  · obtain ⟨h5, h6⟩ := hc
    simp (disch := omega) only [h5, h6, and_self, decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega
  · have hc' : x ≠ 0 ∨ y ≠ 0 := by tauto
    rw [if_neg hc]
    simp (disch := omega) only [decide_eq_true, decide_eq_false, Bool.and_true, Bool.and_false,
      Bool.false_and, ite_true, ite_false, Bool.false_eq_true] <;> omega

end degX

namespace Face

theorem hull_cell_mem (R i : ℕ) (hi : i < (hull R).A) : (hull R).cell i ∈ hullCells R := by
  unfold Face.cell; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]
  exact List.getElem_mem _

theorem hull_cell_eq (R i : ℕ) (hi : i < (hull R).A) : (hull R).cell i = (hullCells R)[i]'hi := by
  unfold Face.cell; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]; rfl

/-- The multiplicity of j among the neighbours of i: 1 if the two cells are in-layer neighbours, else 0. -/
theorem hull_count (R i j : ℕ) (hi : i < (hull R).A) (hj : j < (hull R).A) :
    ((hull R).nb i).count j = if d111.dot ((hull R).cell j) = d111.dot ((hull R).cell i) ∧
      (hull R).cell j ∈ nbrs ((hull R).cell i) then 1 else 0 := by
  have e : (hull R).nb i = (nbrs ((hull R).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((hull R).cell i) then (hullCells R).idxOf? q else none := rfl
  rw [e, count_filterMap]
  have hnd := hullCells_nodup R
  rw [← countP_eq_ind_nodup (Threshold.nbrs_nodup _) ((hull R).cell j)
    (d111.dot ((hull R).cell j) = d111.dot ((hull R).cell i))]
  refine List.countP_congr fun q _ => ?_
  have hj' : j < (hullCells R).length := hj
  by_cases hd : d111.dot q = d111.dot ((hull R).cell i)
  · simp only [hd, ite_true, beq_iff_eq, decide_eq_true_eq, idxOf?_nodup hnd hj', hull_cell_eq R j hj]
    constructor
    · intro h; exact ⟨h ▸ hd, h.symm⟩
    · rintro ⟨_, h⟩; exact h.symm
  · simp only [hd, ite_false, beq_iff_eq, reduceCtorEq, false_iff, decide_eq_true_eq, not_and]
    intro h1 h2; exact hd (h2 ▸ h1)

theorem hull_count_symm (R i j : ℕ) (hi : i < (hull R).A) (hj : j < (hull R).A) :
    ((hull R).nb i).count j = ((hull R).nb j).count i := by
  rw [hull_count R i j hi hj, hull_count R j i hj hi]
  have ci := ((mem_hullCells R _).mp (hull_cell_mem R i hi)).2.2.2.2
  have cj := ((mem_hullCells R _).mp (hull_cell_mem R j hj)).2.2.2.2
  have hs := nbrs_symm ci cj
  by_cases h : d111.dot ((hull R).cell j) = d111.dot ((hull R).cell i)
  · have h' : d111.dot ((hull R).cell i) = d111.dot ((hull R).cell j) := h.symm
    by_cases hm : (hull R).cell j ∈ nbrs ((hull R).cell i)
    · rw [if_pos ⟨h, hm⟩, if_pos ⟨h', hs.mp hm⟩]
    · rw [if_neg (fun e => hm e.2), if_neg (fun e => hm (hs.mpr e.2))]
  · have h' : ¬ d111.dot ((hull R).cell i) = d111.dot ((hull R).cell j) := fun e => h e.symm
    rw [if_neg (fun e => h e.1), if_neg (fun e => h' e.1)]

theorem hull_nb_lt (R i : ℕ) : ∀ j ∈ (hull R).nb i, j < (hull R).A := by
  intro j hj
  simp only [nb, List.mem_filterMap] at hj
  obtain ⟨q, _, hq⟩ := hj
  split at hq
  · exact (List.idxOf?_eq_some_iff.mp hq).1
  · cases hq

/-- **Every hull face is balanced.** -/
theorem hull_balanced (R : ℕ) : (hull R).balanced := by
  refine ⟨fun i _ => hull_nb_lt R i, fun j hj => ?_⟩
  rw [sum_congr rfl fun i hi => hull_count_symm R i j (mem_range.mp hi) hj]
  have := countP_eq_sum_count (hull R).A (fun _ => true) ((hull R).nb j) (hull_nb_lt R j)
  simp only [ite_true, List.countP_true] at this
  exact this.symm

theorem hull_deg_eq (R i : ℕ) (hi : i < (hull R).A) :
    ((hull R).nb i).length = (nbrs ((hull R).cell i)).countP (fun q => decide (d111.dot q = d111.dot ((hull R).cell i)) &&
      decide (0 ≤ q.x ∧ 0 ≤ q.y ∧ 0 ≤ q.z)) := by
  have e : (hull R).nb i = (nbrs ((hull R).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((hull R).cell i) then (hullCells R).idxOf? q else none := rfl
  rw [e, filterMap_length_countP]
  obtain ⟨h1, h2, h3, h4, hc⟩ := (mem_hullCells R _).mp (hull_cell_mem R i hi)
  refine List.countP_congr fun q hq => ?_
  by_cases hd : d111.dot q = d111.dot ((hull R).cell i)
  · simp only [hd, ite_true, List.isSome_idxOf?, mem_hullCells, decide_true, Bool.true_and, decide_eq_true_eq]
    have hcq := nbrs_isCell _ hc q hq
    have hs : q.x + q.y + q.z = R := by
      simp only [d111, Diag.dot, sg, ite_true] at hd; omega
    constructor
    · rintro ⟨a, b, c, -, -⟩; exact ⟨a, b, c⟩
    · rintro ⟨a, b, c⟩; exact ⟨a, b, c, hs, hcq⟩
  · simp [hd]

/-- **The three kinds of cell of every hull face**: (degree, m1, m2) is (6, 2, 1) inside, (4, 2, 1) on an edge,
(2, 2, 0) at a corner. -/
theorem hull_type (R i : ℕ) (hi : i < (hull R).A) :
    (((hull R).nb i).length, (hull R).m1 i, (hull R).m2 i) = (6, 2, 1) ∨
    (((hull R).nb i).length, (hull R).m1 i, (hull R).m2 i) = (4, 2, 1) ∨
    (((hull R).nb i).length, (hull R).m1 i, (hull R).m2 i) = (2, 2, 0) := by
  have hm1 := (hull_cells R i hi).1
  rw [hm1, hull_deg_eq R i hi]
  have e2 : (hull R).m2 i = (nbrs ((hull R).cell i)).countP (fun q => decide (d111.dot q =
      d111.dot ((hull R).cell i) - 4) && decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) := rfl
  rw [e2]
  obtain ⟨h1, h2, h3, h4, hc⟩ := (mem_hullCells R _).mp (hull_cell_mem R i hi)
  generalize (hull R).cell i = p at h1 h2 h3 h4 hc ⊢
  obtain ⟨x, y, z⟩ := p
  simp only at h1 h2 h3 h4
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hc
  have hpar : (x % 2 = 1 ∧ y % 2 = 0 ∧ z % 2 = 0) ∨ (x % 2 = 0 ∧ y % 2 = 1 ∧ z % 2 = 0) ∨
      (x % 2 = 0 ∧ y % 2 = 0 ∧ z % 2 = 1) := by omega
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · rw [deg_X x y z h1 h2 h3 hx hy hz, m2_X x y z h1 h2 h3 hx hy hz R h4]
    by_cases a : y = 0 <;> by_cases b : z = 0 <;> simp [a, b]
  · rw [deg_Y x y z h1 h2 h3 hx hy hz, m2_Y x y z h1 h2 h3 hx hy hz R h4]
    by_cases a : x = 0 <;> by_cases b : z = 0 <;> simp [a, b]
  · rw [deg_Z x y z h1 h2 h3 hx hy hz, m2_Z x y z h1 h2 h3 hx hy hz R h4]
    by_cases a : x = 0 <;> by_cases b : y = 0 <;> simp [a, b]

end Face

/-- The local check on the three kinds of cell (decided by the kernel). -/
theorem type_check (d m1 m2 : ℕ) (ht : (d, m1, m2) = (6, 2, 1) ∨ (d, m1, m2) = (4, 2, 1) ∨ (d, m1, m2) = (2, 2, 0)) :
    ∀ k ≤ d, ∀ s : Bool, deltaHull * (if s then 1 else wHull ^ k) ≤
      (1 - aliveProb ρ1 ρ2 m1 m2 k s) * (if s then wHull ^ (d - k) else 1) := by
  rcases ht with h | h | h <;> simp only [Prod.mk.injEq] at h <;> obtain ⟨rfl, rfl, rfl⟩ := h <;> decide +kernel

theorem hull_wcheck (R : ℕ) : (hull R).wcheck ρ1 ρ2 wHull deltaHull = true := by
  unfold Face.wcheck
  rw [List.all_eq_true]; intro i hi
  rw [List.all_eq_true]; intro k hk
  rw [List.all_eq_true]; intro s _
  have hi' : i < (hull R).A := List.mem_range.mp hi
  have hk' : k ≤ ((hull R).nb i).length := Nat.lt_succ_iff.mp (List.mem_range.mp hk)
  exact decide_eq_true (type_check _ _ _ (Face.hull_type R i hi') k hk' s)

/-- **The weighted Theorem 1 on every hull face**: for every R and every quasi-stationary law of `hull R` at
(0.44, 0.42), ln τ = -ln(1 - λ) < 2.2165 · A. -/
theorem lntau_le_hull_all (R : ℕ) (μ : Fin (2 ^ (hull R).A) → ℝ) (lam : ℝ) (hq : IsQSD (hull R) ρ1 ρ2 μ lam)
    (hA : 0 < (hull R).A) : -Real.log (1 - lam) < 2.2165 * (hull R).A :=
  lntau_le_hull_weighted R (Face.hull_balanced R) (hull_wcheck R) μ lam hq hA

end Gump.Dice
