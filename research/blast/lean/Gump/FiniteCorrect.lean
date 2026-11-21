/-
The executable stepper of `Gump/Finite.lean` is correct: for every finite pattern,
`(stepFin live).config = step live.config`, and n applications of `stepFin` give `run`.
So what `gumpcheck` computes is `Gump.step` and `Gump.run`, the functions the theorems are about.

No hypothesis on the pattern is needed: a live point that is not a cell is never counted by a cell
(neighbours of cells are cells), and `step` kills it.

The argument: `stepFin` evaluates `step` on the candidate set (live points and their neighbours) and
keeps the points where it is true. A point outside the candidate set is dead and has no live
neighbour (the neighbourhood is symmetric on cells, `Gump/Symm.lean`), so `step` is false there.
The library facts used about `Std.HashSet` are `fold_eq_foldl_toList`, `mem_toList`, `mem_insert`,
`contains_iff_mem` and `not_mem_empty`.
-/
import Gump.Symm
import Gump.Finite

namespace Gump
open Std

/-- The candidate set of `stepFin`: live points and their neighbours. -/
def cand (live : Pattern) : Pattern :=
  live.fold (fun acc p => (nbrs p).foldl (fun a q => a.insert q) (acc.insert p)) {}

/-- `stepFin` is the filter of the candidate set by `step`. -/
theorem stepFin_eq (live : Pattern) :
    stepFin live = (cand live).fold (fun acc p => if step live.config p then acc.insert p else acc) {} :=
  rfl

theorem mem_foldl_insert (l : List Pt) (acc : Pattern) (x : Pt) :
    x ∈ l.foldl (fun a q => a.insert q) acc ↔ x ∈ acc ∨ x ∈ l := by
  induction l generalizing acc with
  | nil => simp
  | cons q l ih =>
    simp only [List.foldl_cons, ih, HashSet.mem_insert, beq_iff_eq, List.mem_cons]
    constructor
    · rintro ((rfl | h) | h) <;> simp_all
    · rintro (h | rfl | h) <;> simp_all

theorem mem_foldl_cand (l : List Pt) (acc : Pattern) (x : Pt) :
    x ∈ l.foldl (fun acc p => (nbrs p).foldl (fun a q => a.insert q) (acc.insert p)) acc ↔
      x ∈ acc ∨ ∃ p ∈ l, x = p ∨ x ∈ nbrs p := by
  induction l generalizing acc with
  | nil => simp
  | cons q l ih =>
    simp only [List.foldl_cons, ih, mem_foldl_insert, HashSet.mem_insert, beq_iff_eq, List.mem_cons]
    constructor
    · rintro (((rfl | h) | h) | ⟨p, hp, h⟩)
      · exact Or.inr ⟨_, Or.inl rfl, Or.inl rfl⟩
      · exact Or.inl h
      · exact Or.inr ⟨q, Or.inl rfl, Or.inr h⟩
      · exact Or.inr ⟨p, Or.inr hp, h⟩
    · rintro (h | ⟨p, rfl | hp, rfl | h⟩)
      · exact Or.inl (Or.inl (Or.inr h))
      · exact Or.inl (Or.inl (Or.inl rfl))
      · exact Or.inl (Or.inr h)
      · exact Or.inr ⟨_, hp, Or.inl rfl⟩
      · exact Or.inr ⟨p, hp, Or.inr h⟩

/-- **The candidate set** is exactly the live points and their neighbours. -/
theorem mem_cand (live : Pattern) (x : Pt) : x ∈ cand live ↔ ∃ p ∈ live, x = p ∨ x ∈ nbrs p := by
  rw [cand, HashSet.fold_eq_foldl_toList, mem_foldl_cand]
  simp [HashSet.mem_toList]

