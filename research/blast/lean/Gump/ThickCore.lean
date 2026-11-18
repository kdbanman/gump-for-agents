/-
The skeleton K of `research/theory/thickness.md` (Lemma 2) and the remark under T6 of `docs/AUTOMATON.md`:
the largest sealed subset of a set D exists; it is the **9-core** of D (the largest subset in which every point
has at least 9 of its 12 neighbours); its complement is the **bootstrap-percolation closure** (threshold 4) of
the complement of D; and for a history of gump, the largest dead sealed set K(t) only grows and stays dead.

Everything is stated for sets of points of ℤ³ with the neighbourhood `nbrs` of `Gump/Basic.lean`. For a set D
of cells, the points that are not cells play no role: no cell has a neighbour that is not a cell.

Core Lean only: no Mathlib.
-/
import Gump.Thickness

namespace Gump

/-! ## Sealed is the 9-core condition -/

/-- Each point has twelve neighbours, so at most three outside is at least nine inside. -/
theorem out_add_in (S : Pt → Bool) (p : Pt) :
    (nbrs p).countP (fun q => !S q) + (nbrs p).countP S = 12 := by
  have h := List.length_eq_countP_add_countP S (l := nbrs p)
  rw [nbrs_length] at h
  have : (nbrs p).countP (fun q => !S q) = (nbrs p).countP (fun a => decide ¬S a = true) := by
    apply List.countP_congr; intro q _; cases S q <;> simp
  omega

/-- **Sealed means: every point of the set has at least nine of its twelve neighbours in the set.** -/
theorem sealed_iff_nine (S : Pt → Bool) : Sealed S ↔ ∀ p, S p = true → 9 ≤ (nbrs p).countP S := by
  constructor
  · intro h p hp; have := h p hp; have := out_add_in S p; omega
  · intro h p hp; have := h p hp; have := out_add_in S p; omega

/-! ## The largest sealed subset -/

/-- `p` lies in some sealed subset of `D`. -/
def InCore (D : Pt → Bool) (p : Pt) : Prop :=
  ∃ S : Pt → Bool, Sealed S ∧ (∀ q, S q = true → D q = true) ∧ S p = true

/-- The largest sealed subset of `D`: the union of all sealed subsets of `D`. For `D` the dead cells at time
`t` this is the skeleton `K(t)`. -/
noncomputable def core (D : Pt → Bool) : Pt → Bool :=
  fun p => @decide (InCore D p) (Classical.propDecidable _)

theorem core_eq_true {D : Pt → Bool} {p : Pt} : core D p = true ↔ InCore D p := by
  simp [core]

theorem core_sub (D : Pt → Bool) : ∀ p, core D p = true → D p = true := by
  intro p hp
  obtain ⟨S, _, hSD, hSp⟩ := core_eq_true.1 hp
  exact hSD p hSp

/-- Every sealed subset of `D` lies in `core D`. -/
theorem core_largest (D S : Pt → Bool) (hS : Sealed S) (hSD : ∀ q, S q = true → D q = true) :
    ∀ p, S p = true → core D p = true :=
  fun _ hp => core_eq_true.2 ⟨S, hS, hSD, hp⟩

/-- `core D` is sealed (an arbitrary union of sealed sets is sealed). -/
theorem core_sealed (D : Pt → Bool) : Sealed (core D) := by
  intro p hp
  obtain ⟨S, hS, hSD, hSp⟩ := core_eq_true.1 hp
  refine Nat.le_trans ?_ (hS p hSp)
  apply List.countP_mono_left
  intro q _ hq
  cases hSq : S q with
  | false => rfl
  | true => rw [core_largest D S hS hSD q hSq] at hq; contradiction

/-- **The 9-core.** `core D` is the largest subset of `D` in which every point has at least nine neighbours:
it has the property, and every subset of `D` with the property lies in it. -/
theorem core_nine (D : Pt → Bool) :
    (∀ p, core D p = true → D p = true ∧ 9 ≤ (nbrs p).countP (core D)) ∧
    (∀ S : Pt → Bool, (∀ p, S p = true → D p = true) → (∀ p, S p = true → 9 ≤ (nbrs p).countP S) →
      ∀ p, S p = true → core D p = true) :=
  ⟨fun p hp => ⟨core_sub D p hp, (sealed_iff_nine _).1 (core_sealed D) p hp⟩,
   fun S hSD hS9 => core_largest D S ((sealed_iff_nine S).2 hS9) hSD⟩

/-! ## The complement of the core is a bootstrap-percolation closure -/

