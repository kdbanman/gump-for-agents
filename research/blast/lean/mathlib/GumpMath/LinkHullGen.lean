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
