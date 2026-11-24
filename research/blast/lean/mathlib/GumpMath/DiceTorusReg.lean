/-
`Face.regular` for every wrapped face `torus H K D` with H, D > 0 (added 2026-11-24, second task), so that
`lntau_le_regular` (ln τ < 1.9228 · A, `DiceBound2.lean`) holds on every wrapped face (`lntau_le_torus`).

The reduction `red` of a wrapped face is, in the cell coordinates (o, a, b) of `geom.py`, the map
Tr(a, b) = (a mod H, (b - ⌊a/H⌋ K) mod D): it is invariant under the period lattice (`Tr_shift`), differs from
the identity by a lattice vector (`Tr_sub`) and fixes the fundamental domain (`Tr_id`). Hence the neighbour
relation is symmetric: if the neighbour of cell i across the offset v reduces to cell j, the neighbour of j across
-v reduces to i (`red_symm`), and v ↦ -v matches the slots of i that land on j with those of j that land on i
(`torus_count_symm`). Every cell has six slots (the six in-layer offsets, every reduction is a cell), so every
cell is in six slots: `torus_regular`.
-/
import GumpMath.DiceDef
import Mathlib.Tactic.IntervalCases
import Gump.Symm
import GumpMath.DiceHullAll

namespace Gump.Dice
open Gump Finset

/-- the torus reduction in coordinates -/
def Tr (H K D : ℤ) (a b : ℤ) : ℤ × ℤ := (a % H, (b - a / H * K) % D)

theorem Tr_shift (H K D a b s t : ℤ) (hH : H ≠ 0) :
    Tr H K D (a + s * H) (b + s * K + t * D) = Tr H K D a b := by
  unfold Tr
  have e1 : (a + s * H) / H = a / H + s := by rw [Int.add_mul_ediv_right _ _ hH]
  rw [Int.add_mul_emod_self_right, e1]
  congr 1
  have : b + s * K + t * D - (a / H + s) * K = (b - a / H * K) + t * D := by ring
  rw [this, Int.add_mul_emod_self_right]

theorem Tr_sub (H K D a b : ℤ) :
    ∃ s t : ℤ, (a, b) = ((Tr H K D a b).1 + s * H, (Tr H K D a b).2 + s * K + t * D) := by
  refine ⟨a / H, (b - a / H * K) / D, ?_⟩
  unfold Tr
  simp only [Prod.mk.injEq]
  constructor
  · have := Int.emod_def a H; linarith [mul_comm H (a / H)]
  · have := Int.emod_def (b - a / H * K) D; linarith [mul_comm D ((b - a / H * K) / D)]

