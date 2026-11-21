/-
The torus clause of Theorem 3 (`research/theory/thickness.md` section 2): on a torus slab of three or more
layers (and on a 3D torus) every component of a nonempty sealed set contains a non-contractible loop.

Stated on the universal cover. A set on a torus is the set `W` of its lifts, and the torus is the quotient map
`cls : Pt → α` (any map; it is used only through "the cells of `W` have finitely many classes"). A loop in the
torus set is non-contractible iff it lifts to a path from a cell `q` to a *different* lift `q'` of the same
torus cell (`q' = q + λ`, `λ` a nonzero period). So the clause reads: every component of `W` holds a path from
some `q` to some `q' ≠ q` with `cls q = cls q'`.

The paper's hypothesis "sealed on the torus" is taken here as "the lift is sealed in the infinite slab"; the
two agree when neighbours are counted with multiplicity (as the engines and `sealed.py` count them), since the
quotient map sends the twelve neighbours of a lift onto the twelve neighbours of its image.

Core Lean only: no Mathlib.
-/
import Gump.Thickness
import Gump.Symm

namespace Gump

theorem Reach.trans {W : Pt → Bool} {a b c : Pt} (h1 : Reach W a b) (h2 : Reach W b c) : Reach W a c := by
  induction h2 with
  | refl _ => exact h1
  | tail _ hr hW ih => exact Reach.tail ih hr hW

/-- On cells, reachability is symmetric (the neighbourhood is symmetric on cells, `Gump/Symm.lean`). -/
theorem Reach.symm {W : Pt → Bool} (hcell : ∀ p, W p = true → p.isCell = true) {a b : Pt}
    (h : Reach W a b) : Reach W b a := by
  induction h with
  | refl ha => exact Reach.refl ha
  | @tail q r hq hr hWr ih =>
    have hqr : q ∈ nbrs r := mem_nbrs_symm (hcell q hq.mem) hr
    exact Reach.trans (Reach.tail (Reach.refl hWr) hqr hq.mem) ih

/-- **An infinite component has two lifts of one class.** If the component of `p` in `W` is not contained in
any finite list, and the cells of `W` fall into finitely many classes, the component holds a path from some `q`
to some `q' ≠ q` of the same class. -/
theorem component_two_lifts {α : Type} (W : Pt → Bool) (hcell : ∀ p, W p = true → p.isCell = true)
    (p : Pt) (hinf : ¬ ∃ L : List Pt, ∀ q, Reach W p q → q ∈ L)
    (cls : Pt → α) (F : List α) (hF : ∀ q, W q = true → cls q ∈ F) :
    ∃ q q', Reach W p q ∧ Reach W q q' ∧ q ≠ q' ∧ cls q = cls q' := by
  classical
  apply Classical.byContradiction
  intro hno
  apply hinf
  refine ⟨F.filterMap (fun a => if h : ∃ q, Reach W p q ∧ cls q = a then some (Classical.choose h) else none), ?_⟩
  intro q hq
  rw [List.mem_filterMap]
  have hex : ∃ q', Reach W p q' ∧ cls q' = cls q := ⟨q, hq, rfl⟩
  refine ⟨cls q, hF q hq.mem, ?_⟩
  rw [dite_eq_left hex]
  have hspec := Classical.choose_spec hex
  congr 1
  apply Classical.byContradiction
  intro hne
  exact hno ⟨Classical.choose hex, q, hspec.1, Reach.trans (Reach.symm hcell hspec.1) hq, hne, hspec.2⟩

/-- **Theorem 3, torus slab clause.** In a slab of at least three layers, let `W` (the lift of a set on a torus
slab) be sealed in the slab, and let `cls` (the quotient map to the torus) take finitely many values on `W`.
Then every component of `W` holds a path from some `q` to a different lift `q'` of the same torus cell: the
component of the torus set contains a non-contractible loop. -/
theorem torus_slab_loop {α : Type} (d : Diag) (A B : Int) (h3 : ∃ s, s % 2 = 1 ∧ A ≤ s ∧ s + 4 ≤ B)
    (W : Pt → Bool) (hW : SealedIn (slab d A B) W) (hWV : ∀ p, W p = true → slab d A B p = true)
    (cls : Pt → α) (F : List α) (hF : ∀ q, W q = true → cls q ∈ F) (p : Pt) (hp : W p = true) :
    ∃ q q', Reach W p q ∧ Reach W q q' ∧ q ≠ q' ∧ cls q = cls q' := by
  have hcell : ∀ q, W q = true → q.isCell = true := by
    intro q hq
    have := hWV q hq
    simp only [slab, Bool.and_eq_true] at this; exact this.1
  exact component_two_lifts W hcell p (slab_component_infinite d A B h3 W hW hWV p hp) cls F hF

/-- **Theorem 3, 3D torus.** The same in the full lattice: if `W` (a set of cells, the lift of a set on a 3D
torus) is sealed and `cls` takes finitely many values on it, every component of `W` holds a non-contractible
loop. -/
theorem torus_loop {α : Type} (W : Pt → Bool) (hW : Sealed W) (hcell : ∀ p, W p = true → p.isCell = true)
    (cls : Pt → α) (F : List α) (hF : ∀ q, W q = true → cls q ∈ F) (p : Pt) (hp : W p = true) :
    ∃ q q', Reach W p q ∧ Reach W q q' ∧ q ≠ q' ∧ cls q = cls q' :=
  component_two_lifts W hcell p (sealed_component_infinite W hW p hp) cls F hF

end Gump