theorem mem_foldl_filter (c : Config) (l : List Pt) (acc : Pattern) (x : Pt) :
    x ∈ l.foldl (fun acc p => if step c p then acc.insert p else acc) acc ↔
      x ∈ acc ∨ (x ∈ l ∧ step c x = true) := by
  induction l generalizing acc with
  | nil => simp
  | cons q l ih =>
    simp only [List.foldl_cons, ih, List.mem_cons]
    split
    · rename_i hq
      simp only [HashSet.mem_insert, beq_iff_eq]
      constructor
      · rintro ((rfl | h) | ⟨h1, h2⟩)
        · exact Or.inr ⟨Or.inl rfl, hq⟩
        · exact Or.inl h
        · exact Or.inr ⟨Or.inr h1, h2⟩
      · rintro (h | ⟨rfl | h1, h2⟩)
        · exact Or.inl (Or.inr h)
        · exact Or.inl (Or.inl rfl)
        · exact Or.inr ⟨h1, h2⟩
    · rename_i hq
      constructor
      · rintro (h | ⟨h1, h2⟩)
        · exact Or.inl h
        · exact Or.inr ⟨Or.inr h1, h2⟩
      · rintro (h | ⟨rfl | h1, h2⟩)
        · exact Or.inl h
        · exact absurd h2 hq
        · exact Or.inr ⟨h1, h2⟩

/-- **The membership law of `stepFin`.** -/
theorem mem_stepFin (live : Pattern) (x : Pt) :
    x ∈ stepFin live ↔ x ∈ cand live ∧ step live.config x = true := by
  rw [stepFin_eq, HashSet.fold_eq_foldl_toList, mem_foldl_filter]
  simp [HashSet.mem_toList]

/-- **Nothing is born out of nothing.** If a point is alive one generation later, it was alive or it
is a neighbour of a live point. (A point alive after `step` is a cell; if it was dead it had four or
five live neighbours, and it is a neighbour of each of them by symmetry.) -/
theorem step_support (c : Config) (x : Pt) (h : step c x = true) :
    c x = true ∨ ∃ r, c r = true ∧ x ∈ nbrs r := by
  simp only [step, Bool.and_eq_true] at h
  obtain ⟨hcell, hrule⟩ := h
  cases hx : c x with
  | true => exact Or.inl rfl
  | false =>
    right
    rw [hx] at hrule
    have hpos : 0 < count c x := by
      simp [rule] at hrule; omega
    obtain ⟨r, hr, hcr⟩ := List.countP_pos_iff.mp hpos
    exact ⟨r, by simpa using hcr, mem_nbrs_symm hcell hr⟩

/-- **The stepper is correct.** For every finite pattern, the configuration of `stepFin live` is
`step` of the configuration of `live`. -/
theorem stepFin_config (live : Pattern) : (stepFin live).config = step live.config := by
  funext x
  apply Bool.eq_iff_iff.mpr
  simp only [Pattern.config, HashSet.contains_iff_mem]
  rw [mem_stepFin]
  constructor
  · exact fun h => h.2
  · intro h
    refine ⟨?_, h⟩
    rw [mem_cand]
    rcases step_support _ x h with hx | ⟨r, hr, hxr⟩
    · exact ⟨x, by simpa [Pattern.config] using hx, Or.inl rfl⟩
    · exact ⟨r, by simpa [Pattern.config] using hr, Or.inr hxr⟩

/-- n generations of the executable stepper. -/
def runFin (live : Pattern) : Nat → Pattern
  | 0 => live
  | n + 1 => stepFin (runFin live n)

/-- **The n-fold stepper is `run`.** -/
theorem runFin_config (live : Pattern) : ∀ n, (runFin live n).config = run live.config n
  | 0 => rfl
  | n + 1 => by rw [runFin, stepFin_config, runFin_config live n]; rfl

/-- The same with `Nat.repeat`, the form of a loop that applies `stepFin` n times. -/
theorem repeat_stepFin_config (live : Pattern) (n : Nat) :
    (Nat.repeat stepFin n live).config = run live.config n := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [Nat.repeat, stepFin_config, ih]; rfl

end Gump
