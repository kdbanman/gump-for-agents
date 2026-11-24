/-
**Lemma 0 on every hull face, by a general proof** (`hull_lemma0`), so that `hull_full_all` and `hull_full_sym`
hold with no hypothesis (`hull_full_every`).

The construction is the certificate of `link_hull_cert.py`, written out in the hull's coordinates (x, y, z ≥ 0,
x + y + z = R, one coordinate odd: the cell's normal). States are written as masks of point sets (`mask`), and
`k_mask` reads the number of live neighbours of a cell off its six in-layer neighbours (`kc`).
* u = every cell whose normal is not z; every cell can be alive next from it (`aliveF_u`).
* T = the x- and y-cells that are not corners; φ = 3(R - 1 - z) + [stuck], stuck = an x-cell with y = 0 or a
  y-cell with x = 0 below the top row. Every cell of T but the base c0 = (0, 1, R - 1) has a neighbour in T of
  smaller φ (`descent`). Hence a lone live cell walks to c0 (`walk`), and {c0} grows through the sublevel sets of φ
  to T (`grow`; no z-cell alive keeps every k ≤ 4, `kc_le_four`).
* T, then T with the two z-cells beside the x- and y-corners, then u (`last_steps`).
-/
import GumpMath.LinkHullCert

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace Gump.Link.HullGen
open Gump Gump.Dice Gump.Link Finset

variable (R : ℕ)

/-! ### Masks of point sets -/

section Mask
variable (S : Pt → Prop) [DecidablePred S]

/-- The state whose live cells are the cells of the hull in S. -/
noncomputable def maskF : Fin (2 ^ (Gump.Dice.hull R).A) :=
  (Equiv.ofBijective (Wrapped.E (Gump.Dice.hull R) (Equiv.refl _)) (Wrapped.E_bij _ _)).symm
    (univ.filter fun j : Fin (Gump.Dice.hull R).A => S ((Gump.Dice.hull R).cell j))

noncomputable def mask : ℕ := maskF R S

theorem mask_lt : mask R S < 2 ^ (Gump.Dice.hull R).A := (maskF R S).2

theorem mask_bit (j : ℕ) (hj : j < (Gump.Dice.hull R).A) :
    (mask R S).testBit j = decide (S ((Gump.Dice.hull R).cell j)) := by
  have h := Wrapped.mem_E (Gump.Dice.hull R) (Equiv.refl _) (maskF R S) ⟨j, hj⟩
  have e : Wrapped.E (Gump.Dice.hull R) (Equiv.refl _) (maskF R S) =
      univ.filter fun j : Fin (Gump.Dice.hull R).A => S ((Gump.Dice.hull R).cell j) := by
    unfold maskF
    exact Equiv.ofBijective_apply_symm_apply _ _ _
  rw [e] at h
  simp only [Equiv.refl_apply, mem_filter, mem_univ, true_and] at h
  unfold mask
  by_cases hs : S ((Gump.Dice.hull R).cell j)
  · rw [decide_eq_true hs]; exact h.1 hs
  · rw [decide_eq_false hs]
    cases hb : ((maskF R S : Fin _) : ℕ).testBit j
    · rfl
    · exact absurd (h.2 hb) hs

theorem mask_bit_high (j : ℕ) (hj : (Gump.Dice.hull R).A ≤ j) : (mask R S).testBit j = false :=
  Wrapped.high_bits _ (maskF R S) j hj

theorem mask_ne_zero (h : ∃ j < (Gump.Dice.hull R).A, S ((Gump.Dice.hull R).cell j)) : mask R S ≠ 0 := by
  obtain ⟨j, hj, hs⟩ := h
  intro e
  have := mask_bit R S j hj
  rw [e, Nat.zero_testBit, decide_eq_true hs] at this
  exact Bool.false_ne_true this