/-- `X` is closed under bootstrap percolation with threshold 4: a point with at least four neighbours in `X`
is in `X`. -/
def BPClosed (X : Pt → Bool) : Prop := ∀ p, 4 ≤ (nbrs p).countP X → X p = true

/-- The bootstrap-percolation closure of `A` (threshold 4): the points in every closed set containing `A`,
i.e. the least closed superset of `A` (the points reached when a point joins once four of its neighbours
have). -/
def BPClosure (A : Pt → Bool) (p : Pt) : Prop :=
  ∀ X : Pt → Bool, (∀ q, A q = true → X q = true) → BPClosed X → X p = true

/-- **The core is what bootstrap percolation never reaches.** A point is in the largest sealed subset of `D`
iff it is not in the threshold-4 bootstrap closure of the complement of `D`. -/
theorem core_iff_not_bp (D : Pt → Bool) (p : Pt) : core D p = true ↔ ¬ BPClosure (fun q => !D q) p := by
  constructor
  · intro hp hbp
    have hX := hbp (fun q => !core D q)
      (by
        intro q hq
        cases hc : core D q with
        | false => simp
        | true => have := core_sub D q hc; simp [this] at hq)
      (by
        intro q h4
        cases hc : core D q with
        | false => simp [hc]
        | true => have := core_sealed D q hc; have := out_add_in (core D) q; omega)
    simp [hp] at hX
  · intro hbp
    apply Classical.byContradiction
    intro hp
    apply hbp
    intro X hAX hX
    apply Classical.byContradiction
    intro hXp
    apply hp
    refine core_largest D (fun q => !X q) ?_ ?_ p (by simpa using hXp)
    · intro q hq
      apply Classical.byContradiction
      intro h4
      have := hX q (by
        have : (nbrs q).countP (fun r => !(fun r => !X r) r) = (nbrs q).countP X := by
          apply List.countP_congr; intro r _; simp
        omega)
      simp [this] at hq
    · intro q hq
      cases hD : D q with
      | true => rfl
      | false => have := hAX q (by simp [hD]); simp [this] at hq

/-! ## The skeleton of a history only grows -/

/-- The dead cells of a configuration. -/
def deadCells (c : Config) : Pt → Bool := fun p => p.isCell && !c p

/-- The skeleton `K(t)`: the largest sealed set of dead cells at time `t`. -/
noncomputable def skeleton (c : Config) (t : Nat) : Pt → Bool := core (deadCells (run c t))

/-- The skeleton is dead. -/
theorem skeleton_dead (c : Config) (t : Nat) : DeadOn (run c t) (skeleton c t) := by
  intro p hp
  have := core_sub _ p hp
  simp only [deadCells, Bool.and_eq_true, Bool.not_eq_true'] at this
  exact this.2

/-- **`K(t) ⊆ K(t+1)`.** -/
theorem skeleton_mono_step (c : Config) (t : Nat) :
    ∀ p, skeleton c t p = true → skeleton c (t + 1) p = true := by
  apply core_largest _ _ (core_sealed _)
  intro q hq
  have hcell : q.isCell = true := by
    have := core_sub _ q hq
    simp only [deadCells, Bool.and_eq_true] at this; exact this.1
  have hdead := (core_sealed _).step_dead (skeleton_dead c t) q hq
  simp [deadCells, hcell, run, hdead]

/-- **The skeleton only grows, and stays dead**: for `t ≤ t'`, `K(t) ⊆ K(t')`, and `K(t)` is dead at every
later time. -/
theorem skeleton_mono (c : Config) (t : Nat) : ∀ k p, skeleton c t p = true → skeleton c (t + k) p = true
  | 0, _, hp => hp
  | k + 1, p, hp => skeleton_mono_step c (t + k) p (skeleton_mono c t k p hp)

theorem skeleton_dead_later (c : Config) (t k : Nat) : ∀ p, skeleton c t p = true → run c (t + k) p = false :=
  fun p hp => skeleton_dead c (t + k) p (skeleton_mono c t k p hp)

/-- **In the full lattice a nonempty skeleton is infinite** (Theorem 3): if `K(t)` is contained in a finite
list, it is empty. -/
theorem skeleton_infinite (c : Config) (t : Nat) (L : List Pt) (hL : ∀ p, skeleton c t p = true → p ∈ L) :
    ∀ p, skeleton c t p = false := by
  intro p
  apply Classical.byContradiction
  intro hp
  exact not_sealed_of_finite _ L hL ⟨p, by simpa using hp⟩ (core_sealed _)

end Gump
