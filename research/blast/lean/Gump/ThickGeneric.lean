/-
Theorem 3 in a slab of three or more layers, along every generic in-plane direction: a nonempty set sealed in
the slab is unbounded along every in-plane direction `v` orthogonal to no offset. (`Gump/Thickness.lean` proves
"infinite" with one fixed direction per diagonal; this is the paper's proof for every generic `v`, and its
conclusion is sharper: the set reaches arbitrarily far in every generic in-plane direction.)

Genericity cannot be dropped entirely: a face of the slab (`slab_lower_sealed`) is bounded along `d`, which is
not in-plane; whether some in-plane non-generic direction admits a sealed set bounded along it is not settled
here.

Core Lean only: no Mathlib.
-/
import Gump.ThickHalf

namespace Gump

/-- The diagonal as a vector. -/
def Diag.vec (d : Diag) : Pt := ⟨sg d.sx 1, sg d.sy 1, sg d.sz 1⟩

/-- The representatives of the in-layer pairs `±o`. -/
def inReps (a : Axis) (d : Diag) : List Pt := (reps a).filter (fun r => d.dot r == 0)

theorem inLayer_perm (a : Axis) (d : Diag) :
    ((offsets a).filter (fun o => d.dot o == 0)).Perm (inReps a d ++ (inReps a d).map Pt.neg) := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

theorem inReps_length (a : Axis) (d : Diag) : (inReps a d).length = 3 := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

theorem inReps_sub (a : Axis) (d : Diag) : ∀ r ∈ inReps a d, r ∈ offsets a := by
  obtain ⟨sx, sy, sz⟩ := d
  cases a <;> cases sx <;> cases sy <;> cases sz <;> decide

/-- Exactly three of the six in-layer offsets point forward along a direction orthogonal to none of them. -/
theorem inLayer_fwd (a : Axis) (d : Diag) (v : Pt) (hv : ∀ o ∈ offsets a, dotv v o ≠ 0) :
    (offsets a).countP (fun o => d.dot o == 0 && decide (1 ≤ dotv v o)) = 3 := by
  have e0 : (offsets a).countP (fun o => d.dot o == 0 && decide (1 ≤ dotv v o)) =
      ((offsets a).filter (fun o => d.dot o == 0)).countP (fun o => decide (1 ≤ dotv v o)) := by
    rw [List.countP_filter]
    apply List.countP_congr; intro o _; simp [Bool.and_comm]
  rw [e0, List.Perm.countP_eq _ (inLayer_perm a d), List.countP_append, List.countP_map,
    countP_or _ _ _ (by
      intro x _ h1 h2
      simp only [Function.comp, decide_eq_true_eq, dotv_neg] at h1 h2
      omega), ← inReps_length a d, List.countP_eq_length]
  intro r hr
  have := hv r (inReps_sub a d r hr)
  simp only [Function.comp, Bool.or_eq_true, decide_eq_true_eq, dotv_neg]
  omega