theorem Tr_id (H K D a b : ℤ) (ha : 0 ≤ a) (ha' : a < H) (hb : 0 ≤ b) (hb' : b < D) : Tr H K D a b = (a, b) := by
  unfold Tr
  have : a / H = 0 := Int.ediv_eq_zero_of_lt ha ha'
  rw [this, Int.emod_eq_of_lt ha ha']
  simp [Int.emod_eq_of_lt hb hb']

theorem axisIdx_abCell (o : ℕ) (ho : o < 3) (a b : ℤ) : axisIdx (abCell o a b) = o := by
  interval_cases o <;> simp [abCell, axisIdx, Pt.axis] <;> omega

theorem coordA_abCell (o : ℕ) (ho : o < 3) (a b : ℤ) : coordA (abCell o a b) = a := by
  have := axisIdx_abCell o ho a b
  interval_cases o <;> simp only [coordA, this] <;> simp [abCell] <;> omega

theorem coordB_abCell (o : ℕ) (ho : o < 3) (a b : ℤ) : coordB (abCell o a b) = b := by
  have := axisIdx_abCell o ho a b
  interval_cases o <;> simp only [coordB, this] <;> simp [abCell] <;> omega

def shift (a b : ℤ) : Pt := ⟨2 * a + 2 * b, -2 * a, -2 * b⟩
def negP (v : Pt) : Pt := ⟨-v.x, -v.y, -v.z⟩

theorem abCell_shift (o : ℕ) (a b : ℤ) : abCell o a b = abCell o 0 0 + shift a b := by
  match o with
  | 0 => apply Pt.ext' <;> simp [abCell, shift] <;> ring
  | 1 => apply Pt.ext' <;> simp [abCell, shift] <;> ring
  | n + 2 => apply Pt.ext' <;> simp [abCell, shift] <;> ring

theorem axis_add_shift (p : Pt) (a b : ℤ) : (p + shift a b).axis = p.axis := by
  obtain ⟨x, y, z⟩ := p
  simp only [Pt.axis, shift, Pt.add_x, Pt.add_y, Pt.add_z]
  have h1 : (x + (2 * a + 2 * b)) % 2 = x % 2 := by omega
  have h2 : (y + -2 * a) % 2 = y % 2 := by omega
  simp only [h1, h2]

theorem axisIdx_add_shift (p : Pt) (a b : ℤ) : axisIdx (p + shift a b) = axisIdx p := by
  unfold axisIdx; rw [axis_add_shift]

theorem coordA_add_shift (p : Pt) (a b : ℤ) : coordA (p + shift a b) = coordA p + a := by
  unfold coordA; rw [axisIdx_add_shift]; simp only [shift, Pt.add_y]; split <;> omega

theorem coordB_add_shift (p : Pt) (a b : ℤ) : coordB (p + shift a b) = coordB p + b := by
  unfold coordB; rw [axisIdx_add_shift]; simp only [shift, Pt.add_z]; split <;> omega

/-- A point of the layer x + y + z = 1 with exactly one odd coordinate is the cell of its coordinates. -/
theorem decode (p : Pt) (hs : p.x + p.y + p.z = 1) (hc : p.isCell = true) :
    p = abCell (axisIdx p) (coordA p) (coordB p) := by
  obtain ⟨x, y, z⟩ := p
  simp only at hs
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hc
  have hpar : (x % 2 = 1 ∧ y % 2 = 0 ∧ z % 2 = 0) ∨ (x % 2 = 0 ∧ y % 2 = 1 ∧ z % 2 = 0) ∨
      (x % 2 = 0 ∧ y % 2 = 0 ∧ z % 2 = 1) := by omega
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · have : axisIdx ⟨x, y, z⟩ = 0 := by simp [axisIdx, Pt.axis, hx]
    simp only [coordA, coordB, this]; simp [abCell]; omega
  · have : axisIdx ⟨x, y, z⟩ = 1 := by simp [axisIdx, Pt.axis, hx, hy]
    simp only [coordA, coordB, this]; simp [abCell]; omega
  · have : axisIdx ⟨x, y, z⟩ = 2 := by simp [axisIdx, Pt.axis, hx, hy]
    simp only [coordA, coordB, this]; simp [abCell]; omega

theorem torus_red (H K D : ℕ) (p : Pt) :
    (torus H K D).red p = abCell (axisIdx p) (Tr H K D (coordA p) (coordB p)).1 (Tr H K D (coordA p) (coordB p)).2 := rfl

/-- The offsets table, decided: for every orientation and in-layer offset v, the neighbour of the base cell is a
cell of the layer, and -v is an offset of its orientation. -/
theorem offsets_table : ∀ o < 3, ∀ v ∈ offsets (abCell o 0 0).axis, d111.dot v = 0 →
    (abCell o 0 0 + v).isCell = true ∧ (abCell o 0 0 + v).x + (abCell o 0 0 + v).y + (abCell o 0 0 + v).z = 1 ∧
    axisIdx (abCell o 0 0 + v) < 3 ∧ negP v ∈ offsets (abCell o 0 0 + v).axis := by
  decide +kernel

theorem abCell_inj (o o' : ℕ) (ho : o < 3) (ho' : o' < 3) (a b a' b' : ℤ) (h : abCell o a b = abCell o' a' b') :
    o = o' ∧ a = a' ∧ b = b' := by
  refine ⟨?_, ?_, ?_⟩
  · rw [← axisIdx_abCell o ho a b, ← axisIdx_abCell o' ho' a' b', h]
  · rw [← coordA_abCell o ho a b, ← coordA_abCell o' ho' a' b', h]
  · rw [← coordB_abCell o ho a b, ← coordB_abCell o' ho' a' b', h]

theorem add_shift_assoc (p q : Pt) (a b : ℤ) : p + shift a b + q = p + q + shift a b := by
  apply Pt.ext' <;> simp [shift] <;> ring

theorem shift_add (a b c d : ℤ) (p : Pt) : p + shift a b + shift c d = p + shift (a + c) (b + d) := by
  apply Pt.ext' <;> simp [shift] <;> ring

/-- **The symmetry of the torus's neighbour relation**, in the coordinates: if the neighbour of the cell (o,a,b)
across the in-layer offset v reduces to the cell (o_j, a_j, b_j), then the neighbour of the latter across -v reduces
to the former. -/
theorem red_symm (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (o : ℕ) (ho : o < 3) (a b : ℤ) (ha : 0 ≤ a) (ha' : a < H)
    (hb : 0 ≤ b) (hb' : b < D) (oj : ℕ) (hoj : oj < 3) (aj bj : ℤ)
    (v : Pt) (hv : v ∈ offsets (abCell o 0 0).axis) (hv0 : d111.dot v = 0)
    (h : (torus H K D).red (abCell o a b + v) = abCell oj aj bj) :
    (torus H K D).red (abCell oj aj bj + negP v) = abCell o a b := by
  obtain ⟨hc0, hs0, ho0, -⟩ := offsets_table o ho v hv hv0
  set q0 := abCell o 0 0 + v
  have hq0 := decode q0 hs0 hc0
  have e1 : abCell o a b + v = q0 + shift a b := by
    rw [abCell_shift o a b, add_shift_assoc]
  rw [e1, torus_red, axisIdx_add_shift, coordA_add_shift, coordB_add_shift] at h
  obtain ⟨h1, h2, h3⟩ := abCell_inj _ _ ho0 hoj _ _ _ _ h
  -- Tr (α + a, β + b) = (aj, bj)
  obtain ⟨s, t, hst⟩ := Tr_sub H K D (coordA q0 + a) (coordB q0 + b)
  have hT : Tr H K D (coordA q0 + a) (coordB q0 + b) = (aj, bj) := Prod.ext h2 h3
  rw [hT] at hst
  simp only [Prod.mk.injEq] at hst
  -- p_j + (-v) = abCell o 0 0 + shift (aj - α) (bj - β)
  have e2 : abCell oj aj bj + negP v = abCell o 0 0 + shift (aj - coordA q0) (bj - coordB q0) := by
    have : abCell oj aj bj = abCell (axisIdx q0) (coordA q0) (coordB q0) + shift (aj - coordA q0) (bj - coordB q0) := by
      rw [h1, abCell_shift oj (coordA q0), shift_add, ← abCell_shift]; congr 1 <;> ring
    rw [this, ← hq0]
    apply Pt.ext' <;> simp [q0, shift, negP] <;> ring
  rw [e2, torus_red, axisIdx_add_shift, coordA_add_shift, coordB_add_shift, axisIdx_abCell o ho,
    coordA_abCell o ho, coordB_abCell o ho]
  have hH' : (H : ℤ) ≠ 0 := by exact_mod_cast hH.ne'
  have : Tr H K D (0 + (aj - coordA q0)) (0 + (bj - coordB q0)) = Tr H K D (a + (-s) * H) (b + (-s) * K + (-t) * D) := by
    congr 1 <;> linarith
  rw [this, Tr_shift H K D a b (-s) (-t) hH', Tr_id H K D a b ha (by exact_mod_cast ha') hb (by exact_mod_cast hb')]

theorem mem_gridCells (W D : ℕ) (p : Pt) :
    p ∈ gridCells W D ↔ ∃ o < 3, ∃ a b : ℤ, 0 ≤ a ∧ a < W ∧ 0 ≤ b ∧ b < D ∧ p = abCell o a b := by
  unfold gridCells
  simp only [List.mem_flatMap, List.mem_map, List.mem_range]
  constructor
  · rintro ⟨a, ha, b, hb, o, ho, rfl⟩
    exact ⟨o, ho, a, b, by omega, by omega, by omega, by omega, rfl⟩
  · rintro ⟨o, ho, a, b, h1, h2, h3, h4, rfl⟩
    refine ⟨a.toNat, by omega, b.toNat, by omega, o, ho, ?_⟩
    congr 1 <;> omega

theorem gridCells_nodup (W D : ℕ) : (gridCells W D).Nodup := by
  unfold gridCells
  rw [List.nodup_flatMap]
  refine ⟨fun a _ => ?_, ?_⟩
  · rw [List.nodup_flatMap]
    refine ⟨fun b _ => (List.nodup_range).map_on fun o ho o' ho' e => ?_, ?_⟩
    · exact (abCell_inj o o' (List.mem_range.mp ho) (List.mem_range.mp ho') _ _ _ _ e).1
    · refine List.Pairwise.imp_of_mem ?_ (List.nodup_range)
      intro b b' _ _ hbb
      simp only [Function.onFun]
      intro p hp hq
      simp only [List.mem_map, List.mem_range] at hp hq
      obtain ⟨o, ho, rfl⟩ := hp
      obtain ⟨o', ho', e⟩ := hq
      have := (abCell_inj o' o ho' ho _ _ _ _ e).2.2
      omega
  · refine List.Pairwise.imp_of_mem ?_ (List.nodup_range)
    intro a a' _ _ haa
    simp only [Function.onFun]
    intro p hp hq
    simp only [List.mem_flatMap, List.mem_map, List.mem_range] at hp hq
    obtain ⟨b, hb, o, ho, rfl⟩ := hp
    obtain ⟨b', hb', o', ho', e⟩ := hq
    have := (abCell_inj o' o ho' ho _ _ _ _ e).2.1
    omega

theorem axisIdx_lt (p : Pt) : axisIdx p < 3 := by
  unfold axisIdx; split <;> omega

theorem red_mem (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (q : Pt) : (torus H K D).red q ∈ gridCells H D := by
  rw [torus_red, mem_gridCells]
  have hH' : (0 : ℤ) < H := by exact_mod_cast hH
  have hD' : (0 : ℤ) < D := by exact_mod_cast hD
  refine ⟨axisIdx q, axisIdx_lt q, _, _, Int.emod_nonneg _ hH'.ne', Int.emod_lt_of_pos _ hH',
    Int.emod_nonneg _ hD'.ne', Int.emod_lt_of_pos _ hD', rfl⟩

theorem axis_abCell (o : ℕ) (x y : ℤ) : (abCell o x y).axis = (abCell o 0 0).axis := by
  rw [abCell_shift, axis_add_shift]

theorem countP_inlayer (a : Axis) : (offsets a).countP (fun v => decide (d111.dot v = 0)) = 6 := by
  cases a <;> decide

namespace Face

theorem nb_lt' (F : Face) (i : ℕ) : ∀ j ∈ F.nb i, j < F.A := by
  intro j hj
  simp only [nb, List.mem_filterMap] at hj
  obtain ⟨q, _, hq⟩ := hj
  split at hq
  · exact (List.idxOf?_eq_some_iff.mp hq).1
  · cases hq

theorem torus_cell_mem (H K D i : ℕ) (hi : i < (torus H K D).A) : (torus H K D).cell i ∈ gridCells H D := by
  unfold Face.cell; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]
  exact List.getElem_mem _

theorem torus_cell_eq (H K D i : ℕ) (hi : i < (torus H K D).A) :
    (torus H K D).cell i = (gridCells H D)[i]'hi := by
  unfold Face.cell; rw [List.getD_eq_getElem?_getD, List.getElem?_eq_getElem hi]; rfl

theorem torus_count (H K D i j : ℕ) (hj : j < (torus H K D).A) :
    ((torus H K D).nb i).count j = (offsets ((torus H K D).cell i).axis).countP (fun v =>
      decide (d111.dot v = 0) && decide ((torus H K D).red ((torus H K D).cell i + v) = (torus H K D).cell j)) := by
  have e : (torus H K D).nb i = (nbrs ((torus H K D).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((torus H K D).cell i) then (gridCells H D).idxOf? ((torus H K D).red q) else none := rfl
  rw [e, count_filterMap, nbrs, List.countP_map]
  refine List.countP_congr fun v _ => ?_
  have hj' : j < (gridCells H D).length := hj
  simp only [Function.comp, Diag.dot_add, add_eq_left]
  by_cases hd : d111.dot v = 0
  · simp only [hd, ite_true, beq_iff_eq, decide_true, Bool.true_and, decide_eq_true_eq,
      idxOf?_nodup (gridCells_nodup H D) hj', torus_cell_eq H K D j hj]
    exact eq_comm
  · simp [hd]

theorem torus_count_symm (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (i j : ℕ) (hi : i < (torus H K D).A)
    (hj : j < (torus H K D).A) : ((torus H K D).nb i).count j = ((torus H K D).nb j).count i := by
  rw [torus_count H K D i j hj, torus_count H K D j i hi, List.countP_eq_length_filter, List.countP_eq_length_filter]
  obtain ⟨o, ho, a, b, ha, ha', hb, hb', hpi⟩ := (mem_gridCells H D _).mp (torus_cell_mem H K D i hi)
  obtain ⟨o', ho', a', b', ha2, ha2', hb2, hb2', hpj⟩ := (mem_gridCells H D _).mp (torus_cell_mem H K D j hj)
  rw [hpi, hpj]
  -- the map v ↦ -v sends each filtered list into the other
  have key : ∀ (o : ℕ) (ho : o < 3) (a b : ℤ) (ha : 0 ≤ a) (ha' : a < H) (hb : 0 ≤ b) (hb' : b < D)
      (o' : ℕ) (ho' : o' < 3) (a' b' : ℤ) (ha2 : 0 ≤ a') (ha2' : a' < H) (hb2 : 0 ≤ b') (hb2' : b' < D),
      ∀ v ∈ (offsets (abCell o a b).axis).filter (fun v => decide (d111.dot v = 0) &&
        decide ((torus H K D).red (abCell o a b + v) = abCell o' a' b')),
      negP v ∈ (offsets (abCell o' a' b').axis).filter (fun v => decide (d111.dot v = 0) &&
        decide ((torus H K D).red (abCell o' a' b' + v) = abCell o a b)) := by
    intro o ho a b ha ha' hb hb' o' ho' a' b' ha2 ha2' hb2 hb2' v hv
    simp only [List.mem_filter, Bool.and_eq_true, decide_eq_true_eq] at hv ⊢
    obtain ⟨hvo, hv0, hred⟩ := hv
    rw [axis_abCell] at hvo
    obtain ⟨hc0, hs0, ho0, hneg⟩ := offsets_table o ho v hvo hv0
    have hq0 := decode _ hs0 hc0
    refine ⟨?_, ?_, red_symm H K D hH hD o ho a b ha ha' hb hb' o' ho' a' b' v hvo hv0 hred⟩
    · -- the orientation of the target is that of abCell o 0 0 + v
      have e1 : abCell o a b + v = (abCell o 0 0 + v) + shift a b := by rw [abCell_shift o a b, add_shift_assoc]
      rw [e1, torus_red, axisIdx_add_shift] at hred
      have : (abCell o' a' b').axis = (abCell o 0 0 + v).axis := by
        rw [← hred, axis_abCell]
        conv_rhs => rw [hq0]
        exact (axis_abCell _ _ _).symm
      rw [this]; exact hneg
    · simp [negP, d111, Diag.dot, sg] at hv0 ⊢; omega
  have hn : ∀ (l : List Pt), l.Nodup → (l.map negP).Nodup := fun l hl =>
    hl.map fun p q e => by
      apply Pt.ext' <;> simp only [negP, Pt.mk.injEq] at e <;> omega
  have hnd : ∀ (o : ℕ) (x y : ℤ) (P : Pt → Bool), ((offsets (abCell o x y).axis).filter P).Nodup :=
    fun o x y P => (offsets_nodup _).filter _
  apply le_antisymm
  · have := ((hn _ (hnd o a b _)).subperm fun w hw => by
      obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hw
      exact key o ho a b ha ha' hb hb' o' ho' a' b' ha2 ha2' hb2 hb2' v hv).length_le
    simpa using this
  · have := ((hn _ (hnd o' a' b' _)).subperm fun w hw => by
      obtain ⟨v, hv, rfl⟩ := List.mem_map.mp hw
      exact key o' ho' a' b' ha2 ha2' hb2 hb2' o ho a b ha ha' hb hb' v hv).length_le
    simpa using this

/-- **Every wrapped face is regular** (H, D > 0). -/
theorem torus_regular (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) : (torus H K D).regular := by
  have hlen : ∀ i < (torus H K D).A, ((torus H K D).nb i).length = 6 := by
    intro i _
    have e : (torus H K D).nb i = (nbrs ((torus H K D).cell i)).filterMap fun q =>
        if d111.dot q = d111.dot ((torus H K D).cell i) then (gridCells H D).idxOf? ((torus H K D).red q) else none := rfl
    rw [e, filterMap_length_countP, nbrs, List.countP_map, ← countP_inlayer ((torus H K D).cell i).axis]
    refine List.countP_congr fun v _ => ?_
    simp only [Function.comp, Diag.dot_add, add_eq_left]
    by_cases hd : d111.dot v = 0
    · simp [hd, red_mem H K D hH hD]
    · simp [hd]
  refine ⟨hlen, fun i _ => nb_lt' _ i, fun j hj => ?_⟩
  rw [sum_congr rfl fun i hi => torus_count_symm H K D hH hD i j (Finset.mem_range.mp hi) hj]
  have := countP_eq_sum_count (torus H K D).A (fun _ => true) ((torus H K D).nb j) (nb_lt' _ j)
  simp only [ite_true, List.countP_true] at this
  rw [← this, hlen j hj]

end Face

/-- **ln τ < 1.9228 · A on every wrapped face** (H, D > 0), for every quasi-stationary law at (0.44, 0.42). -/
theorem lntau_le_torus (H K D : ℕ) (hH : 0 < H) (hD : 0 < D) (μ : Fin (2 ^ (torus H K D).A) → ℝ) (lam : ℝ)
    (hq : IsQSD (torus H K D) ρ1 ρ2 μ lam) (hA : 0 < (torus H K D).A) :
    -Real.log (1 - lam) < 1.9228 * (torus H K D).A :=
  lntau_le_regular (torus H K D) (fun _ => rfl) (Face.torus_regular H K D hH hD) μ lam hq hA

end Gump.Dice