theorem mask_congr (S' : Pt → Prop) [DecidablePred S']
    (h : ∀ p ∈ Gump.Dice.hullCells R, S p ↔ S' p) : mask R S = mask R S' := by
  apply Nat.eq_of_testBit_eq
  intro j
  by_cases hj : j < (Gump.Dice.hull R).A
  · rw [mask_bit R S j hj, mask_bit R S' j hj]
    exact decide_eq_decide.mpr (h _ (Face.hull_cell_mem R j hj))
  · rw [mask_bit_high R S j (by omega), mask_bit_high R S' j (by omega)]

end Mask

theorem cell_inj {i j : ℕ} (hi : i < (Gump.Dice.hull R).A) (hj : j < (Gump.Dice.hull R).A)
    (h : (Gump.Dice.hull R).cell i = (Gump.Dice.hull R).cell j) : i = j := by
  rw [Face.hull_cell_eq R i hi, Face.hull_cell_eq R j hj] at h
  exact (List.Nodup.getElem_inj_iff (Gump.Dice.hullCells_nodup R)).1 h

theorem exists_idx (p : Pt) (hp : p ∈ Gump.Dice.hullCells R) : ∃ j < (Gump.Dice.hull R).A, (Gump.Dice.hull R).cell j = p := by
  obtain ⟨j, hj, e⟩ := List.getElem_of_mem hp
  exact ⟨j, hj, by rw [Face.hull_cell_eq R j hj]; exact e⟩

theorem single_eq (j : ℕ) (hj : j < (Gump.Dice.hull R).A) :
    2 ^ j = mask R (fun p => p = (Gump.Dice.hull R).cell j) := by
  apply Nat.eq_of_testBit_eq
  intro i
  rw [Nat.testBit_two_pow]
  by_cases hi : i < (Gump.Dice.hull R).A
  · rw [mask_bit R _ i hi]
    by_cases e : j = i
    · subst e; simp
    · have : (Gump.Dice.hull R).cell i ≠ (Gump.Dice.hull R).cell j := fun h => e (cell_inj R hj hi h.symm)
      simp [e, this]
  · rw [mask_bit_high R _ i (by omega)]
    have : j ≠ i := by omega
    simp [this]

/-! ### The number of live neighbours, in coordinates -/

/-- The live in-layer neighbours of p in the hull, for the live set S. -/
def kc (S : Pt → Prop) [DecidablePred S] (p : Pt) : ℕ :=
  (nbrs p).countP fun q => decide (d111.dot q = d111.dot p) && decide (q ∈ Gump.Dice.hullCells R ∧ S q)

theorem countP_filterMap' {α β : Type*} (g : α → Option β) (P : β → Bool) (l : List α) :
    (l.filterMap g).countP P = l.countP fun a => match g a with | some b => P b | none => false := by
  induction l with
  | nil => simp
  | cons a l ih =>
      rw [List.filterMap_cons, List.countP_cons]
      cases h : g a with
      | none => simp [ih, h]
      | some b => simp [ih, h, List.countP_cons]

theorem k_mask (S : Pt → Prop) [DecidablePred S] (i : ℕ) (hi : i < (Gump.Dice.hull R).A) :
    (Gump.Dice.hull R).k (mask R S) i = kc R S ((Gump.Dice.hull R).cell i) := by
  unfold Face.k
  rw [List.countP_congr (q := fun j => decide (S ((Gump.Dice.hull R).cell j))) (fun j hj => by
    rw [mask_bit R S j (Face.hull_nb_lt R i j hj)])]
  have e : (Gump.Dice.hull R).nb i = (nbrs ((Gump.Dice.hull R).cell i)).filterMap fun q =>
      if d111.dot q = d111.dot ((Gump.Dice.hull R).cell i) then (Gump.Dice.hullCells R).idxOf? q else none := rfl
  rw [e, countP_filterMap']
  unfold kc
  refine List.countP_congr fun q _ => ?_
  by_cases hd : d111.dot q = d111.dot ((Gump.Dice.hull R).cell i)
  · simp only [hd, ite_true, decide_true, Bool.true_and]
    by_cases hm : q ∈ Gump.Dice.hullCells R
    · obtain ⟨j, hj, hji⟩ := List.getElem_of_mem hm
      have hidx : (Gump.Dice.hullCells R).idxOf? q = some j := (idxOf?_nodup (Gump.Dice.hullCells_nodup R) hj).2 hji
      have hc : (Gump.Dice.hull R).cell j = q := by rw [Face.hull_cell_eq R j hj]; exact hji
      rw [hidx]
      simp [hc, hm]
    · have hidx : (Gump.Dice.hullCells R).idxOf? q = none := by
        rw [List.idxOf?_eq_none_iff]; exact hm
      rw [hidx]
      simp [hm]
  · simp [hd]

/-- A corner of the triangle: two coordinates zero. -/
def corner (p : Pt) : Prop := (p.y = 0 ∧ p.z = 0) ∨ (p.x = 0 ∧ p.z = 0) ∨ (p.x = 0 ∧ p.y = 0)

instance : DecidablePred corner := fun p => by unfold corner; infer_instance

theorem parity (p : Pt) (hp : p ∈ Gump.Dice.hullCells R) :
    0 ≤ p.x ∧ 0 ≤ p.y ∧ 0 ≤ p.z ∧ p.x + p.y + p.z = R ∧
      ((p.x % 2 = 1 ∧ p.y % 2 = 0 ∧ p.z % 2 = 0) ∨ (p.x % 2 = 0 ∧ p.y % 2 = 1 ∧ p.z % 2 = 0) ∨
        (p.x % 2 = 0 ∧ p.y % 2 = 0 ∧ p.z % 2 = 1)) := by
  obtain ⟨h1, h2, h3, h4, hc⟩ := (Gump.Dice.mem_hullCells R p).mp hp
  refine ⟨h1, h2, h3, h4, ?_⟩
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq] at hc
  omega

theorem m2_eq (i : ℕ) (hi : i < (Gump.Dice.hull R).A) :
    (Gump.Dice.hull R).m2 i = if corner ((Gump.Dice.hull R).cell i) then 0 else 1 := by
  have e2 : (Gump.Dice.hull R).m2 i = (nbrs ((Gump.Dice.hull R).cell i)).countP (fun q => decide (d111.dot q =
      d111.dot ((Gump.Dice.hull R).cell i) - 4) && decide (q.x.natAbs + q.y.natAbs + q.z.natAbs ≤ R)) := rfl
  rw [e2]
  obtain ⟨h1, h2, h3, h4, hpar⟩ := parity R _ (Face.hull_cell_mem R i hi)
  generalize (Gump.Dice.hull R).cell i = p at h1 h2 h3 h4 hpar ⊢
  obtain ⟨x, y, z⟩ := p
  simp only at h1 h2 h3 h4 hpar
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · rw [m2_X x y z h1 h2 h3 hx hy hz R h4]
    by_cases hc : y = 0 ∧ z = 0
    · rw [if_pos hc, if_pos (show corner ⟨x, y, z⟩ from Or.inl hc)]
    · rw [if_neg hc, if_neg (show ¬ corner ⟨x, y, z⟩ by simp only [corner]; omega)]
  · rw [m2_Y x y z h1 h2 h3 hx hy hz R h4]
    by_cases hc : x = 0 ∧ z = 0
    · rw [if_pos hc, if_pos (show corner ⟨x, y, z⟩ from Or.inr (Or.inl hc))]
    · rw [if_neg hc, if_neg (show ¬ corner ⟨x, y, z⟩ by simp only [corner]; omega)]
  · rw [m2_Z x y z h1 h2 h3 hx hy hz R h4]
    by_cases hc : x = 0 ∧ y = 0
    · rw [if_pos hc, if_pos (show corner ⟨x, y, z⟩ from Or.inr (Or.inr hc))]
    · rw [if_neg hc, if_neg (show ¬ corner ⟨x, y, z⟩ by simp only [corner]; omega)]

theorem aliveF_mask (S : Pt → Prop) [DecidablePred S] (i : ℕ) (hi : i < (Gump.Dice.hull R).A) :
    aliveF (Gump.Dice.hull R) (mask R S) i =
      canB 2 (if corner ((Gump.Dice.hull R).cell i) then 0 else 1) (kc R S ((Gump.Dice.hull R).cell i))
        (decide (S ((Gump.Dice.hull R).cell i))) := by
  unfold aliveF
  rw [(Gump.Dice.hull_cells R i hi).1, m2_eq R i hi, k_mask R S i hi, mask_bit R S i hi]

/-- **A possible transition between masks**, checked cell by cell in coordinates. -/
theorem stepN_mask (S S' : Pt → Prop) [DecidablePred S] [DecidablePred S']
    (hne : ∃ p ∈ Gump.Dice.hullCells R, S' p)
    (h : ∀ p ∈ Gump.Dice.hullCells R, S' p → canB 2 (if corner p then 0 else 1) (kc R S p) (decide (S p)) = true) :
    StepN (Gump.Dice.hull R) (mask R S) (mask R S') := by
  refine ⟨mask_lt R S', mask_ne_zero R S' ?_, ?_⟩
  · obtain ⟨p, hp, hs⟩ := hne
    obtain ⟨j, hj, e⟩ := exists_idx R p hp
    exact ⟨j, hj, e ▸ hs⟩
  · simp only [stepF, List.all_eq_true, List.mem_range]
    intro i hi
    rw [mask_bit R S' i hi, aliveF_mask R S i hi]
    by_cases hs : S' ((Gump.Dice.hull R).cell i)
    · rw [h _ (Face.hull_cell_mem R i hi) hs, Bool.or_true]
    · simp [hs]


/-! ### The six in-layer neighbours -/

theorem mk_add_mk (a b c d e f : ℤ) : (⟨a, b, c⟩ : Pt) + ⟨d, e, f⟩ = ⟨a + d, b + e, c + f⟩ := rfl

/-- The in-layer offsets of a cell with the given normal. -/
def inl (a : Axis) : List Pt := (offsets a).filter fun v => decide (d111.dot v = 0)

theorem inl_X : inl .X = [⟨0, 2, -2⟩, ⟨0, -2, 2⟩, ⟨1, -1, 0⟩, ⟨-1, 1, 0⟩, ⟨1, 0, -1⟩, ⟨-1, 0, 1⟩] := by decide
theorem inl_Y : inl .Y = [⟨2, 0, -2⟩, ⟨-2, 0, 2⟩, ⟨-1, 1, 0⟩, ⟨1, -1, 0⟩, ⟨0, 1, -1⟩, ⟨0, -1, 1⟩] := by decide
theorem inl_Z : inl .Z = [⟨2, -2, 0⟩, ⟨-2, 2, 0⟩, ⟨-1, 0, 1⟩, ⟨1, 0, -1⟩, ⟨0, -1, 1⟩, ⟨0, 1, -1⟩] := by decide

theorem kc_eq (S : Pt → Prop) [DecidablePred S] (p : Pt) :
    kc R S p = (inl p.axis).countP fun v => decide (p + v ∈ Gump.Dice.hullCells R ∧ S (p + v)) := by
  unfold kc nbrs inl
  rw [List.countP_map, List.countP_filter]
  refine List.countP_congr fun v _ => ?_
  simp only [Function.comp, Diag.dot_add, add_eq_left, Bool.and_eq_true, decide_eq_true_eq]
  exact and_comm

theorem axis_X (x y z : ℤ) (hx : x % 2 = 1) : Pt.axis ⟨x, y, z⟩ = .X := by simp [Pt.axis, hx]
theorem axis_Y (x y z : ℤ) (hx : x % 2 = 0) (hy : y % 2 = 1) : Pt.axis ⟨x, y, z⟩ = .Y := by simp [Pt.axis, hx, hy]
theorem axis_Z (x y z : ℤ) (hx : x % 2 = 0) (hy : y % 2 = 0) : Pt.axis ⟨x, y, z⟩ = .Z := by
  simp [Pt.axis, hx, hy]

theorem axX (q : Pt) (h : q.x % 2 = 1) : q.axis = .X := by obtain ⟨a, b, c⟩ := q; exact axis_X a b c h
theorem axY (q : Pt) (hx : q.x % 2 = 0) (hy : q.y % 2 = 1) : q.axis = .Y := by
  obtain ⟨a, b, c⟩ := q; exact axis_Y a b c hx hy

/-- **No z-cell alive: at most four live neighbours.** -/
theorem kc_le_four (S : Pt → Prop) [DecidablePred S] (hS : ∀ q, S q → q.z % 2 = 0) (p : Pt)
    (hp : p ∈ Gump.Dice.hullCells R) : kc R S p ≤ 4 := by
  rw [kc_eq]
  have hmono : (inl p.axis).countP (fun v => decide (p + v ∈ Gump.Dice.hullCells R ∧ S (p + v))) ≤
      (inl p.axis).countP (fun v => decide ((p.z + v.z) % 2 = 0)) :=
    List.countP_mono_left fun v _ h => by
      simp only [decide_eq_true_eq] at h ⊢
      exact hS _ h.2
  refine hmono.trans ?_
  obtain ⟨-, -, -, -, hpar⟩ := parity R p hp
  obtain ⟨x, y, z⟩ := p
  simp only at hpar
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · rw [axis_X x y z hx, inl_X]
    simp only [List.countP_cons, List.countP_nil, decide_eq_true_eq]
    split_ifs <;> omega
  · rw [axis_Y x y z hx hy, inl_Y]
    simp only [List.countP_cons, List.countP_nil, decide_eq_true_eq]
    split_ifs <;> omega
  · rw [axis_Z x y z hx hy, inl_Z]
    simp only [List.countP_cons, List.countP_nil, decide_eq_true_eq]
    split_ifs <;> omega

/-- **One live cell: at most one live neighbour.** -/
theorem kc_le_one (c p : Pt) : kc R (fun q => q = c) p ≤ 1 := by
  rw [kc_eq]
  have hmono : (inl p.axis).countP (fun v => decide (p + v ∈ Gump.Dice.hullCells R ∧ p + v = c)) ≤
      (inl p.axis).countP (fun v => decide (p + v = c)) :=
    List.countP_mono_left fun v _ h => by
      simp only [decide_eq_true_eq] at h ⊢
      exact h.2
  refine hmono.trans ?_
  obtain ⟨x, y, z⟩ := p
  obtain ⟨a, b, d⟩ := c
  cases Pt.axis ⟨x, y, z⟩ <;>
  · simp only [inl_X, inl_Y, inl_Z, List.countP_cons, List.countP_nil, decide_eq_true_eq, mk_add_mk, Pt.mk.injEq]
    split_ifs <;> omega

/-- A live in-layer neighbour in the hull gives k ≥ 1. -/
theorem kc_pos (S : Pt → Prop) [DecidablePred S] (p v : Pt) (hv : v ∈ inl p.axis)
    (hm : p + v ∈ Gump.Dice.hullCells R) (hs : S (p + v)) : 1 ≤ kc R S p := by
  rw [kc_eq]
  exact List.countP_pos_iff.2 ⟨v, hv, by simp [hm, hs]⟩


/-! ### The growth region, its potential and the descent -/

/-- The x- and y-cells that are not corners. -/
def T (q : Pt) : Prop := q.z % 2 = 0 ∧ ¬ corner q

instance : DecidablePred T := fun q => by unfold T; infer_instance

/-- An x-cell on the edge y = 0, or a y-cell on the edge x = 0 below the top row. -/
def stuck (q : Pt) : Prop := (q.x % 2 = 1 ∧ q.y = 0) ∨ (q.y % 2 = 1 ∧ q.x = 0 ∧ q.z ≠ (R : ℤ) - 1)

instance : DecidablePred (stuck R) := fun q => by unfold stuck; infer_instance

/-- The potential: three per two layers below the top, one more if stuck. -/
def phi (q : Pt) : ℤ := 3 * ((R : ℤ) - 1 - q.z) + if stuck R q then 1 else 0

/-- The base cell, the y-cell of the top row. -/
def c0 : Pt := ⟨0, 1, (R : ℤ) - 1⟩

def G (n : ℕ) (q : Pt) : Prop := T q ∧ phi R q ≤ n

instance (n : ℕ) : DecidablePred (G R n) := fun q => by unfold G; infer_instance

theorem mem_hull_iff (x y z : ℤ) : (⟨x, y, z⟩ : Pt) ∈ Gump.Dice.hullCells R ↔
    0 ≤ x ∧ 0 ≤ y ∧ 0 ≤ z ∧ x + y + z = R ∧
      ((x % 2 = 1 ∧ y % 2 = 0 ∧ z % 2 = 0) ∨ (x % 2 = 0 ∧ y % 2 = 1 ∧ z % 2 = 0) ∨
        (x % 2 = 0 ∧ y % 2 = 0 ∧ z % 2 = 1)) := by
  rw [Gump.Dice.mem_hullCells]
  simp only [Pt.isCell, Bool.or_eq_true, Bool.and_eq_true, bne_iff_ne, ne_eq, beq_iff_eq]
  constructor
  · rintro ⟨h1, h2, h3, h4, h5⟩; exact ⟨h1, h2, h3, h4, by omega⟩
  · rintro ⟨h1, h2, h3, h4, h5⟩; exact ⟨h1, h2, h3, h4, by omega⟩

theorem c0_mem (hR : 3 ≤ R) (hodd : R % 2 = 1) : c0 R ∈ Gump.Dice.hullCells R := by
  unfold c0; rw [mem_hull_iff]; omega

theorem c0_T (hR : 3 ≤ R) (hodd : R % 2 = 1) : T (c0 R) := by
  unfold T c0 corner; simp only; omega

theorem phi_c0 : phi R (c0 R) = 0 := by
  unfold phi c0 stuck; simp

theorem phi_zero (hodd : R % 2 = 1) (q : Pt) (hq : q ∈ Gump.Dice.hullCells R) (hT : T q) (h : phi R q ≤ 0) :
    q = c0 R := by
  obtain ⟨x, y, z⟩ := q
  rw [mem_hull_iff] at hq
  unfold T corner at hT
  unfold phi stuck at h
  unfold c0
  simp only at hT h
  rw [Pt.mk.injEq]
  split_ifs at h <;> omega

theorem phi_le (q : Pt) (hq : q ∈ Gump.Dice.hullCells R) : phi R q ≤ 3 * R := by
  obtain ⟨x, y, z⟩ := q
  rw [mem_hull_iff] at hq
  unfold phi; split_ifs <;> simp only <;> omega

/-- **The descent**: every cell of T but c0 has an in-layer neighbour in T of smaller potential (and is an
in-layer neighbour of it). -/
theorem descent (hR : 3 ≤ R) (p : Pt) (hp : p ∈ Gump.Dice.hullCells R) (hT : T p) (hne : p ≠ c0 R) :
    ∃ v ∈ inl p.axis, p + v ∈ Gump.Dice.hullCells R ∧ T (p + v) ∧ phi R (p + v) < phi R p ∧
      ∃ w ∈ inl (p + v).axis, p + v + w = p := by
  obtain ⟨x, y, z⟩ := p
  have hm := hp
  rw [mem_hull_iff] at hm
  unfold T corner at hT
  unfold c0 at hne
  simp only [ne_eq, Pt.mk.injEq] at hT hne
  obtain ⟨h1, h2, h3, h4, hpar⟩ := hm
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · rw [axis_X x y z hx, inl_X]
    by_cases hy2 : 2 ≤ y
    · refine ⟨⟨0, -2, 2⟩, by simp, ?_, ?_, ?_, ⟨0, 2, -2⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [mk_add_mk]; unfold phi stuck; simp only; split_ifs <;> omega
      · rw [axX (⟨x, y, z⟩ + ⟨0, -2, 2⟩) (by simp only [Pt.add_x]; omega), inl_X]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
    · refine ⟨⟨-1, 1, 0⟩, by simp, ?_, ?_, ?_, ⟨1, -1, 0⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [mk_add_mk]; unfold phi stuck; simp only; split_ifs <;> omega
      · rw [axY (⟨x, y, z⟩ + ⟨-1, 1, 0⟩) (by simp only [Pt.add_x]; omega) (by simp only [Pt.add_y]; omega), inl_Y]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  · rw [axis_Y x y z hx hy, inl_Y]
    by_cases hx2 : 2 ≤ x
    · refine ⟨⟨-2, 0, 2⟩, by simp, ?_, ?_, ?_, ⟨2, 0, -2⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [mk_add_mk]; unfold phi stuck; simp only; split_ifs <;> omega
      · rw [axY (⟨x, y, z⟩ + ⟨-2, 0, 2⟩) (by simp only [Pt.add_x]; omega) (by simp only [Pt.add_y]; omega), inl_Y]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
    · refine ⟨⟨1, -1, 0⟩, by simp, ?_, ?_, ?_, ⟨-1, 1, 0⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [mk_add_mk]; unfold phi stuck; simp only; split_ifs <;> omega
      · rw [axX (⟨x, y, z⟩ + ⟨1, -1, 0⟩) (by simp only [Pt.add_x]; omega), inl_X]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  · omega

/-- **Into T**: every cell outside T (a z-cell or a corner) has an in-layer neighbour in T. -/
theorem enterT (hR : 3 ≤ R) (p : Pt) (hp : p ∈ Gump.Dice.hullCells R) (hT : ¬ T p) :
    ∃ v ∈ inl p.axis, p + v ∈ Gump.Dice.hullCells R ∧ T (p + v) ∧ ∃ w ∈ inl (p + v).axis, p + v + w = p := by
  obtain ⟨x, y, z⟩ := p
  have hm := hp
  rw [mem_hull_iff] at hm
  unfold T corner at hT
  simp only at hT
  obtain ⟨h1, h2, h3, h4, hpar⟩ := hm
  rcases hpar with ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩ | ⟨hx, hy, hz⟩
  · rw [axis_X x y z hx, inl_X]
    refine ⟨⟨-1, 1, 0⟩, by simp, ?_, ?_, ⟨1, -1, 0⟩, ?_, ?_⟩
    · rw [mk_add_mk, mem_hull_iff]; omega
    · rw [mk_add_mk]; unfold T corner; simp only; omega
    · rw [axY (⟨x, y, z⟩ + ⟨-1, 1, 0⟩) (by simp only [Pt.add_x]; omega) (by simp only [Pt.add_y]; omega), inl_Y]; simp
    · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  · rw [axis_Y x y z hx hy, inl_Y]
    refine ⟨⟨1, -1, 0⟩, by simp, ?_, ?_, ⟨-1, 1, 0⟩, ?_, ?_⟩
    · rw [mk_add_mk, mem_hull_iff]; omega
    · rw [mk_add_mk]; unfold T corner; simp only; omega
    · rw [axX (⟨x, y, z⟩ + ⟨1, -1, 0⟩) (by simp only [Pt.add_x]; omega), inl_X]; simp
    · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
  · rw [axis_Z x y z hx hy, inl_Z]
    by_cases hc : y = 0 ∧ z = 1
    · refine ⟨⟨0, 1, -1⟩, by simp, ?_, ?_, ⟨0, -1, 1⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [axY (⟨x, y, z⟩ + ⟨0, 1, -1⟩) (by simp only [Pt.add_x]; omega) (by simp only [Pt.add_y]; omega), inl_Y]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega
    · refine ⟨⟨1, 0, -1⟩, by simp, ?_, ?_, ⟨-1, 0, 1⟩, ?_, ?_⟩
      · rw [mk_add_mk, mem_hull_iff]; omega
      · rw [mk_add_mk]; unfold T corner; simp only; omega
      · rw [axX (⟨x, y, z⟩ + ⟨1, 0, -1⟩) (by simp only [Pt.add_x]; omega), inl_X]; simp
      · apply Pt.ext' <;> simp only [Pt.add_x, Pt.add_y, Pt.add_z] <;> omega

/-! ### The coin rule as arithmetic -/

theorem canB_1_true (k : ℕ) : canB 2 1 k true = true ↔ k ≤ 5 := by
  simp [canB, List.range_succ, Gump.rule]; omega

theorem canB_1_false (k : ℕ) : canB 2 1 k false = true ↔ 1 ≤ k ∧ k ≤ 5 := by
  simp [canB, List.range_succ, Gump.rule]; omega

theorem canB_0_true (k : ℕ) : canB 2 0 k true = true ↔ 1 ≤ k ∧ k ≤ 5 := by
  simp [canB, List.range_succ, Gump.rule]; omega

theorem canB_0_false (k : ℕ) : canB 2 0 k false = true ↔ 2 ≤ k ∧ k ≤ 5 := by
  simp [canB, List.range_succ, Gump.rule]; omega

end Gump.Link.HullGen