/-- One layer up or down: of the two offsets at `Δs = +2` and their negatives, at least one points forward. -/
theorem side_fwd (a : Axis) (d : Diag) (v : Pt)
    (hv : ∀ o ∈ offsets a, (d.dot o = 2 ∨ d.dot o = -2) → dotv v o ≠ 0) :
    1 ≤ (offsets a).countP (fun o => decide ((d.dot o = 2 ∨ d.dot o = -2) ∧ 1 ≤ dotv v o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  obtain ⟨x, y, z⟩ := v
  cases a <;> cases sx <;> cases sy <;> cases sz <;>
    simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hv <;>
    simp only [offsets, List.countP_cons, List.countP_nil, Diag.dot, sg, dotv] at hv ⊢ <;>
    simp (config := { decide := true }) only [decide_eq_true_eq, ↓reduceIte, Int.reduceNeg, true_and,
      and_true, false_and, true_implies, false_implies, Nat.zero_add, Nat.add_zero] at hv ⊢ <;>
    split <;> split <;> omega

/-- Two layers up (the bottom of the slab): of the offsets at `Δs = +2, +2, +4`, at least one points forward
along an in-plane direction orthogonal to none of them (the identity `e + 2(a + b) = 4d`). -/
theorem up_fwd (a : Axis) (d : Diag) (v : Pt) (hvd : dotv v d.vec = 0)
    (hv : ∀ o ∈ offsets a, 0 < d.dot o → dotv v o ≠ 0) :
    1 ≤ (offsets a).countP (fun o => decide (0 < d.dot o ∧ 1 ≤ dotv v o)) := by
  obtain ⟨sx, sy, sz⟩ := d
  obtain ⟨x, y, z⟩ := v
  cases a <;> cases sx <;> cases sy <;> cases sz <;>
    simp only [offsets, List.mem_cons, List.not_mem_nil, or_false, forall_eq_or_imp, forall_eq] at hv <;>
    simp only [offsets, List.countP_cons, List.countP_nil, Diag.dot, Diag.vec, sg, dotv] at hv hvd ⊢ <;>
    simp (config := { decide := true }) only [decide_eq_true_eq, ↓reduceIte,
      Int.reduceNeg, true_and, and_true, false_and, true_implies, false_implies,
      Nat.zero_add, Nat.add_zero] at hv hvd ⊢ <;>
    split <;> split <;> split <;> omega

theorem Diag.vec_neg (d : Diag) : d.neg.vec = d.vec.neg := by
  obtain ⟨a, b, c⟩ := d
  cases a <;> cases b <;> cases c <;> rfl

/-- **Theorem 3, slab, along every generic in-plane direction.** In a slab of at least three layers, a nonempty
set sealed in the slab reaches beyond every bound `M` along every in-plane direction `v` (`v·d = 0`) that is
orthogonal to none of the 36 offsets. -/
theorem slab_sealed_unbounded (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B)
    (S : Pt → Bool) (hSV : ∀ p, S p = true → slab d A B p = true) (hS : SealedIn (slab d A B) S)
    (hne : ∃ p, S p = true) (v : Pt) (hvd : dotv v d.vec = 0) (hv : ∀ a, ∀ o ∈ offsets a, dotv v o ≠ 0)
    (M : Int) : ∃ p, S p = true ∧ M < dotv v p := by
  apply Classical.byContradiction
  intro hno
  have hb : ∀ p, S p = true → dotv v p ≤ M := fun p hp => by
    apply Classical.byContradiction; intro h; exact hno ⟨p, hp, by omega⟩
  obtain ⟨p₀, hp₀⟩ := hne
  obtain ⟨p, hp, hmax⟩ := exists_max_of_bdd S (dotv v) M hb _ p₀ hp₀ (Nat.le_refl _)
  have hpV := hSV p hp
  simp only [slab, Bool.and_eq_true, decide_eq_true_eq] at hpV
  obtain ⟨hcell, hA, hB⟩ := hpV
  have hodd := dot_odd d p hcell
  obtain ⟨s, hs, hAs, hsB⟩ := h3
  have h3' := hS p hp
  -- forward neighbours inside a window of layers are in the slab and outside `S`
  have key : ∀ (W : Pt → Bool),
      (∀ o ∈ offsets p.axis, W o = true → A ≤ d.dot p + d.dot o ∧ d.dot p + d.dot o ≤ B) →
      (offsets p.axis).countP (fun o => W o && decide (1 ≤ dotv v o)) ≤
        (nbrs p).countP (fun q => slab d A B q && !S q) := by
    intro W hW
    unfold nbrs
    rw [List.countP_map]
    apply List.countP_mono_left
    intro o ho hWo
    simp only [Bool.and_eq_true, decide_eq_true_eq] at hWo
    simp only [Function.comp, Bool.and_eq_true]
    have hq : (p + o).isCell = true := nbrs_isCell p hcell (p + o) (List.mem_map.2 ⟨o, ho, rfl⟩)
    have hl := hW o ho hWo.1
    refine ⟨?_, ?_⟩
    · simp only [slab, hq, Diag.dot_add, Bool.true_and, decide_eq_true_eq]; exact hl
    · cases hSq : S (p + o) with
      | false => rfl
      | true => have := hmax _ hSq; rw [dotv_add] at this; have := hWo.2; omega
  have hin := inLayer_fwd p.axis d v (hv p.axis)
  by_cases hbot : d.dot p - 2 < A
  · -- bottom layer: in-layer and up
    have hup : d.dot p + 4 ≤ B := by omega
    have hu := up_fwd p.axis d v hvd (fun o ho _ => hv p.axis o ho)
    have := countP_add_le (offsets p.axis) (fun o => d.dot o == 0 && decide (1 ≤ dotv v o))
      (fun o => decide (0 < d.dot o ∧ 1 ≤ dotv v o))
      (fun o => decide (0 ≤ d.dot o) && decide (1 ≤ dotv v o))
      (by intro x _ h; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h ⊢; omega)
      (by intro x _ h; simp only [Bool.and_eq_true, decide_eq_true_eq] at h ⊢; omega)
      (by intro x _ h1 h2; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h1 h2; omega)
    have := key (fun o => decide (0 ≤ d.dot o)) (by
      intro o hmem ho
      simp only [decide_eq_true_eq] at ho
      have := dot_offset_le_four p.axis d o hmem
      omega)
    omega
  · by_cases htop : B < d.dot p + 2
    · -- top layer: in-layer and down (`up_fwd` for the opposite diagonal)
      have hdown : A ≤ d.dot p - 4 := by omega
      have hu := up_fwd p.axis d.neg v (by rw [Diag.vec_neg, dotv_neg, hvd]; rfl)
        (fun o ho _ => hv p.axis o ho)
      have e : (offsets p.axis).countP (fun o => decide (0 < d.neg.dot o ∧ 1 ≤ dotv v o)) =
          (offsets p.axis).countP (fun o => decide (d.dot o < 0 ∧ 1 ≤ dotv v o)) := by
        apply List.countP_congr; intro o _; simp only [decide_eq_true_eq, Diag.neg_dot]; omega
      rw [e] at hu
      have := countP_add_le (offsets p.axis) (fun o => d.dot o == 0 && decide (1 ≤ dotv v o))
        (fun o => decide (d.dot o < 0 ∧ 1 ≤ dotv v o))
        (fun o => decide (d.dot o ≤ 0) && decide (1 ≤ dotv v o))
        (by intro x _ h; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h ⊢; omega)
        (by intro x _ h; simp only [Bool.and_eq_true, decide_eq_true_eq] at h ⊢; omega)
        (by intro x _ h1 h2; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h1 h2; omega)
      have := key (fun o => decide (d.dot o ≤ 0)) (by
        intro o hmem ho
        simp only [decide_eq_true_eq] at ho
        have := dot_offset_ge_neg_four p.axis d o hmem
        omega)
      omega
    · -- interior layer: in-layer and one of the four at `Δs = ±2`
      have hu := side_fwd p.axis d v (fun o ho _ => hv p.axis o ho)
      have := countP_add_le (offsets p.axis) (fun o => d.dot o == 0 && decide (1 ≤ dotv v o))
        (fun o => decide ((d.dot o = 2 ∨ d.dot o = -2) ∧ 1 ≤ dotv v o))
        (fun o => decide (-2 ≤ d.dot o ∧ d.dot o ≤ 2) && decide (1 ≤ dotv v o))
        (by intro x _ h; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h ⊢; omega)
        (by intro x _ h; simp only [Bool.and_eq_true, decide_eq_true_eq] at h ⊢; omega)
        (by intro x _ h1 h2; simp only [Bool.and_eq_true, beq_iff_eq, decide_eq_true_eq] at h1 h2; omega)
      have := key (fun o => decide (-2 ≤ d.dot o ∧ d.dot o ≤ 2)) (by
        intro o _ ho
        simp only [decide_eq_true_eq] at ho
        omega)
      omega

end Gump
